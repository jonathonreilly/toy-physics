#!/usr/bin/env python3
"""Path-sum amplitude packet: does a localized wavepacket drift in a field?

Instead of CA patterns, define a "particle" as a localized amplitude
concentration in the path-sum. Launch it from a source and watch
where the amplitude concentrates at the detector.

With no field: amplitude spreads symmetrically.
With a mass: field gradient should pull amplitude toward the mass.
The SHIFT in the amplitude peak IS gravitational deflection.

This unifies mobility and gravity through the path-sum — no CA needed.

PStack experiment: amplitude-packet-mobility
"""

from __future__ import annotations
import math
import cmath
import heapq
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    local_edge_properties,
    infer_arrival_times_from_source,
    build_causal_dag,
)


def launch_packet(
    nodes, rule, node_field, source, width, height,
    detector_xs, screen_ys, detector_tol=0.5,
):
    """Launch amplitude from source, measure distribution at each detector_x.

    Returns: {detector_x: {screen_y: probability}}
    """
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    amplitudes: dict[tuple[int, int], complex] = {source: 1.0 + 0.0j}

    # Propagate
    for node in order:
        if node not in amplitudes:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            _, _, link_amp = local_edge_properties(node, nb, rule, node_field)
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * link_amp

    # Collect at detectors
    result = {}
    for dx in detector_xs:
        dist = {}
        total = 0
        for y in screen_ys:
            p = abs(amplitudes.get((dx, y), 0.0)) ** 2
            dist[y] = p
            total += p
        # Normalize
        if total > 0:
            dist = {y: p / total for y, p in dist.items()}
        result[dx] = dist

    return result


def peak_y(distribution):
    """Find the y with maximum probability."""
    if not distribution:
        return 0.0
    return max(distribution, key=distribution.get)


def centroid_y(distribution):
    """Probability-weighted mean y."""
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in distribution.items()) / total


def main() -> None:
    width = 40
    height = 15
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    nodes = build_rectangular_nodes(width=width, height=height)

    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    detector_xs = list(range(5, width + 1, 5))

    print("=" * 80)
    print("AMPLITUDE PACKET MOBILITY IN FIELD GRADIENT")
    print("=" * 80)
    print(f"Grid: {width}x{2*height+1}, source={source}")
    print()

    # =========================================================
    # CONTROL: Free field — where does amplitude go?
    # =========================================================
    print("CONTROL: Free field (no mass)")
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    free_field = derive_node_field(nodes, free_rule)

    free_result = launch_packet(
        nodes, free_rule, free_field, source, width, height,
        detector_xs, screen_ys,
    )

    print(f"  {'det_x':>6s}  {'peak_y':>7s}  {'centroid_y':>10s}")
    print(f"  {'-' * 27}")
    for dx in detector_xs:
        py = peak_y(free_result[dx])
        cy = centroid_y(free_result[dx])
        print(f"  {dx:6d}  {py:7d}  {cy:10.2f}")

    # =========================================================
    # TEST: Mass above the path — does amplitude shift toward it?
    # =========================================================
    mass_configs = [
        ("mass at (20, +8)", frozenset((20, y) for y in range(6, 11))),
        ("mass at (20, -8)", frozenset((20, y) for y in range(-10, -5))),
        ("mass at (20, +4)", frozenset((20, y) for y in range(2, 7))),
        ("mass at (30, +6)", frozenset((30, y) for y in range(4, 9))),
        ("large mass at (20, +6)", frozenset(
            (x, y) for x in range(18, 23) for y in range(4, 9)
        )),
    ]

    for label, mass_nodes in mass_configs:
        print(f"\n  {label}:")
        dist_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
        dist_field = derive_node_field(nodes, dist_rule)

        grav_result = launch_packet(
            nodes, dist_rule, dist_field, source, width, height,
            detector_xs, screen_ys,
        )

        print(f"  {'det_x':>6s}  {'free_cy':>8s}  {'grav_cy':>8s}  {'shift':>8s}  {'toward?':>7s}")
        print(f"  {'-' * 42}")

        mass_cy = sum(y for _, y in mass_nodes) / len(mass_nodes)
        for dx in detector_xs:
            fcy = centroid_y(free_result[dx])
            gcy = centroid_y(grav_result[dx])
            shift = gcy - fcy
            toward = "YES" if (mass_cy > 0 and shift > 0.1) or \
                              (mass_cy < 0 and shift < -0.1) else "NO"
            print(f"  {dx:6d}  {fcy:8.2f}  {gcy:8.2f}  {shift:+8.2f}  {toward:>7s}")

    # =========================================================
    # TEST 2: Does the shift grow with distance (accumulation)?
    # =========================================================
    print()
    print("=" * 80)
    print("TEST 2: Does amplitude shift accumulate with distance?")
    print("=" * 80)
    print()

    mass_nodes = frozenset((20, y) for y in range(4, 9))
    dist_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    dist_field = derive_node_field(nodes, dist_rule)

    # Use many detector positions for fine resolution
    fine_xs = list(range(1, width + 1))
    fine_result = launch_packet(
        nodes, dist_rule, dist_field, source, width, height,
        fine_xs, screen_ys,
    )
    fine_free = launch_packet(
        nodes, free_rule, free_field, source, width, height,
        fine_xs, screen_ys,
    )

    print(f"  Mass at (20, y=4..8). Source at (0,0).")
    print(f"  {'x':>4s}  {'free_cy':>8s}  {'grav_cy':>8s}  {'cum_shift':>10s}")
    print(f"  {'-' * 34}")
    for x in range(5, width + 1, 2):
        fcy = centroid_y(fine_free[x])
        gcy = centroid_y(fine_result[x])
        print(f"  {x:4d}  {fcy:8.2f}  {gcy:8.2f}  {gcy - fcy:+10.4f}")

    print()
    print("If cum_shift grows with x: amplitude packet deflects toward mass")
    print("(= gravitational deflection of the path-sum 'particle')")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
