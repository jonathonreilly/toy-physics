#!/usr/bin/env python3
"""Noisy/faulty teleportation controls harness.

Status: planning / first artifact. This runner stress-tests ordinary qubit
state teleportation under bounded control faults. It does not claim matter
teleportation, mass transfer, charge transfer, energy transport, or
faster-than-light communication.

Registers are ordered as:

    A = Alice unknown qubit
    R = Alice resource half
    B = Bob resource half

The protocol follows the existing teleportation lane:

    Alice measures A,R in the Bell basis.
    A two-bit Bell record (z, x) is sent over a causal classical channel.
    Bob applies Z^z X^x when the record is available.

Fault layers are explicit and classical:

    resource depolarization: rho_RB(v)=v|Phi+><Phi+|+(1-v)I/4
    Bell-measurement readout bit flips before the record enters the channel
    classical-channel record bit flips, drops, and delays
    Bob correction-control bit flips

Drops and delays are separated in the report. A delayed record hurts fidelity
at a fixed readout deadline, but not after it eventually arrives. A dropped
record never arrives, so Bob uses the identity fallback.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from collections.abc import Callable, Iterable

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
CLASSICAL_AVG_FIDELITY = 2.0 / 3.0


@dataclasses.dataclass(frozen=True)
class FaultProfile:
    """Independent bounded fault probabilities for one teleportation run."""

    label: str
    visibility: float = 1.0
    meas_z_flip: float = 0.0
    meas_x_flip: float = 0.0
    classical_z_flip: float = 0.0
    classical_x_flip: float = 0.0
    drop_probability: float = 0.0
    delay_probability: float = 0.0
    bob_z_error: float = 0.0
    bob_x_error: float = 0.0
    base_latency_ticks: int = 3
    extra_delay_ticks: int = 2


@dataclasses.dataclass(frozen=True)
class ProfileDiagnostics:
    label: str
    visibility: float
    delivered_by_deadline: float
    delivered_eventually: float
    exact_avg_fidelity_deadline: float
    exact_avg_fidelity_eventual: float
    sampled_min_fidelity_deadline: float
    sampled_min_fidelity_eventual: float
    sampled_avg_fidelity_deadline: float
    sampled_avg_fidelity_eventual: float
    max_no_record_distance_to_i2: float
    max_pairwise_no_record_distance: float
    max_branch_probability_span: float
    max_trace_error_deadline: float
    max_trace_error_eventual: float

    @property
    def verdict_deadline(self) -> str:
        return verdict(self.exact_avg_fidelity_deadline)

    @property
    def verdict_eventual(self) -> str:
        return verdict(self.exact_avg_fidelity_eventual)


def verdict(fidelity: float) -> str:
    margin = fidelity - CLASSICAL_AVG_FIDELITY
    if margin > 1e-10:
        return "beats 2/3"
    if abs(margin) <= 1e-10:
        return "at 2/3"
    return "below 2/3"


def validate_probability(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]")


def validate_profile(profile: FaultProfile) -> None:
    for name in (
        "visibility",
        "meas_z_flip",
        "meas_x_flip",
        "classical_z_flip",
        "classical_x_flip",
        "drop_probability",
        "delay_probability",
        "bob_z_error",
        "bob_x_error",
    ):
        validate_probability(name, float(getattr(profile, name)))
    if profile.base_latency_ticks <= 0:
        raise ValueError("base_latency_ticks must be positive")
    if profile.extra_delay_ticks < 0:
        raise ValueError("extra_delay_ticks cannot be negative")


def normalize_state(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def projector(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def hermitian_part(matrix: np.ndarray) -> np.ndarray:
    return 0.5 * (matrix + matrix.conj().T)


def bell_state(z_bit: int, x_bit: int) -> np.ndarray:
    """Bell state |Bell(z,x)> with z as phase bit and x as bit-flip bit."""
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
    return projector(bell_state(z_bit, x_bit))


def correction_operator(z_bit: int, x_bit: int) -> np.ndarray:
    z_op = Z2 if z_bit else I2
    x_op = X2 if x_bit else I2
    return z_op @ x_op


def depolarized_bell_resource(visibility: float) -> np.ndarray:
    validate_probability("visibility", visibility)
    return visibility * projector(bell_state(0, 0)) + (1.0 - visibility) * np.eye(4) / 4.0


def partial_trace(rho: np.ndarray, dims: Iterable[int], keep: Iterable[int]) -> np.ndarray:
    dims = list(dims)
    keep = sorted(keep)
    trace_out = [axis for axis in range(len(dims)) if axis not in keep]
    tensor = rho.reshape(*(dims + dims))
    current_dims = list(dims)
    for axis in sorted(trace_out, reverse=True):
        tensor = np.trace(tensor, axis1=axis, axis2=axis + len(current_dims))
        current_dims.pop(axis)
    final_dim = int(np.prod(current_dims))
    return tensor.reshape(final_dim, final_dim)


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = hermitian_part(first - second)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def pure_state_fidelity(state: np.ndarray, rho: np.ndarray) -> float:
    value = np.vdot(state, rho @ state)
    return float(np.clip(np.real(value), 0.0, 1.0))


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    return normalize_state(rng.standard_normal(2) + 1j * rng.standard_normal(2))


def probe_states(rng: np.random.Generator, n_random: int) -> list[np.ndarray]:
    states = [
        np.array([1.0, 0.0], dtype=complex),
        np.array([0.0, 1.0], dtype=complex),
        normalize_state(np.array([1.0, 1.0], dtype=complex)),
        normalize_state(np.array([1.0, -1.0], dtype=complex)),
        normalize_state(np.array([1.0, 1.0j], dtype=complex)),
        normalize_state(np.array([1.0, -1.0j], dtype=complex)),
    ]
    states.extend(random_qubit(rng) for _ in range(n_random))
    return states


def bit_flip_distribution(p_z: float, p_x: float) -> tuple[tuple[int, int, float], ...]:
    validate_probability("p_z", p_z)
    validate_probability("p_x", p_x)
    return (
        (0, 0, (1.0 - p_z) * (1.0 - p_x)),
        (1, 0, p_z * (1.0 - p_x)),
        (0, 1, (1.0 - p_z) * p_x),
        (1, 1, p_z * p_x),
    )


def delivered_probability(profile: FaultProfile, *, at_deadline: bool) -> float:
    if at_deadline:
        return (1.0 - profile.drop_probability) * (1.0 - profile.delay_probability)
    return 1.0 - profile.drop_probability


def bell_branches(
    input_op: np.ndarray, resource_rho: np.ndarray
) -> dict[tuple[int, int], np.ndarray]:
    joint = np.kron(input_op, resource_rho)
    branches: dict[tuple[int, int], np.ndarray] = {}
    for z_bit, x_bit in OUTCOME_ORDER:
        measurement = np.kron(bell_projector(z_bit, x_bit), I2)
        branch = measurement @ joint @ measurement
        branches[(z_bit, x_bit)] = partial_trace(branch, dims=[2, 2, 2], keep=[2])
    return branches


def bob_no_record_state(input_rho: np.ndarray, resource_rho: np.ndarray) -> np.ndarray:
    output = np.zeros((2, 2), dtype=complex)
    for branch in bell_branches(input_rho, resource_rho).values():
        output += branch
    return output


def bell_branch_probabilities(
    input_rho: np.ndarray, resource_rho: np.ndarray
) -> dict[tuple[int, int], float]:
    probabilities: dict[tuple[int, int], float] = {}
    for outcome, branch in bell_branches(input_rho, resource_rho).items():
        probabilities[outcome] = float(np.real(np.trace(branch)))
    return probabilities


def faulty_channel_apply(
    input_op: np.ndarray,
    profile: FaultProfile,
    *,
    at_deadline: bool,
) -> np.ndarray:
    """Apply the noisy teleportation channel to a single-qubit operator.

    If a record is unavailable, Bob uses the identity fallback. That fallback is
    intentionally conservative and preserves the no-record Bob state.
    """
    validate_profile(profile)
    resource_rho = depolarized_bell_resource(profile.visibility)
    delivered = delivered_probability(profile, at_deadline=at_deadline)
    unavailable = 1.0 - delivered

    measurement_flips = bit_flip_distribution(profile.meas_z_flip, profile.meas_x_flip)
    classical_flips = bit_flip_distribution(
        profile.classical_z_flip,
        profile.classical_x_flip,
    )
    bob_errors = bit_flip_distribution(profile.bob_z_error, profile.bob_x_error)

    output = np.zeros((2, 2), dtype=complex)
    for (true_z, true_x), bob_branch in bell_branches(input_op, resource_rho).items():
        output += unavailable * bob_branch
        for meas_z, meas_x, p_meas in measurement_flips:
            for classical_z, classical_x, p_classical in classical_flips:
                record_z = true_z ^ meas_z ^ classical_z
                record_x = true_x ^ meas_x ^ classical_x
                for bob_z, bob_x, p_bob in bob_errors:
                    actual_z = record_z ^ bob_z
                    actual_x = record_x ^ bob_x
                    probability = delivered * p_meas * p_classical * p_bob
                    correction = correction_operator(actual_z, actual_x)
                    output += probability * correction @ bob_branch @ correction.conj().T
    return output


def choi_matrix(profile: FaultProfile, *, at_deadline: bool) -> np.ndarray:
    choi = np.zeros((4, 4), dtype=complex)
    for row in range(2):
        for col in range(2):
            basis_op = np.zeros((2, 2), dtype=complex)
            basis_op[row, col] = 1.0
            choi += 0.5 * np.kron(
                basis_op,
                faulty_channel_apply(basis_op, profile, at_deadline=at_deadline),
            )
    return choi


def exact_average_fidelity(profile: FaultProfile, *, at_deadline: bool) -> float:
    choi = choi_matrix(profile, at_deadline=at_deadline)
    phi = bell_state(0, 0)
    entanglement_fidelity = float(np.real(np.vdot(phi, choi @ phi)))
    return float((2.0 * entanglement_fidelity + 1.0) / 3.0)


def evaluate_profile(
    profile: FaultProfile,
    states: list[np.ndarray],
) -> ProfileDiagnostics:
    validate_profile(profile)
    resource_rho = depolarized_bell_resource(profile.visibility)
    half_identity = 0.5 * I2

    deadline_fidelities: list[float] = []
    eventual_fidelities: list[float] = []
    branch_probabilities: dict[tuple[int, int], list[float]] = {
        outcome: [] for outcome in OUTCOME_ORDER
    }

    no_record_reference: np.ndarray | None = None
    max_no_record_distance_to_i2 = 0.0
    max_pairwise_no_record_distance = 0.0
    max_trace_error_deadline = 0.0
    max_trace_error_eventual = 0.0

    for state in states:
        input_rho = projector(state)
        deadline_output = faulty_channel_apply(input_rho, profile, at_deadline=True)
        eventual_output = faulty_channel_apply(input_rho, profile, at_deadline=False)
        deadline_fidelities.append(pure_state_fidelity(state, deadline_output))
        eventual_fidelities.append(pure_state_fidelity(state, eventual_output))
        max_trace_error_deadline = max(
            max_trace_error_deadline,
            float(abs(np.trace(deadline_output) - 1.0)),
        )
        max_trace_error_eventual = max(
            max_trace_error_eventual,
            float(abs(np.trace(eventual_output) - 1.0)),
        )

        no_record = bob_no_record_state(input_rho, resource_rho)
        max_no_record_distance_to_i2 = max(
            max_no_record_distance_to_i2,
            trace_distance(no_record, half_identity),
        )
        if no_record_reference is None:
            no_record_reference = no_record
        else:
            max_pairwise_no_record_distance = max(
                max_pairwise_no_record_distance,
                trace_distance(no_record, no_record_reference),
            )

        for outcome, probability in bell_branch_probabilities(input_rho, resource_rho).items():
            branch_probabilities[outcome].append(probability)

    max_branch_probability_span = max(
        max(values) - min(values) for values in branch_probabilities.values()
    )

    return ProfileDiagnostics(
        label=profile.label,
        visibility=profile.visibility,
        delivered_by_deadline=delivered_probability(profile, at_deadline=True),
        delivered_eventually=delivered_probability(profile, at_deadline=False),
        exact_avg_fidelity_deadline=exact_average_fidelity(profile, at_deadline=True),
        exact_avg_fidelity_eventual=exact_average_fidelity(profile, at_deadline=False),
        sampled_min_fidelity_deadline=float(np.min(deadline_fidelities)),
        sampled_min_fidelity_eventual=float(np.min(eventual_fidelities)),
        sampled_avg_fidelity_deadline=float(np.mean(deadline_fidelities)),
        sampled_avg_fidelity_eventual=float(np.mean(eventual_fidelities)),
        max_no_record_distance_to_i2=max_no_record_distance_to_i2,
        max_pairwise_no_record_distance=max_pairwise_no_record_distance,
        max_branch_probability_span=max_branch_probability_span,
        max_trace_error_deadline=max_trace_error_deadline,
        max_trace_error_eventual=max_trace_error_eventual,
    )


def profile_suite() -> list[FaultProfile]:
    return [
        FaultProfile("ideal reference"),
        FaultProfile("resource depolarization v=0.90", visibility=0.90),
        FaultProfile("resource boundary v=1/3", visibility=1.0 / 3.0),
        FaultProfile(
            "Bell readout flips p=0.05",
            meas_z_flip=0.05,
            meas_x_flip=0.05,
        ),
        FaultProfile(
            "classical flips/drop/delay",
            classical_z_flip=0.05,
            classical_x_flip=0.05,
            drop_probability=0.10,
            delay_probability=0.20,
        ),
        FaultProfile(
            "Bob correction errors p=0.03",
            bob_z_error=0.03,
            bob_x_error=0.03,
        ),
        FaultProfile(
            "combined moderate controls",
            visibility=0.85,
            meas_z_flip=0.03,
            meas_x_flip=0.03,
            classical_z_flip=0.04,
            classical_x_flip=0.04,
            drop_probability=0.05,
            delay_probability=0.10,
            bob_z_error=0.02,
            bob_x_error=0.02,
        ),
        FaultProfile(
            "stress below deadline threshold",
            visibility=0.60,
            meas_z_flip=0.15,
            meas_x_flip=0.15,
            classical_z_flip=0.10,
            classical_x_flip=0.10,
            drop_probability=0.25,
            delay_probability=0.30,
            bob_z_error=0.10,
            bob_x_error=0.10,
        ),
    ]


def threshold_increasing(
    fidelity_at: Callable[[float], float],
    *,
    low: float = 0.0,
    high: float = 1.0,
    iterations: int = 80,
) -> float | None:
    low_margin = fidelity_at(low) - CLASSICAL_AVG_FIDELITY
    high_margin = fidelity_at(high) - CLASSICAL_AVG_FIDELITY
    if high_margin <= 0.0:
        return None
    if low_margin >= 0.0:
        return low
    for _ in range(iterations):
        middle = 0.5 * (low + high)
        if fidelity_at(middle) >= CLASSICAL_AVG_FIDELITY:
            high = middle
        else:
            low = middle
    return high


def threshold_decreasing(
    fidelity_at: Callable[[float], float],
    *,
    low: float = 0.0,
    high: float = 1.0,
    iterations: int = 80,
) -> float | None:
    low_margin = fidelity_at(low) - CLASSICAL_AVG_FIDELITY
    high_margin = fidelity_at(high) - CLASSICAL_AVG_FIDELITY
    if low_margin <= 0.0:
        return None
    if high_margin >= 0.0:
        return high
    for _ in range(iterations):
        middle = 0.5 * (low + high)
        if fidelity_at(middle) >= CLASSICAL_AVG_FIDELITY:
            low = middle
        else:
            high = middle
    return low


def threshold_summary() -> dict[str, float | None]:
    combined = FaultProfile(
        "combined moderate threshold template",
        meas_z_flip=0.03,
        meas_x_flip=0.03,
        classical_z_flip=0.04,
        classical_x_flip=0.04,
        drop_probability=0.05,
        delay_probability=0.10,
        bob_z_error=0.02,
        bob_x_error=0.02,
    )

    return {
        "resource_visibility": threshold_increasing(
            lambda v: exact_average_fidelity(
                FaultProfile("resource threshold", visibility=v),
                at_deadline=True,
            )
        ),
        "measurement_bit_flip": threshold_decreasing(
            lambda p: exact_average_fidelity(
                FaultProfile("measurement threshold", meas_z_flip=p, meas_x_flip=p),
                at_deadline=True,
            )
        ),
        "classical_bit_flip": threshold_decreasing(
            lambda p: exact_average_fidelity(
                FaultProfile(
                    "classical threshold",
                    classical_z_flip=p,
                    classical_x_flip=p,
                ),
                at_deadline=True,
            )
        ),
        "bob_correction_error": threshold_decreasing(
            lambda p: exact_average_fidelity(
                FaultProfile("bob threshold", bob_z_error=p, bob_x_error=p),
                at_deadline=True,
            )
        ),
        "drop_probability": threshold_decreasing(
            lambda p: exact_average_fidelity(
                FaultProfile("drop threshold", drop_probability=p),
                at_deadline=True,
            )
        ),
        "deadline_delay_probability": threshold_decreasing(
            lambda p: exact_average_fidelity(
                FaultProfile("delay threshold", delay_probability=p),
                at_deadline=True,
            )
        ),
        "combined_visibility_deadline": threshold_increasing(
            lambda v: exact_average_fidelity(
                dataclasses.replace(combined, visibility=v),
                at_deadline=True,
            )
        ),
        "combined_visibility_eventual": threshold_increasing(
            lambda v: exact_average_fidelity(
                dataclasses.replace(combined, visibility=v),
                at_deadline=False,
            )
        ),
    }


def print_profile_table(diagnostics: list[ProfileDiagnostics]) -> None:
    print("Fault-profile diagnostics:")
    print(
        "  "
        f"{'profile':35s} {'v':>6s} {'D_now':>7s} {'D_evt':>7s} "
        f"{'F_now':>9s} {'F_evt':>9s} {'Fmin_now':>9s} {'Fmin_evt':>9s} "
        f"{'noSig':>9s} {'verdict_now':>12s}"
    )
    for item in diagnostics:
        print(
            "  "
            f"{item.label[:35]:35s} "
            f"{item.visibility:6.3f} "
            f"{item.delivered_by_deadline:7.3f} "
            f"{item.delivered_eventually:7.3f} "
            f"{item.exact_avg_fidelity_deadline:9.6f} "
            f"{item.exact_avg_fidelity_eventual:9.6f} "
            f"{item.sampled_min_fidelity_deadline:9.6f} "
            f"{item.sampled_min_fidelity_eventual:9.6f} "
            f"{item.max_pairwise_no_record_distance:9.3e} "
            f"{item.verdict_deadline:>12s}"
        )
    print()
    print("  D_now is the total probability that the record has arrived by the")
    print("  readout deadline. D_evt is the eventual non-dropped delivery")
    print("  probability. Delays affect F_now, not F_evt, once the record arrives.")


def print_thresholds(thresholds: dict[str, float | None]) -> None:
    def fmt(value: float | None) -> str:
        return "no crossing in [0,1]" if value is None else f"{value:.10f}"

    print("Thresholds and controls:")
    print(f"  classical qubit average-fidelity benchmark: {CLASSICAL_AVG_FIDELITY:.10f}")
    print(
        "  resource depolarization only, rho(v)=v|Phi+><Phi+|+(1-v)I/4: "
        f"v > {fmt(thresholds['resource_visibility'])}"
    )
    print(
        "  symmetric Bell-measurement record bit-flip error only: "
        f"p < {fmt(thresholds['measurement_bit_flip'])}"
    )
    print(
        "  symmetric classical-record bit-flip error only: "
        f"p < {fmt(thresholds['classical_bit_flip'])}"
    )
    print(
        "  symmetric Bob correction-control bit error only: "
        f"p < {fmt(thresholds['bob_correction_error'])}"
    )
    print(
        "  record drop probability only, identity fallback: "
        f"p_drop < {fmt(thresholds['drop_probability'])}"
    )
    print(
        "  record delay past readout deadline only: "
        f"p_delay < {fmt(thresholds['deadline_delay_probability'])}"
    )
    print("  pure delay has no eventual fidelity penalty after the delayed record arrives.")
    print(
        "  combined moderate non-resource faults require visibility by deadline: "
        f"v > {fmt(thresholds['combined_visibility_deadline'])}"
    )
    print(
        "  combined moderate non-resource faults require visibility eventually: "
        f"v > {fmt(thresholds['combined_visibility_eventual'])}"
    )


def print_no_signaling_summary(diagnostics: list[ProfileDiagnostics]) -> None:
    max_no_record_to_i2 = max(item.max_no_record_distance_to_i2 for item in diagnostics)
    max_pairwise = max(item.max_pairwise_no_record_distance for item in diagnostics)
    max_branch_span = max(item.max_branch_probability_span for item in diagnostics)
    max_trace_error_deadline = max(item.max_trace_error_deadline for item in diagnostics)
    max_trace_error_eventual = max(item.max_trace_error_eventual for item in diagnostics)

    print("No-signaling and normalization diagnostics:")
    print(f"  max Bob no-record trace distance to I/2: {max_no_record_to_i2:.3e}")
    print(
        "  max pairwise Bob no-record distance across sampled inputs: "
        f"{max_pairwise:.3e}"
    )
    print(
        "  max Bell-branch probability span across sampled inputs: "
        f"{max_branch_span:.3e}"
    )
    print("  record drop/delay availability is input-independent by construction.")
    print(f"  max output trace error by deadline: {max_trace_error_deadline:.3e}")
    print(f"  max output trace error eventually: {max_trace_error_eventual:.3e}")
    print("  Input-dependent fidelity appears only after causal record delivery.")


def print_acceptance_gates(
    diagnostics: list[ProfileDiagnostics],
    thresholds: dict[str, float | None],
    tolerance: float,
) -> bool:
    by_label = {item.label: item for item in diagnostics}
    ideal = by_label["ideal reference"]
    boundary = by_label["resource boundary v=1/3"]
    moderate = by_label["combined moderate controls"]
    stress = by_label["stress below deadline threshold"]
    max_pairwise = max(item.max_pairwise_no_record_distance for item in diagnostics)
    max_no_record_to_i2 = max(item.max_no_record_distance_to_i2 for item in diagnostics)
    max_trace_error = max(
        max(item.max_trace_error_deadline, item.max_trace_error_eventual)
        for item in diagnostics
    )

    gates = {
        "ideal reference fidelity": abs(ideal.exact_avg_fidelity_deadline - 1.0)
        <= 10 * tolerance,
        "resource boundary lands at 2/3": abs(
            boundary.exact_avg_fidelity_deadline - CLASSICAL_AVG_FIDELITY
        )
        <= 10 * tolerance,
        "thresholds found": all(value is not None for value in thresholds.values()),
        "combined moderate still beats deadline benchmark": moderate.exact_avg_fidelity_deadline
        > CLASSICAL_AVG_FIDELITY,
        "stress control falls below deadline benchmark": stress.exact_avg_fidelity_deadline
        < CLASSICAL_AVG_FIDELITY,
        "Bob pre-record input-independence": (
            max_pairwise <= 10 * tolerance and max_no_record_to_i2 <= 10 * tolerance
        ),
        "trace preservation": max_trace_error <= 10 * tolerance,
    }

    print("Acceptance gates:")
    for name, ok in gates.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()
    print("Claim boundary:")
    print("  This is a planning / first artifact for noisy qubit-state teleportation controls.")
    print("  Faults are independent classical controls around a supplied Bell resource.")
    print("  It is not FTL signaling, matter transport, mass transfer, charge transfer, or energy transport.")
    return all(gates.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=128, help="number of random input states")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--tolerance", type=float, default=1e-10, help="pass/fail tolerance")
    args = parser.parse_args()

    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if args.tolerance <= 0:
        raise ValueError("--tolerance must be positive")

    rng = np.random.default_rng(args.seed)
    states = probe_states(rng, args.trials)
    profiles = profile_suite()
    diagnostics = [evaluate_profile(profile, states) for profile in profiles]
    thresholds = threshold_summary()

    print("NOISY/FAULTY TELEPORTATION CONTROLS HARNESS")
    print("Status: planning / first artifact; quantum state teleportation only")
    print(f"Random input states: {args.trials} plus 6 Pauli-axis probes (seed={args.seed})")
    print("Classical readout deadline: base latency tick; delayed records arrive later")
    print()

    print_profile_table(diagnostics)
    print()
    print_thresholds(thresholds)
    print()
    print_no_signaling_summary(diagnostics)
    print()

    ok = print_acceptance_gates(diagnostics, thresholds, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
