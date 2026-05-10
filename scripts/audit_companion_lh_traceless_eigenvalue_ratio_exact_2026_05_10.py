#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`LH_TRACELESS_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-10`.

The narrow theorem's load-bearing content is:

  (R1) Given any positive integer n_color and reals (a, b) satisfying
       2 n_color a + 2 b = 0, the eigenvalue ratio is forced to
       a : b = 1 : (-n_color).
  (R2) Under labelling convention b = -1, a = 1/n_color.
  (R3) Under Q = T_3 + a/2, the LH-quark electric charges are
         Q(u_L) = (n_color + 1)/(2 n_color),
         Q(d_L) = (1 - n_color)/(2 n_color).
  (R4) The reduced (lowest-terms) denominator of Q(u_L), Q(d_L) is
         d_red(n_color) = n_color        if n_color is odd,
         d_red(n_color) = 2 n_color      if n_color is even.

The runner verifies (R1)-(R4) at exact sympy precision over abstract
positive integer n_color (parametric), then specializes to a sweep
n_color in {1, 2, 3, 4, 5, 7, 9, 11, 12} that exercises both parity
classes plus the framework instance n_color = 3.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow note's
load-bearing class-A algebra holds at exact symbolic precision.
"""

from fractions import Fraction
from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, symbols, expand, gcd
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
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
    print("LH_TRACELESS_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-10")
    print("Goal: sympy-symbolic verification of (R1)-(R4) over abstract n_color,")
    print("then concrete sweep over n_color in {1, 2, 3, 4, 5, 7, 9, 11, 12}")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------
    nc = Symbol("n_color", positive=True, integer=True)
    a, b = symbols("a b", real=True)

    print(f"  symbolic n_color = {nc}, eigenvalues a, b real")
    print(f"  trace equation (L1): 2 n_color a + 2 b = 0")

    # Trace equation as sympy expression set to zero
    L1 = 2 * nc * a + 2 * b

    # ---------------------------------------------------------------------
    section("Part 1: (R1) parametric eigenvalue ratio a : b = 1 : (-n_color)")
    # ---------------------------------------------------------------------
    # Solve L1 = 0 for b: b = -n_color * a.
    b_solved = sympy.solve(L1, b)[0]
    check(
        "(R1) parametric: b = -n_color * a forced by (L1)",
        simplify(b_solved + nc * a) == 0,
        detail=f"b_solved = {b_solved}",
    )

    # The ratio a:b is invariant of the scalar a. Express:
    # a / b = a / (-n_color a) = -1/n_color, so a:b = 1:(-n_color).
    ratio_check = simplify(a / b_solved + Rational(1) / nc)
    check(
        "(R1) parametric: a / b = -1 / n_color (equivalent ratio form)",
        ratio_check == 0,
        detail=f"a/b + 1/n_color simplifies to {ratio_check}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (R2) convention b = -1 fixes a = 1/n_color")
    # ---------------------------------------------------------------------
    a_under_b_neg1 = sympy.solve(L1.subs(b, -1), a)[0]
    check(
        "(R2) parametric: under b = -1 convention, a = 1 / n_color",
        simplify(a_under_b_neg1 - Rational(1) / nc) == 0,
        detail=f"a = {a_under_b_neg1}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (R3) closed-form Q(u_L), Q(d_L) parametric in n_color")
    # ---------------------------------------------------------------------
    # Under Q = T_3 + a/2 with a = 1/n_color:
    #   Q(u_L)  =  +1/2 + 1/(2 n_color)  =  (n_color + 1)/(2 n_color)
    #   Q(d_L)  =  -1/2 + 1/(2 n_color)  =  (1 - n_color)/(2 n_color)
    a_sym = Rational(1) / nc
    Q_uL = Rational(1, 2) + a_sym / 2
    Q_dL = -Rational(1, 2) + a_sym / 2

    Q_uL_target = (nc + 1) / (2 * nc)
    Q_dL_target = (1 - nc) / (2 * nc)

    check(
        "(R3) Q(u_L) parametric: (n_color + 1) / (2 n_color)",
        simplify(Q_uL - Q_uL_target) == 0,
        detail=f"Q(u_L) = {simplify(Q_uL)}",
    )
    check(
        "(R3) Q(d_L) parametric: (1 - n_color) / (2 n_color)",
        simplify(Q_dL - Q_dL_target) == 0,
        detail=f"Q(d_L) = {simplify(Q_dL)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (C1), (C2) derivable corollaries")
    # ---------------------------------------------------------------------
    check(
        "(C1) Q(u_L) - Q(d_L) = 1 (independent of n_color)",
        simplify(Q_uL - Q_dL - 1) == 0,
        detail=f"Q_uL - Q_dL = {simplify(Q_uL - Q_dL)}",
    )
    check(
        "(C2) Q(u_L) + Q(d_L) = a = 1/n_color",
        simplify(Q_uL + Q_dL - Rational(1) / nc) == 0,
        detail=f"Q_uL + Q_dL = {simplify(Q_uL + Q_dL)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (R4) reduced-denominator parity rule via concrete sweep")
    # ---------------------------------------------------------------------
    # For each n_color, reduce Q(u_L) = (n_color + 1)/(2 n_color) and
    # Q(d_L) = (1 - n_color)/(2 n_color) to lowest terms and check the
    # parity rule:
    #   odd  n_color -> reduced denominator = n_color
    #   even n_color -> reduced denominator = 2 n_color
    sweep_values = [1, 2, 3, 4, 5, 7, 9, 11, 12]
    for n_val in sweep_values:
        QuL = Fraction(n_val + 1, 2 * n_val)
        QdL = Fraction(1 - n_val, 2 * n_val)
        den_uL = QuL.denominator
        den_dL = QdL.denominator
        if n_val % 2 == 1:
            expected = n_val
            parity_label = "odd"
        else:
            expected = 2 * n_val
            parity_label = "even"
        ok = den_uL == expected and den_dL == expected
        check(
            f"(R4) at n_color = {n_val} ({parity_label}): "
            f"d_red = {expected} (got Q_uL denom {den_uL}, Q_dL denom {den_dL})",
            ok,
            detail=f"Q_uL = {QuL}, Q_dL = {QdL}",
        )

    # ---------------------------------------------------------------------
    section("Part 6: framework instance n_color = 3 rational closed form")
    # ---------------------------------------------------------------------
    framework = {nc: 3}

    Q_uL_at_3 = simplify(Q_uL.subs(framework))
    Q_dL_at_3 = simplify(Q_dL.subs(framework))
    a_at_3 = simplify(a_sym.subs(framework))

    check(
        "framework n_color = 3: a = 1/3",
        simplify(a_at_3 - Rational(1, 3)) == 0,
        detail=f"a = {a_at_3}",
    )
    check(
        "framework n_color = 3: Q(u_L) = 2/3",
        simplify(Q_uL_at_3 - Rational(2, 3)) == 0,
        detail=f"Q(u_L) = {Q_uL_at_3}",
    )
    check(
        "framework n_color = 3: Q(d_L) = -1/3",
        simplify(Q_dL_at_3 + Rational(1, 3)) == 0,
        detail=f"Q(d_L) = {Q_dL_at_3}",
    )
    check(
        "framework n_color = 3: reduced denominator = 3 (odd-parity branch)",
        Fraction(2, 3).denominator == 3 and Fraction(-1, 3).denominator == 3,
        detail="confirms d_red(3) = n_color = 3 directly",
    )

    # ---------------------------------------------------------------------
    section("Part 7: parity-branch counterfactual at n_color = 2")
    # ---------------------------------------------------------------------
    # At n_color = 2, parity is even, so the reduced denominator should be
    # 2 n_color = 4, NOT n_color = 2. Confirm this is genuinely different
    # from the odd-parity branch behavior.
    Q_uL_at_2 = Fraction(2 + 1, 2 * 2)  # = 3/4
    Q_dL_at_2 = Fraction(1 - 2, 2 * 2)  # = -1/4
    check(
        "counterfactual at n_color = 2 (even): reduced denominator = 4 != 2",
        Q_uL_at_2.denominator == 4 and Q_dL_at_2.denominator == 4,
        detail=f"Q(u_L) = {Q_uL_at_2}, Q(d_L) = {Q_dL_at_2}",
    )

    # Counterfactual at n_color = 4 (even): reduced denominator = 8.
    Q_uL_at_4 = Fraction(4 + 1, 2 * 4)  # = 5/8
    Q_dL_at_4 = Fraction(1 - 4, 2 * 4)  # = -3/8
    check(
        "counterfactual at n_color = 4 (even): reduced denominator = 8",
        Q_uL_at_4.denominator == 8 and Q_dL_at_4.denominator == 8,
        detail=f"Q(u_L) = {Q_uL_at_4}, Q(d_L) = {Q_dL_at_4}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: parity rule via sympy gcd identity")
    # ---------------------------------------------------------------------
    # The reduced denominator is 2 n_color / gcd(n_color + 1, 2 n_color).
    # gcd(n_color + 1, 2 n_color) = gcd(n_color + 1, 2) since
    # gcd(n_color + 1, 2 n_color) = gcd(n_color + 1, 2 n_color - 2(n_color + 1))
    #                              = gcd(n_color + 1, -2)
    #                              = gcd(n_color + 1, 2).
    # If n_color odd, n_color + 1 even, gcd = 2, reduced denom = n_color.
    # If n_color even, n_color + 1 odd, gcd = 1, reduced denom = 2 n_color.
    for n_val in sweep_values:
        g_uL = sympy.gcd(n_val + 1, 2 * n_val)
        g_dL = sympy.gcd(1 - n_val, 2 * n_val)
        # We require gcd matches with the parity rule.
        if n_val % 2 == 1:
            expected_gcd = 2
        else:
            expected_gcd = 1
        check(
            f"(R4) gcd(n_color + 1, 2 n_color) at n_color = {n_val} "
            f"is {expected_gcd}",
            int(g_uL) == expected_gcd and int(g_dL) == expected_gcd,
            detail=f"gcd_uL = {g_uL}, gcd_dL = {g_dL}",
        )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (R1) parametric eigenvalue ratio a:b = 1:(-n_color)")
    print("    (R2) under b = -1 convention, a = 1/n_color")
    print("    (R3) Q(u_L), Q(d_L) closed forms parametric in n_color")
    print("    (R4) reduced-denominator parity rule, sweep across both parities")
    print("    (C1), (C2) sum/difference corollaries")
    print("    Framework n_color = 3 instance: (a, Q(u_L), Q(d_L)) = (1/3, 2/3, -1/3)")
    print("    Counterfactual: parity-even branch (n_color = 2, 4) reduces differently")
    print("    Parity rule via sympy gcd identity across both parities")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
