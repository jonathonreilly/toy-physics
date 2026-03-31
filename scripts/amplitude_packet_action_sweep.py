#!/usr/bin/env python3
"""Amplitude packet: which action formula produces gravitational ATTRACTION?

The spent_delay action increases with field → amplitude REPELS from mass.
In GR, geodesics maximize proper time. The path-sum equivalent:
constructive interference where action is STATIONARY along geodesics.

We test several action formulas to find one where high-field regions
produce better phase alignment → amplitude concentrates TOWARD mass.

Key insight: if action DECREASES with field, the stationary-action
principle pulls amplitude toward mass (= gravitational attraction).

PStack experiment: amplitude-packet-action-sweep
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    build_causal_dag,
)


def edge_amplitude(start, end, node_field, phase_k, atten_power, action_func):
    """Compute amplitude for edge using a custom action function.

    action_func(delay, link_length, retained_update) -> action_increment
    """
    link_length = math.dist(start, end)
    local_field = 0.5 * (node_field.get(start, 0.0) + node_field.get(end, 0.0))
    delay = link_length * (1.0 + local_field)
    retained = math.sqrt(max(delay * delay - link_length * link_length, 0.0))

    action = action_func(delay, link_length, retained)
    amp = cmath.exp(1j * phase_k * action) / (delay ** atten_power)
    return amp


def launch_packet_custom(
    nodes, source, width, height, node_field,
    phase_k, atten_power, action_func,
    detector_xs, screen_ys,
):
    """Launch amplitude packet with custom action formula."""
    # Build arrival times using default rule (for causal ordering)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=RulePostulates(
        phase_per_action=phase_k, attenuation_power=atten_power,
    ))
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    amplitudes: dict[tuple[int, int], complex] = {source: 1.0 + 0.0j}

    for node in order:
        if node not in amplitudes:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            link_amp = edge_amplitude(
                node, nb, node_field, phase_k, atten_power, action_func,
            )
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * link_amp

    result = {}
    for dx in detector_xs:
        dist = {}
        total = 0
        for y in screen_ys:
            p = abs(amplitudes.get((dx, y), 0.0)) ** 2
            dist[y] = p
            total += p
        if total > 0:
            dist = {y: p / total for y, p in dist.items()}
        result[dx] = dist
    return result


def centroid_y(distribution):
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in distribution.items()) / total


# ================================================================
# Action formulas to test
# ================================================================

def action_spent_delay(delay, link_length, retained):
    """Current default: delay - sqrt(delay²-L²). Increases with field."""
    return delay - retained

def action_retained_update(delay, link_length, retained):
    """Proper time analog. Also increases with field."""
    return retained

def action_negative_retained(delay, link_length, retained):
    """Negative proper time: action DECREASES with field.
    Minimizing action = maximizing proper time = GR geodesic principle."""
    return -retained

def action_inverse_delay(delay, link_length, retained):
    """L/delay: DECREASES with field (high delay = low action).
    High-field paths are 'cheaper' → constructive interference near mass."""
    return link_length / delay if delay > 0 else link_length

def action_link_length(delay, link_length, retained):
    """Pure geometry, no field dependence. Control."""
    return link_length

def action_coordinate_delay(delay, link_length, retained):
    """Pure delay. Increases with field."""
    return delay

def action_fractional_spent(delay, link_length, retained):
    """Spent fraction: (delay-retained)/delay = 1 - retained/delay.
    Dimensionless. Increases with field but bounded."""
    return (delay - retained) / delay if delay > 0 else 0.0

def action_retained_fraction(delay, link_length, retained):
    """retained/delay = sqrt(1 - (L/delay)²). DECREASES with field.
    At low field: ≈1. At high field: retained/delay → 1 but slower growth."""
    return retained / delay if delay > 0 else 0.0

def action_log_delay(delay, link_length, retained):
    """log(delay/L). Increases with field, but sublinearly.
    Less aggressive phase rotation than spent_delay."""
    return math.log(delay / link_length) if link_length > 0 and delay > link_length else 0.0


ACTION_FORMULAS = [
    ("spent_delay (default)", action_spent_delay),
    ("retained_update", action_retained_update),
    ("-retained_update", action_negative_retained),
    ("L/delay", action_inverse_delay),
    ("link_length (ctrl)", action_link_length),
    ("coordinate_delay", action_coordinate_delay),
    ("spent_fraction", action_fractional_spent),
    ("retained_fraction", action_retained_fraction),
    ("log(delay/L)", action_log_delay),
]


def main() -> None:
    width = 40
    height = 15
    phase_k = 4.0
    atten_power = 1.0

    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    detector_xs = [10, 20, 30, 40]

    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)

    # Mass above the source line
    mass_nodes = frozenset((20, y) for y in range(4, 9))
    mass_cy = sum(y for _, y in mass_nodes) / len(mass_nodes)

    # Compute field for mass
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)
    free_field = {n: 0.0 for n in nodes}

    print("=" * 80)
    print("AMPLITUDE PACKET ACTION SWEEP")
    print("Which action formula produces gravitational ATTRACTION?")
    print("=" * 80)
    print(f"Grid: {width}x{2*height+1}, source={source}")
    print(f"Mass: column at x=20, y=4..8 (centroid y={mass_cy:.1f})")
    print(f"Phase wavenumber k={phase_k}, attenuation power={atten_power}")
    print()

    for name, action_func in ACTION_FORMULAS:
        print(f"  ACTION: {name}")

        # Free field
        free_result = launch_packet_custom(
            nodes, source, width, height, free_field,
            phase_k, atten_power, action_func,
            detector_xs, screen_ys,
        )

        # With mass
        mass_result = launch_packet_custom(
            nodes, source, width, height, mass_field,
            phase_k, atten_power, action_func,
            detector_xs, screen_ys,
        )

        print(f"    {'det_x':>6s}  {'free_cy':>8s}  {'mass_cy':>8s}  {'shift':>8s}  {'toward?':>7s}")
        print(f"    {'-' * 44}")

        shifts = []
        for dx in detector_xs:
            fcy = centroid_y(free_result[dx])
            mcy = centroid_y(mass_result[dx])
            shift = mcy - fcy
            toward = "YES" if shift > 0.1 else "no"
            print(f"    {dx:6d}  {fcy:8.2f}  {mcy:8.2f}  {shift:+8.2f}  {toward:>7s}")
            shifts.append(shift)

        avg_shift = sum(shifts) / len(shifts)
        direction = "TOWARD mass" if avg_shift > 0.1 else \
                    "AWAY from mass" if avg_shift < -0.1 else "no shift"
        print(f"    → Average shift: {avg_shift:+.2f} ({direction})")
        print()

    # ================================================================
    # TEST 2: Phase wavenumber sweep for promising formulas
    # ================================================================
    print("=" * 80)
    print("TEST 2: Phase wavenumber sweep for L/delay and -retained_update")
    print("=" * 80)
    print()

    promising = [
        ("L/delay", action_inverse_delay),
        ("-retained_update", action_negative_retained),
        ("retained_fraction", action_retained_fraction),
    ]

    for name, action_func in promising:
        print(f"  ACTION: {name}")
        print(f"    {'k':>6s}  {'shift@10':>9s}  {'shift@20':>9s}  {'shift@30':>9s}  {'shift@40':>9s}  {'avg':>8s}")
        print(f"    {'-' * 56}")

        for k in [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]:
            free_result = launch_packet_custom(
                nodes, source, width, height, free_field,
                k, atten_power, action_func,
                detector_xs, screen_ys,
            )
            mass_result = launch_packet_custom(
                nodes, source, width, height, mass_field,
                k, atten_power, action_func,
                detector_xs, screen_ys,
            )

            shifts = []
            for dx in detector_xs:
                fcy = centroid_y(free_result[dx])
                mcy = centroid_y(mass_result[dx])
                shifts.append(mcy - fcy)

            avg = sum(shifts) / len(shifts)
            print(f"    {k:6.1f}  {shifts[0]:+9.2f}  {shifts[1]:+9.2f}  "
                  f"{shifts[2]:+9.2f}  {shifts[3]:+9.2f}  {avg:+8.2f}")
        print()

    # ================================================================
    # TEST 3: Mass on opposite side — does shift flip?
    # ================================================================
    print("=" * 80)
    print("TEST 3: Mass below (y=-4..-8) — does shift reverse?")
    print("=" * 80)
    print()

    mass_below = frozenset((20, y) for y in range(-8, -3))
    below_rule = derive_local_rule(persistent_nodes=mass_below, postulates=postulates)
    below_field = derive_node_field(nodes, below_rule)

    for name, action_func in promising:
        for k in [2.0, 4.0]:
            # Mass above
            above_result = launch_packet_custom(
                nodes, source, width, height, mass_field,
                k, atten_power, action_func,
                detector_xs, screen_ys,
            )
            # Mass below
            below_result = launch_packet_custom(
                nodes, source, width, height, below_field,
                k, atten_power, action_func,
                detector_xs, screen_ys,
            )
            # Free
            free_result = launch_packet_custom(
                nodes, source, width, height, free_field,
                k, atten_power, action_func,
                detector_xs, screen_ys,
            )

            above_shifts = []
            below_shifts = []
            for dx in detector_xs:
                fcy = centroid_y(free_result[dx])
                above_shifts.append(centroid_y(above_result[dx]) - fcy)
                below_shifts.append(centroid_y(below_result[dx]) - fcy)

            above_avg = sum(above_shifts) / len(above_shifts)
            below_avg = sum(below_shifts) / len(below_shifts)
            flips = "YES" if (above_avg > 0.1 and below_avg < -0.1) or \
                             (above_avg < -0.1 and below_avg > 0.1) else "no"

            print(f"  {name}, k={k}: above_shift={above_avg:+.2f}, "
                  f"below_shift={below_avg:+.2f}, flips={flips}")

    print()
    print("ATTRACTION = positive shift (toward mass at y>0)")
    print("REPULSION = negative shift (away from mass at y>0)")
    print("FLIP = shift reverses when mass moves to opposite side (= genuine gravity)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
