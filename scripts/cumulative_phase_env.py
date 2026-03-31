#!/usr/bin/env python3
"""Cumulative phase environment: env grows with mass interactions.

The discrete node-label env weakens with graph size because both slits
reach all mass nodes. Fix: env = binned cumulative action through mass.

Each path accumulates action_at_mass = Σ S(edge) for edges at mass nodes.
Paths from different slits accumulate different total action (different
routes through mass) → different binned env labels → decoherence.

Key property: more mass interactions → more diverse cumulative action
→ MORE slit-discriminating → decoherence should INCREASE with graph size.

PStack experiment: cumulative-phase-env
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


def propagate_cumulative_env(positions, adj, field, src, det, k, mass_set,
                             blocked=None, n_bins=8):
    """Two-register with cumulative action environment.

    env = binned cumulative action through mass nodes.
    Each time a path crosses a mass node edge, the cumulative action grows.
    The env label = floor(cumulative_action * n_bins / max_expected_action).
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

    # State: (node, env_bin) → amplitude
    # env_bin is an integer representing binned cumulative action at mass
    state = {}
    for s in src:
        state[(s, 0)] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {env: amp for (node, env), amp in list(state.items())
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

                # Cumulative env: if this edge touches mass, increment bin
                if i in mass_set or j in mass_set:
                    # Action at this mass edge contributes to env
                    # Bin by quantizing the action contribution
                    action_contrib = act  # could also use field strength
                    new_bin = env_bin + int(action_contrib * n_bins) % n_bins + 1
                else:
                    new_bin = env_bin

                key = (j, new_bin)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    # Partial trace
    det_state = {(d, env): amp for (d, env), amp in state.items() if d in det}
    return det_state


def main():
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("CUMULATIVE PHASE ENVIRONMENT: purity vs graph size")
    print(f"  env = binned cumulative action through mass")
    print("=" * 70)
    print()

    print(f"  {'n_layers':>8s}  {'n_nodes':>7s}  {'pur_node':>8s}  {'pur_cum':>8s}  {'n_valid':>7s}")
    print(f"  {'-' * 44}")

    for n_layers in [6, 8, 10, 12, 15, 18, 20, 25]:
        pur_node_list = []
        pur_cum_list = []

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

            # Node-label env (original)
            from scripts.density_matrix_analysis import propagate_two_register_full
            node_purs = []
            cum_purs = []

            for k in k_band:
                # Node-label
                ds_node = propagate_two_register_full(
                    positions, adj, field, src, det, k, mass_set, blocked)
                p_node, _, _ = compute_purity(ds_node, det_list)
                node_purs.append(p_node)

                # Cumulative
                ds_cum = propagate_cumulative_env(
                    positions, adj, field, src, det, k, mass_set, blocked, n_bins=8)
                p_cum, _, _ = compute_purity(ds_cum, det_list)
                cum_purs.append(p_cum)

            pur_node_list.append(sum(node_purs)/len(node_purs))
            pur_cum_list.append(sum(cum_purs)/len(cum_purs))

        if pur_node_list:
            mn = sum(pur_node_list)/len(pur_node_list)
            mc = sum(pur_cum_list)/len(pur_cum_list)
            positions, _, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius, rng_seed=7)
            print(f"  {n_layers:8d}  {len(positions):7d}  {mn:8.4f}  {mc:8.4f}  {len(pur_node_list):7d}")

    print()
    print("pur_node = node-label env (original)")
    print("pur_cum = cumulative action env (new)")
    print()
    print("If pur_cum decreases with n_layers: cumulative env fixes the scaling")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
