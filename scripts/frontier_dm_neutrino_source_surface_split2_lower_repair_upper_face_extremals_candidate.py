#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 lower-repair upper-face extremals candidate.

Question:
  On the tested split-2 low-slack broad box under the lower-repair constraint
  `Lambda_+ <= Lambda_+(x_*)`, does the remaining transport pressure still fill
  a region, or does it already collapse to explicit upper-face extremals?

Answer:
  On the tested box, it already collapses sharply.

  First, on sampled lower-repair slices of the tested box, both transport-facing
  objectives drift monotonically toward the upper-`m` face `m = -0.14`.

  Second, on that sampled upper face:

  - the best lower-repair transport value on each sampled slack slice is
    attained at the repair-cap boundary

        Lambda_+(-0.14, delta_cap(s), s) = Lambda_+(x_*),

  - the sampled cap profile `delta_cap(s)` is strictly decreasing in `s`,
  - the sampled cap-eta profile is unimodal, peaking near
    `s ~= 0.0195041737783`,
  - the sampled closest-lane point on the whole upper-face feasible region is
    the slack-floor endpoint `s = 0`, `delta = delta_edge`.

  So the tested broad split-2 low-slack pressure is no longer a diffuse box and
  no longer just a vague ridge. It is already compressed to two explicit
  upper-face extremals:

  - best-eta cap point:
      `(m,s,delta) = (-0.14, 0.0195041737783, 1.188513342509166)`
      with `eta/eta_obs ~= 0.884523189582`
  - closest-lane endpoint:
      `(m,s,delta) = (-0.14, 0, 1.188955544069478)`
      with `||sort(P_best)-Q_pref||_2 ~= 0.233274467128`

Boundary:
  This is still a tested upper-face extremal candidate, not interval-certified
  exact-carrier closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from dm_selector_branch_support import PREFERRED_RECOVERED_LIFT
from frontier_dm_neutrino_source_surface_split2_low_slack_transport_incompatibility_candidate import (
    EXPECTED_PREF_REPAIR,
    point_data,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

UPPER_M = -0.14
UPPER_FACE_SLACK_MAX = 0.18528965089385
SLICE_M_GRID = np.linspace(-0.19, -0.14, 11)
SLICE_SLACK_GRID = np.linspace(0.0, 0.195041737783, 21)
SLICE_DELTA_GRID = np.linspace(1.0, 1.25, 401)
CAP_SLACK_GRID = np.linspace(0.0, UPPER_FACE_SLACK_MAX, 20)
CAP_DELTA_SCAN = np.linspace(0.95, 1.25, 601)
CAP_DELTA_GRID_COUNT = 401

EXPECTED_SLICE_MAX_ETA = np.array(
    [
        0.8727888849188903,
        0.8738943594605764,
        0.8749713832165070,
        0.8761536153419146,
        0.8772263384339698,
        0.8784042284944286,
        0.8796157520680362,
        0.8807759526814888,
        0.8819778651089494,
        0.8832524561042897,
        0.8844712245052873,
    ],
    dtype=float,
)
EXPECTED_SLICE_MAX_ETA_SLACK = np.array(
    [
        0.02925626066745,
        0.02925626066745,
        0.02925626066745,
        0.02925626066745,
        0.02925626066745,
        0.02925626066745,
        0.02925626066745,
        0.02925626066745,
        0.0195041737783,
        0.0195041737783,
        0.0195041737783,
    ],
    dtype=float,
)
EXPECTED_SLICE_MIN_DIST = np.array(
    [
        0.29962106966169555,
        0.29156645347627697,
        0.28369543660639734,
        0.27677072285587290,
        0.26924210100062140,
        0.26261794936899810,
        0.25684263776830457,
        0.25047815161554754,
        0.24492710677292600,
        0.23881761787484230,
        0.23348669045316406,
    ],
    dtype=float,
)

EXPECTED_CAP_DELTA_START = 1.1889555440694775
EXPECTED_CAP_DELTA_END = 1.1067278686123574
EXPECTED_CAP_ETA_PEAK_SLACK = 0.0195041737783
EXPECTED_CAP_ETA_PEAK_DELTA = 1.1885133425091660
EXPECTED_CAP_ETA_PEAK = 0.8845231895823408
EXPECTED_CAP_CLOSEST_SLACK = 0.0
EXPECTED_CAP_CLOSEST_DELTA = 1.1889555440694775
EXPECTED_CAP_CLOSEST_DIST = 0.23327446712826647
EXPECTED_CAP_CLOSEST_ETA = 0.8836314248166529


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


def preferred_column() -> np.ndarray:
    m, delta, slack = [float(x) for x in PREFERRED_RECOVERED_LIFT]
    return point_data((m, delta, slack))[3]


def cap_delta(slack: float) -> float:
    vals = np.array([point_data((UPPER_M, delta, slack))[0] - EXPECTED_PREF_REPAIR for delta in CAP_DELTA_SCAN], dtype=float)
    indices = np.where(vals <= 0.0)[0]
    if len(indices) == 0:
        raise ValueError(f"no lower-repair point found on sampled upper face for slack={slack}")
    idx = int(indices[-1])
    if idx < len(CAP_DELTA_SCAN) - 1 and vals[idx] * vals[idx + 1] <= 0.0:
        return float(
            brentq(
                lambda delta: point_data((UPPER_M, float(delta), slack))[0] - EXPECTED_PREF_REPAIR,
                float(CAP_DELTA_SCAN[idx]),
                float(CAP_DELTA_SCAN[idx + 1]),
                xtol=1.0e-14,
                rtol=1.0e-14,
                maxiter=200,
            )
        )
    return float(CAP_DELTA_SCAN[idx])


def part1_sampled_lower_repair_transport_pressure_drifts_monotonically_to_the_upper_face(
    q_pref: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 1: SAMPLED LOWER-REPAIR PRESSURE DRIFTS TO THE UPPER-m FACE")
    print("=" * 88)

    best_eta_vals = []
    best_eta_slacks = []
    best_dist_vals = []
    for m in SLICE_M_GRID:
        max_eta = -1.0
        max_eta_slack = 0.0
        min_dist = float("inf")
        for slack in SLICE_SLACK_GRID:
            for delta in SLICE_DELTA_GRID:
                repair, eta_best, _winner, column = point_data((float(m), float(delta), float(slack)))
                if repair <= EXPECTED_PREF_REPAIR + 1.0e-9:
                    if eta_best > max_eta:
                        max_eta = eta_best
                        max_eta_slack = float(slack)
                    dist = float(np.linalg.norm(column - q_pref))
                    if dist < min_dist:
                        min_dist = dist
        best_eta_vals.append(max_eta)
        best_eta_slacks.append(max_eta_slack)
        best_dist_vals.append(min_dist)

    best_eta_vals = np.asarray(best_eta_vals, dtype=float)
    best_eta_slacks = np.asarray(best_eta_slacks, dtype=float)
    best_dist_vals = np.asarray(best_dist_vals, dtype=float)

    check(
        "The sampled lower-repair slice-wise best eta values are reproduced stably across the split-2 box",
        np.max(np.abs(best_eta_vals - EXPECTED_SLICE_MAX_ETA)) < 1.0e-12
        and np.max(np.abs(best_eta_slacks - EXPECTED_SLICE_MAX_ETA_SLACK)) < 1.0e-12,
        f"eta_by_m={np.round(best_eta_vals, 12)}",
    )
    check(
        "The sampled lower-repair slice-wise closest-lane distances are reproduced stably across the split-2 box",
        np.max(np.abs(best_dist_vals - EXPECTED_SLICE_MIN_DIST)) < 1.0e-12,
        f"dist_by_m={np.round(best_dist_vals, 12)}",
    )
    check(
        "Sampled lower-repair best-eta values increase monotonically toward the upper-m boundary",
        all(b >= a - 1.0e-12 for a, b in zip(best_eta_vals, best_eta_vals[1:])),
        f"eta_start={best_eta_vals[0]:.12f}, eta_end={best_eta_vals[-1]:.12f}",
    )
    check(
        "Sampled lower-repair closest-lane distances decrease monotonically toward the upper-m boundary",
        all(b <= a + 1.0e-12 for a, b in zip(best_dist_vals, best_dist_vals[1:])),
        f"dist_start={best_dist_vals[0]:.12f}, dist_end={best_dist_vals[-1]:.12f}",
    )


def part2_on_the_upper_face_the_eta_pressure_collapses_to_the_repair_cap_profile(
    q_pref: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: ON THE UPPER-m FACE THE ETA PRESSURE COLLAPSES TO THE CAP PROFILE")
    print("=" * 88)

    cap_deltas = []
    cap_etas = []
    cap_dists = []
    eta_at_cap_ok = True

    for slack in CAP_SLACK_GRID:
        d_cap = cap_delta(float(slack))
        d_grid = np.linspace(0.95, d_cap, CAP_DELTA_GRID_COUNT)
        eta_vals = []
        for delta in d_grid:
            _repair, eta_best, _winner, _column = point_data((UPPER_M, float(delta), float(slack)))
            eta_vals.append(eta_best)
        cap_deltas.append(d_cap)
        cap_etas.append(float(max(eta_vals)))
        repair_cap, eta_cap, _winner_cap, column_cap = point_data((UPPER_M, d_cap, float(slack)))
        cap_dists.append(float(np.linalg.norm(column_cap - q_pref)))
        eta_at_cap_ok &= abs(d_grid[int(np.argmax(eta_vals))] - d_cap) < 1.0e-9
        eta_at_cap_ok &= abs(repair_cap - EXPECTED_PREF_REPAIR) < 1.0e-11

    cap_deltas = np.asarray(cap_deltas, dtype=float)
    cap_etas = np.asarray(cap_etas, dtype=float)
    cap_dists = np.asarray(cap_dists, dtype=float)
    peak_idx = int(np.argmax(cap_etas))

    check(
        "On every sampled upper-face slack slice the lower-repair best eta is attained at the repair-cap boundary",
        eta_at_cap_ok,
        f"peak_idx={peak_idx}, peak_s={CAP_SLACK_GRID[peak_idx]:.12f}",
    )
    check(
        "The sampled upper-face repair-cap delta profile is reproduced stably and decreases with slack",
        abs(cap_deltas[0] - EXPECTED_CAP_DELTA_START) < 1.0e-12
        and abs(cap_deltas[-1] - EXPECTED_CAP_DELTA_END) < 1.0e-12
        and all(b < a for a, b in zip(cap_deltas, cap_deltas[1:])),
        f"(delta_start,delta_end)=({cap_deltas[0]:.12f},{cap_deltas[-1]:.12f})",
    )
    check(
        "The sampled upper-face cap-eta profile is unimodal with one small-slack peak",
        peak_idx == 2
        and abs(CAP_SLACK_GRID[peak_idx] - EXPECTED_CAP_ETA_PEAK_SLACK) < 1.0e-12
        and abs(cap_deltas[peak_idx] - EXPECTED_CAP_ETA_PEAK_DELTA) < 1.0e-12
        and abs(cap_etas[peak_idx] - EXPECTED_CAP_ETA_PEAK) < 1.0e-12
        and all(cap_etas[i + 1] >= cap_etas[i] - 1.0e-12 for i in range(peak_idx))
        and all(cap_etas[i + 1] <= cap_etas[i] + 1.0e-12 for i in range(peak_idx, len(cap_etas) - 1)),
        f"(s_peak,delta_peak,eta_peak)=({CAP_SLACK_GRID[peak_idx]:.12f},{cap_deltas[peak_idx]:.12f},{cap_etas[peak_idx]:.12f})",
    )
    check(
        "That sampled best-eta upper-face extremal remains visibly transport-incompatible with closure",
        cap_etas[peak_idx] < 0.885 and cap_etas[peak_idx] < 1.0,
        f"eta_peak={cap_etas[peak_idx]:.12f}",
    )


def part3_the_closest_sampled_lane_on_the_upper_face_is_the_slack_floor_endpoint(
    q_pref: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CLOSEST SAMPLED UPPER-FACE LANE IS THE SLACK-FLOOR ENDPOINT")
    print("=" * 88)

    best_dist = float("inf")
    best_slack = None
    best_delta = None
    best_eta = None
    for slack in CAP_SLACK_GRID:
        d_cap = cap_delta(float(slack))
        d_grid = np.linspace(0.95, d_cap, CAP_DELTA_GRID_COUNT)
        for delta in d_grid:
            repair, eta_best, _winner, column = point_data((UPPER_M, float(delta), float(slack)))
            if repair <= EXPECTED_PREF_REPAIR + 1.0e-9:
                dist = float(np.linalg.norm(column - q_pref))
                if dist < best_dist:
                    best_dist = dist
                    best_slack = float(slack)
                    best_delta = float(delta)
                    best_eta = float(eta_best)

    check(
        "On the sampled upper-face feasible region the closest lane occurs at the slack-floor endpoint",
        abs(best_slack - EXPECTED_CAP_CLOSEST_SLACK) < 1.0e-15
        and abs(best_delta - EXPECTED_CAP_CLOSEST_DELTA) < 1.0e-12
        and abs(best_dist - EXPECTED_CAP_CLOSEST_DIST) < 1.0e-12
        and abs(best_eta - EXPECTED_CAP_CLOSEST_ETA) < 1.0e-12,
        f"(s,delta,dist,eta)=({best_slack:.12f},{best_delta:.12f},{best_dist:.12f},{best_eta:.12f})",
    )
    check(
        "That closest sampled upper-face lane still stays far from the preferred transport quotient",
        best_dist > 0.23 and best_eta < 0.89,
        f"(dist,eta)=({best_dist:.12f},{best_eta:.12f})",
    )


def part4_the_note_records_the_two_extremal_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE TWO-EXTREMAL REDUCTION")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_LOWER_REPAIR_UPPER_FACE_EXTREMALS_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the monotone drift of lower-repair transport pressure to the upper-m face",
        "drift monotonically toward the upper-`m` face" in note and "0.884471224505" in note and "0.233486690453" in note,
    )
    check(
        "The note records the sampled cap-eta extremal point",
        "0.0195041737783" in note and "1.188513342509166" in note and "0.884523189582" in note,
    )
    check(
        "The note records the closest-lane slack-floor endpoint and keeps the theorem boundary honest",
        "1.188955544069478" in note and "0.233274467128" in note and "interval-certified exact-carrier closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 LOWER-REPAIR UPPER-FACE EXTREMALS CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the tested split-2 low-slack lower-repair box, does the residual")
    print("  transport pressure already collapse to explicit upper-face extremals?")

    q_pref = preferred_column()
    part1_sampled_lower_repair_transport_pressure_drifts_monotonically_to_the_upper_face(q_pref)
    part2_on_the_upper_face_the_eta_pressure_collapses_to_the_repair_cap_profile(q_pref)
    part3_the_closest_sampled_lane_on_the_upper_face_is_the_slack_floor_endpoint(q_pref)
    part4_the_note_records_the_two_extremal_reduction()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Tested positive-path carrier reduction:")
    print("    - lower-repair split-2 transport pressure drifts monotonically to the upper-m face")
    print("    - on that sampled upper face, best eta collapses to one cap-profile peak")
    print("    - the closest sampled lane collapses to the slack-floor endpoint")
    print("  RESULT: the tested broad split-2 pressure is reduced to two explicit")
    print("  upper-face extremals, both still transport-incompatible")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
