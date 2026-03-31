#!/usr/bin/env python3
"""Do graph growth rules SELECT for gravitational attraction?

Earlier work showed growth rules select for interference (mean_degree≥3).
This tests whether the same growth parameters also select for
gravitational attraction using the corrected propagator (1/L^p).

Sweep: connect_radius, nodes_per_layer, y_range.
Measure: attraction (centroid shift toward mass), interference (V),
         and graph structural properties (mean_degree, connectivity).

Key question: does the same structural condition that enables
interference (high connectivity) also enable attraction?

PStack experiment: growth-rule-attraction-selection
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag


def compute_field_on_dag(positions, adj, mass_indices, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_indices)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        new_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                new_field[i] = 1.0
                continue
            nbs = undirected.get(i, set())
            if nbs:
                new_field[i] = sum(field[j] for j in nbs) / len(nbs)
        field = new_field
    return field


def pathsum_corrected(positions, adj, field, source_indices, detector_indices,
                      phase_k, atten_power):
    n = len(positions)
    in_degree = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_degree[j] += 1

    from collections import deque
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    order = []
    while queue:
        i = queue.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_degree[j] -= 1
            if in_degree[j] == 0:
                queue.append(j)

    amplitudes = [0.0 + 0.0j] * n
    for s in source_indices:
        amplitudes[s] = 1.0 / len(source_indices) + 0.0j

    for i in order:
        amp = amplitudes[i]
        if abs(amp) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            delay = L * (1.0 + lf)
            retained = math.sqrt(max(delay * delay - L * L, 0.0))
            action = delay - retained
            atten = 1.0 / (L ** atten_power)
            ea = cmath.exp(1j * phase_k * action) * atten
            amplitudes[j] += amp * ea

    probs = {}
    for d in detector_indices:
        probs[d] = abs(amplitudes[d]) ** 2
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def centroid_y(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1] * p for d, p in probs.items()) / total


def measure_graph_properties(positions, adj):
    """Compute structural observables of the graph."""
    n = len(positions)
    edges = sum(len(v) for v in adj.values())
    mean_degree = 2 * edges / n if n > 0 else 0  # undirected count

    # Actually for DAG: out-degree
    out_degrees = [len(adj.get(i, [])) for i in range(n)]
    mean_out = sum(out_degrees) / len(out_degrees) if out_degrees else 0

    return {
        'n_nodes': n,
        'n_edges': edges,
        'mean_out_degree': mean_out,
    }


def test_attraction(positions, adj, source_indices, detector_indices,
                    mass_indices, mass_cy, center_y, k_band, atten_power=1.0):
    """Test attraction with k-averaged propagator. Returns mean shift and attraction bool."""
    free_field = [0.0] * len(positions)
    mass_field = compute_field_on_dag(positions, adj, mass_indices)

    shifts = []
    for k in k_band:
        fp = pathsum_corrected(positions, adj, free_field, source_indices,
                               detector_indices, k, atten_power)
        mp = pathsum_corrected(positions, adj, mass_field, source_indices,
                               detector_indices, k, atten_power)
        fcy = centroid_y(fp, positions)
        mcy = centroid_y(mp, positions)
        shifts.append(mcy - fcy)

    avg_shift = sum(shifts) / len(shifts) if shifts else 0
    toward = mass_cy - center_y
    attracts = (toward > 0 and avg_shift > 0.05) or (toward < 0 and avg_shift < -0.05)
    return avg_shift, attracts


def main() -> None:
    k_band = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    n_seeds_per = 5
    n_layers = 12

    print("=" * 80)
    print("GROWTH RULE SELECTION FOR GRAVITATIONAL ATTRACTION")
    print("  Corrected propagator: exp(i*k*S) / L^p")
    print("  k-averaged over [3, 4, 5, 6, 7, 8]")
    print("=" * 80)
    print()

    # ================================================================
    # SWEEP 1: Connect radius (controls graph density)
    # ================================================================
    print("SWEEP 1: Connect radius (graph density)")
    print(f"  n_layers={n_layers}, nodes_per_layer=20, y_range=10")
    print()

    print(f"  {'radius':>8s}  {'mean_deg':>8s}  {'attract%':>8s}  {'mean_shift':>10s}  {'n_valid':>7s}")
    print(f"  {'-' * 48}")

    for radius in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]:
        attract_count = 0
        all_shifts = []
        all_deg = []
        valid = 0

        for seed in range(n_seeds_per):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=20,
                y_range=10.0, connect_radius=radius,
                rng_seed=seed * 13 + 5,
            )

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue

            source_indices = by_layer[layers[0]]
            detector_indices = by_layer[layers[-1]]
            mid = len(layers) // 2
            mid_indices = by_layer[layers[mid]]

            if not mid_indices or not detector_indices:
                continue

            props = measure_graph_properties(positions, adj)
            all_deg.append(props['mean_out_degree'])

            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_indices = [i for i in mid_indices if positions[i][1] > center_y + 1]
            if len(mass_indices) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)
            shift, attracts = test_attraction(
                positions, adj, source_indices, detector_indices,
                mass_indices, mass_cy, center_y, k_band,
            )
            all_shifts.append(shift)
            if attracts:
                attract_count += 1
            valid += 1

        if valid > 0:
            mean_deg = sum(all_deg) / len(all_deg)
            mean_shift = sum(all_shifts) / len(all_shifts)
            pct = 100 * attract_count / valid
            print(f"  {radius:8.1f}  {mean_deg:8.1f}  {pct:7.0f}%  {mean_shift:+10.3f}  {valid:7d}")

    # ================================================================
    # SWEEP 2: Nodes per layer (controls path diversity)
    # ================================================================
    print()
    print("SWEEP 2: Nodes per layer (path diversity)")
    print(f"  n_layers={n_layers}, connect_radius=3.0, y_range=10")
    print()

    print(f"  {'npl':>8s}  {'mean_deg':>8s}  {'attract%':>8s}  {'mean_shift':>10s}")
    print(f"  {'-' * 40}")

    for npl in [5, 10, 15, 20, 30, 40, 60]:
        attract_count = 0
        all_shifts = []
        all_deg = []
        valid = 0

        for seed in range(n_seeds_per):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=10.0, connect_radius=3.0,
                rng_seed=seed * 13 + 5,
            )

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue

            source_indices = by_layer[layers[0]]
            detector_indices = by_layer[layers[-1]]
            mid = len(layers) // 2
            mid_indices = by_layer[layers[mid]]

            if not mid_indices or not detector_indices:
                continue

            props = measure_graph_properties(positions, adj)
            all_deg.append(props['mean_out_degree'])

            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_indices = [i for i in mid_indices if positions[i][1] > center_y + 1]
            if len(mass_indices) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)
            shift, attracts = test_attraction(
                positions, adj, source_indices, detector_indices,
                mass_indices, mass_cy, center_y, k_band,
            )
            all_shifts.append(shift)
            if attracts:
                attract_count += 1
            valid += 1

        if valid > 0:
            mean_deg = sum(all_deg) / len(all_deg)
            mean_shift = sum(all_shifts) / len(all_shifts)
            pct = 100 * attract_count / valid
            print(f"  {npl:8d}  {mean_deg:8.1f}  {pct:7.0f}%  {mean_shift:+10.3f}")

    # ================================================================
    # SWEEP 3: y_range (controls spatial spread)
    # ================================================================
    print()
    print("SWEEP 3: y_range (spatial spread)")
    print(f"  n_layers={n_layers}, nodes_per_layer=20, connect_radius=3.0")
    print()

    print(f"  {'y_range':>8s}  {'mean_deg':>8s}  {'attract%':>8s}  {'mean_shift':>10s}")
    print(f"  {'-' * 40}")

    for yr in [3.0, 5.0, 8.0, 10.0, 15.0, 20.0, 30.0]:
        attract_count = 0
        all_shifts = []
        all_deg = []
        valid = 0

        for seed in range(n_seeds_per):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=20,
                y_range=yr, connect_radius=3.0,
                rng_seed=seed * 13 + 5,
            )

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue

            source_indices = by_layer[layers[0]]
            detector_indices = by_layer[layers[-1]]
            mid = len(layers) // 2
            mid_indices = by_layer[layers[mid]]

            if not mid_indices or not detector_indices:
                continue

            props = measure_graph_properties(positions, adj)
            all_deg.append(props['mean_out_degree'])

            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_indices = [i for i in mid_indices if positions[i][1] > center_y + 1]
            if len(mass_indices) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)
            shift, attracts = test_attraction(
                positions, adj, source_indices, detector_indices,
                mass_indices, mass_cy, center_y, k_band,
            )
            all_shifts.append(shift)
            if attracts:
                attract_count += 1
            valid += 1

        if valid > 0:
            mean_deg = sum(all_deg) / len(all_deg)
            mean_shift = sum(all_shifts) / len(all_shifts)
            pct = 100 * attract_count / valid
            print(f"  {yr:8.1f}  {mean_deg:8.1f}  {pct:7.0f}%  {mean_shift:+10.3f}")

    # ================================================================
    # SUMMARY: correlate mean_degree with attraction
    # ================================================================
    print()
    print("=" * 80)
    print("CORRELATION ANALYSIS")
    print("=" * 80)
    print()

    # Run one big sweep collecting per-graph data
    all_data = []
    for radius in [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
        for npl in [10, 15, 20, 30]:
            for seed in range(3):
                positions, adj, arrival = generate_causal_dag(
                    n_layers=n_layers, nodes_per_layer=npl,
                    y_range=10.0, connect_radius=radius,
                    rng_seed=seed * 17 + 3,
                )

                by_layer = defaultdict(list)
                for idx, (x, y) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 4:
                    continue

                source_indices = by_layer[layers[0]]
                detector_indices = by_layer[layers[-1]]
                mid = len(layers) // 2
                mid_indices = by_layer[layers[mid]]

                if not mid_indices or not detector_indices:
                    continue

                props = measure_graph_properties(positions, adj)

                all_ys = [y for _, y in positions]
                center_y = sum(all_ys) / len(all_ys)
                mass_indices = [i for i in mid_indices if positions[i][1] > center_y + 1]
                if len(mass_indices) < 2:
                    continue

                mass_cy = sum(positions[i][1] for i in mass_indices) / len(mass_indices)
                shift, attracts = test_attraction(
                    positions, adj, source_indices, detector_indices,
                    mass_indices, mass_cy, center_y, k_band,
                )

                all_data.append({
                    'mean_deg': props['mean_out_degree'],
                    'shift': shift,
                    'attracts': attracts,
                })

    # Bin by mean_degree
    bins = defaultdict(list)
    for d in all_data:
        bin_key = round(d['mean_deg'] / 2) * 2  # Bin to nearest 2
        bins[bin_key].append(d)

    print(f"  {'deg_bin':>8s}  {'n_graphs':>8s}  {'attract%':>8s}  {'mean_shift':>10s}")
    print(f"  {'-' * 40}")

    for deg in sorted(bins.keys()):
        entries = bins[deg]
        n = len(entries)
        attract = sum(1 for e in entries if e['attracts'])
        mean_shift = sum(e['shift'] for e in entries) / n
        pct = 100 * attract / n
        print(f"  {deg:8.0f}  {n:8d}  {pct:7.0f}%  {mean_shift:+10.3f}")

    print()
    print("If attraction% increases with mean_degree:")
    print("  → Graph density SELECTS for attraction")
    print("  → Same structural property enables both interference AND gravity")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
