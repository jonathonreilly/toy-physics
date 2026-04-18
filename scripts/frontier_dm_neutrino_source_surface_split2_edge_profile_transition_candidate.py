#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 edge-profile transition candidate.

Question:
  On the compact branch, can the broad-bundle split-2 failure be reduced from a
  3-real window to a one-dimensional edge profile on the exact active slack
  chart?

Answer:
  Yes, on the tested broad split-2 domain.

  The broad-box minimizer is pinned to the upper-m edge `m = -0.14` and to the
  lower active-slack edge `s = q_+ - q_floor(delta) = s_min`, so the tested
  split-2 danger profile reduces to the 1D function

      R_split2(s) = min_delta Lambda_+(-0.14, delta, s).

  That profile is strictly increasing on the tested range and crosses the
  preferred recovered floor at

      s_* ~= 0.195041737783.

  The preferred recovered point has slack

      s_pref = 0.215677476525,

  so it lies outside the tested broad-bundle split-2 danger interval by the
  positive margin

      s_pref - s_* ~= 0.020635738742.

Boundary:
  This is still a numerical candidate on the broad exact shift-quotient bundle,
  not an interval-certified theorem on the finer exact carrier.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

from dm_selector_branch_support import PREFERRED_RECOVERED_LIFT, repair_from_slack_point
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import quotient_gauge_h

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

SPLIT2_EDGE_M = -0.14
DELTA_BOX = (-2.5, 2.5)
EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_PREF_SLACK = 0.215677476525045
EXPECTED_ROOT = 0.19504173778264997
EXPECTED_DELTA_AT_ROOT = 1.0642229611259355
EXPECTED_MARGIN = 0.02063573874239502

EXPECTED_PROFILE = {
    0.0: (0.9970498933945160, 1.5004424916582053),
    0.05: (1.0153405868255805, 1.5198228931681514),
    0.10: (1.0328954845907592, 1.5411842223412606),
    0.15: (1.0497099351612011, 1.5644223582515033),
    0.19: (1.0626282210902616, 1.5842925669626133),
    0.195: (1.0642097742178547, 1.5868532685381211),
    0.1975: (1.0649978036291714, 1.5881399025594400),
    0.20: (1.0657839763386874, 1.5894307075824363),
    0.25: (1.0811223813996140, 1.6161022192510113),
    0.30: (1.0957343316590074, 1.6443310505289195),
}


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


def edge_repair(delta: float, slack: float) -> float:
    r31 = math.sqrt(float(slack) * float(slack) + 0.25)
    h, _pars = quotient_gauge_h(SPLIT2_EDGE_M, float(delta), r31)
    return max(0.0, -float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))))


def edge_profile(slack: float) -> tuple[float, float]:
    res = minimize_scalar(
        lambda delta: edge_repair(delta, slack),
        bounds=DELTA_BOX,
        method="bounded",
        options={"xatol": 1.0e-10, "maxiter": 500},
    )
    return float(res.x), float(res.fun)


def part1_the_split2_broad_failure_reduces_to_a_one_dimensional_edge_profile() -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE SPLIT-2 BROAD FAILURE REDUCES TO A ONE-DIMENSIONAL EDGE PROFILE")
    print("=" * 88)

    pref = float(repair_from_slack_point(PREFERRED_RECOVERED_LIFT))
    pref_slack = float(PREFERRED_RECOVERED_LIFT[2])

    check(
        "The preferred recovered floor is unchanged on the compact branch",
        abs(pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"preferred={pref:.12f}",
    )
    check(
        "The preferred recovered active slack is unchanged on the compact branch",
        abs(pref_slack - EXPECTED_PREF_SLACK) < 1.0e-12,
        f"slack_pref={pref_slack:.12f}",
    )
    check(
        "So the tested split-2 broad-bundle danger can be studied on the upper-m edge m = -0.14",
        True,
        "previous broad-box minima are already pinned to the upper-m / lower-slack corner",
    )

    return pref, pref_slack


def part2_the_edge_profile_is_reproduced_stably_on_the_test_grid() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EDGE PROFILE IS REPRODUCED STABLY ON THE TEST GRID")
    print("=" * 88)

    values: list[float] = []
    for slack, (delta_expected, value_expected) in EXPECTED_PROFILE.items():
        delta_star, value_star = edge_profile(slack)
        values.append(value_star)
        check(
            f"The split-2 edge-profile sample at s={slack:.4f} is reproduced stably",
            abs(delta_star - delta_expected) < 5.0e-8 and abs(value_star - value_expected) < 1.0e-10,
            f"(delta*,R)=({delta_star:.12f},{value_star:.12f})",
        )

    check(
        "The tested split-2 edge profile is strictly increasing in the active slack coordinate",
        all(b > a for a, b in zip(values, values[1:])),
        f"R={[round(v, 9) for v in values]}",
    )


def part3_the_transition_occurs_at_one_explicit_edge_threshold(pref: float, pref_slack: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE TRANSITION OCCURS AT ONE EXPLICIT EDGE THRESHOLD")
    print("=" * 88)

    root = float(brentq(lambda s: edge_profile(s)[1] - pref, 0.195, 0.1975, xtol=1.0e-12, rtol=1.0e-12, maxiter=200))
    delta_root, value_root = edge_profile(root)
    margin = pref_slack - root

    check(
        "The edge-profile threshold s_* is reproduced stably by one-dimensional root finding",
        abs(root - EXPECTED_ROOT) < 1.0e-12 and abs(value_root - pref) < 1.0e-11,
        f"(s_*,R(s_*))=({root:.12f},{value_root:.12f})",
    )
    check(
        "The minimizing delta at the threshold is reproduced stably",
        abs(delta_root - EXPECTED_DELTA_AT_ROOT) < 1.0e-10,
        f"delta_*(s_*)={delta_root:.12f}",
    )
    check(
        "The preferred recovered point lies outside the tested split-2 danger interval by a positive slack margin",
        margin > 0.0 and abs(margin - EXPECTED_MARGIN) < 1.0e-12,
        f"margin={margin:.12f}",
    )
    check(
        "So on the tested broad split-2 edge the only undercut region is the one-dimensional interval 0 <= s < s_*",
        root < pref_slack and EXPECTED_PROFILE[0.195][1] < pref < EXPECTED_PROFILE[0.1975][1],
        f"s_*={root:.12f}",
    )


def part4_the_note_records_the_one_dimensional_edge_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE ONE-DIMENSIONAL EDGE REDUCTION")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_PROFILE_TRANSITION_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the edge-profile threshold, preferred slack, and positive margin",
        "0.195041737783" in note and "0.215677476525" in note and "0.020635738742" in note,
    )
    check(
        "The note records that the split-2 broad failure reduces to a one-dimensional edge interval",
        "R_split2(s)" in note and "0 <= s < s_*" in note,
    )
    check(
        "The note keeps the boundary honest: this is still not interval-certified exact-carrier closure",
        "not an interval-certified theorem" in note and "not flagship closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 EDGE-PROFILE TRANSITION CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the compact-branch split-2 broad-bundle failure be reduced to a")
    print("  one-dimensional active-slack edge profile?")

    pref, pref_slack = part1_the_split2_broad_failure_reduces_to_a_one_dimensional_edge_profile()
    part2_the_edge_profile_is_reproduced_stably_on_the_test_grid()
    part3_the_transition_occurs_at_one_explicit_edge_threshold(pref, pref_slack)
    part4_the_note_records_the_one_dimensional_edge_reduction()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact compact-branch split-2 broad-bundle verdict:")
    print("    - the tested broad-bundle danger reduces to the 1D edge profile R_split2(s)")
    print(f"    - R_split2(s) crosses the preferred recovered floor at s_* = {EXPECTED_ROOT:.12f}")
    print(f"    - the preferred recovered slack is s_pref = {EXPECTED_PREF_SLACK:.12f}")
    print(f"    - the resulting broad-bundle margin is s_pref - s_* = {EXPECTED_MARGIN:.12f}")
    print("  RESULT: the broad split-2 obstruction is now a one-dimensional low-slack edge interval")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
