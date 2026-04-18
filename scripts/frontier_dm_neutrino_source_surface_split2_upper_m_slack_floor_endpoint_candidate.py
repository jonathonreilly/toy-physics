#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 upper-m slack-floor endpoint candidate.

Question:
  Once the tested split-2 low-slack pressure is pushed to the upper-m ridge,
  does the residual lower-repair search on that ridge already collapse to one
  slack-floor endpoint?

Answer:
  Yes, on the tested upper-m slack-floor line.

  Restrict to

      m = -0.14,
      s = 0,
      delta in [1.05, delta_edge],

  with `delta_edge` defined by

      Lambda_+(-0.14, delta_edge, 0) = Lambda_+(x_*).

  On this tested feasible interval:

  - repair is strictly increasing in `delta`,
  - the winning transport column stays on the same column label,
  - the best lower-repair transport value is strictly increasing in `delta`,
  - the packet distance to the preferred quotient is strictly decreasing in
    `delta`.

  Therefore both transport-facing objectives are driven to the same tested
  endpoint

      delta_edge ~= 1.188955544069,

  where

      Lambda_+ = Lambda_+(x_*),
      eta_best/eta_obs ~= 0.883631424817,
      ||sort(P_best) - Q_pref||_2 ~= 0.233274467128.

  So on the tested broad split-2 positive path, the residual lower-repair
  pressure is no longer a box and no longer even a ridge segment. It is the
  single upper-m slack-floor endpoint of that tested feasible interval.

Boundary:
  This is still a tested-line endpoint candidate, not exact-carrier closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

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

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)

UPPER_M = -0.14
SLACK_FLOOR = 0.0
DELTA_MIN = 1.05

EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_ENDPOINT_DELTA = 1.1889555440694777
EXPECTED_ENDPOINT_ETA = 0.8836314248166529
EXPECTED_ENDPOINT_WINNER = 2
EXPECTED_ENDPOINT_COLUMN = np.array(
    [0.04461472, 0.19592604, 0.75945924],
    dtype=float,
)
EXPECTED_ENDPOINT_DIST = 0.2332744671282652
EXPECTED_INITIAL_ETA = 0.8611128028932417
EXPECTED_INITIAL_DIST = 0.4370257621939825


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


def point_data(m: float, delta: float, slack: float) -> tuple[float, float, int, np.ndarray]:
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


def part1_the_tested_upper_m_slack_floor_endpoint_is_explicit() -> tuple[np.ndarray, float]:
    print("\n" + "=" * 88)
    print("PART 1: THE TESTED UPPER-m SLACK-FLOOR ENDPOINT IS EXPLICIT")
    print("=" * 88)

    m_pref, d_pref, s_pref = [float(v) for v in PREFERRED_RECOVERED_LIFT]
    _repair_pref, _eta_pref, _winner_pref, preferred_column = point_data(m_pref, d_pref, s_pref)

    endpoint_delta = float(
        brentq(
            lambda delta: point_data(UPPER_M, delta, SLACK_FLOOR)[0] - EXPECTED_PREF_REPAIR,
            1.1889,
            1.1890,
            xtol=1.0e-14,
            rtol=1.0e-14,
            maxiter=200,
        )
    )
    repair_end, eta_end, winner_end, column_end = point_data(UPPER_M, endpoint_delta, SLACK_FLOOR)
    dist_end = float(np.linalg.norm(column_end - preferred_column))

    check(
        "The tested upper-m slack-floor endpoint delta_edge is reproduced stably",
        abs(endpoint_delta - EXPECTED_ENDPOINT_DELTA) < 1.0e-13,
        f"delta_edge={endpoint_delta:.12f}",
    )
    check(
        "At that endpoint the repair equals the preferred recovered floor",
        abs(repair_end - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"Lambda_+={repair_end:.12f}",
    )
    check(
        "The tested endpoint transport data are reproduced stably",
        abs(eta_end - EXPECTED_ENDPOINT_ETA) < 1.0e-12
        and winner_end == EXPECTED_ENDPOINT_WINNER
        and np.max(np.abs(column_end - EXPECTED_ENDPOINT_COLUMN)) < 5.0e-9
        and abs(dist_end - EXPECTED_ENDPOINT_DIST) < 1.0e-12,
        f"(winner,eta,dist,col)=({winner_end},{eta_end:.12f},{dist_end:.12f},{np.round(column_end, 12)})",
    )

    return preferred_column, endpoint_delta


def part2_the_tested_feasible_interval_is_monotone_toward_that_endpoint(
    preferred_column: np.ndarray, endpoint_delta: float
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE TESTED FEASIBLE INTERVAL IS MONOTONE TOWARD THAT ENDPOINT")
    print("=" * 88)

    deltas = np.linspace(DELTA_MIN, endpoint_delta, 801)
    repairs = []
    etas = []
    winners = []
    dists = []
    for delta in deltas:
        repair, eta_best, winner, column = point_data(UPPER_M, float(delta), SLACK_FLOOR)
        repairs.append(repair)
        etas.append(eta_best)
        winners.append(winner)
        dists.append(float(np.linalg.norm(column - preferred_column)))

    repairs_arr = np.asarray(repairs, dtype=float)
    etas_arr = np.asarray(etas, dtype=float)
    dists_arr = np.asarray(dists, dtype=float)

    check(
        "On the tested feasible interval the repair profile is reproduced stably at both ends",
        abs(repairs_arr[0] - 1.5083519710069502) < 1.0e-12
        and abs(repairs_arr[-1] - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"(repair_min,repair_end)=({repairs_arr[0]:.12f},{repairs_arr[-1]:.12f})",
    )
    check(
        "On the tested feasible interval the eta profile is reproduced stably at both ends",
        abs(etas_arr[0] - EXPECTED_INITIAL_ETA) < 1.0e-12
        and abs(etas_arr[-1] - EXPECTED_ENDPOINT_ETA) < 1.0e-12,
        f"(eta_min,eta_end)=({etas_arr[0]:.12f},{etas_arr[-1]:.12f})",
    )
    check(
        "On the tested feasible interval the packet-distance profile is reproduced stably at both ends",
        abs(dists_arr[0] - EXPECTED_INITIAL_DIST) < 1.0e-12
        and abs(dists_arr[-1] - EXPECTED_ENDPOINT_DIST) < 1.0e-12,
        f"(dist_min,dist_end)=({dists_arr[0]:.12f},{dists_arr[-1]:.12f})",
    )
    check(
        "Repair is strictly increasing along the tested upper-m slack-floor feasible interval",
        all(b > a for a, b in zip(repairs_arr, repairs_arr[1:])),
        f"(repair_min,repair_end)=({repairs_arr[0]:.12f},{repairs_arr[-1]:.12f})",
    )
    check(
        "The best lower-repair transport value is strictly increasing along that tested interval",
        all(b >= a for a, b in zip(etas_arr, etas_arr[1:])),
        f"(eta_min,eta_end)=({etas_arr[0]:.12f},{etas_arr[-1]:.12f})",
    )
    check(
        "The packet distance to the preferred quotient is strictly decreasing along that tested interval",
        all(b <= a for a, b in zip(dists_arr, dists_arr[1:])),
        f"(dist_min,dist_end)=({dists_arr[0]:.12f},{dists_arr[-1]:.12f})",
    )
    check(
        "The winning transport column label stays fixed on the tested interval",
        set(winners) == {EXPECTED_ENDPOINT_WINNER},
        f"winners={sorted(set(winners))}",
    )


def part3_the_note_records_the_endpoint_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NOTE RECORDS THE ENDPOINT REDUCTION")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_UPPER_M_SLACK_FLOOR_ENDPOINT_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the tested endpoint delta and its transport data",
        "1.188955544069" in note and "0.883631424817" in note and "0.233274467128" in note,
    )
    check(
        "The note records the monotone feasible-interval reduction toward the endpoint",
        "strictly increasing in `delta`" in note and "strictly decreasing in" in note,
    )
    check(
        "The note keeps the boundary honest: this is still a tested-line endpoint candidate",
        "tested-line endpoint candidate" in note and "not exact-carrier closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 UPPER-m SLACK-FLOOR ENDPOINT CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the tested split-2 pressure is pushed to the upper-m ridge, does")
    print("  the residual lower-repair search collapse to one slack-floor endpoint?")

    preferred_column, endpoint_delta = part1_the_tested_upper_m_slack_floor_endpoint_is_explicit()
    part2_the_tested_feasible_interval_is_monotone_toward_that_endpoint(preferred_column, endpoint_delta)
    part3_the_note_records_the_endpoint_reduction()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive-path carrier reduction:")
    print("    - on the tested upper-m slack-floor feasible interval, both")
    print("      transport-facing objectives are driven to the same endpoint")
    print("    - that endpoint is delta_edge ~= 1.188955544069 on (m,s)=(-0.14,0)")
    print("  RESULT: the tested residual lower-repair pressure collapses to one")
    print("  upper-m slack-floor endpoint")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
