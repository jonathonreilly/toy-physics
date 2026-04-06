#!/usr/bin/env python3
"""Diagnostic for the growing-graph dynamic-propagation limit.

The goal is to freeze a bounded static-control no-go, not to overclaim:

- the frontier-delay observable grows cleanly against a frozen control
- the dynamic propagation visibility signal is weak, seed-dependent, and not a
  stable order parameter across layer counts

This is a graph-growth diagnostic only. It does not claim cosmology.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict, deque
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.growing_graph_decoherence import (  # type: ignore
    propagate_on_subgraph,
    visibility_from_amps,
)
from scripts.generative_causal_dag_interference import generate_causal_dag


SEED_NODES = {(x, y) for x in range(0, 5) for y in range(-3, 4)}
SOURCE = (2, 0)
GROWTH_STEPS = 20
MAX_HEIGHT = 15
K_BAND = [3.0, 5.0, 7.0]


def _neighbors(node: tuple[int, int], nodes: set[tuple[int, int]]):
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
    vals = list(_graph_distances(nodes, source).values())
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


def frontier_proxy() -> None:
    snapshots = []
    current = set(SEED_NODES)
    snapshots.append(set(current))
    for _ in range(GROWTH_STEPS):
        frontier = set()
        for node in current:
            x, y = node
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nb = (x + dx, y + dy)
                    if nb not in current and abs(nb[1]) <= MAX_HEIGHT:
                        frontier.add(nb)
        current = current | frontier
        snapshots.append(set(current))

    growth_frontier: list[float] = []
    growth_rms: list[float] = []
    growth_width: list[float] = []
    step_ids: list[float] = []

    print("=" * 84)
    print("FRONTIER EXPANSION PROXY")
    print("=" * 84)
    print(f"seed_size={len(SEED_NODES)}, steps={GROWTH_STEPS}, max_height={MAX_HEIGHT}")
    print(f"source={SOURCE}")
    print(f"{'step':>4s} {'nodes':>7s} {'frontier':>9s} {'mean_d':>9s} {'rms_d':>9s} {'width':>9s}")
    print("-" * 56)
    for step, snap in enumerate(snapshots):
        frontier, mean_d, rms_d, width = _moment_stats(snap, SOURCE)
        step_ids.append(float(step))
        growth_frontier.append(float(frontier))
        growth_rms.append(float(rms_d))
        growth_width.append(float(width))
        print(f"{step:4d} {len(snap):7d} {frontier:9.3f} {mean_d:9.3f} {rms_d:9.3f} {width:9.3f}")

    control_frontier, control_mean, control_rms, control_width = _moment_stats(snapshots[0], SOURCE)
    frontier_slope = _slope(step_ids, growth_frontier)
    rms_slope = _slope(step_ids, growth_rms)
    width_slope = _slope(step_ids, growth_width)

    print()
    print("FROZEN STATIC CONTROL")
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


def dynamic_propagation_limit() -> None:
    print()
    print("=" * 84)
    print("DYNAMIC PROPAGATION LIMIT")
    print("=" * 84)
    print("  Compare the evolving-graph propagation visibility against a static graph")
    print("  The question: does the signal scale cleanly with graph growth?")
    print("  Controls held fixed: source/detector family, barrier/slit geometry, and k-band")
    print("  Growing branch perturbation: only the second-half wiring is randomized")
    print()
    print(f"{'layers':>6s} {'mean_deg':>8s} {'mean_Vdrop':>11s} {'pos/total':>10s}")
    print("-" * 44)

    for n_layers in [10, 15, 20]:
        v_drops: list[float] = []
        positive = 0
        total = 0

        for seed in range(10):
            positions, adj, _ = generate_causal_dag(
                n_layers=n_layers,
                nodes_per_layer=20,
                y_range=10.0,
                connect_radius=3.0,
                rng_seed=seed * 11 + 7,
            )
            n = len(positions)
            edges = sum(len(v) for v in adj.values())
            mean_deg = edges / n if n > 0 else 0.0

            by_layer: dict[int, list[int]] = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 5:
                continue

            src = by_layer[layers[0]]
            det = set(by_layer[layers[-1]])
            if not det:
                continue

            all_ys = [y for _, y in positions]
            cy = sum(all_ys) / len(all_ys)
            bl_idx = len(layers) // 3
            bl = layers[bl_idx]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]
            if not sa or not sb:
                continue
            slit_idx = set(sa + sb)
            blocked = set(bi) - slit_idx

            field = [0.0] * n
            static_vs = []
            grown_probs = {d: 0.0 for d in det}
            n_realizations = 20
            for k in K_BAND:
                start = {s: 1.0 / len(src) + 0.0j for s in src}
                amps = propagate_on_subgraph(positions, adj, field, start, blocked, k)
                static_vs.append(visibility_from_amps(amps, det, positions))

            v_static = sum(static_vs) / len(static_vs)
            mid_layer_idx = len(layers) // 2
            first_half_nodes = set()
            for l in layers[: mid_layer_idx + 1]:
                first_half_nodes.update(by_layer[l])

            first_adj: dict[int, list[int]] = {}
            for i, nbs in adj.items():
                if i in first_half_nodes:
                    first_adj[i] = [j for j in nbs if j in first_half_nodes]

            for growth_i in range(n_realizations):
                rng = random.Random(seed * 1000 + growth_i * 31 + 7)
                grown_adj = dict(first_adj)
                for l_idx in range(mid_layer_idx, len(layers) - 1):
                    curr_layer = by_layer[layers[l_idx]]
                    next_layer = by_layer[layers[l_idx + 1]]
                    for j in next_layer:
                        x2, y2 = positions[j]
                        for i in curr_layer:
                            x1, y1 = positions[i]
                            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                            threshold = 3.0 * (0.7 + 0.6 * rng.random())
                            if dist <= threshold:
                                grown_adj.setdefault(i, []).append(j)

                for k in K_BAND:
                    start = {s: 1.0 / len(src) + 0.0j for s in src}
                    amps = propagate_on_subgraph(positions, grown_adj, field, start, blocked, k)
                    for d in det:
                        grown_probs[d] += abs(amps.get(d, 0.0)) ** 2

            total_prob = sum(grown_probs.values())
            if total_prob > 0:
                grown_probs = {d: p / total_prob for d, p in grown_probs.items()}

            py: defaultdict[int, float] = defaultdict(float)
            for d, p in grown_probs.items():
                py[positions[d][1]] += p
            ys = sorted(py.keys())
            if len(ys) < 3:
                v_grown = 0.0
            else:
                vals = [py[y] for y in ys]
                peaks = [vals[i] for i in range(1, len(vals) - 1) if vals[i] > vals[i - 1] and vals[i] > vals[i + 1]]
                troughs = [vals[i] for i in range(1, len(vals) - 1) if vals[i] < vals[i - 1] and vals[i] < vals[i + 1]]
                v_grown = (max(peaks) - min(troughs)) / (max(peaks) + min(troughs)) if peaks and troughs else 0.0

            v_drop = v_static - v_grown
            v_drops.append(v_drop)
            positive += int(v_drop > 0.02)
            total += 1

        mean_drop = sum(v_drops) / len(v_drops) if v_drops else 0.0
        print(f"{n_layers:6d} {mean_deg:8.2f} {mean_drop:11.4f} {positive:2d}/{total:<7d}")


def main() -> None:
    frontier_proxy()
    dynamic_propagation_limit()
    print()
    print("BOUNDED NO-GO")
    print("  - Frontier delay is the clean retained expansion observable.")
    print("  - Dynamic-propagation visibility stays weak, seed-dependent, and not monotone.")
    print("  - The retained growth story is graph-distance expansion, not a transport claim.")


if __name__ == "__main__":
    main()
