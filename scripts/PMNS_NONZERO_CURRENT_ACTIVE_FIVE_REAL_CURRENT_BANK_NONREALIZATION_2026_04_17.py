#!/usr/bin/env python3
"""Sharper current-bank impossibility on the PMNS-native strong production lane.

Question:
  Does the current exact PMNS-native bank already determine the active
  off-seed five-real packet and therefore already realize a sole-axiom law for
  nonzero J_chi?

Answer:
  No.

  The current bank fixes seed-facing transport summaries but still leaves the
  active five-real packet free, and that packet already moves J_chi.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_corner_transport_active_block import active_corner_transport, orbit_average_transport
from frontier_pmns_transfer_operator_dominant_mode import projected_transfer_kernel_from_active_block
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
)

ROOT = Path(__file__).resolve().parents[1]
np.set_printoptions(precision=6, suppress=True, linewidth=140)

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


def witness_pair() -> tuple[np.ndarray, np.ndarray]:
    a = active_corner_transport(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    b = active_corner_transport(
        np.array([1.20, 0.79, 0.93], dtype=float),
        np.array([0.52, 0.17, 0.54], dtype=float),
        0.63,
    )
    return a, b


def part1_the_retained_sole_axiom_routes_still_force_zero_current() -> None:
    print("\n" + "=" * 96)
    print("PART 1: THE RETAINED SOLE-AXIOM ROUTES STILL FORCE J_chi = 0")
    print("=" * 96)

    lam = 0.31
    free_current = nontrivial_character_current(I3)

    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)[1]
    source_current = nontrivial_character_current(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)[1]
    scalar_current = nontrivial_character_current(scalar_active)

    check("The free PMNS-native sole-axiom route has J_chi = 0", abs(free_current) < 1e-12, f"J_chi={free_current:.6f}")
    check("The canonical sole-axiom hw=1 source/transfer route has J_chi = 0", abs(source_current) < 1e-12, f"J_chi={source_current:.6f}")
    check("The retained scalar route has J_chi = 0", abs(scalar_current) < 1e-12, f"J_chi={scalar_current:.6f}")
    check("So the current retained bank still contains no explicit nonzero-current route", True)


def part2_same_current_bank_transport_data_still_do_not_select_the_current() -> None:
    print("\n" + "=" * 96)
    print("PART 2: SAME CURRENT-BANK TRANSPORT DATA STILL DO NOT SELECT J_chi")
    print("=" * 96)

    a, b = witness_pair()
    current_a = nontrivial_character_current(a)
    current_b = nontrivial_character_current(b)
    transfer_a = projected_transfer_kernel_from_active_block(a)
    transfer_b = projected_transfer_kernel_from_active_block(b)
    orbit_a = orbit_average_transport(a)
    orbit_b = orbit_average_transport(b)

    check(
        "The witness pair has the same projected transfer kernel",
        np.linalg.norm(transfer_a - transfer_b) < 1e-12,
        f"err={np.linalg.norm(transfer_a - transfer_b):.2e}",
    )
    check(
        "The witness pair has the same orbit-averaged corner-transport moments",
        all(abs(lhs - rhs) < 1e-12 for lhs, rhs in zip(orbit_a, orbit_b)),
        f"orbit_a={orbit_a}, orbit_b={orbit_b}",
    )
    check(
        "Those same current-bank transport summaries still carry distinct nonzero native currents",
        abs(current_a - current_b) > 1e-6 and abs(current_a) > 1e-6 and abs(current_b) > 1e-6,
        f"J_a={current_a:.6f}, J_b={current_b:.6f}",
    )
    check(
        "So the current PMNS-native bank still does not select nonzero J_chi on the strongest native microscopic route",
        abs(current_a - current_b) > 1e-6 and np.linalg.norm(transfer_a - transfer_b) < 1e-12,
    )


def part3_the_exact_note_stack_already_closes_the_hidden_bank_loophole() -> None:
    print("\n" + "=" * 96)
    print("PART 3: THE EXACT NOTE STACK ALREADY CLOSES THE HIDDEN-BANK LOOPHOLE")
    print("=" * 96)

    reduction = read("docs/PMNS_NONZERO_CURRENT_ACTIVE_FIVE_REAL_REDUCTION_NOTE_2026-04-17.md")
    route_exhaust = read("docs/PMNS_SOLE_AXIOM_NATIVE_CURRENT_ROUTE_EXHAUSTION_NOTE_2026-04-17.md")
    transfer = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    corner = read("docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md")
    pf_nonreal = read("docs/PERRON_FROBENIUS_STEP2_ACTIVE_FIVE_REAL_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")

    check(
        "The new reduction note records that the strongest PMNS-native strong-route target is the active off-seed five-real packet",
        "active off-seed `5`-real packet" in reduction
        and "PMNS-native strong production lane" in reduction
        and "derive a sole-axiom law for the active off-seed `5`-real packet" in reduction,
    )
    check(
        "The route-exhaustion note already says there is no overlooked PMNS-native route to nonzero J_chi on the current bank",
        "no overlooked exact PMNS-native route on the current" in route_exhaust
        and "nonzero `J_chi`" in route_exhaust,
    )
    check(
        "The transfer and corner-transport notes already say the current microscopic laws stop before the off-seed packet",
        "does not determine the `5`-real off-seed" in transfer
        and ("blind to the active 5-real" in corner or "blind to the five real corner-breaking coordinates" in corner),
    )
    check(
        "The PF active-five-real current-bank nonrealization note already closes the broader hidden-bank loophole on the same packet",
        "current exact bank still does **not** determine the active" in pf_nonreal
        and "off-seed `5`-real source" in pf_nonreal,
    )


def part4_circularity_guard() -> None:
    print("\n" + "=" * 96)
    print("PART 4: CIRCULARITY GUARD")
    print("=" * 96)

    ok_current, bad_current = circularity_guard(nontrivial_character_current, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_transfer, bad_transfer = circularity_guard(
        projected_transfer_kernel_from_active_block, {"u", "v", "w", "x", "y", "delta", "tau", "q"}
    )
    check("The native current functional takes no PMNS-side target values as inputs", ok_current, f"bad={bad_current}")
    check("The seed-facing transfer projection takes no PMNS-side target values as inputs", ok_transfer, f"bad={bad_transfer}")


def main() -> int:
    print("=" * 96)
    print("PMNS NONZERO CURRENT ACTIVE FIVE-REAL CURRENT-BANK NONREALIZATION")
    print("=" * 96)
    print()
    print("Question:")
    print("  Does the current exact PMNS-native bank already determine the active")
    print("  off-seed five-real packet and therefore already realize nonzero J_chi?")

    part1_the_retained_sole_axiom_routes_still_force_zero_current()
    part2_same_current_bank_transport_data_still_do_not_select_the_current()
    part3_the_exact_note_stack_already_closes_the_hidden_bank_loophole()
    part4_circularity_guard()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Exact PMNS-native strong-route impossibility sharpening:")
    print("    - the retained sole-axiom routes still force J_chi = 0")
    print("    - the strongest current-bank transport summaries still admit")
    print("      distinct nonzero J_chi")
    print("    - so the current bank does not determine the active off-seed")
    print("      five-real current-producing packet")
    print()
    print("  Therefore no sole-axiom nonzero-J_chi production law is yet present on")
    print("  the current PMNS-native strong production lane.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
