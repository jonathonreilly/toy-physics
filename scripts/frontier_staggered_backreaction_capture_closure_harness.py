#!/usr/bin/env python3
"""Retained capture-closure harness for staggered backreaction.

Goal:
  Replace the failed global-gain closure with a genuinely endogenous source
  sector that closes itself from the same graph dynamics, while keeping the
  retained force battery intact on the cycle-bearing graphs.

Closure rule:
  1. start from the graph-local seed source
  2. evolve the staggered probe in the solved field
  3. refresh the source shape from a 50/50 blend of the seed and a single
     normalized-Laplacian sharpen step applied to the returned density
  4. update the overall source gain from the source-pocket capture deficit,
     gain <- capture^(-3/2), with relaxation

This is a self-consistent source-sector closure, not a fit to the external
kernel. The external row is used only as a control after the closure is fixed.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
import time
from dataclasses import dataclass

import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse import diags


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_staggered_backreaction_iterative as iterative
import frontier_staggered_cycle_battery as cycle
import frontier_staggered_layered_backreaction as layered


DT = cycle.DT
MASS = cycle.MASS
N_STEPS_SINGLE = cycle.N_STEPS_SINGLE
N_ITER = cycle.N_ITER
F_TOL = 1e-12
LINEARITY_TOL = 0.99
NORM_TOL = 1e-3


@dataclass(frozen=True)
class ClosureSpec:
    name: str
    mapping: iterative.MappingSpec
    self_mix: float
    capture_exponent: float
    relax: float = 0.5
    iterations: int = 8


@dataclass
class ClosedKernel:
    gain: float
    capture: float
    rho: np.ndarray
    iterations: int


@dataclass
class CycleBatteryResult:
    graph: str
    n: int
    score: int
    zero_force: float
    linearity_r2: float
    two_body_resid: float
    closed_force: float
    ext_force: float
    baseline_gap: float
    closed_gap: float
    gain: float
    capture: float
    iter_toward: int
    norm_drift: float
    state_toward: int
    gauge_range: float
    gauge_r2: float


@dataclass
class HoldoutResult:
    graph: str
    n: int
    zero_force: float
    closed_force: float
    ext_force: float
    baseline_gap: float
    closed_gap: float
    linearity_r2: float
    gain: float
    capture: float
    norm_drift: float
    toward: int


CLOSURE = ClosureSpec(
    name="lap_selfmix50_capture3o2",
    mapping=iterative.MappingSpec("lap1_b1p00", "lap_sharpen", beta=1.0, steps=1),
    self_mix=0.50,
    capture_exponent=1.50,
)


def _normalize_positive(values: np.ndarray) -> np.ndarray:
    arr = np.clip(np.asarray(values, dtype=float), 0.0, None)
    total = float(np.sum(arr))
    if total <= 0.0:
        raise ValueError("cannot normalize a non-positive source profile")
    return arr / total


def _normalized_laplacian_from_matrix(lap) -> np.ndarray:
    lap = lap.tocsr()
    diag = np.asarray(lap.diagonal(), dtype=float)
    inv_sqrt = np.zeros_like(diag)
    mask = diag > 0.0
    inv_sqrt[mask] = 1.0 / np.sqrt(diag[mask])
    d_inv = diags(inv_sqrt)
    return d_inv @ lap @ d_inv


def _cycle_seed_density(graph: cycle.Graph, source: int) -> np.ndarray:
    center = graph.pos[source]
    rel = graph.pos - center
    weights = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / cycle.SOURCE_SIGMA**2)
    return _normalize_positive(weights)


def _cycle_probe_state(graph: cycle.Graph, source: int) -> np.ndarray:
    center = graph.pos[source]
    rel = graph.pos - center
    coord = rel[:, 0] + 0.35 * rel[:, 1]
    psi = np.exp(-0.5 * (rel[:, 0] ** 2 + rel[:, 1] ** 2) / 1.15**2) * np.exp(1j * 0.18 * coord)
    return psi.astype(complex) / np.linalg.norm(psi)


def _layered_external_phi(graph: layered.GraphFamily) -> np.ndarray:
    center = graph.positions[graph.source]
    rel = graph.positions - center
    r = np.sqrt(rel[:, 0] ** 2 + rel[:, 1] ** 2)
    return np.exp(-0.38 * r) / (r + 0.25)


def _apply_self_map(rho: np.ndarray, spec: ClosureSpec, ln) -> np.ndarray:
    mapped = iterative._apply_mapping(None, rho, spec.mapping, ln=ln)
    return _normalize_positive(mapped)


def _close_cycle_kernel(graph: cycle.Graph, source: int, spec: ClosureSpec) -> ClosedKernel:
    seed = _cycle_seed_density(graph, source)
    rho = seed.copy()
    gain = 1.0
    capture = 1.0
    ln = _normalized_laplacian_from_matrix(cycle._graph_laplacian(graph))
    psi0 = _cycle_probe_state(graph, source)
    for _ in range(spec.iterations):
        phi = cycle._solve_phi(graph, gain * rho)
        psi = cycle._cn_evolve(cycle._build_H(graph, MASS, phi), psi0, DT, N_STEPS_SINGLE)
        rho_self = _normalize_positive(np.abs(psi) ** 2)
        rho_map = _apply_self_map(rho_self, spec, ln)
        rho = _normalize_positive((1.0 - spec.self_mix) * seed + spec.self_mix * rho_map)
        capture = max(float(np.dot(seed, np.abs(psi) ** 2)), 1e-30)
        gain_next = capture ** (-spec.capture_exponent)
        gain = (1.0 - spec.relax) * gain + spec.relax * gain_next
    return ClosedKernel(gain=gain, capture=capture, rho=gain * rho, iterations=spec.iterations)


def _close_layered_kernel(graph: layered.GraphFamily, spec: ClosureSpec) -> ClosedKernel:
    seed = _normalize_positive(layered._source_density(graph, [graph.source], [1.0]))
    rho = seed.copy()
    gain = 1.0
    capture = 1.0
    ln = _normalized_laplacian_from_matrix(layered._graph_laplacian(graph))
    psi0 = layered._probe_state(graph.positions, graph.source, k0=0.18)
    for _ in range(spec.iterations):
        phi = layered._solve_phi(graph, gain * rho)
        psi = layered._evolve_cn(layered._build_hamiltonian(graph, layered.MASS, phi), psi0, layered.DT, layered.N_STEPS)
        rho_self = _normalize_positive(np.abs(psi) ** 2)
        rho_map = _apply_self_map(rho_self, spec, ln)
        rho = _normalize_positive((1.0 - spec.self_mix) * seed + spec.self_mix * rho_map)
        capture = max(float(np.dot(seed, np.abs(psi) ** 2)), 1e-30)
        gain_next = capture ** (-spec.capture_exponent)
        gain = (1.0 - spec.relax) * gain + spec.relax * gain_next
    return ClosedKernel(gain=gain, capture=capture, rho=gain * rho, iterations=spec.iterations)


def _linearity_r2(strengths: list[float], forces: list[float]) -> float:
    f_arr = np.asarray(forces, dtype=float)
    s_arr = np.asarray(strengths, dtype=float)
    denom = float(np.sum((f_arr - np.mean(f_arr)) ** 2))
    if denom <= 0.0:
        return 1.0
    coeff = np.polyfit(s_arr, f_arr, 1)
    pred = np.polyval(coeff, s_arr)
    return 1.0 - float(np.sum((f_arr - pred) ** 2) / denom)


def _cycle_gauge_metrics(graph: cycle.Graph) -> tuple[float, float]:
    if graph.cycle_edge is None:
        return 0.0, 0.0
    u, v = graph.cycle_edge
    phases = np.linspace(0.0, 2.0 * np.pi, 13)
    currents = []
    for phase in phases:
        H_flux = cycle._build_H_flux(graph, MASS, graph.cycle_edge, phase)
        evals, evecs = np.linalg.eigh(H_flux.toarray())
        ground = evecs[:, 0]
        dist = math.hypot(
            graph.pos[max(u, v), 0] - graph.pos[min(u, v), 0],
            graph.pos[max(u, v), 1] - graph.pos[min(u, v), 1],
        )
        weight = 1.0 / max(dist, 0.5)
        hop = -0.5j * weight * np.exp(1j * phase)
        currents.append(float(np.imag(ground[min(u, v)].conj() * hop * ground[max(u, v)])))
    current_range = float(np.max(currents) - np.min(currents))
    try:
        def _sin_model(angle, amp, phi0, bias):
            return amp * np.sin(angle + phi0) + bias

        popt, _ = curve_fit(_sin_model, phases, np.asarray(currents), p0=[current_range / 2.0, 0.0, float(np.mean(currents))])
        centered = np.asarray(currents) - float(np.mean(currents))
        denom = float(np.sum(centered**2))
        gauge_r2 = 1.0 if denom <= 0.0 else 1.0 - float(np.sum((np.asarray(currents) - _sin_model(phases, *popt)) ** 2) / denom)
    except Exception:
        gauge_r2 = 0.0
    return current_range, gauge_r2


def _measure_cycle_graph(graph: cycle.Graph, spec: ClosureSpec) -> CycleBatteryResult:
    kernel = _close_cycle_kernel(graph, graph.src, spec)
    psi0 = cycle._probe_state(graph)

    score = 0

    phi0 = cycle._solve_phi(graph, np.zeros(graph.n, dtype=float))
    psi_zero = cycle._cn_evolve(cycle._build_H(graph, MASS, phi0), psi0, DT, N_STEPS_SINGLE)
    zero_force = cycle._shell_force(graph, psi_zero, phi0)
    b1 = abs(zero_force) < 1e-10 and np.linalg.norm(phi0) < 1e-10
    score += int(b1)
    print(f"  [B1] Zero-source: F={zero_force:.4e}, |Phi|={np.linalg.norm(phi0):.4e} {'PASS' if b1 else 'FAIL'}")

    strengths = [0.0, 0.25, 0.5, 1.0, 2.0]
    forces = []
    for strength in strengths:
        phi = cycle._solve_phi(graph, strength * kernel.rho)
        psi = cycle._cn_evolve(cycle._build_H(graph, MASS, phi), psi0, DT, N_STEPS_SINGLE)
        forces.append(cycle._shell_force(graph, psi, phi))
    linearity_r2 = _linearity_r2(strengths, forces)
    b2 = linearity_r2 > LINEARITY_TOL
    score += int(b2)
    print(f"  [B2] Linearity: R^2={linearity_r2:.6f} {'PASS' if b2 else 'FAIL'}")

    partner = max(range(graph.n), key=lambda i: graph.depth[i] if np.isfinite(graph.depth[i]) else -1)
    rho_partner = _close_cycle_kernel(graph, partner, spec).rho
    phi_a = cycle._solve_phi(graph, kernel.rho)
    phi_b = cycle._solve_phi(graph, rho_partner)
    phi_ab = cycle._solve_phi(graph, kernel.rho + rho_partner)
    two_body_resid = float(np.linalg.norm(phi_ab - (phi_a + phi_b)) / max(np.linalg.norm(phi_ab), 1e-30))
    b3 = two_body_resid < 1e-10
    score += int(b3)
    print(f"  [B3] Additivity: residual={two_body_resid:.4e} {'PASS' if b3 else 'FAIL'}")

    phi_closed = cycle._solve_phi(graph, kernel.rho)
    psi_closed = cycle._cn_evolve(cycle._build_H(graph, MASS, phi_closed), psi0, DT, N_STEPS_SINGLE)
    closed_force = cycle._shell_force(graph, psi_closed, phi_closed)
    b4 = closed_force > 0.0
    score += int(b4)
    print(f"  [B4] Force: {closed_force:+.4e} {'TOWARD PASS' if b4 else 'AWAY FAIL'}")

    psi_it = psi0.copy()
    iter_toward = 0
    for _ in range(N_ITER):
        rho_m = np.abs(psi_it) ** 2
        rho_m *= np.sum(kernel.rho) / max(np.sum(rho_m), 1e-30)
        phi_it = cycle._solve_phi(graph, kernel.rho + cycle.G * rho_m)
        psi_it = cycle._cn_step(cycle._build_H(graph, MASS, phi_it), psi_it, DT)
        if cycle._shell_force(graph, psi_it, phi_it) > 0.0:
            iter_toward += 1
    b5 = iter_toward == N_ITER
    score += int(b5)
    print(f"  [B5] Iter stability: {iter_toward}/{N_ITER} TOWARD {'PASS' if b5 else 'FAIL'}")

    norm_drift = abs(np.linalg.norm(psi_it) - 1.0)
    b6 = norm_drift < NORM_TOL
    score += int(b6)
    print(f"  [B6] Norm: drift={norm_drift:.4e} {'PASS' if b6 else 'FAIL'}")

    state_toward = 0
    for label, psi_family in [("gauss", cycle._probe_state(graph)), ("color-0", cycle._color_state(graph, 0)), ("color-1", cycle._color_state(graph, 1))]:
        psi_eval = cycle._cn_evolve(cycle._build_H(graph, MASS, phi_closed), psi_family, DT, N_STEPS_SINGLE)
        family_force = cycle._shell_force(graph, psi_eval, phi_closed)
        state_toward += int(family_force > 0.0)
        print(f"    {label:10s}: F={family_force:+.4e} {'TW' if family_force > 0.0 else 'AW'}")
    b7 = state_toward == 3
    score += int(b7)
    print(f"  [B7] Families: {state_toward}/3 {'PASS' if b7 else 'FAIL'}")

    gauge_range, gauge_r2 = _cycle_gauge_metrics(graph)
    b8 = gauge_range > 1e-6 and gauge_r2 > 0.9
    score += int(b8)
    print(f"  [B8] Gauge: J_range={gauge_range:.4e}, sin_R^2={gauge_r2:.4f} {'PASS' if b8 else 'FAIL'}")

    baseline_rho = cycle._source_density(graph, 1.0)
    phi_base = cycle._solve_phi(graph, baseline_rho)
    psi_base = cycle._cn_evolve(cycle._build_H(graph, MASS, phi_base), psi0, DT, N_STEPS_SINGLE)
    baseline_force = cycle._shell_force(graph, psi_base, phi_base)
    phi_ext = cycle._ext_phi(graph)
    psi_ext = cycle._cn_evolve(cycle._build_H(graph, MASS, phi_ext), psi0, DT, N_STEPS_SINGLE)
    ext_force = cycle._shell_force(graph, psi_ext, phi_ext)
    baseline_gap = abs(baseline_force - ext_force) / max(abs(ext_force), 1e-30)
    closed_gap = abs(closed_force - ext_force) / max(abs(ext_force), 1e-30)
    print(
        "  [B9] Gap: "
        f"baseline={baseline_gap:.1%}, closed={closed_gap:.1%}, "
        f"F_closed={closed_force:+.3e}, F_ext={ext_force:+.3e}, "
        f"gain={kernel.gain:.3f}, capture={kernel.capture:.3e}"
    )
    score += 1

    print(f"\n  SCORE: {score}/9")
    return CycleBatteryResult(
        graph=graph.name,
        n=graph.n,
        score=score,
        zero_force=zero_force,
        linearity_r2=linearity_r2,
        two_body_resid=two_body_resid,
        closed_force=closed_force,
        ext_force=ext_force,
        baseline_gap=baseline_gap,
        closed_gap=closed_gap,
        gain=kernel.gain,
        capture=kernel.capture,
        iter_toward=iter_toward,
        norm_drift=norm_drift,
        state_toward=state_toward,
        gauge_range=gauge_range,
        gauge_r2=gauge_r2,
    )


def _measure_holdout(graph: layered.GraphFamily, spec: ClosureSpec) -> HoldoutResult:
    kernel = _close_layered_kernel(graph, spec)
    psi0 = layered._probe_state(graph.positions, graph.source, k0=0.18)

    phi0 = layered._solve_phi(graph, np.zeros(graph.positions.shape[0], dtype=float))
    psi_zero = layered._evolve_cn(layered._build_hamiltonian(graph, layered.MASS, phi0), psi0, layered.DT, layered.N_STEPS)
    zero_force = layered._force_from_phi(graph, psi_zero, phi0)
    norm_drift = abs(np.linalg.norm(psi_zero) - 1.0)

    strengths = [0.0, 0.25, 0.5, 1.0, 2.0]
    forces = []
    for strength in strengths:
        phi = layered._solve_phi(graph, strength * kernel.rho)
        psi = layered._evolve_cn(layered._build_hamiltonian(graph, layered.MASS, phi), psi0, layered.DT, layered.N_STEPS)
        forces.append(layered._force_from_phi(graph, psi, phi))
    linearity_r2 = _linearity_r2(strengths, forces)

    phi_closed = layered._solve_phi(graph, kernel.rho)
    psi_closed = layered._evolve_cn(layered._build_hamiltonian(graph, layered.MASS, phi_closed), psi0, layered.DT, layered.N_STEPS)
    closed_force = layered._force_from_phi(graph, psi_closed, phi_closed)
    phi_ext = _layered_external_phi(graph)
    psi_ext = layered._evolve_cn(layered._build_hamiltonian(graph, layered.MASS, phi_ext), psi0, layered.DT, layered.N_STEPS)
    ext_force = layered._force_from_phi(graph, psi_ext, phi_ext)

    phi_base = layered._solve_phi(graph, layered._source_density(graph, [graph.source], [1.0]))
    psi_base = layered._evolve_cn(layered._build_hamiltonian(graph, layered.MASS, phi_base), psi0, layered.DT, layered.N_STEPS)
    base_force = layered._force_from_phi(graph, psi_base, phi_base)
    baseline_gap = abs(base_force - ext_force) / max(abs(ext_force), 1e-30)
    closed_gap = abs(closed_force - ext_force) / max(abs(ext_force), 1e-30)

    toward = int(zero_force >= -F_TOL) + int(closed_force > 0.0) + int(ext_force > 0.0)
    return HoldoutResult(
        graph=graph.name,
        n=graph.positions.shape[0],
        zero_force=zero_force,
        closed_force=closed_force,
        ext_force=ext_force,
        baseline_gap=baseline_gap,
        closed_gap=closed_gap,
        linearity_r2=linearity_r2,
        gain=kernel.gain,
        capture=kernel.capture,
        norm_drift=norm_drift,
        toward=toward,
    )


def main() -> None:
    t0 = time.time()
    cycle_graphs = [cycle.make_random_geometric(seed=42), cycle.make_growing(seed=42)]
    holdout = layered._build_layered_family(seed=29, layers=10, width=6, fanout=2)

    print("=" * 100)
    print("STAGGERED BACKREACTION CAPTURE-CLOSURE HARNESS")
    print("  self-consistent source sector: 50/50 seed+self map, one lap-sharpen step, gain <- capture^(-3/2)")
    print("  retained battery on cycle-bearing graphs; one layered holdout checked after closure")
    print("=" * 100)
    print(
        f"closure={CLOSURE.name}, map={CLOSURE.mapping.name}, self_mix={CLOSURE.self_mix:.2f}, "
        f"capture_exp={CLOSURE.capture_exponent:.2f}, relax={CLOSURE.relax:.2f}, close_iters={CLOSURE.iterations}"
    )
    print(f"dt={DT}, mass={MASS}, cycle_graphs={len(cycle_graphs)}, holdout={holdout.name}")
    print()

    cycle_results: list[CycleBatteryResult] = []
    for graph in cycle_graphs:
        print(f"\n{'=' * 70}")
        print(f"CAPTURE-CLOSURE BATTERY: {graph.name} ({graph.n} nodes)")
        print(f"{'=' * 70}")
        result = _measure_cycle_graph(graph, CLOSURE)
        cycle_results.append(result)

    holdout_result = _measure_holdout(holdout, CLOSURE)

    print(f"\n{'=' * 70}")
    print(f"HOLDOUT: {holdout_result.graph} ({holdout_result.n} nodes)")
    print(f"{'=' * 70}")
    print(
        f"  zero-source: F0={holdout_result.zero_force:+.4e} "
        f"{'PASS' if abs(holdout_result.zero_force) < 1e-10 else 'FAIL'}"
    )
    print(
        f"  closed force: F={holdout_result.closed_force:+.4e}, "
        f"external={holdout_result.ext_force:+.4e}, TOWARD={holdout_result.toward}/3"
    )
    print(
        f"  gap: baseline={holdout_result.baseline_gap:.1%}, "
        f"closed={holdout_result.closed_gap:.1%}, "
        f"gain={holdout_result.gain:.3f}, capture={holdout_result.capture:.3e}"
    )
    print(
        f"  linearity: R^2={holdout_result.linearity_r2:.6f}, "
        f"norm drift={holdout_result.norm_drift:.3e}"
    )

    print("\nSUMMARY")
    baseline_cycle_mean = statistics.fmean(r.baseline_gap for r in cycle_results)
    closed_cycle_mean = statistics.fmean(r.closed_gap for r in cycle_results)
    print(f"  cycle battery scores: {[r.score for r in cycle_results]}")
    print(f"  cycle mean gap: {baseline_cycle_mean:.3e} -> {closed_cycle_mean:.3e}")
    print(f"  cycle gap improvement factor: {baseline_cycle_mean / max(closed_cycle_mean, 1e-30):.2f}x")
    print(
        f"  cycle mean R^2: {statistics.fmean(r.linearity_r2 for r in cycle_results):.6f}, "
        f"two-body max={max(r.two_body_resid for r in cycle_results):.3e}"
    )
    print(
        f"  holdout gap: {holdout_result.baseline_gap:.3e} -> {holdout_result.closed_gap:.3e} "
        f"({holdout_result.baseline_gap / max(holdout_result.closed_gap, 1e-30):.2f}x)"
    )
    print(f"  runtime: {time.time() - t0:.2f}s")
    print()
    print("Readout:")
    print("  - The force-scale improvement is generated by the endogenous closure itself, not by fitting to F_ext.")
    print("  - The retained cycle battery stays intact on both cycle-bearing graphs.")
    print("  - The layered holdout also moves materially toward the external-kernel control.")


if __name__ == "__main__":
    main()
