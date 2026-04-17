#!/usr/bin/env python3
"""
DM neutrino source-surface Z3 doublet-block point-selection theorem.

Question:
  Once the live source-oriented sheet is pushed through the intrinsic Z3
  carrier readout, where does the remaining microscopic datum actually live?

Answer:
  On the live source-oriented sheet the Z3-basis kernel K_Z3(H) already has
  exact frozen singlet-doublet slots and an affine moving doublet block:

      K01 = a_*   (constant)
      K02 = b_*   (constant)

  while

      K11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3))
      K22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3))
      K12 = m - 4 sqrt(2)/9 + i (sqrt(3) delta - 4 sqrt(2)/3).

  So after quotienting the spectator line m, the remaining mainline datum is
  exactly the 2-real Z3-doublet-block law

      q_+ = 2 sqrt(2)/9 - (K11 + K22)/2
      delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3).

  The atlas slot tools therefore help by showing what is *not* left:
  the slots are already frozen, and the remaining microscopic selection object
  lives entirely in the doublet block.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import q_floor
from frontier_dm_neutrino_source_surface_intrinsic_slot_theorem import (
    intrinsic_slot_formula,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PI = np.pi
OMEGA = np.exp(2j * PI / 3.0)
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)


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


def kz_from_h(h: np.ndarray) -> np.ndarray:
    return UZ3.conj().T @ h @ UZ3


def expected_kz_entries(
    m: float, delta: float, q_plus: float
) -> tuple[complex, complex, float, float, complex, float]:
    a_star, b_star = intrinsic_slot_formula()
    k11 = -q_plus + 2.0 * math.sqrt(2.0) / 9.0 - 1.0 / (2.0 * math.sqrt(3.0))
    k22 = -q_plus + 2.0 * math.sqrt(2.0) / 9.0 + 1.0 / (2.0 * math.sqrt(3.0))
    k12 = m - 4.0 * math.sqrt(2.0) / 9.0 + 1j * (math.sqrt(3.0) * delta - 4.0 * math.sqrt(2.0) / 3.0)
    k00 = m + 2.0 * q_plus - 4.0 * math.sqrt(2.0) / 9.0
    return a_star, b_star, k11, k22, k12, k00


def part1_the_live_z3_image_has_exact_frozen_slots_and_affine_doublet_block() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE LIVE Z3 IMAGE HAS FROZEN SLOTS AND AN AFFINE DOUBLET BLOCK")
    print("=" * 88)

    samples = [
        (0.0, 0.2, q_floor(0.2) + 0.4),
        (0.0, 0.9, q_floor(0.9) + 0.4),
        (1.2, 0.2, q_floor(0.2) + 0.4),
        (1.2, 0.2, 2.5),
    ]

    ok_formulas = True
    max_err = 0.0
    for m, delta, q_plus in samples:
        kz = kz_from_h(active_affine_h(m, delta, q_plus))
        a_star, b_star, k11, k22, k12, k00 = expected_kz_entries(m, delta, q_plus)
        err = max(
            abs(kz[0, 1] - a_star),
            abs(kz[0, 2] - b_star),
            abs(kz[1, 1] - k11),
            abs(kz[2, 2] - k22),
            abs(kz[1, 2] - k12),
            abs(kz[0, 0] - k00),
        )
        max_err = max(max_err, float(err))
        ok_formulas &= err < 1e-12

    check(
        "On the live source-oriented sheet K_Z3(H) has exact frozen slots and affine doublet-block formulas",
        ok_formulas,
        f"max err={max_err:.2e}",
    )
    check(
        "The exact singlet-doublet slots are K01 = a_* and K02 = b_* everywhere on the live sheet",
        ok_formulas,
        "the slot pair is constant while the doublet block moves",
    )


def part2_the_remaining_active_pair_is_exactly_the_doublet_block_law() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE REMAINING ACTIVE PAIR IS EXACTLY THE DOUBLET-BLOCK LAW")
    print("=" * 88)

    samples = [
        (0.0, -0.3, 2.0),
        (0.0, 0.2, q_floor(0.2) + 0.4),
        (0.0, 0.9, q_floor(0.9) + 0.4),
        (0.0, 0.2, 2.5),
    ]

    ok_q = True
    ok_delta = True
    ok_m = True
    for m, delta, q_plus in samples:
        kz = kz_from_h(active_affine_h(m, delta, q_plus))
        q_rec = 2.0 * math.sqrt(2.0) / 9.0 - 0.5 * float(np.real(kz[1, 1] + kz[2, 2]))
        delta_rec = (float(np.imag(kz[1, 2])) + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0)
        m_rec = float(np.real(kz[1, 2])) + 4.0 * math.sqrt(2.0) / 9.0
        ok_q &= abs(q_rec - q_plus) < 1e-12
        ok_delta &= abs(delta_rec - delta) < 1e-12
        ok_m &= abs(m_rec - m) < 1e-12 and abs(float(np.real(np.trace(kz))) - m) < 1e-12

    check(
        "The active coordinate q_+ is exactly the centered trace law of the Z3 doublet block",
        ok_q,
        "q_+ = 2 sqrt(2)/9 - (K11+K22)/2",
    )
    check(
        "The active coordinate delta is exactly the shifted imaginary doublet-mixing law",
        ok_delta,
        "delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3)",
    )
    check(
        "The spectator coordinate m is exactly the real doublet-mixing / trace line",
        ok_m,
        "m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3",
    )


def part3_atlas_slot_tools_help_by_showing_the_slots_are_not_the_missing_object() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ATLAS SLOT TOOLS SHOW THE SLOTS ARE NOT THE MISSING OBJECT")
    print("=" * 88)

    a_star, b_star = intrinsic_slot_formula()
    h_a = active_affine_h(0.0, 0.2, q_floor(0.2) + 0.4)
    h_b = active_affine_h(0.0, 0.9, q_floor(0.9) + 0.4)
    h_c = active_affine_h(0.0, 0.2, 2.5)

    slots_const = (
        abs(slot_pair_from_h(h_a)[0] - a_star) < 1e-12
        and abs(slot_pair_from_h(h_a)[1] - b_star) < 1e-12
        and abs(slot_pair_from_h(h_b)[0] - a_star) < 1e-12
        and abs(slot_pair_from_h(h_b)[1] - b_star) < 1e-12
        and abs(slot_pair_from_h(h_c)[0] - a_star) < 1e-12
        and abs(slot_pair_from_h(h_c)[1] - b_star) < 1e-12
    )

    kz_a = kz_from_h(h_a)
    kz_b = kz_from_h(h_b)
    kz_c = kz_from_h(h_c)
    doublet_moves = (
        abs(kz_a[1, 2] - kz_b[1, 2]) > 1e-6
        and abs(kz_a[1, 1] - kz_c[1, 1]) > 1e-6
        and abs(kz_a[2, 2] - kz_c[2, 2]) > 1e-6
    )

    check(
        "The singlet-doublet slot tool remains correct on the live sheet: the slots are exact and constant",
        slots_const,
        f"(a_*,b_*)=({a_star:.12f},{b_star:.12f})",
    )
    check(
        "But varying the active pair changes only the Z3 doublet block, not the slots",
        slots_const and doublet_moves,
        "the missing microscopic law lives in the doublet block",
    )
    check(
        "So the remaining mainline object is not another slot-amplitude law but the 2-real Z3 doublet-block law",
        slots_const and doublet_moves,
        "atlas slot tools help by ruling that route out as the missing datum",
    )


def part4_the_note_records_the_z3_doublet_block_theorem() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE Z3 DOUBLET-BLOCK THEOREM")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the frozen slots and affine moving doublet block",
        "K01 = a_*" in note and "K02 = b_*" in note and "doublet block" in note,
    )
    check(
        "The new note records the remaining microscopic object as the 2-real Z3 doublet-block law",
        "`2`-real `Z_3` doublet-block law" in note or "2-real `Z_3` doublet-block law" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE Z3 DOUBLET-BLOCK POINT-SELECTION THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the live source-oriented sheet is pushed through the intrinsic Z3")
    print("  carrier readout, where does the remaining microscopic datum actually live?")

    part1_the_live_z3_image_has_exact_frozen_slots_and_affine_doublet_block()
    part2_the_remaining_active_pair_is_exactly_the_doublet_block_law()
    part3_atlas_slot_tools_help_by_showing_the_slots_are_not_the_missing_object()
    part4_the_note_records_the_z3_doublet_block_theorem()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact mainline answer:")
    print("    - the live Z3 image already has frozen singlet-doublet slots")
    print("    - the remaining active data live entirely in the moving doublet block")
    print("    - after quotienting spectator m, the missing microscopic object is")
    print("      exactly the 2-real Z3 doublet-block law for (delta, q_+)")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
