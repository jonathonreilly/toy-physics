#!/usr/bin/env python3
"""Lower-level passive-kernel derivation from source-response columns."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    circularity_guard,
    derive_passive_block_from_response_columns,
    effective_block_from_sector_operator,
    passive_operator,
    passive_response_columns_from_sector_operator,
    recover_passive_coeffs,
    recover_q_from_block,
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


def sample_passive_sector_operator() -> np.ndarray:
    target = passive_operator(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    return sector_operator_fixture_from_effective_block(target, seed=307)


def part1_response_columns_recover_passive_block() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SOURCE-RESPONSE COLUMNS RECOVER THE PASSIVE BLOCK")
    print("=" * 88)

    lam = 0.27
    sector = sample_passive_sector_operator()
    reference, columns = passive_response_columns_from_sector_operator(sector, lam)
    kernel, block = derive_passive_block_from_response_columns(columns, lam)
    expected = np.column_stack(columns)
    check("The lower-level observable pack is exactly the passive response-column set", np.linalg.norm(kernel - expected) < 1e-12)
    check(
        "The passive block is recovered exactly from the microscopic-sector-derived response-column set",
        np.linalg.norm(block - reference) < 1e-12,
        f"error={np.linalg.norm(block - reference):.2e}",
    )


def part2_q_and_ai_are_recovered_from_response_only() -> None:
    print("\n" + "=" * 88)
    print("PART 2: q AND a_i ARE RECOVERED FROM RESPONSES ONLY")
    print("=" * 88)

    lam = 0.27
    sector = sample_passive_sector_operator()
    reference = effective_block_from_sector_operator(sector)
    columns = passive_response_columns_from_sector_operator(sector, lam)[1]
    _kernel, block = derive_passive_block_from_response_columns(columns, lam)
    recovered_q = recover_q_from_block(block)
    recovered_coeffs = recover_passive_coeffs(block, recovered_q)
    ref_q = recover_q_from_block(reference)
    ref_coeffs = recover_passive_coeffs(reference, ref_q)

    check("q is recovered from the derived passive block", recovered_q == ref_q, f"recovered={recovered_q}")
    check("a_i is recovered from the derived passive block", np.linalg.norm(recovered_coeffs - ref_coeffs) < 1e-12,
          f"coeffs={np.round(recovered_coeffs, 6)}")


def part3_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(derive_passive_block_from_response_columns, {"q", "a", "a_i", "coeffs"})
    check("The passive derivation function takes no PMNS-side target values as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS PASSIVE KERNEL FROM SOURCE RESPONSES")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the passive monomial block be derived from lower-level")
    print("  source-response columns without taking q or a_i as theorem inputs?")

    part1_response_columns_recover_passive_block()
    part2_q_and_ai_are_recovered_from_response_only()
    part3_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact lower-level passive derivation:")
    print("    - three source-response columns determine the passive kernel")
    print("    - the passive kernel determines the passive block")
    print("    - the passive block determines q and a_i")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
