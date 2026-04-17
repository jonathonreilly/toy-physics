#!/usr/bin/env python3
"""Phase noise: ensemble-averaged decoherence.

Per-realization V stays high because each is a coherent path-sum.
The proper decoherence measure: average P(y) over realizations, THEN
compute V. If different realizations have shifted fringes, the average
smooths them → V drops.

Also: gravity (centroid shift) should survive averaging because it
doesn't depend on fringe positions.

PStack experiment: phase-noise-ensemble-avg
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
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
    local_edge_properties,
)


def propagate_noisy(nodes, source, field, rule, dag, arrival,
                    blocked, screen_ys, det_x, eta, rng):
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
            la *= cmath.exp(1j * eta * rng.gauss(0, 1))
            if nb not in amps:
                amps[nb] = 0.0+0.0j
            amps[nb] += a * la
    return {y: abs(amps.get((det_x, y), 0.0))**2 for y in screen_ys}


def visibility(probs, screen_ys):
    vals = [probs.get(y, 0) for y in sorted(screen_ys)]
    peaks = [vals[i] for i in range(1, len(vals)-1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def centroid(probs, screen_ys):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(y*p for y, p in probs.items()) / total


def main():
    width = 50
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height+1))
    barrier_x = 20
    det_x = 40

    barrier = set((barrier_x, y) for y in range(-height, height+1))
    slits = set()
    for sy in [-4, 4]:
        for y in range(sy-1, sy+2):
            slits.add((barrier_x, y))
    blocked = barrier - slits

    post = RulePostulates(phase_per_action=2.0, attenuation_power=1.0,
                          attenuation_mode="geometry")
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
    field = derive_node_field(nodes, rule)
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)

    # Mass
    mass_mn = frozenset((25, y) for y in range(4, 9))
    mass_rule = derive_local_rule(persistent_nodes=mass_mn, postulates=post)
    mass_field = derive_node_field(nodes, mass_rule)
    mass_arrival = infer_arrival_times_from_source(nodes, source, mass_rule)
    mass_dag = build_causal_dag(nodes, mass_arrival)

    N = 50  # realizations

    print("=" * 70)
    print("ENSEMBLE-AVERAGED PHASE NOISE DECOHERENCE")
    print(f"  {N} realizations, corrected propagator, k=2.0")
    print("=" * 70)
    print()

    # ================================================================
    # TEST 1: Ensemble-averaged V vs η
    # ================================================================
    print("TEST 1: Ensemble-averaged V (average P first, then V)")
    print()
    print(f"  {'eta':>6s}  {'V_ensemble':>10s}  {'V_mean_ind':>10s}  {'grav_shift':>10s}")
    print(f"  {'-' * 40}")

    for eta in [0.0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
        # Ensemble average for interference
        avg_probs = {y: 0.0 for y in screen_ys}
        ind_vs = []
        for i in range(N):
            rng = random.Random(i*31+7)
            probs = propagate_noisy(nodes, source, field, rule, dag, arrival,
                                    blocked, screen_ys, det_x, eta, rng)
            for y in screen_ys:
                avg_probs[y] += probs.get(y, 0)
            ind_vs.append(visibility(probs, screen_ys))

        # Normalize ensemble average
        total = sum(avg_probs.values())
        if total > 0:
            avg_probs = {y: p/total for y, p in avg_probs.items()}

        v_ens = visibility(avg_probs, screen_ys)
        v_ind = sum(ind_vs)/len(ind_vs)

        # Gravity: ensemble-averaged centroid shift
        avg_free = {y: 0.0 for y in screen_ys}
        avg_mass = {y: 0.0 for y in screen_ys}
        for i in range(N):
            rng_f = random.Random(i*31+7)
            rng_m = random.Random(i*31+7)
            fp = propagate_noisy(nodes, source, field, rule, dag, arrival,
                                 set(), screen_ys, det_x, eta, rng_f)
            mp = propagate_noisy(nodes, source, mass_field, mass_rule,
                                 mass_dag, mass_arrival,
                                 set(), screen_ys, det_x, eta, rng_m)
            for y in screen_ys:
                avg_free[y] += fp.get(y, 0)
                avg_mass[y] += mp.get(y, 0)

        tf = sum(avg_free.values())
        tm = sum(avg_mass.values())
        if tf > 0:
            avg_free = {y: p/tf for y, p in avg_free.items()}
        if tm > 0:
            avg_mass = {y: p/tm for y, p in avg_mass.items()}

        shift = centroid(avg_mass, screen_ys) - centroid(avg_free, screen_ys)

        print(f"  {eta:6.2f}  {v_ens:10.4f}  {v_ind:10.4f}  {shift:+10.3f}")

    print()
    print("KEY:")
    print("  V_ensemble = V of the averaged distribution (decoherence measure)")
    print("  V_mean_ind = mean V across individual realizations")
    print("  grav_shift = centroid shift of ensemble-averaged distribution")
    print()
    print("SUCCESS = V_ensemble drops with η while grav_shift remains positive")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
