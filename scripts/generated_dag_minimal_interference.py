#!/usr/bin/env python3
"""Find the MINIMAL generated graph that supports endogenous interference.

Sweep n_layers and nodes_per_layer downward to find the smallest
graph where a persistent pattern's gravitational field still
produces measurable detector pattern changes.

Also: identify which graph observables (node count, edge count,
path diversity, field extent) predict whether interference works.

PStack experiment: minimal-endogenous-interference
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.generative_dag_gravity import compute_field_on_dag
from scripts.generated_dag_gravity_induced_phase import pathsum_with_field


def test_endogenous_interference(
    n_layers: int, npl: int, y_range: float, seed: int,
) -> dict:
    """Generate a DAG, add a mass, measure pattern change."""
    positions, adj, arrival = generate_causal_dag(
        n_layers=n_layers, nodes_per_layer=npl,
        y_range=y_range, connect_radius=2.5, rng_seed=seed,
    )
    n = len(positions)
    edges = sum(len(v) for v in adj.values())
    detector_layer = n_layers - 1
    detector_ys = [float(y) for y in range(-int(y_range), int(y_range) + 1)]
    detector_tol = 2.0

    # Free field
    free_field = {i: 0.0 for i in range(n)}
    free_pattern = pathsum_with_field(
        positions, adj, arrival, 0,
        float(detector_layer), detector_ys, detector_tol, free_field,
    )
    total_free = sum(free_pattern.values())

    if total_free == 0:
        return {"n": n, "edges": edges, "signal": False, "pattern_shift": 0, "mass_nodes": 0}

    # Mass at mid-graph, upper region
    mid_layer = n_layers // 2
    mass_idx = frozenset(
        i for i, (x, y) in enumerate(positions)
        if mid_layer - 2 <= x <= mid_layer + 2 and 1.0 <= y <= y_range
    )

    if len(mass_idx) < 2:
        return {"n": n, "edges": edges, "signal": True, "pattern_shift": 0, "mass_nodes": len(mass_idx)}

    dist_field = compute_field_on_dag(positions, adj, mass_idx)
    nonzero_field = sum(1 for v in dist_field.values() if v > 0.001)

    grav_pattern = pathsum_with_field(
        positions, adj, arrival, 0,
        float(detector_layer), detector_ys, detector_tol, dist_field,
    )
    total_grav = sum(grav_pattern.values())

    if total_grav == 0:
        return {"n": n, "edges": edges, "signal": True, "pattern_shift": 0,
                "mass_nodes": len(mass_idx), "field_extent": nonzero_field}

    max_shift = max(
        abs(grav_pattern.get(dy, 0)/total_grav - free_pattern.get(dy, 0)/total_free)
        for dy in detector_ys
    )

    return {
        "n": n, "edges": edges, "signal": True,
        "pattern_shift": max_shift, "mass_nodes": len(mass_idx),
        "field_extent": nonzero_field,
    }


def main() -> None:
    print("=" * 80)
    print("MINIMAL GRAPH FOR ENDOGENOUS INTERFERENCE")
    print("=" * 80)
    print()

    configs = [
        (5, 5, 4.0),
        (7, 5, 4.0),
        (10, 5, 5.0),
        (10, 8, 5.0),
        (10, 12, 6.0),
        (15, 8, 6.0),
        (15, 12, 7.0),
        (15, 20, 8.0),
        (20, 12, 7.0),
        (20, 20, 8.0),
        (25, 20, 8.0),
    ]

    print(f"{'layers':>7s}  {'n/layer':>7s}  {'y_range':>7s}  {'nodes':>6s}  {'edges':>6s}  "
          f"{'signal':>7s}  {'mass':>5s}  {'field_ext':>9s}  "
          f"{'mean_shift':>10s}  {'max_shift':>10s}  {'n_working':>10s}")
    print("-" * 95)

    for n_layers, npl, yr in configs:
        shifts = []
        signals = 0
        working = 0
        total_nodes = 0
        total_edges = 0
        total_mass = 0
        total_field = 0

        for seed in range(10):
            result = test_endogenous_interference(n_layers, npl, yr, seed)
            total_nodes += result["n"]
            total_edges += result["edges"]

            if result["signal"]:
                signals += 1
            if result["pattern_shift"] > 0.01:
                working += 1
                shifts.append(result["pattern_shift"])
            total_mass += result.get("mass_nodes", 0)
            total_field += result.get("field_extent", 0)

        mean_shift = sum(shifts) / len(shifts) if shifts else 0
        max_shift = max(shifts) if shifts else 0

        print(f"{n_layers:7d}  {npl:7d}  {yr:7.1f}  {total_nodes//10:6d}  {total_edges//10:6d}  "
              f"{signals:7d}/10  {total_mass//10:5d}  {total_field//10:9d}  "
              f"{mean_shift:10.4f}  {max_shift:10.4f}  {working:10d}/10")

    # Detailed view of the smallest working config
    print()
    print("=" * 80)
    print("DETAILED: Smallest configs that work")
    print("=" * 80)
    print()

    for n_layers, npl, yr in [(7, 5, 4.0), (10, 5, 5.0), (10, 8, 5.0)]:
        print(f"  {n_layers} layers, {npl} nodes/layer, y_range={yr}:")
        for seed in range(5):
            result = test_endogenous_interference(n_layers, npl, yr, seed)
            status = "WORKS" if result["pattern_shift"] > 0.01 else "no effect"
            print(f"    seed={seed}: {result['n']} nodes, {result['edges']} edges, "
                  f"mass={result.get('mass_nodes', 0)}, shift={result['pattern_shift']:.4f} [{status}]")
        print()

    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
