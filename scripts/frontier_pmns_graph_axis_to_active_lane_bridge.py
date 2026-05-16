#!/usr/bin/env python3
"""
Graph-axis -> active Hermitian lane bridge for the PMNS graph-first alignment.

This runner exercises the bridge lemma documented in
`docs/PMNS_GRAPH_AXIS_TO_ACTIVE_LANE_BRIDGE_NOTE.md`.

Setup:
  C^8 = (C^2)^{otimes 3} with canonical cube-shifts
      S_1 = sigma_x ⊗ I ⊗ I,
      S_2 = I ⊗ sigma_x ⊗ I,
      S_3 = I ⊗ I ⊗ sigma_x.
  hw=1 carrier  V_1 = span(X_1, X_2, X_3),  X_mu := S_mu |000>.
  Axis permutation sigma in S_3 acts on C^8 by tensor-factor permutation
      T_sigma |b_1 b_2 b_3> := |b_{sigma^{-1}(1)} b_{sigma^{-1}(2)} b_{sigma^{-1}(3)}>.

We check:
  1. Each T_sigma is unitary and conjugates S_mu to S_{sigma(mu)}.
  2. Each T_sigma preserves V_1 and sends X_mu to X_{sigma(mu)}.
  3. The restriction T_sigma|_{V_1} in basis (X_1, X_2, X_3) is the permutation
     matrix P_sigma; in particular T_(23)|_{V_1} = P_23.
  4. A Hermitian H on V_1 is invariant under the residual Z_2 stabilizer of
     axis e_1 if and only if P_23 H P_23 = H.
  5. The aligned core H = [[a,b,b],[b,c,d],[b,d,c]] used by the parent note
     satisfies the bridge invariance.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np


np.set_printoptions(precision=8, suppress=True, linewidth=120)


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
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
    return condition


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
I8 = np.eye(8, dtype=complex)
P23 = np.array(
    [
        [1, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
    ],
    dtype=complex,
)


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def build_cube_shifts() -> list[np.ndarray]:
    return [
        kron3(SX, I2, I2),
        kron3(I2, SX, I2),
        kron3(I2, I2, SX),
    ]


def computational_basis() -> dict[tuple[int, int, int], np.ndarray]:
    e0 = np.array([1.0, 0.0], dtype=complex)
    e1 = np.array([0.0, 1.0], dtype=complex)
    es = [e0, e1]
    table: dict[tuple[int, int, int], np.ndarray] = {}
    for bits in itertools.product((0, 1), repeat=3):
        table[bits] = np.kron(es[bits[0]], np.kron(es[bits[1]], es[bits[2]]))
    return table


def bits_to_index(bits: tuple[int, int, int]) -> int:
    return bits[0] * 4 + bits[1] * 2 + bits[2]


def factor_permutation(sigma: tuple[int, int, int]) -> np.ndarray:
    """
    Tensor-factor permutation unitary on C^8.

    Convention: sigma is a permutation of (1,2,3) given as a 3-tuple of images
    of (1,2,3) (1-indexed). The unitary T_sigma sends
        |b_1 b_2 b_3> -> |b_{sigma^{-1}(1)} b_{sigma^{-1}(2)} b_{sigma^{-1}(3)}>,
    so that T_sigma S_mu T_sigma^dagger = S_{sigma(mu)}.
    """
    # 1-indexed sigma; convert to 0-indexed
    sig0 = [s - 1 for s in sigma]
    inv = [0, 0, 0]
    for i, s in enumerate(sig0):
        inv[s] = i
    U = np.zeros((8, 8), dtype=complex)
    for bits in itertools.product((0, 1), repeat=3):
        new_bits = (bits[inv[0]], bits[inv[1]], bits[inv[2]])
        row = bits_to_index(new_bits)
        col = bits_to_index(bits)
        U[row, col] = 1.0
    return U


def all_sigmas() -> list[tuple[int, int, int]]:
    return list(itertools.permutations((1, 2, 3)))


def perm_matrix_3(sigma: tuple[int, int, int]) -> np.ndarray:
    P = np.zeros((3, 3), dtype=complex)
    for i, s in enumerate(sigma, start=1):
        # sigma sends mu = i to s; P e_i = e_s
        P[s - 1, i - 1] = 1.0
    return P


def hw1_basis(shifts: list[np.ndarray]) -> np.ndarray:
    cb = computational_basis()
    vac = cb[(0, 0, 0)]
    cols = [shifts[mu] @ vac for mu in range(3)]
    return np.stack(cols, axis=1)  # 8 x 3


def part1_shift_triplet_covariance() -> None:
    print("\n" + "=" * 88)
    print("PART 1: T_sigma is unitary and conjugates S_mu to S_{sigma(mu)}")
    print("=" * 88)

    shifts = build_cube_shifts()
    for sigma in all_sigmas():
        T = factor_permutation(sigma)
        check(
            f"T_{sigma} is unitary",
            np.allclose(T @ T.conj().T, I8, atol=1e-12)
            and np.allclose(T.conj().T @ T, I8, atol=1e-12),
        )
        ok = True
        for mu in range(3):
            target = shifts[sigma[mu] - 1]
            actual = T @ shifts[mu] @ T.conj().T
            if not np.allclose(actual, target, atol=1e-12):
                ok = False
                break
        check(f"T_{sigma} S_mu T_{sigma}^dagger = S_(sigma(mu)) for all mu", ok)


def part2_carrier_invariance() -> None:
    print("\n" + "=" * 88)
    print("PART 2: T_sigma preserves V_1 and sends X_mu to X_{sigma(mu)}")
    print("=" * 88)

    shifts = build_cube_shifts()
    V = hw1_basis(shifts)
    G = V.conj().T @ V
    check(
        "(X_1, X_2, X_3) is orthonormal in C^8",
        np.allclose(G, np.eye(3), atol=1e-12),
    )

    for sigma in all_sigmas():
        T = factor_permutation(sigma)
        ok = True
        for mu in range(3):
            image = T @ V[:, mu]
            expected = V[:, sigma[mu] - 1]
            if not np.allclose(image, expected, atol=1e-12):
                ok = False
                break
        check(f"T_{sigma} X_mu = X_(sigma(mu)) for all mu", ok)

        img = T @ V
        coords, *_ = np.linalg.lstsq(V, img, rcond=None)
        residual = float(np.linalg.norm(V @ coords - img))
        check(
            f"T_{sigma} preserves V_1 (least-squares residual ~ 0)",
            residual < 1e-10,
            f"residual={residual:.2e}",
        )


def part3_permutation_block() -> None:
    print("\n" + "=" * 88)
    print("PART 3: T_sigma|_{V_1} = P_sigma in basis (X_1, X_2, X_3)")
    print("=" * 88)

    shifts = build_cube_shifts()
    V = hw1_basis(shifts)

    for sigma in all_sigmas():
        T = factor_permutation(sigma)
        block = V.conj().T @ T @ V
        target = perm_matrix_3(sigma)
        check(
            f"V_1-block of T_{sigma} equals permutation matrix P_{sigma}",
            np.allclose(block, target, atol=1e-12),
        )

    tau = (1, 3, 2)
    T_tau = factor_permutation(tau)
    block = V.conj().T @ T_tau @ V
    check(
        "V_1-block of T_(2 3) equals P_23 exactly",
        np.allclose(block, P23, atol=1e-12),
    )


def part4_active_lane_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 4: residual Z_2 invariance on V_1 is exactly P_23 H P_23 = H")
    print("=" * 88)

    shifts = build_cube_shifts()
    V = hw1_basis(shifts)
    tau = (1, 3, 2)
    T_tau = factor_permutation(tau)
    block = V.conj().T @ T_tau @ V

    check(
        "T_(2 3)|_{V_1} squares to identity (Z_2 action)",
        np.allclose(block @ block, np.eye(3), atol=1e-12),
    )

    rng = np.random.default_rng(0)
    for trial in range(20):
        A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        H_arbitrary = 0.5 * (A + A.conj().T)
        H_inv = 0.5 * (H_arbitrary + block @ H_arbitrary @ block)
        check(
            f"trial {trial}: projection to Z_2-invariant subalgebra satisfies P_23 H P_23 = H",
            np.allclose(block @ H_inv @ block, H_inv, atol=1e-12),
        )
        check(
            f"trial {trial}: projection is Hermitian",
            np.allclose(H_inv, H_inv.conj().T, atol=1e-12),
        )

    # Forward direction: any P_23-invariant Hermitian is Z_2-invariant on V_1.
    for trial in range(5):
        a = float(rng.normal())
        b = float(rng.normal())
        c = float(rng.normal())
        d = float(rng.normal())
        H = np.array([[a, b, b], [b, c, d], [b, d, c]], dtype=complex)
        check(
            f"aligned-core trial {trial}: H is P_23-invariant",
            np.allclose(P23 @ H @ P23, H, atol=1e-12),
        )
        # Lift to V_1 and check Z_2 invariance under T_tau on the embedded operator.
        H_emb = V @ H @ V.conj().T
        check(
            f"aligned-core trial {trial}: V_1-embedded H is T_(2 3)-invariant",
            np.allclose(T_tau @ H_emb @ T_tau.conj().T, H_emb, atol=1e-10),
        )


def part5_consistency_with_parent_aligned_core() -> None:
    print("\n" + "=" * 88)
    print("PART 5: bridge composes with the parent aligned-core form")
    print("=" * 88)

    H = np.array(
        [
            [1.10, 0.26, 0.26],
            [0.26, 0.81, 0.17],
            [0.26, 0.17, 0.81],
        ],
        dtype=complex,
    )
    check(
        "aligned core [[a,b,b],[b,c,d],[b,d,c]] is P_23-invariant",
        np.allclose(P23 @ H @ P23, H, atol=1e-12),
    )

    # And conversely: the Z_2-invariant Hermitian normal form on V_1 with the
    # selected axis at index 1 has exactly the parent aligned-core grammar
    # b_12 = b_13, c_22 = c_33, d_23 real (a single real degree of freedom).
    rng = np.random.default_rng(1)
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    H_inv = 0.25 * (
        (A + A.conj().T) + P23 @ (A + A.conj().T) @ P23
    )
    check(
        "Z_2-invariant Hermitian on V_1 satisfies H[0,1] == H[0,2]",
        np.isclose(H_inv[0, 1], H_inv[0, 2], atol=1e-12),
    )
    check(
        "Z_2-invariant Hermitian on V_1 satisfies H[1,1] == H[2,2]",
        np.isclose(H_inv[1, 1], H_inv[2, 2], atol=1e-12),
    )
    check(
        "Z_2-invariant Hermitian on V_1 satisfies H[1,2] == H[2,1] (Hermiticity + P_23)",
        np.isclose(H_inv[1, 2], H_inv[2, 1], atol=1e-12),
    )


def main() -> int:
    print("=" * 88)
    print("PMNS GRAPH-AXIS -> ACTIVE HERMITIAN LANE BRIDGE")
    print("=" * 88)
    print()
    print("Bridge lemma: the residual Z_2 stabilizer of the graph-first selected")
    print("axis on V_1 acts on the active Hermitian lane Herm(V_1) exactly by the")
    print("permutation matrix P_23 (after relabeling the selected axis to e_1).")

    part1_shift_triplet_covariance()
    part2_carrier_invariance()
    part3_permutation_block()
    part4_active_lane_bridge()
    part5_consistency_with_parent_aligned_core()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
