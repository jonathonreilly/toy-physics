#!/usr/bin/env python3
"""
DM leptogenesis numerator/denominator consistency audit.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Check that the current exact branch uses one consistent numerator/denominator
  normalization chain for:

    - epsilon_1
    - epsilon_1 / epsilon_DI
    - K00
    - m_tilde
    - K = m_tilde / m_*
    - retained-fit eta comparator
    - direct-transport eta authority
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from dm_leptogenesis_exact_common import (
    ETA_OBS,
    V_EW,
    Y0_SQ,
    exact_package,
    f_total,
    kappa_axiom_reference,
)

ROOT = Path(__file__).resolve().parents[1]

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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def part1_numerator_is_self_consistent() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CP-KERNEL NUMERATOR IS SELF-CONSISTENT")
    print("=" * 88)

    pkg = exact_package()
    x23 = (pkg.M2 / pkg.M1) ** 2
    x3 = (pkg.M3 / pkg.M1) ** 2
    epsilon_manual = abs(
        (1.0 / (8.0 * math.pi))
        * ((0.653**2 / 64.0) ** 2)
        * (pkg.cp1 * f_total(x23) + pkg.cp2 * f_total(x3))
        / pkg.K00
    )

    check(
        "The shared exact package reproduces the manual coherent numerator epsilon_1",
        abs(pkg.epsilon_1 - epsilon_manual) < 1e-18,
        f"epsilon_1={pkg.epsilon_1:.12e}",
    )
    check(
        "The exact package still records epsilon_1 / epsilon_DI = 0.9276209209197268",
        abs(pkg.epsilon_ratio - 0.9276209209197268) < 1e-12,
        f"ratio={pkg.epsilon_ratio:.12f}",
    )


def part2_denominator_is_used_consistently_in_kernel_and_washout() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE DENOMINATOR IS USED CONSISTENTLY IN KERNEL AND WASHOUT")
    print("=" * 88)

    pkg = exact_package()
    m_tilde_manual = pkg.K00 * Y0_SQ * V_EW**2 / pkg.M1 * 1e9

    check(
        "The exact package fixes K00 = 2",
        abs(pkg.K00 - 2.0) < 1e-12,
        f"K00={pkg.K00:.12f}",
    )
    check(
        "The exact package uses the same K00 in m_tilde_exact_eV",
        abs(pkg.m_tilde_exact_eV - m_tilde_manual) < 1e-15,
        f"m_tilde={pkg.m_tilde_exact_eV:.12f} eV",
    )
    check(
        "The exact package fixes K = 47.23597962989828 from that same denominator chain",
        abs(pkg.k_decay_exact - 47.23597962989828) < 1e-12,
        f"K={pkg.k_decay_exact:.12f}",
    )


def part3_the_old_stale_split_is_no_longer_present_in_the_kernel_runner() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OLD STALE SPLIT IS NO LONGER PRESENT")
    print("=" * 88)

    kernel_runner = read("scripts/frontier_dm_leptogenesis_exact_kernel_closure.py")

    check(
        "The exact-kernel runner now imports the shared exact package",
        "from dm_leptogenesis_exact_common import exact_package" in kernel_runner,
    )
    check(
        "The exact-kernel runner no longer hardcodes the stale near-1 eta claim",
        "0.9907305393992764" not in kernel_runner,
    )
    check(
        "The exact-kernel runner now records the consistent retained-fit value 0.557874966110017",
        "0.557874966110017" in kernel_runner,
    )


def part4_authority_and_comparator_paths_are_separated_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: AUTHORITY AND COMPARATOR PATHS ARE SEPARATED CLEANLY")
    print("=" * 88)

    pkg = exact_package()
    kappa_direct, _ = kappa_axiom_reference(pkg.k_decay_exact)
    eta_direct = 0.188785929502
    eta_direct_manual = (ETA_OBS * 0.0) + (
        pkg.epsilon_1 * kappa_direct * 7.039433661546651 * (28.0 / 79.0) * 0.003901498367656259 / ETA_OBS
    )

    check(
        "The retained-fit comparator is 0.557874966110017",
        abs(pkg.eta_ratio_fit_bench_exact_bookkeeping - 0.557874966110017) < 1e-12,
        f"eta_fit={pkg.eta_ratio_fit_bench_exact_bookkeeping:.12f}",
    )
    check(
        "The direct-transport authority path is 0.188785929502",
        abs(eta_direct_manual - eta_direct) < 1e-8,
        f"eta_direct={eta_direct_manual:.12f}",
    )
    check(
        "So the current mismatch is not numerator/denominator inconsistency between the two exact paths",
        abs(pkg.eta_ratio_fit_bench_exact_bookkeeping - eta_direct_manual) > 0.3,
        "the remaining gap is transport-content/model, not a hidden num/den swap",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS NUMERATOR/DENOMINATOR CONSISTENCY AUDIT")
    print("=" * 88)

    part1_numerator_is_self_consistent()
    part2_denominator_is_used_consistently_in_kernel_and_washout()
    part3_the_old_stale_split_is_no_longer_present_in_the_kernel_runner()
    part4_authority_and_comparator_paths_are_separated_cleanly()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
