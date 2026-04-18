#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 edge transport-lane obstruction candidate.

Question:
  Does the tested broad-bundle split-2 dangerous edge already lie on the same
  transport-selected packet lane as the preferred recovered point?

Answer:
  No, on the tested dangerous edge interval.

  Let the preferred recovered point be

      x_* = (m_*, delta_*, s_*)
          = (1.021038842009, 1.380791428982, 0.215677476525)

  with active coordinate q_+* = 0.467879209399 and winning transport column

      Q_pref = sort(P_best(x_*))
             = (0.035644251472, 0.035644362528, 0.928711385999),

  carrying

      eta_best(x_*) / eta_obs = 1.052220313052.

  On the tested split-2 dangerous edge

      m = -0.14,
      0 <= s <= s_*^edge ~= 0.195041737783,
      delta = delta_edge(s) minimizing Lambda_+ on that edge,

  the best transport column never approaches that preferred small-leakage lane:

      max eta_best / eta_obs <= 0.847299300834,
      min ||sort(P_best) - Q_pref||_2 >= 0.293939334980,
      min |p_2 - p_1|           >= 0.057100889715,
      max p_3                   <= 0.691413921653.

  So the broad split-2 low-slack undercut does not by itself realize the
  preferred transport-selected quotient. The remaining carrier-side issue is
  narrower: whether the exact transport carrier can enter a lower-repair,
  transport-compatible lane inside that low-slack interval.

Boundary:
  This is still a tested-edge obstruction candidate, not interval-certified
  exact-carrier closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

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
    SPLIT2_EDGE_M,
    edge_profile,
)

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)

EXPECTED_PREF_Q = 0.467879209398938
EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_PREF_ETA = 1.052220313051713
EXPECTED_PREF_WINNER = 2
EXPECTED_PREF_COLUMN = np.array(
    [0.03564425147218436, 0.035644362528105066, 0.9287113859997107],
    dtype=float,
)

EXPECTED_EDGE_SAMPLES = {
    0.0: {
        "delta": 0.9970498933945160,
        "q_plus": 0.6359432684609361,
        "repair": 1.5004424916582053,
        "eta": 0.8472993008336142,
        "winner": 2,
        "column": np.array([0.02638337302875077, 0.4296679157412071, 0.5439487112300421], dtype=float),
    },
    0.1: {
        "delta": 1.0328954845907592,
        "q_plus": 0.7000976772646929,
        "repair": 1.5411842223412606,
        "eta": 0.7949431967197641,
        "winner": 2,
        "column": np.array([0.017335713125881176, 0.43987296830296285, 0.5427913185711563], dtype=float),
    },
    EXPECTED_ROOT: {
        "delta": 1.0642229611259355,
        "q_plus": 0.7638119385121666,
        "repair": 1.5868747147296784,
        "eta": 0.7714607550678538,
        "winner": 1,
        "column": np.array([0.12281349396718477, 0.18577258437947614, 0.691413921653339], dtype=float),
    },
}

EXPECTED_MAX_EDGE_ETA = 0.8472993008336142
EXPECTED_ETA_GAP = 0.20492101221809877
EXPECTED_MIN_COLUMN_DIST = 0.29393933497993874
EXPECTED_MIN_LEAKAGE_ASYM = 0.05710088971483221
EXPECTED_MAX_LARGEST_ENTRY = 0.691413921653339


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


def transport_packet_data(m: float, delta: float, q_plus: float) -> tuple[np.ndarray, np.ndarray, int, np.ndarray]:
    packet = active_packet_from_h(active_affine_h(m, delta, q_plus)).T
    values = np.array(
        [flavored_column_functional(packet[:, idx], Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL) for idx in range(3)],
        dtype=float,
    )
    etas = np.array([eta_ratio_from_transport_factor(value) for value in values], dtype=float)
    winner = int(np.argmax(etas))
    column = np.sort(packet[:, winner])
    return packet, etas, winner, column


def part1_the_preferred_recovered_point_carries_one_sharp_transport_lane() -> tuple[float, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE PREFERRED RECOVERED POINT CARRIES ONE SHARP TRANSPORT LANE")
    print("=" * 88)

    m_pref, d_pref, s_pref = [float(x) for x in PREFERRED_RECOVERED_LIFT]
    q_pref = q_floor(d_pref) + s_pref
    _packet_pref, etas_pref, winner_pref, column_pref = transport_packet_data(m_pref, d_pref, q_pref)
    repair_pref = float(repair_from_slack_point(PREFERRED_RECOVERED_LIFT))
    eta_pref = float(np.max(etas_pref))

    check(
        "The preferred recovered active coordinate q_+ is unchanged on this branch",
        abs(q_pref - EXPECTED_PREF_Q) < 1.0e-12,
        f"q_+*={q_pref:.12f}",
    )
    check(
        "The preferred recovered repair is unchanged on this branch",
        abs(repair_pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"Lambda_+*={repair_pref:.12f}",
    )
    check(
        "The preferred recovered point still carries the same winning eta/eta_obs and winning column",
        abs(eta_pref - EXPECTED_PREF_ETA) < 1.0e-12
        and winner_pref == EXPECTED_PREF_WINNER
        and np.max(np.abs(column_pref - EXPECTED_PREF_COLUMN)) < 1.0e-12,
        f"(winner,eta,col)=({winner_pref},{eta_pref:.12f},{np.round(column_pref, 12)})",
    )

    return eta_pref, column_pref


def part2_the_split2_edge_transport_data_are_reproduced_stably() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SPLIT-2 EDGE TRANSPORT DATA ARE REPRODUCED STABLY")
    print("=" * 88)

    for slack, expected in EXPECTED_EDGE_SAMPLES.items():
        delta, repair = edge_profile(slack)
        q_plus = q_floor(delta) + slack
        _packet, etas, winner, column = transport_packet_data(SPLIT2_EDGE_M, delta, q_plus)
        eta_best = float(np.max(etas))

        check(
            f"The split-2 edge sample at s={slack:.12f} reproduces its minimizing point stably",
            abs(delta - expected["delta"]) < 1.0e-10
            and abs(q_plus - expected["q_plus"]) < 1.0e-10
            and abs(repair - expected["repair"]) < 1.0e-10,
            f"(delta,q_+,Lambda_+)=({delta:.12f},{q_plus:.12f},{repair:.12f})",
        )
        check(
            f"The split-2 edge sample at s={slack:.12f} reproduces its winning transport lane stably",
            winner == expected["winner"]
            and abs(eta_best - expected["eta"]) < 1.0e-12
            and np.max(np.abs(column - expected["column"])) < 1.0e-12,
            f"(winner,eta,col)=({winner},{eta_best:.12f},{np.round(column, 12)})",
        )


def part3_the_tested_dangerous_edge_stays_off_the_preferred_transport_lane(
    eta_pref: float, column_pref: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE TESTED DANGEROUS EDGE STAYS OFF THE PREFERRED TRANSPORT LANE")
    print("=" * 88)

    rows: list[tuple[float, float, int, float, float, float]] = []
    for slack in np.linspace(0.0, EXPECTED_ROOT, 161):
        delta, _repair = edge_profile(float(slack))
        q_plus = q_floor(delta) + float(slack)
        _packet, etas, winner, column = transport_packet_data(SPLIT2_EDGE_M, delta, q_plus)
        eta_best = float(np.max(etas))
        rows.append(
            (
                float(slack),
                eta_best,
                winner,
                float(np.linalg.norm(column - column_pref)),
                float(abs(column[1] - column[0])),
                float(column[2]),
            )
        )

    max_eta_row = max(rows, key=lambda row: row[1])
    min_dist_row = min(rows, key=lambda row: row[3])
    min_asym_row = min(rows, key=lambda row: row[4])
    max_large_row = max(rows, key=lambda row: row[5])
    eta_gap = eta_pref - max_eta_row[1]

    check(
        "Across the tested dangerous split-2 edge, the best eta/eta_obs stays far below the preferred recovered value",
        max_eta_row[1] < eta_pref - 0.2
        and abs(max_eta_row[1] - EXPECTED_MAX_EDGE_ETA) < 1.0e-12
        and abs(eta_gap - EXPECTED_ETA_GAP) < 1.0e-12,
        f"(max_edge_eta,gap)=({max_eta_row[1]:.12f},{eta_gap:.12f})",
    )
    check(
        "Across the tested dangerous split-2 edge, the winning transport column stays separated from the preferred quotient lane",
        min_dist_row[3] > 0.29 and abs(min_dist_row[3] - EXPECTED_MIN_COLUMN_DIST) < 1.0e-12,
        f"(s_min,dist) = ({min_dist_row[0]:.12f},{min_dist_row[3]:.12f})",
    )
    check(
        "Across the tested dangerous split-2 edge, the winning column never develops the preferred near-symmetric small-leakage pair",
        min_asym_row[4] > 0.057 and abs(min_asym_row[4] - EXPECTED_MIN_LEAKAGE_ASYM) < 1.0e-12,
        f"(s_min,|p2-p1|)=({min_asym_row[0]:.12f},{min_asym_row[4]:.12f})",
    )
    check(
        "Across the tested dangerous split-2 edge, the winning column never develops the preferred dominant entry near 0.93",
        max_large_row[5] < 0.7 and abs(max_large_row[5] - EXPECTED_MAX_LARGEST_ENTRY) < 1.0e-12,
        f"(s_max,p3)=({max_large_row[0]:.12f},{max_large_row[5]:.12f})",
    )


def part4_the_note_records_the_transport_lane_obstruction_honestly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE TRANSPORT-LANE OBSTRUCTION HONESTLY")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_TRANSPORT_LANE_OBSTRUCTION_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the preferred transport lane and its eta value",
        "1.052220313052" in note and "0.928711385999" in note,
    )
    check(
        "The note records the tested dangerous-edge transport separation numbers",
        "0.847299300834" in note and "0.293939334980" in note and "0.057100889715" in note,
    )
    check(
        "The note keeps the boundary honest: this is still not exact-carrier closure",
        "not interval-certified" in note and "not flagship closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 EDGE TRANSPORT-LANE OBSTRUCTION CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the tested broad-bundle split-2 dangerous edge already lie on the")
    print("  same transport-selected packet lane as the preferred recovered point?")

    eta_pref, column_pref = part1_the_preferred_recovered_point_carries_one_sharp_transport_lane()
    part2_the_split2_edge_transport_data_are_reproduced_stably()
    part3_the_tested_dangerous_edge_stays_off_the_preferred_transport_lane(eta_pref, column_pref)
    part4_the_note_records_the_transport_lane_obstruction_honestly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Sharp carrier-side transport read on the broad split-2 edge:")
    print("    - the dangerous edge is real on the broad bundle, but it does not")
    print("      realize the preferred recovered transport lane")
    print("    - its best eta/eta_obs stays below 0.847299300834, more than 0.20")
    print("      below the preferred recovered 1.052220313052")
    print("    - its winning packet columns stay packet-level separated from the")
    print("      preferred small-leakage quotient")
    print("  RESULT: the broad split-2 low-slack undercut is transport-incompatible")
    print("  with the preferred recovered lane on the tested edge interval")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
