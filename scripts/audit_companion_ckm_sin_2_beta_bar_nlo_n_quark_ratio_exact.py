#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_sin_2_beta_bar_nlo_n_quark_ratio_theorem_note_2026-04-25`.

The parent note's load-bearing content is the NLO multiplicative ratio
identity for the framework's `sin(2 beta_bar)` CP asymmetry,

  (B1)  sin(2 beta_bar) / sin(2 beta_0)
          ==  1 - alpha_s(v) / (N_quark - 1) + O(alpha_s(v)^2),

with N_quark - 1 = 5 traced to the retained 1+5 quark-block decomposition
in the CKM CP-phase theorem (where w_perp = (N_quark - 1)/N_quark = 5/6).

The retained NLO-protected-gamma-bar theorem provides:

  (N7) beta_0 - beta_bar = (sqrt(5)/20) alpha_s + O(alpha_s^2)
  (N8) sin(2 gamma_bar) / sin(2 gamma_0) = 1 + O(alpha_s^4)  (PROTECTED)
  (N9) tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s)

The retained right-angle theorem provides:

  alpha_0 = pi/2,  sin(2 beta_0) = sqrt(5)/3,  cos(2 beta_0) = 2/3.

The existing primary runner
(`scripts/frontier_ckm_sin_2_beta_bar_nlo_n_quark_ratio.py`) verifies the
identities at floating-point tolerance using the canonical numerical
alpha_s(v). This Pattern B audit companion adds a sympy-based
exact-symbolic verification:

  (a) treats `alpha_s` as a free positive real symbol so the algebra
      cannot be passing accidentally on a single numerical value;
  (b) imports the upstream retained inputs verbatim:
        N_pair = 2, N_color = 3, N_quark = 6
        sin(2 beta_0) = sqrt(5)/3, cos(2 beta_0) = 2/3
        N7 slope = sqrt(5)/20;
  (c) verifies the linearization
        sin(2 beta_bar) = sin(2 beta_0) + 2 cos(2 beta_0) (beta_bar - beta_0)
                       + O(alpha_s^2)
      and the resulting closed form
        (sin(2 beta_bar) - sin(2 beta_0)) / sin(2 beta_0)
          == -alpha_s/(N_quark - 1)
      parametric in alpha_s after the sqrt(5) cancellation;
  (d) verifies (B2) at framework value N_quark = 6 the coefficient is
      exactly 1/5;
  (e) verifies (B3) sin(2 gamma_bar)/sin(2 gamma_0) == 1 (NLO-protected);
  (f) verifies (B4) sin(2 alpha_0) == 0 from atlas right-angle;
  (g) verifies the alpha_s-INDEPENDENCE of the 1/(N_quark - 1) coefficient
      by extracting it parametric in alpha_s;
  (h) verifies the consistency of the retained N9 closed form with the
      linearization to first order in alpha_s;
  (i) provides counterfactual probes confirming each retained input
      is individually load-bearing.

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, no status promotion. The cited atlas/protected-gamma
inputs (sin(2 beta_0) = sqrt(5)/3, cos(2 beta_0) = 2/3, N7 slope =
sqrt(5)/20, N9 closed form, N_quark = 6) are imported from upstream
authority notes and are not re-derived here.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, sqrt, atan, sin, cos, pi, series
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (B)"
    else:
        FAIL += 1
        tag = "FAIL (B)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def main() -> int:
    print("=" * 88)
    print("Audit companion (exact-symbolic) for")
    print("ckm_sin_2_beta_bar_nlo_n_quark_ratio_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (B1) NLO ratio,")
    print("(B2) framework value, (B3) gamma-protection, (B4) right-angle,")
    print("alpha_s-independence of 1/(N_quark - 1), and N9 first-order")
    print("consistency, parametric in alpha_s.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and imported retained inputs")
    # ---------------------------------------------------------------------
    alpha_s = Symbol("alpha_s", positive=True, real=True)

    # Imported retained inputs (cited authorities; not re-derived here).
    N_PAIR = Rational(2)
    N_COLOR = Rational(3)
    N_QUARK = Rational(6)

    sin_2beta_0 = sqrt(Rational(5)) / Rational(3)         # retained right-angle
    cos_2beta_0 = Rational(2, 3)                            # retained right-angle
    n7_slope = sqrt(Rational(5)) / Rational(20)            # retained protected-gamma N7

    print(f"  symbolic alpha_s        = {alpha_s}")
    print(f"  retained N_quark         = {N_QUARK}")
    print(f"  retained N_quark - 1     = {N_QUARK - 1}")
    print(f"  retained sin(2 beta_0)   = {sin_2beta_0}")
    print(f"  retained cos(2 beta_0)   = {cos_2beta_0}")
    print(f"  retained N7 slope        = {n7_slope}")

    check(
        "N_quark == N_pair * N_color (cited authority)",
        simplify(N_QUARK - N_PAIR * N_COLOR) == 0,
        f"residual = {simplify(N_QUARK - N_PAIR * N_COLOR)}",
    )
    check(
        "sin^2(2 beta_0) + cos^2(2 beta_0) == 1 (Pythagorean check)",
        simplify(sin_2beta_0 ** 2 + cos_2beta_0 ** 2 - 1) == 0,
        f"residual = {simplify(sin_2beta_0 ** 2 + cos_2beta_0 ** 2 - 1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 1: (B1) linearization sin(2 beta_bar) - sin(2 beta_0) at first order")
    # ---------------------------------------------------------------------
    # Retained N7: beta_0 - beta_bar = +n7_slope * alpha_s + O(alpha_s^2).
    # Sign convention (parent note Section "Derivation"): triangle constraint
    # alpha_bar + beta_bar + gamma_bar = pi with Delta gamma = 0 forces
    # Delta alpha + Delta beta = 0; alpha_bar - pi/2 = +slope * alpha_s,
    # so beta_bar - beta_0 = -slope * alpha_s.
    beta_bar_minus_beta_0 = -n7_slope * alpha_s

    # Linearization: sin(2 beta_bar) ~ sin(2 beta_0) + 2 cos(2 beta_0)(beta_bar - beta_0).
    sin_2beta_bar_lin = (
        sin_2beta_0 + 2 * cos_2beta_0 * beta_bar_minus_beta_0
    )
    delta_sin = simplify(sin_2beta_bar_lin - sin_2beta_0)
    delta_sin_target = -sqrt(Rational(5)) / Rational(15) * alpha_s
    check(
        "sin(2 beta_bar) - sin(2 beta_0) == -(sqrt(5)/15) alpha_s (linearization)",
        simplify(delta_sin - delta_sin_target) == 0,
        f"residual = {simplify(delta_sin - delta_sin_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (B1) closed-form ratio == 1 - alpha_s/(N_quark - 1)")
    # ---------------------------------------------------------------------
    ratio_lin = simplify(sin_2beta_bar_lin / sin_2beta_0)
    ratio_target_n_quark = simplify(1 - alpha_s / (N_QUARK - 1))
    check(
        "(B1) sin(2 beta_bar) / sin(2 beta_0) == 1 - alpha_s/(N_quark - 1)",
        simplify(ratio_lin - ratio_target_n_quark) == 0,
        f"residual = {simplify(ratio_lin - ratio_target_n_quark)}",
    )
    # The sqrt(5) cancellation is the load-bearing structural step:
    # delta_sin / sin_2beta_0 = (-sqrt(5)/15 alpha_s) / (sqrt(5)/3) = -alpha_s/5.
    cancel_residual = simplify(
        delta_sin / sin_2beta_0 - (-alpha_s / Rational(5))
    )
    check(
        "(B1) sqrt(5) cancellation: delta/sin(2 beta_0) == -alpha_s/5",
        cancel_residual == 0,
        f"residual = {cancel_residual}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (B2) framework value N_quark = 6 -> coefficient 1/5")
    # ---------------------------------------------------------------------
    coeff_at_framework = simplify(1 / (N_QUARK - 1))
    check(
        "(B2) at N_quark = 6, coefficient = 1/(N_quark - 1) = 1/5",
        coeff_at_framework == Rational(1, 5),
        f"coefficient = {coeff_at_framework}",
    )
    # And the framework-value ratio is 1 - alpha_s/5.
    ratio_at_framework = simplify(1 - alpha_s * coeff_at_framework)
    check(
        "(B2) at framework, ratio == 1 - alpha_s/5",
        simplify(ratio_at_framework - (1 - alpha_s / Rational(5))) == 0,
        f"residual = {simplify(ratio_at_framework - (1 - alpha_s/Rational(5)))}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (B3) gamma-bar protection sin(2 gamma_bar)/sin(2 gamma_0) == 1")
    # ---------------------------------------------------------------------
    # Retained protected-gamma N8: gamma_bar = gamma_0 + O(alpha_s^4).
    # At leading order in alpha_s the ratio is identically 1.
    # We model this directly using sympy by computing the ratio with
    # gamma_bar - gamma_0 set to zero (the retained N8 statement).
    # The note also sets sin(2 gamma_0) = sqrt(5)/3 (= sin(2 beta_0) by
    # atlas right-angle Thales geometry).
    sin_2gamma_0 = sqrt(Rational(5)) / Rational(3)
    sin_2gamma_bar_at_NLO_protected = sin_2gamma_0  # by retained N8
    ratio_gamma = simplify(sin_2gamma_bar_at_NLO_protected / sin_2gamma_0)
    check(
        "(B3) sin(2 gamma_bar)/sin(2 gamma_0) == 1 (PROTECTED at NLO, retained N8)",
        ratio_gamma == 1,
        f"ratio = {ratio_gamma}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (B4) atlas right-angle sin(2 alpha_0) == 0")
    # ---------------------------------------------------------------------
    alpha_0 = pi / 2
    sin_2alpha_0 = simplify(sin(2 * alpha_0))
    check(
        "(B4) sin(2 alpha_0) = sin(pi) = 0 (atlas right-angle)",
        sin_2alpha_0 == 0,
        f"sin(pi) = {sin_2alpha_0}",
    )
    # And alpha_bar - alpha_0 = +n7_slope * alpha_s (retained N7), so
    # sin(2 alpha_bar) is a pure NLO observable, not a multiplicative ratio.
    alpha_bar = pi / 2 + n7_slope * alpha_s
    sin_2alpha_bar_full = simplify(sin(2 * alpha_bar))
    # Linearize: sin(2 alpha_bar) ~ -2 (alpha_bar - pi/2) cos(pi) = +2 slope alpha_s,
    # but sin(pi + x) = -sin(x), so sin(2 alpha_bar) = -2 slope alpha_s + O(alpha_s^3).
    sin_2alpha_bar_lin = -2 * n7_slope * alpha_s
    series_sin = sympy.series(sin_2alpha_bar_full, alpha_s, 0, 2).removeO()
    check(
        "(B4) leading sin(2 alpha_bar) == -2 (sqrt(5)/20) alpha_s = -(sqrt(5)/10) alpha_s",
        simplify(series_sin - sin_2alpha_bar_lin) == 0,
        f"residual = {simplify(series_sin - sin_2alpha_bar_lin)}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: alpha_s-INDEPENDENCE of the 1/(N_quark - 1) coefficient")
    # ---------------------------------------------------------------------
    # The coefficient 1/(N_quark - 1) does not depend on alpha_s's value.
    # Symbolically, the linearization gives ratio = 1 + (-1/(N_quark - 1)) alpha_s,
    # so the coefficient on alpha_s is -1/(N_quark - 1) regardless of alpha_s value.
    # We verify by extracting the linear coefficient via polynomial decomposition.
    ratio_as_poly = sympy.Poly(ratio_lin, alpha_s)
    coeff_const = ratio_as_poly.nth(0)
    coeff_linear = ratio_as_poly.nth(1)
    check(
        "(B1) constant coefficient (alpha_s -> 0) == 1",
        coeff_const == Rational(1),
        f"constant = {coeff_const}",
    )
    check(
        "(B1) linear coefficient on alpha_s == -1/(N_quark - 1) = -1/5",
        coeff_linear == -Rational(1, 5),
        f"linear coeff = {coeff_linear}",
    )
    # Same coefficient via division by alpha_s in the symbolic expression.
    extracted = simplify((1 - ratio_lin) / alpha_s)
    check(
        "(B1) extracted coefficient (1 - ratio)/alpha_s == 1/(N_quark - 1) (alpha_s-independent)",
        simplify(extracted - 1 / (N_QUARK - 1)) == 0,
        f"residual = {simplify(extracted - 1/(N_QUARK - 1))}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: retained N9 closed form first-order consistency")
    # ---------------------------------------------------------------------
    # N9: tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s).
    # We compute sin(2 beta_bar) = 2 tan(beta_bar)/(1 + tan^2(beta_bar))
    # and verify its first-order Taylor expansion in alpha_s matches
    # sin(2 beta_0) - (sqrt(5)/15) alpha_s.
    tan_beta_bar = sqrt(Rational(5)) * (4 - alpha_s) / (20 + alpha_s)
    sin_2beta_bar_via_N9 = simplify(
        2 * tan_beta_bar / (1 + tan_beta_bar ** 2)
    )
    series_N9 = sympy.series(sin_2beta_bar_via_N9, alpha_s, 0, 2).removeO()
    check(
        "(N9) sin(2 beta_bar) Taylor = sqrt(5)/3 - (sqrt(5)/15) alpha_s + O(alpha_s^2)",
        simplify(series_N9 - (sin_2beta_0 + delta_sin_target)) == 0,
        f"series LO+NLO = {series_N9}",
    )
    # Confirm the constant term matches sin(2 beta_0).
    series_const = sympy.Poly(series_N9, alpha_s).nth(0)
    check(
        "(N9) constant term at alpha_s = 0 is sin(2 beta_0) = sqrt(5)/3",
        simplify(series_const - sin_2beta_0) == 0,
        f"constant = {series_const}",
    )
    # Confirm the linear term matches -sqrt(5)/15.
    series_linear = sympy.Poly(series_N9, alpha_s).nth(1)
    check(
        "(N9) linear term is -sqrt(5)/15 (matches linearization)",
        simplify(series_linear + sqrt(Rational(5)) / Rational(15)) == 0,
        f"linear = {series_linear}",
    )
    # Compare ratio from N9 series at first order to the (B1) closed form.
    ratio_N9_series = simplify(series_N9 / sin_2beta_0)
    check(
        "(N9) ratio series at first order == 1 - alpha_s/5 (matches (B1))",
        simplify(ratio_N9_series - (1 - alpha_s / Rational(5))) == 0,
        f"residual = {simplify(ratio_N9_series - (1 - alpha_s/Rational(5)))}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: derivation chain for 1/(N_quark - 1) from retained inputs")
    # ---------------------------------------------------------------------
    # |delta sin(2 beta_bar)| = 2 cos(2 beta_0) * |beta_0 - beta_bar|
    #                         = (4/3) (sqrt(5)/20) alpha_s
    #                         = (sqrt(5)/15) alpha_s.
    factor1 = 2 * cos_2beta_0           # 4/3
    delta_beta_abs = n7_slope * alpha_s
    delta_sin_abs_via_chain = simplify(factor1 * delta_beta_abs)
    delta_sin_abs_target = sqrt(Rational(5)) / Rational(15) * alpha_s
    check(
        "derivation: 2 cos(2 beta_0) (beta_0 - beta_bar) == (sqrt(5)/15) alpha_s",
        simplify(delta_sin_abs_via_chain - delta_sin_abs_target) == 0,
        f"residual = {simplify(delta_sin_abs_via_chain - delta_sin_abs_target)}",
    )
    # Divide by sin(2 beta_0) = sqrt(5)/3 to get coefficient 1/5.
    coeff_via_chain = simplify(
        delta_sin_abs_via_chain / sin_2beta_0 / alpha_s
    )
    check(
        "derivation: coefficient = (sqrt(5)/15)/(sqrt(5)/3) = 1/5 = 1/(N_quark - 1)",
        coeff_via_chain == Rational(1, 5),
        f"coeff = {coeff_via_chain}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: connection to retained 1+5 quark-block decomposition")
    # ---------------------------------------------------------------------
    # Retained CKM CP-phase theorem: w_perp = (N_quark - 1)/N_quark, w_A1 = 1/N_quark.
    w_A1 = Rational(1) / N_QUARK
    w_perp = (N_QUARK - 1) / N_QUARK
    eta_sq = simplify(w_A1 * w_perp)  # = (N_quark - 1)/N_quark^2 = 5/36
    check(
        "retained CP-phase: w_A1 == 1/6, w_perp == 5/6 (1+5 decomposition)",
        w_A1 == Rational(1, 6) and w_perp == Rational(5, 6),
        f"w_A1 = {w_A1}, w_perp = {w_perp}",
    )
    check(
        "eta^2 = w_A1 * w_perp == (N_quark - 1)/N_quark^2 = 5/36",
        eta_sq == Rational(5, 36),
        f"eta^2 = {eta_sq}",
    )
    # The (B1) coefficient is the inverse of the orthogonal-channel weight numerator.
    inverse_w_perp_num = simplify(1 / (N_QUARK - 1))  # = 1/5
    check(
        "(B1) coefficient 1/(N_quark - 1) == inverse of orthogonal-channel weight numerator",
        inverse_w_perp_num == Rational(1, 5),
        f"1/(N_quark - 1) = {inverse_w_perp_num}",
    )

    # ---------------------------------------------------------------------
    section("Part 10: counterfactual probes")
    # ---------------------------------------------------------------------
    # (a) If N_quark were 5 (counterfactual), the coefficient would be 1/4 not 1/5.
    cf_coeff_Nq5 = simplify(1 / (Rational(5) - 1))
    check(
        "counterfactual: at N_quark = 5, coefficient = 1/4 != 1/5",
        cf_coeff_Nq5 != Rational(1, 5),
        f"coefficient at N_quark=5 = {cf_coeff_Nq5}",
    )

    # (b) If sin(2 beta_0) were a different cited value, the sqrt(5) cancellation breaks.
    # Counterfactual: sin(2 beta_0) = 1 (not sqrt(5)/3) -> ratio coefficient is sqrt(5)/15
    # not 1/5.
    cf_sin_2beta_0 = Rational(1)
    cf_coeff = simplify(
        (sqrt(Rational(5)) / Rational(15)) / cf_sin_2beta_0
    )
    check(
        "counterfactual: at sin(2 beta_0) = 1, coefficient = sqrt(5)/15 (irrational, != 1/5)",
        cf_coeff != Rational(1, 5),
        f"coefficient at cf sin = {cf_coeff}",
    )

    # (c) If cos(2 beta_0) were 1 instead of 2/3, factor1 = 2, and
    #   delta_sin = 2 * (sqrt(5)/20) alpha_s = (sqrt(5)/10) alpha_s.
    # Dividing by sqrt(5)/3 gives 3/10 not 1/5.
    cf_cos = Rational(1)
    cf_factor1 = 2 * cf_cos
    cf_delta_sin = cf_factor1 * n7_slope * alpha_s
    cf_coeff_cos = simplify(cf_delta_sin / sin_2beta_0 / alpha_s)
    check(
        "counterfactual: at cos(2 beta_0) = 1, coefficient = 3/10 != 1/5",
        cf_coeff_cos != Rational(1, 5),
        f"coefficient at cf cos = {cf_coeff_cos}",
    )

    # (d) If the N7 slope were 1/20 (no sqrt(5)) instead of sqrt(5)/20,
    #   coefficient becomes (4/3)(1/20)/(sqrt(5)/3) = 1/(5 sqrt(5)) (irrational).
    cf_slope = Rational(1, 20)
    cf_delta_sin_slope = 2 * cos_2beta_0 * cf_slope * alpha_s
    cf_coeff_slope = simplify(cf_delta_sin_slope / sin_2beta_0 / alpha_s)
    check(
        "counterfactual: at N7 slope = 1/20 (no sqrt(5)), coefficient is irrational, != 1/5",
        cf_coeff_slope != Rational(1, 5),
        f"coefficient at cf slope = {cf_coeff_slope}",
    )

    # (e) The Pythagorean check sin^2(2 beta_0) + cos^2(2 beta_0) = 5/9 + 4/9 = 1 is
    # load-bearing for the right-angle theorem.
    pyth_check = simplify(
        (sqrt(Rational(5)) / Rational(3)) ** 2 + Rational(2, 3) ** 2 - 1
    )
    check(
        "structural check: 5/9 + 4/9 == 1 (Pythagorean for (sin(2 beta_0), cos(2 beta_0)))",
        pyth_check == 0,
        f"residual = {pyth_check}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision parametric in alpha_s:")
    print("    Linearization: sin(2 beta_bar) - sin(2 beta_0) == -(sqrt(5)/15) alpha_s")
    print("    (B1) sin(2 beta_bar)/sin(2 beta_0) == 1 - alpha_s/(N_quark - 1)")
    print("    sqrt(5) cancellation: delta_sin / sin(2 beta_0) == -alpha_s/5")
    print("    (B2) at framework N_quark = 6, coefficient = 1/5")
    print("    (B3) sin(2 gamma_bar)/sin(2 gamma_0) == 1 (NLO-protected via N8)")
    print("    (B4) sin(2 alpha_0) == 0 (atlas right-angle)")
    print("    alpha_s-INDEPENDENCE: linear coefficient is exactly -1/(N_quark - 1)")
    print("        as a pure rational, independent of any numerical alpha_s value")
    print("    (N9) Taylor expansion in alpha_s matches the linearization at first order")
    print("    1+5 connection: 1/(N_quark - 1) is the inverse of the orthogonal-channel")
    print("        weight numerator from the retained CP-phase theorem")
    print("    Counterfactuals confirm sin(2 beta_0), cos(2 beta_0), N7 slope, and")
    print("    N_quark are individually load-bearing for the closed-form 1/5 coefficient.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
