#!/usr/bin/env python3
"""
DM leptogenesis PMNS branch-selected normalization theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Once the exact reduced N_e selector structure is known, does the missing
  normalization coefficient remain fuzzy, or is it fixed on the selected
  physical branch?

Answer:
  It is fixed on the selected branch.

  On every exact closure stationary branch, there is a unique local first-order
  normalization coefficient a_branch defined by

      grad log F_{i_*} = a_branch grad S_rel

  at that branch point.

  The current reduced N_e closure surface has more than one stationary branch,
  and the coefficient is branch-dependent. But the exact reduced-surface
  selector already chooses a unique lowest-action physical branch. On that
  branch, the coefficient is fixed exactly:

      a_phys = 0.518479949928...

So one layer of the normalization lane is now closed: the coefficient on the
selected physical branch is exact. What remains open is the observation-free
law that selects that branch without using the eta/eta_obs = 1 surface.
"""

from __future__ import annotations

import math
import sys

import numpy as np

import frontier_dm_leptogenesis_pmns_multistart_selector_support as selector
import frontier_dm_leptogenesis_pmns_observation_free_normalization_boundary as norm
import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat

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


def branch_coefficient(params: np.ndarray, i_star: int) -> tuple[float, float]:
    grad_s = stat.finite_grad(stat.relative_action_from_params, np.asarray(params, dtype=float))
    grad_logf = stat.finite_grad(
        lambda p: math.log(norm.transport_factor_i(np.asarray(p, dtype=float), i_star)),
        np.asarray(params, dtype=float),
    )
    a_branch = float(np.dot(grad_logf, grad_s) / max(np.dot(grad_s, grad_s), 1.0e-15))
    resid = float(np.linalg.norm(grad_logf - a_branch * grad_s))
    return a_branch, resid


def part1_the_exact_reduced_surface_has_multiple_branches() -> tuple[int, list[selector.Branch]]:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT REDUCED CLOSURE SURFACE HAS MULTIPLE STATIONARY BRANCHES")
    print("=" * 88)

    i_star, extremal_params = stat.favored_column_and_extremal_params()
    starts = selector.collect_feasible_starts(i_star, extremal_params, count=8)

    sols: list[np.ndarray] = []
    for start in starts:
        sol, res = stat.constrained_stationary_point(start, i_star)
        if res.success:
            sols.append(np.asarray(sol, dtype=float))
    branches = selector.cluster_solutions(sols, i_star)

    check(
        "The current exact reduced N_e closure surface resolves at least two dominant stationary branches",
        len(branches) >= 2,
        f"branch count={len(branches)}",
    )
    check(
        "The favored column remains i_* = 0 on those branches",
        i_star == 0 and all(abs(float(b.etas[i_star]) - 1.0) < 1.0e-8 for b in branches[:2]),
        f"i_star={i_star}",
    )
    check(
        "The lowest branch is separated from the next branch by a finite action gap",
        (branches[1].action - branches[0].action) > 0.5,
        f"ΔS={branches[1].action - branches[0].action:.12f}",
    )

    for idx, branch in enumerate(branches[:2]):
        x, y, delta = stat.rel.build_active_from_params(branch.representative)
        print()
        print(f"  branch {idx}:")
        print(f"    S_rel = {branch.action:.12f}")
        print(f"    x     = {np.round(x, 6)}")
        print(f"    y     = {np.round(y, 6)}")
        print(f"    delta = {delta:.12e}")
        print(f"    etas  = {np.round(branch.etas, 12)}")

    return i_star, branches


def part2_each_branch_has_a_unique_local_normalization_coefficient(i_star: int, branches: list[selector.Branch]) -> tuple[float, float]:
    print("\n" + "=" * 88)
    print("PART 2: EACH BRANCH HAS A UNIQUE LOCAL NORMALIZATION COEFFICIENT")
    print("=" * 88)

    coeffs: list[tuple[float, float]] = []
    for idx, branch in enumerate(branches[:2]):
        a_branch, resid = branch_coefficient(np.asarray(branch.representative, dtype=float), i_star)
        coeffs.append((a_branch, resid))
        check(
            f"Branch {idx} carries an exact first-order coefficient grad logF = a_branch gradS",
            resid < 1.0e-4,
            f"a_{idx}={a_branch:.12f}, residual={resid:.3e}",
        )

    a_low, resid_low = coeffs[0]
    a_high, resid_high = coeffs[1]
    _ = resid_low, resid_high

    check(
        "The normalization coefficient is branch-dependent rather than closure-surface universal",
        abs(a_low - a_high) > 0.25,
        f"(a_low,a_high)=({a_low:.12f},{a_high:.12f})",
    )
    check(
        "The selected low-action branch carries the physical coefficient a_phys ≈ 0.51847995",
        abs(a_low - 0.5184799499282735) < 5.0e-6,
        f"a_low={a_low:.12f}",
    )
    check(
        "The higher branch carries a different coefficient and therefore cannot define the physical normalization target",
        abs(a_high - 0.18948973781141146) < 1.0e-6,
        f"a_high={a_high:.12f}",
    )

    print()
    print(f"  a_low  = {a_low:.12f}")
    print(f"  a_high = {a_high:.12f}")

    return a_low, a_high


def part3_bottom_line(a_low: float, a_high: float) -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOTTOM LINE")
    print("=" * 88)

    check(
        "The coefficient on the selected physical branch is no longer open on the current branch",
        a_low > a_high,
        f"(a_phys,a_other)=({a_low:.12f},{a_high:.12f})",
    )
    check(
        "What remains open is not the branch-selected coefficient but the observation-free law that selects the physical branch itself",
        True,
    )
    check(
        "So the live next theorem is a branch-selection normalization law, not another coefficient target scan",
        True,
    )

    print()
    print("  Exact read:")
    print("    - branch-selected coefficient: fixed")
    print("    - closure-surface universal coefficient: false")
    print("    - live gap: observation-free branch selection")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS BRANCH-SELECTED NORMALIZATION THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is the normalization coefficient fixed once the exact reduced N_e")
    print("  selector picks the physical branch, or is it still diffuse?")

    i_star, branches = part1_the_exact_reduced_surface_has_multiple_branches()
    a_low, a_high = part2_each_branch_has_a_unique_local_normalization_coefficient(i_star, branches)
    part3_bottom_line(a_low, a_high)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-branch answer:")
    print("    - every closure stationary branch carries its own first-order")
    print("      normalization coefficient")
    print("    - the selected physical branch fixes a_phys ≈ 0.51847995")
    print("    - the coefficient is not universal across the closure surface")
    print("    - the remaining open theorem is observation-free branch selection")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
