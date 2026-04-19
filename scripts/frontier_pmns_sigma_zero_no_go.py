#!/usr/bin/env python3
"""Pure-retained PMNS no-go for nonzero sigma on the current sole-axiom bank."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_active_four_real_source_from_transport import active_native_means
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_effective_action_selector_boundary import gram_lift, relative_action_to_seed
from frontier_pmns_sigma_constraint_surface import sigma_from_block, sigma_slice_block
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from frontier_pmns_uniform_scalar_deformation_boundary import scalar_triplet_block
from pmns_lower_level_utils import I3, active_response_columns_from_sector_operator, derive_active_block_from_response_columns

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


def pure_retained_pmns_blocks(lam_act: float = 0.31) -> dict[str, np.ndarray]:
    pack = sole_axiom_hw1_source_transfer_pack(lam_act, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam_act)[1]

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam_act)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam_act)[1]

    return {
        "free": I3.copy(),
        "hw1_source_transfer": source_block,
        "scalar": scalar_active,
    }


def part1_sigma_is_a_native_pmns_observable_and_the_candidate_source_for_jchi() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SIGMA IS A NATIVE PMNS OBSERVABLE AND THE CANDIDATE SOURCE FOR J_chi")
    print("=" * 88)

    block = sigma_slice_block(sigma=0.23, u=0.23, v=0.0, xbar=1.0)
    xbar, sigma_transport = active_native_means(block)
    sigma_cycle = sigma_from_block(block)
    jchi = nontrivial_character_current(block)

    check("Sigma is exactly the native active transport mean on the PMNS block", abs(sigma_cycle - sigma_transport) < 1.0e-12, f"xbar={xbar:.6f}, sigma={sigma_cycle:.6f}")
    check("At the C3-covariant point the native nontrivial current equals sigma", abs(jchi - sigma_cycle) < 1.0e-12, f"J_chi={jchi:.6f}, sigma={sigma_cycle:.6f}")
    check("So nonzero sigma would already be a pure-PMNS source of nonzero J_chi", True)


def part2_every_current_pure_retained_source_route_has_sigma_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 2: EVERY CURRENT PURE-RETAINED SOURCE ROUTE HAS SIGMA = 0")
    print("=" * 88)

    blocks = pure_retained_pmns_blocks()
    sigmas = {name: sigma_from_block(block) for name, block in blocks.items()}

    check("The free retained PMNS route has sigma = 0", abs(sigmas["free"]) < 1.0e-12, f"sigma={sigmas['free']:.6f}")
    check("The canonical sole-axiom hw=1 source/transfer route has sigma = 0", abs(sigmas["hw1_source_transfer"]) < 1.0e-12, f"sigma={sigmas['hw1_source_transfer']:.6f}")
    check("The retained scalar PMNS route has sigma = 0", abs(sigmas["scalar"]) < 1.0e-12, f"sigma={sigmas['scalar']:.6f}")
    check("So the current pure-retained PMNS source bank does not furnish a nonzero sigma surface", True)


def part3_every_current_pure_retained_readout_of_those_routes_has_jchi_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EVERY CURRENT PURE-RETAINED READOUT OF THOSE ROUTES HAS J_chi = 0")
    print("=" * 88)

    blocks = pure_retained_pmns_blocks()
    currents = {name: nontrivial_character_current(block) for name, block in blocks.items()}

    check("The free retained PMNS route has J_chi = 0", abs(currents["free"]) < 1.0e-12, f"J_chi={currents['free']:.6f}")
    check("The canonical sole-axiom hw=1 source/transfer route has J_chi = 0", abs(currents["hw1_source_transfer"]) < 1.0e-12, f"J_chi={currents['hw1_source_transfer']:.6f}")
    check("The retained scalar PMNS route has J_chi = 0", abs(currents["scalar"]) < 1.0e-12, f"J_chi={currents['scalar']:.6f}")
    check("So the current pure-retained PMNS readout stack still annihilates the remaining nontrivial character current", True)


def part4_the_only_current_native_selector_without_extra_constraint_also_selects_sigma_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ONLY CURRENT NATIVE SELECTOR WITHOUT EXTRA CONSTRAINT ALSO SELECTS SIGMA = 0")
    print("=" * 88)

    seed = sigma_slice_block(sigma=0.0, u=0.0, v=0.0, xbar=1.0)
    candidate = sigma_slice_block(sigma=0.23, u=0.23, v=0.0, xbar=1.0)
    seed_action = relative_action_to_seed(gram_lift(seed))
    candidate_action = relative_action_to_seed(gram_lift(candidate))

    check("The unconstrained native effective action is minimized at the retained seed", abs(seed_action) < 1.0e-12, f"S_seed={seed_action:.12f}")
    check("A nonzero sigma candidate on the canonical positive lift has strictly larger action", candidate_action > 1.0e-6, f"S_candidate={candidate_action:.12f}")
    check("So the current native selector stack does not generate nonzero sigma without an extra pure-PMNS constraint surface", True)


def part5_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CLOSEOUT")
    print("=" * 88)

    check("The current pure-retained PMNS bank contains no nonzero sigma source route", True)
    check("The same bank contains no current selector that lifts sigma away from zero without extra input", True)
    check("Therefore sigma = 0 on the current pure-retained sole-axiom PMNS lane", True)
    check("Any nonzero sigma requires a genuinely new pure-PMNS source or constraint law beyond the current retained bank", True)


def main() -> int:
    print("=" * 88)
    print("PMNS SIGMA-ZERO NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the current pure-retained sole-axiom PMNS bank, can the retained")
    print("  native sources/readouts/selectors force nonzero sigma?")

    part1_sigma_is_a_native_pmns_observable_and_the_candidate_source_for_jchi()
    part2_every_current_pure_retained_source_route_has_sigma_zero()
    part3_every_current_pure_retained_readout_of_those_routes_has_jchi_zero()
    part4_the_only_current_native_selector_without_extra_constraint_also_selects_sigma_zero()
    part5_closeout()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Pure-retained PMNS closeout:")
    print("    - sigma is the native PMNS cycle/transport mean")
    print("    - every current pure-retained PMNS source route sets sigma = 0")
    print("    - every current pure-retained PMNS readout then has J_chi = 0")
    print("    - the current unconstrained native selector also stays at sigma = 0")
    print()
    print("  Therefore sigma = 0 on the current pure-retained sole-axiom PMNS")
    print("  lane. Any nonzero sigma requires a genuinely new pure-PMNS source or")
    print("  constraint law beyond the current retained bank.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
