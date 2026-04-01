#!/usr/bin/env python3
"""Graph-memory scars: local persistent records on the substrate.

When amplitude traverses a mass edge, a local bit is written on that
edge: "this interaction channel was activated." The scar lives on the
graph substrate, not in a global env label.

The env state is the SET of scarred edges. Two paths that traverse
different mass edges produce different scar sets. The detector
probability is computed after tracing over the scar configuration:

  P(det) = Σ_{scar_set} |ψ(det, scar_set)|²

Key difference from previous architectures:
- NOT a single label (last node, angle bin)
- NOT a compressed hash (cumulative, distributed record)
- The scar set grows with the number of mass edges traversed
- Each path creates a UNIQUE scar set (its exact mass-edge trajectory)
- Scar sets are SUBSETS, not SEQUENCES — order doesn't matter

This should give high env entropy because different paths through
the mass region traverse different edge subsets.

Uses the promoted angle² β=0.8 propagator.

PStack experiment: graph-memory-scar-decoherence
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import build_post_barrier_setup, compute_detector_metrics

BETA = 0.8


def propagate_with_scars(positions, adj, field, src, det, k,
                         mass_set, blocked=None, max_scar_size=3):
    """Angle-weighted propagator with graph-memory scars.

    State: (node, frozenset_of_scarred_edges) → amplitude
    When amplitude crosses edge (i,j) touching mass, that edge is
    added to the scar set. The scar set is capped at max_scar_size
    most recent edges to keep state space bounded.

    To cap: when scar set exceeds max_scar_size, keep only the
    max_scar_size edges closest to the current position (by layer).
    Simplified: keep the last max_scar_size edges added.
    """
    n = len(positions)
    blocked = blocked or set()

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

    # State: (node, scar_tuple) → amplitude
    # scar_tuple = tuple of scarred edge indices, bounded
    state = {}
    for s in src:
        state[(s, ())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {scar: amp for (node, scar), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for scar, amp in entries.items():
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx = x2-x1
                dy = y2-y1
                L = math.sqrt(dx*dx+dy*dy)
                if L < 1e-10:
                    continue
                lf = 0.5*(field[i]+field[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA*theta*theta)
                ea = cmath.exp(1j*k*act) * w / (L**1.0)

                # Scar: if edge touches mass, add edge ID to scar set
                if i in mass_set or j in mass_set:
                    edge_id = (min(i,j), max(i,j))  # canonical edge ID
                    # Add to scar, cap size
                    if edge_id not in scar:
                        new_scar = (scar + (edge_id,))[-max_scar_size:]
                    else:
                        new_scar = scar
                else:
                    new_scar = scar

                key = (j, new_scar)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    det_state = {(d, scar): amp for (d, scar), amp in state.items()
                 if d in det}
    return det_state


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("GRAPH-MEMORY SCAR DECOHERENCE")
    print(f"  Propagator: 1/L^p × exp(-{BETA}×θ²)")
    print(f"  Scar: set of mass edges traversed (max 3)")
    print(f"  P(det) = Σ_scar |ψ(det, scar)|²")
    print("=" * 70)
    print()

    # ================================================================
    # Test 1: Purity vs graph size
    # ================================================================
    print("TEST 1: Purity vs graph size")
    print()
    print(f"  {'N':>4s}  {'n_mass':>6s}  {'n_scar':>6s}  "
          f"{'pur_scar':>8s}  {'pur_node':>8s}  {'scar_off':>8s}")
    print(f"  {'-' * 48}")

    for nl in [8, 12, 18]:
        ps_list, pn_list, p0_list = [], [], []
        n_mass_count = 0
        max_scars = 0

        for seed in range(3):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]
            n_mass_count = len(mass_set)

            for k in k_band:
                # Scar env
                ds_s = propagate_with_scars(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, mass_set, setup["blocked"], max_scar_size=6)
                ps, _, _, _ = compute_detector_metrics(ds_s, setup["det_list"])
                if not math.isnan(ps):
                    ps_list.append(ps)
                scars = set(scar for (d, scar) in ds_s.keys())
                max_scars = max(max_scars, len(scars))

                # Node-label env (comparison)
                n = len(positions)
                in_deg = [0]*n
                for i, nbs in adj.items():
                    for j in nbs: in_deg[j] += 1
                q = deque(i for i in range(n) if in_deg[i] == 0)
                order = []
                while q:
                    i = q.popleft(); order.append(i)
                    for j in adj.get(i, []):
                        in_deg[j] -= 1
                        if in_deg[j] == 0: q.append(j)

                state_n = {}
                for s in setup["src"]:
                    state_n[(s, -1)] = 1.0/len(setup["src"]) + 0.0j
                processed = set()
                for i in order:
                    if i in processed: continue
                    processed.add(i)
                    entries = {env: amp for (node, env), amp in list(state_n.items())
                               if node == i and abs(amp) > 1e-30}
                    if not entries or i in setup["blocked"]: continue
                    for env, amp in entries.items():
                        new_env = i if i in mass_set else env
                        for j in adj.get(i, []):
                            if j in setup["blocked"]: continue
                            x1,y1=positions[i]; x2,y2=positions[j]
                            dx=x2-x1; dy=y2-y1
                            L=math.sqrt(dx*dx+dy*dy)
                            if L < 1e-10: continue
                            lf=0.5*(setup["field"][i]+setup["field"][j])
                            dl=L*(1+lf); ret=math.sqrt(max(dl*dl-L*L,0)); act=dl-ret
                            theta_e=math.atan2(abs(dy), max(dx, 1e-10))
                            w=math.exp(-BETA*theta_e*theta_e)
                            ea=cmath.exp(1j*k*act)*w/(L**1.0)
                            key=(j, new_env)
                            if key not in state_n: state_n[key]=0.0+0.0j
                            state_n[key] += amp*ea
                ds_n = {(d, env): amp for (d, env), amp in state_n.items()
                        if d in setup["det"]}
                pn, _, _, _ = compute_detector_metrics(ds_n, setup["det_list"])
                if not math.isnan(pn):
                    pn_list.append(pn)

                # Scars OFF (unitary baseline)
                ds_0 = propagate_with_scars(
                    positions, adj, setup["field"], setup["src"], setup["det"],
                    k, set(), setup["blocked"], max_scar_size=6)  # empty mass_set
                p0, _, _, _ = compute_detector_metrics(ds_0, setup["det_list"])
                if not math.isnan(p0):
                    p0_list.append(p0)

        if ps_list:
            print(f"  {nl:4d}  {n_mass_count:6d}  {max_scars:6d}  "
                  f"{sum(ps_list)/len(ps_list):8.4f}  "
                  f"{sum(pn_list)/len(pn_list):8.4f}  "
                  f"{sum(p0_list)/len(p0_list):8.4f}")

    print()
    print("pur_scar = scar env (this test)")
    print("pur_node = node-label env (comparison)")
    print("scar_off = scars disabled (should be ~1.0, unitary baseline)")
    print()
    print("PASS: pur_scar does not rise with N")
    print("FAIL: pur_scar rises with N (same as node-label)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
