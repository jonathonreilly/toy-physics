#!/usr/bin/env python3
"""Causal classical-record channel harness for teleportation.

This is a narrow harness for the Bell-measurement record used by ordinary
qubit teleportation. The directed lattice/DAG below schedules explicit
classical bits with positive latency. It does not derive the bits, and it does
not model faster-than-light signaling or transport of matter.
"""

from __future__ import annotations

import argparse
import dataclasses
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

Point = tuple[int, int]


class DuplicateRecordError(ValueError):
    """Raised when a Bell record id is reused."""


@dataclasses.dataclass(frozen=True)
class DirectedLatticeDAG:
    """A finite 2D directed lattice with edges only in +x and +y."""

    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("lattice dimensions must be positive")

    def route(self, source: Point, target: Point) -> tuple[Point, ...]:
        if not self.contains(source) or not self.contains(target):
            raise ValueError("source and target must be inside the lattice")
        if target[0] < source[0] or target[1] < source[1]:
            raise ValueError("directed lattice route must move only in +x/+y")

        path = [source]
        x, y = source
        while x < target[0]:
            x += 1
            path.append((x, y))
        while y < target[1]:
            y += 1
            path.append((x, y))

        if len(path) < 2:
            raise ValueError("record route must have positive latency")
        if not self.is_valid_dag_route(path):
            raise ValueError("route is not a directed acyclic lattice path")
        return tuple(path)

    def contains(self, point: Point) -> bool:
        return 0 <= point[0] < self.width and 0 <= point[1] < self.height

    @staticmethod
    def is_valid_dag_route(path: Iterable[Point]) -> bool:
        points = tuple(path)
        if len(points) < 2 or len(set(points)) != len(points):
            return False
        for first, second in zip(points, points[1:]):
            dx = second[0] - first[0]
            dy = second[1] - first[1]
            if (dx, dy) not in ((1, 0), (0, 1)):
                return False
            if sum(second) <= sum(first):
                return False
        return True


@dataclasses.dataclass(frozen=True)
class BellRecord:
    """Explicit two-bit Bell record moving on the causal channel."""

    record_id: str
    sender: str
    receiver: str
    source: Point
    target: Point
    route: tuple[Point, ...]
    created_at_tick: int
    deliver_at_tick: int
    z_bit: int
    x_bit: int
    extra_delay_ticks: int = 0
    derived_by_channel: bool = False

    @property
    def label(self) -> str:
        return OUTCOME_LABELS[(self.z_bit, self.x_bit)]

    @property
    def path_latency_ticks(self) -> int:
        return len(self.route) - 1

    @property
    def minimal_deliver_at_tick(self) -> int:
        return self.created_at_tick + self.path_latency_ticks


class CausalBellRecordChannel:
    """Exactly-once channel for explicit two-bit records."""

    def __init__(self, dag: DirectedLatticeDAG) -> None:
        self.dag = dag
        self.current_tick = 0
        self._in_flight: dict[str, BellRecord] = {}
        self._used_record_ids: set[str] = set()
        self._delivered_record_ids: set[str] = set()

    def advance_to(self, tick: int) -> None:
        if tick < self.current_tick:
            raise ValueError("channel time cannot run backward")
        self.current_tick = tick

    def send(
        self,
        *,
        record_id: str,
        sender: str,
        receiver: str,
        z_bit: int,
        x_bit: int,
        source: Point,
        target: Point,
        extra_delay_ticks: int = 0,
    ) -> BellRecord:
        if record_id in self._used_record_ids:
            raise DuplicateRecordError(f"duplicate Bell record id: {record_id}")
        if z_bit not in (0, 1) or x_bit not in (0, 1):
            raise ValueError("Bell record bits must be binary")
        if extra_delay_ticks < 0:
            raise ValueError("extra_delay_ticks cannot be negative")

        route = self.dag.route(source, target)
        path_latency = len(route) - 1
        if path_latency <= 0:
            raise ValueError("Bell record must have positive causal latency")

        record = BellRecord(
            record_id=record_id,
            sender=sender,
            receiver=receiver,
            source=source,
            target=target,
            route=route,
            created_at_tick=self.current_tick,
            deliver_at_tick=self.current_tick + path_latency + extra_delay_ticks,
            z_bit=z_bit,
            x_bit=x_bit,
            extra_delay_ticks=extra_delay_ticks,
        )
        self._in_flight[record.record_id] = record
        self._used_record_ids.add(record.record_id)
        return record

    def receive(self, *, receiver: str, at_node: Point) -> list[BellRecord]:
        delivered: list[BellRecord] = []
        for record in tuple(self._in_flight.values()):
            if record.receiver != receiver or record.target != at_node:
                continue
            if record.deliver_at_tick > self.current_tick:
                continue
            delivered.append(record)
            del self._in_flight[record.record_id]
            self._delivered_record_ids.add(record.record_id)
        return delivered

    def pending_count(self) -> int:
        return len(self._in_flight)


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


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


def prepare_three_register_state(input_state: np.ndarray) -> np.ndarray:
    """Prepare |psi>_A tensor |Phi+>_R,B in A,R,B order."""
    return np.kron(input_state, bell_state(0, 0))


def bob_reduced_from_three_register_state(state: np.ndarray) -> np.ndarray:
    """Trace out Alice's A,R registers from a pure A,R,B state."""
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
        raise ValueError("Bell branch has zero probability")
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
    diff = first - second
    diff = 0.5 * (diff + diff.conj().T)
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def no_signaling_probe_states() -> tuple[np.ndarray, ...]:
    theta = math.acos(1.0 / math.sqrt(3.0))
    phi = math.pi / 4.0
    tetrahedral = np.array(
        [
            math.cos(theta / 2.0),
            complex(math.cos(phi), math.sin(phi)) * math.sin(theta / 2.0),
        ],
        dtype=complex,
    )
    return (
        np.array([1.0, 0.0], dtype=complex),
        np.array([0.0, 1.0], dtype=complex),
        normalize(np.array([1.0, 1.0], dtype=complex)),
        normalize(np.array([1.0, 1.0j], dtype=complex)),
        normalize(tetrahedral),
    )


def run_bob_no_signaling_probe() -> dict[str, object]:
    half_identity = 0.5 * I2
    max_before_measurement_distance = 0.0
    max_before_delivery_distance = 0.0
    max_pairwise_before_delivery_distance = 0.0
    max_bell_probability_error = 0.0
    reference_before_delivery: np.ndarray | None = None

    for input_state in no_signaling_probe_states():
        three_register_state = prepare_three_register_state(input_state)
        rho_before_measurement = bob_reduced_from_three_register_state(three_register_state)
        max_before_measurement_distance = max(
            max_before_measurement_distance,
            trace_distance(rho_before_measurement, half_identity),
        )

        rho_before_delivery = np.zeros((2, 2), dtype=complex)
        for z_bit, x_bit in OUTCOME_ORDER:
            probability, _, bob_rho = project_bell_branch(
                three_register_state, z_bit, x_bit
            )
            max_bell_probability_error = max(
                max_bell_probability_error,
                abs(probability - 0.25),
            )
            rho_before_delivery += probability * bob_rho

        max_before_delivery_distance = max(
            max_before_delivery_distance,
            trace_distance(rho_before_delivery, half_identity),
        )
        if reference_before_delivery is None:
            reference_before_delivery = rho_before_delivery
        else:
            max_pairwise_before_delivery_distance = max(
                max_pairwise_before_delivery_distance,
                trace_distance(rho_before_delivery, reference_before_delivery),
            )

    return {
        "probe_count": len(no_signaling_probe_states()),
        "max_before_measurement_distance": max_before_measurement_distance,
        "max_before_delivery_distance": max_before_delivery_distance,
        "max_pairwise_before_delivery_distance": max_pairwise_before_delivery_distance,
        "max_bell_probability_error": max_bell_probability_error,
    }


def run_channel_harness() -> dict[str, object]:
    dag = DirectedLatticeDAG(width=4, height=2)
    alice_node = (0, 0)
    bob_node = (3, 1)
    channel = CausalBellRecordChannel(dag)

    input_state = no_signaling_probe_states()[-1]
    three_register_state = prepare_three_register_state(input_state)
    z_bit, x_bit = (1, 1)
    probability, bob_state, _ = project_bell_branch(three_register_state, z_bit, x_bit)

    channel.advance_to(7)
    sent = channel.send(
        record_id="bell-record-0001",
        sender="Alice",
        receiver="Bob",
        z_bit=z_bit,
        x_bit=x_bit,
        source=alice_node,
        target=bob_node,
    )
    positive_latency = sent.deliver_at_tick > sent.created_at_tick

    try:
        channel.send(
            record_id=sent.record_id,
            sender="Alice",
            receiver="Bob",
            z_bit=z_bit,
            x_bit=x_bit,
            source=alice_node,
            target=bob_node,
        )
        duplicate_id_rejected = False
    except DuplicateRecordError:
        duplicate_id_rejected = True

    early_tick = sent.deliver_at_tick - 1
    channel.advance_to(early_tick)
    early_records = channel.receive(receiver="Bob", at_node=bob_node)
    early_delivery_blocked = len(early_records) == 0 and channel.pending_count() == 1

    channel.advance_to(sent.deliver_at_tick)
    wrong_receiver_records = channel.receive(receiver="Mallory", at_node=bob_node)
    wrong_receiver_blocked = (
        len(wrong_receiver_records) == 0 and channel.pending_count() == 1
    )
    delivered_records = channel.receive(receiver="Bob", at_node=bob_node)
    duplicate_delivery_records = channel.receive(receiver="Bob", at_node=bob_node)
    delivered_once = (
        len(delivered_records) == 1
        and len(duplicate_delivery_records) == 0
        and channel.pending_count() == 0
    )

    delivered = delivered_records[0] if delivered_records else sent
    corrected = correction_operator(delivered.z_bit, delivered.x_bit) @ bob_state
    correct_fidelity = state_fidelity(input_state, corrected)

    wrong_z_bit = delivered.z_bit ^ 1
    wrong_corrected = correction_operator(wrong_z_bit, delivered.x_bit) @ bob_state
    wrong_bit_fidelity = state_fidelity(input_state, wrong_corrected)

    delayed_channel = CausalBellRecordChannel(dag)
    delayed_channel.advance_to(20)
    delayed = delayed_channel.send(
        record_id="bell-record-delayed-control",
        sender="Alice",
        receiver="Bob",
        z_bit=z_bit,
        x_bit=x_bit,
        source=alice_node,
        target=bob_node,
        extra_delay_ticks=2,
    )
    delayed_channel.advance_to(delayed.minimal_deliver_at_tick)
    delayed_base_records = delayed_channel.receive(receiver="Bob", at_node=bob_node)
    delayed_blocked_at_base = (
        len(delayed_base_records) == 0 and delayed_channel.pending_count() == 1
    )
    delayed_channel.advance_to(delayed.deliver_at_tick)
    delayed_late_records = delayed_channel.receive(receiver="Bob", at_node=bob_node)
    delayed_delivered_late = (
        len(delayed_late_records) == 1 and delayed_channel.pending_count() == 0
    )

    return {
        "dag_width": dag.width,
        "dag_height": dag.height,
        "route": sent.route,
        "record_id": sent.record_id,
        "record_label": sent.label,
        "record_bits": (sent.z_bit, sent.x_bit),
        "created_at_tick": sent.created_at_tick,
        "deliver_at_tick": sent.deliver_at_tick,
        "path_latency_ticks": sent.path_latency_ticks,
        "channel_derives_bits": sent.derived_by_channel,
        "positive_latency": positive_latency,
        "early_tick": early_tick,
        "early_delivery_blocked": early_delivery_blocked,
        "wrong_receiver_blocked": wrong_receiver_blocked,
        "duplicate_id_rejected": duplicate_id_rejected,
        "delivered_once": delivered_once,
        "branch_probability": probability,
        "correct_fidelity": correct_fidelity,
        "wrong_bit_fidelity": wrong_bit_fidelity,
        "delayed_extra_ticks": delayed.extra_delay_ticks,
        "delayed_minimal_deliver_at_tick": delayed.minimal_deliver_at_tick,
        "delayed_deliver_at_tick": delayed.deliver_at_tick,
        "delayed_blocked_at_base": delayed_blocked_at_base,
        "delayed_delivered_late": delayed_delivered_late,
    }


def print_summary(
    channel: dict[str, object],
    no_signal: dict[str, object],
    tolerance: float,
    wrong_fidelity_ceiling: float,
) -> bool:
    print("TELEPORTATION BELL-RECORD CAUSAL CHANNEL HARNESS")
    print("Status: planning / first artifact; explicit classical record only")
    print()

    print("Directed lattice DAG:")
    print(f"  lattice: {channel['dag_width']} x {channel['dag_height']}")
    print(f"  route Alice->Bob: {channel['route']}")
    print(f"  path latency ticks: {channel['path_latency_ticks']}")
    print()

    print("Explicit Bell record:")
    print(
        "  record: "
        f"{channel['record_label']} bits(z,x)={channel['record_bits']} "
        f"created t={channel['created_at_tick']} "
        f"deliver t={channel['deliver_at_tick']}"
    )
    print(f"  channel derives Bell bits: {channel['channel_derives_bits']}")
    print(f"  Bell branch probability: {channel['branch_probability']:.16f}")
    print()

    print("Causal channel checks:")
    print(f"  positive latency: {channel['positive_latency']}")
    print(
        f"  receive at t={channel['early_tick']} blocked: "
        f"{channel['early_delivery_blocked']}"
    )
    print(f"  wrong receiver blocked: {channel['wrong_receiver_blocked']}")
    print(f"  duplicate record id rejected: {channel['duplicate_id_rejected']}")
    print(f"  receive at delivery exactly once: {channel['delivered_once']}")
    print(
        "  delayed control blocked at base arrival: "
        f"{channel['delayed_blocked_at_base']} "
        f"(base t={channel['delayed_minimal_deliver_at_tick']}, "
        f"actual t={channel['delayed_deliver_at_tick']})"
    )
    print(f"  delayed control delivered late: {channel['delayed_delivered_late']}")
    print()

    print("Correction controls:")
    print(f"  correct-record fidelity: {channel['correct_fidelity']:.16f}")
    print(f"  wrong-bit control fidelity: {channel['wrong_bit_fidelity']:.16f}")
    print()

    print("Bob no-signaling before record delivery:")
    print(f"  probe states: {no_signal['probe_count']}")
    print(
        "  max Bob trace distance to I/2 before Alice measurement: "
        f"{no_signal['max_before_measurement_distance']:.3e}"
    )
    print(
        "  max Bob trace distance to I/2 after Alice measurement before delivery: "
        f"{no_signal['max_before_delivery_distance']:.3e}"
    )
    print(
        "  max pairwise pre-delivery Bob-state distance across inputs: "
        f"{no_signal['max_pairwise_before_delivery_distance']:.3e}"
    )
    print(
        "  max Bell probability error from 1/4: "
        f"{no_signal['max_bell_probability_error']:.3e}"
    )
    print()

    pass_checks = {
        "explicit not derived record channel": not channel["channel_derives_bits"],
        "positive channel latency": bool(channel["positive_latency"]),
        "no early delivery": bool(channel["early_delivery_blocked"]),
        "duplicate prevention": bool(
            channel["duplicate_id_rejected"] and channel["delivered_once"]
        ),
        "wrong/delayed record controls": bool(
            channel["wrong_receiver_blocked"]
            and channel["wrong_bit_fidelity"] < wrong_fidelity_ceiling
            and channel["delayed_blocked_at_base"]
            and channel["delayed_delivered_late"]
        ),
        "post-delivery correction": bool(1.0 - channel["correct_fidelity"] < tolerance),
        "Bob pre-delivery no-signaling": bool(
            no_signal["max_before_measurement_distance"] < tolerance
            and no_signal["max_before_delivery_distance"] < tolerance
            and no_signal["max_pairwise_before_delivery_distance"] < tolerance
            and no_signal["max_bell_probability_error"] < tolerance
        ),
    }

    print("Acceptance gates:")
    for name, ok in pass_checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()

    print("Claim boundary:")
    print("  This models only a causal classical Bell-record channel.")
    print("  It is not FTL signaling, matter transport, mass transfer, or charge transfer.")
    print("  It does not derive the classical record from the DAG or from a CHSH lane.")

    return all(pass_checks.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tolerance", type=float, default=1e-12, help="pass/fail tolerance")
    parser.add_argument(
        "--wrong-fidelity-ceiling",
        type=float,
        default=0.99,
        help="wrong-record control must stay below this fidelity",
    )
    args = parser.parse_args()

    if args.tolerance <= 0:
        raise ValueError("--tolerance must be positive")
    if not 0.0 < args.wrong_fidelity_ceiling < 1.0:
        raise ValueError("--wrong-fidelity-ceiling must be in (0, 1)")

    channel = run_channel_harness()
    no_signal = run_bob_no_signaling_probe()
    ok = print_summary(channel, no_signal, args.tolerance, args.wrong_fidelity_ceiling)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
