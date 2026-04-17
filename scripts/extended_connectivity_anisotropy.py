#!/usr/bin/env python3
"""Test whether extended neighbor connectivity reduces grid anisotropy.

The 8-neighbor grid has 8.2% signal speed anisotropy. Adding more
neighbor directions (knight's moves, etc.) should reduce this by
giving the path-finder more angles to approximate off-axis paths.

Tests connectivity levels:
- 8 neighbors (standard): offsets with max(|dx|,|dy|) <= 1
- 16 neighbors: offsets with max(|dx|,|dy|) <= 2 (adds knight's moves)
- 24 neighbors: offsets with max(|dx|,|dy|) <= 3

For each: measure signal speed anisotropy and action/distance ratio.

PStack experiment: extended-connectivity
"""

from __future__ import annotations
import math
import heapq
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def build_nodes(width: int, height: int) -> set[tuple[int, int]]:
    return {(x, y) for x in range(width + 1) for y in range(-height, height + 1)}


def get_neighbors(node: tuple[int, int], nodes: set, max_step: int) -> list[tuple[tuple[int, int], float]]:
    """Get neighbors within max_step, with Euclidean distances."""
    x, y = node
    result = []
    for dx in range(-max_step, max_step + 1):
        for dy in range(-max_step, max_step + 1):
            if dx == 0 and dy == 0:
                continue
            nb = (x + dx, y + dy)
            if nb in nodes:
                dist = math.sqrt(dx * dx + dy * dy)
                result.append((nb, dist))
    return result


def compute_arrival_times(
    nodes: set, source: tuple[int, int], max_step: int,
) -> dict[tuple[int, int], float]:
    """Dijkstra with extended neighbor connectivity. delay = distance (free field)."""
    arrival = {source: 0.0}
    frontier = [(0.0, source)]
    while frontier:
        t, node = heapq.heappop(frontier)
        if t > arrival.get(node, float("inf")):
            continue
        for nb, dist in get_neighbors(node, nodes, max_step):
            new_t = t + dist  # delay = distance in free field
            if new_t < arrival.get(nb, float("inf")):
                arrival[nb] = new_t
                heapq.heappush(frontier, (new_t, nb))
    return arrival


def shortest_path_action(
    nodes: set, source: tuple[int, int], target: tuple[int, int], max_step: int,
) -> float:
    """Shortest path action (sum of edge lengths) with extended connectivity."""
    arrival = compute_arrival_times(nodes, source, max_step)
    return arrival.get(target, float("inf"))


def main() -> None:
    width = 50
    height = 50
    nodes = build_nodes(width, height)
    source = (0, 0)

    print("=" * 72)
    print("EXTENDED CONNECTIVITY ANISOTROPY TEST")
    print("=" * 72)
    print(f"Grid: {width}x{2*height+1}, source={source}")
    print()

    for max_step, label in [(1, "8-neighbor"), (2, "24-neighbor"), (3, "48-neighbor")]:
        # Count actual neighbor directions
        center_nbs = get_neighbors((25, 0), nodes, max_step)
        n_dirs = len(center_nbs)

        print(f"\n{'=' * 60}")
        print(f"{label} (max_step={max_step}, {n_dirs} directions)")
        print(f"{'=' * 60}")

        arrival = compute_arrival_times(nodes, source, max_step)

        # Signal speed at various angles, radius ~20
        radius = 20
        angle_speeds = []
        for x in range(0, width + 1):
            for y in range(-height, height + 1):
                d = math.dist(source, (x, y))
                if abs(d - radius) < 1.5 and (x, y) in arrival and arrival[(x, y)] > 0:
                    speed = d / arrival[(x, y)]
                    angle = math.degrees(math.atan2(y, x))
                    angle_speeds.append((angle, speed))

        angle_speeds.sort()
        speeds = [s for _, s in angle_speeds]
        aniso = (max(speeds) - min(speeds)) / min(speeds) * 100 if speeds else 0

        print(f"  Signal speed anisotropy at radius {radius}: {aniso:.4f}%")
        print(f"  Speed range: [{min(speeds):.6f}, {max(speeds):.6f}]")
        print()

        # Action/distance for specific angles
        test_targets = [
            ((20, 0), "0° (horizontal)"),
            ((14, 14), "45° (diagonal)"),
            ((17, 10), "~30°"),
            ((10, 17), "~60°"),
            ((7, 19), "~70°"),
        ]

        print(f"  {'target':>12s}  {'angle':>8s}  {'euclid':>8s}  {'arrival':>8s}  {'speed':>8s}  {'excess%':>8s}")
        print(f"  {'-' * 58}")

        for target, angle_label in test_targets:
            if target not in arrival:
                continue
            d = math.dist(source, target)
            t = arrival[target]
            speed = d / t
            excess = (1.0 / speed - 1.0) * 100
            print(f"  {str(target):>12s}  {angle_label:>8s}  {d:8.4f}  {t:8.4f}  {speed:8.6f}  {excess:7.4f}%")

    # Summary comparison
    print()
    print("=" * 72)
    print("SUMMARY: Anisotropy vs connectivity")
    print("=" * 72)
    print()
    print(f"  {'connectivity':>15s}  {'n_directions':>12s}  {'anisotropy%':>12s}")
    print(f"  {'-' * 42}")

    for max_step, label in [(1, "8-neighbor"), (2, "24-neighbor"), (3, "48-neighbor")]:
        arrival = compute_arrival_times(nodes, source, max_step)
        speeds = []
        for x in range(0, width + 1):
            for y in range(-height, height + 1):
                d = math.dist(source, (x, y))
                if abs(d - 20) < 1.5 and (x, y) in arrival and arrival[(x, y)] > 0:
                    speeds.append(d / arrival[(x, y)])

        center_nbs = get_neighbors((25, 0), nodes, max_step)
        aniso = (max(speeds) - min(speeds)) / min(speeds) * 100
        print(f"  {label:>15s}  {len(center_nbs):12d}  {aniso:11.4f}%")

    print()
    print("If anisotropy decreases: continuum limit via richer connectivity.")
    print("Prediction: anisotropy ~ 1/n_directions for large n.")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
