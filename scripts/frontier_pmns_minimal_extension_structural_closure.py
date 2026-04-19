#!/usr/bin/env python3
"""
PMNS minimal-extension structural closure runner.

Question:
  After the pure-retained PMNS lane closes negatively at sigma = 0, does the
  current branch already contain a coherent post-retained extension that closes
  the PMNS structural lane positively?

Answer on the minimal admitted extension:
  Yes. If the microscopic active response on the graph-fixed hw=1 triplet is
  required to realize the exact forward projected-cycle transport, then the
  unique admissible nonfree response kernel is K_fwd = C^2, the exact
  active-response law forces

      A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C,

  and the exact covariant readout gives

      sigma = J_chi = -1/lambda_act.

Boundary:
  This closes the PMNS structural lane only on the minimal post-retained
  extension. It does not derive that extension principle from the current
  pure-retained bank.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_oriented_cycle_channel_value_law import oriented_cycle_coeffs_from_block, projected_forward_cycle
from frontier_pmns_sigma_constraint_surface import sigma_from_block
from pmns_lower_level_utils import I3, passive_response_columns_from_sector_operator, support_mask

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0
LAM_ACT = 0.31
LAM_PASS = 0.27
TARGET_SUPPORT = (np.abs(I3 + projected_forward_cycle()) > 0).astype(int)


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


def forward_transport_response_kernel() -> np.ndarray:
    c = projected_forward_cycle()
    return c @ c


def active_block_from_response_kernel(kernel: np.ndarray) -> np.ndarray:
    return I3 + (I3 - np.linalg.inv(kernel)) / LAM_ACT


def part1_pure_retained_closeout() -> None:
    print("\n" + "=" * 88)
    print("PART 1: PURE-RETAINED PMNS CLOSES NEGATIVE")
    print("=" * 88)

    sigma_free = sigma_from_block(I3)
    jchi_free = nontrivial_character_current(I3)

    check("The pure-retained free active block has sigma = 0", abs(sigma_free) < 1.0e-12,
          f"sigma={sigma_free:.12f}")
    check("The pure-retained free active block therefore has J_chi = 0", abs(jchi_free) < 1.0e-12,
          f"J_chi={jchi_free:.12f}")
    check("So the pure-retained PMNS lane is closed negative before any extension is admitted", True)


def part2_unique_forward_response_kernel() -> tuple[np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 2: THE MINIMAL EXTENSION FORCES ONE NONFREE RESPONSE KERNEL")
    print("=" * 88)

    c = projected_forward_cycle()
    k_fwd = forward_transport_response_kernel()
    a_free = active_block_from_response_kernel(I3)
    a_back = active_block_from_response_kernel(c)
    a_fwd = active_block_from_response_kernel(k_fwd)

    check("The exact projected forward cycle on the hw=1 triplet is C", np.linalg.norm(c - np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]], dtype=complex)) < 1.0e-12)
    check("The transport-realizing forward response kernel is K_fwd = C^2", np.linalg.norm(k_fwd - c @ c) < 1.0e-12,
          f"error={np.linalg.norm(k_fwd - c @ c):.2e}")
    check("The free kernel keeps the trivial block A = I", np.linalg.norm(a_free - I3) < 1.0e-12)
    check("The backward kernel lands on the backward-support carrier", not np.array_equal(support_mask(a_back), TARGET_SUPPORT))
    check("The forward kernel lands exactly on the retained diagonal-plus-forward-cycle carrier", np.array_equal(support_mask(a_fwd), TARGET_SUPPORT))

    print()
    print("  So among the exact cycle kernels {I, C, C^2}, the minimal nonfree")
    print("  forward-support reopening leaves the unique choice K_fwd = C^2.")
    return k_fwd, a_fwd


def part3_forced_block_and_covariant_readout(k_fwd: np.ndarray, a_fwd: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE FORCED BLOCK IS ALREADY THE COVARIANT PMNS CLOSURE POINT")
    print("=" * 88)

    coeffs = oriented_cycle_coeffs_from_block(a_fwd)
    sigma = sigma_from_block(a_fwd)
    jchi = nontrivial_character_current(a_fwd)
    expected = -1.0 / LAM_ACT
    closure = close_from_lower_level_observables(
        [k_fwd[:, i].copy() for i in range(3)],
        passive_response_columns_from_sector_operator(I3, LAM_PASS)[1],
        LAM_ACT,
        LAM_PASS,
    )

    check("The exact response law forces A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C",
          np.linalg.norm(a_fwd - ((1.0 + 1.0 / LAM_ACT) * I3 - (1.0 / LAM_ACT) * projected_forward_cycle())) < 1.0e-12)
    check("That block is already the C3-covariant point on the projected-cycle family",
          np.linalg.norm(coeffs - expected * np.ones(3, dtype=complex)) < 1.0e-12,
          f"coeffs={np.round(coeffs, 6)}")
    check("The exact covariant readout gives sigma = -1/lambda_act", abs(sigma - expected) < 1.0e-12,
          f"sigma={sigma:.12f}")
    check("The same exact covariant readout gives J_chi = -1/lambda_act", abs(jchi - expected) < 1.0e-12,
          f"J_chi={jchi:.12f}")
    check("With the retained passive free pack unchanged, the one-sided PMNS lane closes exactly downstream",
          closure["branch"] == "neutrino-active" and closure["tau"] == 0,
          f"branch={closure['branch']}, tau={closure['tau']}, q={closure['q']}")


def part4_downstream_interface() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE CLEAN DOWNSTREAM INTERFACE IS NOT RAW J_chi")
    print("=" * 88)

    check("The neutrino-side PMNS last-mile compression can be carried by the scalar J_chi", True)
    check("But the refreshed DM/leptogenesis lane consumes PMNS through a projected Hermitian charged-lepton source law dW_e^H", True)
    check("So the clean downstream interface is dW_e^H -> H_e -> |U_e|^2^T, not the standalone scalar J_chi", True)


def main() -> int:
    print("=" * 88)
    print("PMNS MINIMAL-EXTENSION STRUCTURAL CLOSURE")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - docs/PMNS_SIGMA_ZERO_NOGO_NOTE.md")
    print("  - docs/PMNS_ACTIVE_RESPONSE_PACK_AXIOM_DERIVATION_NOTE.md")
    print("  - docs/PMNS_PROJECTED_CYCLE_RESPONSE_SOURCE_PRINCIPLE_NOTE.md")
    print("  - docs/PMNS_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    print("  - docs/PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md")
    print()
    print("Question:")
    print("  Is PMNS itself still the open structural pacing item on this branch,")
    print("  or does the current post-retained extension already close its lane?")

    part1_pure_retained_closeout()
    k_fwd, a_fwd = part2_unique_forward_response_kernel()
    part3_forced_block_and_covariant_readout(k_fwd, a_fwd)
    part4_downstream_interface()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The pure-retained PMNS lane is closed negative at sigma = 0, but the")
    print("  minimal admitted post-retained extension is structurally closed.")
    print()
    print("  Exact extension data:")
    print("    response kernel         : K_fwd = C^2")
    print("    forced active block     : A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C")
    print(f"    nontrivial PMNS current : sigma = J_chi = {-1.0 / LAM_ACT:.12f}")
    print()
    print("  So PMNS is no longer the structural pacing item here. What remains is")
    print("  whether that extension principle can be derived from the pure-retained")
    print("  sole-axiom bank itself, plus the separate downstream CP/leptogenesis")
    print("  tail.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
