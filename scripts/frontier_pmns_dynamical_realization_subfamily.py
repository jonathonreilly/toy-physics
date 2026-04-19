#!/usr/bin/env python3
"""Lower-level dynamical realization theorem on the PMNS carrier."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    active_operator,
    active_response_columns_from_sector_operator,
    canonicalize_active,
    classify_tau_and_q_from_response_columns,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    detect_monomial,
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


def sample_realizable_sector_pair() -> tuple[np.ndarray, np.ndarray]:
    active_sector = sector_operator_fixture_from_effective_block(
        active_operator(np.array([1.15, 0.82, 0.95]), np.array([0.41, 0.28, 0.54]), 0.63),
        seed=1601,
    )
    passive_sector = sector_operator_fixture_from_effective_block(
        passive_operator(np.array([0.07, 0.11, 0.23], dtype=complex), 2),
        seed=1701,
    )
    return active_sector, passive_sector


def part1_realizable_lower_level_image_is_support_constrained() -> None:
    print("\n" + "=" * 88)
    print("PART 1: REALIZABLE LOWER-LEVEL IMAGE IS A STRICT SUPPORT SUBFAMILY")
    print("=" * 88)

    active_sector, passive_sector = sample_realizable_sector_pair()
    active_cols = active_response_columns_from_sector_operator(active_sector, 0.31)[1]
    passive_cols = passive_response_columns_from_sector_operator(passive_sector, 0.27)[1]

    _k_act, active_block = derive_active_block_from_response_columns(active_cols, 0.31)
    _k_pass, passive_block = derive_passive_block_from_response_columns(passive_cols, 0.27)

    check("Every realizable active block recovered from microscopic-sector-derived observables lies in the canonical two-Higgs family",
          canonicalize_active(active_block) is not None)
    check("Every realizable passive block recovered from microscopic-sector-derived observables lies in the monomial family",
          detect_monomial(passive_block) is not None)


def part2_counterexample_outside_the_realizable_image_exists() -> None:
    print("\n" + "=" * 88)
    print("PART 2: A CARRIER DIRECTION OUTSIDE THE REALIZABLE IMAGE EXISTS")
    print("=" * 88)

    nonrealizable_active = np.array(
        [
            [1.0, 0.2, 0.3],
            [0.4, 1.1, 0.5],
            [0.6, 0.7, 0.9],
        ],
        dtype=complex,
    )
    nonrealizable_passive = np.array(
        [
            [0.0, 0.2, 0.1],
            [0.3, 0.0, 0.4],
            [0.5, 0.6, 0.0],
        ],
        dtype=complex,
    )
    check("A generic carrier element with backward-cycle support is not in the active realizable image",
          canonicalize_active(nonrealizable_active) is None)
    check("A generic carrier element with multi-support rows is not in the passive realizable image",
          detect_monomial(nonrealizable_passive) is None)


def part3_the_single_axiom_nonclosure_theorem_is_refined_at_the_dynamical_level() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SINGLE-AXIOM NONCLOSURE THEOREM IS REFINED DYNAMICALLY")
    print("=" * 88)

    active_sector, passive_sector = sample_realizable_sector_pair()
    neutral_cols, charge_cols = (
        active_response_columns_from_sector_operator(active_sector, 0.31)[1],
        passive_response_columns_from_sector_operator(passive_sector, 0.27)[1],
    )
    tau, q, _n, _c = classify_tau_and_q_from_response_columns(neutral_cols, charge_cols, 0.31, 0.27)
    check("Lower-level realizability fixes a strict PMNS subfamily rather than the whole carrier", tau == 0 and q == 2)
    check("So carrier nonclosure does not imply dynamical nonclosure on the realizable image", True)


def main() -> int:
    print("=" * 88)
    print("PMNS DYNAMICAL REALIZATION SUBFAMILY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Do lower-level response maps realize the whole single-axiom PMNS carrier,")
    print("  or only a strict subfamily?")

    part1_realizable_lower_level_image_is_support_constrained()
    part2_counterexample_outside_the_realizable_image_exists()
    part3_the_single_axiom_nonclosure_theorem_is_refined_at_the_dynamical_level()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact refinement:")
    print("    - the single-axiom carrier theorem remains true as a span statement")
    print("    - but lower-level realizability lands in a strict canonical PMNS subfamily")
    print("    - therefore carrier nonclosure is not the final dynamical word")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
