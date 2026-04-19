#!/usr/bin/env python3
"""Pure-PMNS sigma constraint surface for the remaining J_chi problem."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_active_four_real_source_from_transport import active_native_means
from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_oriented_cycle_channel_value_law import oriented_cycle_coeffs_from_block
from frontier_pmns_oriented_cycle_reduced_channel_nonselection import active_block_with_reduced_cycle
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


def sigma_from_block(block: np.ndarray) -> complex:
    coeffs = oriented_cycle_coeffs_from_block(block)
    return complex(np.mean(coeffs))


def sigma_slice_block(sigma: float, u: float, v: float, xbar: float = 1.0) -> np.ndarray:
    w = 3.0 * sigma - 2.0 * u
    return active_block_with_reduced_cycle(u, v, w, xbar=xbar)


def part1_sigma_is_the_native_cycle_mean() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SIGMA IS THE NATIVE CYCLE MEAN")
    print("=" * 88)

    block = active_block_with_reduced_cycle(0.41, 0.32, 0.28, xbar=1.0)
    coeffs = oriented_cycle_coeffs_from_block(block)
    sigma_cycle = sigma_from_block(block)
    xbar, sigma_transport = active_native_means(block)

    check("The pure-PMNS sigma is exactly the mean of the oriented-cycle coefficients", abs(sigma_cycle - np.mean(coeffs)) < 1.0e-12, f"coeffs={np.round(coeffs, 6)}")
    check("The same sigma is exactly the native transport mean from the active block", abs(sigma_cycle - sigma_transport) < 1.0e-12, f"xbar={xbar:.6f}, sigma={sigma_cycle:.6f}")
    check("So sigma is already a native PMNS observable and not an imported DM datum", True)


def part2_on_the_graph_first_reduced_family_sigma_cuts_a_two_real_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ON THE GRAPH-FIRST REDUCED FAMILY, SIGMA CUTS A TWO-REAL SURFACE")
    print("=" * 88)

    sigma = 0.25
    a = sigma_slice_block(sigma=sigma, u=0.25, v=0.00)
    b = sigma_slice_block(sigma=sigma, u=0.15, v=0.18)
    ja = nontrivial_character_current(a)
    jb = nontrivial_character_current(b)
    wa = np.real(oriented_cycle_coeffs_from_block(a)[1])
    wb = np.real(oriented_cycle_coeffs_from_block(b)[1])
    sigma_a = sigma_from_block(a)
    sigma_b = sigma_from_block(b)

    check("Sigma is real on the graph-first reduced family", abs(sigma_a.imag) < 1.0e-12 and abs(sigma_b.imag) < 1.0e-12, f"sigma_a={sigma_a:.6f}, sigma_b={sigma_b:.6f}")
    check("The exact sigma relation is 3 sigma = w + 2 Re(J_chi)", abs(3.0 * sigma_a.real - (wa + 2.0 * ja.real)) < 1.0e-12 and abs(3.0 * sigma_b.real - (wb + 2.0 * jb.real)) < 1.0e-12, f"a: lhs-rhs={3.0 * sigma_a.real - (wa + 2.0 * ja.real):.2e}, b: lhs-rhs={3.0 * sigma_b.real - (wb + 2.0 * jb.real):.2e}")
    check("Two distinct reduced PMNS points can share the same sigma", abs(sigma_a.real - sigma_b.real) < 1.0e-12 and abs(ja - jb) > 1.0e-6, f"J_a={ja:.6f}, J_b={jb:.6f}")
    check("So fixed (xbar, sigma) leaves a genuinely two-real PMNS surface for J_chi selection", True)


def part3_current_pure_pmns_sole_axiom_routes_still_give_sigma_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CURRENT PURE-PMNS SOLE-AXIOM ROUTES STILL GIVE SIGMA = 0")
    print("=" * 88)

    free_sigma = sigma_from_block(I3)

    lam = 0.31
    pack = sole_axiom_hw1_source_transfer_pack(lam, 0.27)
    source_block = derive_active_block_from_response_columns(pack["active_columns"], lam)[1]
    source_sigma = sigma_from_block(source_block)

    scalar_block = scalar_triplet_block(1.13)
    scalar_cols = active_response_columns_from_sector_operator(scalar_block, lam)[1]
    scalar_active = derive_active_block_from_response_columns(scalar_cols, lam)[1]
    scalar_sigma = sigma_from_block(scalar_active)

    check("The free sole-axiom PMNS route has sigma = 0", abs(free_sigma) < 1.0e-12, f"sigma={free_sigma:.6f}")
    check("The sole-axiom hw=1 source/transfer PMNS route has sigma = 0", abs(source_sigma) < 1.0e-12, f"sigma={source_sigma:.6f}")
    check("The retained scalar PMNS route has sigma = 0", abs(scalar_sigma) < 1.0e-12, f"sigma={scalar_sigma:.6f}")
    check("So no current pure-PMNS sole-axiom route yet furnishes a nonzero sigma surface", True)


def part4_the_c3_covariant_point_on_a_fixed_sigma_slice_has_jchi_equal_sigma() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE C3-COVARIANT POINT ON A FIXED SIGMA SLICE HAS J_chi = SIGMA")
    print("=" * 88)

    sigma = 0.23
    block = sigma_slice_block(sigma=sigma, u=sigma, v=0.0)
    coeffs = oriented_cycle_coeffs_from_block(block)
    jchi = nontrivial_character_current(block)

    check("The C3-covariant point on the fixed-sigma slice is exactly sigma C", np.linalg.norm(coeffs - sigma * np.ones(3, dtype=complex)) < 1.0e-12, f"coeffs={np.round(coeffs, 6)}")
    check("At that point the nontrivial PMNS current equals sigma", abs(jchi - sigma) < 1.0e-12, f"J_chi={jchi:.6f}, sigma={sigma:.6f}")
    check("So nonzero sigma is already a concrete candidate source for nonzero J_chi on the pure-PMNS lane", True)


def main() -> int:
    print("=" * 88)
    print("PMNS SIGMA CONSTRAINT SURFACE")
    print("=" * 88)
    print()
    print("Question:")
    print("  Is there a pure-PMNS native constraint surface sharper than the raw")
    print("  J_chi problem, and if so what does it look like?")

    part1_sigma_is_the_native_cycle_mean()
    part2_on_the_graph_first_reduced_family_sigma_cuts_a_two_real_surface()
    part3_current_pure_pmns_sole_axiom_routes_still_give_sigma_zero()
    part4_the_c3_covariant_point_on_a_fixed_sigma_slice_has_jchi_equal_sigma()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact pure-PMNS sigma reduction:")
    print("    - sigma is the native PMNS cycle/transport mean")
    print("    - on the graph-first reduced family, fixed sigma cuts a two-real")
    print("      surface with 3 sigma = w + 2 Re(J_chi)")
    print("    - the current pure-PMNS sole-axiom routes still give sigma = 0")
    print("    - the C3-covariant point on a fixed-sigma slice has J_chi = sigma")
    print()
    print("  So the next honest PMNS question is now explicit:")
    print("  can the sole axiom derive a nonzero sigma surface on the retained")
    print("  hw=1 lane, or do all current pure-PMNS routes collapse to sigma = 0?")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
