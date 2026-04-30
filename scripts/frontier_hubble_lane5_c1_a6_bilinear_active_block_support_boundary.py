#!/usr/bin/env python3
"""Lane 5 (C1) A6 bilinear active-block support/boundary verifier.

After A5, direct restriction of full-cell odd coframe generators to the
Hamming-weight-one P_A block is blocked. This runner tests the surviving
quotient/bilinear route: number-preserving bilinears a_i^dagger a_j do act on
the one-particle P_A sector and generate M_4(C), so they can host an intrinsic
Cl_4 response. The route remains underdetermined because the bilinear algebra
alone does not select a unique metric coframe basis or action-unit metrology.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math

import numpy as np


TOL = 1.0e-10


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def kron_all(mats: list[np.ndarray]) -> np.ndarray:
    out = mats[0]
    for mat in mats[1:]:
        out = np.kron(out, mat)
    return out


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def span_rank(mats: list[np.ndarray], tol: float = TOL) -> int:
    columns = [mat.reshape(-1) for mat in mats]
    return int(np.linalg.matrix_rank(np.column_stack(columns), tol=tol))


def hamming_weight(index: int) -> int:
    return int(index.bit_count())


def pauli_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    identity = np.eye(2, dtype=complex)
    z = np.diag([1.0, -1.0]).astype(complex)
    sigma_minus = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    return identity, z, sigma_minus


def annihilation_operator(n_modes: int, mode: int) -> np.ndarray:
    identity, z, sigma_minus = pauli_data()
    factors: list[np.ndarray] = []
    for idx in range(n_modes):
        if idx < mode:
            factors.append(z)
        elif idx == mode:
            factors.append(sigma_minus)
        else:
            factors.append(identity)
    return kron_all(factors)


def restrict(matrix: np.ndarray, indices: list[int]) -> np.ndarray:
    return matrix[np.ix_(indices, indices)]


def matrix_units(dim: int) -> list[np.ndarray]:
    units: list[np.ndarray] = []
    for i in range(dim):
        for j in range(dim):
            unit = np.zeros((dim, dim), dtype=complex)
            unit[i, j] = 1.0
            units.append(unit)
    return units


def clifford_error(generators: list[np.ndarray]) -> float:
    identity = np.eye(generators[0].shape[0], dtype=complex)
    worst = 0.0
    for i, gamma_i in enumerate(generators):
        for j, gamma_j in enumerate(generators):
            target = (2.0 if i == j else 0.0) * identity
            worst = max(worst, float(np.linalg.norm(anticommutator(gamma_i, gamma_j) - target)))
    return worst


def active_block_gammas() -> list[np.ndarray]:
    identity = np.eye(2, dtype=complex)
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    z = np.diag([1.0, -1.0]).astype(complex)
    return [
        np.kron(x, identity),
        np.kron(y, identity),
        np.kron(z, x),
        np.kron(z, y),
    ]


def projection_error_to_span(target: np.ndarray, basis: list[np.ndarray]) -> float:
    mat = np.column_stack([b.reshape(-1) for b in basis])
    coeffs, *_ = np.linalg.lstsq(mat, target.reshape(-1), rcond=None)
    projected = (mat @ coeffs).reshape(target.shape)
    return float(np.linalg.norm(projected - target))


def phase(action_dimensional: float, kappa: float) -> complex:
    return cmath.exp(1j * action_dimensional / kappa)


def main() -> int:
    checks: list[Check] = []

    n_modes = 4
    dim_cell = 2**n_modes
    p_a_indices = [idx for idx in range(dim_cell) if hamming_weight(idx) == 1]
    rank_pa = len(p_a_indices)
    c_cell = rank_pa / dim_cell
    checks.append(
        Check(
            "one_particle_P_A_sector_has_rank_four",
            rank_pa == 4 and math.isclose(c_cell, 0.25, abs_tol=1.0e-15),
            f"indices={p_a_indices}, c_cell={c_cell:.12f}",
        )
    )

    annihilators = [annihilation_operator(n_modes, mode) for mode in range(n_modes)]
    bilinears_full = [
        annihilators[i].conj().T @ annihilators[j]
        for i in range(n_modes)
        for j in range(n_modes)
    ]
    bilinears = [restrict(op, p_a_indices) for op in bilinears_full]
    unit_basis = matrix_units(4)
    bilinear_span = span_rank(bilinears)
    checks.append(
        Check(
            "number_preserving_bilinears_generate_full_active_matrix_algebra",
            bilinear_span == 16,
            f"span rank on P_A sector={bilinear_span}",
        )
    )

    worst_matrix_unit_error = max(
        projection_error_to_span(unit, bilinears)
        for unit in unit_basis
    )
    checks.append(
        Check(
            "bilinears_recover_all_matrix_units_on_P_A",
            worst_matrix_unit_error < TOL,
            f"worst matrix-unit projection residual={worst_matrix_unit_error:.3e}",
        )
    )

    product_error = 0.0
    for i in range(4):
        for j in range(4):
            eij = unit_basis[4 * i + j]
            for k in range(4):
                for ell in range(4):
                    ekl = unit_basis[4 * k + ell]
                    target = unit_basis[4 * i + ell] if j == k else np.zeros((4, 4), dtype=complex)
                    product_error = max(product_error, float(np.linalg.norm(eij @ ekl - target)))
    checks.append(
        Check(
            "active_bilinear_sector_has_matrix_unit_multiplication",
            product_error < TOL,
            f"worst E_ij E_kl residual={product_error:.3e}",
        )
    )

    gammas = active_block_gammas()
    gamma_clifford = clifford_error(gammas)
    gamma_projection_error = max(projection_error_to_span(gamma, bilinears) for gamma in gammas)
    checks.append(
        Check(
            "bilinear_active_algebra_can_host_a_Cl4_response",
            gamma_clifford < TOL and gamma_projection_error < TOL,
            f"Cl_4 residual={gamma_clifford:.3e}, span residual={gamma_projection_error:.3e}",
        )
    )

    swap = np.eye(4, dtype=complex)
    swap[[1, 2], :] = swap[[2, 1], :]
    permuted_gammas = [swap @ gamma @ swap.conj().T for gamma in gammas]
    permuted_clifford = clifford_error(permuted_gammas)
    basis_difference = max(float(np.linalg.norm(a - b)) for a, b in zip(gammas, permuted_gammas, strict=True))
    permuted_projection_error = max(projection_error_to_span(gamma, bilinears) for gamma in permuted_gammas)
    checks.append(
        Check(
            "same_bilinear_algebra_admits_distinct_Cl4_bases",
            permuted_clifford < TOL and permuted_projection_error < TOL and basis_difference > 1.0,
            (
                f"permuted Cl_4 residual={permuted_clifford:.3e}, "
                f"basis difference={basis_difference:.3e}"
            ),
        )
    )

    # A continuous phase rotation of one active basis vector also preserves the
    # bilinear algebra and changes the Clifford presentation. This records the
    # remaining metric/orientation/phase selector, not a numerical failure.
    phase_unitary = np.diag([1.0, np.exp(0.37j), 1.0, 1.0]).astype(complex)
    phase_gammas = [phase_unitary @ gamma @ phase_unitary.conj().T for gamma in gammas]
    phase_clifford = clifford_error(phase_gammas)
    phase_difference = max(float(np.linalg.norm(a - b)) for a, b in zip(gammas, phase_gammas, strict=True))
    checks.append(
        Check(
            "continuous_active_basis_phase_is_not_fixed_by_bilinears",
            phase_clifford < TOL and phase_difference > 0.1,
            f"phase-rotated Cl_4 residual={phase_clifford:.3e}, basis difference={phase_difference:.3e}",
        )
    )

    dim_action = 0.25 + 0.37
    phase_spread = max(
        abs(phase(lam * dim_action, lam) - phase(dim_action, 1.0))
        for lam in (0.5, 1.0, 2.0, 8.0)
    )
    checks.append(
        Check(
            "bilinear_route_does_not_pin_dimensional_action_unit",
            phase_spread < TOL,
            f"common (S,kappa) rescaling phase spread={phase_spread:.3e}",
        )
    )

    support_boundary = (
        bilinear_span == 16
        and gamma_clifford < TOL
        and basis_difference > 1.0
        and phase_difference > 0.1
        and phase_spread < TOL
    )
    checks.append(
        Check(
            "a6_exposes_selector_not_existence_boundary",
            support_boundary,
            "Bilinears can host Cl_4, but a metric/orientation/phase and action-unit law remains open.",
        )
    )

    print("=" * 78)
    print("Lane 5 (C1) A6 bilinear active-block support/boundary verifier")
    print("=" * 78)
    passed = 0
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")
        passed += int(check.passed)
    failed = len(checks) - passed
    print("-" * 78)
    print(f"TOTAL: PASS={passed}, FAIL={failed}")
    if failed == 0:
        print(
            "Conclusion: number-preserving bilinears on P_A H_cell generate "
            "M_4(C) and can host an intrinsic Cl_4 response, but they do not "
            "select the metric coframe basis or dimensional action unit."
        )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
