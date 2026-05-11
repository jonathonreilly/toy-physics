#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_barred_apex_angle_exact_closed_form_theorem_note_2026-04-25`.

The parent note's load-bearing content is the closed-form derivation
that on the cited NLO Wolfenstein protected-gamma-bar surface

  tan(gamma_bar) = sqrt(5)                       (cited N4 / N8, alpha_s-protected)
  tan(beta_bar)  = sqrt(5)(4 - alpha_s)/(20 + alpha_s)  (cited N5)
  alpha_bar      = pi - gamma_0 - beta_bar       (cited N6, with gamma_bar = gamma_0 by N4)

force the named exact-in-alpha_s closed forms

  (A1)  tan(alpha_bar)    = -4 sqrt(5)/alpha_s
  (A2)  cot(alpha_bar)    = -alpha_s/(4 sqrt(5)) = -(sqrt(5)/20) alpha_s
  (A3)  tan(alpha_bar - pi/2) = +(sqrt(5)/20) alpha_s
  (A4)  alpha_bar - pi/2  = arctan((sqrt(5)/20) alpha_s)
  (A5)  sin^2(alpha_bar)  = 80/(80 + alpha_s^2)
  (A6)  cos^2(alpha_bar)  = alpha_s^2/(80 + alpha_s^2)
  (A7)  sin(2 alpha_bar)  = -8 sqrt(5) alpha_s/(80 + alpha_s^2)
  (A8)  cos(2 alpha_bar)  = -(80 - alpha_s^2)/(80 + alpha_s^2)
  (A9)  common denominator 80 + alpha_s^2 = 96 R_t_bar^2
  (A10) Taylor of (alpha_bar - pi/2) has only ODD powers of alpha_s
  (A11) tan(alpha_bar) = -N_pair^2 sqrt(N_quark - 1) / alpha_s

The existing primary runner
(`scripts/frontier_ckm_barred_apex_angle_exact_closed_form.py`) verifies
these identities at floating-point tolerance using the canonical
numerical `alpha_s(v)`. This Pattern B audit companion adds a
sympy-based exact-symbolic verification:

  (a) treats `alpha_s(v)` as a free positive real symbol;
  (b) imports cited `tan(beta_bar)`, `tan(gamma_bar)`, and the angle
      sum (N6) verbatim;
  (c) verifies (A1) via tangent-of-sum and (4 - alpha_s) / (20 + alpha_s)
      cancellations parametric in alpha_s;
  (d) derives (A5)-(A8) from (A1) using the standard sin^2 / cos^2 and
      double-angle identities;
  (e) verifies the parity selection rule (A10) by computing the Taylor
      series of arctan((sqrt(5)/20) alpha_s) around alpha_s = 0 to
      explicit order alpha_s^9 and asserting all even-order
      coefficients vanish exactly;
  (f) verifies (A11) the structural-integer factorization at
      N_pair = 2, N_quark = 6;
  (g) provides counterfactual probes confirming protected
      tan(gamma_bar) = sqrt(5) is what produces the single-monomial
      (A1) closed form, and confirming the (20 + alpha_s) factor
      cancellation in tan(alpha_bar) is what makes (A1) exact in
      alpha_s.

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, no status promotion. The cited inputs (N4, N5, N6, structural counts) are imported from upstream authority
notes and are not re-derived here.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, sqrt, atan, series, Poly, expand
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
    print("ckm_barred_apex_angle_exact_closed_form_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (A1)-(A11) parametric in alpha_s")
    print("on the cited NLO protected-gamma-bar surface.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and cited inputs")
    # ---------------------------------------------------------------------
    alpha_s = Symbol("alpha_s", positive=True, real=True)
    N_pair = Rational(2)
    N_quark = Rational(6)

    # Cited N5 + N4 tangents.
    tan_beta_bar = sqrt(5) * (4 - alpha_s) / (20 + alpha_s)
    tan_gamma_bar = sqrt(5)

    print(f"  symbolic alpha_s(v) = {alpha_s}")
    print(f"  tan(beta_bar) (N5)  = {tan_beta_bar}")
    print(f"  tan(gamma_bar) (N4) = {tan_gamma_bar}")

    # ---------------------------------------------------------------------
    section("Part 1: (A1) tan(alpha_bar) = -4 sqrt(5)/alpha_s via tangent-of-sum")
    # ---------------------------------------------------------------------
    # alpha_bar = pi - gamma_bar - beta_bar (N6 with gamma_bar = gamma_0).
    # tan(alpha_bar) = -tan(beta_bar + gamma_bar) = -(t_b + t_g)/(1 - t_b t_g).
    num_sum = simplify(tan_beta_bar + tan_gamma_bar)
    den_sum = simplify(1 - tan_beta_bar * tan_gamma_bar)
    tan_alpha_bar = simplify(-num_sum / den_sum)
    target_A1 = -4 * sqrt(5) / alpha_s

    check(
        "(A1) tan(alpha_bar) == -4 sqrt(5)/alpha_s (parametric in alpha_s)",
        simplify(tan_alpha_bar - target_A1) == 0,
        f"residual = {simplify(tan_alpha_bar - target_A1)}",
    )

    # Numerator of the tangent-sum reduces to 24 sqrt(5)/(20 + alpha_s).
    check(
        "tan(beta_bar) + tan(gamma_bar) == 24 sqrt(5)/(20 + alpha_s)",
        simplify(num_sum - 24 * sqrt(5) / (20 + alpha_s)) == 0,
        f"residual = {simplify(num_sum - 24*sqrt(5)/(20 + alpha_s))}",
    )
    # Denominator reduces to 6 alpha_s/(20 + alpha_s).
    check(
        "1 - tan(beta_bar) tan(gamma_bar) == 6 alpha_s/(20 + alpha_s)",
        simplify(den_sum - 6 * alpha_s / (20 + alpha_s)) == 0,
        f"residual = {simplify(den_sum - 6*alpha_s/(20 + alpha_s))}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (A2) cot, (A3) tan(alpha_bar - pi/2), (A4) arctan inversion")
    # ---------------------------------------------------------------------
    cot_alpha_bar = simplify(1 / tan_alpha_bar)
    target_A2 = -sqrt(5) * alpha_s / Rational(20)
    check(
        "(A2) cot(alpha_bar) == -(sqrt(5)/20) alpha_s",
        simplify(cot_alpha_bar - target_A2) == 0,
        f"residual = {simplify(cot_alpha_bar - target_A2)}",
    )

    # tan(alpha_bar - pi/2) = -cot(alpha_bar) = +(sqrt(5)/20) alpha_s.
    target_A3 = sqrt(5) * alpha_s / Rational(20)
    check(
        "(A3) tan(alpha_bar - pi/2) == +(sqrt(5)/20) alpha_s",
        simplify(-cot_alpha_bar - target_A3) == 0,
        f"residual = {simplify(-cot_alpha_bar - target_A3)}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (A5)-(A8) sin^2, cos^2, double-angle closed forms")
    # ---------------------------------------------------------------------
    tan_sq = simplify(tan_alpha_bar ** 2)  # = 80/alpha_s^2
    cos_sq = simplify(1 / (1 + tan_sq))    # = alpha_s^2/(80 + alpha_s^2)
    sin_sq = simplify(1 - cos_sq)          # = 80/(80 + alpha_s^2)
    target_A5 = 80 / (80 + alpha_s ** 2)
    target_A6 = alpha_s ** 2 / (alpha_s ** 2 + 80)
    check(
        "(A5) sin^2(alpha_bar) == 80/(80 + alpha_s^2)",
        simplify(sin_sq - target_A5) == 0,
        f"residual = {simplify(sin_sq - target_A5)}",
    )
    check(
        "(A6) cos^2(alpha_bar) == alpha_s^2/(80 + alpha_s^2)",
        simplify(cos_sq - target_A6) == 0,
        f"residual = {simplify(cos_sq - target_A6)}",
    )

    # Double-angle: alpha_bar = pi/2 + delta with tan(delta) = (sqrt(5)/20) alpha_s.
    # cos(2 alpha_bar) = -(1 - tan^2 delta)/(1 + tan^2 delta).
    # sin(2 alpha_bar) = -2 tan(delta)/(1 + tan^2 delta).
    tan_delta = sqrt(5) * alpha_s / Rational(20)
    tan_delta_sq = simplify(tan_delta ** 2)  # = alpha_s^2/80
    cos_2alpha = simplify(-(1 - tan_delta_sq) / (1 + tan_delta_sq))
    sin_2alpha = simplify(-2 * tan_delta / (1 + tan_delta_sq))
    target_A8 = -(80 - alpha_s ** 2) / (80 + alpha_s ** 2)
    target_A7 = -8 * sqrt(5) * alpha_s / (80 + alpha_s ** 2)
    check(
        "(A8) cos(2 alpha_bar) == -(80 - alpha_s^2)/(80 + alpha_s^2)",
        simplify(cos_2alpha - target_A8) == 0,
        f"residual = {simplify(cos_2alpha - target_A8)}",
    )
    check(
        "(A7) sin(2 alpha_bar) == -8 sqrt(5) alpha_s/(80 + alpha_s^2)",
        simplify(sin_2alpha - target_A7) == 0,
        f"residual = {simplify(sin_2alpha - target_A7)}",
    )

    # Sin^2(2alpha) + cos^2(2alpha) = 1 sanity.
    pythag_2alpha = simplify(sin_2alpha ** 2 + cos_2alpha ** 2)
    check(
        "sin^2(2 alpha_bar) + cos^2(2 alpha_bar) == 1 (sanity)",
        simplify(pythag_2alpha - 1) == 0,
        f"residual = {simplify(pythag_2alpha - 1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (A9) common denominator 80 + alpha_s^2 = 96 R_t_bar^2")
    # ---------------------------------------------------------------------
    # R_t_bar^2 = (1 - rho_bar)^2 + eta_bar^2 with rho_bar = (4-alpha_s)/24,
    # eta_bar = sqrt(5)(4-alpha_s)/24. The cross-link to the rho-lambda
    # sum-rule note gives R_t_bar^2 = (80 + alpha_s^2)/96.
    rho_bar = (4 - alpha_s) / Rational(24)
    eta_bar = sqrt(5) * (4 - alpha_s) / Rational(24)
    Rt_bar_sq = simplify((1 - rho_bar) ** 2 + eta_bar ** 2)
    target_Rt_bar_sq = (80 + alpha_s ** 2) / Rational(96)
    check(
        "R_t_bar^2 == (80 + alpha_s^2)/96 (parametric)",
        simplify(Rt_bar_sq - target_Rt_bar_sq) == 0,
        f"residual = {simplify(Rt_bar_sq - target_Rt_bar_sq)}",
    )
    check(
        "(A9) 80 + alpha_s^2 == 96 R_t_bar^2",
        simplify((80 + alpha_s ** 2) - 96 * Rt_bar_sq) == 0,
        f"residual = {simplify((80 + alpha_s**2) - 96 * Rt_bar_sq)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (A10) parity selection rule -- arctan series odd-only")
    # ---------------------------------------------------------------------
    # alpha_bar - pi/2 = arctan((sqrt(5)/20) alpha_s).
    # arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ... (only odd powers).
    # We confirm by computing the Taylor expansion to order alpha_s^9 and
    # asserting all even-order coefficients (alpha_s^2, alpha_s^4, ...) vanish.
    expansion = series(atan(tan_delta), alpha_s, 0, 10).removeO()
    poly_exp = Poly(expand(expansion), alpha_s)
    coeff_dict = {p[0]: c for p, c in poly_exp.terms()}

    # Even-order coefficients in alpha_s^0, alpha_s^2, alpha_s^4, alpha_s^6, alpha_s^8.
    for n in (0, 2, 4, 6, 8):
        c_n = coeff_dict.get(n, Rational(0))
        check(
            f"(A10) coefficient of alpha_s^{n} in (alpha_bar - pi/2) is 0",
            simplify(c_n) == 0,
            f"coeff = {c_n}",
        )

    # Linear coefficient is sqrt(5)/20.
    c1 = coeff_dict.get(1, Rational(0))
    check(
        "(A10) linear coefficient (alpha_s^1) is sqrt(5)/20 (matches cited N7)",
        simplify(c1 - sqrt(5) / Rational(20)) == 0,
        f"c1 = {c1}",
    )
    # Cubic coefficient is -(sqrt(5)/20)^3 / 3 = -5 sqrt(5)/24000.
    c3 = coeff_dict.get(3, Rational(0))
    target_c3 = -(sqrt(5) / Rational(20)) ** 3 / 3
    check(
        "(A10) cubic coefficient (alpha_s^3) is -(sqrt(5)/20)^3/3 = -5 sqrt(5)/24000",
        simplify(c3 - target_c3) == 0,
        f"c3 = {c3}, target = {simplify(target_c3)}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (A11) structural-integer factorization")
    # ---------------------------------------------------------------------
    # tan(alpha_bar) = -N_pair^2 sqrt(N_quark - 1)/alpha_s, with N_pair = 2,
    # N_quark = 6 giving N_pair^2 = 4 and sqrt(N_quark - 1) = sqrt(5).
    target_A11 = -N_pair ** 2 * sqrt(N_quark - 1) / alpha_s
    check(
        "(A11) tan(alpha_bar) == -N_pair^2 sqrt(N_quark - 1)/alpha_s at (N_pair, N_quark) = (2, 6)",
        simplify(target_A11 - target_A1) == 0,
        f"residual = {simplify(target_A11 - target_A1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: counterfactual probes")
    # ---------------------------------------------------------------------
    # If tan(gamma_bar) were not protected at sqrt(5), the (20 + alpha_s)
    # cancellation would not produce the single-monomial closed form.
    tan_gamma_alt = Rational(1)
    num_alt = tan_beta_bar + tan_gamma_alt
    den_alt = 1 - tan_beta_bar * tan_gamma_alt
    tan_alpha_alt = simplify(-num_alt / den_alt)
    check(
        "counterfactual: at tan(gamma_bar) = 1, tan(alpha_bar) is no longer -4 sqrt(5)/alpha_s",
        simplify(tan_alpha_alt - target_A1) != 0,
        "alternate tan(alpha_bar) does not collapse to the closed form",
    )

    # If we drop the (20 + alpha_s) denominator from tan(beta_bar) (i.e. set
    # it to a pure constant sqrt(5)(4-alpha_s)), the sum-of-tangents
    # numerator no longer cancels cleanly with the denominator.
    tan_beta_alt = sqrt(5) * (4 - alpha_s)  # missing /(20 + alpha_s)
    num_alt2 = tan_beta_alt + tan_gamma_bar
    den_alt2 = 1 - tan_beta_alt * tan_gamma_bar
    tan_alpha_alt2 = simplify(-num_alt2 / den_alt2)
    check(
        "counterfactual: dropping (20+alpha_s) denominator from tan(beta_bar) breaks (A1)",
        simplify(tan_alpha_alt2 - target_A1) != 0,
        "alternate tan(alpha_bar) does not collapse to single-monomial form",
    )

    # ---------------------------------------------------------------------
    section("Part 8: trailing numerical sanity (canonical alpha_s pin)")
    # ---------------------------------------------------------------------
    try:
        from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

        alpha_s_value = float(CANONICAL_ALPHA_S_V)
        tan_a_num = float(target_A1.subs(alpha_s, alpha_s_value))
        sin_sq_num = float(target_A5.subs(alpha_s, alpha_s_value))
        cos_sq_num = float(target_A6.subs(alpha_s, alpha_s_value))
        print(f"  canonical alpha_s(v) = {alpha_s_value:.15f}")
        print(f"  tan(alpha_bar) = {tan_a_num:.10f}")
        print(f"  sin^2(alpha_bar) = {sin_sq_num:.10f}, cos^2 = {cos_sq_num:.10f}")
        check(
            "tan(alpha_bar) ~ -86.5822 at canonical alpha_s",
            abs(tan_a_num - (-86.5822023401)) < 1e-4,
            f"got {tan_a_num:.10f}",
        )
        check(
            "sin^2(alpha_bar) ~ 0.99986662 at canonical alpha_s",
            abs(sin_sq_num - 0.9998666218) < 1e-7,
            f"got {sin_sq_num:.10f}",
        )
    except ImportError:
        print("  skipped: canonical_plaquette_surface not on PYTHONPATH")

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (A1) tan(alpha_bar) == -4 sqrt(5)/alpha_s (from N5, N4, N6)")
    print("    (A2) cot(alpha_bar) == -(sqrt(5)/20) alpha_s")
    print("    (A3) tan(alpha_bar - pi/2) == +(sqrt(5)/20) alpha_s")
    print("    (A5) sin^2(alpha_bar) == 80/(80 + alpha_s^2)")
    print("    (A6) cos^2(alpha_bar) == alpha_s^2/(80 + alpha_s^2)")
    print("    (A7) sin(2 alpha_bar) == -8 sqrt(5) alpha_s/(80 + alpha_s^2)")
    print("    (A8) cos(2 alpha_bar) == -(80 - alpha_s^2)/(80 + alpha_s^2)")
    print("    (A9) 80 + alpha_s^2 == 96 R_t_bar^2 (common denominator)")
    print("    (A10) Taylor of (alpha_bar - pi/2) has only ODD powers of alpha_s")
    print("         (linear coefficient sqrt(5)/20, cubic coefficient -5 sqrt(5)/24000)")
    print("    (A11) tan(alpha_bar) == -N_pair^2 sqrt(N_quark - 1)/alpha_s at (2, 6)")
    print("    Counterfactuals confirm tan(gamma_bar) = sqrt(5) (protection) and")
    print("    the (20 + alpha_s) factor cancellation are individually load-bearing.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
