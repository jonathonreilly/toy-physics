#!/usr/bin/env python3
"""Prototype: evolving network dynamics (Axiom 1).

The model currently uses static rectangular grids. Axiom 1 says
"reality is an evolving network." This prototype implements the
simplest possible graph evolution: new events are created at the
network frontier, old events become frozen, and the graph GROWS.

The key question: can interference, gravity, and persistence
survive on an evolving (growing) graph?

Approach:
1. Start with a small seed grid
2. At each step, add new events at the frontier (nodes adjacent
   to the current boundary)
3. Compute the delay field and path-sum on the growing graph
4. Measure whether interference and gravity appear at each stage

This is NOT a full dynamical theory — it's a proof-of-concept
that the model's phenomena can exist on non-static graphs.

PStack experiment: evolving-network-prototype
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict
from typing import DefaultDict
import heapq

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    derive_local_rule,
    derive_node_field,
    local_edge_properties,
    derive_persistence_support,
    graph_neighbors,
    boundary_nodes,
)


def grow_network(
    seed_nodes: set[tuple[int, int]],
    growth_steps: int,
    max_height: int = 20,
) -> list[set[tuple[int, int]]]:
    """Grow network from seed by adding frontier nodes at each step."""
    snapshots = [set(seed_nodes)]
    current = set(seed_nodes)

    for _ in range(growth_steps):
        frontier = set()
        for node in current:
            x, y = node
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nb = (x + dx, y + dy)
                    if nb not in current and abs(nb[1]) <= max_height:
                        frontier.add(nb)
        current = current | frontier
        snapshots.append(set(current))

    return snapshots


def measure_interference_on_graph(
    nodes: set[tuple[int, int]],
    source: tuple[int, int],
    slit_ys: set[int],
    barrier_x: int,
    detector_x: int,
    screen_ys: list[int],
    n_phases: int = 12,
) -> dict[int, float]:
    """Measure fringe visibility on an arbitrary node set."""
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    node_field = derive_node_field(nodes, rule)

    # Build arrival times
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

    # Build DAG
    dag: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    for node in nodes:
        if node not in arrival_times:
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nb = (node[0] + dx, node[1] + dy)
                if nb in nodes and nb in arrival_times and arrival_times[nb] > arrival_times[node]:
                    dag[node].append(nb)

    # Add barrier blocking
    blocked_at_barrier = set()
    for node in nodes:
        if node[0] == barrier_x and node[1] not in slit_ys:
            blocked_at_barrier.add(node)

    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    vis_by_y: dict[int, float] = {}

    for y in screen_ys:
        if (detector_x, y) not in nodes:
            vis_by_y[y] = -1.0  # Not reachable
            continue

        probs = []
        for phase in phases:
            states: DefaultDict[tuple[tuple[int, int], tuple[int, int]], complex] = defaultdict(complex)
            states[(source, (1, 0))] = 1.0 + 0.0j

            order = sorted(arrival_times, key=arrival_times.get)
            for node in order:
                matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
                if not matching:
                    continue
                if node[0] == detector_x:
                    continue
                if node in blocked_at_barrier:
                    for state, _ in matching:
                        del states[state]
                    continue
                for (cur, heading), amp in matching:
                    del states[(cur, heading)]
                    for nb in dag.get(node, []):
                        if nb in blocked_at_barrier:
                            continue
                        _, _, link_amp = local_edge_properties(node, nb, rule, node_field)
                        if node[0] < barrier_x <= nb[0] and nb[1] in slit_ys:
                            if nb[1] > 0:
                                link_amp *= cmath.exp(1j * phase)
                        states[(nb, (nb[0]-node[0], nb[1]-node[1]))] += amp * link_amp

            total_amp = sum(a for (n, _), a in states.items() if n == (detector_x, y))
            probs.append(abs(total_amp) ** 2)

        if probs:
            pm, pn = max(probs), min(probs)
            vis_by_y[y] = (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0
        else:
            vis_by_y[y] = 0.0

    return vis_by_y


def main() -> None:
    print("=" * 72)
    print("EVOLVING NETWORK PROTOTYPE")
    print("=" * 72)
    print()

    # Start with a thin seed strip
    seed = {(x, y) for x in range(0, 5) for y in range(-3, 4)}
    print(f"Seed: {len(seed)} nodes, x=[0,4], y=[-3,3]")
    print()

    snapshots = grow_network(seed, growth_steps=20, max_height=15)

    print("Growth history:")
    for i, snap in enumerate(snapshots):
        min_x = min(x for x, _ in snap)
        max_x = max(x for x, _ in snap)
        min_y = min(y for _, y in snap)
        max_y = max(y for _, y in snap)
        print(f"  Step {i:2d}: {len(snap):5d} nodes, x=[{min_x},{max_x}], y=[{min_y},{max_y}]")

    # =========================================================
    # Test interference at selected growth stages
    # =========================================================
    print()
    print("=" * 72)
    print("INTERFERENCE ON GROWING GRAPH")
    print("=" * 72)
    print()

    for step_idx in [5, 10, 15, 20]:
        if step_idx >= len(snapshots):
            continue
        snap = snapshots[step_idx]
        max_x = max(x for x, _ in snap)
        min_y = min(y for _, y in snap)
        max_y = max(y for _, y in snap)

        if max_x < 10:
            print(f"  Step {step_idx}: grid too small (max_x={max_x})")
            continue

        barrier_x = max_x // 2
        detector_x = max_x
        source = (0, 0)
        slit_sep = min(4, (max_y - min_y) // 4)
        if slit_sep < 1:
            continue
        slit_ys = {-slit_sep, slit_sep}
        screen_ys = list(range(min_y, max_y + 1))

        vis = measure_interference_on_graph(
            snap, source, slit_ys, barrier_x, detector_x, screen_ys
        )
        valid_vis = {y: v for y, v in vis.items() if v >= 0}
        mean_v = sum(valid_vis.values()) / len(valid_vis) if valid_vis else 0
        v_at_0 = vis.get(0, -1)

        print(f"  Step {step_idx}: {len(snap)} nodes, barrier_x={barrier_x}, "
              f"slits=±{slit_sep}, V(y=0)={v_at_0:.6f}, mean_V={mean_v:.6f}")

    # =========================================================
    # Test gravity at selected growth stages
    # =========================================================
    print()
    print("=" * 72)
    print("GRAVITY ON GROWING GRAPH")
    print("=" * 72)
    print()

    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    for step_idx in [10, 15, 20]:
        if step_idx >= len(snapshots):
            continue
        snap = snapshots[step_idx]
        max_x = max(x for x, _ in snap)

        if max_x < 15:
            print(f"  Step {step_idx}: grid too small")
            continue

        # Place mass at center
        mass_x = max_x // 2
        mass_nodes = frozenset((mass_x, y) for y in [3, 4, 5, 6, 7] if (mass_x, y) in snap)

        if len(mass_nodes) < 2:
            print(f"  Step {step_idx}: not enough mass nodes")
            continue

        rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
        field = derive_node_field(snap, rule)

        # Measure field at center vs edge
        f_center = field.get((mass_x, 0), 0)
        f_edge_r = field.get((max_x, 0), 0)
        f_edge_l = field.get((0, 0), 0)

        support = derive_persistence_support(snap, mass_nodes)
        max_support = max(support.values())

        print(f"  Step {step_idx}: {len(snap)} nodes, {len(mass_nodes)} mass nodes, "
              f"max_support={max_support:.4f}, "
              f"field(center)={f_center:.6f}, field(edge)={f_edge_r:.6f}")

    print()
    print("PROTOTYPE COMPLETE")


if __name__ == "__main__":
    main()
