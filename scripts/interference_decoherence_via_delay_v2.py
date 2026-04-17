#!/usr/bin/env python3
"""Non-trivial decoherence v2: graduated persistent-node clusters.

Fixed: v1 used isolated slit nodes (zero support). v2 uses
clusters of adjacent nodes around each slit so the delay field
actually changes.

The record_strength parameter now controls BOTH:
1. The amplitude split ratio (√p for recorded, √(1-p) for free)
2. The size of the persistent-node cluster at each slit

PStack experiment: decoherence-via-delay-v2
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


def build_slit_cluster(slit_y: int, barrier_x: int, radius: int,
                       nodes: set[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    """Build a cluster of persistent nodes around a slit position."""
    cluster = set()
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            nb = (barrier_x + dx, slit_y + dy)
            if nb in nodes:
                cluster.add(nb)
    return frozenset(cluster)


def decoherence_sweep(
    width: int, height: int, slit_ys: set[int],
    cluster_radius: int, p_values: list[float],
    n_phases: int = 24,
) -> list[dict]:
    """Sweep record probability p with fixed cluster radius."""
    barrier_x = width // 2
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    blocked_nodes = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked_nodes)
    source = (1, 0)
    detector_x = width
    screen_ys = list(range(-height, height + 1))

    # Build fields
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    free_field = derive_node_field(nodes, free_rule)

    persistent = set()
    for sy in slit_ys:
        persistent |= set(build_slit_cluster(sy, barrier_x, cluster_radius, nodes))
    distorted_rule = derive_local_rule(persistent_nodes=frozenset(persistent), postulates=postulates)
    distorted_field = derive_node_field(nodes, distorted_rule)

    # Check field difference
    field_diffs = sum(1 for n in nodes if abs(distorted_field.get(n, 0) - free_field.get(n, 0)) > 1e-10)

    # Build DAG (same for all p — topology doesn't change)
    arrival_times = infer_arrival_times_from_source(nodes, source, free_rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    results = []

    for p in p_values:
        vis_by_y: dict[int, float] = {}

        for y in screen_ys:
            probs_across_phase = []

            for phase in phases:
                # Propagate
                states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
                states[(source, (1, 0), "pre")] = 1.0 + 0.0j
                boundary_amps: DefaultDict[str, complex] = defaultdict(complex)

                for node in order:
                    matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
                    if not matching:
                        continue
                    if node[0] == detector_x and node[1] == y:
                        for state, amp in matching:
                            boundary_amps[state[2]] += amp
                            del states[state]
                        continue
                    if node[0] == detector_x:
                        for state, _ in matching:
                            del states[state]
                        continue

                    for (cur, heading, status), amp in matching:
                        del states[(cur, heading, status)]
                        field = distorted_field if status == "recorded" else free_field

                        for neighbor in dag.get(node, []):
                            _, _, link_amp = local_edge_properties(
                                node, neighbor, free_rule, field
                            )
                            next_status = status

                            if node[0] < barrier_x <= neighbor[0] and neighbor[1] in slit_ys:
                                if status == "pre" and p > 0:
                                    rec_link = link_amp * math.sqrt(p)
                                    free_link = link_amp * math.sqrt(1 - p)
                                    if neighbor[1] > 0:
                                        rec_link *= cmath.exp(1j * phase)
                                        free_link *= cmath.exp(1j * phase)
                                    nh = (neighbor[0]-node[0], neighbor[1]-node[1])
                                    states[(neighbor, nh, "recorded")] += amp * rec_link
                                    states[(neighbor, nh, "free")] += amp * free_link
                                    continue
                                elif status == "pre":
                                    next_status = "free"
                                if neighbor[1] > 0:
                                    link_amp *= cmath.exp(1j * phase)

                            nh = (neighbor[0]-node[0], neighbor[1]-node[1])
                            states[(neighbor, nh, next_status)] += amp * link_amp

                coherent_amp = boundary_amps.get("free", 0.0) + boundary_amps.get("pre", 0.0)
                prob = abs(coherent_amp) ** 2 + abs(boundary_amps.get("recorded", 0.0)) ** 2
                probs_across_phase.append(prob)

            p_max, p_min = max(probs_across_phase), min(probs_across_phase)
            vis_by_y[y] = (p_max - p_min) / (p_max + p_min) if (p_max + p_min) > 0 else 0.0

        mean_v = sum(vis_by_y.values()) / len(vis_by_y)
        results.append({
            "p": p, "V0": vis_by_y[0], "V1": vis_by_y.get(1, 0),
            "V2": vis_by_y.get(2, 0), "mean_V": mean_v, "field_diffs": field_diffs,
        })

    return results


def main() -> None:
    width = 20
    height = 10
    slit_ys = {-4, 4}
    p_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    print("=" * 72)
    print("NON-TRIVIAL DECOHERENCE v2: Graduated Persistent-Node Clusters")
    print("=" * 72)
    print()

    for radius in [1, 2, 3]:
        print(f"\n{'=' * 60}")
        print(f"CLUSTER RADIUS = {radius}")
        print(f"{'=' * 60}")

        results = decoherence_sweep(width, height, slit_ys, radius, p_values)

        print(f"  Field nodes changed: {results[0]['field_diffs']}")
        print()
        print(f"  {'p':>5s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'V(y=2)':>10s}  "
              f"{'mean_V':>10s}  {'trivial':>10s}  {'deviation':>10s}")
        print(f"  {'-' * 68}")

        v0_baseline = results[0]["V0"]
        for r in results:
            trivial = v0_baseline * (1 - r["p"])
            dev = r["V0"] - trivial
            print(f"  {r['p']:5.1f}  {r['V0']:10.6f}  {r['V1']:10.6f}  {r['V2']:10.6f}  "
                  f"{r['mean_V']:10.6f}  {trivial:10.6f}  {dev:10.6f}")

    print("\n\nSWEEP COMPLETE")


if __name__ == "__main__":
    main()
