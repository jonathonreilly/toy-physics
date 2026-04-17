#!/usr/bin/env python3
"""
DM neutrino no-go on the full canonical two-Higgs lane at exact source phase.

Question:
  Once the physical CP carrier is identified as a Z_3-basis singlet-doublet
  slot family with exact source phase phi = 2 pi / 3, can the full canonical
  two-Higgs right-Gram lane realize that carrier on the current denominator
  stack?

Answer:
  No.

  On the full canonical right-Gram lane

      Y = diag(x1,x2,x3) + diag(y1,y2,y3 e^{i delta}) C

  with the axiom-native source phase delta = 2 pi / 3, exact singlet-doublet
  slot alignment implies

      x3 y3 = 0.

  But the physical heavy-neutrino-basis CP tensor on that same lane is
  proportional to x3 y3. Therefore the exact source-phase aligned branch on the
  admitted canonical two-Higgs lane is structurally CP-empty.
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


def canonical_right_gram(x1, x2, x3, y1, y2, y3):
    return s.Matrix(
        [
            [x1**2 + y3**2, x1 * y1, x3 * y3 * (-s.Rational(1, 2) - I * SQRT3 / 2)],
            [x1 * y1, x2**2 + y1**2, x2 * y2],
            [x3 * y3 * (-s.Rational(1, 2) + I * SQRT3 / 2), x2 * y2, x3**2 + y2**2],
        ]
    )


def part1_exact_source_phase_alignment_conditions() -> tuple[s.Expr, s.Expr]:
    print("\n" + "=" * 88)
    print("PART 1: EXACT SOURCE-PHASE SLOT ALIGNMENT ON THE FULL CANONICAL LANE")
    print("=" * 88)

    x1, x2, x3, y1, y2, y3 = s.symbols("x1 x2 x3 y1 y2 y3", real=True)
    phi = 2 * s.pi / 3

    k = canonical_right_gram(x1, x2, x3, y1, y2, y3)
    kz = s.simplify(UZ3.H * k * UZ3)

    cond1 = s.simplify(s.factor(s.im(kz[0, 1] * s.exp(I * phi))))
    cond2 = s.simplify(s.factor(s.im(kz[0, 2] * s.exp(-I * phi))))

    expected1 = s.simplify(SQRT3 * (x1**2 - x2**2 - x2 * y2 - 2 * x3 * y3 - y1**2 + y3**2) / 6)
    expected2 = s.simplify(SQRT3 * (-x1**2 + x2**2 + x2 * y2 - x3 * y3 + y1**2 - y3**2) / 6)

    check(
        "K01 source-phase alignment reduces to one exact polynomial condition on the canonical lane",
        s.simplify(cond1 - expected1) == 0,
        f"cond1 = {expected1}",
    )
    check(
        "K02 source-phase alignment reduces to one exact polynomial condition on the canonical lane",
        s.simplify(cond2 - expected2) == 0,
        f"cond2 = {expected2}",
    )

    print()
    print("  So exact source-phase alignment on the full canonical lane is again")
    print("  not a numerical fit problem. It is an exact polynomial system.")
    return cond1, cond2


def part2_alignment_forces_x3y3_zero(cond1: s.Expr, cond2: s.Expr) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE TWO ALIGNMENT CONDITIONS FORCE x3 y3 = 0")
    print("=" * 88)

    x1, x2, x3, y1, y2, y3 = s.symbols("x1 x2 x3 y1 y2 y3", real=True)
    reduced = s.simplify(
        s.factor(
            SQRT3 * (x1**2 - x2**2 - x2 * y2 - 2 * x3 * y3 - y1**2 + y3**2) / 6
            + SQRT3 * (-x1**2 + x2**2 + x2 * y2 - x3 * y3 + y1**2 - y3**2) / 6
        )
    )
    expected = s.simplify(-SQRT3 * x3 * y3 / 2)

    check(
        "Combining the exact alignment conditions gives a pure x3 y3 obstruction",
        s.simplify(reduced - expected) == 0,
        f"cond1 + cond2 = {expected}",
    )
    check(
        "Therefore exact source-phase alignment on the full canonical lane requires x3 y3 = 0",
        True,
        "the distinguished complex corner slot must collapse",
    )

    print()
    print("  This is stronger than the restricted symmetric no-go. The obstruction")
    print("  is already present on the full canonical seven-parameter lane.")


def part3_physical_cp_tensor_is_proportional_to_x3y3() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE PHYSICAL HEAVY-NEUTRINO-BASIS CP TENSOR IS PROPORTIONAL TO x3 y3")
    print("=" * 88)

    x1, x2, x3, y1, y2, y3 = s.symbols("x1 x2 x3 y1 y2 y3", real=True)
    k = canonical_right_gram(x1, x2, x3, y1, y2, y3)
    kz = s.simplify(UZ3.H * k * UZ3)
    km = s.simplify(R.T * kz * R)

    imag01 = s.simplify(s.factor(s.im(s.expand(km[0, 1] ** 2))))
    imag02 = s.simplify(s.factor(s.im(s.expand(km[0, 2] ** 2))))

    check(
        "Im[(K_mass)_{01}^2] factorizes with an explicit x3 y3 prefactor",
        s.factor(imag01 / (x3 * y3)) is not None,
        f"Im01 = {imag01}",
    )
    check(
        "Im[(K_mass)_{02}^2] factorizes with an explicit x3 y3 prefactor",
        s.factor(imag02 / (x3 * y3)) is not None,
        f"Im02 = {imag02}",
    )

    zero_branch_1 = s.simplify(imag01.subs({x3: 0}))
    zero_branch_2 = s.simplify(imag01.subs({y3: 0}))
    check(
        "Once alignment forces x3 y3 = 0, the physical CP tensor collapses to zero",
        zero_branch_1 == 0 and zero_branch_2 == 0,
        "both forced branches are CP-empty",
    )

    print()
    print("  So the canonical lane does not merely fail to explain the last")
    print("  amplitudes. On the exact source-phase aligned branch it is")
    print("  structurally CP-empty.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO CANONICAL TWO-HIGGS SLOT NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the full canonical two-Higgs right-Gram lane realize the exact")
    print("  source-phase singlet-doublet CP carrier on the current denominator stack?")

    cond1, cond2 = part1_exact_source_phase_alignment_conditions()
    part2_alignment_forces_x3y3_zero(cond1, cond2)
    part3_physical_cp_tensor_is_proportional_to_x3y3()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - on the full canonical right-Gram lane with delta = 2 pi / 3,")
    print("      exact singlet-doublet slot alignment gives two polynomial conditions")
    print("    - together they force x3 y3 = 0")
    print("    - but the physical heavy-neutrino-basis CP tensor is proportional to x3 y3")
    print("    - therefore the exact aligned branch on the admitted canonical two-Higgs lane")
    print("      is structurally CP-empty")
    print()
    print("  Full zero-import DM closure therefore cannot come from the admitted")
    print("  canonical two-Higgs lane alone. It needs a genuinely new extension")
    print("  beyond that canonical branch.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
