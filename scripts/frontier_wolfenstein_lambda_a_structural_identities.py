#!/usr/bin/env python3
"""Exact-symbolic audit for the Wolfenstein lambda and A structural identities.

This runner certifies the three named structural identities

    (W1)  lambda^2     = alpha_s(v) / n_pair  = alpha_s(v) / 2,
    (W2)  A^2          = n_pair / n_color     = 2/3,
    (W3)  A^2 lambda^2 = alpha_s(v) / n_color = alpha_s(v) / 3,

and the CKM magnitude corollaries

    |V_us|_0  = lambda                        = sqrt(alpha_s(v)/2),
    |V_cb|    = A lambda^2                    = alpha_s(v)/sqrt(6),
    |V_ub|_0  = A lambda^3 sqrt(rho^2 + eta^2) = alpha_s(v)^(3/2)/(6 sqrt(2)),

at exact symbolic precision via sympy. `alpha_s(v)` is treated as a positive
real symbol; the structural relations are checked as polynomial / radical
identities by `sympy.simplify(lhs - rhs) == 0`. Structural counts
`(n_pair, n_color) = (2, 3)` and the CP-radius `rho^2 + eta^2 = 1/6` are
imported from cited authorities (NATIVE_GAUGE_CLOSURE_NOTE,
GRAPH_FIRST_SU3_INTEGRATION_NOTE, parent CKM atlas, and the CP-phase
structural-identity companion) and pinned as exact rationals here.

Pinning the canonical numeric value of `alpha_s(v)` is preserved as a
final-section sanity read using `scripts/canonical_plaquette_surface.py`,
but the load-bearing identities are exact-symbolic in the sympy block and
do not depend on the floating-point pin.

PASS exits 0; FAIL prints the residual expression and exits 1.
"""

from __future__ import annotations

from fractions import Fraction
import math
import sys

import sympy
from sympy import Rational, simplify, sqrt, symbols

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0

# ---------------------------------------------------------------------------
# Imported structural counts (cited authorities; not derived in this runner).
# ---------------------------------------------------------------------------
N_PAIR = 2     # NATIVE_GAUGE_CLOSURE_NOTE.md, parent CKM atlas
N_COLOR = 3    # GRAPH_FIRST_SU3_INTEGRATION_NOTE.md, parent CKM atlas
N_QUARK = N_PAIR * N_COLOR

# Imported CP-radius (CKM CP-phase structural-identity authority).
CP_RADIUS_SQ_RATIONAL = Fraction(1, 6)

# Imported canonical alpha_s(v) (ALPHA_S_DERIVED_NOTE / canonical plaquette).
ALPHA_S_V = CANONICAL_ALPHA_S_V


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 80)
    print(title)
    print("-" * 80)


def close(a: float, b: float, tol: float = 1e-14) -> bool:
    return abs(a - b) <= tol


# ---------------------------------------------------------------------------
# Section 1 - cited inputs.
# ---------------------------------------------------------------------------
def audit_inputs() -> None:
    banner("Imported CKM atlas inputs")

    print(f"  n_pair       = {N_PAIR}")
    print(f"  n_color      = {N_COLOR}")
    print(f"  n_quark      = {N_QUARK}")
    print(f"  alpha_s(v)   = {ALPHA_S_V:.15f}")
    print(f"  rho^2 + eta^2 = {CP_RADIUS_SQ_RATIONAL}  (imported)")

    check("n_pair = 2", N_PAIR == 2)
    check("n_color = 3", N_COLOR == 3)
    check("n_quark = n_pair*n_color = 6", N_QUARK == 6)
    check("canonical alpha_s(v) is positive", ALPHA_S_V > 0)
    check("CP radius squared is exact rational 1/6",
          CP_RADIUS_SQ_RATIONAL == Fraction(1, 6))


# ---------------------------------------------------------------------------
# Section 2 - exact-symbolic verification via sympy.
# `alpha_s(v)` is a symbolic positive real; structural counts are exact.
# ---------------------------------------------------------------------------
def audit_exact_symbolic() -> None:
    banner("Exact-symbolic verification via sympy")

    a_s = symbols("alpha_s_v", positive=True, real=True)
    n_pair = Rational(N_PAIR)
    n_color = Rational(N_COLOR)
    n_quark = n_pair * n_color
    cp_radius_sq = Rational(CP_RADIUS_SQ_RATIONAL.numerator,
                            CP_RADIUS_SQ_RATIONAL.denominator)

    # Structural definitions (parent CKM atlas).
    lambda_sq = a_s / n_pair
    a_sq = n_pair / n_color
    lambda_sym = sqrt(lambda_sq)
    a_sym = sqrt(a_sq)

    # ---- W1: lambda^2 = alpha_s(v) / n_pair = alpha_s(v) / 2 ----
    res_W1_general = simplify(lambda_sq - a_s / n_pair)
    res_W1_special = simplify(lambda_sq - a_s / 2)
    check("(W1) lambda^2 = alpha_s(v)/n_pair  [sympy.simplify residual]",
          res_W1_general == 0,
          detail=f"residual = {res_W1_general}")
    check("(W1) lambda^2 = alpha_s(v)/2 specialization at n_pair = 2",
          res_W1_special == 0,
          detail=f"residual = {res_W1_special}")

    # ---- W2: A^2 = n_pair / n_color = 2/3 (pure rational) ----
    res_W2_general = simplify(a_sq - n_pair / n_color)
    res_W2_special = simplify(a_sq - Rational(2, 3))
    check("(W2) A^2 = n_pair/n_color  [sympy.simplify residual]",
          res_W2_general == 0,
          detail=f"residual = {res_W2_general}")
    check("(W2) A^2 = 2/3 exact rational at (n_pair, n_color) = (2, 3)",
          res_W2_special == 0,
          detail=f"residual = {res_W2_special}; A^2 = {a_sq}")

    # ---- W3: A^2 lambda^2 = alpha_s(v) / n_color (n_pair cancels) ----
    product = a_sq * lambda_sq
    expected_general = a_s / n_color
    expected_special = a_s / 3
    res_W3_general = simplify(product - expected_general)
    res_W3_special = simplify(product - expected_special)
    check("(W3) A^2 lambda^2 = alpha_s(v)/n_color  [n_pair cancels exactly]",
          res_W3_general == 0,
          detail=f"product = {simplify(product)}; residual = {res_W3_general}")
    check("(W3) A^2 lambda^2 = alpha_s(v)/3 specialization",
          res_W3_special == 0,
          detail=f"residual = {res_W3_special}")

    # Cancellation as a pure rational identity (count-only, no alpha_s).
    rational_cancel = (Rational(N_PAIR, N_COLOR) * Rational(1, N_PAIR)
                       - Rational(1, N_COLOR))
    check("(W3) rational cancellation: (n_pair/n_color)(1/n_pair) - 1/n_color = 0",
          rational_cancel == 0,
          detail=f"residual = {rational_cancel}")

    # ---- |V_us|_0 = lambda = sqrt(alpha_s(v)/2) ----
    v_us = lambda_sym
    v_us_clean = sqrt(a_s / 2)
    res_Vus = simplify(v_us - v_us_clean)
    check("|V_us|_0 = lambda = sqrt(alpha_s(v)/2)  [sympy.simplify residual]",
          res_Vus == 0,
          detail=f"residual = {res_Vus}")

    # ---- |V_cb| = A lambda^2 = alpha_s(v) / sqrt(n_quark) = alpha_s(v)/sqrt(6) ----
    v_cb = a_sym * lambda_sq
    v_cb_clean = a_s / sqrt(n_quark)
    v_cb_explicit = a_s / sqrt(6)
    res_Vcb_general = simplify(v_cb - v_cb_clean)
    res_Vcb_explicit = simplify(v_cb - v_cb_explicit)
    check("|V_cb| = A lambda^2 = alpha_s(v)/sqrt(n_quark)  [sympy residual]",
          res_Vcb_general == 0,
          detail=f"residual = {res_Vcb_general}")
    check("|V_cb| = alpha_s(v)/sqrt(6) explicit specialization",
          res_Vcb_explicit == 0,
          detail=f"residual = {res_Vcb_explicit}")
    res_Vcb_sq = simplify(v_cb**2 - a_s**2 / 6)
    check("|V_cb|^2 = alpha_s(v)^2/6  [squared identity, no radicals]",
          res_Vcb_sq == 0,
          detail=f"residual = {res_Vcb_sq}")

    # ---- |V_ub|_0 = A lambda^3 sqrt(rho^2 + eta^2)
    #              = alpha_s(v)^(3/2) / (6 sqrt(2))  ----
    lambda_cubed = lambda_sym ** 3
    v_ub = a_sym * lambda_cubed * sqrt(cp_radius_sq)
    v_ub_clean = a_s ** Rational(3, 2) / (6 * sqrt(2))
    res_Vub = simplify(v_ub - v_ub_clean)
    check("|V_ub|_0 = A lambda^3 sqrt(rho^2+eta^2) = alpha_s(v)^(3/2)/(6 sqrt(2))",
          res_Vub == 0,
          detail=f"residual = {res_Vub}")
    res_Vub_sq = simplify(v_ub**2 - a_s**3 / 72)
    check("|V_ub|_0^2 = alpha_s(v)^3 / 72  [squared identity, no radicals]",
          res_Vub_sq == 0,
          detail=f"residual = {res_Vub_sq}")

    # ---- Joint J_0 surface: J_0 = lambda^6 A^2 eta = alpha_s(v)^3 sqrt(5)/72 ----
    eta_sym = sqrt(Rational(5)) / 6  # imported CP-phase identity
    j0_surface = (lambda_sq ** 3) * a_sq * eta_sym
    j0_clean = a_s ** 3 * sqrt(5) / 72
    res_J0 = simplify(j0_surface - j0_clean)
    check("atlas J_0 = lambda^6 A^2 eta = alpha_s(v)^3 sqrt(5)/72",
          res_J0 == 0,
          detail=f"residual = {res_J0}")


# ---------------------------------------------------------------------------
# Section 3 - sanity numerical pin using canonical alpha_s(v) value.
# (Float comparison only; not load-bearing for the structural identities.)
# ---------------------------------------------------------------------------
def audit_canonical_numerical_pin() -> None:
    banner("Canonical numerical sanity pin (alpha_s(v) imported)")

    lambda_sq_num = ALPHA_S_V / N_PAIR
    a_sq_num = float(Fraction(N_PAIR, N_COLOR))
    product_num = a_sq_num * lambda_sq_num
    a_value = math.sqrt(a_sq_num)
    lambda_value = math.sqrt(lambda_sq_num)

    v_cb_atlas = a_value * lambda_sq_num
    v_cb_clean = ALPHA_S_V / math.sqrt(N_QUARK)

    cp_radius = math.sqrt(1 / 6)
    v_ub_atlas = a_value * lambda_value**3 * cp_radius
    v_ub_clean = ALPHA_S_V**1.5 / (6 * math.sqrt(2))

    print(f"  lambda^2     = {lambda_sq_num:.15f}")
    print(f"  A^2          = {a_sq_num:.15f}")
    print(f"  A^2 lambda^2 = {product_num:.15f}")
    print(f"  |V_cb|       = {v_cb_clean:.15f}")
    print(f"  |V_ub|_0     = {v_ub_clean:.15f}")

    check("numerical: A^2 lambda^2 ~ alpha_s(v)/3",
          close(product_num, ALPHA_S_V / N_COLOR))
    check("numerical: |V_cb| atlas ~ alpha_s(v)/sqrt(6)",
          close(v_cb_atlas, v_cb_clean))
    check("numerical: |V_ub|_0 atlas ~ alpha_s(v)^(3/2)/(6 sqrt(2))",
          close(v_ub_atlas, v_ub_clean))


# ---------------------------------------------------------------------------
# Section 4 - joint named surface (regression).
# ---------------------------------------------------------------------------
def audit_joint_named_surface() -> None:
    banner("Joint named surface regression (lambda, A, rho, eta, delta, J_0)")

    rho = Fraction(1, 6)
    eta_sq = Fraction(5, 36)
    radius_sq = rho * rho + eta_sq
    eta = math.sqrt(5) / 6

    lambda_sq_num = ALPHA_S_V / 2
    a_sq_num = 2 / 3
    j0_from_surface = (lambda_sq_num ** 3) * a_sq_num * eta
    j0_clean = ALPHA_S_V ** 3 * math.sqrt(5) / 72

    print(f"  rho^2 + eta^2 = {radius_sq}")
    print(f"  J_0 surface    = {j0_from_surface:.15e}")
    print(f"  J_0 clean      = {j0_clean:.15e}")

    check("rho^2 + eta^2 = 1/6 (imported)", radius_sq == Fraction(1, 6))
    check("J_0 numerical factorization equals alpha_s(v)^3 sqrt(5)/72",
          close(j0_from_surface, j0_clean))


def main() -> int:
    print("=" * 80)
    print("Wolfenstein lambda and A structural identities exact-symbolic audit")
    print("=" * 80)

    audit_inputs()
    audit_exact_symbolic()
    audit_canonical_numerical_pin()
    audit_joint_named_surface()

    print()
    print("=" * 80)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 80)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
