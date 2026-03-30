#!/usr/bin/env python3
"""Test gravity with oscillating persistent patterns.

The self-maintenance sweep showed the default rule produces period-3
oscillators (sizes 5↔8↔9). This means the delay field pulsates.

Questions:
1. Does path bending persist with a pulsating source?
2. Does the bending magnitude oscillate with the source?
3. Is there a time-averaged effective field that governs path selection?
4. Does the oscillation produce any WAVE-LIKE propagation signature?

PStack experiment: pulsating-gravity
"""

from __future__ import annotations
import ast
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    build_graph_neighbor_lookup,
    derive_local_rule,
    derive_node_field,
    evolve_self_maintaining_pattern,
    compare_geodesics,
)


def main() -> None:
    width = 30
    height = 12
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    source = (0, 0)
    target_ys = [-3, 0, 3, 6]

    nodes = build_rectangular_nodes(width=width, height=height)
    lookup = build_graph_neighbor_lookup(nodes)
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)

    print("=" * 72)
    print("PULSATING GRAVITY: Oscillating Persistent Patterns")
    print("=" * 72)
    print(f"width={width}, height={height}")
    print()

    # =========================================================
    # 1. Evolve a persistent pattern and measure gravity at each phase
    # =========================================================
    # Seed: 3x3 block centered at (15, 5) — this oscillates with period 3
    seed = frozenset((15 + dx, 5 + dy) for dx in range(-1, 2) for dy in range(-1, 2))

    print("Evolving seed (3x3 block at (15,5)) under default rule S={3,4} B={3,4}:")
    history = evolve_self_maintaining_pattern(
        nodes, seed,
        survive_counts=frozenset({3, 4}),
        birth_counts=frozenset({3, 4}),
        steps=12,
        neighbor_lookup=lookup,
    )

    for step, state in enumerate(history):
        print(f"  Step {step:2d}: {len(state)} nodes  {sorted(state)[:8]}{'...' if len(state) > 8 else ''}")

    print()

    # =========================================================
    # 2. Measure geodesic bending at each oscillation phase
    # =========================================================
    print("=" * 72)
    print("GEODESIC BENDING vs OSCILLATION PHASE")
    print("=" * 72)
    print()

    # Use one full period (steps 6-8 for a period-3 oscillator)
    phase_states = history[6:9]  # One full period after transients settle

    print(f"{'phase':>6s}  {'n_nodes':>8s}  {'target_y':>8s}  {'action_diff':>12s}  "
          f"{'max_defl':>10s}  dist_path")
    print("-" * 80)

    for phase_idx, pnodes in enumerate(phase_states):
        distorted_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
        comps = compare_geodesics(
            width=width, height=height, source=source,
            target_ys=target_ys, free_rule=free_rule, distorted_rule=distorted_rule,
        )
        for comp in comps:
            free_ys = ast.literal_eval(comp.free_path_y)
            dist_ys = ast.literal_eval(comp.distorted_path_y)
            max_d = max(abs(d - f) for f, d in zip(free_ys, dist_ys))
            ad = comp.distorted_action - comp.free_action
            print(f"{phase_idx:6d}  {len(pnodes):8d}  {comp.target_y:8d}  {ad:12.4f}  "
                  f"{max_d:10.4f}  {comp.distorted_path_y[:60]}")

    # =========================================================
    # 3. Compare: static 5-node cluster vs oscillating pattern
    # =========================================================
    print()
    print("=" * 72)
    print("COMPARISON: STATIC vs OSCILLATING source")
    print("=" * 72)
    print()

    static_nodes = frozenset((15, y) for y in [3, 4, 5, 6, 7])
    static_rule = derive_local_rule(persistent_nodes=static_nodes, postulates=postulates)

    # Time-averaged field from oscillating pattern
    fields = []
    for pnodes in phase_states:
        rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)
        field = derive_node_field(nodes, rule)
        fields.append(field)

    avg_field = {n: sum(f[n] for f in fields) / len(fields) for n in nodes}
    static_field = derive_node_field(nodes, static_rule)

    # Compare fields at key positions
    print(f"{'position':>12s}  {'static_field':>12s}  {'avg_osc_field':>14s}  {'ratio':>8s}")
    print("-" * 52)
    for x in range(10, 21, 2):
        for y in [0, 3, 5]:
            sf = static_field.get((x, y), 0)
            af = avg_field.get((x, y), 0)
            ratio = af / sf if sf > 0 else 0
            print(f"  ({x:2d},{y:2d})  {sf:12.6f}  {af:14.6f}  {ratio:8.4f}")

    # =========================================================
    # 4. Field pulsation amplitude
    # =========================================================
    print()
    print("=" * 72)
    print("FIELD PULSATION: amplitude of oscillation at each node")
    print("=" * 72)
    print()

    # Measure field variation across the oscillation period
    max_variations = []
    for x in range(0, width + 1, 3):
        for y in [0, 3, 5]:
            vals = [f.get((x, y), 0) for f in fields]
            variation = max(vals) - min(vals)
            if variation > 0.001:
                max_variations.append(((x, y), variation, min(vals), max(vals)))

    max_variations.sort(key=lambda x: -x[1])
    print(f"  {'position':>10s}  {'variation':>10s}  {'min_field':>10s}  {'max_field':>10s}")
    print(f"  {'-' * 46}")
    for pos, var, mn, mx in max_variations[:20]:
        print(f"  ({pos[0]:2d},{pos[1]:2d})  {var:10.6f}  {mn:10.6f}  {mx:10.6f}")

    if max_variations:
        print(f"\n  Max pulsation amplitude: {max_variations[0][1]:.6f} at {max_variations[0][0]}")
        print(f"  Pulsation-to-average ratio: {max_variations[0][1] / avg_field.get(max_variations[0][0], 1):.4f}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
