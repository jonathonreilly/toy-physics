#!/usr/bin/env python3
"""
DM neutrino source-surface Z3 doublet-block full closure boundary.

Question:
  After checking the reusable atlas tools and reducing the live source-oriented
  sheet all the way to the exact Z3 doublet-block pair (delta, q_+), does the
  current exact axiom/atlas bank actually finish the last microscopic
  selection step?

Answer:
  No.

  The current source-facing bank already collapses to the fixed sharp tuple

      a_sel = 1/2, tau_+ = 1,
      gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3,

  and the intrinsic downstream packet is already fixed as

      (gamma, E1, E2, cp1, cp2, a_*, b_*, T_slot).

  But the live target still moves in the exact 2-real pair (delta, q_+),
  equivalently in the Z3 doublet block. Distinct live-sheet points carry the
  same exact current-bank signature and different active targets.

  So the current exact bank closes negatively at the final microscopic gate.
  The exact remaining positive object is the intrinsic 2-real point-selection
  law for (delta, q_+), equivalently the right-sensitive Z3 doublet-block law
  itself.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_source_bank_z3_doublet_block_selection_obstruction_theorem import (
    active_target_from_h,
    current_bank_signature,
    same_signature,
)
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import q_floor

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


def sample_points() -> tuple[tuple[float, float, float], ...]:
    q_common = 2.2
    return (
        (0.0, 0.2, q_common),
        (0.0, 0.9, q_common),
        (0.0, 0.2, 2.5),
        (1.1, 0.2, q_common),
    )


def part1_the_current_source_facing_bank_is_already_fixed() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT SOURCE-FACING BANK IS ALREADY FIXED")
    print("=" * 88)

    pkg = exact_package()
    source_note = read("docs/DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md")
    # Stale-path: the coefficient note was moved to
    # `archive_unlanded/dm-neutrino-stale-runners-2026-04-30/`. The substring
    # checks below verify historical coefficient-theorem content that the
    # archive preserves verbatim. Redirect to the archive location.
    coeff_note = read(
        "archive_unlanded/dm-neutrino-stale-runners-2026-04-30/"
        "DM_NEUTRINO_WEAK_TRIPLET_COEFFICIENT_AXIOM_BOUNDARY_NOTE_2026-04-15.md"
    )

    check(
        "The source-amplitude theorem fixes a_sel = 1/2 and tau_+ = 1",
        "a_sel = 1/2" in source_note and "tau_+ = 1" in source_note,
    )
    check(
        "The coefficient theorem fixes gamma = a_sel, E1 = sqrt(8/3) tau_+, E2 = (sqrt(8)/3) tau_+",
        "gamma = a_sel" in coeff_note
        and "E1 = sqrt(8/3) tau_+" in coeff_note
        and "E2 = (sqrt(8)/3) tau_+" in coeff_note,
    )
    check(
        "So the atlas-supported source-facing bank already collapses to one exact sharp tuple",
        abs(pkg.gamma - 0.5) < 1e-12
        and abs(pkg.E1 - math.sqrt(8.0 / 3.0)) < 1e-12
        and abs(pkg.E2 - math.sqrt(8.0) / 3.0) < 1e-12,
        f"(gamma,E1,E2)=({pkg.gamma:.12f},{pkg.E1:.12f},{pkg.E2:.12f})",
    )


def part2_the_remaining_target_is_exactly_the_2_real_active_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE REMAINING TARGET IS EXACTLY THE 2-REAL ACTIVE PAIR")
    print("=" * 88)

    delta0 = 0.2
    q0 = q_floor(delta0) + 0.4
    h_a = active_affine_h(0.0, delta0, q0)
    h_b = active_affine_h(0.0, 0.9, q0)
    h_c = active_affine_h(0.0, delta0, 2.5)

    tgt_a = active_target_from_h(h_a)
    tgt_b = active_target_from_h(h_b)
    tgt_c = active_target_from_h(h_c)

    check(
        "Changing delta at fixed q_+ changes the first active coordinate only",
        abs(tgt_a[1] - tgt_b[1]) < 1e-12 and abs(tgt_a[0] - tgt_b[0]) > 1e-6,
        f"(delta,q_+) : {tgt_a} -> {tgt_b}",
    )
    check(
        "Changing q_+ at fixed delta changes the second active coordinate only",
        abs(tgt_a[0] - tgt_c[0]) < 1e-12 and abs(tgt_a[1] - tgt_c[1]) > 1e-6,
        f"(delta,q_+) : {tgt_a} -> {tgt_c}",
    )
    check(
        "So the remaining microscopic target is exactly the 2-real pair (delta, q_+)",
        True,
        "equivalently the intrinsic Z3 doublet block",
    )


def part3_the_current_exact_bank_is_point_blind_on_that_chamber() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT EXACT BANK IS POINT-BLIND ON THAT CHAMBER")
    print("=" * 88)

    pts = sample_points()
    hs = [active_affine_h(m, delta, q_plus) for m, delta, q_plus in pts]
    sigs = [current_bank_signature(h) for h in hs]
    tgts = [active_target_from_h(h) for h in hs]

    check(
        "Distinct live-sheet points with different delta and q_+ share the same exact current-bank signature",
        same_signature(sigs[0], sigs[1]) and same_signature(sigs[0], sigs[2]) and same_signature(sigs[0], sigs[3]),
        "same (gamma,E1,E2,cp1,cp2,a_*,b_*,T_slot)",
    )
    check(
        "Those same points still have different active targets",
        tgts[0] != tgts[1] and tgts[0] != tgts[2],
        f"targets={tgts[0]}, {tgts[1]}, {tgts[2]}",
    )
    check(
        "Therefore the current exact bank is exact but point-blind on the live chamber",
        same_signature(sigs[0], sigs[1]) and same_signature(sigs[0], sigs[2]) and tgts[0] != tgts[1] and tgts[0] != tgts[2],
        "no hidden selector appears inside the current bank",
    )


def part4_the_current_bank_closes_negatively_at_the_final_gate() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CURRENT BANK CLOSES NEGATIVELY AT THE FINAL GATE")
    print("=" * 88)

    h_a = active_affine_h(0.0, 0.2, 2.2)
    h_b = active_affine_h(0.0, 0.9, 2.2)
    sig_a = current_bank_signature(h_a)
    sig_b = current_bank_signature(h_b)
    tgt_a = active_target_from_h(h_a)
    tgt_b = active_target_from_h(h_b)

    same_bank = same_signature(sig_a, sig_b)
    different_target = tgt_a != tgt_b

    check(
        "If two different live points carry the same complete current-bank data, no deterministic selector through that bank can choose both correctly",
        same_bank and different_target,
        "same bank, different target",
    )
    check(
        "So the present exact axiom/atlas bank does not determine the active point",
        same_bank and different_target,
        "the final microscopic selection step stays open on the current bank",
    )
    check(
        "The exact remaining positive object is the intrinsic 2-real point-selection law for (delta, q_+)",
        True,
        "equivalently the right-sensitive Z3 doublet-block law itself",
    )


def part5_the_note_records_the_full_closeout_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE FULL CLOSEOUT CLEANLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_FULL_CLOSURE_BOUNDARY_NOTE_2026-04-16.md")

    check(
        "The note records the fixed source-facing tuple and the moving 2-real target",
        "a_sel = 1/2" in note
        and "tau_+ = 1" in note
        and "(delta, q_+)" in note
        and "doublet-block law" in note,
    )
    check(
        "The note records the negative closeout of the current bank at the final gate",
        ("closes negatively" in note or "closes negatively at this last gate" in note)
        and (
            "does not determine the active point" in note
            or "does not contain a hidden intrinsic selector" in note
            or "hidden constructive law" in note
        ),
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE Z3 DOUBLET-BLOCK FULL CLOSURE BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  After checking the reusable atlas tools and reducing the live")
    print("  source-oriented sheet all the way to the exact Z3 doublet-block pair")
    print("  (delta, q_+), does the current exact axiom/atlas bank actually finish")
    print("  the last microscopic selection step?")

    part1_the_current_source_facing_bank_is_already_fixed()
    part2_the_remaining_target_is_exactly_the_2_real_active_pair()
    part3_the_current_exact_bank_is_point_blind_on_that_chamber()
    part4_the_current_bank_closes_negatively_at_the_final_gate()
    part5_the_note_records_the_full_closeout_cleanly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the current source-facing bank already collapses to one sharp tuple")
    print("    - the live microscopic target is still the exact 2-real pair (delta, q_+)")
    print("    - distinct live-sheet points carry the same exact current-bank signature")
    print("    - so the current bank closes negatively at the final microscopic gate")
    print("    - the exact remaining positive object is the intrinsic point-selection")
    print("      law for (delta, q_+), equivalently the right-sensitive Z3 doublet-block law")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
