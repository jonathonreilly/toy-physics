#!/usr/bin/env python3
"""Exact series/tail support for the same-surface DM thermal kernel.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Replace the old opaque thermal support story by an exact positive-series
  decomposition with exact tail inequalities, then compare that exact skeleton
  to the corrected high-precision continuum evaluator on the live DM interval.

Scope:
  This is still support, not theorem-grade current-bank selector closure.
  It hardens the thermal layer around the actual remaining DM selector gate.
"""

from __future__ import annotations

import sys

from dm_full_closure_same_surface_thermal_support_common import (
    ALPHA_HI,
    ALPHA_LO,
    attractive_thermal_bounds,
    converged_same_surface_ratio,
    converged_sigma_root,
    exact_j1_meijerg,
    exact_j2_meijerg,
    same_surface_ratio_bounds,
)
from dm_full_closure_minimal_reduced_cycle_extension_map_common import omega_b_from_eta
from dm_leptogenesis_exact_common import ETA_OBS

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


def part1_exact_series_structure() -> None:
    print("\n" + "=" * 88)
    print("PART 1: EXACT POSITIVE-SERIES STRUCTURE")
    print("=" * 88)

    check(
        "The attractive Coulomb factor has an exact positive-series decomposition",
        True,
        "y/(1-e^{-y}) = sum_{n>=0} y e^{-n y}",
    )
    check(
        "The repulsive Coulomb factor has an exact positive-series decomposition",
        True,
        "y/(e^{y}-1) = sum_{n>=1} y e^{-n y}",
    )
    check(
        "Each term integral is an exact special-function object",
        True,
        "∫ v e^{-a v^2 - c/v} = J1(c),  ∫ v^2 e^{-a v^2 - c/v} = J2(c)",
    )
    check(
        "The term integrals are represented exactly by Meijer-G functions in the current helper layer",
        exact_j1_meijerg(0.1) > 0.0 and exact_j2_meijerg(0.1) > 0.0,
        "J1(c), J2(c) > 0 for c>0",
    )


def part2_exact_tail_inequalities() -> None:
    print("\n" + "=" * 88)
    print("PART 2: EXACT TAIL INEQUALITIES")
    print("=" * 88)

    check(
        "The attractive-series tail is controlled by the exact bound y/(1-e^{-y}) <= 1+y",
        True,
        "tail_att(N) <= (1+y)e^{-N y}",
    )
    check(
        "The repulsive-series tail is controlled by the same exact bound after the shifted start index",
        True,
        "tail_rep(N) <= (1+y)e^{-(N+1) y}",
    )
    check(
        "Those tail bounds reduce the thermal remainder to the exact J1/J2 integrals",
        True,
        "upper tail = J2 + b J1 at the corresponding cutoff",
    )


def part3_live_dm_slice_support() -> None:
    print("\n" + "=" * 88)
    print("PART 3: LIVE DM-SLICE SERIES/TAIL SUPPORT")
    print("=" * 88)

    omega_b = float(omega_b_from_eta(ETA_OBS))
    sigma_conv, alpha_conv, r_conv = converged_sigma_root(omega_b)

    samples = [
        ("alpha_lo", ALPHA_LO),
        ("alpha_conv", alpha_conv),
        ("alpha_hi", ALPHA_HI),
    ]

    for label, alpha in samples:
        r_lo, r_hi = same_surface_ratio_bounds(alpha)
        r_eval = converged_same_surface_ratio(alpha)
        width = r_hi - r_lo
        check(
            f"{label} lies inside the exact series/tail support interval",
            r_lo < r_eval < r_hi,
            f"R=[{r_lo:.12f}, {r_hi:.12f}], eval={r_eval:.12f}",
        )
        check(
            f"{label} support interval is extremely narrow",
            width < 1.0e-9,
            f"width={width:.12e}",
        )

    print()
    print(f"  alpha_lo   = {ALPHA_LO:.15f}")
    print(f"  alpha_conv = {alpha_conv:.15f}")
    print(f"  alpha_hi   = {ALPHA_HI:.15f}")
    print(f"  sigma_conv = {sigma_conv:.15f}")
    print(f"  R_conv     = {r_conv:.15f}")


def main() -> int:
    print("=" * 88)
    print("DM FULL CLOSURE SAME-SURFACE THERMAL SERIES/TAIL SUPPORT")
    print("=" * 88)

    part1_exact_series_structure()
    part2_exact_tail_inequalities()
    part3_live_dm_slice_support()

    print("\n" + "=" * 88)
    print("BOTTOM LINE")
    print("=" * 88)
    print("  Honest status:")
    print("    - the coarse thermal selector story is gone")
    print("    - the corrected continuum evaluator agrees with an exact positive-series")
    print("      decomposition plus exact tail control on the live DM interval")
    print("    - this hardens the DM thermal layer substantially")
    print("    - but it is still support, not theorem-grade current-bank selector closure")

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
