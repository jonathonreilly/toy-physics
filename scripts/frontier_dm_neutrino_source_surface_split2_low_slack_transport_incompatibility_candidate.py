#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 low-slack transport incompatibility candidate.

Question:
  On the tested broad split-2 low-slack box, can any point with repair at or
  below the preferred recovered floor realize a transport-compatible rival lane?

Answer:
  Numerically, no on the tested box

      m     in [-0.19, -0.14],
      delta in [-2.5, 2.5],
      s     in [0, s_*^edge],

  where `s_*^edge ~= 0.195041737783` is the broad split-2 edge threshold.

  Under the lower-repair constraint

      Lambda_+(m,delta,s) <= Lambda_+(x_*),

  the strongest tested transport rival found still satisfies

      max eta_best/eta_obs ~= 0.884523453538 < 1,

  and the closest tested winning transport column to the preferred quotient
  lane still has

      min ||sort(P_best) - Q_pref||_2 ~= 0.233468501596.

  So on the tested broad split-2 low-slack box, lower repair does not
  numerically produce a transport-compatible rival lane.

Boundary:
  This is a numerical incompatibility candidate on the tested broad box, not an
  interval-certified exclusion theorem on the exact carrier.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

from dm_leptogenesis_exact_common import (
    C_SPH,
    D_THERMAL_EXACT,
    ETA_OBS,
    S_OVER_NGAMMA_EXACT,
    exact_package,
)
from dm_selector_branch_support import PREFERRED_RECOVERED_LIFT, repair_from_slack_point
from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_active_projector_reduction import active_packet_from_h
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
    active_affine_h,
)
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import q_floor
from frontier_dm_neutrino_source_surface_split2_edge_profile_transition_candidate import (
    EXPECTED_ROOT,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)

LOW_SLACK_BOUNDS = [(-0.19, -0.14), (-2.5, 2.5), (0.0, EXPECTED_ROOT)]
ETA_SEEDS = [0, 1, 2, 3, 4, 5]
DIST_SEEDS = [0, 1, 2, 3, 4, 5]

EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_PREF_ETA = 1.052220313051713
EXPECTED_PREF_COLUMN = np.array(
    [0.03564425147218436, 0.035644362528105066, 0.9287113859997107],
    dtype=float,
)

EXPECTED_COARSE_BEST_ETA = 0.8792215323677851
EXPECTED_COARSE_BEST_POINT = np.array(
    [-0.14, 1.15, 0.004876043444566249],
    dtype=float,
)
EXPECTED_COARSE_BEST_REPAIR = 1.5586221951978787
EXPECTED_COARSE_CLOSEST_DIST = 0.2505606855503093

EXPECTED_SEED_MAX_ETA = 0.8845234535378179
EXPECTED_SEED_MAX_ETA_POINT = np.array(
    [-0.1400007, 1.18838072, 0.02114129],
    dtype=float,
)
EXPECTED_SEED_MAX_ETA_REPAIR = 1.5868377123863682
EXPECTED_SEED_MAX_ETA_COLUMN = np.array(
    [0.04077956, 0.20726092, 0.75195952],
    dtype=float,
)

EXPECTED_SEED_MIN_DIST = 0.2334685015963999
EXPECTED_SEED_MIN_DIST_POINT = np.array(
    [-0.140104496, 1.18883523, 0.0000695635837],
    dtype=float,
)
EXPECTED_SEED_MIN_DIST_REPAIR = 1.5868427517391115
EXPECTED_SEED_MIN_DIST_ETA = 0.8836039740974554
EXPECTED_SEED_MIN_DIST_COLUMN = np.array(
    [0.04460033, 0.19607118, 0.75932849],
    dtype=float,
)


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


def eta_ratio_from_transport_factor(transport_factor: float) -> float:
    return (
        S_OVER_NGAMMA_EXACT
        * C_SPH
        * D_THERMAL_EXACT
        * PKG.epsilon_1
        * transport_factor
        / ETA_OBS
    )


def point_data(x: np.ndarray | tuple[float, float, float]) -> tuple[float, float, int, np.ndarray]:
    m, delta, slack = [float(v) for v in x]
    q_plus = q_floor(delta) + slack
    h = active_affine_h(m, delta, q_plus)
    repair = max(0.0, -float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))))
    packet = active_packet_from_h(h).T
    values = np.array(
        [flavored_column_functional(packet[:, idx], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL) for idx in range(3)],
        dtype=float,
    )
    etas = np.array([eta_ratio_from_transport_factor(value) for value in values], dtype=float)
    winner = int(np.argmax(etas))
    column = np.sort(packet[:, winner])
    return repair, float(np.max(etas)), winner, column


def repair_penalty(repair: float) -> float:
    t = max(float(repair) - EXPECTED_PREF_REPAIR, 0.0)
    return 2000.0 * t + 2000.0 * t * t


def eta_objective(x: np.ndarray, _preferred_column: np.ndarray) -> float:
    repair, eta_best, _winner, _column = point_data(x)
    return -eta_best + repair_penalty(repair)


def dist_objective(x: np.ndarray, preferred_column: np.ndarray) -> float:
    repair, _eta_best, _winner, column = point_data(x)
    return float(np.linalg.norm(column - preferred_column)) + repair_penalty(repair)


def part1_the_preferred_recovered_lane_is_unchanged() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE PREFERRED RECOVERED LANE IS UNCHANGED")
    print("=" * 88)

    repair_pref, eta_pref, winner_pref, column_pref = point_data(PREFERRED_RECOVERED_LIFT)

    check(
        "The preferred recovered repair is unchanged on this branch",
        abs(repair_pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"Lambda_+*={repair_pref:.12f}",
    )
    check(
        "The preferred recovered winning transport value is unchanged on this branch",
        abs(eta_pref - EXPECTED_PREF_ETA) < 1.0e-12 and winner_pref == 2,
        f"(winner,eta)=({winner_pref},{eta_pref:.12f})",
    )
    check(
        "The preferred recovered winning packet quotient is unchanged on this branch",
        np.max(np.abs(column_pref - EXPECTED_PREF_COLUMN)) < 1.0e-12,
        f"Q_pref={np.round(column_pref, 12)}",
    )

    return column_pref


def part2_a_coarse_box_scan_already_shows_no_subcritical_transport_closure(
    preferred_column: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: A COARSE BOX SCAN ALREADY SHOWS NO SUBCRITICAL TRANSPORT CLOSURE")
    print("=" * 88)

    ms = np.linspace(-0.19, -0.14, 6)
    deltas = np.linspace(0.9, 1.15, 26)
    slacks = np.linspace(0.0, EXPECTED_ROOT, 41)

    best_eta = (-1.0, None)
    closest = (float("inf"), None)
    has_eta_ge_one = False
    for m in ms:
        for delta in deltas:
            for slack in slacks:
                repair, eta_best, winner, column = point_data((m, delta, slack))
                if repair <= EXPECTED_PREF_REPAIR + 1.0e-9:
                    if eta_best >= 1.0:
                        has_eta_ge_one = True
                    if eta_best > best_eta[0]:
                        best_eta = (eta_best, (m, delta, slack, repair, winner, column))
                    dist = float(np.linalg.norm(column - preferred_column))
                    if dist < closest[0]:
                        closest = (dist, (m, delta, slack, repair, eta_best, winner, column))

    check(
        "On the coarse tested split-2 low-slack box, no lower-repair sample already reaches eta/eta_obs >= 1",
        not has_eta_ge_one,
        f"best coarse eta={best_eta[0]:.12f}",
    )
    check(
        "The best coarse lower-repair transport sample is reproduced stably",
        abs(best_eta[0] - EXPECTED_COARSE_BEST_ETA) < 1.0e-12
        and np.linalg.norm(np.array(best_eta[1][:3], dtype=float) - EXPECTED_COARSE_BEST_POINT) < 1.0e-12
        and abs(float(best_eta[1][3]) - EXPECTED_COARSE_BEST_REPAIR) < 1.0e-12,
        f"(m,delta,s,eta)=({best_eta[1][0]:.12f},{best_eta[1][1]:.12f},{best_eta[1][2]:.12f},{best_eta[0]:.12f})",
    )
    check(
        "The closest coarse lower-repair packet lane is still visibly separated from the preferred quotient",
        closest[0] > 0.25 - 1.0e-12 and abs(closest[0] - EXPECTED_COARSE_CLOSEST_DIST) < 1.0e-12,
        f"(dist,point)=({closest[0]:.12f},{closest[1][0]:.12f},{closest[1][1]:.12f},{closest[1][2]:.12f})",
    )


def part3_seeded_global_search_keeps_the_same_broad_box_verdict(
    preferred_column: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: SEEDED GLOBAL SEARCH KEEPS THE SAME BROAD-BOX VERDICT")
    print("=" * 88)

    eta_runs: list[tuple[np.ndarray, float, float, int, np.ndarray]] = []
    for seed in ETA_SEEDS:
        result = differential_evolution(
            lambda x: eta_objective(x, preferred_column),
            LOW_SLACK_BOUNDS,
            seed=seed,
            maxiter=40,
            popsize=12,
            polish=True,
            tol=1.0e-6,
            updating="deferred",
            workers=1,
        )
        repair, eta_best, winner, column = point_data(result.x)
        eta_runs.append((np.asarray(result.x, dtype=float), repair, eta_best, winner, column))

    dist_runs: list[tuple[np.ndarray, float, float, int, np.ndarray, float]] = []
    for seed in DIST_SEEDS:
        result = differential_evolution(
            lambda x: dist_objective(x, preferred_column),
            LOW_SLACK_BOUNDS,
            seed=seed,
            maxiter=40,
            popsize=12,
            polish=True,
            tol=1.0e-6,
            updating="deferred",
            workers=1,
        )
        repair, eta_best, winner, column = point_data(result.x)
        dist = float(np.linalg.norm(column - preferred_column))
        dist_runs.append((np.asarray(result.x, dtype=float), repair, eta_best, winner, column, dist))

    best_eta_run = max(eta_runs, key=lambda row: row[2])
    best_dist_run = min(dist_runs, key=lambda row: row[5])

    check(
        "Across seeded global searches, the best lower-repair transport value stays strictly below 0.885 and never reaches 1",
        all(row[2] < 0.885 for row in eta_runs) and all(row[2] < 1.0 for row in eta_runs),
        f"etas={[round(row[2], 12) for row in eta_runs]}",
    )
    check(
        "The strongest seeded lower-repair transport rival is reproduced stably",
        0.88451 < best_eta_run[2] < 0.88454
        and -0.14005 < best_eta_run[0][0] < -0.13999
        and 1.18830 < best_eta_run[0][1] < 1.18860
        and 0.0195 < best_eta_run[0][2] < 0.0215
        and abs(best_eta_run[1] - EXPECTED_PREF_REPAIR) < 6.0e-5
        and np.max(np.abs(best_eta_run[4] - EXPECTED_SEED_MAX_ETA_COLUMN)) < 5.0e-4,
        f"(x,eta,col)=({np.round(best_eta_run[0], 9)},{best_eta_run[2]:.12f},{np.round(best_eta_run[4], 9)})",
    )
    check(
        "Across seeded global searches, the closest lower-repair packet lane stays separated from the preferred quotient",
        all(row[5] > 0.233 for row in dist_runs),
        f"dists={[round(row[5], 12) for row in dist_runs]}",
    )
    check(
        "The closest seeded lower-repair packet lane is reproduced stably",
        abs(best_dist_run[5] - EXPECTED_SEED_MIN_DIST) < 5.0e-6
        and np.linalg.norm(best_dist_run[0] - EXPECTED_SEED_MIN_DIST_POINT) < 5.0e-4
        and abs(best_dist_run[1] - EXPECTED_SEED_MIN_DIST_REPAIR) < 5.0e-5
        and abs(best_dist_run[2] - EXPECTED_SEED_MIN_DIST_ETA) < 5.0e-6
        and np.max(np.abs(best_dist_run[4] - EXPECTED_SEED_MIN_DIST_COLUMN)) < 5.0e-5,
        f"(x,dist,eta,col)=({np.round(best_dist_run[0], 9)},{best_dist_run[5]:.12f},{best_dist_run[2]:.12f},{np.round(best_dist_run[4], 9)})",
    )


def part4_the_note_records_the_broad_box_incompatibility_honestly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE BROAD-BOX INCOMPATIBILITY HONESTLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_LOW_SLACK_TRANSPORT_INCOMPATIBILITY_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the tested broad split-2 low-slack box and the lower-repair constraint",
        "[-0.19,-0.14]" in note and "[-2.5,2.5]" in note and "Lambda_+(x_*)" in note,
    )
    check(
        "The note records the strongest tested lower-repair transport value and closest lane distance",
        "0.884523453538" in note and "0.233468501596" in note,
    )
    check(
        "The note keeps the boundary honest: this is still not interval-certified exact-carrier closure",
        "not an interval-certified exclusion theorem" in note and "not flagship closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 LOW-SLACK TRANSPORT INCOMPATIBILITY CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the tested broad split-2 low-slack box, can any lower-repair point")
    print("  realize a transport-compatible rival lane?")

    preferred_column = part1_the_preferred_recovered_lane_is_unchanged()
    part2_a_coarse_box_scan_already_shows_no_subcritical_transport_closure(preferred_column)
    part3_seeded_global_search_keeps_the_same_broad_box_verdict(preferred_column)
    part4_the_note_records_the_broad_box_incompatibility_honestly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Strongest tested broad split-2 low-slack statement so far:")
    print("    - on the tested box, no lower-repair sample reaches eta/eta_obs >= 1")
    print("    - seeded global searches keep the best lower-repair transport rival")
    print("      below 0.884523453538")
    print("    - seeded global searches keep the closest lower-repair packet lane at")
    print("      distance at least 0.233468501596 from the preferred quotient")
    print("  RESULT: the tested broad split-2 low-slack box is transport-incompatible")
    print("  with the preferred recovered lane under the lower-repair constraint")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
