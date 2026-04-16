#!/usr/bin/env python3
"""
Neutrino Cascade Geometry on the Weak Axis
==========================================

STATUS: EXACT operator geometry, bounded physics interpretation

Purpose:
  Isolate the exact weak-axis Yukawa geometry behind the neutrino-Yukawa
  candidate notes. The key object is the weak-direction Clifford generator
  Gamma_1 acting on the T_1 / O_0 / T_2 taste sectors.

  The exact result is:
    - Gamma_1 maps one T_1 state to the singlet O_0
    - Gamma_1 maps the other two T_1 states to T_2
    - the second-order return operator splits exactly into
        rank-1 singlet channel + rank-2 T_2 channel

  This does NOT yet prove a neutrino Yukawa theorem. It does show why a
  second-order cascade is the first serious exact place to look.
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
GAMMA_1 = np.kron(SX, np.kron(I2, I2))

STATES = [(s1, s2, s3) for s1 in range(2) for s2 in range(2) for s3 in range(2)]
INDEX = {s: i for i, s in enumerate(STATES)}

O0 = [(0, 0, 0)]
T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]


def basis(states: list[tuple[int, int, int]]) -> np.ndarray:
    vecs = []
    eye = np.eye(8, dtype=complex)
    for state in states:
        vecs.append(eye[:, INDEX[state]])
    return np.column_stack(vecs)


def pretty_matrix(matrix: np.ndarray) -> str:
    rows = []
    for row in matrix:
        entries = " ".join(f"{val.real:5.1f}" for val in row)
        rows.append(f"    [{entries} ]")
    return "\n".join(rows)


def main() -> int:
    b0 = basis(O0)
    b1 = basis(T1)
    b2 = basis(T2)

    p0 = b0 @ b0.conj().T
    p1 = b1 @ b1.conj().T
    p2 = b2 @ b2.conj().T

    one_hop_t1_to_t1 = b1.conj().T @ GAMMA_1 @ b1
    one_hop_t1_to_o0 = b0.conj().T @ GAMMA_1 @ b1
    one_hop_t1_to_t2 = b2.conj().T @ GAMMA_1 @ b1

    second_order_via_o0 = b1.conj().T @ GAMMA_1 @ p0 @ GAMMA_1 @ b1
    second_order_via_t2 = b1.conj().T @ GAMMA_1 @ p2 @ GAMMA_1 @ b1
    second_order_total = b1.conj().T @ GAMMA_1 @ (p0 + p2) @ GAMMA_1 @ b1

    print("=" * 78)
    print("NEUTRINO CASCADE GEOMETRY ON THE WEAK AXIS")
    print("=" * 78)
    print()
    print("Taste-sector basis:")
    print(f"  O_0 = {O0}")
    print(f"  T_1 = {T1}")
    print(f"  T_2 = {T2}")
    print()

    print("One-hop weak-axis action:")
    print("  P_T1 Gamma_1 P_T1 =")
    print(pretty_matrix(one_hop_t1_to_t1))
    print()
    print("  P_O0 Gamma_1 P_T1 =")
    print(pretty_matrix(one_hop_t1_to_o0))
    print()
    print("  P_T2 Gamma_1 P_T1 =")
    print(pretty_matrix(one_hop_t1_to_t2))
    print()

    check(
        "no one-hop T1 -> T1 matrix element",
        np.allclose(one_hop_t1_to_t1, np.zeros((3, 3)), atol=1e-12),
        "Gamma_1 maps T_1 out of T_1",
    )
    check(
        "one-hop T1 -> O0 is rank 1",
        np.linalg.matrix_rank(one_hop_t1_to_o0, tol=1e-12) == 1,
        f"rank = {np.linalg.matrix_rank(one_hop_t1_to_o0, tol=1e-12)}",
    )
    check(
        "one-hop T1 -> T2 is rank 2",
        np.linalg.matrix_rank(one_hop_t1_to_t2, tol=1e-12) == 2,
        f"rank = {np.linalg.matrix_rank(one_hop_t1_to_t2, tol=1e-12)}",
    )

    print()
    print("Second-order return operators on T_1:")
    print("  via O_0:")
    print(pretty_matrix(second_order_via_o0))
    print()
    print("  via T_2:")
    print(pretty_matrix(second_order_via_t2))
    print()
    print("  total:")
    print(pretty_matrix(second_order_total))
    print()

    check(
        "singlet channel isolates one mode",
        np.allclose(second_order_via_o0, np.diag([1.0, 0.0, 0.0]), atol=1e-12),
        "via O_0 = diag(1,0,0)",
    )
    check(
        "T2 channel isolates residual pair",
        np.allclose(second_order_via_t2, np.diag([0.0, 1.0, 1.0]), atol=1e-12),
        "via T_2 = diag(0,1,1)",
    )
    check(
        "second-order channels close back to identity on T1",
        np.allclose(second_order_total, np.eye(3), atol=1e-12),
        "via O_0 + via T_2 = I_3",
    )

    print()
    print("Honest read:")
    print("  1. The weak-axis Yukawa insertion does NOT act inside T_1 at one hop.")
    print("  2. It splits exactly into one singlet path and a residual two-state")
    print("     T_2 path.")
    print("  3. That makes a second-order cascade the first exact operator surface")
    print("     where the 1+2 structure is visible without model inputs.")
    print("  4. The physics step from this exact geometry to a neutrino Dirac Yukawa")
    print("     theorem is still open: chirality, sector normalization, and the")
    print("     full 4D operator matching are not closed here.")
    print()
    print("=" * 78)
    print(f"RESULT: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 78)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
