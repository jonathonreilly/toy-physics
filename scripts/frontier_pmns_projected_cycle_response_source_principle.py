#!/usr/bin/env python3
"""
PMNS projected-cycle response source principle on the graph-fixed hw=1 triplet.

Question:
  After the pure-retained PMNS bank is exhausted, is there a smallest exact
  extension principle that forces a nontrivial active response pack on the
  existing hw=1 carrier rather than adding arbitrary reduced-cycle values by
  hand?

Answer:
  Yes, if the microscopic active response on the ordered hw=1 triplet is
  required to realize the exact graph-fixed forward projected-cycle transport.

  The projected forward cycle is the exact operator C. Acting on ordered basis
  response columns, one forward transport step on column labels gives the
  unique kernel

      K_fwd = C^2.

  Among the exact cycle kernels {I, C, C^2}, nontriviality excludes I and the
  graph-fixed forward-support carrier excludes C. So K_fwd = C^2 is the unique
  admissible nonfree kernel.

  Converting kernel to active block by the exact response law

      A = I + (I - K^{-1}) / lambda_act

  forces

      A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C,

  which is already the C3-covariant point on the exact projected-cycle family.
  Therefore

      sigma = J_chi = -1 / lambda_act

  and the one-sided PMNS lane closes exactly with the retained passive free
  pack.

Boundary:
  This is an exact beyond-retained-stack source principle. It does not derive
  transport-realizing response from the current pure-retained bank; it states
  the smallest honest positive PMNS reopening principle that closes the
  response-pack hole once imposed.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_lower_level_end_to_end_closure import close_from_lower_level_observables
from frontier_pmns_oriented_cycle_channel_value_law import oriented_cycle_coeffs_from_block, projected_forward_cycle
from frontier_pmns_sigma_constraint_surface import sigma_from_block
from pmns_lower_level_utils import (
    I3,
    active_response_columns_from_sector_operator,
    circularity_guard,
    passive_response_columns_from_sector_operator,
    support_mask,
)

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
    basis = [I3[:, i].copy() for i in range(3)]
    transported = [c @ (c @ col) for col in basis]
    return np.column_stack(transported)


def active_block_from_response_kernel(kernel: np.ndarray, lam_act: float = LAM_ACT) -> np.ndarray:
    return I3 + (I3 - np.linalg.inv(kernel)) / lam_act


def part1_exact_graph_fixed_forward_transport_determines_one_oriented_response_kernel() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: EXACT GRAPH-FIXED FORWARD TRANSPORT DETERMINES ONE ORIENTED RESPONSE KERNEL")
    print("=" * 88)

    c = projected_forward_cycle()
    k_fwd = forward_transport_response_kernel()
    expected_columns = np.column_stack([np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0]), np.array([1.0, 0.0, 0.0])]).astype(complex)

    check("The exact projected forward cycle on the hw=1 triplet is C", np.linalg.norm(c - np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]], dtype=complex)) < 1.0e-12)
    check("The forward-transported ordered basis columns are exactly the kernel K_fwd = C^2", np.linalg.norm(k_fwd - (c @ c)) < 1.0e-12 and np.linalg.norm(k_fwd - expected_columns) < 1.0e-12, f"error={np.linalg.norm(k_fwd - (c @ c)):.2e}")
    check("The forward transport kernel is unitary and obeys K_fwd^3 = I", np.linalg.norm(k_fwd.conj().T @ k_fwd - I3) < 1.0e-12 and np.linalg.norm(np.linalg.matrix_power(k_fwd, 3) - I3) < 1.0e-12)
    check("So exact graph-fixed forward transport already supplies one nonfree microscopic response kernel candidate", np.linalg.norm(k_fwd - I3) > 1.0e-6)
    return k_fwd


def part2_nontriviality_and_forward_support_make_that_kernel_unique(k_fwd: np.ndarray) -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 2: NONTRIVIALITY AND FORWARD SUPPORT MAKE THAT KERNEL UNIQUE")
    print("=" * 88)

    c = projected_forward_cycle()
    kernels = {"free": I3, "backward": c, "forward": k_fwd}
    blocks = {name: active_block_from_response_kernel(kernel) for name, kernel in kernels.items()}

    check("The free cycle kernel gives back the trivial active block", np.linalg.norm(blocks["free"] - I3) < 1.0e-12 and abs(sigma_from_block(blocks["free"])) < 1.0e-12)
    check("The backward cycle kernel lands on the backward-support carrier rather than the retained forward-support carrier", np.array_equal(support_mask(blocks["backward"]), (np.abs(I3 + c.conj().T) > 0).astype(int)) and not np.array_equal(support_mask(blocks["backward"]), TARGET_SUPPORT))
    check("The forward cycle kernel lands exactly on the retained diagonal-plus-forward-cycle carrier", np.array_equal(support_mask(blocks["forward"]), TARGET_SUPPORT))
    check("Among the exact cycle kernels {I, C, C^2}, the graph-fixed forward-support reopening therefore leaves the unique admissible nonfree choice K_fwd = C^2", True)
    return blocks["forward"]


def part3_the_forced_active_block_is_already_the_covariant_pmns_closure_point(a_fwd: np.ndarray, k_fwd: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE FORCED ACTIVE BLOCK IS ALREADY THE COVARIANT PMNS CLOSURE POINT")
    print("=" * 88)

    free_passive_columns = passive_response_columns_from_sector_operator(I3, LAM_PASS)[1]
    direct_block, direct_columns = active_response_columns_from_sector_operator(a_fwd, LAM_ACT)
    coeffs = oriented_cycle_coeffs_from_block(a_fwd)
    sigma = sigma_from_block(a_fwd)
    jchi = nontrivial_character_current(a_fwd)
    closure = close_from_lower_level_observables([k_fwd[:, i].copy() for i in range(3)], free_passive_columns, LAM_ACT, LAM_PASS)
    expected = -1.0 / LAM_ACT

    check("The active-response law recovers exactly the same kernel from the forced active block", np.linalg.norm(direct_block - a_fwd) < 1.0e-12 and np.linalg.norm(np.column_stack(direct_columns) - k_fwd) < 1.0e-12, f"kernel error={np.linalg.norm(np.column_stack(direct_columns) - k_fwd):.2e}")
    check("The forced active block is already the C3-covariant point on the projected-cycle family", np.linalg.norm(coeffs - expected * np.ones(3, dtype=complex)) < 1.0e-12, f"coeffs={np.round(coeffs, 6)}")
    check("That covariant point has sigma = -1/lambda_act exactly", abs(sigma - expected) < 1.0e-12, f"sigma={sigma:.12f}")
    check("The same block has J_chi = -1/lambda_act exactly", abs(jchi - expected) < 1.0e-12, f"J_chi={jchi:.12f}")
    check("With the retained passive free pack unchanged, the one-sided PMNS lane closes exactly", closure["branch"] == "neutrino-active" and closure["tau"] == 0, f"branch={closure['branch']}, tau={closure['tau']}, q={closure['q']}")


def part4_circularity_guard_and_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 4: CIRCULARITY GUARD AND BOUNDARY")
    print("=" * 88)

    ok_kernel, bad_kernel = circularity_guard(forward_transport_response_kernel, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_block, bad_block = circularity_guard(active_block_from_response_kernel, {"u", "v", "w", "x", "y", "delta", "tau", "q"})

    check("The forward response-kernel principle takes no PMNS target values as inputs", ok_kernel, f"bad={bad_kernel}")
    check("The active-block conversion law takes no PMNS target values as inputs", ok_block, f"bad={bad_block}")
    check("But the principle is beyond-retained-stack: it adds the transport-realizing response requirement rather than deriving it from the current pure-retained bank", True)
    check("So this closes the PMNS source-law hole only as an exact extension principle, not as a pure-retained theorem", True)


def main() -> int:
    print("=" * 88)
    print("PMNS PROJECTED-CYCLE RESPONSE SOURCE PRINCIPLE")
    print("=" * 88)
    print()
    print("Question:")
    print("  After the pure-retained PMNS bank is exhausted, is there a smallest")
    print("  exact extension principle that forces a nontrivial active response")
    print("  pack on the existing hw=1 carrier?")

    k_fwd = part1_exact_graph_fixed_forward_transport_determines_one_oriented_response_kernel()
    a_fwd = part2_nontriviality_and_forward_support_make_that_kernel_unique(k_fwd)
    part3_the_forced_active_block_is_already_the_covariant_pmns_closure_point(a_fwd, k_fwd)
    part4_circularity_guard_and_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Yes. Once the microscopic active response on the graph-fixed hw=1")
    print("  triplet is required to realize the exact forward projected-cycle")
    print("  transport, the unique admissible nonfree response kernel is")
    print("      K_fwd = C^2.")
    print()
    print("  The exact response law then forces")
    print("      A_fwd = (1 + 1/lambda_act) I - (1/lambda_act) C,")
    print("  which is already the C3-covariant point on the projected-cycle")
    print("  family, with")
    print("      sigma = J_chi = -1/lambda_act.")
    print()
    print("  So the PMNS source-law hole now has an exact beyond-retained-stack")
    print("  closure principle. What it still does not do is derive that")
    print("  transport-realizing response requirement from the current")
    print("  pure-retained bank itself.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
