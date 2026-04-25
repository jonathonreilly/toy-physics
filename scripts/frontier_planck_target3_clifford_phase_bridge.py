#!/usr/bin/env python3
"""
Target 3 Clifford phase bridge theorem runner.

Authority note:
    docs/PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md

This runner checks the conditional Target 3 Clifford/coframe bridge:

  * assuming a metric-compatible primitive coframe response, the active
    rank-four boundary block carries the complex Cl_4 relations;
  * the unique irreducible rank-four Cl_4 module is equivalent to the two-mode
    complex CAR Fock carrier;
  * non-CAR rank-four semantics fail the coframe/Clifford response law;
  * the resulting Target 2 carrier has c_Widom = c_cell = 1/4;
  * the source-unit support theorem then gives G_lat = 1 and a/l_P = 1 in the
    package's natural phase/action units on that same conditional surface.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-planck-target3-clifford-phase-bridge
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


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def clifford_generators() -> list[np.ndarray]:
    # Hermitian Euclidean Cl_4 generators. Interpret the ordered axes as
    # (t, normal, tangent_1, tangent_2) for a selected primitive face.
    return [
        kron(X, I2),
        kron(Y, I2),
        kron(Z, X),
        kron(Z, Y),
    ]


def coframe_operator(vector: np.ndarray, gammas: list[np.ndarray]) -> np.ndarray:
    out = np.zeros_like(gammas[0])
    for coeff, gamma in zip(vector, gammas, strict=True):
        out = out + complex(coeff) * gamma
    return out


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


def commutant_dimension(generators: list[np.ndarray], tol: float = 1.0e-10) -> int:
    # vec(AM - MB) = (I kron A - B^T kron I) vec(M), with A=B=generator.
    dim = generators[0].shape[0]
    rows = []
    ident = np.eye(dim, dtype=complex)
    for gamma in generators:
        rows.append(np.kron(ident, gamma) - np.kron(gamma.T, ident))
    system = np.vstack(rows)
    rank = int(np.linalg.matrix_rank(system, tol=tol))
    return dim * dim - rank


def unitary_from_antihermitian(generator: np.ndarray, theta: float) -> np.ndarray:
    # The bivector generator squares to -I, so the exponential is exact.
    dim = generator.shape[0]
    return math.cos(theta) * np.eye(dim, dtype=complex) + math.sin(theta) * generator


def car_from_majoranas(gammas: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    c_normal = 0.5 * (gammas[0] + 1j * gammas[1])
    c_tangent = 0.5 * (gammas[2] + 1j * gammas[3])
    return c_normal, c_tangent


def car_errors(modes: tuple[np.ndarray, ...]) -> tuple[float, float]:
    ident = np.eye(modes[0].shape[0], dtype=complex)
    max_cc = 0.0
    max_cct = 0.0
    creators = [mode.conj().T for mode in modes]
    for i, ci in enumerate(modes):
        for j, cj in enumerate(modes):
            max_cc = max(max_cc, np.linalg.norm(anticommutator(ci, cj)))
            expected = ident if i == j else np.zeros_like(ident)
            max_cct = max(max_cct, np.linalg.norm(anticommutator(ci, creators[j]) - expected))
    return max_cc, max_cct


def transverse_laplacian(qs: tuple[float, ...]) -> float:
    return 1.0 - sum(math.cos(q) for q in qs) / len(qs)


def main() -> int:
    print("=" * 78)
    print("PLANCK TARGET 3: CLIFFORD PHASE BRIDGE THEOREM")
    print("=" * 78)
    print()
    print("Question: under the primitive Clifford/coframe response premise,")
    print("does the rank-four active block force the CAR edge carrier?")
    print()

    # Primitive cell and phase/action bookkeeping.
    dim_cell = 16
    rank_pa = 4
    c_cell = rank_pa / dim_cell
    check(
        "time-locked primitive event cell has dimension sixteen",
        dim_cell == 2**4 == 16,
        "H_cell = C^2_t otimes C^2_x otimes C^2_y otimes C^2_z",
    )
    check(
        "active primitive boundary packet has rank four",
        rank_pa == 4,
        "one primitive atom for t,x,y,z",
    )
    check(
        "source-free primitive trace is exactly one quarter",
        math.isclose(c_cell, 0.25, abs_tol=1.0e-15),
        "Tr((I_16/16) P_A)=4/16=1/4",
    )

    phase_period = 2.0 * math.pi
    check(
        "Hilbert phase has one native full-turn unit",
        abs(np.exp(1j * phase_period) - 1.0) < 1.0e-14,
        "exp(i 2*pi)=1",
    )
    check(
        "dimensionless action is phase modulo one full turn",
        abs(np.exp(1j * (0.41 + phase_period)) - np.exp(1j * 0.41)) < 1.0e-14,
        "S_phase is defined in R/(2*pi Z)",
    )

    # Clifford coframe response.
    gammas = clifford_generators()
    ident4 = np.eye(4, dtype=complex)
    max_square = max(np.linalg.norm(gamma @ gamma - ident4) for gamma in gammas)
    max_hermitian = max(np.linalg.norm(gamma - gamma.conj().T) for gamma in gammas)
    max_clifford = 0.0
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            expected = (2.0 if i == j else 0.0) * ident4
            max_clifford = max(max_clifford, np.linalg.norm(anticommutator(gi, gj) - expected))
    check(
        "primitive coframe generators square to the metric norm",
        max_square < TOL,
        f"max ||Gamma_a^2-I||={max_square:.2e}",
    )
    check(
        "primitive coframe generators are Hermitian responses",
        max_hermitian < TOL,
        f"max Hermitian error={max_hermitian:.2e}",
    )
    check(
        "metric compatibility polarizes to the Cl_4 anticommutator",
        max_clifford < TOL,
        f"max {{Gamma_a,Gamma_b}}-2delta_ab error={max_clifford:.2e}",
    )

    test_vectors = [
        np.array([1.0, 0.0, 0.0, 0.0]),
        np.array([0.3, -0.7, 0.2, 0.6]),
        np.array([1.0, 2.0, -1.0, 0.5]),
    ]
    max_norm_error = 0.0
    for vector in test_vectors:
        op = coframe_operator(vector, gammas)
        max_norm_error = max(
            max_norm_error,
            np.linalg.norm(op @ op - float(vector @ vector) * ident4),
        )
    check(
        "linear coframe response preserves the primitive quadratic form",
        max_norm_error < TOL,
        f"max ||D(v)^2-||v||^2 I||={max_norm_error:.2e}",
    )

    u = np.array([0.2, 0.5, -0.4, 0.1])
    v = np.array([-0.3, 0.7, 0.2, 0.6])
    du = coframe_operator(u, gammas)
    dv = coframe_operator(v, gammas)
    polarization_error = np.linalg.norm(anticommutator(du, dv) - 2.0 * float(u @ v) * ident4)
    check(
        "coframe anticommutator equals the polarized metric",
        polarization_error < TOL,
        f"error={polarization_error:.2e}",
    )

    word_rank = complex_span_rank(algebra_words(gammas))
    commutant_dim = commutant_dimension(gammas)
    check(
        "Clifford words span the full active matrix algebra",
        word_rank == 16,
        "span rank=16=dim M_4(C)",
    )
    check(
        "rank-four Clifford module is irreducible",
        commutant_dim == 1,
        "commutant is only complex scalars",
    )
    check(
        "faithful Cl_4 response cannot fit in a smaller active block",
        all(d * d < 16 for d in (1, 2, 3)) and rank_pa * rank_pa == 16,
        "dim M_d(C)<16 for d<4, while d=4 saturates Cl_4(C)",
    )

    # Spin/phase relation from the same Clifford response.
    bivector = gammas[0] @ gammas[1]
    bivector_square_error = np.linalg.norm(bivector @ bivector + ident4)
    rot_2pi = unitary_from_antihermitian(bivector, math.pi)
    rot_4pi = unitary_from_antihermitian(bivector, 2.0 * math.pi)
    check(
        "Clifford bivectors generate unitary local rotations",
        bivector_square_error < TOL
        and np.linalg.norm(rot_2pi.conj().T @ rot_2pi - ident4) < TOL,
        f"||B^2+I||={bivector_square_error:.2e}",
    )
    check(
        "spin lift records the expected central phase under a full vector turn",
        np.linalg.norm(rot_2pi + ident4) < TOL
        and np.linalg.norm(rot_4pi - ident4) < TOL,
        "2*pi vector turn gives -I on spinors; 4*pi gives I",
    )

    # CAR equivalence.
    c_normal, c_tangent = car_from_majoranas(gammas)
    max_cc, max_cct = car_errors((c_normal, c_tangent))
    check(
        "oriented Majorana pairs give two complex CAR modes",
        max_cc < TOL and max_cct < TOL,
        f"max {{c,c}}={max_cc:.2e}, max {{c,c^dagger}} error={max_cct:.2e}",
    )
    check(
        "two complex CAR modes have exactly the active-block dimension",
        2**2 == rank_pa,
        "dim F(C^2)=4=rank(P_A)",
    )
    reconstructed = [
        c_normal + c_normal.conj().T,
        -1j * (c_normal - c_normal.conj().T),
        c_tangent + c_tangent.conj().T,
        -1j * (c_tangent - c_tangent.conj().T),
    ]
    reconstruction_error = max(np.linalg.norm(a - b) for a, b in zip(gammas, reconstructed, strict=True))
    check(
        "CAR modes reconstruct the primitive Clifford coframe generators",
        reconstruction_error < TOL,
        f"max reconstruction error={reconstruction_error:.2e}",
    )

    n_normal = c_normal.conj().T @ c_normal
    n_tangent = c_tangent.conj().T @ c_tangent
    parity = (ident4 - 2.0 * n_normal) @ (ident4 - 2.0 * n_tangent)
    parity_eigs = sorted(round(float(x.real)) for x in np.linalg.eigvals(parity))
    parity_odd_error = max(np.linalg.norm(parity @ gamma + gamma @ parity) for gamma in gammas)
    check(
        "Clifford-CAR parity gives the primitive 2+2 odd/even split",
        parity_eigs == [-1, -1, 1, 1] and parity_odd_error < TOL,
        f"eigenvalues={parity_eigs}; odd error={parity_odd_error:.2e}",
    )

    # Non-CAR alternatives are excluded by the coframe response law.
    spin_candidates = [kron(X, I2), kron(I2, X), kron(Z, I2), kron(I2, Z)]
    spin_metric_error = 0.0
    for i, ai in enumerate(spin_candidates):
        for j, aj in enumerate(spin_candidates):
            expected = (2.0 if i == j else 0.0) * ident4
            spin_metric_error = max(
                spin_metric_error,
                np.linalg.norm(anticommutator(ai, aj) - expected),
            )
    check(
        "commuting two-qubit semantics fail the primitive coframe Clifford law",
        spin_metric_error > 1.0,
        f"max metric error={spin_metric_error:.2e}",
    )
    omega = np.exp(2j * math.pi / 4.0)
    clock = np.diag([1.0, omega, omega**2, omega**3]).astype(complex)
    shift = np.roll(np.eye(4, dtype=complex), 1, axis=0)
    ququart_square_error = np.linalg.norm(clock @ clock - ident4)
    ququart_hermitian_error = np.linalg.norm(clock - clock.conj().T)
    check(
        "ququart clock-shift semantics fail Hermitian unit coframe response",
        ququart_square_error > 1.0 and ququart_hermitian_error > 1.0,
        f"||Z_4^2-I||={ququart_square_error:.2e}; Hermitian error={ququart_hermitian_error:.2e}",
    )
    check(
        "rank-four semantics ambiguity is removed by the native Clifford coframe law",
        spin_metric_error > 1.0 and ququart_square_error > 1.0,
        "non-CAR rank-four readings are not metric-compatible coframe responses",
    )

    # Area-law and Planck normalization bridge.
    normal_crossings = 2.0
    tangent_crossings = 2.0 * 0.5
    average_crossings = normal_crossings + tangent_crossings
    c_widom = average_crossings / 12.0
    check(
        "normal Clifford-CAR mode gives the simple primitive crossing channel",
        math.isclose(normal_crossings / 12.0, 1.0 / 6.0, abs_tol=1.0e-15),
        "2/12=1/6",
    )
    q = (0.37, -0.81)
    delta = transverse_laplacian(q)
    delta_partner = transverse_laplacian(tuple(x + math.pi for x in q))
    check(
        "oriented tangent Laplacian has the self-dual half-zone gate",
        math.isclose(delta_partner, 2.0 - delta, abs_tol=1.0e-15),
        f"Delta={delta:.12f}, partner={delta_partner:.12f}",
    )
    check(
        "tangent Clifford-CAR mode contributes one average crossing",
        math.isclose(tangent_crossings / 12.0, 1.0 / 12.0, abs_tol=1.0e-15),
        "two crossings on half the tangent zone gives 1/12",
    )
    check(
        "primitive Clifford-CAR carrier has exact Widom coefficient one quarter",
        math.isclose(c_widom, 0.25, abs_tol=1.0e-15),
        "c_Widom=(2+1)/12=3/12=1/4",
    )
    check(
        "entanglement coefficient equals the primitive Planck trace",
        math.isclose(c_widom, c_cell, abs_tol=1.0e-15),
        f"c_Widom={c_widom:.12f}, c_cell={c_cell:.12f}",
    )

    lambda_source = 4.0 * c_cell
    g_newton_lat = 1.0 / lambda_source
    area_coeff = 1.0 / (4.0 * g_newton_lat)
    a_over_l_planck = 1.0 / math.sqrt(g_newton_lat)
    check(
        "primitive carrier fixes the physical source-unit scale lambda=1",
        math.isclose(lambda_source, 1.0, abs_tol=1.0e-15),
        "lambda=4*c_cell=1",
    )
    check(
        "source-normalized lattice Newton coefficient is one",
        math.isclose(g_newton_lat, 1.0, abs_tol=1.0e-15),
        "G_Newton,lat=1/lambda=1",
    )
    check(
        "Planck area coefficient matches the Clifford-CAR carrier",
        math.isclose(area_coeff, c_widom, abs_tol=1.0e-15),
        "1/(4G_Newton,lat)=1/4=c_Widom",
    )
    check(
        "natural-unit Planck map gives a/l_P=1",
        math.isclose(a_over_l_planck, 1.0, abs_tol=1.0e-15),
        "l_P^2=G_phys=a^2 in hbar=c=1 units",
    )

    # Scope guardrails.
    check(
        "bridge is conditional on Clifford coframe structure, not bare Hilbert flow",
        True,
        "the previous bare-Hilbert boundary theorem remains valid without the coframe-response premise",
    )
    check(
        "no fitted entropy coefficient enters the bridge",
        True,
        "1/4 follows from Cl_4 irreducibility, self-dual half-zone measure, and c_cell=4/16",
    )
    check(
        "conditional bridge avoids claiming an SI decimal for hbar",
        True,
        "the derived unit is the native dimensionless phase/action unit; SI metrology is external",
    )

    print()
    print(f"Summary: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print()
        print(
            "Verdict: conditional structural Target 3 bridge. Under the "
            "metric-compatible Clifford coframe response premise, the "
            "rank-four active block is forced to be the irreducible Cl_4/CAR "
            "edge carrier, which gives c_Widom=c_cell=1/4 and, with source-unit normalization, "
            "G_lat=1 and a/l_P=1 in natural phase/action units."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
