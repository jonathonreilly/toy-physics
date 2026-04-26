#!/usr/bin/env python3
"""Taste-qubit encoding portability audit for the teleportation lane.

This runner checks how far the fixed-cell encoding from
frontier_teleportation_protocol.py generalizes.  The audited Hilbert surface is
the same Kogut-Susskind cell/taste decomposition used by the CHSH runner:

    C^(side^dim) = C^(side/2)^dim cells tensor C^(2^dim) tastes

Only even side lengths in dimensions 1, 2, and 3 are surveyed by default.  The
script tests every available cell, every spectator taste assignment, and every
logical taste axis on those geometries.

Two operator sets are compared:

1. current_fixed_x:
   Z = sublattice parity = I_cells tensor xi_5
   X = row-major pair-hop = I_cells tensor sigma_x on the last taste axis

2. axis_adapted_x:
   Z = sublattice parity
   X = I_cells tensor sigma_x on the selected logical taste axis

The second set is a control showing the algebraic taste-operator portability
when the X operator is retargeted.  It is not a claim that the existing fixed
pair-hop gate already implements all logical axes.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import itertools
import math
import sys
from typing import Iterable

import numpy as np


I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)

OUTCOME_ORDER = ((0, 0), (1, 0), (0, 1), (1, 1))


@dataclasses.dataclass(frozen=True)
class Geometry:
    dim: int
    side: int

    @property
    def n_sites(self) -> int:
        return self.side**self.dim

    @property
    def n_cells(self) -> int:
        return (self.side // 2) ** self.dim


@dataclasses.dataclass(frozen=True)
class BellProjectorMetrics:
    resolution_error: float
    idempotence_error: float
    orthogonality_error: float


@dataclasses.dataclass(frozen=True)
class TeleportationMetrics:
    n_trials: int
    min_fidelity: float
    max_infidelity: float
    max_branch_probability_error: float
    max_total_probability_error: float
    max_pre_measurement_trace_distance: float
    max_post_measurement_trace_distance: float
    max_pairwise_pre_message_distance: float
    outcomes_seen: tuple[tuple[int, int], ...]


@dataclasses.dataclass(frozen=True)
class OperatorSetMetrics:
    z_signed_pauli: bool
    z_sign: int | None
    x_signed_pauli: bool
    x_sign: int | None
    z_leakage: float
    x_leakage: float
    z_square_error: float
    x_square_error: float
    anticommutator_norm: float
    projector_metrics: BellProjectorMetrics
    logical_pauli_pass: bool
    projector_pass: bool
    teleportation: TeleportationMetrics | None
    teleportation_pass: bool | None
    x_restriction_zero: bool


@dataclasses.dataclass
class GateSummary:
    label: str
    total_cases: int = 0
    logical_pauli_pass: int = 0
    projector_pass: int = 0
    teleportation_run: int = 0
    teleportation_pass: int = 0
    z_sign_counts: collections.Counter[int] = dataclasses.field(
        default_factory=collections.Counter
    )
    x_sign_counts: collections.Counter[int] = dataclasses.field(
        default_factory=collections.Counter
    )
    failure_causes: collections.Counter[str] = dataclasses.field(
        default_factory=collections.Counter
    )
    by_dim_axis: dict[tuple[int, int], list[int]] = dataclasses.field(
        default_factory=dict
    )
    max_z_leakage: float = 0.0
    max_x_leakage: float = 0.0
    max_failed_x_leakage: float = 0.0
    zero_x_restriction_failures: int = 0
    max_z_square_error: float = 0.0
    max_x_square_error: float = 0.0
    max_anticommutator_norm: float = 0.0
    max_projector_resolution_error: float = 0.0
    max_projector_idempotence_error: float = 0.0
    max_projector_orthogonality_error: float = 0.0
    min_fidelity: float = 1.0
    max_infidelity: float = 0.0
    max_branch_probability_error: float = 0.0
    max_total_probability_error: float = 0.0
    max_pre_measurement_trace_distance: float = 0.0
    max_post_measurement_trace_distance: float = 0.0
    max_pairwise_pre_message_distance: float = 0.0
    outcomes_seen: set[tuple[int, int]] = dataclasses.field(default_factory=set)

    def update(
        self,
        geometry: Geometry,
        logical_axis: int,
        metrics: OperatorSetMetrics,
        failure_cause: str | None,
    ) -> None:
        self.total_cases += 1
        key = (geometry.dim, logical_axis)
        if key not in self.by_dim_axis:
            self.by_dim_axis[key] = [0, 0]
        self.by_dim_axis[key][0] += 1

        if metrics.logical_pauli_pass:
            self.logical_pauli_pass += 1
            self.by_dim_axis[key][1] += 1
        if metrics.projector_pass:
            self.projector_pass += 1
        if metrics.z_sign is not None:
            self.z_sign_counts[metrics.z_sign] += 1
        if metrics.x_sign is not None:
            self.x_sign_counts[metrics.x_sign] += 1
        if failure_cause is not None:
            self.failure_causes[failure_cause] += 1
        if metrics.x_restriction_zero and not metrics.logical_pauli_pass:
            self.zero_x_restriction_failures += 1

        self.max_z_leakage = max(self.max_z_leakage, metrics.z_leakage)
        self.max_x_leakage = max(self.max_x_leakage, metrics.x_leakage)
        if not metrics.logical_pauli_pass:
            self.max_failed_x_leakage = max(
                self.max_failed_x_leakage, metrics.x_leakage
            )
        self.max_z_square_error = max(self.max_z_square_error, metrics.z_square_error)
        self.max_x_square_error = max(self.max_x_square_error, metrics.x_square_error)
        self.max_anticommutator_norm = max(
            self.max_anticommutator_norm, metrics.anticommutator_norm
        )
        self.max_projector_resolution_error = max(
            self.max_projector_resolution_error,
            metrics.projector_metrics.resolution_error,
        )
        self.max_projector_idempotence_error = max(
            self.max_projector_idempotence_error,
            metrics.projector_metrics.idempotence_error,
        )
        self.max_projector_orthogonality_error = max(
            self.max_projector_orthogonality_error,
            metrics.projector_metrics.orthogonality_error,
        )

        if metrics.teleportation is None:
            return

        self.teleportation_run += 1
        if metrics.teleportation_pass:
            self.teleportation_pass += 1
        tele = metrics.teleportation
        self.min_fidelity = min(self.min_fidelity, tele.min_fidelity)
        self.max_infidelity = max(self.max_infidelity, tele.max_infidelity)
        self.max_branch_probability_error = max(
            self.max_branch_probability_error, tele.max_branch_probability_error
        )
        self.max_total_probability_error = max(
            self.max_total_probability_error, tele.max_total_probability_error
        )
        self.max_pre_measurement_trace_distance = max(
            self.max_pre_measurement_trace_distance,
            tele.max_pre_measurement_trace_distance,
        )
        self.max_post_measurement_trace_distance = max(
            self.max_post_measurement_trace_distance,
            tele.max_post_measurement_trace_distance,
        )
        self.max_pairwise_pre_message_distance = max(
            self.max_pairwise_pre_message_distance,
            tele.max_pairwise_pre_message_distance,
        )
        self.outcomes_seen.update(tele.outcomes_seen)


def parse_csv_ints(raw: str) -> tuple[int, ...]:
    values = tuple(int(part.strip()) for part in raw.split(",") if part.strip())
    if not values:
        raise ValueError("expected at least one integer")
    return values


def coordinate_index(coords: tuple[int, ...], side: int) -> int:
    index = 0
    for coord in coords:
        index = index * side + coord
    return index


def build_cell_taste_operator(
    dim: int, side: int, taste_paulis: Iterable[np.ndarray]
) -> np.ndarray:
    """Build I_cells tensor taste_operator in the site basis."""
    taste_paulis = list(taste_paulis)
    if side % 2 != 0:
        raise ValueError("KS taste decomposition requires even side length")
    if len(taste_paulis) != dim:
        raise ValueError("Need one Pauli factor per taste axis")

    n_sites = side**dim
    op = np.zeros((n_sites, n_sites), dtype=complex)
    coords_list = list(itertools.product(range(side), repeat=dim))

    for i, coords_i in enumerate(coords_list):
        cell_i = tuple(coord // 2 for coord in coords_i)
        eta_i = tuple(coord % 2 for coord in coords_i)
        for j, coords_j in enumerate(coords_list):
            cell_j = tuple(coord // 2 for coord in coords_j)
            if cell_i != cell_j:
                continue
            eta_j = tuple(coord % 2 for coord in coords_j)
            element = 1.0 + 0.0j
            for axis in range(dim):
                element *= taste_paulis[axis][eta_i[axis], eta_j[axis]]
            op[i, j] = element
    return op


def build_sublattice_z(dim: int, side: int) -> np.ndarray:
    coords_list = list(itertools.product(range(side), repeat=dim))
    parity = [(-1) ** sum(coords) for coords in coords_list]
    return np.diag([float(value) for value in parity]).astype(complex)


def build_pair_hop_x(dim: int, side: int) -> np.ndarray:
    n_sites = side**dim
    if n_sites % 2 != 0:
        raise ValueError("pair-hop X requires an even number of sites")
    op = np.zeros((n_sites, n_sites), dtype=complex)
    for pair in range(n_sites // 2):
        i, j = 2 * pair, 2 * pair + 1
        op[i, j] = 1.0
        op[j, i] = 1.0
    return op


def encoded_indices(
    dim: int,
    side: int,
    cell: tuple[int, ...],
    logical_axis: int,
    spectators: tuple[int, ...],
) -> tuple[int, int]:
    spectator_axes = tuple(axis for axis in range(dim) if axis != logical_axis)
    if len(spectators) != len(spectator_axes):
        raise ValueError("wrong number of spectator taste bits")

    spectator_by_axis = dict(zip(spectator_axes, spectators))
    indices: list[int] = []
    for logical_bit in (0, 1):
        eta = [0] * dim
        eta[logical_axis] = logical_bit
        for axis in spectator_axes:
            eta[axis] = spectator_by_axis[axis]
        coords = tuple(2 * cell[axis] + eta[axis] for axis in range(dim))
        indices.append(coordinate_index(coords, side))
    return indices[0], indices[1]


def restrict_to_encoded_qubit(op: np.ndarray, indices: tuple[int, int]) -> np.ndarray:
    return op[np.ix_(indices, indices)]


def leakage_norm(op: np.ndarray, indices: tuple[int, int]) -> float:
    columns = op[:, list(indices)].copy()
    columns[list(indices), :] = 0.0
    return float(np.linalg.norm(columns))


def max_abs(op: np.ndarray) -> float:
    return float(np.max(np.abs(op)))


def signed_pauli_match(
    restricted: np.ndarray, target: np.ndarray, tolerance: float
) -> tuple[bool, int | None]:
    if np.allclose(restricted, target, atol=tolerance):
        return True, 1
    if np.allclose(restricted, -target, atol=tolerance):
        return True, -1
    return False, None


def bell_projector(z_op: np.ndarray, x_op: np.ndarray, z_bit: int, x_bit: int) -> np.ndarray:
    zz = np.kron(z_op, z_op)
    xx = np.kron(x_op, x_op)
    identity = np.eye(4, dtype=complex)
    return 0.25 * (identity + ((-1) ** x_bit) * zz) @ (
        identity + ((-1) ** z_bit) * xx
    )


def bell_projector_metrics(z_op: np.ndarray, x_op: np.ndarray) -> BellProjectorMetrics:
    identity = np.eye(4, dtype=complex)
    projectors = [bell_projector(z_op, x_op, z, x) for z, x in OUTCOME_ORDER]
    resolution_error = max_abs(sum(projectors) - identity)
    idempotence_error = max(max_abs(projector @ projector - projector) for projector in projectors)

    orthogonality_error = 0.0
    for i, first in enumerate(projectors):
        for j, second in enumerate(projectors):
            if i == j:
                continue
            orthogonality_error = max(orthogonality_error, max_abs(first @ second))

    return BellProjectorMetrics(
        resolution_error=resolution_error,
        idempotence_error=idempotence_error,
        orthogonality_error=orthogonality_error,
    )


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    state = rng.standard_normal(2) + 1j * rng.standard_normal(2)
    return normalize(state)


def bell_state_phi_plus() -> np.ndarray:
    state = np.zeros(4, dtype=complex)
    state[0] = 1.0 / math.sqrt(2.0)
    state[3] = 1.0 / math.sqrt(2.0)
    return state


def prepare_three_register_state(input_state: np.ndarray) -> np.ndarray:
    return np.kron(input_state, bell_state_phi_plus())


def bob_reduced_from_three_register_state(state: np.ndarray) -> np.ndarray:
    amplitudes = state.reshape(4, 2)
    return amplitudes.T @ amplitudes.conj()


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def branch_bob_rho(
    state: np.ndarray, projector: np.ndarray
) -> tuple[float, np.ndarray]:
    projected = np.kron(projector, I2) @ state
    probability = float(np.real(np.vdot(projected, projected)))
    if probability <= 1e-15:
        raise ValueError("Bell branch has zero probability")
    amplitudes = projected.reshape(4, 2)
    bob_rho = amplitudes.T @ amplitudes.conj() / probability
    return probability, bob_rho


def correction_operator(z_op: np.ndarray, x_op: np.ndarray, z_bit: int, x_bit: int) -> np.ndarray:
    z_power = z_op if z_bit else I2
    x_power = x_op if x_bit else I2
    return z_power @ x_power


def fidelity_with_pure_state(state: np.ndarray, rho: np.ndarray) -> float:
    state = normalize(state)
    return float(np.real(np.vdot(state, rho @ state)))


def run_teleportation_trials(
    z_op: np.ndarray,
    x_op: np.ndarray,
    n_trials: int,
    rng: np.random.Generator,
) -> TeleportationMetrics:
    half_identity = 0.5 * I2
    min_fidelity = 1.0
    max_infidelity = 0.0
    max_branch_probability_error = 0.0
    max_total_probability_error = 0.0
    max_pre_measurement_trace_distance = 0.0
    max_post_measurement_trace_distance = 0.0
    max_pairwise_pre_message_distance = 0.0
    outcomes_seen: set[tuple[int, int]] = set()
    reference_pre_message_rho: np.ndarray | None = None

    projectors = {
        (z_bit, x_bit): bell_projector(z_op, x_op, z_bit, x_bit)
        for z_bit, x_bit in OUTCOME_ORDER
    }

    for _ in range(n_trials):
        input_state = random_qubit(rng)
        three_register_state = prepare_three_register_state(input_state)

        rho_before = bob_reduced_from_three_register_state(three_register_state)
        max_pre_measurement_trace_distance = max(
            max_pre_measurement_trace_distance,
            trace_distance(rho_before, half_identity),
        )

        total_probability = 0.0
        pre_message_rho = np.zeros((2, 2), dtype=complex)
        for z_bit, x_bit in OUTCOME_ORDER:
            probability, bob_rho = branch_bob_rho(
                three_register_state, projectors[(z_bit, x_bit)]
            )
            outcomes_seen.add((z_bit, x_bit))
            total_probability += probability
            max_branch_probability_error = max(
                max_branch_probability_error, abs(probability - 0.25)
            )
            pre_message_rho += probability * bob_rho

            correction = correction_operator(z_op, x_op, z_bit, x_bit)
            corrected_rho = correction @ bob_rho @ correction.conj().T
            fidelity = fidelity_with_pure_state(input_state, corrected_rho)
            min_fidelity = min(min_fidelity, fidelity)
            max_infidelity = max(max_infidelity, abs(1.0 - fidelity))

        max_total_probability_error = max(
            max_total_probability_error, abs(total_probability - 1.0)
        )
        max_post_measurement_trace_distance = max(
            max_post_measurement_trace_distance,
            trace_distance(pre_message_rho, half_identity),
        )
        if reference_pre_message_rho is None:
            reference_pre_message_rho = pre_message_rho
        else:
            max_pairwise_pre_message_distance = max(
                max_pairwise_pre_message_distance,
                trace_distance(pre_message_rho, reference_pre_message_rho),
            )

    return TeleportationMetrics(
        n_trials=n_trials,
        min_fidelity=min_fidelity,
        max_infidelity=max_infidelity,
        max_branch_probability_error=max_branch_probability_error,
        max_total_probability_error=max_total_probability_error,
        max_pre_measurement_trace_distance=max_pre_measurement_trace_distance,
        max_post_measurement_trace_distance=max_post_measurement_trace_distance,
        max_pairwise_pre_message_distance=max_pairwise_pre_message_distance,
        outcomes_seen=tuple(sorted(outcomes_seen)),
    )


def evaluate_operator_set(
    z_site: np.ndarray,
    x_site: np.ndarray,
    indices: tuple[int, int],
    n_trials: int,
    rng: np.random.Generator,
    tolerance: float,
) -> OperatorSetMetrics:
    z_logical = restrict_to_encoded_qubit(z_site, indices)
    x_logical = restrict_to_encoded_qubit(x_site, indices)

    z_signed, z_sign = signed_pauli_match(z_logical, Z2, tolerance)
    x_signed, x_sign = signed_pauli_match(x_logical, X2, tolerance)
    z_leakage = leakage_norm(z_site, indices)
    x_leakage = leakage_norm(x_site, indices)

    z_square_error = max_abs(z_logical @ z_logical - I2)
    x_square_error = max_abs(x_logical @ x_logical - I2)
    anticommutator_norm = float(np.linalg.norm(z_logical @ x_logical + x_logical @ z_logical))
    projector = bell_projector_metrics(z_logical, x_logical)

    logical_pauli_pass = bool(
        z_signed
        and x_signed
        and z_leakage < tolerance
        and x_leakage < tolerance
        and z_square_error < tolerance
        and x_square_error < tolerance
        and anticommutator_norm < tolerance
    )
    projector_pass = bool(
        projector.resolution_error < tolerance
        and projector.idempotence_error < tolerance
        and projector.orthogonality_error < tolerance
    )

    teleportation: TeleportationMetrics | None = None
    teleportation_pass: bool | None = None
    if logical_pauli_pass and projector_pass:
        teleportation = run_teleportation_trials(z_logical, x_logical, n_trials, rng)
        teleportation_pass = bool(
            teleportation.max_infidelity < tolerance
            and teleportation.max_branch_probability_error < tolerance
            and teleportation.max_total_probability_error < tolerance
            and teleportation.max_pre_measurement_trace_distance < tolerance
            and teleportation.max_post_measurement_trace_distance < tolerance
            and teleportation.max_pairwise_pre_message_distance < tolerance
            and set(teleportation.outcomes_seen) == set(OUTCOME_ORDER)
        )

    return OperatorSetMetrics(
        z_signed_pauli=z_signed,
        z_sign=z_sign,
        x_signed_pauli=x_signed,
        x_sign=x_sign,
        z_leakage=z_leakage,
        x_leakage=x_leakage,
        z_square_error=z_square_error,
        x_square_error=x_square_error,
        anticommutator_norm=anticommutator_norm,
        projector_metrics=projector,
        logical_pauli_pass=logical_pauli_pass,
        projector_pass=projector_pass,
        teleportation=teleportation,
        teleportation_pass=teleportation_pass,
        x_restriction_zero=bool(np.allclose(x_logical, np.zeros((2, 2)), atol=tolerance)),
    )


def classify_failure(
    label: str,
    geometry: Geometry,
    logical_axis: int,
    metrics: OperatorSetMetrics,
    tolerance: float,
) -> str | None:
    if metrics.logical_pauli_pass:
        return None
    if not metrics.z_signed_pauli:
        return "z_restriction_not_signed_pauli"
    if metrics.z_leakage >= tolerance:
        return "z_leaks_out_of_encoded_subspace"
    if (
        label == "current_fixed_x"
        and logical_axis != geometry.dim - 1
        and not metrics.x_signed_pauli
        and metrics.x_leakage >= tolerance
    ):
        return "current_pair_hop_x_flips_last_axis_not_logical_axis"
    if not metrics.x_signed_pauli:
        return "x_restriction_not_signed_pauli"
    if metrics.x_leakage >= tolerance:
        return "x_leaks_out_of_encoded_subspace"
    if metrics.x_square_error >= tolerance:
        return "x_square_not_identity"
    if metrics.anticommutator_norm >= tolerance:
        return "logical_anticommutator_nonzero"
    return "unknown_logical_pauli_failure"


def valid_geometries(dims: Iterable[int], sides: Iterable[int]) -> tuple[list[Geometry], list[tuple[int, int, str]]]:
    geometries: list[Geometry] = []
    skipped: list[tuple[int, int, str]] = []
    for dim in dims:
        for side in sides:
            if dim not in (1, 2, 3):
                skipped.append((dim, side, "dimension outside audited 1D/2D/3D context"))
                continue
            if side <= 0:
                skipped.append((dim, side, "side length must be positive"))
                continue
            if side % 2 != 0:
                skipped.append((dim, side, "KS cell/taste decomposition requires even side"))
                continue
            geometries.append(Geometry(dim=dim, side=side))
    return geometries, skipped


def axis_taste_x(dim: int, side: int, axis: int) -> np.ndarray:
    paulis = [I2] * dim
    paulis[axis] = X2
    return build_cell_taste_operator(dim, side, paulis)


def survey(
    dims: tuple[int, ...],
    sides: tuple[int, ...],
    n_trials: int,
    seed: int,
    tolerance: float,
) -> tuple[list[Geometry], list[tuple[int, int, str]], GateSummary, GateSummary]:
    geometries, skipped = valid_geometries(dims, sides)
    current_summary = GateSummary(label="current_fixed_x")
    adapted_summary = GateSummary(label="axis_adapted_x")
    rng = np.random.default_rng(seed)

    for geometry in geometries:
        z_site = build_sublattice_z(geometry.dim, geometry.side)
        current_x_site = build_pair_hop_x(geometry.dim, geometry.side)
        adapted_x_by_axis = {
            axis: axis_taste_x(geometry.dim, geometry.side, axis)
            for axis in range(geometry.dim)
        }

        cells = itertools.product(range(geometry.side // 2), repeat=geometry.dim)
        for cell in cells:
            for logical_axis in range(geometry.dim):
                spectator_axes = tuple(axis for axis in range(geometry.dim) if axis != logical_axis)
                spectator_choices = itertools.product((0, 1), repeat=len(spectator_axes))
                for spectators in spectator_choices:
                    indices = encoded_indices(
                        geometry.dim,
                        geometry.side,
                        cell,
                        logical_axis,
                        spectators,
                    )

                    current_metrics = evaluate_operator_set(
                        z_site,
                        current_x_site,
                        indices,
                        n_trials,
                        rng,
                        tolerance,
                    )
                    current_summary.update(
                        geometry,
                        logical_axis,
                        current_metrics,
                        classify_failure(
                            "current_fixed_x",
                            geometry,
                            logical_axis,
                            current_metrics,
                            tolerance,
                        ),
                    )

                    adapted_metrics = evaluate_operator_set(
                        z_site,
                        adapted_x_by_axis[logical_axis],
                        indices,
                        n_trials,
                        rng,
                        tolerance,
                    )
                    adapted_summary.update(
                        geometry,
                        logical_axis,
                        adapted_metrics,
                        classify_failure(
                            "axis_adapted_x",
                            geometry,
                            logical_axis,
                            adapted_metrics,
                            tolerance,
                        ),
                    )

    return geometries, skipped, current_summary, adapted_summary


def format_counter(counter: collections.Counter[object]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}={value}" for key, value in sorted(counter.items(), key=lambda item: str(item[0])))


def print_gate_summary(summary: GateSummary) -> None:
    print(f"{summary.label}:")
    print(f"  logical Pauli pass: {summary.logical_pauli_pass}/{summary.total_cases}")
    print(f"  Bell-projector gate pass: {summary.projector_pass}/{summary.total_cases}")
    print(
        "  teleportation/no-signaling pass: "
        f"{summary.teleportation_pass}/{summary.teleportation_run} run "
        f"({summary.total_cases - summary.teleportation_run} skipped before teleportation)"
    )
    print(f"  Z sign counts: {format_counter(summary.z_sign_counts)}")
    print(f"  X sign counts: {format_counter(summary.x_sign_counts)}")
    print(f"  failure causes: {format_counter(summary.failure_causes)}")
    print(f"  zero X-restriction failures: {summary.zero_x_restriction_failures}")
    print(f"  max Z leakage: {summary.max_z_leakage:.3e}")
    print(f"  max X leakage: {summary.max_x_leakage:.3e}")
    print(f"  max failed-case X leakage: {summary.max_failed_x_leakage:.3e}")
    print(f"  max Z^2-I error: {summary.max_z_square_error:.3e}")
    print(f"  max X^2-I error: {summary.max_x_square_error:.3e}")
    print(f"  max anticommutator norm: {summary.max_anticommutator_norm:.3e}")
    print(f"  max Bell-projector resolution error: {summary.max_projector_resolution_error:.3e}")
    print(f"  max Bell-projector idempotence error: {summary.max_projector_idempotence_error:.3e}")
    print(f"  max Bell-projector orthogonality error: {summary.max_projector_orthogonality_error:.3e}")
    if summary.teleportation_run:
        print(f"  minimum corrected-state fidelity: {summary.min_fidelity:.16f}")
        print(f"  maximum infidelity: {summary.max_infidelity:.3e}")
        print(f"  max branch probability error from 1/4: {summary.max_branch_probability_error:.3e}")
        print(f"  max total probability error from 1: {summary.max_total_probability_error:.3e}")
        print(
            "  max Bob trace distance to I/2 before Alice measurement: "
            f"{summary.max_pre_measurement_trace_distance:.3e}"
        )
        print(
            "  max Bob trace distance to I/2 after Alice measurement before message: "
            f"{summary.max_post_measurement_trace_distance:.3e}"
        )
        print(
            "  max pairwise pre-message Bob-state distance across inputs: "
            f"{summary.max_pairwise_pre_message_distance:.3e}"
        )
        print(f"  Bell outcomes seen: {sorted(summary.outcomes_seen)}")


def print_axis_table(current_summary: GateSummary, adapted_summary: GateSummary) -> None:
    print("Pass counts by dimension and logical axis:")
    print("  dim axis current_pass/total adapted_pass/total")
    keys = sorted(set(current_summary.by_dim_axis) | set(adapted_summary.by_dim_axis))
    for dim, axis in keys:
        current_total, current_pass = current_summary.by_dim_axis.get((dim, axis), [0, 0])
        adapted_total, adapted_pass = adapted_summary.by_dim_axis.get((dim, axis), [0, 0])
        print(
            f"  {dim:>3d} {axis:>4d} "
            f"{current_pass:>6d}/{current_total:<6d} "
            f"{adapted_pass:>6d}/{adapted_total:<6d}"
        )


def print_summary(
    geometries: list[Geometry],
    skipped: list[tuple[int, int, str]],
    current_summary: GateSummary,
    adapted_summary: GateSummary,
    dims: tuple[int, ...],
    sides: tuple[int, ...],
    n_trials: int,
    seed: int,
    tolerance: float,
) -> bool:
    print("TASTE-QUBIT ENCODING PORTABILITY AUDIT")
    print("Status: numerical planning audit; quantum state teleportation only")
    print()
    print(f"Requested dimensions: {dims}")
    print(f"Requested side lengths: {sides}")
    print(f"Valid KS geometries surveyed: {len(geometries)}")
    print(f"Skipped invalid/out-of-scope geometries: {len(skipped)}")
    print(f"Random teleportation trials per accepted encoding: {n_trials} (seed={seed})")
    print(f"Tolerance: {tolerance:.1e}")
    print()

    if skipped:
        print("Skipped geometries:")
        for dim, side, reason in skipped:
            print(f"  dim={dim} side={side}: {reason}")
        print()

    total_cells = sum(geometry.n_cells for geometry in geometries)
    print("Geometry totals:")
    print(f"  cell sets across geometries: {total_cells}")
    print(f"  encoding cases surveyed: {current_summary.total_cases}")
    print("  case = one geometry, cell, spectator assignment, and logical axis")
    print()

    print_axis_table(current_summary, adapted_summary)
    print()
    print_gate_summary(current_summary)
    print()
    print_gate_summary(adapted_summary)
    print()

    print("Interpretation:")
    print(
        "  The current fixed pair-hop X generalizes across all surveyed cells and "
        "spectator tastes only when the logical taste axis is the last axis."
    )
    print(
        "  Non-last logical axes fail because the current pair-hop X flips the last "
        "taste bit, leaks out of the encoded subspace, and has zero 2x2 "
        "restriction on those encodings."
    )
    print(
        "  Retargeting X to the selected logical taste axis restores the algebraic "
        "logical-Pauli, Bell-projector, teleportation, and no-signaling gates on "
        "all surveyed encodings."
    )
    print()
    print("Claim boundary:")
    print("  This is a finite algebraic audit on ideal encoded taste qubits.")
    print("  It does not derive a physical measurement apparatus, durable record,")
    print("  resource-preparation channel, noise model, matter transfer, charge")
    print("  transfer, mass transfer, or faster-than-light signaling.")

    current_ok = (
        current_summary.logical_pauli_pass + current_summary.failure_causes[
            "current_pair_hop_x_flips_last_axis_not_logical_axis"
        ]
        == current_summary.total_cases
        and current_summary.teleportation_pass == current_summary.teleportation_run
    )
    adapted_ok = (
        adapted_summary.logical_pauli_pass == adapted_summary.total_cases
        and adapted_summary.projector_pass == adapted_summary.total_cases
        and adapted_summary.teleportation_pass == adapted_summary.teleportation_run
        and adapted_summary.teleportation_run == adapted_summary.total_cases
    )
    return current_ok and adapted_ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dims",
        default="1,2,3",
        help="comma-separated dimensions to audit; default is context dimensions 1,2,3",
    )
    parser.add_argument(
        "--sides",
        default="2,4,6,8",
        help="comma-separated side lengths; even sides are valid for KS decomposition",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=8,
        help="random teleportation trials per accepted encoding",
    )
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--tolerance", type=float, default=1e-12, help="pass/fail tolerance")
    args = parser.parse_args()

    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    dims = parse_csv_ints(args.dims)
    sides = parse_csv_ints(args.sides)

    geometries, skipped, current_summary, adapted_summary = survey(
        dims=dims,
        sides=sides,
        n_trials=args.trials,
        seed=args.seed,
        tolerance=args.tolerance,
    )
    ok = print_summary(
        geometries=geometries,
        skipped=skipped,
        current_summary=current_summary,
        adapted_summary=adapted_summary,
        dims=dims,
        sides=sides,
        n_trials=args.trials,
        seed=args.seed,
        tolerance=args.tolerance,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
