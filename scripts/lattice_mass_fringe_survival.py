#!/usr/bin/env python3
"""Why does mass kill fringes on the lattice but not on DAGs?

Lattice at k=2.0: V_free=0.987, V_with_mass=0.000.
DAGs at k=5.0: V_free=0.99, V_with_mass=0.95.

Hypotheses:
A. Phase uniformity: on lattice, ALL paths through mass get the same
   phase shift → uniform cancellation. On DAGs, varied path lengths
   give varied phase shifts → some fringes survive.
B. k-regime: k=2.0 happens to be where mass-induced phase shift is
   exactly π (destructive). Different k might preserve fringes.
C. Mass size: lattice mass is 5 nodes, DAG mass is 10-20.

Test: sweep k on lattice WITH mass, find if any k preserves V>0.

PStack experiment: lattice-mass-fringe-survival
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
    local_edge_properties,
)


def propagate_grid(nodes, source, field, rule, blocked, screen_ys, det_x):
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)
    amps = {source: 1.0+0.0j}
    for node in order:
        if node not in amps or node in blocked:
            continue
        a = amps[node]
        for nb in dag.get(node, []):
            if nb in blocked:
                continue
            _, _, la = local_edge_properties(node, nb, rule, field)
            if nb not in amps:
                amps[nb] = 0.0+0.0j
            amps[nb] += a*la
    probs = {}
    total = 0
    for y in screen_ys:
        p = abs(amps.get((det_x, y), 0.0))**2
        probs[y] = p
        total += p
    if total > 0:
        probs = {y: p/total for y, p in probs.items()}
    return probs


def visibility(probs):
    ys = sorted(probs.keys())
    vals = [probs[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals)-1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def main():
    width = 50
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height+1))
    det_x = 40
    barrier_x = 20

    slit_ys = [-4, 4]
    barrier = set((barrier_x, y) for y in range(-height, height+1))
    slit_nodes = set()
    for sy in slit_ys:
        for y in range(sy-1, sy+2):
            slit_nodes.add((barrier_x, y))
    blocked = barrier - slit_nodes

    print("=" * 70)
    print("WHY DOES MASS KILL FRINGES ON LATTICE?")
    print("=" * 70)
    print()

    # TEST 1: k sweep with mass present
    print("TEST 1: k sweep — V_free vs V_mass on lattice")
    print(f"  Mass at x=25, y=4..8 (downstream of barrier)")
    print()

    mass_nodes = frozenset((25, y) for y in range(4, 9))

    print(f"  {'k':>5s}  {'V_free':>8s}  {'V_mass':>8s}  {'V_drop':>8s}")
    print(f"  {'-' * 32}")

    for k in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0]:
        post = RulePostulates(phase_per_action=k, attenuation_power=1.0,
                              attenuation_mode="geometry")
        rule_f = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
        field_f = derive_node_field(nodes, rule_f)
        pf = propagate_grid(nodes, source, field_f, rule_f, blocked, screen_ys, det_x)
        vf = visibility(pf)

        rule_m = derive_local_rule(persistent_nodes=mass_nodes, postulates=post)
        field_m = derive_node_field(nodes, rule_m)
        pm = propagate_grid(nodes, source, field_m, rule_m, blocked, screen_ys, det_x)
        vm = visibility(pm)

        print(f"  {k:5.1f}  {vf:8.4f}  {vm:8.4f}  {vf-vm:+8.4f}")

    # TEST 2: Mass position sweep at k=2
    print()
    print("TEST 2: Mass position sweep at k=2.0")
    print(f"  Mass: 3 nodes at varying (x, y=6)")
    print()

    print(f"  {'mass_x':>6s}  {'V_mass':>8s}")
    print(f"  {'-' * 18}")

    for mx in [5, 10, 15, 22, 25, 30, 35, 40]:
        mn = frozenset((mx, y) for y in range(5, 8))
        post = RulePostulates(phase_per_action=2.0, attenuation_power=1.0,
                              attenuation_mode="geometry")
        rule_m = derive_local_rule(persistent_nodes=mn, postulates=post)
        field_m = derive_node_field(nodes, rule_m)
        pm = propagate_grid(nodes, source, field_m, rule_m, blocked, screen_ys, det_x)
        vm = visibility(pm)
        print(f"  {mx:6d}  {vm:8.4f}")

    # TEST 3: Mass size sweep
    print()
    print("TEST 3: Mass size sweep at k=2.0, x=25")
    print()

    print(f"  {'n_mass':>6s}  {'V_mass':>8s}")
    print(f"  {'-' * 18}")

    for n in [1, 2, 3, 5, 7, 10]:
        half = n//2
        mn = frozenset((25, y) for y in range(6-half, 6+half+1))
        post = RulePostulates(phase_per_action=2.0, attenuation_power=1.0,
                              attenuation_mode="geometry")
        rule_m = derive_local_rule(persistent_nodes=mn, postulates=post)
        field_m = derive_node_field(nodes, rule_m)
        pm = propagate_grid(nodes, source, field_m, rule_m, blocked, screen_ys, det_x)
        vm = visibility(pm)
        print(f"  {len(mn):6d}  {vm:8.4f}")

    print()
    print("If V_mass > 0 at some k: the fringe destruction is k-specific.")
    print("If V_mass = 0 at all k: the lattice geometry prevents coexistence.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
