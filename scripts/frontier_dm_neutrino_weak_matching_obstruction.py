#!/usr/bin/env python3
"""
Neutrino Weak Matching Obstruction
==================================

STATUS: EXACT historical obstruction to the old active-space matching route

Purpose:
  Attack the sharpest remaining denominator question directly:

    can the branch derive a theorem-grade active-space matching

        y_nu^(0) = g_weak

    for the direct local Gamma_1 neutrino bridge?

  The exact answer from the current machinery is:

    not by reusing the top-Yukawa Ward / centrality route.

  The top-Yukawa protection works because G5 is central in Cl(3), so Yukawa
  insertions factor through arbitrary gauge / propagator chains. The direct
  neutrino bridge uses Gamma_1, and Gamma_1 is NOT central. The factorization
  step therefore fails.

  What remains true:

    - the direct local bridge P_R Gamma_1 P_L has unit active-space norm
    - the SU(2) doublet normalization still fixes the mass relation m = y*v/sqrt(2)
    - if a new weak-sector matching theorem existed, the natural active-space
      benchmark would be y_nu^(0) = g_weak

  What is not yet true:

    - the branch has no theorem forcing coefficient sharing between the
      weak-sector gauge vertex and the direct Gamma_1 fermion bridge

  This should now be read as a historical negative result. The later
  bosonic-normalization theorem rejects the active-space benchmark as the
  physical selector and instead picks the full-space g_weak/sqrt(2) surface.
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
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = np.eye(8, dtype=complex)
I16 = np.eye(16, dtype=complex)


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, c))


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G1 = kron3(SX, I2, I2)
G2 = kron3(SY, SX, I2)
G3 = kron3(SY, SY, SX)
G5 = 1j * G1 @ G2 @ G3

B1 = -0.5j * G2 @ G3
B2 = -0.5j * G3 @ G1
B3 = -0.5j * G1 @ G2

G0_4D = kron4(SZ, SZ, SZ, SX)
G1_4D = kron4(SX, I2, I2, I2)
G2_4D = kron4(SZ, SX, I2, I2)
G3_4D = kron4(SZ, SZ, SX, I2)
GAMMA5_4D = G0_4D @ G1_4D @ G2_4D @ G3_4D
P_L = (I16 + GAMMA5_4D) / 2.0
P_R = (I16 - GAMMA5_4D) / 2.0
Y_BRIDGE = P_R @ G1_4D @ P_L


def taste_propagator(k: tuple[float, float, float], m: float) -> np.ndarray:
    d_inv = m * G5 + 0j
    for mu, gamma in enumerate((G1, G2, G3)):
        d_inv = d_inv + 1j * math.sin(k[mu]) * gamma
    return np.linalg.inv(d_inv)


def main() -> int:
    print("=" * 78)
    print("NEUTRINO WEAK MATCHING OBSTRUCTION")
    print("=" * 78)
    print()

    print("Part 1: Exact retained positives")
    active_ratio = np.linalg.svd(Y_BRIDGE, compute_uv=False).max() / np.linalg.svd(G1_4D, compute_uv=False).max()
    print(f"  operator-norm ratio on active bridge = {active_ratio:.6f}")
    print("  Higgs doublet mass relation remains m = y*v/sqrt(2)")
    print("  this runner tests only the old active-space y = g_weak route")
    print()
    check("active bridge has unit operator norm",
          abs(active_ratio - 1.0) < 1e-12,
          detail=f"ratio = {active_ratio:.12f}")

    print()
    print("Part 2: Gamma_1 is not central")
    central_tests = [
        ("[Gamma_1, Gamma_2]", np.linalg.norm(G1 @ G2 - G2 @ G1)),
        ("[Gamma_1, Gamma_3]", np.linalg.norm(G1 @ G3 - G3 @ G1)),
        ("[Gamma_1, B_1]", np.linalg.norm(G1 @ B1 - B1 @ G1)),
        ("[Gamma_1, B_2]", np.linalg.norm(G1 @ B2 - B2 @ G1)),
        ("[Gamma_1, B_3]", np.linalg.norm(G1 @ B3 - B3 @ G1)),
    ]
    for label, value in central_tests:
        print(f"  {label:<18s} = {value:.6f}")

    check("Gamma_1 fails centrality in Cl(3)",
          central_tests[0][1] > 1e-12 and central_tests[1][1] > 1e-12,
          detail="commutators with Gamma_2 and Gamma_3 are nonzero")
    check("Gamma_1 does not commute with all weak generators",
          central_tests[3][1] > 1e-12 and central_tests[4][1] > 1e-12,
          detail="B_2 and B_3 commutators are nonzero")
    check("Gamma_1 commutes with only one weak generator",
          central_tests[2][1] < 1e-12,
          detail="B_1 commutator vanishes, but this is not enough for centrality")

    print()
    print("Part 3: Propagator / chain factorization fails")
    k_generic = (0.37, 0.91, 1.23)
    m_generic = 0.41
    s_generic = taste_propagator(k_generic, m_generic)
    fail_prop = np.linalg.norm(s_generic @ G1 - G1 @ s_generic)
    print(f"  ||S(k) Gamma_1 - Gamma_1 S(k)|| = {fail_prop:.6e} at k={k_generic}")
    check("Gamma_1 does not factor through generic propagator",
          fail_prop > 1e-8,
          detail=f"norm = {fail_prop:.3e}")

    chain = B2 @ s_generic @ B3
    fail_chain = np.linalg.norm(chain @ G1 - G1 @ chain)
    print(f"  ||(B2 S B3) Gamma_1 - Gamma_1 (B2 S B3)|| = {fail_chain:.6e}")
    check("Gamma_1 does not factor through gauge-vertex chain",
          fail_chain > 1e-8,
          detail=f"norm = {fail_chain:.3e}")

    print()
    print("Part 4: Comparison to the top-Yukawa mechanism")
    g5_central = max(
        np.linalg.norm(G5 @ x - x @ G5)
        for x in (I8, G1, G2, G3, B1, B2, B3)
    )
    print(f"  max_X ||[G5, X]|| over Cl(3) generators/bivectors = {g5_central:.6e}")
    check("G5 remains central in the comparison set",
          g5_central < 1e-12,
          detail=f"max = {g5_central:.3e}")
    check("Gamma_1 obstruction is genuinely different from G5 lane",
          fail_chain > 1e-8 and g5_central < 1e-12,
          detail="top-Yukawa factorization route does not transfer")

    print()
    print("Honest read:")
    print("  1. The direct local neutrino bridge is fixed, and its active-space")
    print("     operator norm is exactly unit.")
    print("  2. The standard Higgs doublet factor v/sqrt(2) is still exact, but")
    print("     this runner only addresses the historical active-space benchmark.")
    print("  3. But the top-Yukawa protection mechanism does not recycle here:")
    print("     Gamma_1 is non-central and fails propagator / gauge-chain")
    print("     factorization.")
    print("  4. So this specific route stays negative: the old active-space")
    print("     y_nu^(0) = g_weak matching claim does not land from top-Yukawa")
    print("     factorization. The later bosonic selector moves the physical")
    print("     benchmark to g_weak/sqrt(2) instead.")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
