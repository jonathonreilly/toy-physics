#!/usr/bin/env python3
"""Two-register decoherence on rectangular lattice.

All two-register tests were on generated DAGs. Does it work on the
regular lattice? The lattice has perfect 8-fold symmetry, which might
prevent slit-selective env coupling.

Uses corrected propagator (1/L^p via attenuation_mode="geometry")
through the core simulator.

PStack experiment: two-register-lattice
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


def propagate_two_register_grid(
    nodes, source, field, rule, dag, arrival,
    blocked, mass_set, screen_ys, det_x, env_mode="fine",
):
    """Two-register propagation on rectangular grid."""
    order = sorted(arrival, key=arrival.get)

    # State: (node, env_label) → amplitude
    state = {(source, -1): 1.0 + 0.0j}

    processed = set()
    for node in order:
        if node in processed:
            continue
        processed.add(node)

        entries = {env: amp for (n, env), amp in list(state.items())
                   if n == node and abs(amp) > 1e-30}
        if not entries or node in blocked:
            continue

        for env, amp in entries.items():
            if node in mass_set:
                if env_mode == "fine":
                    new_env = hash(node)  # unique per node
                elif env_mode == "binary":
                    new_env = 1
                elif env_mode == "ybin":
                    new_env = 1 if node[1] > 0 else -1
                else:
                    new_env = env
            else:
                new_env = env

            for nb in dag.get(node, []):
                if nb in blocked:
                    continue
                _, _, link_amp = local_edge_properties(node, nb, rule, field)
                key = (nb, new_env)
                if key not in state:
                    state[key] = 0.0 + 0.0j
                state[key] += amp * link_amp

    # Partial trace at detector
    probs = defaultdict(float)
    for (node, env), amp in state.items():
        if node[0] == det_x:
            probs[node[1]] += abs(amp) ** 2

    total = sum(probs.values())
    if total > 0:
        probs = {y: p / total for y, p in probs.items()}
    return probs


def propagate_coherent_grid(nodes, source, field, rule, dag, arrival,
                            blocked, screen_ys, det_x):
    """Standard coherent propagation on grid."""
    order = sorted(arrival, key=arrival.get)
    amps = {source: 1.0 + 0.0j}

    for node in order:
        if node not in amps or node in blocked:
            continue
        a = amps[node]
        for nb in dag.get(node, []):
            if nb in blocked:
                continue
            _, _, link_amp = local_edge_properties(node, nb, rule, field)
            if nb not in amps:
                amps[nb] = 0.0 + 0.0j
            amps[nb] += a * link_amp

    probs = {}
    total = 0
    for y in screen_ys:
        p = abs(amps.get((det_x, y), 0.0)) ** 2
        probs[y] = p
        total += p
    if total > 0:
        probs = {y: p / total for y, p in probs.items()}
    return probs


def visibility(probs):
    ys = sorted(probs.keys())
    vals = [probs[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals) - 1)
             if vals[i] > vals[i - 1] and vals[i] > vals[i + 1]]
    troughs = [vals[i] for i in range(1, len(vals) - 1)
               if vals[i] < vals[i - 1] and vals[i] < vals[i + 1]]
    if peaks and troughs:
        return (max(peaks) - min(troughs)) / (max(peaks) + min(troughs))
    return 0.0


def main():
    width = 50
    height = 15
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height + 1))
    det_x = 40
    barrier_x = 20
    slit_ys = [-4, 4]

    barrier = set((barrier_x, y) for y in range(-height, height + 1))
    slit_nodes = set()
    for sy in slit_ys:
        for y in range(sy - 1, sy + 2):
            slit_nodes.add((barrier_x, y))
    blocked = barrier - slit_nodes

    # k sweep to find the right regime
    for k_test in [1.0, 2.0, 3.0, 4.0, 6.0]:
        post_test = RulePostulates(phase_per_action=k_test, attenuation_power=1.0,
                                    attenuation_mode="geometry")
        rule_test = derive_local_rule(persistent_nodes=frozenset(), postulates=post_test)
        field_test = derive_node_field(nodes, rule_test)
        arr_test = infer_arrival_times_from_source(nodes, source, rule_test)
        dag_test = build_causal_dag(nodes, arr_test)
        p = propagate_coherent_grid(nodes, source, field_test, rule_test, dag_test,
                                     arr_test, blocked, screen_ys, det_x)
        v = visibility(p)
        print(f"  k={k_test}: V_free={v:.4f}")
    print()

    postulates = RulePostulates(
        phase_per_action=2.0, attenuation_power=1.0,
        attenuation_mode="geometry",
    )

    # Mass: post-barrier, between slits
    mass_nodes = frozenset((barrier_x + 1, y) for y in range(-2, 3))
    mass_set = set(mass_nodes)

    rule = derive_local_rule(persistent_nodes=mass_nodes, postulates=postulates)
    mass_field = derive_node_field(nodes, rule)
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    free_field = derive_node_field(nodes, free_rule)

    arrival = infer_arrival_times_from_source(nodes, source, free_rule)
    dag = build_causal_dag(nodes, arrival)

    print("=" * 70)
    print("TWO-REGISTER DECOHERENCE ON RECTANGULAR LATTICE")
    print(f"  Grid: {width}x{2*height+1}, barrier at x={barrier_x}, det at x={det_x}")
    print(f"  Mass at x={barrier_x+1}, y=-2..2 (between slits)")
    print(f"  Corrected propagator (1/L^p)")
    print("=" * 70)
    print()

    for env_mode in ["fine", "binary", "ybin"]:
        # Coherent baseline (mass present, no env register)
        p_coh = propagate_coherent_grid(
            nodes, source, mass_field, rule, dag, arrival,
            blocked, screen_ys, det_x)
        v_coh = visibility(p_coh)

        # Two-register
        p_2reg = propagate_two_register_grid(
            nodes, source, mass_field, rule, dag, arrival,
            blocked, mass_set, screen_ys, det_x, env_mode)
        v_2reg = visibility(p_2reg)

        v_drop = v_coh - v_2reg

        print(f"  env_mode='{env_mode}': V_coh={v_coh:.4f}, V_2reg={v_2reg:.4f}, "
              f"V_drop={v_drop:+.4f}")

    # Gravity check
    print()
    p_free = propagate_coherent_grid(
        nodes, source, free_field, free_rule, dag, arrival,
        set(), screen_ys, det_x)
    p_mass = propagate_two_register_grid(
        nodes, source, mass_field, rule, dag, arrival,
        set(), mass_set, screen_ys, det_x, "fine")

    fcy = sum(y * p for y, p in p_free.items())
    mcy = sum(y * p for y, p in p_mass.items())
    print(f"  Gravity: free_cy={fcy:.2f}, mass_cy={mcy:.2f}, shift={mcy-fcy:+.2f}")

    # Sweep mass positions
    print()
    print("SWEEP: mass x-offset from barrier")
    print(f"  {'x_off':>5s}  {'V_coh':>7s}  {'V_fine':>7s}  {'V_drop':>7s}")
    print(f"  {'-' * 30}")

    for x_off in [1, 2, 3, 4, 5, 8, 10]:
        mn = frozenset((barrier_x + x_off, y) for y in range(-2, 3))
        ms = set(mn)
        mr = derive_local_rule(persistent_nodes=mn, postulates=postulates)
        mf = derive_node_field(nodes, mr)

        pc = propagate_coherent_grid(
            nodes, source, mf, mr, dag, arrival,
            blocked, screen_ys, det_x)
        p2 = propagate_two_register_grid(
            nodes, source, mf, mr, dag, arrival,
            blocked, ms, screen_ys, det_x, "fine")

        vc = visibility(pc)
        v2 = visibility(p2)
        vd = vc - v2
        print(f"  {x_off:5d}  {vc:7.4f}  {v2:7.4f}  {vd:+7.4f}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
