#!/usr/bin/env python3
"""Nonlocal fractional-Green closure probe for staggered backreaction.

Goal:
  Attack the endogenous-field force-scale miss with a genuinely different
  source-to-field map while keeping the staggered transport law fixed.

What is changed:
  - source sector only: use a fractional Green operator in Laplacian spectral
    space, (L + mu^2 I)^(-alpha), instead of the local screened Poisson solve
  - transport law is unchanged
  - force remains the primary gravity observable

What is measured:
  - zero-source control
  - source-response linearity
  - two-body additivity
  - norm stability
  - TOWARD sign
  - calibrated cycle-bearing force gap vs the external-kernel control
  - shell / spectral flattening relative to the external kernel

This is deliberately narrow. The question is whether a nonlocal source sector
can materially reduce the over-smoothing diagnosed in the shell/spectral note
without breaking the retained battery.
"""

from __future__ import annotations

import math
import os
import statistics
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

import frontier_staggered_backreaction_prototype as base  # noqa: E402


ALPHAS = (1.00, 0.80, 0.60, 0.40, 0.20, 0.10, 0.00)
GAIN_GRID = np.geomspace(0.25, 64.0, 41)


@dataclass(frozen=True)
class NonlocalSpec:
    name: str
    alpha: float


@dataclass
class FamilyCache:
    graph: base.GraphFamily
    rho_source: np.ndarray
    phi_raw: np.ndarray
    phi_ext: np.ndarray
    force_ext: float
    shell_ext: np.ndarray
    shell_solved: np.ndarray
    shell_depths: np.ndarray
    shell_ratio: float
    shell_fit_r2: float
    rho_low_frac: float
    raw_low_frac: float
    ext_low_frac: float
    rho_centroid: float
    raw_centroid: float
    ext_centroid: float


@dataclass
class FamilyResult:
    alpha: float
    gain: float
    family: str
    n: int
    zero_force: float
    force_ext: float
    force_raw: float
    force_cal: float
    raw_gap_rel: float
    cal_gap_rel: float
    source_r2: float
    two_body_resid: float
    toward_fraction: int
    toward_total: int
    norm_drift: float
    self_gap_rel: float
    shell_ratio: float
    shell_fit_r2: float
    rho_low_frac: float
    raw_low_frac: float
    ext_low_frac: float
    rho_centroid: float
    raw_centroid: float
    ext_centroid: float


def _fractional_green_phi(graph: base.GraphFamily, rho: np.ndarray, alpha: float) -> np.ndarray:
    if np.allclose(rho, 0.0):
        return np.zeros_like(rho)
    lap = base._graph_laplacian(graph).toarray()
    evals, evecs = np.linalg.eigh(lap)
    shifted = np.maximum(evals + base.POISSON_MU2, 1e-12)
    weights = shifted ** (-alpha)
    coeff = evecs.T @ rho
    phi = evecs @ (weights * coeff)
    return np.asarray(np.real_if_close(phi), dtype=float)


def _shell_profile(graph: base.GraphFamily, values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    shell_map: dict[int, list[float]] = {}
    for i, d in enumerate(graph.depth):
        if not np.isfinite(d):
            continue
        shell_map.setdefault(int(d), []).append(float(values[i]))
    if not shell_map:
        return np.array([0], dtype=int), np.array([0.0], dtype=float)
    shells = np.array(sorted(shell_map), dtype=int)
    means = np.array([statistics.fmean(shell_map[int(d)]) for d in shells], dtype=float)
    return shells, means


def _fit_line(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    if len(x) < 2:
        return 0.0, 0.0, 1.0
    coeff = np.polyfit(x, y, 1)
    pred = np.polyval(coeff, x)
    denom = float(np.sum((y - np.mean(y)) ** 2))
    if denom <= 0:
        r2 = 1.0
    else:
        r2 = 1.0 - float(np.sum((y - pred) ** 2) / denom)
    return float(coeff[0]), float(coeff[1]), float(r2)


def _spectral_stats(graph: base.GraphFamily, values: np.ndarray) -> tuple[float, float]:
    lap = base._graph_laplacian(graph).toarray()
    evals, evecs = np.linalg.eigh(lap)
    mask = evals > 1e-10
    if not np.any(mask):
        return 0.0, 0.0
    centered = values - np.mean(values)
    coeff = evecs.T @ centered
    power = np.abs(coeff) ** 2
    total = float(np.sum(power[mask]))
    if total <= 0:
        return 0.0, 0.0
    low_idx = np.where(mask)[0][: min(5, int(np.count_nonzero(mask)))]
    low_frac = float(np.sum(power[low_idx]) / total)
    centroid = float(np.sum(evals[mask] * power[mask]) / total)
    return low_frac, centroid


def _build_cache(graph: base.GraphFamily) -> FamilyCache:
    rho_source = base._source_density(graph, [graph.source], [1.0])
    phi_ext = base._external_phi(graph, [graph.source], [1.0])
    phi_raw = _fractional_green_phi(graph, rho_source, alpha=1.0)
    shell_depths, shell_raw = _shell_profile(graph, phi_raw)
    _, shell_ext = _shell_profile(graph, phi_ext)
    shell_ratio = float(np.max(shell_raw) - np.min(shell_raw)) / max(float(np.max(shell_ext) - np.min(shell_ext)), 1e-30)
    shell_fit_r2 = _fit_line(shell_ext, shell_raw)[2] if len(shell_ext) >= 2 else 1.0
    rho_low_frac, rho_centroid = _spectral_stats(graph, rho_source)
    raw_low_frac, raw_centroid = _spectral_stats(graph, phi_raw)
    ext_low_frac, ext_centroid = _spectral_stats(graph, phi_ext)
    force_ext = base._force_from_phi(
        graph,
        base._evolve_cn(base._build_hamiltonian(graph, base.MASS, phi_ext), base._probe_state(graph.positions, graph.source, k0=0.18), base.DT, base.N_STEPS),
        phi_ext,
    )
    return FamilyCache(
        graph=graph,
        rho_source=rho_source,
        phi_raw=phi_raw,
        phi_ext=phi_ext,
        force_ext=force_ext,
        shell_ext=shell_ext,
        shell_solved=shell_raw,
        shell_depths=shell_depths,
        shell_ratio=shell_ratio,
        shell_fit_r2=shell_fit_r2,
        rho_low_frac=rho_low_frac,
        raw_low_frac=raw_low_frac,
        ext_low_frac=ext_low_frac,
        rho_centroid=rho_centroid,
        raw_centroid=raw_centroid,
        ext_centroid=ext_centroid,
    )


def _force_and_state(graph: base.GraphFamily, phi: np.ndarray) -> tuple[float, np.ndarray, float]:
    psi0 = base._probe_state(graph.positions, graph.source, k0=0.18)
    H = base._build_hamiltonian(graph, base.MASS, phi)
    psi = base._evolve_cn(H, psi0, base.DT, base.N_STEPS)
    force = base._force_from_phi(graph, psi, phi)
    norm_drift = abs(np.linalg.norm(psi) - 1.0)
    return force, psi, norm_drift


def _calibrated_gap(caches: list[FamilyCache], alpha: float, gain: float) -> tuple[float, list[float]]:
    gaps = []
    forces = []
    for cache in caches:
        phi = gain * _fractional_green_phi(cache.graph, cache.rho_source, alpha)
        force, _, _ = _force_and_state(cache.graph, phi)
        gaps.append(abs(force - cache.force_ext) / max(abs(cache.force_ext), 1e-30))
        forces.append(force)
    return float(statistics.fmean(gaps)), forces


def _fit_gain(caches: list[FamilyCache], alpha: float, gain_grid: np.ndarray) -> tuple[float, float]:
    best_gain = float(gain_grid[0])
    best_gap = float("inf")
    for gain in gain_grid:
        gap, _ = _calibrated_gap(caches, alpha, float(gain))
        if gap < best_gap:
            best_gap = gap
            best_gain = float(gain)
    return best_gain, best_gap


def _measure_family(graph: base.GraphFamily, alpha: float, gain: float) -> FamilyResult:
    rho_source = base._source_density(graph, [graph.source], [1.0])
    phi_raw = _fractional_green_phi(graph, rho_source, alpha)
    phi_cal = gain * phi_raw
    phi_ext = base._external_phi(graph, [graph.source], [1.0])

    force_raw, psi_raw, norm_raw = _force_and_state(graph, phi_raw)
    force_cal, psi_cal, norm_cal = _force_and_state(graph, phi_cal)
    force_ext, psi_ext, _ = _force_and_state(graph, phi_ext)

    raw_gap_rel = abs(force_raw - force_ext) / max(abs(force_ext), 1e-30)
    cal_gap_rel = abs(force_cal - force_ext) / max(abs(force_ext), 1e-30)

    strengths = list(base.SOURCE_STRENGTHS)
    forces = []
    for s in strengths:
        phi = gain * _fractional_green_phi(graph, base._source_density(graph, [graph.source], [s]), alpha)
        forces.append(_force_and_state(graph, phi)[0])
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
        partner = max(range(graph.positions.shape[0]), key=lambda i: graph.depth[i] if np.isfinite(graph.depth[i]) else -1)
    rho_a = base._source_density(graph, [graph.source], [1.0])
    rho_b = base._source_density(graph, [partner], [1.0])
    rho_ab = base._source_density(graph, [graph.source, partner], [1.0, 1.0])
    phi_a = gain * _fractional_green_phi(graph, rho_a, alpha)
    phi_b = gain * _fractional_green_phi(graph, rho_b, alpha)
    phi_ab = gain * _fractional_green_phi(graph, rho_ab, alpha)
    denom = max(np.linalg.norm(phi_ab), 1e-30)
    phi_residual = float(np.linalg.norm(phi_ab - (phi_a + phi_b)) / denom)
    force_ab = _force_and_state(graph, phi_ab)[0]
    force_add = _force_and_state(graph, phi_a + phi_b)[0]
    two_body_resid = abs(force_ab - force_add) / max(abs(force_ab), 1e-30)

    rho_self = np.abs(psi_cal) ** 2
    rho_self *= max(np.sum(rho_source), 1e-30) / max(np.sum(rho_self), 1e-30)
    phi_self = gain * _fractional_green_phi(graph, rho_self, alpha)
    self_force = _force_and_state(graph, phi_self)[0]
    self_gap_rel = abs(self_force - force_cal) / max(abs(force_cal), 1e-30)

    toward_total = 3
    toward_fraction = int(force_raw > 0) + int(force_cal > 0) + int(force_ext > 0)

    shell_depths, shell_raw = _shell_profile(graph, phi_raw)
    _, shell_ext = _shell_profile(graph, phi_ext)
    shell_ratio = float(np.max(shell_raw) - np.min(shell_raw)) / max(float(np.max(shell_ext) - np.min(shell_ext)), 1e-30)
    shell_fit_r2 = _fit_line(shell_ext, shell_raw)[2] if len(shell_ext) >= 2 else 1.0
    rho_low_frac, rho_centroid = _spectral_stats(graph, rho_source)
    raw_low_frac, raw_centroid = _spectral_stats(graph, phi_raw)
    ext_low_frac, ext_centroid = _spectral_stats(graph, phi_ext)

    return FamilyResult(
        alpha=alpha,
        gain=gain,
        family=graph.name,
        n=graph.positions.shape[0],
        zero_force=_force_and_state(graph, np.zeros_like(phi_raw))[0],
        force_ext=force_ext,
        force_raw=force_raw,
        force_cal=force_cal,
        raw_gap_rel=raw_gap_rel,
        cal_gap_rel=cal_gap_rel,
        source_r2=source_r2,
        two_body_resid=two_body_resid,
        toward_fraction=toward_fraction,
        toward_total=toward_total,
        norm_drift=max(norm_raw, norm_cal),
        self_gap_rel=self_gap_rel,
        shell_ratio=shell_ratio,
        shell_fit_r2=shell_fit_r2,
        rho_low_frac=rho_low_frac,
        raw_low_frac=raw_low_frac,
        ext_low_frac=ext_low_frac,
        rho_centroid=rho_centroid,
        raw_centroid=raw_centroid,
        ext_centroid=ext_centroid,
    )


def _mean_gap(results: list[FamilyResult]) -> float:
    return statistics.fmean(r.cal_gap_rel for r in results) if results else float("nan")


def main() -> None:
    t0 = time.time()
    graphs = base._make_graphs()
    caches = [_build_cache(g) for g in graphs]
    cycle_caches = [c for c in caches if "layered" not in c.graph.name]

    print("=" * 110)
    print("STAGGERED NONLOCAL / FRACTIONAL-GREEN CLOSURE PROBE")
    print("  source sector varies; transport law fixed")
    print("  primary observable: force F = < -dPhi/dd >")
    print("=" * 110)
    print(
        f"dt={base.DT}, steps={base.N_STEPS}, mass={base.MASS}, mu2={base.POISSON_MU2}, "
        f"ext_mu={base.EXT_KERNEL_MU}, source_sigma={base.SOURCE_SIGMA}"
    )
    print(f"alphas={ALPHAS}")
    print()

    baseline_gain, baseline_cycle_gap = _fit_gain(cycle_caches, alpha=1.0, gain_grid=GAIN_GRID)
    print(f"baseline alpha=1.00 best gain={baseline_gain:.3f} cycle-gap={baseline_cycle_gap:.3e}")
    print()

    summary_rows: list[tuple[float, float, float]] = []
    all_results: list[FamilyResult] = []
    for alpha in ALPHAS:
        gain, cycle_gap = _fit_gain(cycle_caches, alpha=alpha, gain_grid=GAIN_GRID)
        summary_rows.append((alpha, gain, cycle_gap))
        print(f"== alpha={alpha:.2f} gain={gain:.3f} cycle-gap={cycle_gap:.3e} ==")
        for cache in caches:
            result = _measure_family(cache.graph, alpha, gain)
            all_results.append(result)
            print(
                f"{result.family:<26} n={result.n:<3d} "
                f"F_ext={result.force_ext:+.3e} F_raw={result.force_raw:+.3e} "
                f"F_cal={result.force_cal:+.3e} "
                f"raw_gap={result.raw_gap_rel:.3e} cal_gap={result.cal_gap_rel:.3e} "
                f"R2={result.source_r2:.4f} 2body={result.two_body_resid:.3e} "
                f"self_gap={result.self_gap_rel:.3e} norm={result.norm_drift:.2e} "
                f"TOWARD={result.toward_fraction}/{result.toward_total}"
            )
        print()

    by_alpha: dict[float, list[FamilyResult]] = {}
    for r in all_results:
        by_alpha.setdefault(r.alpha, []).append(r)

    best_alpha, best_gain, best_cycle_gap = min(summary_rows, key=lambda t: t[2])
    best_results = by_alpha[best_alpha]
    baseline_results = by_alpha[1.0]

    print("SUMMARY")
    print(f"  baseline calibrated linear cycle gap: {baseline_cycle_gap:.3e} (alpha=1.00, gain={baseline_gain:.3f})")
    print(f"  best calibrated cycle gap: {best_cycle_gap:.3e} (alpha={best_alpha:.2f}, gain={best_gain:.3f})")
    print(
        f"  improvement factor vs calibrated linear: "
        f"{baseline_cycle_gap / max(best_cycle_gap, 1e-30):.2f}x"
    )
    print(
        f"  baseline holdout gap (layered): "
        f"{statistics.fmean(r.cal_gap_rel for r in baseline_results if 'layered' in r.family):.3e}"
    )
    print(
        f"  best holdout gap (layered): "
        f"{statistics.fmean(r.cal_gap_rel for r in best_results if 'layered' in r.family):.3e}"
    )
    print(f"  baseline source-response R2 mean: {statistics.fmean(r.source_r2 for r in baseline_results):.4f}")
    print(f"  best source-response R2 mean: {statistics.fmean(r.source_r2 for r in best_results):.4f}")
    print(
        f"  baseline two-body resid max: {max(r.two_body_resid for r in baseline_results):.3e}"
    )
    print(f"  best two-body resid max: {max(r.two_body_resid for r in best_results):.3e}")
    print(f"  baseline norm drift max: {max(r.norm_drift for r in baseline_results):.3e}")
    print(f"  best norm drift max: {max(r.norm_drift for r in best_results):.3e}")
    print()
    print("Shell / spectral readout for the best candidate:")
    for cache in caches:
        if "layered" not in cache.graph.name:
            r = next(r for r in best_results if r.family == cache.graph.name)
            print(
                f"  {cache.graph.name}: shell_ratio={r.shell_ratio:.3f}, "
                f"shell_fit_R2={r.shell_fit_r2:.4f}, "
                f"rho_low={r.rho_low_frac:.3f}, raw_low={r.raw_low_frac:.3f}, ext_low={r.ext_low_frac:.3f}, "
                f"raw_centroid={r.raw_centroid:.3e}, ext_centroid={r.ext_centroid:.3e}"
            )
    print(f"  runtime: {time.time() - t0:.2f}s")
    print()
    print("Readout:")
    print("  - alpha=1.00 is the local screened-Poisson baseline.")
    print("  - alpha<1.00 is a nonlocal fractional-Green source sector that should")
    print("    reduce low-mode over-smoothing if it helps.")
    print("  - The map counts as a real improvement only if the calibrated cycle-bearing")
    print("    force gap drops materially below the calibrated linear baseline while")
    print("    preserving TOWARD sign, linearity, additivity, and norm stability.")


if __name__ == "__main__":
    main()
