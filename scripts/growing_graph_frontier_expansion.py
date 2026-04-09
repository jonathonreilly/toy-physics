#!/usr/bin/env python3
"""Growing-graph frontier expansion proxy on the existing prototype family.

This is intentionally narrow:

- start from the existing growing-graph prototype
- compare it to a static no-growth control
- track one observable only: frontier delay growth

The observable is the unweighted graph-distance frontier delay from a fixed
seed center to the farthest node in each snapshot.

This is a graph-expansion proxy, not a cosmology claim.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import deque
from typing import Iterable

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.evolving_network_prototype import grow_network


SEED_NODES = {(x, y) for x in range(0, 5) for y in range(-3, 4)}
SOURCE = (2, 0)
GROWTH_STEPS = 20
MAX_HEIGHT = 15


def _neighbors(node: tuple[int, int], nodes: set[tuple[int, int]]) -> Iterable[tuple[int, int]]:
    x, y = node
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nb = (x + dx, y + dy)
            if nb in nodes:
                yield nb


def _graph_distances(nodes: set[tuple[int, int]], source: tuple[int, int]) -> dict[tuple[int, int], int]:
    if source not in nodes:
        raise ValueError(f"source {source} is not in the node set")
    dist = {source: 0}
    q = deque([source])
    while q:
        node = q.popleft()
        for nb in _neighbors(node, nodes):
            if nb in dist:
                continue
            dist[nb] = dist[node] + 1
            q.append(nb)
    return dist


def _moment_stats(nodes: set[tuple[int, int]], source: tuple[int, int]) -> tuple[int, float, float, float]:
    dists = _graph_distances(nodes, source).values()
    vals = list(dists)
    frontier = max(vals)
    mean = statistics.fmean(vals)
    width = statistics.pstdev(vals) if len(vals) > 1 else 0.0
    rms = math.sqrt(statistics.fmean([v * v for v in vals]))
    return frontier, mean, rms, width


def _slope(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0
    xbar = statistics.fmean(xs)
    ybar = statistics.fmean(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom <= 1e-30:
        return 0.0
    numer = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    return numer / denom


def main() -> None:
    snapshots = grow_network(SEED_NODES, growth_steps=GROWTH_STEPS, max_height=MAX_HEIGHT)
    frozen_control = snapshots[0]

    print("=" * 84)
    print("GROWING-GRAPH FRONTIER EXPANSION PROXY")
    print("  Static graph control vs growing-graph frontier delay")
    print("=" * 84)
    print(f"seed_size={len(SEED_NODES)}, steps={GROWTH_STEPS}, max_height={MAX_HEIGHT}")
    print(f"source={SOURCE}")
    print()

    growth_frontier: list[float] = []
    growth_rms: list[float] = []
    growth_width: list[float] = []
    step_ids: list[float] = []

    print(f"{'step':>4s} {'nodes':>7s} {'frontier':>9s} {'mean_d':>9s} {'rms_d':>9s} {'width':>9s}")
    print("-" * 56)
    for step, snap in enumerate(snapshots):
        frontier, mean_d, rms_d, width = _moment_stats(snap, SOURCE)
        step_ids.append(float(step))
        growth_frontier.append(float(frontier))
        growth_rms.append(float(rms_d))
        growth_width.append(float(width))
        print(f"{step:4d} {len(snap):7d} {frontier:9.3f} {mean_d:9.3f} {rms_d:9.3f} {width:9.3f}")

    control_frontier, control_mean, control_rms, control_width = _moment_stats(frozen_control, SOURCE)
    frontier_slope = _slope(step_ids, growth_frontier)
    rms_slope = _slope(step_ids, growth_rms)
    width_slope = _slope(step_ids, growth_width)

    print()
    print("STATIC CONTROL")
    print(f"  frozen step-0 graph: nodes={len(frozen_control)}")
    print(f"  frontier delay: {control_frontier:.3f}")
    print(f"  mean delay:     {control_mean:.3f}")
    print(f"  rms delay:      {control_rms:.3f}")
    print(f"  width:          {control_width:.3f}")

    print()
    print("GROWTH SUMMARY")
    print(f"  frontier slope vs step: {frontier_slope:+.4f} hops/step")
    print(f"  rms slope vs step:      {rms_slope:+.4f} hops/step")
    print(f"  width slope vs step:    {width_slope:+.4f} hops/step")
    print(f"  final frontier / control frontier: {growth_frontier[-1] / max(control_frontier, 1):.3f}x")

    print()
    print("SAFE READ")
    print("  - The growing graph shows a monotone frontier-delay increase.")
    print("  - The static control is frozen and does not generate expansion by itself.")
    print("  - This is a graph-expansion proxy only; it does not claim cosmological expansion.")


if __name__ == "__main__":
    main()
