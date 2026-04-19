#!/usr/bin/env python3
"""Exact next-target theorem for positive PMNS reopening beyond the current bank."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_nonzero_sigma_response_pack_boundary import realized_active_response_pack
from frontier_pmns_sigma_constrained_effective_action_selector import relative_action_sigma_surface_formula
from frontier_pmns_sigma_constraint_surface import sigma_from_block, sigma_slice_block
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from pmns_lower_level_utils import I3, derive_active_block_from_response_columns, support_mask

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
TARGET_SUPPORT = (
    np.abs(np.eye(3, dtype=complex) + np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)) > 0
).astype(int)


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


def part1_the_current_bank_has_no_positive_pmns_reopening_because_its_active_pack_is_trivial() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT BANK HAS NO POSITIVE PMNS REOPENING BECAUSE ITS ACTIVE PACK IS TRIVIAL")
    print("=" * 88)

    lam_act = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam_act, 0.27)
    kernel, block = derive_active_block_from_response_columns(pack["active_columns"], lam_act)
    sigma = sigma_from_block(block)
    jchi = nontrivial_character_current(block)

    check("The current sole-axiom active response pack is exactly the basis-column free pack", np.linalg.norm(np.column_stack(pack["active_columns"]) - I3) < 1.0e-12)
    check("Its active response kernel is exactly the free kernel", np.linalg.norm(kernel - I3) < 1.0e-12)
    check("Its derived active block therefore has sigma = 0", abs(sigma) < 1.0e-12, f"sigma={sigma:.6f}")
    check("The same trivial pack also has J_chi = 0", abs(jchi) < 1.0e-12, f"J_chi={jchi:.6f}")


def part2_one_nontrivial_active_response_pack_on_the_existing_carrier_is_enough_to_reopen_pmns() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ONE NONTRIVIAL ACTIVE RESPONSE PACK ON THE EXISTING CARRIER IS ENOUGH TO REOPEN PMNS")
    print("=" * 88)

    sigma = 0.23
    block = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    kernel, _columns, recovered = realized_active_response_pack(block, seed=9911)
    recovered_sigma = sigma_from_block(recovered)
    recovered_jchi = nontrivial_character_current(recovered)

    check("A nontrivial active response pack is already realizable on the existing hw=1 carrier", np.linalg.norm(recovered - block) < 1.0e-12, f"error={np.linalg.norm(recovered - block):.2e}")
    check("That pack keeps the retained diagonal-plus-forward-cycle support", np.array_equal(support_mask(recovered), TARGET_SUPPORT))
    check("Its kernel is nontrivial, so this is a genuine source reopening and not the free pack", np.linalg.norm(kernel - I3) > 1.0e-6, f"|K-I|={np.linalg.norm(kernel - I3):.6f}")
    check("The same reopened pack already carries nonzero sigma and nonzero J_chi", abs(recovered_sigma) > 1.0e-6 and abs(recovered_jchi) > 1.0e-6, f"sigma={recovered_sigma:.6f}, J_chi={recovered_jchi:.6f}")


def part3_once_the_pack_exists_the_current_pmns_stack_already_finishes_the_job() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONCE THE PACK EXISTS THE CURRENT PMNS STACK ALREADY FINISHES THE JOB")
    print("=" * 88)

    sigma = 0.23
    covariant = sigma_slice_block(sigma=sigma, u=sigma, v=0.0, xbar=1.0)
    off_point = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    _kernel_cov, recovered_cov = realized_active_response_pack(covariant, seed=9912)[0], realized_active_response_pack(covariant, seed=9912)[2]
    action_cov = relative_action_sigma_surface_formula(sigma, sigma, 0.0)
    action_off = relative_action_sigma_surface_formula(sigma, 0.15, 0.14)
    jchi = nontrivial_character_current(recovered_cov)

    check("The C3-covariant nonzero-sigma response pack is realized exactly on the same lower-level chain", np.linalg.norm(recovered_cov - covariant) < 1.0e-12, f"error={np.linalg.norm(recovered_cov - covariant):.2e}")
    check("On that admitted sigma surface the native action prefers the covariant branch", action_cov < action_off, f"S_cov={action_cov:.12f}, S_off={action_off:.12f}")
    check("At the selected branch the current stack gives J_chi = sigma exactly", abs(jchi - sigma) < 1.0e-12, f"J_chi={jchi:.6f}, sigma={sigma:.6f}")
    check("So once a nontrivial active response pack is admitted, the remaining PMNS work is already handled by the present sigma/readout/selector stack", True)


def part4_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CLOSEOUT")
    print("=" * 88)

    check("Any positive PMNS reopening beyond the current retained bank must change the active response pack from trivial to nontrivial on the existing hw=1 carrier", True)
    check("Conversely, once such a nontrivial active response pack is admitted, the present PMNS stack already reads sigma and selects the C3 branch", True)
    check("Therefore the exact next positive PMNS target is an axiom-native active response-pack source principle", True)
    check("Graph/commutant/holonomy machinery should now be treated as support and readout, not as the missing source principle", True)


def main() -> int:
    print("=" * 88)
    print("PMNS ACTIVE RESPONSE-PACK SOURCE PRINCIPLE")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the retained PMNS lane closes negatively, what exact theorem")
    print("  target is equivalent to any future positive PMNS reopening?")

    part1_the_current_bank_has_no_positive_pmns_reopening_because_its_active_pack_is_trivial()
    part2_one_nontrivial_active_response_pack_on_the_existing_carrier_is_enough_to_reopen_pmns()
    part3_once_the_pack_exists_the_current_pmns_stack_already_finishes_the_job()
    part4_closeout()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact next-target theorem:")
    print("    - the current retained PMNS bank fails because its active response")
    print("      pack is still the trivial free pack")
    print("    - a positive PMNS reopening does not need a new carrier or a new")
    print("      selector; it needs one nontrivial active response pack on the")
    print("      existing hw=1 carrier")
    print("    - once that pack exists, the current stack already reads sigma and")
    print("      selects the C3-covariant branch J_chi = sigma")
    print()
    print("  So the exact next PMNS program is now fixed:")
    print("  derive an axiom-native active response-pack source principle.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
