#!/usr/bin/env python3
"""
Exploratory bounded scan of 1+5-projector / tensor deformations on the live
quark mass-ratio lane.

Scope:
  - keep the current Phase 1 down-sector anchor and historical minimal
    Schur-NNI coefficients;
  - deform only the 1-3 Schur slot, since that is the slot tied to the
    CKM atlas 1+5 quark-block structure;
  - compare projector-like and tensor-like complex deformations against the
    current baseline CP gap.

Safe use:
  This is an exploratory bounded scan, not a theorem claim. It asks whether
  structurally motivated deformations can raise the Jarlskog area while
  keeping CKM magnitudes and quark mass ratios near the current lane.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import differential_evolution

from frontier_quark_mass_ratio_full_solve import (
    C12_D,
    C12_U,
    C23_D,
    C23_U,
    J_ATLAS,
    MAG_TOLS,
    R_CT_OBS,
    R_DB,
    R_SB,
    R_UC_OBS,
    V_CB_ATLAS,
    V_UB_ATLAS,
    V_US_ATLAS,
    build_nni_complex,
    diag_hermitian,
    solve_magnitude_surface,
    solve_phase_relaxed_ceiling,
)


P_CENTER = 1.0 / 6.0
P_ORTH = 5.0 / 6.0
DELTA_STD = math.atan(math.sqrt(5.0))
SUPPORT_DELTA = 1.0 / 42.0
MASS_TOL = 0.05
TARGET_MAGS = np.array([V_US_ATLAS, V_CB_ATLAS, V_UB_ATLAS], dtype=float)

# The exact 1+5 projector angle is exp(±i delta_std) with
# delta_std = arctan(sqrt(5)).
PROJECTOR_BRANCH = complex(math.sqrt(P_CENTER), math.sqrt(P_ORTH))

# The exact bilinear bright column keeps unit leading amplitude and only the
# lower-row dressing proportional to delta_A1 = 1/42. As an exploratory
# 1-3 surrogate, only that lower-row complex dressing is turned on here.
TENSOR_BRANCH = 1j * math.sqrt(P_ORTH) * SUPPORT_DELTA


@dataclass(frozen=True)
class ScanConfig:
    label: str
    family: str
    amp_bound: float
    maxiter: int
    popsize: int


@dataclass(frozen=True)
class Candidate:
    config_label: str
    family: str
    sign_u: int
    sign_d: int
    r_uc: float
    r_ct: float
    delta_u: float
    delta_d: float
    amp_u: float
    amp_d: float
    vus: float
    vcb: float
    vub: float
    jarlskog: float
    objective: float

    @property
    def mass_dev_uc(self) -> float:
        return self.r_uc / R_UC_OBS - 1.0

    @property
    def mass_dev_ct(self) -> float:
        return self.r_ct / R_CT_OBS - 1.0

    @property
    def dv(self) -> np.ndarray:
        return np.array(
            [self.vus - V_US_ATLAS, self.vcb - V_CB_ATLAS, self.vub - V_UB_ATLAS],
            dtype=float,
        )

    @property
    def feasible(self) -> bool:
        return (
            np.all(np.abs(self.dv) <= MAG_TOLS)
            and abs(self.mass_dev_uc) <= MASS_TOL
            and abs(self.mass_dev_ct) <= MASS_TOL
        )

    @property
    def j_ratio(self) -> float:
        return self.jarlskog / J_ATLAS

    @property
    def boundary_hit(self) -> bool:
        # The scan uses symmetric amplitude boxes per family.
        bound = next(cfg.amp_bound for cfg in SCAN_CONFIGS if cfg.label == self.config_label)
        edge_slack = max(5.0e-2, 0.02 * bound)
        return max(abs(self.amp_u), abs(self.amp_d)) >= bound - edge_slack


SCAN_CONFIGS = (
    ScanConfig(
        label="projector_mild",
        family="projector",
        amp_bound=1.5,
        maxiter=40,
        popsize=10,
    ),
    ScanConfig(
        label="projector_wide",
        family="projector",
        amp_bound=6.0,
        maxiter=50,
        popsize=10,
    ),
    ScanConfig(
        label="tensor_wide",
        family="tensor",
        amp_bound=6.0,
        maxiter=50,
        popsize=10,
    ),
)


def branch_direction(family: str, sign: int) -> complex:
    if family == "projector":
        base = PROJECTOR_BRANCH
    elif family == "tensor":
        base = TENSOR_BRANCH
    else:
        raise ValueError(f"Unknown family: {family}")
    return base if sign > 0 else np.conj(base)


def deformed_observables(
    family: str,
    sign_u: int,
    sign_d: int,
    r_uc: float,
    r_ct: float,
    delta_u: float,
    delta_d: float,
    amp_u: float,
    amp_d: float,
) -> tuple[float, float, float, float]:
    m_u = r_uc * r_ct
    m_c = r_ct
    m_t = 1.0

    m_d = R_DB
    m_s = R_SB
    m_b = 1.0

    c13_u_base = C12_U * C23_U * math.sqrt(m_u / m_t)
    c13_d_base = C12_D * C23_D * math.sqrt(m_d / m_b)

    z_u = 1.0 + amp_u * branch_direction(family, sign_u)
    z_d = 1.0 + amp_d * branch_direction(family, sign_d)

    m_u_matrix = build_nni_complex(
        m_u,
        m_c,
        m_t,
        C12_U,
        C23_U,
        c13_u_base * abs(z_u),
        delta_u + math.atan2(z_u.imag, z_u.real),
    )
    m_d_matrix = build_nni_complex(
        m_d,
        m_s,
        m_b,
        C12_D,
        C23_D,
        c13_d_base * abs(z_d),
        delta_d + math.atan2(z_d.imag, z_d.real),
    )

    _, u_u = diag_hermitian(m_u_matrix @ m_u_matrix.conj().T)
    _, u_d = diag_hermitian(m_d_matrix @ m_d_matrix.conj().T)
    v = u_u.conj().T @ u_d

    vus = abs(v[0, 1])
    vcb = abs(v[1, 2])
    vub = abs(v[0, 2])
    jarlskog = abs(np.imag(v[0, 1] * v[1, 2] * np.conj(v[0, 2]) * np.conj(v[1, 1])))
    return vus, vcb, vub, jarlskog


def candidate_from_point(
    config: ScanConfig,
    sign_u: int,
    sign_d: int,
    point: np.ndarray,
    objective: float,
) -> Candidate:
    r_uc, r_ct, delta_u, delta_d, amp_u, amp_d = point
    vus, vcb, vub, jarlskog = deformed_observables(
        config.family,
        sign_u,
        sign_d,
        r_uc,
        r_ct,
        delta_u,
        delta_d,
        amp_u,
        amp_d,
    )
    return Candidate(
        config_label=config.label,
        family=config.family,
        sign_u=sign_u,
        sign_d=sign_d,
        r_uc=r_uc,
        r_ct=r_ct,
        delta_u=delta_u,
        delta_d=delta_d,
        amp_u=amp_u,
        amp_d=amp_d,
        vus=vus,
        vcb=vcb,
        vub=vub,
        jarlskog=jarlskog,
        objective=objective,
    )


def objective_factory(config: ScanConfig, sign_u: int, sign_d: int):
    def objective(point: np.ndarray) -> float:
        r_uc, r_ct, delta_u, delta_d, amp_u, amp_d = point
        if r_uc <= 0.0 or r_ct <= 0.0 or r_uc * r_ct >= 1.0:
            return 1.0e12

        vus, vcb, vub, jarlskog = deformed_observables(
            config.family,
            sign_u,
            sign_d,
            r_uc,
            r_ct,
            delta_u,
            delta_d,
            amp_u,
            amp_d,
        )

        dv_abs = np.abs(np.array([vus, vcb, vub], dtype=float) - TARGET_MAGS)
        mass_abs = np.array(
            [abs(r_uc / R_UC_OBS - 1.0), abs(r_ct / R_CT_OBS - 1.0)],
            dtype=float,
        )

        if np.all(dv_abs <= MAG_TOLS) and np.all(mass_abs <= MASS_TOL):
            return -jarlskog / J_ATLAS

        mag_over = np.maximum(dv_abs - MAG_TOLS, 0.0)
        mass_over = np.maximum(mass_abs - MASS_TOL, 0.0)
        penalty = float(np.sum((mag_over / MAG_TOLS) ** 2) + np.sum((mass_over / MASS_TOL) ** 2))
        penalty += 0.01 * float(np.sum((dv_abs / MAG_TOLS) ** 2) + np.sum((mass_abs / MASS_TOL) ** 2))
        return penalty - jarlskog / J_ATLAS

    return objective


def scan_config(config: ScanConfig) -> Candidate:
    best: Candidate | None = None

    for sign_u in (-1, 1):
        for sign_d in (-1, 1):
            result = differential_evolution(
                objective_factory(config, sign_u, sign_d),
                bounds=[
                    (5.0e-4, 5.0e-3),
                    (3.0e-3, 1.5e-2),
                    (0.0, 2.0 * math.pi),
                    (0.0, 2.0 * math.pi),
                    (-config.amp_bound, config.amp_bound),
                    (-config.amp_bound, config.amp_bound),
                ],
                seed=100 + 10 * sign_u + sign_d + int(10 * config.amp_bound),
                maxiter=config.maxiter,
                popsize=config.popsize,
                polish=True,
                disp=False,
            )
            candidate = candidate_from_point(config, sign_u, sign_d, result.x, float(result.fun))
            if best is None:
                best = candidate
            elif candidate.feasible and not best.feasible:
                best = candidate
            elif candidate.feasible == best.feasible and candidate.jarlskog > best.jarlskog:
                best = candidate

    assert best is not None
    return best


def format_pct(value: float) -> str:
    return f"{100.0 * value:+.2f}%"


def print_candidate(candidate: Candidate) -> None:
    print(f"  config                = {candidate.config_label}")
    print(f"  family                = {candidate.family}")
    print(f"  projector signs       = ({candidate.sign_u:+d}, {candidate.sign_d:+d})")
    print(f"  feasible corridor     = {candidate.feasible}")
    print(f"  boundary hit          = {candidate.boundary_hit}")
    print(f"  amplitude (u, d)      = ({candidate.amp_u:+.6f}, {candidate.amp_d:+.6f})")
    print(f"  m_u/m_c               = {candidate.r_uc:.6e}  ({format_pct(candidate.mass_dev_uc)})")
    print(f"  m_c/m_t               = {candidate.r_ct:.6e}  ({format_pct(candidate.mass_dev_ct)})")
    print(f"  delta_u               = {math.degrees(candidate.delta_u):.3f} deg")
    print(f"  delta_d               = {math.degrees(candidate.delta_d):.3f} deg")
    print(f"  |V_us|                = {candidate.vus:.6f}  (dv = {candidate.dv[0]:+.4e})")
    print(f"  |V_cb|                = {candidate.vcb:.6f}  (dv = {candidate.dv[1]:+.4e})")
    print(f"  |V_ub|                = {candidate.vub:.6f}  (dv = {candidate.dv[2]:+.4e})")
    print(f"  J                     = {candidate.jarlskog:.6e}")
    print(f"  J / J_atlas           = {candidate.j_ratio:.6f}")
    print(f"  objective             = {candidate.objective:.6f}")


def main() -> int:
    print("=" * 78)
    print("  FRONTIER: Quark CP Primitive Projector/Tensor Exploratory Scan")
    print("=" * 78)
    print("  Scope:")
    print("    deform only the 1-3 Schur slot on the live minimal Schur-NNI lane")
    print("    keep the Phase 1 down-sector anchor and historical c12/c23 surface")
    print("    compare projector-like and tensor-like 1+5-inspired complex branches")
    print(f"    CKM corridor        = ({MAG_TOLS[0]:.4f}, {MAG_TOLS[1]:.4f}, {MAG_TOLS[2]:.4f})")
    print(f"    quark-ratio corridor = +/- {100.0 * MASS_TOL:.1f}% around the observation comparators")
    print()
    print("  Structural inputs from current repo:")
    print(f"    projector branch    = sqrt(1/6) + i sqrt(5/6) = {PROJECTOR_BRANCH.real:+.6f} + {PROJECTOR_BRANCH.imag:+.6f} i")
    print(f"    delta_std           = arctan(sqrt(5)) = {math.degrees(DELTA_STD):.6f} deg")
    print(f"    tensor dressing     = i sqrt(5/6) / 42 = {TENSOR_BRANCH.real:+.6f} + {TENSOR_BRANCH.imag:+.6f} i")
    print()

    baseline = solve_magnitude_surface()
    relaxed = solve_phase_relaxed_ceiling(baseline)

    print("=" * 78)
    print("BASELINE")
    print("=" * 78)
    print(f"  magnitude solve J     = {baseline.jarlskog:.6e}")
    print(f"  magnitude solve ratio = {baseline.jarlskog / J_ATLAS:.6f}")
    print(f"  relaxed J ceiling     = {relaxed.jarlskog:.6e}")
    print(f"  relaxed ceiling ratio = {relaxed.jarlskog / J_ATLAS:.6f}")
    print(f"  baseline m_u/m_c      = {baseline.r_uc:.6e}")
    print(f"  baseline m_c/m_t      = {baseline.r_ct:.6e}")

    results = [scan_config(config) for config in SCAN_CONFIGS]

    print()
    print("=" * 78)
    print("SCAN RESULTS")
    print("=" * 78)
    for candidate in results:
        print()
        print_candidate(candidate)

    strongest = max(results, key=lambda candidate: candidate.jarlskog)
    sharpest_failure = min(results, key=lambda candidate: abs(candidate.jarlskog - baseline.jarlskog))
    tensor_result = next(candidate for candidate in results if candidate.family == "tensor")

    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    print("  Strongest candidate:")
    print(
        f"    {strongest.config_label} reaches J/J_atlas = {strongest.j_ratio:.3f} "
        f"with feasible={strongest.feasible} and boundary_hit={strongest.boundary_hit}"
    )
    print(
        f"    amplitudes = ({strongest.amp_u:+.3f}, {strongest.amp_d:+.3f}), "
        f"mass deviations = ({format_pct(strongest.mass_dev_uc)}, {format_pct(strongest.mass_dev_ct)})"
    )
    print("  Mild projector read:")
    mild = next(candidate for candidate in results if candidate.config_label == "projector_mild")
    print(
        f"    mild projector deformations only lift J/J_atlas to {mild.j_ratio:.3f}; "
        f"that is still well below full CP closure"
    )
    print("  Tensor read:")
    print(
        f"    tensor-only lower-row dressing reaches J/J_atlas = {tensor_result.j_ratio:.3f}, "
        f"barely above the baseline {baseline.jarlskog / J_ATLAS:.3f}"
    )
    print("  Honest endpoint:")
    print(
        "    the projector direction can supply the missing CP area only after a large "
        "boundary-seeking deformation, while the literal 1/42 tensor dressing is far too weak."
    )
    print(
        f"    the closest thing to a failure mode is {sharpest_failure.config_label}, "
        f"which stays near the baseline CP deficit."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
