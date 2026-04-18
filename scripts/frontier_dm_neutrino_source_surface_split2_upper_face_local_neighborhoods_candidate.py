#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 upper-face local neighborhoods candidate.

Question:
  After the broad split-2 lower-repair pressure is compressed to the two
  explicit upper-face extremals, does any tested local 3D neighborhood around
  those extremals already look transport-compatible?

Answer:
  No on the tested local boxes.

  In a tested local 3D box around the best-eta cap point, the lower-repair
  eta maximum remains exactly at that cap point, but the whole box stays below
  transport closure and the closest lower-repair packet lane in that box still
  stays well away from the preferred quotient.

  In a tested local 3D box around the slack-floor closest-lane endpoint, the
  lower-repair closest-lane point remains exactly that endpoint, but the whole
  box still stays well below transport closure.

Boundary:
  This is a local tested-neighborhood exhaustion candidate, not interval-
  certified exact-carrier closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_dm_neutrino_source_surface_split2_low_slack_transport_incompatibility_candidate import (
    EXPECTED_PREF_REPAIR,
    point_data,
)
from frontier_dm_neutrino_source_surface_split2_lower_repair_upper_face_extremals_candidate import (
    EXPECTED_CAP_CLOSEST_DELTA,
    EXPECTED_CAP_CLOSEST_DIST,
    EXPECTED_CAP_CLOSEST_ETA,
    EXPECTED_CAP_CLOSEST_SLACK,
    EXPECTED_CAP_ETA_PEAK,
    EXPECTED_CAP_ETA_PEAK_DELTA,
    EXPECTED_CAP_ETA_PEAK_SLACK,
    UPPER_M,
    preferred_column,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

CAP_BOX = {
    "m": (-0.145, -0.14),
    "delta": (1.1835, 1.1935),
    "slack": (0.0145, 0.0245),
}
ENDPOINT_BOX = {
    "m": (-0.145, -0.14),
    "delta": (1.1839, 1.1890),
    "slack": (0.0, 0.005),
}

EXPECTED_CAP_BOX_COUNT = 3352
EXPECTED_CAP_BOX_BEST_ETA = EXPECTED_CAP_ETA_PEAK
EXPECTED_CAP_BOX_MIN_DIST = 0.24228352737364428
EXPECTED_CAP_BOX_MIN_DIST_POINT = np.array(
    [-0.14, EXPECTED_CAP_ETA_PEAK_DELTA, 0.0145],
    dtype=float,
)

EXPECTED_ENDPOINT_BOX_COUNT = 6430
EXPECTED_ENDPOINT_BOX_BEST_ETA = 0.8839775785479420
EXPECTED_ENDPOINT_BOX_BEST_ETA_POINT = np.array(
    [-0.14, 1.18883, 0.005],
    dtype=float,
)
EXPECTED_ENDPOINT_BOX_MIN_DIST = EXPECTED_CAP_CLOSEST_DIST


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


def anchored_grid(lo: float, hi: float, count: int, special: float) -> np.ndarray:
    vals = np.linspace(float(lo), float(hi), int(count))
    vals = np.unique(np.sort(np.concatenate([vals, np.array([float(special)], dtype=float)])))
    return vals


def local_box_scan(
    m_bounds: tuple[float, float],
    delta_bounds: tuple[float, float],
    slack_bounds: tuple[float, float],
    m_special: float,
    delta_special: float,
    slack_special: float,
    preferred_column_vec: np.ndarray,
) -> dict[str, object]:
    ms = anchored_grid(m_bounds[0], m_bounds[1], 11, m_special)
    deltas = anchored_grid(delta_bounds[0], delta_bounds[1], 31, delta_special)
    slacks = anchored_grid(slack_bounds[0], slack_bounds[1], 31, slack_special)

    feasible = 0
    best_eta = (-1.0, None)
    min_dist = (float("inf"), None)
    has_transport_closure = False

    for m in ms:
        for delta in deltas:
            for slack in slacks:
                repair, eta_best, _winner, column = point_data((float(m), float(delta), float(slack)))
                if repair <= EXPECTED_PREF_REPAIR + 1.0e-9:
                    feasible += 1
                    if eta_best >= 1.0:
                        has_transport_closure = True
                    if eta_best > best_eta[0]:
                        best_eta = (eta_best, np.array([m, delta, slack, repair], dtype=float))
                    dist = float(np.linalg.norm(column - preferred_column_vec))
                    if dist < min_dist[0]:
                        min_dist = (dist, np.array([m, delta, slack, repair, eta_best], dtype=float))

    return {
        "feasible": feasible,
        "best_eta_value": float(best_eta[0]),
        "best_eta_point": np.asarray(best_eta[1], dtype=float),
        "min_dist_value": float(min_dist[0]),
        "min_dist_point": np.asarray(min_dist[1], dtype=float),
        "has_transport_closure": bool(has_transport_closure),
    }


def part1_the_cap_neighborhood_keeps_the_same_eta_peak_and_stays_transport_incompatible(
    q_pref: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CAP NEIGHBORHOOD KEEPS THE SAME ETA PEAK")
    print("=" * 88)

    stats = local_box_scan(
        CAP_BOX["m"],
        CAP_BOX["delta"],
        CAP_BOX["slack"],
        UPPER_M,
        EXPECTED_CAP_ETA_PEAK_DELTA,
        EXPECTED_CAP_ETA_PEAK_SLACK,
        q_pref,
    )

    best_eta_point = stats["best_eta_point"]
    min_dist_point = stats["min_dist_point"]

    check(
        "The tested cap neighborhood feasible lower-repair count is stable",
        int(stats["feasible"]) == EXPECTED_CAP_BOX_COUNT,
        f"count={stats['feasible']}",
    )
    check(
        "The tested cap neighborhood keeps the same local lower-repair eta maximizer",
        abs(float(stats["best_eta_value"]) - EXPECTED_CAP_BOX_BEST_ETA) < 1.0e-12
        and np.linalg.norm(best_eta_point[:3] - np.array([UPPER_M, EXPECTED_CAP_ETA_PEAK_DELTA, EXPECTED_CAP_ETA_PEAK_SLACK], dtype=float)) < 1.0e-12
        and abs(float(best_eta_point[3]) - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"(m,delta,s,eta)=({best_eta_point[0]:.12f},{best_eta_point[1]:.12f},{best_eta_point[2]:.12f},{float(stats['best_eta_value']):.12f})",
    )
    check(
        "Even on that tested cap neighborhood, no lower-repair point reaches transport closure",
        not bool(stats["has_transport_closure"]) and float(stats["best_eta_value"]) < 1.0,
        f"best eta={float(stats['best_eta_value']):.12f}",
    )
    check(
        "Even on that tested cap neighborhood, the closest lower-repair packet lane still stays far from the preferred quotient",
        abs(float(stats["min_dist_value"]) - EXPECTED_CAP_BOX_MIN_DIST) < 1.0e-12
        and np.linalg.norm(min_dist_point[:3] - EXPECTED_CAP_BOX_MIN_DIST_POINT) < 1.0e-12
        and float(stats["min_dist_value"]) > 0.24,
        f"(m,delta,s,dist)=({min_dist_point[0]:.12f},{min_dist_point[1]:.12f},{min_dist_point[2]:.12f},{float(stats['min_dist_value']):.12f})",
    )


def part2_the_endpoint_neighborhood_keeps_the_same_closest_lane_and_stays_transport_incompatible(
    q_pref: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ENDPOINT NEIGHBORHOOD KEEPS THE SAME CLOSEST LANE")
    print("=" * 88)

    stats = local_box_scan(
        ENDPOINT_BOX["m"],
        ENDPOINT_BOX["delta"],
        ENDPOINT_BOX["slack"],
        UPPER_M,
        EXPECTED_CAP_CLOSEST_DELTA,
        EXPECTED_CAP_CLOSEST_SLACK,
        q_pref,
    )

    best_eta_point = stats["best_eta_point"]
    min_dist_point = stats["min_dist_point"]

    check(
        "The tested endpoint neighborhood feasible lower-repair count is stable",
        int(stats["feasible"]) == EXPECTED_ENDPOINT_BOX_COUNT,
        f"count={stats['feasible']}",
    )
    check(
        "The tested endpoint neighborhood keeps the same local lower-repair closest-lane point",
        abs(float(stats["min_dist_value"]) - EXPECTED_ENDPOINT_BOX_MIN_DIST) < 1.0e-12
        and np.linalg.norm(min_dist_point[:3] - np.array([UPPER_M, EXPECTED_CAP_CLOSEST_DELTA, EXPECTED_CAP_CLOSEST_SLACK], dtype=float)) < 1.0e-12
        and abs(float(min_dist_point[3]) - EXPECTED_PREF_REPAIR) < 1.0e-12
        and abs(float(min_dist_point[4]) - EXPECTED_CAP_CLOSEST_ETA) < 1.0e-12,
        f"(m,delta,s,dist)=({min_dist_point[0]:.12f},{min_dist_point[1]:.12f},{min_dist_point[2]:.12f},{float(stats['min_dist_value']):.12f})",
    )
    check(
        "Even on that tested endpoint neighborhood, the best lower-repair transport value stays well below closure",
        abs(float(stats["best_eta_value"]) - EXPECTED_ENDPOINT_BOX_BEST_ETA) < 1.0e-12
        and np.linalg.norm(best_eta_point[:3] - EXPECTED_ENDPOINT_BOX_BEST_ETA_POINT) < 1.0e-12
        and float(stats["best_eta_value"]) < 0.89,
        f"(m,delta,s,eta)=({best_eta_point[0]:.12f},{best_eta_point[1]:.12f},{best_eta_point[2]:.12f},{float(stats['best_eta_value']):.12f})",
    )
    check(
        "So even that closest-lane neighborhood still has no lower-repair transport-compatible rival",
        not bool(stats["has_transport_closure"]),
        f"closest dist={float(stats['min_dist_value']):.12f}",
    )


def part3_the_note_records_the_local_upper_face_exhaustion() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NOTE RECORDS THE LOCAL UPPER-FACE EXHAUSTION")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_UPPER_FACE_LOCAL_NEIGHBORHOODS_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the cap neighborhood and its pinned eta peak",
        "1.188513342509166" in note and "0.0195041737783" in note and "0.884523189582" in note,
    )
    check(
        "The note records the endpoint neighborhood and its pinned closest-lane point",
        "1.188955544069478" in note and "0.233274467128" in note and "0.883631424817" in note,
    )
    check(
        "The note records that the carrier-side pressure is exhausted to those two local neighborhoods rather than a diffuse split-2 region",
        "exhausted to the two explicit local upper-face neighborhoods" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 UPPER-FACE LOCAL NEIGHBORHOODS")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the split-2 broad lower-repair pressure is compressed to the")
    print("  two explicit upper-face extremals, do tested local 3D neighborhoods")
    print("  around those extremals already look transport-compatible?")

    q_pref = preferred_column()
    part1_the_cap_neighborhood_keeps_the_same_eta_peak_and_stays_transport_incompatible(q_pref)
    part2_the_endpoint_neighborhood_keeps_the_same_closest_lane_and_stays_transport_incompatible(q_pref)
    part3_the_note_records_the_local_upper_face_exhaustion()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Result:")
    print("    - the cap neighborhood keeps the same local eta peak")
    print("    - the endpoint neighborhood keeps the same local closest-lane point")
    print("    - both tested neighborhoods remain transport-incompatible")
    print("  RESULT: split-2 carrier pressure is exhausted to two explicit local")
    print("  upper-face neighborhoods on the current branch")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
