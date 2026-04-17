#!/usr/bin/env python3
"""Decoherence from topology change during propagation.

Weak decoherence (5/12) with corrected propagator because uniform
attenuation preserves coherence. But the earlier Sorkin test showed
I₃≠0 when the DAG topology changes.

New test: propagate through a two-slit barrier, then MODIFY the graph
between slit and detector (add/remove random edges). This changes
the path structure mid-propagation, breaking the phase relationships
that produce interference.

If topology change reduces V: decoherence from graph dynamics.
If V unchanged: topology change doesn't affect coherence.

Uses corrected propagator (attenuation_mode='geometry') via core API.

PStack experiment: topology-change-decoherence
"""

from __future__ import annotations
import math
import cmath
import random
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
    local_edge_properties,
)


def propagate_with_modified_dag(
    nodes, source, node_field, rule, dag, arrival_times,
    blocked, screen_ys, det_x,
):
    """Propagate on a (possibly modified) DAG."""
    order = sorted(arrival_times, key=arrival_times.get)
    amplitudes = {source: 1.0 + 0.0j}

    for node in order:
        if node not in amplitudes or node in blocked:
            continue
        amp = amplitudes[node]
        for nb in dag.get(node, []):
            if nb in blocked:
                continue
            _, _, link_amp = local_edge_properties(node, nb, rule, node_field)
            if nb not in amplitudes:
                amplitudes[nb] = 0.0 + 0.0j
            amplitudes[nb] += amp * link_amp

    probs = {y: abs(amplitudes.get((det_x, y), 0.0)) ** 2 for y in screen_ys}
    total = sum(probs.values())
    if total > 0:
        probs = {y: p / total for y, p in probs.items()}
    return probs


def visibility(probs, screen_ys):
    vals = [probs.get(y, 0) for y in sorted(screen_ys)]
    peaks = [vals[i] for i in range(1, len(vals) - 1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals) - 1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks) - min(troughs)) / (max(peaks) + min(troughs))
    return 0.0


def modify_dag_edges(dag, nodes, region_x_min, region_x_max, height,
                     n_add=0, n_remove=0, rng=None):
    """Add or remove random edges in a region of the DAG."""
    rng = rng or random.Random(42)
    new_dag = {k: list(v) for k, v in dag.items()}

    # Collect edges in region
    region_edges = []
    region_nodes = [(x, y) for x, y in nodes
                    if region_x_min <= x <= region_x_max]

    for node in region_nodes:
        for nb in new_dag.get(node, []):
            if region_x_min <= nb[0] <= region_x_max:
                region_edges.append((node, nb))

    # Remove random edges
    if n_remove > 0 and region_edges:
        to_remove = rng.sample(region_edges, min(n_remove, len(region_edges)))
        for node, nb in to_remove:
            if nb in new_dag.get(node, []):
                new_dag[node].remove(nb)

    # Add random forward edges
    for _ in range(n_add):
        n1 = rng.choice(region_nodes)
        candidates = [(x, y) for x, y in region_nodes
                      if x > n1[0] and math.dist(n1, (x, y)) < 2.5]
        if candidates:
            n2 = rng.choice(candidates)
            if n2 not in new_dag.get(n1, []):
                if n1 not in new_dag:
                    new_dag[n1] = []
                new_dag[n1].append(n2)

    return new_dag


def main() -> None:
    width = 50
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))

    barrier_x = 20
    det_x = 40
    slit_ys = [-4, 4]

    # Build barrier
    barrier_all = set()
    for y in range(-height, height + 1):
        barrier_all.add((barrier_x, y))
    slit_nodes = set()
    for sy in slit_ys:
        for y in range(sy - 1, sy + 2):
            slit_nodes.add((barrier_x, y))
    blocked = barrier_all - slit_nodes

    print("=" * 80)
    print("TOPOLOGY-CHANGE DECOHERENCE")
    print(f"  Grid: {width}x{2*height+1}, barrier at x={barrier_x}, det at x={det_x}")
    print("  Corrected propagator: attenuation_mode='geometry'")
    print("=" * 80)
    print()

    # ================================================================
    # TEST 1: Edge removal between slit and detector
    # ================================================================
    print("TEST 1: Remove random edges between slit and detector")
    print("  Region: x=[25, 35]")
    print()

    # Use corrected propagator
    postulates = RulePostulates(
        phase_per_action=2.0, attenuation_power=1.0,
        attenuation_mode="geometry",
    )
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)

    # Baseline: no modification
    baseline = propagate_with_modified_dag(
        nodes, source, field, rule, dag, arrival_times,
        blocked, screen_ys, det_x,
    )
    v_baseline = visibility(baseline, screen_ys)
    print(f"  Baseline V: {v_baseline:.4f}")
    print()

    print(f"  {'n_remove':>8s}  {'mean_V':>8s}  {'V_drop':>8s}  {'n_seeds':>7s}")
    print(f"  {'-' * 36}")

    for n_rem in [0, 10, 30, 50, 100, 200, 500, 1000]:
        v_list = []
        for seed in range(10):
            rng = random.Random(seed * 7 + 13)
            mod_dag = modify_dag_edges(
                dag, nodes, 25, 35, height,
                n_add=0, n_remove=n_rem, rng=rng,
            )
            probs = propagate_with_modified_dag(
                nodes, source, field, rule, mod_dag, arrival_times,
                blocked, screen_ys, det_x,
            )
            v_list.append(visibility(probs, screen_ys))

        mean_v = sum(v_list) / len(v_list)
        v_drop = v_baseline - mean_v
        print(f"  {n_rem:8d}  {mean_v:8.4f}  {v_drop:+8.4f}  {len(v_list):7d}")

    # ================================================================
    # TEST 2: Edge addition between slit and detector
    # ================================================================
    print()
    print("TEST 2: Add random edges between slit and detector")
    print()

    print(f"  {'n_add':>8s}  {'mean_V':>8s}  {'V_drop':>8s}")
    print(f"  {'-' * 28}")

    for n_add in [0, 10, 30, 50, 100, 200, 500]:
        v_list = []
        for seed in range(10):
            rng = random.Random(seed * 7 + 13)
            mod_dag = modify_dag_edges(
                dag, nodes, 25, 35, height,
                n_add=n_add, n_remove=0, rng=rng,
            )
            probs = propagate_with_modified_dag(
                nodes, source, field, rule, mod_dag, arrival_times,
                blocked, screen_ys, det_x,
            )
            v_list.append(visibility(probs, screen_ys))

        mean_v = sum(v_list) / len(v_list)
        v_drop = v_baseline - mean_v
        print(f"  {n_add:8d}  {mean_v:8.4f}  {v_drop:+8.4f}")

    # ================================================================
    # TEST 3: Mixed modification (add + remove)
    # ================================================================
    print()
    print("TEST 3: Simultaneous add + remove (topology scramble)")
    print()

    print(f"  {'n_mod':>8s}  {'mean_V':>8s}  {'V_drop':>8s}  {'decoh%':>6s}")
    print(f"  {'-' * 36}")

    for n_mod in [0, 10, 30, 50, 100, 200, 500]:
        v_list = []
        for seed in range(10):
            rng = random.Random(seed * 7 + 13)
            mod_dag = modify_dag_edges(
                dag, nodes, 25, 35, height,
                n_add=n_mod, n_remove=n_mod, rng=rng,
            )
            probs = propagate_with_modified_dag(
                nodes, source, field, rule, mod_dag, arrival_times,
                blocked, screen_ys, det_x,
            )
            v_list.append(visibility(probs, screen_ys))

        mean_v = sum(v_list) / len(v_list)
        v_drop = v_baseline - mean_v
        decoh_pct = 100 * v_drop / v_baseline if v_baseline > 0 else 0
        print(f"  {n_mod:8d}  {mean_v:8.4f}  {v_drop:+8.4f}  {decoh_pct:5.1f}%")

    print()
    print("=" * 80)
    print("INTERPRETATION")
    print("=" * 80)
    print()
    print("If V drops with topology change: decoherence from graph dynamics.")
    print("The amount of V drop = decoherence strength.")
    print("This would mean: decoherence requires the graph to CHANGE,")
    print("not just have a field. The corrected propagator's weak decoherence")
    print("is correct for a STATIC graph. Dynamic graphs produce decoherence.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
