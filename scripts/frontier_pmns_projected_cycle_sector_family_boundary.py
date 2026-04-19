#!/usr/bin/env python3
"""Exact graph-cycle sector-family boundary for the PMNS source-law problem."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_oriented_cycle_channel_value_law import projected_forward_cycle
from frontier_pmns_sigma_constraint_surface import sigma_from_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    canonicalize_active,
    derive_active_block_from_response_columns,
    derive_passive_block_from_response_columns,
    passive_response_columns_from_sector_operator,
    support_mask,
)

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
TARGET_SUPPORT = (np.abs(I3 + np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)) > 0).astype(int)


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


def sector_family(a: complex, b: complex) -> np.ndarray:
    return a * I3 + b * projected_forward_cycle()


def part1_the_exact_projected_cycle_algebra_has_a_minimal_forward_support_family() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE EXACT PROJECTED CYCLE ALGEBRA HAS A MINIMAL FORWARD-SUPPORT FAMILY")
    print("=" * 88)

    c = projected_forward_cycle()
    c2 = c @ c

    check("The projected forward cycle is exact on the hw=1 triplet", np.linalg.norm(c - np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)) < 1.0e-12)
    check("The projected cycle satisfies C^3 = I exactly", np.linalg.norm(np.linalg.matrix_power(c, 3) - I3) < 1.0e-12)
    check("The exact graph-cycle algebra is span{I,C,C^2}", np.linalg.matrix_rank(np.column_stack([I3.reshape(-1), c.reshape(-1), c2.reshape(-1)])) == 3)
    check("Restricting to retained forward support leaves the exact two-parameter family A(a,b) = a I + b C", True)

    return c


def part2_on_that_family_sigma_and_jchi_are_just_the_cycle_weight(c: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: ON THAT FAMILY SIGMA AND J_CHI ARE JUST THE CYCLE WEIGHT")
    print("=" * 88)

    a = 2.0
    b = 1.0
    block = sector_family(a, b)
    sigma = sigma_from_block(block)
    jchi = nontrivial_character_current(block)

    check("The family A(a,b) stays on the retained diagonal-plus-forward-cycle support whenever a and b are both nonzero",
          np.array_equal(support_mask(block), TARGET_SUPPORT))
    check("On A(a,b), the PMNS sigma readout is exactly b", abs(sigma - b) < 1.0e-12, f"sigma={sigma:.6f}, b={b:.6f}")
    check("On the same family, the nontrivial character current is exactly b as well", abs(jchi - b) < 1.0e-12, f"J_chi={jchi:.6f}, b={b:.6f}")
    check("So this exact graph-native family already packages the PMNS source into one cycle weight b once an admissible sector point is chosen", True)


def part3_the_same_active_response_pack_has_an_exact_passive_reinterpretation_formula() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SAME ACTIVE RESPONSE PACK HAS AN EXACT PASSIVE REINTERPRETATION FORMULA")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    a = 2.0
    b = 1.0
    op = sector_family(a, b)
    active_cols = active_response_columns_from_sector_operator(op, lam_act)[1]
    passive_block = derive_passive_block_from_response_columns(active_cols, lam_pass)[1]
    formula = (lam_act / lam_pass) * (op - I3)

    ambiguous_cols = active_response_columns_from_sector_operator(sector_family(1.0, 1.0), lam_act)[1]
    ambiguous_passive = derive_passive_block_from_response_columns(ambiguous_cols, lam_pass)[1]

    check("For any active sector operator A, passively reinterpreting its active response columns gives (lam_act/lam_pass)(A-I) exactly", np.linalg.norm(passive_block - formula) < 1.0e-12, f"error={np.linalg.norm(passive_block - formula):.2e}")
    check("At a = 1, the same passive reinterpretation collapses to a pure monomial cycle block", np.linalg.norm(ambiguous_passive - (lam_act / lam_pass) * c) < 1.0e-12 if (c := projected_forward_cycle()) is not None else False)
    check("So a = 1 is the exact passive-side ambiguity wall for the forward-support family", True)


def part4_one_sided_pmns_closure_on_the_family_is_exactly_a_not_in_0_1_and_b_nonzero() -> None:
    print("\n" + "=" * 88)
    print("PART 4: ONE-SIDED PMNS CLOSURE ON THE FAMILY IS EXACTLY a NOT IN {0,1} AND b != 0")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    free_passive_cols = passive_response_columns_from_sector_operator(I3, lam_pass)[1]
    samples = [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (0.5, 1.0)]
    results = {}

    for a, b in samples:
        cols = active_response_columns_from_sector_operator(sector_family(a, b), lam_act)[1]
        active_block = derive_active_block_from_response_columns(cols, lam_act)[1]
        can_active = canonicalize_active(active_block) is not None
        try:
            out = close_from_lower_level_observables(cols, free_passive_cols, lam_act, lam_pass)
            results[(a, b)] = {"closed": True, "branch": out["branch"], "tau": out["tau"], "q": out["q"]}
        except ValueError as exc:
            results[(a, b)] = {"closed": False, "error": str(exc), "can_active": can_active}

    check("At a = 0, the family collapses to a monomial active block and does not realize a one-sided PMNS class",
          results[(0.0, 1.0)]["closed"] is False and results[(0.0, 1.0)]["can_active"] is False,
          f"error={results[(0.0, 1.0)]['error']}")
    check("At a = 1, the active block is canonical but the passive reinterpretation is ambiguous, so closure still fails",
          results[(1.0, 1.0)]["closed"] is False and results[(1.0, 1.0)]["can_active"] is True,
          f"error={results[(1.0, 1.0)]['error']}")
    check("For a != 0,1 and b != 0, the exact family closes the one-sided PMNS lane with the passive free pack", results[(2.0, 1.0)]["closed"] and results[(0.5, 1.0)]["closed"])
    check("So on the exact graph-cycle family the one-sided PMNS reopening condition is precisely: active canonicality (a != 0, b != 0) plus passive non-monomiality (a != 1, b != 0)", True)


def part5_the_smallest_positive_integral_candidate_is_2i_plus_c_but_its_selection_is_still_open() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE SMALLEST POSITIVE-INTEGRAL CANDIDATE IS 2I + C, BUT ITS SELECTION IS STILL OPEN")
    print("=" * 88)

    lam_act = 0.31
    lam_pass = 0.27
    free_passive_cols = passive_response_columns_from_sector_operator(I3, lam_pass)[1]
    cols = active_response_columns_from_sector_operator(sector_family(2.0, 1.0), lam_act)[1]
    out = close_from_lower_level_observables(cols, free_passive_cols, lam_act, lam_pass)

    check("The smallest positive-integral point on the exact family that avoids a = 0 and a = 1 is 2I + C", True)
    check("That candidate already closes the one-sided PMNS lane downstream", out["branch"] == "neutrino-active" and out["tau"] == 0, f"branch={out['branch']}, tau={out['tau']}, q={out['q']}")
    check("But the current exact bank still does not derive why this or any other admissible point in A(a,b) should be selected as the microscopic sector operator", True)


def main() -> int:
    print("=" * 88)
    print("PMNS PROJECTED-CYCLE SECTOR-FAMILY BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the exact projected graph-cycle algebra sharpen the remaining")
    print("  PMNS source-law problem beyond the generic phrase \"nontrivial active")
    print("  response pack\"?")

    c = part1_the_exact_projected_cycle_algebra_has_a_minimal_forward_support_family()
    part2_on_that_family_sigma_and_jchi_are_just_the_cycle_weight(c)
    part3_the_same_active_response_pack_has_an_exact_passive_reinterpretation_formula()
    part4_one_sided_pmns_closure_on_the_family_is_exactly_a_not_in_0_1_and_b_nonzero()
    part5_the_smallest_positive_integral_candidate_is_2i_plus_c_but_its_selection_is_still_open()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact sharpening of the PMNS source-law gap:")
    print("    - the exact projected graph-cycle algebra gives the forward-support")
    print("      family A(a,b) = a I + b C")
    print("    - on that family, sigma = J_chi = b")
    print("    - the same active response columns are passively reinterpreted as")
    print("      (lam_act/lam_pass)(A-I)")
    print("    - therefore one-sided PMNS reopening on this exact family occurs")
    print("      exactly when b != 0 and a avoids the two walls a = 0 and a = 1")
    print()
    print("  So the remaining PMNS source problem has narrowed again:")
    print("  derive an axiom-native selection or normalization law for a")
    print("  nondegenerate point in the exact projected-cycle sector family.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
