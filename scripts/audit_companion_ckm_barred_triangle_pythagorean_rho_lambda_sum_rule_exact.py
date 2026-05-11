#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`ckm_barred_triangle_pythagorean_rho_lambda_sum_rule_theorem_note_2026-04-25`.

The parent note's load-bearing content is the closed-form derivation
that on the cited NLO Wolfenstein protected-gamma-bar surface

  rho_bar  = (4 - alpha_s) / 24            (cited N1)
  eta_bar  = sqrt(5)(4 - alpha_s) / 24     (cited N2)
  R_b_bar^2 = (4 - alpha_s)^2 / 96         (cited N3)
  lambda^2  = alpha_s / 2                  (cited Wolfenstein W1)

force the named Pythagorean sum rule

  (P1) R_b_bar^2 = rho_bar^2 + eta_bar^2 = (4 - alpha_s)^2 / 96  [cited N3]
  (P2) R_t_bar^2 = (1 - rho_bar)^2 + eta_bar^2 = (80 + alpha_s^2) / 96  [NEW]
  (P3) R_b_bar^2 + R_t_bar^2 = 1 - alpha_s/12 + alpha_s^2/48  [NEW Pythagorean defect]
  (P4) R_b_bar^2 + R_t_bar^2 + rho_bar * lambda^2 = 1  [NEW EXACT, no O(alpha_s^3)]
  (P5) defect = rho_bar * lambda^2 = alpha_s(4 - alpha_s)/48
              = alpha_s / 12 - alpha_s^2 / 48
              with leading coefficient 1/12 = 1/(N_quark * N_pair)

The existing primary runner
(`scripts/frontier_ckm_barred_triangle_pythagorean_rho_lambda_sum_rule.py`)
verifies these identities at floating-point tolerance using the
canonical numerical alpha_s(v). This Pattern B audit companion adds a
sympy-based exact-symbolic verification:

  (a) treats alpha_s(v) as a free positive real symbol;
  (b) imports cited (N1), (N2), (N3) and Wolfenstein W1 verbatim;
  (c) verifies (P2) R_t_bar^2 closed form symbolically;
  (d) verifies (P3) the Pythagorean defect closed form symbolically;
  (e) verifies (P4) the exact sum rule
        R_b_bar^2 + R_t_bar^2 + rho_bar lambda^2 == 1
      via simplify(LHS - 1) == 0 parametric in alpha_s; this is the
      headline EXACT identity that confirms there are no
      O(alpha_s^3) corrections;
  (f) verifies the defect coefficient structure (P5);
  (g) provides counterfactual probes confirming (4 - alpha_s)
      cancellation and W1 lambda^2 = alpha_s/2 are individually
      load-bearing for the EXACT cancellation in (P4).

Companion role: Pattern B audit-acceleration only. Not a new claim row,
not a new source note, no status promotion. The cited inputs (N1-N3, Wolfenstein W1, structural counts N_pair = 2, N_quark = 6) are
imported from upstream authority notes and are not re-derived here.
"""

from __future__ import annotations

import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, sqrt, Poly, expand
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
    print("ckm_barred_triangle_pythagorean_rho_lambda_sum_rule_theorem_note_2026-04-25")
    print("Goal: sympy-symbolic verification of (P1)-(P5) at exact precision")
    print("parametric in alpha_s on the cited NLO protected-gamma-bar surface.")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup and cited inputs")
    # ---------------------------------------------------------------------
    alpha_s = Symbol("alpha_s", positive=True, real=True)
    N_pair = Rational(2)
    N_quark = Rational(6)

    rho_bar = (4 - alpha_s) / Rational(24)
    eta_bar = sqrt(5) * (4 - alpha_s) / Rational(24)
    Rb_bar_sq = (4 - alpha_s) ** 2 / Rational(96)
    lambda_sq = alpha_s / Rational(2)  # Wolfenstein W1

    print(f"  symbolic alpha_s(v) = {alpha_s}")
    print(f"  rho_bar  (N1)     = {rho_bar}")
    print(f"  eta_bar  (N2)     = {eta_bar}")
    print(f"  R_b_bar^2 (N3)    = {Rb_bar_sq}")
    print(f"  lambda^2 (W1)     = {lambda_sq}")
    print(f"  N_pair = {N_pair}, N_quark = {N_quark}")

    # ---------------------------------------------------------------------
    section("Part 1: (P1) R_b_bar^2 = rho_bar^2 + eta_bar^2 = (4 - alpha_s)^2/96")
    # ---------------------------------------------------------------------
    Rb_bar_sq_lhs = simplify(rho_bar ** 2 + eta_bar ** 2)
    check(
        "(P1) rho_bar^2 + eta_bar^2 == (4 - alpha_s)^2/96 (parametric)",
        simplify(Rb_bar_sq_lhs - Rb_bar_sq) == 0,
        f"residual = {simplify(Rb_bar_sq_lhs - Rb_bar_sq)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (P2) R_t_bar^2 = (80 + alpha_s^2)/96")
    # ---------------------------------------------------------------------
    Rt_bar_sq_lhs = simplify((1 - rho_bar) ** 2 + eta_bar ** 2)
    Rt_bar_sq_target = (80 + alpha_s ** 2) / Rational(96)
    check(
        "(P2) (1 - rho_bar)^2 + eta_bar^2 == (80 + alpha_s^2)/96 (parametric)",
        simplify(Rt_bar_sq_lhs - Rt_bar_sq_target) == 0,
        f"residual = {simplify(Rt_bar_sq_lhs - Rt_bar_sq_target)}",
    )

    # Atlas-LO recovery: R_t_bar^2 -> 80/96 = 5/6 at alpha_s = 0.
    Rt_LO = simplify(Rt_bar_sq_target.subs(alpha_s, 0))
    check(
        "(P2) atlas-LO recovery R_t_bar^2 -> 5/6 at alpha_s = 0",
        Rt_LO == Rational(5, 6),
        f"Rt_LO = {Rt_LO}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (P3) Pythagorean defect closed form")
    # ---------------------------------------------------------------------
    sum_squares = simplify(Rb_bar_sq + Rt_bar_sq_target)
    sum_target = 1 - alpha_s / Rational(12) + alpha_s ** 2 / Rational(48)
    check(
        "(P3) R_b_bar^2 + R_t_bar^2 == 1 - alpha_s/12 + alpha_s^2/48 (parametric)",
        simplify(sum_squares - sum_target) == 0,
        f"residual = {simplify(sum_squares - sum_target)}",
    )

    defect = simplify(1 - sum_squares)
    defect_target = alpha_s / Rational(12) - alpha_s ** 2 / Rational(48)
    check(
        "(P3) defect = 1 - (R_b^2 + R_t^2) == alpha_s/12 - alpha_s^2/48",
        simplify(defect - defect_target) == 0,
        f"residual = {simplify(defect - defect_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (P4) EXACT sum rule R_b^2 + R_t^2 + rho_bar lambda^2 = 1")
    # ---------------------------------------------------------------------
    rho_lambda_sq = simplify(rho_bar * lambda_sq)
    rho_lambda_sq_target = alpha_s * (4 - alpha_s) / Rational(48)
    check(
        "rho_bar * lambda^2 == alpha_s(4 - alpha_s)/48 (parametric)",
        simplify(rho_lambda_sq - rho_lambda_sq_target) == 0,
        f"residual = {simplify(rho_lambda_sq - rho_lambda_sq_target)}",
    )

    # The headline (P4) identity.
    P4_lhs = simplify(Rb_bar_sq + Rt_bar_sq_target + rho_lambda_sq)
    check(
        "(P4) R_b_bar^2 + R_t_bar^2 + rho_bar * lambda^2 == 1 (parametric, EXACT)",
        simplify(P4_lhs - 1) == 0,
        f"residual = {simplify(P4_lhs - 1)}",
    )

    # Confirm no alpha_s residual at any order: P4_lhs - 1 should be
    # the zero polynomial in alpha_s (no O(alpha_s^3) tail).
    residual_poly = expand(simplify(P4_lhs - 1))
    check(
        "(P4) residual polynomial is identically 0 (no alpha_s^k corrections)",
        residual_poly == 0,
        f"residual_poly = {residual_poly}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (P5) defect coefficient structure")
    # ---------------------------------------------------------------------
    # Leading coefficient: 1/12 = 1/(N_quark * N_pair) at (N_pair, N_quark) = (2, 6).
    leading = Rational(1) / (N_quark * N_pair)
    check(
        "(P5) leading defect coefficient 1/12 == 1/(N_quark * N_pair) at (2, 6)",
        leading == Rational(1, 12),
        f"value = {leading}",
    )

    # Sub-leading coefficient: 1/48 = 1/(N_quark * N_pair^3) at (2, 6).
    subleading = Rational(1) / (N_quark * N_pair ** 3)
    check(
        "(P5) sub-leading defect coefficient 1/48 == 1/(N_quark * N_pair^3) at (2, 6)",
        subleading == Rational(1, 48),
        f"value = {subleading}",
    )

    # Confirm the parent-note polynomial form
    # defect = alpha_s/(N_quark N_pair) - alpha_s^2/(N_quark N_pair^3)
    defect_struct = alpha_s / (N_quark * N_pair) - alpha_s ** 2 / (N_quark * N_pair ** 3)
    check(
        "(P5) defect == alpha_s/(N_quark N_pair) - alpha_s^2/(N_quark N_pair^3) at (2, 6)",
        simplify(defect_struct - defect_target) == 0,
        f"residual = {simplify(defect_struct - defect_target)}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (P6) law-of-cosines geometric interpretation")
    # ---------------------------------------------------------------------
    # Law of cosines: 1 = R_b^2 + R_t^2 - 2 R_b R_t cos(alpha_bar). So
    # 1 - (R_b^2 + R_t^2) = -2 R_b R_t cos(alpha_bar). Combined with (P4):
    # rho_bar * lambda^2 = -2 R_b R_t cos(alpha_bar). Squaring removes the
    # ambiguity from sqrt, giving (rho_bar lambda^2)^2 = 4 R_b^2 R_t^2 cos^2.
    # We do not have cos(alpha_bar) in scope here without the apex theorem,
    # so we content ourselves with verifying defect == -2 R_b R_t cos(alpha_bar)
    # via the apex-angle theorem's cos^2(alpha_bar) = alpha_s^2/(80+alpha_s^2)
    # and confirming the squared form matches.
    cos_sq_alpha_bar = alpha_s ** 2 / (80 + alpha_s ** 2)  # from apex-angle theorem
    rhs_sq = simplify(4 * Rb_bar_sq * Rt_bar_sq_target * cos_sq_alpha_bar)
    lhs_sq = simplify(defect_target ** 2)
    check(
        "(P6) defect^2 == 4 R_b^2 R_t^2 cos^2(alpha_bar) (parametric, squared form)",
        simplify(lhs_sq - rhs_sq) == 0,
        f"residual = {simplify(lhs_sq - rhs_sq)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: counterfactual probes")
    # ---------------------------------------------------------------------
    # (4 - alpha_s) cancellation between rho_bar and eta_bar is what makes
    # (P2) collapse to (80 + alpha_s^2)/96. If the (4 - alpha_s) factor
    # were not coupled in N1 and N2, the cancellation would not occur
    # cleanly.
    eta_bar_alt = sqrt(5) * Rational(4) / Rational(24)  # drops (4-alpha_s) coupling
    Rt_alt = simplify((1 - rho_bar) ** 2 + eta_bar_alt ** 2)
    check(
        "counterfactual: dropping (4-alpha_s) from eta_bar breaks (P2)",
        simplify(Rt_alt - Rt_bar_sq_target) != 0,
        "alternate R_t_bar^2 is no longer (80 + alpha_s^2)/96",
    )

    # If lambda^2 were not alpha_s/2 (e.g. lambda^2 = alpha_s), the EXACT
    # sum rule (P4) would acquire an alpha_s^k residual.
    lambda_sq_alt = alpha_s
    P4_alt = simplify(Rb_bar_sq + Rt_bar_sq_target + rho_bar * lambda_sq_alt)
    check(
        "counterfactual: at lambda^2 = alpha_s, (P4) sum != 1 (acquires alpha_s residual)",
        simplify(P4_alt - 1) != 0,
        f"residual = {simplify(P4_alt - 1)}",
    )

    # If rho_bar were 1/6 (atlas-LO instead of NLO), the defect would be
    # alpha_s/12 (only) and not match the second-order term in (P3).
    rho_bar_alt = Rational(1, 6)
    P4_alt2 = simplify(Rb_bar_sq + Rt_bar_sq_target + rho_bar_alt * lambda_sq)
    check(
        "counterfactual: at rho_bar = 1/6 (atlas-LO), (P4) sum != 1 in alpha_s^2 term",
        simplify(P4_alt2 - 1) != 0,
        f"residual = {simplify(P4_alt2 - 1)}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: trailing numerical sanity (canonical alpha_s pin)")
    # ---------------------------------------------------------------------
    try:
        from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

        alpha_s_value = float(CANONICAL_ALPHA_S_V)
        Rb_num = float(Rb_bar_sq.subs(alpha_s, alpha_s_value))
        Rt_num = float(Rt_bar_sq_target.subs(alpha_s, alpha_s_value))
        defect_num = float(defect_target.subs(alpha_s, alpha_s_value))
        sum_num = Rb_num + Rt_num + defect_num
        print(f"  canonical alpha_s(v) = {alpha_s_value:.15f}")
        print(f"  R_b_bar^2 = {Rb_num:.10f}")
        print(f"  R_t_bar^2 = {Rt_num:.10f}")
        print(f"  rho_bar * lambda^2 = {defect_num:.10f}")
        print(f"  sum (should be 1.0) = {sum_num:.15f}")
        check(
            "R_b_bar^2 + R_t_bar^2 + rho_bar lambda^2 ~ 1.0 at canonical alpha_s",
            abs(sum_num - 1.0) < 1e-12,
            f"got {sum_num:.15f}",
        )
        check(
            "defect ~ 0.008386 at canonical alpha_s",
            abs(defect_num - 0.008386) < 1e-5,
            f"got {defect_num:.6f}",
        )
    except ImportError:
        print("  skipped: canonical_plaquette_surface not on PYTHONPATH")

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (P1) R_b_bar^2 == rho_bar^2 + eta_bar^2 == (4 - alpha_s)^2/96")
    print("    (P2) R_t_bar^2 == (80 + alpha_s^2)/96")
    print("    (P3) R_b_bar^2 + R_t_bar^2 == 1 - alpha_s/12 + alpha_s^2/48")
    print("    (P4) R_b_bar^2 + R_t_bar^2 + rho_bar lambda^2 == 1 (EXACT, no alpha_s^3+)")
    print("    (P5) defect == alpha_s/(N_quark N_pair) - alpha_s^2/(N_quark N_pair^3)")
    print("         leading 1/12, sub-leading 1/48 at (N_pair, N_quark) = (2, 6)")
    print("    (P6) defect^2 == 4 R_b^2 R_t^2 cos^2(alpha_bar) (law-of-cosines)")
    print("    Counterfactuals confirm (4 - alpha_s) coupling, lambda^2 = alpha_s/2,")
    print("    and rho_bar NLO form are individually load-bearing for (P4) exactness.")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
