#!/usr/bin/env python3
"""Does decoherence convert amplitude REPULSION into ATTRACTION?

Key hypothesis: the model's quantum amplitude packets repel from mass
because high-field regions cause destructive self-interference. But
classical gravity (attraction) might emerge when decoherence suppresses
the interference that causes repulsion.

If true: decoherence is not just "loss of quantum effects" — it's
the mechanism that ENABLES classical gravity.

Test: add partial recording (decoherence parameter p) to the amplitude
packet experiment. At p=0 (full coherence), expect repulsion.
At p=1 (full decoherence), expect attraction or neutral.

Decoherence model: at each barrier node, with probability p, the
which-path information is recorded. This converts interference terms
into classical probability addition.

Practical implementation: propagate through each path independently
(incoherent sum) with weight p, and coherently with weight (1-p).
The total probability is: (1-p)|sum_i a_i|² + p × sum_i |a_i|²

PStack experiment: decoherence-enables-attraction
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


def propagate_amplitude(nodes, source, node_field, phase_k, atten_power):
    """Full coherent propagation, return amplitudes at all nodes."""
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    amplitudes = {source: 1.0 + 0.0j}
    for node in order:
        if node not in amplitudes:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            link_length = math.dist(node, nb)
            local_field = 0.5 * (node_field.get(node, 0.0) + node_field.get(nb, 0.0))
            delay = link_length * (1.0 + local_field)
            action = delay - math.sqrt(max(delay * delay - link_length * link_length, 0.0))
            edge_amp = cmath.exp(1j * phase_k * action) / (delay ** atten_power)
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * edge_amp

    return amplitudes


def propagate_via_channels(
    nodes, source, node_field, phase_k, atten_power,
    channel_x, channel_ys, decoherence_p,
    detector_xs, screen_ys,
):
    """Propagate through channels with partial decoherence.

    At channel_x, amplitude passes through channel_ys (like slits).
    With probability decoherence_p, which-channel info is recorded →
    incoherent addition. With (1-p), coherent.

    Returns: dict of {det_x: {y: probability}} for detector planes.
    """
    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    def edge_amp(n1, n2):
        link_length = math.dist(n1, n2)
        local_field = 0.5 * (node_field.get(n1, 0.0) + node_field.get(n2, 0.0))
        delay = link_length * (1.0 + local_field)
        action = delay - math.sqrt(max(delay * delay - link_length * link_length, 0.0))
        return cmath.exp(1j * phase_k * action) / (delay ** atten_power)

    # Phase 1: propagate from source to channel
    pre_channel = {source: 1.0 + 0.0j}
    for node in order:
        if node[0] >= channel_x:
            break
        if node not in pre_channel:
            continue
        amp = pre_channel[node]
        for nb in dag.get(node, []):
            ea = edge_amp(node, nb)
            if nb not in pre_channel:
                pre_channel[nb] = 0.0 + 0.0j
            pre_channel[nb] += amp * ea

    # Phase 2: for each channel, propagate separately to detectors
    # channel_amplitudes[ch_y] = amplitude arriving at channel node
    channel_amplitudes = {}
    for cy in channel_ys:
        ch_node = (channel_x, cy)
        if ch_node in pre_channel:
            # Sum contributions from all nodes just before channel
            channel_amplitudes[cy] = pre_channel[ch_node]

    # Propagate from each channel node to detectors
    per_channel_amps = {}  # {cy: {det_node: amplitude}}
    for cy in channel_ys:
        ch_node = (channel_x, cy)
        ch_amp = channel_amplitudes.get(cy, 0.0 + 0.0j)
        if abs(ch_amp) < 1e-30:
            continue

        # Propagate from channel node
        amps = {ch_node: ch_amp}
        for node in order:
            if node[0] < channel_x:
                continue
            if node not in amps:
                continue
            a = amps[node]
            for nb in dag.get(node, []):
                ea = edge_amp(node, nb)
                if nb not in amps:
                    amps[nb] = 0.0 + 0.0j
                amps[nb] += a * ea

        per_channel_amps[cy] = amps

    # Phase 3: combine coherent and incoherent contributions
    result = {}
    for dx in detector_xs:
        dist = {}
        for y in screen_ys:
            det_node = (dx, y)

            # Coherent sum: |(1-p) × sum_ch a_ch(det)|²
            coherent_sum = 0.0 + 0.0j
            for cy in channel_ys:
                if cy in per_channel_amps:
                    coherent_sum += per_channel_amps[cy].get(det_node, 0.0 + 0.0j)

            # Incoherent sum: p × sum_ch |a_ch(det)|²
            incoherent_sum = 0.0
            for cy in channel_ys:
                if cy in per_channel_amps:
                    incoherent_sum += abs(per_channel_amps[cy].get(det_node, 0.0)) ** 2

            # Mixed probability
            prob = (1.0 - decoherence_p) * abs(coherent_sum) ** 2 + \
                   decoherence_p * incoherent_sum
            dist[y] = prob

        total = sum(dist.values())
        if total > 0:
            dist = {y: p / total for y, p in dist.items()}
        result[dx] = dist

    return result


def centroid_y(distribution):
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    return sum(y * p for y, p in distribution.items()) / total


def main() -> None:
    width = 40
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    phase_k = 4.0
    atten_power = 1.0

    postulates = RulePostulates(phase_per_action=phase_k, attenuation_power=atten_power)

    # Mass above beam center
    mass_nodes = frozenset((20, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, mass_rule)
    free_field = {n: 0.0 for n in nodes}

    # Channel at x=10 (before mass at x=20)
    channel_x = 10
    channel_ys = list(range(-height, height + 1))  # All y-positions are channels

    detector_xs = [25, 30, 35, 40]

    print("=" * 80)
    print("DECOHERENCE → ATTRACTION HYPOTHESIS")
    print("Does decoherence convert quantum repulsion into classical attraction?")
    print("=" * 80)
    print(f"Grid: {width}x{2*height+1}, source={source}")
    print(f"Mass: column at x=20, y=4..8")
    print(f"Channel: x={channel_x} (all y-positions)")
    print(f"Phase k={phase_k}, attenuation={atten_power}")
    print()

    # ================================================================
    # TEST 1: Decoherence parameter sweep
    # ================================================================
    print("TEST 1: Decoherence sweep — shift vs recording probability")
    print()

    print(f"  {'p':>6s}", end="")
    for dx in detector_xs:
        print(f"  {'@' + str(dx):>8s}", end="")
    print(f"  {'avg':>8s}  {'dir':>10s}")
    print(f"  {'-' * 58}")

    for p in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        free_result = propagate_via_channels(
            nodes, source, free_field, phase_k, atten_power,
            channel_x, channel_ys, p, detector_xs, screen_ys,
        )
        mass_result = propagate_via_channels(
            nodes, source, mass_field, phase_k, atten_power,
            channel_x, channel_ys, p, detector_xs, screen_ys,
        )

        shifts = [centroid_y(mass_result[dx]) - centroid_y(free_result[dx])
                  for dx in detector_xs]
        avg = sum(shifts) / len(shifts)
        d = "ATTRACT" if avg > 0.3 else "REPEL" if avg < -0.3 else "neutral"

        print(f"  {p:6.1f}", end="")
        for s in shifts:
            print(f"  {s:+8.2f}", end="")
        print(f"  {avg:+8.2f}  {d:>10s}")

    # ================================================================
    # TEST 2: Fewer channels (more like actual slits)
    # ================================================================
    print()
    print("TEST 2: Restricted channels (5 evenly spaced) — amplifies effect")
    print()

    restricted_ys = [-10, -5, 0, 5, 10]

    print(f"  {'p':>6s}", end="")
    for dx in detector_xs:
        print(f"  {'@' + str(dx):>8s}", end="")
    print(f"  {'avg':>8s}  {'dir':>10s}")
    print(f"  {'-' * 58}")

    for p in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        free_result = propagate_via_channels(
            nodes, source, free_field, phase_k, atten_power,
            channel_x, restricted_ys, p, detector_xs, screen_ys,
        )
        mass_result = propagate_via_channels(
            nodes, source, mass_field, phase_k, atten_power,
            channel_x, restricted_ys, p, detector_xs, screen_ys,
        )

        shifts = [centroid_y(mass_result[dx]) - centroid_y(free_result[dx])
                  for dx in detector_xs]
        avg = sum(shifts) / len(shifts)
        d = "ATTRACT" if avg > 0.3 else "REPEL" if avg < -0.3 else "neutral"

        print(f"  {p:6.1f}", end="")
        for s in shifts:
            print(f"  {s:+8.2f}", end="")
        print(f"  {avg:+8.2f}  {d:>10s}")

    # ================================================================
    # TEST 3: Pure classical (p=1) vs pure quantum (p=0) comparison
    # ================================================================
    print()
    print("TEST 3: Pure quantum (p=0) vs pure classical (p=1) — detailed")
    print()

    for label, p_val in [("QUANTUM (p=0)", 0.0), ("CLASSICAL (p=1)", 1.0)]:
        free_result = propagate_via_channels(
            nodes, source, free_field, phase_k, atten_power,
            channel_x, channel_ys, p_val, detector_xs, screen_ys,
        )
        mass_result = propagate_via_channels(
            nodes, source, mass_field, phase_k, atten_power,
            channel_x, channel_ys, p_val, detector_xs, screen_ys,
        )

        print(f"  {label}:")
        total_shift = 0
        for dx in detector_xs:
            fcy = centroid_y(free_result[dx])
            mcy = centroid_y(mass_result[dx])
            shift = mcy - fcy
            total_shift += shift
            print(f"    det_x={dx}: free_cy={fcy:+.2f}, mass_cy={mcy:+.2f}, shift={shift:+.2f}")
        avg = total_shift / len(detector_xs)
        print(f"    Average: {avg:+.2f} ({'TOWARD mass' if avg > 0.3 else 'AWAY from mass' if avg < -0.3 else 'neutral'})")
        print()

    # ================================================================
    # TEST 4: Verify with mass below — does attraction flip?
    # ================================================================
    print("TEST 4: Mass below (y=-4..-8) at p=1.0 — flip test")
    print()

    mass_below = frozenset((20, y) for y in range(-8, -3))
    below_rule = derive_local_rule(persistent_nodes=mass_below, postulates=postulates)
    below_field = derive_node_field(nodes, below_rule)

    for p_val in [0.0, 0.5, 1.0]:
        # Mass above
        above_result = propagate_via_channels(
            nodes, source, mass_field, phase_k, atten_power,
            channel_x, channel_ys, p_val, detector_xs, screen_ys,
        )
        # Mass below
        below_result = propagate_via_channels(
            nodes, source, below_field, phase_k, atten_power,
            channel_x, channel_ys, p_val, detector_xs, screen_ys,
        )
        # Free
        free_result = propagate_via_channels(
            nodes, source, free_field, phase_k, atten_power,
            channel_x, channel_ys, p_val, detector_xs, screen_ys,
        )

        above_shifts = [centroid_y(above_result[dx]) - centroid_y(free_result[dx])
                        for dx in detector_xs]
        below_shifts = [centroid_y(below_result[dx]) - centroid_y(free_result[dx])
                        for dx in detector_xs]
        above_avg = sum(above_shifts) / len(above_shifts)
        below_avg = sum(below_shifts) / len(below_shifts)

        flips = "YES" if (above_avg > 0.3 and below_avg < -0.3) or \
                         (above_avg < -0.3 and below_avg > 0.3) else "no"
        print(f"  p={p_val:.1f}: above={above_avg:+.2f}, below={below_avg:+.2f}, flips={flips}")

    print()
    print("=" * 80)
    print("INTERPRETATION")
    print("=" * 80)
    print()
    print("If repulsion at p=0 and attraction at p=1:")
    print("  → Gravity is fundamentally CLASSICAL. It requires decoherence.")
    print("  → Quantum amplitude packets don't gravitate — they repel.")
    print("  → Classical trajectories (decohered paths) attract because")
    print("    individual geodesics bend toward mass.")
    print()
    print("If repulsion at all p:")
    print("  → The phase effect (destructive interference near mass) dominates")
    print("    even in the classical limit.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
