#!/usr/bin/env python3
"""
DM neutrino source-surface split-2 low-slack upper-m ridge candidate.

Question:
  On the tested broad split-2 low-slack box under the lower-repair constraint,
  do the transport-compatibility objectives already collapse toward the upper-m
  boundary?

Answer:
  Yes, on the tested coarse split-2 low-slack box.

  On the coarse slices

      m in {-0.19,-0.18,-0.17,-0.16,-0.15,-0.14},
      delta in [1.05,1.25],
      s in [0,0.06],

  subject to

      Lambda_+(m,delta,s) <= Lambda_+(x_*),

  both transport-facing objectives sharpen monotonically toward the upper-m
  boundary:

  - the slice-wise best lower-repair transport value increases monotonically
    from `0.872467928964` at `m=-0.19` to `0.883821045613` at `m=-0.14`;
  - the slice-wise minimum packet distance to the preferred quotient decreases
    monotonically from `0.301833484766` at `m=-0.19` to `0.239159397681` at
    `m=-0.14`.

  Moreover the closest-lane point on every tested m-slice sits at `s = 0`,
  and the best-eta point on every tested m-slice stays at small slack
  `s <= 0.032`.

  So on the tested broad split-2 low-slack box, the residual positive-path
  threat is no longer spread across the 3-real box. It is already pushed toward
  the upper-m low-slack ridge, with the strongest tested pressure at `m=-0.14`.

Boundary:
  This is a coarse tested-grid ridge candidate, not interval-certified exact-
  carrier closure.
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

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PKG = exact_package()
Z_GRID, SOURCE_PROFILE, WASHOUT_TAIL = flavored_transport_kernel(PKG.k_decay_exact)

M_SLICES = [-0.19, -0.18, -0.17, -0.16, -0.15, -0.14]
DELTA_GRID = np.linspace(1.05, 1.25, 31)
SLACK_GRID = np.linspace(0.0, 0.06, 31)

EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_BEST_ETAS = np.array(
    [
        0.8724679289637858,
        0.8749209885244682,
        0.8767508756632361,
        0.8795352478523553,
        0.8816192882068256,
        0.8838210456134706,
    ],
    dtype=float,
)
EXPECTED_MIN_DISTS = np.array(
    [
        0.30183348476555366,
        0.29004103745115956,
        0.27048603409725136,
        0.25970272434379027,
        0.24926159406719264,
        0.23915939768125272,
    ],
    dtype=float,
)
EXPECTED_BEST_POINTS = [
    (1.1366666666666667, 0.032),
    (1.15, 0.032),
    (1.1633333333333333, 0.012),
    (1.17, 0.028),
    (1.1766666666666667, 0.024),
    (1.1833333333333333, 0.02),
]
EXPECTED_CLOSEST_POINTS = [
    (1.1433333333333333, 0.0),
    (1.15, 0.0),
    (1.1633333333333333, 0.0),
    (1.17, 0.0),
    (1.1766666666666667, 0.0),
    (1.1833333333333333, 0.0),
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


def part1_the_preferred_lane_is_still_the_reference_target() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE PREFERRED LANE IS STILL THE REFERENCE TARGET")
    print("=" * 88)

    m_pref, d_pref, s_pref = [float(v) for v in PREFERRED_RECOVERED_LIFT]
    repair_pref, eta_pref, winner_pref, column_pref = point_data(m_pref, d_pref, s_pref)

    check(
        "The preferred recovered repair is unchanged on this branch",
        abs(repair_pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"Lambda_+*={repair_pref:.12f}",
    )
    check(
        "The preferred recovered lane still carries eta/eta_obs > 1",
        eta_pref > 1.0 and winner_pref == 2,
        f"(winner,eta)=({winner_pref},{eta_pref:.12f})",
    )

    return column_pref


def part2_slice_profiles_force_the_transport_search_toward_upper_m(
    preferred_column: np.ndarray,
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: SLICE PROFILES FORCE THE TRANSPORT SEARCH TOWARD UPPER-m")
    print("=" * 88)

    best_etas: list[float] = []
    min_dists: list[float] = []
    best_points: list[tuple[float, float]] = []
    closest_points: list[tuple[float, float]] = []

    for m in M_SLICES:
        best_eta = (-1.0, None)
        closest = (float("inf"), None)
        feasible = 0
        for delta in DELTA_GRID:
            for slack in SLACK_GRID:
                repair, eta_best, winner, column = point_data(float(m), float(delta), float(slack))
                if repair <= EXPECTED_PREF_REPAIR + 1.0e-9:
                    feasible += 1
                    if eta_best > best_eta[0]:
                        best_eta = (eta_best, (delta, slack, repair, winner, column))
                    dist = float(np.linalg.norm(column - preferred_column))
                    if dist < closest[0]:
                        closest = (dist, (delta, slack, repair, eta_best, winner, column))

        best_etas.append(float(best_eta[0]))
        min_dists.append(float(closest[0]))
        best_points.append((float(best_eta[1][0]), float(best_eta[1][1])))
        closest_points.append((float(closest[1][0]), float(closest[1][1])))

        check(
            f"Slice m={m:.2f} still contains feasible lower-repair points on the tested grid",
            feasible > 0,
            f"feasible={feasible}",
        )

    best_etas_arr = np.array(best_etas, dtype=float)
    min_dists_arr = np.array(min_dists, dtype=float)

    check(
        "The slice-wise best lower-repair transport value is reproduced stably",
        np.max(np.abs(best_etas_arr - EXPECTED_BEST_ETAS)) < 1.0e-12,
        f"best_etas={np.round(best_etas_arr, 12)}",
    )
    check(
        "The slice-wise closest packet-lane distance is reproduced stably",
        np.max(np.abs(min_dists_arr - EXPECTED_MIN_DISTS)) < 1.0e-12,
        f"min_dists={np.round(min_dists_arr, 12)}",
    )
    check(
        "The slice-wise best transport values increase monotonically toward the upper-m boundary",
        all(b > a for a, b in zip(best_etas_arr, best_etas_arr[1:])),
        f"best_etas={np.round(best_etas_arr, 12)}",
    )
    check(
        "The slice-wise closest packet-lane distances decrease monotonically toward the upper-m boundary",
        all(b < a for a, b in zip(min_dists_arr, min_dists_arr[1:])),
        f"min_dists={np.round(min_dists_arr, 12)}",
    )
    check(
        "The strongest tested lower-repair transport pressure therefore sits at m = -0.14 on the coarse slices",
        int(np.argmax(best_etas_arr)) == len(M_SLICES) - 1 and int(np.argmin(min_dists_arr)) == len(M_SLICES) - 1,
        f"(argmax_eta,argmin_dist)=({int(np.argmax(best_etas_arr))},{int(np.argmin(min_dists_arr))})",
    )

    check(
        "The best-eta points stay in a small-slack ridge on every tested m-slice",
        all(abs(dp[0] - ep[0]) < 1.0e-12 and abs(dp[1] - ep[1]) < 1.0e-12 for dp, ep in zip(best_points, EXPECTED_BEST_POINTS))
        and all(0.0 <= point[1] <= 0.032 for point in best_points),
        f"best_points={best_points}",
    )
    check(
        "The closest-lane points sit exactly on the slack floor s = 0 on every tested m-slice",
        all(abs(dp[0] - ep[0]) < 1.0e-12 and abs(dp[1] - ep[1]) < 1.0e-12 for dp, ep in zip(closest_points, EXPECTED_CLOSEST_POINTS)),
        f"closest_points={closest_points}",
    )


def part3_the_note_records_the_upper_m_ridge_reduction() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NOTE RECORDS THE UPPER-m RIDGE REDUCTION")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_LOW_SLACK_UPPER_M_RIDGE_CANDIDATE_NOTE_2026-04-18.md")

    check(
        "The note records the monotone upper-m drift of the best eta profile",
        "0.872467928964" in note and "0.883821045613" in note and "upper-\\(m\\) boundary" in note,
    )
    check(
        "The note records the monotone upper-m drift of the closest packet-lane distance",
        "0.301833484766" in note and "0.239159397681" in note,
    )
    check(
        "The note keeps the boundary honest: this is still a coarse tested-grid ridge candidate",
        "coarse tested-grid ridge candidate" in note and "not interval-certified" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE SPLIT-2 LOW-SLACK UPPER-m RIDGE CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the tested broad split-2 low-slack box, do the transport-facing")
    print("  objectives already collapse toward the upper-m boundary?")

    preferred_column = part1_the_preferred_lane_is_still_the_reference_target()
    part2_slice_profiles_force_the_transport_search_toward_upper_m(preferred_column)
    part3_the_note_records_the_upper_m_ridge_reduction()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Positive-path carrier reduction:")
    print("    - on the tested coarse split-2 low-slack slices, both transport")
    print("      objectives move monotonically toward the upper-m boundary")
    print("    - the best-eta ridge stays at small slack, and the closest-lane")
    print("      ridge sits exactly on s = 0")
    print("  RESULT: the residual tested transport threat is already pushed toward")
    print("  the upper-m low-slack ridge, with strongest pressure at m = -0.14")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
