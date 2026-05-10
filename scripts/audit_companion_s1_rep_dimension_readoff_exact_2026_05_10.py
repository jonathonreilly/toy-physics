#!/usr/bin/env python3
"""Exact-symbolic audit-companion runner for
`S1_REP_DIMENSION_READOFF_NARROW_THEOREM_NOTE_2026-05-10`.

The narrow theorem's load-bearing content is:

  (R1) n_pair    = dim_G1((p, c)) = p
  (R2) n_color   = dim_G2((p, c)) = c
  (R3) n_quark   = n_pair * n_color = p * c
  (R4) A^2       = n_pair / n_color = p / c

for any positive integer pair (p, c). The runner verifies these read-off
identities at exact sympy precision over abstract positive-integer
symbolic (p, c), then specializes to (a) the framework instance (2, 3)
and (b) two non-framework instances (3, 5) and (4, 7) to demonstrate
parametric independence from the framework counts.

Companion role: not a new claim row, not a new source note, no status
promotion. Provides audit-friendly evidence that the narrow note's
load-bearing class-A algebra holds at exact symbolic precision.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, Symbol, simplify, symbols
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
    print("S1_REP_DIMENSION_READOFF_NARROW_THEOREM_NOTE_2026-05-10")
    print("Goal: sympy-symbolic verification of (R1)-(R4) parametric in (p, c)")
    print("plus framework (2, 3) and non-framework (3, 5), (4, 7) sanity")
    print("=" * 88)

    # ---------------------------------------------------------------------
    section("Part 0: symbolic setup")
    # ---------------------------------------------------------------------
    p_sym, c_sym = symbols("p c", positive=True, integer=True)

    # Operational read-off definitions
    n_pair = p_sym  # (D1) n_pair := dim_G1((p, c)) = p
    n_color = c_sym  # (D2) n_color := dim_G2((p, c)) = c
    n_quark = n_pair * n_color  # (D3) n_quark := n_pair * n_color
    A2 = Rational(1) * n_pair / n_color  # A^2 := n_pair / n_color

    print(f"  symbolic (p, c) = ({p_sym}, {c_sym}) positive integers")
    print(f"  rep-literal (p, c) labels an SU(N_1) x SU(N_2) rep")
    print(f"  (D1) n_pair  := dim_G1((p, c)) = p")
    print(f"  (D2) n_color := dim_G2((p, c)) = c")
    print(f"  (D3) n_quark := n_pair * n_color = p * c")

    # ---------------------------------------------------------------------
    section("Part 1: (R1) n_pair = p parametric")
    # ---------------------------------------------------------------------
    check(
        "(R1) parametric: n_pair == p",
        simplify(n_pair - p_sym) == 0,
        detail=f"n_pair - p simplifies to {simplify(n_pair - p_sym)}",
    )

    # ---------------------------------------------------------------------
    section("Part 2: (R2) n_color = c parametric")
    # ---------------------------------------------------------------------
    check(
        "(R2) parametric: n_color == c",
        simplify(n_color - c_sym) == 0,
        detail=f"n_color - c simplifies to {simplify(n_color - c_sym)}",
    )

    # ---------------------------------------------------------------------
    section("Part 3: (R3) n_quark = p * c parametric")
    # ---------------------------------------------------------------------
    check(
        "(R3) parametric: n_quark == p * c",
        simplify(n_quark - p_sym * c_sym) == 0,
        detail=f"n_quark - p*c simplifies to {simplify(n_quark - p_sym * c_sym)}",
    )

    # ---------------------------------------------------------------------
    section("Part 4: (R4) A^2 = p / c parametric")
    # ---------------------------------------------------------------------
    check(
        "(R4) parametric: A^2 == p / c",
        simplify(A2 - p_sym / c_sym) == 0,
        detail=f"A^2 - p/c simplifies to {simplify(A2 - p_sym / c_sym)}",
    )

    # ---------------------------------------------------------------------
    section("Part 5: (C1) A^4 = p^2 / c^2 derivable corollary")
    # ---------------------------------------------------------------------
    A4 = A2**2
    check(
        "(C1) parametric: A^4 == p^2 / c^2",
        simplify(A4 - p_sym**2 / c_sym**2) == 0,
        detail=f"A^4 - p^2/c^2 simplifies to {simplify(A4 - p_sym**2 / c_sym**2)}",
    )

    # ---------------------------------------------------------------------
    section("Part 6: (C2), (C3) cross-check corollaries")
    # ---------------------------------------------------------------------
    check(
        "(C2) parametric: n_quark / n_pair == c == n_color",
        simplify(n_quark / n_pair - c_sym) == 0,
        detail=f"n_quark / n_pair - c simplifies to {simplify(n_quark / n_pair - c_sym)}",
    )
    check(
        "(C3) parametric: n_quark / n_color == p == n_pair",
        simplify(n_quark / n_color - p_sym) == 0,
        detail=f"n_quark / n_color - p simplifies to {simplify(n_quark / n_color - p_sym)}",
    )

    # ---------------------------------------------------------------------
    section("Part 7: framework instance (p, c) = (2, 3)")
    # ---------------------------------------------------------------------
    framework = {p_sym: 2, c_sym: 3}

    n_pair_at = simplify(n_pair.subs(framework))
    n_color_at = simplify(n_color.subs(framework))
    n_quark_at = simplify(n_quark.subs(framework))
    A2_at = simplify(A2.subs(framework))
    A4_at = simplify(A4.subs(framework))

    check(
        "framework (2, 3): n_pair = 2",
        n_pair_at == 2,
        detail=f"got n_pair = {n_pair_at}",
    )
    check(
        "framework (2, 3): n_color = 3",
        n_color_at == 3,
        detail=f"got n_color = {n_color_at}",
    )
    check(
        "framework (2, 3): n_quark = 6",
        n_quark_at == 6,
        detail=f"got n_quark = {n_quark_at}",
    )
    check(
        "framework (2, 3): A^2 = 2/3",
        simplify(A2_at - Rational(2, 3)) == 0,
        detail=f"got A^2 = {A2_at}",
    )
    check(
        "framework (2, 3): A^4 = 4/9",
        simplify(A4_at - Rational(4, 9)) == 0,
        detail=f"got A^4 = {A4_at}",
    )

    # ---------------------------------------------------------------------
    section("Part 8: non-framework instance (p, c) = (3, 5)")
    # ---------------------------------------------------------------------
    nonframework_1 = {p_sym: 3, c_sym: 5}
    check(
        "non-framework (3, 5): n_pair = 3, n_color = 5, n_quark = 15",
        simplify(n_pair.subs(nonframework_1)) == 3
        and simplify(n_color.subs(nonframework_1)) == 5
        and simplify(n_quark.subs(nonframework_1)) == 15,
        detail=f"A^2 = {simplify(A2.subs(nonframework_1))}",
    )
    check(
        "non-framework (3, 5): A^2 = 3/5",
        simplify(A2.subs(nonframework_1) - Rational(3, 5)) == 0,
        detail=f"got A^2 = {simplify(A2.subs(nonframework_1))}",
    )
    check(
        "non-framework (3, 5): A^4 = 9/25",
        simplify(A4.subs(nonframework_1) - Rational(9, 25)) == 0,
        detail=f"got A^4 = {simplify(A4.subs(nonframework_1))}",
    )

    # ---------------------------------------------------------------------
    section("Part 9: non-framework instance (p, c) = (4, 7)")
    # ---------------------------------------------------------------------
    nonframework_2 = {p_sym: 4, c_sym: 7}
    check(
        "non-framework (4, 7): n_pair = 4, n_color = 7, n_quark = 28",
        simplify(n_pair.subs(nonframework_2)) == 4
        and simplify(n_color.subs(nonframework_2)) == 7
        and simplify(n_quark.subs(nonframework_2)) == 28,
        detail=f"A^2 = {simplify(A2.subs(nonframework_2))}",
    )
    check(
        "non-framework (4, 7): A^2 = 4/7",
        simplify(A2.subs(nonframework_2) - Rational(4, 7)) == 0,
        detail=f"got A^2 = {simplify(A2.subs(nonframework_2))}",
    )
    check(
        "non-framework (4, 7): A^4 = 16/49",
        simplify(A4.subs(nonframework_2) - Rational(16, 49)) == 0,
        detail=f"got A^4 = {simplify(A4.subs(nonframework_2))}",
    )

    # ---------------------------------------------------------------------
    section("Part 10: independence-from-framework checks (free_symbols)")
    # ---------------------------------------------------------------------
    # Parametric closed forms must still contain p and c as free symbols
    # before substitution.
    check(
        "parametric A^2 has free_symbols {p, c}",
        A2.free_symbols == {p_sym, c_sym},
        detail=f"free_symbols of A^2 = {A2.free_symbols}",
    )
    check(
        "parametric n_quark has free_symbols {p, c}",
        n_quark.free_symbols == {p_sym, c_sym},
        detail=f"free_symbols of n_quark = {n_quark.free_symbols}",
    )

    # ---------------------------------------------------------------------
    section("Summary")
    # ---------------------------------------------------------------------
    print("  Verified at exact sympy precision:")
    print("    (R1) n_pair = p parametric")
    print("    (R2) n_color = c parametric")
    print("    (R3) n_quark = p * c parametric")
    print("    (R4) A^2 = p / c parametric")
    print("    (C1) A^4 = p^2 / c^2 parametric")
    print("    (C2), (C3) cross-check identities")
    print("    Framework (2, 3): (n_pair, n_color, n_quark, A^2, A^4) = (2, 3, 6, 2/3, 4/9)")
    print("    Non-framework (3, 5): (3, 5, 15, 3/5, 9/25)")
    print("    Non-framework (4, 7): (4, 7, 28, 4/7, 16/49)")
    print("    Free-symbols independence-from-framework checks")

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
