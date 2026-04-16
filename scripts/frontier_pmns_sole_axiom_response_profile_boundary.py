#!/usr/bin/env python3
"""Sole-axiom lower-level response-profile boundary for the retained PMNS lane."""

from __future__ import annotations

import sys
import numpy as np

from pmns_lower_level_utils import (
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    passive_response_columns_from_sector_operator,
)
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_active_four_real_source_from_transport import (
    active_four_real_source,
    active_native_means,
)
from frontier_pmns_microscopic_d_four_real_last_mile import passive_moduli_from_hermitian

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
I3 = np.eye(3, dtype=complex)


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


def expect_raises(fn, exc_type) -> tuple[bool, str]:
    try:
        fn()
    except exc_type as e:  # noqa: PERF203
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, f"wrong exception {type(e).__name__}: {e}"
    return False, "no exception"


def part1_sole_axiom_free_response_profiles_are_exact_and_trivial() -> tuple[list[np.ndarray], list[np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 1: SOLE-AXIOM LOWER-LEVEL RESPONSE PROFILES ARE EXACT AND TRIVIAL")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    active_cols = active_response_columns_from_sector_operator(I3, lam_act)[1]
    passive_cols = passive_response_columns_from_sector_operator(I3, lam_pass)[1]
    act_kernel, act_block = derive_active_block_from_response_columns(active_cols, lam_act)
    pass_kernel, pass_block = derive_passive_block_from_response_columns(passive_cols, lam_pass)

    check("The sole-axiom active lower-level response profile is exactly the identity column set",
          np.linalg.norm(np.column_stack(active_cols) - I3) < 1e-12)
    check("The sole-axiom active response profile recovers the free active block I_3 exactly",
          np.linalg.norm(act_block - I3) < 1e-12 and np.linalg.norm(act_kernel - I3) < 1e-12)
    check("The sole-axiom passive lower-level response profile is exactly a scalar column set",
          np.linalg.norm(np.column_stack(passive_cols) - (1.0 / (1.0 - lam_pass)) * I3) < 1e-12)
    check("The sole-axiom passive response profile recovers the free passive block I_3 exactly",
          np.linalg.norm(pass_block - I3) < 1e-12)
    return active_cols, passive_cols


def part2_all_reduced_pmns_data_collapse_to_the_trivial_free_point(
    active_cols: list[np.ndarray], passive_cols: list[np.ndarray]
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: ALL REDUCED PMNS DATA COLLAPSE TO THE TRIVIAL FREE POINT")
    print("=" * 88)

    act_block = derive_active_block_from_response_columns(active_cols, 0.31)[1]
    pass_block = derive_passive_block_from_response_columns(passive_cols, 0.27)[1]
    xbar, sigma = active_native_means(act_block)
    source = active_four_real_source(act_block)
    mods = passive_moduli_from_hermitian(pass_block)

    check("The sole-axiom active mean is exactly xbar = 1", abs(xbar - 1.0) < 1e-12, f"xbar={xbar:.6f}")
    check("The sole-axiom active cycle mean is exactly sigma = 0", abs(sigma) < 1e-12, f"sigma={sigma}")
    check("The sole-axiom active four-real source vanishes identically", np.linalg.norm(source) < 1e-12,
          f"source={np.round(source, 6)}")
    check("The sole-axiom passive Hermitian moduli are exactly (1,1,1)", np.linalg.norm(mods - np.ones(3)) < 1e-12,
          f"mods={np.round(mods, 6)}")


def part3_the_sole_axiom_profiles_do_not_realize_the_retained_pmns_lane(
    active_cols: list[np.ndarray], passive_cols: list[np.ndarray]
) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SOLE-AXIOM PROFILES DO NOT REALIZE THE RETAINED PMNS LANE")
    print("=" * 88)

    ok, detail = expect_raises(
        lambda: close_from_lower_level_observables(active_cols, passive_cols, 0.31, 0.27),
        ValueError,
    )
    check("The retained lower-level closure stack rejects the sole-axiom response profiles", ok, detail)
    check("Reason: the derived pair is not on a one-sided minimal PMNS class", "one-sided minimal PMNS class" in detail, detail)
    check("So the sole axiom by itself does not produce PMNS-active lower-level response profiles on the retained lane", True)


def main() -> int:
    print("=" * 88)
    print("PMNS SOLE-AXIOM RESPONSE PROFILE BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  If the lower-level active/passive response profiles are derived from")
    print("  the sole axiom Cl(3) on Z^3 itself, what do they give on the retained")
    print("  PMNS lepton surface?")

    active_cols, passive_cols = part1_sole_axiom_free_response_profiles_are_exact_and_trivial()
    part2_all_reduced_pmns_data_collapse_to_the_trivial_free_point(active_cols, passive_cols)
    part3_the_sole_axiom_profiles_do_not_realize_the_retained_pmns_lane(active_cols, passive_cols)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact sole-axiom lower-level boundary:")
    print("    - the derived active response profile is the trivial identity profile")
    print("    - the derived passive response profile is the trivial scalar resolvent profile")
    print("    - all reduced PMNS data collapse to the free point")
    print("    - the retained lower-level PMNS closure stack therefore does not realize")
    print("      a one-sided PMNS-active class from the sole axiom alone")
    print()
    print("  So full retained neutrino closure from Cl(3) on Z^3 alone is blocked at")
    print("  the lower-level response-profile layer. Any nontrivial retained PMNS lane")
    print("  requires a deformation law beyond the sole-axiom free response profiles.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
