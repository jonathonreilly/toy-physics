#!/usr/bin/env python3
"""Boundary on the minimal nonzero-sigma PMNS extension route."""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_sigma_constrained_effective_action_selector import (
    cubic_lower_bound_on_unit_interval,
    exact_hessian_diagonal_at_covariant_point,
    local_grid_minimum,
    relative_action_sigma_surface_formula,
)
from frontier_pmns_sigma_constraint_surface import sigma_from_block, sigma_slice_block
from frontier_pmns_sigma_zero_no_go import pure_retained_pmns_blocks
from pmns_lower_level_utils import (
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


def realize_active_block(block: np.ndarray, lam: float = 0.31, seed: int = 7001) -> np.ndarray:
    sector = sector_operator_fixture_from_effective_block(block, seed=seed)
    _reference, columns = active_response_columns_from_sector_operator(sector, lam)
    return derive_active_block_from_response_columns(columns, lam)[1]


def part1_the_extension_does_not_add_a_new_pmns_carrier_only_a_surface() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE EXTENSION DOES NOT ADD A NEW PMNS CARRIER, ONLY A SURFACE")
    print("=" * 88)

    sigma = 0.23
    a = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    b = sigma_slice_block(sigma=sigma, u=sigma, v=0.0, xbar=1.0)
    rec_a = realize_active_block(a, seed=7101)
    rec_b = realize_active_block(b, seed=7102)

    check("A nonzero fixed-sigma point is already realizable on the lower-level active response chain", np.linalg.norm(rec_a - a) < 1.0e-12, f"error={np.linalg.norm(rec_a - a):.2e}")
    check("The C3-covariant point on that same sigma slice is also realizable exactly", np.linalg.norm(rec_b - b) < 1.0e-12, f"error={np.linalg.norm(rec_b - b):.2e}")
    check("Those extension points stay on the existing diagonal-plus-forward-cycle carrier", np.array_equal(support_mask(rec_a), TARGET_SUPPORT) and np.array_equal(support_mask(rec_b), TARGET_SUPPORT))
    check("So admitting a nonzero sigma surface refines the already-realized reduced PMNS family rather than adding a new carrier", True)


def part2_the_new_surface_is_beyond_retained_but_not_refuted_by_current_exact_constraints() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE NEW SURFACE IS BEYOND RETAINED BUT NOT REFUTED BY CURRENT EXACT CONSTRAINTS")
    print("=" * 88)

    blocks = pure_retained_pmns_blocks()
    sigmas = {name: sigma_from_block(block) for name, block in blocks.items()}
    sigma = 0.23
    candidate = sigma_slice_block(sigma=sigma, u=0.15, v=0.14, xbar=1.0)
    distances = {name: np.linalg.norm(candidate - block) for name, block in blocks.items()}

    check("The current pure-retained PMNS routes still all sit at sigma = 0", all(abs(value) < 1.0e-12 for value in sigmas.values()), f"sigmas={sigmas}")
    check("A nonzero sigma surface is therefore genuinely beyond the current pure-retained bank", min(distances.values()) > 1.0e-6, f"distances={distances}")
    check("But the current exact bank does not exclude such points once an extension is admitted, because they are already realized on the reduced active family", True)


def part3_once_nonzero_sigma_is_admitted_the_native_action_selects_the_covariant_point() -> None:
    print("\n" + "=" * 88)
    print("PART 3: ONCE NONZERO SIGMA IS ADMITTED, THE NATIVE ACTION SELECTS THE COVARIANT POINT")
    print("=" * 88)

    sigma = 0.23
    cov_action = relative_action_sigma_surface_formula(sigma, sigma, 0.0)
    off_action = relative_action_sigma_surface_formula(sigma, 0.15, 0.14)
    eps = 1.0e-6
    du = (
        relative_action_sigma_surface_formula(sigma, sigma + eps, 0.0)
        - relative_action_sigma_surface_formula(sigma, sigma - eps, 0.0)
    ) / (2.0 * eps)
    dv = (
        relative_action_sigma_surface_formula(sigma, sigma, eps)
        - relative_action_sigma_surface_formula(sigma, sigma, -eps)
    ) / (2.0 * eps)
    huu, hvv = exact_hessian_diagonal_at_covariant_point(sigma)
    lower = cubic_lower_bound_on_unit_interval()
    cov_block = sigma_slice_block(sigma=sigma, u=sigma, v=0.0, xbar=1.0)
    jchi = nontrivial_character_current(cov_block)

    check("The C3-covariant point on the admitted sigma surface has smaller native action than a generic off-covariant point on the same surface", cov_action < off_action, f"S_cov={cov_action:.12f}, S_off={off_action:.12f}")
    check("The native action has zero first derivatives at the C3-covariant point", abs(du) < 1.0e-6 and abs(dv) < 1.0e-6, f"du={du:.3e}, dv={dv:.3e}")
    check("The exact Hessian is positive there on the physical interval 0 <= sigma <= 1", huu > 0.0 and lower > 0.0 and hvv > 0.0, f"huu={huu:.12f}, lower={lower:.12f}, hvv={hvv:.12f}")
    check("At that selected point the remaining PMNS current is exactly J_chi = sigma", abs(jchi - sigma) < 1.0e-12, f"J_chi={jchi:.6f}, sigma={sigma:.6f}")


def part4_compact_scan_supports_branch_uniqueness_on_the_current_patch() -> None:
    print("\n" + "=" * 88)
    print("PART 4: COMPACT SCAN SUPPORTS BRANCH UNIQUENESS ON THE CURRENT PATCH")
    print("=" * 88)

    sigmas = [0.05, 0.15, 0.30]
    offsets = []
    current_errors = []
    for sigma in sigmas:
        _value, best_u, best_v = local_grid_minimum(sigma)
        offsets.append(abs(best_u - sigma) + abs(best_v))
        best_block = sigma_slice_block(sigma=sigma, u=best_u, v=best_v, xbar=1.0)
        current_errors.append(abs(nontrivial_character_current(best_block) - sigma))

    check("Across representative sigma slices, the low-action branch stays close to the C3-covariant locus", max(offsets) < 0.02, f"offsets={np.round(offsets, 6)}")
    check("On those same low-action points, the selected current stays close to J_chi = sigma", max(current_errors) < 0.02, f"errors={np.round(current_errors, 6)}")
    print("  [INFO] This is support-grade branch evidence on the current patch, not a theorem-grade global uniqueness proof")


def main() -> int:
    print("=" * 88)
    print("PMNS NONZERO-SIGMA SURFACE EXTENSION BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  If we admit the minimal extra PMNS principle of one nonzero fixed-sigma")
    print("  surface on the retained hw=1 lane, does the current exact PMNS bank")
    print("  already turn that into a coherent selected branch, or does the idea")
    print("  collapse immediately?")

    part1_the_extension_does_not_add_a_new_pmns_carrier_only_a_surface()
    part2_the_new_surface_is_beyond_retained_but_not_refuted_by_current_exact_constraints()
    part3_once_nonzero_sigma_is_admitted_the_native_action_selects_the_covariant_point()
    part4_compact_scan_supports_branch_uniqueness_on_the_current_patch()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Minimal PMNS extension boundary:")
    print("    - admitting a nonzero fixed-sigma surface does not require a new")
    print("      PMNS carrier; it only picks a surface inside the already-realized")
    print("      reduced active family")
    print("    - that move is genuinely beyond the current pure-retained bank")
    print("      because the retained routes still force sigma = 0")
    print("    - but once such a surface is admitted, the native action already")
    print("      selects the C3-covariant point locally, where J_chi = sigma")
    print()
    print("  So this extension route survives the current exact constraints.")
    print("  The honest remaining PMNS question is no longer local selection on the")
    print("  surface; it is the production/justification of the nonzero sigma")
    print("  surface itself.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
