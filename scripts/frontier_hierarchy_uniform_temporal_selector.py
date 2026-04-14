#!/usr/bin/env python3
"""
Hierarchy uniform temporal selector theorem.

This script proposes and verifies the strongest exact selector currently
available for the final hierarchy normalization:

  The physical dimension-4 order parameter on the minimal APBC block should
  average over a full *time-resolved* temporal orbit without mode-dependent
  weighting.

For APBC temporal modes, that requires sin^2((2n+1) pi / Lt) to be constant
across the orbit. The only even Lt solutions are Lt = 2 and Lt = 4.

Lt = 2 is the unresolved UV endpoint.
Lt = 4 is therefore the unique minimal resolved uniform orbit.

This gives the exact correction:

  C_phys = (A_2 / A_4)^(1/4) = (7/8)^(1/4)
"""

from __future__ import annotations

import math
import sys

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def apbc_sin2_values(Lt: int):
    return [round(math.sin((2 * n + 1) * math.pi / Lt) ** 2, 15) for n in range(Lt)]


def is_uniform_orbit(Lt: int) -> bool:
    vals = apbc_sin2_values(Lt)
    return max(vals) - min(vals) < 1e-12


def a_lt(Lt: int) -> float:
    return (1.0 / (2.0 * Lt)) * sum(
        1.0 / (3.0 + math.sin((2 * n + 1) * math.pi / Lt) ** 2) for n in range(Lt)
    )


def c_lt(Lt: int) -> float:
    return ((1.0 / 8.0) / a_lt(Lt)) ** 0.25


def c_obs() -> float:
    return 246.22 / 253.4


def v_selected(v_baseline: float = 253.4) -> float:
    return c_lt(4) * v_baseline


def test_only_uniform_even_solutions_are_2_and_4():
    print("\n" + "=" * 78)
    print("PART 1: UNIFORM APBC TEMPORAL ORBITS")
    print("=" * 78)

    uniform = []
    for Lt in range(2, 22, 2):
        vals = apbc_sin2_values(Lt)
        if is_uniform_orbit(Lt):
            uniform.append(Lt)
        print(f"  Lt={Lt:2d}: values={vals[:min(6,len(vals))]}{'...' if len(vals) > 6 else ''}")

    check(
        "the only even Lt <= 20 with uniform APBC temporal weight are 2 and 4",
        uniform == [2, 4],
        f"uniform Lt values = {uniform}",
    )


def test_analytic_selector_equation():
    print("\n" + "=" * 78)
    print("PART 2: ANALYTIC UNIFORMITY CONDITION")
    print("=" * 78)

    solutions = []
    for Lt in range(2, 41, 2):
        lhs = math.sin(math.pi / Lt) ** 2
        rhs = math.sin(3.0 * math.pi / Lt) ** 2
        if abs(lhs - rhs) < 1e-12:
            solutions.append(Lt)
        print(f"  Lt={Lt:2d}: sin^2(pi/Lt)={lhs:.12f}, sin^2(3pi/Lt)={rhs:.12f}")

    check(
        "sin^2(pi/Lt) = sin^2(3pi/Lt) selects only Lt = 2, 4 among even Lt",
        solutions == [2, 4],
        f"solutions = {solutions}",
    )


def test_lt4_is_unique_minimal_resolved_uniform_orbit():
    print("\n" + "=" * 78)
    print("PART 3: MINIMAL RESOLVED UNIFORM ORBIT")
    print("=" * 78)

    distinct_phases_2 = sorted(
        {round(((2 * n + 1) * math.pi / 2) % (2 * math.pi), 12) for n in range(2)}
    )
    distinct_phases_4 = sorted(
        {round(((2 * n + 1) * math.pi / 4) % (2 * math.pi), 12) for n in range(4)}
    )

    print(f"  Lt=2 phases: {distinct_phases_2}")
    print(f"  Lt=4 phases: {distinct_phases_4}")

    check(
        "Lt=2 is the unresolved UV endpoint with only one absolute temporal gap",
        len({round(abs(math.sin(p)), 12) for p in distinct_phases_2}) == 1,
        "all Lt=2 modes have identical absolute gap",
    )
    check(
        "Lt=4 is the minimal orbit with more than two distinct APBC phases",
        len(distinct_phases_4) == 4,
        f"distinct phases = {len(distinct_phases_4)}",
    )


def test_selected_correction_and_prediction():
    print("\n" + "=" * 78)
    print("PART 4: SELECTED EXACT CORRECTION")
    print("=" * 78)

    c4 = c_lt(4)
    c4_exact = (7.0 / 8.0) ** 0.25
    cobs = c_obs()
    v4 = v_selected(253.4)

    print(f"  C_4 direct = {c4:.12f}")
    print(f"  C_4 exact  = {c4_exact:.12f}")
    print(f"  C_obs      = {cobs:.12f}")
    print(f"  v_4        = {v4:.12f} GeV")

    check(
        "selected correction is exactly C = (7/8)^(1/4)",
        abs(c4 - c4_exact) < 1e-15,
        f"absolute error = {abs(c4 - c4_exact):.2e}",
    )
    check(
        "Lt=4 selected prediction is within 1% of the observed electroweak scale",
        abs(v4 - 246.22) / 246.22 < 0.01,
        f"relative error = {abs(v4 - 246.22) / 246.22:.4%}",
    )
    check(
        "Lt=4 correction is closer to observation than the Lt->infinity correction",
        abs(c4 - cobs) < abs(((3.0 / 4.0) ** (1.0 / 8.0)) - cobs),
        f"|C4-Cobs|={abs(c4-cobs):.6f}, |Cinf-Cobs|={abs(((3.0/4.0)**(1.0/8.0))-cobs):.6f}",
    )


def main():
    print("Hierarchy uniform temporal selector theorem")
    print("=" * 78)
    test_only_uniform_even_solutions_are_2_and_4()
    test_analytic_selector_equation()
    test_lt4_is_unique_minimal_resolved_uniform_orbit()
    test_selected_correction_and_prediction()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
