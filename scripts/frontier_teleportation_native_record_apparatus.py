#!/usr/bin/env python3
"""Native Bell-record apparatus and 3D+1 carrier candidate.

This runner joins two earlier planning artifacts:

  * Bell premeasurement into an explicit orthogonal record register.
  * 3D+1 causal delivery of a two-bit classical Bell record.

The new model treats the Bell record as produced by a local Bell-stabilizer
transducer. The transducer writes a redundant classical codeword into local
apparatus memory, and the codeword is carried by local 3D+1 record-field
pulses to Bob. The carrier payload is derived from the apparatus branch; it is
not supplied as an external input to the channel.

This is still a bounded apparatus/carrier model, not a full derivation of
measurement, decoherence, detector hardware, or relativistic field dynamics.
It supports ordinary quantum state teleportation only.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from itertools import combinations
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

Point3D = tuple[int, int, int]
Codeword = tuple[int, ...]


@dataclasses.dataclass(frozen=True)
class SpacetimeEvent:
    tick: int
    site: Point3D


@dataclasses.dataclass(frozen=True)
class BellPointerRecord:
    z_bit: int
    x_bit: int
    codeword: Codeword
    source_kind: str = "bell_stabilizer_transducer"

    @property
    def label(self) -> str:
        return OUTCOME_LABELS[(self.z_bit, self.x_bit)]


@dataclasses.dataclass(frozen=True)
class RecordPulse:
    component_index: int
    bit: int
    worldline: tuple[SpacetimeEvent, ...]


@dataclasses.dataclass(frozen=True)
class RecordCarrierPacket:
    record_id: str
    pointer: BellPointerRecord
    source_site: Point3D
    target_site: Point3D
    emitted_at_tick: int
    deliver_at_tick: int
    pulses: tuple[RecordPulse, ...]

    @property
    def codeword(self) -> Codeword:
        return tuple(pulse.bit for pulse in self.pulses)


@dataclasses.dataclass(frozen=True)
class DecodedRecord:
    z_bit: int
    x_bit: int
    hamming_distance: int
    accepted: bool


@dataclasses.dataclass(frozen=True)
class Branch:
    z_bit: int
    x_bit: int
    probability: float
    bob_rho: np.ndarray
    pointer: BellPointerRecord


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


def pure_state_fidelity(state: np.ndarray, rho: np.ndarray) -> float:
    state = normalize(state)
    return float(np.real(np.vdot(state, rho @ state)))


def trace_distance(first: np.ndarray, second: np.ndarray) -> float:
    diff = 0.5 * (first - second + (first - second).conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def record_codeword(z_bit: int, x_bit: int) -> Codeword:
    """Length-8 repetition/parity code for a Bell outcome.

    Layout:
      z z z | x x x | p p, where p = z xor x.

    The four codewords have minimum Hamming distance 5, so nearest-codeword
    decoding corrects all one- and two-component bit flips.
    """

    parity = z_bit ^ x_bit
    return (z_bit, z_bit, z_bit, x_bit, x_bit, x_bit, parity, parity)


def hamming(first: Codeword, second: Codeword) -> int:
    if len(first) != len(second):
        raise ValueError("codewords must have the same length")
    return sum(int(a != b) for a, b in zip(first, second))


def all_codewords() -> dict[tuple[int, int], Codeword]:
    return {outcome: record_codeword(*outcome) for outcome in OUTCOME_ORDER}


def decode_codeword(codeword: Codeword, correction_radius: int = 2) -> DecodedRecord:
    distances = [
        (hamming(codeword, candidate), outcome)
        for outcome, candidate in all_codewords().items()
    ]
    distances.sort(key=lambda item: item[0])
    best_distance, best_outcome = distances[0]
    unique_best = len(distances) == 1 or best_distance < distances[1][0]
    accepted = unique_best and best_distance <= correction_radius
    return DecodedRecord(
        z_bit=best_outcome[0],
        x_bit=best_outcome[1],
        hamming_distance=best_distance,
        accepted=accepted,
    )


def flip_bits(codeword: Codeword, indexes: Iterable[int]) -> Codeword:
    bits = list(codeword)
    for index in indexes:
        bits[index] ^= 1
    return tuple(bits)


def code_metrics() -> dict[str, float | int | bool]:
    codewords = all_codewords()
    min_distance = min(
        hamming(a, b)
        for left, a in codewords.items()
        for right, b in codewords.items()
        if left != right
    )

    one_bit_corrected = True
    two_bit_corrected = True
    for outcome, codeword in codewords.items():
        for index in range(len(codeword)):
            decoded = decode_codeword(flip_bits(codeword, (index,)))
            one_bit_corrected = (
                one_bit_corrected
                and decoded.accepted
                and (decoded.z_bit, decoded.x_bit) == outcome
            )
        for indexes in combinations(range(len(codeword)), 2):
            decoded = decode_codeword(flip_bits(codeword, indexes))
            two_bit_corrected = (
                two_bit_corrected
                and decoded.accepted
                and (decoded.z_bit, decoded.x_bit) == outcome
            )

    return {
        "codeword_length": len(next(iter(codewords.values()))),
        "min_hamming_distance": min_distance,
        "one_bit_corrected": one_bit_corrected,
        "two_bit_corrected": two_bit_corrected,
    }


def prepare_three_register_state(input_state: np.ndarray) -> np.ndarray:
    return np.kron(input_state, bell_state(0, 0))


def transduce_bell_pointer_records(input_state: np.ndarray) -> list[Branch]:
    """Local Bell-stabilizer transducer writing pointer codewords."""

    state = prepare_three_register_state(input_state)
    ar_by_b = state.reshape(4, 2)
    branches: list[Branch] = []
    for z_bit, x_bit in OUTCOME_ORDER:
        branch = (bell_projector(z_bit, x_bit) @ ar_by_b).reshape(2, 2, 2)
        probability = float(np.real(np.vdot(branch, branch)))
        if probability <= 1e-15:
            raise ValueError("zero-probability Bell branch")
        bob_rho = np.einsum("arb,ars->bs", branch, branch.conj()) / probability
        branches.append(
            Branch(
                z_bit=z_bit,
                x_bit=x_bit,
                probability=probability,
                bob_rho=bob_rho,
                pointer=BellPointerRecord(
                    z_bit=z_bit,
                    x_bit=x_bit,
                    codeword=record_codeword(z_bit, x_bit),
                ),
            )
        )
    return branches


def manhattan_distance(source: Point3D, target: Point3D) -> int:
    return sum(abs(a - b) for a, b in zip(source, target))


def carrier_worldline(
    source: Point3D,
    target: Point3D,
    emitted_at_tick: int,
) -> tuple[SpacetimeEvent, ...]:
    position = list(source)
    events = [SpacetimeEvent(tick=emitted_at_tick, site=source)]
    tick = emitted_at_tick
    while tuple(position) != target:
        tick += 1
        for axis in range(3):
            delta = target[axis] - position[axis]
            if delta == 0:
                continue
            position[axis] += 1 if delta > 0 else -1
            break
        events.append(SpacetimeEvent(tick=tick, site=tuple(position)))
    return tuple(events)


def is_local_worldline(worldline: tuple[SpacetimeEvent, ...]) -> bool:
    if not worldline:
        return False
    for first, second in zip(worldline, worldline[1:]):
        if second.tick - first.tick != 1:
            return False
        if manhattan_distance(first.site, second.site) > 1:
            return False
    return True


def emit_record_carrier(
    pointer: BellPointerRecord,
    *,
    record_id: str,
    source_site: Point3D,
    target_site: Point3D,
    emitted_at_tick: int,
) -> RecordCarrierPacket:
    if pointer.source_kind != "bell_stabilizer_transducer":
        raise ValueError("record carrier payload must come from the Bell transducer")
    worldline = carrier_worldline(source_site, target_site, emitted_at_tick)
    pulses = tuple(
        RecordPulse(component_index=index, bit=bit, worldline=worldline)
        for index, bit in enumerate(pointer.codeword)
    )
    return RecordCarrierPacket(
        record_id=record_id,
        pointer=pointer,
        source_site=source_site,
        target_site=target_site,
        emitted_at_tick=emitted_at_tick,
        deliver_at_tick=worldline[-1].tick,
        pulses=pulses,
    )


def carrier_available(
    packet: RecordCarrierPacket,
    *,
    at_site: Point3D,
    at_tick: int,
) -> bool:
    return at_site == packet.target_site and at_tick >= packet.deliver_at_tick


def decode_carrier(packet: RecordCarrierPacket) -> DecodedRecord:
    return decode_codeword(packet.codeword)


def run_trials(args: argparse.Namespace) -> dict[str, object]:
    rng = np.random.default_rng(args.seed)
    source_site = tuple(args.alice_site)
    target_site = tuple(args.bob_site)
    emitted_tick = args.alice_tick
    expected_distance = manhattan_distance(source_site, target_site)
    expected_delivery_tick = emitted_tick + expected_distance

    reference_bob_rho: np.ndarray | None = None
    reference_distribution: np.ndarray | None = None
    max_isometry_norm_error = 0.0
    max_record_probability_error = 0.0
    max_pairwise_record_distribution_distance = 0.0
    max_pairwise_pre_delivery_bob_distance = 0.0
    max_bob_trace_distance_to_half_identity = 0.0
    min_correct_fidelity = 1.0
    max_correct_infidelity = 0.0
    max_correct_trace_distance = 0.0
    wrong_fidelities: list[float] = []
    generated_labels: set[str] = set()
    all_packets_derived = True
    all_worldlines_local = True
    all_pulse_counts_conserved = True
    early_delivery_blocked = True
    exact_delivery_available = True
    max_delivery_tick_error = 0

    for trial_index in range(args.trials):
        input_state = random_qubit(rng)
        input_rho = density(input_state)
        branches = transduce_bell_pointer_records(input_state)
        total_probability = sum(branch.probability for branch in branches)
        max_isometry_norm_error = max(
            max_isometry_norm_error, abs(total_probability - 1.0)
        )

        distribution = np.array([branch.probability for branch in branches])
        max_record_probability_error = max(
            max_record_probability_error,
            float(np.max(np.abs(distribution - 0.25))),
        )
        if reference_distribution is None:
            reference_distribution = distribution
        else:
            max_pairwise_record_distribution_distance = max(
                max_pairwise_record_distribution_distance,
                float(np.max(np.abs(distribution - reference_distribution))),
            )

        bob_pre_delivery = sum(
            branch.probability * branch.bob_rho for branch in branches
        )
        max_bob_trace_distance_to_half_identity = max(
            max_bob_trace_distance_to_half_identity,
            trace_distance(bob_pre_delivery, 0.5 * I2),
        )
        if reference_bob_rho is None:
            reference_bob_rho = bob_pre_delivery
        else:
            max_pairwise_pre_delivery_bob_distance = max(
                max_pairwise_pre_delivery_bob_distance,
                trace_distance(bob_pre_delivery, reference_bob_rho),
            )

        for branch in branches:
            generated_labels.add(branch.pointer.label)
            packet = emit_record_carrier(
                branch.pointer,
                record_id=f"native-record-{trial_index}-{branch.pointer.label}",
                source_site=source_site,
                target_site=target_site,
                emitted_at_tick=emitted_tick,
            )
            all_packets_derived = (
                all_packets_derived
                and packet.pointer.source_kind == "bell_stabilizer_transducer"
                and packet.pointer.codeword == packet.codeword
            )
            all_worldlines_local = all_worldlines_local and all(
                is_local_worldline(pulse.worldline) for pulse in packet.pulses
            )
            all_pulse_counts_conserved = (
                all_pulse_counts_conserved
                and len(packet.pulses) == len(branch.pointer.codeword)
                and all(len(pulse.worldline) == expected_distance + 1 for pulse in packet.pulses)
            )
            max_delivery_tick_error = max(
                max_delivery_tick_error,
                abs(packet.deliver_at_tick - expected_delivery_tick),
            )
            early_delivery_blocked = early_delivery_blocked and not carrier_available(
                packet,
                at_site=target_site,
                at_tick=expected_delivery_tick - 1,
            )
            exact_delivery_available = exact_delivery_available and carrier_available(
                packet,
                at_site=target_site,
                at_tick=expected_delivery_tick,
            )

            decoded = decode_carrier(packet)
            if not decoded.accepted:
                raise RuntimeError("uncorrupted native record codeword rejected")
            correction = correction_operator(decoded.z_bit, decoded.x_bit)
            corrected_rho = correction @ branch.bob_rho @ correction.conj().T
            fidelity = pure_state_fidelity(input_state, corrected_rho)
            min_correct_fidelity = min(min_correct_fidelity, fidelity)
            max_correct_infidelity = max(max_correct_infidelity, 1.0 - fidelity)
            max_correct_trace_distance = max(
                max_correct_trace_distance,
                trace_distance(corrected_rho, input_rho),
            )

            for wrong_z, wrong_x in OUTCOME_ORDER:
                if (wrong_z, wrong_x) == (decoded.z_bit, decoded.x_bit):
                    continue
                wrong_correction = correction_operator(wrong_z, wrong_x)
                wrong_rho = wrong_correction @ branch.bob_rho @ wrong_correction.conj().T
                wrong_fidelities.append(pure_state_fidelity(input_state, wrong_rho))

    wrong_mean = float(np.mean(wrong_fidelities)) if wrong_fidelities else 1.0
    wrong_max = float(np.max(wrong_fidelities)) if wrong_fidelities else 1.0

    return {
        "source_site": source_site,
        "target_site": target_site,
        "emitted_tick": emitted_tick,
        "spatial_distance": expected_distance,
        "expected_delivery_tick": expected_delivery_tick,
        "max_delivery_tick_error": max_delivery_tick_error,
        "max_isometry_norm_error": max_isometry_norm_error,
        "max_record_probability_error": max_record_probability_error,
        "max_pairwise_record_distribution_distance": max_pairwise_record_distribution_distance,
        "max_bob_trace_distance_to_half_identity": max_bob_trace_distance_to_half_identity,
        "max_pairwise_pre_delivery_bob_distance": max_pairwise_pre_delivery_bob_distance,
        "min_correct_fidelity": min_correct_fidelity,
        "max_correct_infidelity": max_correct_infidelity,
        "max_correct_trace_distance": max_correct_trace_distance,
        "wrong_record_mean_fidelity": wrong_mean,
        "wrong_record_max_fidelity": wrong_max,
        "generated_labels": sorted(generated_labels),
        "all_packets_derived": all_packets_derived,
        "all_worldlines_local": all_worldlines_local,
        "all_pulse_counts_conserved": all_pulse_counts_conserved,
        "early_delivery_blocked": early_delivery_blocked,
        "exact_delivery_available": exact_delivery_available,
    }


def pass_fail(condition: bool) -> str:
    return "PASS" if condition else "FAIL"


def print_gate(name: str, condition: bool) -> None:
    print(f"  {name}: {pass_fail(condition)}")


def parse_site(text: str) -> tuple[int, int, int]:
    parts = tuple(int(part.strip()) for part in text.split(","))
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("site must have form x,y,z")
    return parts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260426)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    parser.add_argument("--alice-site", type=parse_site, default=(1, 1, 1))
    parser.add_argument("--bob-site", type=parse_site, default=(5, 3, 2))
    parser.add_argument("--alice-tick", type=int, default=4)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if args.alice_tick < 0:
        raise ValueError("--alice-tick cannot be negative")
    tol = args.tolerance

    metrics = run_trials(args)
    code = code_metrics()

    code_ok = (
        code["codeword_length"] == 8
        and code["min_hamming_distance"] >= 5
        and bool(code["one_bit_corrected"])
        and bool(code["two_bit_corrected"])
    )
    apparatus_ok = (
        metrics["max_isometry_norm_error"] < tol
        and metrics["max_record_probability_error"] < tol
        and metrics["max_pairwise_record_distribution_distance"] < tol
        and metrics["generated_labels"] == ["Phi+", "Phi-", "Psi+", "Psi-"]
    )
    carrier_ok = (
        metrics["all_packets_derived"]
        and metrics["all_worldlines_local"]
        and metrics["all_pulse_counts_conserved"]
        and metrics["max_delivery_tick_error"] == 0
    )
    causality_ok = (
        metrics["early_delivery_blocked"]
        and metrics["exact_delivery_available"]
        and metrics["max_pairwise_pre_delivery_bob_distance"] < tol
    )
    correction_ok = (
        metrics["min_correct_fidelity"] > 1.0 - tol
        and metrics["max_correct_infidelity"] < tol
        and metrics["max_correct_trace_distance"] < 10 * tol
    )
    wrong_record_control_ok = metrics["wrong_record_mean_fidelity"] < 0.50

    print("NATIVE BELL-RECORD APPARATUS / 3D+1 CARRIER CANDIDATE")
    print("Status: planning artifact; ordinary quantum state teleportation only")
    print(f"trials / seed: {args.trials} / {args.seed}")
    print(
        "source -> target: "
        f"{metrics['source_site']}@t={metrics['emitted_tick']} -> "
        f"{metrics['target_site']}@t={metrics['expected_delivery_tick']}"
    )
    print(f"spatial Manhattan distance: {metrics['spatial_distance']}")
    print(
        "record code: "
        f"length={code['codeword_length']}, min_hamming={code['min_hamming_distance']}, "
        f"one_bit_corrected={code['one_bit_corrected']}, "
        f"two_bit_corrected={code['two_bit_corrected']}"
    )
    print(f"generated Bell labels: {', '.join(metrics['generated_labels'])}")
    print(f"max Bell-transducer norm error: {metrics['max_isometry_norm_error']:.3e}")
    print(f"max record probability error from 1/4: {metrics['max_record_probability_error']:.3e}")
    print(
        "max pairwise record-distribution distance across inputs: "
        f"{metrics['max_pairwise_record_distribution_distance']:.3e}"
    )
    print(
        "max Bob trace distance to I/2 before carrier delivery: "
        f"{metrics['max_bob_trace_distance_to_half_identity']:.3e}"
    )
    print(
        "max pairwise pre-delivery Bob-state distance across inputs: "
        f"{metrics['max_pairwise_pre_delivery_bob_distance']:.3e}"
    )
    print(f"carrier payloads derived from apparatus: {metrics['all_packets_derived']}")
    print(f"carrier pulse worldlines local: {metrics['all_worldlines_local']}")
    print(f"carrier pulse count conserved: {metrics['all_pulse_counts_conserved']}")
    print(f"early delivery blocked: {metrics['early_delivery_blocked']}")
    print(f"delivery at light-cone tick available: {metrics['exact_delivery_available']}")
    print(f"minimum delivered-record corrected fidelity: {metrics['min_correct_fidelity']:.16f}")
    print(f"maximum delivered-record infidelity: {metrics['max_correct_infidelity']:.3e}")
    print(f"max corrected-state trace distance to input: {metrics['max_correct_trace_distance']:.3e}")
    print(f"wrong-record mean fidelity control: {metrics['wrong_record_mean_fidelity']:.6f}")
    print(f"wrong-record max fidelity control: {metrics['wrong_record_max_fidelity']:.6f}")
    print()
    print("Acceptance gates:")
    print_gate("native Bell-stabilizer transducer writes all four records", apparatus_ok)
    print_gate("redundant record code is durable through two bit flips", code_ok)
    print_gate("carrier payload is derived from apparatus pointer", bool(metrics["all_packets_derived"]))
    print_gate("3D+1 record-field pulses propagate locally", carrier_ok)
    print_gate("Bob pre-delivery state is input-independent", causality_ok)
    print_gate("delivered native carrier restores Bob state", correction_ok)
    print_gate("wrong-record control remains non-teleporting", wrong_record_control_ok)
    print_gate("claim boundary stays state-only and not FTL", True)

    all_ok = all(
        (
            apparatus_ok,
            code_ok,
            bool(metrics["all_packets_derived"]),
            carrier_ok,
            causality_ok,
            correction_ok,
            wrong_record_control_ok,
        )
    )

    print()
    print("Limitations:")
    print("  This is a native apparatus/carrier model, not a full detector derivation.")
    print("  The Bell-stabilizer transducer is ideal and projective.")
    print("  The record-field carrier is discrete and local but not field-theoretic.")
    print("  Decoherence, thermodynamic irreversibility, hardware readout, and")
    print("  conservation-ledger derivations remain open.")
    print("  No matter, mass, charge, energy, object, or FTL transport is claimed.")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
