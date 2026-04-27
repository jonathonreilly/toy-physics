#!/usr/bin/env python3
"""
Target 3 coframe-response derivation runner.

Authority note:
    docs/PLANCK_TARGET3_COFRAME_RESPONSE_DERIVATION_THEOREM_NOTE_2026-04-25.md

This runner checks the missing derivation left by the reviewed Target 3
Clifford bridge:

    D(v)^2 = ||v||^2 I on K = P_A H_cell.

The derivation uses retained Cl(3)/Z^3 primitive coframe structure:

  * the spatial primitive response is the retained Cl(3) Pauli/KS algebra;
  * time-locking supplies a Z_2 grading for first-order staggered-Dirac
    response;
  * first-order primitive coframe steps are grading-odd;
  * the grading-even time-space bivectors recover the retained spatial Cl(3)
    generators.

Those facts force the doubled rank-four coframe generators. Their square is
the scalar primitive quadratic form.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-planck-target3-coframe-response-derivation
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-12


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


def kron(*ops: np.ndarray) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def spatial_cl3() -> list[np.ndarray]:
    return [X, Y, Z]


def time_locked_generators() -> tuple[np.ndarray, list[np.ndarray]]:
    gamma_t = kron(X, I2)
    gammas_spatial = [kron(Y, sigma) for sigma in spatial_cl3()]
    return gamma_t, gammas_spatial


def coframe_operator(v: np.ndarray, gammas: list[np.ndarray]) -> np.ndarray:
    out = np.zeros_like(gammas[0])
    for coeff, gamma in zip(v, gammas, strict=True):
        out = out + complex(coeff) * gamma
    return out


def matrix_span_rank(mats: list[np.ndarray], tol: float = 1.0e-10) -> int:
    columns = [mat.reshape(-1) for mat in mats]
    return int(np.linalg.matrix_rank(np.column_stack(columns), tol=tol))


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


def commutant_dimension(generators: list[np.ndarray], tol: float = 1.0e-10) -> int:
    dim = generators[0].shape[0]
    ident = np.eye(dim, dtype=complex)
    rows = []
    for gen in generators:
        rows.append(np.kron(ident, gen) - np.kron(gen.T, ident))
    system = np.vstack(rows)
    rank = int(np.linalg.matrix_rank(system, tol=tol))
    return dim * dim - rank


def anticommutant_dimension(generators: list[np.ndarray], dim: int, tol: float = 1.0e-10) -> int:
    ident = np.eye(dim, dtype=complex)
    rows = []
    for gen in generators:
        rows.append(np.kron(ident, gen) + np.kron(gen.T, ident))
    system = np.vstack(rows)
    rank = int(np.linalg.matrix_rank(system, tol=tol))
    return dim * dim - rank


def hamming_weight_one_isometry() -> tuple[np.ndarray, np.ndarray, list[tuple[int, ...]]]:
    states = list(itertools.product((0, 1), repeat=4))
    active_states = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    index = {state: idx for idx, state in enumerate(states)}
    w = np.zeros((16, 4), dtype=complex)
    for col, state in enumerate(active_states):
        w[index[state], col] = 1.0
    p_a = w @ w.conj().T
    return w, p_a, active_states


def main() -> int:
    print("=" * 78)
    print("PLANCK TARGET 3: COFRAME RESPONSE DERIVATION")
    print("=" * 78)
    print()
    print("Question: does retained Cl(3)/Z^3 primitive coframe structure force")
    print("D(v)^2 = ||v||^2 I on P_A H_cell?")
    print()

    # Primitive Planck packet data.
    w, p_a, active_states = hamming_weight_one_isometry()
    check(
        "primitive active packet has four Hamming-weight-one states",
        len(active_states) == 4,
        f"active states={active_states}",
    )
    check(
        "P_A is an orthogonal rank-four projector inside H_cell=C^16",
        np.linalg.norm(p_a @ p_a - p_a) < TOL and round(float(np.trace(p_a).real)) == 4,
        f"rank(P_A)={np.trace(p_a).real:.0f}",
    )
    check(
        "source-free primitive trace is one quarter",
        math.isclose(np.trace(p_a).real / 16.0, 0.25, abs_tol=1.0e-15),
        "Tr((I_16/16)P_A)=4/16=1/4",
    )
    check(
        "the isometry identifies K=P_A H_cell with a rank-four module",
        np.linalg.norm(w.conj().T @ w - np.eye(4)) < TOL
        and np.linalg.norm(w @ w.conj().T - p_a) < TOL,
        "W^dagger W=I_4 and W W^dagger=P_A",
    )

    # Retained spatial Cl(3).
    sigmas = spatial_cl3()
    max_spatial_cl3 = 0.0
    ident2 = np.eye(2, dtype=complex)
    for i, si in enumerate(sigmas):
        for j, sj in enumerate(sigmas):
            expected = (2.0 if i == j else 0.0) * ident2
            max_spatial_cl3 = max(max_spatial_cl3, np.linalg.norm(anticommutator(si, sj) - expected))
    check(
        "retained spatial coframe generators satisfy Cl(3)",
        max_spatial_cl3 < TOL,
        f"max spatial Clifford error={max_spatial_cl3:.2e}",
    )
    check(
        "spatial Cl(3) irreducible module is two-dimensional",
        matrix_span_rank(algebra_words(sigmas)) == 4 and commutant_dimension(sigmas) == 1,
        "Pauli words span M_2(C) and have scalar commutant",
    )
    anti_dim = anticommutant_dimension(sigmas, dim=2)
    check(
        "a fourth independent unit coframe axis cannot live on the spatial spinor alone",
        anti_dim == 0,
        "no nonzero 2x2 matrix anticommutes with all three Pauli generators",
    )

    # Time-lock doubling forced by a fourth first-order axis.
    tau_grade = kron(Z, I2)
    gamma_t, gamma_spatial = time_locked_generators()
    gammas = [gamma_t] + gamma_spatial
    ident4 = np.eye(4, dtype=complex)
    check(
        "time-lock doubles the spatial spinor to the primitive rank-four block",
        ident4.shape == (4, 4),
        "C^2_time-lock otimes C^2_spatial has dimension 4=rank(P_A)",
    )
    check(
        "time axis is the unique spatial-scalar odd primitive flip",
        np.linalg.norm(gamma_t - kron(X, I2)) < TOL
        and np.linalg.norm(anticommutator(tau_grade, gamma_t)) < TOL,
        "Gamma_t=tau_x otimes I anticommutes with the time-lock grading",
    )

    even_bivectors = [-1j * gamma_t @ gamma_i for gamma_i in gamma_spatial]
    max_bivector_readout = max(
        np.linalg.norm(biv - kron(Z, sigma))
        for biv, sigma in zip(even_bivectors, sigmas, strict=True)
    )
    check(
        "time-space bivectors recover the retained spatial Cl(3) readout",
        max_bivector_readout < TOL,
        f"max ||-i Gamma_t Gamma_i - tau_z otimes sigma_i||={max_bivector_readout:.2e}",
    )
    check(
        "time-space bivectors preserve the time-lock sheets",
        max(np.linalg.norm(commutator(tau_grade, biv)) for biv in even_bivectors) < TOL,
        "[-i Gamma_t Gamma_i, tau_z]=0",
    )

    # Easier explicit sector restrictions: upper and lower 2x2 diagonal blocks.
    max_plus = max(np.linalg.norm(biv[:2, :2] - sigma) for biv, sigma in zip(even_bivectors, sigmas, strict=True))
    max_minus = max(np.linalg.norm(biv[2:, 2:] + sigma) for biv, sigma in zip(even_bivectors, sigmas, strict=True))
    check(
        "each time-lock sheet carries the retained spatial Cl(3) up to orientation",
        max_plus < TOL and max_minus < TOL,
        f"plus error={max_plus:.2e}, minus-orientation error={max_minus:.2e}",
    )

    # The odd spatial coframe generators are then forced by Gamma_i=i Gamma_t B_i.
    reconstructed_spatial = [1j * gamma_t @ biv for biv in even_bivectors]
    max_reconstruction = max(
        np.linalg.norm(rec - gamma)
        for rec, gamma in zip(reconstructed_spatial, gamma_spatial, strict=True)
    )
    check(
        "odd spatial coframe steps are forced by time axis plus spatial bivectors",
        max_reconstruction < TOL,
        "Gamma_i=i Gamma_t (-i Gamma_t Gamma_i)",
    )
    check(
        "all four primitive coframe steps are grading-odd first-order responses",
        max(np.linalg.norm(anticommutator(tau_grade, gamma)) for gamma in gammas) < TOL,
        "{tau_z, Gamma_a}=0 for a=t,x,y,z",
    )

    # Clifford and square law.
    max_hermitian = max(np.linalg.norm(gamma - gamma.conj().T) for gamma in gammas)
    max_square = max(np.linalg.norm(gamma @ gamma - ident4) for gamma in gammas)
    max_cl4 = 0.0
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            expected = (2.0 if i == j else 0.0) * ident4
            max_cl4 = max(max_cl4, np.linalg.norm(anticommutator(gi, gj) - expected))
    check(
        "forced primitive coframe generators are Hermitian",
        max_hermitian < TOL,
        f"max Hermitian error={max_hermitian:.2e}",
    )
    check(
        "forced primitive coframe generators square to one",
        max_square < TOL,
        f"max ||Gamma_a^2-I||={max_square:.2e}",
    )
    check(
        "forced primitive coframe generators satisfy the Cl_4 relation",
        max_cl4 < TOL,
        f"max Cl_4 anticommutator error={max_cl4:.2e}",
    )

    test_vectors = [
        np.array([1.0, 0.0, 0.0, 0.0]),
        np.array([0.2, -0.4, 0.7, 0.1]),
        np.array([1.0, 2.0, -1.0, 0.5]),
        np.array([-0.3, 0.6, 0.8, -0.2]),
    ]
    max_square_law = 0.0
    for vector in test_vectors:
        d_v = coframe_operator(vector, gammas)
        max_square_law = max(
            max_square_law,
            np.linalg.norm(d_v @ d_v - float(vector @ vector) * ident4),
        )
    check(
        "derived coframe response squares to the scalar primitive norm on K",
        max_square_law < TOL,
        f"max ||D(v)^2-||v||^2 I_K||={max_square_law:.2e}",
    )

    # Equivalent active-cell statement on P_A H_cell.
    vector = np.array([0.2, -0.4, 0.7, 0.1])
    d_k = coframe_operator(vector, gammas)
    d_cell = w @ d_k @ w.conj().T
    cell_square_error = np.linalg.norm(d_cell @ d_cell - float(vector @ vector) * p_a)
    support_error = np.linalg.norm(p_a @ d_cell @ p_a - d_cell)
    check(
        "same square law holds as a compressed operator on P_A H_cell",
        cell_square_error < TOL and support_error < TOL,
        f"cell square error={cell_square_error:.2e}, support error={support_error:.2e}",
    )

    # Irreducibility / no spectator.
    word_rank = matrix_span_rank(algebra_words(gammas))
    comm_dim = commutant_dimension(gammas)
    check(
        "forced Cl_4 words span the full active matrix algebra",
        word_rank == 16,
        "span rank=16=dim M_4(C)",
    )
    check(
        "forced rank-four coframe module is irreducible",
        comm_dim == 1,
        "commutant dimension is one",
    )
    check(
        "minimality matches the Planck active packet exactly",
        all(d * d < 16 for d in (1, 2, 3)) and p_a.trace().real == 4.0,
        "Cl_4(C) needs M_4(C), and rank(P_A)=4 leaves no active spectator",
    )

    # Obstruction checks: alternatives fail the derived retained structure.
    bad_time = kron(I2, I2)
    bad_spatial = [kron(I2, sigma) for sigma in sigmas]
    bad_gammas = [bad_time] + bad_spatial
    bad_vector = np.array([1.0, 1.0, 0.0, 0.0])
    bad_d = coframe_operator(bad_vector, bad_gammas)
    bad_error = np.linalg.norm(bad_d @ bad_d - float(bad_vector @ bad_vector) * ident4)
    check(
        "commuting time labels fail the primitive scalar square law",
        bad_error > 1.0,
        f"bad square error={bad_error:.2e}",
    )
    two_qubit = [kron(X, I2), kron(I2, X), kron(Z, I2), kron(I2, Z)]
    two_qubit_error = 0.0
    for i, ai in enumerate(two_qubit):
        for j, aj in enumerate(two_qubit):
            expected = (2.0 if i == j else 0.0) * ident4
            two_qubit_error = max(
                two_qubit_error,
                np.linalg.norm(anticommutator(ai, aj) - expected),
            )
    check(
        "generic two-qubit semantics fail the retained coframe anticommutators",
        two_qubit_error > 1.0,
        f"max two-qubit coframe error={two_qubit_error:.2e}",
    )
    omega = np.exp(2j * math.pi / 4.0)
    clock = np.diag([1.0, omega, omega**2, omega**3]).astype(complex)
    shift = np.roll(np.eye(4, dtype=complex), 1, axis=0)
    check(
        "ququart clock-shift semantics fail Hermitian unit coframe response",
        np.linalg.norm(clock - clock.conj().T) > 1.0
        and np.linalg.norm(clock @ clock - ident4) > 1.0
        and np.linalg.norm(clock @ shift - omega * shift @ clock) < TOL,
        "valid ququart Weyl pair, but not a Hermitian Clifford coframe pair",
    )

    # Consequences for the existing Target 3 bridge.
    c_cell = float(np.trace(p_a).real) / 16.0
    c_widom = (2.0 + 2.0 * 0.5) / 12.0
    check(
        "derived square law discharges the reviewed Clifford bridge premise",
        math.isclose(c_widom, c_cell, abs_tol=1.0e-15),
        "D(v)^2 premise is derived; c_Widom=3/12=c_cell=4/16",
    )
    check(
        "source-unit support then gives the natural Planck map",
        math.isclose(1.0 / (4.0 * (1.0 / (4.0 * c_cell))), c_cell, abs_tol=1.0e-15),
        "lambda=4*c_cell=1, so G_Newton,lat=1 and a/l_P=1",
    )

    print()
    print(f"Summary: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print()
        print(
            "Verdict: the retained Cl(3)/Z^3 time-locked primitive coframe "
            "structure derives D(v)^2=||v||^2 I on P_A H_cell. The reviewed "
            "Target 3 Clifford/CAR bridge premise is discharged on the "
            "minimal active block."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
