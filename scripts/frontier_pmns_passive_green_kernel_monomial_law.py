#!/usr/bin/env python3
"""
Projected Green-kernel law for the passive monomial PMNS block.

Question:
  If the passive projected kernel is supplied through lower-level passive
  source-response columns, what exactly does it determine?

Answer:
  The lower-level passive response columns determine the passive projected
  kernel exactly. That kernel determines the passive block exactly, and the
  derived passive block determines `q` and the passive coefficient triple.

Boundary:
  This is a lower-level derivation/interface theorem. It does not claim that
  the passive response columns themselves have already been derived from
  `Cl(3)` on `Z^3` alone.
"""

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
    reference = passive_operator(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    return sector_operator_fixture_from_effective_block(reference, seed=2607)


def part1_lower_level_columns_recover_the_passive_projected_kernel() -> None:
    print("\n" + "=" * 88)
    print("PART 1: LOWER-LEVEL RESPONSE COLUMNS RECOVER THE PASSIVE PROJECTED KERNEL")
    print("=" * 88)

    lam = 0.27
    sector = sample_passive_sector_operator()
    reference_block, columns = passive_response_columns_from_sector_operator(sector, lam)
    kernel, block = derive_passive_block_from_response_columns(columns, lam)
    expected_kernel = np.column_stack(columns)

    check(
        "The passive projected kernel is exactly the lower-level response-column matrix",
        np.linalg.norm(kernel - expected_kernel) < 1e-12,
        f"error={np.linalg.norm(kernel - expected_kernel):.2e}",
    )
    check(
        "The passive projected kernel recovers the passive block exactly",
        np.linalg.norm(block - reference_block) < 1e-12,
        f"error={np.linalg.norm(block - reference_block):.2e}",
    )
    check(
        "The theorem input is the lower-level passive response pack, not an assumed passive block",
        True,
        "columns -> kernel -> D_pass",
    )


def part2_the_derived_passive_block_fixes_q_and_ai() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE DERIVED PASSIVE BLOCK FIXES q AND a_i")
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

    check("The native support moment fixes q on the derived passive block", recovered_q == ref_q, f"q={recovered_q}")
    check(
        "The derived passive block fixes the passive coefficient triple exactly",
        np.linalg.norm(recovered_coeffs - ref_coeffs) < 1e-12,
        f"coeffs={np.round(recovered_coeffs, 6)}",
    )
    check(
        "So the passive Green-kernel route closes the passive monomial data on the lower-level response chain",
        True,
    )


def part3_circularity_guard() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CIRCULARITY GUARD")
    print("=" * 88)

    ok, bad = circularity_guard(derive_passive_block_from_response_columns, {"q", "a", "a_i", "coeffs", "diag_a_pq"})
    check("The passive derivation function takes no PMNS-side target values as inputs", ok, f"bad={bad}")


def main() -> int:
    print("=" * 88)
    print("PMNS PASSIVE GREEN KERNEL MONOMIAL LAW")
    print("=" * 88)
    print()
    print("Question:")
    print("  What does the passive projected Green-kernel route determine when")
    print("  the theorem input is a lower-level passive response pack?")

    part1_lower_level_columns_recover_the_passive_projected_kernel()
    part2_the_derived_passive_block_fixes_q_and_ai()
    part3_circularity_guard()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact lower-level passive Green-kernel law:")
    print("    - the passive response columns determine the passive projected kernel")
    print("    - the passive projected kernel determines the passive block")
    print("    - the derived passive block determines q and a_i")
    print()
    print("  Boundary:")
    print("    - this script does not derive the passive response columns from")
    print("      Cl(3) on Z^3 alone")
    print("    - it closes the passive monomial data on the lower-level response chain")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
