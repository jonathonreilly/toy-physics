#!/usr/bin/env python3
"""Lower-level active-kernel derivation from source-response columns."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    active_operator,
    active_response_columns_from_sector_operator,
    circularity_guard,
    derive_active_block_from_response_columns,
    effective_block_from_sector_operator,
    seed_source_from_active_block,
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


def sample_active_sector_operator() -> np.ndarray:
    target = active_operator(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    return sector_operator_fixture_from_effective_block(target, seed=211)


def part1_response_columns_recover_the_active_block() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SOURCE-RESPONSE COLUMNS RECOVER THE ACTIVE BLOCK")
    print("=" * 88)

    lam = 0.31
    sector = sample_active_sector_operator()
    reference = effective_block_from_sector_operator(sector)
    reference, columns = active_response_columns_from_sector_operator(sector, lam)
    kernel, block = derive_active_block_from_response_columns(columns, lam)

    expected = np.column_stack(columns)
    check("The lower-level observable pack is exactly the active response-column set", np.linalg.norm(kernel - expected) < 1e-12)
    check(
        "The active block is recovered exactly from the microscopic-sector-derived response-column set",
        np.linalg.norm(block - reference) < 1e-12,
        f"error={np.linalg.norm(block - reference):.2e}",
    )


def part2_coordinates_are_recovered_without_pmns_inputs() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ACTIVE COORDINATES ARE RECONSTRUCTED FROM RESPONSES ONLY")
    print("=" * 88)

    lam = 0.31
    sector = sample_active_sector_operator()
    reference = effective_block_from_sector_operator(sector)
    columns = active_response_columns_from_sector_operator(sector, lam)[1]
    _kernel, block = derive_active_block_from_response_columns(columns, lam)
    coords = seed_source_from_active_block(block)
    ref_coords = seed_source_from_active_block(reference)

    check("xbar is recovered from microscopic-sector-derived source-response data only", abs(coords["xbar"] - ref_coords["xbar"]) < 1e-12,
          f"xbar={coords['xbar']:.6f}")
    check("ybar is recovered from microscopic-sector-derived source-response data only", abs(coords["ybar"] - ref_coords["ybar"]) < 1e-12,
          f"ybar={coords['ybar']:.6f}")
    check(
        "The 5-real source is recovered from microscopic-sector-derived source-response data only",
        np.linalg.norm(
            np.array([coords["xi1"], coords["xi2"], coords["eta1"], coords["eta2"], coords["delta"]])
            - np.array([ref_coords["xi1"], ref_coords["xi2"], ref_coords["eta1"], ref_coords["eta2"], ref_coords["delta"]])
        ) < 1e-12,
    )


def part3_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(derive_active_block_from_response_columns, {"tau", "q", "x", "y", "delta"})
    check("The active derivation function takes no PMNS-side target values as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS ACTIVE KERNEL FROM SOURCE RESPONSES")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the active block be derived from lower-level source-response columns")
    print("  without taking PMNS-side value data as theorem inputs?")

    part1_response_columns_recover_the_active_block()
    part2_coordinates_are_recovered_without_pmns_inputs()
    part3_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact lower-level active derivation:")
    print("    - three source-response columns determine the active kernel")
    print("    - the active kernel determines the active block")
    print("    - the active block determines (xbar, ybar, xi_1, xi_2, eta_1, eta_2, delta)")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
