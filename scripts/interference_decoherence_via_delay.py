#!/usr/bin/env python3
"""Non-trivial decoherence: records that distort the delay field.

Instead of just labeling sectors (which gives trivial V = V_0(1-p)),
this version makes record formation ADD a persistent node at the
slit position. The persistent node creates a local delay-field
distortion that changes the continuation landscape for all
subsequent paths.

This couples record formation to the gravity mechanism — a record
doesn't just "tag" a path, it physically changes the network
structure that future paths traverse.

PStack experiment: decoherence-via-delay
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_causal_dag,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    infer_arrival_times_from_source,
    local_edge_properties,
)


def delay_decoherence_two_slit(
    screen_positions: list[int],
    record_strength: float,
    width: int = 20, height: int = 10,
    slit_ys: set[int] | None = None,
    phase_shift_upper: float = 0.0,
    normalize: bool = True,
) -> dict[int, float]:
    """Two-slit where record formation creates persistent nodes.

    record_strength controls how many persistent nodes are placed
    around each slit when a record forms:
    - 0.0: no persistent nodes (pure coherent)
    - 0.5: persistent nodes at slit positions only
    - 1.0: persistent nodes at slit + immediate neighbors

    The persistent nodes create a delay-field distortion that
    changes the action landscape. Both the "recorded" and
    "unrecorded" sectors propagate on their respective distorted
    or undistorted fields.
    """
    if slit_ys is None:
        slit_ys = {-4, 4}
    barrier_x = width // 2
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    # Build the undistorted (free) network
    blocked_nodes = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked_nodes)

    # Free field (no persistent nodes)
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    free_field = derive_node_field(nodes, free_rule)

    # Distorted field: persistent nodes at/near slits
    # Strength determines how many neighbors become persistent
    persistent = set()
    if record_strength > 0:
        for sy in slit_ys:
            persistent.add((barrier_x, sy))  # slit node itself
            if record_strength >= 0.5:
                # Add immediate neighbors of the slit node
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nb = (barrier_x + dx, sy + dy)
                        if nb in nodes:
                            persistent.add(nb)
            if record_strength >= 1.0:
                # Add second ring
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        nb = (barrier_x + dx, sy + dy)
                        if nb in nodes:
                            persistent.add(nb)

    distorted_rule = derive_local_rule(
        persistent_nodes=frozenset(persistent), postulates=postulates
    )
    distorted_field = derive_node_field(nodes, distorted_rule)

    # Propagate using FREE field (no record yet)
    source = (1, 0)
    detector_x = width
    arrival_times = infer_arrival_times_from_source(nodes, source, free_rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    # State: (node, heading, record_status) -> amplitude
    # record_status: "pre" (before barrier), "free" (crossed without record),
    #                "recorded" (crossed with record)
    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "pre")] = 1.0 + 0.0j

    boundary_distribution: DefaultDict[int, DefaultDict[str, complex]] = defaultdict(
        lambda: defaultdict(complex)
    )

    for node in order:
        matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
        if not matching:
            continue

        if node[0] == detector_x:
            for state, amp in matching:
                boundary_distribution[node[1]][state[2]] += amp
                del states[state]
            continue

        for (cur, heading, status), amp in matching:
            del states[(cur, heading, status)]

            # Choose which field to use based on record status
            if status == "recorded":
                field = distorted_field
            else:
                field = free_field

            for neighbor in dag.get(node, []):
                _delay, _action, link_amp = local_edge_properties(
                    node, neighbor, free_rule, field
                )

                next_status = status

                # At barrier crossing: split into recorded/free
                if node[0] < barrier_x <= neighbor[0] and neighbor[1] in slit_ys:
                    if status == "pre":
                        if record_strength > 0:
                            # Split: recorded path uses distorted field from here
                            rec_amp = link_amp * math.sqrt(record_strength)
                            free_amp = link_amp * math.sqrt(1.0 - record_strength)

                            if neighbor[1] > 0:
                                rec_amp *= cmath.exp(1j * phase_shift_upper)
                                free_amp *= cmath.exp(1j * phase_shift_upper)

                            states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]),
                                    "recorded")] += amp * rec_amp
                            states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]),
                                    "free")] += amp * free_amp
                            continue
                        else:
                            next_status = "free"

                    if neighbor[1] > 0:
                        link_amp *= cmath.exp(1j * phase_shift_upper)

                states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]),
                        next_status)] += amp * link_amp

    # Compute probabilities
    # "recorded" sectors: incoherent (probabilities add)
    # "free"/"pre" sectors: coherent (amplitudes add, then square)
    distribution: dict[int, float] = {}
    for y in screen_positions:
        sector_amps = boundary_distribution.get(y, {})
        coherent_amp = sector_amps.get("free", 0.0) + sector_amps.get("pre", 0.0)
        coherent_prob = abs(coherent_amp) ** 2
        recorded_prob = abs(sector_amps.get("recorded", 0.0)) ** 2
        distribution[y] = coherent_prob + recorded_prob

    if not normalize:
        return distribution
    norm = sum(distribution.values())
    if norm == 0:
        return {y: 0.0 for y in screen_positions}
    return {y: p / norm for y, p in distribution.items()}


def visibility(probs: list[float]) -> float:
    p_max, p_min = max(probs), min(probs)
    denom = p_max + p_min
    return (p_max - p_min) / denom if denom > 0 else 0.0


def main() -> None:
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    height = 10
    width = 20
    slit_ys = {-4, 4}
    screen_ys = list(range(-height, height + 1))

    strengths = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    print("=" * 72)
    print("NON-TRIVIAL DECOHERENCE: Records That Distort the Delay Field")
    print("=" * 72)
    print(f"width={width}, height={height}, slits at y={sorted(slit_ys)}")
    print(f"record_strengths: {strengths}")
    print()

    # Compare trivial (sector-only) vs non-trivial (delay-distortion)
    print("=" * 72)
    print("DECOHERENCE CURVE: V(y) vs record_strength")
    print("=" * 72)
    print()
    print(f"{'strength':>9s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'V(y=2)':>10s}  "
          f"{'mean_V':>10s}  {'trivial_V0':>10s}  {'deviation':>10s}")
    print("-" * 75)

    # Get trivial baseline for comparison: V_trivial = V_0 * (1 - strength)
    baseline_vis = {}
    for y in screen_ys:
        probs = []
        for phase in phases:
            dist = delay_decoherence_two_slit(
                screen_positions=[y], record_strength=0.0,
                width=width, height=height, slit_ys=slit_ys,
                phase_shift_upper=phase, normalize=False,
            )
            probs.append(dist[y])
        baseline_vis[y] = visibility(probs)

    for strength in strengths:
        vis_by_y: dict[int, float] = {}
        for y in screen_ys:
            probs = []
            for phase in phases:
                dist = delay_decoherence_two_slit(
                    screen_positions=[y], record_strength=strength,
                    width=width, height=height, slit_ys=slit_ys,
                    phase_shift_upper=phase, normalize=False,
                )
                probs.append(dist[y])
            vis_by_y[y] = visibility(probs)

        mean_v = sum(vis_by_y.values()) / len(vis_by_y)
        trivial_v0 = baseline_vis[0] * (1.0 - strength)
        deviation = vis_by_y[0] - trivial_v0

        print(f"{strength:9.1f}  {vis_by_y[0]:10.6f}  {vis_by_y.get(1, 0):10.6f}  "
              f"{vis_by_y.get(2, 0):10.6f}  {mean_v:10.6f}  {trivial_v0:10.6f}  "
              f"{deviation:10.6f}")

    print()
    print("If deviation = 0 everywhere: delay distortion has no effect beyond trivial splitting.")
    print("If deviation != 0: the delay-field distortion creates NON-TRIVIAL decoherence.")

    print("\n\nSWEEP COMPLETE")


if __name__ == "__main__":
    main()
