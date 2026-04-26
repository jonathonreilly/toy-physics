#!/usr/bin/env python3
"""Taste-only readout/operator model for native taste-qubit teleportation.

Status: planning / first artifact. This runner audits native site/taste
operators against the operational condition needed by the traced logical
teleportation lane:

    native operator = O_logical tensor I_env

where the retained logical qubit is the last Kogut-Susskind taste bit and the
environment is cell labels plus all spectator taste bits.

The test separates three facts that are easy to conflate:

* a fixed-environment restriction can look like a logical Pauli;
* a traced reduced state gives correct statistics only for operators that are
  identity on cells/spectators;
* Bob's pre-message input-independence is a no-signaling condition, not proof
  that Bob's marginal is unbiased or that a native readout is operational.

This is ordinary quantum state teleportation planning only. It does not claim
matter teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.
"""

from __future__ import annotations

import argparse
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
OUTCOME_LABELS = {
    (0, 0): "Phi+",
    (1, 0): "Phi-",
    (0, 1): "Psi+",
    (1, 1): "Psi-",
}


@dataclasses.dataclass(frozen=True)
class SiteFactorization:
    dim: int
    side: int
    logical_axis: int
    logical: np.ndarray
    env: np.ndarray
    env_labels: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]

    @property
    def n_sites(self) -> int:
        return self.side**self.dim

    @property
    def n_env(self) -> int:
        return len(self.env_labels)


@dataclasses.dataclass(frozen=True)
class OperatorAudit:
    name: str
    role: str
    passes: bool
    frobenius_residual: float
    relative_residual: float
    max_abs_residual: float
    env_offdiag_norm: float
    env_diag_variation_norm: float
    logical_candidate: np.ndarray
    expected_error: float | None
    note: str


@dataclasses.dataclass(frozen=True)
class PairOperatorAudit:
    name: str
    role: str
    passes: bool
    frobenius_residual: float
    relative_residual: float
    logical_candidate: np.ndarray
    expected_error: float | None
    note: str


@dataclasses.dataclass(frozen=True)
class CaseAudit:
    dim: int
    side: int
    logical_axis: int
    n_sites: int
    n_env: int
    fixed_pair_equals_axis_x: float
    single_register: tuple[OperatorAudit, ...]
    pair_register: tuple[PairOperatorAudit, ...]


@dataclasses.dataclass(frozen=True)
class NoMessageAudit:
    probe_count: int
    bob_marginal_bias: float
    max_no_record_to_marginal: float
    max_pairwise_no_record_distance: float
    max_branch_probability_span: float
    note: str


def coords_from_index(index: int, dim: int, side: int) -> tuple[int, ...]:
    coords: list[int] = []
    remaining = index
    for power in range(dim - 1, -1, -1):
        stride = side**power
        coord = remaining // stride
        coords.append(coord)
        remaining %= stride
    return tuple(coords)


def factor_sites(dim: int, side: int, logical_axis: int | None = None) -> SiteFactorization:
    if side % 2 != 0:
        raise ValueError("KS taste factorization requires an even side length")
    if logical_axis is None:
        logical_axis = dim - 1
    if logical_axis < 0 or logical_axis >= dim:
        raise ValueError("logical_axis is outside the spatial dimension")

    n_sites = side**dim
    logical = np.zeros(n_sites, dtype=int)
    raw_env: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    for site in range(n_sites):
        coords = coords_from_index(site, dim, side)
        cell = tuple(coord // 2 for coord in coords)
        eta = tuple(coord % 2 for coord in coords)
        spectator = tuple(bit for axis, bit in enumerate(eta) if axis != logical_axis)
        logical[site] = eta[logical_axis]
        raw_env.append((cell, spectator))

    env_labels = tuple(dict.fromkeys(raw_env))
    env_index = {label: index for index, label in enumerate(env_labels)}
    env = np.array([env_index[label] for label in raw_env], dtype=int)
    return SiteFactorization(
        dim=dim,
        side=side,
        logical_axis=logical_axis,
        logical=logical,
        env=env,
        env_labels=env_labels,
    )


def build_cell_taste_operator(
    dim: int, side: int, taste_paulis: Iterable[np.ndarray]
) -> np.ndarray:
    taste_paulis = list(taste_paulis)
    if side % 2 != 0:
        raise ValueError("KS taste decomposition requires an even side length")
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


def build_axis_taste_operator(
    dim: int, side: int, logical_axis: int, pauli: np.ndarray
) -> np.ndarray:
    paulis = [I2.copy() for _ in range(dim)]
    paulis[logical_axis] = pauli
    return build_cell_taste_operator(dim, side, paulis)


def build_sublattice_z(dim: int, side: int) -> np.ndarray:
    n_sites = side**dim
    parity = []
    for site in range(n_sites):
        coords = coords_from_index(site, dim, side)
        parity.append((-1) ** sum(coords))
    return np.diag([float(value) for value in parity]).astype(complex)


def build_fixed_pair_hop_x(dim: int, side: int) -> np.ndarray:
    n_sites = side**dim
    if n_sites % 2 != 0:
        raise ValueError("fixed pair-hop X requires an even site count")
    op = np.zeros((n_sites, n_sites), dtype=complex)
    for pair in range(n_sites // 2):
        i = 2 * pair
        j = i + 1
        op[i, j] = 1.0
        op[j, i] = 1.0
    return op


def fixed_site_projector(n_sites: int, site: int = 0) -> np.ndarray:
    projector = np.zeros((n_sites, n_sites), dtype=complex)
    projector[site, site] = 1.0
    return projector


def env_projector(factors: SiteFactorization, env_index: int = 0) -> np.ndarray:
    projector = np.zeros((factors.n_sites, factors.n_sites), dtype=complex)
    for site, env in enumerate(factors.env):
        if env == env_index:
            projector[site, site] = 1.0
    return projector


def blocks_by_logical_env(op: np.ndarray, factors: SiteFactorization) -> np.ndarray:
    if op.shape != (factors.n_sites, factors.n_sites):
        raise ValueError("operator shape does not match the site factorization")
    blocks = np.zeros((2, factors.n_env, 2, factors.n_env), dtype=complex)
    for row_site in range(factors.n_sites):
        logical_row = factors.logical[row_site]
        env_row = factors.env[row_site]
        for col_site in range(factors.n_sites):
            logical_col = factors.logical[col_site]
            env_col = factors.env[col_site]
            blocks[logical_row, env_row, logical_col, env_col] = op[row_site, col_site]
    return blocks


def env_trace(op: np.ndarray, factors: SiteFactorization) -> np.ndarray:
    blocks = blocks_by_logical_env(op, factors)
    return np.einsum("aebe->ab", blocks, optimize=True)


def factorization_audit(
    name: str,
    role: str,
    op: np.ndarray,
    factors: SiteFactorization,
    tolerance: float,
    expected: np.ndarray | None,
    note: str,
) -> OperatorAudit:
    blocks = blocks_by_logical_env(op, factors)
    candidate = np.einsum("aebe->ab", blocks, optimize=True) / factors.n_env
    residual = blocks.copy()
    offdiag = blocks.copy()
    diag_variation_sq = 0.0
    for env in range(factors.n_env):
        residual[:, env, :, env] -= candidate
        offdiag[:, env, :, env] = 0.0
        diag_variation_sq += float(np.linalg.norm(blocks[:, env, :, env] - candidate) ** 2)

    frobenius_residual = float(np.linalg.norm(residual))
    total_norm = float(np.linalg.norm(blocks))
    expected_error = None
    if expected is not None:
        expected_error = float(np.max(np.abs(candidate - expected)))

    return OperatorAudit(
        name=name,
        role=role,
        passes=bool(np.max(np.abs(residual)) <= tolerance),
        frobenius_residual=frobenius_residual,
        relative_residual=frobenius_residual / total_norm if total_norm > 0.0 else 0.0,
        max_abs_residual=float(np.max(np.abs(residual))),
        env_offdiag_norm=float(np.linalg.norm(offdiag)),
        env_diag_variation_norm=math.sqrt(max(diag_variation_sq, 0.0)),
        logical_candidate=candidate,
        expected_error=expected_error,
        note=note,
    )


def frobenius_inner(first: np.ndarray, second: np.ndarray) -> complex:
    return complex(np.vdot(first, second))


def pair_factorization_audit(
    name: str,
    role: str,
    terms: Iterable[tuple[complex, np.ndarray, np.ndarray]],
    factors: SiteFactorization,
    tolerance: float,
    expected: np.ndarray | None,
    note: str,
) -> PairOperatorAudit:
    term_list = list(terms)
    env_dimension = factors.n_env * factors.n_env
    candidate = np.zeros((4, 4), dtype=complex)

    for coeff, op_a, op_b in term_list:
        trace_a = env_trace(op_a, factors)
        trace_b = env_trace(op_b, factors)
        candidate += coeff * np.kron(trace_a, trace_b) / env_dimension

    full_norm_sq = 0.0 + 0.0j
    for coeff_i, op_a_i, op_b_i in term_list:
        for coeff_j, op_a_j, op_b_j in term_list:
            full_norm_sq += (
                coeff_i.conjugate()
                * coeff_j
                * frobenius_inner(op_a_i, op_a_j)
                * frobenius_inner(op_b_i, op_b_j)
            )

    projection_norm_sq = env_dimension * float(np.linalg.norm(candidate) ** 2)
    residual_sq = max(float(np.real(full_norm_sq)) - projection_norm_sq, 0.0)
    total_norm = math.sqrt(max(float(np.real(full_norm_sq)), 0.0))
    frobenius_residual = math.sqrt(residual_sq)
    expected_error = None
    if expected is not None:
        expected_error = float(np.max(np.abs(candidate - expected)))

    return PairOperatorAudit(
        name=name,
        role=role,
        passes=bool(frobenius_residual <= tolerance * max(math.sqrt(env_dimension), 1.0)),
        frobenius_residual=frobenius_residual,
        relative_residual=frobenius_residual / total_norm if total_norm > 0.0 else 0.0,
        logical_candidate=candidate,
        expected_error=expected_error,
        note=note,
    )


def bell_projector(z_bit: int, x_bit: int) -> np.ndarray:
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    identity = np.eye(4, dtype=complex)
    return 0.25 * (identity + ((-1) ** x_bit) * zz) @ (
        identity + ((-1) ** z_bit) * xx
    )


def bell_terms(
    z_bit: int, x_bit: int, z_op: np.ndarray, x_op: np.ndarray
) -> tuple[tuple[complex, np.ndarray, np.ndarray], ...]:
    identity = np.eye(z_op.shape[0], dtype=complex)
    zx_op = z_op @ x_op
    z_sign = (-1) ** z_bit
    x_sign = (-1) ** x_bit
    return (
        (0.25 + 0.0j, identity, identity),
        (0.25 * x_sign + 0.0j, z_op, z_op),
        (0.25 * z_sign + 0.0j, x_op, x_op),
        (0.25 * x_sign * z_sign + 0.0j, zx_op, zx_op),
    )


def audit_case(dim: int, side: int, tolerance: float) -> CaseAudit:
    logical_axis = dim - 1
    factors = factor_sites(dim, side, logical_axis=logical_axis)
    identity = np.eye(factors.n_sites, dtype=complex)

    native_z = build_sublattice_z(dim, side)
    axis_z = build_axis_taste_operator(dim, side, logical_axis, Z2)
    axis_x = build_axis_taste_operator(dim, side, logical_axis, X2)
    fixed_x = build_fixed_pair_hop_x(dim, side)
    native_z_fixed_x = native_z @ fixed_x
    axis_z_axis_x = axis_z @ axis_x

    audits = (
        factorization_audit(
            "native sublattice Z",
            "readout/correction",
            native_z,
            factors,
            tolerance,
            Z2 if dim == 1 else None,
            "Parity Z is xi_5. It equals retained-bit Z only when there are no spectator tastes.",
        ),
        factorization_audit(
            "axis logical Z",
            "readout/correction",
            axis_z,
            factors,
            tolerance,
            Z2,
            "Z on the retained taste axis with identity on cells and spectators.",
        ),
        factorization_audit(
            "axis-adapted X",
            "readout/correction",
            axis_x,
            factors,
            tolerance,
            X2,
            "X on the retained taste axis with identity on cells and spectators.",
        ),
        factorization_audit(
            "fixed pair-hop X",
            "readout/correction",
            fixed_x,
            factors,
            tolerance,
            X2,
            "The row-major pair-hop flips the last coordinate, so it matches the retained last taste bit.",
        ),
        factorization_audit(
            "native Z then fixed X",
            "correction",
            native_z_fixed_x,
            factors,
            tolerance,
            Z2 @ X2 if dim == 1 else None,
            "Composite correction inherits the spectator leak from native sublattice Z in dim > 1.",
        ),
        factorization_audit(
            "axis Z then axis X",
            "correction",
            axis_z_axis_x,
            factors,
            tolerance,
            Z2 @ X2,
            "Taste-only composite retained-qubit correction.",
        ),
        factorization_audit(
            "native Z+ projector",
            "measurement",
            0.5 * (identity + native_z),
            factors,
            tolerance,
            0.5 * (I2 + Z2) if dim == 1 else None,
            "Projector generated by sublattice parity; spectator-resolved in dim > 1.",
        ),
        factorization_audit(
            "axis Z+ projector",
            "measurement",
            0.5 * (identity + axis_z),
            factors,
            tolerance,
            0.5 * (I2 + Z2),
            "Retained taste-bit computational-basis measurement.",
        ),
        factorization_audit(
            "axis X+ projector",
            "measurement",
            0.5 * (identity + axis_x),
            factors,
            tolerance,
            0.5 * (I2 + X2),
            "Retained taste-bit X-basis measurement.",
        ),
        factorization_audit(
            "fixed site projector",
            "measurement",
            fixed_site_projector(factors.n_sites, site=0),
            factors,
            tolerance,
            0.5 * (I2 + Z2) if factors.n_env == 1 else None,
            "Site-resolved readout selects a cell/spectator environment branch.",
        ),
        factorization_audit(
            "fixed env projector",
            "measurement",
            env_projector(factors, env_index=0),
            factors,
            tolerance,
            I2 if factors.n_env == 1 else None,
            "Environment-resolved readout is explicitly not blind to cells/spectators.",
        ),
    )

    pair_audits = (
        pair_factorization_audit(
            "axis Bell Phi+ projector",
            "Bell measurement",
            bell_terms(0, 0, axis_z, axis_x),
            factors,
            tolerance,
            bell_projector(0, 0),
            "Bell projector built from retained-bit Z and X stabilizers.",
        ),
        pair_factorization_audit(
            "native-Z/fixed-X Bell Phi+ projector",
            "Bell measurement",
            bell_terms(0, 0, native_z, fixed_x),
            factors,
            tolerance,
            bell_projector(0, 0) if dim == 1 else None,
            "Bell projector using sublattice Z; leaks spectator sectors in dim > 1.",
        ),
        pair_factorization_audit(
            "native ZZ stabilizer",
            "joint measurement",
            ((1.0 + 0.0j, native_z, native_z),),
            factors,
            tolerance,
            np.kron(Z2, Z2) if dim == 1 else None,
            "Product of parity-Z measurements; not an environment-blind logical ZZ in dim > 1.",
        ),
        pair_factorization_audit(
            "fixed XX stabilizer",
            "joint measurement",
            ((1.0 + 0.0j, fixed_x, fixed_x),),
            factors,
            tolerance,
            np.kron(X2, X2),
            "Product of retained-axis pair-hop X measurements.",
        ),
    )

    return CaseAudit(
        dim=dim,
        side=side,
        logical_axis=logical_axis,
        n_sites=factors.n_sites,
        n_env=factors.n_env,
        fixed_pair_equals_axis_x=float(np.max(np.abs(fixed_x - axis_x))),
        single_register=audits,
        pair_register=pair_audits,
    )


def projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def bell_state(z_bit: int, x_bit: int) -> np.ndarray:
    sign = -1.0 if z_bit else 1.0
    state = np.zeros(4, dtype=complex)
    if x_bit == 0:
        state[0] = 1.0 / math.sqrt(2.0)
        state[3] = sign / math.sqrt(2.0)
    else:
        state[1] = 1.0 / math.sqrt(2.0)
        state[2] = sign / math.sqrt(2.0)
    return state


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def partial_trace(rho: np.ndarray, dims: list[int], keep: list[int]) -> np.ndarray:
    keep_set = set(keep)
    traced = rho.reshape(*dims, *dims)
    current_dims = list(dims)
    for subsystem in reversed(range(len(dims))):
        if subsystem in keep_set:
            continue
        traced = np.trace(traced, axis1=subsystem, axis2=subsystem + len(current_dims))
        current_dims.pop(subsystem)
    kept_dim = int(np.prod(current_dims))
    return traced.reshape(kept_dim, kept_dim)


def teleport_no_record(
    input_rho: np.ndarray, resource_rho: np.ndarray
) -> tuple[np.ndarray, dict[tuple[int, int], float]]:
    total = np.kron(input_rho, resource_rho).reshape(2, 2, 2, 2, 2, 2)
    no_record = np.zeros((2, 2), dtype=complex)
    probabilities: dict[tuple[int, int], float] = {}
    for z_bit, x_bit in OUTCOME_ORDER:
        beta = bell_state(z_bit, x_bit).reshape(2, 2)
        branch = np.einsum("ar,arbcsd,cs->bd", beta.conj(), total, beta)
        probability = float(np.real(np.trace(branch)))
        probabilities[(z_bit, x_bit)] = probability
        no_record += branch
    return no_record, probabilities


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize zero state")
    return state / norm


def probe_states(seed: int, random_count: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    states = [
        np.array([1.0, 0.0], dtype=complex),
        np.array([0.0, 1.0], dtype=complex),
        np.array([1.0, 1.0], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, -1.0], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, 1.0j], dtype=complex) / math.sqrt(2.0),
        np.array([1.0, -1.0j], dtype=complex) / math.sqrt(2.0),
    ]
    for _ in range(random_count):
        states.append(normalize(rng.standard_normal(2) + 1j * rng.standard_normal(2)))
    return states


def no_message_audit(seed: int, random_inputs: int) -> NoMessageAudit:
    states = probe_states(seed, random_inputs)
    biased_resource = projector(np.array([1.0, 0.0, 0.0, 0.0], dtype=complex))
    bob_marginal = partial_trace(biased_resource, dims=[2, 2], keep=[1])
    half_identity = 0.5 * I2
    reference: np.ndarray | None = None
    max_no_record_to_marginal = 0.0
    max_pairwise = 0.0
    max_probability_span = 0.0

    for state in states:
        no_record, probabilities = teleport_no_record(projector(state), biased_resource)
        max_no_record_to_marginal = max(
            max_no_record_to_marginal,
            trace_distance(no_record, bob_marginal),
        )
        if reference is None:
            reference = no_record
        else:
            max_pairwise = max(max_pairwise, trace_distance(no_record, reference))
        probability_values = list(probabilities.values())
        max_probability_span = max(
            max_probability_span,
            float(max(probability_values) - min(probability_values)),
        )

    return NoMessageAudit(
        probe_count=len(states),
        bob_marginal_bias=trace_distance(bob_marginal, half_identity),
        max_no_record_to_marginal=max_no_record_to_marginal,
        max_pairwise_no_record_distance=max_pairwise,
        max_branch_probability_span=max_probability_span,
        note=(
            "Input independence holds here even though Bob's marginal is maximally "
            "biased from I/2 for a qubit and the resource is not a useful "
            "teleportation channel."
        ),
    )


def matrix_label(matrix: np.ndarray, tolerance: float) -> str:
    known = {
        "I": I2,
        "X": X2,
        "Z": Z2,
        "ZX": Z2 @ X2,
        "Pz+": 0.5 * (I2 + Z2),
        "Px+": 0.5 * (I2 + X2),
        "0": np.zeros((2, 2), dtype=complex),
    }
    if matrix.shape == (2, 2):
        for label, known_matrix in known.items():
            if np.max(np.abs(matrix - known_matrix)) <= tolerance:
                return label
    if matrix.shape == (4, 4):
        if np.max(np.abs(matrix - bell_projector(0, 0))) <= tolerance:
            return "Bell Phi+"
        if np.max(np.abs(matrix - np.kron(Z2, Z2))) <= tolerance:
            return "ZZ"
        if np.max(np.abs(matrix - np.kron(X2, X2))) <= tolerance:
            return "XX"
    return "mixed"


def fmt_float(value: float) -> str:
    if value == 0.0:
        return "0"
    if abs(value) < 1e-3:
        return f"{value:.3e}"
    return f"{value:.6f}"


def print_single_audit(audit: OperatorAudit, tolerance: float) -> None:
    status = "PASS" if audit.passes else "FAIL"
    expected = ""
    if audit.expected_error is not None:
        expected = f", expected err={fmt_float(audit.expected_error)}"
    print(
        f"    {status:4s} {audit.name:28s} "
        f"role={audit.role:17s} "
        f"max={fmt_float(audit.max_abs_residual)} "
        f"rel={fmt_float(audit.relative_residual)} "
        f"offdiag={fmt_float(audit.env_offdiag_norm)} "
        f"diag-var={fmt_float(audit.env_diag_variation_norm)} "
        f"candidate={matrix_label(audit.logical_candidate, tolerance)}"
        f"{expected}"
    )


def print_pair_audit(audit: PairOperatorAudit, tolerance: float) -> None:
    status = "PASS" if audit.passes else "FAIL"
    expected = ""
    if audit.expected_error is not None:
        expected = f", expected err={fmt_float(audit.expected_error)}"
    print(
        f"    {status:4s} {audit.name:34s} "
        f"role={audit.role:16s} "
        f"fro={fmt_float(audit.frobenius_residual)} "
        f"rel={fmt_float(audit.relative_residual)} "
        f"candidate={matrix_label(audit.logical_candidate, tolerance)}"
        f"{expected}"
    )


def print_case(case: CaseAudit, tolerance: float) -> None:
    print(f"Case: dim={case.dim} side={case.side}")
    print(
        "  factorization: "
        f"N={case.n_sites}, envs={case.n_env}, retained taste axis={case.logical_axis}"
    )
    print(
        "  fixed pair-hop X versus axis-adapted retained-bit X: "
        f"max difference={fmt_float(case.fixed_pair_equals_axis_x)}"
    )
    print("  single-register O_logical tensor I_env tests:")
    for audit in case.single_register:
        print_single_audit(audit, tolerance)
    print("  two-register representative measurement tests:")
    for audit in case.pair_register:
        print_pair_audit(audit, tolerance)
    print()


def print_conditions() -> None:
    print("Operational conditions for ignoring cells/spectators:")
    print(
        "  Cells/spectators can be ignored only for preparation, readout, Bell "
        "measurement, and correction operators proved to be O_logical tensor I_env, "
        "or for an apparatus proven blind to env labels within the target tolerance."
    )
    print(
        "  A fixed-cell/fixed-spectator restriction is not enough for the traced "
        "logical protocol; it is an environment-selected branch unless a heralding "
        "workflow and branch-conditioned operations are supplied."
    )
    print(
        "  In dim > 1, sublattice parity Z is xi_5 and contains spectator taste "
        "signs, so it is not a retained-bit-only logical Z. Use an axis logical Z "
        "for taste-only readout/correction."
    )
    print(
        "  Bob pre-message input-independence is a separate no-signaling check. "
        "It does not imply Bob's marginal is I/2 and does not establish native "
        "readout operationality."
    )
    print(
        "  Claim boundary: ordinary quantum state teleportation planning only; no "
        "matter, mass, charge, energy, object, or faster-than-light transport."
    )


def expected_single_pass(case: CaseAudit, audit: OperatorAudit) -> bool:
    always_pass = {
        "axis logical Z",
        "axis-adapted X",
        "fixed pair-hop X",
        "axis Z then axis X",
        "axis Z+ projector",
        "axis X+ projector",
    }
    dim_one_only = {
        "native sublattice Z",
        "native Z then fixed X",
        "native Z+ projector",
    }
    env_trivial_only = {
        "fixed site projector",
        "fixed env projector",
    }
    if audit.name in always_pass:
        return True
    if audit.name in dim_one_only:
        return case.dim == 1
    if audit.name in env_trivial_only:
        return case.n_env == 1
    raise ValueError(f"missing expected-pass rule for {audit.name}")


def expected_pair_pass(case: CaseAudit, audit: PairOperatorAudit) -> bool:
    always_pass = {
        "axis Bell Phi+ projector",
        "fixed XX stabilizer",
    }
    dim_one_only = {
        "native-Z/fixed-X Bell Phi+ projector",
        "native ZZ stabilizer",
    }
    if audit.name in always_pass:
        return True
    if audit.name in dim_one_only:
        return case.dim == 1
    raise ValueError(f"missing expected-pass rule for {audit.name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dims",
        type=int,
        nargs="+",
        default=[1, 2, 3],
        help="spatial dimensions to audit",
    )
    parser.add_argument(
        "--sides",
        type=int,
        nargs="+",
        default=[2, 4],
        help="even side lengths to audit",
    )
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument(
        "--random-inputs",
        type=int,
        default=16,
        help="random inputs for Bob no-message separation check",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1e-12,
        help="operator factorization tolerance",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.tolerance <= 0.0:
        raise ValueError("--tolerance must be positive")
    if args.random_inputs < 0:
        raise ValueError("--random-inputs must be nonnegative")
    for side in args.sides:
        if side <= 0 or side % 2 != 0:
            raise ValueError("--sides must contain positive even lengths")
    for dim in args.dims:
        if dim not in (1, 2, 3):
            raise ValueError("--dims supports only 1, 2, and 3")

    print("TELEPORTATION TASTE READOUT/OPERATOR MODEL")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(
        "Criterion: native operator must factor as O_logical tensor I_env for "
        "the retained last KS taste bit"
    )
    print(
        "Audit grid: "
        f"dims={','.join(str(dim) for dim in args.dims)} "
        f"sides={','.join(str(side) for side in args.sides)} "
        f"tolerance={args.tolerance:.1e}"
    )
    print()

    cases = [
        audit_case(dim=dim, side=side, tolerance=args.tolerance)
        for dim in args.dims
        for side in args.sides
    ]
    for case in cases:
        print_case(case, tolerance=args.tolerance)

    no_message = no_message_audit(args.seed, args.random_inputs)
    print("Bob pre-message separation check:")
    print(
        f"  probes={no_message.probe_count}, "
        f"Bob marginal bias from I/2={fmt_float(no_message.bob_marginal_bias)}, "
        f"max no-record to Bob marginal={fmt_float(no_message.max_no_record_to_marginal)}, "
        f"max pairwise no-record input distance="
        f"{fmt_float(no_message.max_pairwise_no_record_distance)}, "
        f"max branch probability span={fmt_float(no_message.max_branch_probability_span)}"
    )
    print(f"  note: {no_message.note}")
    print()
    print_conditions()

    unexpected: list[str] = []
    for case in cases:
        for audit in case.single_register:
            expected = expected_single_pass(case, audit)
            if audit.passes != expected:
                unexpected.append(
                    f"dim={case.dim} side={case.side} {audit.name}: "
                    f"expected {'PASS' if expected else 'FAIL'}, got "
                    f"{'PASS' if audit.passes else 'FAIL'}"
                )
        for audit in case.pair_register:
            expected = expected_pair_pass(case, audit)
            if audit.passes != expected:
                unexpected.append(
                    f"dim={case.dim} side={case.side} {audit.name}: "
                    f"expected {'PASS' if expected else 'FAIL'}, got "
                    f"{'PASS' if audit.passes else 'FAIL'}"
                )

    if unexpected:
        print()
        print("Unexpected classifications:")
        for item in unexpected:
            print(f"  {item}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
