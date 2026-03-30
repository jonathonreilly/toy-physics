#!/usr/bin/env python3
"""Audit per-slit amplitude contributions in the exact-zero visibility regime.

Tests whether V=0 is caused by single-slit reachability (topological)
or by perfect cancellation of two-slit amplitudes (interference).
PStack experiment: slit-reachability
"""

from __future__ import annotations
import math, cmath, sys, os
from collections import defaultdict
from typing import DefaultDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toy_event_physics import (
    RulePostulates, build_causal_dag, build_rectangular_nodes,
    derive_local_rule, derive_node_field, infer_arrival_times_from_source,
    local_edge_properties,
)


def per_slit_amplitudes(
    screen_y: int, width: int, height: int,
    slit_ys: set[int], phase_shift_upper: float = 0.0,
) -> dict[str, complex]:
    """Return amplitude at screen_y decomposed by which slit the path used."""
    barrier_x = width // 2
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
    source = (1, 0)
    detector_x = width
    blocked_nodes = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in slit_ys
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked_nodes)
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    # Track which slit each path went through
    # state: (node, heading, slit_used) -> amplitude
    states: DefaultDict[tuple[tuple[int, int], tuple[int, int], str], complex] = defaultdict(complex)
    states[(source, (1, 0), "none")] = 1.0 + 0.0j

    # Collect at detector
    arrivals: DefaultDict[str, complex] = defaultdict(complex)

    for node in order:
        matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
        if not matching:
            continue
        if node[0] == detector_x:
            for state, amp in matching:
                if node[1] == screen_y:
                    arrivals[state[2]] += amp
                del states[state]
            continue
        for (cur, heading, slit_used), amp in matching:
            del states[(cur, heading, slit_used)]
            for neighbor in dag.get(node, []):
                dx, dy = neighbor[0] - node[0], neighbor[1] - node[1]
                _, _, link_amp = local_edge_properties(node, neighbor, rule, node_field)
                new_slit = slit_used
                if node[0] < barrier_x <= neighbor[0] and neighbor[1] in slit_ys:
                    new_slit = f"slit_y={neighbor[1]}"
                    if neighbor[1] > 0:
                        link_amp *= cmath.exp(1j * phase_shift_upper)
                states[(neighbor, (dx, dy), new_slit)] += amp * link_amp

    return dict(arrivals)


def main() -> None:
    height = 10

    # Test cases: geometries known to produce V=0 at various y
    test_cases = [
        # (width, slit_half, y) — from the off-center sweep, these had V=0
        (8, 4, 1),   # width=8, slit_sep=8, y=1: V=0
        (8, 4, 3),   # width=8, slit_sep=8, y=3: V=0
        (8, 4, 5),   # width=8, slit_sep=8, y=5: V=0
        (12, 4, 3),  # width=12, slit_sep=8, y=3: V=0
        (16, 4, 5),  # width=16, slit_sep=8, y=5: V=0
        (8, 6, 1),   # width=8, slit_sep=12, y=1: V=0
        # And cases known to have V > 0 for comparison
        (12, 4, 1),  # width=12, slit_sep=8, y=1: V=0.927
        (16, 4, 1),  # width=16, slit_sep=8, y=1: V=0.963
        (16, 4, 3),  # width=16, slit_sep=8, y=3: V=0.157
        (24, 4, 5),  # width=24, slit_sep=8, y=5: V=0.052
    ]

    print("=" * 72)
    print("SLIT REACHABILITY AUDIT")
    print("=" * 72)
    print()
    print("For each (width, slit_sep, screen_y), decompose amplitude by slit.")
    print("If V=0 is caused by single-slit reachability, only one slit contributes.")
    print("If V=0 is caused by cancellation, both slits contribute but cancel.")
    print()

    for w, sh, y in test_cases:
        slit_ys = {-sh, sh}
        amps = per_slit_amplitudes(y, w, height, slit_ys, phase_shift_upper=0.0)

        print(f"--- width={w}, slit_sep={sh*2}, screen_y={y} ---")
        total = complex(0)
        for slit_label, amp in sorted(amps.items()):
            mag = abs(amp)
            phase_deg = math.degrees(cmath.phase(amp)) if mag > 0 else 0
            print(f"  {slit_label:>15s}: |A| = {mag:.10e}  phase = {phase_deg:+8.2f} deg")
            total += amp

        print(f"  {'TOTAL':>15s}: |A| = {abs(total):.10e}")

        # Classify
        contributing_slits = [k for k, v in amps.items() if abs(v) > 1e-30 and k != "none"]
        if len(contributing_slits) == 0:
            print(f"  DIAGNOSIS: NO paths reach this position")
        elif len(contributing_slits) == 1:
            print(f"  DIAGNOSIS: SINGLE-SLIT REACHABILITY (only {contributing_slits[0]})")
        else:
            print(f"  DIAGNOSIS: BOTH slits contribute ({len(contributing_slits)} paths)")
        print()

    print("AUDIT COMPLETE")


if __name__ == "__main__":
    main()
