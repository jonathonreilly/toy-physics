#!/usr/bin/env python3
"""Do graph growth rules SELECT for interference-producing structure?

Sweep growth parameters (connect_radius, nodes_per_layer, inhibit_radius)
and measure both the graph's structural observables and the resulting
gravity-induced interference strength.

If certain growth parameters systematically produce stronger interference,
the growth dynamics SELECT for the conditions that enable the phenomenon.

PStack experiment: growth-rule-selection
"""

from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.generative_dag_gravity import compute_field_on_dag
from scripts.generated_dag_gravity_induced_phase import pathsum_with_field


def measure_interference_strength(
    n_layers, npl, y_range, connect_radius, seed,
):
    """Generate DAG with specific parameters, measure gravity-induced interference."""
    positions, adj, arrival = generate_causal_dag(
        n_layers=n_layers, nodes_per_layer=npl,
        y_range=y_range, connect_radius=connect_radius, rng_seed=seed,
    )
    n = len(positions)
    edges = sum(len(v) for v in adj.values())
    detector_layer = n_layers - 1
    detector_ys = [float(y) for y in range(-int(y_range), int(y_range) + 1)]
    detector_tol = 2.0

    free_field = {i: 0.0 for i in range(n)}
    free_pattern = pathsum_with_field(
        positions, adj, arrival, 0,
        float(detector_layer), detector_ys, detector_tol, free_field,
    )
    total_free = sum(free_pattern.values())
    if total_free == 0:
        return None

    mid = n_layers // 2
    mass_idx = frozenset(
        i for i, (x, y) in enumerate(positions)
        if mid - 2 <= x <= mid + 2 and 1.0 <= y <= y_range
    )
    if len(mass_idx) < 2:
        return None

    dist_field = compute_field_on_dag(positions, adj, mass_idx)
    grav_pattern = pathsum_with_field(
        positions, adj, arrival, 0,
        float(detector_layer), detector_ys, detector_tol, dist_field,
    )
    total_grav = sum(grav_pattern.values())
    if total_grav == 0:
        return None

    max_shift = max(
        abs(grav_pattern.get(dy, 0)/total_grav - free_pattern.get(dy, 0)/total_free)
        for dy in detector_ys
    )

    # Structural observables
    degrees = [len(adj.get(i, [])) for i in range(n)]
    mean_degree = sum(degrees) / n

    return {
        "n": n, "edges": edges, "mean_degree": mean_degree,
        "mass_nodes": len(mass_idx), "pattern_shift": max_shift,
    }


def main() -> None:
    n_layers = 15
    y_range = 6.0
    n_seeds = 8

    print("=" * 80)
    print("GROWTH RULE INTERFERENCE SELECTION")
    print("  Do growth parameters systematically affect interference strength?")
    print("=" * 80)
    print()

    # Sweep connect_radius at fixed npl
    print("SWEEP 1: connect_radius (fixed npl=12)")
    print(f"{'radius':>7s}  {'mean_nodes':>10s}  {'mean_edges':>10s}  {'mean_deg':>9s}  "
          f"{'mean_shift':>10s}  {'std_shift':>10s}  {'min_shift':>10s}  {'max_shift':>10s}")
    print("-" * 82)

    for radius in [1.5, 1.8, 2.0, 2.2, 2.5, 3.0, 3.5]:
        shifts = []
        nodes_list = []
        edges_list = []
        deg_list = []

        for seed in range(n_seeds):
            r = measure_interference_strength(n_layers, 12, y_range, radius, seed)
            if r:
                shifts.append(r["pattern_shift"])
                nodes_list.append(r["n"])
                edges_list.append(r["edges"])
                deg_list.append(r["mean_degree"])

        if shifts:
            mean_s = sum(shifts) / len(shifts)
            std_s = math.sqrt(sum((s - mean_s)**2 for s in shifts) / len(shifts))
            print(f"{radius:7.1f}  {sum(nodes_list)/len(nodes_list):10.0f}  "
                  f"{sum(edges_list)/len(edges_list):10.0f}  "
                  f"{sum(deg_list)/len(deg_list):9.2f}  "
                  f"{mean_s:10.4f}  {std_s:10.4f}  {min(shifts):10.4f}  {max(shifts):10.4f}")

    # Sweep npl at fixed radius
    print()
    print("SWEEP 2: nodes_per_layer (fixed radius=2.5)")
    print(f"{'npl':>5s}  {'mean_nodes':>10s}  {'mean_edges':>10s}  {'mean_deg':>9s}  "
          f"{'mean_shift':>10s}  {'std_shift':>10s}")
    print("-" * 60)

    for npl in [4, 6, 8, 12, 16, 20, 30]:
        shifts = []
        nodes_list = []
        edges_list = []
        deg_list = []

        for seed in range(n_seeds):
            r = measure_interference_strength(n_layers, npl, y_range, 2.5, seed)
            if r:
                shifts.append(r["pattern_shift"])
                nodes_list.append(r["n"])
                edges_list.append(r["edges"])
                deg_list.append(r["mean_degree"])

        if shifts:
            mean_s = sum(shifts) / len(shifts)
            std_s = math.sqrt(sum((s - mean_s)**2 for s in shifts) / len(shifts))
            print(f"{npl:5d}  {sum(nodes_list)/len(nodes_list):10.0f}  "
                  f"{sum(edges_list)/len(edges_list):10.0f}  "
                  f"{sum(deg_list)/len(deg_list):9.2f}  "
                  f"{mean_s:10.4f}  {std_s:10.4f}")

    # Sweep y_range (controls aspect ratio)
    print()
    print("SWEEP 3: y_range (controls graph width, fixed npl=12, radius=2.5)")
    print(f"{'y_range':>7s}  {'mean_shift':>10s}  {'std_shift':>10s}")
    print("-" * 30)

    for yr in [3.0, 4.0, 5.0, 6.0, 8.0, 10.0]:
        shifts = []
        for seed in range(n_seeds):
            r = measure_interference_strength(n_layers, 12, yr, 2.5, seed)
            if r:
                shifts.append(r["pattern_shift"])
        if shifts:
            mean_s = sum(shifts) / len(shifts)
            std_s = math.sqrt(sum((s - mean_s)**2 for s in shifts) / len(shifts))
            print(f"{yr:7.1f}  {mean_s:10.4f}  {std_s:10.4f}")

    print()
    print("If mean_shift varies systematically with growth parameters:")
    print("  → growth rules SELECT for interference-producing structure")
    print("If mean_shift is constant regardless of parameters:")
    print("  → interference is robust to graph structure (universal)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
