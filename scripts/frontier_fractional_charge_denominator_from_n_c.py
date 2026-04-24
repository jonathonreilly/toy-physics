#!/usr/bin/env python3
"""
Fractional charge denominator = N_c theorem verification.

Verifies (★) and (★★) in
  docs/FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md

  (★)   Y(Q_L) : Y(L_L) = +1 : −N_c    (from tracelessness on C^{2N_c+2})
  (★★)  fractional charge denominator =
            N_c    if N_c is odd
            2 N_c  if N_c is even

For retained N_c = 3 (graph-first SU(3)), the SM third-integer charge spectrum
{0, ±1/3, ±2/3, ±1} is forced.

Authorities (all retained on main):
  - HYPERCHARGE_IDENTIFICATION_NOTE.md (6a + 2b = 0 ⇒ b = -3a)
  - STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE (denominators {1, 3})
  - GRAPH_FIRST_SU3_INTEGRATION_NOTE.md (N_c = 3)
  - SU2_WITTEN_Z2_ANOMALY_THEOREM (odd-N_c Witten requirement)
"""

from __future__ import annotations

import sys
from fractions import Fraction
from math import gcd

try:
    import sympy
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# --------------------------------------------------------------------------
# Hypercharge solver under tracelessness, parametrised by N_c
# --------------------------------------------------------------------------

def hypercharges_at_n_c(n_c: int) -> tuple:
    """
    Returns (Y_QL, Y_LL) such that:
      tracelessness: 2*N_c * Y_QL + 2 * Y_LL = 0
      convention: Y_LL = -1
    """
    Y_LL = Fraction(-1, 1)
    Y_QL = -Y_LL / n_c  # from N_c · a + b = 0, so a = -b/N_c
    return Y_QL, Y_LL


def electric_charges_at_n_c(n_c: int) -> dict:
    """
    Returns {field: Q} with Q = T_3 + Y/2 convention.
    """
    Y_QL, Y_LL = hypercharges_at_n_c(n_c)
    return {
        "u_L":  Fraction(1, 2) + Y_QL / 2,
        "d_L":  Fraction(-1, 2) + Y_QL / 2,
        "nu_L": Fraction(1, 2) + Y_LL / 2,
        "e_L":  Fraction(-1, 2) + Y_LL / 2,
    }


def fractional_denominator(charges: dict) -> int:
    """
    Returns the largest denominator across the non-zero charges.
    """
    denoms = [c.denominator for c in charges.values() if c != 0]
    return max(denoms) if denoms else 1


# --------------------------------------------------------------------------
# Part 0: tracelessness derivation at retained N_c = 3
# --------------------------------------------------------------------------

def part0_tracelessness_n_c_3() -> None:
    banner("Part 0: tracelessness on C^8 at retained N_c = 3")

    n_c = 3
    Y_QL, Y_LL = hypercharges_at_n_c(n_c)

    print(f"  N_c = {n_c}")
    print(f"  Quark multiplicity:   2 × N_c × 1 generation = {2*n_c}  fermions")
    print(f"  Lepton multiplicity:  2 × 1 × 1 generation   = 2  fermions")
    print(f"  Tracelessness:  {2*n_c} · Y_QL + 2 · Y_LL = 0")
    print(f"  ⟹ Y_QL = -Y_LL / N_c")
    print(f"  Convention Y_LL = -1 ⟹ Y_QL = +1/{n_c}")
    print()

    # Verify tracelessness
    trace = 2 * n_c * Y_QL + 2 * Y_LL
    check(
        "tracelessness 2 N_c · Y_QL + 2 · Y_LL = 0 at N_c = 3",
        trace == 0,
        f"trace = {trace}",
    )

    # Verify ratio (★)
    ratio = Y_QL / Y_LL
    expected_ratio = -Fraction(1, n_c)
    check(
        "(★) eigenvalue ratio Y(Q_L) : Y(L_L) = 1 : -N_c at retained N_c = 3",
        ratio == expected_ratio,
        f"ratio = {ratio} = -1/{n_c}",
    )

    # Verify Y values
    check(
        "Y(Q_L) = +1/3 (matches retained convention)",
        Y_QL == Fraction(1, 3),
        f"Y(Q_L) = {Y_QL}",
    )
    check(
        "Y(L_L) = -1 (convention)",
        Y_LL == Fraction(-1, 1),
        f"Y(L_L) = {Y_LL}",
    )


# --------------------------------------------------------------------------
# Part 1: electric-charge spectrum at retained N_c = 3
# --------------------------------------------------------------------------

def part1_electric_charges_n_c_3() -> None:
    banner("Part 1: electric-charge spectrum at retained N_c = 3")

    charges = electric_charges_at_n_c(3)

    print(f"  Q(u_L)  = {charges['u_L']}")
    print(f"  Q(d_L)  = {charges['d_L']}")
    print(f"  Q(ν_L)  = {charges['nu_L']}")
    print(f"  Q(e_L)  = {charges['e_L']}")
    print()

    expected_charges = {
        "u_L":  Fraction(2, 3),
        "d_L":  Fraction(-1, 3),
        "nu_L": Fraction(0),
        "e_L":  Fraction(-1, 1),
    }
    for field, expected in expected_charges.items():
        check(
            f"Q({field}) = {expected}",
            charges[field] == expected,
            f"actual = {charges[field]}",
        )

    # Spectrum check
    distinct = set(charges.values())
    expected_set = {Fraction(0), Fraction(2, 3), Fraction(-1, 3), Fraction(-1, 1)}
    check(
        "fermion-only spectrum = {0, 2/3, -1/3, -1}",
        distinct == expected_set,
        f"computed = {sorted(distinct, key=float)}",
    )

    # Denominator
    denom = fractional_denominator(charges)
    check(
        "(★★) fractional denominator = N_c = 3 at retained content",
        denom == 3,
        f"denominator = {denom}",
    )


# --------------------------------------------------------------------------
# Part 2: parity dependence — scan N_c
# --------------------------------------------------------------------------

def part2_n_c_scan() -> None:
    banner("Part 2: scan over N_c — parity dependence of denominator")

    print(f"  {'N_c':>4s}  {'parity':>6s}  {'Y(Q_L)':>8s}  {'Q(u_L)':>10s}  {'Q(d_L)':>10s}  {'denom':>5s}  {'expect = N_c?':>14s}")

    for n_c in range(1, 11):
        Y_QL, _ = hypercharges_at_n_c(n_c)
        charges = electric_charges_at_n_c(n_c)
        denom = fractional_denominator(charges)
        parity = "odd" if n_c % 2 == 1 else "even"
        expected_denom = n_c if n_c % 2 == 1 else 2 * n_c
        match = "✓" if denom == expected_denom else "✗"
        print(f"  {n_c:>4d}  {parity:>6s}  {str(Y_QL):>8s}  {str(charges['u_L']):>10s}  {str(charges['d_L']):>10s}  {denom:>5d}  {match:>14s}")

        check(
            f"N_c = {n_c} ({parity}): denominator = {expected_denom}",
            denom == expected_denom,
            f"computed = {denom}, expected = {expected_denom}",
        )


# --------------------------------------------------------------------------
# Part 3: joint constraint with Witten Z_2 anomaly
# --------------------------------------------------------------------------

def part3_witten_joint_constraint() -> None:
    banner("Part 3: joint constraint with Witten Z₂ anomaly cancellation")

    print(f"  {'N_c':>4s}  {'parity':>6s}  {'N_D = N_c+1':>12s}  {'Witten?':>8s}  {'frac. denom':>12s}")
    for n_c in range(1, 11):
        N_D = n_c + 1
        witten_ok = (N_D % 2 == 0)
        denom = fractional_denominator(electric_charges_at_n_c(n_c))
        parity = "odd" if n_c % 2 == 1 else "even"
        marker = "✓" if witten_ok else "✗"
        print(f"  {n_c:>4d}  {parity:>6s}  {N_D:>12d}  {marker:>8s}  {denom:>12d}")

    # Verify only odd N_c is Witten-consistent
    odd_witten = all((n_c + 1) % 2 == 0 for n_c in [1, 3, 5, 7, 9])
    even_witten = all((n_c + 1) % 2 == 1 for n_c in [2, 4, 6, 8])

    check(
        "Witten consistent only for odd N_c (N_c + 1 must be even)",
        odd_witten and even_witten,
        "verified across N_c = 1..9",
    )

    # Combined: Witten + denominator = N_c for retained N_c = 3
    n_c = 3
    n_d = n_c + 1
    denom_3 = fractional_denominator(electric_charges_at_n_c(n_c))
    check(
        "retained N_c = 3 satisfies BOTH Witten (N_D=4 even) AND denominator = N_c (=3)",
        (n_d % 2 == 0) and (denom_3 == 3),
        f"N_D = {n_d}, denominator = {denom_3}",
    )


# --------------------------------------------------------------------------
# Part 4: sympy symbolic verification
# --------------------------------------------------------------------------

def part4_sympy_symbolic() -> None:
    banner("Part 4: sympy symbolic verification")

    if not HAVE_SYMPY:
        print("  sympy not available; skipping symbolic verification")
        return

    N_c, Y_QL, Y_LL = sympy.symbols("N_c Y_QL Y_LL", real=True)

    # Tracelessness equation
    trace_eq = 2 * N_c * Y_QL + 2 * Y_LL  # = 0

    # Solve for Y_QL given Y_LL = -1
    solution = sympy.solve(trace_eq.subs(Y_LL, -1), Y_QL)
    print(f"  Symbolic solution for Y_QL given Y_LL = -1: Y_QL = {solution[0]}")

    Y_QL_sym = solution[0]
    expected_sym = sympy.Rational(1, 1) / N_c
    check(
        "sympy: Y_QL = 1/N_c symbolically",
        sympy.simplify(Y_QL_sym - expected_sym) == 0,
        f"Y_QL = {Y_QL_sym}",
    )

    # Specialise to N_c = 3
    Y_QL_at_3 = Y_QL_sym.subs(N_c, 3)
    check(
        "sympy: at N_c = 3, Y_QL = 1/3",
        Y_QL_at_3 == sympy.Rational(1, 3),
        f"Y_QL at N_c=3 = {Y_QL_at_3}",
    )

    # Electric charge formulas
    Q_uL = sympy.Rational(1, 2) + Y_QL_sym / 2  # T_3 = +1/2 for u_L
    Q_dL = sympy.Rational(-1, 2) + Y_QL_sym / 2

    Q_uL_at_3 = Q_uL.subs(N_c, 3)
    Q_dL_at_3 = Q_dL.subs(N_c, 3)
    check(
        "sympy: Q(u_L) at N_c = 3 simplifies to 2/3",
        Q_uL_at_3 == sympy.Rational(2, 3),
        f"Q(u_L) = {Q_uL_at_3}",
    )
    check(
        "sympy: Q(d_L) at N_c = 3 simplifies to -1/3",
        Q_dL_at_3 == sympy.Rational(-1, 3),
        f"Q(d_L) = {Q_dL_at_3}",
    )


# --------------------------------------------------------------------------
# Part 5: structural form (N_c + 1)/(2 N_c) reduction
# --------------------------------------------------------------------------

def part5_reduction_structure() -> None:
    banner("Part 5: structural reduction (N_c + 1)/(2 N_c)")

    print(f"  Q(u_L) = (N_c + 1) / (2 N_c)")
    print(f"  Reduction depends on gcd(N_c + 1, 2 N_c)")
    print()

    print(f"  {'N_c':>4s}  {'(N_c+1)/(2N_c)':>17s}  {'gcd':>4s}  {'reduced':>10s}  {'denom':>6s}")
    for n_c in range(1, 11):
        unreduced_num = n_c + 1
        unreduced_den = 2 * n_c
        g = gcd(unreduced_num, unreduced_den)
        reduced_frac = Fraction(unreduced_num, unreduced_den)
        print(f"  {n_c:>4d}  {unreduced_num:>4d}/{unreduced_den:<8d}  {g:>4d}  {str(reduced_frac):>10s}  {reduced_frac.denominator:>6d}")

    # Verify gcd pattern
    for n_c in [1, 3, 5, 7]:
        g = gcd(n_c + 1, 2 * n_c)
        check(
            f"N_c = {n_c} (odd): gcd(N_c+1, 2 N_c) = 2 (since N_c+1 even)",
            g == 2,
            f"gcd = {g}",
        )

    for n_c in [2, 4, 6, 8]:
        g = gcd(n_c + 1, 2 * n_c)
        check(
            f"N_c = {n_c} (even): gcd(N_c+1, 2 N_c) = 1 (since N_c+1 odd, 2 N_c even)",
            g == 1,
            f"gcd = {g}",
        )


# --------------------------------------------------------------------------
# Part 6: cross-check with retained ν_R and SM hypercharges
# --------------------------------------------------------------------------

def part6_sm_cross_check() -> None:
    banner("Part 6: cross-check with retained SM hypercharges + Q convention")

    # At N_c = 3, this theorem gives Y(Q_L) = 1/3, Y(L_L) = -1.
    # The retained SM_HYPERCHARGE_UNIQUENESS gives RH values: y_1 = 4/3, y_2 = -2/3, y_3 = -2, y_4 = 0.
    # Verify electric charges match:

    Y_QL = Fraction(1, 3)
    Y_LL = Fraction(-1, 1)
    Y_uR = Fraction(4, 3)
    Y_dR = Fraction(-2, 3)
    Y_eR = Fraction(-2, 1)
    Y_nuR = Fraction(0)

    # Electric charges: Q = T_3 + Y/2 for doublets; Q = Y/2 for singlets (T_3 = 0)
    Q = {
        "u_L":  Fraction(1, 2) + Y_QL / 2,
        "d_L":  Fraction(-1, 2) + Y_QL / 2,
        "nu_L": Fraction(1, 2) + Y_LL / 2,
        "e_L":  Fraction(-1, 2) + Y_LL / 2,
        "u_R":  Y_uR / 2,
        "d_R":  Y_dR / 2,
        "e_R":  Y_eR / 2,
        "nu_R": Y_nuR / 2,
    }

    print(f"  Field charges from this theorem + retained RH hypercharges:")
    for field, q in Q.items():
        print(f"    Q({field}) = {q}")
    print()

    expected = {
        "u_L":  Fraction(2, 3),
        "d_L":  Fraction(-1, 3),
        "nu_L": Fraction(0),
        "e_L":  Fraction(-1, 1),
        "u_R":  Fraction(2, 3),
        "d_R":  Fraction(-1, 3),
        "e_R":  Fraction(-1, 1),
        "nu_R": Fraction(0),
    }
    for field, expected_q in expected.items():
        check(
            f"Q({field}) = {expected_q}",
            Q[field] == expected_q,
            f"actual = {Q[field]}",
        )

    # All denominators in {1, 3}
    distinct_denoms = {q.denominator for q in Q.values() if q != 0}
    check(
        "all non-zero charge denominators in {1, 3} = {1, N_c} for retained N_c = 3",
        distinct_denoms <= {1, 3},
        f"denominators = {sorted(distinct_denoms)}",
    )


# --------------------------------------------------------------------------
# Part 7: summary
# --------------------------------------------------------------------------

def part7_summary() -> None:
    banner("Part 7: summary - fractional charge denominator from N_c retained")

    print("  THEOREM:")
    print("    (★)  Tracelessness on C^{2 N_c + 2} forces Y(Q_L) : Y(L_L) = +1 : -N_c")
    print("    (★★) Fractional charge denominator =")
    print("           N_c    if N_c is odd")
    print("           2 N_c  if N_c is even")
    print()
    print("  RETAINED N_c = 3 (graph-first SU(3)):")
    print("    Y(Q_L) = +1/3, Y(L_L) = -1")
    print("    Q(u_L) = +2/3, Q(d_L) = -1/3, Q(ν_L) = 0, Q(e_L) = -1")
    print("    Fractional denominator = 3 = N_c")
    print("    SM third-integer charges {0, ±1/3, ±2/3, ±1} forced.")
    print()
    print("  JOINT WITH WITTEN Z_2:")
    print("    Witten consistent ⟺ N_c odd")
    print("    On consistent set, denominator = N_c always")
    print("    Retained N_c = 3 doubly forced (Witten + clean denominator)")
    print()
    print("  STRUCTURAL CONSEQUENCES:")
    print("    - SM 'third-integer' fractional charges are an N_c = 3 imprint")
    print("    - Hypothetical N_c = 2: even N_c → 'quarter-integer' denominators")
    print("    - Hypothetical N_c = 5: odd → 'fifth-integer' denominators (also clean)")
    print()
    print("  DOES NOT CLAIM:")
    print("    - Native-axiom uniqueness of N_c = 3 (separate retained theorem)")
    print("    - RH hypercharges (covered in SM_HYPERCHARGE_UNIQUENESS)")
    print("    - Beyond-SM extensions (e.g., multi-Higgs, additional U(1)s)")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    print("=" * 88)
    print("Fractional charge denominator from N_c theorem verification")
    print("See docs/FRACTIONAL_CHARGE_DENOMINATOR_FROM_N_C_THEOREM_NOTE_2026-04-24.md")
    print("=" * 88)

    part0_tracelessness_n_c_3()
    part1_electric_charges_n_c_3()
    part2_n_c_scan()
    part3_witten_joint_constraint()
    part4_sympy_symbolic()
    part5_reduction_structure()
    part6_sm_cross_check()
    part7_summary()

    print()
    print("=" * 88)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
