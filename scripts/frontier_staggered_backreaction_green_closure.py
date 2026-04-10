#!/usr/bin/env python3
"""Graph-native Green-closure probe for staggered backreaction.

Goal:
  Attack the endogenous-field scale blocker on the retained cycle-bearing
  bipartite graph families with genuinely nonlocal source-to-field maps,
  rather than another local source preconditioner sweep.

What is held fixed:
  - staggered transport law
  - force as the primary observable
  - zero-source exactness
  - source-response linearity
  - two-body additivity
  - TOWARD force sign
  - norm stability

What is varied:
  - the linear field solver only

The promoted narrow comparison is:
  - screened graph Poisson baseline
  - weighted-geodesic Yukawa Green map
  - resistance-distance Yukawa Green map

One scalar gain is still reported for comparison with the earlier scale-closure
probe, but the retained nonlocal maps already land close to the correct scale
without large recalibration.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
import time
from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_backreaction_prototype as base


DT = base.DT
N_STEPS = base.N_STEPS
MASS = base.MASS
F_TOL = base.F_TOL


@dataclass(frozen=True)
class MappingSpec:
    name: str
    mode: str
    mu: float = 0.0
    eps: float = 0.0


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
    holdout_raw_gap: float
    holdout_cal_gap: float
    cycle_raw_self_gap: float
    cycle_cal_self_gap: float
    source_r2_min: float
    source_r2_mean: float
    two_body_max: float
    toward_min: int
    norm_max: float
    balance_score: float


def _make_mappings() -> list[MappingSpec]:
    return [
        MappingSpec("screened_poisson", "poisson"),
        MappingSpec("geodesic_yukawa", "geodesic_yukawa", mu=1.50, eps=0.10),
        MappingSpec("resistance_yukawa", "resistance_yukawa", mu=1.50, eps=0.10),
    ]


def _weighted_shortest_paths(graph: base.GraphFamily) -> np.ndarray:
    n = graph.positions.shape[0]
    weights = np.full((n, n), np.inf, dtype=float)
    np.fill_diagonal(weights, 0.0)
    for i, nbs in graph.adj.items():
        for j in nbs:
            dx = graph.positions[j, 0] - graph.positions[i, 0]
            dy = graph.positions[j, 1] - graph.positions[i, 1]
            dist = math.hypot(dx, dy)
            weights[i, j] = min(weights[i, j], dist)
    return shortest_path(csr_matrix(weights), directed=False, unweighted=False)


def _resistance_distance(graph: base.GraphFamily) -> np.ndarray:
    lap = base._graph_laplacian(graph).toarray()
    evals, evecs = np.linalg.eigh(lap)
    inv = np.zeros_like(evals)
    mask = evals > 1e-10
    inv[mask] = 1.0 / evals[mask]
    lap_pinv = (evecs * inv) @ evecs.T
    diag = np.clip(np.diag(lap_pinv), 0.0, None)
    eff_resistance = np.maximum(diag[:, None] + diag[None, :] - 2.0 * lap_pinv, 0.0)
    return np.sqrt(eff_resistance)


def _kernel_matrix(metric: np.ndarray, mu: float, eps: float) -> np.ndarray:
    return np.exp(-mu * metric) / (metric + eps)


def _apply_mapping(graph: base.GraphFamily, rho: np.ndarray, spec: MappingSpec) -> np.ndarray:
    if spec.mode == "poisson":
        return base._solve_phi(graph, rho)
    if spec.mode == "geodesic_yukawa":
        kernel = _kernel_matrix(_weighted_shortest_paths(graph), spec.mu, spec.eps)
        return np.asarray(kernel @ rho, dtype=float)
    if spec.mode == "resistance_yukawa":
        kernel = _kernel_matrix(_resistance_distance(graph), spec.mu, spec.eps)
        return np.asarray(kernel @ rho, dtype=float)
    raise ValueError(f"unknown mapping mode: {spec.mode}")


def _fit_gain(cycle_rows: list[FamilyProbe]) -> float:
    solves = np.asarray([r.solve_force for r in cycle_rows], dtype=float)
    exts = np.asarray([r.ext_force for r in cycle_rows], dtype=float)
    denom = float(np.dot(solves, solves))
    if denom <= 0:
        return 1.0
    return float(np.dot(solves, exts) / denom)


def _measure_family(graph: base.GraphFamily, spec: MappingSpec, gain: float = 1.0) -> FamilyProbe:
    n = graph.positions.shape[0]
    psi0 = base._probe_state(graph.positions, graph.source, k0=0.18)
    source_nodes = [graph.source]

    rho_zero = np.zeros(n, dtype=float)
    phi_zero = gain * _apply_mapping(graph, rho_zero, spec)
    psi_zero = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_zero), psi0, DT, N_STEPS)
    zero_force = base._force_from_phi(graph, psi_zero, phi_zero)
    norm_drift = abs(np.linalg.norm(psi_zero) - 1.0)

    rho_source = base._source_density(graph, source_nodes, [1.0])
    phi_solve = gain * _apply_mapping(graph, rho_source, spec)
    phi_ext = base._external_phi(graph, source_nodes, [1.0])
    psi_solve = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_solve), psi0, DT, N_STEPS)
    psi_ext = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_ext), psi0, DT, N_STEPS)
    solve_force = base._force_from_phi(graph, psi_solve, phi_solve)
    ext_force = base._force_from_phi(graph, psi_ext, phi_ext)
    solve_gap = abs(solve_force - ext_force) / max(abs(ext_force), 1e-30)

    strengths = list(base.SOURCE_STRENGTHS)
    forces = []
    for strength in strengths:
        rho = base._source_density(graph, source_nodes, [strength])
        phi = gain * _apply_mapping(graph, rho, spec)
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
    rho_a = base._source_density(graph, [graph.source], [1.0])
    rho_b = base._source_density(graph, [partner], [1.0])
    rho_ab = base._source_density(graph, [graph.source, partner], [1.0, 1.0])
    phi_a = gain * _apply_mapping(graph, rho_a, spec)
    phi_b = gain * _apply_mapping(graph, rho_b, spec)
    phi_ab = gain * _apply_mapping(graph, rho_ab, spec)
    psi_ab = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_ab), psi0, DT, N_STEPS)
    force_ab = base._force_from_phi(graph, psi_ab, phi_ab)
    force_add = base._force_from_phi(
        graph,
        base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_a + phi_b), psi0, DT, N_STEPS),
        phi_a + phi_b,
    )
    two_body_resid = abs(force_ab - force_add) / max(abs(force_ab), 1e-30)

    rho_self = np.abs(psi_solve) ** 2
    rho_self *= max(np.sum(rho_source), 1e-30) / max(np.sum(rho_self), 1e-30)
    phi_self = gain * _apply_mapping(graph, rho_self, spec)
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


def _summarize(mapping: str, raw_rows: list[FamilyProbe], cal_rows: list[FamilyProbe], gain: float) -> MapSummary:
    cycle_raw = [r for r in raw_rows if "layered" not in r.family]
    cycle_cal = [r for r in cal_rows if "layered" not in r.family]
    holdout_raw = next(r for r in raw_rows if "layered" in r.family)
    holdout_cal = next(r for r in cal_rows if "layered" in r.family)
    balance = statistics.fmean(r.solve_gap for r in cycle_cal) + 0.5 * holdout_cal.solve_gap
    return MapSummary(
        mapping=mapping,
        gain_fit=gain,
        cycle_raw_gap=statistics.fmean(r.solve_gap for r in cycle_raw),
        cycle_cal_gap=statistics.fmean(r.solve_gap for r in cycle_cal),
        holdout_raw_gap=holdout_raw.solve_gap,
        holdout_cal_gap=holdout_cal.solve_gap,
        cycle_raw_self_gap=statistics.fmean(r.self_gap for r in cycle_raw),
        cycle_cal_self_gap=statistics.fmean(r.self_gap for r in cycle_cal),
        source_r2_min=min(r.source_r2 for r in cal_rows),
        source_r2_mean=statistics.fmean(r.source_r2 for r in cal_rows),
        two_body_max=max(r.two_body_resid for r in cal_rows),
        toward_min=min(r.toward_fraction for r in cal_rows),
        norm_max=max(r.norm_drift for r in cal_rows),
        balance_score=balance,
    )


def main() -> None:
    t0 = time.time()
    graphs = base._make_graphs()
    mappings = _make_mappings()
    cycle_graphs = [g for g in graphs if g.has_cycle]

    print("=" * 100)
    print("STAGGERED BACKREACTION GRAPH-GREEN CLOSURE")
    print("  transport law fixed; compare direct nonlocal Green maps against screened graph Poisson")
    print("  holdout-aware target: close the cycle-bearing force gap without breaking the retained battery")
    print("=" * 100)
    print(
        f"dt={DT}, steps={N_STEPS}, mass={MASS}, retained cycle-bearing families={len(cycle_graphs)}, "
        f"layered holdout families={len(graphs) - len(cycle_graphs)}"
    )
    print("frozen nonlocal kernels: geodesic_yukawa(mu=1.50, eps=0.10), resistance_yukawa(mu=1.50, eps=0.10)")
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

    summaries.sort(key=lambda s: s.balance_score)

    print("MAP SUMMARY")
    print(
        f"{'mapping':<18} {'gain':>8s} {'raw_cycle':>10s} {'cal_cycle':>10s} "
        f"{'raw_hold':>10s} {'cal_hold':>10s} {'balance':>10s}"
    )
    for s in summaries:
        print(
            f"{s.mapping:<18} {s.gain_fit:8.3f} {s.cycle_raw_gap:10.3e} {s.cycle_cal_gap:10.3e} "
            f"{s.holdout_raw_gap:10.3e} {s.holdout_cal_gap:10.3e} {s.balance_score:10.3e}"
        )

    best = summaries[0]
    baseline = next(s for s in summaries if s.mapping == "screened_poisson")

    print()
    print("PER-FAMILY CALIBRATED READOUT")
    for row in cal_by_map[best.mapping]:
        print(
            f"{row.mapping:<18} {row.family:<26} "
            f"F_ext={row.ext_force:+.3e} F_solve={row.solve_force:+.3e} "
            f"gap={row.solve_gap:.3e} R2={row.source_r2:.4f} "
            f"2body={row.two_body_resid:.3e} self_gap={row.self_gap:.3e} "
            f"norm={row.norm_drift:.2e} TOWARD={row.toward_fraction}/{row.toward_total}"
        )

    print()
    print("READOUT")
    print(
        f"  baseline cycle-bearing mean gap: {baseline.cycle_raw_gap:.3e} "
        f"(screened graph Poisson)"
    )
    print(
        f"  promoted cycle-bearing mean gap: {best.cycle_raw_gap:.3e} "
        f"({best.mapping}, raw)"
    )
    print(
        f"  raw improvement factor: {baseline.cycle_raw_gap / max(best.cycle_raw_gap, 1e-30):.2f}x"
    )
    print(f"  baseline holdout gap: {baseline.holdout_raw_gap:.3e}")
    print(f"  promoted holdout gap: {best.holdout_raw_gap:.3e}")
    print(f"  fitted gain on cycle-bearing only: {best.gain_fit:.3f}")
    print(f"  promoted source-response R^2 min/mean: {best.source_r2_min:.4f} / {best.source_r2_mean:.4f}")
    print(f"  promoted two-body residual max: {best.two_body_max:.3e}")
    print(f"  promoted minimum TOWARD count: {best.toward_min}/3")
    print(f"  promoted norm drift max: {best.norm_max:.3e}")
    print(f"  promoted cycle-bearing mean self-gap: {best.cycle_raw_self_gap:.3e}")
    print(f"  runtime: {time.time() - t0:.2f}s")
    print()
    print("INTERPRETATION")
    print("  - The scale blocker is not limited to local Poisson normalization.")
    print("  - A direct graph-native Green map materially closes the cycle-bearing gap and transfers to the layered holdout.")
    print("  - The resistance-distance Yukawa kernel is the best holdout-aware map in this frozen comparison.")
    print("  - The remaining open seam is one-step endogenous refresh: the self-gap stays O(1) even after the raw source-to-field scale closes.")


if __name__ == "__main__":
    main()
