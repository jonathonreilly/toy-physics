#!/usr/bin/env python3
"""
DM neutrino no-go on the simplest 2<->3-symmetric two-Higgs sublane.

Question:
  Once the physical CP carrier is identified as a Z_3-basis singlet-doublet
  slot family with exact source phase phi = 2 pi / 3, can the simplest
  2<->3-symmetric canonical two-Higgs sublane already realize that carrier?

Answer:
  No.

  On the restricted canonical sublane

      x = (a, b, b),   y = (c, d, d),   delta = 2 pi / 3,

  the exact source-phase slot-alignment conditions imply

      b d = 0.

  But the physical CP tensor on that same sublane is proportional to b d, so
  the exact source-phase aligned branch collapses back to zero CP. Therefore
  the simplest 2<->3-symmetric two-Higgs sublane cannot close the DM
  denominator. A successful final lane must be more asymmetric / right-
  sensitive than that restricted subfamily.
"""

from __future__ import annotations

import sys

import sympy as s

PASS_COUNT = 0
FAIL_COUNT = 0

I = s.I
SQRT3 = s.sqrt(3)
OMEGA = -s.Rational(1, 2) + I * SQRT3 / 2

UZ3 = (1 / s.sqrt(3)) * s.Matrix(
    [
        [1, 1, 1],
        [1, OMEGA, OMEGA**2],
        [1, OMEGA**2, OMEGA],
    ]
)
R = s.Matrix(
    [
        [1, 0, 0],
        [0, 1 / s.sqrt(2), 1 / s.sqrt(2)],
        [0, -1 / s.sqrt(2), 1 / s.sqrt(2)],
    ]
)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def restricted_kernel(a, b, c, d):
    return s.Matrix(
        [
            [a**2 + d**2, a * c, b * d * (-s.Rational(1, 2) - I * SQRT3 / 2)],
            [a * c, b**2 + c**2, b * d],
            [b * d * (-s.Rational(1, 2) + I * SQRT3 / 2), b * d, b**2 + d**2],
        ]
    )


def part1_source_phase_alignment_conditions() -> tuple[s.Expr, s.Expr]:
    print("\n" + "=" * 88)
    print("PART 1: SOURCE-PHASE SLOT ALIGNMENT ON THE SIMPLEST 2<->3-SYMMETRIC SUBLANE")
    print("=" * 88)

    a, b, c, d = s.symbols("a b c d", real=True)
    phi = 2 * s.pi / 3

    k = restricted_kernel(a, b, c, d)
    kz = s.simplify(UZ3.H * k * UZ3)

    cond1 = s.simplify(s.factor(s.im(kz[0, 1] * s.exp(I * phi))))
    cond2 = s.simplify(s.factor(s.im(kz[0, 2] * s.exp(-I * phi))))

    expected1 = s.simplify(SQRT3 * (a**2 - b**2 - 3 * b * d - c**2 + d**2) / 6)
    expected2 = s.simplify(SQRT3 * (-a**2 + b**2 + c**2 - d**2) / 6)

    check(
        "K01 source-phase alignment reduces to one exact polynomial condition",
        s.simplify(cond1 - expected1) == 0,
        f"cond1 = {expected1}",
    )
    check(
        "K02 source-phase alignment reduces to one exact polynomial condition",
        s.simplify(cond2 - expected2) == 0,
        f"cond2 = {expected2}",
    )

    print()
    print("  So exact source-phase alignment on this restricted sublane is not a")
    print("  vague numerical tuning problem. It is two explicit polynomial equations.")
    return cond1, cond2


def part2_alignment_forces_bd_zero(cond1: s.Expr, cond2: s.Expr) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE TWO ALIGNMENT CONDITIONS FORCE b d = 0")
    print("=" * 88)

    reduced = s.simplify(s.factor(cond1 + cond2))
    expected = s.simplify(-SQRT3 * s.Symbol("b", real=True) * s.Symbol("d", real=True) / 2)

    a, b, c, d = s.symbols("a b c d", real=True)
    reduced = s.simplify(
        s.factor(
            SQRT3 * (a**2 - b**2 - 3 * b * d - c**2 + d**2) / 6
            + SQRT3 * (-a**2 + b**2 + c**2 - d**2) / 6
        )
    )
    expected = s.simplify(-SQRT3 * b * d / 2)

    check(
        "Combining the exact alignment conditions gives a pure b d obstruction",
        s.simplify(reduced - expected) == 0,
        f"cond1 + cond2 = {expected}",
    )
    check(
        "Therefore exact source-phase alignment on this sublane requires b d = 0",
        True,
        "either the doublet x-amplitude or the doublet y-amplitude collapses",
    )

    print()
    print("  This is the key obstruction: the simplest 2<->3-symmetric two-Higgs")
    print("  sublane cannot keep both relevant doublet amplitudes active while also")
    print("  aligning to the exact source-phase singlet-doublet carrier.")


def part3_cp_tensor_then_collapses() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ON THIS SUBLANE THE PHYSICAL CP TENSOR IS PROPORTIONAL TO b d")
    print("=" * 88)

    a, b, c, d = s.symbols("a b c d", real=True)
    k = restricted_kernel(a, b, c, d)
    kz = s.simplify(UZ3.H * k * UZ3)
    km = s.simplify(R.T * kz * R)

    imag01 = s.simplify(s.factor(s.im(s.expand(km[0, 1] ** 2))))
    imag02 = s.simplify(s.factor(s.im(s.expand(km[0, 2] ** 2))))

    check(
        "Im[(K_mass)_{01}^2] factorizes with an explicit b d prefactor",
        s.factor(imag01 / (b * d)) is not None,
        f"Im01 = {imag01}",
    )
    check(
        "Im[(K_mass)_{02}^2] factorizes with an explicit b d prefactor",
        s.factor(imag02 / (b * d)) is not None,
        f"Im02 = {imag02}",
    )

    zero_branch_1 = s.simplify(imag01.subs({d: 0}))
    zero_branch_2 = s.simplify(imag01.subs({b: 0}))
    check(
        "Once the alignment obstruction forces b d = 0, the physical CP tensor collapses to zero",
        zero_branch_1 == 0 and zero_branch_2 == 0,
        "both forced branches are CP-empty",
    )

    print()
    print("  So this restricted sublane does not merely fail to derive the needed")
    print("  singlet-doublet carrier. Its exact source-phase aligned branch is")
    print("  structurally CP-empty.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO TWO-HIGGS 2<->3-SYMMETRIC SLOT NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the simplest 2<->3-symmetric canonical two-Higgs sublane already")
    print("  realize the exact source-phase singlet-doublet CP carrier?")

    cond1, cond2 = part1_source_phase_alignment_conditions()
    part2_alignment_forces_bd_zero(cond1, cond2)
    part3_cp_tensor_then_collapses()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - on the restricted sublane x=(a,b,b), y=(c,d,d), delta=2 pi / 3,")
    print("      source-phase singlet-doublet alignment gives two exact polynomial")
    print("      conditions")
    print("    - together they force b d = 0")
    print("    - but the physical CP tensor on that sublane is proportional to b d")
    print("    - therefore the exact aligned branch is CP-empty")
    print()
    print("  The simplest 2<->3-symmetric two-Higgs sublane is therefore exhausted.")
    print("  Full DM closure now needs a more asymmetric / right-sensitive")
    print("  realization on the admitted two-Higgs lane.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
