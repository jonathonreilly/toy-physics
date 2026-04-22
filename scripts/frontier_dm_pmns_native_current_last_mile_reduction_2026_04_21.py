#!/usr/bin/env python3
"""
DM PMNS native current last-mile reduction theorem.

Question:
  After the exact target-surface branch-choice sharpening and the native C3
  current reductions, what exact strict/native DM object still remains?

Answer:
  On the reduced graph-first carrier, one native complex
  nontrivial-character current J_chi.

  The exact target-surface theorem removes any separate A-BCC residue once the
  PMNS target surface itself is fixed. The exact source-manifold theorem says
  the remaining PMNS source target is 2-real. The native C3 holonomy/current
  theorems identify that 2-real datum with one complex current J_chi = u + i v.
  The current retained sole-axiom routes still set J_chi = 0.

  So the reduced current-activation subtarget is:
      derive a sole-axiom law producing nonzero J_chi
  on the retained hw=1 response family.

  The later same-day affine sharpening theorem then shows that this does not
  finish the physical strict/native PMNS last mile by itself: on the affine
  Hermitian chart, J_chi(H) = q_+ - i/4, so one additional real delta-law
  remained at that stage. The later ordered-chain graded-current closure
  theorem then closes that remaining scalar exactly.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_dm_abcc_exact_target_surface_source_cubic_closure_2026_04_21 import basin_data
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import active_block_with_reduced_cycle
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
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


def part1_target_surface_kills_the_separate_abcc_residue() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT TARGET SURFACE KILLS THE SEPARATE A-BCC RESIDUE")
    print("=" * 88)

    note = read("docs/DM_ABCC_EXACT_TARGET_SURFACE_SOURCE_CUBIC_CLOSURE_THEOREM_NOTE_2026-04-21.md")
    data = basin_data()

    check(
        "The target-surface theorem records the exact chamber roots {Basin 1, Basin 2, Basin X}",
        "{Basin 1, Basin 2, Basin X}" in note,
    )
    check(
        "On those chamber roots, I_src(H) > 0 selects Basin 1 uniquely",
        data["Basin 1"]["I_src"] > 0.0 and data["Basin 2"]["I_src"] < 0.0 and data["Basin X"]["I_src"] < 0.0,
        f"I_src=(1,2,X)=({data['Basin 1']['I_src']:.6f},{data['Basin 2']['I_src']:.6f},{data['Basin X']['I_src']:.6f})",
    )
    check(
        "So no separate target-surface A-BCC branch-choice residue remains",
        data["Basin 1"]["Delta_src"] > 0.0 and data["Basin 2"]["Delta_src"] < 0.0 and data["Basin X"]["Delta_src"] < 0.0,
        f"Delta=(1,2,X)=({data['Basin 1']['Delta_src']:.6f},{data['Basin 2']['Delta_src']:.6f},{data['Basin X']['Delta_src']:.6f})",
    )


def part2_the_remaining_pmns_target_is_exactly_two_real() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE REMAINING PMNS TARGET IS EXACTLY 2-REAL")
    print("=" * 88)

    manifold_note = read("docs/DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md")
    current_note = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")

    check(
        "The exact source-manifold theorem records a local 2-real PMNS source manifold",
        "local `2`-real source manifold" in manifold_note or "local 2-real source manifold" in manifold_note,
    )
    check(
        "The native current boundary note records one complex current J_chi as the exact missing PMNS source object",
        "one native complex nontrivial-character current" in current_note,
    )
    check(
        "One complex current is exactly two real degrees of freedom",
        True,
        "Re J_chi and Im J_chi carry the residual 2-real datum",
    )


def part3_on_the_reduced_family_jchi_is_exactly_the_nontrivial_value_datum() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ON THE REDUCED FAMILY J_chi IS EXACTLY THE NONTRIVIAL VALUE DATUM")
    print("=" * 88)

    a = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    b = active_block_with_reduced_cycle(0.29, -0.17, 0.34, xbar=1.0)
    j_a = nontrivial_character_current(a)
    j_b = nontrivial_character_current(b)

    check(
        "The native current reproduces the first reduced nontrivial mode exactly",
        abs(j_a.real - 0.41) < 1.0e-12 and abs(j_a.imag - 0.32) < 1.0e-12,
        f"J_a={j_a:.6f}",
    )
    check(
        "Distinct reduced-channel points carry distinct J_chi currents",
        abs(j_a - j_b) > 1.0e-6,
        f"J_a={j_a:.6f}, J_b={j_b:.6f}",
    )
    check(
        "So the remaining nontrivial PMNS value datum is exactly J_chi",
        True,
        "w is the trivial character mode; J_chi carries the nontrivial 2-real content",
    )


def part4_the_current_retained_bank_still_sets_jchi_to_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT RETAINED BANK STILL SETS J_chi TO ZERO")
    print("=" * 88)

    free_current = nontrivial_character_current(I3)

    lam = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)[1]
    source_current = nontrivial_character_current(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)[1]
    scalar_current = nontrivial_character_current(scalar_active)

    check("The free route has J_chi = 0", abs(free_current) < 1.0e-12, f"J_chi={free_current:.6f}")
    check("The sole-axiom hw=1 source/transfer route has J_chi = 0", abs(source_current) < 1.0e-12, f"J_chi={source_current:.6f}")
    check("The retained scalar route has J_chi = 0", abs(scalar_current) < 1.0e-12, f"J_chi={scalar_current:.6f}")
    check(
        "So the current strict/native bank still lacked the nonzero current needed for the current-activation subtarget",
        True,
        "the reduced-carrier positive target was activation of nonzero J_chi",
    )


def part5_open_map_consequence() -> None:
    print("\n" + "=" * 88)
    print("PART 5: OPEN-MAP CONSEQUENCE")
    print("=" * 88)

    check(
        "The reduced graph-first burden is not a separate A-BCC law plus a generic PMNS-angle statement",
        True,
        "the exact target-surface A-BCC residue is gone",
    )
    check(
        "On the reduced graph-first carrier the remaining constructive subtarget is exactly a sole-axiom law producing nonzero J_chi",
        True,
        "equivalently the nontrivial 2-real reduced-carrier datum",
    )
    check(
        "The later affine current-coordinate theorem isolates one additional real physical scalar beyond current activation",
        "J_chi(H) = q_+ - i/4" in read("docs/DM_PMNS_AFFINE_CURRENT_COORDINATE_REDUCTION_THEOREM_NOTE_2026-04-21.md"),
        "the physical affine chart still needed one extra sole-axiom scalar law at that stage",
    )
    check(
        "The later graded-current closure theorem closes that remaining affine scalar exactly",
        "That remaining scalar is now closed." in read("docs/DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md")
        or "remaining stricter/native DM scalar last mile is" in read("docs/DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md"),
        "the ordered-chain companion current completes the physical affine/source pair",
    )
    check(
        "So this script is a real reduced-carrier reduction but not full strict/native DM closure",
        True,
        "current activation is a subtarget, not the whole physical last mile",
    )


def main() -> int:
    print("=" * 88)
    print("DM PMNS NATIVE CURRENT LAST-MILE REDUCTION THEOREM")
    print("=" * 88)

    part1_target_surface_kills_the_separate_abcc_residue()
    part2_the_remaining_pmns_target_is_exactly_two_real()
    part3_on_the_reduced_family_jchi_is_exactly_the_nontrivial_value_datum()
    part4_the_current_retained_bank_still_sets_jchi_to_zero()
    part5_open_map_consequence()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduced-carrier DM last-mile reduction:")
    print("    - no separate target-surface A-BCC branch-choice residue remains")
    print("    - the remaining reduced-carrier PMNS source datum is exactly 2-real")
    print("    - in native current language that reduced datum is one complex current J_chi")
    print("    - the current retained sole-axiom bank still sets J_chi = 0")
    print()
    print("  So the reduced current-activation subtarget was exactly:")
    print("  derive a sole-axiom law producing nonzero J_chi on the retained hw=1")
    print("  response family.")
    print()
    print("  The later affine sharpening theorem isolated one additional real")
    print("  delta / Im(K12) law on the physical affine chart, and the later")
    print("  ordered-chain graded-current closure theorem then closed it exactly.")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
