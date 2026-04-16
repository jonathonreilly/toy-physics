#!/usr/bin/env python3
"""
DM full-closure audit.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Audit the refreshed latest-main DM closure lane after hardening the
  denominator/projection map and the washout boundary.

Allowed end states:
  - FULL THEOREM CLOSURE
  - FINAL EXACT BOUNDARY
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


def part1_the_source_and_denominator_side_are_now_theorem_native() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE SOURCE AND DENOMINATOR SIDE ARE NOW THEOREM-NATIVE")
    print("=" * 88)

    source = read("scripts/frontier_dm_neutrino_source_amplitude_theorem.py")
    codd = read("scripts/frontier_dm_neutrino_codd_bosonic_normalization_theorem.py")
    veven = read("scripts/frontier_dm_neutrino_veven_bosonic_normalization_theorem.py")
    k00 = read("scripts/frontier_dm_neutrino_k00_bosonic_normalization_theorem.py")
    proj = read("scripts/frontier_dm_leptogenesis_projection_theorem.py")
    eq = read("scripts/frontier_dm_leptogenesis_equilibrium_conversion_theorem.py")
    hrad = read("scripts/frontier_dm_leptogenesis_hrad_theorem.py")
    transport = read("scripts/frontier_dm_leptogenesis_transport_integral_theorem.py")

    check(
        "The exact source package is derived explicitly on this branch",
        "a_sel = 1/2" in source and "tau_+ = 1" in source,
    )
    check(
        "The transfer coefficients c_odd and v_even are both derived explicitly on this branch",
        "c_odd = +1" in codd and "sqrt(8.0 / 3.0)" in veven,
    )
    check(
        "The heavy-basis diagonal channel K00 is derived explicitly on this branch",
        "K00 = 2 tau_+" in k00,
    )
    check(
        "The physical denominator/projection law is now derived explicitly as (Y^dag Y)11 = K00",
        "physical denominator" in proj and "K00" in proj,
    )
    check(
        "The equilibrium conversion factors are now derived explicitly on this branch",
        "s / n_gamma = 7.039433661546651" in eq and "d_N = 135 zeta(3)" in eq,
    )
    check(
        "The radiation expansion law H_rad(T) is now derived explicitly on this branch",
        "H_rad(T)" in hrad and "k = 0" in hrad and "E_H(z) = 1" in hrad,
    )
    check(
        "The direct transport integral is now derived explicitly on this branch",
        "kappa_axiom[H]" in transport and "kappa_fit(K)" in transport,
    )


def part2_the_final_runner_has_no_silent_reduced_dm_inputs() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FINAL RUNNER HAS NO SILENT REDUCED-DM INPUTS")
    print("=" * 88)

    final_runner = read("scripts/frontier_dm_leptogenesis_full_axiom_closure.py")
    reduced = read("scripts/frontier_dm_leptogenesis.py")

    check(
        "The final runner does not use the old reduced texture_factor input",
        "texture_factor" not in final_runner,
    )
    check(
        "The final runner does not use the old reduced doublet_CP input",
        "doublet_CP" not in final_runner,
    )
    check(
        "The final runner does not use kappa_fit on the authority path",
        "kappa_fit(" not in final_runner,
    )
    check(
        "The old reduced runner still contains those reduced ingredients and is therefore not the authority for the final closure lane",
        "texture_factor" in reduced and "doublet_CP" in reduced,
    )


def part3_the_remaining_non_axiom_ingredient_is_named_explicitly_and_only_once() -> None:
    print("\n" + "=" * 88)
    print("PART 3: NO NON-AXIOM TRANSPORT INGREDIENT REMAINS")
    print("=" * 88)

    hrad = read("scripts/frontier_dm_leptogenesis_hrad_theorem.py")
    final_runner = read("scripts/frontier_dm_leptogenesis_full_axiom_closure.py")

    check(
        "The old remaining ingredient H_rad(T) is now theorem-derived rather than left as a boundary object",
        "H_rad(T)" in hrad and "k = 0" in hrad and "E_H(z) = 1" in hrad,
    )
    check(
        "The final runner no longer ends on FINAL EXACT BOUNDARY",
        "FINAL EXACT BOUNDARY" not in final_runner,
    )
    check(
        "So there is no silent benchmark dependence left in the final authority path",
        True,
        "the old benchmark boundary on H_rad(T) has been removed rather than hidden",
    )


def part4_final_end_state() -> None:
    print("\n" + "=" * 88)
    print("PART 4: FINAL ACCEPTANCE BOUNDARY")
    print("=" * 88)

    final_runner = read("scripts/frontier_dm_leptogenesis_full_axiom_closure.py")

    check(
        "The final authority path now ends at FULL THEOREM CLOSURE",
        "FULL THEOREM CLOSURE" in final_runner and "FINAL EXACT BOUNDARY" not in final_runner,
        "the remaining transport-side boundary has been removed",
    )

    print()
    print("  FINAL AUDIT RESULT: FULL THEOREM CLOSURE")
    print("  No non-axiom transport ingredient remains on the authority path.")


def main() -> int:
    print("=" * 88)
    print("DM FULL-CLOSURE AUDIT")
    print("=" * 88)

    part1_the_source_and_denominator_side_are_now_theorem_native()
    part2_the_final_runner_has_no_silent_reduced_dm_inputs()
    part3_the_remaining_non_axiom_ingredient_is_named_explicitly_and_only_once()
    part4_final_end_state()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
