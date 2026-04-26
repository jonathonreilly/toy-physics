#!/usr/bin/env python3
"""3D+1 causal Bell-record channel harness for teleportation.

This is a narrow planning artifact for ordinary qubit teleportation. Alice's
Bell measurement emits an explicit two-bit classical record at one 3D lattice
site and integer tick. Bob can receive that record only at the target 3D site
after the corresponding event lies inside the chosen discrete future light
cone.

The model schedules a classical record. It does not move matter, mass, charge,
energy, or objects, and it does not claim faster-than-light signaling.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from typing import Literal

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
Metric = Literal["manhattan", "chebyshev"]


class DuplicateRecordError(ValueError):
    """Raised when a Bell record id is reused."""


class LightConeViolation(ValueError):
    """Raised when a proposed event is outside the configured 3D+1 cone."""


@dataclasses.dataclass(frozen=True)
class SpatialLattice3D:
    """Finite 3D integer lattice for classical record propagation."""

    width: int
    height: int
    depth: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0 or self.depth <= 0:
            raise ValueError("lattice dimensions must be positive")

    def contains(self, point: Point3D) -> bool:
        x, y, z = point
        return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth


@dataclasses.dataclass(frozen=True)
class SpacetimeEvent:
    tick: int
    site: Point3D


@dataclasses.dataclass(frozen=True)
class DiscreteLightCone3D1:
    """3D spatial lattice plus one integer time direction."""

    lattice: SpatialLattice3D
    metric: Metric = "manhattan"
    max_speed_sites_per_tick: int = 1

    def __post_init__(self) -> None:
        if self.metric not in ("manhattan", "chebyshev"):
            raise ValueError("metric must be 'manhattan' or 'chebyshev'")
        if self.max_speed_sites_per_tick <= 0:
            raise ValueError("max_speed_sites_per_tick must be positive")

    def spatial_distance(self, source: Point3D, target: Point3D) -> int:
        self._require_site(source, "source")
        self._require_site(target, "target")
        deltas = [abs(target[axis] - source[axis]) for axis in range(3)]
        if self.metric == "manhattan":
            return sum(deltas)
        return max(deltas)

    def propagation_ticks(self, source: Point3D, target: Point3D) -> int:
        distance = self.spatial_distance(source, target)
        return ceil_div(distance, self.max_speed_sites_per_tick)

    def earliest_arrival_tick(
        self, source: Point3D, emitted_at_tick: int, target: Point3D
    ) -> int:
        if emitted_at_tick < 0:
            raise ValueError("emitted_at_tick cannot be negative")
        return emitted_at_tick + self.propagation_ticks(source, target)

    def contains_future_event(
        self,
        source: Point3D,
        emitted_at_tick: int,
        event_site: Point3D,
        event_tick: int,
    ) -> bool:
        if event_tick < emitted_at_tick:
            return False
        if not self.lattice.contains(source) or not self.lattice.contains(event_site):
            return False
        elapsed = event_tick - emitted_at_tick
        distance = self.spatial_distance(source, event_site)
        return distance <= self.max_speed_sites_per_tick * elapsed

    def propagation_worldline(
        self,
        source: Point3D,
        emitted_at_tick: int,
        target: Point3D,
        extra_delay_ticks: int = 0,
    ) -> tuple[SpacetimeEvent, ...]:
        if emitted_at_tick < 0:
            raise ValueError("emitted_at_tick cannot be negative")
        if extra_delay_ticks < 0:
            raise ValueError("extra_delay_ticks cannot be negative")
        self._require_site(source, "source")
        self._require_site(target, "target")

        ticks = self.propagation_ticks(source, target)
        position = list(source)
        events = [SpacetimeEvent(tick=emitted_at_tick, site=source)]
        for step_index in range(1, ticks + 1):
            if self.metric == "manhattan":
                budget = self.max_speed_sites_per_tick
                for axis in range(3):
                    delta = target[axis] - position[axis]
                    if delta == 0 or budget == 0:
                        continue
                    step = min(abs(delta), budget)
                    position[axis] += sign(delta) * step
                    budget -= step
            else:
                for axis in range(3):
                    delta = target[axis] - position[axis]
                    if delta == 0:
                        continue
                    step = min(abs(delta), self.max_speed_sites_per_tick)
                    position[axis] += sign(delta) * step

            site = tuple(position)  # type: ignore[assignment]
            events.append(SpacetimeEvent(tick=emitted_at_tick + step_index, site=site))

        if events[-1].site != target:
            raise RuntimeError("failed to construct a complete local worldline")

        for delay in range(1, extra_delay_ticks + 1):
            events.append(
                SpacetimeEvent(tick=emitted_at_tick + ticks + delay, site=target)
            )

        if not self.is_local_worldline(tuple(events)):
            raise RuntimeError("constructed worldline violates locality")
        return tuple(events)

    def is_local_worldline(self, worldline: tuple[SpacetimeEvent, ...]) -> bool:
        if not worldline:
            return False
        if any(not self.lattice.contains(event.site) for event in worldline):
            return False
        for first, second in zip(worldline, worldline[1:]):
            delta_tick = second.tick - first.tick
            if delta_tick <= 0:
                return False
            distance = self.spatial_distance(first.site, second.site)
            if distance > self.max_speed_sites_per_tick * delta_tick:
                return False
        return True

    def _require_site(self, point: Point3D, label: str) -> None:
        if not self.lattice.contains(point):
            raise ValueError(f"{label} site is outside the 3D lattice")


@dataclasses.dataclass(frozen=True)
class BellRecord:
    """Explicit two-bit Bell record moving inside a 3D+1 light cone."""

    record_id: str
    sender: str
    receiver: str
    source_site: Point3D
    target_site: Point3D
    emitted_at_tick: int
    earliest_deliver_at_tick: int
    deliver_at_tick: int
    z_bit: int
    x_bit: int
    metric: Metric
    max_speed_sites_per_tick: int
    spatial_distance: int
    worldline: tuple[SpacetimeEvent, ...]
    extra_delay_ticks: int = 0
    derived_by_channel: bool = False

    @property
    def label(self) -> str:
        return OUTCOME_LABELS[(self.z_bit, self.x_bit)]

    @property
    def base_latency_ticks(self) -> int:
        return self.earliest_deliver_at_tick - self.emitted_at_tick


class CausalBellRecordChannel3D1:
    """Exactly-once channel for explicit two-bit records on a 3D+1 lattice."""

    def __init__(self, cone: DiscreteLightCone3D1) -> None:
        self.cone = cone
        self.current_tick = 0
        self._in_flight: dict[str, BellRecord] = {}
        self._used_record_ids: set[str] = set()
        self._delivered_record_ids: set[str] = set()
        self._dropped_record_ids: set[str] = set()

    def advance_to(self, tick: int) -> None:
        if tick < self.current_tick:
            raise ValueError("channel time cannot run backward")
        self.current_tick = tick

    def emit(
        self,
        *,
        record_id: str,
        sender: str,
        receiver: str,
        z_bit: int,
        x_bit: int,
        source_site: Point3D,
        target_site: Point3D,
        extra_delay_ticks: int = 0,
    ) -> BellRecord:
        if record_id in self._used_record_ids:
            raise DuplicateRecordError(f"duplicate Bell record id: {record_id}")
        if z_bit not in (0, 1) or x_bit not in (0, 1):
            raise ValueError("Bell record bits must be binary")
        if extra_delay_ticks < 0:
            raise ValueError("extra_delay_ticks cannot be negative")

        earliest = self.cone.earliest_arrival_tick(
            source_site, self.current_tick, target_site
        )
        distance = self.cone.spatial_distance(source_site, target_site)
        deliver_at = earliest + extra_delay_ticks
        if not self.cone.contains_future_event(
            source_site, self.current_tick, target_site, earliest
        ):
            raise LightConeViolation("target delivery event is outside the light cone")

        record = BellRecord(
            record_id=record_id,
            sender=sender,
            receiver=receiver,
            source_site=source_site,
            target_site=target_site,
            emitted_at_tick=self.current_tick,
            earliest_deliver_at_tick=earliest,
            deliver_at_tick=deliver_at,
            z_bit=z_bit,
            x_bit=x_bit,
            metric=self.cone.metric,
            max_speed_sites_per_tick=self.cone.max_speed_sites_per_tick,
            spatial_distance=distance,
            worldline=self.cone.propagation_worldline(
                source_site,
                self.current_tick,
                target_site,
                extra_delay_ticks=extra_delay_ticks,
            ),
            extra_delay_ticks=extra_delay_ticks,
        )
        self._in_flight[record.record_id] = record
        self._used_record_ids.add(record.record_id)
        return record

    def receive(self, *, receiver: str, at_site: Point3D) -> list[BellRecord]:
        delivered: list[BellRecord] = []
        for record in tuple(self._in_flight.values()):
            if record.receiver != receiver or record.target_site != at_site:
                continue
            if record.deliver_at_tick > self.current_tick:
                continue
            if not self.cone.contains_future_event(
                record.source_site,
                record.emitted_at_tick,
                at_site,
                self.current_tick,
            ):
                continue
            delivered.append(record)
            del self._in_flight[record.record_id]
            self._delivered_record_ids.add(record.record_id)
        return delivered

    def drop(self, record_id: str) -> bool:
        if record_id not in self._in_flight:
            return False
        del self._in_flight[record_id]
        self._dropped_record_ids.add(record_id)
        return True

    def pending_count(self) -> int:
        return len(self._in_flight)


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def sign(value: int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def density(state: np.ndarray) -> np.ndarray:
    return np.outer(state, state.conj())


def bell_state(z_bit: int, x_bit: int) -> np.ndarray:
    """Bell state |Bell(z,x)> with z as phase bit and x as bit-flip bit."""
    sign_factor = -1.0 if z_bit else 1.0
    state = np.zeros(4, dtype=complex)
    if x_bit == 0:
        state[0] = 1.0 / math.sqrt(2.0)
        state[3] = sign_factor / math.sqrt(2.0)
    else:
        state[1] = 1.0 / math.sqrt(2.0)
        state[2] = sign_factor / math.sqrt(2.0)
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
    bob_rho = density(bob_state)
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


def worldline_text(worldline: tuple[SpacetimeEvent, ...]) -> str:
    return " -> ".join(f"t={event.tick}:{event.site}" for event in worldline)


def run_bob_pre_delivery_input_independence() -> dict[str, object]:
    half_identity = 0.5 * I2
    reference_before_delivery: np.ndarray | None = None
    max_before_measurement_distance = 0.0
    max_before_delivery_distance = 0.0
    max_pairwise_before_delivery_distance = 0.0
    max_bell_probability_error = 0.0

    for input_state in no_signaling_probe_states():
        three_register_state = prepare_three_register_state(input_state)
        rho_before_measurement = bob_reduced_from_three_register_state(
            three_register_state
        )
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


def run_channel_harness(metric: Metric, max_speed_sites_per_tick: int) -> dict[str, object]:
    lattice = SpatialLattice3D(width=8, height=6, depth=5)
    cone = DiscreteLightCone3D1(
        lattice=lattice,
        metric=metric,
        max_speed_sites_per_tick=max_speed_sites_per_tick,
    )
    alice_site = (1, 1, 1)
    bob_site = (5, 3, 2)
    created_tick = 4
    z_bit, x_bit = (1, 1)

    input_state = no_signaling_probe_states()[-1]
    three_register_state = prepare_three_register_state(input_state)
    probability, bob_state, _ = project_bell_branch(
        three_register_state, z_bit, x_bit
    )

    channel = CausalBellRecordChannel3D1(cone)
    channel.advance_to(created_tick)
    sent = channel.emit(
        record_id="bell-record-3d1-0001",
        sender="Alice",
        receiver="Bob",
        z_bit=z_bit,
        x_bit=x_bit,
        source_site=alice_site,
        target_site=bob_site,
    )

    expected_latency = ceil_div(sent.spatial_distance, max_speed_sites_per_tick)
    expected_earliest_tick = sent.emitted_at_tick + expected_latency
    distance_rule_ok = (
        sent.base_latency_ticks == expected_latency
        and sent.earliest_deliver_at_tick == expected_earliest_tick
    )
    local_worldline_ok = cone.is_local_worldline(sent.worldline)
    delivery_inside_future_cone = cone.contains_future_event(
        alice_site, sent.emitted_at_tick, bob_site, sent.earliest_deliver_at_tick
    )

    outside_cone_tick = sent.earliest_deliver_at_tick - 1
    outside_cone_event_rejected = not cone.contains_future_event(
        alice_site, sent.emitted_at_tick, bob_site, outside_cone_tick
    )

    try:
        channel.emit(
            record_id=sent.record_id,
            sender="Alice",
            receiver="Bob",
            z_bit=z_bit,
            x_bit=x_bit,
            source_site=alice_site,
            target_site=bob_site,
        )
        duplicate_id_rejected = False
    except DuplicateRecordError:
        duplicate_id_rejected = True

    channel.advance_to(outside_cone_tick)
    early_records = channel.receive(receiver="Bob", at_site=bob_site)
    early_delivery_blocked = len(early_records) == 0 and channel.pending_count() == 1

    channel.advance_to(sent.deliver_at_tick)
    wrong_receiver_records = channel.receive(receiver="Mallory", at_site=bob_site)
    wrong_receiver_blocked = (
        len(wrong_receiver_records) == 0 and channel.pending_count() == 1
    )
    wrong_site = (bob_site[0] - 1, bob_site[1], bob_site[2])
    wrong_site_records = channel.receive(receiver="Bob", at_site=wrong_site)
    wrong_site_blocked = len(wrong_site_records) == 0 and channel.pending_count() == 1
    delivered_records = channel.receive(receiver="Bob", at_site=bob_site)
    duplicate_delivery_records = channel.receive(receiver="Bob", at_site=bob_site)
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
    wrong_record_fidelity = state_fidelity(input_state, wrong_corrected)
    dropped_or_pre_delivery_fidelity = state_fidelity(input_state, bob_state)

    dropped_channel = CausalBellRecordChannel3D1(cone)
    dropped_channel.advance_to(created_tick)
    dropped = dropped_channel.emit(
        record_id="bell-record-3d1-dropped-control",
        sender="Alice",
        receiver="Bob",
        z_bit=z_bit,
        x_bit=x_bit,
        source_site=alice_site,
        target_site=bob_site,
    )
    dropped_before_delivery = dropped_channel.drop(dropped.record_id)
    dropped_channel.advance_to(dropped.deliver_at_tick)
    dropped_records = dropped_channel.receive(receiver="Bob", at_site=bob_site)
    dropped_control_blocked = (
        dropped_before_delivery
        and len(dropped_records) == 0
        and dropped_channel.pending_count() == 0
    )

    delayed_channel = CausalBellRecordChannel3D1(cone)
    delayed_channel.advance_to(created_tick)
    delayed = delayed_channel.emit(
        record_id="bell-record-3d1-delayed-control",
        sender="Alice",
        receiver="Bob",
        z_bit=z_bit,
        x_bit=x_bit,
        source_site=alice_site,
        target_site=bob_site,
        extra_delay_ticks=2,
    )
    delayed_channel.advance_to(delayed.earliest_deliver_at_tick)
    delayed_base_records = delayed_channel.receive(receiver="Bob", at_site=bob_site)
    delayed_blocked_at_base = (
        len(delayed_base_records) == 0 and delayed_channel.pending_count() == 1
    )
    delayed_channel.advance_to(delayed.deliver_at_tick)
    delayed_late_records = delayed_channel.receive(receiver="Bob", at_site=bob_site)
    delayed_delivered_late = (
        len(delayed_late_records) == 1 and delayed_channel.pending_count() == 0
    )
    delayed_delivered = delayed_late_records[0] if delayed_late_records else delayed
    delayed_corrected = (
        correction_operator(delayed_delivered.z_bit, delayed_delivered.x_bit)
        @ bob_state
    )

    return {
        "lattice_shape": (lattice.width, lattice.height, lattice.depth),
        "metric": cone.metric,
        "max_speed_sites_per_tick": cone.max_speed_sites_per_tick,
        "alice_site": alice_site,
        "bob_site": bob_site,
        "record_id": sent.record_id,
        "record_label": sent.label,
        "record_bits": (sent.z_bit, sent.x_bit),
        "emitted_at_tick": sent.emitted_at_tick,
        "spatial_distance": sent.spatial_distance,
        "expected_latency_ticks": expected_latency,
        "earliest_deliver_at_tick": sent.earliest_deliver_at_tick,
        "deliver_at_tick": sent.deliver_at_tick,
        "worldline": worldline_text(sent.worldline),
        "channel_derives_bits": sent.derived_by_channel,
        "distance_rule_ok": distance_rule_ok,
        "local_worldline_ok": local_worldline_ok,
        "delivery_inside_future_cone": delivery_inside_future_cone,
        "outside_cone_tick": outside_cone_tick,
        "outside_cone_event_rejected": outside_cone_event_rejected,
        "early_delivery_blocked": early_delivery_blocked,
        "wrong_receiver_blocked": wrong_receiver_blocked,
        "wrong_site_blocked": wrong_site_blocked,
        "duplicate_id_rejected": duplicate_id_rejected,
        "delivered_once": delivered_once,
        "branch_probability": probability,
        "correct_fidelity": correct_fidelity,
        "wrong_record_fidelity": wrong_record_fidelity,
        "dropped_or_pre_delivery_fidelity": dropped_or_pre_delivery_fidelity,
        "dropped_control_blocked": dropped_control_blocked,
        "delayed_extra_ticks": delayed.extra_delay_ticks,
        "delayed_base_tick": delayed.earliest_deliver_at_tick,
        "delayed_deliver_at_tick": delayed.deliver_at_tick,
        "delayed_blocked_at_base": delayed_blocked_at_base,
        "delayed_delivered_late": delayed_delivered_late,
        "delayed_corrected_fidelity": state_fidelity(input_state, delayed_corrected),
    }


def print_summary(
    channel: dict[str, object],
    no_signal: dict[str, object],
    tolerance: float,
    wrong_fidelity_ceiling: float,
) -> bool:
    print("TELEPORTATION 3D+1 CAUSAL BELL-RECORD CHANNEL")
    print("Status: planning / first 3D+1 local record-propagation artifact")
    print()

    print("3D+1 discrete light cone:")
    print(f"  lattice shape: {channel['lattice_shape']}")
    print(
        "  metric / speed: "
        f"{channel['metric']} / {channel['max_speed_sites_per_tick']} site(s)/tick"
    )
    print(
        "  Alice event: "
        f"site={channel['alice_site']} t={channel['emitted_at_tick']}"
    )
    print(f"  Bob target site: {channel['bob_site']}")
    print(f"  spatial distance: {channel['spatial_distance']}")
    print(f"  expected light-cone latency: {channel['expected_latency_ticks']} tick(s)")
    print(f"  earliest delivery tick: {channel['earliest_deliver_at_tick']}")
    print(f"  propagation worldline: {channel['worldline']}")
    print(f"  worldline local under metric: {channel['local_worldline_ok']}")
    print(f"  delivery event inside future cone: {channel['delivery_inside_future_cone']}")
    print()

    print("Explicit Bell record:")
    print(
        "  record: "
        f"{channel['record_label']} bits(z,x)={channel['record_bits']} "
        f"id={channel['record_id']}"
    )
    print(f"  channel derives Bell bits: {channel['channel_derives_bits']}")
    print(f"  Bell branch probability: {channel['branch_probability']:.16f}")
    print()

    print("Causal delivery checks:")
    print(f"  earliest tick equals distance/velocity rule: {channel['distance_rule_ok']}")
    print(
        f"  target event at t={channel['outside_cone_tick']} outside cone rejected: "
        f"{channel['outside_cone_event_rejected']}"
    )
    print(f"  receive before cone arrival blocked: {channel['early_delivery_blocked']}")
    print(f"  wrong receiver blocked: {channel['wrong_receiver_blocked']}")
    print(f"  wrong 3D site blocked: {channel['wrong_site_blocked']}")
    print(f"  duplicate record id rejected: {channel['duplicate_id_rejected']}")
    print(f"  receive at delivery exactly once: {channel['delivered_once']}")
    print()

    print("Correction and record controls:")
    print(f"  correct delivered-record fidelity: {channel['correct_fidelity']:.16f}")
    print(f"  wrong-record fidelity: {channel['wrong_record_fidelity']:.16f}")
    print(
        "  dropped/pre-delivery no-correction fidelity: "
        f"{channel['dropped_or_pre_delivery_fidelity']:.16f}"
    )
    print(f"  dropped record remains undelivered: {channel['dropped_control_blocked']}")
    print(
        "  delayed control blocked at base arrival: "
        f"{channel['delayed_blocked_at_base']} "
        f"(base t={channel['delayed_base_tick']}, "
        f"actual t={channel['delayed_deliver_at_tick']})"
    )
    print(f"  delayed control delivered late: {channel['delayed_delivered_late']}")
    print(
        "  delayed delivered-record fidelity after waiting: "
        f"{channel['delayed_corrected_fidelity']:.16f}"
    )
    print()

    print("Bob pre-message input-independence:")
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
        "3D+1 light-cone locality": bool(
            channel["local_worldline_ok"] and channel["delivery_inside_future_cone"]
        ),
        "distance/velocity earliest arrival": bool(channel["distance_rule_ok"]),
        "outside-cone attempts fail": bool(
            channel["outside_cone_event_rejected"]
            and channel["early_delivery_blocked"]
        ),
        "no duplicate delivery": bool(
            channel["duplicate_id_rejected"] and channel["delivered_once"]
        ),
        "correct record restores Bob state": bool(
            1.0 - channel["correct_fidelity"] < tolerance
            and 1.0 - channel["delayed_corrected_fidelity"] < tolerance
        ),
        "wrong/dropped/delayed controls": bool(
            channel["wrong_receiver_blocked"]
            and channel["wrong_site_blocked"]
            and channel["wrong_record_fidelity"] < wrong_fidelity_ceiling
            and channel["dropped_or_pre_delivery_fidelity"] < wrong_fidelity_ceiling
            and channel["dropped_control_blocked"]
            and channel["delayed_blocked_at_base"]
            and channel["delayed_delivered_late"]
        ),
        "Bob pre-delivery input-independence": bool(
            no_signal["max_before_measurement_distance"] < tolerance
            and no_signal["max_before_delivery_distance"] < tolerance
            and no_signal["max_pairwise_before_delivery_distance"] < tolerance
            and no_signal["max_bell_probability_error"] < tolerance
        ),
        "explicit not derived record channel": not channel["channel_derives_bits"],
    }

    print("Acceptance gates:")
    for name, ok in pass_checks.items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()

    print("Claim boundary:")
    print("  This models only a causal classical Bell-record channel.")
    print("  It is ordinary quantum state teleportation only.")
    print("  It does not transfer matter, mass, charge, energy, or objects.")
    print("  It does not enable faster-than-light signaling or pre-message control.")
    print("  It does not derive the Bell record, Bell resource, or measurement dynamics.")

    return all(pass_checks.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metric",
        choices=("manhattan", "chebyshev"),
        default="manhattan",
        help="3D discrete light-cone metric",
    )
    parser.add_argument(
        "--speed",
        type=int,
        default=1,
        help="maximum sites per tick under the chosen metric",
    )
    parser.add_argument("--tolerance", type=float, default=1e-12, help="pass/fail tolerance")
    parser.add_argument(
        "--wrong-fidelity-ceiling",
        type=float,
        default=0.99,
        help="wrong/dropped-record controls must stay below this fidelity",
    )
    args = parser.parse_args()

    if args.speed <= 0:
        raise ValueError("--speed must be positive")
    if args.tolerance <= 0:
        raise ValueError("--tolerance must be positive")
    if not 0.0 < args.wrong_fidelity_ceiling < 1.0:
        raise ValueError("--wrong-fidelity-ceiling must be in (0, 1)")

    channel = run_channel_harness(args.metric, args.speed)
    no_signal = run_bob_pre_delivery_input_independence()
    ok = print_summary(
        channel,
        no_signal,
        args.tolerance,
        args.wrong_fidelity_ceiling,
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
