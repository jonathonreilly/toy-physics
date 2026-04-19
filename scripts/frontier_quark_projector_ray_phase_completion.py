#!/usr/bin/env python3
"""
Bounded reduced quark closure on a fixed CKM projector ray.

Status:
  bounded reduced full-closure extension on top of the minimal Schur-NNI solve

Safe claim:
  The minimal Schur-NNI surface still fails as a self-contained CKM+CP closure.
  The freer complex-carrier completion also still exists.

  This runner asks for the smallest current bounded carrier that still closes
  the full quark package well. It restricts the added 1-3 carrier to the exact
  CKM projector direction

      sqrt(1/6) + i sqrt(5/6)

  and tests two reduced ansatze:

    1. phase-free additive amplitudes on that fixed ray;
    2. the same two sector amplitudes plus one shared extra phase on the ray.

  Result:
    - the phase-free ansatz already lands very close to the full target;
    - one shared phase closes the full quark package numerically while keeping
      arg det(M_u M_d) = 0 mod 2pi.

  This is still bounded support, not a retained theorem.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import differential_evolution, minimize

from frontier_quark_mass_ratio_full_solve import (
    C12_D,
    C12_U,
    C23_D,
    C23_U,
    J_ATLAS,
    R_CT_OBS,
    R_DB,
    R_SB,
    R_UC_OBS,
    V_CB_ATLAS,
    V_UB_ATLAS,
    V_US_ATLAS,
    solve_magnitude_surface,
)


PASS_COUNT = 0
FAIL_COUNT = 0

PROJECTOR_BRANCH = complex(math.sqrt(1.0 / 6.0), math.sqrt(5.0 / 6.0))


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def wrap_to_pi(angle: float) -> float:
    return ((angle + math.pi) % (2.0 * math.pi)) - math.pi


@dataclass(frozen=True)
class ProjectorSolve:
    r_uc: float
    r_ct: float
    amp_u: float
    amp_d: float
    phase: float
    c13_u_base: float
    c13_d_base: float
    c13_u_total: complex
    c13_d_total: complex
    vus: float
    vcb: float
    vub: float
    jarlskog: float
    det_phase: float
    objective: float


def build_nni_with_complex_13(
    m1: float,
    m2: float,
    m3: float,
    c12: float,
    c23: float,
    c13_complex: complex,
) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=complex)
    matrix[0, 0] = m1
    matrix[1, 1] = m2
    matrix[2, 2] = m3
    matrix[0, 1] = c12 * math.sqrt(m1 * m2)
    matrix[1, 0] = np.conj(matrix[0, 1])
    matrix[1, 2] = c23 * math.sqrt(m2 * m3)
    matrix[2, 1] = np.conj(matrix[1, 2])
    matrix[0, 2] = c13_complex * math.sqrt(m1 * m3)
    matrix[2, 0] = np.conj(matrix[0, 2])
    return matrix


def diag_hermitian_square(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h = matrix @ matrix.conj().T
    eigvals, eigvecs = np.linalg.eigh(h)
    order = np.argsort(eigvals)
    return eigvals[order], eigvecs[:, order]


def compute_projector_observables(
    point: np.ndarray,
    shared_phase: bool,
) -> tuple[float, float, complex, complex, float, float, float, float, float]:
    if shared_phase:
        r_uc, r_ct, amp_u, amp_d, phase = point
    else:
        r_uc, r_ct, amp_u, amp_d = point
        phase = 0.0

    if r_uc <= 0.0 or r_ct <= 0.0 or r_uc * r_ct >= 1.0:
        raise ValueError("invalid mass-ratio point")

    m_u = r_uc * r_ct
    m_c = r_ct
    m_t = 1.0

    m_d = R_DB
    m_s = R_SB
    m_b = 1.0

    c13_u_base = C12_U * C23_U * math.sqrt(m_u / m_t)
    c13_d_base = C12_D * C23_D * math.sqrt(m_d / m_b)

    rotated_branch = PROJECTOR_BRANCH * complex(math.cos(phase), math.sin(phase))
    c13_u_total = c13_u_base + amp_u * rotated_branch
    c13_d_total = c13_d_base + amp_d * rotated_branch

    m_u_matrix = build_nni_with_complex_13(m_u, m_c, m_t, C12_U, C23_U, c13_u_total)
    m_d_matrix = build_nni_with_complex_13(m_d, m_s, m_b, C12_D, C23_D, c13_d_total)

    _, u_u = diag_hermitian_square(m_u_matrix)
    _, u_d = diag_hermitian_square(m_d_matrix)
    v = u_u.conj().T @ u_d

    vus = abs(v[0, 1])
    vcb = abs(v[1, 2])
    vub = abs(v[0, 2])
    jarlskog = abs(np.imag(v[0, 1] * v[1, 2] * np.conj(v[0, 2]) * np.conj(v[1, 1])))
    det_prod = np.linalg.det(m_u_matrix) * np.linalg.det(m_d_matrix)
    det_phase = abs(wrap_to_pi(cmath.phase(det_prod)))

    return (
        c13_u_base,
        c13_d_base,
        c13_u_total,
        c13_d_total,
        vus,
        vcb,
        vub,
        jarlskog,
        det_phase,
    )


def projector_objective(point: np.ndarray, shared_phase: bool) -> float:
    try:
        (
            _c13_u_base,
            _c13_d_base,
            _c13_u_total,
            _c13_d_total,
            vus,
            vcb,
            vub,
            jarlskog,
            _det_phase,
        ) = compute_projector_observables(point, shared_phase)
    except ValueError:
        return 1.0e12

    r_uc, r_ct = point[:2]
    residuals = np.array(
        [
            (r_uc - R_UC_OBS) / 1.0e-4,
            (r_ct - R_CT_OBS) / 1.0e-4,
            (vus - V_US_ATLAS) / 1.0e-4,
            (vcb - V_CB_ATLAS) / 1.0e-4,
            (vub - V_UB_ATLAS) / 1.0e-4,
            (jarlskog - J_ATLAS) / 2.0e-6,
        ],
        dtype=float,
    )
    return float(np.sum(residuals**2))


def solve_projector_surface(shared_phase: bool) -> ProjectorSolve:
    if shared_phase:
        bounds = [
            (5.0e-4, 5.0e-3),
            (4.0e-3, 2.0e-2),
            (-1.0, 1.0),
            (-1.0, 1.0),
            (-math.pi, math.pi),
        ]
        seeds = [
            np.array([R_UC_OBS, R_CT_OBS, -0.81, -0.16, 3.10], dtype=float),
            np.array([R_UC_OBS, R_CT_OBS, 0.79, 0.15, 0.0], dtype=float),
        ]
        seed_id = 52
    else:
        bounds = [
            (5.0e-4, 5.0e-3),
            (4.0e-3, 2.0e-2),
            (-1.0, 1.0),
            (-1.0, 1.0),
        ]
        seeds = [np.array([R_UC_OBS, R_CT_OBS, 0.79, 0.15], dtype=float)]
        seed_id = 42

    global_result = differential_evolution(
        lambda x: projector_objective(x, shared_phase),
        bounds,
        maxiter=120,
        popsize=18,
        seed=seed_id,
        polish=False,
    )

    best_x: np.ndarray | None = None
    best_fun: float | None = None
    for seed in [global_result.x, *seeds]:
        result = minimize(
            lambda x: projector_objective(x, shared_phase),
            seed,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 1200},
        )
        if best_fun is None or result.fun < best_fun:
            best_x = result.x
            best_fun = float(result.fun)

    assert best_x is not None and best_fun is not None

    (
        c13_u_base,
        c13_d_base,
        c13_u_total,
        c13_d_total,
        vus,
        vcb,
        vub,
        jarlskog,
        det_phase,
    ) = compute_projector_observables(best_x, shared_phase)

    phase = float(best_x[4]) if shared_phase else 0.0
    return ProjectorSolve(
        r_uc=float(best_x[0]),
        r_ct=float(best_x[1]),
        amp_u=float(best_x[2]),
        amp_d=float(best_x[3]),
        phase=phase,
        c13_u_base=c13_u_base,
        c13_d_base=c13_d_base,
        c13_u_total=c13_u_total,
        c13_d_total=c13_d_total,
        vus=vus,
        vcb=vcb,
        vub=vub,
        jarlskog=jarlskog,
        det_phase=det_phase,
        objective=best_fun,
    )


def part1_anchor() -> float:
    print("\n" + "=" * 72)
    print("PART 1: Minimal-Surface Anchor")
    print("=" * 72)

    anchor = solve_magnitude_surface()
    ratio = anchor.jarlskog / J_ATLAS

    print(f"\n  anchor m_u/m_c      = {anchor.r_uc:.6e}")
    print(f"  anchor m_c/m_t      = {anchor.r_ct:.6e}")
    print(f"  anchor |V_us|       = {anchor.vus:.6f}")
    print(f"  anchor |V_cb|       = {anchor.vcb:.6f}")
    print(f"  anchor |V_ub|       = {anchor.vub:.6f}")
    print(f"  anchor J            = {anchor.jarlskog:.6e}")
    print(f"  anchor J/J_atlas    = {ratio:.6f}")

    check(
        "The minimal surface still undershoots J by more than 5x",
        J_ATLAS / anchor.jarlskog > 5.0,
        f"factor = {J_ATLAS / anchor.jarlskog:.2f}",
    )
    return anchor.jarlskog


def summarize_solution(label: str, result: ProjectorSolve) -> None:
    dev_uc = (result.r_uc / R_UC_OBS - 1.0) * 100.0
    dev_ct = (result.r_ct / R_CT_OBS - 1.0) * 100.0
    print(f"\n  {label}:")
    print(f"    m_u/m_c = {result.r_uc:.6e}  (dev: {dev_uc:+.3f}%)")
    print(f"    m_c/m_t = {result.r_ct:.6e}  (dev: {dev_ct:+.3f}%)")
    print(f"    amp_u   = {result.amp_u:+.6f}")
    print(f"    amp_d   = {result.amp_d:+.6f}")
    if abs(result.phase) > 0.0:
        print(f"    phase   = {math.degrees(result.phase):.6f} deg")
    print(
        f"    c13_u(total) = {result.c13_u_total.real:+.6f} {result.c13_u_total.imag:+.6f} i"
    )
    print(
        f"    c13_d(total) = {result.c13_d_total.real:+.6f} {result.c13_d_total.imag:+.6f} i"
    )
    print(f"    |V_us| = {result.vus:.9f}")
    print(f"    |V_cb| = {result.vcb:.9f}")
    print(f"    |V_ub| = {result.vub:.9f}")
    print(f"    J      = {result.jarlskog:.9e}")
    print(f"    arg det(M_u M_d) = {result.det_phase:.3e} rad")
    print(f"    objective score  = {result.objective:.6f}")


def part2_reduced_completions(anchor_j: float) -> tuple[ProjectorSolve, ProjectorSolve]:
    print("\n" + "=" * 72)
    print("PART 2: Reduced Projector-Ray Completions")
    print("=" * 72)
    print(f"\n  fixed projector ray = {PROJECTOR_BRANCH.real:+.6f} {PROJECTOR_BRANCH.imag:+.6f} i")
    print("  ansatz A            = base + amp_u/d * projector_ray")
    print("  ansatz B            = base + amp_u/d * projector_ray * exp(i phi_shared)")

    phase_free = solve_projector_surface(shared_phase=False)
    summarize_solution("Phase-free projector amplitudes", phase_free)

    shared_phase = solve_projector_surface(shared_phase=True)
    summarize_solution("Projector amplitudes + shared phase", shared_phase)

    check(
        "The phase-free projector ansatz already lands within 2% of the atlas J",
        abs(phase_free.jarlskog / J_ATLAS - 1.0) < 0.02,
        f"ratio = {phase_free.jarlskog / J_ATLAS:.6f}",
    )
    check(
        "The shared-phase projector ansatz matches J within 1%",
        abs(shared_phase.jarlskog / J_ATLAS - 1.0) < 0.01,
        f"ratio = {shared_phase.jarlskog / J_ATLAS:.6f}",
    )
    check(
        "The shared-phase projector ansatz keeps both quark ratios within 1%",
        abs(shared_phase.r_uc / R_UC_OBS - 1.0) < 0.01
        and abs(shared_phase.r_ct / R_CT_OBS - 1.0) < 0.01,
        f"dev = ({(shared_phase.r_uc / R_UC_OBS - 1.0) * 100:+.3f}%, {(shared_phase.r_ct / R_CT_OBS - 1.0) * 100:+.3f}%)",
    )
    check(
        "The shared-phase projector ansatz matches all CKM magnitudes within 0.1%",
        abs(shared_phase.vus / V_US_ATLAS - 1.0) < 1.0e-3
        and abs(shared_phase.vcb / V_CB_ATLAS - 1.0) < 1.0e-3
        and abs(shared_phase.vub / V_UB_ATLAS - 1.0) < 1.0e-3,
        f"ratios = ({shared_phase.vus / V_US_ATLAS:.6f}, {shared_phase.vcb / V_CB_ATLAS:.6f}, {shared_phase.vub / V_UB_ATLAS:.6f})",
    )
    check(
        "The projector completions keep determinant phase closure",
        phase_free.det_phase < 1.0e-10 and shared_phase.det_phase < 1.0e-10,
        f"det phases = ({phase_free.det_phase:.3e}, {shared_phase.det_phase:.3e})",
    )
    check(
        "One shared phase materially improves the reduced projector fit",
        shared_phase.objective < phase_free.objective,
        f"objective ratio = {shared_phase.objective / phase_free.objective:.3f}",
    )
    check(
        "The shared-phase projector fit lifts J by more than 6x over the minimal anchor",
        shared_phase.jarlskog / anchor_j > 6.0,
        f"lift = {shared_phase.jarlskog / anchor_j:.3f}x",
    )

    return phase_free, shared_phase


def part3_summary(shared_phase: ProjectorSolve) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Summary")
    print("=" * 72)

    print("\n  Strongest current bounded closure on this branch:")
    print("    one fixed projector ray, two sector amplitudes, and one shared phase")
    print("    are already enough to close the full quark package numerically")
    print()
    print("  Honest status:")
    print("    this is stronger than the free complex-carrier completion because the")
    print("    added carrier is now compressed to a common ray with minimal extra freedom")
    print("    but it is still bounded because the amplitudes and shared phase are solved,")
    print("    not retained-derived")
    print()
    print("  Solved shared phase:")
    print(f"    phi_shared = {math.degrees(shared_phase.phase):.6f} deg")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Reduced Quark Closure on a Fixed Projector Ray")
    print("=" * 72)

    anchor_j = part1_anchor()
    _phase_free, shared_phase = part2_reduced_completions(anchor_j)
    part3_summary(shared_phase)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
