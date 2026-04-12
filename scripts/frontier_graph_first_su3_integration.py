#!/usr/bin/env python3
"""Graph-first SU(3) integration theorem on the selected-axis surface.

This script finishes the graph-first route opened by
`frontier_graph_first_selector_derivation.py`.

Input:
  - the canonical 3-cube taste graph
  - a selected weak axis from the derived graph-first selector

Goal:
  - build the full weak su(2) from graph-native fiber operators
  - derive the residual swap on the complementary base
  - recover the bounded commutant theorem directly from the selected graph axis

This avoids the old native-bivector -> KS bridge bottleneck. The selected axis
is now graph-canonical, and the factorization is the graph projection that
forgets that axis.
"""

from __future__ import annotations

import itertools
import math
from typing import Iterable

import numpy as np

np.set_printoptions(precision=8, suppress=True, linewidth=120)

I8 = np.eye(8, dtype=complex)

PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if condition:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def cube_basis() -> list[tuple[int, int, int]]:
    return list(itertools.product((0, 1), repeat=3))


def cube_index() -> dict[tuple[int, int, int], int]:
    b = cube_basis()
    return {x: i for i, x in enumerate(b)}


def shift_op(axis: int) -> np.ndarray:
    idx = cube_index()
    op = np.zeros((8, 8), dtype=complex)
    for x, i in idx.items():
        y = list(x)
        y[axis] = 1 - y[axis]
        op[idx[tuple(y)], i] = 1.0
    return op


def parity_op(axis: int) -> np.ndarray:
    idx = cube_index()
    op = np.zeros((8, 8), dtype=complex)
    for x, i in idx.items():
        op[i, i] = 1.0 if x[axis] == 0 else -1.0
    return op


def residual_swap_op(axis: int) -> np.ndarray:
    others = [i for i in range(3) if i != axis]
    a, b = others
    idx = cube_index()
    op = np.zeros((8, 8), dtype=complex)
    for x, i in idx.items():
        y = list(x)
        y[a], y[b] = y[b], y[a]
        op[idx[tuple(y)], i] = 1.0
    return op


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def commutant_basis(operators: list[np.ndarray], tol: float = 1e-10) -> tuple[np.ndarray, int]:
    n = operators[0].shape[0]
    constraints = []
    for op in operators:
        constraints.append(np.kron(np.eye(n), op) - np.kron(op.T, np.eye(n)))
    m = np.vstack(constraints)
    _, s, vh = np.linalg.svd(m)
    rank = np.sum(s > tol)
    null = vh[rank:].conj().T
    return null, null.shape[1]


def is_close(a: np.ndarray, b: np.ndarray, tol: float = 1e-10) -> bool:
    return np.linalg.norm(a - b) < tol


def make_change_of_basis(axis: int) -> np.ndarray:
    """Graph-native basis: first factor is selected-axis fiber, second is base.

    Basis vector order:
      |fiber_bit> ⊗ |base_bits>
    where base_bits are the remaining two coordinates in their natural order.
    """
    idx = cube_index()
    basis_cols = []
    others = [i for i in range(3) if i != axis]
    for fiber_bit in (0, 1):
        for b1 in (0, 1):
            for b2 in (0, 1):
                x = [0, 0, 0]
                x[axis] = fiber_bit
                x[others[0]] = b1
                x[others[1]] = b2
                col = np.zeros(8, dtype=complex)
                col[idx[tuple(x)]] = 1.0
                basis_cols.append(col)
    U = np.column_stack(basis_cols)
    return U


def gell_mann_matrices() -> list[np.ndarray]:
    return [
        np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex),
        np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / math.sqrt(3.0),
    ]


def verify_selected_axis(axis: int) -> None:
    print("\n" + "=" * 76)
    print(f"SELECTED AXIS {axis + 1}")
    print("=" * 76)

    X = shift_op(axis)
    Z = parity_op(axis)
    Y = -1j * Z @ X
    weak = [X / 2.0, Y / 2.0, Z / 2.0]

    check("X is Hermitian", is_close(X, X.conj().T))
    check("Z is Hermitian", is_close(Z, Z.conj().T))
    check("Y is Hermitian", is_close(Y, Y.conj().T))
    check("X^2 = I", is_close(X @ X, I8))
    check("Y^2 = I", is_close(Y @ Y, I8))
    check("Z^2 = I", is_close(Z @ Z, I8))
    check("[X,Y] = 2iZ", is_close(commutator(X, Y), 2j * Z))
    check("[Y,Z] = 2iX", is_close(commutator(Y, Z), 2j * X))
    check("[Z,X] = 2iY", is_close(commutator(Z, X), 2j * Y))

    # Graph-native fiber/base factorization induced by forgetting the selected axis.
    U = make_change_of_basis(axis)
    check("Selected-axis graph basis is unitary", is_close(U.conj().T @ U, np.eye(8)))
    X_new = U.conj().T @ X @ U
    Y_new = U.conj().T @ Y @ U
    Z_new = U.conj().T @ Z @ U

    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    I4 = np.eye(4, dtype=complex)

    check("X = sigma_x on graph fiber", is_close(X_new, np.kron(sx, I4)))
    check("Y = sigma_y on graph fiber", is_close(Y_new, np.kron(sy, I4)))
    check("Z = sigma_z on graph fiber", is_close(Z_new, np.kron(sz, I4)))

    null_su2, dim_su2 = commutant_basis(weak)
    check("dim Comm(graph weak su(2)) = 16", dim_su2 == 16, detail=f"got {dim_su2}")

    swap = residual_swap_op(axis)
    for i, T in enumerate(weak, start=1):
        check(f"[SWAP_rest, T_{i}] = 0", is_close(commutator(swap, T), np.zeros((8, 8))))

    swap_new = U.conj().T @ swap @ U
    P4 = np.zeros((4, 4), dtype=complex)
    for b in range(2):
        for c in range(2):
            P4[2 * c + b, 2 * b + c] = 1.0
    check("Residual swap acts on graph base", is_close(swap_new, np.kron(I2, P4)))

    evals = np.sort(np.linalg.eigvalsh(swap.real))
    check("Residual swap spectrum is +1 x 6, -1 x 2", np.allclose(evals, [-1, -1, 1, 1, 1, 1, 1, 1]))

    null_both, dim_both = commutant_basis(weak + [swap])
    check("dim Comm(graph weak su(2), residual swap) = 10", dim_both == 10, detail=f"got {dim_both}")

    Pi_plus = (I8 + swap) / 2.0
    Pi_minus = (I8 - swap) / 2.0
    check("rank Pi_+ = 6", np.linalg.matrix_rank(Pi_plus, tol=1e-10) == 6)
    check("rank Pi_- = 2", np.linalg.matrix_rank(Pi_minus, tol=1e-10) == 2)

    w, v = np.linalg.eigh(swap.real)
    Vp = v[:, w > 0.5]
    Vm = v[:, w < -0.5]
    comm_mats = [null_both[:, i].reshape(8, 8) for i in range(dim_both)]
    rp = np.array([(Vp.conj().T @ M @ Vp).reshape(-1) for M in comm_mats])
    rm = np.array([(Vm.conj().T @ M @ Vm).reshape(-1) for M in comm_mats])
    check("Symmetric block rank = 9", np.linalg.matrix_rank(rp, tol=1e-8) == 9)
    check("Antisymmetric block rank = 1", np.linalg.matrix_rank(rm, tol=1e-8) == 1)

    # Explicit su(3) generators on the symmetric base block.
    e0 = np.array([1, 0], dtype=complex)
    e1 = np.array([0, 1], dtype=complex)
    U4 = np.column_stack([
        np.kron(e0, e0),
        (np.kron(e0, e1) + np.kron(e1, e0)) / math.sqrt(2.0),
        np.kron(e1, e1),
        (np.kron(e0, e1) - np.kron(e1, e0)) / math.sqrt(2.0),
    ])
    U8sa = np.kron(I2, U4)
    lam = gell_mann_matrices()
    T_su3 = []
    for la in lam:
        la4 = np.zeros((4, 4), dtype=complex)
        la4[:3, :3] = la / 2.0
        T = U @ U8sa @ np.kron(I2, la4) @ U8sa.conj().T @ U.conj().T
        T_su3.append(T)
        ok = all(is_close(commutator(T, W), np.zeros((8, 8))) for W in weak) and is_close(commutator(T, swap), np.zeros((8, 8)))
        check("Embedded lambda_a commutes with graph weak su(2)+swap", ok)

    max_err = 0.0
    for a in range(8):
        for b in range(a + 1, 8):
            cab = commutator(T_su3[a], T_su3[b])
            coeffs = [
                np.trace(cab @ T_su3[c].conj().T) / np.trace(T_su3[c] @ T_su3[c].conj().T)
                for c in range(8)
            ]
            recon = sum(c * T for c, T in zip(coeffs, T_su3))
            max_err = max(max_err, np.linalg.norm(cab - recon))
    check("Graph-first su(3) closes under commutation", max_err < 1e-8, detail=f"max err = {max_err:.2e}")

    # Hypercharge-like traceless U(1) on the left-handed surface.
    Yhyp = (1.0 / 3.0) * Pi_plus - 1.0 * Pi_minus
    check("Y_hyp is Hermitian", is_close(Yhyp, Yhyp.conj().T))
    check("Tr Y_hyp = 0", abs(np.trace(Yhyp)) < 1e-10)
    eigs = np.sort(np.linalg.eigvalsh(Yhyp.real))
    check("Y_hyp has +1/3 x 6", np.sum(np.abs(eigs - 1.0 / 3.0) < 1e-8) == 6)
    check("Y_hyp has -1 x 2", np.sum(np.abs(eigs + 1.0) < 1e-8) == 2)


def main() -> int:
    print("=" * 76)
    print("GRAPH-FIRST SU(3) INTEGRATION THEOREM")
    print("=" * 76)
    print("Selected graph axis -> graph-native weak su(2) -> residual swap -> su(3) ⊕ u(1)")

    for axis in range(3):
        verify_selected_axis(axis)

    print("\nSUMMARY")
    print("  Once the graph-first selector chooses an axis, the selected graph")
    print("  projection canonically splits the cube into 2-point fibers over a")
    print("  4-point base. The selected-axis shift/parity pair generates the weak")
    print("  su(2) on the fibers. The residual swap of the other two axes acts on")
    print("  the base and splits it into 3 ⊕ 1. The joint commutant is therefore")
    print("  gl(3) ⊕ gl(1), with compact semisimple part su(3).")
    print("  This closes the structural graph-first route to the color lane.")

    if FAIL:
        print(f"\nFAIL={FAIL}")
        return 1
    print(f"\nPASS={PASS} FAIL=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
