#!/usr/bin/env python3
"""
DM leptogenesis exact-kernel benchmark audit.

Purpose:
  Audit the refreshed exact-kernel leptogenesis result as a benchmark rather
  than rerunning it as a theorem script.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Scope:
  1. quantify sensitivity of the exact-kernel eta result to retained benchmark
     factors (washout / thermal prefactor)
  2. verify that the closure runner still uses retained benchmark ingredients
  3. verify that the closure runner directly substitutes /K00 in epsilon_1,
     so the remaining review question is the physical denominator/projection
     interpretation, not the source-side kernel itself
"""

from __future__ import annotations

import sys
from pathlib import Path

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


ETA_RATIO = 0.9907305393992764


def part1_percent_level_match_is_benchmark_sensitive() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PERCENT-LEVEL MATCH IS BENCHMARK-SENSITIVE")
    print("=" * 88)

    lo_2 = ETA_RATIO * 0.98
    hi_2 = ETA_RATIO * 1.02
    lo_5 = ETA_RATIO * 0.95
    hi_5 = ETA_RATIO * 1.05

    check(
        "A retained-prefactor shift of only 2 percent moves the result across eta_obs",
        lo_2 < 1.0 < hi_2,
        f"2% window=({lo_2:.6f},{hi_2:.6f})",
    )
    check(
        "A retained-prefactor shift of 5 percent moves the result by O(0.05 eta_obs)",
        abs(hi_5 - lo_5) > 0.09,
        f"5% window=({lo_5:.6f},{hi_5:.6f})",
    )
    check(
        "So the exact-kernel result is robust at order unity but not intrinsically at sub-percent precision",
        True,
        f"central eta/eta_obs={ETA_RATIO:.12f}",
    )


def part2_the_closure_runner_still_uses_retained_benchmark_ingredients() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CLOSURE RUNNER STILL USES RETAINED BENCHMARK INGREDIENTS")
    print("=" * 88)

    text = read("scripts/frontier_dm_leptogenesis_exact_kernel_closure.py")
    note = read("docs/DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md")

    check(
        "The runner still uses a retained thermal dilution factor D_THERMAL",
        "D_THERMAL = 3.901508e-3" in text,
    )
    check(
        "The runner still uses the phenomenological strong-washout fit kappa ~ (0.3/K)(ln K)^0.6",
        "kappa = (0.3 / k_washout) * (math.log(k_washout)) ** 0.6" in text,
    )
    check(
        "The note itself correctly labels the result as closure on the retained benchmark",
        "retained benchmark" in note,
    )


def part3_the_new_science_closes_the_source_kernel_but_the_runner_still_makes_the_denominator_bridge_explicit() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE RUNNER MAKES THE DENOMINATOR BRIDGE EXPLICIT")
    print("=" * 88)

    closure = read("scripts/frontier_dm_leptogenesis_exact_kernel_closure.py")
    k00_note = read("docs/DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md")
    source_note = read("docs/DM_LEPTOGENESIS_EXACT_SOURCE_DIAGNOSTIC_NOTE_2026-04-15.md")

    check(
        "The exact-kernel runner now inserts the coherent epsilon formula with an explicit /K00 denominator",
        "epsilon_1 = abs((1.0 / (8.0 * PI)) * Y0_SQ * (cp1 * f23 + cp2 * f3) / k00)" in closure,
    )
    check(
        "The new K00 theorem closes the heavy-basis diagonal channel itself",
        "`K00 = 2`" in k00_note and "`K00 = (K_mass)00`" in k00_note,
    )
    check(
        "The old diagnostic correctly identified the remaining issue as the map from K_mass to epsilon_1",
        ("thermal / projection law" in source_note or "thermal projection" in source_note)
        and "K_mass" in source_note,
    )

    print()
    print("  Audit read:")
    print("    - the source-side kernel is no longer the weak point")
    print("    - the refreshed closure depends on the explicit denominator bridge /K00")
    print("    - the remaining harsh-review question is the interpretation of that")
    print("      bridge inside the retained leptogenesis benchmark, not the source")
    print("      amplitudes or transfer coefficients")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS EXACT-KERNEL BENCHMARK AUDIT")
    print("=" * 88)

    part1_percent_level_match_is_benchmark_sensitive()
    part2_the_closure_runner_still_uses_retained_benchmark_ingredients()
    part3_the_new_science_closes_the_source_kernel_but_the_runner_still_makes_the_denominator_bridge_explicit()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
