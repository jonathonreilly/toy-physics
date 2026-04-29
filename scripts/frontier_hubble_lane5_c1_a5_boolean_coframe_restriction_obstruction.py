#!/usr/bin/env python3
"""Lane 5 (C1) A5 Boolean-coframe restriction obstruction verifier.

The direct P_A module-morphism route asks whether the Hamming-weight-one
primitive block P_A H_cell inherits the metric-compatible Clifford/CAR
coframe response from natural full-cell Boolean/Jordan-Wigner coframe
operators on H_cell = (C^2)^4.

It does not. The natural odd coframe generators change Hamming weight, so the
weight-one block is not a reducing submodule. Their compression to P_A H_cell
is zero, not a Cl_4 response. A positive route must construct the active-block
coframe response intrinsically, through a quotient/bilinear theorem, or as an
explicit carrier premise.
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
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


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def span_rank(mats: list[np.ndarray], tol: float = TOL) -> int:
    columns = [mat.reshape(-1) for mat in mats]
    return int(np.linalg.matrix_rank(np.column_stack(columns), tol=tol))


def hamming_weight(index: int) -> int:
    return int(index.bit_count())


def hamming_projection(weight: int, n_axes: int) -> np.ndarray:
    dim = 2**n_axes
    projection = np.zeros((dim, dim), dtype=complex)
    for idx in range(dim):
        if hamming_weight(idx) == weight:
            projection[idx, idx] = 1.0
    return projection


def pauli_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    identity = np.eye(2, dtype=complex)
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    z = np.diag([1.0, -1.0]).astype(complex)
    return identity, x, y, z


def jordan_wigner_gamma(n_axes: int, axis: int) -> np.ndarray:
    identity, x, _y, z = pauli_data()
    factors: list[np.ndarray] = []
    for idx in range(n_axes):
        if idx < axis:
            factors.append(z)
        elif idx == axis:
            factors.append(x)
        else:
            factors.append(identity)
    return kron_all(factors)


def clifford_error(generators: list[np.ndarray], identity: np.ndarray) -> float:
    worst = 0.0
    for i, gamma_i in enumerate(generators):
        for j, gamma_j in enumerate(generators):
            target = (2.0 if i == j else 0.0) * identity
            worst = max(worst, float(np.linalg.norm(anticommutator(gamma_i, gamma_j) - target)))
    return worst


def internal_active_block_gammas() -> list[np.ndarray]:
    identity, x, y, z = pauli_data()
    return [
        np.kron(x, identity),
        np.kron(y, identity),
        np.kron(z, x),
        np.kron(z, y),
    ]


def matrix_product(mats: list[np.ndarray]) -> np.ndarray:
    out = mats[0]
    for mat in mats[1:]:
        out = out @ mat
    return out


def main() -> int:
    checks: list[Check] = []

    n_axes = 4
    dim_cell = 2**n_axes
    identity16 = np.eye(dim_cell, dtype=complex)
    p_a = hamming_projection(1, n_axes)
    p_a_rank = int(round(float(np.trace(p_a).real)))
    c_cell = p_a_rank / dim_cell
    checks.append(
        Check(
            "hamming_weight_one_block_is_the_primitive_P_A_carrier",
            p_a_rank == 4 and math.isclose(c_cell, 0.25, abs_tol=1.0e-15),
            f"rank(P_A)={p_a_rank}, dim(H_cell)={dim_cell}, c_cell={c_cell:.12f}",
        )
    )

    gammas = [jordan_wigner_gamma(n_axes, axis) for axis in range(n_axes)]
    full_clifford = clifford_error(gammas, identity16)
    checks.append(
        Check(
            "natural_full_cell_jordan_wigner_coframe_is_clifford",
            full_clifford < TOL,
            f"full-cell Cl_4 residual={full_clifford:.3e}",
        )
    )

    commutator_residual = max(float(np.linalg.norm(commutator(p_a, gamma))) for gamma in gammas)
    compressed = [p_a @ gamma @ p_a for gamma in gammas]
    compression_norm = max(float(np.linalg.norm(op)) for op in compressed)
    checks.append(
        Check(
            "P_A_is_not_reducing_for_natural_odd_coframe_generators",
            commutator_residual > 1.0 and compression_norm < TOL,
            f"max ||[P_A,Gamma_i]||={commutator_residual:.3e}, max ||P_A Gamma_i P_A||={compression_norm:.3e}",
        )
    )

    compressed_metric_error = max(float(np.linalg.norm(op @ op - p_a)) for op in compressed)
    checks.append(
        Check(
            "compressed_odd_coframe_response_fails_metric_compatibility",
            compressed_metric_error > 1.0,
            f"max ||(P_A Gamma_i P_A)^2-P_A||={compressed_metric_error:.3e}",
        )
    )

    p_a_basis_indices = [idx for idx in range(dim_cell) if hamming_weight(idx) == 1]
    leakage_counts: list[int] = []
    for axis, gamma in enumerate(gammas):
        leaked = 0
        for idx in p_a_basis_indices:
            image = gamma[:, idx]
            support = [row for row, value in enumerate(image) if abs(value) > TOL]
            if not support or any(hamming_weight(row) != 1 for row in support):
                leaked += 1
        leakage_counts.append(leaked)
    checks.append(
        Check(
            "natural_odd_generators_shift_weight_one_outside_P_A",
            leakage_counts == [4, 4, 4, 4],
            f"leaking basis states by axis={leakage_counts}",
        )
    )

    _identity2, _x, _y, z = pauli_data()
    full_occupation_parity = kron_all([z, z, z, z])
    restricted_parity = p_a @ full_occupation_parity @ p_a
    parity_error = float(np.linalg.norm(restricted_parity + p_a))
    checks.append(
        Check(
            "full_cell_occupation_parity_restricts_to_scalar_on_P_A",
            parity_error < TOL,
            f"||P_A parity P_A + P_A||={parity_error:.3e}",
        )
    )

    compressed_span = span_rank([p_a] + compressed)
    checks.append(
        Check(
            "compressed_direct_restriction_has_no_active_clifford_content",
            compressed_span == 1,
            f"span rank of P_A and compressed odd generators={compressed_span}",
        )
    )

    # The obstruction is not that C^4 cannot carry Cl_4. It can. The issue is
    # that the active-block response is not obtained by naive restriction of
    # the full-cell odd Boolean coframe maps.
    identity4 = np.eye(4, dtype=complex)
    internal = internal_active_block_gammas()
    internal_clifford = clifford_error(internal, identity4)
    internal_span = span_rank(
        [
            np.linalg.matrix_power(np.eye(4, dtype=complex), 1)
        ]
        + [
            matrix_product([internal[idx] for idx in indices])
            for length in range(1, len(internal) + 1)
            for indices in itertools.combinations(range(len(internal)), length)
        ]
    )
    checks.append(
        Check(
            "intrinsic_active_block_clifford_response_exists_but_is_extra",
            internal_clifford < TOL and internal_span == 16,
            f"internal Cl_4 residual={internal_clifford:.3e}, internal span={internal_span}",
        )
    )

    obstruction = (
        full_clifford < TOL
        and commutator_residual > 1.0
        and compression_norm < TOL
        and compressed_span == 1
        and internal_clifford < TOL
    )
    checks.append(
        Check(
            "a5_exposes_active_block_response_import",
            obstruction,
            "Need an intrinsic active-block coframe law, quotient/bilinear theorem, or explicit carrier premise.",
        )
    )

    print("=" * 78)
    print("Lane 5 (C1) A5 Boolean-coframe restriction obstruction verifier")
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
            "Conclusion: P_A H_cell does not inherit the natural full-cell odd "
            "Boolean/Jordan-Wigner coframe response by restriction. The active "
            "Cl_4/CAR response must be derived intrinsically or kept conditional."
        )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
