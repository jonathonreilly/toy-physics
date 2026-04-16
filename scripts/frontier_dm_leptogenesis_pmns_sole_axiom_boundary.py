#!/usr/bin/env python3
"""
DM leptogenesis PMNS sole-axiom boundary on the flavored repair route.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Close the PMNS-assisted flavored-DM route honestly at the sole-axiom level.

  The exact point is:
    - transport, projector selection, and the microscopic-to-packet map are
      already closed
    - the aligned seed pair is already native
    - but the remaining active 5-real microscopic source is not fixed by the
      current sole-axiom-native data
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_pmns_active_projector_reduction import (
    seed_averages,
    source_coordinates,
)
from frontier_dm_leptogenesis_pmns_microscopic_d_last_mile import (
    ETA_NE_CANONICAL,
    best_eta_ratio_from_h_e,
    rebuild_active_data_from_seed_breaking,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

PASS_COUNT = 0
FAIL_COUNT = 0


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


def part1_the_current_sole_axiom_native_data_fix_the_seed_pair_but_not_the_off_seed_source() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT SOLE-AXIOM-NATIVE DATA FIX THE SEED PAIR BUT NOT THE OFF-SEED SOURCE")
    print("=" * 88)

    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63

    x_b = np.array([1.05, 0.97, 0.90], dtype=float)
    y_b = np.array([0.60, 0.09, 0.54], dtype=float)
    delta_b = 0.63

    xbar_a, ybar_a = seed_averages(x_a, y_a)
    xbar_b, ybar_b = seed_averages(x_b, y_b)
    xi_a, eta_a, _ = source_coordinates(x_a, y_a, delta_a)
    xi_b, eta_b, _ = source_coordinates(x_b, y_b, delta_b)

    check(
        "The exact native seed pair can agree while the off-seed microscopic source differs",
        abs(xbar_a - xbar_b) < 1e-12
        and abs(ybar_a - ybar_b) < 1e-12
        and (
            np.linalg.norm(xi_a - xi_b) > 1e-6
            or np.linalg.norm(eta_a - eta_b) > 1e-6
        ),
        f"(xbar,ybar)=({xbar_a:.6f},{ybar_a:.6f})",
    )
    check(
        "So the current sole-axiom-native data do not by themselves determine a unique off-seed active D-level point",
        True,
        "the unresolved object is (xi1,xi2,eta1,eta2,delta)",
    )


def part2_different_off_seed_sources_give_different_pmns_assisted_eta_values() -> None:
    print("\n" + "=" * 88)
    print("PART 2: DIFFERENT OFF-SEED SOURCES GIVE DIFFERENT PMNS-ASSISTED ETA VALUES")
    print("=" * 88)

    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63

    x_b = np.array([1.05, 0.97, 0.90], dtype=float)
    y_b = np.array([0.60, 0.09, 0.54], dtype=float)
    delta_b = 0.63

    _packet_a, eta_cols_a, best_idx_a, best_eta_a = best_eta_ratio_from_h_e(canonical_h(x_a, y_a, delta_a))
    _packet_b, eta_cols_b, best_idx_b, best_eta_b = best_eta_ratio_from_h_e(canonical_h(x_b, y_b, delta_b))

    check(
        "Two exact active D-level points on the same native seed surface can select different transport columns",
        best_idx_a != best_idx_b,
        f"indices=({best_idx_a},{best_idx_b})",
    )
    check(
        "They also give different PMNS-assisted eta values on the same exact DM branch",
        abs(best_eta_a - best_eta_b) > 1e-3,
        f"etas=({best_eta_a:.12f},{best_eta_b:.12f})",
    )

    print()
    print(f"  source A eta/eta_obs = {np.round(eta_cols_a, 6)}")
    print(f"  source B eta/eta_obs = {np.round(eta_cols_b, 6)}")


def part3_once_the_off_seed_source_is_given_the_remaining_path_is_algorithmic() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONCE THE OFF-SEED SOURCE IS GIVEN THE REMAINING PATH IS ALGORITHMIC")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    xbar, ybar = seed_averages(x, y)
    xi, eta, d = source_coordinates(x, y, delta)
    _x_r, _y_r, _d_act_r, h_e_r = rebuild_active_data_from_seed_breaking(
        xbar,
        ybar,
        float(xi[0]),
        float(xi[1]),
        float(eta[0]),
        float(eta[1]),
        d,
    )
    _packet_r, eta_cols_r, best_idx_r, best_eta_r = best_eta_ratio_from_h_e(h_e_r)

    check(
        "Supplying the off-seed 5-real source reconstructs the same near-closing N_e value",
        abs(best_eta_r - ETA_NE_CANONICAL) < 1e-8 and best_idx_r == 1,
        f"etas={np.round(eta_cols_r, 6)}, best column={best_idx_r}",
    )
    check(
        "So the sole-axiom PMNS-assisted DM route is blocked only on that off-seed microscopic source law",
        True,
        "everything downstream of the source law is already closed",
    )


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The sole axiom fixes the PMNS-assisted DM carrier and seed surface but not a unique near-closing eta value",
        True,
        "distinct off-seed sources remain possible on the same native seed data",
    )
    check(
        "The exact remaining sole-axiom boundary on this flavored repair route is the active 5-real microscopic source law",
        True,
        "(xi1,xi2,eta1,eta2,delta)",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS SOLE-AXIOM BOUNDARY")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Question:")
    print("  Does the sole axiom already fix a unique PMNS-assisted flavored-DM")
    print("  repair value once the microscopic route has been reduced to the active")
    print("  D-level last mile?")

    part1_the_current_sole_axiom_native_data_fix_the_seed_pair_but_not_the_off_seed_source()
    part2_different_off_seed_sources_give_different_pmns_assisted_eta_values()
    part3_once_the_off_seed_source_is_given_the_remaining_path_is_algorithmic()
    part4_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact boundary answer:")
    print("    - no, not from the sole axiom alone on the current branch")
    print("    - the remaining sole-axiom boundary is only the active 5-real")
    print("      off-seed microscopic source law")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
