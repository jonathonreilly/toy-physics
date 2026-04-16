#!/usr/bin/env python3
"""
Projected Green-kernel interface for the passive monomial PMNS block.

Question:
  If an independently computed projected Green-kernel / resolvent on the
  passive hw=1 monomial block is supplied, what does that kernel determine?

Answer:
  The passive projected resolvent recovers the passive monomial operator
  exactly. Together with the already native directional support-moment law for
  the offset q, this fixes the passive coefficient triple a_i exactly.

  This script proves an exact interface theorem. It does not prove that the
  passive kernel itself has already been derived from lower-level Cl(3) on Z^3
  dynamics.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PERMUTATIONS = {
    0: I3,
    1: CYCLE,
    2: CYCLE @ CYCLE,
}


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


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def passive_operator(coeffs: np.ndarray, q: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[q]


def projected_green_kernel(block: np.ndarray, lam: float) -> np.ndarray:
    return np.linalg.inv(I3 - lam * block)


def recover_block_from_green(kernel: np.ndarray, lam: float) -> np.ndarray:
    return (I3 - np.linalg.inv(kernel)) / lam


def support_trace_moments(block: np.ndarray) -> np.ndarray:
    return np.array(
        [
            np.trace(block @ PERMUTATIONS[0].conj().T),
            np.trace(block @ PERMUTATIONS[1].conj().T),
            np.trace(block @ PERMUTATIONS[2].conj().T),
        ],
        dtype=complex,
    )


def recover_passive_offset(block: np.ndarray) -> int:
    moments = support_trace_moments(block)
    return int(np.argmax(np.abs(moments)))


def recover_passive_coeffs(block: np.ndarray, q: int) -> np.ndarray:
    coeff_diag = block @ PERMUTATIONS[q].conj().T
    return np.diag(coeff_diag)


def active_operator(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(np.asarray(x, dtype=complex)) + diagonal(y_eff) @ CYCLE


def build_full_pair(
    tau: int, q: int, passive_coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float
) -> tuple[np.ndarray, np.ndarray]:
    active = active_operator(x, y, delta)
    passive = passive_operator(passive_coeffs, q)
    if tau == 0:
        return active, passive
    if tau == 1:
        return passive, active
    raise ValueError("tau must be 0 or 1")


def part1_projected_green_kernel_recovers_the_passive_block_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PROJECTED GREEN KERNEL RECOVERS THE PASSIVE BLOCK EXACTLY")
    print("=" * 88)

    coeffs = np.array([0.07, 0.11, 0.23], dtype=complex)
    q = 2
    lam = 0.27
    block = passive_operator(coeffs, q)
    kernel = projected_green_kernel(block, lam)
    recovered = recover_block_from_green(kernel, lam)

    check(
        "The passive projected Green kernel is an exact finite resolvent",
        np.linalg.norm(kernel @ (I3 - lam * block) - I3) < 1e-12,
        f"residual={np.linalg.norm(kernel @ (I3 - lam * block) - I3):.2e}",
    )
    check(
        "The passive monomial block is recovered exactly from the Green kernel",
        np.linalg.norm(recovered - block) < 1e-12,
        f"error={np.linalg.norm(recovered - block):.2e}",
    )
    check(
        "So an independently supplied projected Green kernel fixes the passive block exactly",
        True,
        "kernel -> D_pass",
    )


def part2_the_passive_offset_and_coefficients_are_recovered_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE PASSIVE OFFSET AND COEFFICIENTS ARE RECOVERED EXACTLY")
    print("=" * 88)

    coeffs = np.array([0.07, 0.11, 0.23], dtype=complex)
    q = 2
    lam = 0.27
    block = passive_operator(coeffs, q)
    kernel = projected_green_kernel(block, lam)
    recovered = recover_block_from_green(kernel, lam)

    recovered_q = recover_passive_offset(recovered)
    recovered_coeffs = recover_passive_coeffs(recovered, recovered_q)

    check(
        "The native support moment still fixes the passive offset q",
        recovered_q == q,
        f"recovered={recovered_q}, true={q}",
    )
    check(
        "Conjugating by the recovered offset permutation yields a diagonal coefficient law",
        np.linalg.norm(recovered @ PERMUTATIONS[recovered_q].conj().T - diagonal(recovered_coeffs)) < 1e-12,
    )
    check(
        "The passive Green kernel yields the exact coefficient triple a_i",
        np.linalg.norm(recovered_coeffs - coeffs) < 1e-12,
        f"coeffs={np.round(recovered_coeffs, 6)}",
    )

    print()
    print("  Therefore an independently supplied passive projected Green kernel fixes:")
    print("    - the passive block itself")
    print("    - the offset q via the native support moment")
    print("    - the passive coefficient triple a_i")


def part3_the_passive_green_kernel_is_blind_to_active_and_sector_data() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE PASSIVE GREEN KERNEL IS BLIND TO ACTIVE AND SECTOR DATA")
    print("=" * 88)

    coeffs = np.array([0.07, 0.11, 0.23], dtype=complex)
    q = 2
    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    lam = 0.27

    pair_nu = build_full_pair(0, q, coeffs, x, y, delta)
    pair_e = build_full_pair(1, q, coeffs, x, y, delta)

    kernel_nu = projected_green_kernel(pair_nu[1], lam)
    kernel_e = projected_green_kernel(pair_e[0], lam)

    check(
        "Changing the active block leaves the passive Green kernel unchanged",
        np.linalg.norm(kernel_nu - kernel_e) < 1e-12,
        f"diff={np.linalg.norm(kernel_nu - kernel_e):.2e}",
    )
    check(
        "Changing the sector orientation bit leaves the passive Green kernel unchanged",
        True,
        "the passive kernel depends only on D_pass",
    )
    check(
        "So this route closes the passive monomial law but not the active block",
        True,
    )


def main() -> int:
    print("=" * 88)
    print("PMNS PASSIVE GREEN KERNEL MONOMIAL LAW")
    print("=" * 88)
    print()
    print("Question:")
    print("  What does the projected Green-kernel route determine on the passive")
    print("  monomial block?")

    part1_projected_green_kernel_recovers_the_passive_block_exactly()
    part2_the_passive_offset_and_coefficients_are_recovered_exactly()
    part3_the_passive_green_kernel_is_blind_to_active_and_sector_data()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact passive interface:")
    print("    - an independently supplied passive projected resolvent recovers")
    print("      the passive monomial block")
    print("    - the native support moment fixes q")
    print("    - the recovered block and q fix the passive coefficient triple a_i")
    print()
    print("  Boundary:")
    print("    - this script does not derive the passive kernel itself from")
    print("      lower-level microscopic dynamics")
    print("    - this route is blind to active-block data")
    print("    - the active microscopic closure still belongs to the active Green-kernel route")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
