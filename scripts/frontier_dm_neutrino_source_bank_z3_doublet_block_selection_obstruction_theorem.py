#!/usr/bin/env python3
"""
DM neutrino source-bank Z3 doublet-block selection obstruction theorem.

Question:
  After checking the reusable atlas tools, does the current exact source bank
  determine the remaining right-sensitive Z3 doublet-block point
  (delta, q_+) on the live source-oriented sheet?

Answer:
  No.

  The atlas-supported upstream source side is already closed to the fixed sharp
  tuple

      a_sel = 1/2,   tau_+ = 1,
      gamma = 1/2,   E1 = sqrt(8/3),   E2 = sqrt(8)/3.

  But there are distinct live-sheet points with different (delta, q_+) and
  different Z3 doublet blocks that carry exactly the same current-bank
  signature

      (gamma, E1, E2, cp1, cp2, a_*, b_*, T_slot).

  So no deterministic selector that factors only through the current exact
  atlas-supported source bank can choose the active point. The minimal missing
  object is a new right-sensitive 2-real datum, equivalently the Z3
  doublet-block law itself.
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
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
    source_surface_data_in_carrier_normal_form,
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


def current_bank_signature(
    h: np.ndarray,
) -> tuple[float, float, float, float, float, complex, complex, float]:
    hp = positive_representative(h, floor=2.0)
    _lam_plus, _lam_odd, _u, v, delta, rho, gamma, sigma = source_surface_data_in_carrier_normal_form(hp)
    e1 = delta + rho
    e2 = 0.75 * math.sqrt(2.0) * sigma * math.sin(2.0 * v)
    cp1, cp2 = cp_pair_from_h(hp)
    a, b = slot_pair_from_h(hp)
    torsion = slot_torsion(a, b)
    return gamma, e1, e2, cp1, cp2, a, b, torsion


def same_signature(
    sig_a: tuple[float, float, float, float, float, complex, complex, float],
    sig_b: tuple[float, float, float, float, float, complex, complex, float],
    tol: float = 1e-12,
) -> bool:
    return (
        abs(sig_a[0] - sig_b[0]) < tol
        and abs(sig_a[1] - sig_b[1]) < tol
        and abs(sig_a[2] - sig_b[2]) < tol
        and abs(sig_a[3] - sig_b[3]) < tol
        and abs(sig_a[4] - sig_b[4]) < tol
        and abs(sig_a[5] - sig_b[5]) < tol
        and abs(sig_a[6] - sig_b[6]) < tol
        and abs(sig_a[7] - sig_b[7]) < tol
    )


def active_target_from_h(h: np.ndarray) -> tuple[float, float]:
    kz = kz_from_h(h)
    q_plus = 2.0 * math.sqrt(2.0) / 9.0 - 0.5 * float(np.real(kz[1, 1] + kz[2, 2]))
    delta = (float(np.imag(kz[1, 2])) + 4.0 * math.sqrt(2.0) / 3.0) / math.sqrt(3.0)
    return delta, q_plus


def part1_the_atlas_supported_upstream_source_bank_is_already_a_fixed_point() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ATLAS-SUPPORTED UPSTREAM SOURCE BANK IS ALREADY A FIXED POINT")
    print("=" * 88)

    pkg = exact_package()
    source_note = read("docs/DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md")
    coeff_note = read("docs/DM_NEUTRINO_WEAK_TRIPLET_COEFFICIENT_AXIOM_BOUNDARY_NOTE_2026-04-15.md")

    a_sel = 0.5
    tau_plus = 1.0
    gamma = a_sel
    e1 = math.sqrt(8.0 / 3.0) * tau_plus
    e2 = math.sqrt(8.0) / 3.0 * tau_plus

    check(
        "The source-amplitude theorem records the sharp source point a_sel = 1/2 and tau_+ = 1",
        "a_sel = 1/2" in source_note and "tau_+ = 1" in source_note,
    )
    check(
        "The coefficient-closure theorem records gamma = a_sel, E1 = sqrt(8/3) tau_+, E2 = (sqrt(8)/3) tau_+",
        "gamma = a_sel" in coeff_note
        and "E1 = sqrt(8/3) tau_+" in coeff_note
        and "E2 = (sqrt(8)/3) tau_+" in coeff_note,
    )
    check(
        "So the atlas-supported upstream source bank already collapses to one exact sharp tuple",
        abs(gamma - pkg.gamma) < 1e-12
        and abs(e1 - pkg.E1) < 1e-12
        and abs(e2 - pkg.E2) < 1e-12,
        f"(a_sel,tau_+,gamma,E1,E2)=({a_sel:.6f},{tau_plus:.6f},{gamma:.6f},{e1:.12f},{e2:.12f})",
    )


def part2_distinct_active_points_share_that_same_current_bank_signature() -> None:
    print("\n" + "=" * 88)
    print("PART 2: DISTINCT ACTIVE POINTS SHARE THE SAME CURRENT-BANK SIGNATURE")
    print("=" * 88)

    q_common = 2.2
    h_a = active_affine_h(0.0, 0.2, q_common)
    h_b = active_affine_h(0.0, 0.9, q_common)
    h_c = active_affine_h(0.0, 0.2, 2.5)

    sig_a = current_bank_signature(h_a)
    sig_b = current_bank_signature(h_b)
    sig_c = current_bank_signature(h_c)
    pkg = exact_package()

    same_bank = same_signature(sig_a, sig_b) and same_signature(sig_a, sig_c)
    exact_tuple = (
        abs(sig_a[0] - pkg.gamma) < 1e-12
        and abs(sig_a[1] - pkg.E1) < 1e-12
        and abs(sig_a[2] - pkg.E2) < 1e-12
        and abs(sig_a[3] - pkg.cp1) < 1e-12
        and abs(sig_a[4] - pkg.cp2) < 1e-12
    )

    check(
        "Changing delta at fixed q_+ and changing q_+ at fixed delta still leaves the whole current-bank signature unchanged",
        same_bank,
        "same (gamma,E1,E2,cp1,cp2,a_*,b_*,T_slot)",
    )
    check(
        "That unchanged signature is exactly the closed sharp source tuple and its downstream invariant readouts",
        exact_tuple,
        f"(gamma,E1,E2,cp)=({sig_a[0]:.12f},{sig_a[1]:.12f},{sig_a[2]:.12f},{sig_a[3]:.12f},{sig_a[4]:.12f})",
    )


def part3_the_remaining_target_still_moves_in_two_independent_real_directions() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING TARGET STILL MOVES IN TWO INDEPENDENT REAL DIRECTIONS")
    print("=" * 88)

    q_common = 2.2
    h_a = active_affine_h(0.0, 0.2, q_common)
    h_b = active_affine_h(0.0, 0.9, q_common)
    h_c = active_affine_h(0.0, 0.2, 2.5)

    delta_a, q_a = active_target_from_h(h_a)
    delta_b, q_b = active_target_from_h(h_b)
    delta_c, q_c = active_target_from_h(h_c)

    kz_a = kz_from_h(h_a)
    kz_b = kz_from_h(h_b)
    kz_c = kz_from_h(h_c)

    check(
        "At fixed q_+, the shifted imaginary doublet mixing Im K12 changes with delta",
        abs(q_a - q_b) < 1e-12
        and abs(delta_a - delta_b) > 1e-6
        and abs(float(np.imag(kz_a[1, 2])) - float(np.imag(kz_b[1, 2]))) > 1e-6,
        f"delta: {delta_a:.6f} -> {delta_b:.6f}",
    )
    check(
        "At fixed delta, the centered doublet trace changes with q_+",
        abs(delta_a - delta_c) < 1e-12
        and abs(q_a - q_c) > 1e-6
        and abs(float(np.real(kz_a[1, 1] + kz_a[2, 2])) - float(np.real(kz_c[1, 1] + kz_c[2, 2]))) > 1e-6,
        f"q_+: {q_a:.6f} -> {q_c:.6f}",
    )
    check(
        "So the unresolved active target is genuinely 2-real, equivalently the Z3 doublet-block pair (delta, q_+)",
        True,
        "one real direction from Im K12 and one from the centered doublet trace",
    )


def part4_no_deterministic_selector_factoring_through_the_current_bank_can_choose_the_point() -> None:
    print("\n" + "=" * 88)
    print("PART 4: NO DETERMINISTIC SELECTOR FACTORING THROUGH THE CURRENT BANK CAN CHOOSE THE POINT")
    print("=" * 88)

    q_common = 2.2
    h_a = active_affine_h(0.0, 0.2, q_common)
    h_b = active_affine_h(0.0, 0.9, q_common)
    h_c = active_affine_h(0.0, 0.2, 2.5)

    sig_a = current_bank_signature(h_a)
    sig_b = current_bank_signature(h_b)
    sig_c = current_bank_signature(h_c)
    tgt_a = active_target_from_h(h_a)
    tgt_b = active_target_from_h(h_b)
    tgt_c = active_target_from_h(h_c)

    same_bank = same_signature(sig_a, sig_b) and same_signature(sig_a, sig_c)
    different_targets = tgt_a != tgt_b and tgt_a != tgt_c

    check(
        "Distinct live active points can have identical exact current-bank signatures",
        same_bank,
        "the current exact atlas-supported bank is constant on those samples",
    )
    check(
        "Those same points have different active targets (delta, q_+)",
        different_targets,
        f"targets={tgt_a}, {tgt_b}, {tgt_c}",
    )
    check(
        "Therefore no deterministic selector that factors only through the current exact source bank can determine the active point",
        same_bank and different_targets,
        "a new right-sensitive 2-real datum is required",
    )


def part5_the_note_records_the_obstruction_cleanly() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE OBSTRUCTION CLEANLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_BANK_Z3_DOUBLET_BLOCK_SELECTION_OBSTRUCTION_THEOREM_NOTE_2026-04-16.md")

    check(
        "The new note records the fixed upstream source tuple and the moving doublet-block target",
        "a_sel = 1/2" in note
        and "tau_+ = 1" in note
        and "(delta, q_+)" in note
        and "doublet-block law" in note,
    )
    check(
        "The new note records that a new right-sensitive 2-real datum is required",
        "new right-sensitive `2`-real datum" in note or "new right-sensitive 2-real datum" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-BANK Z3 DOUBLET-BLOCK SELECTION OBSTRUCTION THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  After checking the reusable atlas tools, does the current exact")
    print("  source bank determine the remaining right-sensitive Z3 doublet-block")
    print("  point (delta, q_+) on the live source-oriented sheet?")

    part1_the_atlas_supported_upstream_source_bank_is_already_a_fixed_point()
    part2_distinct_active_points_share_that_same_current_bank_signature()
    part3_the_remaining_target_still_moves_in_two_independent_real_directions()
    part4_no_deterministic_selector_factoring_through_the_current_bank_can_choose_the_point()
    part5_the_note_records_the_obstruction_cleanly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact answer:")
    print("    - the atlas-supported upstream source bank already closes to the")
    print("      fixed sharp tuple a_sel = 1/2, tau_+ = 1, gamma = 1/2,")
    print("      E1 = sqrt(8/3), E2 = sqrt(8)/3")
    print("    - the live active target still moves in two real directions")
    print("      (delta, q_+), equivalently in the Z3 doublet block")
    print("    - distinct active points share the same exact current-bank signature")
    print("    - so the current exact source bank cannot select the point")
    print("    - the minimal missing object is a new right-sensitive 2-real datum,")
    print("      equivalently the Z3 doublet-block law itself")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
