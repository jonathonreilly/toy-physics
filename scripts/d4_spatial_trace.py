#!/usr/bin/env python3
"""D4: Spatial trace — erase mass-region information entirely.

Instead of labeling paths through mass, trace out the mass region.
1. Propagate from source through slits to mass-region entry nodes
2. For each entry node, propagate through mass to exit nodes
3. The mass region's internal state is traced out at exit
4. Continue propagation from exit nodes to detector

The partial trace at the mass exit boundary means:
P(det) = Σ_exit |Σ_entry T(exit,entry) × ψ(entry)|²

If different slits create different distributions across entry nodes,
the trace produces decoherence. On larger graphs, the mass region has
MORE internal degrees of freedom → more complete trace.

Pass criterion: purity should NOT increase from N=12 to N=25.

PStack experiment: d4-spatial-trace
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import (
    build_post_barrier_setup, compute_detector_metrics,
)
from scripts.two_register_decoherence import compute_field


def propagate_with_spatial_trace(positions, adj, field, src, det, k,
                                 mass_set, blocked=None):
    """Propagator with spatial trace over mass region.

    Amplitude propagates coherently EXCEPT: at the mass-region exit
    boundary, we trace over which mass-exit node the amplitude came from.

    This means: for each mass-exit node, we compute the probability
    independently, then sum probabilities (not amplitudes).
    """
    n = len(positions)
    blocked = blocked or set()

    # Identify mass-exit nodes: mass nodes with edges to non-mass nodes
    mass_exit = set()
    for m in mass_set:
        for j in adj.get(m, []):
            if j not in mass_set and j not in blocked:
                mass_exit.add(m)
                break

    if not mass_exit:
        # No exit nodes — fall back to coherent propagation
        mass_exit = mass_set

    in_deg = [0]*n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    # Phase 1: propagate coherently, tracking which mass-exit node
    # amplitude last passed through (env = last mass-exit node)
    state = {}
    for s in src:
        state[(s, -1)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env: amp for (node, env), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env, amp in entries.items():
            # Update env at mass-exit nodes
            new_env = i if i in mass_exit else env

            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                L = math.sqrt((x2-x1)**2+(y2-y1)**2)
                if L < 1e-10:
                    continue
                lf = 0.5*(field[i]+field[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                ea = cmath.exp(1j*k*act)/(L**1.0)
                key = (j, new_env)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    # Phase 2: spatial trace — sum probabilities over exit-node labels
    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("D4: SPATIAL TRACE OVER MASS REGION")
    print("  Trace out mass-exit-node information at boundary")
    print("=" * 70)
    print()

    print(f"  {'N_layers':>8s}  {'pur_fine':>8s}  {'pur_d4':>8s}  {'n_exits':>7s}")
    print(f"  {'-' * 38}")

    for nl in [8, 10, 12, 15, 20, 25]:
        pur_fine, pur_d4 = [], []
        max_exits = 0

        for seed in range(6):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            scaled_depth = max(1, round(nl/6))
            setup = build_post_barrier_setup(positions, adj,
                                              env_depth_layers=scaled_depth)
            if setup is None:
                continue

            pf_k, pd_k = [], []
            for k in k_band:
                from scripts.density_matrix_analysis import propagate_two_register_full
                ds_f = propagate_two_register_full(
                    positions, adj, setup["field"], setup["src"], setup["det"], k,
                    setup["mass_set"], setup["blocked"])
                pf, _, _, _ = compute_detector_metrics(ds_f, setup["det_list"])
                if not math.isnan(pf):
                    pf_k.append(pf)

                ds_d = propagate_with_spatial_trace(
                    positions, adj, setup["field"], setup["src"], setup["det"], k,
                    setup["mass_set"], setup["blocked"])
                pd, _, _, _ = compute_detector_metrics(ds_d, setup["det_list"])
                if not math.isnan(pd):
                    pd_k.append(pd)

                exits = set(env for (d, env) in ds_d.keys() if env >= 0)
                max_exits = max(max_exits, len(exits))

            if pf_k:
                pur_fine.append(sum(pf_k)/len(pf_k))
            if pd_k:
                pur_d4.append(sum(pd_k)/len(pd_k))

        if pur_fine and pur_d4:
            print(f"  {nl:8d}  {sum(pur_fine)/len(pur_fine):8.4f}  "
                  f"{sum(pur_d4)/len(pur_d4):8.4f}  {max_exits:7d}")

    print()
    print("PASS: pur_d4 at N=25 <= pur_d4 at N=12")
    print("FAIL: pur_d4 increases with N")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
