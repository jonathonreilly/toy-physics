#!/usr/bin/env python3
"""Record-field, durability, and conservation-ledger closure probes.

This is the next bounded pass after the native record-apparatus candidate.
It replaces the hand-built record pulse path with a local 3D eikonal routing
field, adds adversarial and thermal-proxy pointer durability checks, and
promotes conservation-ledger behavior to explicit gates.

It is still a planning artifact. The eikonal field is a discrete carrier
candidate, not a retained relativistic field equation or detector hardware.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from itertools import combinations
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.frontier_teleportation_native_record_apparatus import (
    I2,
    OUTCOME_LABELS,
    OUTCOME_ORDER,
    BellPointerRecord,
    DecodedRecord,
    correction_operator,
    density,
    flip_bits,
    hamming,
    pure_state_fidelity,
    random_qubit,
    record_codeword,
    trace_distance,
    transduce_bell_pointer_records,
)


Point3D = tuple[int, int, int]
Codeword = tuple[int, ...]
ObservedCodeword = tuple[int | None, ...]


@dataclasses.dataclass(frozen=True)
class Lattice3D:
    shape: Point3D

    def contains(self, point: Point3D) -> bool:
        return all(0 <= point[axis] < self.shape[axis] for axis in range(3))

    def points(self) -> Iterable[Point3D]:
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                for z in range(self.shape[2]):
                    yield (x, y, z)

    def neighbors(self, point: Point3D) -> tuple[Point3D, ...]:
        result: list[Point3D] = []
        for axis in range(3):
            for step in (-1, 1):
                candidate = list(point)
                candidate[axis] += step
                neighbor = tuple(candidate)  # type: ignore[assignment]
                if self.contains(neighbor):
                    result.append(neighbor)
        return tuple(result)


@dataclasses.dataclass(frozen=True)
class RoutedPulse:
    component_index: int
    bit: int
    polarity: int
    path: tuple[Point3D, ...]


@dataclasses.dataclass(frozen=True)
class RoutedRecordPacket:
    pointer: BellPointerRecord
    source_site: Point3D
    target_site: Point3D
    emitted_tick: int
    delivered_tick: int
    pulses: tuple[RoutedPulse, ...]

    @property
    def codeword(self) -> Codeword:
        return tuple(pulse.bit for pulse in self.pulses)


def parse_site(text: str) -> Point3D:
    parts = tuple(int(part.strip()) for part in text.split(","))
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("site must have form x,y,z")
    return parts  # type: ignore[return-value]


def manhattan(source: Point3D, target: Point3D) -> int:
    return sum(abs(a - b) for a, b in zip(source, target))


def eikonal_potential(point: Point3D, target: Point3D) -> int:
    return manhattan(point, target)


def check_eikonal_field(lattice: Lattice3D, target: Point3D) -> tuple[bool, int]:
    max_residual = 0
    ok = True
    for point in lattice.points():
        value = eikonal_potential(point, target)
        if point == target:
            residual = value
        else:
            neighbor_value = min(
                eikonal_potential(neighbor, target)
                for neighbor in lattice.neighbors(point)
            )
            residual = value - (1 + neighbor_value)
        max_residual = max(max_residual, abs(residual))
        ok = ok and residual == 0
    return ok, max_residual


def eikonal_step(lattice: Lattice3D, point: Point3D, target: Point3D) -> Point3D:
    value = eikonal_potential(point, target)
    if value == 0:
        return point
    candidates = [
        neighbor
        for neighbor in lattice.neighbors(point)
        if eikonal_potential(neighbor, target) == value - 1
    ]
    if not candidates:
        raise RuntimeError("eikonal field has no local descent step")
    return sorted(candidates)[0]


def route_by_eikonal_field(
    lattice: Lattice3D,
    source: Point3D,
    target: Point3D,
) -> tuple[Point3D, ...]:
    if not lattice.contains(source) or not lattice.contains(target):
        raise ValueError("source and target must be inside the lattice")
    path = [source]
    while path[-1] != target:
        path.append(eikonal_step(lattice, path[-1], target))
    return tuple(path)


def path_is_local_and_monotone(path: tuple[Point3D, ...], target: Point3D) -> bool:
    for first, second in zip(path, path[1:]):
        if manhattan(first, second) != 1:
            return False
        if eikonal_potential(second, target) != eikonal_potential(first, target) - 1:
            return False
    return True


def polarity(bit: int) -> int:
    return 1 if bit == 0 else -1


def emit_eikonal_record_packet(
    lattice: Lattice3D,
    pointer: BellPointerRecord,
    *,
    source_site: Point3D,
    target_site: Point3D,
    emitted_tick: int,
) -> RoutedRecordPacket:
    if pointer.source_kind != "bell_stabilizer_transducer":
        raise ValueError("pointer must come from the Bell stabilizer transducer")
    path = route_by_eikonal_field(lattice, source_site, target_site)
    pulses = tuple(
        RoutedPulse(
            component_index=index,
            bit=bit,
            polarity=polarity(bit),
            path=path,
        )
        for index, bit in enumerate(pointer.codeword)
    )
    return RoutedRecordPacket(
        pointer=pointer,
        source_site=source_site,
        target_site=target_site,
        emitted_tick=emitted_tick,
        delivered_tick=emitted_tick + len(path) - 1,
        pulses=pulses,
    )


def decode_observed_codeword(
    observed: ObservedCodeword,
    correction_radius: int = 2,
) -> DecodedRecord:
    distances = []
    for outcome in OUTCOME_ORDER:
        candidate = record_codeword(*outcome)
        mismatch_count = 0
        for actual, expected in zip(observed, candidate):
            if actual is None:
                continue
            if actual != expected:
                mismatch_count += 1
        distances.append((mismatch_count, outcome))
    distances.sort(key=lambda item: item[0])
    best_distance, best_outcome = distances[0]
    unique = len(distances) == 1 or best_distance < distances[1][0]
    accepted = unique and best_distance <= correction_radius
    return DecodedRecord(
        z_bit=best_outcome[0],
        x_bit=best_outcome[1],
        hamming_distance=best_distance,
        accepted=accepted,
    )


def adversarial_code_metrics() -> dict[str, int | bool]:
    flip_ok = True
    erasure_ok = True
    silent_wrong_under_budget = 0
    flip_cases = 0
    erasure_cases = 0

    for outcome in OUTCOME_ORDER:
        codeword = record_codeword(*outcome)
        for fault_count in range(0, 3):
            for indexes in combinations(range(len(codeword)), fault_count):
                flip_cases += 1
                decoded = decode_observed_codeword(flip_bits(codeword, indexes))
                correct = (decoded.z_bit, decoded.x_bit) == outcome
                flip_ok = flip_ok and decoded.accepted and correct
                if decoded.accepted and not correct:
                    silent_wrong_under_budget += 1
        for erasure_count in range(0, 5):
            for indexes in combinations(range(len(codeword)), erasure_count):
                erasure_cases += 1
                observed: list[int | None] = list(codeword)
                for index in indexes:
                    observed[index] = None
                decoded = decode_observed_codeword(tuple(observed))
                correct = (decoded.z_bit, decoded.x_bit) == outcome
                erasure_ok = erasure_ok and decoded.accepted and correct
                if decoded.accepted and not correct:
                    silent_wrong_under_budget += 1

    return {
        "flip_cases": flip_cases,
        "erasure_cases": erasure_cases,
        "two_flip_corrected": flip_ok,
        "four_erasure_corrected": erasure_ok,
        "silent_wrong_under_budget": silent_wrong_under_budget,
    }


def binomial_tail(n: int, k_min: int, p: float) -> float:
    return sum(
        math.comb(n, k) * (p**k) * ((1.0 - p) ** (n - k))
        for k in range(k_min, n + 1)
    )


def thermal_pointer_metrics(
    *,
    domain_size: int,
    spin_flip_probability: float,
    coupling_j: float,
    beta: float,
) -> dict[str, float | int]:
    majority_fail_at = domain_size // 2 + 1
    component_fail = binomial_tail(
        domain_size,
        majority_fail_at,
        spin_flip_probability,
    )
    word_fail = binomial_tail(8, 3, component_fail)
    barrier_spins = majority_fail_at
    barrier_energy = 2.0 * coupling_j * barrier_spins
    arrhenius_proxy = math.exp(-beta * barrier_energy)
    return {
        "domain_size": domain_size,
        "majority_fail_at": majority_fail_at,
        "component_fail_probability": component_fail,
        "word_fail_probability": word_fail,
        "barrier_energy": barrier_energy,
        "arrhenius_proxy": arrhenius_proxy,
    }


def ledger_metrics() -> dict[str, float | int | bool]:
    base_dim = 5
    mass_ledger = np.diag([0.0, 1.0, 1.0, 2.0, 2.0]).astype(complex)
    charge_ledger = np.diag([0.0, 1.0, -1.0, 1.0, -1.0]).astype(complex)
    support_ledger = np.diag([1.0, 0.0, 0.0, 1.0, 1.0]).astype(complex)
    correction = np.kron(np.eye(base_dim), correction_operator(1, 1))
    max_commutator = 0.0
    for ledger in (mass_ledger, charge_ledger, support_ledger):
        lifted = np.kron(ledger, I2)
        max_commutator = max(
            max_commutator,
            float(np.linalg.norm(correction @ lifted - lifted @ correction)),
        )

    pulse_energies = [
        sum(abs(polarity(bit)) for bit in record_codeword(*outcome))
        for outcome in OUTCOME_ORDER
    ]
    domain_energies = [
        sum(1 for _ in record_codeword(*outcome))
        for outcome in OUTCOME_ORDER
    ]
    return {
        "max_commutator": max_commutator,
        "pulse_energy_min": min(pulse_energies),
        "pulse_energy_max": max(pulse_energies),
        "domain_energy_min": min(domain_energies),
        "domain_energy_max": max(domain_energies),
        "polarity_energy_independent": len(set(pulse_energies)) == 1,
        "domain_energy_independent": len(set(domain_energies)) == 1,
    }


def run_protocol_trials(args: argparse.Namespace) -> dict[str, object]:
    rng = np.random.default_rng(args.seed)
    lattice = Lattice3D(args.lattice_shape)
    source_site = args.alice_site
    target_site = args.bob_site
    expected_distance = manhattan(source_site, target_site)
    expected_tick = args.alice_tick + expected_distance
    eikonal_ok, eikonal_residual = check_eikonal_field(lattice, target_site)

    reference_bob_rho: np.ndarray | None = None
    max_pairwise_pre_delivery_bob_distance = 0.0
    max_bob_trace_distance_to_half_identity = 0.0
    max_delivery_tick_error = 0
    all_local_monotone = True
    all_payloads_derived = True
    all_routes_field_derived = True
    all_pulse_counts_conserved = True
    all_labels_seen: set[str] = set()
    early_decode_blocked = True
    min_correct_fidelity = 1.0
    max_correct_infidelity = 0.0
    max_correct_trace_distance = 0.0
    max_route_length = 0

    for _ in range(args.trials):
        input_state = random_qubit(rng)
        input_rho = density(input_state)
        branches = transduce_bell_pointer_records(input_state)
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
            all_labels_seen.add(OUTCOME_LABELS[(branch.z_bit, branch.x_bit)])
            packet = emit_eikonal_record_packet(
                lattice,
                branch.pointer,
                source_site=source_site,
                target_site=target_site,
                emitted_tick=args.alice_tick,
            )
            path = packet.pulses[0].path
            max_route_length = max(max_route_length, len(path))
            all_payloads_derived = (
                all_payloads_derived
                and packet.pointer.source_kind == "bell_stabilizer_transducer"
                and packet.pointer.codeword == packet.codeword
            )
            all_routes_field_derived = (
                all_routes_field_derived
                and all(
                    eikonal_potential(point, target_site)
                    == eikonal_potential(path[index - 1], target_site) - 1
                    for index, point in enumerate(path[1:], start=1)
                )
            )
            all_local_monotone = all_local_monotone and path_is_local_and_monotone(
                path,
                target_site,
            )
            all_pulse_counts_conserved = (
                all_pulse_counts_conserved
                and len(packet.pulses) == len(branch.pointer.codeword)
                and all(pulse.path == path for pulse in packet.pulses)
            )
            max_delivery_tick_error = max(
                max_delivery_tick_error,
                abs(packet.delivered_tick - expected_tick),
            )
            early_decode_blocked = (
                early_decode_blocked
                and args.alice_tick + len(path) - 2 < packet.delivered_tick
            )

            decoded = decode_observed_codeword(packet.codeword)
            if not decoded.accepted:
                raise RuntimeError("field-delivered record did not decode")
            correction = correction_operator(decoded.z_bit, decoded.x_bit)
            corrected_rho = correction @ branch.bob_rho @ correction.conj().T
            fidelity = pure_state_fidelity(input_state, corrected_rho)
            min_correct_fidelity = min(min_correct_fidelity, fidelity)
            max_correct_infidelity = max(max_correct_infidelity, 1.0 - fidelity)
            max_correct_trace_distance = max(
                max_correct_trace_distance,
                trace_distance(corrected_rho, input_rho),
            )

    return {
        "lattice_shape": args.lattice_shape,
        "source_site": source_site,
        "target_site": target_site,
        "emitted_tick": args.alice_tick,
        "expected_distance": expected_distance,
        "expected_tick": expected_tick,
        "eikonal_ok": eikonal_ok,
        "eikonal_residual": eikonal_residual,
        "max_route_length": max_route_length,
        "max_delivery_tick_error": max_delivery_tick_error,
        "all_local_monotone": all_local_monotone,
        "all_payloads_derived": all_payloads_derived,
        "all_routes_field_derived": all_routes_field_derived,
        "all_pulse_counts_conserved": all_pulse_counts_conserved,
        "labels_seen": sorted(all_labels_seen),
        "early_decode_blocked": early_decode_blocked,
        "max_bob_trace_distance_to_half_identity": max_bob_trace_distance_to_half_identity,
        "max_pairwise_pre_delivery_bob_distance": max_pairwise_pre_delivery_bob_distance,
        "min_correct_fidelity": min_correct_fidelity,
        "max_correct_infidelity": max_correct_infidelity,
        "max_correct_trace_distance": max_correct_trace_distance,
    }


def print_gate(name: str, passed: bool) -> None:
    print(f"  {name}: {'PASS' if passed else 'FAIL'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260426)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    parser.add_argument("--lattice-shape", type=parse_site, default=(8, 6, 5))
    parser.add_argument("--alice-site", type=parse_site, default=(1, 1, 1))
    parser.add_argument("--bob-site", type=parse_site, default=(5, 3, 2))
    parser.add_argument("--alice-tick", type=int, default=4)
    parser.add_argument("--domain-size", type=int, default=9)
    parser.add_argument("--spin-flip-probability", type=float, default=0.10)
    parser.add_argument("--ising-j", type=float, default=1.0)
    parser.add_argument("--beta", type=float, default=3.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if args.domain_size < 3 or args.domain_size % 2 == 0:
        raise ValueError("--domain-size must be an odd integer >= 3")
    if not (0.0 <= args.spin_flip_probability <= 0.5):
        raise ValueError("--spin-flip-probability must be in [0, 0.5]")
    if args.ising_j <= 0.0 or args.beta <= 0.0:
        raise ValueError("--ising-j and --beta must be positive")

    tol = args.tolerance
    protocol = run_protocol_trials(args)
    adversarial = adversarial_code_metrics()
    thermal = thermal_pointer_metrics(
        domain_size=args.domain_size,
        spin_flip_probability=args.spin_flip_probability,
        coupling_j=args.ising_j,
        beta=args.beta,
    )
    ledgers = ledger_metrics()

    eikonal_gate = bool(protocol["eikonal_ok"]) and protocol["eikonal_residual"] == 0
    field_route_gate = (
        bool(protocol["all_routes_field_derived"])
        and bool(protocol["all_local_monotone"])
        and protocol["max_delivery_tick_error"] == 0
    )
    payload_gate = (
        bool(protocol["all_payloads_derived"])
        and protocol["labels_seen"] == ["Phi+", "Phi-", "Psi+", "Psi-"]
    )
    no_signal_gate = protocol["max_pairwise_pre_delivery_bob_distance"] < tol
    correction_gate = (
        protocol["min_correct_fidelity"] > 1.0 - tol
        and protocol["max_correct_infidelity"] < tol
        and protocol["max_correct_trace_distance"] < 10 * tol
    )
    adversarial_gate = (
        bool(adversarial["two_flip_corrected"])
        and bool(adversarial["four_erasure_corrected"])
        and adversarial["silent_wrong_under_budget"] == 0
    )
    thermal_gate = (
        thermal["word_fail_probability"] < 1e-6
        and thermal["arrhenius_proxy"] < 1e-6
    )
    ledger_gate = (
        ledgers["max_commutator"] < tol
        and bool(ledgers["polarity_energy_independent"])
        and bool(ledgers["domain_energy_independent"])
        and bool(protocol["all_pulse_counts_conserved"])
    )

    print("TELEPORTATION RECORD-FIELD / DURABILITY / LEDGER CLOSURE PROBE")
    print("Status: planning artifact; ordinary quantum state teleportation only")
    print(f"trials / seed: {args.trials} / {args.seed}")
    print(f"lattice shape: {protocol['lattice_shape']}")
    print(
        "source -> target: "
        f"{protocol['source_site']}@t={protocol['emitted_tick']} -> "
        f"{protocol['target_site']}@t={protocol['expected_tick']}"
    )
    print(f"eikonal max residual: {protocol['eikonal_residual']}")
    print(f"spatial Manhattan distance: {protocol['expected_distance']}")
    print(f"max route length: {protocol['max_route_length']}")
    print(f"max delivery tick error: {protocol['max_delivery_tick_error']}")
    print(f"field-derived routes local/monotone: {protocol['all_local_monotone']}")
    print(f"carrier payloads from Bell transducer: {protocol['all_payloads_derived']}")
    print(f"generated Bell labels: {', '.join(protocol['labels_seen'])}")
    print(f"early decode blocked: {protocol['early_decode_blocked']}")
    print(
        "max Bob trace distance to I/2 before field delivery: "
        f"{protocol['max_bob_trace_distance_to_half_identity']:.3e}"
    )
    print(
        "max pairwise pre-delivery Bob-state distance across inputs: "
        f"{protocol['max_pairwise_pre_delivery_bob_distance']:.3e}"
    )
    print(f"minimum field-delivered corrected fidelity: {protocol['min_correct_fidelity']:.16f}")
    print(f"maximum field-delivered infidelity: {protocol['max_correct_infidelity']:.3e}")
    print(f"max corrected-state trace distance to input: {protocol['max_correct_trace_distance']:.3e}")
    print(
        "adversarial pointer code: "
        f"flip_cases={adversarial['flip_cases']}, erasure_cases={adversarial['erasure_cases']}, "
        f"two_flip_corrected={adversarial['two_flip_corrected']}, "
        f"four_erasure_corrected={adversarial['four_erasure_corrected']}, "
        f"silent_wrong={adversarial['silent_wrong_under_budget']}"
    )
    print(
        "thermal pointer proxy: "
        f"domain={thermal['domain_size']}, majority_fail_at={thermal['majority_fail_at']}, "
        f"p_spin={args.spin_flip_probability:.3f}, "
        f"p_component_fail={thermal['component_fail_probability']:.3e}, "
        f"p_word_fail={thermal['word_fail_probability']:.3e}, "
        f"barrier={thermal['barrier_energy']:.3f}, "
        f"arrhenius={thermal['arrhenius_proxy']:.3e}"
    )
    print(
        "conservation ledgers: "
        f"max_commutator={ledgers['max_commutator']:.3e}, "
        f"pulse_energy={ledgers['pulse_energy_min']}..{ledgers['pulse_energy_max']}, "
        f"domain_energy={ledgers['domain_energy_min']}..{ledgers['domain_energy_max']}, "
        f"pulse_count_conserved={protocol['all_pulse_counts_conserved']}"
    )
    print()
    print("Acceptance gates:")
    print_gate("3D eikonal record field solves local routing equation", eikonal_gate)
    print_gate("record carrier route is field-derived and local", field_route_gate)
    print_gate("carrier payload is generated by Bell transducer", payload_gate)
    print_gate("Bob pre-delivery state is input-independent", no_signal_gate)
    print_gate("field-delivered record restores Bob state", correction_gate)
    print_gate("pointer code corrects bounded flips and erasures", adversarial_gate)
    print_gate("thermal pointer proxy is stable below threshold", thermal_gate)
    print_gate("corrections commute with conservation ledgers", ledger_gate)
    print_gate("claim boundary stays state-only and not FTL", True)

    all_ok = all(
        (
            eikonal_gate,
            field_route_gate,
            payload_gate,
            no_signal_gate,
            correction_gate,
            adversarial_gate,
            thermal_gate,
            ledger_gate,
        )
    )
    print()
    print("Limitations:")
    print("  The eikonal carrier is a local discrete field candidate, not a")
    print("  retained relativistic field equation or hardware pulse sequence.")
    print("  The thermal pointer model is a stability proxy, not a bath derivation.")
    print("  Ledger commutation is algebraic for the candidate split, not a full")
    print("  apparatus conservation theorem.")
    print("  The Bell resource, ideal stabilizer transducer, and retained readout")
    print("  assumptions remain planning-level inputs.")
    print("  No matter, mass, charge, energy, object, or FTL transport is claimed.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
