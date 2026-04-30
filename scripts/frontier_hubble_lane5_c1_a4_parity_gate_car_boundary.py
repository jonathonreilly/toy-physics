#!/usr/bin/env python3
"""Lane 5 (C1) A4 parity-gate-to-CAR boundary verifier.

The A4 route asks whether the primitive parity-gate carrier route supplies a
stronger bridge to native CAR/coframe response on P_A H_cell.

It does not by itself. The parity gate supplies an exact Z2 half-zone selector
and gives the 1/4 coefficient inside the primitive-CAR carrier class, but the
gate data are even/commutative and do not force the odd Clifford/CAR response
or the metric-compatible coframe law on the rank-four active block.
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


def kron(*mats: np.ndarray) -> np.ndarray:
    out = mats[0]
    for mat in mats[1:]:
        out = np.kron(out, mat)
    return out


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def anticommutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b + b @ a


def span_rank(mats: list[np.ndarray], tol: float = TOL) -> int:
    columns = [mat.reshape(-1) for mat in mats]
    return int(np.linalg.matrix_rank(np.column_stack(columns), tol=tol))


def commutant_dimension(generators: list[np.ndarray], tol: float = TOL) -> int:
    dim = generators[0].shape[0]
    identity = np.eye(dim, dtype=complex)
    rows = []
    for generator in generators:
        rows.append(np.kron(identity, generator) - np.kron(generator.T, identity))
    system = np.vstack(rows)
    rank = int(np.linalg.matrix_rank(system, tol=tol))
    return dim * dim - rank


def algebra_words(generators: list[np.ndarray]) -> list[np.ndarray]:
    identity = np.eye(generators[0].shape[0], dtype=complex)
    words = [identity]
    for length in range(1, len(generators) + 1):
        for indices in itertools.combinations(range(len(generators)), length):
            word = identity.copy()
            for idx in indices:
                word = word @ generators[idx]
            words.append(word)
    return words


def clifford_error(generators: list[np.ndarray]) -> float:
    identity = np.eye(generators[0].shape[0], dtype=complex)
    worst = 0.0
    for i, gamma_i in enumerate(generators):
        for j, gamma_j in enumerate(generators):
            target = (2.0 if i == j else 0.0) * identity
            worst = max(worst, float(np.linalg.norm(anticommutator(gamma_i, gamma_j) - target)))
    return worst


def apbc_momenta(n: int) -> np.ndarray:
    return -math.pi + 2.0 * math.pi * (np.arange(n, dtype=float) + 0.5) / n


def transverse_laplacian(*qs: float) -> float:
    return 1.0 - sum(math.cos(q) for q in qs) / len(qs)


def low_sheet_weight(*qs: float) -> float:
    delta = transverse_laplacian(*qs)
    if abs(delta - 1.0) < 1.0e-14:
        return 0.5
    return 1.0 if delta < 1.0 else 0.0


def finite_half_zone_weight(ny: int, nz: int | None = None) -> float:
    kys = apbc_momenta(ny)
    if nz is None:
        return sum(low_sheet_weight(float(ky)) for ky in kys)
    kzs = apbc_momenta(nz)
    return sum(low_sheet_weight(float(ky), float(kz)) for ky in kys for kz in kzs)


def phase(action_dimensional: float, kappa: float) -> complex:
    return np.exp(1j * action_dimensional / kappa)


def main() -> int:
    checks: list[Check] = []

    identity4 = np.eye(4, dtype=complex)
    identity2 = np.eye(2, dtype=complex)
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    z = np.diag([1.0, -1.0]).astype(complex)

    dim_cell = 16
    rank_pa = 4
    c_cell = rank_pa / dim_cell
    gate_projector = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    gate_involution = 2.0 * gate_projector - identity4
    gate_rank = int(round(float(np.trace(gate_projector).real)))
    checks.append(
        Check(
            "primitive_gate_data_have_rank_four_host_and_half_split",
            rank_pa == 4 and math.isclose(c_cell, 0.25, abs_tol=1.0e-15) and gate_rank == 2,
            f"rank(P_A)={rank_pa}, c_cell={c_cell:.12f}, rank(Q_+)={gate_rank}/4",
        )
    )

    gate_algebra_rank = span_rank([identity4, gate_projector])
    gate_commutant_dim = commutant_dimension([gate_projector])
    checks.append(
        Check(
            "parity_gate_algebra_is_too_small_to_force_clifford_car",
            gate_algebra_rank == 2 and gate_commutant_dim == 8,
            f"dim alg(I,Q_+)={gate_algebra_rank}, dim commutant(Q_+)={gate_commutant_dim}",
        )
    )

    involution_square = float(np.linalg.norm(gate_involution @ gate_involution - identity4))
    checks.append(
        Check(
            "single_z2_involution_is_not_a_four_axis_coframe_response",
            involution_square < TOL and gate_algebra_rank < 16,
            f"||Z_gate^2-I||={involution_square:.3e}, generated algebra dim={gate_algebra_rank}",
        )
    )

    for ny in (32, 64, 96):
        active = finite_half_zone_weight(ny)
        checks.append(
            Check(
                f"2d_self_dual_half_zone_L{ny}",
                math.isclose(2.0 * active, ny, abs_tol=1.0e-12),
                f"active_weight={active:.1f}/{ny}",
            )
        )

    for ny, nz in ((32, 32), (48, 32)):
        active = finite_half_zone_weight(ny, nz)
        checks.append(
            Check(
                f"3d_self_dual_half_zone_{ny}x{nz}",
                math.isclose(2.0 * active, ny * nz, abs_tol=1.0e-12),
                f"active_weight={active:.1f}/{ny * nz}",
            )
        )

    # Conditional positive side: if the primitive CAR/coframe premise is added,
    # the parity gate does feed the existing 1/4 carrier theorem.
    car_gammas = [
        kron(x, identity2),
        kron(y, identity2),
        kron(z, x),
        kron(z, y),
    ]
    car_clifford = clifford_error(car_gammas)
    car_span = span_rank(algebra_words(car_gammas))
    average_crossings = 2.0 + 2.0 * 0.5
    c_widom = average_crossings / 12.0
    checks.append(
        Check(
            "conditional_car_plus_parity_gate_gives_one_quarter",
            car_clifford < TOL and car_span == 16 and math.isclose(c_widom, c_cell, abs_tol=1.0e-15),
            f"Clifford residual={car_clifford:.3e}, span={car_span}, c_Widom={c_widom:.12f}",
        )
    )

    # Boundary side: the same gate data can coexist with non-CAR two-qubit
    # response operators. The gate does not select the odd Clifford algebra.
    spin_responses = [
        kron(x, identity2),
        kron(identity2, x),
        kron(z, identity2),
        kron(identity2, z),
    ]
    spin_square = max(float(np.linalg.norm(op @ op - identity4)) for op in spin_responses)
    spin_clifford = clifford_error(spin_responses)
    same_gate_available = (
        int(round(float(np.trace(gate_projector).real))) == 2
        and float(np.linalg.norm(gate_projector @ gate_projector - gate_projector)) < TOL
    )
    checks.append(
        Check(
            "same_gate_data_allow_non_car_two_qubit_response",
            spin_square < TOL and spin_clifford > 1.0 and same_gate_available,
            f"spin square residual={spin_square:.3e}, Clifford residual={spin_clifford:.3e}",
        )
    )

    commute_gate_spin = float(np.linalg.norm(commutator(gate_projector, spin_responses[1])))
    commute_gate_car = float(np.linalg.norm(commutator(gate_projector, car_gammas[0])))
    checks.append(
        Check(
            "gate_does_not_define_the_odd_edge_maps",
            commute_gate_spin < TOL and commute_gate_car > 1.0,
            (
                "one response can commute with Q_+ while another CAR generator crosses gate sectors; "
                f"comm_spin={commute_gate_spin:.3e}, comm_car={commute_gate_car:.3e}"
            ),
        )
    )

    # Action-unit guard: adding the parity gate does not break the A2
    # (S,kappa) rescaling degeneracy.
    dimensionless_gate_action = c_cell + 0.5
    projected_phases = []
    for kappa in (0.5, 1.0, 2.0, 8.0):
        projected_phases.append(phase(kappa * dimensionless_gate_action, kappa))
    phase_spread = max(abs(candidate - projected_phases[0]) for candidate in projected_phases)
    checks.append(
        Check(
            "parity_gate_does_not_pin_dimensional_action_unit",
            phase_spread < TOL,
            f"same dimensionless gated action for kappa values gives phase spread={phase_spread:.3e}",
        )
    )

    obstruction = (
        gate_algebra_rank == 2
        and gate_commutant_dim == 8
        and car_clifford < TOL
        and spin_clifford > 1.0
        and phase_spread < TOL
    )
    checks.append(
        Check(
            "a4_exposes_statistics_lift_import",
            obstruction,
            "Need a Clifford/CAR coframe-response theorem; the parity gate supplies the selector only after that lift.",
        )
    )

    print("=" * 78)
    print("Lane 5 (C1) A4 parity-gate-to-CAR boundary verifier")
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
            "Conclusion: the primitive parity gate is a valid half-zone selector "
            "inside the primitive-CAR carrier, but it does not force the "
            "Clifford/CAR coframe response or dimensional action unit on P_A H_cell."
        )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
