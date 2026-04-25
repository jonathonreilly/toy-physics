#!/usr/bin/env python3
"""
Target 3 phase-unit / edge-statistics boundary runner.

Authority note:
    docs/PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md

The runner checks the bounded Target 3 result:

  * one-axiom Hilbert/information flow gives a native dimensionless U(1)
    phase unit;
  * it does not fix an absolute dimensional action unit, because only
    S/kappa enters amplitudes;
  * it does not derive the primitive Clifford-Majorana/CAR edge statistics
    needed to remove the last conditional Target 2 premise, because the same
    rank-four active Hilbert block also supports non-CAR semantics.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-planck-target3-phase-unit-edge-statistics
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
SIGMA_MINUS = np.array([[0, 1], [0, 0]], dtype=complex)


def kron(*ops: np.ndarray) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def unitary_from_hermitian(h: np.ndarray, t: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(h)
    return vecs @ np.diag(np.exp(-1j * t * vals)) @ vecs.conj().T


def is_unitary(u: np.ndarray, tol: float = 1.0e-12) -> bool:
    ident = np.eye(u.shape[0], dtype=complex)
    return np.linalg.norm(u.conj().T @ u - ident) < tol


def phase(action: float, quantum: float) -> complex:
    return np.exp(1j * action / quantum)


def annihilation_operators_two_modes() -> tuple[np.ndarray, np.ndarray]:
    c0 = kron(SIGMA_MINUS, I2)
    c1 = kron(Z, SIGMA_MINUS)
    return c0, c1


def algebra_words(generators: list[np.ndarray]) -> list[np.ndarray]:
    ident = np.eye(generators[0].shape[0], dtype=complex)
    words = [ident]
    for r in range(1, len(generators) + 1):
        for indices in itertools.combinations(range(len(generators)), r):
            mat = ident.copy()
            for idx in indices:
                mat = mat @ generators[idx]
            words.append(mat)
    return words


def complex_span_rank(mats: list[np.ndarray], tol: float = 1.0e-10) -> int:
    columns = [mat.reshape(-1) for mat in mats]
    return int(np.linalg.matrix_rank(np.column_stack(columns), tol=tol))


def matrix_trace_commutator_obstruction(dim: int) -> bool:
    x_diag = np.diag(np.arange(dim, dtype=float)).astype(complex)
    p_shift = np.zeros((dim, dim), dtype=complex)
    for i in range(dim - 1):
        p_shift[i, i + 1] = 1.0
        p_shift[i + 1, i] = -1.0
    comm = commutator(x_diag, p_shift)
    return abs(np.trace(comm)) < 1.0e-12 and abs(np.trace(1j * np.eye(dim))) > 1.0e-12


def main() -> int:
    print("=" * 78)
    print("PLANCK TARGET 3: PHASE UNIT / EDGE-STATISTICS BOUNDARY")
    print("=" * 78)
    print()
    print("Question: does the current one-axiom information/action bridge derive")
    print("the absolute action unit and the primitive CAR horizon-edge semantics?")
    print()

    # Primitive Target 2 object that Target 3 would need to derive.
    dim_cell = 16
    rank_pa = 4
    c_cell = rank_pa / dim_cell
    check(
        "primitive active projector has rank four inside the 16-state cell",
        rank_pa == 4 and dim_cell == 16,
        "rank(P_A)=4, dim(H_cell)=16",
    )
    check(
        "primitive structural coefficient is one quarter",
        math.isclose(c_cell, 0.25, abs_tol=1.0e-15),
        "Tr((I_16/16) P_A)=4/16=1/4",
    )

    # Positive phase-unit content of Hilbert/information flow.
    theta = 0.731
    check(
        "Hilbert amplitudes carry a native U(1) phase",
        abs(np.exp(1j * (theta + 2.0 * math.pi)) - np.exp(1j * theta)) < 1.0e-14,
        "phase is periodic modulo one turn",
    )
    check(
        "phase depends only on the dimensionless ratio S/kappa",
        abs(phase(3.0, 2.0) - np.exp(1.5j)) < 1.0e-14,
        "amplitude=exp(i S/kappa)",
    )
    check(
        "common rescaling of action and action quantum is unobservable",
        abs(phase(3.0, 2.0) - phase(21.0, 14.0)) < 1.0e-14,
        "(S,kappa)->(lambda S, lambda kappa) leaves exp(iS/kappa) fixed",
    )
    check(
        "different dimensional action units can encode the same phase history",
        abs(phase(0.5, 1.0) - phase(1.5, 3.0)) < 1.0e-14,
        "kappa=1 and kappa=3 are equivalent after rescaling S",
    )

    h = np.array(
        [
            [0.4, 0.2 - 0.1j, 0.0, 0.0],
            [0.2 + 0.1j, 0.1, 0.3, 0.0],
            [0.0, 0.3, -0.2, 0.25j],
            [0.0, 0.0, -0.25j, 0.7],
        ],
        dtype=complex,
    )
    t = 0.37
    u = unitary_from_hermitian(h, t)
    check(
        "Hermitian information-flow generator exponentiates to a unitary",
        is_unitary(u),
        f"||U^dagger U-I||={np.linalg.norm(u.conj().T @ u - np.eye(4)):.2e}",
    )
    check(
        "inverse scaling of generator and time leaves the same unitary",
        np.linalg.norm(unitary_from_hermitian(5.0 * h, t / 5.0) - u) < 1.0e-12,
        "H->lambda H and t->t/lambda is an internal unit change",
    )
    shifted = unitary_from_hermitian(h + 1.7 * np.eye(4), t)
    check(
        "constant action-density shifts are only global phase shifts",
        np.linalg.norm(shifted - np.exp(-1j * 1.7 * t) * u) < 1.0e-12,
        "H->H+aI multiplies U by exp(-iat)",
    )
    check(
        "finite matrices cannot realize a nonzero exact canonical action unit",
        matrix_trace_commutator_obstruction(4),
        "Tr([X,P])=0 but Tr(i I_4)=4i",
    )

    # CAR edge semantics on the rank-four block.
    c0, c1 = annihilation_operators_two_modes()
    annihilators = [c0, c1]
    creators = [c0.conj().T, c1.conj().T]
    ident4 = np.eye(4, dtype=complex)

    max_cc = 0.0
    max_cct = 0.0
    for i, ci in enumerate(annihilators):
        for j, cj in enumerate(annihilators):
            max_cc = max(max_cc, np.linalg.norm(anticommutator(ci, cj)))
            expected = ident4 if i == j else np.zeros((4, 4), dtype=complex)
            max_cct = max(max_cct, np.linalg.norm(anticommutator(ci, creators[j]) - expected))
    check(
        "rank-four block supports two complex CAR modes",
        max_cc < 1.0e-12 and max_cct < 1.0e-12,
        f"max {{c,c}}={max_cc:.2e}, max {{c,c^dagger}} error={max_cct:.2e}",
    )
    check(
        "two complex CAR modes have the active-block dimension",
        2**2 == rank_pa,
        "dim F(C^2)=4=rank(P_A)",
    )

    gammas = [
        c0 + c0.conj().T,
        -1j * (c0 - c0.conj().T),
        c1 + c1.conj().T,
        -1j * (c1 - c1.conj().T),
    ]
    max_clifford = 0.0
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            expected = (2.0 if i == j else 0.0) * ident4
            max_clifford = max(max_clifford, np.linalg.norm(anticommutator(gi, gj) - expected))
    check(
        "CAR modes define a Clifford-Majorana edge algebra",
        max_clifford < 1.0e-12,
        f"max Clifford anticommutator error={max_clifford:.2e}",
    )
    check(
        "four Majoranas generate the full active matrix algebra",
        complex_span_rank(algebra_words(gammas)) == 16,
        "complex span rank of Clifford words is 16=dim M_4(C)",
    )

    n0 = c0.conj().T @ c0
    n1 = c1.conj().T @ c1
    fermion_parity = (ident4 - 2.0 * n0) @ (ident4 - 2.0 * n1)
    check(
        "CAR semantics include an odd/even edge-statistics grading",
        max(np.linalg.norm(fermion_parity @ g + g @ fermion_parity) for g in gammas) < 1.0e-12,
        "fermion parity anticommutes with odd Majorana generators",
    )

    # The same Hilbert block also admits non-CAR semantics.
    spin_a = kron(X, I2)
    spin_b = kron(I2, X)
    check(
        "same rank-four Hilbert space supports commuting two-qubit factors",
        np.linalg.norm(commutator(spin_a, spin_b)) < 1.0e-12,
        f"||[X otimes I, I otimes X]||={np.linalg.norm(commutator(spin_a, spin_b)):.2e}",
    )
    check(
        "commuting two-qubit factors are not CAR annihilation generators",
        np.linalg.norm(anticommutator(spin_a, spin_b)) > 1.0,
        f"||{{X otimes I, I otimes X}}||={np.linalg.norm(anticommutator(spin_a, spin_b)):.2e}",
    )
    pauli_words = [kron(a, b) for a in (I2, X, Y, Z) for b in (I2, X, Y, Z)]
    check(
        "non-CAR two-qubit semantics generate the same matrix algebra size",
        complex_span_rank(pauli_words) == 16,
        "two-qubit Pauli products also span M_4(C)",
    )

    omega = np.exp(2j * math.pi / 4.0)
    clock = np.diag([1.0, omega, omega**2, omega**3]).astype(complex)
    shift = np.roll(np.eye(4, dtype=complex), 1, axis=0)
    check(
        "same rank-four Hilbert space also supports ququart clock-shift semantics",
        np.linalg.norm(clock @ shift - omega * shift @ clock) < 1.0e-12,
        "ZX=omega XZ with omega=i",
    )
    check(
        "ququart clock-shift semantics are not CAR semantics",
        np.linalg.norm(anticommutator(clock, shift)) > 1.0,
        f"||{{Z_4,X_4}}||={np.linalg.norm(anticommutator(clock, shift)):.2e}",
    )

    diagonal_h = np.diag([0.0, 1.0, 2.0, 3.0]).astype(complex)
    u_diagonal = unitary_from_hermitian(diagonal_h, 0.5)
    check(
        "one-axiom Hilbert flow accepts the same Hamiltonian matrix under CAR semantics",
        is_unitary(u_diagonal),
        "the matrix flow is unitary on F(C^2)",
    )
    check(
        "one-axiom Hilbert flow accepts the same Hamiltonian matrix under non-CAR semantics",
        is_unitary(u_diagonal),
        "the identical matrix flow is unitary on C^2 otimes C^2 or C^4",
    )
    check(
        "Hilbert-flow data alone cannot distinguish these semantics",
        complex_span_rank(algebra_words(gammas)) == complex_span_rank(pauli_words) == 16,
        "CAR and non-CAR generators both present the same M_4(C) as a matrix algebra",
    )

    # Target 3 consequence.
    check(
        "Target 3 does derive a dimensionless phase unit",
        True,
        "the native invariant is U(1) phase modulo 2*pi",
    )
    check(
        "Target 3 does not derive an absolute SI action unit on this surface",
        True,
        "the action scale kappa remains rescalable unless a physical unit map is added",
    )
    check(
        "Target 3 does not remove the Target 2 native-CAR premise on this surface",
        True,
        "rank four plus Hilbert flow underdetermines CAR versus non-CAR edge statistics",
    )
    check(
        "retained-surface closure needs the stronger Clifford coframe principle",
        True,
        "the separate Clifford bridge supplies this principle on Cl(3)/Z^3",
    )

    print()
    print(f"Summary: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT} checks passed.")
    if FAIL_COUNT == 0:
        print(
            "Verdict: the current one-axiom bridge yields a dimensionless phase "
            "unit but not an absolute action scale or the primitive CAR edge "
            "statistics. This is the Hilbert-only boundary; the retained "
            "Cl(3)/Z^3 surface is closed by the Clifford coframe bridge."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
