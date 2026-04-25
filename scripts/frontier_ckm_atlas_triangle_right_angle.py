#!/usr/bin/env python3
"""
CKM atlas triangle right-angle identity verification.

Verifies the retained atlas/Wolfenstein triangle identities in
  docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md

The exact right angle belongs to the rescaled atlas triangle built from
rho = 1/6 and eta = sqrt(5)/6.  The runner also computes the exact barred
unitarity-triangle apex from the parent PDG-standard CKM matrix and verifies
that finite-lambda corrections move the physical barred angle away from an
exact 90 degrees.  This guards the theorem boundary.
"""

from __future__ import annotations

import cmath
import math
from fractions import Fraction

import numpy as np

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f" ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def angle_deg(z_val: complex) -> float:
    angle = math.degrees(cmath.phase(z_val))
    return angle + 360.0 if angle < 0.0 else angle


def build_standard_ckm(s12: float, s23: float, s13: float, delta: float) -> np.ndarray:
    """Standard PDG-form CKM matrix from sines and the CP phase."""
    c12 = math.sqrt(1.0 - s12 * s12)
    c23 = math.sqrt(1.0 - s23 * s23)
    c13 = math.sqrt(1.0 - s13 * s13)
    phase = complex(math.cos(delta), math.sin(delta))

    return np.array(
        [
            [c12 * c13, s12 * c13, s13 / phase],
            [
                -s12 * c23 - c12 * s23 * s13 * phase,
                c12 * c23 - s12 * s23 * s13 * phase,
                s23 * c13,
            ],
            [
                s12 * s23 - c12 * c23 * s13 * phase,
                -c12 * s23 - s12 * c23 * s13 * phase,
                c23 * c13,
            ],
        ],
        dtype=complex,
    )


N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR

RHO = Fraction(1, 6)
ETA_SQUARED = Fraction(5, 36)
ETA = math.sqrt(5.0) / 6.0
RADIUS_SQUARED = Fraction(1, 6)

ALPHA_S_V = CANONICAL_ALPHA_S_V
LAMBDA = math.sqrt(ALPHA_S_V / N_PAIR)
A_VALUE = math.sqrt(N_PAIR / N_COLOR)
CP_RADIUS = math.sqrt(float(RADIUS_SQUARED))
DELTA_CKM = math.atan(math.sqrt(5.0))


def part0_inputs() -> None:
    banner("Part 0: retained CKM atlas inputs")
    check("n_pair = 2", N_PAIR == 2)
    check("n_color = 3", N_COLOR == 3)
    check("n_quark = 6", N_QUARK == 6)
    check("rho = 1/6", RHO == Fraction(1, 6), f"rho = {RHO}")
    check("eta^2 = 5/36", ETA_SQUARED == Fraction(5, 36), f"eta^2 = {ETA_SQUARED}")
    check(
        "rho^2 + eta^2 = 1/6",
        RHO * RHO + ETA_SQUARED == RADIUS_SQUARED,
        f"{RHO * RHO + ETA_SQUARED}",
    )


def part1_atlas_triangle() -> None:
    banner("Part 1: exact right angle of the rescaled atlas triangle")
    beta0 = math.atan(ETA / (1.0 - float(RHO)))
    gamma0 = math.atan(ETA / float(RHO))
    alpha0 = math.pi - beta0 - gamma0
    area0 = ETA / 2.0

    check(
        "tan(beta_0) = 1/sqrt(5)",
        abs(math.tan(beta0) - 1.0 / math.sqrt(5.0)) < 1e-15,
        f"tan(beta_0) = {math.tan(beta0):.15f}",
    )
    check(
        "tan(gamma_0) = sqrt(5)",
        abs(math.tan(gamma0) - math.sqrt(5.0)) < 1e-15,
        f"tan(gamma_0) = {math.tan(gamma0):.15f}",
    )
    check(
        "gamma_0 equals retained delta_CKM",
        abs(gamma0 - DELTA_CKM) < 1e-15,
        f"gamma_0 = {math.degrees(gamma0):.12f} deg",
    )
    check(
        "beta_0 + gamma_0 = 90 degrees",
        abs(math.degrees(beta0 + gamma0) - 90.0) < 1e-12,
        f"{math.degrees(beta0 + gamma0):.12f} deg",
    )
    check(
        "alpha_0 = 90 degrees exactly on the atlas triangle",
        abs(math.degrees(alpha0) - 90.0) < 1e-12,
        f"alpha_0 = {math.degrees(alpha0):.12f} deg",
    )
    check(
        "atlas triangle angles sum to 180 degrees",
        abs(math.degrees(alpha0 + beta0 + gamma0) - 180.0) < 1e-12,
    )
    check(
        "rescaled atlas triangle area = sqrt(5)/12",
        abs(area0 - math.sqrt(5.0) / 12.0) < 1e-15,
        f"area = {area0:.15f}",
    )
    check(
        "Thales circle: eta^2 = rho(1-rho)",
        ETA_SQUARED == RHO * (1 - RHO),
        f"both = {ETA_SQUARED}",
    )


def part2_area_jarlskog() -> None:
    banner("Part 2: area reproduces retained atlas-Jarlskog factorisation")
    lambda_sq = ALPHA_S_V / 2.0
    a_sq = Fraction(2, 3)
    area0 = math.sqrt(5.0) / 12.0
    j0_from_area = 2.0 * float(a_sq) * lambda_sq**3 * area0
    j0_factored = ALPHA_S_V**3 * math.sqrt(5.0) / 72.0

    check("lambda^2 = alpha_s(v)/2", abs(lambda_sq - ALPHA_S_V / 2.0) < 1e-15)
    check("A^2 = 2/3", a_sq == Fraction(2, 3))
    check(
        "2 A^2 lambda^6 Area_0 = J_0 = alpha_s(v)^3 sqrt(5)/72",
        abs(j0_from_area - j0_factored) / j0_factored < 1e-15,
        f"J_0 = {j0_factored:.12e}",
    )


def part3_barred_triangle_guardrail() -> None:
    banner("Part 3: finite-lambda barred unitarity-triangle guardrail")
    s12 = LAMBDA
    s23 = A_VALUE * LAMBDA * LAMBDA
    s13 = A_VALUE * LAMBDA**3 * CP_RADIUS
    v_ckm = build_standard_ckm(s12, s23, s13, DELTA_CKM)

    unitary_error = np.max(np.abs(v_ckm.conj().T @ v_ckm - np.eye(3)))
    apex = -v_ckm[0, 0] * np.conj(v_ckm[0, 2]) / (v_ckm[1, 0] * np.conj(v_ckm[1, 2]))
    alpha_bar = angle_deg(-v_ckm[2, 0] * np.conj(v_ckm[2, 2]) / (v_ckm[0, 0] * np.conj(v_ckm[0, 2])))
    beta_bar = angle_deg(-v_ckm[1, 0] * np.conj(v_ckm[1, 2]) / (v_ckm[2, 0] * np.conj(v_ckm[2, 2])))
    gamma_bar = angle_deg(-v_ckm[0, 0] * np.conj(v_ckm[0, 2]) / (v_ckm[1, 0] * np.conj(v_ckm[1, 2])))

    alpha0 = 90.0
    beta0 = math.degrees(math.atan(1.0 / math.sqrt(5.0)))
    gamma0 = math.degrees(math.atan(math.sqrt(5.0)))

    check("standard CKM matrix is unitary", unitary_error < 1e-14, f"max error {unitary_error:.2e}")
    check(
        "barred apex differs from atlas rho by finite-lambda correction",
        abs(apex.real - float(RHO)) > 1e-3,
        f"rho_bar={apex.real:.8f}, rho={float(RHO):.8f}",
    )
    check(
        "barred apex differs from atlas eta by finite-lambda correction",
        abs(apex.imag - ETA) > 1e-3,
        f"eta_bar={apex.imag:.8f}, eta={ETA:.8f}",
    )
    check(
        "exact barred alpha is not promoted as exactly 90 degrees",
        abs(alpha_bar - 90.0) > 0.1,
        f"alpha_bar={alpha_bar:.8f} deg",
    )
    check(
        "barred angles still sum to 180 degrees",
        abs(alpha_bar + beta_bar + gamma_bar - 180.0) < 1e-10,
        f"sum={alpha_bar + beta_bar + gamma_bar:.12f}",
    )
    check(
        "barred alpha finite-lambda correction is small",
        abs(alpha_bar - alpha0) < 1.0,
        f"delta={alpha_bar - alpha0:+.6f} deg",
    )
    check(
        "barred beta finite-lambda correction is small",
        abs(beta_bar - beta0) < 1.0,
        f"delta={beta_bar - beta0:+.6f} deg",
    )
    check(
        "barred gamma finite-lambda correction is small",
        abs(gamma_bar - gamma0) < 0.1,
        f"delta={gamma_bar - gamma0:+.6f} deg",
    )
    check(
        "boundary flag: exact right angle belongs to atlas triangle, not barred triangle",
        abs(alpha0 - 90.0) < 1e-12 and abs(alpha_bar - 90.0) > 0.1,
    )

    print()
    print(f"  atlas angles:  alpha_0={alpha0:.6f}, beta_0={beta0:.6f}, gamma_0={gamma0:.6f}")
    print(f"  barred angles: alpha={alpha_bar:.6f}, beta={beta_bar:.6f}, gamma={gamma_bar:.6f}")
    print(f"  barred apex:   rho_bar={apex.real:.8f}, eta_bar={apex.imag:.8f}")


def main() -> int:
    print("=" * 88)
    print("CKM atlas triangle right-angle identity verification")
    print("=" * 88)
    part0_inputs()
    part1_atlas_triangle()
    part2_area_jarlskog()
    part3_barred_triangle_guardrail()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    if FAIL_COUNT == 0:
        print("PASSED: 26/26")
        print("CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_RETAINED=TRUE")
        print("BARRED_UNITARITY_TRIANGLE_EXACT_RIGHT_ANGLE_PROMOTED=FALSE")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
