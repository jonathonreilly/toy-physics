#!/usr/bin/env python3
"""
Exact S_3 mass-matrix no-go on the hw=1 triplet.

Safe statement:
  On the hw=1 carrier V = span(X_1, X_2, X_3) with the natural permutation
  action of S_3, every S_3-invariant Hermitian operator has the form
  alpha I_3 + beta P_(A_1). Therefore the exact unbroken S_3 class allows at
  most two distinct eigenvalues on this carrier. The residual axis-fixing Z_2
  invariant Hermitian space has real dimension 5.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def hw1_s3_representation() -> dict[str, np.ndarray]:
    return {
        "e": np.eye(3, dtype=complex),
        "(12)": np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=complex),
        "(23)": np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
        "(13)": np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=complex),
        "(123)": np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
        "(132)": np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    }


def invariant_projector(operators: dict[str, np.ndarray]) -> np.ndarray:
    projector = np.zeros((9, 9), dtype=complex)
    for operator in operators.values():
        for i, j in itertools.product(range(3), repeat=2):
            basis = np.zeros((3, 3), dtype=complex)
            basis[i, j] = 1.0
            averaged = operator @ basis @ operator.conj().T
            projector[:, i * 3 + j] += averaged.reshape(9) / len(operators)
    return projector


def part1_invariant_algebra() -> None:
    print("\n" + "=" * 72)
    print("PART 1: S_3-invariant Hermitian algebra on hw=1")
    print("=" * 72)

    operators = hw1_s3_representation()
    projector = invariant_projector(operators)
    rank = np.linalg.matrix_rank(projector, tol=1e-10)
    check("dim End(C^3)^(S_3) = 2", rank == 2, f"rank = {rank}")

    identity = np.eye(3, dtype=complex)
    all_ones = np.ones((3, 3), dtype=complex)
    p_a1 = all_ones / 3.0
    check("I_3 is S_3-invariant", all(np.allclose(U @ identity @ U.conj().T, identity) for U in operators.values()))
    check("J_3 is S_3-invariant", all(np.allclose(U @ all_ones @ U.conj().T, all_ones) for U in operators.values()))
    check("P_(A_1) is idempotent", np.allclose(p_a1 @ p_a1, p_a1))
    check("rank P_(A_1) = 1", np.linalg.matrix_rank(p_a1) == 1)


def part2_spectrum() -> None:
    print("\n" + "=" * 72)
    print("PART 2: Forced two-value spectrum")
    print("=" * 72)

    identity = np.eye(3, dtype=complex)
    p_a1 = np.ones((3, 3), dtype=complex) / 3.0

    for alpha, beta in [(1.0, 0.0), (1.0, 1.0), (0.5, 2.0), (-1.0, 3.0)]:
        matrix = alpha * identity + beta * p_a1
        eigenvalues = sorted(float(x) for x in np.real(np.linalg.eigvalsh(matrix)))
        expected = sorted([alpha, alpha, alpha + beta])
        check(
            f"spectrum matches ({alpha:+.2f}, {beta:+.2f})",
            all(abs(eigenvalues[i] - expected[i]) < 1e-10 for i in range(3)),
            f"got {eigenvalues}",
        )

    equal_matrix = 2.0 * identity
    equal_eigs = np.real(np.linalg.eigvalsh(equal_matrix))
    check("beta = 0 gives one distinct eigenvalue", abs(max(equal_eigs) - min(equal_eigs)) < 1e-10)

    split_matrix = identity + p_a1
    distinct = len(set(round(float(x), 10) for x in np.real(np.linalg.eigvalsh(split_matrix))))
    check("beta != 0 gives exactly two distinct eigenvalues", distinct == 2, f"distinct = {distinct}")


def part3_random_audit() -> None:
    print("\n" + "=" * 72)
    print("PART 3: Random audit of the exact S_3 class")
    print("=" * 72)

    rng = np.random.default_rng(42)
    identity = np.eye(3, dtype=complex)
    p_a1 = np.ones((3, 3), dtype=complex) / 3.0
    max_distinct = 0
    for _ in range(100):
        alpha = rng.normal()
        beta = rng.normal()
        matrix = alpha * identity + beta * p_a1
        distinct = len(set(round(float(x), 10) for x in np.real(np.linalg.eigvalsh(matrix))))
        max_distinct = max(max_distinct, distinct)
    check("no random S_3-invariant sample exceeds two spectral values", max_distinct <= 2, f"max distinct = {max_distinct}")


def part4_residual_z2_dimension() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Residual Z_2 dimension jump")
    print("=" * 72)

    operators = {
        "e": np.eye(3, dtype=complex),
        "(12)": np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=complex),
    }
    projector = invariant_projector(operators)
    rank = np.linalg.matrix_rank(projector, tol=1e-10)
    check("dim End(C^3)^(Z_2) = 5", rank == 5, f"rank = {rank}")


def main() -> int:
    print("=" * 72)
    print("S_3 MASS-MATRIX NO-GO ON THE hw=1 TRIPLET")
    print("=" * 72)
    part1_invariant_algebra()
    part2_spectrum()
    part3_random_audit()
    part4_residual_z2_dimension()
    print("\n" + "=" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
