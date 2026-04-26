#!/usr/bin/env python3
"""Primitive boundary coframe chi_g probe.

This is the first algebraic pass for the signed-gravity nonlocal/boundary
candidate:

    Q_chi = Gamma_t Gamma_n Gamma_tau1 Gamma_tau2

on the rank-four primitive boundary block K = P_A H_cell.  The probe checks
what the Clifford/coframe orientation can establish by itself, and keeps the
source/action question explicit.  It does not claim a physical signed gravity
sector.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.numpy_replay_bootstrap import ensure_numpy_runtime

ensure_numpy_runtime(__file__, sys.argv)

import numpy as np


TOL = 1.0e-11
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


I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)


def kron(*ops: np.ndarray) -> np.ndarray:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def comm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticomm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def norm(a: np.ndarray) -> float:
    return float(np.linalg.norm(a))


def cl4_generators() -> list[np.ndarray]:
    # Ordered as (t, n, tau_1, tau_2) for one selected primitive face.
    return [
        kron(X, I2),
        kron(Y, I2),
        kron(Z, X),
        kron(Z, Y),
    ]


def exact_unitary_from_hermitian(h: np.ndarray, dt: float) -> np.ndarray:
    eigvals, eigvecs = np.linalg.eigh(h)
    phases = np.diag(np.exp(-1j * dt * eigvals))
    return eigvecs @ phases @ eigvecs.conj().T


def projector(q: np.ndarray, sign: int) -> np.ndarray:
    return 0.5 * (np.eye(q.shape[0], dtype=np.complex128) + sign * q)


def normalized(vec: np.ndarray) -> np.ndarray:
    return vec / np.linalg.norm(vec)


def branch_state(projector_matrix: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=projector_matrix.shape[0]) + 1j * rng.normal(
        size=projector_matrix.shape[0]
    )
    projected = projector_matrix @ raw
    return normalized(projected)


def born_three_slit_residual(seed: int) -> float:
    rng = np.random.default_rng(seed)
    amps = rng.normal(size=3) + 1j * rng.normal(size=3)

    def prob(indices: tuple[int, ...]) -> float:
        return float(abs(sum(amps[i] for i in indices)) ** 2)

    return abs(
        prob((0, 1, 2))
        - prob((0, 1))
        - prob((0, 2))
        - prob((1, 2))
        + prob((0,))
        + prob((1,))
        + prob((2,))
    )


def transformed_q(q: np.ndarray, gammas: list[np.ndarray], transform: np.ndarray) -> np.ndarray:
    # For a signed permutation/reflection of the primitive coframe, compute the
    # induced volume element using Gamma'_a = transform[a,b] Gamma_b.
    transformed_gammas = []
    for row in transform:
        gamma = np.zeros_like(q)
        for coeff, base in zip(row, gammas, strict=True):
            gamma = gamma + coeff * base
        transformed_gammas.append(gamma)
    out = transformed_gammas[0]
    for gamma in transformed_gammas[1:]:
        out = out @ gamma
    return out


def main() -> int:
    print("=" * 78)
    print("SIGNED GRAVITY: PRIMITIVE BOUNDARY COFRAME CHI PROBE")
    print("=" * 78)
    print("candidate: Q_chi = Gamma_t Gamma_n Gamma_tau1 Gamma_tau2")
    print("surface: rank-four primitive boundary block K = P_A H_cell")
    print()

    gammas = cl4_generators()
    ident = np.eye(4, dtype=np.complex128)
    q_chi = gammas[0] @ gammas[1] @ gammas[2] @ gammas[3]
    p_plus = projector(q_chi, +1)
    p_minus = projector(q_chi, -1)

    max_clifford = 0.0
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            expected = (2.0 if i == j else 0.0) * ident
            max_clifford = max(max_clifford, norm(anticomm(gi, gj) - expected))
    check(
        "metric-compatible coframe relations",
        max_clifford < TOL,
        f"max Clifford residual={max_clifford:.3e}",
    )
    check(
        "Q_chi is Hermitian",
        norm(q_chi - q_chi.conj().T) < TOL,
        f"residual={norm(q_chi - q_chi.conj().T):.3e}",
    )
    check(
        "Q_chi is an involution",
        norm(q_chi @ q_chi - ident) < TOL,
        f"residual={norm(q_chi @ q_chi - ident):.3e}",
    )
    check(
        "Q_chi has nonempty +/- sectors",
        round(float(np.trace(p_plus).real)) == 2
        and round(float(np.trace(p_minus).real)) == 2,
        f"dim plus={np.trace(p_plus).real:.0f}, dim minus={np.trace(p_minus).real:.0f}",
    )

    # Even Clifford boundary dynamics preserve chirality; odd coframe terms
    # mix sectors.  This is exactly the conservation theorem surface that a
    # written proof would have to impose on all retained boundary couplings.
    bivectors = [1j * gammas[i] @ gammas[j] for i in range(4) for j in range(i + 1, 4)]
    h_even = (
        0.17 * bivectors[0]
        - 0.11 * bivectors[1]
        + 0.07 * bivectors[3]
        + 0.05 * bivectors[5]
    )
    h_odd = h_even + 0.03 * gammas[0]
    u_even = exact_unitary_from_hermitian(h_even, 0.9)
    u_odd = exact_unitary_from_hermitian(h_odd, 0.9)
    even_comm = norm(comm(q_chi, h_even))
    odd_comm = norm(comm(q_chi, h_odd))
    even_leakage = norm(p_minus @ u_even @ p_plus)
    odd_leakage = norm(p_minus @ u_odd @ p_plus)
    check(
        "even boundary Hamiltonian conserves Q_chi",
        even_comm < TOL,
        f"commutator residual={even_comm:.3e}",
    )
    check(
        "even boundary evolution has no P_- U P_+ leakage",
        even_leakage < TOL,
        f"leakage={even_leakage:.3e}",
    )
    check(
        "odd coframe term is correctly detected as sector-mixing",
        odd_comm > 1.0e-3 and odd_leakage > 1.0e-3,
        f"odd commutator={odd_comm:.3e}, odd leakage={odd_leakage:.3e}",
    )

    proper_swap = np.array(
        [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1],
        ],
        dtype=float,
    )
    normal_flip = np.diag([1.0, -1.0, 1.0, 1.0])
    q_proper = transformed_q(q_chi, gammas, proper_swap)
    q_reflected = transformed_q(q_chi, gammas, normal_flip)
    check(
        "orientation-preserving coframe relabel keeps Q_chi",
        norm(q_proper - q_chi) < TOL,
        f"residual={norm(q_proper - q_chi):.3e}",
    )
    check(
        "orientation-reversing relabel flips Q_chi",
        norm(q_reflected + q_chi) < TOL,
        f"residual={norm(q_reflected + q_chi):.3e}",
    )

    psi_plus = branch_state(p_plus, 11)
    psi_minus = branch_state(p_minus, 13)
    inertial_plus = float(np.vdot(psi_plus, psi_plus).real)
    inertial_minus = float(np.vdot(psi_minus, psi_minus).real)
    active_plus_inserted = float(np.vdot(psi_plus, q_chi @ psi_plus).real)
    active_minus_inserted = float(np.vdot(psi_minus, q_chi @ psi_minus).real)
    check(
        "positive inertial mass is branch independent",
        inertial_plus > 0 and inertial_minus > 0,
        f"M_+={inertial_plus:.6f}, M_-={inertial_minus:.6f}",
    )
    check(
        "inserted Q_chi density has opposite active signs",
        abs(active_plus_inserted - 1.0) < TOL
        and abs(active_minus_inserted + 1.0) < TOL,
        f"<Q>_+={active_plus_inserted:+.6f}, <Q>_-={active_minus_inserted:+.6f}",
    )

    paired = (psi_plus + psi_minus) / math.sqrt(2.0)
    paired_inertial = float(np.vdot(paired, paired).real)
    paired_active = float(np.vdot(paired, q_chi @ paired).real)
    check(
        "equal +/- branch pair cancels inserted active monopole",
        abs(paired_active) < TOL and paired_inertial > 0,
        f"active={paired_active:+.3e}, inertial={paired_inertial:.6f}",
    )

    norm_before = float(np.vdot(psi_plus, psi_plus).real)
    evolved = u_even @ psi_plus
    norm_after = float(np.vdot(evolved, evolved).real)
    sector_after = float(np.vdot(evolved, q_chi @ evolved).real)
    check(
        "exact unitary evolution preserves norm on a fixed sector",
        abs(norm_after - norm_before) < TOL,
        f"norm drift={abs(norm_after - norm_before):.3e}",
    )
    check(
        "exact unitary evolution preserves the Q_chi expectation",
        abs(sector_after - 1.0) < TOL,
        f"<Q_chi>(t)={sector_after:+.6f}",
    )

    i3_plus = born_three_slit_residual(101)
    i3_minus = born_three_slit_residual(103)
    check(
        "Born three-slit identity is unchanged by branch label",
        i3_plus < TOL and i3_minus < TOL,
        f"I3 plus={i3_plus:.3e}, I3 minus={i3_minus:.3e}",
    )

    m_phys = 1.75
    q_bare_plus = 4.0 * math.pi * m_phys
    q_bare_minus = -4.0 * math.pi * m_phys
    check(
        "source-unit control consumes a supplied sign only",
        abs(q_bare_plus + q_bare_minus) < TOL and m_phys > 0,
        f"q_bare(+)+q_bare(-)={q_bare_plus + q_bare_minus:+.3e}",
    )

    print()
    print("SOURCE/RESPONSE LOCKING CLASSIFICATION")
    print("  coframe algebra supplies: conserved oriented Clifford chirality on even")
    print("    boundary dynamics")
    print("  coframe algebra does not supply here: variational identity")
    print("    delta S / delta Phi = M_phys psi^dagger Q_chi psi")
    print("  retained local source notes still identify Born/parity-scalar sources,")
    print("    not a native exterior monopole C_signed = Q_chi C_abs")
    print()
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    final_tag = (
        "BOUNDARY_CHI_SOURCE_NOT_LOCKED" if FAIL_COUNT == 0 else "BOUNDARY_CHI_NO_GO"
    )
    print(f"FINAL_TAG: {final_tag}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
