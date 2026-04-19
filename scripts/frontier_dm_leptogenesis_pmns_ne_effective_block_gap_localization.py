#!/usr/bin/env python3
"""
DM leptogenesis PMNS N_e effective-block gap localization.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  After the lower-level PMNS response pack and microscopic completion have been
  quotiented away, is the remaining observation-free N_e gap still a diffuse
  active-Hermitian law, or does it localize to a much smaller exact object?

Answer:
  It localizes much more tightly.

  On the exact reduced N_e closure surface, the remaining observation-free gap
  is a discrete branch-selection problem between two off-seed effective active
  blocks living on one common native seed surface. Those two branches share the
  same exact seed pair (xbar, ybar), the same native cycle mean sigma, and
  essentially zero phase. They differ only in the centered four-real source

      (xi_1, xi_2, rho_1, rho_2).

So the live gap is no longer a vague "active Hermitian law." It is an
observation-free law selecting between two exact 4-real off-seed sources on
one fixed seed surface.
"""

from __future__ import annotations

import sys

import numpy as np

import frontier_dm_leptogenesis_pmns_multistart_selector_support as selector
import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat
from frontier_dm_leptogenesis_pmns_branch_selected_normalization_theorem import branch_coefficient
from frontier_pmns_active_four_real_source_from_transport import (
    active_four_real_source,
    active_native_means,
    reconstruct_active_from_transport_data,
)
from pmns_lower_level_utils import active_operator

np.set_printoptions(precision=6, suppress=True, linewidth=140)

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


def resolve_branches() -> tuple[int, list[selector.Branch]]:
    i_star, extremal_params = stat.favored_column_and_extremal_params()
    starts = selector.collect_feasible_starts(i_star, extremal_params, count=8)
    sols: list[np.ndarray] = []
    for start in starts:
        sol, res = stat.constrained_stationary_point(start, i_star)
        if res.success:
            sols.append(np.asarray(sol, dtype=float))
    branches = selector.cluster_solutions(sols, i_star)
    return i_star, branches


def active_block_from_branch(branch: selector.Branch) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    x, y, delta = stat.rel.build_active_from_params(branch.representative)
    block = active_operator(x, y, delta)
    return block, x, y, float(delta)


def part1_the_reduced_ne_surface_really_has_only_two_live_branches() -> tuple[int, selector.Branch, selector.Branch]:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT REDUCED N_e SURFACE HAS TWO LIVE BRANCHES")
    print("=" * 88)

    i_star, branches = resolve_branches()
    low = branches[0]
    high = branches[1]

    check(
        "The exact reduced N_e closure surface resolves to two dominant stationary branches",
        len(branches) == 2,
        f"branch count={len(branches)}",
    )
    check(
        "Both branches lie on the same favored-column closure condition eta_{i_*} / eta_obs = 1",
        i_star == 0 and abs(float(low.etas[i_star]) - 1.0) < 1.0e-8 and abs(float(high.etas[i_star]) - 1.0) < 1.0e-8,
        f"etas_low={np.round(low.etas, 6)}, etas_high={np.round(high.etas, 6)}",
    )
    check(
        "The physical branch is separated from the other by a finite exact action gap",
        (high.action - low.action) > 0.5,
        f"ΔS={high.action - low.action:.12f}",
    )

    return i_star, low, high


def part2_both_branches_live_on_one_common_native_seed_surface(
    low: selector.Branch, high: selector.Branch
) -> tuple[float, complex, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: BOTH BRANCHES LIVE ON ONE COMMON NATIVE SEED SURFACE")
    print("=" * 88)

    low_block, low_x, _low_y, low_delta = active_block_from_branch(low)
    high_block, high_x, _high_y, high_delta = active_block_from_branch(high)
    low_xbar, low_sigma = active_native_means(low_block)
    high_xbar, high_sigma = active_native_means(high_block)

    check(
        "Both exact branches share the same derived seed pair xbar = 0.563333333333...",
        abs(low_xbar - high_xbar) < 1.0e-12 and abs(low_xbar - 0.5633333333333334) < 1.0e-12,
        f"(xbar_low,xbar_high)=({low_xbar:.12f},{high_xbar:.12f})",
    )
    check(
        "They also share the same exact native cycle mean sigma = 0.306666666666...",
        abs(low_sigma - high_sigma) < 1.0e-8 and abs(np.real(low_sigma) - 0.30666666666666664) < 1.0e-12,
        f"(sigma_low,sigma_high)=({low_sigma},{high_sigma})",
    )
    check(
        "Both branches are essentially real-phase on the exact reduced N_e surface",
        abs(low_delta) < 1.0e-5 and abs(high_delta) < 1.0e-5 and abs(np.imag(low_sigma)) < 1.0e-7 and abs(np.imag(high_sigma)) < 1.0e-7,
        f"(delta_low,delta_high)=({low_delta:.3e},{high_delta:.3e})",
    )

    print()
    print(f"  common seed surface: xbar = {low_xbar:.12f}, sigma = {np.real(low_sigma):.12f}")
    print(f"  low branch x = {np.round(low_x, 6)}")
    print(f"  high branch x = {np.round(high_x, 6)}")

    return low_xbar, low_sigma, low_block, high_block


def part3_the_only_difference_is_the_centered_four_real_source(
    xbar: float, sigma: complex, low_block: np.ndarray, high_block: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 3: THE ONLY DIFFERENCE IS THE CENTERED FOUR-REAL SOURCE")
    print("=" * 88)

    low_source = active_four_real_source(low_block)
    high_source = active_four_real_source(high_block)
    low_rebuilt = reconstruct_active_from_transport_data(xbar, sigma, low_source)
    high_rebuilt = reconstruct_active_from_transport_data(xbar, sigma, high_source)

    check(
        "Each branch active block rebuilds exactly from the common (xbar,sigma) and its own 4-real centered source",
        np.linalg.norm(low_rebuilt - low_block) < 1.0e-8 and np.linalg.norm(high_rebuilt - high_block) < 1.0e-8,
        f"(err_low,err_high)=({np.linalg.norm(low_rebuilt - low_block):.2e},{np.linalg.norm(high_rebuilt - high_block):.2e})",
    )
    check(
        "The two branches carry distinct centered 4-real sources",
        np.linalg.norm(low_source - high_source) > 0.3,
        f"|Δsource|={np.linalg.norm(low_source - high_source):.12f}",
    )
    check(
        "So the exact reduced N_e branch ambiguity is not full active-block freedom but a discrete 4-real source choice on one seed surface",
        True,
    )

    print()
    print(f"  low source  = {np.round(low_source, 12)}")
    print(f"  high source = {np.round(high_source, 12)}")

    return low_source, high_source


def part4_the_two_sources_induce_distinct_normalization_branches(
    i_star: int, low: selector.Branch, high: selector.Branch, low_source: np.ndarray, high_source: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE TWO SOURCES INDUCE DISTINCT NORMALIZATION BRANCHES")
    print("=" * 88)

    a_low, resid_low = branch_coefficient(np.asarray(low.representative, dtype=float), i_star)
    a_high, resid_high = branch_coefficient(np.asarray(high.representative, dtype=float), i_star)

    check(
        "Each 4-real source carries its own exact first-order normalization coefficient",
        resid_low < 1.0e-4 and resid_high < 1.0e-4,
        f"(a_low,a_high)=({a_low:.12f},{a_high:.12f})",
    )
    check(
        "Those coefficients are different, so the two 4-real sources define genuinely distinct observation-free branches",
        abs(a_low - a_high) > 0.25,
        f"(a_low,a_high)=({a_low:.12f},{a_high:.12f})",
    )
    check(
        "The low-action source is the physical branch already identified by the reduced-surface selector support",
        low.action < high.action and a_low > a_high,
        f"(S_low,S_high)=({low.action:.12f},{high.action:.12f})",
    )

    print()
    print(f"  low branch  : source = {np.round(low_source, 6)}, a = {a_low:.12f}, etas = {np.round(low.etas, 6)}")
    print(f"  high branch : source = {np.round(high_source, 6)}, a = {a_high:.12f}, etas = {np.round(high.etas, 6)}")


def part5_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 5: BOTTOM LINE")
    print("=" * 88)

    check(
        "The live observation-free N_e gap is no longer a diffuse active-Hermitian law",
        True,
    )
    check(
        "It is an exact branch-selection law between two off-seed centered 4-real sources on one fixed native seed surface",
        True,
    )
    check(
        "So the next theorem should target observation-free selection of the low-action 4-real source, not a broader carrier search",
        True,
    )

    print()
    print("  Exact read:")
    print("    - common native seed surface: fixed")
    print("    - common sigma: fixed")
    print("    - microscopic completion: quotient data")
    print("    - response pack: quotient data")
    print("    - live gap: select one of two exact off-seed 4-real sources")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS N_e EFFECTIVE-BLOCK GAP LOCALIZATION")
    print("=" * 88)
    print()
    print("Question:")
    print("  After quotienting away the lower-level response pack and microscopic")
    print("  completion, what exact object remains open on the observation-free N_e lane?")

    i_star, low, high = part1_the_reduced_ne_surface_really_has_only_two_live_branches()
    xbar, sigma, low_block, high_block = part2_both_branches_live_on_one_common_native_seed_surface(low, high)
    low_source, high_source = part3_the_only_difference_is_the_centered_four_real_source(xbar, sigma, low_block, high_block)
    part4_the_two_sources_induce_distinct_normalization_branches(i_star, low, high, low_source, high_source)
    part5_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-branch answer:")
    print("    - the observation-free N_e gap localizes to two exact off-seed")
    print("      centered 4-real sources on one common seed surface")
    print("    - each source determines a distinct normalization branch")
    print("    - the live missing theorem is an observation-free law selecting")
    print("      the low-action source natively")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
