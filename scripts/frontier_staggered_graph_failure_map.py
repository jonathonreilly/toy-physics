#!/usr/bin/env python3
"""Adversarial failure map for the retained staggered graph lane.

Goal:
  Probe the retained staggered / Kahler-Dirac force battery at the boundaries
  described in GRAPH_DIRAC_REQUIREMENTS_2026-04-10.md:

  - odd-cycle defects
  - parity ambiguity / wrap inconsistencies
  - dense shortcuts
  - high-degree contamination

This is intentionally narrow. It reuses the retained force battery from the
portability probe and classifies outcomes as:

  - graceful_degradation: the battery still survives, but the graph is more
    irregular or gauge response is less clean
  - structural_break: the retained battery fails or the graph violates the
    staggered assumptions outright
"""

from __future__ import annotations

import math
import os
import random
import sys
from dataclasses import dataclass

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.frontier_staggered_graph_portability as port  # noqa: E402


@dataclass(frozen=True)
class FailureCase:
    label: str
    kind: str
    graph: port.GraphFamily
    defect_count: int
    long_edge_fraction: float
    max_degree: int
    note: str


@dataclass
class FailureResult:
    label: str
    kind: str
    n: int
    defect_count: int
    long_edge_fraction: float
    max_degree: int
    retained_passes: int
    retained_total: int
    force_sign: str
    fm_r2: float
    achrom_cv: float
    equiv_cv: float
    robust_toward: int
    robust_total: int
    gauge_status: str
    classification: str
    note: str


def _copy_adj(adj: dict[int, list[int]]) -> dict[int, set[int]]:
    return {i: set(nbs) for i, nbs in adj.items()}


def _same_color_edges(graph: port.GraphFamily) -> int:
    count = 0
    for i, nbs in graph.adj.items():
        for j in nbs:
            if i < j and graph.colors[i] == graph.colors[j]:
                count += 1
    return count


def _max_degree(adj: dict[int, list[int]]) -> int:
    return max((len(nbs) for nbs in adj.values()), default=0)


def _edge_lengths(graph: port.GraphFamily) -> list[float]:
    lengths: list[float] = []
    for i, nbs in graph.adj.items():
        for j in nbs:
            if i < j:
                dx = graph.positions[j, 0] - graph.positions[i, 0]
                dy = graph.positions[j, 1] - graph.positions[i, 1]
                lengths.append(math.hypot(dx, dy))
    return lengths


def _long_edge_fraction(graph: port.GraphFamily, threshold: float = 1.75) -> float:
    lengths = _edge_lengths(graph)
    if not lengths:
        return 0.0
    long_edges = sum(length > threshold for length in lengths)
    return long_edges / len(lengths)


def _rebuild_graph(
    template: port.GraphFamily,
    *,
    name: str,
    positions: np.ndarray | None = None,
    colors: np.ndarray | None = None,
    adj_sets: dict[int, set[int]] | None = None,
    source: int | None = None,
    detector: list[int] | None = None,
) -> port.GraphFamily:
    pos = template.positions if positions is None else positions
    cols = template.colors if colors is None else colors
    adj = template.adj if adj_sets is None else port._finalize_adj(adj_sets)
    src = template.source if source is None else source
    depth = port._bfs_depth(adj, src, pos.shape[0])
    if detector is None:
        finite = np.isfinite(depth)
        if np.any(finite):
            max_depth = np.nanmax(depth[finite])
            det = [i for i, d in enumerate(depth) if np.isfinite(d) and d == max_depth]
        else:
            det = []
    else:
        det = detector
    cycle_edge = port._find_cycle_edge(adj)
    return port.GraphFamily(name, pos, cols, adj, src, det, depth, cycle_edge is not None, cycle_edge)


def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _odd_cycle_defect(template: port.GraphFamily) -> port.GraphFamily:
    adj = _copy_adj(template.adj)
    source = template.source
    same_color = [i for i in range(template.positions.shape[0]) if i != source and template.colors[i] == template.colors[source]]
    same_color.sort(key=lambda i: (template.depth[i], np.linalg.norm(template.positions[i] - template.positions[source])))
    if same_color:
        _add_edge(adj, source, same_color[0])
    return _rebuild_graph(template, name=f"{template.name}_odd_cycle_defect", adj_sets=adj)


def _parity_wrap_inconsistency(template: port.GraphFamily) -> port.GraphFamily:
    adj = _copy_adj(template.adj)
    same_color = [i for i in range(template.positions.shape[0]) if template.colors[i] == template.colors[template.source] and i != template.source]
    same_color.sort(key=lambda i: (abs(template.depth[i] - template.depth[template.source]), -np.linalg.norm(template.positions[i] - template.positions[template.source])))
    if same_color:
        _add_edge(adj, template.source, same_color[-1])
    return _rebuild_graph(template, name=f"{template.name}_parity_wrap_inconsistency", adj_sets=adj)


def _dense_shortcuts(template: port.GraphFamily) -> port.GraphFamily:
    rng = random.Random(23)
    adj = _copy_adj(template.adj)
    n = template.positions.shape[0]
    pairs: list[tuple[float, int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            if template.colors[i] == template.colors[j]:
                continue
            if j in adj.get(i, set()):
                continue
            dx = template.positions[j, 0] - template.positions[i, 0]
            dy = template.positions[j, 1] - template.positions[i, 1]
            dist = math.hypot(dx, dy)
            if dist < 1.8:
                continue
            pairs.append((dist + 0.01 * rng.random(), i, j))
    pairs.sort(reverse=True)
    for _, i, j in pairs[: max(4, n // 8)]:
        _add_edge(adj, i, j)
    return _rebuild_graph(template, name=f"{template.name}_dense_shortcuts", adj_sets=adj)


def _high_degree_contamination(template: port.GraphFamily) -> port.GraphFamily:
    adj = _copy_adj(template.adj)
    n = template.positions.shape[0]
    target_color = 1 - int(template.colors[template.source])
    targets = [i for i in range(n) if template.colors[i] == target_color]
    if not targets:
        targets = list(range(n))
        target_color = 1 - int(template.colors[template.source])
    hub_pos = np.mean(template.positions, axis=0, keepdims=True)
    positions = np.vstack([template.positions, hub_pos])
    # Keep the hub bipartite-compatible: connect it to the target-color nodes
    # but assign the hub the opposite color.
    colors = np.concatenate([template.colors, np.asarray([1 - target_color], dtype=int)])
    hub = n
    for i in targets[: max(6, len(targets) // 2)]:
        _add_edge(adj, hub, i)
    adj.setdefault(hub, set())
    source = template.source
    return _rebuild_graph(
        template,
        name=f"{template.name}_high_degree_contamination",
        positions=positions,
        colors=colors,
        adj_sets=adj,
        source=source,
    )


def _long_edge_fraction_for_case(graph: port.GraphFamily) -> float:
    return _long_edge_fraction(graph, threshold=1.90 if graph.positions.shape[0] > 50 else 1.75)


def _build_cases() -> list[FailureCase]:
    control_random, control_growing, control_dag = port._make_graphs()
    return [
        FailureCase(
            label="control_random_geometric",
            kind="control",
            graph=control_random,
            defect_count=_same_color_edges(control_random),
            long_edge_fraction=_long_edge_fraction_for_case(control_random),
            max_degree=_max_degree(control_random.adj),
            note="portable baseline",
        ),
        FailureCase(
            label="odd_cycle_defect",
            kind="odd_cycle_defect",
            graph=_odd_cycle_defect(control_growing),
            defect_count=0,
            long_edge_fraction=0.0,
            max_degree=0,
            note="same-color edge injected to break bipartiteness",
        ),
        FailureCase(
            label="parity_wrap_inconsistency",
            kind="parity_wrap_inconsistency",
            graph=_parity_wrap_inconsistency(control_dag),
            defect_count=0,
            long_edge_fraction=0.0,
            max_degree=0,
            note="wrap-edge parity inconsistency injected on layered family",
        ),
        FailureCase(
            label="dense_shortcuts",
            kind="dense_shortcuts",
            graph=_dense_shortcuts(control_random),
            defect_count=0,
            long_edge_fraction=0.0,
            max_degree=0,
            note="long-range opposite-color shortcuts added",
        ),
        FailureCase(
            label="high_degree_contamination",
            kind="high_degree_contamination",
            graph=_high_degree_contamination(control_growing),
            defect_count=0,
            long_edge_fraction=0.0,
            max_degree=0,
            note="hub node added to contaminate degree distribution",
        ),
    ]


def _classify(case: FailureCase, result: port.FamilyResult) -> str:
    retained_ok = result.born_lin < 1e-10 and result.norm_drift < 1e-10 and result.force_value > 0.0
    retained_ok = retained_ok and result.fm_r2 > 0.9 and result.achrom_cv < 0.05 and result.equiv_cv < 0.05
    retained_ok = retained_ok and result.robust_toward == result.robust_total

    if case.kind in {"odd_cycle_defect", "parity_wrap_inconsistency"}:
        return "structural_break"
    if not retained_ok:
        return "structural_break"
    if case.kind in {"dense_shortcuts", "high_degree_contamination"}:
        return "graceful_degradation"
    return "baseline"


def _measure(case: FailureCase) -> FailureResult:
    graph = case.graph
    result = port._measure_family(graph)
    defect_count = _same_color_edges(graph)
    max_deg = _max_degree(graph.adj)
    long_edge_fraction = _long_edge_fraction_for_case(graph)
    retained_passes = sum(
        [
            result.born_lin < 1e-10,
            result.norm_drift < 1e-10,
            result.force_value > 0.0,
            result.fm_r2 > 0.9,
            result.achrom_cv < 0.05,
            result.equiv_cv < 0.05,
            result.robust_toward == result.robust_total,
            result.gauge_status in ("PASS", "N/A"),
        ]
    )
    classification = _classify(case, result)
    return FailureResult(
        label=case.label,
        kind=case.kind,
        n=graph.positions.shape[0],
        defect_count=defect_count,
        long_edge_fraction=long_edge_fraction,
        max_degree=max_deg,
        retained_passes=retained_passes,
        retained_total=8,
        force_sign=result.force_sign,
        fm_r2=result.fm_r2,
        achrom_cv=result.achrom_cv,
        equiv_cv=result.equiv_cv,
        robust_toward=result.robust_toward,
        robust_total=result.robust_total,
        gauge_status=result.gauge_status,
        classification=classification,
        note=case.note,
    )


def _print_result(result: FailureResult) -> None:
    print(
        f"{result.label:<28} "
        f"kind={result.kind:<28} "
        f"n={result.n:<3d} "
        f"same-color-edges={result.defect_count:<2d} "
        f"long-edge-frac={result.long_edge_fraction:.2f} "
        f"maxdeg={result.max_degree:<2d} "
        f"retained={result.retained_passes}/{result.retained_total} "
        f"force={result.force_sign:<7s} "
        f"F~M={result.fm_r2:.3f} "
        f"achrom={result.achrom_cv:.2e} "
        f"equiv={result.equiv_cv:.2e} "
        f"gauge={result.gauge_status:<4s} "
        f"classification={result.classification}"
    )


def main() -> None:
    print("=" * 110)
    print("STAGGERED GRAPH FAILURE MAP")
    print("  Adversarial boundaries: odd-cycle defects, parity ambiguity, dense shortcuts,")
    print("  wrap/parity inconsistencies, and high-degree contamination")
    print("  Retained battery: Born/linearity, norm, force sign, F∝M, achromatic force,")
    print("  equivalence, robustness, gauge if cycles exist")
    print("=" * 110)
    print(f"  dt={port.DT}, steps={port.N_STEPS}, mass={port.MASS}, G={port.G}, source={port.SOURCE_STRENGTH}")
    print()

    results: list[FailureResult] = []
    for case in _build_cases():
        result = _measure(case)
        results.append(result)
        _print_result(result)

    print()
    print("SUMMARY")
    for result in results:
        if result.classification == "baseline":
            verdict = "BASELINE"
        else:
            verdict = result.classification.upper()
        print(
            f"  {result.label:<28} {verdict:<18} "
            f"retained={result.retained_passes}/{result.retained_total} "
            f"gauge={result.gauge_status}"
        )

    print()
    print("Interpretation:")
    print("  - Same-color edges indicate a structural bipartite/parity defect.")
    print("  - Dense shortcuts and hub contamination are only graceful if the retained")
    print("    force battery still survives without reintroducing centroid-style pathologies.")
    print("  - Gauge/current is only meaningful on cycle-bearing families.")


if __name__ == "__main__":
    main()
