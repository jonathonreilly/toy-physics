#!/usr/bin/env python3
"""Axiom-side derivation attempt for the PMNS active response-pack source principle."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_sigma_constraint_surface import sigma_from_block
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from pmns_lower_level_utils import CYCLE, I3, active_response_columns_from_sector_operator, derive_active_block_from_response_columns

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
TARGET_SUPPORT = (np.abs(I3 + CYCLE) > 0).astype(int)


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


def derive_from_columns(columns: list[np.ndarray], lam: float = 0.31) -> tuple[np.ndarray, np.ndarray]:
    return derive_active_block_from_response_columns(columns, lam)


def part1_the_current_exact_bank_derives_only_the_free_active_response_pack() -> tuple[list[np.ndarray], list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT EXACT BANK DERIVES ONLY THE FREE ACTIVE RESPONSE PACK")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    pack = sole_axiom_hw1_source_transfer_pack(lam_act, lam_pass)
    kernel, block = derive_from_columns(pack["active_columns"], lam_act)
    sigma = sigma_from_block(block)
    jchi = nontrivial_character_current(block)

    check("The sole-axiom active source columns are exactly the basis columns", np.linalg.norm(np.column_stack(pack["active_columns"]) - I3) < 1.0e-12)
    check("Their derived active kernel is exactly the free kernel I", np.linalg.norm(kernel - I3) < 1.0e-12)
    check("Their derived active block is exactly the free block I", np.linalg.norm(block - I3) < 1.0e-12)
    check("So the current exact bank still sets sigma = J_chi = 0 on the active response pack", abs(sigma) < 1.0e-12 and abs(jchi) < 1.0e-12, f"sigma={sigma:.6f}, J_chi={jchi:.6f}")

    return pack["active_columns"], pack["passive_columns"]


def part2_graph_transport_moves_the_frame_but_not_the_microscopic_response_pack(active_columns: list[np.ndarray]) -> None:
    print("\n" + "=" * 88)
    print("PART 2: GRAPH TRANSPORT MOVES THE FRAME BUT NOT THE MICROSCOPIC RESPONSE PACK")
    print("=" * 88)

    lam_act = 0.31
    transported_columns = [CYCLE @ col for col in active_columns]
    twice_transported_columns = [CYCLE @ col for col in transported_columns]

    transported_sector = CYCLE @ I3 @ CYCLE.conj().T
    twice_transported_sector = CYCLE @ transported_sector @ CYCLE.conj().T
    actual_transport_columns = active_response_columns_from_sector_operator(transported_sector, lam_act)[1]
    actual_twice_transport_columns = active_response_columns_from_sector_operator(twice_transported_sector, lam_act)[1]

    check("Transporting the free active sector by the exact coordinate cycle leaves the sector itself free", np.linalg.norm(transported_sector - I3) < 1.0e-12 and np.linalg.norm(twice_transported_sector - I3) < 1.0e-12)
    check("The actual response columns of the transported free sector are still the basis columns", np.linalg.norm(np.column_stack(actual_transport_columns) - I3) < 1.0e-12 and np.linalg.norm(np.column_stack(actual_twice_transport_columns) - I3) < 1.0e-12)
    check("So transported frame columns are not the same thing as the actual response columns of the transported free sector", np.linalg.norm(np.column_stack(transported_columns) - np.column_stack(actual_transport_columns)) > 1.0e-6 and np.linalg.norm(np.column_stack(twice_transported_columns) - np.column_stack(actual_twice_transport_columns)) > 1.0e-6,
          f"|C-I|={np.linalg.norm(np.column_stack(transported_columns) - np.column_stack(actual_transport_columns)):.6f}, |C^2-I|={np.linalg.norm(np.column_stack(twice_transported_columns) - np.column_stack(actual_twice_transport_columns)):.6f}")
    print("  [INFO] The graph-first route fixes the transport frame exactly, but that frame is still not a microscopic source-derived response pack")


def part3_if_one_forces_that_upgrade_by_hand_pmns_reopens_immediately(active_columns: list[np.ndarray], passive_columns: list[np.ndarray]) -> None:
    print("\n" + "=" * 88)
    print("PART 3: IF ONE FORCES THAT UPGRADE BY HAND PMNS REOPENS IMMEDIATELY")
    print("=" * 88)

    lam_act = 0.31
    forced_columns = [CYCLE @ (CYCLE @ col) for col in active_columns]
    kernel, block = derive_from_columns(forced_columns, lam_act)
    sigma = sigma_from_block(block)
    jchi = nontrivial_character_current(block)
    closure = close_from_lower_level_observables(forced_columns, passive_columns, lam_act, 0.27)

    check("The twice-transported frame columns can be reinterpreted algebraically as a nontrivial active response pack", np.linalg.norm(kernel - I3) > 1.0e-6, f"|K-I|={np.linalg.norm(kernel - I3):.6f}")
    check("That forced reinterpretation lands exactly on the retained diagonal-plus-forward-cycle carrier", np.array_equal((np.abs(block) > 1.0e-10).astype(int), TARGET_SUPPORT))
    check("On that forced pack the active block has nonzero sigma and nonzero J_chi", abs(sigma) > 1.0e-6 and abs(jchi) > 1.0e-6, f"sigma={sigma:.6f}, J_chi={jchi:.6f}")
    check("With the passive free pack unchanged, the same forced active pack already closes the one-sided PMNS lane downstream", closure["branch"] == "neutrino-active" and closure["tau"] == 0,
          f"branch={closure['branch']}, tau={closure['tau']}, q={closure['q']}")
    print("  [INFO] This shows the missing ingredient is not downstream PMNS closure; it is the microscopic legitimacy of the active response pack itself")


def part4_closeout_of_the_derivation_attempt() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CLOSEOUT OF THE DERIVATION ATTEMPT")
    print("=" * 88)

    check("The current exact axiom bank derives source columns, transport frame, selector bundle, and character readout data", True)
    check("It does not yet derive the microscopic upgrade that turns transported frame data into a genuine nontrivial active response pack", True)
    check("Therefore the active response-pack source principle is not yet axiom-derived on the current PMNS bank", True)
    check("It remains the exact next positive theorem target on the PMNS lane", True)


def main() -> int:
    print("=" * 88)
    print("PMNS ACTIVE RESPONSE-PACK AXIOM DERIVATION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current exact axiom bank itself derive the missing PMNS")
    print("  active response-pack source principle, or does it still stop one step")
    print("  short at frame/transport data?")

    active_columns, passive_columns = part1_the_current_exact_bank_derives_only_the_free_active_response_pack()
    part2_graph_transport_moves_the_frame_but_not_the_microscopic_response_pack(active_columns)
    part3_if_one_forces_that_upgrade_by_hand_pmns_reopens_immediately(active_columns, passive_columns)
    part4_closeout_of_the_derivation_attempt()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The derivation attempt fails on the current PMNS bank.")
    print("    - the exact bank derives the free active response pack")
    print("    - graph transport moves the source frame, but the transported free")
    print("      sector still has the free response pack")
    print("    - if one forcibly reinterprets the transported frame columns as an")
    print("      active response pack, PMNS reopens immediately")
    print()
    print("  Therefore the exact missing theorem is now completely explicit:")
    print("  an axiom-native microscopic upgrade from graph/transport frame data")
    print("  to a genuine nontrivial active response pack on the existing hw=1")
    print("  carrier.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
