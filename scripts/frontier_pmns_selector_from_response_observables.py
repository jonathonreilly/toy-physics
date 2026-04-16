#!/usr/bin/env python3
"""Selector derivation from lower-level response observables."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    active_operator,
    active_response_columns_from_sector_operator,
    circularity_guard,
    classify_tau_and_q_from_response_columns,
    passive_operator,
    passive_response_columns_from_sector_operator,
    sector_operator_fixture_from_effective_block,
)

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


def build_observable_packs(
    tau: int, q: int, coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float, lam_act: float, lam_pass: float
) -> tuple[list[np.ndarray], list[np.ndarray]]:
    active_sector = sector_operator_fixture_from_effective_block(active_operator(x, y, delta), seed=401 + 17 * tau + q)
    passive_sector = sector_operator_fixture_from_effective_block(passive_operator(coeffs, q), seed=557 + 17 * tau + q)
    active_cols = active_response_columns_from_sector_operator(active_sector, lam_act)[1]
    passive_cols = passive_response_columns_from_sector_operator(passive_sector, lam_pass)[1]
    return (active_cols, passive_cols) if tau == 0 else (passive_cols, active_cols)


def part1_selector_is_derived_from_response_observable_packs() -> None:
    print("\n" + "=" * 88)
    print("PART 1: TAU AND q ARE DERIVED FROM RESPONSE OBSERVABLE PACKS")
    print("=" * 88)

    samples = [
        ("neutrino-active", 0, 2, np.array([0.07, 0.11, 0.23], dtype=complex), np.array([1.15, 0.82, 0.95]), np.array([0.41, 0.28, 0.54]), 0.63),
        ("charged-lepton-active", 1, 1, np.array([0.17, 0.09, 0.04], dtype=complex), np.array([0.92, 1.08, 0.85]), np.array([0.33, 0.49, 0.26]), -0.37),
    ]
    for label, tau, q, coeffs, x, y, delta in samples:
        neutral_cols, charge_cols = build_observable_packs(tau, q, coeffs, x, y, delta, 0.31, 0.27)
        recovered_tau, recovered_q, _neutral_block, _charge_block = classify_tau_and_q_from_response_columns(
            neutral_cols, charge_cols, 0.31, 0.27
        )
        check(f"{label}: tau is derived from lower-level response observables", recovered_tau == tau, f"recovered={recovered_tau}")
        check(f"{label}: q is derived from lower-level response observables", recovered_q == q, f"recovered={recovered_q}")


def part2_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 2: CIRCULARITY GUARD")
    print("=" * 88)
    ok, bad = circularity_guard(classify_tau_and_q_from_response_columns, {"tau", "q", "d0_trip", "dm_trip"})
    check("The selector derivation takes no PMNS-side target values as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS SELECTOR FROM RESPONSE OBSERVABLES")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can tau and q be derived in the same chain from lower-level")
    print("  microscopic response observables?")

    part1_selector_is_derived_from_response_observable_packs()
    part2_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact lower-level selector derivation:")
    print("    - tau is derived by active/passive family classification on the")
    print("      response-derived blocks")
    print("    - q is derived from the passive response-derived block")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
