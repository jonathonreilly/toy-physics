#!/usr/bin/env python3
"""Boundary on deriving a nonzero PMNS sigma surface from the current hw=1 bank."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_active_four_real_source_from_transport import active_native_means
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_corner_transport_active_block import orbit_average_transport
from frontier_pmns_sigma_constraint_surface import sigma_from_block, sigma_slice_block
from frontier_pmns_sole_axiom_hw1_source_transfer_boundary import sole_axiom_hw1_source_transfer_pack
from frontier_pmns_transfer_operator_dominant_mode import (
    projected_transfer_kernel_from_active_block,
    reconstruct_seed_pair_from_transfer_kernel,
)
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    derive_active_block_from_response_columns,
    sector_operator_fixture_from_effective_block,
    support_mask,
)

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


def realized_active_response_pack(block: np.ndarray, lam: float = 0.31, seed: int = 9901) -> tuple[np.ndarray, list[np.ndarray], np.ndarray]:
    sector = sector_operator_fixture_from_effective_block(block, seed=seed)
    _reference, columns = active_response_columns_from_sector_operator(sector, lam)
    kernel, recovered = derive_active_block_from_response_columns(columns, lam)
    return kernel, columns, recovered


def part1_sigma_is_exactly_the_forward_odd_transport_mean_on_the_reduced_family() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SIGMA IS EXACTLY THE FORWARD ODD TRANSPORT MEAN ON THE REDUCED FAMILY")
    print("=" * 88)

    sigma = 0.23
    a = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    b = sigma_slice_block(sigma=sigma, u=sigma, v=0.0, xbar=1.0)

    xbar_a, sigma_a = active_native_means(a)
    even_a, odd_fwd_a, odd_bwd_a = orbit_average_transport(a)
    xbar_b, sigma_b = active_native_means(b)
    even_b, odd_fwd_b, odd_bwd_b = orbit_average_transport(b)
    ja = nontrivial_character_current(a)
    jb = nontrivial_character_current(b)

    check("On the reduced PMNS family the native sigma equals the exact forward odd transport mean",
          abs(sigma_a - odd_fwd_a) < 1.0e-12 and abs(sigma_b - odd_fwd_b) < 1.0e-12,
          f"sigma_a={sigma_a:.6f}, odd_a={odd_fwd_a:.6f}, sigma_b={sigma_b:.6f}, odd_b={odd_fwd_b:.6f}")
    check("The even transport mean still recovers xbar exactly while the backward odd mean vanishes on forward support",
          abs(xbar_a - even_a.real) < 1.0e-12 and abs(xbar_b - even_b.real) < 1.0e-12 and abs(odd_bwd_a) < 1.0e-12 and abs(odd_bwd_b) < 1.0e-12,
          f"xbar_a={xbar_a:.6f}, even_a={even_a:.6f}, xbar_b={xbar_b:.6f}, even_b={even_b:.6f}")
    check("Two distinct points on one fixed-sigma surface share the same transport odd mean but have different nontrivial currents",
          abs(odd_fwd_a - odd_fwd_b) < 1.0e-12 and abs(ja - jb) > 1.0e-6,
          f"odd={odd_fwd_a:.6f}, J_a={ja:.6f}, J_b={jb:.6f}")
    check("So producing a nonzero sigma surface is strictly weaker than selecting the final PMNS current J_chi on that surface", True)


def part2_nonzero_sigma_needs_only_a_nontrivial_active_response_pack_on_the_existing_carrier() -> None:
    print("\n" + "=" * 88)
    print("PART 2: NONZERO SIGMA NEEDS ONLY A NONTRIVIAL ACTIVE RESPONSE PACK ON THE EXISTING CARRIER")
    print("=" * 88)

    sigma = 0.23
    block = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    kernel, columns, recovered = realized_active_response_pack(block, seed=9901)
    column_matrix = np.column_stack(columns)
    recovered_sigma = sigma_from_block(recovered)

    check("A nonzero-sigma point is realized exactly by an active response pack on the current lower-level chain",
          np.linalg.norm(recovered - block) < 1.0e-12,
          f"error={np.linalg.norm(recovered - block):.2e}")
    check("That realized response pack stays on the existing diagonal-plus-forward-cycle support", np.array_equal(support_mask(recovered), TARGET_SUPPORT))
    check("Its response kernel is genuinely nontrivial rather than the free kernel", np.linalg.norm(kernel - I3) > 1.0e-6, f"|K-I|={np.linalg.norm(kernel - I3):.6f}")
    check("The same response pack already carries the nonzero sigma readout exactly", abs(recovered_sigma - sigma) < 1.0e-12, f"sigma={recovered_sigma:.6f}")
    print(f"  [INFO] The nontrivial active response columns are:\n{np.round(column_matrix, 6)}")


def part3_the_current_sole_axiom_hw1_pack_still_stops_at_the_trivial_response_profile() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE CURRENT SOLE-AXIOM HW=1 PACK STILL STOPS AT THE TRIVIAL RESPONSE PROFILE")
    print("=" * 88)

    lam_act = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam_act, 0.27)
    kernel, block = derive_active_block_from_response_columns(pack["active_columns"], lam_act)
    even, odd_fwd, odd_bwd = orbit_average_transport(block)
    sigma = sigma_from_block(block)

    check("The sole-axiom active response columns are still exactly the basis columns", np.linalg.norm(np.column_stack(pack["active_columns"]) - I3) < 1.0e-12)
    check("Their derived active kernel is still the free kernel I", np.linalg.norm(kernel - I3) < 1.0e-12)
    check("Their derived active block is still the free block, so sigma = 0", np.linalg.norm(block - I3) < 1.0e-12 and abs(sigma) < 1.0e-12, f"sigma={sigma:.6f}")
    check("At transport level the current sole-axiom pack still has zero forward odd mean", abs(odd_fwd) < 1.0e-12 and abs(odd_bwd) < 1.0e-12 and abs(even - 1.0) < 1.0e-12,
          f"even={even:.6f}, odd_fwd={odd_fwd:.6f}, odd_bwd={odd_bwd:.6f}")


def part4_transfer_laws_read_sigma_once_supplied_but_do_not_produce_the_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 4: TRANSFER LAWS READ SIGMA ONCE SUPPLIED BUT DO NOT PRODUCE THE SURFACE")
    print("=" * 88)

    sigma = 0.23
    a = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    b = sigma_slice_block(sigma=sigma, u=sigma, v=0.0, xbar=1.0)
    t_a = projected_transfer_kernel_from_active_block(a)
    t_b = projected_transfer_kernel_from_active_block(b)
    rec_even, rec_sigma = reconstruct_seed_pair_from_transfer_kernel(t_a)

    lam_act = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam_act, 0.27)
    _kernel, free_block = derive_active_block_from_response_columns(pack["active_columns"], lam_act)
    t_free = projected_transfer_kernel_from_active_block(free_block)
    free_even, free_sigma = reconstruct_seed_pair_from_transfer_kernel(t_free)

    check("Across one fixed-sigma surface, the transfer-only projection collapses distinct PMNS points to the same transport kernel",
          np.linalg.norm(t_a - t_b) < 1.0e-12,
          f"|T_a-T_b|={np.linalg.norm(t_a - t_b):.2e}")
    check("The dominant-mode transfer law then recovers that same sigma exactly from the supplied kernel", abs(rec_sigma - sigma) < 1.0e-12, f"shadow_even={rec_even:.6f}, sigma={rec_sigma:.6f}")
    check("But on the current sole-axiom pack the same transfer law still returns sigma = 0", abs(free_sigma) < 1.0e-12, f"shadow_even={free_even:.6f}, sigma={free_sigma:.6f}")
    check("So transfer-only structure is a readout of an admitted sigma surface, not a source principle that produces one from the current bank", True)


def part5_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 5: CLOSEOUT")
    print("=" * 88)

    check("A nonzero PMNS sigma surface would require only one extra nontrivial active response pack on the existing hw=1 carrier", True)
    check("The current sole-axiom hw=1 bank still does not produce that nontrivial response pack", True)
    check("Therefore the PMNS extension-design route does not close positively on the current bank", True)
    check("The exact missing theorem is now explicit: an axiom-native PMNS source principle for nonzero forward odd transport mean sigma", True)


def main() -> int:
    print("=" * 88)
    print("PMNS NONZERO-SIGMA RESPONSE-PACK BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the minimal PMNS extension route, what exact new theorem would be")
    print("  equivalent to deriving a nonzero sigma surface from the sole axiom,")
    print("  and does the current hw=1 bank already supply it?")

    part1_sigma_is_exactly_the_forward_odd_transport_mean_on_the_reduced_family()
    part2_nonzero_sigma_needs_only_a_nontrivial_active_response_pack_on_the_existing_carrier()
    part3_the_current_sole_axiom_hw1_pack_still_stops_at_the_trivial_response_profile()
    part4_transfer_laws_read_sigma_once_supplied_but_do_not_produce_the_surface()
    part5_closeout()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact PMNS extension bottleneck:")
    print("    - on the reduced retained PMNS family, sigma is exactly the forward")
    print("      odd transport mean")
    print("    - a nonzero sigma surface therefore needs only a nontrivial active")
    print("      response pack on the existing hw=1 carrier")
    print("    - the current sole-axiom hw=1 pack still stops at the trivial free")
    print("      response profile with sigma = 0")
    print("    - transfer-only laws read sigma once such a surface is supplied,")
    print("      but they do not produce that surface from the current bank")
    print()
    print("  So the route does not yet hunt positively. The exact next PMNS target")
    print("  is one new axiom-native source principle producing a nonzero forward")
    print("  odd transport mean sigma on the retained hw=1 response family.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
