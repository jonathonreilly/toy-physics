#!/usr/bin/env python3
"""Sorkin inclusion-exclusion test for genuine multi-path interference.

In standard quantum mechanics, the Born rule guarantees that all
interference is pairwise: the three-slit pattern equals the sum of
all two-slit-pair patterns minus the single-slit patterns. The
Sorkin parameter I_3 measures the deviation:

  I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C

If I_3 = 0: all interference is pairwise (Born rule holds)
If I_3 != 0: genuine third-order interference exists

This tests whether the model's path-sum respects the Born rule's
pairwise structure or produces higher-order interference.

PStack experiment: sorkin-inclusion-exclusion
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


def slit_distribution(
    screen_positions: list[int],
    width: int, height: int,
    open_slits: set[int],
    source: tuple[int, int] = (1, 0),
    normalize: bool = False,
) -> dict[int, float]:
    """Coherent distribution with specified open slits. No records."""
    barrier_x = width // 2
    rule = derive_local_rule(
        persistent_nodes=frozenset(),
        postulates=RulePostulates(phase_per_action=4.0, attenuation_power=1.0),
    )
    detector_x = width
    blocked_nodes = frozenset(
        (barrier_x, y) for y in range(-height, height + 1) if y not in open_slits
    )
    nodes = build_rectangular_nodes(width=width, height=height, blocked_nodes=blocked_nodes)
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
                states[(neighbor, (neighbor[0]-node[0], neighbor[1]-node[1]))] += amp * link_amp

    distribution = {y: abs(boundary_amps.get(y, 0.0)) ** 2 for y in screen_positions}

    if normalize:
        norm = sum(distribution.values())
        if norm > 0:
            distribution = {y: p / norm for y, p in distribution.items()}
    return distribution


def main() -> None:
    width = 20
    height = 10
    screen_ys = list(range(-height, height + 1))

    # Three slits: A, B, C
    slit_configs = [
        ("SYMMETRIC (y=-4, 0, +4)", -4, 0, 4),
        ("CLOSE (y=-2, 0, +2)", -2, 0, 2),
        ("WIDE (y=-6, 0, +6)", -6, 0, 6),
        ("ASYMMETRIC (y=-4, +1, +6)", -4, 1, 6),
    ]

    print("=" * 72)
    print("SORKIN INCLUSION-EXCLUSION TEST")
    print("=" * 72)
    print(f"width={width}, height={height}")
    print()
    print("I_3(y) = P_ABC(y) - P_AB(y) - P_AC(y) - P_BC(y) + P_A(y) + P_B(y) + P_C(y)")
    print("If I_3 = 0 everywhere: Born rule (pairwise interference only)")
    print("If I_3 != 0: genuine third-order interference")
    print()

    for label, ya, yb, yc in slit_configs:
        print(f"\n{'=' * 60}")
        print(f"CONFIG: {label}")
        print(f"  Slits A={ya}, B={yb}, C={yc}")
        print(f"{'=' * 60}")

        # Compute all 7 required distributions (unnormalized!)
        P_ABC = slit_distribution(screen_ys, width, height, {ya, yb, yc})
        P_AB = slit_distribution(screen_ys, width, height, {ya, yb})
        P_AC = slit_distribution(screen_ys, width, height, {ya, yc})
        P_BC = slit_distribution(screen_ys, width, height, {yb, yc})
        P_A = slit_distribution(screen_ys, width, height, {ya})
        P_B = slit_distribution(screen_ys, width, height, {yb})
        P_C = slit_distribution(screen_ys, width, height, {yc})

        # Compute I_3 at each screen position
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

        print(f"  {'y':>4s}  {'P_ABC':>14s}  {'I_3':>14s}  {'I_3/P_ABC':>12s}  bar")
        print(f"  {'-'*62}")

        for y in screen_ys:
            p = P_ABC[y]
            i3 = i3_values[y]
            ratio = i3 / p if p > 1e-30 else 0.0
            bar_len = int(abs(i3) / max(max_i3, 1e-30) * 30)
            bar = ("+" if i3 > 0 else "-") * bar_len if bar_len > 0 else ""
            marker = " <-- slit" if y in {ya, yb, yc} else ""
            print(f"  {y:+4d}  {p:14.6e}  {i3:14.6e}  {ratio:12.6e}  {bar}{marker}")

        # Summary
        print(f"\n  VERDICT: ", end="")
        if max_i3 / max_prob < 1e-10:
            print("I_3 = 0 to machine precision. BORN RULE HOLDS (pairwise only).")
        elif max_i3 / max_prob < 1e-3:
            print(f"I_3 is nonzero but tiny ({max_i3/max_prob:.2e} of P). Near-pairwise.")
        else:
            print(f"I_3 is SIGNIFICANT ({max_i3/max_prob:.2e} of P). HIGHER-ORDER INTERFERENCE.")

    print("\n\nTEST COMPLETE")


if __name__ == "__main__":
    main()
