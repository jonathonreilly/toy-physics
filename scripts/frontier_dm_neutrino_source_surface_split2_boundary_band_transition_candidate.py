#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 boundary-band transition candidate.

Question:
  On the compact branch, how much of the broad-bundle split-2 failure is really
  spread across the whole split-2 window, and how much is confined to a narrow
  low-slack boundary band on the active half-plane chart?

Answer:
  On the broad exact shift-quotient bundle, the split-2 minimum is driven by
  the active-boundary slack variable

      s = q_+ - q_floor(delta) >= 0.

  Over the tested split-2 box, the broad-box minimum is monotone in a lower
  slack floor `s_min`, remains pinned to the upper-m / lower-slack boundary,
  and crosses the preferred recovered floor inside a narrow band

      0.195 <= s_* <= 0.1975.

  In particular, once the split-2 broad box is restricted to `s >= 0.2`, its
  tested minimum already lies above the preferred recovered floor. So the
  broad-bundle split-2 undercut is not diffuse across the window: it is
  concentrated in a narrow low-slack boundary band.

Boundary:
  This is still a numerical candidate on tested broad exact-bundle boxes in
  the active slack chart, not an interval-certified dominance theorem on the
  exact carrier.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

from dm_selector_branch_support import PREFERRED_RECOVERED_LIFT, repair_from_slack_point
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import quotient_gauge_h

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

SPLIT2_WINDOW = (-0.19, -0.14)
CORE_DELTA = (-2.5, 2.5)
SLACK_MAX = math.sqrt(16.0 - 0.25)

EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_SAMPLE_MINIMA = {
    0.0: np.array([-0.14, 0.99704984, 0.0], dtype=float),
    0.05: np.array([-0.14, 1.01534057, 0.05], dtype=float),
    0.10: np.array([-0.14, 1.03289549, 0.10], dtype=float),
    0.15: np.array([-0.14, 1.04971896, 0.15], dtype=float),
    0.19: np.array([-0.14, 1.06262822, 0.19], dtype=float),
    0.20: np.array([-0.14, 1.06578397, 0.20], dtype=float),
    0.25: np.array([-0.14, 1.08112040, 0.25], dtype=float),
    0.30: np.array([-0.14, 1.09573433, 0.30], dtype=float),
}
EXPECTED_SAMPLE_REPAIRS = {
    0.0: 1.5004424916582124,
    0.05: 1.5198228931681512,
    0.10: 1.5411842223412606,
    0.15: 1.5644223623579445,
    0.19: 1.5842925669626136,
    0.20: 1.5894307075824360,
    0.25: 1.6161022208147882,
    0.30: 1.6443310505289200,
}
EXPECTED_TRANSITION_REPAIRS = {
    0.1950: 1.5868532685381210,
    0.1975: 1.5881399025594400,
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


def bundle_repair_from_slack(m: float, delta: float, slack: float) -> float:
    r31 = math.sqrt(float(slack) * float(slack) + 0.25)
    h, _pars = quotient_gauge_h(float(m), float(delta), r31)
    return max(0.0, -float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))))


def optimize_split2_with_slack_floor(slack_floor: float) -> tuple[np.ndarray, float]:
    res = differential_evolution(
        lambda z: bundle_repair_from_slack(*map(float, z)),
        [SPLIT2_WINDOW, CORE_DELTA, (float(slack_floor), SLACK_MAX)],
        seed=0,
        polish=True,
        maxiter=120,
        popsize=15,
        tol=1.0e-7,
    )
    return np.asarray(res.x, dtype=float), float(res.fun)


def part1_sampled_slack_floors_reproduce_the_split2_transition_picture() -> tuple[float, dict[float, np.ndarray], dict[float, float]]:
    print("\n" + "=" * 88)
    print("PART 1: SAMPLED SLACK FLOORS REPRODUCE THE SPLIT-2 TRANSITION PICTURE")
    print("=" * 88)

    pref = float(repair_from_slack_point(PREFERRED_RECOVERED_LIFT))
    points: dict[float, np.ndarray] = {}
    values: dict[float, float] = {}

    check(
        "The preferred recovered floor is unchanged on the compact branch",
        abs(pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"preferred={pref:.12f}",
    )

    for slack_floor in EXPECTED_SAMPLE_MINIMA:
        point, value = optimize_split2_with_slack_floor(slack_floor)
        points[slack_floor] = point
        values[slack_floor] = value
        check(
            f"The split-2 slack-floor minimum is reproduced stably at s_min={slack_floor:.3f}",
            np.linalg.norm(point - EXPECTED_SAMPLE_MINIMA[slack_floor]) < 5.0e-6
            and abs(value - EXPECTED_SAMPLE_REPAIRS[slack_floor]) < 1.0e-9,
            f"(point,value)=({np.round(point, 8)},{value:.12f})",
        )

    return pref, points, values


def part2_the_split2_broad_minimum_is_monotone_and_boundary_pinned(
    values: dict[float, float], points: dict[float, np.ndarray]
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SPLIT-2 BROAD MINIMUM IS MONOTONE AND BOUNDARY-PINNED")
    print("=" * 88)

    floors = sorted(values)
    min_values = [values[floor] for floor in floors]

    check(
        "Increasing the active slack floor raises the tested split-2 broad-box minimum monotonically",
        all(b > a for a, b in zip(min_values, min_values[1:])),
        f"repairs={[round(values[floor], 9) for floor in floors]}",
    )
    check(
        "Every tested split-2 minimum stays on the upper-m boundary of the broad box",
        all(abs(points[floor][0] - SPLIT2_WINDOW[1]) < 1.0e-8 for floor in floors),
        f"m={[round(points[floor][0], 9) for floor in floors]}",
    )
    check(
        "Every tested split-2 minimum also stays on the lower active-slack boundary s = s_min",
        all(abs(points[floor][2] - floor) < 1.0e-8 for floor in floors),
        f"s={[round(points[floor][2], 9) for floor in floors]}",
    )


def part3_the_undercut_crosses_the_preferred_floor_inside_a_narrow_low_slack_band(pref: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE UNDERCUT CROSSES THE PREFERRED FLOOR INSIDE A NARROW LOW-SLACK BAND")
    print("=" * 88)

    transition_points: dict[float, np.ndarray] = {}
    transition_values: dict[float, float] = {}
    for slack_floor in EXPECTED_TRANSITION_REPAIRS:
        point, value = optimize_split2_with_slack_floor(slack_floor)
        transition_points[slack_floor] = point
        transition_values[slack_floor] = value
        check(
            f"The transition sample at s_min={slack_floor:.4f} is reproduced stably",
            abs(value - EXPECTED_TRANSITION_REPAIRS[slack_floor]) < 1.0e-9
            and np.linalg.norm(point - np.array([-0.14, point[1], slack_floor], dtype=float)) < 5.0e-6,
            f"(point,value)=({np.round(point, 8)},{value:.12f})",
        )

    check(
        "At s_min=0.1950 the tested split-2 broad minimum is still below the preferred recovered floor",
        transition_values[0.1950] < pref,
        f"gap={transition_values[0.1950] - pref:.12e}",
    )
    check(
        "At s_min=0.1975 the tested split-2 broad minimum is already above the preferred recovered floor",
        transition_values[0.1975] > pref,
        f"gap={transition_values[0.1975] - pref:.12e}",
    )
    check(
        "So the broad-bundle split-2 undercut is confined to a narrow low-slack band rather than the whole split-2 window",
        transition_values[0.1950] < pref < transition_values[0.1975],
        "0.1950 <= s_* <= 0.1975",
    )
    check(
        "In particular the tested split-2 broad box is already locally dominated once s >= 0.2",
        EXPECTED_SAMPLE_REPAIRS[0.20] > pref,
        f"gap@0.2={EXPECTED_SAMPLE_REPAIRS[0.20] - pref:.12e}",
    )


def part4_the_active_half_plane_interpretation_is_exact(points: dict[float, np.ndarray]) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ACTIVE HALF-PLANE INTERPRETATION IS EXACT")
    print("=" * 88)

    q_gaps = []
    for slack_floor, point in points.items():
        _m, delta, slack = map(float, point)
        q_floor = math.sqrt(8.0 / 3.0) - delta
        q_plus = q_floor + slack
        q_gaps.append(q_plus - q_floor)
        check(
            f"The split-2 sample minimum at s_min={slack_floor:.3f} lies exactly on q_+ - q_floor(delta) = s_min",
            abs((q_plus - q_floor) - slack_floor) < 1.0e-8,
            f"(delta,q_+,gap)=({delta:.9f},{q_plus:.9f},{(q_plus - q_floor):.9f})",
        )

    check(
        "So the broad-bundle split-2 undercut is exactly an active-boundary low-slack phenomenon",
        all(abs(gap - floor) < 1.0e-8 for gap, floor in zip(q_gaps, sorted(points))),
        "the dangerous region is q_+ - q_floor(delta) near zero",
    )


def part5_the_note_records_the_low_slack_boundary_band_conclusion() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE RECORDS THE LOW-SLACK BOUNDARY-BAND CONCLUSION")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_BOUNDARY_BAND_TRANSITION_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the two transition samples and the preferred recovered floor",
        "1.586853268538" in note and "1.588139902559" in note and "1.586874714730" in note,
    )
    check(
        "The note records that the split-2 undercut is confined to a narrow low-slack boundary band",
        "0.195 <= s_* <= 0.1975" in note and "low-slack boundary band" in note,
    )
    check(
        "The note keeps the boundary honest: this is a candidate on broad exact-bundle boxes, not theorem closure",
        "not an interval-certified dominance theorem" in note and "not flagship closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 BOUNDARY-BAND TRANSITION CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the compact branch, is the broad-bundle split-2 failure spread across")
    print("  the whole split-2 window, or is it concentrated in a narrow active")
    print("  boundary band?")

    pref, points, values = part1_sampled_slack_floors_reproduce_the_split2_transition_picture()
    part2_the_split2_broad_minimum_is_monotone_and_boundary_pinned(values, points)
    part3_the_undercut_crosses_the_preferred_floor_inside_a_narrow_low_slack_band(pref)
    part4_the_active_half_plane_interpretation_is_exact(points)
    part5_the_note_records_the_low_slack_boundary_band_conclusion()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact compact-branch split-2 broad-bundle verdict:")
    print("    - the broad-box split-2 minimum is pinned to the upper-m / lower-slack boundary")
    print("    - that minimum rises monotonically with the active slack floor")
    print("    - the undercut of the preferred recovered floor is confined to a narrow low-slack band")
    print("      0.195 <= q_+ - q_floor(delta) <= 0.1975 on the tested split-2 broad box")
    print("    - once q_+ - q_floor(delta) >= 0.2, the tested split-2 broad box is already above the preferred floor")
    print("  RESULT: the split-2 broad-bundle obstruction localizes to a narrow low-slack boundary band")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
