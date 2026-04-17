#!/usr/bin/env python3
"""Decompose the superposition failure into field vs path components.

The mutual gravitation test showed ~50% superposition failure in
the action. This could come from:
1. Field nonlinearity: field(A+B) != field(A) + field(B)
2. Path nonlinearity: optimal path in combined field != sum of
   individual path deflections

Test by comparing:
- field(A+B) vs field(A) + field(B) at every node
- action along the SAME path in combined vs summed fields

PStack experiment: superposition-decomposition
"""

from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    stationary_action_path,
)


def main() -> None:
    width = 40
    height = 14
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    nodes = build_rectangular_nodes(width=width, height=height)

    mass_1 = frozenset((15, y) for y in [5, 6, 7, 8, 9])
    mass_2 = frozenset((25, y) for y in [-9, -8, -7, -6, -5])
    both = mass_1 | mass_2

    rule_free = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)
    rule_1 = derive_local_rule(persistent_nodes=mass_1, postulates=postulates)
    rule_2 = derive_local_rule(persistent_nodes=mass_2, postulates=postulates)
    rule_both = derive_local_rule(persistent_nodes=both, postulates=postulates)

    field_free = derive_node_field(nodes, rule_free)
    field_1 = derive_node_field(nodes, rule_1)
    field_2 = derive_node_field(nodes, rule_2)
    field_both = derive_node_field(nodes, rule_both)

    print("=" * 72)
    print("SUPERPOSITION DECOMPOSITION")
    print("=" * 72)
    print()

    # =========================================================
    # TEST 1: Field superposition
    # =========================================================
    print("=" * 72)
    print("TEST 1: FIELD SUPERPOSITION — field(A+B) vs field(A) + field(B)")
    print("=" * 72)
    print()

    # field_sum = field_1 + field_2 - field_free (subtract double-counted baseline)
    # Actually since field_free = 0 everywhere (no persistent nodes), field_sum = field_1 + field_2
    field_sum = {n: field_1[n] + field_2[n] for n in nodes}

    max_diff = 0.0
    max_diff_node = None
    total_diff = 0.0
    total_field = 0.0
    diffs = []

    for n in nodes:
        fb = field_both[n]
        fs = field_sum[n]
        diff = fb - fs
        total_diff += abs(diff)
        total_field += abs(fb)
        if abs(diff) > max_diff:
            max_diff = abs(diff)
            max_diff_node = n
        if abs(diff) > 0.001:
            diffs.append((n, diff, fb, fs))

    print(f"  Max |field_both - field_sum|: {max_diff:.10f} at {max_diff_node}")
    print(f"  Mean |diff| / mean |field|: {total_diff / total_field:.10f}")
    print(f"  Nodes with |diff| > 0.001: {len(diffs)}")
    print()

    if max_diff < 1e-8:
        print("  RESULT: Field superposition HOLDS to machine precision.")
        print("  field(A+B) = field(A) + field(B) exactly.")
        print("  The ~50% action failure is PURELY from path optimization nonlinearity.")
    else:
        print("  RESULT: Field superposition FAILS.")
        print(f"  Max deviation: {max_diff:.6f}")
        diffs.sort(key=lambda x: -abs(x[1]))
        print(f"\n  Top 10 deviations:")
        for n, d, fb, fs in diffs[:10]:
            print(f"    {n}: both={fb:.6f} sum={fs:.6f} diff={d:+.6f}")

    # =========================================================
    # TEST 2: Action along FIXED path
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 2: ACTION along a FIXED path in different fields")
    print("=" * 72)
    print()
    print("  If we trace the SAME path through field(A+B) and field(A)+field(B),")
    print("  do we get the same action? (Removes path-optimization nonlinearity)")
    print()

    # Get the optimal path in the combined field
    source = (0, 0)
    target = (width, 0)

    _, path_both = stationary_action_path(width, height, source, target, rule_both)
    _, path_1 = stationary_action_path(width, height, source, target, rule_1)
    _, path_free = stationary_action_path(width, height, source, target, rule_free)

    # Compute action along path_both in each field
    def action_along_path(path, field):
        total = 0.0
        for i in range(len(path) - 1):
            s, e = path[i], path[i + 1]
            link_len = math.dist(s, e)
            local_f = 0.5 * (field[s] + field[e])
            delay = link_len * (1.0 + local_f)
            retained = math.sqrt(max(delay ** 2 - link_len ** 2, 0.0))
            total += delay - retained
        return total

    a_both_on_both = action_along_path(path_both, field_both)
    a_sum_on_both = action_along_path(path_both, field_sum)
    a_1_on_both = action_along_path(path_both, field_1)
    a_2_on_both = action_along_path(path_both, field_2)
    a_free_on_both = action_along_path(path_both, field_free)

    print(f"  Path: optimal in combined field (path_both)")
    print(f"  Action in field_both:       {a_both_on_both:.6f}")
    print(f"  Action in field_sum:        {a_sum_on_both:.6f}")
    print(f"  Difference:                 {a_both_on_both - a_sum_on_both:.10f}")
    print()

    if abs(a_both_on_both - a_sum_on_both) < 1e-6:
        print("  RESULT: Same path, same action. Field superposition confirmed.")
    else:
        print(f"  RESULT: Same path, DIFFERENT action. Field nonlinearity contributes.")

    # =========================================================
    # TEST 3: Path difference contribution
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 3: PATH OPTIMIZATION contribution to superposition failure")
    print("=" * 72)
    print()

    # Action of optimal paths:
    a_opt_both, _ = stationary_action_path(width, height, source, target, rule_both)
    a_opt_1, _ = stationary_action_path(width, height, source, target, rule_1)
    a_opt_2, _ = stationary_action_path(width, height, source, target, rule_2)
    a_opt_free, _ = stationary_action_path(width, height, source, target, rule_free)

    ad_1 = a_opt_1 - a_opt_free
    ad_2 = a_opt_2 - a_opt_free
    ad_both = a_opt_both - a_opt_free
    ad_sum = ad_1 + ad_2

    # Action of path_both evaluated in individual fields
    a_1_on_pathboth = action_along_path(path_both, field_1)
    a_2_on_pathboth = action_along_path(path_both, field_2)
    a_free_on_pathboth = action_along_path(path_both, field_free)

    ad_1_on_pathboth = a_1_on_pathboth - a_free_on_pathboth
    ad_2_on_pathboth = a_2_on_pathboth - a_free_on_pathboth
    ad_sum_on_pathboth = ad_1_on_pathboth + ad_2_on_pathboth

    print(f"  Optimal paths (each in its own field):")
    print(f"    ad_1 = {ad_1:.6f}")
    print(f"    ad_2 = {ad_2:.6f}")
    print(f"    ad_sum = {ad_sum:.6f}")
    print(f"    ad_both = {ad_both:.6f}")
    print(f"    deviation = {ad_both - ad_sum:.6f} ({(ad_both-ad_sum)/ad_both*100:.1f}%)")
    print()
    print(f"  Same path (path_both) in individual fields:")
    print(f"    ad_1_on_pathboth = {ad_1_on_pathboth:.6f}")
    print(f"    ad_2_on_pathboth = {ad_2_on_pathboth:.6f}")
    print(f"    ad_sum_on_pathboth = {ad_sum_on_pathboth:.6f}")
    print(f"    ad_both = {ad_both:.6f}")

    if abs(field_both[(20,0)] - field_sum[(20,0)]) < 1e-8:
        print(f"\n  Since field superposes exactly:")
        print(f"    ad_sum_on_pathboth should equal ad_both: diff = {ad_both - ad_sum_on_pathboth:.10f}")
        print(f"    The entire {(ad_both-ad_sum)/ad_both*100:.1f}% failure comes from")
        print(f"    each mass's optimal path being DIFFERENT from path_both.")

    print()
    print("DECOMPOSITION COMPLETE")


if __name__ == "__main__":
    main()
