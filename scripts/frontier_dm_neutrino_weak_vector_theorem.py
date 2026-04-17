#!/usr/bin/env python3
"""
Neutrino Weak Vector Theorem
============================

STATUS: EXACT representation theorem; base normalization closed elsewhere

Purpose:
  Tighten the direct-bridge story one more step:

    do the exact local chiral bridges

        Y_i = P_R Gamma_i P_L

    form a genuine weak vector under the derived SU(2), and if so does that
    force the neutrino base coupling?

The exact answer from the current branch is:

  1. yes, the bridge family is an exact spin-1 weak vector
  2. no, that covariance alone does not fix the absolute coefficient

More precisely:

  - the bivectors B_a = -(i/2) eps_{abc} Gamma_b Gamma_c form exact su(2)
  - the spatial Gamma_i family on C^8 transforms as a vector:
        [B_a, Gamma_b] = i eps_{abc} Gamma_c
        sum_a [B_a,[B_a,Gamma_b]] = 2 Gamma_b
  - the chiral bridges Y_i = P_R Gamma_i P_L on C^16 obey the same exact
    vector law and are trace-orthogonal
  - but the covariance equations are homogeneous: lambda * Y_i satisfies the
    same weak-vector relations for any scalar lambda

So the theorem closes the representation content of the direct bridge, but it
does NOT by itself select the physical base normalization. That later step is
handled separately by the bosonic-normalization theorem.
"""

from __future__ import annotations

import math
import sys
import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


I2 = np.eye(2, dtype=complex)
I8 = np.eye(8, dtype=complex)
I16 = np.eye(16, dtype=complex)

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


def eps(a: int, b: int, c: int) -> int:
    if len({a, b, c}) < 3:
        return 0
    if (a, b, c) in ((1, 2, 3), (2, 3, 1), (3, 1, 2)):
        return 1
    return -1


G1 = kron3(SX, I2, I2)
G2 = kron3(SY, SX, I2)
G3 = kron3(SY, SY, SX)
G_SPATIAL_8 = [G1, G2, G3]

B1 = -0.5j * G2 @ G3
B2 = -0.5j * G3 @ G1
B3 = -0.5j * G1 @ G2
B_8 = [B1, B2, B3]

G0_4D = kron4(SZ, SZ, SZ, SX)
G1_4D = kron4(SX, I2, I2, I2)
G2_4D = kron4(SZ, SX, I2, I2)
G3_4D = kron4(SZ, SZ, SX, I2)
G_SPATIAL_16 = [G1_4D, G2_4D, G3_4D]

B1_4D = -0.5j * G2_4D @ G3_4D
B2_4D = -0.5j * G3_4D @ G1_4D
B3_4D = -0.5j * G1_4D @ G2_4D
B_16 = [B1_4D, B2_4D, B3_4D]

GAMMA5_4D = G0_4D @ G1_4D @ G2_4D @ G3_4D
P_L = (I16 + GAMMA5_4D) / 2.0
P_R = (I16 - GAMMA5_4D) / 2.0
Y_BRIDGES = [P_R @ G @ P_L for G in G_SPATIAL_16]


def vector_error(generators: list[np.ndarray], family: list[np.ndarray]) -> float:
    worst = 0.0
    for a, B in enumerate(generators, start=1):
        for b, X in enumerate(family, start=1):
            target = sum(1j * eps(a, b, c) * family[c - 1] for c in range(1, 4))
            err = np.linalg.norm(B @ X - X @ B - target)
            worst = max(worst, float(err))
    return worst


def double_commutator_error(generators: list[np.ndarray], family: list[np.ndarray], coeff: float) -> float:
    worst = 0.0
    for X in family:
        double = sum(B @ (B @ X - X @ B) - (B @ X - X @ B) @ B for B in generators)
        err = np.linalg.norm(double - coeff * X)
        worst = max(worst, float(err))
    return worst


def gram_matrix(family: list[np.ndarray]) -> np.ndarray:
    n = len(family)
    gram = np.zeros((n, n), dtype=complex)
    for i, Xi in enumerate(family):
        for j, Xj in enumerate(family):
            gram[i, j] = np.trace(Xi.conj().T @ Xj)
    return gram


def main() -> int:
    print("=" * 78)
    print("NEUTRINO WEAK VECTOR THEOREM")
    print("=" * 78)
    print()

    print("Part 1: Derived weak SU(2) on the taste space")
    su2_err = 0.0
    for a, Ba in enumerate(B_8, start=1):
        for b, Bb in enumerate(B_8, start=1):
            target = sum(1j * eps(a, b, c) * B_8[c - 1] for c in range(1, 4))
            su2_err = max(su2_err, float(np.linalg.norm(Ba @ Bb - Bb @ Ba - target)))
    casimir_err = np.linalg.norm(sum(B @ B for B in B_8) - 0.75 * I8)
    gram_b = gram_matrix(B_8)
    print(f"  max su(2) commutator error = {su2_err:.3e}")
    print(f"  ||sum_a B_a^2 - (3/4)I|| = {casimir_err:.3e}")
    print()
    check("bivectors form exact su(2)", su2_err < 1e-12, detail=f"max err = {su2_err:.3e}")
    check("fermion-space Casimir is 3/4", casimir_err < 1e-12, detail=f"err = {casimir_err:.3e}")
    check(
        "bivector trace Gram matrix is diagonal",
        np.allclose(gram_b, 2.0 * np.eye(3), atol=1e-12),
        detail="Tr(B_a^dag B_b) = 2 delta_ab",
    )

    print()
    print("Part 2: Spatial Gamma_i form an exact weak vector on C^8")
    vec_err_8 = vector_error(B_8, G_SPATIAL_8)
    cas_vec_8 = double_commutator_error(B_8, G_SPATIAL_8, coeff=2.0)
    gram_g = gram_matrix(G_SPATIAL_8)
    avg_conj_err = 0.0
    for G in G_SPATIAL_8:
        avg_conj_err = max(avg_conj_err, float(np.linalg.norm(sum(B @ G @ B for B in B_8) + 0.25 * G)))
    print(f"  max vector-law error = {vec_err_8:.3e}")
    print(f"  max double-commutator error = {cas_vec_8:.3e}")
    print(f"  max sum_a B_a G_i B_a + (1/4) G_i error = {avg_conj_err:.3e}")
    print()
    check("Gamma_i obey exact weak-vector commutator law", vec_err_8 < 1e-12)
    check("Gamma_i carry spin-1 Casimir", cas_vec_8 < 1e-12, detail="sum_a ad(B_a)^2 = 2")
    check(
        "Gamma_i are trace-orthogonal",
        np.allclose(gram_g, 8.0 * np.eye(3), atol=1e-12),
        detail="Tr(Gamma_i^dag Gamma_j) = 8 delta_ij",
    )
    check("conjugation average matches vector identity", avg_conj_err < 1e-12)

    print()
    print("Part 3: Chiral bridges Y_i = P_R Gamma_i P_L form the same weak vector on C^16")
    gamma5_comm = max(float(np.linalg.norm(B @ GAMMA5_4D - GAMMA5_4D @ B)) for B in B_16)
    vec_err_16 = vector_error(B_16, Y_BRIDGES)
    cas_vec_16 = double_commutator_error(B_16, Y_BRIDGES, coeff=2.0)
    gram_y = gram_matrix(Y_BRIDGES)
    print(f"  max [B_a, gamma_5] error = {gamma5_comm:.3e}")
    print(f"  max bridge vector-law error = {vec_err_16:.3e}")
    print(f"  max bridge double-commutator error = {cas_vec_16:.3e}")
    print()
    check("weak generators commute with gamma_5", gamma5_comm < 1e-12)
    check("bridge family obeys exact weak-vector commutator law", vec_err_16 < 1e-12)
    check("bridge family carries spin-1 Casimir", cas_vec_16 < 1e-12, detail="sum_a ad(B_a)^2 = 2")
    check(
        "bridge family is trace-orthogonal",
        np.allclose(gram_y, 8.0 * np.eye(3), atol=1e-12),
        detail="Tr(Y_i^dag Y_j) = 8 delta_ij",
    )

    print()
    print("Part 4: Weak-vector covariance does not fix absolute normalization")
    lambdas = [0.5, math.sqrt(2.0), 2.0]
    for lam in lambdas:
        scaled = [lam * Y for Y in Y_BRIDGES]
        err_cov = vector_error(B_16, scaled)
        err_cas = double_commutator_error(B_16, scaled, coeff=2.0)
        gram_scaled = gram_matrix(scaled)
        print(f"  lambda = {lam:.6f}: max cov err = {err_cov:.3e}, max Casimir err = {err_cas:.3e}")
        check(
            f"scaled family lambda={lam:.6f} preserves weak-vector covariance",
            err_cov < 1e-12 and err_cas < 1e-12,
            detail=f"Tr-scaled norm = {gram_scaled[0,0].real:.6f}",
        )

    print()
    print("Honest read:")
    print("  1. The direct local chiral bridges Y_i = P_R Gamma_i P_L are now an")
    print("     exact weak-vector family, not just an axis-picked operator guess.")
    print("  2. This is real theorem-grade progress: the bridge family carries the")
    print("     spin-1 Casimir and exact adjoint SU(2) transformation law.")
    print("  3. But covariance alone is homogeneous. Rescaled families lambda Y_i")
    print("     satisfy the same weak-vector equations, so the representation law")
    print("     does not by itself select the physical base normalization.")
    print("  4. The later bosonic-normalization theorem closes that base step.")
    print("     What remains beyond this runner is the second-order suppression")
    print("     law, not weak-vector classification.")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
