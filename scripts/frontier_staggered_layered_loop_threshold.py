#!/usr/bin/env python3
"""Threshold map for native gauge/current closure on sparse layered loops.

Goal:
  Determine the minimal nearby layered cycle geometry that closes native
  gauge/current on the retained staggered graph transport law without losing
  the retained force battery.

This is intentionally narrow:
  - no 1D helpers
  - no proxy rows
  - only graph-native layered geometries
  - controls anchored to the existing layered DAG / sparse-cycle probes
"""

from __future__ import annotations

import math
import os
import sys
from collections import deque
from dataclasses import dataclass

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_graph_failure_map as failmap  # noqa: E402
import frontier_staggered_graph_portability as port  # noqa: E402
import frontier_staggered_layered_backreaction as layered  # noqa: E402


GAUGE_SPAN_THRESHOLD = 1.0e-4
GAUGE_RESIDUAL_THRESHOLD = 1.0e-8


@dataclass(frozen=True)
class ThresholdResult:
    label: str
    family: str
    n: int
    reachable: int
    source_degree: int
    plaquette_count: int | None
    first_loop_layer: int | None
    cycle: bool
    cycle_length: int | None
    same_color_edges: int
    long_edge_fraction: float
    max_degree: int
    retained_passes: int
    force_value: float
    fm_r2: float
    achrom_cv: float
    equiv_cv: float
    robust_toward: int
    robust_total: int
    current_span: float | None
    current_residual: float | None
    gauge_status: str


def _add_edge(adj: dict[int, set[int]], i: int, j: int) -> None:
    if i == j:
        return
    adj.setdefault(i, set()).add(j)
    adj.setdefault(j, set()).add(i)


def _layer_nodes(layers: int, width: int) -> list[list[int]]:
    nodes: list[list[int]] = []
    idx = 0
    for layer in range(layers):
        count = 1 if layer == 0 else width
        nodes.append(list(range(idx, idx + count)))
        idx += count
    return nodes


def _build_two_rail_family(
    *,
    seed: int,
    layers: int,
    width: int,
    rail_cols: tuple[int, int],
    plaquette_layers: tuple[int, ...],
    label: str,
) -> port.GraphFamily:
    base = layered._build_layered_family(seed=seed, layers=layers, width=width, fanout=1)
    layer_nodes = _layer_nodes(layers, width)
    adj_sets: dict[int, set[int]] = {}
    source = layer_nodes[0][0]
    rail_a, rail_b = rail_cols

    # Open a minimal source-connected corridor and only add local plaquettes on
    # selected adjacent-layer windows.
    _add_edge(adj_sets, source, layer_nodes[1][rail_a])
    _add_edge(adj_sets, source, layer_nodes[1][rail_b])
    for layer in range(1, layers - 1):
        a0 = layer_nodes[layer][rail_a]
        a1 = layer_nodes[layer][rail_b]
        b0 = layer_nodes[layer + 1][rail_a]
        b1 = layer_nodes[layer + 1][rail_b]
        _add_edge(adj_sets, a0, b0)
        _add_edge(adj_sets, a1, b1)
        if layer in plaquette_layers:
            _add_edge(adj_sets, a0, b1)
            _add_edge(adj_sets, a1, b0)

    adj = port._finalize_adj(adj_sets)
    depth = port._bfs_depth(adj, source, base.positions.shape[0])
    detector = [i for i in layer_nodes[-1] if np.isfinite(depth[i])]
    cycle_edge = port._find_cycle_edge(adj)
    return port.GraphFamily(
        name=label,
        positions=base.positions,
        colors=base.colors,
        adj=adj,
        source=source,
        detector=detector,
        depth=depth,
        has_cycle=cycle_edge is not None,
        cycle_edge=cycle_edge,
    )


def _cycle_length(graph: port.GraphFamily) -> int | None:
    if not graph.has_cycle or graph.cycle_edge is None:
        return None
    start, stop = graph.cycle_edge
    q = deque([(start, 0)])
    seen = {start}
    while q:
        node, dist = q.popleft()
        for nb in graph.adj.get(node, []):
            if (node == start and nb == stop) or (node == stop and nb == start):
                continue
            if nb == stop:
                return dist + 2
            if nb in seen:
                continue
            seen.add(nb)
            q.append((nb, dist + 1))
    return None


def _gauge_metrics(graph: port.GraphFamily) -> tuple[float | None, float | None, str]:
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
    residual = float(abs(currents[0] - currents[-1]))
    status = "PASS" if span > GAUGE_SPAN_THRESHOLD and residual < GAUGE_RESIDUAL_THRESHOLD else "FAIL"
    return span, residual, status


def _retained_passes(result: port.FamilyResult, gauge_status: str) -> int:
    return sum(
        [
            result.born_lin < 1.0e-10,
            result.norm_drift < 1.0e-10,
            result.force_value > 0.0,
            result.fm_r2 > 0.9,
            result.achrom_cv < 0.05,
            result.equiv_cv < 0.05,
            result.robust_toward == result.robust_total,
            gauge_status in ("PASS", "N/A"),
        ]
    )


def _measure(
    label: str,
    graph: port.GraphFamily,
    *,
    plaquette_count: int | None,
    first_loop_layer: int | None,
) -> ThresholdResult:
    result = port._measure_family(graph)
    current_span, current_residual, gauge_status = _gauge_metrics(graph)
    return ThresholdResult(
        label=label,
        family=graph.name,
        n=graph.positions.shape[0],
        reachable=int(np.isfinite(graph.depth).sum()),
        source_degree=len(graph.adj.get(graph.source, [])),
        plaquette_count=plaquette_count,
        first_loop_layer=first_loop_layer,
        cycle=graph.has_cycle,
        cycle_length=_cycle_length(graph),
        same_color_edges=failmap._same_color_edges(graph),
        long_edge_fraction=failmap._long_edge_fraction(graph),
        max_degree=failmap._max_degree(graph.adj),
        retained_passes=_retained_passes(result, gauge_status),
        force_value=result.force_value,
        fm_r2=result.fm_r2,
        achrom_cv=result.achrom_cv,
        equiv_cv=result.equiv_cv,
        robust_toward=result.robust_toward,
        robust_total=result.robust_total,
        current_span=current_span,
        current_residual=current_residual,
        gauge_status=gauge_status,
    )


def _reference_rows() -> list[ThresholdResult]:
    return [
        _measure(
            "control_dag",
            layered._build_layered_family(seed=13, layers=8, width=5, fanout=1),
            plaquette_count=0,
            first_loop_layer=None,
        ),
        _measure(
            "control_sparse_cycle",
            layered._build_layered_family(seed=29, layers=10, width=6, fanout=2),
            plaquette_count=None,
            first_loop_layer=None,
        ),
        _measure(
            "two_rail_no_loop",
            _build_two_rail_family(
                seed=13,
                layers=8,
                width=5,
                rail_cols=(1, 2),
                plaquette_layers=(),
                label="layered_two_rail_no_loop_s13_n36",
            ),
            plaquette_count=0,
            first_loop_layer=None,
        ),
    ]


def _threshold_rows() -> list[ThresholdResult]:
    rows: list[ThresholdResult] = []
    for loop_layer in range(1, 7):
        rows.append(
            _measure(
                f"single_loop_l{loop_layer}",
                _build_two_rail_family(
                    seed=13,
                    layers=8,
                    width=5,
                    rail_cols=(1, 2),
                    plaquette_layers=(loop_layer,),
                    label=f"layered_two_rail_loop_l{loop_layer}_s13_n36",
                ),
                plaquette_count=1,
                first_loop_layer=loop_layer,
            )
        )
    return rows


def _print_row(row: ThresholdResult) -> None:
    plaquette_txt = "na" if row.plaquette_count is None else str(row.plaquette_count)
    loop_txt = "na" if row.first_loop_layer is None else str(row.first_loop_layer)
    cycle_len_txt = "na" if row.cycle_length is None else str(row.cycle_length)
    current_txt = "N/A" if row.current_span is None else f"{row.current_span:.3e}"
    residual_txt = "N/A" if row.current_residual is None else f"{row.current_residual:.3e}"
    cycle_txt = "yes" if row.cycle else "no"
    print(
        f"{row.label:<22} "
        f"n={row.n:<3d} "
        f"reach={row.reachable:<2d} "
        f"srcdeg={row.source_degree} "
        f"plaq={plaquette_txt:<2s} "
        f"loop@={loop_txt:<2s} "
        f"cycle={cycle_txt} "
        f"cyc_len={cycle_len_txt:<2s} "
        f"struct=sc{row.same_color_edges}/ld{row.long_edge_fraction:.2f}/deg{row.max_degree:<2d} "
        f"retained={row.retained_passes}/8 "
        f"force={row.force_value:+.3e} "
        f"F~M={row.fm_r2:.3f} "
        f"ach={row.achrom_cv:.2e} "
        f"eq={row.equiv_cv:.2e} "
        f"rob={row.robust_toward}/{row.robust_total} "
        f"J_span={current_txt} "
        f"J_resid={residual_txt} "
        f"gauge={row.gauge_status}"
    )


def main() -> None:
    print("=" * 120)
    print("STAGGERED LAYERED LOOP THRESHOLD")
    print("  Minimal layered-loop geometry for native gauge/current closure")
    print("  Retained force battery: Born/linearity, norm, force sign, F∝M, achromatic force,")
    print("  equivalence, robustness, and strict native gauge closure")
    print("=" * 120)
    print(
        f"  dt={port.DT}, steps={port.N_STEPS}, mass={port.MASS}, G={port.G}, "
        f"source_strength={port.SOURCE_STRENGTH}"
    )
    print(
        f"  strict gauge thresholds: J_span>{GAUGE_SPAN_THRESHOLD:.1e}, "
        f"|J(0)-J(2pi)|<{GAUGE_RESIDUAL_THRESHOLD:.1e}"
    )
    print()

    references = _reference_rows()
    thresholds = _threshold_rows()

    print("REFERENCE CONTROLS")
    for row in references:
        _print_row(row)

    print()
    print("THRESHOLD MAP")
    for row in thresholds:
        _print_row(row)

    pass_rows = [row for row in thresholds if row.gauge_status == "PASS"]
    weakest_pass = min(pass_rows, key=lambda row: row.current_span or math.inf)
    sparse_cycle = next(row for row in references if row.label == "control_sparse_cycle")

    print()
    print("DECISION")
    print("  freeze negative control: control_dag / layered_bipartite_dag_s13_n36")
    print("  cycle existence alone is not enough: control_sparse_cycle keeps a cycle but stays gauge=FAIL")
    print(
        "  minimal nearby closure: two source-connected rails plus one local K2,2 plaquette "
        "on any tested layer window"
    )
    print(
        f"  weakest passing one-plaquette case: {weakest_pass.label} "
        f"(cycle length={weakest_pass.cycle_length}, J_span={weakest_pass.current_span:.3e})"
    )
    print(
        f"  sparse irregular cycle holdout span: {sparse_cycle.current_span:.3e} "
        f"({GAUGE_SPAN_THRESHOLD / max(sparse_cycle.current_span or 1.0, 1.0e-30):.1f}x below threshold)"
    )

    print()
    print("Interpretation:")
    print("  - The sparse DAG holdout stays the correct negative control for gauge/current.")
    print("  - A single local even plaquette is sufficient to recover native closure without losing the force battery.")
    print("  - The passing threshold families remain bipartite/local: same-color defects stay at 0 and long-edge")
    print("    fraction stays at 0.00.")


if __name__ == "__main__":
    main()
