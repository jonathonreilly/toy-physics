#!/usr/bin/env python3
"""Native gauge/current closure probe for the staggered graph lane.

Goal:
  Attack gauge/current closure on cycle-bearing layered or stress graphs using
  the same graph-native staggered transport law.

This probe is intentionally narrow:
  - no 1D helpers
  - no slit-phase proxy rows
  - gauge/current is only scored on graph families with cycles
  - acyclic layered families are reported as N/A

The retained transport law is reused from
`frontier_staggered_graph_portability.py`.
"""

from __future__ import annotations

import math
import os
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
import frontier_staggered_graph_portability_stress as stress  # noqa: E402
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


def _cycle_current(graph: port.GraphFamily) -> tuple[float, float, float]:
    if not graph.has_cycle or graph.cycle_edge is None:
        return (math.nan, math.nan, math.nan)

    phi_vals = np.linspace(0.0, 2.0 * np.pi, 9)
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

    current_span = float(max(currents) - min(currents))
    current_residual = float(abs(currents[0] - currents[-1]))
    current_mean = float(np.mean(currents))
    return current_span, current_residual, current_mean


def _measure(graph: port.GraphFamily) -> GaugeResult:
    retained = port._measure_family(graph)
    current_span, current_residual, _ = _cycle_current(graph)
    if graph.has_cycle and graph.cycle_edge is not None:
        gauge_status = "PASS" if current_span > 1e-4 and current_residual < 1e-8 else "FAIL"
    else:
        gauge_status = "N/A"

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
        current_span=None if not np.isfinite(current_span) else current_span,
        current_residual=None if not np.isfinite(current_residual) else current_residual,
        gauge_status=gauge_status,
        force_sign="TOWARD" if retained.force_value > 0 else "AWAY" if retained.force_value < 0 else "ZERO",
        fm_r2=retained.fm_r2,
        achrom_cv=retained.achrom_cv,
        equiv_cv=retained.equiv_cv,
        robust_toward=retained.robust_toward,
        robust_total=retained.robust_total,
    )


def _families() -> list[port.GraphFamily]:
    stress_graphs = stress._stress_graphs()
    layered_dag = layered._build_layered_family(seed=13, layers=8, width=5, fanout=1)
    layered_stress = layered._build_layered_family(seed=29, layers=10, width=6, fanout=2)
    return [
        stress_graphs[0],
        stress_graphs[1],
        stress_graphs[2],
        layered_dag,
        layered_stress,
    ]


def main() -> None:
    print("=" * 96)
    print("STAGGERED GRAPH GAUGE CLOSURE")
    print("  Native flux-threaded current on cycle-bearing layered/stress graphs")
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
            f"{result.family:<38} "
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
    if cycle_results:
        best = max(cycle_results, key=lambda r: r.current_span or -1.0)
        print()
        print("CLOSURE")
        print(
            f"  best geometry: {best.family} "
            f"(current span={best.current_span:.3e}, residual={best.current_residual:.3e})"
        )
        print("  operator: native staggered Hamiltonian with flux threaded through the detected cycle edge")
        print("  observable: ground-state persistent-current span over phi in [0, 2pi]")
    else:
        print()
        print("CLOSURE")
        print("  no cycle-bearing family produced a scored current observable")

    print()
    print("Interpretation:")
    print("  - Gauge/current is retained only on cycle-bearing families.")
    print("  - DAG-compatible families correctly report gauge=N/A.")
    print("  - Force remains the primary gravity observable; current is the gauge observable.")


if __name__ == "__main__":
    main()
