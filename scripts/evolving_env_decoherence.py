#!/usr/bin/env python3
"""Evolving environment: env state propagates between mass interactions.

The scaling problem: passive env labels (node-label, cumulative) become
shared as graphs grow. Fix: give the env its own dynamics.

Between mass nodes, the env state picks up phase from the local graph
structure. Different paths between mass nodes → different env phases →
env states become more orthogonal on larger graphs.

Implementation: env is a complex phase that evolves along the path.
At each edge, env_phase += edge_action * coupling_strength.
At mass nodes, the env is "measured" (binned into discrete labels).
Between mass nodes, the env evolves freely (continuous phase).

The partial trace bins by the final env phase.

PStack experiment: evolving-env-decoherence
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.two_register_decoherence import compute_field
from scripts.density_matrix_analysis import compute_purity


def propagate_evolving_env(positions, adj, field, src, det, k, mass_set,
                           blocked=None, env_coupling=0.5, n_bins=12):
    """Two-register with evolving environment phase.

    The env accumulates phase at EVERY edge (not just mass edges).
    At mass edges, the coupling is stronger (env_coupling).
    At non-mass edges, the coupling is weaker (env_coupling * 0.1).
    The env phase is binned at the detector for the partial trace.
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

    # State: (node, env_phase_bin) → amplitude
    state = {}
    for s in src:
        state[(s, 0)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env_bin: amp for (node, env_bin), amp in list(state.items())
                   if node == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue

        for env_bin, amp in entries.items():
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

                # Env phase evolution: stronger at mass, weaker elsewhere
                if i in mass_set or j in mass_set:
                    env_delta = act * env_coupling
                else:
                    env_delta = act * env_coupling * 0.1

                # Convert continuous env phase to bin
                new_phase = (env_bin * 2 * math.pi / n_bins) + env_delta
                new_bin = int((new_phase % (2 * math.pi)) * n_bins / (2 * math.pi))

                key = (j, new_bin)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def main():
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("EVOLVING ENVIRONMENT: purity vs graph size")
    print(f"  env accumulates phase at every edge")
    print(f"  stronger coupling at mass, weaker elsewhere")
    print("=" * 70)
    print()

    for coupling in [0.1, 0.5, 1.0]:
        print(f"  env_coupling = {coupling}:")
        print(f"    {'n_layers':>8s}  {'pur_node':>8s}  {'pur_evol':>8s}  {'n_valid':>7s}")
        print(f"    {'-' * 36}")

        for n_layers in [6, 8, 10, 12, 15, 20, 25]:
            pur_node_list = []
            pur_evol_list = []

            for seed in range(n_seeds):
                positions, adj, _ = generate_causal_dag(
                    n_layers=n_layers, nodes_per_layer=npl,
                    y_range=y_range, connect_radius=radius,
                    rng_seed=seed*11+7,
                )
                n = len(positions)
                by_layer = defaultdict(list)
                for idx, (x, y) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 5:
                    continue

                src = by_layer[layers[0]]
                det = set(by_layer[layers[-1]])
                det_list = list(det)
                if not det:
                    continue

                all_ys = [y for _, y in positions]
                cy = sum(all_ys)/len(all_ys)

                bl_idx = len(layers)//3
                bl = layers[bl_idx]
                bi = by_layer[bl]
                sa = [i for i in bi if positions[i][1] > cy+3][:3]
                sb = [i for i in bi if positions[i][1] < cy-3][:3]
                if not sa or not sb:
                    continue
                si = set(sa+sb)
                blocked = set(bi) - si

                post_bl = layers[bl_idx+1]
                mass_nodes = [i for i in by_layer[post_bl] if abs(positions[i][1]-cy) <= 3]
                if len(mass_nodes) < 2:
                    continue
                mass_set = set(mass_nodes)

                grav_layer = layers[2*len(layers)//3]
                grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy+1]
                full_mass = mass_set | set(grav_mass)
                field = compute_field(positions, adj, list(full_mass))

                from scripts.density_matrix_analysis import propagate_two_register_full
                node_purs = []
                evol_purs = []

                for k_val in k_band:
                    ds_node = propagate_two_register_full(
                        positions, adj, field, src, det, k_val, mass_set, blocked)
                    p_node, _, _ = compute_purity(ds_node, det_list)
                    node_purs.append(p_node)

                    ds_evol = propagate_evolving_env(
                        positions, adj, field, src, det, k_val, mass_set,
                        blocked, coupling, n_bins=12)
                    p_evol, _, _ = compute_purity(ds_evol, det_list)
                    evol_purs.append(p_evol)

                pur_node_list.append(sum(node_purs)/len(node_purs))
                pur_evol_list.append(sum(evol_purs)/len(evol_purs))

            if pur_node_list:
                mn = sum(pur_node_list)/len(pur_node_list)
                me = sum(pur_evol_list)/len(pur_evol_list)
                print(f"    {n_layers:8d}  {mn:8.4f}  {me:8.4f}  {len(pur_node_list):7d}")

        # Check trend
        print()

    print("If pur_evol DECREASES with n_layers: evolving env fixes scaling")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
