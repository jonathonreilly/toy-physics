#!/usr/bin/env python3
"""Probe a nonlocal projector-difference chi_g candidate.

This is a first concrete pass on Candidate C from the nonlocal/boundary target
note.  It tests the formal algebra of

    Q_chi = P_+ - P_-

on a global two-sector extension of a local staggered chain.  The harness keeps
two questions separate:

  1. Does an externally supplied superselected sector label behave coherently?
  2. Is that label native to the retained scalar source action?

The first can pass as a control.  The second is the hard source-locking gate and
is not derived by this toy projector split.
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


EPS = 1e-11


def fro_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, ord="fro"))


def passfail(condition: bool) -> str:
    return "PASS" if condition else "FAIL"


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm == 0:
        raise ValueError("cannot normalize a zero state")
    return state / norm


def projector(position_count: int, sector_index: int) -> np.ndarray:
    local = np.zeros((position_count, position_count), dtype=np.complex128)
    local[sector_index, sector_index] = 1.0
    return local


def local_chain_hamiltonian(position_count: int, mass: float = 0.37) -> np.ndarray:
    parity = np.diag([1.0 if x % 2 == 0 else -1.0 for x in range(position_count)])
    h = mass * parity.astype(np.complex128)
    for x in range(position_count - 1):
        h[x, x + 1] = -0.5j
        h[x + 1, x] = 0.5j
    return h


def unitary_from_hamiltonian(h: np.ndarray, time: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(h)
    phases = np.exp(-1j * time * vals)
    return (vecs * phases) @ vecs.conj().T


def born_i3(a: complex, b: complex, c: complex) -> float:
    p_abc = abs(a + b + c) ** 2
    p_ab = abs(a + b) ** 2
    p_ac = abs(a + c) ** 2
    p_bc = abs(b + c) ** 2
    p_a = abs(a) ** 2
    p_b = abs(b) ** 2
    p_c = abs(c) ** 2
    return float(p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c)


def finite_difference_source_residual(
    state: np.ndarray,
    source_matrix: np.ndarray,
    density: np.ndarray,
    position_count: int,
    sector_count: int,
    source_mass: float,
) -> float:
    step = 2e-6
    numeric = []
    for x in range(position_count):
        phi = np.zeros(position_count)
        phi[x] = step
        h_plus = source_mass * np.kron(np.diag(phi), source_matrix)
        h_minus = -h_plus
        e_plus = float(np.vdot(state, h_plus @ state).real)
        e_minus = float(np.vdot(state, h_minus @ state).real)
        numeric.append((e_plus - e_minus) / (2.0 * step))
    del sector_count
    return float(np.max(np.abs(np.array(numeric) - density)))


def position_sector_state(
    position_count: int,
    sector_count: int,
    position_index: int,
    sector_vector: np.ndarray,
) -> np.ndarray:
    local = np.zeros(position_count, dtype=np.complex128)
    local[position_index] = 1.0
    return np.kron(local, normalize(sector_vector))


def sector_density(
    state: np.ndarray,
    position_count: int,
    sector_operator: np.ndarray,
    source_mass: float,
) -> np.ndarray:
    reshaped = state.reshape(position_count, sector_operator.shape[0])
    out = np.zeros(position_count)
    for x in range(position_count):
        sx = reshaped[x]
        out[x] = source_mass * float(np.vdot(sx, sector_operator @ sx).real)
    return out


def inertial_density(state: np.ndarray, position_count: int, source_mass: float) -> np.ndarray:
    reshaped = state.reshape(position_count, -1)
    return source_mass * np.sum(np.abs(reshaped) ** 2, axis=1).real


def force_prefactor(source_sign: int, response_sign: int) -> int:
    return source_sign * response_sign


def main() -> None:
    position_count = 8
    sector_count = 2
    source_mass = 1.7

    i_pos = np.eye(position_count, dtype=np.complex128)
    i_sec = np.eye(sector_count, dtype=np.complex128)
    q_sec = np.diag([1.0, -1.0]).astype(np.complex128)
    x_sec = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    p_plus_sec = 0.5 * (i_sec + q_sec)
    p_minus_sec = 0.5 * (i_sec - q_sec)

    q_chi = np.kron(i_pos, q_sec)
    p_plus = np.kron(i_pos, p_plus_sec)
    p_minus = np.kron(i_pos, p_minus_sec)

    h_local = local_chain_hamiltonian(position_count)
    h_retained = np.kron(h_local, i_sec)
    h_mixing = h_retained + 0.025 * np.kron(i_pos, x_sec)
    u_retained = unitary_from_hamiltonian(h_retained, time=1.4)

    parity = np.diag([1.0 if x % 2 == 0 else -1.0 for x in range(position_count)])
    epsilon_retained = np.kron(parity.astype(np.complex128), i_sec)

    psi_plus = position_sector_state(position_count, sector_count, 3, np.array([1.0, 0.0]))
    psi_minus = position_sector_state(position_count, sector_count, 3, np.array([0.0, 1.0]))
    psi_equal_pair = normalize(psi_plus + psi_minus)
    psi_weighted = normalize(2.0 * psi_plus + psi_minus)

    rho_q_plus = sector_density(psi_plus, position_count, q_sec, source_mass)
    rho_q_pair = sector_density(psi_equal_pair, position_count, q_sec, source_mass)
    rho_inert_pair = inertial_density(psi_equal_pair, position_count, source_mass)

    scalar_density_plus = source_mass * np.diag(parity) * inertial_density(
        psi_plus, position_count, 1.0
    )
    projector_source_residual = finite_difference_source_residual(
        psi_plus, q_sec, rho_q_plus, position_count, sector_count, source_mass
    )
    scalar_source_residual = finite_difference_source_residual(
        psi_plus, i_sec, source_mass * inertial_density(psi_plus, position_count, 1.0),
        position_count, sector_count, source_mass
    )

    sector_expect_weighted = float(np.vdot(psi_weighted, q_chi @ psi_weighted).real)
    q_rotated = np.kron(i_pos, x_sec)
    rotated_expect_same_state = float(np.vdot(psi_plus, q_rotated @ psi_plus).real)
    plus_as_x_branch = normalize(psi_plus + psi_minus)
    x_branch_expect = float(np.vdot(plus_as_x_branch, q_rotated @ plus_as_x_branch).real)

    born_residual = born_i3(0.30 + 0.20j, -0.17 + 0.11j, 0.07 - 0.23j)
    norm_before = float(np.vdot(psi_weighted, psi_weighted).real)
    norm_after = float(np.vdot(u_retained @ psi_weighted, u_retained @ psi_weighted).real)

    same_sector_force = force_prefactor(+1, +1)
    opposite_sector_force = force_prefactor(+1, -1)
    action_reaction_residual = abs(force_prefactor(+1, -1) - force_prefactor(-1, +1))

    epsilon_plus_block = p_plus @ epsilon_retained @ p_plus
    epsilon_minus_block = p_minus @ epsilon_retained @ p_minus
    plus_epsilon_eigs = np.linalg.eigvalsh(epsilon_plus_block[p_plus.diagonal().real > 0.5][:, p_plus.diagonal().real > 0.5])
    minus_epsilon_eigs = np.linalg.eigvalsh(epsilon_minus_block[p_minus.diagonal().real > 0.5][:, p_minus.diagonal().real > 0.5])

    conserved_residual = max(fro_norm(p_plus @ h_retained - h_retained @ p_plus), fro_norm(p_minus @ h_retained - h_retained @ p_minus))
    mixing_residual = max(fro_norm(p_plus @ h_mixing - h_mixing @ p_plus), fro_norm(p_minus @ h_mixing - h_mixing @ p_minus))
    leakage = fro_norm(p_minus @ u_retained @ p_plus)

    q_bare_plus = 4.0 * math.pi * float(np.sum(rho_q_plus))
    q_bare_pair = 4.0 * math.pi * float(np.sum(rho_q_pair))

    formal_controls_pass = (
        fro_norm(q_chi - q_chi.conj().T) < EPS
        and fro_norm(q_chi @ q_chi - np.eye(position_count * sector_count)) < EPS
        and conserved_residual < EPS
        and leakage < EPS
        and float(np.sum(rho_inert_pair)) > 0.0
        and abs(float(np.sum(rho_q_pair))) < EPS
        and abs(born_residual) < EPS
        and abs(norm_after - norm_before) < EPS
        and action_reaction_residual == 0
    )

    scalar_pinning_fails = (
        np.min(plus_epsilon_eigs) < -0.5
        and np.max(plus_epsilon_eigs) > 0.5
        and np.min(minus_epsilon_eigs) < -0.5
        and np.max(minus_epsilon_eigs) > 0.5
    )
    basis_ambiguous = abs(rotated_expect_same_state) < EPS and abs(x_branch_expect - 1.0) < EPS
    source_inserted = projector_source_residual < 5e-10 and np.max(np.abs(scalar_density_plus - rho_q_plus)) > 1.0

    final_tag = (
        "NONLOCAL_PROJECTOR_FORMAL_CONTROL_ONLY"
        if formal_controls_pass and scalar_pinning_fails and basis_ambiguous and source_inserted
        else "NONLOCAL_PROJECTOR_PROBE_INCONCLUSIVE"
    )

    print("=" * 92)
    print("SIGNED GRAVITY NONLOCAL PROJECTOR-DIFFERENCE CHARGE PROBE")
    print("  Candidate C: Q_chi = P_+ - P_- on an external two-sector extension")
    print("=" * 92)
    print()
    print("PROJECTOR ALGEBRA")
    print(f"  Q Hermitian residual: {fro_norm(q_chi - q_chi.conj().T):.3e}")
    print(f"  Q^2-I residual:       {fro_norm(q_chi @ q_chi - np.eye(position_count * sector_count)):.3e}")
    print(f"  sector dimensions:    +{int(round(np.trace(p_plus).real))} / -{int(round(np.trace(p_minus).real))}")
    print()
    print("CONSERVATION / SUPERSELECTION")
    print(f"  [P_+/-, H_retained] residual: {conserved_residual:.3e}  {passfail(conserved_residual < EPS)}")
    print(f"  P_- U_retained P_+ leakage:   {leakage:.3e}  {passfail(leakage < EPS)}")
    print(f"  sector-mixing perturbation residual: {mixing_residual:.3e}  control should fail if allowed")
    print()
    print("SCALAR-SOURCE PINNING")
    print(f"  epsilon spectrum in P_+ sector: [{np.min(plus_epsilon_eigs):+.1f}, {np.max(plus_epsilon_eigs):+.1f}]")
    print(f"  epsilon spectrum in P_- sector: [{np.min(minus_epsilon_eigs):+.1f}, {np.max(minus_epsilon_eigs):+.1f}]")
    print(f"  scalar pinning status: {passfail(not scalar_pinning_fails)}")
    print()
    print("SOURCE / RESPONSE LOCKING")
    print(f"  inserted projector-source finite-difference residual: {projector_source_residual:.3e}")
    print(f"  positive Born-source finite-difference residual:       {scalar_source_residual:.3e}")
    print("  retained scalar source is not changed by the projector unless the Q source action is added")
    print(f"  same-sector force prefactor:     {same_sector_force:+d}")
    print(f"  opposite-sector force prefactor: {opposite_sector_force:+d}")
    print(f"  action-reaction prefactor residual when source=response sign: {action_reaction_residual:.3e}")
    print()
    print("POSITIVE INERTIAL MASS / NULL CONTROLS")
    print(f"  pure + active charge:       {float(np.sum(rho_q_plus)):+.6f}")
    print(f"  equal +/- active charge:    {float(np.sum(rho_q_pair)):+.6e}")
    print(f"  equal +/- inertial mass:    {float(np.sum(rho_inert_pair)):.6f}")
    print(f"  q_bare pure +:              {q_bare_plus:+.6f}")
    print(f"  q_bare equal +/-:           {q_bare_pair:+.6e}")
    print()
    print("BORN / NORM CONTROLS")
    print(f"  Born I3 residual:           {born_residual:+.3e}")
    print(f"  unitary norm drift:         {abs(norm_after - norm_before):.3e}")
    print()
    print("BASIS / MIXED-SUPERPOSITION AMBIGUITY")
    print(f"  weighted superposition <Q>:         {sector_expect_weighted:+.6f}")
    print(f"  same state under rotated Q=X:       {rotated_expect_same_state:+.6f}")
    print(f"  equal +/- state as X-branch <X>:    {x_branch_expect:+.6f}")
    print("  mixed states have expectation-valued active charge unless sectors are superselected")
    print()
    print("VERDICT")
    print("  The external projector split passes the formal conserved-sector controls.")
    print("  It does not by itself derive a native signed source from the retained scalar action,")
    print("  does not pin the local scalar source, and is basis-dependent without an independent")
    print("  boundary/global constraint that fixes P_+ and P_-.")
    print(f"FINAL_TAG: {final_tag}")


if __name__ == "__main__":
    main()
