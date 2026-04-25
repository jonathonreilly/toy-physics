#!/usr/bin/env python3
"""Backreaction observable split on larger staggered graph stress families.

This is the P2 follow-up to the graph-observables backlog:

  1. keep the larger stress graph families from
     frontier_staggered_graph_portability_stress.py,
  2. replace the imposed depth potential by the retained graph-native
     resistance-Yukawa Green source sector, and
  3. re-run the force/current observable split without changing the canonical
     staggered cards.

Rows are intentionally source-sector rows, not a new universal card:

  - zero-source exactness
  - norm preservation
  - endogenous force sign
  - source-response linearity
  - two-body field additivity
  - achromatic force
  - robustness over probe momenta
  - native gauge/current when cycles exist
"""

from __future__ import annotations

import math
import os
import sys
import time
from dataclasses import dataclass

import numpy as np
from scipy.sparse import eye as speye
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_graph_portability as base
import frontier_staggered_graph_portability_stress as stress


MASS = base.MASS
DT = base.DT
N_STEPS = base.N_STEPS
SOURCE_SIGMA = 0.90
GREEN_MU = 1.50
GREEN_EPS = 0.10
STRENGTHS = (0.0, 0.25, 0.50, 1.0, 2.0)
ACHROM_K = (0.0, 0.12, 0.24, 0.36, 0.48)
ROBUST_K = (0.0, 0.2, 0.4)


@dataclass
class BackreactionObsResult:
    family: str
    n: int
    edges: int
    has_cycle: bool
    retained_passes: int
    retained_total: int
    zero_force: float
    norm_drift: float
    source_force: float
    source_r2: float
    two_body_resid: float
    achrom_cv: float
    robust_toward: int
    robust_total: int
    gauge_status: str
    gauge_j_range: float | None
    centroid_shift: float
    shell_bias: float


def _edge_count(graph: base.GraphFamily) -> int:
    return sum(len(nbs) for nbs in graph.adj.values()) // 2


def _source_density(graph: base.GraphFamily, node: int, strength: float = 1.0) -> np.ndarray:
    center = graph.positions[node]
    rel = graph.positions - center
    weights = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / SOURCE_SIGMA**2)
    weights = weights / max(float(np.sum(weights)), 1e-30)
    return strength * weights


def _weighted_laplacian(graph: base.GraphFamily) -> np.ndarray:
    n = graph.positions.shape[0]
    lap = np.zeros((n, n), dtype=float)
    for i, nbs in graph.adj.items():
        for j in nbs:
            if i >= j:
                continue
            dx = graph.positions[j, 0] - graph.positions[i, 0]
            dy = graph.positions[j, 1] - graph.positions[i, 1]
            dist = math.hypot(dx, dy)
            weight = 1.0 / max(dist, 0.5)
            lap[i, j] -= weight
            lap[j, i] -= weight
            lap[i, i] += weight
            lap[j, j] += weight
    return lap


def _resistance_distance(graph: base.GraphFamily) -> np.ndarray:
    lap = _weighted_laplacian(graph)
    evals, evecs = np.linalg.eigh(lap)
    inv = np.zeros_like(evals)
    mask = evals > 1e-10
    inv[mask] = 1.0 / evals[mask]
    lap_pinv = (evecs * inv) @ evecs.T
    diag = np.clip(np.diag(lap_pinv), 0.0, None)
    resistance = np.maximum(diag[:, None] + diag[None, :] - 2.0 * lap_pinv, 0.0)
    return np.sqrt(resistance)


def _green_kernel(graph: base.GraphFamily) -> np.ndarray:
    metric = _resistance_distance(graph)
    return np.exp(-GREEN_MU * metric) / (metric + GREEN_EPS)


def _build_hamiltonian_phi(
    graph: base.GraphFamily,
    phi: np.ndarray,
    flux: float = 0.0,
    flux_edge: tuple[int, int] | None = None,
):
    n = graph.positions.shape[0]
    hamiltonian = lil_matrix((n, n), dtype=complex)
    parity = np.where(graph.colors == 0, 1.0, -1.0)
    hamiltonian.setdiag((MASS + phi) * parity)

    phase_edge = None
    if flux_edge is not None:
        a, b = flux_edge
        phase_edge = (min(a, b), max(a, b))

    for i, nbs in graph.adj.items():
        for j in nbs:
            if i >= j:
                continue
            dx = graph.positions[j, 0] - graph.positions[i, 0]
            dy = graph.positions[j, 1] - graph.positions[i, 1]
            dist = math.hypot(dx, dy)
            weight = 1.0 / max(dist, 0.5)
            phase = flux if phase_edge is not None and (i, j) == phase_edge else 0.0
            hop = -0.5j * weight * np.exp(1j * phase)
            hamiltonian[i, j] += hop
            hamiltonian[j, i] += np.conj(hop)
    return hamiltonian.tocsr()


def _evolve_cn(hamiltonian, psi0: np.ndarray) -> np.ndarray:
    n = hamiltonian.shape[0]
    aplus = (speye(n, format="csc") + 1j * hamiltonian * DT / 2).tocsc()
    aminus = speye(n, format="csr") - 1j * hamiltonian * DT / 2
    psi = psi0.copy()
    for _ in range(N_STEPS):
        psi = spsolve(aplus, aminus.dot(psi))
    return psi


def _probe_state(graph: base.GraphFamily, k0: float) -> np.ndarray:
    return base._probe_state(graph.positions.shape[0], graph.positions, graph.source, sigma=base.SOURCE_SIGMA, k0=k0)


def _shell_means(graph: base.GraphFamily, values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    max_depth = int(np.max(graph.depth[np.isfinite(graph.depth)]))
    sums = np.zeros(max_depth + 1, dtype=float)
    counts = np.zeros(max_depth + 1, dtype=float)
    for i, depth in enumerate(graph.depth):
        if not np.isfinite(depth):
            continue
        d = int(depth)
        sums[d] += float(values[i])
        counts[d] += 1.0
    mask = counts > 0
    sums[mask] /= counts[mask]
    return np.arange(max_depth + 1), sums


def _force_from_phi(graph: base.GraphFamily, psi: np.ndarray, phi: np.ndarray) -> float:
    if np.allclose(phi, 0.0):
        return 0.0
    _, rho_shell = _shell_means(graph, np.abs(psi) ** 2)
    _, phi_shell = _shell_means(graph, phi)
    max_depth = min(len(rho_shell), len(phi_shell)) - 1
    if max_depth <= 0:
        return 0.0

    grad_toward = np.zeros(max_depth + 1, dtype=float)
    for depth in range(max_depth + 1):
        if depth == 0:
            grad_toward[depth] = phi_shell[0] - phi_shell[1]
        elif depth == max_depth:
            grad_toward[depth] = phi_shell[depth - 1] - phi_shell[depth]
        else:
            grad_toward[depth] = 0.5 * (phi_shell[depth - 1] - phi_shell[depth + 1])
    return float(np.sum(rho_shell[: max_depth + 1] * grad_toward))


def _mean_depth(graph: base.GraphFamily, psi: np.ndarray) -> float:
    rho = np.abs(psi) ** 2
    mask = np.isfinite(graph.depth)
    return float(np.sum(rho[mask] * graph.depth[mask]) / max(float(np.sum(rho[mask])), 1e-30))


def _shell_bias(graph: base.GraphFamily, psi: np.ndarray) -> float:
    rho = np.abs(psi) ** 2
    source_mass = float(rho[graph.source])
    detector_mass = float(np.sum(rho[graph.detector])) if graph.detector else 0.0
    return detector_mass - source_mass


def _fit_r2(xs: tuple[float, ...], ys: list[float]) -> float:
    x_arr = np.asarray(xs, dtype=float)
    y_arr = np.asarray(ys, dtype=float)
    denom = float(np.sum((y_arr - np.mean(y_arr)) ** 2))
    if denom <= 0:
        return 1.0
    coeff = np.polyfit(x_arr, y_arr, 1)
    pred = np.polyval(coeff, x_arr)
    return 1.0 - float(np.sum((y_arr - pred) ** 2) / denom)


def _gauge_current_range(graph: base.GraphFamily, phi: np.ndarray) -> float | None:
    if not graph.has_cycle or graph.cycle_edge is None:
        return None
    currents = []
    for flux in np.linspace(0.0, 2.0 * math.pi, 7):
        h_flux = _build_hamiltonian_phi(graph, phi, flux=flux, flux_edge=graph.cycle_edge)
        _evals, evecs = np.linalg.eigh(h_flux.toarray())
        ground = evecs[:, 0]
        i, j = graph.cycle_edge
        hop = h_flux[i, j]
        currents.append(float(np.imag(np.conj(ground[i]) * hop * ground[j])))
    return float(max(currents) - min(currents))


def _measure_graph(graph: base.GraphFamily) -> BackreactionObsResult:
    kernel = _green_kernel(graph)
    rho_source = _source_density(graph, graph.source, 1.0)
    phi_source = np.asarray(kernel @ rho_source, dtype=float)
    psi0 = _probe_state(graph, k0=0.18)

    phi_zero = np.zeros(graph.positions.shape[0], dtype=float)
    psi_zero = _evolve_cn(_build_hamiltonian_phi(graph, phi_zero), psi0)
    zero_force = _force_from_phi(graph, psi_zero, phi_zero)

    psi_source = _evolve_cn(_build_hamiltonian_phi(graph, phi_source), psi0)
    source_force = _force_from_phi(graph, psi_source, phi_source)
    norm_drift = abs(np.linalg.norm(psi_source) - 1.0)

    forces_by_strength = []
    for strength in STRENGTHS:
        phi = strength * phi_source
        psi = _evolve_cn(_build_hamiltonian_phi(graph, phi), psi0)
        forces_by_strength.append(_force_from_phi(graph, psi, phi))
    source_r2 = _fit_r2(STRENGTHS, forces_by_strength)

    partner = graph.detector[0] if graph.detector else int(np.argmax(graph.depth[np.isfinite(graph.depth)]))
    rho_partner = _source_density(graph, partner, 1.0)
    phi_a = np.asarray(kernel @ rho_source, dtype=float)
    phi_b = np.asarray(kernel @ rho_partner, dtype=float)
    phi_ab = np.asarray(kernel @ (rho_source + rho_partner), dtype=float)
    two_body_resid = float(np.linalg.norm(phi_ab - phi_a - phi_b) / max(np.linalg.norm(phi_ab), 1e-30))

    force_by_k = []
    for k0 in ACHROM_K:
        psi_k = _evolve_cn(_build_hamiltonian_phi(graph, phi_source), _probe_state(graph, k0=k0))
        force_by_k.append(_force_from_phi(graph, psi_k, phi_source))
    achrom_cv = float(np.std(force_by_k) / max(abs(float(np.mean(force_by_k))), 1e-30))

    robust_toward = 0
    for k0 in ROBUST_K:
        psi_k = _evolve_cn(_build_hamiltonian_phi(graph, phi_source), _probe_state(graph, k0=k0))
        robust_toward += int(_force_from_phi(graph, psi_k, phi_source) > 0.0)

    gauge_range = _gauge_current_range(graph, phi_source)
    gauge_status = "N/A" if gauge_range is None else "PASS" if gauge_range > 1e-4 else "FAIL"

    pass_rows = [
        abs(zero_force) < 1e-10,
        norm_drift < 1e-10,
        source_force > 0.0,
        source_r2 > 0.99,
        two_body_resid < 1e-10,
        achrom_cv < 0.05,
        robust_toward == len(ROBUST_K),
        gauge_status in ("PASS", "N/A"),
    ]

    return BackreactionObsResult(
        family=graph.name,
        n=graph.positions.shape[0],
        edges=_edge_count(graph),
        has_cycle=graph.has_cycle,
        retained_passes=sum(pass_rows),
        retained_total=len(pass_rows),
        zero_force=zero_force,
        norm_drift=norm_drift,
        source_force=source_force,
        source_r2=source_r2,
        two_body_resid=two_body_resid,
        achrom_cv=achrom_cv,
        robust_toward=robust_toward,
        robust_total=len(ROBUST_K),
        gauge_status=gauge_status,
        gauge_j_range=gauge_range,
        centroid_shift=_mean_depth(graph, psi_source) - _mean_depth(graph, psi0),
        shell_bias=_shell_bias(graph, psi_source),
    )


def main() -> None:
    t0 = time.time()
    print("=" * 104)
    print("STAGGERED GRAPH OBSERVABLES: BACKREACTION STRESS")
    print("  Larger stress families; source sector = resistance-Yukawa Green map")
    print("  Rows: zero, norm, force, linearity, additivity, achromatic, robustness, gauge/current")
    print("=" * 104)
    print(
        f"dt={DT}, steps={N_STEPS}, mass={MASS}, source_sigma={SOURCE_SIGMA}, "
        f"kernel=exp(-{GREEN_MU} R_eff)/(R_eff+{GREEN_EPS})"
    )
    print()
    print(
        f"{'family':<42} {'n':>4} {'|E|':>4} {'cycle':>5} {'rows':>6} "
        f"{'F_src':>11} {'R2':>7} {'2body':>10} {'achCV':>9} "
        f"{'robust':>7} {'gauge':>13} {'dDepth':>10} {'shell':>10}"
    )
    print("-" * 104)

    results = []
    for graph in stress._stress_graphs():
        row = _measure_graph(graph)
        results.append(row)
        gauge = "N/A" if row.gauge_j_range is None else f"{row.gauge_j_range:.3e}/{row.gauge_status}"
        print(
            f"{row.family:<42} {row.n:4d} {row.edges:4d} {str(row.has_cycle):>5s} "
            f"{row.retained_passes:2d}/{row.retained_total:<3d} "
            f"{row.source_force:+11.3e} {row.source_r2:7.4f} {row.two_body_resid:10.2e} "
            f"{row.achrom_cv:9.2e} {row.robust_toward:2d}/{row.robust_total:<3d} "
            f"{gauge:>13s} {row.centroid_shift:+10.3e} {row.shell_bias:+10.3e}"
        )

    print()
    print("SUMMARY")
    for row in results:
        gauge_only_gap = row.gauge_status == "FAIL" and row.retained_passes == row.retained_total - 1
        label = "RETAINED" if row.retained_passes == row.retained_total else "PARTIAL_GAUGE" if gauge_only_gap else "PARTIAL"
        print(
            f"  {row.family:<42} {label} "
            f"({row.retained_passes}/{row.retained_total}; gauge={row.gauge_status})"
        )

    all_rows = all(row.retained_passes == row.retained_total for row in results)
    non_gauge_rows = all(
        row.retained_passes == row.retained_total
        or (row.gauge_status == "FAIL" and row.retained_passes == row.retained_total - 1)
        for row in results
    )
    cycle_rows = [row for row in results if row.has_cycle]
    print()
    print("READOUT")
    print(f"  all eight retained rows pass: {all_rows}")
    print(f"  all non-gauge source-sector rows pass: {non_gauge_rows}")
    print(f"  cycle-family gauge rows pass: {all(row.gauge_status == 'PASS' for row in cycle_rows)}")
    print(
        "  force range: "
        f"[{min(row.source_force for row in results):+.3e}, {max(row.source_force for row in results):+.3e}]"
    )
    print(
        "  secondary diagnostics remain non-gating: "
        "centroid/depth shifts and shell bias are reported but not promoted"
    )
    print(f"  runtime: {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
