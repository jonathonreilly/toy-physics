#!/usr/bin/env python3
"""
Neutrino Dirac Bridge Theorem
=============================

STATUS: EXACT operator-selection bridge; base normalization closed elsewhere

Purpose:
  Close the cleanest part of the neutrino-Yukawa bridge:

    1. identify the physical post-EWSB local chiral Dirac operator on C^16
    2. show why the effective action on the generation triplet T_1 starts
       only at second order

  The theorem proved here is:

    - on the 3+1 completed lattice, the graph-local spatial Higgs family
      M(phi) = sum_i phi_i Gamma_i is chiral off-diagonal
    - the exact selector V_sel picks axis minima phi = e_i
    - after EWSB axis selection, the local Dirac surface is uniquely Gamma_i
      up to the broken S_3 choice and an overall sign
    - in the branch convention with weak axis 1, this gives Gamma_1
    - restricted to the T_1 generation triplet, Gamma_1 has no one-hop
      return, so the first exact closed action on T_1 is second order

  This does NOT derive the neutrino-sector normalization or the eventual
  y_nu scale. It closes operator selection on the local chiral surface.
"""

from __future__ import annotations

import itertools
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
I16 = np.eye(16, dtype=complex)


def kron4(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.kron(a, np.kron(b, np.kron(c, d)))


G0 = kron4(SZ, SZ, SZ, SX)
G1 = kron4(SX, I2, I2, I2)
G2 = kron4(SZ, SX, I2, I2)
G3 = kron4(SZ, SZ, SX, I2)
SPATIAL_GAMMAS = [G1, G2, G3]
GAMMA_5_4D = G0 @ G1 @ G2 @ G3
XI_5 = G1 @ G2 @ G3 @ G0

P_L = (I16 + GAMMA_5_4D) / 2.0
P_R = (I16 - GAMMA_5_4D) / 2.0

SPATIAL_STATES = [(a, b, c) for a in range(2) for b in range(2) for c in range(2)]
FULL_STATES = [(a, b, c, t) for a in range(2) for b in range(2) for c in range(2) for t in range(2)]
INDEX = {state: i for i, state in enumerate(FULL_STATES)}

O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
O3 = [(1, 1, 1)]


def selector_potential(phi: tuple[float, float, float]) -> float:
    return 32.0 * sum(phi[i] ** 2 * phi[j] ** 2 for i in range(3) for j in range(i + 1, 3))


def normalized_simplex_grid(step: float = 0.05) -> list[np.ndarray]:
    n = int(round(1.0 / step))
    pts = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            k = n - i - j
            pts.append(np.array([i, j, k], dtype=float) / n)
    return pts


def m_phi(phi: tuple[float, float, float]) -> np.ndarray:
    return sum(c * g for c, g in zip(phi, SPATIAL_GAMMAS))


def projector(spatial_states: list[tuple[int, int, int]]) -> np.ndarray:
    p = np.zeros((16, 16), dtype=complex)
    for t in (0, 1):
        for s in spatial_states:
            p[INDEX[s + (t,)], INDEX[s + (t,)]] = 1.0
    return p


def pretty_matrix(matrix: np.ndarray) -> str:
    rows = []
    for row in matrix:
        entries = " ".join(f"{val.real:5.1f}" for val in row)
        rows.append(f"    [{entries} ]")
    return "\n".join(rows)


def rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1e-12))


def main() -> int:
    print("=" * 78)
    print("NEUTRINO DIRAC BRIDGE THEOREM")
    print("=" * 78)
    print()
    print("Candidate local post-EWSB family:")
    print("  M(phi) = phi_1 Gamma_1 + phi_2 Gamma_2 + phi_3 Gamma_3")
    print("  with phi on the selector surface V_sel = 32 sum_{i<j} phi_i^2 phi_j^2")
    print()

    sample_phis = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 1.0, 1.0),
        (1.0, 2.0, 3.0),
    ]

    print("Part 1: Local chiral Dirac family on C^16")
    for phi in sample_phis:
        M = m_phi(phi)
        norm2 = float(sum(x * x for x in phi))
        anti = np.linalg.norm(M @ GAMMA_5_4D + GAMMA_5_4D @ M)
        sq = np.linalg.norm(M @ M - norm2 * I16)
        ll = rank(P_L @ M @ P_L)
        rr = rank(P_R @ M @ P_R)
        rl = rank(P_R @ M @ P_L)
        check(f"{{M(phi), gamma_5}} = 0 for phi={phi}", anti < 1e-12)
        check(f"M(phi)^2 = |phi|^2 I for phi={phi}", sq < 1e-12)
        check(
            f"M(phi) is purely chiral off-diagonal for phi={phi}",
            ll == 0 and rr == 0 and (rl == 0 if norm2 == 0 else rl == 8),
            detail=f"rank(PR M PL) = {rl}",
        )

    print()
    print("Part 2: Exact selector chooses the weak axis")
    vertices = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
    ]
    for idx, vertex in enumerate(vertices, start=1):
        value = selector_potential(tuple(vertex))
        check(f"V_sel(e_{idx}) = 0", abs(value) < 1e-12, detail=f"V = {value:.1f}")

    pts = normalized_simplex_grid(step=0.05)
    values = np.array([sum(p[i] * p[j] for i in range(3) for j in range(i + 1, 3)) for p in pts])
    min_val = float(values.min())
    mins = [p for p, val in zip(pts, values) if abs(val - min_val) < 1e-12]
    exact_vertices = all(any(np.allclose(p, v, atol=1e-12) for v in vertices) for p in mins)
    check("Normalized selector minima are axis vertices", exact_vertices, detail=f"{len(mins)} minima on coarse simplex")
    check("V_sel(1,1,0) > 0", selector_potential((1.0, 1.0, 0.0)) > 0.0)
    check("V_sel(1,1,1) > 0", selector_potential((1.0, 1.0, 1.0)) > 0.0)

    print()
    print("Part 3: Post-EWSB operator selection")
    axis_ops = [m_phi(tuple(v)) for v in vertices]
    for idx, op in enumerate(axis_ops, start=1):
        check(f"M(e_{idx}) = Gamma_{idx}", np.allclose(op, SPATIAL_GAMMAS[idx - 1], atol=1e-12))

    check(
        "Xi_5 is excluded as direct Dirac operator",
        np.linalg.norm(XI_5 @ GAMMA_5_4D - GAMMA_5_4D @ XI_5) < 1e-12
        and rank(P_R @ XI_5 @ P_L) == 0,
        detail="Xi_5 commutes with gamma_5 and has zero LR block",
    )

    print()
    print("Part 4: Minimal operator order on the generation triplet")
    p_o0 = projector(O0)
    p_t1 = projector(T1)
    p_t2 = projector(T2)
    p_o3 = projector(O3)

    one_hop_t1 = p_t1 @ G1 @ p_t1
    second_via_o0_t2 = p_t1 @ G1 @ (p_o0 + p_t2) @ G1 @ p_t1
    second_via_all = p_t1 @ G1 @ (p_o0 + p_t2 + p_o3) @ G1 @ p_t1

    t1_basis_cols = []
    for t in (0, 1):
        for s in T1:
            e = np.zeros((16, 1), dtype=complex)
            e[INDEX[s + (t,)], 0] = 1.0
            t1_basis_cols.append(e)
    basis_t1 = np.hstack(t1_basis_cols)
    one_hop_restricted = basis_t1.conj().T @ one_hop_t1 @ basis_t1
    second_restricted = basis_t1.conj().T @ second_via_o0_t2 @ basis_t1
    second_all_restricted = basis_t1.conj().T @ second_via_all @ basis_t1

    print("  P_T1 Gamma_1 P_T1 =")
    print(pretty_matrix(one_hop_restricted))
    print()
    print("  P_T1 Gamma_1 (P_O0 + P_T2) Gamma_1 P_T1 =")
    print(pretty_matrix(second_restricted))
    print()

    check(
        "No one-hop return on T1",
        np.allclose(one_hop_restricted, np.zeros_like(one_hop_restricted), atol=1e-12),
    )
    check(
        "Second order closes on T1 through O0 + T2",
        np.allclose(second_restricted, np.eye(second_restricted.shape[0]), atol=1e-12),
    )
    check(
        "O3 does not contribute to the first closed T1 return",
        np.allclose(second_all_restricted, second_restricted, atol=1e-12),
    )

    print()
    print("Honest read:")
    print("  1. On the 3+1 completed lattice, the local spatial Higgs family")
    print("     M(phi) is exactly chiral off-diagonal.")
    print("  2. The exact selector picks axis minima, so after EWSB the local")
    print("     post-EWSB Dirac surface is uniquely Gamma_i up to S_3 / sign.")
    print("  3. In the branch convention with weak axis 1, that operator is Gamma_1.")
    print("  4. Xi_5 is not a direct Dirac Yukawa surface because it is chiral")
    print("     diagonal rather than chiral off-diagonal.")
    print("  5. The effective action on the T_1 generation triplet starts only")
    print("     at second order, which is exactly why the neutrino cascade")
    print("     mechanism remains relevant after operator selection closes.")
    print("  6. What remains open is the neutrino-sector normalization /")
    print("     suppression theorem, not the Gamma_1 versus Xi_5 choice.")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
