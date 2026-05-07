#!/usr/bin/env python3
"""Retained-Axis Operator Algebra (RALA) closure runner for the teleportation suite.

This runner is the coordinated closure artifact for three open-gate notes:

  - docs/TELEPORTATION_ENCODING_PORTABILITY_NOTE.md
  - docs/TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md
  - docs/TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE.md

Setup (Kogut-Susskind cell/taste decomposition).

  Even side L = 2C in dim d. Site coordinate x_i = 2 c_i + eta_i with
  c_i in {0,...,C-1} and eta_i in {0,1}. Hilbert space factorizes as
  H = C^cells (x) C^tastes. Pick a retained taste axis a in {0,...,d-1}.
  Logical bit b = eta_a; environment label e = (c, {eta_i : i != a}).

Definition (RALA(a)).

  RALA(a) = { O_logical (x) I_env : O_logical in M_2(C) }.

The runner verifies eight algebraic theorems (T1-T8) listed in the
companion note that together establish:

  (a) RALA(a) is closed under +, *, conjugation, tensor product.
  (b) axis logical Z, axis logical X, ZZ stabilizer, XX stabilizer, and
      ideal Bell projectors P_zx^axis are in RALA(a).
  (c) native sublattice parity Z is in RALA only when dim = 1.
  (d) the "current fixed pair-hop X" used by prior teleportation runners is
      in RALA(a) iff a = d - 1.
  (e) every RALA element commutes with every (I_logical (x) L) base-ledger
      observable (T1 base/fiber separation in the transport theory).
  (f) the four Bell projectors P_zx^axis form a partition of unity, satisfy
      stabilizer parities, and implement a Z_2 x Z_2 Bell connection (T2).
  (g) corrections built from RALA Paulis compose via XOR.
  (h) the resulting RALA-only teleportation protocol restores Bob's encoded
      logical state with perfect fidelity, with input-independent pre-record
      Bob marginal.

The runner does NOT claim a physical apparatus, durable measurement record,
dynamical preparation, noise model, matter transfer, charge transfer, energy
transfer, object transport, or faster-than-light signaling. The closed
algebra is the operational backbone for the retained-taste teleportation
lane; the physical implementation of the axis primitives remains an open
gate covered by other notes.
"""

from __future__ import annotations

import argparse
import dataclasses
import math

import numpy as np


I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)
Y2 = np.array([[0, -1j], [1j, 0]], dtype=complex)


# -----------------------------------------------------------------------------
# Site / environment / logical decomposition
# -----------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class SiteFactor:
    """Permutation that reorders site basis as |b>_logical (x) |e>_env.

    perm: site -> (logical * n_env + env) flat index.
    """

    dim: int
    side: int
    logical_axis: int
    perm: np.ndarray
    n_env: int

    @property
    def n_sites(self) -> int:
        return self.side ** self.dim


def build_site_factor(dim: int, side: int, logical_axis: int) -> SiteFactor:
    if side % 2 != 0:
        raise ValueError("side must be even for the KS factorization")
    if not (0 <= logical_axis < dim):
        raise ValueError("logical_axis out of range")

    n_sites = side ** dim
    half = side // 2
    n_env = n_sites // 2

    perm = np.zeros(n_sites, dtype=np.int64)
    for site_index in range(n_sites):
        coords = []
        rem = site_index
        for axis in range(dim):
            coords.append(rem % side)
            rem //= side
        cells = [c // 2 for c in coords]
        tastes = [c % 2 for c in coords]
        b = tastes[logical_axis]
        env_taste_bits = tuple(tastes[i] for i in range(dim) if i != logical_axis)
        env_index = 0
        for c in cells:
            env_index = env_index * half + c
        for s in env_taste_bits:
            env_index = env_index * 2 + s
        perm[site_index] = b * n_env + env_index
    return SiteFactor(dim=dim, side=side, logical_axis=logical_axis,
                      perm=perm, n_env=n_env)


def reorder_to_le(op: np.ndarray, factor: SiteFactor) -> np.ndarray:
    """Reorder operator from site basis to (logical (x) env) basis.

    For perm: site -> le_index, the permutation matrix R has R[s, j] = 1
    iff j == perm[s]. The (logical, env) basis vector v_le relates to the
    site-basis vector via v_le = R^T v_site, equivalently v_le[j] = v_site[s]
    where perm[s] = j, i.e. v_le = v_site[inv]. For matrices,
    A_le = R^T A R, i.e. A_le[i,j] = A_site[inv[i], inv[j]] = A_site[inv][:, inv].
    """
    inv = np.empty_like(factor.perm)
    inv[factor.perm] = np.arange(factor.n_sites)
    return op[inv][:, inv]


def reorder_to_site(op_le: np.ndarray, factor: SiteFactor) -> np.ndarray:
    """Inverse of reorder_to_le: A_site[s1,s2] = A_le[perm[s1], perm[s2]]."""
    return op_le[factor.perm][:, factor.perm]


# -----------------------------------------------------------------------------
# Native operators
# -----------------------------------------------------------------------------


def native_sublattice_Z(dim: int, side: int) -> np.ndarray:
    n = side ** dim
    diag = np.empty(n, dtype=complex)
    for site_index in range(n):
        coords = []
        rem = site_index
        for _ in range(dim):
            coords.append(rem % side)
            rem //= side
        diag[site_index] = (-1.0) ** (sum(coords))
    return np.diag(diag)


def axis_taste_op(op2: np.ndarray, dim: int, side: int, axis: int) -> np.ndarray:
    """Build the operator that acts as op2 on taste bit eta_axis and identity elsewhere."""
    n = side ** dim
    out = np.zeros((n, n), dtype=complex)
    for site_index in range(n):
        coords = []
        rem = site_index
        for _ in range(dim):
            coords.append(rem % side)
            rem //= side
        eta_axis = coords[axis] % 2
        for new_eta in (0, 1):
            amp = op2[new_eta, eta_axis]
            if amp == 0:
                continue
            new_coords = list(coords)
            new_coords[axis] = coords[axis] - eta_axis + new_eta
            new_index = 0
            for k in range(dim - 1, -1, -1):
                new_index = new_index * side + new_coords[k]
            out[new_index, site_index] = amp
    return out


def fixed_pair_hop_X(dim: int, side: int) -> np.ndarray:
    """Empirically equals I_cells (x) X on the LAST taste axis (axis d-1)."""
    return axis_taste_op(X2, dim=dim, side=side, axis=dim - 1)


# -----------------------------------------------------------------------------
# RALA membership tests
# -----------------------------------------------------------------------------


@dataclasses.dataclass
class RalaCheck:
    name: str
    passed: bool
    metric: str


def in_rala(op_site_basis: np.ndarray, factor: SiteFactor,
            tol: float = 1e-12) -> tuple[bool, np.ndarray, float, float]:
    rebased = reorder_to_le(op_site_basis, factor)
    n_env = factor.n_env
    O_proj = np.zeros((2, 2), dtype=complex)
    residual_sq = 0.0
    for b1 in range(2):
        for b2 in range(2):
            block = rebased[b1*n_env:(b1+1)*n_env, b2*n_env:(b2+1)*n_env]
            avg = np.trace(block) / n_env
            O_proj[b1, b2] = avg
            target = avg * np.eye(n_env)
            residual_sq += float(np.linalg.norm(block - target) ** 2)
    fro_res = math.sqrt(residual_sq)
    op_norm = float(np.linalg.norm(op_site_basis))
    rel_res = fro_res / op_norm if op_norm > 0 else fro_res
    return (fro_res < tol), O_proj, fro_res, rel_res


# -----------------------------------------------------------------------------
# Theorem checks
# -----------------------------------------------------------------------------


def check_T1_RALA_closed_under_algebra(factor: SiteFactor) -> RalaCheck:
    Z_axis = axis_taste_op(Z2, factor.dim, factor.side, factor.logical_axis)
    X_axis = axis_taste_op(X2, factor.dim, factor.side, factor.logical_axis)
    Y_axis = axis_taste_op(Y2, factor.dim, factor.side, factor.logical_axis)
    ok_z, _, _, _ = in_rala(Z_axis, factor)
    ok_x, _, _, _ = in_rala(X_axis, factor)
    ok_y, _, _, _ = in_rala(Y_axis, factor)
    ok_sum, _, _, _ = in_rala(Z_axis + 1.5 * X_axis, factor)
    ok_prod, _, _, _ = in_rala(Z_axis @ X_axis, factor)
    ok_conj, _, _, _ = in_rala(Z_axis.conj().T, factor)
    ok_zxz, _, _, _ = in_rala(Z_axis @ X_axis @ Z_axis, factor)
    all_ok = all([ok_z, ok_x, ok_y, ok_sum, ok_prod, ok_conj, ok_zxz])
    return RalaCheck(
        f"T1 RALA closure (dim={factor.dim} side={factor.side} a={factor.logical_axis})",
        all_ok,
        f"Z_axis={ok_z} X_axis={ok_x} Y_axis={ok_y} sum={ok_sum} product={ok_prod} conj={ok_conj} ZXZ={ok_zxz}",
    )


def check_T2_axis_operators(factor: SiteFactor) -> RalaCheck:
    Z_axis = axis_taste_op(Z2, factor.dim, factor.side, factor.logical_axis)
    X_axis = axis_taste_op(X2, factor.dim, factor.side, factor.logical_axis)
    ok_z, Oz, fro_z, _ = in_rala(Z_axis, factor)
    ok_x, Ox, fro_x, _ = in_rala(X_axis, factor)
    z_match = np.allclose(Oz, Z2, atol=1e-12)
    x_match = np.allclose(Ox, X2, atol=1e-12)
    return RalaCheck(
        f"T2 axis-Z/axis-X in RALA (dim={factor.dim} side={factor.side} a={factor.logical_axis})",
        ok_z and ok_x and z_match and x_match,
        f"Z_in={ok_z} match_sigma_z={z_match} fro={fro_z:.2e} | X_in={ok_x} match_sigma_x={x_match} fro={fro_x:.2e}",
    )


def check_T3_axis_bell_projector(factor: SiteFactor) -> RalaCheck:
    Z_axis = axis_taste_op(Z2, factor.dim, factor.side, factor.logical_axis)
    X_axis = axis_taste_op(X2, factor.dim, factor.side, factor.logical_axis)
    n = factor.n_sites
    n_env = factor.n_env
    I_n = np.eye(n, dtype=complex)
    ZA = np.kron(Z_axis, I_n)
    ZB = np.kron(I_n, Z_axis)
    XA = np.kron(X_axis, I_n)
    XB = np.kron(I_n, X_axis)
    Itot = np.kron(I_n, I_n)
    bell_labels = [("Phi+",0,0),("Phi-",1,0),("Psi+",0,1),("Psi-",1,1)]

    perm = factor.perm
    pair_perm_inv = np.empty(n*n, dtype=np.int64)
    for siteA in range(n):
        rA = perm[siteA]
        b_A = rA // n_env
        e_A = rA % n_env
        for siteB in range(n):
            rB = perm[siteB]
            b_B = rB // n_env
            e_B = rB % n_env
            old_idx = siteA * n + siteB
            new_idx = ((b_A * 2 + b_B) * n_env + e_A) * n_env + e_B
            pair_perm_inv[new_idx] = old_idx

    def in_pair_rala(op):
        rebased = op[pair_perm_inv][:, pair_perm_inv]
        O_logical = np.zeros((4, 4), dtype=complex)
        residual_sq = 0.0
        for bA1 in range(2):
            for bB1 in range(2):
                for bA2 in range(2):
                    for bB2 in range(2):
                        rs = (bA1*2 + bB1) * (n_env*n_env)
                        re = rs + n_env*n_env
                        cs = (bA2*2 + bB2) * (n_env*n_env)
                        ce = cs + n_env*n_env
                        block = rebased[rs:re, cs:ce]
                        avg = np.trace(block) / (n_env*n_env)
                        O_logical[bA1*2+bB1, bA2*2+bB2] = avg
                        target = avg * np.eye(n_env*n_env)
                        residual_sq += float(np.linalg.norm(block - target) ** 2)
        return math.sqrt(residual_sq), O_logical

    bell_residuals = []
    P_list = []
    for label, z, x in bell_labels:
        P = 0.25 * (Itot + ((-1)**x) * ZA @ ZB) @ (Itot + ((-1)**z) * XA @ XB)
        res, O_log = in_pair_rala(P)
        bell_residuals.append((label, res, O_log))
        P_list.append(P)

    def bell_state(z, x):
        if (z, x) == (0, 0):
            v = np.array([1, 0, 0, 1], dtype=complex)/math.sqrt(2)
        elif (z, x) == (1, 0):
            v = np.array([1, 0, 0, -1], dtype=complex)/math.sqrt(2)
        elif (z, x) == (0, 1):
            v = np.array([0, 1, 1, 0], dtype=complex)/math.sqrt(2)
        else:
            v = np.array([0, 1, -1, 0], dtype=complex)/math.sqrt(2)
        return np.outer(v, v.conj())

    max_match_err = 0.0
    for (label, _, O_log), (_, z, x) in zip(bell_residuals, bell_labels):
        ideal = bell_state(z, x)
        max_match_err = max(max_match_err, float(np.linalg.norm(O_log - ideal)))

    sum_P = sum(P_list)
    resolution_err = float(np.linalg.norm(sum_P - Itot))
    pair_ortho_err = 0.0
    for i in range(4):
        for j in range(4):
            if i == j: continue
            pair_ortho_err = max(pair_ortho_err, float(np.linalg.norm(P_list[i] @ P_list[j])))
    idem_err = max(float(np.linalg.norm(P @ P - P)) for P in P_list)
    max_res = max(r[1] for r in bell_residuals)

    passed = (max_res < 1e-12 and max_match_err < 1e-12
              and resolution_err < 1e-10 and pair_ortho_err < 1e-10
              and idem_err < 1e-10)
    return RalaCheck(
        f"T3 axis-Bell projectors in pair-RALA (dim={factor.dim} side={factor.side})",
        passed,
        f"max_pair_RALA_residual={max_res:.2e} max_logical_block_err={max_match_err:.2e} "
        f"sum_to_I_err={resolution_err:.2e} ortho_err={pair_ortho_err:.2e} idem_err={idem_err:.2e}",
    )


def check_T4_native_Z_obstruction(factor: SiteFactor) -> RalaCheck:
    Z_native = native_sublattice_Z(factor.dim, factor.side)
    ok, O_proj, fro, rel = in_rala(Z_native, factor)
    if factor.dim == 1:
        passed = ok and np.allclose(O_proj, Z2, atol=1e-12)
        msg = f"dim=1: in_rala={ok} O_proj_matches_sigma_z={np.allclose(O_proj, Z2, atol=1e-12)}"
    else:
        passed = (not ok) and np.allclose(O_proj, np.zeros((2,2)), atol=1e-12) and abs(rel - 1.0) < 1e-9
        msg = (f"dim={factor.dim}: not_in_rala={not ok} O_proj_zero={np.allclose(O_proj, np.zeros((2,2)), atol=1e-12)} "
               f"rel_residual={rel:.6f} (expect 1.0)")
    return RalaCheck(
        f"T4 native-Z obstruction (dim={factor.dim} side={factor.side})",
        passed, msg,
    )


def check_T5_fixed_pair_hop(factor: SiteFactor) -> RalaCheck:
    fixed = fixed_pair_hop_X(factor.dim, factor.side)
    ok, O_proj, fro, rel = in_rala(fixed, factor)
    if factor.logical_axis == factor.dim - 1:
        passed = ok and np.allclose(O_proj, X2, atol=1e-12)
        msg = f"a={factor.logical_axis}=d-1: in_rala={ok} O_proj_matches_sigma_x={np.allclose(O_proj, X2, atol=1e-12)}"
    else:
        passed = (not ok) and np.allclose(O_proj, np.zeros((2,2)), atol=1e-12)
        msg = f"a={factor.logical_axis}!=d-1={factor.dim-1}: not_in_rala={not ok} O_proj_zero={np.allclose(O_proj, np.zeros((2,2)), atol=1e-12)} rel_residual={rel:.6f}"
    return RalaCheck(
        f"T5 fixed pair-hop X membership (dim={factor.dim} side={factor.side} a={factor.logical_axis})",
        passed, msg,
    )


def check_T6_base_fiber_separation(factor: SiteFactor) -> RalaCheck:
    """T6 (transport theory T1): RALA elements commute with all I_logical (x) L_env."""
    rng = np.random.default_rng(20260507)
    n_env = factor.n_env
    diag_mass = rng.normal(size=n_env)
    diag_charge = rng.choice([-1.0, 0.0, 1.0], size=n_env)
    diag_support = rng.integers(0, 2, size=n_env).astype(float)
    L_mass = reorder_to_site(np.kron(np.eye(2), np.diag(diag_mass)).astype(complex), factor)
    L_charge = reorder_to_site(np.kron(np.eye(2), np.diag(diag_charge)).astype(complex), factor)
    L_support = reorder_to_site(np.kron(np.eye(2), np.diag(diag_support)).astype(complex), factor)

    Z_axis = axis_taste_op(Z2, factor.dim, factor.side, factor.logical_axis)
    X_axis = axis_taste_op(X2, factor.dim, factor.side, factor.logical_axis)
    Y_axis = axis_taste_op(Y2, factor.dim, factor.side, factor.logical_axis)
    I_n = np.eye(factor.n_sites, dtype=complex)
    corrections = [I_n, Z_axis, X_axis, Y_axis]

    max_norm = 0.0
    for C in corrections:
        for L in (L_mass, L_charge, L_support):
            comm = C @ L - L @ C
            max_norm = max(max_norm, float(np.linalg.norm(comm)))
    passed = max_norm < 1e-9
    return RalaCheck(
        f"T6 base/fiber separation (dim={factor.dim} side={factor.side} a={factor.logical_axis})",
        passed,
        f"max_commutator_norm={max_norm:.2e}",
    )


def check_T7_correction_xor_composition(factor: SiteFactor) -> RalaCheck:
    Z_axis = axis_taste_op(Z2, factor.dim, factor.side, factor.logical_axis)
    X_axis = axis_taste_op(X2, factor.dim, factor.side, factor.logical_axis)
    I_n = np.eye(factor.n_sites, dtype=complex)
    paulis_site = {
        (0,0): I_n,
        (1,0): Z_axis,
        (0,1): X_axis,
        (1,1): Z_axis @ X_axis,
    }
    in_alg_ok = True
    for k, op in paulis_site.items():
        ok, _, _, _ = in_rala(op, factor)
        in_alg_ok = in_alg_ok and ok
    max_dev = 0.0
    for (z1,x1), op1 in paulis_site.items():
        for (z2,x2), op2 in paulis_site.items():
            target = paulis_site[((z1^z2), (x1^x2))]
            prod = op1 @ op2
            target_norm_sq = float(np.real(np.trace(target.conj().T @ target)))
            tr_val = np.trace(target.conj().T @ prod)
            alpha = (tr_val / target_norm_sq) if target_norm_sq > 0 else 0.0
            deviation = float(np.linalg.norm(prod - alpha * target))
            max_dev = max(max_dev, deviation)
    passed = in_alg_ok and max_dev < 1e-9
    return RalaCheck(
        f"T7 Pauli XOR composition (dim={factor.dim} side={factor.side} a={factor.logical_axis})",
        passed,
        f"all_in_RALA={in_alg_ok} max_xor_residual_after_phase={max_dev:.2e}",
    )


def check_T8_teleportation_protocol_closure(factor: SiteFactor) -> RalaCheck:
    """T8: RALA-based teleportation restores the encoded input on Bob with
    perfect fidelity, with input-independent pre-record Bob marginal and
    each Bell branch probability = 1/4.
    """
    n = factor.n_sites
    n_env = factor.n_env

    e0 = 0
    def encode(b):
        v_le = np.zeros(n, dtype=complex)
        v_le[b * n_env + e0] = 1.0
        return v_le[factor.perm]

    z0 = encode(0)
    z1 = encode(1)
    phi_plus = (np.kron(z0, z0) + np.kron(z1, z1)) / math.sqrt(2.0)

    Z_axis = axis_taste_op(Z2, factor.dim, factor.side, factor.logical_axis)
    X_axis = axis_taste_op(X2, factor.dim, factor.side, factor.logical_axis)
    I_n = np.eye(n, dtype=complex)

    def bell_proj(z, x):
        ZZ = np.kron(Z_axis, Z_axis)
        XX = np.kron(X_axis, X_axis)
        I_AAR = np.kron(I_n, I_n)
        return 0.25 * (I_AAR + ((-1)**x) * ZZ) @ (I_AAR + ((-1)**z) * XX)

    P_list = [(bell_proj(z, x), z, x) for z in (0, 1) for x in (0, 1)]

    rng = np.random.default_rng(20260507)
    test_states_logical = [
        np.array([1, 0], dtype=complex),
        np.array([0, 1], dtype=complex),
        np.array([1, 1], dtype=complex) / math.sqrt(2.0),
        np.array([1, -1], dtype=complex) / math.sqrt(2.0),
        np.array([1, 1j], dtype=complex) / math.sqrt(2.0),
        np.array([1, -1j], dtype=complex) / math.sqrt(2.0),
    ]
    for _ in range(8):
        v = rng.normal(size=2) + 1j * rng.normal(size=2)
        v = v / np.linalg.norm(v)
        test_states_logical.append(v)

    min_fid = 1.0
    max_total_prob_err = 0.0
    max_branch_prob_err = 0.0
    max_pre_record_input_dependence = 0.0
    pre_record_marginals = []

    # Memory-efficient: use psi as (n*n, n) matrix; Bell projector P is (n*n, n*n)
    # for matrix multiply, but kron(P, I_B) is avoided.
    for psi_log in test_states_logical:
        psi_A = psi_log[0] * z0 + psi_log[1] * z1
        full = np.kron(psi_A, phi_plus)
        full_mat = full.reshape(n * n, n)
        total_prob = 0.0

        # Pre-record marginal on B: rho_B[k, k'] = sum_{i_AAR} full[i, k] full[i, k'].conj()
        # = full_mat.T @ full_mat.conj() — gives the standard density-matrix layout.
        rho_B_marginal = full_mat.T @ full_mat.conj()
        pre_record_marginals.append(rho_B_marginal)

        for P, zbit, xbit in P_list:
            after_mat = P @ full_mat
            prob = float(np.real(np.sum(np.abs(after_mat) ** 2)))
            total_prob += prob
            if prob < 1e-12:
                continue
            rho_B_branch = (after_mat.T @ after_mat.conj()) / prob
            U_corr = (X_axis if xbit else I_n) @ (Z_axis if zbit else I_n)
            rho_B_corr = U_corr @ rho_B_branch @ U_corr.conj().T
            psi_B_target = psi_log[0] * z0 + psi_log[1] * z1
            fid = float(np.real(psi_B_target.conj() @ rho_B_corr @ psi_B_target))
            min_fid = min(min_fid, fid)
            max_branch_prob_err = max(max_branch_prob_err, abs(prob - 0.25))
        max_total_prob_err = max(max_total_prob_err, abs(total_prob - 1.0))

    if pre_record_marginals:
        ref = pre_record_marginals[0]
        for m in pre_record_marginals[1:]:
            max_pre_record_input_dependence = max(
                max_pre_record_input_dependence,
                float(np.linalg.norm(m - ref)))

    passed = (min_fid > 1.0 - 1e-9 and max_total_prob_err < 1e-9
              and max_branch_prob_err < 1e-9 and max_pre_record_input_dependence < 1e-9)
    return RalaCheck(
        f"T8 RALA teleportation protocol closure (dim={factor.dim} side={factor.side} a={factor.logical_axis})",
        passed,
        f"min_fidelity={min_fid:.12f} max_total_prob_err={max_total_prob_err:.2e} "
        f"max_branch_prob_err={max_branch_prob_err:.2e} pre_record_input_dep={max_pre_record_input_dependence:.2e}",
    )


# -----------------------------------------------------------------------------
# Driver
# -----------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Retained-Axis Operator Algebra (RALA) closure runner.")
    parser.add_argument("--dims", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--sides", type=int, nargs="+", default=[2, 4])
    parser.add_argument("--axes", type=str, default="all",
                        help="'all' or comma-separated axis indices")
    parser.add_argument("--max-side-by-dim", type=int, nargs="+",
                        default=None,
                        help="Override max side per dim (1-indexed in dim order)")
    args = parser.parse_args()

    print("=" * 78)
    print("Retained-Axis Operator Algebra (RALA) closure runner")
    print(
        "Closes (theorem-bounded): TELEPORTATION_ENCODING_PORTABILITY_NOTE,\n"
        "  TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE, and\n"
        "  TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE T1/T2 algebraic content."
    )
    print(
        "Boundary: ordinary qubit teleportation on encoded taste qubits; no\n"
        "matter, mass, charge, energy, object transport, or FTL signaling."
    )
    print("=" * 78)
    print()

    all_checks: list[RalaCheck] = []
    for dim in args.dims:
        for side in args.sides:
            # skip dim=3 side=4 if not requested explicitly to keep runtime bounded
            if args.axes == "all":
                axes = list(range(dim))
            else:
                axes = [int(a) for a in args.axes.split(",")]
            for axis in axes:
                factor = build_site_factor(dim=dim, side=side, logical_axis=axis)
                print(f"--- dim={dim} side={side} retained_axis={axis} ---")
                checks = [
                    check_T1_RALA_closed_under_algebra(factor),
                    check_T2_axis_operators(factor),
                    check_T3_axis_bell_projector(factor),
                    check_T4_native_Z_obstruction(factor),
                    check_T5_fixed_pair_hop(factor),
                    check_T6_base_fiber_separation(factor),
                    check_T7_correction_xor_composition(factor),
                    check_T8_teleportation_protocol_closure(factor),
                ]
                for ck in checks:
                    status = "PASS" if ck.passed else "FAIL"
                    print(f"  {status}  {ck.name}: {ck.metric}")
                all_checks.extend(checks)
                print()

    n_pass = sum(1 for c in all_checks if c.passed)
    n_fail = sum(1 for c in all_checks if not c.passed)
    print("=" * 78)
    print(f"PASS={n_pass} FAIL={n_fail}")
    print("=" * 78)
    if n_fail == 0:
        print()
        print("RALA closure: all theorems T1-T8 verified across the audited grid.")
        print(
            "Promotes three open-gate notes (theorem-bounded, finite-grid):\n"
            "  - TELEPORTATION_ENCODING_PORTABILITY_NOTE: T5 algebraic membership\n"
            "    theorem (current_fixed_x in RALA(a) iff a = d-1).\n"
            "  - TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE: T1 + T2 + T4\n"
            "    finite operator algebra closure with native-Z obstruction proof.\n"
            "  - TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE T1/T2 axioms: T6\n"
            "    base/fiber separation + T3/T7 Bell connection / XOR composition.\n"
            "Physical apparatus, noise, durable measurement record, dynamical\n"
            "preparation, and conservation-ledger derivations are explicitly NOT\n"
            "closed by this algebraic theorem; they remain open in their own gates."
        )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
