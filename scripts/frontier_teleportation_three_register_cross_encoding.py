#!/usr/bin/env python3
"""Three-register cross-encoding taste-qubit teleportation audit.

Status: exact-support telemetry for the ideal logical three-register
cross-encoding map.  It extends the bounded cross-encoding audit from two
independently chosen
encodings to three independently chosen encodings:

    A = Alice unknown input encoding
    R = Alice Bell-resource-half encoding
    B = Bob Bell-resource-half encoding

The audited Hilbert surface is still the Kogut-Susskind cell/taste
factorization used by the protocol, portability, and cross-encoding runners:

    C^(side^dim) = C^((side/2)^dim cells) tensor C^(2^dim tastes)

This is ordinary quantum state teleportation only.  It does not claim matter
transport, mass transfer, charge transfer, energy transfer, object transport,
or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import itertools
import sys
from typing import Iterable

import numpy as np


I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)

OUTCOME_ORDER = ((0, 0), (1, 0), (0, 1), (1, 1))
OUTCOME_LABELS = {
    (0, 0): "Phi+",
    (1, 0): "Phi-",
    (0, 1): "Psi+",
    (1, 1): "Psi-",
}


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


@dataclasses.dataclass
class Encoding:
    geometry: Geometry
    cell: tuple[int, ...]
    logical_axis: int
    spectators: tuple[int, ...]
    indices: tuple[int, int]
    eta_pair: tuple[tuple[int, ...], tuple[int, ...]]
    z_logical: np.ndarray
    adapted_x_logical: np.ndarray
    fixed_x_logical: np.ndarray
    z_sign: int
    adapted_x_sign: int
    fixed_x_sign: int | None
    fixed_x_signed_pauli: bool
    fixed_x_leakage: float
    fixed_x_square_error: float
    fixed_x_anticommutator_norm: float
    fixed_x_restriction_zero: bool
    fixed_x_usable: bool

    @property
    def canonical_z_logical(self) -> np.ndarray:
        return self.z_sign * self.z_logical

    @property
    def canonical_adapted_x_logical(self) -> np.ndarray:
        return self.adapted_x_sign * self.adapted_x_logical


@dataclasses.dataclass(frozen=True)
class BellProjectorMetrics:
    resolution_error: float
    idempotence_error: float
    orthogonality_error: float


@dataclasses.dataclass(frozen=True)
class TeleportationMetrics:
    n_trials: int
    projector_resolution_error: float
    projector_idempotence_error: float
    projector_orthogonality_error: float
    min_fidelity: float
    max_infidelity: float
    max_branch_probability_error: float
    max_total_probability_error: float
    max_pre_measurement_trace_distance: float
    max_post_measurement_trace_distance: float
    max_pairwise_pre_message_distance: float
    max_corrected_trace_error: float
    outcomes_seen: tuple[tuple[int, int], ...]


@dataclasses.dataclass
class MapSummary:
    label: str
    total_cases: int = 0
    expected_pass_cases: int = 0
    teleportation_run: int = 0
    teleportation_pass: int = 0
    skipped_before_teleportation: int = 0
    unexpected_results: int = 0
    failure_causes: collections.Counter[str] = dataclasses.field(
        default_factory=collections.Counter
    )
    by_geometry: dict[tuple[int, int], list[int]] = dataclasses.field(default_factory=dict)
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
    max_corrected_trace_error: float = 0.0
    outcomes_seen: set[tuple[int, int]] = dataclasses.field(default_factory=set)

    def _record_case(self, geometry: Geometry, expected_pass: bool, result_pass: bool) -> None:
        self.total_cases += 1
        self.expected_pass_cases += int(expected_pass)
        key = (geometry.dim, geometry.side)
        if key not in self.by_geometry:
            self.by_geometry[key] = [0, 0, 0]
        self.by_geometry[key][0] += 1
        self.by_geometry[key][1] += int(result_pass)
        self.by_geometry[key][2] += int(expected_pass)
        if result_pass != expected_pass:
            self.unexpected_results += 1

    def update_skip(self, geometry: Geometry, expected_pass: bool, cause: str) -> None:
        self.skipped_before_teleportation += 1
        self.failure_causes[cause] += 1
        self._record_case(geometry, expected_pass=expected_pass, result_pass=False)

    def update_metrics(
        self,
        geometry: Geometry,
        metrics: TeleportationMetrics,
        expected_pass: bool,
        tolerance: float,
        failure_cause: str | None = None,
    ) -> None:
        result_pass = teleportation_metrics_pass(metrics, tolerance)
        if failure_cause is not None and not result_pass:
            self.failure_causes[failure_cause] += 1
        self._record_case(geometry, expected_pass=expected_pass, result_pass=result_pass)

        self.teleportation_run += 1
        self.teleportation_pass += int(result_pass)
        self.max_projector_resolution_error = max(
            self.max_projector_resolution_error,
            metrics.projector_resolution_error,
        )
        self.max_projector_idempotence_error = max(
            self.max_projector_idempotence_error,
            metrics.projector_idempotence_error,
        )
        self.max_projector_orthogonality_error = max(
            self.max_projector_orthogonality_error,
            metrics.projector_orthogonality_error,
        )
        self.min_fidelity = min(self.min_fidelity, metrics.min_fidelity)
        self.max_infidelity = max(self.max_infidelity, metrics.max_infidelity)
        self.max_branch_probability_error = max(
            self.max_branch_probability_error,
            metrics.max_branch_probability_error,
        )
        self.max_total_probability_error = max(
            self.max_total_probability_error,
            metrics.max_total_probability_error,
        )
        self.max_pre_measurement_trace_distance = max(
            self.max_pre_measurement_trace_distance,
            metrics.max_pre_measurement_trace_distance,
        )
        self.max_post_measurement_trace_distance = max(
            self.max_post_measurement_trace_distance,
            metrics.max_post_measurement_trace_distance,
        )
        self.max_pairwise_pre_message_distance = max(
            self.max_pairwise_pre_message_distance,
            metrics.max_pairwise_pre_message_distance,
        )
        self.max_corrected_trace_error = max(
            self.max_corrected_trace_error,
            metrics.max_corrected_trace_error,
        )
        self.outcomes_seen.update(metrics.outcomes_seen)


@dataclasses.dataclass
class RequirementSummary:
    total_possible_triples: int = 0
    surveyed_triples: int = 0
    by_geometry: dict[tuple[int, int], list[int]] = dataclasses.field(default_factory=dict)
    a_to_r_same_support: int = 0
    explicit_a_to_r_maps: int = 0
    r_to_b_same_support: int = 0
    explicit_r_to_b_maps: int = 0
    no_site_maps_needed: int = 0
    both_site_maps_needed: int = 0
    cross_register_bell_pairing_required: int = 0
    axis_adapted_bell_x_required: int = 0
    adapted_bell_measurement_required: int = 0
    fixed_last_axis_bell_x_sufficient: int = 0
    a_to_r_pair_kinds: collections.Counter[str] = dataclasses.field(
        default_factory=collections.Counter
    )
    r_to_b_pair_kinds: collections.Counter[str] = dataclasses.field(
        default_factory=collections.Counter
    )
    max_partial_isometry_error: float = 0.0

    def add_geometry(self, geometry: Geometry, possible: int, surveyed: int) -> None:
        self.total_possible_triples += possible
        key = (geometry.dim, geometry.side)
        if key not in self.by_geometry:
            self.by_geometry[key] = [0, 0]
        self.by_geometry[key][0] += possible
        self.by_geometry[key][1] += surveyed

    def update(self, a_encoding: Encoding, r_encoding: Encoding, b_encoding: Encoding) -> None:
        self.surveyed_triples += 1

        a_to_r_kind = pair_requirement_kind(a_encoding, r_encoding)
        r_to_b_kind = pair_requirement_kind(r_encoding, b_encoding)
        self.a_to_r_pair_kinds[a_to_r_kind] += 1
        self.r_to_b_pair_kinds[r_to_b_kind] += 1

        a_to_r_same = a_to_r_kind == "same_support"
        r_to_b_same = r_to_b_kind == "same_support"
        self.a_to_r_same_support += int(a_to_r_same)
        self.explicit_a_to_r_maps += int(not a_to_r_same)
        self.r_to_b_same_support += int(r_to_b_same)
        self.explicit_r_to_b_maps += int(not r_to_b_same)
        self.no_site_maps_needed += int(a_to_r_same and r_to_b_same)
        self.both_site_maps_needed += int((not a_to_r_same) and (not r_to_b_same))

        fixed_bell_x_sufficient = a_encoding.fixed_x_usable and r_encoding.fixed_x_usable
        cross_pairing_required = not a_to_r_same
        axis_adapted_required = not fixed_bell_x_sufficient
        adapted_bell_required = cross_pairing_required or axis_adapted_required

        self.cross_register_bell_pairing_required += int(cross_pairing_required)
        self.axis_adapted_bell_x_required += int(axis_adapted_required)
        self.adapted_bell_measurement_required += int(adapted_bell_required)
        self.fixed_last_axis_bell_x_sufficient += int(fixed_bell_x_sufficient)

        self.max_partial_isometry_error = max(
            self.max_partial_isometry_error,
            partial_isometry_error(a_encoding, r_encoding),
            partial_isometry_error(r_encoding, b_encoding),
        )


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


def encoded_indices_and_etas(
    dim: int,
    side: int,
    cell: tuple[int, ...],
    logical_axis: int,
    spectators: tuple[int, ...],
) -> tuple[tuple[int, int], tuple[tuple[int, ...], tuple[int, ...]]]:
    spectator_axes = tuple(axis for axis in range(dim) if axis != logical_axis)
    if len(spectators) != len(spectator_axes):
        raise ValueError("wrong number of spectator taste bits")

    spectator_by_axis = dict(zip(spectator_axes, spectators))
    indices: list[int] = []
    etas: list[tuple[int, ...]] = []
    for logical_bit in (0, 1):
        eta = [0] * dim
        eta[logical_axis] = logical_bit
        for axis in spectator_axes:
            eta[axis] = spectator_by_axis[axis]
        eta_tuple = tuple(eta)
        coords = tuple(2 * cell[axis] + eta_tuple[axis] for axis in range(dim))
        indices.append(coordinate_index(coords, side))
        etas.append(eta_tuple)
    return (indices[0], indices[1]), (etas[0], etas[1])


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


def axis_taste_x(dim: int, side: int, axis: int) -> np.ndarray:
    paulis = [I2] * dim
    paulis[axis] = X2
    return build_cell_taste_operator(dim, side, paulis)


def enumerate_encodings(geometry: Geometry, tolerance: float) -> list[Encoding]:
    z_site = build_sublattice_z(geometry.dim, geometry.side)
    fixed_x_site = build_pair_hop_x(geometry.dim, geometry.side)
    adapted_x_by_axis = {
        axis: axis_taste_x(geometry.dim, geometry.side, axis)
        for axis in range(geometry.dim)
    }

    encodings: list[Encoding] = []
    for cell in itertools.product(range(geometry.side // 2), repeat=geometry.dim):
        for logical_axis in range(geometry.dim):
            spectator_axes = tuple(axis for axis in range(geometry.dim) if axis != logical_axis)
            for spectators in itertools.product((0, 1), repeat=len(spectator_axes)):
                indices, eta_pair = encoded_indices_and_etas(
                    geometry.dim,
                    geometry.side,
                    cell,
                    logical_axis,
                    spectators,
                )
                z_logical = restrict_to_encoded_qubit(z_site, indices)
                adapted_x_logical = restrict_to_encoded_qubit(
                    adapted_x_by_axis[logical_axis],
                    indices,
                )
                fixed_x_logical = restrict_to_encoded_qubit(fixed_x_site, indices)

                z_signed, z_sign = signed_pauli_match(z_logical, Z2, tolerance)
                adapted_x_signed, adapted_x_sign = signed_pauli_match(
                    adapted_x_logical,
                    X2,
                    tolerance,
                )
                fixed_x_signed, fixed_x_sign = signed_pauli_match(
                    fixed_x_logical,
                    X2,
                    tolerance,
                )
                if not z_signed or z_sign is None:
                    raise ValueError(f"Z is not a signed Pauli on indices {indices}")
                if not adapted_x_signed or adapted_x_sign is None:
                    raise ValueError(f"adapted X is not a signed Pauli on indices {indices}")

                fixed_x_square_error = max_abs(fixed_x_logical @ fixed_x_logical - I2)
                fixed_x_anticommutator_norm = float(
                    np.linalg.norm(z_logical @ fixed_x_logical + fixed_x_logical @ z_logical)
                )
                fixed_x_leakage = leakage_norm(fixed_x_site, indices)
                fixed_x_usable = bool(
                    fixed_x_signed
                    and fixed_x_leakage < tolerance
                    and fixed_x_square_error < tolerance
                    and fixed_x_anticommutator_norm < tolerance
                )

                encodings.append(
                    Encoding(
                        geometry=geometry,
                        cell=cell,
                        logical_axis=logical_axis,
                        spectators=spectators,
                        indices=indices,
                        eta_pair=eta_pair,
                        z_logical=z_logical,
                        adapted_x_logical=adapted_x_logical,
                        fixed_x_logical=fixed_x_logical,
                        z_sign=z_sign,
                        adapted_x_sign=adapted_x_sign,
                        fixed_x_sign=fixed_x_sign,
                        fixed_x_signed_pauli=fixed_x_signed,
                        fixed_x_leakage=fixed_x_leakage,
                        fixed_x_square_error=fixed_x_square_error,
                        fixed_x_anticommutator_norm=fixed_x_anticommutator_norm,
                        fixed_x_restriction_zero=bool(
                            np.allclose(fixed_x_logical, np.zeros((2, 2)), atol=tolerance)
                        ),
                        fixed_x_usable=fixed_x_usable,
                    )
                )
    return encodings


def bell_projector(
    z_a: np.ndarray,
    x_a: np.ndarray,
    z_r: np.ndarray,
    x_r: np.ndarray,
    z_bit: int,
    x_bit: int,
) -> np.ndarray:
    zz = np.kron(z_a, z_r)
    xx = np.kron(x_a, x_r)
    identity = np.eye(4, dtype=complex)
    return 0.25 * (identity + ((-1) ** x_bit) * zz) @ (
        identity + ((-1) ** z_bit) * xx
    )


def bell_projector_metrics(
    z_a: np.ndarray,
    x_a: np.ndarray,
    z_r: np.ndarray,
    x_r: np.ndarray,
) -> BellProjectorMetrics:
    identity = np.eye(4, dtype=complex)
    projectors = [
        bell_projector(z_a, x_a, z_r, x_r, z_bit, x_bit)
        for z_bit, x_bit in OUTCOME_ORDER
    ]
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


def conversion_bell_state(conversion_map: np.ndarray) -> np.ndarray:
    state = np.zeros(4, dtype=complex)
    for logical_bit in range(2):
        resource_basis = np.zeros(2, dtype=complex)
        resource_basis[logical_bit] = 1.0
        state += np.kron(resource_basis, conversion_map[:, logical_bit])
    return normalize(state)


def prepare_three_register_state(input_state: np.ndarray, resource_conversion_map: np.ndarray) -> np.ndarray:
    return np.kron(input_state, conversion_bell_state(resource_conversion_map))


def bob_reduced_from_three_register_state(state: np.ndarray) -> np.ndarray:
    amplitudes = state.reshape(4, 2)
    return amplitudes.T @ amplitudes.conj()


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def branch_bob_rho(state: np.ndarray, measurement_operator: np.ndarray) -> tuple[float, np.ndarray]:
    projected = np.kron(measurement_operator, I2) @ state
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
    measure_z_a: np.ndarray,
    measure_x_a: np.ndarray,
    measure_z_r: np.ndarray,
    measure_x_r: np.ndarray,
    bob_z_op: np.ndarray,
    bob_x_op: np.ndarray,
    resource_conversion_map: np.ndarray,
    target_conversion_map: np.ndarray,
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
    max_corrected_trace_error = 0.0
    outcomes_seen: set[tuple[int, int]] = set()
    reference_pre_message_rho: np.ndarray | None = None

    projector_metrics = bell_projector_metrics(
        measure_z_a,
        measure_x_a,
        measure_z_r,
        measure_x_r,
    )
    measurement_operators = {
        (z_bit, x_bit): bell_projector(
            measure_z_a,
            measure_x_a,
            measure_z_r,
            measure_x_r,
            z_bit,
            x_bit,
        )
        for z_bit, x_bit in OUTCOME_ORDER
    }

    for _ in range(n_trials):
        input_state = random_qubit(rng)
        target_state = normalize(target_conversion_map @ input_state)
        three_register_state = prepare_three_register_state(
            input_state,
            resource_conversion_map,
        )

        rho_before = bob_reduced_from_three_register_state(three_register_state)
        max_pre_measurement_trace_distance = max(
            max_pre_measurement_trace_distance,
            trace_distance(rho_before, half_identity),
        )

        total_probability = 0.0
        pre_message_rho = np.zeros((2, 2), dtype=complex)
        for z_bit, x_bit in OUTCOME_ORDER:
            probability, bob_rho = branch_bob_rho(
                three_register_state,
                measurement_operators[(z_bit, x_bit)],
            )
            outcomes_seen.add((z_bit, x_bit))
            total_probability += probability
            max_branch_probability_error = max(
                max_branch_probability_error,
                abs(probability - 0.25),
            )
            pre_message_rho += probability * bob_rho

            correction = correction_operator(bob_z_op, bob_x_op, z_bit, x_bit)
            corrected_rho = correction @ bob_rho @ correction.conj().T
            max_corrected_trace_error = max(
                max_corrected_trace_error,
                float(abs(np.trace(corrected_rho) - 1.0)),
            )
            fidelity = fidelity_with_pure_state(target_state, corrected_rho)
            min_fidelity = min(min_fidelity, fidelity)
            max_infidelity = max(max_infidelity, abs(1.0 - fidelity))

        max_total_probability_error = max(
            max_total_probability_error,
            abs(total_probability - 1.0),
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
        projector_resolution_error=projector_metrics.resolution_error,
        projector_idempotence_error=projector_metrics.idempotence_error,
        projector_orthogonality_error=projector_metrics.orthogonality_error,
        min_fidelity=min_fidelity,
        max_infidelity=max_infidelity,
        max_branch_probability_error=max_branch_probability_error,
        max_total_probability_error=max_total_probability_error,
        max_pre_measurement_trace_distance=max_pre_measurement_trace_distance,
        max_post_measurement_trace_distance=max_post_measurement_trace_distance,
        max_pairwise_pre_message_distance=max_pairwise_pre_message_distance,
        max_corrected_trace_error=max_corrected_trace_error,
        outcomes_seen=tuple(sorted(outcomes_seen)),
    )


def teleportation_metrics_pass(metrics: TeleportationMetrics, tolerance: float) -> bool:
    return bool(
        metrics.projector_resolution_error < tolerance
        and metrics.projector_idempotence_error < tolerance
        and metrics.projector_orthogonality_error < tolerance
        and metrics.max_infidelity < tolerance
        and metrics.max_branch_probability_error < tolerance
        and metrics.max_total_probability_error < tolerance
        and metrics.max_pre_measurement_trace_distance < tolerance
        and metrics.max_post_measurement_trace_distance < tolerance
        and metrics.max_pairwise_pre_message_distance < tolerance
        and metrics.max_corrected_trace_error < tolerance
        and set(metrics.outcomes_seen) == set(OUTCOME_ORDER)
    )


def partial_isometry_error(source: Encoding, target: Encoding) -> float:
    n_sites = source.geometry.n_sites
    conversion = np.zeros((n_sites, n_sites), dtype=complex)
    source_projector = np.zeros((n_sites, n_sites), dtype=complex)
    target_projector = np.zeros((n_sites, n_sites), dtype=complex)
    for source_index, target_index in zip(source.indices, target.indices):
        conversion[target_index, source_index] = 1.0
        source_projector[source_index, source_index] = 1.0
        target_projector[target_index, target_index] = 1.0
    return max(
        max_abs(conversion.conj().T @ conversion - source_projector),
        max_abs(conversion @ conversion.conj().T - target_projector),
    )


def pair_requirement_kind(source: Encoding, target: Encoding) -> str:
    same_support = source.indices == target.indices
    same_cell = source.cell == target.cell
    same_taste = source.eta_pair == target.eta_pair

    if same_support:
        return "same_support"
    if same_taste and not same_cell:
        return "relocation_same_taste"
    if same_cell and not same_taste:
        return "in_cell_retaste"
    return "relocation_and_retaste"


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


def encode_triple_index(a_index: int, r_index: int, b_index: int, n_encodings: int) -> int:
    return (a_index * n_encodings + r_index) * n_encodings + b_index


def decode_triple_index(index: int, n_encodings: int) -> tuple[int, int, int]:
    b_index = index % n_encodings
    quotient = index // n_encodings
    r_index = quotient % n_encodings
    a_index = quotient // n_encodings
    return a_index, r_index, b_index


def select_triple_indices(
    n_encodings: int,
    max_triples: int,
    rng: np.random.Generator,
) -> list[int]:
    total = n_encodings**3
    if max_triples <= 0 or total <= max_triples:
        return list(range(total))

    selected: set[int] = set()

    def add(a_index: int, r_index: int, b_index: int) -> None:
        if len(selected) < max_triples:
            selected.add(encode_triple_index(a_index, r_index, b_index, n_encodings))

    for i in range(n_encodings):
        add(i, i, i)
    for i in range(n_encodings):
        add(i, (i + 1) % n_encodings, (i + 1) % n_encodings)
    for i in range(n_encodings):
        add(i, i, (i + 1) % n_encodings)
    for i in range(n_encodings):
        add(i, (i + 1) % n_encodings, (i + 2) % n_encodings)

    while len(selected) < max_triples:
        selected.add(int(rng.integers(0, total)))

    return sorted(selected)


def classify_fixed_bell_failure(a_encoding: Encoding, r_encoding: Encoding) -> str:
    a_bad = not a_encoding.fixed_x_usable
    r_bad = not r_encoding.fixed_x_usable
    if a_bad and r_bad:
        return "a_and_r_bell_x_not_axis_adapted"
    if a_bad:
        return "a_bell_x_not_axis_adapted"
    if r_bad:
        return "r_bell_x_not_axis_adapted"
    return "unexpected_fixed_bell_failure"


def classify_bob_fixed_failure(b_encoding: Encoding) -> str:
    if b_encoding.fixed_x_restriction_zero:
        return "bob_fixed_pairhop_x_zero_on_encoding"
    if not b_encoding.fixed_x_signed_pauli:
        return "bob_fixed_pairhop_x_not_logical_x"
    if b_encoding.fixed_x_leakage > 0.0:
        return "bob_fixed_pairhop_x_leaks_out_of_encoding"
    return "bob_fixed_pairhop_x_not_usable"


def format_counter(counter: collections.Counter[object]) -> str:
    if not counter:
        return "none"
    return ", ".join(
        f"{key}={value}" for key, value in sorted(counter.items(), key=lambda item: str(item[0]))
    )


def format_outcomes(outcomes: set[tuple[int, int]]) -> str:
    ordered = [outcome for outcome in OUTCOME_ORDER if outcome in outcomes]
    return ", ".join(OUTCOME_LABELS[outcome] for outcome in ordered)


def print_by_geometry(summary: MapSummary) -> None:
    print("  by geometry: dim side pass/total expected_pass")
    for (dim, side), (total, passed, expected) in sorted(summary.by_geometry.items()):
        print(f"    {dim:>3d} {side:>4d} {passed:>6d}/{total:<6d} {expected:>6d}")


def print_map_summary(summary: MapSummary) -> None:
    print(f"{summary.label}:")
    print(f"  expected pass cases: {summary.expected_pass_cases}/{summary.total_cases}")
    print(
        "  teleportation/no-signaling pass: "
        f"{summary.teleportation_pass}/{summary.teleportation_run} run "
        f"({summary.skipped_before_teleportation} skipped before teleportation)"
    )
    print(f"  unexpected result count: {summary.unexpected_results}")
    print(f"  failure causes: {format_counter(summary.failure_causes)}")
    print_by_geometry(summary)
    if summary.teleportation_run:
        print(f"  max Bell-projector resolution error: {summary.max_projector_resolution_error:.3e}")
        print(f"  max Bell-projector idempotence error: {summary.max_projector_idempotence_error:.3e}")
        print(f"  max Bell-projector orthogonality error: {summary.max_projector_orthogonality_error:.3e}")
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
        print(f"  max corrected-state trace error: {summary.max_corrected_trace_error:.3e}")
        print("  Bell outcomes seen: " + format_outcomes(summary.outcomes_seen))


def survey(
    dims: tuple[int, ...],
    sides: tuple[int, ...],
    n_trials: int,
    seed: int,
    tolerance: float,
    max_triples_per_geometry: int,
) -> tuple[
    list[Geometry],
    list[tuple[int, int, str]],
    dict[Geometry, list[Encoding]],
    RequirementSummary,
    MapSummary,
    MapSummary,
    MapSummary,
    MapSummary,
    MapSummary,
]:
    geometries, skipped = valid_geometries(dims, sides)
    encodings_by_geometry = {
        geometry: enumerate_encodings(geometry, tolerance) for geometry in geometries
    }

    requirements = RequirementSummary()
    adapted_summary = MapSummary(label="axis_adapted_three_register_cross_encoding")
    missing_a_to_r_summary = MapSummary(label="missing_a_to_r_conversion_control")
    fixed_bell_summary = MapSummary(label="non_adapted_bell_measurement_control")
    bob_fixed_summary = MapSummary(label="non_adapted_bob_correction_control")
    wrong_resource_summary = MapSummary(label="wrong_b_resource_conversion_control")

    trial_rng = np.random.default_rng(seed)
    selection_rng = np.random.default_rng(seed + 1)

    for geometry in geometries:
        encodings = encodings_by_geometry[geometry]
        n_encodings = len(encodings)
        triple_indices = select_triple_indices(
            n_encodings,
            max_triples=max_triples_per_geometry,
            rng=selection_rng,
        )
        requirements.add_geometry(
            geometry,
            possible=n_encodings**3,
            surveyed=len(triple_indices),
        )

        for triple_index in triple_indices:
            a_index, r_index, b_index = decode_triple_index(triple_index, n_encodings)
            a_encoding = encodings[a_index]
            r_encoding = encodings[r_index]
            b_encoding = encodings[b_index]
            requirements.update(a_encoding, r_encoding, b_encoding)

            adapted_metrics = run_teleportation_trials(
                measure_z_a=a_encoding.canonical_z_logical,
                measure_x_a=a_encoding.canonical_adapted_x_logical,
                measure_z_r=r_encoding.canonical_z_logical,
                measure_x_r=r_encoding.canonical_adapted_x_logical,
                bob_z_op=b_encoding.canonical_z_logical,
                bob_x_op=b_encoding.canonical_adapted_x_logical,
                resource_conversion_map=I2,
                target_conversion_map=I2,
                n_trials=n_trials,
                rng=trial_rng,
            )
            adapted_summary.update_metrics(
                geometry=geometry,
                metrics=adapted_metrics,
                expected_pass=True,
                tolerance=tolerance,
            )

            if a_encoding.indices == r_encoding.indices:
                missing_a_to_r_summary.update_metrics(
                    geometry=geometry,
                    metrics=adapted_metrics,
                    expected_pass=True,
                    tolerance=tolerance,
                )
            else:
                missing_a_to_r_summary.update_skip(
                    geometry=geometry,
                    expected_pass=False,
                    cause="missing_explicit_a_to_r_site_conversion",
                )

            fixed_bell_expected = a_encoding.fixed_x_usable and r_encoding.fixed_x_usable
            if fixed_bell_expected:
                fixed_bell_metrics = run_teleportation_trials(
                    measure_z_a=a_encoding.canonical_z_logical,
                    measure_x_a=a_encoding.fixed_x_logical,
                    measure_z_r=r_encoding.canonical_z_logical,
                    measure_x_r=r_encoding.fixed_x_logical,
                    bob_z_op=b_encoding.canonical_z_logical,
                    bob_x_op=b_encoding.canonical_adapted_x_logical,
                    resource_conversion_map=I2,
                    target_conversion_map=I2,
                    n_trials=n_trials,
                    rng=trial_rng,
                )
                fixed_bell_summary.update_metrics(
                    geometry=geometry,
                    metrics=fixed_bell_metrics,
                    expected_pass=True,
                    tolerance=tolerance,
                )
            else:
                fixed_bell_summary.update_skip(
                    geometry=geometry,
                    expected_pass=False,
                    cause=classify_fixed_bell_failure(a_encoding, r_encoding),
                )

            bob_fixed_metrics = run_teleportation_trials(
                measure_z_a=a_encoding.canonical_z_logical,
                measure_x_a=a_encoding.canonical_adapted_x_logical,
                measure_z_r=r_encoding.canonical_z_logical,
                measure_x_r=r_encoding.canonical_adapted_x_logical,
                bob_z_op=b_encoding.canonical_z_logical,
                bob_x_op=b_encoding.fixed_x_logical,
                resource_conversion_map=I2,
                target_conversion_map=I2,
                n_trials=n_trials,
                rng=trial_rng,
            )
            bob_fixed_summary.update_metrics(
                geometry=geometry,
                metrics=bob_fixed_metrics,
                expected_pass=b_encoding.fixed_x_usable,
                tolerance=tolerance,
                failure_cause=(
                    None
                    if b_encoding.fixed_x_usable
                    else classify_bob_fixed_failure(b_encoding)
                ),
            )

            wrong_resource_metrics = run_teleportation_trials(
                measure_z_a=a_encoding.canonical_z_logical,
                measure_x_a=a_encoding.canonical_adapted_x_logical,
                measure_z_r=r_encoding.canonical_z_logical,
                measure_x_r=r_encoding.canonical_adapted_x_logical,
                bob_z_op=b_encoding.canonical_z_logical,
                bob_x_op=b_encoding.canonical_adapted_x_logical,
                resource_conversion_map=X2,
                target_conversion_map=I2,
                n_trials=n_trials,
                rng=trial_rng,
            )
            wrong_resource_summary.update_metrics(
                geometry=geometry,
                metrics=wrong_resource_metrics,
                expected_pass=False,
                tolerance=tolerance,
                failure_cause="wrong_b_resource_conversion_map",
            )

    return (
        geometries,
        skipped,
        encodings_by_geometry,
        requirements,
        adapted_summary,
        missing_a_to_r_summary,
        fixed_bell_summary,
        bob_fixed_summary,
        wrong_resource_summary,
    )


def print_requirement_summary(requirements: RequirementSummary) -> None:
    print("Three-register requirement classification:")
    print("  geometry: dim side surveyed/possible triples")
    for (dim, side), (possible, surveyed) in sorted(requirements.by_geometry.items()):
        print(f"    {dim:>3d} {side:>4d} {surveyed:>6d}/{possible:<8d}")
    print(f"  triples surveyed: {requirements.surveyed_triples}")
    print(f"  possible triples in requested geometries: {requirements.total_possible_triples}")
    print()
    print("  A input -> R Alice-resource-half map:")
    print(f"    no site conversion needed: {requirements.a_to_r_same_support}")
    print(f"    explicit A->R site maps needed: {requirements.explicit_a_to_r_maps}")
    print(f"    breakdown: {format_counter(requirements.a_to_r_pair_kinds)}")
    print()
    print("  R Alice-resource-half -> B Bob-resource-half map:")
    print(f"    no site conversion needed: {requirements.r_to_b_same_support}")
    print(f"    explicit R->B resource site maps needed: {requirements.explicit_r_to_b_maps}")
    print(f"    breakdown: {format_counter(requirements.r_to_b_pair_kinds)}")
    print()
    print("  Bell-measurement adaptation:")
    print(f"    cross-register A/R Bell pairing required: {requirements.cross_register_bell_pairing_required}")
    print(f"    axis-adapted Bell X required: {requirements.axis_adapted_bell_x_required}")
    print(f"    adapted Bell measurement required by either condition: {requirements.adapted_bell_measurement_required}")
    print(f"    fixed last-axis Bell X sufficient: {requirements.fixed_last_axis_bell_x_sufficient}")
    print()
    print("  Combined site-map requirements:")
    print(f"    no A->R or R->B site maps needed: {requirements.no_site_maps_needed}")
    print(f"    both A->R and R->B site maps needed: {requirements.both_site_maps_needed}")
    print(
        "    max partial-isometry error C^dag C=P_source, C C^dag=P_target: "
        f"{requirements.max_partial_isometry_error:.3e}"
    )


def print_summary(
    geometries: list[Geometry],
    skipped: list[tuple[int, int, str]],
    encodings_by_geometry: dict[Geometry, list[Encoding]],
    requirements: RequirementSummary,
    adapted_summary: MapSummary,
    missing_a_to_r_summary: MapSummary,
    fixed_bell_summary: MapSummary,
    bob_fixed_summary: MapSummary,
    wrong_resource_summary: MapSummary,
    dims: tuple[int, ...],
    sides: tuple[int, ...],
    n_trials: int,
    seed: int,
    tolerance: float,
    max_triples_per_geometry: int,
) -> bool:
    print("THREE-REGISTER CROSS-ENCODING TASTE-QUBIT TELEPORTATION AUDIT")
    print("Status: exact-support logical audit; quantum state teleportation only")
    print()
    print(f"Requested dimensions: {dims}")
    print(f"Requested side lengths: {sides}")
    print(f"Valid KS geometries surveyed: {len(geometries)}")
    print(f"Skipped invalid/out-of-scope geometries: {len(skipped)}")
    print(f"Random teleportation trials per surveyed triple: {n_trials} (seed={seed})")
    print(f"Max triples per geometry: {max_triples_per_geometry} (0 means exhaustive)")
    print(f"Tolerance: {tolerance:.1e}")
    print()

    if skipped:
        print("Skipped geometries:")
        for dim, side, reason in skipped:
            print(f"  dim={dim} side={side}: {reason}")
        print()

    total_encodings = sum(len(encodings) for encodings in encodings_by_geometry.values())
    print("Encoding totals:")
    print(f"  encoding supports across geometries: {total_encodings}")
    for geometry in geometries:
        n_encodings = len(encodings_by_geometry[geometry])
        print(
            f"  dim={geometry.dim} side={geometry.side}: "
            f"{n_encodings} encodings, {n_encodings ** 3} possible A/R/B triples"
        )
    print()

    print_requirement_summary(requirements)
    print()

    print_map_summary(adapted_summary)
    print()
    print_map_summary(missing_a_to_r_summary)
    print()
    print_map_summary(fixed_bell_summary)
    print()
    print_map_summary(bob_fixed_summary)
    print()
    print_map_summary(wrong_resource_summary)
    print()

    print("Interpretation:")
    print(
        "  Axis-adapted A/R Bell measurements plus axis-adapted Bob corrections "
        "pass for every surveyed three-register encoding triple."
    )
    print(
        "  If A and R are different site supports, an explicit A->R site "
        "partial isometry is required to define the Bell-pairing map."
    )
    print(
        "  If either Alice-side Bell register uses a non-last logical taste axis, "
        "the fixed pair-hop X is insufficient and the Bell measurement must be "
        "axis-adapted."
    )
    print(
        "  If R and B differ, the Bell resource requires an explicit R->B site "
        "partial isometry; a wrong logical B-side conversion preserves "
        "pre-message no-signaling but fails post-message fidelity."
    )
    print()
    print("Claim boundary:")
    print("  This is a finite algebraic audit on ideal encoded taste qubits.")
    print("  It does not derive apparatus dynamics, durable records, resource")
    print("  preparation, Hamiltonian transport, noise tolerance, matter transfer,")
    print("  object transport, charge transfer, mass transfer, energy transfer,")
    print("  or FTL signaling.")

    pass_checks = {
        "axis-adapted three-register maps": adapted_summary.unexpected_results == 0
        and adapted_summary.teleportation_pass == adapted_summary.total_cases,
        "axis-adapted all Bell outcomes": adapted_summary.outcomes_seen == set(OUTCOME_ORDER),
        "axis-adapted Bob pre-message input-independence": (
            adapted_summary.max_pre_measurement_trace_distance < tolerance
            and adapted_summary.max_post_measurement_trace_distance < tolerance
            and adapted_summary.max_pairwise_pre_message_distance < tolerance
        ),
        "missing A->R conversion control": (
            missing_a_to_r_summary.unexpected_results == 0
            and missing_a_to_r_summary.expected_pass_cases
            == missing_a_to_r_summary.teleportation_pass
            and missing_a_to_r_summary.skipped_before_teleportation
            == requirements.explicit_a_to_r_maps
        ),
        "non-adapted Bell measurement boundary": (
            fixed_bell_summary.unexpected_results == 0
            and fixed_bell_summary.expected_pass_cases == fixed_bell_summary.teleportation_pass
        ),
        "non-adapted Bob correction control": (
            bob_fixed_summary.unexpected_results == 0
            and bob_fixed_summary.expected_pass_cases == bob_fixed_summary.teleportation_pass
            and bob_fixed_summary.max_infidelity > 0.5
        ),
        "wrong B resource conversion control": (
            wrong_resource_summary.unexpected_results == 0
            and wrong_resource_summary.teleportation_pass == 0
            and wrong_resource_summary.max_infidelity > 0.5
        ),
    }
    print()
    print("Acceptance gates:")
    for name, ok in pass_checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")

    return all(pass_checks.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dims",
        default="1,2,3",
        help="comma-separated dimensions to audit; default is context dimensions 1,2,3",
    )
    parser.add_argument(
        "--sides",
        default="2,4",
        help="comma-separated even side lengths; default keeps three-register count bounded",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=4,
        help="random teleportation trials per surveyed A/R/B triple",
    )
    parser.add_argument(
        "--max-triples-per-geometry",
        type=int,
        default=512,
        help="bounded deterministic sample per geometry; use 0 for exhaustive triples",
    )
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--tolerance", type=float, default=1e-12, help="pass/fail tolerance")
    args = parser.parse_args()

    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if args.max_triples_per_geometry < 0:
        raise ValueError("--max-triples-per-geometry must be nonnegative")

    dims = parse_csv_ints(args.dims)
    sides = parse_csv_ints(args.sides)

    (
        geometries,
        skipped,
        encodings_by_geometry,
        requirements,
        adapted_summary,
        missing_a_to_r_summary,
        fixed_bell_summary,
        bob_fixed_summary,
        wrong_resource_summary,
    ) = survey(
        dims=dims,
        sides=sides,
        n_trials=args.trials,
        seed=args.seed,
        tolerance=args.tolerance,
        max_triples_per_geometry=args.max_triples_per_geometry,
    )
    ok = print_summary(
        geometries=geometries,
        skipped=skipped,
        encodings_by_geometry=encodings_by_geometry,
        requirements=requirements,
        adapted_summary=adapted_summary,
        missing_a_to_r_summary=missing_a_to_r_summary,
        fixed_bell_summary=fixed_bell_summary,
        bob_fixed_summary=bob_fixed_summary,
        wrong_resource_summary=wrong_resource_summary,
        dims=dims,
        sides=sides,
        n_trials=args.trials,
        seed=args.seed,
        tolerance=args.tolerance,
        max_triples_per_geometry=args.max_triples_per_geometry,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
