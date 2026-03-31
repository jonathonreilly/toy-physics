#!/usr/bin/env python3
"""Does gravity bend a glider's path?

A translating pattern (glider) moves in a straight line.
Place a stationary mass nearby. Does the glider's trajectory
curve toward the mass — gravitational deflection of a moving object?

This tests Axiom 8 (gravity = continuation in distorted structure)
combined with Axiom 7 (inertia = undisturbed continuation).
Together: an undisturbed glider goes straight; a gravitationally
disturbed glider curves.

NOTE: The gravity mechanism works through the delay FIELD, but the
glider's motion is governed by the self-maintenance RULE (cellular
automaton). These are separate mechanisms in the current model.
The glider doesn't "feel" the delay field — it follows the CA rule.

So the real test is: does the MASS (as a static CA structure)
alter the glider's CA evolution? Not through the field, but
through direct CA interaction (the glider's cells interact with
the mass's cells via the birth/survival rule).

PStack experiment: glider-deflection
"""

from __future__ import annotations
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    build_rectangular_nodes,
    build_graph_neighbor_lookup,
    evolve_self_maintaining_pattern,
)


def pattern_centroid(state):
    if not state:
        return (0.0, 0.0)
    return (sum(x for x, _ in state) / len(state),
            sum(y for _, y in state) / len(state))


def main() -> None:
    width = 80
    height = 40
    steps = 100
    nodes = build_rectangular_nodes(width=width, height=height)
    lookup = build_graph_neighbor_lookup(nodes)

    # Standard Life rule (supports gliders)
    survive = frozenset({2, 3})
    birth = frozenset({3})

    # Glider seed moving in +x, -y direction
    glider_seed = frozenset([(10, 10), (11, 10), (12, 10), (12, 11), (11, 12)])

    print("=" * 80)
    print("GLIDER GRAVITATIONAL DEFLECTION TEST")
    print("=" * 80)
    print(f"Grid: {width}x{2*height+1}, rule: S={{2,3}} B={{3}}")
    print()

    # =========================================================
    # CONTROL: Glider with no mass (straight trajectory)
    # =========================================================
    print("CONTROL: Glider alone (no mass)")
    control_history = evolve_self_maintaining_pattern(
        nodes, glider_seed, survive_counts=survive, birth_counts=birth,
        steps=steps, neighbor_lookup=lookup,
    )
    control_centroids = [pattern_centroid(s) for s in control_history]
    control_sizes = [len(s) for s in control_history]

    print(f"  Steps: {steps}, final size: {control_sizes[-1]}")
    for i in range(0, min(len(control_centroids), 100), 20):
        cx, cy = control_centroids[i]
        print(f"    Step {i:3d}: centroid=({cx:.1f}, {cy:.1f}), size={control_sizes[i]}")

    # =========================================================
    # TEST: Glider with stationary mass nearby
    # =========================================================
    # Place a stable "still life" block near the glider's path
    # Under S={2,3} B={3}, a 2x2 block is a stable still life
    mass_configs = [
        ("mass at (30, -5)", frozenset([(30, -5), (31, -5), (30, -4), (31, -4)])),
        ("mass at (30, 0)", frozenset([(30, 0), (31, 0), (30, 1), (31, 1)])),
        ("mass at (30, 5)", frozenset([(30, 5), (31, 5), (30, 6), (31, 6)])),
        ("mass at (25, -2)", frozenset([(25, -2), (26, -2), (25, -1), (26, -1)])),
        ("mass at (25, -8)", frozenset([(25, -8), (26, -8), (25, -7), (26, -7)])),
        ("large mass (3x3) at (30, 0)", frozenset([
            (30, -1), (30, 0), (30, 1), (31, -1), (31, 0), (31, 1),
            (32, -1), (32, 0), (32, 1),
        ])),
    ]

    print()
    for mass_label, mass_nodes in mass_configs:
        # Combined seed: glider + mass
        combined_seed = glider_seed | mass_nodes

        history = evolve_self_maintaining_pattern(
            nodes, combined_seed, survive_counts=survive, birth_counts=birth,
            steps=steps, neighbor_lookup=lookup,
        )

        # Separate the glider from the mass in the evolved state
        # (track which component is the glider by proximity to initial position)
        centroids = [pattern_centroid(s) for s in history]
        sizes = [len(s) for s in history]

        # Compute deflection from control trajectory
        max_deflection = 0
        deflections_at_20 = []
        for i in range(min(len(centroids), len(control_centroids))):
            if control_sizes[i] > 0 and sizes[i] > 0:
                dx = centroids[i][0] - control_centroids[i][0]
                dy = centroids[i][1] - control_centroids[i][1]
                defl = math.sqrt(dx**2 + dy**2)
                max_deflection = max(max_deflection, defl)
                if i % 20 == 0:
                    deflections_at_20.append((i, dx, dy, defl))

        print(f"  {mass_label}:")
        print(f"    Final size: {sizes[-1]} (control: {control_sizes[-1]})")
        print(f"    Max deflection from control: {max_deflection:.2f}")
        for step, dx, dy, d in deflections_at_20:
            print(f"      Step {step:3d}: delta=({dx:+.1f}, {dy:+.1f}), |d|={d:.2f}")

        # Did the glider survive or get absorbed/destroyed?
        if sizes[-1] == 0:
            print(f"    OUTCOME: Pattern died")
        elif sizes[-1] == len(mass_nodes):
            print(f"    OUTCOME: Glider absorbed, only mass remains")
        elif sizes[-1] > len(mass_nodes) + 10:
            print(f"    OUTCOME: Interaction produced growth")
        elif abs(sizes[-1] - control_sizes[-1] - len(mass_nodes)) < 3:
            print(f"    OUTCOME: Glider + mass coexist")
        else:
            print(f"    OUTCOME: Complex interaction")
        print()

    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
