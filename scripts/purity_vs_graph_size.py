#!/usr/bin/env python3
"""Does purity decrease with graph size?

If purity → 0 as n_layers grows: decoherence becomes complete.
If purity → constant > 0: decoherence saturates.

Sweep n_layers from 8 to 30, measure mean purity.

PStack experiment: purity-vs-graph-size
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
from scripts.density_matrix_analysis import propagate_two_register_full, compute_purity


def main():
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("PURITY vs GRAPH SIZE")
    print(f"  Does decoherence increase with more layers?")
    print("=" * 70)
    print()

    print(f"  {'n_layers':>8s}  {'n_nodes':>7s}  {'mean_pur':>8s}  {'min_pur':>8s}  {'max_pur':>8s}  {'n_valid':>7s}")
    print(f"  {'-' * 52}")

    for n_layers in [6, 8, 10, 12, 15, 18, 20, 25]:
        purities = []

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

            seed_purities = []
            for k in k_band:
                det_state = propagate_two_register_full(
                    positions, adj, field, src, det, k, mass_set, blocked)
                purity, _, _ = compute_purity(det_state, det_list)
                seed_purities.append(purity)

            purities.append(sum(seed_purities)/len(seed_purities))

        if purities:
            mean_p = sum(purities)/len(purities)
            min_p = min(purities)
            max_p = max(purities)
            # Estimate n_nodes
            positions, _, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=7,
            )
            print(f"  {n_layers:8d}  {len(positions):7d}  {mean_p:8.4f}  {min_p:8.4f}  {max_p:8.4f}  {len(purities):7d}")

    print()
    print("If mean_purity decreases with n_layers: decoherence grows with graph size")
    print("If mean_purity is constant: decoherence saturates")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
