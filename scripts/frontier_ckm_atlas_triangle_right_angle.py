#!/usr/bin/env python3
"""
CKM atlas triangle right-angle identity verification.

Verifies the cited atlas/Wolfenstein triangle identities in
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
import sympy as sp

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
    banner("Part 0: cited CKM atlas inputs")
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
        "gamma_0 equals cited delta_CKM",
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
    banner("Part 2: area reproduces cited atlas-Jarlskog factorisation")
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
        "exact barred alpha is not claimed as exactly 90 degrees",
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


def part4_exact_symbolic() -> None:
    """Exact-symbolic right-angle proof in sympy.

    Inputs (imported from the upstream CKM CP-phase structural-identity
    theorem): rho = 1/6, eta = sqrt(5)/6, exact rationals/surds.

    Claim: at the apex vertex V_C = (rho, eta) of the rescaled atlas triangle
    with vertices V_A = (0, 0), V_B = (1, 0), V_C = (rho, eta), the interior
    angle alpha_0 satisfies cos(alpha_0) = 0 exactly, hence alpha_0 = pi/2.

    Proof: form the two edge vectors emanating from V_C:
        u = V_A - V_C = (-rho, -eta),
        w = V_B - V_C = (1 - rho, -eta).
    Their dot product is
        u . w = -rho (1 - rho) + eta^2.
    Substituting eta^2 = 5/36 and rho (1 - rho) = (1/6)(5/6) = 5/36 gives
        u . w = -5/36 + 5/36 = 0
    exactly in QQ.  The norms |u|, |w| are positive surds, so
        cos(alpha_0) = (u . w) / (|u| |w|) = 0
    and alpha_0 = pi/2 exactly.

    Equivalent geometric reading: the identity eta^2 = rho (1 - rho) places
    V_C on the Thales circle with diameter V_A V_B, and Thales' theorem then
    gives angle(V_A V_C V_B) = pi/2.

    The runner also performs the same proof in the standard unitarity-triangle
    apex form, where the apex coordinate is the complex ratio
        z = -(V_ud V_ub^*) / (V_cd V_cb^*).
    On the rescaled atlas the leading apex is z = rho + i eta = 1/6 + i sqrt(5)/6.
    The angle alpha is the argument of (z - 1) / (-z) = (1 - z) / z, and
        cos(alpha) = Re((1 - z)/|1 - z| * conj(z)/|z|)
                   = (rho (1 - rho) - eta^2) / (|z||1 - z|)  (sign convention),
    which sympy.simplify reduces to 0 with the same identity.
    """
    banner("Part 4: exact-symbolic sympy proof of cos(alpha_0) = 0")

    # Exact symbolic inputs imported from the upstream CKM CP-phase
    # structural-identity theorem.  These are not floats: sympy treats them
    # as exact rationals/surds, and every algebraic step that follows is
    # carried out in exact arithmetic.
    rho_s = sp.Rational(1, 6)
    eta_s = sp.sqrt(sp.Rational(5, 36))

    print(f"  Symbolic inputs: rho = {rho_s}, eta = {sp.nsimplify(eta_s)}")
    check(
        "sympy: rho = 1/6 (exact)",
        rho_s == sp.Rational(1, 6),
        f"rho = {rho_s}",
    )
    check(
        "sympy: eta^2 = 5/36 (exact)",
        sp.simplify(eta_s ** 2 - sp.Rational(5, 36)) == 0,
        f"eta^2 = {sp.simplify(eta_s ** 2)}",
    )
    check(
        "sympy: rho^2 + eta^2 = 1/6 (atlas-leading CP radius squared)",
        sp.simplify(rho_s ** 2 + eta_s ** 2 - sp.Rational(1, 6)) == 0,
    )

    # ---- (a) Rescaled atlas triangle, dot-product form -------------------
    # Vertices V_A = (0, 0), V_B = (1, 0), V_C = (rho, eta).
    # Edge vectors emanating from the apex V_C.
    u_x = sp.Integer(0) - rho_s
    u_y = sp.Integer(0) - eta_s
    w_x = sp.Integer(1) - rho_s
    w_y = sp.Integer(0) - eta_s

    dot_uw = sp.expand(u_x * w_x + u_y * w_y)
    dot_uw_simplified = sp.simplify(dot_uw)

    print(f"  u = V_A - V_C = (-rho, -eta) = ({u_x}, {-eta_s})")
    print(f"  w = V_B - V_C = (1 - rho, -eta) = ({w_x}, {-eta_s})")
    print(f"  u . w = -rho(1 - rho) + eta^2")
    print(f"        = {sp.expand(-rho_s * (1 - rho_s) + eta_s ** 2)}")
    print(f"  sympy.simplify(u . w) = {dot_uw_simplified}")

    check(
        "sympy: u . w = 0 exactly (apex dot product vanishes)",
        dot_uw_simplified == 0,
        f"u . w = {dot_uw_simplified}",
    )

    norm_u = sp.simplify(sp.sqrt(u_x ** 2 + u_y ** 2))
    norm_w = sp.simplify(sp.sqrt(w_x ** 2 + w_y ** 2))
    check(
        "sympy: |u| > 0",
        sp.simplify(norm_u - sp.sqrt(sp.Rational(1, 6))) == 0,
        f"|u| = sqrt(rho^2 + eta^2) = {norm_u}",
    )
    check(
        "sympy: |w| > 0",
        sp.simplify(norm_w - sp.sqrt(sp.Rational(5, 6))) == 0,
        f"|w| = sqrt((1-rho)^2 + eta^2) = {norm_w}",
    )

    cos_alpha = sp.simplify(dot_uw_simplified / (norm_u * norm_w))
    check(
        "sympy: cos(alpha_0) = 0 exactly",
        cos_alpha == 0,
        f"cos(alpha_0) = {cos_alpha}",
    )

    alpha_atan2 = sp.atan2(
        sp.simplify(u_x * w_y - u_y * w_x),
        sp.simplify(u_x * w_x + u_y * w_y),
    )
    alpha_simplified = sp.simplify(alpha_atan2)
    check(
        "sympy: atan2(|u x w|, u . w) = +/- pi/2 exactly",
        sp.simplify(sp.Abs(alpha_simplified) - sp.pi / 2) == 0,
        f"atan2(...) = {alpha_simplified}",
    )

    # ---- (b) Unitarity-triangle apex form --------------------------------
    # On the rescaled atlas surface the apex is z = rho + i eta.  The
    # interior angle at the apex is arg((1 - z)/(-z)) = arg(-(1 - z)/z),
    # which equals arg((1 - z) * conj(-z)) mod 2*pi (numerator argument
    # after multiplying by a positive real |z|^2/|z|^2).  We compute
    # Re((1 - z) * conj(-z)) and verify it vanishes exactly.
    z = rho_s + sp.I * eta_s
    apex_numerator = sp.expand((1 - z) * sp.conjugate(-z))
    re_part = sp.simplify(sp.re(apex_numerator))
    im_part = sp.simplify(sp.im(apex_numerator))

    print(f"  Apex form: z = rho + i*eta = {z}")
    print(f"  (1 - z) * conj(-z) = {sp.simplify(apex_numerator)}")
    print(f"  Re((1 - z) conj(-z)) = -rho(1 - rho) + eta^2 = {re_part}")
    print(f"  Im((1 - z) conj(-z)) = +eta = {im_part}")

    check(
        "sympy: Re((1 - z) conj(-z)) = 0 exactly (apex right angle)",
        re_part == 0,
        f"Re = {re_part}",
    )
    check(
        "sympy: Im((1 - z) conj(-z)) = +eta != 0 (angle is +pi/2, not 0/pi)",
        sp.simplify(im_part - eta_s) == 0,
        f"Im = {im_part}",
    )
    check(
        "sympy: arg((1 - z) conj(-z)) = pi/2 (Re=0, Im>0)",
        sp.simplify(sp.atan2(im_part, re_part) - sp.pi / 2) == 0,
    )

    # ---- (c) Thales-circle algebraic identity ----------------------------
    thales_residue = sp.simplify(eta_s ** 2 - rho_s * (1 - rho_s))
    check(
        "sympy: Thales identity eta^2 - rho(1 - rho) = 0 exactly",
        thales_residue == 0,
        f"eta^2 - rho(1 - rho) = {thales_residue}",
    )

    # ---- (d) Beta_0 + gamma_0 = pi/2 exactly via arctan addition --------
    # gamma_0 = arctan(eta/rho) = arctan(sqrt(5)),
    # beta_0  = arctan(eta/(1 - rho)) = arctan(1/sqrt(5)).
    # arctan(x) + arctan(1/x) = pi/2 for x > 0.
    # sympy does not auto-fold atan(x)+atan(1/x) -> pi/2, so we certify the
    # sum via cos(g+b) and sin(g+b) using the addition formulas, which sympy
    # does simplify cleanly.
    gamma_0_sym = sp.atan(eta_s / rho_s)
    beta_0_sym = sp.atan(eta_s / (1 - rho_s))

    cos_sum = sp.simplify(
        sp.cos(gamma_0_sym) * sp.cos(beta_0_sym)
        - sp.sin(gamma_0_sym) * sp.sin(beta_0_sym)
    )
    sin_sum = sp.simplify(
        sp.sin(gamma_0_sym) * sp.cos(beta_0_sym)
        + sp.cos(gamma_0_sym) * sp.sin(beta_0_sym)
    )

    check(
        "sympy: tan(gamma_0) = sqrt(5) (exact surd)",
        sp.simplify(sp.tan(gamma_0_sym) - sp.sqrt(5)) == 0,
    )
    check(
        "sympy: tan(beta_0) = 1/sqrt(5) (exact surd)",
        sp.simplify(sp.tan(beta_0_sym) - 1 / sp.sqrt(5)) == 0,
    )
    check(
        "sympy: tan(gamma_0) * tan(beta_0) = 1 exactly",
        sp.simplify(sp.tan(gamma_0_sym) * sp.tan(beta_0_sym) - 1) == 0,
    )
    check(
        "sympy: cos(beta_0 + gamma_0) = 0 exactly (addition formula)",
        cos_sum == 0,
        f"cos(b+g) = {cos_sum}",
    )
    check(
        "sympy: sin(beta_0 + gamma_0) = 1 exactly (addition formula)",
        sin_sum == 1,
        f"sin(b+g) = {sin_sum}",
    )
    # cos(beta_0 + gamma_0) = 0 and sin(beta_0 + gamma_0) = 1, with both
    # angles in (0, pi/2), forces beta_0 + gamma_0 = pi/2 (unique solution
    # in (0, pi)).  Hence alpha_0 = pi - (beta_0 + gamma_0) = pi/2 exactly.
    check(
        "sympy: alpha_0 = pi/2 exactly (from cos=0 + sin=1, sum in (0,pi))",
        cos_sum == 0 and sin_sum == 1,
    )

    # ---- (e) Area certificate -------------------------------------------
    # Area_0 = (1/2) |det([V_B - V_A; V_C - V_A])| = (1/2) eta = sqrt(5)/12.
    area_sym = sp.Rational(1, 2) * sp.Abs(
        sp.Matrix([[1 - 0, 0 - 0], [rho_s - 0, eta_s - 0]]).det()
    )
    area_target = sp.sqrt(5) / 12
    check(
        "sympy: Area_0 = sqrt(5)/12 exactly",
        sp.simplify(area_sym - area_target) == 0,
        f"Area_0 = {sp.simplify(area_sym)}",
    )


def main() -> int:
    print("=" * 88)
    print("CKM atlas triangle right-angle identity verification")
    print("=" * 88)
    part0_inputs()
    part1_atlas_triangle()
    part2_area_jarlskog()
    part3_barred_triangle_guardrail()
    part4_exact_symbolic()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    if FAIL_COUNT == 0:
        print(f"PASSED: {PASS_COUNT}/{PASS_COUNT}")
        print("CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_ATLAS_IDENTITY_PASS=TRUE")
        print("CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_EXACT_SYMBOLIC_PASS=TRUE")
        print("BARRED_UNITARITY_TRIANGLE_EXACT_RIGHT_ANGLE_CLAIMED=FALSE")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
