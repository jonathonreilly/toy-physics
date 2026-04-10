#!/usr/bin/env python3
"""Engineered layered-cycle gauge/current probe for the staggered graph lane.

Goal:
  Build a layered bipartite geometry with explicit, well-conditioned loop
  structure and test native flux-threaded current closure on the same
  staggered transport law.

This is intentionally narrow:
  - no 1D helpers
  - no slit-phase proxies
  - no centroid substitution
  - gauge/current is only scored on cycle-bearing families

The probe compares:
  - the current layered DAG holdout
  - an engineered layered brickwall/plaquette geometry
  - a wrapped layered cylinder variant with an explicit loop basis

The retained force battery is reused from the staggered graph portability lane.
"""

from __future__ import annotations

import math
import os
import random
import sys
from dataclasses import dataclass

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_graph_portability as port  # noqa: E402
import frontier_staggered_layered_backreaction as layered  # noqa: E402


@dataclass(frozen=True)
class GaugeResult:
    family: str
    n: int
    cycle: bool
    retained_passes: int
    current_span: float | None
    current_residual: float | None
    gauge_status: str
    force_sign: str
    fm_r2: float
    achrom_cv: float
    equiv_cv: float
    robust_toward: int
    robust_total: int


def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _finalize_adj(adj_sets: dict[int, set[int]]) -> dict[int, list[int]]:
    return {i: sorted(list(nbs)) for i, nbs in adj_sets.items()}


def _find_cycle_edge(adj: dict[int, list[int]]) -> tuple[int, int] | None:
    state: dict[int, int] = {}

    def dfs(node: int, prev: int | None) -> tuple[int, int] | None:
        state[node] = 1
        for nb in adj.get(node, []):
            if nb == prev:
                continue
            if nb not in state:
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


def _build_layered_brickwall(
    seed: int,
    *,
    layers: int,
    width: int,
    wrap_width: bool,
    name: str,
) -> port.GraphFamily:
    rng = random.Random(seed)
    coords: list[tuple[float, float]] = []
    colors: list[int] = []
    index: dict[tuple[int, int], int] = {}
    layer_nodes: list[list[int]] = []
    idx = 0

    for layer in range(layers):
        this_layer: list[int] = []
        for col in range(width):
            x = float(layer) + 0.03 * (rng.random() - 0.5)
            y = float(col) + 0.06 * (rng.random() - 0.5)
            coords.append((x, y))
            colors.append(layer % 2)
            index[(layer, col)] = idx
            this_layer.append(idx)
            idx += 1
        layer_nodes.append(this_layer)

    coords_a = np.asarray(coords, dtype=float)
    colors_a = np.asarray(colors, dtype=int)
    adj_sets: dict[int, set[int]] = {}

    # Brickwall pattern: every node connects forward to the same column and to
    # a staggered neighbor in the next layer. This creates explicit plaquettes
    # while keeping the graph bipartite.
    for layer in range(layers - 1):
        for col in range(width):
            a = index[(layer, col)]
            same = index[(layer + 1, col)]
            _add_edge(adj_sets, a, same)

            shift = 1 if layer % 2 == 0 else -1
            col2 = col + shift
            if wrap_width:
                col2 %= width
                b = index[(layer + 1, col2)]
                _add_edge(adj_sets, a, b)
            elif 0 <= col2 < width:
                b = index[(layer + 1, col2)]
                _add_edge(adj_sets, a, b)

    # Add a second staggered pass every other layer to strengthen loop closure
    # without changing bipartite parity.
    for layer in range(0, layers - 2, 2):
        for col in range(width):
            a = index[(layer, col)]
            col2 = (col + 1) % width if wrap_width else col + 1
            if 0 <= col2 < width:
                b = index[(layer + 2, col2)]
                _add_edge(adj_sets, a, b)

    adj = _finalize_adj(adj_sets)
    source = layer_nodes[0][0]
    detector = layer_nodes[-1][:]

    depth = np.full(len(coords_a), np.inf)
    depth[source] = 0.0
    q = [source]
    while q:
        i = q.pop(0)
        for j in adj.get(i, []):
            if depth[j] != np.inf:
                continue
            depth[j] = depth[i] + 1.0
            q.append(j)

    cycle_edge = _find_cycle_edge(adj)
    return port.GraphFamily(
        name=name,
        positions=coords_a,
        colors=colors_a,
        adj=adj,
        source=source,
        detector=detector,
        depth=depth,
        has_cycle=cycle_edge is not None,
        cycle_edge=cycle_edge,
    )


def _gauge_current(graph: port.GraphFamily) -> tuple[float | None, float | None, str]:
    if not graph.has_cycle or graph.cycle_edge is None:
        return None, None, "N/A"

    phi_vals = np.linspace(0.0, 2.0 * math.pi, 9)
    currents: list[float] = []
    for phi in phi_vals:
        H_phi = port._build_hamiltonian(
            graph,
            port.MASS,
            port.SOURCE_STRENGTH,
            flux=phi,
            flux_edge=graph.cycle_edge,
        )
        evals, evecs = np.linalg.eigh(H_phi.toarray())
        gs = evecs[:, 0]
        i, j = graph.cycle_edge
        hop = H_phi[i, j]
        currents.append(float(np.imag(np.conj(gs[i]) * hop * gs[j])))

    span = float(max(currents) - min(currents))
    resid = float(abs(currents[0] - currents[-1]))
    status = "PASS" if span > 1e-4 and resid < 1e-8 else "FAIL"
    return span, resid, status


def _measure(graph: port.GraphFamily) -> GaugeResult:
    retained = port._measure_family(graph)
    current_span, current_residual, gauge_status = _gauge_current(graph)
    retained_passes = sum(
        [
            retained.born_lin < 1e-10,
            retained.norm_drift < 1e-10,
            retained.force_value > 0.0,
            retained.fm_r2 > 0.9,
            retained.achrom_cv < 0.05,
            retained.equiv_cv < 0.05,
            retained.robust_toward == retained.robust_total,
            retained.gauge_status in ("PASS", "N/A"),
        ]
    )

    return GaugeResult(
        family=graph.name,
        n=graph.positions.shape[0],
        cycle=graph.has_cycle,
        retained_passes=retained_passes,
        current_span=current_span,
        current_residual=current_residual,
        gauge_status=gauge_status,
        force_sign="TOWARD" if retained.force_value > 0 else "AWAY" if retained.force_value < 0 else "ZERO",
        fm_r2=retained.fm_r2,
        achrom_cv=retained.achrom_cv,
        equiv_cv=retained.equiv_cv,
        robust_toward=retained.robust_toward,
        robust_total=retained.robust_total,
    )


def _families() -> list[port.GraphFamily]:
    return [
        layered._build_layered_family(seed=13, layers=8, width=5, fanout=1),
        layered._build_layered_family(seed=29, layers=10, width=6, fanout=2),
        _build_layered_brickwall(41, layers=8, width=6, wrap_width=False, name="layered_brickwall_open"),
        _build_layered_brickwall(43, layers=8, width=6, wrap_width=True, name="layered_brickwall_wrap"),
    ]


def main() -> None:
    print("=" * 96)
    print("STAGGERED LAYERED GAUGE ENGINEERING")
    print("  Native flux-threaded current on layered cycle geometries")
    print("  Retained force battery reused from the staggered graph lane")
    print("=" * 96)
    print(f"  dt={port.DT}, steps={port.N_STEPS}, mass={port.MASS}, source_strength={port.SOURCE_STRENGTH}")
    print()

    results: list[GaugeResult] = []
    for graph in _families():
        result = _measure(graph)
        results.append(result)
        cycle_txt = "yes" if result.cycle else "no"
        span_txt = "N/A" if result.current_span is None else f"{result.current_span:.3e}"
        resid_txt = "N/A" if result.current_residual is None else f"{result.current_residual:.3e}"
        print(
            f"{result.family:<34} "
            f"n={result.n:<3d} "
            f"cycle={cycle_txt} "
            f"retained={result.retained_passes}/8 "
            f"force={result.force_sign} "
            f"F~M={result.fm_r2:.3f} "
            f"achrom={result.achrom_cv:.3e} "
            f"equiv={result.equiv_cv:.3e} "
            f"robust={result.robust_toward}/{result.robust_total} "
            f"J_span={span_txt} "
            f"J_resid={resid_txt} "
            f"gauge={result.gauge_status}"
        )

    cycle_results = [r for r in results if r.current_span is not None and r.gauge_status != "N/A"]
    print()
    print("CLOSURE")
    if cycle_results:
        best = max(cycle_results, key=lambda r: r.current_span or -1.0)
        print(
            f"  best geometry: {best.family} "
            f"(current span={best.current_span:.3e}, residual={best.current_residual:.3e})"
        )
        print("  observable: ground-state persistent-current span over phi in [0, 2pi]")
        print("  operator: native staggered Hamiltonian with flux threaded through the detected cycle edge")
    else:
        print("  no cycle-bearing family produced a scored current observable")

    print()
    print("Interpretation:")
    print("  - Gauge/current is only scored on cycle-bearing layered graphs.")
    print("  - The DAG-compatible holdout remains N/A for gauge/current.")
    print("  - Force remains the primary gravity observable; current is the gauge observable.")


if __name__ == "__main__":
    main()
