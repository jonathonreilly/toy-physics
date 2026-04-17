#!/usr/bin/env python3
"""
Exact residual Z_2 Hermitian normal form on the hw=1 triplet.

Safe statement:
  In the ordered basis (X_3, X_1, X_2), every Z_2-invariant Hermitian
  operator on the hw=1 triplet has the five-real-parameter form
      [[a, d, d], [d*, b, c], [d*, c, b]]
  with a, b, c real and d complex. The sign eigenvalue and the remaining
  2x2 block are explicit, and generic points give three distinct eigenvalues.
"""

from __future__ import annotations

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


U_Z2 = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=complex,
)


def build_M(a: float, b: float, c: float, d: complex) -> np.ndarray:
    return np.array(
        [
            [a, d, d],
            [np.conj(d), b, c],
            [np.conj(d), c, b],
        ],
        dtype=complex,
    )


def part1_parametrization() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Completeness of the five-parameter family")
    print("=" * 72)

    rng = np.random.default_rng(0)
    for _ in range(10):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        matrix = build_M(a, b, c, d)
        if not np.allclose(matrix, matrix.conj().T):
            check("sample matrix is Hermitian", False)
            return
        if not np.allclose(U_Z2 @ matrix @ U_Z2, matrix):
            check("sample matrix is Z_2-invariant", False)
            return
    check("all random samples are Hermitian and Z_2-invariant", True)

    basis = []
    for a, b, c, dr, di in [
        (1, 0, 0, 0, 0),
        (0, 1, 0, 0, 0),
        (0, 0, 1, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 0, 0, 0, 1),
    ]:
        basis.append(build_M(a, b, c, dr + 1j * di))
    stacked = np.stack([matrix.reshape(9) for matrix in basis], axis=1)
    real_rank = np.linalg.matrix_rank(np.vstack([stacked.real, stacked.imag]), tol=1e-10)
    check("the explicit family has real dimension 5", real_rank == 5, f"rank = {real_rank}")

    hermitian_basis = []
    for idx in range(3):
        matrix = np.zeros((3, 3), dtype=complex)
        matrix[idx, idx] = 1.0
        hermitian_basis.append(matrix)
    for i in range(3):
        for j in range(i + 1, 3):
            real = np.zeros((3, 3), dtype=complex)
            real[i, j] = 1.0
            real[j, i] = 1.0
            imag = np.zeros((3, 3), dtype=complex)
            imag[i, j] = 1j
            imag[j, i] = -1j
            hermitian_basis.extend([real, imag])

    projected = []
    for matrix in hermitian_basis:
        projected.append(0.5 * (matrix + U_Z2 @ matrix @ U_Z2))
    stacked = np.stack([matrix.reshape(9) for matrix in projected], axis=1)
    projected_rank = np.linalg.matrix_rank(np.vstack([stacked.real, stacked.imag]), tol=1e-10)
    check("the full Z_2-invariant Hermitian space has real dimension 5", projected_rank == 5, f"rank = {projected_rank}")


def part2_sign_eigenvector() -> None:
    print("\n" + "=" * 72)
    print("PART 2: Exact sign eigenvector")
    print("=" * 72)

    v_sign = np.array([0.0, 1.0, -1.0], dtype=complex) / np.sqrt(2.0)
    check("the sign vector is a Z_2 eigenvector with eigenvalue -1", np.allclose(U_Z2 @ v_sign, -v_sign))

    rng = np.random.default_rng(7)
    for _ in range(5):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        matrix = build_M(a, b, c, d)
        if not np.allclose(matrix @ v_sign, (b - c) * v_sign, atol=1e-12):
            check("M v_sign = (b-c) v_sign", False)
            return
    check("M v_sign = (b-c) v_sign for random samples", True)


def part3_block_and_spectrum() -> None:
    print("\n" + "=" * 72)
    print("PART 3: Trivial block and closed-form spectrum")
    print("=" * 72)

    rng = np.random.default_rng(13)
    e0 = np.array([1.0, 0.0, 0.0], dtype=complex)
    e1 = np.array([0.0, 1.0, 1.0], dtype=complex) / np.sqrt(2.0)

    for _ in range(10):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        matrix = build_M(a, b, c, d)
        block = np.array(
            [
                [np.vdot(e0, matrix @ e0), np.vdot(e0, matrix @ e1)],
                [np.vdot(e1, matrix @ e0), np.vdot(e1, matrix @ e1)],
            ],
            dtype=complex,
        )
        expected_block = np.array([[a, np.sqrt(2.0) * d], [np.sqrt(2.0) * np.conj(d), b + c]], dtype=complex)
        if not np.allclose(block, expected_block, atol=1e-12):
            check("the trivial block has the expected form", False)
            return
    check("the trivial block has the expected form", True)

    for _ in range(10):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        matrix = build_M(a, b, c, d)
        discriminant = np.sqrt((a - b - c) ** 2 + 8.0 * abs(d) ** 2)
        expected = sorted(
            [
                b - c,
                (a + b + c - discriminant) / 2.0,
                (a + b + c + discriminant) / 2.0,
            ]
        )
        actual = sorted(float(x) for x in np.real(np.linalg.eigvalsh(matrix)))
        if not all(abs(actual[i] - expected[i]) < 1e-10 for i in range(3)):
            check("the closed-form spectrum matches the numerical spectrum", False, f"got {actual}, expected {expected}")
            return
    check("the closed-form spectrum matches the numerical spectrum", True)


def part4_genericity_and_s3_locus() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Genericity and the exact S_3 locus")
    print("=" * 72)

    rng = np.random.default_rng(21)
    counts = {1: 0, 2: 0, 3: 0}
    for _ in range(500):
        a, b, c = rng.normal(size=3)
        d = rng.normal() + 1j * rng.normal()
        eigenvalues = np.real(np.linalg.eigvalsh(build_M(a, b, c, d)))
        distinct = len(set(round(float(x), 10) for x in eigenvalues))
        counts[distinct] += 1
    fraction_three = counts[3] / 500.0
    fraction_degenerate = (counts[1] + counts[2]) / 500.0
    check("generic random samples have three distinct eigenvalues", fraction_three > 0.99, f"fraction = {fraction_three:.3f}")
    check("degenerate samples are rare in random sampling", fraction_degenerate < 0.01, f"fraction = {fraction_degenerate:.3f}")

    matrix = build_M(2.2, 1.5, 0.7, 0.0)
    eigenvalues = np.real(np.linalg.eigvalsh(matrix))
    distinct = len(set(round(float(x), 10) for x in eigenvalues))
    check("the exact S_3 locus d = 0, a = b + c collapses to two values", distinct == 2, f"distinct = {distinct}")


def main() -> int:
    print("=" * 72)
    print("Z_2 hw=1 MASS-MATRIX PARAMETRIZATION")
    print("=" * 72)
    part1_parametrization()
    part2_sign_eigenvector()
    part3_block_and_spectrum()
    part4_genericity_and_s3_locus()
    print("\n" + "=" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
