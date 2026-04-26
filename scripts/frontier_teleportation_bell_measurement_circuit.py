#!/usr/bin/env python3
"""Bell-measurement circuit/decomposition for taste-qubit teleportation.

Status: planning / first artifact. This runner stays inside ordinary quantum
state teleportation on encoded taste qubits. It does not claim matter
teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.

The artifact decomposes the ideal Bell projectors already used by the
teleportation protocol,

    P_zx = 1/4 (I + (-1)^x Z_A Z_R) (I + (-1)^z X_A X_R),

into two equivalent ideal logical/taste measurement forms:

1. Direct commuting taste-stabilizer measurements of Z_A Z_R and X_A X_R.
2. A logical Bell-measurement circuit: CNOT(A -> R), H(A), then Z-basis
   measurements on A and R. The computational output bits are (z, x).

The construction assumes ideal logical/taste gates or ideal logical/taste
stabilizer measurements. It does not derive an apparatus Hamiltonian,
measurement durability, or a native physical implementation of those gates.
"""

from __future__ import annotations

import argparse
import itertools
import math
import sys
from typing import Iterable

import numpy as np


I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)
H2 = (1.0 / math.sqrt(2.0)) * np.array([[1, 1], [1, -1]], dtype=complex)

OUTCOME_ORDER = ((0, 0), (1, 0), (0, 1), (1, 1))
OUTCOME_LABELS = {
    (0, 0): "Phi+",
    (1, 0): "Phi-",
    (0, 1): "Psi+",
    (1, 1): "Psi-",
}


def coordinate_index(coords: tuple[int, ...], side: int) -> int:
    """Row-major lattice index matching the retained teleportation artifacts."""
    index = 0
    for coord in coords:
        index = index * side + coord
    return index


def build_cell_taste_operator(
    dim: int, side: int, taste_paulis: Iterable[np.ndarray]
) -> np.ndarray:
    """Build I_cells tensor taste_operator in the site basis.

    Site coordinates decompose as x_mu = 2 X_mu + eta_mu, with eta_mu in
    {0, 1}. This is the explicit Kogut-Susskind cell/taste factorization used
    by the prior taste-qubit teleportation runners.
    """
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


def encoded_taste_indices(
    dim: int = 3,
    side: int = 4,
    cell: tuple[int, int, int] = (0, 0, 0),
    logical_axis: int = 2,
) -> tuple[int, int]:
    """Return site indices for |0_L>, |1_L> in one fixed taste axis."""
    indices: list[int] = []
    for bit in (0, 1):
        eta = [0] * dim
        eta[logical_axis] = bit
        coords = tuple(2 * cell[axis] + eta[axis] for axis in range(dim))
        indices.append(coordinate_index(coords, side))
    return indices[0], indices[1]


def restrict_to_encoded_qubit(op: np.ndarray, indices: tuple[int, int]) -> np.ndarray:
    return op[np.ix_(indices, indices)]


def density(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    state = rng.standard_normal(2) + 1j * rng.standard_normal(2)
    return normalize(state)


def bell_state(z_bit: int, x_bit: int) -> np.ndarray:
    """Bell state |Bell(z,x)> with x=bit-flip and z=phase bit."""
    sign = -1.0 if z_bit else 1.0
    state = np.zeros(4, dtype=complex)
    if x_bit == 0:
        state[0] = 1.0 / math.sqrt(2.0)
        state[3] = sign / math.sqrt(2.0)
    else:
        state[1] = 1.0 / math.sqrt(2.0)
        state[2] = sign / math.sqrt(2.0)
    return state


def bell_projector(z_bit: int, x_bit: int) -> np.ndarray:
    """Bell projector using the protocol's stabilizer convention."""
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    identity = np.eye(4, dtype=complex)
    return 0.25 * (identity + ((-1) ** x_bit) * zz) @ (
        identity + ((-1) ** z_bit) * xx
    )


def cnot_control_first() -> np.ndarray:
    """Two-qubit CNOT with the first qubit as control in |00>,|01>,|10>,|11>."""
    gate = np.zeros((4, 4), dtype=complex)
    for control in (0, 1):
        for target in (0, 1):
            source_index = 2 * control + target
            target_index = 2 * control + (target ^ control)
            gate[target_index, source_index] = 1.0
    return gate


def bell_measurement_unitary() -> np.ndarray:
    """CNOT(A -> R), then H(A), before computational Z-basis measurement."""
    return np.kron(H2, I2) @ cnot_control_first()


def computational_projector(z_bit: int, x_bit: int) -> np.ndarray:
    projector = np.zeros((4, 4), dtype=complex)
    projector[2 * z_bit + x_bit, 2 * z_bit + x_bit] = 1.0
    return projector


def circuit_projector(z_bit: int, x_bit: int) -> np.ndarray:
    """Heisenberg pullback of output |z,x> measurement to Bell input space."""
    unitary = bell_measurement_unitary()
    return unitary.conj().T @ computational_projector(z_bit, x_bit) @ unitary


def native_taste_measurement_check() -> dict[str, object]:
    dim = 3
    side = 4
    xi5 = build_cell_taste_operator(dim, side, [Z2, Z2, Z2])
    xi_last = build_cell_taste_operator(dim, side, [I2, I2, X2])
    site_z = build_sublattice_z(dim, side)
    site_x = build_pair_hop_x(dim, side)
    indices = encoded_taste_indices(dim=dim, side=side)

    z_logical = restrict_to_encoded_qubit(site_z, indices)
    x_logical = restrict_to_encoded_qubit(site_x, indices)
    identity = np.eye(4, dtype=complex)

    max_native_projector_error = 0.0
    for z_bit, x_bit in OUTCOME_ORDER:
        native_projector = 0.25 * (
            identity + ((-1) ** x_bit) * np.kron(z_logical, z_logical)
        ) @ (identity + ((-1) ** z_bit) * np.kron(x_logical, x_logical))
        max_native_projector_error = max(
            max_native_projector_error,
            float(np.max(np.abs(native_projector - bell_projector(z_bit, x_bit)))),
        )

    p0_from_z = 0.5 * (I2 + z_logical)
    p1_from_z = 0.5 * (I2 - z_logical)
    p0 = np.array([[1, 0], [0, 0]], dtype=complex)
    p1 = np.array([[0, 0], [0, 1]], dtype=complex)

    return {
        "dim": dim,
        "side": side,
        "indices": indices,
        "site_z_matches_xi5": bool(np.allclose(site_z, xi5, atol=1e-12)),
        "site_x_matches_xi_last": bool(np.allclose(site_x, xi_last, atol=1e-12)),
        "z_restricts_to_pauli": bool(np.allclose(z_logical, Z2, atol=1e-12)),
        "x_restricts_to_pauli": bool(np.allclose(x_logical, X2, atol=1e-12)),
        "anticommutator_norm": float(np.linalg.norm(z_logical @ x_logical + x_logical @ z_logical)),
        "computational_z_readout_error": float(
            max(np.max(np.abs(p0_from_z - p0)), np.max(np.abs(p1_from_z - p1)))
        ),
        "native_stabilizer_projector_error": max_native_projector_error,
    }


def verify_stabilizer_projectors() -> dict[str, float]:
    identity = np.eye(4, dtype=complex)
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    projectors = [bell_projector(z, x) for z, x in OUTCOME_ORDER]

    resolution_error = float(np.max(np.abs(sum(projectors) - identity)))
    orthogonality_error = 0.0
    idempotence_error = 0.0
    state_projector_error = 0.0
    stabilizer_eigen_error = 0.0

    for i, projector in enumerate(projectors):
        z_bit, x_bit = OUTCOME_ORDER[i]
        state = bell_state(z_bit, x_bit)
        idempotence_error = max(
            idempotence_error, float(np.max(np.abs(projector @ projector - projector)))
        )
        state_projector_error = max(
            state_projector_error,
            float(np.max(np.abs(projector - density(state)))),
        )
        stabilizer_eigen_error = max(
            stabilizer_eigen_error,
            float(np.linalg.norm((zz - ((-1) ** x_bit) * identity) @ state)),
            float(np.linalg.norm((xx - ((-1) ** z_bit) * identity) @ state)),
        )
        for j, other in enumerate(projectors):
            if i == j:
                continue
            orthogonality_error = max(
                orthogonality_error, float(np.max(np.abs(projector @ other)))
            )

    return {
        "resolution_error": resolution_error,
        "orthogonality_error": orthogonality_error,
        "idempotence_error": idempotence_error,
        "state_projector_error": state_projector_error,
        "stabilizer_eigen_error": stabilizer_eigen_error,
    }


def verify_circuit_decomposition() -> dict[str, object]:
    unitary = bell_measurement_unitary()
    identity = np.eye(4, dtype=complex)
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    z_first = np.kron(Z2, I2)
    z_second = np.kron(I2, Z2)

    phase_observable = unitary.conj().T @ z_first @ unitary
    flip_observable = unitary.conj().T @ z_second @ unitary

    max_projector_error = 0.0
    max_record_wrong_probability = 0.0
    min_record_right_probability = 1.0
    record_map: dict[str, tuple[int, int]] = {}
    for z_bit, x_bit in OUTCOME_ORDER:
        pulled_back = circuit_projector(z_bit, x_bit)
        max_projector_error = max(
            max_projector_error,
            float(np.max(np.abs(pulled_back - bell_projector(z_bit, x_bit)))),
        )

        transformed = unitary @ bell_state(z_bit, x_bit)
        probabilities = np.abs(transformed) ** 2
        target_index = 2 * z_bit + x_bit
        min_record_right_probability = min(
            min_record_right_probability, float(probabilities[target_index])
        )
        wrong_probability = float(np.sum(probabilities) - probabilities[target_index])
        max_record_wrong_probability = max(max_record_wrong_probability, wrong_probability)
        record_map[OUTCOME_LABELS[(z_bit, x_bit)]] = (z_bit, x_bit)

    unitarity_error = float(np.max(np.abs(unitary.conj().T @ unitary - identity)))
    return {
        "unitarity_error": unitarity_error,
        "phase_observable_xx_error": float(np.max(np.abs(phase_observable - xx))),
        "flip_observable_zz_error": float(np.max(np.abs(flip_observable - zz))),
        "max_circuit_projector_error": max_projector_error,
        "min_record_right_probability": min_record_right_probability,
        "max_record_wrong_probability": max_record_wrong_probability,
        "record_map": record_map,
    }


def prepare_three_register_state(input_state: np.ndarray) -> np.ndarray:
    """Prepare |psi>_A tensor |Phi+>_RB in A,R,B register order."""
    return np.kron(input_state, bell_state(0, 0))


def bob_reduced_from_three_register_state(state: np.ndarray) -> np.ndarray:
    amplitudes = state.reshape(4, 2)
    return amplitudes.T @ amplitudes.conj()


def branch_from_circuit_projector(
    state: np.ndarray, z_bit: int, x_bit: int
) -> tuple[float, np.ndarray]:
    """Project A,R with the circuit-derived Bell projector and return Bob rho."""
    ar_by_b = state.reshape(4, 2)
    branch = circuit_projector(z_bit, x_bit) @ ar_by_b
    probability = float(np.real(np.vdot(branch, branch)))
    if probability <= 1e-15:
        raise ValueError("Bell outcome has zero probability")
    bob_rho = branch.T @ branch.conj() / probability
    return probability, bob_rho


def correction_operator(z_bit: int, x_bit: int) -> np.ndarray:
    z_op = Z2 if z_bit else I2
    x_op = X2 if x_bit else I2
    return z_op @ x_op


def pure_state_fidelity(state: np.ndarray, rho: np.ndarray) -> float:
    state = normalize(state)
    return float(np.real(np.vdot(state, rho @ state)))


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def run_circuit_teleportation_trials(n_trials: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    half_identity = 0.5 * I2
    reference_pre_message_rho: np.ndarray | None = None

    outcomes_seen: set[tuple[int, int]] = set()
    max_probability_error = 0.0
    max_bob_before_trace_distance = 0.0
    max_bob_pre_message_trace_distance = 0.0
    max_pairwise_pre_message_distance = 0.0
    min_corrected_fidelity = 1.0
    max_corrected_infidelity = 0.0
    max_corrected_trace_distance = 0.0

    for _ in range(n_trials):
        input_state = random_qubit(rng)
        input_rho = density(input_state)
        state = prepare_three_register_state(input_state)

        bob_before = bob_reduced_from_three_register_state(state)
        max_bob_before_trace_distance = max(
            max_bob_before_trace_distance,
            trace_distance(bob_before, half_identity),
        )

        pre_message_rho = np.zeros((2, 2), dtype=complex)
        for z_bit, x_bit in OUTCOME_ORDER:
            probability, bob_rho = branch_from_circuit_projector(state, z_bit, x_bit)
            outcomes_seen.add((z_bit, x_bit))
            max_probability_error = max(max_probability_error, abs(probability - 0.25))
            pre_message_rho += probability * bob_rho

            correction = correction_operator(z_bit, x_bit)
            corrected_rho = correction @ bob_rho @ correction.conj().T
            fidelity = pure_state_fidelity(input_state, corrected_rho)
            min_corrected_fidelity = min(min_corrected_fidelity, fidelity)
            max_corrected_infidelity = max(max_corrected_infidelity, 1.0 - fidelity)
            max_corrected_trace_distance = max(
                max_corrected_trace_distance,
                trace_distance(corrected_rho, input_rho),
            )

        max_bob_pre_message_trace_distance = max(
            max_bob_pre_message_trace_distance,
            trace_distance(pre_message_rho, half_identity),
        )
        if reference_pre_message_rho is None:
            reference_pre_message_rho = pre_message_rho
        else:
            max_pairwise_pre_message_distance = max(
                max_pairwise_pre_message_distance,
                trace_distance(pre_message_rho, reference_pre_message_rho),
            )

    return {
        "n_trials": n_trials,
        "seed": seed,
        "outcomes_seen": sorted(OUTCOME_LABELS[outcome] for outcome in outcomes_seen),
        "max_probability_error": max_probability_error,
        "max_bob_before_trace_distance": max_bob_before_trace_distance,
        "max_bob_pre_message_trace_distance": max_bob_pre_message_trace_distance,
        "max_pairwise_pre_message_distance": max_pairwise_pre_message_distance,
        "min_corrected_fidelity": min_corrected_fidelity,
        "max_corrected_infidelity": max_corrected_infidelity,
        "max_corrected_trace_distance": max_corrected_trace_distance,
    }


def print_summary(
    native: dict[str, object],
    projectors: dict[str, float],
    circuit: dict[str, object],
    trials: dict[str, object],
    tolerance: float,
) -> bool:
    print("TELEPORTATION BELL-MEASUREMENT CIRCUIT/DECOMPOSITION")
    print("Status: planning / ideal logical taste-measurement artifact")
    print()

    print("Native logical taste surface:")
    print(f"  lattice: {native['dim']}D side={native['side']}")
    print(f"  encoded site indices |0_L>, |1_L>: {native['indices']}")
    print(f"  site Z == I_cells tensor xi_5: {native['site_z_matches_xi5']}")
    print(f"  site X == I_cells tensor xi_last: {native['site_x_matches_xi_last']}")
    print(f"  restricted Z_L is Pauli Z: {native['z_restricts_to_pauli']}")
    print(f"  restricted X_L is Pauli X: {native['x_restricts_to_pauli']}")
    print(f"  restricted anticommutator norm: {native['anticommutator_norm']:.3e}")
    print(
        "  computational taste-Z readout projector error: "
        f"{native['computational_z_readout_error']:.3e}"
    )
    print(
        "  native ZZ/XX stabilizer projector error vs ideal P_zx: "
        f"{native['native_stabilizer_projector_error']:.3e}"
    )
    print()

    print("Stabilizer Bell projectors:")
    print("  P_zx = 1/4 (I + (-1)^x Z_A Z_R)(I + (-1)^z X_A X_R)")
    print(f"  resolution error: {projectors['resolution_error']:.3e}")
    print(f"  orthogonality error: {projectors['orthogonality_error']:.3e}")
    print(f"  idempotence error: {projectors['idempotence_error']:.3e}")
    print(f"  Bell-state outer-product error: {projectors['state_projector_error']:.3e}")
    print(f"  Bell-state stabilizer eigenvalue error: {projectors['stabilizer_eigen_error']:.3e}")
    print()

    print("Logical circuit decomposition:")
    print("  circuit: CNOT(A -> R), H(A), computational Z-basis measurement")
    print("  output bit on A is z (XX phase record); output bit on R is x (ZZ flip record)")
    print(f"  circuit unitarity error: {circuit['unitarity_error']:.3e}")
    print(
        "  pulled-back first output Z observable error vs X_A X_R: "
        f"{circuit['phase_observable_xx_error']:.3e}"
    )
    print(
        "  pulled-back second output Z observable error vs Z_A Z_R: "
        f"{circuit['flip_observable_zz_error']:.3e}"
    )
    print(
        "  max circuit measurement projector error vs P_zx: "
        f"{circuit['max_circuit_projector_error']:.3e}"
    )
    print(
        "  Bell input -> computational record min right probability: "
        f"{circuit['min_record_right_probability']:.16f}"
    )
    print(
        "  Bell input -> computational record max wrong probability: "
        f"{circuit['max_record_wrong_probability']:.3e}"
    )
    for label, bits in circuit["record_map"].items():
        print(f"  {label} -> bits(z,x)={bits}")
    print()

    print("Teleportation trials using circuit-derived Bell measurement:")
    print(f"  random input states: {trials['n_trials']} (seed={trials['seed']})")
    print(f"  Bell outcomes exercised: {', '.join(trials['outcomes_seen'])}")
    print(f"  max Bell probability error from 1/4: {trials['max_probability_error']:.3e}")
    print(f"  minimum corrected fidelity: {trials['min_corrected_fidelity']:.16f}")
    print(f"  maximum corrected infidelity: {trials['max_corrected_infidelity']:.3e}")
    print(
        "  max corrected-state trace distance to input: "
        f"{trials['max_corrected_trace_distance']:.3e}"
    )
    print(
        "  max Bob trace distance to I/2 before Alice measurement: "
        f"{trials['max_bob_before_trace_distance']:.3e}"
    )
    print(
        "  max Bob trace distance to I/2 after Alice measurement but before message: "
        f"{trials['max_bob_pre_message_trace_distance']:.3e}"
    )
    print(
        "  max pairwise pre-message Bob-state distance across inputs: "
        f"{trials['max_pairwise_pre_message_distance']:.3e}"
    )
    print()

    pass_checks = {
        "native taste logical Pauli surface": bool(
            native["site_z_matches_xi5"]
            and native["site_x_matches_xi_last"]
            and native["z_restricts_to_pauli"]
            and native["x_restricts_to_pauli"]
            and native["anticommutator_norm"] < tolerance
            and native["computational_z_readout_error"] < tolerance
            and native["native_stabilizer_projector_error"] < tolerance
        ),
        "stabilizer Bell projectors": bool(
            projectors["resolution_error"] < tolerance
            and projectors["orthogonality_error"] < tolerance
            and projectors["idempotence_error"] < tolerance
            and projectors["state_projector_error"] < tolerance
            and projectors["stabilizer_eigen_error"] < tolerance
        ),
        "CNOT-H circuit decomposition": bool(
            circuit["unitarity_error"] < tolerance
            and circuit["phase_observable_xx_error"] < tolerance
            and circuit["flip_observable_zz_error"] < tolerance
            and circuit["max_circuit_projector_error"] < tolerance
            and 1.0 - circuit["min_record_right_probability"] < tolerance
            and circuit["max_record_wrong_probability"] < tolerance
        ),
        "all Bell outcomes": set(trials["outcomes_seen"])
        == {OUTCOME_LABELS[outcome] for outcome in OUTCOME_ORDER},
        "random-state correction fidelity": bool(
            trials["max_corrected_infidelity"] < tolerance
            and trials["max_corrected_trace_distance"] < tolerance
        ),
        "Bob pre-message input-independence": bool(
            trials["max_bob_before_trace_distance"] < tolerance
            and trials["max_bob_pre_message_trace_distance"] < tolerance
            and trials["max_pairwise_pre_message_distance"] < tolerance
        ),
    }

    print("Acceptance gates:")
    for name, ok in pass_checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()

    print("Physical assumptions left open:")
    print("  ideal encoded Bell resource is supplied")
    print("  ideal logical taste CNOT/H gates or ideal ZZ/XX stabilizer measurements are supplied")
    print("  ideal taste computational-basis readout and classical record handling are supplied")
    print("  no apparatus Hamiltonian, decoherence, or durable-record derivation is supplied")
    print("  no matter, mass, charge, energy, object transport, or FTL signaling is claimed")

    return all(pass_checks.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=64, help="number of random input states")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--tolerance", type=float, default=1e-12, help="pass/fail tolerance")
    args = parser.parse_args()

    if args.trials <= 0:
        raise ValueError("--trials must be positive")

    native = native_taste_measurement_check()
    projectors = verify_stabilizer_projectors()
    circuit = verify_circuit_decomposition()
    trials = run_circuit_teleportation_trials(args.trials, args.seed)

    ok = print_summary(native, projectors, circuit, trials, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
