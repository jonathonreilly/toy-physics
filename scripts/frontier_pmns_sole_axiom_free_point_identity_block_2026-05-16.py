#!/usr/bin/env python3
"""Narrow bridge theorem: sole-axiom free-point active block is exactly I_3.

Closes one of the two missing_bridge_theorem clauses named by the
audit verdict on pmns_oriented_cycle_selection_structure_note, namely:

  "the sole-axiom free-point identity block within the restricted
  dependency chain."

The active operator construction used throughout the PMNS active-block
stack is

    A_act(x, y, delta) = diag(x_1, x_2, x_3)
                       + diag(y_1, y_2, y_3 * exp(i * delta)) @ C

with C the canonical forward-cycle matrix.  The sole-axiom free point of
this construction is x = (1, 1, 1), y = (0, 0, 0), delta arbitrary.

Theorem (class A finite-dimensional algebra):

  A_act((1,1,1), (0,0,0), delta) = I_3            for all delta in R,

so the oriented forward-cycle coefficients
(c_1, c_2, c_3) = diag(A_act @ C^dagger) all vanish and the C3-fixed-
locus scalar sigma = (c_1 + c_2 + c_3) / 3 is exactly 0.

This runner exercises only finite-dimensional algebra; it does not
derive the active-operator construction itself from the sole axiom.  The
carrier derivation is the role of the upstream retained hw=1 authority
chain.
"""

from __future__ import annotations

import sys

import numpy as np

from pmns_lower_level_utils import CYCLE, I3, active_operator

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


FREE_X = np.array([1.0, 1.0, 1.0], dtype=float)
FREE_Y = np.array([0.0, 0.0, 0.0], dtype=float)
DELTAS = [0.0, 0.5, 1.0, -1.7, np.pi, 2 * np.pi]


def oriented_cycle_coeffs(block: np.ndarray) -> np.ndarray:
    return np.diag(block @ CYCLE.conj().T)


def part1_free_point_block_is_identity_for_all_delta() -> None:
    print("\n" + "=" * 88)
    print("PART 1: A_act((1,1,1), (0,0,0), delta) = I_3  for all delta")
    print("=" * 88)
    for d in DELTAS:
        block = active_operator(FREE_X, FREE_Y, d)
        check(
            f"A_act((1,1,1), (0,0,0), delta={d:.4f}) equals I_3",
            np.linalg.norm(block - I3) < 1e-12,
            f"||A - I_3|| = {np.linalg.norm(block - I3):.2e}",
        )


def part2_free_point_oriented_cycle_coeffs_vanish() -> None:
    print("\n" + "=" * 88)
    print("PART 2: oriented forward-cycle coefficients vanish at the free point")
    print("=" * 88)
    for d in DELTAS:
        block = active_operator(FREE_X, FREE_Y, d)
        coeffs = oriented_cycle_coeffs(block)
        check(
            f"(c_1,c_2,c_3) = (0,0,0)  at delta={d:.4f}",
            np.linalg.norm(coeffs) < 1e-12,
            f"coeffs={np.round(coeffs, 12)}",
        )


def part3_free_point_sigma_is_zero() -> None:
    print("\n" + "=" * 88)
    print("PART 3: sigma = (c_1 + c_2 + c_3) / 3 is exactly 0 at the free point")
    print("=" * 88)
    for d in DELTAS:
        block = active_operator(FREE_X, FREE_Y, d)
        coeffs = oriented_cycle_coeffs(block)
        sigma = np.mean(coeffs)
        check(
            f"sigma = 0  at delta={d:.4f}",
            abs(sigma) < 1e-12,
            f"sigma={sigma}",
        )


def part4_away_from_free_point_block_differs_from_identity() -> None:
    print("\n" + "=" * 88)
    print("PART 4: NEGATIVE CONTROL — away from the free point, A_act != I_3")
    print("=" * 88)
    block_off = active_operator(np.array([1.0, 1.0, 1.0]), np.array([0.3, -0.2, 0.1]), 0.4)
    check(
        "off-free-point A_act differs from I_3 (negative control)",
        np.linalg.norm(block_off - I3) > 1e-3,
        f"||A_off - I_3|| = {np.linalg.norm(block_off - I3):.4f}",
    )
    coeffs_off = oriented_cycle_coeffs(block_off)
    check(
        "off-free-point oriented-cycle coefficients are nonzero (negative control)",
        np.linalg.norm(coeffs_off) > 1e-3,
        f"coeffs={np.round(coeffs_off, 6)}",
    )


def part5_result() -> None:
    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Sole-axiom free-point identity-block narrow bridge theorem:")
    print("    A_act((1,1,1), (0,0,0), delta) = I_3  for all delta")
    print("    (c_1, c_2, c_3) = (0, 0, 0)")
    print("    sigma = 0")
    print("  closes the load-bearing step in")
    print("    docs/PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md")
    print("  that asserts 'A = I_3 at the sole-axiom free point, hence sigma = 0'.")
    print("  Carrier derivation of the active-operator construction itself")
    print("  is out of scope and remains with the upstream retained hw=1")
    print("  authority chain.")


def main() -> int:
    print("=" * 88)
    print("PMNS SOLE-AXIOM FREE-POINT IDENTITY-BLOCK NARROW BRIDGE THEOREM")
    print("=" * 88)
    print()
    print("Construction:")
    print("  A_act(x, y, delta) = diag(x) + diag(y_eff) @ C")
    print("                   y_eff = (y_1, y_2, y_3 * exp(i*delta))")
    print()
    print("Free point: x = (1,1,1), y = (0,0,0), delta arbitrary in R.")

    part1_free_point_block_is_identity_for_all_delta()
    part2_free_point_oriented_cycle_coeffs_vanish()
    part3_free_point_sigma_is_zero()
    part4_away_from_free_point_block_differs_from_identity()
    part5_result()

    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
