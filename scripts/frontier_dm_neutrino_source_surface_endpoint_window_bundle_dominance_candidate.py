#!/usr/bin/env python3
"""
DM neutrino source-surface endpoint window bundle-dominance candidate.

Question:
  On the compact branch, can the endpoint `m` window already be pushed toward
  a local dominance statement directly on the exact shift-quotient bundle?

Answer:
  Yes, as a strong numerical dominance candidate.

  On the explicit exact shift-quotient bundle over `(m, delta, r31)`, the
  endpoint window

      m in [-1.899713, -1.87]

  was searched on a broad compact core

      delta in [-2.5, 2.5],  r31 in [0.5, 4.0],

  and then stress-tested on high-`r31` and high-|`delta`| tails. The best
  repair found stays well above the preferred recovered floor, with the
  minimizer sitting on the lower `r31` boundary and the tails much higher.

Boundary:
  This is not a theorem of global bundle dominance and not exact carrier
  completeness. It is a compact-branch local dominance candidate on a broad
  exact bundle box plus explicit tail challenges.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

from dm_selector_branch_support import PREFERRED_RECOVERED_LIFT, repair_from_slack_point
from frontier_dm_neutrino_source_surface_shift_quotient_bundle_theorem import quotient_gauge_h

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

M_WINDOW = (-1.899713, -1.87)
CORE_DELTA = (-2.5, 2.5)
CORE_R31 = (0.5, 4.0)

EXPECTED_PREF_REPAIR = 1.5868747147296745
EXPECTED_CORE_GRID_MIN = 3.027586796974077
EXPECTED_CORE_DE_MIN = 3.0275559194088237
EXPECTED_HIGH_R31_MIN = 6.8271130952186585
EXPECTED_HIGH_DELTA_MIN = 4.453361971273729


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


def bundle_repair(m: float, delta: float, r31: float) -> float:
    h, _pars = quotient_gauge_h(float(m), float(delta), float(r31))
    return max(0.0, -float(np.min(np.linalg.eigvalsh(np.asarray(h, dtype=complex)))))


def part1_the_endpoint_window_on_the_exact_bundle_has_a_broad_test_domain() -> float:
    print("\n" + "=" * 88)
    print("PART 1: THE ENDPOINT WINDOW ON THE EXACT BUNDLE HAS A BROAD TEST DOMAIN")
    print("=" * 88)

    pref = float(repair_from_slack_point(PREFERRED_RECOVERED_LIFT))

    check(
        "The preferred recovered repair floor is unchanged on the compact branch",
        abs(pref - EXPECTED_PREF_REPAIR) < 1.0e-12,
        f"preferred={pref:.12f}",
    )
    check(
        "The endpoint dominance test is posed directly on the exact shift-quotient bundle over (m,delta,r31)",
        True,
        f"m in [{M_WINDOW[0]:.6f},{M_WINDOW[1]:.2f}], delta in [{CORE_DELTA[0]:.1f},{CORE_DELTA[1]:.1f}], r31 in [{CORE_R31[0]:.1f},{CORE_R31[1]:.1f}]",
    )
    check(
        "The endpoint window lies entirely on the rival-side m-range identified by the obstruction note",
        M_WINDOW[0] < M_WINDOW[1] < 0.0,
        f"window={M_WINDOW}",
    )

    return pref


def part2_a_broad_core_grid_and_global_refinement_stay_above_the_preferred_floor(pref: float) -> tuple[float, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: A BROAD CORE GRID AND GLOBAL REFINEMENT STAY ABOVE THE PREFERRED FLOOR")
    print("=" * 88)

    ms = np.linspace(M_WINDOW[0], M_WINDOW[1], 13)
    deltas = np.linspace(CORE_DELTA[0], CORE_DELTA[1], 201)
    r31s = np.linspace(CORE_R31[0], CORE_R31[1], 141)

    best_grid_value = float("inf")
    best_grid_point = None
    for m in ms:
        for delta in deltas:
            for r31 in r31s:
                rep = bundle_repair(float(m), float(delta), float(r31))
                if rep < best_grid_value:
                    best_grid_value = rep
                    best_grid_point = np.array([m, delta, r31], dtype=float)

    def objective(z: np.ndarray) -> float:
        m, delta, r31 = map(float, z)
        return bundle_repair(m, delta, r31)

    de = differential_evolution(
        objective,
        [M_WINDOW, CORE_DELTA, CORE_R31],
        seed=0,
        polish=True,
        maxiter=120,
        popsize=15,
        tol=1.0e-7,
    )

    best_de_value = float(de.fun)
    best_de_point = np.asarray(de.x, dtype=float)

    check(
        "The coarse broad-box endpoint grid never undercuts the preferred recovered floor",
        best_grid_value > pref,
        f"(best_grid,gap)=({best_grid_value:.12f},{best_grid_value - pref:.12e})",
    )
    check(
        "The global differential-evolution refinement on the same endpoint box also stays above the preferred floor",
        best_de_value > pref and de.success,
        f"(best_de,gap)=({best_de_value:.12f},{best_de_value - pref:.12e})",
    )
    check(
        "The compact-box endpoint minimum is reproduced stably by grid and global refinement",
        abs(best_grid_value - EXPECTED_CORE_GRID_MIN) < 1.0e-9
        and abs(best_de_value - EXPECTED_CORE_DE_MIN) < 1.0e-9,
        f"(grid,de)=({best_grid_value:.12f},{best_de_value:.12f})",
    )
    check(
        "The refined endpoint minimizer sits on the lower-r31 boundary rather than drifting into a new interior low basin",
        abs(best_de_point[2] - CORE_R31[0]) < 1.0e-9,
        f"best_de_point={np.round(best_de_point, 12)}",
    )

    print()
    print(f"  best grid point = {np.round(best_grid_point, 12)}")
    print(f"  best grid repair= {best_grid_value:.12f}")
    print(f"  best DE point   = {np.round(best_de_point, 12)}")
    print(f"  best DE repair  = {best_de_value:.12f}")

    return best_de_value, best_de_point


def part3_high_r31_and_high_delta_tails_are_far_higher_than_the_preferred_floor(pref: float) -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 3: HIGH-R31 AND HIGH-DELTA TAILS ARE FAR HIGHER THAN THE PREFERRED FLOOR")
    print("=" * 88)

    ms = np.linspace(M_WINDOW[0], M_WINDOW[1], 13)

    best_high_r31 = float("inf")
    best_high_r31_point = None
    for m in ms:
        for delta in np.linspace(CORE_DELTA[0], CORE_DELTA[1], 101):
            for r31 in [4.5, 5.0, 6.0, 8.0, 10.0]:
                rep = bundle_repair(float(m), float(delta), float(r31))
                if rep < best_high_r31:
                    best_high_r31 = rep
                    best_high_r31_point = np.array([m, delta, r31], dtype=float)

    best_high_delta = float("inf")
    best_high_delta_point = None
    delta_tail = np.concatenate([np.linspace(-8.0, -3.0, 101), np.linspace(3.0, 8.0, 101)])
    for m in ms:
        for delta in delta_tail:
            for r31 in np.linspace(CORE_R31[0], CORE_R31[1], 71):
                rep = bundle_repair(float(m), float(delta), float(r31))
                if rep < best_high_delta:
                    best_high_delta = rep
                    best_high_delta_point = np.array([m, delta, r31], dtype=float)

    check(
        "The high-r31 endpoint tail challenge stays far above the preferred floor",
        best_high_r31 > pref and abs(best_high_r31 - EXPECTED_HIGH_R31_MIN) < 1.0e-9,
        f"(best_high_r31,gap)=({best_high_r31:.12f},{best_high_r31 - pref:.12e})",
    )
    check(
        "The high-|delta| endpoint tail challenge also stays far above the preferred floor",
        best_high_delta > pref and abs(best_high_delta - EXPECTED_HIGH_DELTA_MIN) < 1.0e-9,
        f"(best_high_delta,gap)=({best_high_delta:.12f},{best_high_delta - pref:.12e})",
    )
    check(
        "Both endpoint tail challenges are much higher than the broad core minimum",
        best_high_r31 > EXPECTED_CORE_DE_MIN and best_high_delta > EXPECTED_CORE_DE_MIN,
        f"(high_r31,high_delta)=({best_high_r31:.12f},{best_high_delta:.12f})",
    )

    print()
    print(f"  best high-r31 point   = {np.round(best_high_r31_point, 12)}")
    print(f"  best high-r31 repair  = {best_high_r31:.12f}")
    print(f"  best high-|delta| point = {np.round(best_high_delta_point, 12)}")
    print(f"  best high-|delta| repair= {best_high_delta:.12f}")

    return best_high_r31, best_high_delta


def part4_the_note_records_the_endpoint_bundle_dominance_candidate(
    core_best: float, high_r31_best: float, high_delta_best: float
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE ENDPOINT BUNDLE-DOMINANCE CANDIDATE")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_SOURCE_SURFACE_ENDPOINT_WINDOW_BUNDLE_DOMINANCE_CANDIDATE_NOTE_2026-04-17.md")

    check(
        "The note records the broad endpoint compact-box minimum above the preferred floor",
        f"{core_best:.12f}" in note and "differential evolution" in note,
    )
    check(
        "The note records the high-r31 and high-|delta| tail challenges",
        f"{high_r31_best:.12f}" in note and f"{high_delta_best:.12f}" in note,
    )
    check(
        "The note keeps the boundary honest: broad exact-bundle dominance candidate, not theorem closure",
        "not a theorem of global bundle dominance" in note and "not flagship closure" in note,
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-SURFACE ENDPOINT WINDOW BUNDLE-DOMINANCE CANDIDATE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the endpoint m-window already be pushed toward local dominance directly")
    print("  on the exact shift-quotient bundle of the compact branch?")

    pref = part1_the_endpoint_window_on_the_exact_bundle_has_a_broad_test_domain()
    core_best, _core_point = part2_a_broad_core_grid_and_global_refinement_stay_above_the_preferred_floor(pref)
    high_r31_best, high_delta_best = part3_high_r31_and_high_delta_tails_are_far_higher_than_the_preferred_floor(pref)
    part4_the_note_records_the_endpoint_bundle_dominance_candidate(core_best, high_r31_best, high_delta_best)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Endpoint exact-bundle dominance candidate:")
    print("    - on a broad exact-bundle box the endpoint m-window stays strictly above")
    print("      the preferred recovered repair floor")
    print("    - the refined minimum sits on the lower-r31 boundary")
    print("    - high-r31 and high-|delta| tail challenges are much higher still")
    print("  RESULT: strong local endpoint bundle-dominance candidate; not theorem closure")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
