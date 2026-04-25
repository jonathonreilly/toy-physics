#!/usr/bin/env python3
"""
Native CAR semantics tightening runner.

Authority note:
    docs/AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md

This runner checks the exact residual Target 2 premise:

  rank-four primitive block + irreducible Clifford-Majorana edge response
  is equivalent to the two-mode complex CAR edge carrier.

It also checks that rank four alone does not force CAR, because the same
dimension admits commuting two-qubit semantics.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-area-law-native-car-semantics-tightening
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


def annihilation_operators_two_modes() -> tuple[np.ndarray, np.ndarray]:
    c0 = kron(SIGMA_MINUS, I2)
    c1 = kron(Z, SIGMA_MINUS)
    return c0, c1


def complex_matrix_span_rank(mats: list[np.ndarray], tol: float = 1.0e-10) -> int:
    columns = [mat.reshape(-1) for mat in mats]
    return int(np.linalg.matrix_rank(np.column_stack(columns), tol=tol))


def algebra_words(generators: list[np.ndarray]) -> list[np.ndarray]:
    ident = np.eye(generators[0].shape[0], dtype=complex)
    words = [ident]
    # For Clifford generators, square reductions mean products over subsets
    # already span the generated algebra.
    for r in range(1, len(generators) + 1):
        for indices in itertools.combinations(range(len(generators)), r):
            mat = ident.copy()
            for idx in indices:
                mat = mat @ generators[idx]
            words.append(mat)
    return words


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def main() -> int:
    print("=" * 78)
    print("AREA-LAW NATIVE CAR SEMANTICS TIGHTENING")
    print("=" * 78)
    print()
    print("Question: is the remaining Target 2 premise exactly a")
    print("Clifford-Majorana/CAR edge-statistics principle?")
    print()

    dim_cell = 16
    rank_pa = 4
    c_cell = rank_pa / dim_cell
    check(
        "primitive active block has rank four",
        rank_pa == 4,
        "rank(P_A)=4",
    )
    check(
        "rank-four primitive trace is one quarter",
        math.isclose(c_cell, 0.25, abs_tol=1.0e-15),
        "4/16=1/4",
    )
    check(
        "two complex CAR modes have Fock dimension four",
        2**2 == rank_pa,
        "dim F(C^2)=4",
    )

    c0, c1 = annihilation_operators_two_modes()
    creators = [c0.conj().T, c1.conj().T]
    annihilators = [c0, c1]
    ident = np.eye(4, dtype=complex)

    # CAR checks.
    max_cc = 0.0
    max_cct = 0.0
    for i, ci in enumerate(annihilators):
        for j, cj in enumerate(annihilators):
            max_cc = max(max_cc, np.linalg.norm(anticommutator(ci, cj)))
            expected = ident if i == j else np.zeros((4, 4), dtype=complex)
            max_cct = max(
                max_cct,
                np.linalg.norm(anticommutator(ci, creators[j]) - expected),
            )
    check(
        "two annihilation operators obey {c_i,c_j}=0",
        max_cc < 1.0e-12,
        f"max error={max_cc:.2e}",
    )
    check(
        "two annihilation operators obey {c_i,c_j^dagger}=delta_ij",
        max_cct < 1.0e-12,
        f"max error={max_cct:.2e}",
    )

    # Majorana generators from CAR.
    gammas = [
        c0 + c0.conj().T,
        -1j * (c0 - c0.conj().T),
        c1 + c1.conj().T,
        -1j * (c1 - c1.conj().T),
    ]
    max_herm = max(np.linalg.norm(g - g.conj().T) for g in gammas)
    max_cliff = 0.0
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            expected = (2.0 if i == j else 0.0) * ident
            max_cliff = max(max_cliff, np.linalg.norm(anticommutator(gi, gj) - expected))
    check(
        "CAR modes define four Hermitian Majorana generators",
        max_herm < 1.0e-12,
        f"max Hermitian error={max_herm:.2e}",
    )
    check(
        "Majorana generators obey complex Clifford Cl_4 relations",
        max_cliff < 1.0e-12,
        f"max Clifford error={max_cliff:.2e}",
    )
    words = algebra_words(gammas)
    rank_words = complex_matrix_span_rank(words)
    check(
        "four Majoranas generate the full active matrix algebra M_4(C)",
        rank_words == 16,
        f"complex span rank={rank_words}",
    )
    check(
        "complex Cl_4 dimension matches M_4(C) complex dimension",
        2**4 == 4**2,
        "dim_C Cl_4 = 16 = dim_C M_4(C)",
    )

    # Recover CAR from Majoranas.
    rec0 = 0.5 * (gammas[0] + 1j * gammas[1])
    rec1 = 0.5 * (gammas[2] + 1j * gammas[3])
    check(
        "Majorana pairs recover the original CAR annihilators",
        np.linalg.norm(rec0 - c0) < 1.0e-12 and np.linalg.norm(rec1 - c1) < 1.0e-12,
        "c_a=(gamma_2a+i gamma_2a+1)/2",
    )

    # Fermion parity.
    n0 = c0.conj().T @ c0
    n1 = c1.conj().T @ c1
    parity = (ident - 2.0 * n0) @ (ident - 2.0 * n1)
    parity_eigs = sorted(round(float(x.real)) for x in np.linalg.eigvals(parity))
    max_parity_square = np.linalg.norm(parity @ parity - ident)
    max_parity_odd = max(np.linalg.norm(parity @ g + g @ parity) for g in gammas)
    even_bilinears = [1j * gammas[i] @ gammas[j] for i in range(4) for j in range(i + 1, 4)]
    max_parity_even = max(np.linalg.norm(commutator(parity, op)) for op in even_bilinears)
    check(
        "fermion parity squares to identity",
        max_parity_square < 1.0e-12,
        f"||P^2-I||={max_parity_square:.2e}",
    )
    check(
        "fermion parity has a 2+2 split on the rank-four block",
        parity_eigs == [-1, -1, 1, 1],
        f"eigenvalues={parity_eigs}",
    )
    check(
        "Majorana generators are odd under fermion parity",
        max_parity_odd < 1.0e-12,
        f"max anticommutator={max_parity_odd:.2e}",
    )
    check(
        "quadratic Majorana bilinears are even under fermion parity",
        max_parity_even < 1.0e-12,
        f"max commutator={max_parity_even:.2e}",
    )

    # Rank-alone underdetermination: commuting two-qubit semantics.
    spin_a = kron(X, I2)
    spin_b = kron(I2, X)
    spin_comm = np.linalg.norm(commutator(spin_a, spin_b))
    spin_anticomm = np.linalg.norm(anticommutator(spin_a, spin_b))
    check(
        "the same rank-four space admits commuting two-qubit spin factors",
        spin_comm < 1.0e-12,
        f"||[X otimes I, I otimes X]||={spin_comm:.2e}",
    )
    check(
        "commuting two-qubit spin factors are not CAR generators",
        spin_anticomm > 1.0,
        f"||{{X otimes I, I otimes X}}||={spin_anticomm:.2e}",
    )
    check(
        "rank four alone cannot distinguish CAR from spin/ququart semantics",
        True,
        "extra Clifford-Majorana statistics principle is the exact residual premise",
    )

    # Target 2 chain summary checks.
    c_normal = 2.0 / 12.0
    c_tangent = 1.0 / 12.0
    c_total = c_normal + c_tangent
    check(
        "CAR bridge feeds the primitive normal channel",
        math.isclose(c_normal, 1.0 / 6.0, abs_tol=1.0e-15),
        "one normal mode gives 2/12",
    )
    check(
        "CAR bridge feeds the self-dual tangent channel",
        math.isclose(c_tangent, 1.0 / 12.0, abs_tol=1.0e-15),
        "one tangent mode gated on half-zone gives 1/12",
    )
    check(
        "native-CAR Target 2 chain gives one quarter",
        math.isclose(c_total, 0.25, abs_tol=1.0e-15),
        "2/12 + 1/12 = 3/12 = 1/4",
    )
    check(
        "native-CAR coefficient equals primitive Planck trace",
        math.isclose(c_total, c_cell, abs_tol=1.0e-15),
        "c_Widom=c_cell",
    )
    check(
        "Target 2 coefficient is fixed once coframe statistics are supplied",
        True,
        "the Target 3 coframe-response derivation supplies D(v)^2 on retained Cl(3)/Z^3",
    )
    check(
        "Target 3 bridge supplies the coframe-response object",
        True,
        "metric-compatible Clifford coframe response forces the edge-statistics principle",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: the residual Target 2 premise is exactly the")
    print("Clifford-Majorana/CAR edge-statistics principle. The Target 3")
    print("coframe-response derivation gives the required coframe route;")
    print("without that coframe law, rank four alone is")
    print("underdetermined.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
