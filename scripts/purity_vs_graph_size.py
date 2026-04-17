#!/usr/bin/env python3
"""Does detector-state purity decrease with graph size?

If purity → 0 as n_layers grows: decoherence becomes complete.
If purity → constant > 0: decoherence saturates.

Sweep n_layers while comparing:
  1. fixed one-layer environment region
  2. depth-scaled environment region

This separates graph growth from simple environment dilution.

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
from scripts.density_matrix_analysis import (
    propagate_two_register_full,
    build_post_barrier_setup,
    compute_detector_metrics,
)


def main():
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("PURITY vs GRAPH SIZE")
    print("  detector-state purity with fixed vs depth-scaled env region")
    print("=" * 70)
    print()

    print(
        f"  {'n_layers':>8s}  {'n_nodes':>7s}  {'depth':>5s}  "
        f"{'pur_fix':>8s}  {'hit_fix':>8s}  {'pur_scl':>8s}  {'hit_scl':>8s}  {'n_valid':>7s}"
    )
    print(f"  {'-' * 79}")

    for n_layers in [6, 8, 10, 12, 15, 18, 20, 25]:
        pur_fixed = []
        hit_fixed = []
        pur_scaled = []
        hit_scaled = []
        scaled_depth = max(1, round(n_layers / 6))

        for seed in range(n_seeds):
            positions, adj, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=seed*11+7,
            )
            fixed = build_post_barrier_setup(positions, adj, env_depth_layers=1)
            scaled = build_post_barrier_setup(positions, adj, env_depth_layers=scaled_depth)
            if fixed is None or scaled is None:
                continue

            seed_fix_p = []
            seed_fix_hit = []
            for k in k_band:
                det_state = propagate_two_register_full(
                    positions, adj, fixed["field"], fixed["src"], fixed["det"], k,
                    fixed["mass_set"], fixed["blocked"])
                purity, _, _, det_prob = compute_detector_metrics(det_state, fixed["det_list"])
                seed_fix_p.append(purity)
                seed_fix_hit.append(det_prob)

            seed_scl_p = []
            seed_scl_hit = []
            for k in k_band:
                det_state = propagate_two_register_full(
                    positions, adj, scaled["field"], scaled["src"], scaled["det"], k,
                    scaled["mass_set"], scaled["blocked"])
                purity, _, _, det_prob = compute_detector_metrics(det_state, scaled["det_list"])
                seed_scl_p.append(purity)
                seed_scl_hit.append(det_prob)

            pur_fixed.append(sum(seed_fix_p)/len(seed_fix_p))
            hit_fixed.append(sum(seed_fix_hit)/len(seed_fix_hit))
            pur_scaled.append(sum(seed_scl_p)/len(seed_scl_p))
            hit_scaled.append(sum(seed_scl_hit)/len(seed_scl_hit))

        if pur_fixed:
            # Estimate n_nodes
            positions, _, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=7,
            )
            print(
                f"  {n_layers:8d}  {len(positions):7d}  {scaled_depth:5d}  "
                f"{sum(pur_fixed)/len(pur_fixed):8.4f}  {sum(hit_fixed)/len(hit_fixed):8.4f}  "
                f"{sum(pur_scaled)/len(pur_scaled):8.4f}  {sum(hit_scaled)/len(hit_scaled):8.4f}  "
                f"{len(pur_fixed):7d}"
            )

    print()
    print("pur_fix/hit_fix: fixed one-layer post-barrier environment region")
    print("pur_scl/hit_scl: post-barrier environment depth scales ~ n_layers/6")
    print("All purities are detector-state purities conditioned on detector hits")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
