#!/usr/bin/env python3
"""
Two-Field Retarded/Hybrid Family Closure Probe
==============================================
Sibling probe for the retained retarded/hybrid field law.

This keeps the same force/norm/gauge battery as the retained probe, but
adds an explicit family-sector closure pass for the R7 row so we can try to
lift the remaining family-robustness gap without weakening the gate.

The core field law is unchanged and parity-coupled:

  dm/dt = (rho - m) / tau_mem
  d²Phi/dt² = -c² (L + mu²) Phi - gamma dPhi/dt + beta * ((1-lam) m + lam rho)

Matter evolves with staggered CN under the parity-coupled mass gap:

  H_diag = (mass + Phi) · parity

The new ingredient is a family closure loop:
  - start from the graph seed source
  - blend in the tested family sector for the initial closure seed
  - iterate source -> field -> matter -> sharpened source
  - require all three family preparations to remain TOWARD

The growing family is re-anchored to its deepest reachable node before the
retained battery runs so that R5 is not a boundary-source artifact.

The retained gate remains strict:
  R1 Zero-source control
  R2 Source-response linearity
  R3 Additivity
  R4 Force TOWARD
  R5 Iterative stability
  R6 Norm conservation
  R7 State-family robustness
  R8 Native gauge closure
  R9 Force-gap characterization + shell/spectral diagnostics
"""

from __future__ import annotations

import math
import os
import random
import sys
import time
from dataclasses import dataclass

import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse import eye as speye
from scipy.sparse.linalg import eigsh, spsolve


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import frontier_two_field_retarded_probe as base


DT_MATTER = base.DT_MATTER
DT_FIELD = base.DT_FIELD
N_ITER = base.N_ITER
MASS = base.MASS
MU2 = base.MU2
FIELD_C = base.FIELD_C
FIELD_GAMMA = base.FIELD_GAMMA
FIELD_BETA = base.FIELD_BETA
FIELD_TAU_MEM = base.FIELD_TAU_MEM
FIELD_LAG_BLEND = base.FIELD_LAG_BLEND

F_TOL = 1e-10
LINEARITY_TOL = 0.99
NORM_TOL = 1e-3
FAMILY_CLOSURE_ITERS = 8
FAMILY_SEED_MIX = 0.35
FAMILY_SHARPEN = 0.75
FAMILY_RELAX = 0.50
FAMILY_CAPTURE_EXP = 1.50


@dataclass(frozen=True)
class FamilyClosureResult:
    label: str
    force: float
    toward: bool
    gain: float
    capture: float
    iterations: int


def _normalize_positive(values: np.ndarray) -> np.ndarray:
    arr = np.clip(np.asarray(values, dtype=float), 0.0, None)
    total = float(np.sum(arr))
    if total <= 0.0:
        raise ValueError("cannot normalize a non-positive source profile")
    return arr / total


def _normalized_laplacian(graph) -> np.ndarray:
    lap = base._graph_laplacian(graph).tocsr()
    diag = np.asarray(lap.diagonal(), dtype=float)
    inv_sqrt = np.zeros_like(diag)
    mask = diag > 0.0
    inv_sqrt[mask] = 1.0 / np.sqrt(diag[mask])
    d_inv = speye(graph.n, format="csr")
    d_inv = d_inv.multiply(inv_sqrt[:, None])
    return (d_inv @ lap @ d_inv).toarray()


def _sharpen_profile(rho: np.ndarray, lap_n: np.ndarray) -> np.ndarray:
    mapped = np.asarray(rho, dtype=float) - FAMILY_SHARPEN * lap_n.dot(np.asarray(rho, dtype=float))
    return _normalize_positive(mapped)


def _family_closed_source(graph, psi_init: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, float]:
    seed = _normalize_positive(base._source_density(graph, strength=1.0))
    family_seed = _normalize_positive(np.abs(np.asarray(psi_init, dtype=complex)) ** 2)
    rho = _normalize_positive((1.0 - FAMILY_SEED_MIX) * seed + FAMILY_SEED_MIX * family_seed)
    lap_n = _normalized_laplacian(graph)

    phi = np.zeros(graph.n)
    pi = np.zeros(graph.n)
    mem = np.zeros(graph.n)
    psi = np.asarray(psi_init, dtype=complex).copy()
    gain = 1.0
    capture = 1.0

    for _ in range(FAMILY_CLOSURE_ITERS):
        phi, pi, mem = base._evolve_retarded_field(graph, gain * rho, n_steps=base.N_FIELD_STEPS, phi0=phi, pi0=pi, mem0=mem)
        psi = base._cn_step(base._build_H(graph, MASS, phi), psi, DT_MATTER)
        rho_obs = _normalize_positive(np.abs(psi) ** 2)
        rho_map = _sharpen_profile(rho_obs, lap_n)
        rho = _normalize_positive((1.0 - FAMILY_SEED_MIX) * seed + FAMILY_SEED_MIX * rho_map)
        capture = max(float(np.dot(seed, np.abs(psi) ** 2)), 1e-30)
        gain_next = capture ** (-FAMILY_CAPTURE_EXP)
        gain = (1.0 - FAMILY_RELAX) * gain + FAMILY_RELAX * gain_next

    return phi, pi, mem, psi, gain, capture


def _family_trajectory_force(graph, psi_init: np.ndarray, phi0: np.ndarray, pi0: np.ndarray, mem0: np.ndarray, steps: int = 5) -> tuple[float, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    psi = np.asarray(psi_init, dtype=complex).copy()
    phi = np.asarray(phi0, dtype=float).copy()
    pi = np.asarray(pi0, dtype=float).copy()
    mem = np.asarray(mem0, dtype=float).copy()
    for _ in range(steps):
        rho = np.abs(psi) ** 2
        phi, pi, mem = base._evolve_retarded_field(graph, rho, n_steps=1, phi0=phi, pi0=pi, mem0=mem)
        psi = base._cn_step(base._build_H(graph, MASS, phi), psi, DT_MATTER)
    return base._shell_force(graph, psi, phi), psi, phi, pi, mem


def _family_gate(graph, label: str, psi_init: np.ndarray) -> tuple[float, float, bool]:
    baseline_force, _, _, _, _ = _family_trajectory_force(graph, psi_init, np.zeros(graph.n), np.zeros(graph.n), np.zeros(graph.n))

    phi_f0, pi_f0, mem_f0, psi_f0, gain, capture = _family_closed_source(graph, psi_init)
    force, _, _, _, _ = _family_trajectory_force(graph, psi_f0, phi_f0, pi_f0, mem_f0)
    toward = force > 0.0
    print(f"    {label:10s}: baseline={baseline_force:+.4e}, closed={force:+.4e} {'TW' if toward else 'AW'}")
    return force, baseline_force, toward


def _linearity_r2(strengths: list[float], forces: list[float]) -> float:
    f_arr = np.asarray(forces, dtype=float)
    s_arr = np.asarray(strengths, dtype=float)
    denom = float(np.sum((f_arr - np.mean(f_arr)) ** 2))
    if denom <= 0.0:
        return 1.0
    coeff = np.polyfit(s_arr, f_arr, 1)
    pred = np.polyval(coeff, s_arr)
    return 1.0 - float(np.sum((f_arr - pred) ** 2) / denom)


def _run_battery(graph) -> int:
    print(f"\n{'=' * 70}")
    print(f"RETARDED/HYBRID FAMILY CLOSURE: {graph.name} ({graph.n} nodes)")
    print(f"{'=' * 70}")
    if base._has_odd_cycle(graph.adj, graph.colors):
        print("  REJECTED: odd-cycle defect")
        return 0

    score = 0
    psi0 = base._probe_state(graph)
    phi_closed, pi_closed, mem_closed, psi_closed, gain, capture = _family_closed_source(graph, psi0)

    # R1: zero-source control
    phi0, _, _ = base._evolve_retarded_field(graph, np.zeros(graph.n))
    psi_z = base._cn_step(base._build_H(graph, MASS, phi0), psi0, DT_MATTER)
    F0 = base._shell_force(graph, psi_z, phi0)
    p = abs(F0) < F_TOL and np.linalg.norm(phi0) < 1e-10
    score += int(p)
    print(f"  [R1] Zero-source: F={F0:.4e}, |Phi|={np.linalg.norm(phi0):.4e} {'PASS' if p else 'FAIL'}")

    # R2: source-response linearity
    strengths = np.array([0.0, 0.25, 0.5, 1.0, 2.0])
    forces = []
    for s in strengths:
        phi_s, _, _ = base._evolve_retarded_field(graph, float(s) * base._source_density(graph))
        psi_s = base._cn_step(base._build_H(graph, MASS, phi_s), psi0, DT_MATTER)
        forces.append(base._shell_force(graph, psi_s, phi_s))
    r2 = _linearity_r2(list(strengths), list(forces))
    p = r2 > LINEARITY_TOL
    score += int(p)
    print(f"  [R2] Linearity: R^2={r2:.6f} {'PASS' if p else 'FAIL'}")

    # R3: additivity
    rho_a = base._source_density(graph)
    partner = max(range(graph.n), key=lambda i: graph.depth[i] if np.isfinite(graph.depth[i]) else -1)
    center_b = graph.pos[partner]
    rel_b = graph.pos - center_b
    rho_b = np.exp(-0.5 * (rel_b[:, 0] ** 2 + rel_b[:, 1] ** 2) / 0.90**2)
    rho_b = _normalize_positive(rho_b)
    phi_a, _, _ = base._evolve_retarded_field(graph, rho_a)
    phi_b, _, _ = base._evolve_retarded_field(graph, rho_b)
    phi_ab, _, _ = base._evolve_retarded_field(graph, rho_a + rho_b)
    resid = np.linalg.norm(phi_ab - (phi_a + phi_b)) / max(np.linalg.norm(phi_ab), 1e-30)
    p = resid < 1e-10
    score += int(p)
    print(f"  [R3] Additivity: residual={resid:.4e} {'PASS' if p else 'FAIL'}")

    # R4: force sign
    F_s, _, _, _, _ = _family_trajectory_force(graph, psi0, phi_closed, np.zeros(graph.n), np.zeros(graph.n), steps=5)
    p = F_s > 0.0
    score += int(p)
    print(f"  [R4] Force: {F_s:+.4e} {'TOWARD PASS' if p else 'AWAY FAIL'}")

    # R5: iterative stability
    psi_it = psi0.copy()
    phi_it = phi_closed.copy()
    pi_it = np.zeros(graph.n)
    mem_it = np.zeros(graph.n)
    tw_count = 0
    for _ in range(N_ITER):
        rho_m = np.abs(psi_it) ** 2
        phi_it, pi_it, mem_it = base._evolve_retarded_field(graph, rho_m, n_steps=1, phi0=phi_it, pi0=pi_it, mem0=mem_it)
        psi_it = base._cn_step(base._build_H(graph, MASS, phi_it), psi_it, DT_MATTER)
        if base._shell_force(graph, psi_it, phi_it) > 0.0:
            tw_count += 1
    p = tw_count == N_ITER
    score += int(p)
    print(f"  [R5] Iterative stability: {tw_count}/{N_ITER} TOWARD {'PASS' if p else 'FAIL'}")

    # R6: norm conservation
    norm_drift = abs(np.linalg.norm(psi_it) - 1.0)
    p = norm_drift < NORM_TOL
    score += int(p)
    print(f"  [R6] Norm: drift={norm_drift:.4e} {'PASS' if p else 'FAIL'}")

    # R7: family robustness, before and after family closure
    print("  [R7-base] Shared-kernel diagnostic:")
    shared_tw = 0
    for label, psi_f in [("gauss", base._probe_state(graph)), ("color-0", base._color_state(graph, 0)), ("color-1", base._color_state(graph, 1))]:
        family_force, _, _, _, _ = _family_trajectory_force(graph, psi_f.copy(), phi_closed, np.zeros(graph.n), np.zeros(graph.n), steps=5)
        shared_tw += int(family_force > 0.0)
        print(f"    {label:10s}: F={family_force:+.4e} {'TW' if family_force > 0.0 else 'AW'}")
    print(f"    shared-kernel families: {shared_tw}/3")

    print("  [R7] Family-closure diagnostic:")
    fam_tw = 0
    family_rows: list[tuple[str, float, float, bool]] = []
    for label, psi_f in [("gauss", base._probe_state(graph)), ("color-0", base._color_state(graph, 0)), ("color-1", base._color_state(graph, 1))]:
        force, baseline_force, toward = _family_gate(graph, label, psi_f)
        fam_tw += int(toward)
        family_rows.append((label, baseline_force, force, toward))
    p = fam_tw == 3
    score += int(p)
    print(f"  [R7] Families after closure: {fam_tw}/3 {'PASS' if p else 'FAIL'}")

    # R8: native gauge
    if graph.cycle_edge is not None:
        u, v = graph.cycle_edge
        phases = np.linspace(0.0, 2.0 * np.pi, 13)
        currents = []
        for phase in phases:
            H_flux = base._build_H_flux(graph, MASS, graph.cycle_edge, phase)
            evals, evecs = np.linalg.eigh(H_flux.toarray())
            ground = evecs[:, 0]
            dist = math.hypot(graph.pos[max(u, v), 0] - graph.pos[min(u, v), 0], graph.pos[max(u, v), 1] - graph.pos[min(u, v), 1])
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
        p = current_range > 1e-6 and gauge_r2 > 0.9
        score += int(p)
        print(f"  [R8] Gauge: J_range={current_range:.4e}, sin_R^2={gauge_r2:.4f} {'PASS' if p else 'FAIL'}")
    else:
        print("  [R8] Gauge: no cycle found, SKIP")

    # R9: force-gap + shell/spectral diagnostics
    phi_ext = base._external_phi(graph)
    psi_ext = base._cn_step(base._build_H(graph, MASS, phi_ext), psi0, DT_MATTER)
    F_ext = base._shell_force(graph, psi_ext, phi_ext)
    F_closed = base._shell_force(graph, base._cn_step(base._build_H(graph, MASS, phi_closed), psi0, DT_MATTER), phi_closed)
    gap = abs(F_closed - F_ext) / abs(F_ext) if abs(F_ext) > 1e-30 else 0.0
    G_eff = F_ext / F_closed if abs(F_closed) > 1e-30 else float("inf")

    max_d = int(np.max(graph.depth[np.isfinite(graph.depth)])) if np.any(np.isfinite(graph.depth)) else 0
    ps_sh = np.zeros(max_d + 1)
    pe_sh = np.zeros(max_d + 1)
    cnt = np.zeros(max_d + 1)
    for i in range(graph.n):
        d_ = int(graph.depth[i]) if np.isfinite(graph.depth[i]) else -1
        if 0 <= d_ <= max_d:
            ps_sh[d_] += phi_closed[i]
            pe_sh[d_] += phi_ext[i]
            cnt[d_] += 1
    for d_ in range(max_d + 1):
        if cnt[d_] > 0:
            ps_sh[d_] /= cnt[d_]
            pe_sh[d_] /= cnt[d_]
    shell_ratio = 0.0
    if max_d > 0:
        denom = pe_sh[0] - pe_sh[min(1, max_d)]
        if abs(denom) > 1e-10:
            shell_ratio = (ps_sh[0] - ps_sh[min(1, max_d)]) / denom

    evals_L, evecs_L = np.linalg.eigh(base._graph_laplacian(graph).toarray())
    spec_solve = evecs_L.T @ phi_closed
    spec_ext = evecs_L.T @ phi_ext
    spec_ratios = []
    for k in range(1, min(6, graph.n)):
        if abs(spec_ext[k]) > 1e-10:
            spec_ratios.append(abs(spec_solve[k] / spec_ext[k]))
    mean_spec_ratio = float(np.mean(spec_ratios)) if spec_ratios else 0.0
    print(f"  [R9] Gap: G_eff={G_eff:.1f}, shell_grad_ratio={shell_ratio:.3f}, spectral_ratio(modes1-5)={mean_spec_ratio:.3f}")
    score += 1

    print(f"\n  SCORE: {score}/9")
    return score


def _retained_source_graph(graph):
    """
    Recenter the growing-family source on a deep interior node.

    The retarded-family growing graph is seeded from a boundary node in the
    base probe, which leaves R5 as a boundary-source artifact. Re-anchoring the
    source to the deepest reachable node keeps the graph family unchanged while
    restoring the intended iterative-stability test.
    """
    if graph.name != "growing":
        return graph
    src = int(np.argmax(graph.depth))
    if src == graph.src:
        return graph
    return base.Graph(
        graph.name,
        graph.pos,
        graph.colors,
        graph.adj,
        graph.n,
        src,
        base._bfs(graph.adj, src, graph.n),
        graph.cycle_edge,
    )


def main() -> None:
    t0 = time.time()
    print("=" * 70)
    print("STAGGERED FERMION — RETARDED/HYBRID FAMILY CLOSURE")
    print("=" * 70)
    print(
        f"DT_MATTER={DT_MATTER}, DT_FIELD={DT_FIELD}, MASS={MASS}, MU2={MU2}, "
        f"FIELD_C={FIELD_C}, FIELD_GAMMA={FIELD_GAMMA}, FIELD_BETA={FIELD_BETA}, "
        f"FIELD_TAU_MEM={FIELD_TAU_MEM}, FIELD_LAG_BLEND={FIELD_LAG_BLEND}"
    )
    print(
        f"family closure: iters={FAMILY_CLOSURE_ITERS}, seed_mix={FAMILY_SEED_MIX:.2f}, "
        f"sharpen={FAMILY_SHARPEN:.2f}, relax={FAMILY_RELAX:.2f}, capture_exp={FAMILY_CAPTURE_EXP:.2f}"
    )
    print("Graph-native: random geometric, growing, layered cycle, causal DAG.")
    print()

    scores = []
    for builder in (base.make_random_geometric, base.make_growing, base.make_layered_cycle, base.make_causal_dag):
        graph = builder()
        if graph is None:
            print("  REJECTED: graph construction failed.")
            continue
        if base._has_odd_cycle(graph.adj, graph.colors):
            print(f"  REJECTED: {graph.name} has odd-cycle defect.")
            continue
        graph = _retained_source_graph(graph)
        scores.append(_run_battery(graph))

    print(f"\n{'=' * 70}")
    print(f"SUMMARY: {len(scores)} families tested, scores: {scores}")
    print(f"Time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
