#!/usr/bin/env python3
"""Von-Neumann-style Bell-measurement record model for teleportation.

This runner pushes the first teleportation artifact's measurement limitation
one step: Alice's ideal Bell projectors are coupled to an explicit orthogonal
record register,

    V |Psi>_ARB = sum_zx (P_zx^AR tensor I_B) |Psi>_ARB tensor |zx>_M.

The record basis is assumed classical/orthogonal. This is a small
measurement-record model, not a derivation of measurement dynamics,
decoherence, or durable endogenous records.
"""

from __future__ import annotations

import argparse
import math
import sys

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
OUTCOME_INDEX = {outcome: index for index, outcome in enumerate(OUTCOME_ORDER)}


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    state = rng.standard_normal(2) + 1j * rng.standard_normal(2)
    return normalize(state)


def density(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


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
    """Bell projector using the same stabilizer convention as the protocol."""
    zz = np.kron(Z2, Z2)
    xx = np.kron(X2, X2)
    identity = np.eye(4, dtype=complex)
    return 0.25 * (identity + ((-1) ** x_bit) * zz) @ (
        identity + ((-1) ** z_bit) * xx
    )


def correction_operator(z_bit: int, x_bit: int) -> np.ndarray:
    z_op = Z2 if z_bit else I2
    x_op = X2 if x_bit else I2
    return z_op @ x_op


def prepare_three_register_state(input_state: np.ndarray) -> np.ndarray:
    """Prepare |psi>_A tensor |Phi+>_RB in A,R,B register order."""
    return np.kron(input_state, bell_state(0, 0))


def premeasure_bell_record(state: np.ndarray) -> np.ndarray:
    """Entangle Alice's Bell outcome to a four-state orthogonal record.

    Input shape is the pure A,R,B state. Output register order is A,R,B,M,
    where M is the Bell-record register ordered by OUTCOME_ORDER.
    """
    ar_by_b = state.reshape(4, 2)
    output = np.zeros((2, 2, 2, 4), dtype=complex)
    for z_bit, x_bit in OUTCOME_ORDER:
        record_index = OUTCOME_INDEX[(z_bit, x_bit)]
        branch = (bell_projector(z_bit, x_bit) @ ar_by_b).reshape(2, 2, 2)
        output[:, :, :, record_index] = branch
    return output.reshape(32)


def bob_reduced_from_record_state(record_state: np.ndarray) -> np.ndarray:
    """Trace out A,R and the inaccessible record M."""
    amplitudes = record_state.reshape(2, 2, 2, 4)
    rho = np.einsum("arbm,arsm->bs", amplitudes, amplitudes.conj())
    return rho


def record_probabilities(record_state: np.ndarray) -> dict[tuple[int, int], float]:
    amplitudes = record_state.reshape(2, 2, 2, 4)
    marginal = np.sum(np.abs(amplitudes) ** 2, axis=(0, 1, 2))
    return {
        outcome: float(np.real(marginal[OUTCOME_INDEX[outcome]]))
        for outcome in OUTCOME_ORDER
    }


def conditional_bob_rho(
    record_state: np.ndarray, z_bit: int, x_bit: int
) -> tuple[float, np.ndarray]:
    """Condition on a delivered record and return Bob's branch state."""
    record_index = OUTCOME_INDEX[(z_bit, x_bit)]
    branch = record_state.reshape(2, 2, 2, 4)[:, :, :, record_index]
    probability = float(np.real(np.vdot(branch, branch)))
    if probability <= 1e-15:
        raise ValueError("record branch has zero probability")
    rho = np.einsum("arb,ars->bs", branch, branch.conj()) / probability
    return probability, rho


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def pure_state_fidelity(state: np.ndarray, rho: np.ndarray) -> float:
    state = normalize(state)
    return float(np.real(np.vdot(state, rho @ state)))


def verify_bell_projectors() -> dict[str, float]:
    identity = np.eye(4, dtype=complex)
    projectors = [bell_projector(z, x) for z, x in OUTCOME_ORDER]
    resolution_error = float(np.max(np.abs(sum(projectors) - identity)))
    orthogonality_error = 0.0
    idempotence_error = 0.0
    state_projector_error = 0.0

    for i, first in enumerate(projectors):
        idempotence_error = max(
            idempotence_error, float(np.max(np.abs(first @ first - first)))
        )
        z_bit, x_bit = OUTCOME_ORDER[i]
        state_projector_error = max(
            state_projector_error,
            float(np.max(np.abs(first - density(bell_state(z_bit, x_bit))))),
        )
        for j, second in enumerate(projectors):
            if i == j:
                continue
            orthogonality_error = max(
                orthogonality_error, float(np.max(np.abs(first @ second)))
            )

    return {
        "resolution_error": resolution_error,
        "orthogonality_error": orthogonality_error,
        "idempotence_error": idempotence_error,
        "state_projector_error": state_projector_error,
    }


def run_record_trials(n_trials: int, seed: int) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    half_identity = 0.5 * I2
    reference_bob_rho: np.ndarray | None = None
    reference_record_probs: np.ndarray | None = None

    max_isometry_norm_error = 0.0
    max_record_probability_error = 0.0
    max_pairwise_record_probability_distance = 0.0
    max_bob_trace_distance_to_half_identity = 0.0
    max_pairwise_bob_pre_record_distance = 0.0
    min_conditioned_correction_fidelity = 1.0
    max_conditioned_infidelity = 0.0
    max_corrected_trace_distance = 0.0
    delivered_records_seen: set[tuple[int, int]] = set()

    for _ in range(n_trials):
        input_state = random_qubit(rng)
        input_rho = density(input_state)
        initial_state = prepare_three_register_state(input_state)
        record_state = premeasure_bell_record(initial_state)

        max_isometry_norm_error = max(
            max_isometry_norm_error,
            abs(float(np.vdot(record_state, record_state).real) - 1.0),
        )

        probs = record_probabilities(record_state)
        prob_vector = np.array([probs[outcome] for outcome in OUTCOME_ORDER])
        max_record_probability_error = max(
            max_record_probability_error,
            max(abs(prob - 0.25) for prob in prob_vector),
        )
        if reference_record_probs is None:
            reference_record_probs = prob_vector
        else:
            max_pairwise_record_probability_distance = max(
                max_pairwise_record_probability_distance,
                float(np.max(np.abs(prob_vector - reference_record_probs))),
            )

        bob_rho = bob_reduced_from_record_state(record_state)
        max_bob_trace_distance_to_half_identity = max(
            max_bob_trace_distance_to_half_identity,
            trace_distance(bob_rho, half_identity),
        )
        if reference_bob_rho is None:
            reference_bob_rho = bob_rho
        else:
            max_pairwise_bob_pre_record_distance = max(
                max_pairwise_bob_pre_record_distance,
                trace_distance(bob_rho, reference_bob_rho),
            )

        for z_bit, x_bit in OUTCOME_ORDER:
            probability, branch_rho = conditional_bob_rho(record_state, z_bit, x_bit)
            delivered_records_seen.add((z_bit, x_bit))
            max_record_probability_error = max(
                max_record_probability_error, abs(probability - 0.25)
            )
            correction = correction_operator(z_bit, x_bit)
            corrected_rho = correction @ branch_rho @ correction.conj().T
            fidelity = pure_state_fidelity(input_state, corrected_rho)
            min_conditioned_correction_fidelity = min(
                min_conditioned_correction_fidelity, fidelity
            )
            max_conditioned_infidelity = max(max_conditioned_infidelity, 1.0 - fidelity)
            max_corrected_trace_distance = max(
                max_corrected_trace_distance, trace_distance(corrected_rho, input_rho)
            )

    return {
        "n_trials": n_trials,
        "seed": seed,
        "max_isometry_norm_error": max_isometry_norm_error,
        "max_record_probability_error": max_record_probability_error,
        "max_pairwise_record_probability_distance": max_pairwise_record_probability_distance,
        "max_bob_trace_distance_to_half_identity": max_bob_trace_distance_to_half_identity,
        "max_pairwise_bob_pre_record_distance": max_pairwise_bob_pre_record_distance,
        "delivered_records_seen": sorted(
            OUTCOME_LABELS[outcome] for outcome in delivered_records_seen
        ),
        "min_conditioned_correction_fidelity": min_conditioned_correction_fidelity,
        "max_conditioned_infidelity": max_conditioned_infidelity,
        "max_corrected_trace_distance": max_corrected_trace_distance,
    }


def print_summary(
    projectors: dict[str, float], trials: dict[str, object], tolerance: float
) -> bool:
    print("TELEPORTATION BELL-MEASUREMENT RECORD MODEL")
    print("Status: explicit ideal record model; not a measurement derivation")
    print()

    print("Model:")
    print("  V |Psi>_ARB = sum_zx (P_zx^AR tensor I_B)|Psi>_ARB tensor |zx>_M")
    print("  record basis: four orthogonal Bell labels Phi+, Phi-, Psi+, Psi-")
    print("  correction convention after delivered record: U_zx = Z^z X^x")
    print()

    print("Bell projectors:")
    print(f"  resolution error: {projectors['resolution_error']:.3e}")
    print(f"  orthogonality error: {projectors['orthogonality_error']:.3e}")
    print(f"  idempotence error: {projectors['idempotence_error']:.3e}")
    print(f"  state-projector error: {projectors['state_projector_error']:.3e}")
    print()

    print("Record trials:")
    print(f"  random input states: {trials['n_trials']} (seed={trials['seed']})")
    print(f"  max premeasurement isometry norm error: {trials['max_isometry_norm_error']:.3e}")
    print(
        "  max Bell-record probability error from 1/4: "
        f"{trials['max_record_probability_error']:.3e}"
    )
    print(
        "  max pairwise record-probability distance across inputs: "
        f"{trials['max_pairwise_record_probability_distance']:.3e}"
    )
    print(
        "  max Bob trace distance to I/2 before receiving record: "
        f"{trials['max_bob_trace_distance_to_half_identity']:.3e}"
    )
    print(
        "  max pairwise Bob pre-record distance across inputs: "
        f"{trials['max_pairwise_bob_pre_record_distance']:.3e}"
    )
    print(f"  delivered records conditioned: {', '.join(trials['delivered_records_seen'])}")
    print(
        "  minimum post-delivery corrected fidelity: "
        f"{trials['min_conditioned_correction_fidelity']:.16f}"
    )
    print(f"  maximum post-delivery infidelity: {trials['max_conditioned_infidelity']:.3e}")
    print(
        "  max corrected-state trace distance to input: "
        f"{trials['max_corrected_trace_distance']:.3e}"
    )
    print()

    pass_checks = {
        "Bell projector algebra": bool(
            projectors["resolution_error"] < tolerance
            and projectors["orthogonality_error"] < tolerance
            and projectors["idempotence_error"] < tolerance
            and projectors["state_projector_error"] < tolerance
        ),
        "record isometry": bool(trials["max_isometry_norm_error"] < tolerance),
        "record marginal input-independence": bool(
            trials["max_record_probability_error"] < tolerance
            and trials["max_pairwise_record_probability_distance"] < tolerance
        ),
        "Bob pre-record input-independence": bool(
            trials["max_bob_trace_distance_to_half_identity"] < tolerance
            and trials["max_pairwise_bob_pre_record_distance"] < tolerance
        ),
        "delivered-record correction": bool(
            trials["max_conditioned_infidelity"] < tolerance
            and trials["max_corrected_trace_distance"] < tolerance
            and set(trials["delivered_records_seen"])
            == {OUTCOME_LABELS[outcome] for outcome in OUTCOME_ORDER}
        ),
    }

    print("Acceptance gates:")
    for name, ok in pass_checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()

    print("Claim boundary:")
    print("  This models an ideal orthogonal Bell-measurement record register.")
    print("  It does not derive record durability, apparatus dynamics, Born weights,")
    print("  environmental decoherence, matter transport, or faster-than-light signaling.")

    return all(pass_checks.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=64, help="number of random input states")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument("--tolerance", type=float, default=1e-12, help="pass/fail tolerance")
    args = parser.parse_args()

    if args.trials <= 0:
        raise ValueError("--trials must be positive")

    projectors = verify_bell_projectors()
    trials = run_record_trials(args.trials, args.seed)
    ok = print_summary(projectors, trials, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
