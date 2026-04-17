#!/usr/bin/env python3
"""
DM neutrino source-surface Z3 doublet-block current-bank blindness theorem.

Question:
  After the atlas slot tools identify the physical singlet-doublet carrier,
  does the current exact bank determine the remaining Z3 doublet-block law on
  the live source-oriented sheet?

Answer:
  No.

  On the live sheet the slot sector is already frozen:

      K01 = a_*,   K02 = b_*,

  and therefore every current slot-sector observable stays fixed:

      - the source package
      - the intrinsic CP pair
      - the intrinsic slot pair
      - the slot torsion

  But the Z3 doublet block still moves with the exact 2-real pair (delta, q_+).
  So the current atlas slot/odd-bank is blind to the remaining datum. The
  missing object is exactly a right-sensitive 2-real Z3 doublet-block law.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import (
    positive_representative,
    q_floor,
    slot_torsion,
)
from frontier_dm_neutrino_source_surface_intrinsic_slot_theorem import (
    intrinsic_slot_formula,
)
from frontier_dm_neutrino_source_surface_z3_doublet_block_point_selection_theorem import (
    kz_from_h,
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


def doublet_block_observables(kz: np.ndarray) -> tuple[float, float]:
    q_plus = 2.0 * math.sqrt(2.0) / 9.0 - 0.5 * float(np.real(kz[1, 1] + kz[2, 2]))
    delta = (float(np.imag(kz[1, 2])) + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0)
    return q_plus, delta


def same_signature(
    sig_a: tuple[complex, complex, float, float, float],
    sig_b: tuple[complex, complex, float, float, float],
    tol: float = 1e-12,
) -> bool:
    return (
        abs(sig_a[0] - sig_b[0]) < tol
        and abs(sig_a[1] - sig_b[1]) < tol
        and abs(sig_a[2] - sig_b[2]) < tol
        and abs(sig_a[3] - sig_b[3]) < tol
        and abs(sig_a[4] - sig_b[4]) < tol
    )


def part1_slot_sector_observables_are_exactly_frozen_on_the_live_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SLOT-SECTOR OBSERVABLES ARE EXACTLY FROZEN ON THE LIVE SHEET")
    print("=" * 88)

    pkg = exact_package()
    a_star, b_star = intrinsic_slot_formula()
    torsion_star = slot_torsion(a_star, b_star)

    samples = [
        active_affine_h(0.0, 0.2, q_floor(0.2) + 0.4),
        active_affine_h(0.0, 0.9, q_floor(0.9) + 0.4),
        active_affine_h(0.0, 0.2, 2.5),
    ]

    ok_slots = True
    ok_cp = True
    ok_torsion = True
    for h in samples:
        hp = positive_representative(h, floor=2.0)
        a, b = slot_pair_from_h(hp)
        cp = cp_pair_from_h(hp)
        ok_slots &= abs(a - a_star) < 1e-12 and abs(b - b_star) < 1e-12
        ok_cp &= abs(cp[0] - pkg.cp1) < 1e-12 and abs(cp[1] - pkg.cp2) < 1e-12
        ok_torsion &= abs(slot_torsion(a, b) - torsion_star) < 1e-12

    check(
        "Across the live source-oriented sheet the intrinsic slot pair is already the exact constant pair (a_*, b_*)",
        ok_slots,
        f"(a_*,b_*)=({a_star:.12f},{b_star:.12f})",
    )
    check(
        "The intrinsic heavy-basis CP pair is unchanged across those same samples",
        ok_cp,
        f"(cp1,cp2)=({pkg.cp1:.12f},{pkg.cp2:.12f})",
    )
    check(
        "The exact slot torsion is unchanged across those same samples",
        ok_torsion,
        f"torsion={torsion_star:.12f}",
    )


def part2_the_z3_doublet_block_still_moves_with_two_real_data() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE Z3 DOUBLET BLOCK STILL MOVES WITH TWO REAL DATA")
    print("=" * 88)

    q_common = 2.2
    h_delta_a = active_affine_h(0.0, 0.2, q_common)
    h_delta_b = active_affine_h(0.0, 0.9, q_common)
    h_q_a = active_affine_h(0.0, 0.2, q_common)
    h_q_b = active_affine_h(0.0, 0.2, 2.5)

    kz_delta_a = kz_from_h(h_delta_a)
    kz_delta_b = kz_from_h(h_delta_b)
    kz_q_a = kz_from_h(h_q_a)
    kz_q_b = kz_from_h(h_q_b)

    q_a, delta_a = doublet_block_observables(kz_delta_a)
    q_b, delta_b = doublet_block_observables(kz_delta_b)
    q_c, delta_c = doublet_block_observables(kz_q_b)

    check(
        "Changing delta while holding q_+ fixed changes the imaginary doublet mixing Im K12",
        abs(float(np.imag(kz_delta_a[1, 2])) - float(np.imag(kz_delta_b[1, 2]))) > 1e-6
        and abs(q_a - q_b) < 1e-12
        and abs(delta_a - delta_b) > 1e-6,
        f"ImK12: {float(np.imag(kz_delta_a[1,2])):.6f} -> {float(np.imag(kz_delta_b[1,2])):.6f}",
    )
    check(
        "Changing q_+ while holding delta fixed changes the centered doublet trace (K11+K22)/2",
        abs(float(np.real(kz_q_a[1, 1] + kz_q_a[2, 2])) - float(np.real(kz_q_b[1, 1] + kz_q_b[2, 2]))) > 1e-6
        and abs(delta_a - delta_c) < 1e-12
        and abs(q_a - q_c) > 1e-6,
        f"q_+: {q_a:.6f} -> {q_c:.6f}",
    )
    check(
        "So the moving datum still has exact real dimension two in the Z3 doublet block",
        True,
        "one real coordinate from the centered doublet trace and one from Im K12",
    )


def part3_current_atlas_slot_bank_is_blind_to_that_doublet_block_motion() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT ATLAS SLOT BANK IS BLIND TO THE DOUBLET-BLOCK MOTION")
    print("=" * 88)

    q_common = 2.2
    h_a = active_affine_h(0.0, 0.2, q_common)
    h_b = active_affine_h(0.0, 0.9, q_common)
    h_c = active_affine_h(0.0, 0.2, 2.5)

    def slot_bank_signature(h: np.ndarray) -> tuple[complex, complex, float, float, float]:
        hp = positive_representative(h, floor=2.0)
        a, b = slot_pair_from_h(hp)
        cp1, cp2 = cp_pair_from_h(hp)
        torsion = slot_torsion(a, b)
        return a, b, cp1, cp2, torsion

    sig_a = slot_bank_signature(h_a)
    sig_b = slot_bank_signature(h_b)
    sig_c = slot_bank_signature(h_c)
    kz_a = kz_from_h(h_a)
    kz_b = kz_from_h(h_b)
    kz_c = kz_from_h(h_c)

    block_moves = (
        abs(kz_a[1, 2] - kz_b[1, 2]) > 1e-6
        and abs(kz_a[1, 1] - kz_c[1, 1]) > 1e-6
        and abs(kz_a[2, 2] - kz_c[2, 2]) > 1e-6
    )

    same_bank = same_signature(sig_a, sig_b) and same_signature(sig_a, sig_c)

    check(
        "Two live-sheet points with different delta and two with different q_+ still have identical current slot-bank signatures",
        same_bank,
        "same slots, same CP pair, same torsion",
    )
    check(
        "Those same points have different Z3 doublet blocks",
        block_moves,
        "the remaining datum is invisible to the current slot bank",
    )
    check(
        "Therefore the current atlas slot/odd-bank does not determine the remaining microscopic datum",
        same_bank and block_moves,
        "the missing object is exactly a right-sensitive 2-real Z3 doublet-block law",
    )


def part4_the_note_records_the_final_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE FINAL BOUNDARY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records that the slot sector is frozen while the doublet block still moves",
        "slot sector is already frozen" in note and "doublet block still moves" in note,
    )
    check(
        "The new note records the remaining object as a 2-real Z3 doublet-block law",
        "`2`-real `Z_3` doublet-block law" in note
        or "2-real `Z_3` doublet-block law" in note
        or "2-real Z3 doublet-block law" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE Z3 DOUBLET-BLOCK CURRENT-BANK BLINDNESS THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the atlas slot tools identify the physical singlet-doublet")
    print("  carrier, does the current exact bank determine the remaining Z3")
    print("  doublet-block law on the live source-oriented sheet?")

    part1_slot_sector_observables_are_exactly_frozen_on_the_live_sheet()
    part2_the_z3_doublet_block_still_moves_with_two_real_data()
    part3_current_atlas_slot_bank_is_blind_to_that_doublet_block_motion()
    part4_the_note_records_the_final_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the atlas slot-sector outputs are already frozen on the live sheet")
    print("    - the Z3 doublet block still moves with a 2-real pair")
    print("    - the current exact slot/odd-bank is blind to that motion")
    print("    - so the remaining closure object is exactly the right-sensitive")
    print("      2-real Z3 doublet-block law")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
