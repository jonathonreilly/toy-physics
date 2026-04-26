#!/usr/bin/env python3
"""Native taste-qubit teleportation first artifact.

Status: planning / first artifact. This runner tests ordinary quantum state
teleportation on an encoded Kogut-Susskind taste qubit. It does not claim
matter teleportation, mass transfer, charge transfer, or faster-than-light
transport.

The native hook is the same taste surface used by the retained CHSH lane:

    single-particle C^N = C^{N_cells} tensor C^{2^d}
    Z = I_cells tensor xi_5
    X = I_cells tensor xi_last

Here one logical qubit is encoded by fixing one 3D cell and the two spectator
taste bits, then using the last taste bit as |0_L>, |1_L>. The script verifies
that the restricted site-basis taste operators act as Pauli Z and X on this
logical subspace, builds Bell projectors from ZZ and XX stabilizers, and tests
the four-outcome teleportation protocol with an explicit delayed two-bit
classical record channel.
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
class ClassicalRecord:
    """Causal two-bit Bell-measurement record."""

    sender: str
    receiver: str
    created_at_tick: int
    deliver_at_tick: int
    z_bit: int
    x_bit: int
    basis: str = "taste Bell basis"

    @property
    def label(self) -> str:
        return OUTCOME_LABELS[(self.z_bit, self.x_bit)]


class CausalTwoBitChannel:
    """Minimal causal record channel with positive integer latency."""

    def __init__(self, latency_ticks: int) -> None:
        if latency_ticks <= 0:
            raise ValueError("latency_ticks must be positive")
        self.latency_ticks = latency_ticks
        self.current_tick = 0
        self._in_flight: list[ClassicalRecord] = []

    def advance_to(self, tick: int) -> None:
        if tick < self.current_tick:
            raise ValueError("channel time cannot run backward")
        self.current_tick = tick

    def send(self, sender: str, receiver: str, z_bit: int, x_bit: int) -> ClassicalRecord:
        if z_bit not in (0, 1) or x_bit not in (0, 1):
            raise ValueError("Bell record bits must be binary")
        record = ClassicalRecord(
            sender=sender,
            receiver=receiver,
            created_at_tick=self.current_tick,
            deliver_at_tick=self.current_tick + self.latency_ticks,
            z_bit=z_bit,
            x_bit=x_bit,
        )
        self._in_flight.append(record)
        return record

    def receive(self, receiver: str) -> list[ClassicalRecord]:
        delivered = [
            record
            for record in self._in_flight
            if record.receiver == receiver and record.deliver_at_tick <= self.current_tick
        ]
        self._in_flight = [record for record in self._in_flight if record not in delivered]
        return delivered

    def pending_count(self) -> int:
        return len(self._in_flight)


def coordinate_index(coords: tuple[int, ...], side: int) -> int:
    """Row-major lattice index matching the CHSH lane conventions."""
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
    by the CHSH lane.
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


def native_taste_encoding_check() -> dict[str, object]:
    dim = 3
    side = 4
    sigma_z = Z2
    sigma_x = X2

    xi5 = build_cell_taste_operator(dim, side, [sigma_z, sigma_z, sigma_z])
    xi_last = build_cell_taste_operator(dim, side, [I2, I2, sigma_x])
    site_z = build_sublattice_z(dim, side)
    site_x = build_pair_hop_x(dim, side)

    indices = encoded_taste_indices(dim=dim, side=side)
    z_logical = restrict_to_encoded_qubit(site_z, indices)
    x_logical = restrict_to_encoded_qubit(site_x, indices)

    return {
        "dim": dim,
        "side": side,
        "indices": indices,
        "site_z_matches_xi5": bool(np.allclose(site_z, xi5, atol=1e-12)),
        "site_x_matches_xi_last": bool(np.allclose(site_x, xi_last, atol=1e-12)),
        "z_restricts_to_pauli": bool(np.allclose(z_logical, Z2, atol=1e-12)),
        "x_restricts_to_pauli": bool(np.allclose(x_logical, X2, atol=1e-12)),
        "anticommutator_norm": float(np.linalg.norm(z_logical @ x_logical + x_logical @ z_logical)),
    }


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
    """Bell projector built from taste Pauli stabilizers ZZ and XX."""
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    identity = np.eye(4, dtype=complex)
    return 0.25 * (identity + ((-1) ** x_bit) * zz) @ (
        identity + ((-1) ** z_bit) * xx
    )


def verify_bell_projectors() -> dict[str, object]:
    identity = np.eye(4, dtype=complex)
    projectors = [bell_projector(z, x) for z, x in OUTCOME_ORDER]
    max_idempotence_error = max(
        float(np.max(np.abs(projector @ projector - projector))) for projector in projectors
    )
    max_state_projector_error = max(
        float(
            np.max(
                np.abs(
                    bell_projector(z, x)
                    - np.outer(bell_state(z, x), bell_state(z, x).conj())
                )
            )
        )
        for z, x in OUTCOME_ORDER
    )
    resolution_error = float(np.max(np.abs(sum(projectors) - identity)))
    orthogonality_error = 0.0
    for i, first in enumerate(projectors):
        for j, second in enumerate(projectors):
            if i == j:
                continue
            orthogonality_error = max(
                orthogonality_error, float(np.max(np.abs(first @ second)))
            )

    return {
        "max_idempotence_error": max_idempotence_error,
        "max_state_projector_error": max_state_projector_error,
        "resolution_error": resolution_error,
        "orthogonality_error": orthogonality_error,
    }


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    state = rng.standard_normal(2) + 1j * rng.standard_normal(2)
    return normalize(state)


def prepare_three_register_state(input_state: np.ndarray) -> np.ndarray:
    """Prepare |psi>_A tensor |Phi+>_R,Bob in A,R,B register order."""
    return np.kron(input_state, bell_state(0, 0))


def bob_reduced_from_three_register_state(state: np.ndarray) -> np.ndarray:
    """Trace out Alice's two registers from a pure A,R,B state."""
    amplitudes = state.reshape(4, 2)
    return amplitudes.conj().T @ amplitudes


def project_bell_branch(
    state: np.ndarray, z_bit: int, x_bit: int
) -> tuple[float, np.ndarray, np.ndarray]:
    """Project Alice's A,R registers and return Bob probability/state/rho."""
    amplitudes = state.reshape(2, 2, 2)
    bell = bell_state(z_bit, x_bit).reshape(2, 2)
    bob_unnormalized = np.tensordot(bell.conj(), amplitudes, axes=([0, 1], [0, 1]))
    probability = float(np.real(np.vdot(bob_unnormalized, bob_unnormalized)))
    if probability <= 1e-15:
        raise ValueError("Bell outcome has zero probability")
    bob_state = bob_unnormalized / math.sqrt(probability)
    bob_rho = np.outer(bob_state, bob_state.conj())
    return probability, bob_state, bob_rho


def correction_operator(z_bit: int, x_bit: int) -> np.ndarray:
    z_op = Z2 if z_bit else I2
    x_op = X2 if x_bit else I2
    return z_op @ x_op


def state_fidelity(first: np.ndarray, second: np.ndarray) -> float:
    first = normalize(first)
    second = normalize(second)
    return float(abs(np.vdot(first, second)) ** 2)


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def run_random_teleportation_trials(n_trials: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    half_identity = 0.5 * I2
    outcomes_seen: set[tuple[int, int]] = set()
    min_fidelity = 1.0
    max_infidelity = 0.0
    max_probability_error = 0.0
    max_pre_measurement_trace_distance = 0.0
    max_post_measurement_trace_distance = 0.0
    max_pairwise_pre_message_distance = 0.0
    reference_pre_message_rho: np.ndarray | None = None

    for _ in range(n_trials):
        input_state = random_qubit(rng)
        three_register_state = prepare_three_register_state(input_state)

        rho_before_measurement = bob_reduced_from_three_register_state(three_register_state)
        max_pre_measurement_trace_distance = max(
            max_pre_measurement_trace_distance,
            trace_distance(rho_before_measurement, half_identity),
        )

        pre_message_rho = np.zeros((2, 2), dtype=complex)
        for z_bit, x_bit in OUTCOME_ORDER:
            probability, bob_state, bob_rho = project_bell_branch(
                three_register_state, z_bit, x_bit
            )
            outcomes_seen.add((z_bit, x_bit))
            max_probability_error = max(max_probability_error, abs(probability - 0.25))
            pre_message_rho += probability * bob_rho

            corrected = correction_operator(z_bit, x_bit) @ bob_state
            fidelity = state_fidelity(input_state, corrected)
            min_fidelity = min(min_fidelity, fidelity)
            max_infidelity = max(max_infidelity, 1.0 - fidelity)

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

    return {
        "n_trials": n_trials,
        "seed": seed,
        "outcomes_seen": sorted(OUTCOME_LABELS[outcome] for outcome in outcomes_seen),
        "min_fidelity": min_fidelity,
        "max_infidelity": max_infidelity,
        "max_probability_error": max_probability_error,
        "max_pre_measurement_trace_distance": max_pre_measurement_trace_distance,
        "max_post_measurement_trace_distance": max_post_measurement_trace_distance,
        "max_pairwise_pre_message_distance": max_pairwise_pre_message_distance,
    }


def run_causal_channel_demo(seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    input_state = random_qubit(rng)
    state = prepare_three_register_state(input_state)
    z_bit, x_bit = 1, 1
    probability, bob_state, _ = project_bell_branch(state, z_bit, x_bit)

    channel = CausalTwoBitChannel(latency_ticks=3)
    channel.advance_to(10)
    sent = channel.send("Alice", "Bob", z_bit=z_bit, x_bit=x_bit)

    channel.advance_to(12)
    pre_delivery_records = channel.receive("Bob")
    pre_delivery_blocked = len(pre_delivery_records) == 0 and channel.pending_count() == 1

    channel.advance_to(13)
    delivered_records = channel.receive("Bob")
    delivered_once = len(delivered_records) == 1 and channel.pending_count() == 0
    delivered = delivered_records[0] if delivered_records else sent
    corrected = correction_operator(delivered.z_bit, delivered.x_bit) @ bob_state

    return {
        "latency_ticks": channel.latency_ticks,
        "created_at_tick": sent.created_at_tick,
        "pre_delivery_tick": 12,
        "deliver_at_tick": sent.deliver_at_tick,
        "pre_delivery_blocked": pre_delivery_blocked,
        "delivered_once": delivered_once,
        "record_label": delivered.label,
        "record_bits": (delivered.z_bit, delivered.x_bit),
        "branch_probability": probability,
        "post_delivery_fidelity": state_fidelity(input_state, corrected),
    }


def print_summary(
    encoding: dict[str, object],
    projectors: dict[str, object],
    trials: dict[str, object],
    channel: dict[str, object],
    tolerance: float,
) -> bool:
    print("NATIVE TASTE-QUBIT TELEPORTATION FIRST ARTIFACT")
    print("Status: planning / first artifact; quantum state teleportation only")
    print()

    print("Native KS taste encoding:")
    print(f"  lattice: {encoding['dim']}D side={encoding['side']}")
    print(f"  encoded site indices |0_L>, |1_L>: {encoding['indices']}")
    print(f"  site Z == I_cells tensor xi_5: {encoding['site_z_matches_xi5']}")
    print(f"  site X == I_cells tensor xi_last: {encoding['site_x_matches_xi_last']}")
    print(f"  restricted Z is Pauli Z: {encoding['z_restricts_to_pauli']}")
    print(f"  restricted X is Pauli X: {encoding['x_restricts_to_pauli']}")
    print(f"  restricted anticommutator norm: {encoding['anticommutator_norm']:.3e}")
    print()

    print("Bell projectors from taste Pauli stabilizers:")
    print(f"  resolution error: {projectors['resolution_error']:.3e}")
    print(f"  orthogonality error: {projectors['orthogonality_error']:.3e}")
    print(f"  idempotence error: {projectors['max_idempotence_error']:.3e}")
    print(f"  state-projector error: {projectors['max_state_projector_error']:.3e}")
    print()

    print("Teleportation trials:")
    print(f"  random trials: {trials['n_trials']} (seed={trials['seed']})")
    print(f"  Bell outcomes exercised: {', '.join(trials['outcomes_seen'])}")
    print(f"  minimum corrected-state fidelity: {trials['min_fidelity']:.16f}")
    print(f"  maximum infidelity: {trials['max_infidelity']:.3e}")
    print(f"  max Bell probability error from 1/4: {trials['max_probability_error']:.3e}")
    print(
        "  max Bob trace distance to I/2 before Alice measurement: "
        f"{trials['max_pre_measurement_trace_distance']:.3e}"
    )
    print(
        "  max Bob trace distance to I/2 after Alice measurement but before message: "
        f"{trials['max_post_measurement_trace_distance']:.3e}"
    )
    print(
        "  max pairwise pre-message Bob-state distance across inputs: "
        f"{trials['max_pairwise_pre_message_distance']:.3e}"
    )
    print()

    print("Causal two-bit record channel:")
    print(
        "  record: "
        f"{channel['record_label']} bits(z,x)={channel['record_bits']} "
        f"created t={channel['created_at_tick']} deliver t={channel['deliver_at_tick']}"
    )
    print(
        f"  receive at t={channel['pre_delivery_tick']} blocked: "
        f"{channel['pre_delivery_blocked']}"
    )
    print(f"  receive at delivery tick exactly once: {channel['delivered_once']}")
    print(f"  post-delivery correction fidelity: {channel['post_delivery_fidelity']:.16f}")
    print()

    pass_checks = {
        "native taste encoding": bool(
            encoding["site_z_matches_xi5"]
            and encoding["site_x_matches_xi_last"]
            and encoding["z_restricts_to_pauli"]
            and encoding["x_restricts_to_pauli"]
            and encoding["anticommutator_norm"] < tolerance
        ),
        "Bell projectors": bool(
            projectors["resolution_error"] < tolerance
            and projectors["orthogonality_error"] < tolerance
            and projectors["max_idempotence_error"] < tolerance
            and projectors["max_state_projector_error"] < tolerance
        ),
        "random-state fidelity": bool(trials["max_infidelity"] < tolerance),
        "all Bell outcomes": set(trials["outcomes_seen"])
        == {OUTCOME_LABELS[outcome] for outcome in OUTCOME_ORDER},
        "Bob pre-message input-independence": bool(
            trials["max_pre_measurement_trace_distance"] < tolerance
            and trials["max_post_measurement_trace_distance"] < tolerance
            and trials["max_pairwise_pre_message_distance"] < tolerance
        ),
        "causal record channel": bool(
            channel["pre_delivery_blocked"]
            and channel["delivered_once"]
            and 1.0 - channel["post_delivery_fidelity"] < tolerance
        ),
    }

    print("Acceptance gates:")
    for name, ok in pass_checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()
    print("Claim boundary:")
    print("  This is quantum state teleportation on encoded taste qubits only.")
    print("  It is not matter teleportation, mass transfer, charge transfer, or FTL transport.")

    return all(pass_checks.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=64, help="number of random input states")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--tolerance", type=float, default=1e-12, help="pass/fail tolerance")
    args = parser.parse_args()

    if args.trials <= 0:
        raise ValueError("--trials must be positive")

    encoding = native_taste_encoding_check()
    projectors = verify_bell_projectors()
    trials = run_random_teleportation_trials(args.trials, args.seed)
    channel = run_causal_channel_demo(args.seed + 1)

    ok = print_summary(encoding, projectors, trials, channel, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
