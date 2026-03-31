#!/usr/bin/env python3
"""Test interference through NATURAL graph bottlenecks.

Instead of imposing a barrier with slits, find natural bottleneck
regions in the generated graph — places where few edges cross a
vertical cut. These are endogenous "barriers" with endogenous "slits."

If interference emerges through natural bottlenecks, the barrier
is no longer essential scaffold — the graph generates it.

PStack experiment: natural-bottleneck-interference
"""

from __future__ import annotations
import math
import cmath
import heapq
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag


def find_bottleneck(positions, adj, n_layers):
    """Find the layer with minimum edge crossing (natural bottleneck)."""
    min_crossing = float("inf")
    best_layer = None

    for layer_x in range(3, n_layers - 3):
        crossing = 0
        for i, children in adj.items():
            ix = positions[i][0]
            for j in children:
                jx = positions[j][0]
                if ix < layer_x <= jx or jx < layer_x <= ix:
                    crossing += 1
        if crossing < min_crossing:
            min_crossing = crossing
            best_layer = layer_x

    return best_layer, min_crossing


def find_crossing_edges(positions, adj, barrier_x):
    """Find all edges that cross the barrier_x line. These are the 'slits'."""
    crossings = []
    for i, children in adj.items():
        ix, iy = positions[i]
        for j in children:
            jx, jy = positions[j]
            if ix < barrier_x <= jx:
                crossings.append((i, j, iy, jy))
    return crossings


def pathsum_natural_barrier(
    positions, adj, arrival, source_idx,
    detector_x, detector_ys, detector_tol,
    barrier_x, crossing_edges,
    phase_shift_edge_idx=None,
    phase_shift=0.0,
):
    """Path-sum where the barrier is NATURAL — only crossing_edges pass through.

    No amplitude zeroing needed: the graph's own structure limits
    which paths cross the bottleneck.

    phase_shift_edge_idx: if set, apply phase shift to paths that
    use this specific crossing edge (the "upper slit").
    """
    n = len(positions)
    order = sorted(range(n), key=lambda i: arrival[i])

    # Set of crossing edge parent nodes for phase tracking
    crossing_parents = {i for i, j, _, _ in crossing_edges}
    upper_edges = set()
    if phase_shift_edge_idx is not None:
        upper_edges = {(crossing_edges[phase_shift_edge_idx][0],
                        crossing_edges[phase_shift_edge_idx][1])}

    amplitudes: dict[int, complex] = {source_idx: 1.0 + 0.0j}
    detector_amps: dict[float, complex] = defaultdict(complex)

    for i in order:
        if i not in amplitudes:
            continue
        amp = amplitudes[i]
        x, y = positions[i]

        if abs(x - detector_x) < 0.5:
            for dy in detector_ys:
                if abs(y - dy) < detector_tol:
                    detector_amps[dy] += amp
            continue

        for j in adj.get(i, []):
            jx, jy = positions[j]
            dist = math.dist(positions[i], positions[j])
            delay = dist
            action = delay
            link_amp = cmath.exp(1j * 4.0 * action) / max(delay, 0.01)

            # Apply phase shift on the designated "upper" crossing edge
            if (i, j) in upper_edges:
                link_amp *= cmath.exp(1j * phase_shift)

            if j not in amplitudes:
                amplitudes[j] = 0.0 + 0.0j
            amplitudes[j] += amp * link_amp

    return {dy: abs(detector_amps[dy]) ** 2 for dy in detector_ys}


def visibility(probs):
    pm, pn = max(probs), min(probs)
    return (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0


def main() -> None:
    n_layers = 25
    nodes_per_layer = 20
    y_range = 8.0
    detector_layer = n_layers - 1
    n_phases = 16
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    detector_ys = [float(y) for y in range(-8, 9)]
    detector_tol = 1.5

    print("=" * 80)
    print("NATURAL BOTTLENECK INTERFERENCE")
    print("  No hand-imposed barrier. The graph's own sparse region is the barrier.")
    print("=" * 80)
    print()

    results = []

    for seed in range(20):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )

        # Find the natural bottleneck
        bottleneck_x, min_crossing = find_bottleneck(positions, adj, n_layers)
        crossing_edges = find_crossing_edges(positions, adj, bottleneck_x)

        if len(crossing_edges) < 2:
            print(f"  seed={seed}: bottleneck at x={bottleneck_x}, "
                  f"{min_crossing} crossings — too few edges, skipping")
            continue

        # Use the topmost and bottommost crossing edges as natural "slits"
        crossing_edges.sort(key=lambda e: (e[2] + e[3]) / 2)  # Sort by average y
        lower_edge_idx = 0
        upper_edge_idx = len(crossing_edges) - 1

        lower_y = (crossing_edges[lower_edge_idx][2] + crossing_edges[lower_edge_idx][3]) / 2
        upper_y = (crossing_edges[upper_edge_idx][2] + crossing_edges[upper_edge_idx][3]) / 2

        # Phase sweep on the upper crossing edge
        probs_center = []
        for phase in phases:
            dist = pathsum_natural_barrier(
                positions, adj, arrival, 0,
                float(detector_layer), [0.0], detector_tol,
                bottleneck_x, crossing_edges,
                phase_shift_edge_idx=upper_edge_idx,
                phase_shift=phase,
            )
            probs_center.append(dist.get(0.0, 0.0))

        if any(p > 0 for p in probs_center):
            v = visibility(probs_center)
        else:
            v = -1.0

        row = {
            "seed": seed, "V": v, "bottleneck_x": bottleneck_x,
            "n_crossings": len(crossing_edges), "min_crossing": min_crossing,
            "upper_y": upper_y, "lower_y": lower_y,
            "slit_sep": upper_y - lower_y,
        }
        results.append(row)

        print(f"  seed={seed:2d}: bottleneck x={bottleneck_x}, "
              f"{len(crossing_edges):2d} crossings, "
              f"natural slits at y=[{lower_y:.1f}, {upper_y:.1f}], "
              f"V(y=0)={v:.4f}")

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    valid = [r for r in results if r["V"] >= 0]
    if valid:
        mean_v = sum(r["V"] for r in valid) / len(valid)
        nonzero = sum(1 for r in valid if r["V"] > 0.01)
        print(f"  Valid seeds: {len(valid)}/{len(results)}")
        print(f"  Mean V(y=0): {mean_v:.4f}")
        print(f"  Seeds with V > 0.01: {nonzero}")
        print(f"  Mean bottleneck crossings: {sum(r['n_crossings'] for r in valid)/len(valid):.1f}")
        print(f"  Mean slit separation: {sum(r['slit_sep'] for r in valid)/len(valid):.1f}")
    else:
        print("  No valid results")

    print()
    print("If V > 0 at natural bottlenecks: the graph generates its own interference")
    print("without ANY hand-imposed barrier structure.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
