#!/usr/bin/env python3
"""Test gravity on a generated causal DAG.

Experiment #33 showed interference emerges on random graphs.
Does gravity (path bending from persistent nodes) also work?

Place persistent-node clusters on the random DAG, compute the
delay field, find stationary-action paths, and check for bending.

PStack experiment: generative-dag-gravity
"""

from __future__ import annotations
import math
import cmath
import random
import heapq
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import causal_order, generate_causal_dag


def compute_field_on_dag(
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    persistent_indices: frozenset[int],
    tolerance: float = 1e-8,
    max_iterations: int = 400,
) -> dict[int, float]:
    """Compute a delay-like field on the generated DAG via relaxation.

    Persistent nodes have field = 1.0 (source).
    Leaf nodes (no children) have field = 0.0 (boundary).
    Interior nodes relax to average of neighbors.
    Uses undirected adjacency for the relaxation.
    """
    n = len(positions)
    # Build undirected adjacency
    undirected: dict[int, list[int]] = defaultdict(list)
    for i, children in adj.items():
        for j in children:
            undirected[i].append(j)
            undirected[j].append(i)

    # Identify boundary (nodes with degree 1 or no children in forward DAG)
    all_children = set()
    for children in adj.values():
        all_children.update(children)
    leaf_nodes = {i for i in range(n) if i not in adj or len(adj.get(i, [])) == 0}
    # Also treat the first-layer source as boundary
    boundary = leaf_nodes | {0}

    field = {i: 0.0 for i in range(n)}
    for i in persistent_indices:
        field[i] = 1.0

    for _ in range(max_iterations):
        max_change = 0.0
        updated = {}
        for i in range(n):
            if i in boundary and i not in persistent_indices:
                updated[i] = 0.0
            elif i in persistent_indices:
                updated[i] = 1.0
            else:
                nbs = undirected.get(i, [])
                if nbs:
                    avg = sum(field[j] for j in nbs) / len(nbs)
                    updated[i] = avg
                else:
                    updated[i] = 0.0
            max_change = max(max_change, abs(updated[i] - field[i]))
        field = updated
        if max_change < tolerance:
            break

    return field


def find_path_on_dag(
    adj: dict[int, list[int]],
    positions: list[tuple[float, float]],
    arrival: list[float],
    field: dict[int, float],
    source_idx: int,
    target_layer: int,
    target_y: float,
    target_tolerance: float,
    phase_per_action: float = 4.0,
) -> tuple[float, list[int]]:
    """Find lowest-action path from source to target region on DAG.

    Uses dynamic programming on the DAG (topological order).
    Action on each edge = delay - sqrt(delay² - link_length²)
    where delay = link_length * (1 + avg_field).
    """
    n = len(positions)
    order = causal_order(positions, arrival)

    # DP: best action and predecessor for each node
    best_action: dict[int, float] = {source_idx: 0.0}
    predecessor: dict[int, int] = {}

    for i in order:
        if i not in best_action:
            continue
        for j in adj.get(i, []):
            px, py = positions[i]
            qx, qy = positions[j]
            link_len = math.dist((px, py), (qx, qy))
            avg_field = 0.5 * (field.get(i, 0) + field.get(j, 0))
            delay = link_len * (1.0 + avg_field)
            retained = math.sqrt(max(delay ** 2 - link_len ** 2, 0.0))
            action_inc = delay - retained

            new_action = best_action[i] + action_inc
            if new_action < best_action.get(j, float("inf")):
                best_action[j] = new_action
                predecessor[j] = i

    # Find best target node
    best_target = None
    best_target_action = float("inf")
    for i in range(n):
        x, y = positions[i]
        if abs(x - target_layer) < 0.5 and abs(y - target_y) < target_tolerance:
            if i in best_action and best_action[i] < best_target_action:
                best_target = i
                best_target_action = best_action[i]

    if best_target is None:
        return float("inf"), []

    # Reconstruct path
    path = [best_target]
    while path[-1] in predecessor:
        path.append(predecessor[path[-1]])
    path.reverse()

    return best_target_action, path


def main() -> None:
    print("=" * 72)
    print("GRAVITY ON GENERATED CAUSAL DAG")
    print("=" * 72)
    print()

    n_layers = 25
    nodes_per_layer = 20
    y_range = 8.0
    detector_layer = n_layers - 1

    for seed in [42, 123, 456]:
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )

        print(f"\n{'=' * 60}")
        print(f"SEED = {seed}: {len(positions)} nodes, {sum(len(v) for v in adj.values())} edges")
        print(f"{'=' * 60}")

        # Place persistent nodes at layers 10-14, y=4-6 (upper region)
        mass_indices = frozenset(
            i for i, (x, y) in enumerate(positions)
            if 10 <= x <= 14 and 3.5 <= y <= 6.5
        )

        if len(mass_indices) < 2:
            print(f"  Not enough mass nodes ({len(mass_indices)}), skipping")
            continue

        print(f"  Mass: {len(mass_indices)} persistent nodes at x=[10,14], y=[3.5,6.5]")

        # Compute free and distorted fields
        free_field = {i: 0.0 for i in range(len(positions))}
        distorted_field = compute_field_on_dag(positions, adj, mass_indices)

        # Check field has structure
        nonzero_field = sum(1 for v in distorted_field.values() if v > 0.001)
        max_field = max(distorted_field.values())
        print(f"  Field: {nonzero_field} nonzero nodes, max={max_field:.4f}")

        # Find paths to several target y-positions
        print()
        print(f"  {'target_y':>8s}  {'free_action':>12s}  {'dist_action':>12s}  "
              f"{'action_diff':>12s}  {'free_steps':>10s}  {'dist_steps':>10s}")
        print(f"  {'-' * 68}")

        for target_y in [-6.0, -3.0, 0.0, 3.0, 6.0]:
            free_action, free_path = find_path_on_dag(
                adj, positions, arrival, free_field,
                0, detector_layer, target_y, 2.0,
            )
            dist_action, dist_path = find_path_on_dag(
                adj, positions, arrival, distorted_field,
                0, detector_layer, target_y, 2.0,
            )

            if free_action < float("inf") and dist_action < float("inf"):
                ad = dist_action - free_action
                print(f"  {target_y:8.1f}  {free_action:12.4f}  {dist_action:12.4f}  "
                      f"{ad:12.4f}  {len(free_path):10d}  {len(dist_path):10d}")
            else:
                print(f"  {target_y:8.1f}  {'no path':>12s}")

        # Compare: do paths bend toward the mass?
        print()
        print("  Path y-profiles (free vs distorted) for target_y=0.0:")
        _, free_path = find_path_on_dag(adj, positions, arrival, free_field, 0, detector_layer, 0.0, 2.0)
        _, dist_path = find_path_on_dag(adj, positions, arrival, distorted_field, 0, detector_layer, 0.0, 2.0)

        if free_path and dist_path:
            # Sample path y-values at a few x-positions
            def path_y_at_x(path, target_x):
                for idx in path:
                    x, y = positions[idx]
                    if abs(x - target_x) < 1.0:
                        return y
                return None

            print(f"    {'x':>4s}  {'free_y':>8s}  {'dist_y':>8s}  {'shift':>8s}")
            print(f"    {'-' * 32}")
            for x in range(0, n_layers, 3):
                fy = path_y_at_x(free_path, x)
                dy = path_y_at_x(dist_path, x)
                if fy is not None and dy is not None:
                    print(f"    {x:4d}  {fy:8.2f}  {dy:8.2f}  {dy - fy:+8.2f}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
