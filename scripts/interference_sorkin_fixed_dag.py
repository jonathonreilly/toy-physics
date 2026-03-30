#!/usr/bin/env python3
"""Fixed-DAG Sorkin test: isolate genuine higher-order interference
from DAG reconfiguration artifacts.

Instead of blocking barrier nodes (which changes the causal DAG),
this version keeps ALL barrier nodes present but multiplies the
amplitude by 0 at non-slit positions. The DAG is identical for
all slit configurations — only the amplitude mask changes.

If I_3 = 0 here: the original I_3 != 0 was pure DAG reconfiguration.
If I_3 != 0 here: the model has genuine higher-order interference
beyond the Born rule's pairwise structure.

PStack experiment: sorkin-fixed-dag
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


def fixed_dag_slit_distribution(
    screen_positions: list[int],
    width: int, height: int,
    all_slit_ys: set[int],
    open_slits: set[int],
    source: tuple[int, int] = (1, 0),
) -> dict[int, float]:
    """Path-sum with fixed DAG. All barrier positions are open in the network,
    but amplitude is zeroed when crossing the barrier at a non-open slit."""
    barrier_x = width // 2
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
    detector_x = width
    # NO blocked nodes — all barrier positions are present
    nodes = build_rectangular_nodes(width=width, height=height)
    node_field = derive_node_field(nodes, rule)
    arrival_times = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival_times)
    order = sorted(arrival_times, key=arrival_times.get)

    states: DefaultDict[tuple[tuple[int, int], tuple[int, int]], complex] = defaultdict(complex)
    states[(source, (1, 0))] = 1.0 + 0.0j
    boundary_amps: DefaultDict[int, complex] = defaultdict(complex)

    for node in order:
        matching = [(s, a) for s, a in list(states.items()) if s[0] == node]
        if not matching:
            continue
        if node[0] == detector_x:
            for state, amp in matching:
                boundary_amps[node[1]] += amp
                del states[state]
            continue
        for (cur, heading), amp in matching:
            del states[(cur, heading)]
            for neighbor in dag.get(node, []):
                _, _, link_amp = local_edge_properties(node, neighbor, rule, node_field)

                # AMPLITUDE MASK: zero out barrier crossings at non-open slits
                if node[0] < barrier_x <= neighbor[0]:
                    # This is a barrier crossing
                    if neighbor[1] not in open_slits:
                        link_amp = 0.0  # Block amplitude, not topology

                states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]))] += amp * link_amp

    return {y: abs(boundary_amps.get(y, 0.0)) ** 2 for y in screen_positions}


def main() -> None:
    width = 20
    height = 10
    screen_ys = list(range(-height, height + 1))

    configs = [
        ("SYMMETRIC (-4, 0, +4)", -4, 0, 4),
        ("CLOSE (-2, 0, +2)", -2, 0, 2),
        ("WIDE (-6, 0, +6)", -6, 0, 6),
        ("ASYMMETRIC (-4, +1, +6)", -4, 1, 6),
    ]

    print("=" * 72)
    print("FIXED-DAG SORKIN TEST")
    print("=" * 72)
    print(f"width={width}, height={height}")
    print("DAG is FIXED — same network for all slit configs.")
    print("Only amplitude transmission varies (0 at closed slits).")
    print()

    for label, ya, yb, yc in configs:
        all_slits = {ya, yb, yc}

        print(f"\n{'=' * 60}")
        print(f"CONFIG: {label}")
        print(f"  Slits A={ya}, B={yb}, C={yc}")
        print(f"{'=' * 60}")

        P_ABC = fixed_dag_slit_distribution(screen_ys, width, height, all_slits, {ya, yb, yc})
        P_AB  = fixed_dag_slit_distribution(screen_ys, width, height, all_slits, {ya, yb})
        P_AC  = fixed_dag_slit_distribution(screen_ys, width, height, all_slits, {ya, yc})
        P_BC  = fixed_dag_slit_distribution(screen_ys, width, height, all_slits, {yb, yc})
        P_A   = fixed_dag_slit_distribution(screen_ys, width, height, all_slits, {ya})
        P_B   = fixed_dag_slit_distribution(screen_ys, width, height, all_slits, {yb})
        P_C   = fixed_dag_slit_distribution(screen_ys, width, height, all_slits, {yc})

        i3_values = {}
        for y in screen_ys:
            i3 = (P_ABC[y] - P_AB[y] - P_AC[y] - P_BC[y]
                  + P_A[y] + P_B[y] + P_C[y])
            i3_values[y] = i3

        max_prob = max(max(P_ABC.values()), 1e-30)
        max_i3 = max(abs(v) for v in i3_values.values())

        print(f"\n  max |P_ABC|  = {max(P_ABC.values()):.6e}")
        print(f"  max |I_3|    = {max_i3:.6e}")
        print(f"  max |I_3| / max |P_ABC| = {max_i3 / max_prob:.6e}")
        print()

        print(f"  {'y':>4s}  {'P_ABC':>14s}  {'I_3':>14s}  {'I_3/P_ABC':>12s}")
        print(f"  {'-'*50}")

        for y in screen_ys:
            p = P_ABC[y]
            i3 = i3_values[y]
            ratio = i3 / p if p > 1e-30 else 0.0
            marker = " <-- slit" if y in {ya, yb, yc} else ""
            print(f"  {y:+4d}  {p:14.6e}  {i3:14.6e}  {ratio:12.6e}{marker}")

        print(f"\n  VERDICT: ", end="")
        if max_i3 / max_prob < 1e-10:
            print("I_3 = 0 to machine precision. BORN RULE HOLDS.")
        elif max_i3 / max_prob < 1e-3:
            print(f"I_3 nonzero but tiny ({max_i3/max_prob:.2e}). Near-pairwise.")
        else:
            print(f"I_3 SIGNIFICANT ({max_i3/max_prob:.2e}). HIGHER-ORDER INTERFERENCE.")

    # COMPARISON: original (topology-change) vs fixed-DAG
    print()
    print("=" * 72)
    print("COMPARISON: ORIGINAL vs FIXED-DAG Sorkin parameter")
    print("=" * 72)
    print()
    print("Original test (DAG changes with slit config):")
    print("  Symmetric: max|I_3|/|P| = 1.67e+06")
    print("  Close:     max|I_3|/|P| = 9.19e+01")
    print("  Wide:      max|I_3|/|P| = 4.61e+09")
    print("  Asymmetric:max|I_3|/|P| = 4.21e+09")
    print()
    print("If fixed-DAG I_3 ≈ 0: original I_3 was pure DAG reconfiguration.")
    print("If fixed-DAG I_3 >> 0: model has genuine higher-order interference.")

    print("\n\nTEST COMPLETE")


if __name__ == "__main__":
    main()
