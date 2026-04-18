#!/usr/bin/env python3
"""
DM neutrino source-surface global dominance completeness obstruction.

Question:
  Once the selector class is compressed to the canonical extremal law, can the
  preferred recovered point already be promoted to a full exact-carrier winner?

Answer:
  No.

  The recovered winner is real, but the branch still lacks exact-carrier
  completeness or an interval-certified rival-window dominance theorem.

Boundary:
  This is a branch-local obstruction runner. It records the exact stopping
  point of the carrier side without reviving the candidate forest.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from dm_selector_branch_support import (
    EXCEPTIONAL_WINDOWS,
    PREFERRED_RECOVERED_LIFT,
    recovered_bank,
    repair_from_slack_point,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

EXPECTED_TARGET = (1.380791428982, 0.467879209399)
EXPECTED_WINDOWS = [
    ("endpoint", (-1.899713, -1.87)),
    ("split_1", (-1.16, -1.10)),
    ("split_2", (-0.19, -0.14)),
]


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


def part1_the_preferred_recovered_point_is_a_real_recovered_carrier_winner() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PREFERRED RECOVERED POINT IS A REAL RECOVERED-CARRIER WINNER")
    print("=" * 88)

    lifts, _hs, repairs, targets = recovered_bank()
    preferred_idx = int(np.argmin(repairs))
    sorted_repairs = np.sort(repairs)
    winner_gap = float(sorted_repairs[1] - sorted_repairs[0])
    preferred_target = targets[preferred_idx]

    check(
        "The recovered carrier still consists of the same five clustered exact lifts",
        len(lifts) == 5,
        f"repairs={np.round(repairs, 12)}",
    )
    check(
        "The preferred recovered lift is still the unique least-repair point on that recovered carrier",
        preferred_idx == 0 and winner_gap > 0.0,
        f"(winner,gap)=({preferred_idx},{winner_gap:.12e})",
    )
    check(
        "That preferred recovered lift is still the named target point on the active sheet",
        np.linalg.norm(np.asarray(lifts[preferred_idx], dtype=float) - PREFERRED_RECOVERED_LIFT) < 1.0e-12,
        f"preferred={np.round(lifts[preferred_idx], 12)}",
    )
    check(
        "The preferred recovered target in (delta,q_+) is unchanged on the branch",
        abs(preferred_target[0] - EXPECTED_TARGET[0]) < 1.0e-12
        and abs(preferred_target[1] - EXPECTED_TARGET[1]) < 1.0e-12,
        f"target=({preferred_target[0]:.12f},{preferred_target[1]:.12f})",
    )


def part2_the_unresolved_rival_geometry_is_localized_to_three_windows() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE UNRESOLVED RIVAL GEOMETRY IS LOCALIZED TO THREE WINDOWS")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_GLOBAL_DOMINANCE_COMPLETENESS_OBSTRUCTION_NOTE_2026-04-17.md")
    windows = [(name, tuple(float(v) for v in EXCEPTIONAL_WINDOWS[name])) for name, _ in EXPECTED_WINDOWS]
    ordered = [bounds for _name, bounds in windows]

    check(
        "The branch still localizes the rival-side uncertainty to exactly three exposed windows",
        windows == EXPECTED_WINDOWS,
        f"windows={windows}",
    )
    check(
        "Those windows are ordered and disjoint across the rival side",
        ordered[0][0] < ordered[0][1] < ordered[1][0] < ordered[1][1] < ordered[2][0] < ordered[2][1],
        f"ordered={ordered}",
    )
    check(
        "The obstruction note records that the rival-side uncertainty is localized rather than diffuse",
        "localized rival-window picture" in note and "Outside those windows" in note,
    )
    check(
        "The obstruction note records the still-underresolved split-2 slice rather than claiming interval certification",
        "still-underresolved split-2 slice" in note and "interval-certified" in note,
    )
    check(
        "The obstruction note sharpens split-2 further to a low-slack boundary-band issue rather than a whole-window broad failure",
        "low-slack boundary band" in note and "s >= 0.2" in note,
    )
    check(
        "The obstruction note now records the one-dimensional split-2 edge interval on the tested broad bundle",
        "R_split2(s)" in note and "0 <= s < s_*" in note and "0.215677476525" in note,
    )
    check(
        "The obstruction note records that endpoint and split-1 broad-window pressure are already absent on the tested edge-profile hierarchy",
        "collapses entirely to the split-2 edge" in note,
    )
    check(
        "The obstruction note records that the tested split-2 edge undercut is transport-incompatible with the preferred recovered lane",
        "transport-incompatible with the preferred" in note and "0.847299300834" in note and "1.052220313052" in note,
    )
    check(
        "The obstruction note records that no lower-repair transport-compatible lane is currently visible on the tested broad split-2 low-slack box",
        "0.884523453538" in note and "0.233468501596" in note and "no lower-repair transport-compatible lane is currently" in note,
    )
    check(
        "The obstruction note records that the tested residual transport pressure already collapses toward the upper-m low-slack ridge",
        "upper-" in note and "m=-0.14" in note and "low-slack ridge" in note,
    )
    check(
        "The obstruction note records that the sampled split-2 upper-face pressure sharpens to two explicit extremals",
        "0.0195041737783" in note and "1.188513342509166" in note and "1.188955544069478" in note and "0.233274467128" in note,
    )


def part3_exact_carrier_completeness_and_global_dominance_remain_unproved() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EXACT-CARRIER COMPLETENESS AND GLOBAL DOMINANCE REMAIN UNPROVED")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_GLOBAL_DOMINANCE_COMPLETENESS_OBSTRUCTION_NOTE_2026-04-17.md")
    conclusion_note = read("docs/DM_SELECTOR_BRANCH_CONCLUSION_NOTE_2026-04-17.md")

    check(
        "The obstruction note explicitly says the recovered carrier has not yet been promoted to the full exact carrier",
        "recovered carrier already exhausts the full exact carrier" in note,
    )
    check(
        "The obstruction note names interval-certified completeness or dominance as the missing theorem",
        "interval-certified exclusion theorem" in note and "global lower-bound theorem" in note,
    )
    check(
        "The obstruction note sharpens the missing carrier theorem to transport-compatible neighborhoods of the two split-2 upper-face extremals",
        "transport-compatible lane" in note and "two explicit split-2 upper-`m` face extremals" in note,
    )
    check(
        "The branch conclusion note keeps the overall branch verdict at obstruction",
        "Final verdict: `obstruction`." in conclusion_note,
    )
    check(
        "The branch conclusion note names exact-carrier completeness / global dominance as one of the two exact blockers",
        "exact-carrier completeness / global dominance" in conclusion_note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE GLOBAL DOMINANCE COMPLETENESS OBSTRUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  After representation compression, can the preferred recovered point already")
    print("  be promoted to a full exact-carrier winner?")

    part1_the_preferred_recovered_point_is_a_real_recovered_carrier_winner()
    part2_the_unresolved_rival_geometry_is_localized_to_three_windows()
    part3_exact_carrier_completeness_and_global_dominance_remain_unproved()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact carrier-side branch verdict:")
    print("    - the preferred recovered point is a real recovered-carrier winner")
    print("    - the unresolved rival geometry is localized to three exposed windows")
    print("    - exact-carrier completeness / global dominance is still unproved")
    print("  RESULT: obstruction at exact-carrier completeness / global dominance")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
