#!/usr/bin/env python3
"""Iterative source-to-field probe for staggered backreaction.

Goal:
  Attack the endogenous-field scaling blocker by keeping the staggered matter
  transport law fixed, while trying linear alternative source-to-field maps
  that may lift the solved graph field toward the external-kernel force scale.

What is varied:
  - source density mapping only
  - transport law is unchanged
  - primary observable remains force F = < -dPhi/dd >

What is retained:
  - zero-source control
  - source-response linearity
  - two-body additivity
  - norm stability
  - TOWARD sign on the force rows

The experiment is intentionally narrow: it compares a baseline Gaussian source
map against linear Laplacian-sharpened and inverse-heat maps on the retained
cycle-bearing bipartite families, then checks whether any map closes the force
gap to the external-kernel control materially.
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
from scipy.sparse.linalg import expm_multiply

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
POISSON_MU2 = base.POISSON_MU2
EXT_KERNEL_MU = base.EXT_KERNEL_MU
EXT_KERNEL_EPS = base.EXT_KERNEL_EPS
SOURCE_SIGMA = base.SOURCE_SIGMA
SOURCE_STRENGTHS = base.SOURCE_STRENGTHS
F_TOL = base.F_TOL


@dataclass(frozen=True)
class MappingSpec:
    name: str
    mode: str
    beta: float = 0.0
    steps: int = 0


@dataclass
class IterativeResult:
    mapping: str
    family: str
    n: int
    zero_force: float
    ext_force: float
    solve_force: float
    force_gap_rel: float
    source_r2: float
    two_body_resid: float
    toward_fraction: int
    toward_total: int
    norm_drift: float
    self_force: float
    self_gap_rel: float


def _normalized_laplacian(graph: base.GraphFamily):
    lap = base._graph_laplacian(graph).tocsr()
    diag = np.asarray(lap.diagonal(), dtype=float)
    inv_sqrt = np.zeros_like(diag)
    mask = diag > 0
    inv_sqrt[mask] = 1.0 / np.sqrt(diag[mask])
    d_inv = diags(inv_sqrt)
    return d_inv @ lap @ d_inv


def _source_density(graph: base.GraphFamily, source_nodes: list[int], strengths: list[float]) -> np.ndarray:
    return base._source_density(graph, source_nodes, strengths)


def _apply_mapping(graph: base.GraphFamily, rho: np.ndarray, spec: MappingSpec, ln=None) -> np.ndarray:
    if spec.mode == "identity":
        return rho.astype(float, copy=True)
    if ln is None:
        ln = _normalized_laplacian(graph)

    if spec.mode == "lap_sharpen":
        mapped = rho.astype(float, copy=True)
        for _ in range(max(spec.steps, 1)):
            mapped = mapped + spec.beta * (ln @ mapped)
        return np.asarray(mapped, dtype=float)
    if spec.mode == "inverse_heat":
        return np.asarray(expm_multiply(spec.beta * ln, rho), dtype=float)
    raise ValueError(f"unknown mapping mode: {spec.mode}")


def _mean_graph_force_gap(results: list[IterativeResult]) -> float:
    if not results:
        return float("nan")
    return statistics.fmean(r.force_gap_rel for r in results)


def _measure_family(graph: base.GraphFamily, spec: MappingSpec) -> IterativeResult:
    n = graph.positions.shape[0]
    ln = _normalized_laplacian(graph)
    source_nodes = [graph.source]
    psi0 = base._probe_state(graph.positions, graph.source, k0=0.18)

    rho_zero = np.zeros(n, dtype=float)
    phi_zero = base._solve_phi(graph, rho_zero)
    H_zero = base._build_hamiltonian(graph, MASS, phi_zero)
    psi_zero = base._evolve_cn(H_zero, psi0, DT, N_STEPS)
    zero_force = base._force_from_phi(graph, psi_zero, phi_zero)
    norm_drift = abs(np.linalg.norm(psi_zero) - 1.0)

    rho_source = _source_density(graph, source_nodes, [1.0])
    rho_eff = _apply_mapping(graph, rho_source, spec, ln=ln)
    phi_solve = base._solve_phi(graph, rho_eff)
    phi_ext = base._external_phi(graph, source_nodes, [1.0])

    psi_solve = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_solve), psi0, DT, N_STEPS)
    psi_ext = base._evolve_cn(base._build_hamiltonian(graph, MASS, phi_ext), psi0, DT, N_STEPS)
    force_solve = base._force_from_phi(graph, psi_solve, phi_solve)
    force_ext = base._force_from_phi(graph, psi_ext, phi_ext)
    force_gap_rel = abs(force_solve - force_ext) / max(abs(force_ext), 1e-30)

    strengths = list(SOURCE_STRENGTHS)
    forces = []
    for strength in strengths:
        rho = _source_density(graph, source_nodes, [strength])
        rho_map = _apply_mapping(graph, rho, spec, ln=ln)
        phi = base._solve_phi(graph, rho_map)
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
    phi_a = base._solve_phi(graph, _apply_mapping(graph, rho_a, spec, ln=ln))
    phi_b = base._solve_phi(graph, _apply_mapping(graph, rho_b, spec, ln=ln))
    phi_ab = base._solve_phi(graph, _apply_mapping(graph, rho_ab, spec, ln=ln))
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

    # One-step endogenous update: source density gets refreshed by the evolved
    # probe density, then mapped through the same linear source operator.
    rho_self = np.abs(psi_solve) ** 2
    rho_self *= max(np.sum(rho_eff), 1e-30) / max(np.sum(rho_self), 1e-30)
    phi_self = base._solve_phi(graph, _apply_mapping(graph, rho_self, spec, ln=ln))
    self_force = base._force_from_phi(graph, psi_solve, phi_self)
    self_gap_rel = abs(self_force - force_solve) / max(abs(force_solve), 1e-30)

    toward_total = 3
    toward_samples = int(zero_force >= -F_TOL) + int(force_solve > 0) + int(force_ext > 0)
    return IterativeResult(
        mapping=spec.name,
        family=graph.name,
        n=n,
        zero_force=zero_force,
        ext_force=force_ext,
        solve_force=force_solve,
        force_gap_rel=force_gap_rel,
        source_r2=source_r2,
        two_body_resid=two_body_resid,
        toward_fraction=toward_samples,
        toward_total=toward_total,
        norm_drift=norm_drift,
        self_force=self_force,
        self_gap_rel=self_gap_rel,
    )


def _print_result(r: IterativeResult) -> None:
    print(
        f"{r.mapping:<18} {r.family:<26} "
        f"n={r.n:<3d} "
        f"F_ext={r.ext_force:+.3e} "
        f"F_solve={r.solve_force:+.3e} "
        f"gap={r.force_gap_rel:.3e} "
        f"R2={r.source_r2:.4f} "
        f"2body={r.two_body_resid:.3e} "
        f"selfF={r.self_force:+.3e} "
        f"self_gap={r.self_gap_rel:.3e} "
        f"norm={r.norm_drift:.2e} "
        f"TOWARD={r.toward_fraction}/{r.toward_total}"
    )


def main() -> None:
    t0 = time.time()
    mappings = [
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

    graphs = base._make_graphs()
    cycle_bearing = [g for g in graphs if g.has_cycle]

    print("=" * 100)
    print("STAGGERED BACKREACTION ITERATIVE SOURCE-MAPPING PROBE")
    print("  transport law fixed; only the source->field map is varied")
    print("  primary observable: force F = < -dPhi/dd >")
    print("=" * 100)
    print(
        f"dt={DT}, steps={N_STEPS}, mass={MASS}, mu2={POISSON_MU2}, "
        f"ext_mu={EXT_KERNEL_MU}, source_sigma={SOURCE_SIGMA}"
    )
    print()

    all_results: list[IterativeResult] = []
    for spec in mappings:
        print(f"== mapping: {spec.name} ==")
        for graph in graphs:
            result = _measure_family(graph, spec)
            all_results.append(result)
            _print_result(result)
        print()

    print("SUMMARY")
    by_map: dict[str, list[IterativeResult]] = {}
    by_map_cycle: dict[str, list[IterativeResult]] = {}
    for r in all_results:
        by_map.setdefault(r.mapping, []).append(r)
        if "layered" not in r.family:
            by_map_cycle.setdefault(r.mapping, []).append(r)

    baseline = by_map_cycle["gaussian"]
    baseline_gap = _mean_graph_force_gap(baseline)
    print(f"  baseline cycle-bearing mean gap: {baseline_gap:.3e}")
    best_name = None
    best_gap = float("inf")
    for name, vals in by_map_cycle.items():
        gap = _mean_graph_force_gap(vals)
        if gap < best_gap:
            best_gap = gap
            best_name = name
    print(f"  best cycle-bearing mean gap: {best_gap:.3e} ({best_name})")
    print(f"  gap improvement factor: {baseline_gap / max(best_gap, 1e-30):.2f}x")
    print(
        f"  baseline source-response R^2 mean: {statistics.fmean(r.source_r2 for r in baseline):.4f}"
    )
    print(
        f"  best-map source-response R^2 mean: "
        f"{statistics.fmean(r.source_r2 for r in by_map[best_name]):.4f}"
    )
    print(
        f"  baseline self-gap mean: {statistics.fmean(r.self_gap_rel for r in baseline):.3e}"
    )
    print(
        f"  best-map self-gap mean: "
        f"{statistics.fmean(r.self_gap_rel for r in by_map[best_name]):.3e}"
    )
    print(
        f"  baseline norm drift mean: {statistics.fmean(r.norm_drift for r in baseline):.3e}"
    )
    print(
        f"  best-map norm drift mean: "
        f"{statistics.fmean(r.norm_drift for r in by_map[best_name]):.3e}"
    )
    print(f"  runtime: {time.time() - t0:.2f}s")
    print()
    print("Readout:")
    print("  - This is a linear source-mapping probe, not a transport-law change.")
    print("  - A mapping counts as materially improved only if it reduces the")
    print("    cycle-bearing mean force gap substantially without losing TOWARD,")
    print("    linearity, additivity, or norm stability.")
    print("  - The next step is to keep the best retained map only if it beats the")
    print("    external-kernel control on the cycle-bearing families by more than a")
    print("    small calibration margin.")


if __name__ == "__main__":
    main()
