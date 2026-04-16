#!/usr/bin/env python3
"""
DM Neutrino Operator Selection Obstruction
==========================================

STATUS: EXACT obstruction, not closure

Purpose:
  Isolate the operator-selection gap behind the current neutrino-Yukawa
  blocker. The branch currently uses two different framework-native operator
  surfaces:

    1. Xi_5  -- the exact staggered mass operator used in the y_t notes
    2. Gamma_1 -- the weak-axis EWSB insertion used in the generation /
                  neutrino cascade notes

  The point of this runner is not to choose one. The point is to show, using
  exact operator algebra on the current branch conventions, that they are
  genuinely different objects:

    - different chirality behavior in the 3+1 completion
    - different locality / hop order on the taste cube
    - different orbit-level action on O_0 / T_1 / T_2 / O_3

  That is the formal obstruction: the branch does not yet derive why the
  physical neutrino Dirac Yukawa should live on one surface rather than the
  other.
"""

from __future__ import annotations

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
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


# 4D KS operators from the existing branch conventions.
G0 = kron4(SZ, SZ, SZ, SX)
G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)
G4 = kron4(SZ, SZ, SZ, SX)

GAMMA_1 = G1
XI_5 = G1 @ G2 @ G3 @ G4
GAMMA_5_4D = G0 @ G1 @ G2 @ G3

I16 = np.eye(16, dtype=complex)
P_L = (I16 + GAMMA_5_4D) / 2.0
P_R = (I16 - GAMMA_5_4D) / 2.0

STATES = [(a, b, c, d) for a in range(2) for b in range(2) for c in range(2) for d in range(2)]
INDEX = {state: i for i, state in enumerate(STATES)}

O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
O3 = [(1, 1, 1)]


def hamming_distance(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    return sum(int(x != y) for x, y in zip(a, b))


def projector(spatial_states: list[tuple[int, int, int]]) -> np.ndarray:
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            idx = INDEX[s + (t,)]
            p[idx, idx] = 1.0
    return p


def unique_image_distances(operator: np.ndarray) -> list[int]:
    distances = []
    for source in STATES:
        column = operator[:, INDEX[source]]
        nz = np.where(np.abs(column) > 1e-12)[0]
        if len(nz) != 1:
            raise RuntimeError("expected permutation-like action")
        target = STATES[nz[0]]
        distances.append(hamming_distance(source, target))
    return distances


def rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1e-12))


def main() -> int:
    print("=" * 78)
    print("DM NEUTRINO OPERATOR SELECTION OBSTRUCTION")
    print("=" * 78)
    print()
    print("Operators under audit:")
    print("  Xi_5    = G1 G2 G3 G4   (staggered mass / taste-chirality surface)")
    print("  Gamma_1 = G1            (weak-axis EWSB insertion)")
    print()

    check("Gamma_1 is Hermitian involution",
          np.allclose(GAMMA_1, GAMMA_1.conj().T, atol=1e-12)
          and np.allclose(GAMMA_1 @ GAMMA_1, I16, atol=1e-12))
    check("Xi_5 is Hermitian involution",
          np.allclose(XI_5, XI_5.conj().T, atol=1e-12)
          and np.allclose(XI_5 @ XI_5, I16, atol=1e-12))

    print()
    print("3+1 chirality behavior:")
    gamma1_comm = np.linalg.norm(GAMMA_1 @ GAMMA_5_4D - GAMMA_5_4D @ GAMMA_1)
    gamma1_anti = np.linalg.norm(GAMMA_1 @ GAMMA_5_4D + GAMMA_5_4D @ GAMMA_1)
    xi5_comm = np.linalg.norm(XI_5 @ GAMMA_5_4D - GAMMA_5_4D @ XI_5)
    xi5_anti = np.linalg.norm(XI_5 @ GAMMA_5_4D + GAMMA_5_4D @ XI_5)
    print(f"  ||[Gamma_1, gamma_5]|| = {gamma1_comm:.1f}")
    print(f"  ||{{Gamma_1, gamma_5}}|| = {gamma1_anti:.1f}")
    print(f"  ||[Xi_5, gamma_5]|| = {xi5_comm:.1f}")
    print(f"  ||{{Xi_5, gamma_5}}|| = {xi5_anti:.1f}")
    print()

    check("Gamma_1 anticommutes with 4D gamma_5",
          gamma1_anti < 1e-12 and gamma1_comm > 1.0)
    check("Xi_5 commutes with 4D gamma_5",
          xi5_comm < 1e-12 and xi5_anti > 1.0)

    g1_rl = rank(P_R @ GAMMA_1 @ P_L)
    g1_ll = rank(P_L @ GAMMA_1 @ P_L)
    xi5_rl = rank(P_R @ XI_5 @ P_L)
    xi5_ll = rank(P_L @ XI_5 @ P_L)
    xi5_rr = rank(P_R @ XI_5 @ P_R)
    print("Chiral block ranks:")
    print(f"  rank(P_R Gamma_1 P_L) = {g1_rl}")
    print(f"  rank(P_L Gamma_1 P_L) = {g1_ll}")
    print(f"  rank(P_R Xi_5 P_L)    = {xi5_rl}")
    print(f"  rank(P_L Xi_5 P_L)    = {xi5_ll}")
    print(f"  rank(P_R Xi_5 P_R)    = {xi5_rr}")
    print()

    check("Gamma_1 is chiral off-diagonal",
          g1_rl == 8 and g1_ll == 0)
    check("Xi_5 is chiral diagonal",
          xi5_rl == 0 and xi5_ll == 8 and xi5_rr == 8)

    print("Hop order on the 4-bit cube:")
    gamma1_distances = unique_image_distances(GAMMA_1)
    xi5_distances = unique_image_distances(XI_5)
    print(f"  Gamma_1 image distances = {sorted(set(gamma1_distances))}")
    print(f"  Xi_5 image distances    = {sorted(set(xi5_distances))}")
    print()

    check("Gamma_1 is single-hop on every basis state",
          set(gamma1_distances) == {1})
    check("Xi_5 is four-hop on every basis state",
          set(xi5_distances) == {4})

    p_o0 = projector(O0)
    p_t1 = projector(T1)
    p_t2 = projector(T2)
    p_o3 = projector(O3)

    gamma1_blocks = {
        "O0 <- T1": rank(p_o0 @ GAMMA_1 @ p_t1),
        "T1 <- O0": rank(p_t1 @ GAMMA_1 @ p_o0),
        "T2 <- T1": rank(p_t2 @ GAMMA_1 @ p_t1),
        "T1 <- T2": rank(p_t1 @ GAMMA_1 @ p_t2),
        "O3 <- T2": rank(p_o3 @ GAMMA_1 @ p_t2),
        "T2 <- O3": rank(p_t2 @ GAMMA_1 @ p_o3),
    }
    xi5_blocks = {
        "O0 <- O3": rank(p_o0 @ XI_5 @ p_o3),
        "O3 <- O0": rank(p_o3 @ XI_5 @ p_o0),
        "T1 <- T2": rank(p_t1 @ XI_5 @ p_t2),
        "T2 <- T1": rank(p_t2 @ XI_5 @ p_t1),
    }

    print("Spatial-orbit action:")
    print("  Gamma_1:")
    for label, value in gamma1_blocks.items():
        print(f"    {label:<10s} rank = {value}")
    print("  Xi_5:")
    for label, value in xi5_blocks.items():
        print(f"    {label:<10s} rank = {value}")
    print()

    check("Gamma_1 follows the adjacent-hamming cascade",
          gamma1_blocks == {
              "O0 <- T1": 2,
              "T1 <- O0": 2,
              "T2 <- T1": 4,
              "T1 <- T2": 4,
              "O3 <- T2": 2,
              "T2 <- O3": 2,
          })
    check("Xi_5 follows the opposite-corner pairing",
          xi5_blocks == {
              "O0 <- O3": 2,
              "O3 <- O0": 2,
              "T1 <- T2": 6,
              "T2 <- T1": 6,
          })

    print()
    print("Honest read:")
    print("  1. Gamma_1 and Xi_5 are both exact framework-native operators, but")
    print("     they live on different operator classes.")
    print("  2. Gamma_1 is a weak-axis single-hop, chiral off-diagonal insertion.")
    print("  3. Xi_5 is a four-hop, chiral diagonal staggered mass surface.")
    print("  4. The 3+1 completion adds chirality and RH singlets, but it does")
    print("     not derive a bridge from Xi_5 to Gamma_1.")
    print("  5. That bridge is the current theorem-grade blocker behind the")
    print("     neutrino Dirac Yukawa story.")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
