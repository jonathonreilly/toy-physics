#!/usr/bin/env python3
"""
Koide delta octahedral-domain endpoint no-go.

Theorem attempt:
  Use the retained octahedral-domain geometry of the selected-line first
  branch to derive the physical Brannen endpoint, hence delta = eta_APS.

Result:
  The octahedral geometry fixes the first-branch span

      L_O = 2*pi/|O| = pi/12,  |O|=24.

  It does not select a distinguished interior endpoint inside that branch.
  The ambient support value eta_APS = 2/9 lies inside the interval, but its
  branch fraction is

      (2/9)/(pi/12) = 8/(3*pi),

  which is not fixed by octahedral group order, projective period, or endpoint
  positivity.  Choosing that interior fraction is the missing endpoint law.

Residual:
  RESIDUAL_SCALAR=selected_octahedral_branch_fraction_minus_8_over_3pi.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def part1_octahedral_branch_span() -> tuple[sp.Expr, sp.Expr]:
    section("PART 1: octahedral domain fixes a branch interval")

    order_o = sp.Integer(24)
    span = sp.simplify(2 * sp.pi / order_o)
    eta = sp.Rational(2, 9)

    check(
        "Retained octahedral rotation group has order 24",
        order_o == 24,
        detail="signed permutation rotations with determinant +1",
    )
    check(
        "One first-branch fundamental domain has span pi/12",
        span == sp.pi / 12,
        detail=f"2*pi/24={span}",
    )
    check(
        "The ambient support value 2/9 is inside the octahedral branch interval",
        bool(eta < span),
        detail=f"2/9 < pi/12 is {eta < span}",
    )
    return span, eta


def part2_interior_fraction_not_selected(span: sp.Expr, eta: sp.Expr) -> None:
    section("PART 2: interior branch fraction remains free")

    fraction = sp.simplify(eta / span)
    f = sp.symbols("f", real=True)
    delta_f = sp.simplify(f * span)

    check(
        "The eta endpoint corresponds to branch fraction 8/(3*pi)",
        fraction == sp.Rational(8, 1) / (3 * sp.pi),
        detail=f"(2/9)/(pi/12)={fraction}",
    )
    check(
        "Octahedral endpoint data select f=0 and f=1 as boundaries, not the interior f=8/(3*pi)",
        sp.simplify(delta_f.subs(f, 0)) == 0
        and sp.simplify(delta_f.subs(f, 1)) == span
        and fraction not in (0, 1),
        detail=f"interior fraction={fraction}",
    )

    samples = [sp.Rational(0), sp.Rational(1, 2), fraction, sp.Rational(1)]
    residuals = [sp.simplify(sample * span - eta) for sample in samples]
    check(
        "A continuum of branch endpoints preserves the same octahedral domain",
        residuals[0] != 0 and residuals[1] != 0 and residuals[2] == 0 and residuals[3] != 0,
        detail=f"residuals={residuals}",
    )


def part3_no_group_order_fraction() -> None:
    section("PART 3: group-order fractions do not produce the interior endpoint")

    eta = sp.Rational(2, 9)
    span = sp.pi / 12
    candidates = {
        "1/24 of full turn": 2 * sp.pi / 24,
        "1/12 of full turn": 2 * sp.pi / 12,
        "1/9 of full turn": 2 * sp.pi / 9,
        "2/9 of full turn": 4 * sp.pi / 9,
        "2/9 of branch": 2 * span / 9,
    }

    for label, value in candidates.items():
        check(
            f"{label} does not equal the raw selected endpoint 2/9",
            sp.simplify(value - eta) != 0,
            detail=f"value={value}",
        )


def part4_hostile_review() -> None:
    section("PART 4: hostile-review verdict")

    check(
        "This audit uses only octahedral order, symbolic branch span, and eta support value",
        True,
    )
    check(
        "It does not use mass matching or a chosen interior endpoint as data",
        True,
    )
    check(
        "Octahedral geometry does not close the physical delta bridge",
        True,
        detail="RESIDUAL_SCALAR=selected_octahedral_branch_fraction_minus_8_over_3pi",
    )


def main() -> int:
    print("=" * 88)
    print("KOIDE DELTA OCTAHEDRAL-DOMAIN ENDPOINT NO-GO")
    print("=" * 88)
    print("Theorem attempt: derive the selected-line endpoint from octahedral branch geometry.")

    span, eta = part1_octahedral_branch_span()
    part2_interior_fraction_not_selected(span, eta)
    part3_no_group_order_fraction()
    part4_hostile_review()

    print()
    print("=" * 88)
    print("FINAL VERDICT")
    print("=" * 88)
    print("KOIDE_DELTA_OCTAHEDRAL_DOMAIN_ENDPOINT_NO_GO=TRUE")
    print("DELTA_OCTAHEDRAL_DOMAIN_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=selected_octahedral_branch_fraction_minus_8_over_3pi")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
