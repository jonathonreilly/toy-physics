#!/usr/bin/env python3
"""Staggered backreaction scale-closure probe.

Goal:
  Attack the endogenous-field force-scale blocker by testing whether a single
  linear normalization of the source-generated Phi can materially close the
  external-vs-solved force gap on cycle-bearing bipartite graph families.

What is held fixed:
  - staggered transport law
  - force as the primary observable
  - zero-source control
  - source-response linearity
  - two-body additivity
  - norm stability

What is varied:
  - source-to-field linear preconditioning family
  - one global scalar gain fitted on the cycle-bearing families only

This is intentionally narrower than a new self-gravity theory. It is a
normalization/closure probe: if a single gain closes the gap materially without
losing the retained checks, the blocker is largely calibration. If not, the
gap is structural.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
import time
from dataclasses import dataclass

import numpy as np
from scipy.sparse import diags

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_backreaction_iterative as iterative
import frontier_staggered_backreaction_prototype as base


DT = base.DT
N_STEPS = base.N_STEPS
MASS = base.MASS
F_TOL = base.F_TOL


@dataclass(frozen=True)
class MappingSpec:
    name: str
    mode: str
    beta: float = 0.0
    steps: int = 0


@dataclass
class FamilyProbe:
    mapping: str
    family: str
    n: int
    zero_force: float
    ext_force: float
    solve_force: float
    solve_gap: float
    source_r2: float
    two_body_resid: float
    toward_fraction: int
    toward_total: int
    norm_drift: float
    self_force: float
    self_gap: float


@dataclass
class MapSummary:
    mapping: str
    gain_fit: float
    cycle_raw_gap: float
    cycle_cal_gap: float
    cycle_raw_self_gap: float
    cycle_cal_self_gap: float
    holdout_raw_gap: float
    holdout_cal_gap: float
    gain_mean: float
    gain_std: float
    source_r2_mean: float
    two_body_max: float
    toward_min: int
    norm_max: float


def _make_mappings() -> list[MappingSpec]:
    return [
        MappingSpec("gaussian", "identity"),
        MappingSpec("lap1_b0p25", "lap_sharpen", beta=0.25, steps=1),
        MappingSpec("lap2_b0p25", "lap_sharpen", beta=0.25, steps=2),
        MappingSpec("lap1_b0p50", "lap_sharpen", beta=0.50, steps=1),
        MappingSpec("lap2_b1p00", "lap_sharpen", beta=1.00, steps=2),
        MappingSpec("invheat_b0p25", "inverse_heat", beta=0.25),
        MappingSpec("invheat_b0p50", "inverse_heat", beta=0.50),
        MappingSpec("invheat_b1p00", "inverse_heat", beta=1.00),
        MappingSpec("invheat_b1p50", "inverse_heat", beta=1.50),
        MappingSpec("invheat_b2p00", "inverse_heat", beta=2.00),
        MappingSpec("invheat_b3p00", "inverse_heat", beta=3.00),
    ]


def _normalized_laplacian(graph: base.GraphFamily):
    lap = base._graph_laplacian(graph).tocsr()
    diag = np.asarray(lap.diagonal(), dtype=float)
    inv_sqrt = np.zeros_like(diag)
    mask = diag > 0
    inv_sqrt[mask] = 1.0 / np.sqrt(diag[mask])
    d_inv = diags(inv_sqrt)
    return d_inv @ lap @ d_inv


def _apply_mapping(graph: base.GraphFamily, rho: np.ndarray, spec: MappingSpec, ln=None) -> np.ndarray:
    return iterative._apply_mapping(graph, rho, spec, ln=ln)


def _source_density(graph: base.GraphFamily, source_nodes: list[int], strengths: list[float]) -> np.ndarray:
    return base._source_density(graph, source_nodes, strengths)


def _measure_family(graph: base.GraphFamily, spec: MappingSpec, gain: float = 1.0) -> FamilyProbe:
    n = graph.positions.shape[0]
    ln = _normalized_laplacian(graph)
    psi0 = base._probe_state(graph.positions, graph.source, k0=0.18)
    source_nodes = [graph.source]

    rho_zero = np.zeros(n, dtype=float)
    phi_zero = base._solve_phi(graph, rho_zero)
    psi_zero = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_zero), psi0, DT, N_STEPS)
    zero_force = base._force_from_phi(graph, psi_zero, phi_zero)
    norm_drift = abs(np.linalg.norm(psi_zero) - 1.0)

    rho_source = _source_density(graph, source_nodes, [1.0])
    rho_eff = gain * _apply_mapping(graph, rho_source, spec, ln=ln)
    phi_solve = base._solve_phi(graph, rho_eff)
    phi_ext = base._external_phi(graph, source_nodes, [1.0])
    psi_solve = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_solve), psi0, DT, N_STEPS)
    psi_ext = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_ext), psi0, DT, N_STEPS)
    solve_force = base._force_from_phi(graph, psi_solve, phi_solve)
    ext_force = base._force_from_phi(graph, psi_ext, phi_ext)
    solve_gap = abs(solve_force - ext_force) / max(abs(ext_force), 1e-30)

    strengths = list(base.SOURCE_STRENGTHS)
    forces = []
    for strength in strengths:
        rho = _source_density(graph, source_nodes, [strength])
        rho_eff_s = gain * _apply_mapping(graph, rho, spec, ln=ln)
        phi = base._solve_phi(graph, rho_eff_s)
        psi = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi), psi0, DT, N_STEPS)
        forces.append(base._force_from_phi(graph, psi, phi))
    f_arr = np.asarray(forces, dtype=float)
    s_arr = np.asarray(strengths, dtype=float)
    if np.sum((f_arr - np.mean(f_arr)) ** 2) > 0:
        coeff = np.polyfit(s_arr, f_arr, 1)
        pred = np.polyval(coeff, s_arr)
        source_r2 = 1.0 - float(np.sum((f_arr - pred) ** 2) / np.sum((f_arr - np.mean(f_arr)) ** 2))
    else:
        source_r2 = 1.0

    if len(graph.detector) > 0:
        partner = graph.detector[0]
    else:
        partner = max(range(n), key=lambda i: graph.depth[i] if np.isfinite(graph.depth[i]) else -1)
    rho_a = _source_density(graph, [graph.source], [1.0])
    rho_b = _source_density(graph, [partner], [1.0])
    rho_ab = _source_density(graph, [graph.source, partner], [1.0, 1.0])
    phi_a = base._solve_phi(graph, gain * _apply_mapping(graph, rho_a, spec, ln=ln))
    phi_b = base._solve_phi(graph, gain * _apply_mapping(graph, rho_b, spec, ln=ln))
    phi_ab = base._solve_phi(graph, gain * _apply_mapping(graph, rho_ab, spec, ln=ln))
    denom = max(np.linalg.norm(phi_ab), 1e-30)
    phi_residual = float(np.linalg.norm(phi_ab - (phi_a + phi_b)) / denom)
    psi_ab = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_ab), psi0, DT, N_STEPS)
    force_ab = base._force_from_phi(graph, psi_ab, phi_ab)
    force_add = base._force_from_phi(
        graph,
        base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_a + phi_b), psi0, DT, N_STEPS),
        phi_a + phi_b,
    )
    two_body_resid = abs(force_ab - force_add) / max(abs(force_ab), 1e-30)

    rho_self = np.abs(psi_solve) ** 2
    rho_self *= max(np.sum(rho_eff), 1e-30) / max(np.sum(rho_self), 1e-30)
    phi_self = base._solve_phi(graph, rho_self)
    self_force = base._force_from_phi(graph, psi_solve, phi_self)
    self_gap = abs(self_force - solve_force) / max(abs(solve_force), 1e-30)

    toward_total = 3
    toward_samples = int(zero_force >= -F_TOL) + int(solve_force > 0) + int(ext_force > 0)
    return FamilyProbe(
        mapping=spec.name,
        family=graph.name,
        n=n,
        zero_force=zero_force,
        ext_force=ext_force,
        solve_force=solve_force,
        solve_gap=solve_gap,
        source_r2=source_r2,
        two_body_resid=two_body_resid,
        toward_fraction=toward_samples,
        toward_total=toward_total,
        norm_drift=norm_drift,
        self_force=self_force,
        self_gap=self_gap,
    )


def _fit_gain(cycle_rows: list[FamilyProbe]) -> float:
    solves = np.asarray([r.solve_force for r in cycle_rows], dtype=float)
    exts = np.asarray([r.ext_force for r in cycle_rows], dtype=float)
    denom = float(np.dot(solves, solves))
    if denom <= 0:
        return 1.0
    return float(np.dot(solves, exts) / denom)


def _summarize(mapping: str, raw_rows: list[FamilyProbe], cal_rows: list[FamilyProbe], gain: float) -> MapSummary:
    cycle_raw = [r for r in raw_rows if "layered" not in r.family]
    cycle_cal = [r for r in cal_rows if "layered" not in r.family]
    holdout_raw = next(r for r in raw_rows if "layered" in r.family)
    holdout_cal = next(r for r in cal_rows if "layered" in r.family)
    gains = [r.ext_force / max(r.solve_force, 1e-30) for r in cycle_raw]
    return MapSummary(
        mapping=mapping,
        gain_fit=gain,
        cycle_raw_gap=statistics.fmean(r.solve_gap for r in cycle_raw),
        cycle_cal_gap=statistics.fmean(r.solve_gap for r in cycle_cal),
        cycle_raw_self_gap=statistics.fmean(r.self_gap for r in cycle_raw),
        cycle_cal_self_gap=statistics.fmean(r.self_gap for r in cycle_cal),
        holdout_raw_gap=holdout_raw.solve_gap,
        holdout_cal_gap=holdout_cal.solve_gap,
        gain_mean=statistics.fmean(gains),
        gain_std=statistics.pstdev(gains) if len(gains) > 1 else 0.0,
        source_r2_mean=statistics.fmean(r.source_r2 for r in raw_rows),
        two_body_max=max(r.two_body_resid for r in raw_rows),
        toward_min=min(r.toward_fraction for r in raw_rows),
        norm_max=max(r.norm_drift for r in raw_rows),
    )


def main() -> None:
    t0 = time.time()
    graphs = base._make_graphs()
    mappings = _make_mappings()
    cycle_graphs = [g for g in graphs if g.has_cycle]

    print("=" * 100)
    print("STAGGERED BACKREACTION SCALE-CLOSURE PROBE")
    print("  transport law fixed; source->field map varied; one global gain fitted per map")
    print("  primary question: can a single normalization materially close the external-vs-solved force gap?")
    print("=" * 100)
    print(
        f"dt={DT}, steps={N_STEPS}, mass={MASS}, retained cycle-bearing families={len(cycle_graphs)}, "
        f"holdout DAG families={len(graphs) - len(cycle_graphs)}"
    )
    print()

    raw_by_map: dict[str, list[FamilyProbe]] = {}
    cal_by_map: dict[str, list[FamilyProbe]] = {}
    summaries: list[MapSummary] = []

    for spec in mappings:
        raw_rows = [_measure_family(graph, spec, gain=1.0) for graph in graphs]
        cycle_rows = [r for r in raw_rows if "layered" not in r.family]
        gain = _fit_gain(cycle_rows)
        cal_rows = [_measure_family(graph, spec, gain=gain) for graph in graphs]
        raw_by_map[spec.name] = raw_rows
        cal_by_map[spec.name] = cal_rows
        summaries.append(_summarize(spec.name, raw_rows, cal_rows, gain))

    summaries.sort(key=lambda s: s.cycle_cal_gap)

    print("MAP SUMMARY")
    print(
        f"{'mapping':<16} {'gain':>9s} {'raw_gap':>10s} {'cal_gap':>10s} "
        f"{'raw_hold':>10s} {'cal_hold':>10s} {'gain_mu':>10s} {'gain_sd':>10s}"
    )
    for s in summaries:
        print(
            f"{s.mapping:<16} {s.gain_fit:9.3f} {s.cycle_raw_gap:10.3e} {s.cycle_cal_gap:10.3e} "
            f"{s.holdout_raw_gap:10.3e} {s.holdout_cal_gap:10.3e} {s.gain_mean:10.3f} {s.gain_std:10.3f}"
        )

    best = summaries[0]
    best_cycle_rows = [r for r in cal_by_map[best.mapping] if "layered" not in r.family]
    baseline = [r for r in raw_by_map["gaussian"] if "layered" not in r.family]
    baseline_holdout = next(r for r in raw_by_map["gaussian"] if "layered" in r.family)
    best_holdout = next(r for r in cal_by_map[best.mapping] if "layered" in r.family)

    print()
    print("READOUT")
    print(f"  baseline cycle-bearing mean gap: {statistics.fmean(r.solve_gap for r in baseline):.3e}")
    print(f"  best cycle-bearing mean gap: {best.cycle_cal_gap:.3e} ({best.mapping}, gain={best.gain_fit:.3f})")
    print(
        f"  improvement factor: {statistics.fmean(r.solve_gap for r in baseline) / max(best.cycle_cal_gap, 1e-30):.2f}x"
    )
    print(f"  baseline holdout gap: {baseline_holdout.solve_gap:.3e}")
    print(f"  best holdout gap: {best_holdout.solve_gap:.3e}")
    print(f"  best-map cycle-bearing mean self-gap: {best.cycle_cal_self_gap:.3e}")
    print(f"  best-map source-response R^2 mean: {best.source_r2_mean:.4f}")
    print(f"  best-map two-body residual max: {best.two_body_max:.3e}")
    print(f"  best-map minimum TOWARD count: {best.toward_min}/3")
    print(f"  best-map norm drift max: {best.norm_max:.3e}")
    print(f"  runtime: {time.time() - t0:.2f}s")
    print()
    print("INTERPRETATION")
    print("  - This is a scale-normalization probe, not a transport-law change.")
    print("  - A material closure would mean the calibrated cycle-bearing gap is")
    print("    much smaller than the raw gap while the retained checks remain exact.")
    print("  - If the calibrated gap still sits far from the external-kernel control,")
    print("    the blocker is structural rather than a single missing normalization.")


if __name__ == "__main__":
    main()
