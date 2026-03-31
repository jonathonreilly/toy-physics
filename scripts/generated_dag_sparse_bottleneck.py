#!/usr/bin/env python3
"""Find graph parameters that produce SPARSE natural bottlenecks.

The previous test found ~213 crossing edges at bottlenecks — too many
for interference. Sweep connect_radius and nodes_per_layer to find
parameter regimes where bottlenecks have 2-10 crossings.

Then test interference at those sparse bottlenecks.

PStack experiment: sparse-bottleneck-search
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.generated_dag_natural_bottleneck import (
    find_bottleneck, find_crossing_edges,
    pathsum_natural_barrier, visibility,
)


def main() -> None:
    n_layers = 25
    y_range = 8.0
    detector_layer = n_layers - 1
    n_phases = 16
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]

    print("=" * 80)
    print("SPARSE BOTTLENECK SEARCH")
    print("=" * 80)
    print()

    # Sweep parameters to find sparse bottlenecks
    print("SWEEP: connect_radius x nodes_per_layer → bottleneck sparsity")
    print()
    print(f"{'radius':>7s}  {'n/layer':>7s}  {'bn_crossings':>13s}  {'total_edges':>12s}  {'seed_range':>12s}")
    print("-" * 56)

    for radius in [1.2, 1.5, 1.8, 2.0, 2.5]:
        for npl in [5, 8, 12, 20]:
            crossings_list = []
            edges_list = []
            for seed in range(5):
                positions, adj, arrival = generate_causal_dag(
                    n_layers=n_layers, nodes_per_layer=npl,
                    y_range=y_range, connect_radius=radius, rng_seed=seed,
                )
                bn_x, _ = find_bottleneck(positions, adj, n_layers)
                crossing = find_crossing_edges(positions, adj, bn_x)
                crossings_list.append(len(crossing))
                edges_list.append(sum(len(v) for v in adj.values()))

            mean_c = sum(crossings_list) / len(crossings_list)
            mean_e = sum(edges_list) / len(edges_list)
            print(f"{radius:7.1f}  {npl:7d}  {mean_c:13.1f}  {mean_e:12.0f}  "
                  f"[{min(crossings_list)}-{max(crossings_list)}]")

    # Find the sweet spot and test interference
    print()
    print("=" * 80)
    print("INTERFERENCE AT SPARSE BOTTLENECKS")
    print("=" * 80)
    print()

    # Try the sparsest viable configs
    test_configs = [
        (1.2, 5, "very sparse"),
        (1.5, 5, "sparse"),
        (1.5, 8, "moderate"),
        (1.8, 8, "moderate-dense"),
    ]

    for radius, npl, label in test_configs:
        print(f"\n--- {label}: radius={radius}, nodes/layer={npl} ---")
        print(f"{'seed':>5s}  {'bn_x':>5s}  {'crossings':>10s}  {'V(y=0)':>8s}  {'upper_y':>8s}  {'lower_y':>8s}")
        print("-" * 52)

        v_values = []

        for seed in range(15):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius, rng_seed=seed,
            )
            bn_x, _ = find_bottleneck(positions, adj, n_layers)
            crossings = find_crossing_edges(positions, adj, bn_x)

            if len(crossings) < 2:
                print(f"{seed:5d}  {bn_x:5d}  {len(crossings):10d}  {'skip':>8s}")
                continue

            crossings.sort(key=lambda e: (e[2] + e[3]) / 2)
            upper_idx = len(crossings) - 1
            upper_y = (crossings[upper_idx][2] + crossings[upper_idx][3]) / 2
            lower_y = (crossings[0][2] + crossings[0][3]) / 2

            probs = []
            for phase in phases:
                dist = pathsum_natural_barrier(
                    positions, adj, arrival, 0,
                    float(detector_layer), [0.0], 2.0,
                    bn_x, crossings,
                    phase_shift_edge_idx=upper_idx,
                    phase_shift=phase,
                )
                probs.append(dist.get(0.0, 0.0))

            if any(p > 0 for p in probs):
                v = visibility(probs)
            else:
                v = -1.0

            v_values.append(v)
            print(f"{seed:5d}  {bn_x:5d}  {len(crossings):10d}  {v:8.4f}  {upper_y:8.1f}  {lower_y:8.1f}")

        if v_values:
            valid = [v for v in v_values if v >= 0]
            if valid:
                print(f"  → mean V = {sum(valid)/len(valid):.4f}, "
                      f"V > 0.1: {sum(1 for v in valid if v > 0.1)}/{len(valid)}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
