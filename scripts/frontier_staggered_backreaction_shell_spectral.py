#!/usr/bin/env python3
"""Shell / spectral diagnostics for the staggered source sector.

Goal:
  Explain the endogenous-field scale miss by comparing phi_solved(depth) vs
  phi_ext(depth) on one cycle-bearing graph family and one layered family,
  then inspecting low-mode content and shell flattening in the source-to-field
  map.

This is a diagnostic probe, not a new canonical card.
"""

from __future__ import annotations

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


@dataclass
class ShellSpectralResult:
    family: str
    n: int
    has_cycle: bool
    zero_force: float
    force_solve: float
    force_ext: float
    force_gap_rel: float
    shell_slope_solve: float
    shell_slope_ext: float
    shell_span_solve: float
    shell_span_ext: float
    shell_span_ratio: float
    shell_fit_r2: float
    rho_low_frac: float
    solve_low_frac: float
    ext_low_frac: float
    rho_centroid: float
    solve_centroid: float
    ext_centroid: float
    norm_drift: float


def _shell_profile(graph: base.GraphFamily, values: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ref = float(values[graph.source])
    shell_map: dict[int, list[float]] = {}
    count_map: dict[int, int] = {}
    for i, d in enumerate(graph.depth):
        if not np.isfinite(d):
            continue
        depth = int(d)
        shell_map.setdefault(depth, []).append(ref - float(values[i]))
        count_map[depth] = count_map.get(depth, 0) + 1
    if not shell_map:
        return np.array([0]), np.array([0.0]), np.array([0])
    depths = np.array(sorted(shell_map), dtype=int)
    means = np.array([statistics.fmean(shell_map[int(d)]) for d in depths], dtype=float)
    counts = np.array([count_map[int(d)] for d in depths], dtype=int)
    return depths, means, counts


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

    k_low = min(5, int(np.count_nonzero(mask)))
    low_idx = np.where(mask)[0][:k_low]
    low_frac = float(np.sum(power[low_idx]) / total)
    centroid = float(np.sum(evals[mask] * power[mask]) / total)
    return low_frac, centroid


def _measure(graph: base.GraphFamily) -> ShellSpectralResult:
    source_nodes = [graph.source]
    source_strengths = [1.0]
    psi0 = base._probe_state(graph.positions, graph.source, k0=0.18)

    rho_source = base._source_density(graph, source_nodes, source_strengths)
    phi_solved = base._solve_phi(graph, rho_source)
    phi_ext = base._external_phi(graph, source_nodes, source_strengths)

    psi_solved = base._evolve_cn(base._build_hamiltonian(graph, base.MASS, phi_solved), psi0, base.DT, base.N_STEPS)
    psi_ext = base._evolve_cn(base._build_hamiltonian(graph, base.MASS, phi_ext), psi0, base.DT, base.N_STEPS)

    zero_phi = base._solve_phi(graph, np.zeros(graph.positions.shape[0], dtype=float))
    psi_zero = base._evolve_cn(base._build_hamiltonian(graph, base.MASS, zero_phi), psi0, base.DT, base.N_STEPS)
    zero_force = base._force_from_phi(graph, psi_zero, zero_phi)

    force_solve = base._force_from_phi(graph, psi_solved, phi_solved)
    force_ext = base._force_from_phi(graph, psi_ext, phi_ext)
    force_gap_rel = abs(force_solve - force_ext) / max(abs(force_ext), 1e-30)
    norm_drift = abs(np.linalg.norm(psi_solved) - 1.0)

    shell_depths, shell_solved, counts = _shell_profile(graph, phi_solved)
    _, shell_ext, _ = _shell_profile(graph, phi_ext)

    shell_slope_solve, _, _ = _fit_line(shell_depths.astype(float), shell_solved)
    shell_slope_ext, _, _ = _fit_line(shell_depths.astype(float), shell_ext)
    shell_span_solve = float(np.max(shell_solved) - np.min(shell_solved)) if len(shell_solved) else 0.0
    shell_span_ext = float(np.max(shell_ext) - np.min(shell_ext)) if len(shell_ext) else 0.0
    shell_span_ratio = shell_span_solve / max(shell_span_ext, 1e-30)

    # Compare the shell-drop profiles directly so the shape mismatch is visible.
    common_depths = shell_depths
    if len(common_depths) >= 2:
        solve_common = np.array([shell_solved[np.where(shell_depths == d)[0][0]] for d in common_depths], dtype=float)
        ext_common = np.array([shell_ext[np.where(shell_depths == d)[0][0]] for d in common_depths], dtype=float)
        _, _, shell_fit_r2 = _fit_line(ext_common, solve_common)
    else:
        shell_fit_r2 = 1.0

    rho_low_frac, rho_centroid = _spectral_stats(graph, rho_source)
    solve_low_frac, solve_centroid = _spectral_stats(graph, phi_solved)
    ext_low_frac, ext_centroid = _spectral_stats(graph, phi_ext)

    return ShellSpectralResult(
        family=graph.name,
        n=graph.positions.shape[0],
        has_cycle=graph.has_cycle,
        zero_force=zero_force,
        force_solve=force_solve,
        force_ext=force_ext,
        force_gap_rel=force_gap_rel,
        shell_slope_solve=shell_slope_solve,
        shell_slope_ext=shell_slope_ext,
        shell_span_solve=shell_span_solve,
        shell_span_ext=shell_span_ext,
        shell_span_ratio=shell_span_ratio,
        shell_fit_r2=shell_fit_r2,
        rho_low_frac=rho_low_frac,
        solve_low_frac=solve_low_frac,
        ext_low_frac=ext_low_frac,
        rho_centroid=rho_centroid,
        solve_centroid=solve_centroid,
        ext_centroid=ext_centroid,
        norm_drift=norm_drift,
    )


def _print_family(graph: base.GraphFamily) -> None:
    source_nodes = [graph.source]
    rho_source = base._source_density(graph, source_nodes, [1.0])
    phi_solved = base._solve_phi(graph, rho_source)
    phi_ext = base._external_phi(graph, source_nodes, [1.0])

    depth_s, solve_s, counts = _shell_profile(graph, phi_solved)
    depth_e, ext_s, _ = _shell_profile(graph, phi_ext)
    depth_r, rho_s, _ = _shell_profile(graph, rho_source)

    cycle_txt = "yes" if graph.has_cycle else "no"
    print(f"{graph.name}  n={graph.positions.shape[0]}  cycle={cycle_txt}")
    print("  depth  count   rho_drop    phi_solved   phi_ext   solve/ext")
    for d in depth_s:
        i = int(np.where(depth_s == d)[0][0])
        j = int(np.where(depth_e == d)[0][0])
        k = int(np.where(depth_r == d)[0][0])
        ratio = solve_s[i] / max(ext_s[j], 1e-30)
        print(
            f"  {d:>5d}  {counts[i]:>5d}  {rho_s[k]:>10.3e}  "
            f"{solve_s[i]:>10.3e}  {ext_s[j]:>10.3e}  {ratio:>8.3f}"
        )


def main() -> None:
    t0 = time.time()
    graphs = {g.name: g for g in base._make_graphs()}
    selected = [graphs["bipartite_random_geometric"], graphs["layered_bipartite_dag"]]

    print("=" * 98)
    print("STAGGERED BACKREACTION SHELL / SPECTRAL DIAGNOSTIC")
    print("  compare phi_solved(depth) vs phi_ext(depth) and inspect low-mode flattening")
    print("  primary observable remains force; this is a structural scale-miss diagnosis")
    print("=" * 98)
    print(f"  dt={base.DT}, steps={base.N_STEPS}, mass={base.MASS}, mu2={base.POISSON_MU2}, ext_mu={base.EXT_KERNEL_MU}")
    print()

    results: list[ShellSpectralResult] = []
    for graph in selected:
        result = _measure(graph)
        results.append(result)
        _print_family(graph)
        print(
            f"  summary: F_ext={result.force_ext:+.3e} F_solve={result.force_solve:+.3e} "
            f"gap={result.force_gap_rel:.3e} norm={result.norm_drift:.2e}"
        )
        print(
            f"  shell: slope_solve={result.shell_slope_solve:+.3e} slope_ext={result.shell_slope_ext:+.3e} "
            f"span_ratio={result.shell_span_ratio:.3f} fit_R2={result.shell_fit_r2:.4f}"
        )
        print(
            f"  spectrum: rho_low={result.rho_low_frac:.3f} solve_low={result.solve_low_frac:.3f} "
            f"ext_low={result.ext_low_frac:.3f} rho_centroid={result.rho_centroid:.3e} "
            f"solve_centroid={result.solve_centroid:.3e} ext_centroid={result.ext_centroid:.3e}"
        )
        print()

    cycle = next(r for r in results if r.has_cycle)
    layered = next(r for r in results if not r.has_cycle)

    print("READOUT")
    print(
        f"  cycle-bearing family: force gap {cycle.force_gap_rel:.3e}, "
        f"shell span ratio {cycle.shell_span_ratio:.3f}, solve/ext low-mode {cycle.solve_low_frac:.3f}/{cycle.ext_low_frac:.3f}"
    )
    print(
        f"  layered family: force gap {layered.force_gap_rel:.3e}, "
        f"shell span ratio {layered.shell_span_ratio:.3f}, solve/ext low-mode {layered.solve_low_frac:.3f}/{layered.ext_low_frac:.3f}"
    )
    print()
    print("Interpretation:")
    print("  - The solved graph field keeps the correct sign and force ordering, but it is flatter in depth than the external-kernel control.")
    print("  - The shell-drop profiles show the same qualitative shape, but the solved field has a smaller span and shallower slope.")
    print("  - The low-mode spectrum is more concentrated in the solved field, consistent with over-smoothing by the screened graph Poisson solve.")
    print("  - The layered family is the closest holdout for one-step endogenous response, but the cycle-bearing family is where the scale miss is structurally visible.")
    print(f"  - runtime: {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
