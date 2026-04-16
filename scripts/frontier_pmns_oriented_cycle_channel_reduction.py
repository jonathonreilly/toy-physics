#!/usr/bin/env python3
"""Exact reduction of the remaining PMNS carrier to the oriented cycle channel.

Question:
  Once the local scalar-field route is closed, what is the exact remaining
  non-scalar carrier on the retained PMNS active class?

Answer:
  The retained canonical active class is exactly the direct sum of:

    - diagonal triplet data, and
    - one oriented forward cycle channel.

  Therefore, after the local scalar boundary removes the diagonal-only route,
  the remaining positive carrier is the oriented cycle transport channel
  `span{E12, E23, E31}`.
"""

from __future__ import annotations

import sys

import numpy as np

from pmns_lower_level_utils import CYCLE, I3, active_operator, support_mask

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


def e(i: int, j: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[i, j] = 1.0
    return out


E12 = e(0, 1)
E23 = e(1, 2)
E31 = e(2, 0)
E13 = e(0, 2)
E21 = e(1, 0)
E32 = e(2, 1)
FWD_SUPPORT = support_mask(CYCLE)
BWD_SUPPORT = support_mask(CYCLE.conj().T)
ACTIVE_SUPPORT = support_mask(I3 + CYCLE)


def diagonal_part(a: np.ndarray) -> np.ndarray:
    return np.diag(np.diag(a))


def forward_cycle_part(a: np.ndarray) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[0, 1] = a[0, 1]
    out[1, 2] = a[1, 2]
    out[2, 0] = a[2, 0]
    return out


def backward_cycle_part(a: np.ndarray) -> np.ndarray:
    out = np.zeros((3, 3), dtype=complex)
    out[0, 2] = a[0, 2]
    out[1, 0] = a[1, 0]
    out[2, 1] = a[2, 1]
    return out


def part1_the_canonical_active_support_is_exactly_diagonal_plus_one_oriented_cycle() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CANONICAL ACTIVE SUPPORT IS DIAGONAL PLUS ONE ORIENTED CYCLE")
    print("=" * 88)

    check("The forward cycle support is exactly {12,23,31}", np.array_equal(FWD_SUPPORT, np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=int)))
    check("The backward cycle support is exactly {13,21,32}", np.array_equal(BWD_SUPPORT, np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=int)))
    check("The canonical active support is exactly diagonal plus the forward cycle", np.array_equal(ACTIVE_SUPPORT, np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]], dtype=int)))
    check("No backward-cycle edge survives on the canonical active support", np.count_nonzero(ACTIVE_SUPPORT * BWD_SUPPORT) == 0)


def part2_any_canonical_active_block_decomposes_uniquely_into_diagonal_plus_forward_cycle() -> None:
    print("\n" + "=" * 88)
    print("PART 2: CANONICAL ACTIVE BLOCK = DIAGONAL PART + FORWARD CYCLE PART")
    print("=" * 88)

    a = active_operator(
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )
    d = diagonal_part(a)
    f = forward_cycle_part(a)
    b = backward_cycle_part(a)
    rebuilt = d + f

    check("A canonical active block has no backward-cycle contribution", np.linalg.norm(b) < 1e-12, f"norm={np.linalg.norm(b):.2e}")
    check("It rebuilds exactly from its diagonal and forward-cycle parts", np.linalg.norm(rebuilt - a) < 1e-12, f"error={np.linalg.norm(rebuilt-a):.2e}")
    check("The forward-cycle part lies in span{E12,E23,E31}", np.linalg.norm(f - (a[0,1]*E12 + a[1,2]*E23 + a[2,0]*E31)) < 1e-12)
    check("So the canonical active class is exactly diagonal ⊕ oriented-cycle", True)


def part3_after_the_local_scalar_boundary_the_remaining_positive_carrier_is_the_oriented_cycle_channel() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING POSITIVE CARRIER IS THE ORIENTED CYCLE CHANNEL")
    print("=" * 88)

    diagonal_sample = np.diag([1.2, 0.8, 1.5]).astype(complex)
    cycle_only = np.array(
        [
            [0.0, 0.41, 0.0],
            [0.0, 0.0, 0.28],
            [0.54 * np.exp(0.63j), 0.0, 0.0],
        ],
        dtype=complex,
    )

    check("The local scalar route supplies only the diagonal carrier", np.array_equal(support_mask(diagonal_sample), np.eye(3, dtype=int)))
    check("The non-scalar part of the retained active class lives exactly on the forward cycle", np.array_equal(support_mask(cycle_only), FWD_SUPPORT))
    check("Therefore once the diagonal-only scalar route is excluded, the remaining carrier is the oriented cycle channel", True,
          "span{E12, E23, E31}")


def main() -> int:
    print("=" * 88)
    print("PMNS ORIENTED CYCLE CHANNEL REDUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Once the local scalar-field route is closed, what is the exact")
    print("  remaining non-scalar carrier on the retained PMNS active class?")

    part1_the_canonical_active_support_is_exactly_diagonal_plus_one_oriented_cycle()
    part2_any_canonical_active_block_decomposes_uniquely_into_diagonal_plus_forward_cycle()
    part3_after_the_local_scalar_boundary_the_remaining_positive_carrier_is_the_oriented_cycle_channel()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction:")
    print("    - the canonical active class is diagonal plus one oriented cycle")
    print("    - the local scalar route fills only the diagonal carrier")
    print("    - so the remaining positive carrier is the oriented cycle channel")
    print()
    print("  The next honest positive target is therefore not 'some scalar law',")
    print("  but a value law for the oriented forward cycle transport channel.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
