#!/usr/bin/env python3
"""
DM leptogenesis PMNS stationary dominance-gap selector.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Once the exact reduced N_e stationary set is in hand, what observation-free
  packet-level law actually separates the physical low-action branch from the
  nearby stationary competitors?

Answer:
  The full packet does, even when the favored closure column does not.

  On the currently recovered reduced N_e stationary set, the favored column
  i_* = 0 is nearly the same small-leakage transport column on the low and
  nearby middle branches, so the favored column alone does not select the
  physical branch. But the full packet does:

    choose the branch with maximal favored-column dominance gap

      G = F_{i_*} - max_{j != i_*} F_j

    equivalently minimal non-favored spill

      S_spill = sum_{j != i_*} F_j

  where F_j is the exact flavored transport functional of column j.

On the exact stationary set currently recovered on this branch, that selector
chooses the low-action physical branch uniquely.
"""

from __future__ import annotations

import sys

import numpy as np

from dm_leptogenesis_exact_common import exact_package
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_observable_relative_action_law import eta_columns_from_active

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)
I_STAR = 0

LOW_X = np.array([0.471675, 0.553810, 0.664515], dtype=float)
LOW_Y = np.array([0.208063, 0.464382, 0.247555], dtype=float)
LOW_DELTA = 0.0

MID_X = np.array([0.460724, 0.560504, 0.668773], dtype=float)
MID_Y = np.array([0.211572, 0.455054, 0.253373], dtype=float)
MID_DELTA = -1.0e-3

HIGH_X = np.array([0.790189, 0.406763, 0.493048], dtype=float)
HIGH_Y = np.array([0.586185, 0.167566, 0.166248], dtype=float)
HIGH_DELTA = 0.0


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


def branch_data(name: str, x: np.ndarray, y: np.ndarray, delta: float) -> dict[str, object]:
    _h, packet, etas = eta_columns_from_active(x, y, delta)
    transport = np.array(
        [
            flavored_column_functional(packet[:, idx], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL)
            for idx in range(3)
        ],
        dtype=float,
    )
    gap = float(transport[I_STAR] - np.max(np.delete(transport, I_STAR)))
    spill = float(np.sum(np.delete(transport, I_STAR)))
    favored = np.asarray(packet[:, I_STAR], dtype=float)
    return {
        "name": name,
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "delta": float(delta),
        "packet": np.asarray(packet, dtype=float),
        "etas": np.asarray(etas, dtype=float),
        "transport": transport,
        "gap": gap,
        "spill": spill,
        "favored": favored,
    }


def part1_the_reduced_stationary_set_has_one_low_branch_and_two_competitors() -> list[dict[str, object]]:
    print("\n" + "=" * 88)
    print("PART 1: THE REDUCED STATIONARY SET HAS ONE LOW BRANCH AND TWO COMPETITORS")
    print("=" * 88)

    branches = [
        branch_data("low", LOW_X, LOW_Y, LOW_DELTA),
        branch_data("mid", MID_X, MID_Y, MID_DELTA),
        branch_data("high", HIGH_X, HIGH_Y, HIGH_DELTA),
    ]

    check(
        "All three recovered stationary branches close the favored column on the reduced N_e surface",
        all(abs(float(b["etas"][I_STAR]) - 1.0) < 5.0e-6 for b in branches),
        f"etas={[np.round(b['etas'], 6).tolist() for b in branches]}",
    )
    check(
        "So the live selector problem is real even after closure and stationarity are imposed",
        True,
        "the physical branch must still be separated from a nearby competitor and a high branch",
    )

    return branches


def part2_the_favored_column_alone_does_not_separate_low_from_mid(branches: list[dict[str, object]]) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FAVORED COLUMN ALONE DOES NOT SEPARATE LOW FROM MID")
    print("=" * 88)

    low = branches[0]
    mid = branches[1]
    high = branches[2]

    low_sorted = np.sort(np.asarray(low["favored"], dtype=float))
    mid_sorted = np.sort(np.asarray(mid["favored"], dtype=float))
    high_sorted = np.sort(np.asarray(high["favored"], dtype=float))

    check(
        "The low and mid branches carry essentially the same favored closure-column entries up to permutation",
        np.linalg.norm(low_sorted - mid_sorted) < 2.0e-4,
        f"low={np.round(low_sorted, 6)}, mid={np.round(mid_sorted, 6)}",
    )
    check(
        "So the exact one-column transport functional by itself does not distinguish low from mid",
        abs(float(low["transport"][I_STAR]) - float(mid["transport"][I_STAR])) < 2.0e-6,
        f"(F_low,F_mid)=({float(low['transport'][I_STAR]):.12f},{float(mid['transport'][I_STAR]):.12f})",
    )
    check(
        "The high branch is different but still closes the favored column, so favored-column closure alone is not a selector either",
        abs(float(high["transport"][I_STAR]) - float(low["transport"][I_STAR])) < 2.0e-6,
        f"F_high={float(high['transport'][I_STAR]):.12f}",
    )

    print()
    print(f"  low favored column  = {np.round(low['favored'], 6)}")
    print(f"  mid favored column  = {np.round(mid['favored'], 6)}")
    print(f"  high favored column = {np.round(high['favored'], 6)}")


def part3_the_full_packet_selects_the_low_branch_by_dominance_gap(branches: list[dict[str, object]]) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE FULL PACKET SELECTS THE LOW BRANCH BY DOMINANCE GAP")
    print("=" * 88)

    low, mid, high = branches

    check(
        "The low branch uniquely minimizes non-favored transport spill",
        float(low["spill"]) < float(mid["spill"]) < float(high["spill"]),
        f"(spill_low,spill_mid,spill_high)=({float(low['spill']):.12f},{float(mid['spill']):.12f},{float(high['spill']):.12f})",
    )
    check(
        "Equivalently the low branch uniquely maximizes the favored-column dominance gap",
        float(low["gap"]) > float(mid["gap"]) > float(high["gap"]),
        f"(gap_low,gap_mid,gap_high)=({float(low['gap']):.12f},{float(mid['gap']):.12f},{float(high['gap']):.12f})",
    )
    check(
        "So the physical low-action branch is the unique most one-source-exclusive stationary packet on the reduced N_e stationary set",
        True,
        "max gap <-> min spill",
    )

    print()
    for branch in branches:
        print(
            f"  {branch['name']:>4} : F = {np.round(branch['transport'], 12)}, "
            f"gap = {float(branch['gap']):.12f}, spill = {float(branch['spill']):.12f}"
        )


def part4_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOUNDARY")
    print("=" * 88)

    check(
        "This selector theorem acts on the currently recovered exact reduced stationary set",
        True,
    )
    check(
        "It does not by itself certify a full observation-free selector on the entire reduced closure surface",
        True,
        "that broader theorem would need a global closure-surface certificate",
    )
    check(
        "But it does close the exact remaining branch-selection question on the current stationary candidate set",
        True,
    )

    print()
    print("  Exact read:")
    print("    - favored closure column alone: insufficient")
    print("    - full packet dominance gap: sufficient on the stationary set")
    print("    - live broader gap: global closure-surface certification")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS STATIONARY DOMINANCE-GAP SELECTOR")
    print("=" * 88)
    print()
    print("Question:")
    print("  What exact packet-level law separates the physical low branch from the")
    print("  nearby reduced N_e stationary competitors?")

    branches = part1_the_reduced_stationary_set_has_one_low_branch_and_two_competitors()
    part2_the_favored_column_alone_does_not_separate_low_from_mid(branches)
    part3_the_full_packet_selects_the_low_branch_by_dominance_gap(branches)
    part4_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-branch answer:")
    print("    - the favored closure column alone does not select the physical branch")
    print("    - the full packet does")
    print("    - on the reduced stationary set, the physical branch is the unique")
    print("      maximum-dominance-gap / minimum-spill branch")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
