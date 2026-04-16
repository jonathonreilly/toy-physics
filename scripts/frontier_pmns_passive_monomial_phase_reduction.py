#!/usr/bin/env python3
"""Exact phase-reduction theorem for passive monomial PMNS blocks."""

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


def monomial_triplet(coeffs: np.ndarray, q: int) -> np.ndarray:
    return diagonal(np.asarray(coeffs, dtype=complex)) @ PERMUTATIONS[q]


def left_rephase_to_positive(block: np.ndarray, q: int) -> tuple[np.ndarray, np.ndarray]:
    coeffs = np.diag(block @ PERMUTATIONS[q].conj().T)
    phases = np.exp(-1j * np.angle(coeffs))
    left = diagonal(phases)
    return left, left @ block


def main() -> int:
    print("=" * 88)
    print("PMNS PASSIVE MONOMIAL PHASE REDUCTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  On the passive monomial PMNS lane, do the coefficient phases carry")
    print("  irreducible data, or are they removable by support-preserving")
    print("  rephasing?")

    for q, coeffs in {
        0: np.array([0.07 * np.exp(0.4j), 0.11 * np.exp(-0.7j), 0.23 * np.exp(1.1j)], dtype=complex),
        1: np.array([0.17 * np.exp(-0.3j), 0.09 * np.exp(0.9j), 0.04 * np.exp(-1.4j)], dtype=complex),
        2: np.array([0.05 * np.exp(0.8j), 0.13 * np.exp(-0.2j), 0.21 * np.exp(0.5j)], dtype=complex),
    }.items():
        block = monomial_triplet(coeffs, q)
        left, reduced = left_rephase_to_positive(block, q)
        recovered = reduced @ PERMUTATIONS[q].conj().T
        mods = np.abs(coeffs)

        check(f"q={q}: left rephasing keeps the monomial support class fixed",
              np.array_equal((np.abs(block) > 1e-12).astype(int), (np.abs(reduced) > 1e-12).astype(int)))
        check(f"q={q}: left rephasing removes all passive coefficient phases",
              np.linalg.norm(np.diag(recovered) - mods) < 1e-12,
              f"diag={np.round(np.diag(recovered), 6)}")
        check(f"q={q}: the reduced passive block is exactly diag(|a_i|) P_q",
              np.linalg.norm(reduced - monomial_triplet(mods, q)) < 1e-12,
              f"err={np.linalg.norm(reduced - monomial_triplet(mods, q)):.2e}")
        check(f"q={q}: the rephasing matrix is unitary", np.linalg.norm(left @ left.conj().T - I3) < 1e-12)

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact passive reduction:")
    print("    - passive monomial phases are removable by support-preserving left rephasing")
    print("    - the invariant passive data reduce to the offset q and three nonnegative moduli")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
