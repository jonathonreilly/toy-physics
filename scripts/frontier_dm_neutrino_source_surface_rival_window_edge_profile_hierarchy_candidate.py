#!/usr/bin/env python3
"""
DM neutrino source-surface rival-window edge-profile hierarchy candidate.

Question:
  After reducing split-2 to a one-dimensional edge interval on the tested broad
  bundle, what remains of the other two rival windows on the same edge-profile
  footing?

Answer:
  On the tested broad exact shift-quotient bundle, the three rival windows have
  a strict edge-profile hierarchy:

      R_endpoint(s) > R_split1(s) > R_split2(s)

  across the tested slack range, with all three profiles strictly increasing in
  `s`. Endpoint and split-1 are already above the preferred recovered floor at
  `s = 0`, while split-2 alone crosses that floor at the explicit threshold
  `s_* ~= 0.195041737783`.

  So on the tested broad bundle, broad-window carrier pressure collapses
  entirely to the one-dimensional split-2 edge interval `0 <= s < s_*`.

Boundary:
  This is still a numerical candidate on broad exact-bundle edge profiles, not
  an interval-certified theorem on the finer exact carrier.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

from dm_selector_branch_support import PREFERRED_RECOVERED_LIFT, repair_from_slack_point

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from frontier_dm_neutrino_source_surface_split2_edge_profile_transition_candidate import (  # noqa: E402
    EXPECTED_ROOT,
    edge_profile as split2_edge_profile,
)
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import quotient_gauge_h  # noqa: E402

PASS_COUNT = 0
FAIL_COUNT = 0

WINDOW_EDGE_M = {
    "endpoint": -1.87,
    "split_1": -1.10,
    "split_2": -0.14,
}
EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_ZERO_SLACK_VALUES = {
    "endpoint": 3.0275558466100914,
    "split_1": 2.3086034009138230,
    "split_2": 1.5004424916582053,
}
EXPECTED_ZERO_SLACK_DELTAS = {
    "endpoint": 1.1456887136709648,
    "split_1": 1.0884024518256670,
}
SLACK_GRID = [0.0, 0.05, 0.10, 0.15, 0.19, 0.20, 0.25, 0.30]


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


def edge_repair(m_edge: float, delta: float, slack: float) -> float:
    r31 = math.sqrt(float(slack) * float(slack) + 0.25)
    h, _pars = quotient_gauge_h(float(m_edge), float(delta), r31)
    return max(0.0, -float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))))


def generic_edge_profile(m_edge: float, slack: float) -> tuple[float, float]:
    res = minimize_scalar(
        lambda delta: edge_repair(m_edge, delta, slack),
        bounds=(-2.5, 2.5),
        method="bounded",
        options={"xatol": 1.0e-10, "maxiter": 500},
    )
    return float(res.x), float(res.fun)


def part1_endpoint_and_split1_start_above_the_preferred_floor_even_at_zero_slack(pref: float) -> None:
    print("\n" + "=" * 88)
    print("PART 1: ENDPOINT AND SPLIT-1 START ABOVE THE PREFERRED FLOOR AT ZERO SLACK")
    print("=" * 88)

    for name in ("endpoint", "split_1"):
        delta_star, value_star = generic_edge_profile(WINDOW_EDGE_M[name], 0.0)
        check(
            f"The {name} edge profile at s=0 is reproduced stably",
            abs(delta_star - EXPECTED_ZERO_SLACK_DELTAS[name]) < 5.0e-8
            and abs(value_star - EXPECTED_ZERO_SLACK_VALUES[name]) < 1.0e-10,
            f"(delta*,R(0))=({delta_star:.12f},{value_star:.12f})",
        )
        check(
            f"The {name} edge profile is already above the preferred recovered floor at s=0",
            value_star > pref,
            f"gap={value_star - pref:.12e}",
        )


def part2_the_three_edge_profiles_form_a_strict_hierarchy_on_the_test_grid() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE THREE EDGE PROFILES FORM A STRICT HIERARCHY ON THE TEST GRID")
    print("=" * 88)

    endpoint_vals = []
    split1_vals = []
    split2_vals = []

    for slack in SLACK_GRID:
        endpoint_vals.append(generic_edge_profile(WINDOW_EDGE_M["endpoint"], slack)[1])
        split1_vals.append(generic_edge_profile(WINDOW_EDGE_M["split_1"], slack)[1])
        split2_vals.append(split2_edge_profile(slack)[1])

    check(
        "The endpoint edge profile is strictly increasing on the tested slack grid",
        all(b > a for a, b in zip(endpoint_vals, endpoint_vals[1:])),
        f"endpoint={[round(v, 9) for v in endpoint_vals]}",
    )
    check(
        "The split-1 edge profile is strictly increasing on the tested slack grid",
        all(b > a for a, b in zip(split1_vals, split1_vals[1:])),
        f"split1={[round(v, 9) for v in split1_vals]}",
    )
    check(
        "The split-2 edge profile is strictly increasing on the tested slack grid",
        all(b > a for a, b in zip(split2_vals, split2_vals[1:])),
        f"split2={[round(v, 9) for v in split2_vals]}",
    )
    check(
        "Across the tested slack grid the edge-profile hierarchy stays strict: endpoint > split-1 > split-2",
        all(e > s1 > s2 for e, s1, s2 in zip(endpoint_vals, split1_vals, split2_vals)),
        "broad-window pressure orders strictly by window",
    )


def part3_broad_bundle_pressure_collapses_to_the_split2_edge_interval(pref: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: BROAD-BUNDLE PRESSURE COLLAPSES TO THE SPLIT-2 EDGE INTERVAL")
    print("=" * 88)

    endpoint_zero = generic_edge_profile(WINDOW_EDGE_M["endpoint"], 0.0)[1]
    split1_zero = generic_edge_profile(WINDOW_EDGE_M["split_1"], 0.0)[1]
    split2_zero = split2_edge_profile(0.0)[1]

    check(
        "Endpoint broad-edge pressure never reaches the preferred floor on the tested slack regime because it already starts well above it",
        endpoint_zero > pref and abs(endpoint_zero - EXPECTED_ZERO_SLACK_VALUES["endpoint"]) < 1.0e-10,
        f"endpoint_gap={endpoint_zero - pref:.12e}",
    )
    check(
        "Split-1 broad-edge pressure also never reaches the preferred floor on the tested slack regime because it already starts above it",
        split1_zero > pref and abs(split1_zero - EXPECTED_ZERO_SLACK_VALUES["split_1"]) < 1.0e-10,
        f"split1_gap={split1_zero - pref:.12e}",
    )
    check(
        "Split-2 alone starts below the preferred floor on the broad edge and therefore carries the only tested broad-bundle undercut",
        split2_zero < pref and abs(split2_zero - EXPECTED_ZERO_SLACK_VALUES["split_2"]) < 1.0e-10,
        f"split2_gap={split2_zero - pref:.12e}",
    )
    check(
        "So on the tested broad bundle the whole rival-window pressure collapses to the split-2 edge interval 0 <= s < s_*",
        endpoint_zero > pref and split1_zero > pref and split2_zero < pref,
        f"s_*={EXPECTED_ROOT:.12f}",
    )


def part4_the_note_records_the_edge_profile_hierarchy() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE EDGE-PROFILE HIERARCHY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_RIVAL_WINDOW_EDGE_PROFILE_HIERARCHY_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the strict edge-profile hierarchy and the split-2 threshold",
        "R_endpoint(s) > R_split1(s) > R_split2(s)" in note and "0.195041737783" in note,
    )
    check(
        "The note records that broad-window pressure collapses to the split-2 edge interval",
        "collapses entirely to the one-dimensional split-2 edge interval" in note,
    )
    check(
        "The note keeps the boundary honest: this is still not interval-certified exact-carrier closure",
        "not an interval-certified theorem" in note and "not flagship closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE RIVAL-WINDOW EDGE-PROFILE HIERARCHY CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the tested broad bundle, what remains of the other rival windows after")
    print("  split-2 is reduced to a one-dimensional edge profile?")

    pref = float(repair_from_slack_point(PREFERRED_RECOVERED_LIFT))
    check(
        "The preferred recovered floor is unchanged on the compact branch",
        abs(pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"preferred={pref:.12f}",
    )

    part1_endpoint_and_split1_start_above_the_preferred_floor_even_at_zero_slack(pref)
    part2_the_three_edge_profiles_form_a_strict_hierarchy_on_the_test_grid()
    part3_broad_bundle_pressure_collapses_to_the_split2_edge_interval(pref)
    part4_the_note_records_the_edge_profile_hierarchy()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact compact-branch broad-bundle rival-window verdict:")
    print("    - endpoint and split-1 edge profiles are already dominated from s = 0 upward")
    print("    - split-2 alone crosses the preferred floor, at s_* = 0.195041737783")
    print("    - broad-window carrier pressure therefore collapses to the split-2 edge interval")
    print("      0 <= s < s_* on the tested broad bundle")
    print("  RESULT: the tested broad-bundle rival geometry is supported only by split-2 edge data")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
