#!/usr/bin/env python3
"""
Minimal Schur-NNI full quark solve on the current quark mass-ratio lane.

Status:
  bounded magnitude closure on the minimal Schur-NNI surface
  plus a quantified CP-area ceiling on that same surface

Safe claim:
  If one combines
    - the current Phase 1 down-type ratios from the promoted CKM atlas,
    - the current CKM atlas magnitudes and phase,
    - and the historical minimal Schur-NNI coefficient surface,
  then the up-sector ratios can be numerically inverted from the CKM
  magnitudes with no observed up-quark mass-ratio input.

  On that surface the magnitude solve is strong:
    m_u/m_c and m_c/m_t land very close to the observation comparator.

  But the same minimal Schur-NNI surface still under-produces the
  Jarlskog invariant by a large factor, even after relaxing the up/down
  1-3 phases while keeping the CKM magnitudes close to the atlas values.
  So the current branch gets a strong quark-magnitude solve, not a full
  CP-complete quark closure theorem.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0


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


ALPHA_S_V = CANONICAL_ALPHA_S_V

# Current Phase 1 down-type ratios.
R_DS = ALPHA_S_V / 2.0
R_SB = (ALPHA_S_V / math.sqrt(6.0)) ** (6.0 / 5.0)
R_DB = R_DS * R_SB

# Promoted CKM atlas surface.
V_US_ATLAS = math.sqrt(ALPHA_S_V / 2.0)
V_CB_ATLAS = ALPHA_S_V / math.sqrt(6.0)
V_UB_ATLAS = ALPHA_S_V ** 1.5 / (6.0 * math.sqrt(2.0))
DELTA_STD = math.atan(math.sqrt(5.0))

S12 = V_US_ATLAS
S23 = V_CB_ATLAS
S13 = V_UB_ATLAS
C12 = math.sqrt(1.0 - S12 * S12)
C23 = math.sqrt(1.0 - S23 * S23)
C13 = math.sqrt(1.0 - S13 * S13)
J_ATLAS = C12 * S12 * C23 * S23 * C13 * C13 * S13 * math.sin(DELTA_STD)

# Observation comparators (not derivation inputs).
R_UC_OBS = 2.16e-3 / 1.273
R_CT_OBS = 1.273 / 172.57

# Historical minimal Schur-NNI coefficient surface.
C12_U = 1.48
C23_U = 0.65
C12_D = 0.91
C23_D = 0.65

# Magnitude-preserving tolerances for the phase-relaxed ceiling search.
MAG_TOLS = np.array([2.0e-3, 2.0e-3, 1.0e-3])


@dataclass(frozen=True)
class MagnitudeSolve:
    r_uc: float
    r_ct: float
    vus: float
    vcb: float
    vub: float
    jarlskog: float
    objective: float


@dataclass(frozen=True)
class CeilingSolve:
    r_uc: float
    r_ct: float
    delta_u: float
    delta_d: float
    vus: float
    vcb: float
    vub: float
    jarlskog: float
    objective: float


def build_nni_complex(
    m1: float,
    m2: float,
    m3: float,
    c12: float,
    c23: float,
    c13: float,
    delta: float,
) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=complex)
    matrix[0, 0] = m1
    matrix[1, 1] = m2
    matrix[2, 2] = m3
    matrix[0, 1] = c12 * math.sqrt(m1 * m2)
    matrix[1, 0] = np.conj(matrix[0, 1])
    matrix[1, 2] = c23 * math.sqrt(m2 * m3)
    matrix[2, 1] = np.conj(matrix[1, 2])
    matrix[0, 2] = c13 * math.sqrt(m1 * m3) * np.exp(1j * delta)
    matrix[2, 0] = np.conj(matrix[0, 2])
    return matrix


def diag_hermitian(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h = matrix @ matrix.conj().T
    eigvals, eigvecs = np.linalg.eigh(h)
    order = np.argsort(eigvals)
    return eigvals[order], eigvecs[:, order]


def compute_ckm_observables(
    r_uc: float,
    r_ct: float,
    delta_u: float,
    delta_d: float,
) -> tuple[float, float, float, float]:
    m_u = r_uc * r_ct
    m_c = r_ct
    m_t = 1.0

    m_d = R_DB
    m_s = R_SB
    m_b = 1.0

    c13_u = C12_U * C23_U * math.sqrt(m_u / m_t)
    c13_d = C12_D * C23_D * math.sqrt(m_d / m_b)

    m_u_matrix = build_nni_complex(m_u, m_c, m_t, C12_U, C23_U, c13_u, delta_u)
    m_d_matrix = build_nni_complex(m_d, m_s, m_b, C12_D, C23_D, c13_d, delta_d)

    _, u_u = diag_hermitian(m_u_matrix)
    _, u_d = diag_hermitian(m_d_matrix)
    v = u_u.conj().T @ u_d

    vus = abs(v[0, 1])
    vcb = abs(v[1, 2])
    vub = abs(v[0, 2])
    jarlskog = abs(np.imag(v[0, 1] * v[1, 2] * np.conj(v[0, 2]) * np.conj(v[1, 1])))
    return vus, vcb, vub, jarlskog


def magnitude_objective(point: np.ndarray) -> float:
    r_uc, r_ct = point
    if r_uc <= 0.0 or r_ct <= 0.0 or r_uc * r_ct >= 1.0:
        return 1.0e12

    vus, vcb, vub, _ = compute_ckm_observables(r_uc, r_ct, DELTA_STD, DELTA_STD)
    residuals = np.array([vus - V_US_ATLAS, vcb - V_CB_ATLAS, vub - V_UB_ATLAS])
    scales = np.array([1.0e-3, 1.0e-3, 5.0e-4])
    return float(np.sum((residuals / scales) ** 2))


def phase_relaxed_objective(point: np.ndarray) -> float:
    r_uc, r_ct, delta_u, delta_d = point
    if r_uc <= 0.0 or r_ct <= 0.0 or r_uc * r_ct >= 1.0:
        return 1.0e12

    vus, vcb, vub, jarlskog = compute_ckm_observables(r_uc, r_ct, delta_u, delta_d)
    mags = np.array([vus, vcb, vub])
    over = np.maximum(np.abs(mags - np.array([V_US_ATLAS, V_CB_ATLAS, V_UB_ATLAS])) - MAG_TOLS, 0.0)
    penalty = np.sum((over / MAG_TOLS) ** 2)

    # Once the magnitudes sit inside the declared corridor, maximize J.
    return float(penalty - jarlskog / J_ATLAS)


def multistart_minimize(
    objective,
    seeds: list[tuple[float, ...]],
    bounds: list[tuple[float, float]],
) -> tuple[np.ndarray, float]:
    best_x: np.ndarray | None = None
    best_fun: float | None = None

    for seed in seeds:
        result = minimize(
            objective,
            np.asarray(seed, dtype=float),
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 800},
        )
        if best_fun is None or result.fun < best_fun:
            best_x = result.x
            best_fun = float(result.fun)

    assert best_x is not None and best_fun is not None
    return best_x, best_fun


def solve_magnitude_surface() -> MagnitudeSolve:
    seeds = [
        (1.7e-3, 7.4e-3),
        (1.0e-3, 5.0e-3),
        (3.0e-3, 1.0e-2),
        (1.0e-2, 2.0e-2),
        (5.0e-4, 2.0e-2),
        (2.0e-2, 5.0e-2),
    ]
    bounds = [(1.0e-6, 0.1), (1.0e-5, 0.1)]

    best_x, best_fun = multistart_minimize(magnitude_objective, seeds, bounds)
    r_uc, r_ct = best_x
    vus, vcb, vub, jarlskog = compute_ckm_observables(r_uc, r_ct, DELTA_STD, DELTA_STD)
    return MagnitudeSolve(r_uc, r_ct, vus, vcb, vub, jarlskog, best_fun)


def solve_phase_relaxed_ceiling(magnitude_solve: MagnitudeSolve) -> CeilingSolve:
    rng = np.random.default_rng(2)
    seeds: list[tuple[float, float, float, float]] = [
        (magnitude_solve.r_uc, magnitude_solve.r_ct, DELTA_STD, DELTA_STD),
        (magnitude_solve.r_uc, magnitude_solve.r_ct, 0.25 * math.pi, 1.55 * math.pi),
        (magnitude_solve.r_uc, magnitude_solve.r_ct, 1.70 * math.pi, 0.75 * math.pi),
        (1.8e-3, 4.5e-2, 5.4, 2.3),
    ]
    for _ in range(120):
        seeds.append(
            (
                10.0 ** rng.uniform(-4.0, -1.0),
                10.0 ** rng.uniform(-3.0, -1.0),
                rng.uniform(0.0, 2.0 * math.pi),
                rng.uniform(0.0, 2.0 * math.pi),
            )
        )

    bounds = [
        (1.0e-6, 0.1),
        (1.0e-5, 0.1),
        (0.0, 2.0 * math.pi),
        (0.0, 2.0 * math.pi),
    ]

    best_feasible: CeilingSolve | None = None
    best_infeasible: CeilingSolve | None = None

    for seed in seeds:
        result = minimize(
            phase_relaxed_objective,
            np.asarray(seed, dtype=float),
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 800},
        )
        r_uc, r_ct, delta_u, delta_d = result.x
        vus, vcb, vub, jarlskog = compute_ckm_observables(r_uc, r_ct, delta_u, delta_d)
        candidate = CeilingSolve(
            r_uc,
            r_ct,
            delta_u,
            delta_d,
            vus,
            vcb,
            vub,
            jarlskog,
            float(result.fun),
        )
        feasible = (
            abs(vus - V_US_ATLAS) <= MAG_TOLS[0]
            and abs(vcb - V_CB_ATLAS) <= MAG_TOLS[1]
            and abs(vub - V_UB_ATLAS) <= MAG_TOLS[2]
        )
        if feasible:
            if best_feasible is None or candidate.jarlskog > best_feasible.jarlskog:
                best_feasible = candidate
        elif best_infeasible is None or candidate.objective < best_infeasible.objective:
            best_infeasible = candidate

    return best_feasible if best_feasible is not None else best_infeasible


def part1_input_surface() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Phase 1 Down-Type Anchor + CKM Atlas Targets")
    print("=" * 72)

    print(f"\n  alpha_s(v)            = {ALPHA_S_V:.12f}")
    print(f"  m_d/m_s               = {R_DS:.6f}")
    print(f"  m_s/m_b               = {R_SB:.6f}")
    print(f"  m_d/m_b               = {R_DB:.6f}")
    print()
    print(f"  |V_us|_atlas          = {V_US_ATLAS:.6f}")
    print(f"  |V_cb|_atlas          = {V_CB_ATLAS:.6f}")
    print(f"  |V_ub|_atlas          = {V_UB_ATLAS:.6f}")
    print(f"  delta_std             = {math.degrees(DELTA_STD):.6f} deg")
    print(f"  J_atlas               = {J_ATLAS:.6e}")

    check(
        "Phase 1 down-type ratio reproduces the atlas Cabibbo magnitude",
        abs(math.sqrt(R_DS) - V_US_ATLAS) < 1.0e-14,
        f"sqrt(m_d/m_s) = {math.sqrt(R_DS):.8f}",
    )
    check(
        "Phase 1 down-type ratio reproduces the atlas 2-3 CKM magnitude",
        abs(R_SB ** (5.0 / 6.0) - V_CB_ATLAS) < 1.0e-14,
        f"(m_s/m_b)^(5/6) = {R_SB ** (5.0 / 6.0):.8f}",
    )
    check(
        "The atlas 1-3 entry obeys |V_ub| = |V_us||V_cb|/sqrt(6)",
        abs(V_UB_ATLAS - (V_US_ATLAS * V_CB_ATLAS / math.sqrt(6.0))) < 1.0e-14,
        f"ratio = {V_UB_ATLAS / (V_US_ATLAS * V_CB_ATLAS):.8f}",
    )
    check(
        "The atlas Jarlskog follows from the atlas magnitudes and delta_std",
        abs(
            J_ATLAS
            - C12 * S12 * C23 * S23 * C13 * C13 * S13 * math.sin(DELTA_STD)
        )
        < 1.0e-16,
        f"J_atlas = {J_ATLAS:.8e}",
    )


def part2_magnitude_solve(result: MagnitudeSolve) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Minimal Schur-NNI Magnitude Solve")
    print("=" * 72)

    dev_uc = (result.r_uc / R_UC_OBS - 1.0) * 100.0
    dev_ct = (result.r_ct / R_CT_OBS - 1.0) * 100.0

    print("\n  Surface assumptions:")
    print("    - down-type ratios fixed by Phase 1")
    print("    - minimal Schur-NNI coefficients fixed to the historical surface")
    print("    - common phase delta_u = delta_d = delta_std")
    print("    - solve only for (m_u/m_c, m_c/m_t) from CKM magnitudes")
    print()
    print(f"  solved m_u/m_c        = {result.r_uc:.6e}  (obs: {R_UC_OBS:.6e})")
    print(f"  solved m_c/m_t        = {result.r_ct:.6e}  (obs: {R_CT_OBS:.6e})")
    print(f"  |V_us|                = {result.vus:.6f}")
    print(f"  |V_cb|                = {result.vcb:.6f}")
    print(f"  |V_ub|                = {result.vub:.6f}")
    print(f"  intrinsic J           = {result.jarlskog:.6e}")
    print(f"  optimizer score       = {result.objective:.6f}")

    check(
        "Magnitude inversion converges to an interior up-sector solve",
        0.0 < result.r_uc < 0.01 and 0.0 < result.r_ct < 0.05,
        f"m_u/m_c = {result.r_uc:.3e}, m_c/m_t = {result.r_ct:.3e}",
    )
    check(
        "|V_us| matches the atlas target within 0.1%",
        abs(result.vus / V_US_ATLAS - 1.0) < 1.0e-3,
        f"ratio = {result.vus / V_US_ATLAS:.6f}",
    )
    check(
        "|V_cb| matches the atlas target within 0.3%",
        abs(result.vcb / V_CB_ATLAS - 1.0) < 3.0e-3,
        f"ratio = {result.vcb / V_CB_ATLAS:.6f}",
    )
    check(
        "|V_ub| matches the atlas target within 5%",
        abs(result.vub / V_UB_ATLAS - 1.0) < 0.05,
        f"ratio = {result.vub / V_UB_ATLAS:.6f}",
    )
    check(
        "Solved m_u/m_c lands within 5% of the observation comparator",
        abs(dev_uc) < 5.0,
        f"dev = {dev_uc:+.2f}%",
    )
    check(
        "Solved m_c/m_t lands within 5% of the observation comparator",
        abs(dev_ct) < 5.0,
        f"dev = {dev_ct:+.2f}%",
    )


def part3_intrinsic_cp_gap(result: MagnitudeSolve) -> None:
    print("\n" + "=" * 72)
    print("PART 3: Intrinsic CP Gap on the Magnitude-Solved Surface")
    print("=" * 72)

    ratio = result.jarlskog / J_ATLAS
    print(f"\n  J_intrinsic / J_atlas = {ratio:.6f}")
    print(f"  J_intrinsic           = {result.jarlskog:.6e}")
    print(f"  J_atlas               = {J_ATLAS:.6e}")
    print(f"  underprediction       = {J_ATLAS / result.jarlskog:.2f}x")

    check(
        "The minimal Schur-NNI magnitude solve under-produces J strongly",
        ratio < 0.25,
        f"J_intrinsic/J_atlas = {ratio:.4f}",
    )
    check(
        "The CP-area deficit is larger than a factor of 5",
        (J_ATLAS / result.jarlskog) > 5.0,
        f"factor = {J_ATLAS / result.jarlskog:.2f}",
    )


def part4_phase_relaxed_ceiling(result: CeilingSolve) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Phase-Relaxed J Ceiling at Fixed CKM Magnitude Corridor")
    print("=" * 72)

    print("\n  Corridor:")
    print(f"    |V_us - target| <= {MAG_TOLS[0]:.4f}")
    print(f"    |V_cb - target| <= {MAG_TOLS[1]:.4f}")
    print(f"    |V_ub - target| <= {MAG_TOLS[2]:.4f}")
    print()
    print(f"  best relaxed m_u/m_c  = {result.r_uc:.6e}")
    print(f"  best relaxed m_c/m_t  = {result.r_ct:.6e}")
    print(f"  delta_u               = {math.degrees(result.delta_u):.3f} deg")
    print(f"  delta_d               = {math.degrees(result.delta_d):.3f} deg")
    print(f"  |V_us|                = {result.vus:.6f}")
    print(f"  |V_cb|                = {result.vcb:.6f}")
    print(f"  |V_ub|                = {result.vub:.6f}")
    print(f"  J_ceiling             = {result.jarlskog:.6e}")

    check(
        "Phase relaxation keeps the CKM magnitudes inside the declared corridor",
        abs(result.vus - V_US_ATLAS) <= MAG_TOLS[0]
        and abs(result.vcb - V_CB_ATLAS) <= MAG_TOLS[1]
        and abs(result.vub - V_UB_ATLAS) <= MAG_TOLS[2],
        f"dv = ({result.vus - V_US_ATLAS:+.4e}, {result.vcb - V_CB_ATLAS:+.4e}, {result.vub - V_UB_ATLAS:+.4e})",
    )
    check(
        "The phase-relaxed J ceiling still stays below 25% of the atlas J",
        result.jarlskog / J_ATLAS < 0.25,
        f"J_ceiling/J_atlas = {result.jarlskog / J_ATLAS:.4f}",
    )
    check(
        "Even the relaxed surface still misses the atlas J by more than 4x",
        (J_ATLAS / result.jarlskog) > 4.0,
        f"factor = {J_ATLAS / result.jarlskog:.2f}",
    )


def part5_summary(magnitude_solve: MagnitudeSolve, ceiling_solve: CeilingSolve) -> None:
    print("\n" + "=" * 72)
    print("PART 5: Summary")
    print("=" * 72)

    print("\n  Strong result on the current branch:")
    print("    the minimal Schur-NNI inversion closes the quark magnitudes well")
    print(f"    m_u/m_c = {magnitude_solve.r_uc:.6e}")
    print(f"    m_c/m_t = {magnitude_solve.r_ct:.6e}")
    print()
    print("  Honest remaining blocker:")
    print("    the same surface does not close the CP area")
    print(f"    intrinsic J = {magnitude_solve.jarlskog:.6e}")
    print(f"    relaxed J ceiling = {ceiling_solve.jarlskog:.6e}")
    print(f"    atlas J = {J_ATLAS:.6e}")
    print()
    print("  Interpretation:")
    print("    the current quark lane is materially stronger than the lepton lane")
    print("    because the magnitudes invert cleanly on this surface")
    print("    but one extra CP-area primitive is still missing for full closure")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Quark Mass-Ratio Full Solve on the Minimal Schur-NNI Surface")
    print("=" * 72)

    part1_input_surface()
    magnitude_solve = solve_magnitude_surface()
    part2_magnitude_solve(magnitude_solve)
    part3_intrinsic_cp_gap(magnitude_solve)
    ceiling_solve = solve_phase_relaxed_ceiling(magnitude_solve)
    part4_phase_relaxed_ceiling(ceiling_solve)
    part5_summary(magnitude_solve, ceiling_solve)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
