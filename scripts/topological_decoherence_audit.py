#!/usr/bin/env python3
"""Audit the topological decoherence V-increase.

Why do DAG shortcuts INCREASE visibility instead of decreasing it?
Decompose per-slit amplitudes on normal vs record DAGs to find out.

Also test: what if the record DAG only has shortcuts at ONE slit
(asymmetric topology change)? Does that produce V-decrease?

PStack investigation: topological-decoherence-audit
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


def build_dag_from_arrivals(nodes, arrival_times):
    dag = defaultdict(list)
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
    return dag


def compute_arrivals(nodes, source, rule, node_field):
    arrival_times = {source: 0.0}
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
    return arrival_times


def add_shortcuts(arrival_times, nodes, slit_ys, barrier_x, rule, node_field):
    """Add shortcut edges from specified slits, re-propagate."""
    at = dict(arrival_times)
    frontier = []
    for sy in slit_ys:
        slit_node = (barrier_x, sy)
        if slit_node not in at:
            continue
        for dy in [-1, 0, 1]:
            target = (barrier_x + 2, sy + dy)
            if target not in nodes:
                continue
            new_t = at[slit_node] + 1.0
            if new_t < at.get(target, float("inf")):
                at[target] = new_t
                heapq.heappush(frontier, (new_t, target))
    while frontier:
        t, node = heapq.heappop(frontier)
        if t > at.get(node, float("inf")):
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
                if new_t < at.get(nb, float("inf")):
                    at[nb] = new_t
                    heapq.heappush(frontier, (new_t, nb))
    return at


def per_slit_pathsum(dag, arrival_times, source, detector_x, screen_y,
                     slit_ys, barrier_x, rule, node_field, phase):
    """Run path-sum tracking which slit each path went through."""
    order = sorted(arrival_times, key=arrival_times.get)
    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "pre")] = 1.0 + 0.0j
    result: DefaultDict[str, complex] = defaultdict(complex)

    for node in order:
        matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
        if not matching:
            continue
        if node[0] == detector_x and node[1] == screen_y:
            for state, amp in matching:
                result[state[2]] += amp
                del states[state]
            continue
        if node[0] == detector_x:
            for state, _ in matching:
                del states[state]
            continue
        for (cur, heading, slit_label), amp in matching:
            del states[(cur, heading, slit_label)]
            for nb in dag.get(node, []):
                _, _, link_amp = local_edge_properties(node, nb, rule, node_field)
                new_label = slit_label
                if node[0] < barrier_x <= nb[0] and nb[1] in slit_ys:
                    new_label = f"slit_{nb[1]}"
                    if nb[1] > 0:
                        link_amp *= cmath.exp(1j * phase)
                nh = (nb[0]-node[0], nb[1]-node[1])
                states[(nb, nh, new_label)] += amp * link_amp

    return dict(result)


def main() -> None:
    width = 20
    height = 10
    slit_ys = {-4, 4}
    barrier_x = 10
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    blocked = frozenset((barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys)
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    node_field = derive_node_field(nodes, rule)
    source = (1, 0)
    detector_x = width

    normal_at = compute_arrivals(nodes, source, rule, node_field)
    shortcut_both_at = add_shortcuts(normal_at, nodes, slit_ys, barrier_x, rule, node_field)
    shortcut_upper_at = add_shortcuts(normal_at, nodes, {4}, barrier_x, rule, node_field)

    normal_dag = build_dag_from_arrivals(nodes, normal_at)
    shortcut_both_dag = build_dag_from_arrivals(nodes, shortcut_both_at)
    shortcut_upper_dag = build_dag_from_arrivals(nodes, shortcut_upper_at)

    print("=" * 72)
    print("TOPOLOGICAL DECOHERENCE AUDIT")
    print("=" * 72)
    print()

    # 1. DAG difference count
    def edge_count(dag):
        return sum(len(nbs) for nbs in dag.values())

    def edge_set(dag):
        return {(n, nb) for n, nbs in dag.items() for nb in nbs}

    ne = edge_set(normal_dag)
    se = edge_set(shortcut_both_dag)
    print(f"Normal DAG edges: {len(ne)}")
    print(f"Shortcut-both DAG edges: {len(se)}")
    print(f"Edges added: {len(se - ne)}")
    print(f"Edges removed: {len(ne - se)}")
    print(f"Net edge change: {len(se) - len(ne)}")
    print()

    # 2. Arrival time differences
    diffs = [(n, shortcut_both_at[n] - normal_at[n]) for n in nodes
             if n in normal_at and n in shortcut_both_at and abs(shortcut_both_at[n] - normal_at[n]) > 1e-10]
    print(f"Nodes with changed arrival times: {len(diffs)}")
    if diffs:
        diffs.sort(key=lambda x: x[1])
        print(f"Max speedup: {diffs[0][1]:.4f} at {diffs[0][0]}")
        print(f"Max slowdown: {diffs[-1][1]:.4f} at {diffs[-1][0]}")
    print()

    # 3. Per-slit amplitude decomposition at y=3 (where V changes most)
    print("=" * 72)
    print("PER-SLIT AMPLITUDES at y=3, phase=0")
    print("=" * 72)
    print()

    for dag_label, dag, at in [("NORMAL", normal_dag, normal_at),
                                 ("SHORTCUT-BOTH", shortcut_both_dag, shortcut_both_at),
                                 ("SHORTCUT-UPPER-ONLY", shortcut_upper_dag, shortcut_upper_at)]:
        amps = per_slit_pathsum(dag, at, source, detector_x, 3, slit_ys, barrier_x, rule, node_field, 0.0)
        print(f"  {dag_label}:")
        for label, amp in sorted(amps.items()):
            print(f"    {label:>15s}: |A| = {abs(amp):.6e}  phase = {math.degrees(cmath.phase(amp)):+.1f}°")
        total = sum(amps.values())
        print(f"    {'TOTAL':>15s}: |A| = {abs(total):.6e}")
        # Amplitude ratio
        slit_amps = {k: abs(v) for k, v in amps.items() if k.startswith("slit")}
        if len(slit_amps) == 2:
            vals = sorted(slit_amps.values())
            print(f"    amplitude ratio (far/near): {vals[0]/vals[1]:.6f}")
        print()

    # 4. Visibility sweep for ASYMMETRIC shortcut (upper slit only)
    print("=" * 72)
    print("ASYMMETRIC TOPOLOGICAL DECOHERENCE (shortcut at upper slit only)")
    print("=" * 72)
    print()

    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    p_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

    print(f"{'p':>5s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'V(y=2)':>10s}  {'V(y=3)':>10s}")
    print("-" * 48)

    for p in p_values:
        vis = {}
        for y in [0, 1, 2, 3]:
            probs = []
            for phase in phases:
                # Normal pathsum
                amps_n = per_slit_pathsum(normal_dag, normal_at, source, detector_x, y,
                                          slit_ys, barrier_x, rule, node_field, phase)
                p_normal = abs(sum(amps_n.values())) ** 2

                # Shortcut-upper pathsum
                amps_s = per_slit_pathsum(shortcut_upper_dag, shortcut_upper_at, source, detector_x, y,
                                          slit_ys, barrier_x, rule, node_field, phase)
                p_shortcut = abs(sum(amps_s.values())) ** 2

                prob = (1 - p) * p_normal + p * p_shortcut
                probs.append(prob)

            pm, pn = max(probs), min(probs)
            vis[y] = (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0

        print(f"{p:5.1f}  {vis[0]:10.6f}  {vis[1]:10.6f}  {vis[2]:10.6f}  {vis[3]:10.6f}")

    print()
    print("AUDIT COMPLETE")


if __name__ == "__main__":
    main()
