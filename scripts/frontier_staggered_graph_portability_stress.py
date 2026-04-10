#!/usr/bin/env python3
"""Staggered graph portability stress probe.

Goal:
  Push the retained staggered / Kahler-Dirac portability result onto larger,
  more irregular, and less forgiving bipartite graph families.

This keeps the same retained battery as the baseline portability probe:
  - Born/linearity
  - norm preservation
  - gravity sign
  - F∝M
  - achromatic force
  - equivalence
  - robustness
  - native gauge response if a cycle exists

The point is not to retune the model. The point is to see where the baseline
stops being portable once the graphs get bigger and less regular.
"""

from __future__ import annotations

import math
import os
import random
import sys
from collections import deque

import numpy as np


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_graph_portability as base


def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _adj_to_lists(adj_sets: dict[int, set[int]]) -> dict[int, list[int]]:
    return {i: sorted(list(nbs)) for i, nbs in adj_sets.items()}


def _bfs_depth(adj: dict[int, list[int]], source: int, n: int) -> np.ndarray:
    depth = np.full(n, np.inf)
    depth[source] = 0.0
    q = deque([source])
    while q:
        i = q.popleft()
        for j in adj.get(i, []):
            if depth[j] != np.inf:
                continue
            depth[j] = depth[i] + 1.0
            q.append(j)
    return depth


def _ensure_connected(
    adj_sets: dict[int, set[int]],
    coords: np.ndarray,
    colors: np.ndarray,
    source: int,
) -> dict[int, list[int]]:
    """Bridge disconnected components with the nearest opposite-color node."""

    def reachable() -> set[int]:
        adj = _adj_to_lists(adj_sets)
        depth = _bfs_depth(adj, source, coords.shape[0])
        return {i for i, d in enumerate(depth) if np.isfinite(d)}

    while True:
        seen = reachable()
        if len(seen) == coords.shape[0]:
            return _adj_to_lists(adj_sets)

        missing = next(i for i in range(coords.shape[0]) if i not in seen)
        best_j = None
        best_d = float("inf")
        for j in seen:
            if colors[j] == colors[missing]:
                continue
            dx = coords[j, 0] - coords[missing, 0]
            dy = coords[j, 1] - coords[missing, 1]
            d = math.hypot(dx, dy)
            if d < best_d:
                best_d = d
                best_j = j
        if best_j is None:
            best_j = min(seen)
        _add_edge(adj_sets, missing, best_j)


def _find_cycle_edge(adj: dict[int, list[int]]) -> tuple[int, int] | None:
    parent: dict[int, int] = {}
    state: dict[int, int] = {}

    def dfs(node: int, prev: int | None) -> tuple[int, int] | None:
        state[node] = 1
        for nb in adj.get(node, []):
            if nb == prev:
                continue
            if nb not in state:
                parent[nb] = node
                hit = dfs(nb, node)
                if hit is not None:
                    return hit
            elif state[nb] == 1:
                return (node, nb)
        state[node] = 2
        return None

    for start in sorted(adj):
        if start in state:
            continue
        hit = dfs(start, None)
        if hit is not None:
            return hit
    return None


def _graph_stats(adj: dict[int, list[int]]) -> tuple[int, float]:
    edges = sum(len(nbs) for nbs in adj.values()) // 2
    degs = [len(nbs) for nbs in adj.values()]
    avg_deg = float(sum(degs)) / max(len(degs), 1)
    return edges, avg_deg


def _bipartite_random_geometric_stress(seed: int, side: int = 9) -> base.GraphFamily:
    rng = random.Random(seed)
    coords = []
    colors = []
    index = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            px = x + 0.22 * (rng.random() - 0.5)
            py = y + 0.22 * (rng.random() - 0.5)
            coords.append((px, py))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    adj_sets: dict[int, set[int]] = {}

    # A larger, noisier version of the retained random geometric family.
    radius = 2.45
    k_max = 4
    for i in range(side):
        for j in range(side):
            a = index[(i, j)]
            scored: list[tuple[float, int]] = []
            for ii in range(side):
                for jj in range(side):
                    b = index[(ii, jj)]
                    if a == b or colors_a[a] == colors_a[b]:
                        continue
                    dx = coords_a[b, 0] - coords_a[a, 0]
                    dy = coords_a[b, 1] - coords_a[a, 1]
                    d = math.hypot(dx, dy)
                    if d <= radius:
                        scored.append((d, b))
            scored.sort(key=lambda t: (t[0], t[1]))
            for _, b in scored[:k_max]:
                _add_edge(adj_sets, a, b)

    source = index[(0, 0)]
    adj = _ensure_connected(adj_sets, coords_a, colors_a, source)
    depth = _bfs_depth(adj, source, len(coords_a))
    detector = [i for i, d in enumerate(depth) if np.isfinite(d) and d == np.nanmax(depth)]
    cycle_edge = _find_cycle_edge(adj)
    return base.GraphFamily(
        f"bipartite_random_geometric_stress_s{seed}_n{len(coords_a)}",
        coords_a,
        colors_a,
        adj,
        source,
        detector,
        depth,
        cycle_edge is not None,
        cycle_edge,
    )


def _bipartite_growing_stress(seed: int, layers: int = 11) -> base.GraphFamily:
    rng = random.Random(seed)
    widths = [5, 8, 6, 9, 7, 10, 7, 9, 6, 8, 7]
    coords = []
    colors = []
    layer_nodes: list[list[int]] = []
    idx = 0
    for layer in range(layers):
        width = widths[layer % len(widths)]
        this_layer = []
        for k in range(width):
            y = (k - (width - 1) / 2.0) + 0.24 * (rng.random() - 0.5)
            x = float(layer) + 0.05 * (rng.random() - 0.5)
            coords.append((x, y))
            colors.append(layer % 2)
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    adj_sets: dict[int, set[int]] = {}

    for layer in range(layers - 1):
        curr = layer_nodes[layer]
        nxt = layer_nodes[layer + 1]
        for pos, i in enumerate(curr):
            scored = []
            fanout = 2 + int(rng.random() < 0.45)
            for j in nxt:
                dx = coords_a[j, 0] - coords_a[i, 0]
                dy = coords_a[j, 1] - coords_a[i, 1]
                scored.append((dx * dx + 0.35 * dy * dy + 0.02 * rng.random(), j))
            scored.sort(key=lambda t: (t[0], t[1]))
            for _, j in scored[:fanout]:
                _add_edge(adj_sets, i, j)

        # Keep the next layer connected even when the branching is sparse.
        for j in nxt:
            if j not in adj_sets:
                best_i = min(
                    curr,
                    key=lambda i: (
                        (coords_a[j, 0] - coords_a[i, 0]) ** 2
                        + (coords_a[j, 1] - coords_a[i, 1]) ** 2,
                        i,
                    ),
                )
                _add_edge(adj_sets, best_i, j)

    source = layer_nodes[0][0]
    adj = _ensure_connected(adj_sets, coords_a, colors_a, source)
    depth = _bfs_depth(adj, source, len(coords_a))
    detector = layer_nodes[-1][:]
    cycle_edge = _find_cycle_edge(adj)
    return base.GraphFamily(
        f"bipartite_growing_stress_s{seed}_n{len(coords_a)}",
        coords_a,
        colors_a,
        adj,
        source,
        detector,
        depth,
        cycle_edge is not None,
        cycle_edge,
    )


def _bipartite_chorded_grid_stress(seed: int, side: int = 12) -> base.GraphFamily:
    rng = random.Random(seed)
    coords = []
    colors = []
    index = {}
    idx = 0
    for x in range(side):
        for y in range(side):
            px = x + 0.04 * (rng.random() - 0.5)
            py = y + 0.04 * (rng.random() - 0.5)
            coords.append((px, py))
            colors.append((x + y) % 2)
            index[(x, y)] = idx
            idx += 1
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    adj_sets: dict[int, set[int]] = {}

    # Base checkerboard grid.
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            for dx, dy in ((1, 0), (0, 1)):
                xx, yy = x + dx, y + dy
                if (xx, yy) not in index:
                    continue
                b = index[(xx, yy)]
                if colors_a[a] != colors_a[b]:
                    _add_edge(adj_sets, a, b)

    # Add irregular odd-parity chords to create longer cycle structure.
    for x in range(side):
        for y in range(side):
            a = index[(x, y)]
            candidates: list[tuple[float, int]] = []
            for xx in range(side):
                for yy in range(side):
                    b = index[(xx, yy)]
                    if a == b or colors_a[a] == colors_a[b]:
                        continue
                    manhattan = abs(xx - x) + abs(yy - y)
                    if manhattan < 3 or manhattan > 7 or manhattan % 2 == 0:
                        continue
                    dx = coords_a[b, 0] - coords_a[a, 0]
                    dy = coords_a[b, 1] - coords_a[a, 1]
                    d = math.hypot(dx, dy)
                    candidates.append((d, b))
            candidates.sort(key=lambda t: (t[0], t[1]))
            keep = 1 + int(rng.random() < 0.35)
            for _, b in candidates[:keep]:
                _add_edge(adj_sets, a, b)

    source = index[(0, 0)]
    adj = _ensure_connected(adj_sets, coords_a, colors_a, source)
    depth = _bfs_depth(adj, source, len(coords_a))
    detector = [i for i, d in enumerate(depth) if np.isfinite(d) and d == np.nanmax(depth)]
    cycle_edge = _find_cycle_edge(adj)
    return base.GraphFamily(
        f"bipartite_chorded_grid_stress_s{seed}_n{len(coords_a)}",
        coords_a,
        colors_a,
        adj,
        source,
        detector,
        depth,
        cycle_edge is not None,
        cycle_edge,
    )


def _layered_bipartite_dag_stress(seed: int, layers: int = 11) -> base.GraphFamily:
    rng = random.Random(seed)
    widths = list(range(1, layers + 1))
    coords = []
    colors = []
    layer_nodes: list[list[int]] = []
    idx = 0
    for layer in range(layers):
        width = widths[layer % len(widths)]
        count = width
        this_layer = []
        for k in range(count):
            x = float(layer) + 0.04 * (rng.random() - 0.5)
            y = (k - (count - 1) / 2.0) + 0.18 * (rng.random() - 0.5)
            coords.append((x, y))
            colors.append(layer % 2)
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)
    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    adj_sets: dict[int, set[int]] = {}

    for layer in range(layers - 1):
        curr = layer_nodes[layer]
        nxt = layer_nodes[layer + 1]
        # Each node in the current layer gets at least one unique child and
        # some nodes get one extra child if the next layer is wider. That keeps
        # the layered graph connected while remaining acyclic as an undirected
        # graph.
        child_allocation = [1] * len(curr)
        extra = max(0, len(nxt) - len(curr))
        for k in range(extra):
            child_allocation[k % len(curr)] += 1

        child_idx = 0
        for pos, i in enumerate(curr):
            n_children = child_allocation[pos]
            scored = []
            for j in nxt[child_idx : child_idx + n_children]:
                dx = coords_a[j, 0] - coords_a[i, 0]
                dy = coords_a[j, 1] - coords_a[i, 1]
                scored.append((dx * dx + 0.20 * dy * dy + 0.03 * rng.random(), j))
            scored.sort(key=lambda t: (t[0], t[1]))
            for _, j in scored[:n_children]:
                _add_edge(adj_sets, i, j)
            child_idx += n_children

        # The graph stays acyclic because each child is assigned once and only
        # to the immediately preceding layer.

    source = layer_nodes[0][0]
    adj = _adj_to_lists(adj_sets)
    depth = _bfs_depth(adj, source, len(coords_a))
    detector = layer_nodes[-1][:]
    cycle_edge = None
    return base.GraphFamily(
        f"layered_bipartite_dag_stress_s{seed}_n{len(coords_a)}",
        coords_a,
        colors_a,
        adj,
        source,
        detector,
        depth,
        cycle_edge is not None,
        cycle_edge,
    )


def _stress_graphs() -> list[base.GraphFamily]:
    return [
        _bipartite_random_geometric_stress(17, side=9),
        _bipartite_growing_stress(23, layers=11),
        _bipartite_chorded_grid_stress(31, side=12),
        _layered_bipartite_dag_stress(47, layers=11),
    ]


def _retained_pass_rows(result: base.FamilyResult) -> list[str]:
    rows = [
        ("Born/linearity", result.born_lin < 1e-10),
        ("norm", result.norm_drift < 1e-10),
        ("force sign", result.force_value > 0),
        ("F∝M", result.fm_r2 > 0.9),
        ("achromatic force", result.achrom_cv < 0.05),
        ("equivalence", result.equiv_cv < 0.05),
        ("robustness", result.robust_toward == result.robust_total),
        ("gauge", result.gauge_status in ("PASS", "N/A")),
    ]
    return [name for name, ok in rows if not ok]


def main() -> None:
    print("=" * 96)
    print("STAGGERED GRAPH PORTABILITY STRESS")
    print("  Larger, more irregular bipartite families with the same retained battery")
    print("=" * 96)
    print(f"  dt={base.DT}, steps={base.N_STEPS}, mass={base.MASS}, G={base.G}, source_strength={base.SOURCE_STRENGTH}")
    print()

    results = []
    for graph in _stress_graphs():
        edges, avg_deg = _graph_stats(graph.adj)
        print(f"{graph.name:<40} |V|={graph.positions.shape[0]:<3d} |E|={edges:<4d} avg_deg={avg_deg:.2f} cycle={graph.has_cycle}")
        result = base._measure_family(graph)
        results.append(result)
        base._print_result(result)
        failures = _retained_pass_rows(result)
        if failures:
            print(f"  failures: {', '.join(failures)}")
        else:
            print("  failures: none")
        print()

    print("SUMMARY")
    for result in results:
        failures = _retained_pass_rows(result)
        pass_rows = 8 - len(failures)
        gauge = result.gauge_status
        print(
            f"  {result.family:<40} {pass_rows}/8 retained rows pass "
            f"(gauge={gauge}; failures={'none' if not failures else ', '.join(failures)})"
        )

    print()
    print("Interpretation:")
    print("  - This is a stress probe, not a new canonical card.")
    print("  - Gauge is only scored when the graph family has a cycle.")
    print("  - Any failure here is a portability failure, not a retuning prompt.")


if __name__ == "__main__":
    main()
