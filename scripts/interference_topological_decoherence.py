#!/usr/bin/env python3
"""Topological decoherence: records that change DAG structure.

The key insight: interference = topology. Field distortion doesn't
cause decoherence. So the record mechanism must change the DAG itself.

Mechanism: when a record forms at a slit with probability p, a new
"detector node" is inserted at the barrier that creates additional
causal edges. These extra edges change the arrival times downstream,
reconfiguring the DAG — the same mechanism that produced I_3 != 0
in the original Sorkin test.

Concretely: at each slit, with probability p, we add a "record node"
one step past the barrier. This node connects to the slit and to
downstream neighbors, creating a shortcut in the causal DAG that
changes which paths exist.

PStack experiment: topological-decoherence
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import heapq
from collections import defaultdict
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    local_edge_properties,
)


def build_dag_with_record_nodes(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    rule,
    node_field: dict,
    record_slit_ys: set[int],
    barrier_x: int,
) -> tuple[dict, dict]:
    """Build causal DAG with extra record-detector nodes past the barrier.

    For each slit in record_slit_ys, adds a virtual node at
    (barrier_x + 0.5, slit_y) that connects slit→record_node and
    record_node→downstream. This creates a shortcut in the DAG.

    We simulate this by adding extra edges from the slit node to
    nodes at (barrier_x+2, slit_y±1) — a "fast lane" that bypasses
    the normal neighbor-to-neighbor propagation.
    """
    # Standard arrival times
    arrival_times: dict[tuple[int, int], float] = {source: 0.0}
    frontier = [(0.0, source)]

    while frontier:
        t, node = heapq.heappop(frontier)
        if t > arrival_times.get(node, float("inf")):
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb not in nodes:
                    continue
                delay, _, _ = local_edge_properties(node, nb, rule, node_field)
                new_t = t + delay
                if new_t < arrival_times.get(nb, float("inf")):
                    arrival_times[nb] = new_t
                    heapq.heappush(frontier, (new_t, nb))

    # Add shortcut edges from record slits
    # The record node at (barrier_x, slit_y) connects to (barrier_x+2, slit_y+dy)
    # with a reduced delay (shortcut), changing arrival times downstream
    for sy in record_slit_ys:
        slit_node = (barrier_x, sy)
        if slit_node not in arrival_times:
            continue
        slit_time = arrival_times[slit_node]
        # Record creates a fast connection to nodes 2 steps past barrier
        for dy in [-1, 0, 1]:
            target = (barrier_x + 2, sy + dy)
            if target not in nodes:
                continue
            # Shortcut delay: half the normal 2-step delay
            shortcut_delay = 1.0  # vs normal ~2.0 for 2 steps
            new_t = slit_time + shortcut_delay
            if new_t < arrival_times.get(target, float("inf")):
                arrival_times[target] = new_t
                # Propagate changed arrival times downstream
                heapq.heappush(frontier, (new_t, target))

    # Re-propagate from changed nodes
    while frontier:
        t, node = heapq.heappop(frontier)
        if t > arrival_times.get(node, float("inf")):
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb not in nodes:
                    continue
                delay, _, _ = local_edge_properties(node, nb, rule, node_field)
                new_t = t + delay
                if new_t < arrival_times.get(nb, float("inf")):
                    arrival_times[nb] = new_t
                    heapq.heappush(frontier, (new_t, nb))

    # Build DAG from arrival times
    dag: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for node in nodes:
        if node not in arrival_times:
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb in nodes and nb in arrival_times:
                    if arrival_times[nb] > arrival_times[node]:
                        dag[node].append(nb)

    return dag, arrival_times


def topological_decoherence_two_slit(
    screen_y: int,
    width: int, height: int,
    slit_ys: set[int],
    record_probability: float,
    phase_shift_upper: float,
) -> float:
    """Compute probability at screen_y with topological record mechanism.

    With probability p: use DAG with record shortcuts (topology changed)
    With probability 1-p: use normal DAG (topology unchanged)

    Probabilities from the two branches add incoherently (the record
    creates a which-path marker that prevents interference between branches).
    """
    barrier_x = width // 2
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    blocked = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    node_field = derive_node_field(nodes, rule)
    source = (1, 0)
    detector_x = width

    def run_pathsum(dag, arrival_times):
        order = sorted(arrival_times, key=arrival_times.get)
        states: DefaultDict[tuple[tuple[int, int], tuple[int, int]], complex] = defaultdict(complex)
        states[(source, (1, 0))] = 1.0 + 0.0j

        for node in order:
            matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
            if not matching:
                continue
            if node[0] == detector_x:
                continue
            for (cur, heading), amp in matching:
                del states[(cur, heading)]
                for nb in dag.get(node, []):
                    _, _, link_amp = local_edge_properties(node, nb, rule, node_field)
                    if node[0] < barrier_x <= nb[0] and nb[1] in slit_ys:
                        if nb[1] > 0:
                            link_amp *= cmath.exp(1j * phase_shift_upper)
                    states[(nb, (nb[0]-node[0], nb[1]-node[1]))] += amp * link_amp

        total_amp = sum(a for (n, _), a in states.items() if n == (detector_x, screen_y))
        return abs(total_amp) ** 2

    # Normal DAG (no record)
    normal_dag, normal_times = {}, {}
    # Build normal arrival times
    normal_times = {source: 0.0}
    frontier = [(0.0, source)]
    while frontier:
        t, node = heapq.heappop(frontier)
        if t > normal_times.get(node, float("inf")):
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb not in nodes:
                    continue
                delay, _, _ = local_edge_properties(node, nb, rule, node_field)
                new_t = t + delay
                if new_t < normal_times.get(nb, float("inf")):
                    normal_times[nb] = new_t
                    heapq.heappush(frontier, (new_t, nb))
    for node in nodes:
        if node not in normal_times:
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb in nodes and nb in normal_times and normal_times[nb] > normal_times[node]:
                    if node not in normal_dag:
                        normal_dag[node] = []
                    normal_dag[node].append(nb)

    # Record DAG (with shortcuts)
    record_dag, record_times = build_dag_with_record_nodes(
        nodes, source, rule, node_field, slit_ys, barrier_x
    )

    p_normal = run_pathsum(normal_dag, normal_times)
    p_record = run_pathsum(record_dag, record_times)

    # Incoherent sum: p * P_record + (1-p) * P_normal
    return record_probability * p_record + (1 - record_probability) * p_normal


def visibility(probs: list[float]) -> float:
    pm, pn = max(probs), min(probs)
    return (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0


def main() -> None:
    width = 20
    height = 10
    slit_ys = {-4, 4}
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    p_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    test_ys = [0, 1, 2, 3]

    print("=" * 72)
    print("TOPOLOGICAL DECOHERENCE: Records That Change the DAG")
    print("=" * 72)
    print(f"width={width}, height={height}, slits at y={sorted(slit_ys)}")
    print("Record mechanism: shortcut edges past barrier (changes arrival times)")
    print()

    # Get baseline V at p=0
    print(f"{'p':>5s}", end="")
    for y in test_ys:
        print(f"  {'V(y='+str(y)+')':>10s}", end="")
    print(f"  {'mean_V':>10s}  {'trivial_V0':>10s}  {'deviation':>10s}")
    print("-" * 72)

    baseline_vis = {}
    for y in test_ys:
        probs = [topological_decoherence_two_slit(y, width, height, slit_ys, 0.0, ph) for ph in phases]
        baseline_vis[y] = visibility(probs)

    for p in p_values:
        vis_by_y = {}
        for y in test_ys:
            probs = [topological_decoherence_two_slit(y, width, height, slit_ys, p, ph) for ph in phases]
            vis_by_y[y] = visibility(probs)

        mean_v = sum(vis_by_y.values()) / len(vis_by_y)
        trivial = baseline_vis[0] * (1 - p)
        dev = vis_by_y[0] - trivial

        print(f"{p:5.1f}", end="")
        for y in test_ys:
            print(f"  {vis_by_y[y]:10.6f}", end="")
        print(f"  {mean_v:10.6f}  {trivial:10.6f}  {dev:10.6f}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
