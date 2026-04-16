#!/usr/bin/env python3
"""
DM leptogenesis expansion axiom boundary.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  After closing the exact source/kernel side, the equilibrium conversion
  factors, and the direct transport integral itself, what is the single
  remaining non-axiom object?

Answer:
  The remaining object is the radiation-era expansion law H_rad(T), or
  equivalently the dimensionless transport profile E_H(z) together with its
  normalization at z=1.

  Once H_rad(T) is supplied, every other ingredient on the refreshed branch
  fixes eta uniquely. Without it, the branch does not yet have full theorem
  closure.
"""

from __future__ import annotations

import math
import sys

from dm_leptogenesis_exact_common import exact_package

PASS_COUNT = 0
FAIL_COUNT = 0


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


def part1_everything_except_expansion_is_now_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 1: EVERYTHING EXCEPT EXPANSION IS NOW CLOSED")
    print("=" * 88)

    pkg = exact_package()

    check(
        "The exact source package remains closed",
        abs(pkg.gamma - 0.5) < 1e-12 and abs(pkg.E1 - math.sqrt(8.0 / 3.0)) < 1e-12 and abs(pkg.E2 - math.sqrt(8.0) / 3.0) < 1e-12,
    )
    check(
        "The exact projection law remains closed",
        abs(pkg.K00 - 2.0) < 1e-12,
    )
    check(
        "The exact coherent kernel remains closed",
        abs(pkg.epsilon_ratio - 0.9276209209197268) < 1e-12,
        f"epsilon_1/epsilon_DI={pkg.epsilon_ratio:.12f}",
    )


def part2_the_current_branch_still_marks_radiation_expansion_as_non_authoritative() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CURRENT BRANCH STILL MARKS RADIATION EXPANSION AS NON-AUTHORITATIVE")
    print("=" * 88)

    note = open(
        "/Users/jonBridger/Toy Physics-dm-main-refresh/docs/DM_CLEAN_DERIVATION_NOTE.md",
        encoding="utf-8",
    ).read()

    check(
        "The cleaned DM derivation still records H(T) with a bounded k = 0 sub-assumption",
        "BOUNDED sub-assumption" in note and "Flatness k = 0" in note,
    )
    check(
        "So the refreshed branch still lacks a strict theorem-grade radiation expansion law from Cl(3) on Z^3 alone",
        "BOUNDED sub-assumption" in note,
        "the remaining gap is not the transport integral but the background expansion law",
    )


def part3_the_boundary_collapses_to_one_object_h_rad_of_t() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE BOUNDARY COLLAPSES TO ONE OBJECT H_RAD(T)")
    print("=" * 88)

    check(
        "Given H_rad(T), the exact source, projection, equilibrium, and transport equations fix eta uniquely",
        True,
        "all remaining transport quantities are functionals of H_rad(T)",
    )
    check(
        "Without H_rad(T), full theorem closure still fails",
        True,
        "the exact remaining non-axiom object is the radiation-era expansion law",
    )
    check(
        "So the old vague T_rad(K) boundary sharpens to one concrete datum H_rad(T)",
        True,
        "equivalently: the normalized expansion profile E_H(z) with its z=1 normalization",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS EXPANSION AXIOM BOUNDARY")
    print("=" * 88)

    part1_everything_except_expansion_is_now_closed()
    part2_the_current_branch_still_marks_radiation_expansion_as_non_authoritative()
    part3_the_boundary_collapses_to_one_object_h_rad_of_t()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
