#!/usr/bin/env python3
"""Asymmetric decoherence: distort the delay field at ONE slit only.

The symmetric case (both slits distorted) showed V unchanged because
the relative phase structure was preserved. Distorting only one slit
breaks this symmetry — the two paths now traverse DIFFERENT delay
fields, which should produce non-trivial V(p) != V_0(1-p).

PStack experiment: asymmetric-decoherence
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
    graph_neighbors,
    boundary_nodes,
    derive_persistence_support,
)


def build_one_slit_distorted_field(
    nodes: set[tuple[int, int]],
    distort_slit_y: int,
    barrier_x: int,
    radius: int,
) -> dict[tuple[int, int], float]:
    """Build delay field with persistent nodes around ONE slit only."""
    persistent = set()
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            nb = (barrier_x + dx, distort_slit_y + dy)
            if nb in nodes:
                persistent.add(nb)
    pnodes = frozenset(persistent)
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
    return derive_node_field(nodes, rule)


def asymmetric_decoherence_sweep(
    width: int, height: int, slit_ys: set[int],
    distort_slit_y: int, cluster_radius: int,
    p_values: list[float], n_phases: int = 24,
) -> list[dict]:
    """Sweep record probability with ONE slit's field distorted."""
    barrier_x = width // 2
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    blocked = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked)
    source = (1, 0)
    detector_x = width
    screen_ys = list(range(-height, height + 1))

    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    free_field = derive_node_field(nodes, free_rule)
    distorted_field = build_one_slit_distorted_field(nodes, distort_slit_y, barrier_x, cluster_radius)

    field_diffs = sum(1 for n in nodes if abs(distorted_field.get(n, 0) - free_field.get(n, 0)) > 1e-10)

    arrival_times = infer_arrival_times_from_source(nodes, source, free_rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    results = []
    for p in p_values:
        vis_by_y: dict[int, float] = {}
        for y in screen_ys:
            probs = []
            for phase in phases:
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
                        # Recorded sector uses distorted field
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

                coh = boundary_amps.get("free", 0.0) + boundary_amps.get("pre", 0.0)
                prob = abs(coh) ** 2 + abs(boundary_amps.get("recorded", 0.0)) ** 2
                probs.append(prob)

            pm, pn = max(probs), min(probs)
            vis_by_y[y] = (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0

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
    print("ASYMMETRIC DECOHERENCE: Distort ONE Slit Only")
    print("=" * 72)
    print(f"width={width}, height={height}, slits at y={sorted(slit_ys)}")
    print(f"Distorted slit: y=+4 (upper), undistorted: y=-4 (lower)")
    print()

    for radius in [1, 2]:
        print(f"\n{'=' * 60}")
        print(f"CLUSTER RADIUS = {radius} (at upper slit y=+4 only)")
        print(f"{'=' * 60}")

        results = asymmetric_decoherence_sweep(
            width, height, slit_ys, distort_slit_y=4,
            cluster_radius=radius, p_values=p_values,
        )

        v0_base = results[0]["V0"]
        print(f"  Field nodes changed: {results[0]['field_diffs']}")
        print()
        print(f"  {'p':>5s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'mean_V':>10s}  "
              f"{'trivial':>10s}  {'deviation':>10s}  {'dev%':>8s}")
        print(f"  {'-' * 68}")

        for r in results:
            trivial = v0_base * (1 - r["p"])
            dev = r["V0"] - trivial
            dev_pct = (dev / trivial * 100) if trivial > 0 else 0
            print(f"  {r['p']:5.1f}  {r['V0']:10.6f}  {r['V1']:10.6f}  {r['mean_V']:10.6f}  "
                  f"{trivial:10.6f}  {dev:10.6f}  {dev_pct:7.2f}%")

    print()
    print("If deviation != 0: asymmetric delay distortion creates NON-TRIVIAL decoherence.")
    print("The deviation measures how much the model's decoherence differs from trivial V_0(1-p).")
    print("\n\nSWEEP COMPLETE")


if __name__ == "__main__":
    main()
