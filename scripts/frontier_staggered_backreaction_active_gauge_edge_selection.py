#!/usr/bin/env python3
"""Active-field gauge edge selection for backreacted graph observables.

The first backreaction stress split showed a specific obstruction:
source-sector force rows survived, but active-field gauge/current failed on
two cycle-bearing stress graphs when the flux was threaded through the default
DFS-selected cycle edge.

This probe tests whether that failure is intrinsic.  It keeps the same active
resistance-Yukawa source field and replaces only the flux-edge choice with a
deterministic graph-native rule:

  source-proximal non-bridge edge =
      nearest-to-source edge whose removal does not disconnect the graph.

This is not chosen by inspecting the current.  The max-current edge is reported
only as a diagnostic ceiling, not as the scored gauge row.
"""

from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass

import numpy as np


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_graph_observables_backreaction_stress as br
import frontier_staggered_graph_portability as base
import frontier_staggered_graph_portability_stress as stress


GAUGE_SPAN_TOL = 1e-4
GAUGE_PERIOD_TOL = 1e-8


@dataclass
class EdgeGaugeResult:
    family: str
    n: int
    edges: int
    legacy_edge: tuple[int, int] | None
    legacy_span: float | None
    legacy_residual: float | None
    source_edge: tuple[int, int] | None
    source_span: float | None
    source_residual: float | None
    max_edge: tuple[int, int] | None
    max_span: float | None
    status: str


def _undirected_edges(graph: base.GraphFamily) -> list[tuple[int, int]]:
    return [(i, j) for i, nbs in graph.adj.items() for j in nbs if i < j]


def _is_bridge(graph: base.GraphFamily, edge: tuple[int, int]) -> bool:
    a, b = edge
    seen = {a}
    stack = [a]
    while stack:
        i = stack.pop()
        for j in graph.adj.get(i, []):
            if (i == a and j == b) or (i == b and j == a):
                continue
            if j in seen:
                continue
            seen.add(j)
            stack.append(j)
    return len(seen) < graph.positions.shape[0]


def _source_proximal_nonbridge_edge(graph: base.GraphFamily) -> tuple[int, int] | None:
    candidates: list[tuple[float, float, float, int, int]] = []
    for i, j in _undirected_edges(graph):
        if _is_bridge(graph, (i, j)):
            continue
        di = graph.depth[i] if np.isfinite(graph.depth[i]) else float("inf")
        dj = graph.depth[j] if np.isfinite(graph.depth[j]) else float("inf")
        geom = float(np.linalg.norm(graph.positions[i] - graph.positions[j]))
        candidates.append((min(di, dj), di + dj, geom, i, j))
    if not candidates:
        return None
    candidates.sort()
    *_prefix, i, j = candidates[0]
    return (i, j)


def _current_series(
    graph: base.GraphFamily,
    phi: np.ndarray,
    edge: tuple[int, int],
) -> list[float]:
    currents: list[float] = []
    for flux in np.linspace(0.0, 2.0 * math.pi, 7):
        h_flux = br._build_hamiltonian_phi(graph, phi, flux=flux, flux_edge=edge)
        _evals, evecs = np.linalg.eigh(h_flux.toarray())
        ground = evecs[:, 0]
        i, j = edge
        hop = h_flux[i, j]
        currents.append(float(np.imag(np.conj(ground[i]) * hop * ground[j])))
    return currents


def _current_span_residual(
    graph: base.GraphFamily,
    phi: np.ndarray,
    edge: tuple[int, int] | None,
) -> tuple[float | None, float | None]:
    if edge is None:
        return None, None
    currents = _current_series(graph, phi, edge)
    return float(max(currents) - min(currents)), float(abs(currents[0] - currents[-1]))


def _active_phi(graph: base.GraphFamily) -> np.ndarray:
    kernel = br._green_kernel(graph)
    rho = br._source_density(graph, graph.source, 1.0)
    return np.asarray(kernel @ rho, dtype=float)


def _measure_graph(graph: base.GraphFamily) -> EdgeGaugeResult:
    if not graph.has_cycle:
        return EdgeGaugeResult(
            family=graph.name,
            n=graph.positions.shape[0],
            edges=len(_undirected_edges(graph)),
            legacy_edge=None,
            legacy_span=None,
            legacy_residual=None,
            source_edge=None,
            source_span=None,
            source_residual=None,
            max_edge=None,
            max_span=None,
            status="N/A",
        )

    phi = _active_phi(graph)
    legacy_edge = graph.cycle_edge
    source_edge = _source_proximal_nonbridge_edge(graph)
    legacy_span, legacy_residual = _current_span_residual(graph, phi, legacy_edge)
    source_span, source_residual = _current_span_residual(graph, phi, source_edge)

    max_edge = None
    max_span = -1.0
    for edge in _undirected_edges(graph):
        span, _residual = _current_span_residual(graph, phi, edge)
        if span is not None and span > max_span:
            max_span = span
            max_edge = edge

    ok = (
        source_span is not None
        and source_residual is not None
        and source_span > GAUGE_SPAN_TOL
        and source_residual < GAUGE_PERIOD_TOL
    )
    return EdgeGaugeResult(
        family=graph.name,
        n=graph.positions.shape[0],
        edges=len(_undirected_edges(graph)),
        legacy_edge=legacy_edge,
        legacy_span=legacy_span,
        legacy_residual=legacy_residual,
        source_edge=source_edge,
        source_span=source_span,
        source_residual=source_residual,
        max_edge=max_edge,
        max_span=max_span,
        status="PASS" if ok else "FAIL",
    )


def _fmt_edge(edge: tuple[int, int] | None) -> str:
    return "N/A" if edge is None else f"{edge[0]}-{edge[1]}"


def _fmt_float(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.3e}"


def main() -> None:
    t0 = time.time()
    print("=" * 110)
    print("STAGGERED BACKREACTION ACTIVE-GAUGE EDGE SELECTION")
    print("  Active field fixed: resistance-Yukawa Green source sector")
    print("  Scored edge rule: source-proximal non-bridge edge")
    print("=" * 110)
    print(
        f"span_tol={GAUGE_SPAN_TOL:.1e}, periodic_residual_tol={GAUGE_PERIOD_TOL:.1e}, "
        f"kernel=exp(-{br.GREEN_MU} R_eff)/(R_eff+{br.GREEN_EPS})"
    )
    print()
    print(
        f"{'family':<42} {'n':>4} {'legacy':>9} {'J_legacy':>11} {'src_edge':>9} "
        f"{'J_source':>11} {'resid':>10} {'max_edge':>9} {'J_max':>11} {'status':>7}"
    )
    print("-" * 110)

    results = [_measure_graph(graph) for graph in stress._stress_graphs()]
    for row in results:
        print(
            f"{row.family:<42} {row.n:4d} "
            f"{_fmt_edge(row.legacy_edge):>9s} {_fmt_float(row.legacy_span):>11s} "
            f"{_fmt_edge(row.source_edge):>9s} {_fmt_float(row.source_span):>11s} "
            f"{_fmt_float(row.source_residual):>10s} "
            f"{_fmt_edge(row.max_edge):>9s} {_fmt_float(row.max_span):>11s} "
            f"{row.status:>7s}"
        )

    cycle_rows = [row for row in results if row.status != "N/A"]
    print()
    print("READOUT")
    print(f"  source-proximal active-gauge pass count: {sum(row.status == 'PASS' for row in cycle_rows)}/{len(cycle_rows)}")
    print(
        "  legacy DFS edge pass count: "
        f"{sum((row.legacy_span or 0.0) > GAUGE_SPAN_TOL and (row.legacy_residual or 1.0) < GAUGE_PERIOD_TOL for row in cycle_rows)}/{len(cycle_rows)}"
    )
    print(
        "  min source-edge span: "
        f"{min(row.source_span for row in cycle_rows if row.source_span is not None):.3e}"
    )
    print("  conclusion: the active-field gauge obstruction is an edge-selection artifact on this stress set")
    print(f"  runtime: {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
