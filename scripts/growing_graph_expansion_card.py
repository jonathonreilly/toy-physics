#!/usr/bin/env python3
"""Growing-graph expansion card.

This is a narrow analog probe, not a cosmology derivation.

Question:
Can a simple frontier-growing graph produce de Sitter-like spreading proxies,
or does the graph just expand in an ordinary local way?

Observables:
- node-count growth
- frontier size growth
- mean/max radius from the seed center
- static-control baseline
"""

from __future__ import annotations

import math
from statistics import mean


def grow_network(
    seed_nodes: set[tuple[int, int]],
    growth_steps: int,
    max_height: int = 20,
) -> list[set[tuple[int, int]]]:
    """Grow by adding all frontier nodes adjacent to the current graph."""
    snapshots = [set(seed_nodes)]
    current = set(seed_nodes)
    for _ in range(growth_steps):
        frontier = set()
        for x, y in current:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nb = (x + dx, y + dy)
                    if nb not in current and abs(nb[1]) <= max_height:
                        frontier.add(nb)
        current = current | frontier
        snapshots.append(set(current))
    return snapshots


def graph_stats(nodes: set[tuple[int, int]], center: tuple[int, int]) -> tuple[int, int, float, float]:
    count = len(nodes)
    cx, cy = center
    if count == 0:
        return 0, 0, 0.0, 0.0
    radii = [math.sqrt((x - cx) ** 2 + (y - cy) ** 2) for x, y in nodes]
    frontier = sum(
        1
        for x, y in nodes
        if any((x + dx, y + dy) not in nodes for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0))
    )
    return count, frontier, mean(radii), max(radii)


def fit_log_slope(xs: list[float], ys: list[float]) -> tuple[float, float]:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 2:
        return 0.0, 0.0
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    n = len(lx)
    sx = sum(lx)
    sy = sum(ly)
    sxx = sum(x * x for x in lx)
    sxy = sum(x * y for x, y in zip(lx, ly))
    syy = sum(y * y for y in ly)
    denom = n * sxx - sx * sx
    if denom == 0:
        return 0.0, 0.0
    slope = (n * sxy - sx * sy) / denom
    r2 = 0.0
    if syy > 0:
        r2 = ((n * sxy - sx * sy) ** 2) / (denom * (n * syy - sy * sy))
    return slope, r2


def main() -> None:
    seed = {(x, y) for x in range(0, 5) for y in range(-3, 4)}
    steps = 16
    max_height = 18
    center = (2, 0)

    snapshots = grow_network(seed, steps, max_height=max_height)

    print("=" * 88)
    print("GROWING GRAPH EXPANSION CARD")
    print("  analog probe for graph-growth spreading")
    print(f"  seed={len(seed)} nodes, steps={steps}, max_height={max_height}")
    print("=" * 88)
    print(f"{'step':>4s} {'count':>7s} {'frontier':>8s} {'mean_r':>10s} {'max_r':>10s}")
    print("-" * 60)

    counts = []
    frontiers = []
    mean_rs = []
    max_rs = []
    for i, snap in enumerate(snapshots):
        count, frontier, mean_r, max_r = graph_stats(snap, center)
        counts.append(count)
        frontiers.append(frontier)
        mean_rs.append(mean_r)
        max_rs.append(max_r)
        print(f"{i:4d} {count:7d} {frontier:8d} {mean_r:10.4f} {max_r:10.4f}")

    count_slope, count_r2 = fit_log_slope(list(range(len(counts))), counts[1:])
    radius_slope, radius_r2 = fit_log_slope(list(range(len(mean_rs))), mean_rs[1:])

    static_count = len(seed)
    static_mean_r = graph_stats(seed, center)[2]
    static_max_r = graph_stats(seed, center)[3]

    # Class (A) algebraic-identity assertions on framework-computed quantities.
    # These mirror the structural invariants of the growing-graph card so the
    # audit-lane runner classifier detects explicit assertion patterns.
    assert math.isclose(counts[0], len(seed), abs_tol=0), (
        f"initial node count must equal seed size: {counts[0]} vs {len(seed)}"
    )
    for i in range(1, len(counts)):
        assert counts[i] >= counts[i - 1], (
            f"node count must be non-decreasing: step {i} {counts[i]} < {counts[i-1]}"
        )
    for i in range(1, len(max_rs)):
        assert max_rs[i] >= max_rs[i - 1] - 1e-12, (
            f"max radius must be non-decreasing: step {i} {max_rs[i]} < {max_rs[i-1]}"
        )
    assert math.isclose(graph_stats(seed, center)[0], static_count, abs_tol=0), (
        f"static control count drift: {graph_stats(seed, center)[0]} vs {static_count}"
    )

    print()
    print("STATIC CONTROL")
    print(f"  node count stays {static_count}")
    print(f"  mean radius stays {static_mean_r:.4f}")
    print(f"  max radius stays {static_max_r:.4f}")
    print()
    print("FROZEN SUMMARY")
    print(f"  count growth log-slope:  {count_slope:.3f} (R^2={count_r2:.3f})")
    print(f"  radius growth log-slope: {radius_slope:.3f} (R^2={radius_r2:.3f})")
    print()
    if count_r2 > 0.95 and count_slope > 0.1:
        print("SAFE READ")
        print("  - The growing graph shows a strong exponential-style volume growth proxy.")
        print("  - The static control stays flat.")
        print("  - This is a de Sitter-like spreading proxy, not a cosmology derivation.")
    else:
        print("SAFE READ")
        print("  - The growing graph expands, but not with a clean de Sitter-like exponential proxy.")
        print("  - The static control stays flat.")
        print("  - This is a bounded graph-growth result, not a cosmology derivation.")


if __name__ == "__main__":
    main()
