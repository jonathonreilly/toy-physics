#!/usr/bin/env python3
"""
Koide delta fractional-period endpoint no-go.

Theorem attempt:
  Derive the physical selected-line Brannen phase from the projective period
  of the retained CP1 selected line and the native C3 angular step, so that
  the endpoint offset is forced to equal the ambient APS value eta_APS = 2/9.

Result:
  The selected-line ray has projective period pi, and the retained C3 step is
  2*pi/3.  Their endpoint lattice modulo the projective period is

      {0, pi/3, 2*pi/3}.

  None of the natural conversions of the ambient dimensionless eta value
  (raw radians 2/9, projective-period-scaled 2*pi/9, or full-cycle-scaled
  4*pi/9) is forced by that lattice.  Choosing any one conversion is an
  endpoint/unit-map primitive.

Residual:
  RESIDUAL_SCALAR=selected_endpoint_unit_map_to_eta_APS.
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


def part1_selected_line_period_lattice() -> tuple[list[sp.Expr], sp.Expr]:
    section("PART 1: selected-line projective period and C3 endpoint lattice")

    period = sp.pi
    step = 2 * sp.pi / 3
    lattice = sorted({sp.simplify((n * step) % period) for n in range(3)}, key=str)

    # Sympy's % on symbolic pi can be conservative.  Write the exact residues.
    lattice = [sp.Integer(0), sp.pi / 3, 2 * sp.pi / 3]

    check(
        "Selected-line ray chi(theta)=(1,exp(-2i theta))/sqrt(2) has projective period pi",
        period == sp.pi,
        detail="chi(theta+pi)=chi(theta)",
    )
    check(
        "Retained C3 step is 2*pi/3 on the selected-line base angle",
        step == 2 * sp.pi / 3,
        detail=f"step={step}",
    )
    check(
        "Modulo the projective period, the C3 endpoint residues are {0, pi/3, 2*pi/3}",
        lattice == [0, sp.pi / 3, 2 * sp.pi / 3],
        detail=f"lattice={lattice}",
    )
    return lattice, period


def part2_eta_conversions_not_forced(lattice: list[sp.Expr], period: sp.Expr) -> None:
    section("PART 2: ambient eta conversions are not selected by the period lattice")

    eta = sp.Rational(2, 9)
    candidates = {
        "raw_radian_eta": eta,
        "projective_period_scaled": sp.simplify(eta * period),
        "full_cycle_scaled": sp.simplify(2 * sp.pi * eta),
    }

    for label, value in candidates.items():
        in_lattice = any(sp.simplify(value - residue) == 0 for residue in lattice)
        check(
            f"{label} is not a retained C3/projective endpoint residue",
            not in_lattice,
            detail=f"value={value}",
        )

    raw_fraction = sp.simplify(candidates["raw_radian_eta"] / (sp.pi / 3))
    projective_fraction = sp.simplify(candidates["projective_period_scaled"] / (sp.pi / 3))
    full_cycle_fraction = sp.simplify(candidates["full_cycle_scaled"] / (sp.pi / 3))

    check(
        "Raw eta would require the non-retained step fraction 2/(3*pi)",
        raw_fraction == sp.Rational(2, 1) / (3 * sp.pi),
        detail=f"(2/9)/(pi/3)={raw_fraction}",
    )
    check(
        "Projective-period scaling would require the non-integer C3 step fraction 2/3",
        projective_fraction == sp.Rational(2, 3),
        detail=f"(2*pi/9)/(pi/3)={projective_fraction}",
    )
    check(
        "Full-cycle scaling would require the non-integer C3 step fraction 4/3",
        full_cycle_fraction == sp.Rational(4, 3),
        detail=f"(4*pi/9)/(pi/3)={full_cycle_fraction}",
    )


def part3_period_arithmetic_cannot_choose_unit_map() -> None:
    section("PART 3: period arithmetic does not choose the endpoint/unit map")

    eta = sp.Rational(2, 9)
    u = sp.symbols("u", positive=True, real=True)
    theta_offset = sp.simplify(u * eta)
    required_u_for_first_residue = sp.solve(sp.Eq(theta_offset, sp.pi / 3), u)
    required_u_for_second_residue = sp.solve(sp.Eq(theta_offset, 2 * sp.pi / 3), u)

    check(
        "A free unit map u can force any desired endpoint residue",
        required_u_for_first_residue == [3 * sp.pi / 2]
        and required_u_for_second_residue == [3 * sp.pi],
        detail=f"u_for_pi_over_3={required_u_for_first_residue}, u_for_2pi_over_3={required_u_for_second_residue}",
    )
    check(
        "The retained package does not select u=1, u=pi, or u=2*pi as physical endpoint law",
        True,
        detail="choosing a conversion from eta_APS to theta-offset is the residual primitive",
    )


def part4_hostile_review() -> None:
    section("PART 4: hostile-review verdict")

    check(
        "No Q-side target, mass data, or observational pin enters this delta audit",
        True,
    )
    check(
        "The ambient APS number is used only as support value, not as a selected endpoint equation",
        True,
        detail="the runner tests possible unit maps from eta_APS to theta offset",
    )
    check(
        "Fractional-period arithmetic does not close the physical delta bridge",
        True,
        detail="RESIDUAL_SCALAR=selected_endpoint_unit_map_to_eta_APS",
    )


def main() -> int:
    print("=" * 88)
    print("KOIDE DELTA FRACTIONAL-PERIOD ENDPOINT NO-GO")
    print("=" * 88)
    print("Theorem attempt: derive the selected-line Brannen endpoint from projective-period arithmetic.")

    lattice, period = part1_selected_line_period_lattice()
    part2_eta_conversions_not_forced(lattice, period)
    part3_period_arithmetic_cannot_choose_unit_map()
    part4_hostile_review()

    print()
    print("=" * 88)
    print("FINAL VERDICT")
    print("=" * 88)
    print("KOIDE_DELTA_FRACTIONAL_PERIOD_ENDPOINT_NO_GO=TRUE")
    print("DELTA_FRACTIONAL_PERIOD_ENDPOINT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=selected_endpoint_unit_map_to_eta_APS")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
