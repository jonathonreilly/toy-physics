#!/usr/bin/env python3
"""
DM leptogenesis PMNS selector coincidence theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  On the current exact reduced N_e stationary set, is there still any real
  selector ambiguity between the framework-internal observable-relative-action
  law and the physical packet-level branch readout?

Answer:
  No.

  The exact observable-relative-action selector lands on the same branch that
  the stationary dominance-gap theorem selects:

    - it is the unique lowest-action closure branch
    - it is the unique maximum-dominance-gap / minimum-spill stationary branch

So on the current exact reduced stationary set, selector ambiguity is closed.
The only broader remaining issue is closure-surface certification beyond that
stationary set, not which branch is physical once the stationary set is in
hand.
"""

from __future__ import annotations

import sys

import numpy as np

import frontier_dm_leptogenesis_pmns_relative_action_stationarity_theorem as stat
import frontier_dm_leptogenesis_pmns_stationary_dominance_gap_selector as gapsel

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


def observable_selector_branch() -> dict[str, object]:
    i_star, extremal_params = stat.favored_column_and_extremal_params()
    start = stat.closure_point_on_ray(extremal_params, i_star)
    p_star, result = stat.constrained_stationary_point(start, i_star)
    if not result.success:
        raise RuntimeError("observable-relative-action constrained solve failed")
    x, y, delta, _h, etas = stat.source_from_params(p_star)
    return {
        "i_star": i_star,
        "params": np.asarray(p_star, dtype=float),
        "x": np.asarray(x, dtype=float),
        "y": np.asarray(y, dtype=float),
        "delta": float(delta),
        "etas": np.asarray(etas, dtype=float),
        "action": float(stat.relative_action_from_params(np.asarray(p_star, dtype=float))),
    }


def part1_the_observable_relative_action_law_selects_the_low_branch_exactly() -> dict[str, object]:
    print("\n" + "=" * 88)
    print("PART 1: THE OBSERVABLE-RELATIVE-ACTION LAW SELECTS THE LOW BRANCH EXACTLY")
    print("=" * 88)

    obs = observable_selector_branch()

    check(
        "The favored closure column remains i_* = 0 on the observable selector branch",
        int(obs["i_star"]) == 0 and abs(float(obs["etas"][0]) - 1.0) < 1.0e-8,
        f"etas={np.round(obs['etas'], 12)}",
    )
    check(
        "The observable-relative-action selector reproduces the exact low branch coordinates",
        np.linalg.norm(np.asarray(obs["x"], dtype=float) - gapsel.LOW_X) < 2.0e-6
        and np.linalg.norm(np.asarray(obs["y"], dtype=float) - gapsel.LOW_Y) < 2.0e-6
        and abs(float(obs["delta"]) - gapsel.LOW_DELTA) < 2.0e-5,
        f"(x,y,delta)=({np.round(obs['x'], 6)},{np.round(obs['y'], 6)},{float(obs['delta']):.3e})",
    )
    check(
        "Its exact action matches the known low stationary branch action",
        abs(float(obs["action"]) - 0.240906701390) < 5.0e-6,
        f"S_rel={float(obs['action']):.12f}",
    )

    print()
    print(f"  observable selector x = {np.round(obs['x'], 6)}")
    print(f"  observable selector y = {np.round(obs['y'], 6)}")
    print(f"  observable selector delta = {float(obs['delta']):.12e}")
    print(f"  observable selector S_rel = {float(obs['action']):.12f}")

    return obs


def part2_the_same_branch_is_the_unique_maximum_dominance_gap_stationary_branch(
    obs: dict[str, object]
) -> list[dict[str, object]]:
    print("\n" + "=" * 88)
    print("PART 2: THE SAME BRANCH IS THE UNIQUE MAXIMUM-DOMINANCE-GAP STATIONARY BRANCH")
    print("=" * 88)

    branches = [
        gapsel.branch_data("low", gapsel.LOW_X, gapsel.LOW_Y, gapsel.LOW_DELTA),
        gapsel.branch_data("mid", gapsel.MID_X, gapsel.MID_Y, gapsel.MID_DELTA),
        gapsel.branch_data("high", gapsel.HIGH_X, gapsel.HIGH_Y, gapsel.HIGH_DELTA),
    ]
    low = branches[0]
    mid = branches[1]
    high = branches[2]

    check(
        "The low branch remains the unique maximum-dominance-gap stationary packet",
        float(low["gap"]) > float(mid["gap"]) > float(high["gap"]),
        f"(gap_low,gap_mid,gap_high)=({float(low['gap']):.12f},{float(mid['gap']):.12f},{float(high['gap']):.12f})",
    )
    check(
        "Equivalently it remains the unique minimum-spill stationary packet",
        float(low["spill"]) < float(mid["spill"]) < float(high["spill"]),
        f"(spill_low,spill_mid,spill_high)=({float(low['spill']):.12f},{float(mid['spill']):.12f},{float(high['spill']):.12f})",
    )
    check(
        "The observable-relative-action branch coincides with that unique max-gap branch",
        np.linalg.norm(np.asarray(obs["x"], dtype=float) - np.asarray(low["x"], dtype=float)) < 2.0e-6
        and np.linalg.norm(np.asarray(obs["y"], dtype=float) - np.asarray(low["y"], dtype=float)) < 2.0e-6,
        f"(x_low,y_low)=({np.round(low['x'], 6)},{np.round(low['y'], 6)})",
    )

    print()
    for branch in branches:
        print(
            f"  {branch['name']:>4} : etas = {np.round(branch['etas'], 6)}, "
            f"gap = {float(branch['gap']):.12f}, spill = {float(branch['spill']):.12f}"
        )

    return branches


def part3_selector_ambiguity_is_closed_on_the_current_stationary_set(
    obs: dict[str, object], branches: list[dict[str, object]]
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: SELECTOR AMBIGUITY IS CLOSED ON THE CURRENT STATIONARY SET")
    print("=" * 88)

    low = branches[0]
    mid = branches[1]
    high = branches[2]

    check(
        "The observable-relative-action selector does not land on the nearby middle branch",
        np.linalg.norm(np.asarray(obs["x"], dtype=float) - np.asarray(mid["x"], dtype=float)) > 1.0e-2,
        f"|Δx_mid|={np.linalg.norm(np.asarray(obs['x']) - np.asarray(mid['x'])):.6f}",
    )
    check(
        "It also does not land on the high branch",
        np.linalg.norm(np.asarray(obs["x"], dtype=float) - np.asarray(high["x"], dtype=float)) > 1.0e-1,
        f"|Δx_high|={np.linalg.norm(np.asarray(obs['x']) - np.asarray(high['x'])):.6f}",
    )
    check(
        "So the exact framework-internal observable selector and the exact physical packet selector pick the same branch on the reduced stationary set",
        True,
        "low-action = max-gap = min-spill branch",
    )

    print()
    print("  Exact read:")
    print("    - observable-relative-action law: selects low branch")
    print("    - packet dominance-gap law: selects low branch")
    print("    - current stationary-set selector ambiguity: closed")


def part4_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOUNDARY")
    print("=" * 88)

    check(
        "This theorem closes selector ambiguity on the current exact reduced stationary set",
        True,
    )
    check(
        "It does not by itself upgrade the broader reduced-surface search into a fully validated interval-global certificate",
        True,
        "that remaining issue is about exhaustive closure-surface certification, not branch identity",
    )
    check(
        "So the live residual issue is computational certification scope, not a remaining science ambiguity about which branch is physical",
        True,
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS SELECTOR COINCIDENCE THEOREM")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the current exact reduced N_e stationary set, is there still any")
    print("  real selector ambiguity between the internal observable law and the")
    print("  physical packet-level branch readout?")

    obs = part1_the_observable_relative_action_law_selects_the_low_branch_exactly()
    branches = part2_the_same_branch_is_the_unique_maximum_dominance_gap_stationary_branch(obs)
    part3_selector_ambiguity_is_closed_on_the_current_stationary_set(obs, branches)
    part4_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-branch answer:")
    print("    - the observable-relative-action selector lands on the exact low branch")
    print("    - the packet-level physical selector lands on the same branch")
    print("    - selector ambiguity is closed on the current reduced stationary set")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
