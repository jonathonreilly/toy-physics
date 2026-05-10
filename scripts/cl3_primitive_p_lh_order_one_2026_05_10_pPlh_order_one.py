#!/usr/bin/env python3
"""P-LH order-one / staggered-Dirac open-gate diagnostic.

This runner supports
docs/P_LH_ORDER_ONE_STAGGERED_DIRAC_OPEN_GATE_NOTE_2026-05-10_pPlh_order_one.md.

It checks only finite algebra and toy-model facts:

1. R[omega] in a Cl(3) Pauli representation is a copy of C.
2. Cl+(3) bivectors satisfy quaternion relations.
3. Diagonal projectors plus a C3 cycle generate the matrix units of M_3(C).
4. These located algebra types live on different carrier sectors in the
   current repo story, so assembly into one H_F remains an open gate.
5. In a toy direct-sum A_F action, order-one is vacuous for block-scalar D_F
   and violated by a generic Yukawa-like off-diagonal D_F.

The runner does not derive a physical finite Hilbert space, a color carrier,
or a physical order-one theorem.
"""

from __future__ import annotations

import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {label}{suffix}")


def close(a: np.ndarray, b: np.ndarray, tol: float = 1e-12) -> bool:
    return bool(np.max(np.abs(a - b)) < tol)


def rank_over_reals(mats: list[np.ndarray], tol: float = 1e-10) -> int:
    rows = [
        np.concatenate([np.real(mat).reshape(-1), np.imag(mat).reshape(-1)])
        for mat in mats
    ]
    return int(np.linalg.matrix_rank(np.array(rows), tol=tol))


I2 = np.eye(2, dtype=complex)
SIG1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIG2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIG3 = np.array([[1, 0], [0, -1]], dtype=complex)
ZERO2 = np.zeros((2, 2), dtype=complex)


def section_complex_summand() -> None:
    print()
    print("=" * 78)
    print("SECTION 1: R[omega] COPY OF C")
    print("=" * 78)

    omega = SIG1 @ SIG2 @ SIG3
    check("omega equals i I in this Pauli representation", close(omega, 1j * I2))
    check("omega^2 = -I", close(omega @ omega, -I2))

    for idx, gamma in enumerate((SIG1, SIG2, SIG3), start=1):
        comm = omega @ gamma - gamma @ omega
        check(f"omega commutes with gamma_{idx}", close(comm, ZERO2))

    rank = rank_over_reals([I2, omega])
    check("R[omega] has real dimension two", rank == 2, f"rank={rank}")

    a, b, c, d = 1.25, -0.5, 2.0, 0.75
    lhs = (a * I2 + b * omega) @ (c * I2 + d * omega)
    rhs = (a * c - b * d) * I2 + (a * d + b * c) * omega
    check(
        "R[omega] multiplication matches complex multiplication",
        close(lhs, rhs),
        "(a+b omega)(c+d omega)",
    )


def section_quaternion_summand() -> None:
    print()
    print("=" * 78)
    print("SECTION 2: Cl+(3) QUATERNION RELATIONS")
    print("=" * 78)

    e12 = SIG1 @ SIG2
    e13 = SIG1 @ SIG3
    e23 = SIG2 @ SIG3

    iq, jq, kq = e23, e13, e12
    for name, unit in (("i", iq), ("j", jq), ("k", kq)):
        check(f"{name}^2 = -I", close(unit @ unit, -I2))

    check("i j = k", close(iq @ jq, kq))
    check("j k = i", close(jq @ kq, iq))
    check("k i = j", close(kq @ iq, jq))
    check("i j k = -I", close(iq @ jq @ kq, -I2))

    rank = rank_over_reals([I2, e12, e13, e23])
    check("Cl+(3) basis has real dimension four", rank == 4, f"rank={rank}")


def matrix_units_from_cycle() -> tuple[list[np.ndarray], np.ndarray, list[np.ndarray]]:
    p1 = np.zeros((3, 3), dtype=complex)
    p2 = np.zeros((3, 3), dtype=complex)
    p3 = np.zeros((3, 3), dtype=complex)
    p1[0, 0] = 1
    p2[1, 1] = 1
    p3[2, 2] = 1
    cycle = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    cycle2 = cycle @ cycle
    units = [p1, p2, p3, cycle @ p1, cycle @ p2, cycle @ p3, cycle2 @ p1, cycle2 @ p2, cycle2 @ p3]
    return [p1, p2, p3], cycle, units


def section_matrix_summand() -> None:
    print()
    print("=" * 78)
    print("SECTION 3: PROJECTORS PLUS C3 GENERATE M_3(C) MATRIX UNITS")
    print("=" * 78)

    projectors, cycle, units = matrix_units_from_cycle()
    eye3 = np.eye(3, dtype=complex)

    check("projectors are idempotent", all(close(p @ p, p) for p in projectors))
    check("projectors are mutually orthogonal", all(close(projectors[i] @ projectors[j], np.zeros((3, 3), dtype=complex)) for i in range(3) for j in range(3) if i != j))
    check("projectors sum to I_3", close(sum(projectors), eye3))
    check("cycle has order three", close(cycle @ cycle @ cycle, eye3))

    expected = []
    for i in range(3):
        for j in range(3):
            eij = np.zeros((3, 3), dtype=complex)
            eij[i, j] = 1
            expected.append(eij)

    generated_rank = rank_over_reals(units)
    target_rank = rank_over_reals(expected)
    check("generated units span nine real matrix-unit directions", generated_rank == 9, f"rank={generated_rank}")
    check("target matrix-unit span has rank nine", target_rank == 9, f"rank={target_rank}")


def section_assembly_gate() -> None:
    print()
    print("=" * 78)
    print("SECTION 4: CARRIER-SECTOR ASSEMBLY GATE")
    print("=" * 78)

    h_per_site_dim = 4
    h_hw1_dim = 3
    connes_hf_dim = 96

    check("per-site carrier dimension is four in this inventory", h_per_site_dim == 4)
    check("hw=1 carrier dimension is three in this inventory", h_hw1_dim == 3)
    check("the two located carriers are not the same dimension", h_per_site_dim != h_hw1_dim)
    check("naive direct sum has dimension seven", h_per_site_dim + h_hw1_dim == 7)
    check(
        "naive direct sum is not the 96-dimensional Connes-style H_F",
        h_per_site_dim + h_hw1_dim != connes_hf_dim,
        f"4+3={h_per_site_dim + h_hw1_dim}, H_F={connes_hf_dim}",
    )


def algebra_action(lam: complex, q: np.ndarray, m: np.ndarray) -> np.ndarray:
    out = np.zeros((6, 6), dtype=complex)
    out[0, 0] = lam
    out[1:3, 1:3] = q
    out[3:6, 3:6] = m
    return out


def order_one_violation(d_op: np.ndarray, a_op: np.ndarray, b_op: np.ndarray) -> float:
    comm = d_op @ a_op - a_op @ d_op
    jbj = np.conjugate(b_op)
    nested = comm @ jbj - jbj @ comm
    return float(np.max(np.abs(nested)))


def algebra_basis() -> list[np.ndarray]:
    m_units = []
    for i in range(3):
        for j in range(3):
            eij = np.zeros((3, 3), dtype=complex)
            eij[i, j] = 1
            m_units.append(eij)

    q_basis = [I2, SIG1, SIG2, SIG3]
    basis = []
    for lam in (1.0, 1.0j):
        basis.append(algebra_action(lam, np.zeros((2, 2), dtype=complex), np.zeros((3, 3), dtype=complex)))
    for q in q_basis:
        basis.append(algebra_action(0.0, q, np.zeros((3, 3), dtype=complex)))
    for m in m_units:
        basis.append(algebra_action(0.0, np.zeros((2, 2), dtype=complex), m))
    return basis


def section_order_one_toy_model() -> None:
    print()
    print("=" * 78)
    print("SECTION 5: TOY ORDER-ONE SELECTION TEST")
    print("=" * 78)

    basis = algebra_basis()
    check("toy A_F basis has 15 tested generators", len(basis) == 15, f"count={len(basis)}")

    d_block = np.zeros((6, 6), dtype=complex)
    d_block[0, 0] = 1.0
    d_block[1:3, 1:3] = 2.0 * I2
    d_block[3:6, 3:6] = 3.0 * np.eye(3, dtype=complex)

    d_zero = np.zeros((6, 6), dtype=complex)

    d_yuk = np.zeros((6, 6), dtype=complex)
    for i, j, val in ((0, 1, 0.5), (0, 2, 0.3), (1, 3, 0.1), (2, 4, 0.2)):
        d_yuk[i, j] = val
        d_yuk[j, i] = val

    def max_violation(d_op: np.ndarray) -> float:
        return max(order_one_violation(d_op, a, b) for a in basis for b in basis)

    block_violation = max_violation(d_block)
    zero_violation = max_violation(d_zero)
    yuk_violation = max_violation(d_yuk)

    check("D=0 satisfies toy order-one vacuously", zero_violation < 1e-12, f"max={zero_violation:.3e}")
    check("block-scalar D satisfies toy order-one vacuously", block_violation < 1e-12, f"max={block_violation:.3e}")
    check("Yukawa-like off-diagonal D violates toy order-one", yuk_violation > 1e-3, f"max={yuk_violation:.3e}")
    check(
        "toy direct-sum algebra shape does not force order-one",
        zero_violation < 1e-12 and block_violation < 1e-12 and yuk_violation > 1e-3,
        "selection depends on D_F choice",
    )


def main() -> int:
    print("=" * 78)
    print("P-LH ORDER-ONE / STAGGERED-DIRAC OPEN-GATE DIAGNOSTIC")
    print("=" * 78)
    print("Finite algebra and toy-model checks only; no primitive admission.")

    section_complex_summand()
    section_quaternion_summand()
    section_matrix_summand()
    section_assembly_gate()
    section_order_one_toy_model()

    print()
    print("=" * 78)
    print(f"P-LH ORDER-ONE OPEN-GATE DIAGNOSTIC: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
