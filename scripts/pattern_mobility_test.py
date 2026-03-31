#!/usr/bin/env python3
"""Test whether self-maintaining patterns can MOVE across the graph.

The self-maintenance rule (S={3,4} B={3,4}) produces period-3
oscillators that stay in place. Can we find rules or initial
conditions where the pattern TRANSLATES — drifting spatially
over time?

If yes: this is the model's version of inertial motion (Axiom 7).
The pattern maintains its identity while moving through the network.

Approach:
1. Test the default rule with asymmetric seeds (glider-like)
2. Sweep rule space for rules that produce translating patterns
3. Test on both rectangular grids and generated DAGs

PStack experiment: pattern-mobility
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


def pattern_centroid(state: frozenset[tuple[int, int]]) -> tuple[float, float]:
    if not state:
        return (0.0, 0.0)
    xs = [x for x, _ in state]
    ys = [y for _, y in state]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def pattern_velocity(history: list[frozenset[tuple[int, int]]]) -> list[tuple[float, float]]:
    """Compute centroid velocity (dx, dy) per step."""
    centroids = [pattern_centroid(s) for s in history]
    velocities = []
    for i in range(1, len(centroids)):
        dx = centroids[i][0] - centroids[i-1][0]
        dy = centroids[i][1] - centroids[i-1][1]
        velocities.append((dx, dy))
    return velocities


def classify_motion(history: list[frozenset]) -> str:
    """Classify: STATIC, OSCILLATING, TRANSLATING, DEAD, CHAOTIC."""
    sizes = [len(s) for s in history]
    if sizes[-1] == 0:
        return "DEAD"

    centroids = [pattern_centroid(s) for s in history]

    # Total displacement
    total_dx = centroids[-1][0] - centroids[0][0]
    total_dy = centroids[-1][1] - centroids[0][1]
    total_displacement = math.sqrt(total_dx**2 + total_dy**2)

    # Check if centroid returns to start (oscillating)
    if total_displacement < 1.0:
        return "STATIC/OSCILLATING"

    # Check if motion is persistent (translating)
    # Compute displacement at each step
    mid = len(centroids) // 2
    first_half_dx = centroids[mid][0] - centroids[0][0]
    first_half_dy = centroids[mid][1] - centroids[0][1]
    second_half_dx = centroids[-1][0] - centroids[mid][0]
    second_half_dy = centroids[-1][1] - centroids[mid][1]

    # If both halves move in similar direction → translating
    dot = first_half_dx * second_half_dx + first_half_dy * second_half_dy
    if dot > 0 and total_displacement > 3.0:
        return "TRANSLATING"

    return "DRIFTING"


def main() -> None:
    width = 60
    height = 30
    steps = 80
    nodes = build_rectangular_nodes(width=width, height=height)
    lookup = build_graph_neighbor_lookup(nodes)

    print("=" * 80)
    print("PATTERN MOBILITY TEST")
    print("  Can self-maintaining patterns translate across the grid?")
    print("=" * 80)
    print(f"Grid: {width}x{2*height+1}, steps={steps}")
    print()

    # =========================================================
    # TEST 1: Glider-like seeds under various rules
    # =========================================================
    print("=" * 80)
    print("TEST 1: Asymmetric seeds — do any translate?")
    print("=" * 80)
    print()

    seeds = {
        "glider_A": frozenset([(30, 0), (31, 0), (32, 0), (32, 1), (31, 2)]),
        "glider_B": frozenset([(30, 0), (31, 0), (32, 0), (32, -1), (31, -2)]),
        "arrow_R": frozenset([(30, 0), (31, 1), (31, -1), (32, 0), (33, 0)]),
        "L_shape": frozenset([(30, 0), (31, 0), (32, 0), (32, 1), (32, 2)]),
        "T_shape": frozenset([(30, 0), (31, 0), (32, 0), (31, 1), (31, -1)]),
        "diagonal": frozenset([(30, 0), (31, 1), (32, 2), (33, 3), (34, 4)]),
        "boat": frozenset([(30, 0), (31, 0), (30, 1), (32, 1), (31, 2)]),
        "hook_R": frozenset([(30, 0), (31, 0), (32, 0), (32, 1), (31, -1)]),
    }

    rules = [
        ("S={3,4} B={3,4}", frozenset({3, 4}), frozenset({3, 4})),
        ("S={2,3} B={3}", frozenset({2, 3}), frozenset({3})),  # Standard Life
        ("S={2,3,4} B={3}", frozenset({2, 3, 4}), frozenset({3})),
        ("S={2,3,4} B={3,4}", frozenset({2, 3, 4}), frozenset({3, 4})),
        ("S={1,2,3} B={3}", frozenset({1, 2, 3}), frozenset({3})),
        ("S={2,3} B={3,6}", frozenset({2, 3}), frozenset({3, 6})),
        ("S={2,3,4,5} B={4}", frozenset({2, 3, 4, 5}), frozenset({4})),
    ]

    print(f"{'rule':>25s}  {'seed':>12s}  {'motion':>18s}  {'displacement':>12s}  "
          f"{'final_size':>10s}  {'centroid_path':>30s}")
    print("-" * 115)

    translators = []

    for rule_name, survive, birth in rules:
        for seed_name, seed_nodes in seeds.items():
            history = evolve_self_maintaining_pattern(
                nodes, seed_nodes,
                survive_counts=survive, birth_counts=birth,
                steps=steps, neighbor_lookup=lookup,
            )
            motion = classify_motion(history)
            centroids = [pattern_centroid(s) for s in history]
            displacement = math.sqrt(
                (centroids[-1][0] - centroids[0][0])**2 +
                (centroids[-1][1] - centroids[0][1])**2
            )
            centroid_path = " → ".join(
                f"({centroids[i][0]:.0f},{centroids[i][1]:.0f})"
                for i in range(0, min(len(centroids), 50), 10)
            )

            if motion == "TRANSLATING":
                translators.append((rule_name, seed_name, displacement, history))

            if motion in ("TRANSLATING", "DRIFTING") or displacement > 2:
                print(f"{rule_name:>25s}  {seed_name:>12s}  {motion:>18s}  "
                      f"{displacement:12.2f}  {len(history[-1]):10d}  {centroid_path:>30s}")

    # =========================================================
    # TEST 2: Details of any translating patterns
    # =========================================================
    if translators:
        print()
        print("=" * 80)
        print(f"TRANSLATING PATTERNS FOUND: {len(translators)}")
        print("=" * 80)
        print()

        for rule_name, seed_name, disp, history in translators[:3]:
            print(f"  {rule_name} / {seed_name}: displacement={disp:.2f}")
            centroids = [pattern_centroid(s) for s in history]
            velocities = pattern_velocity(history)
            mean_vx = sum(v[0] for v in velocities) / len(velocities)
            mean_vy = sum(v[1] for v in velocities) / len(velocities)
            speed = math.sqrt(mean_vx**2 + mean_vy**2)
            sizes = [len(s) for s in history]

            print(f"    Mean velocity: ({mean_vx:.4f}, {mean_vy:.4f}), speed={speed:.4f}")
            print(f"    Sizes: {sizes[:20]}...")
            print(f"    Centroid at step 0: ({centroids[0][0]:.1f}, {centroids[0][1]:.1f})")
            print(f"    Centroid at step {len(history)-1}: ({centroids[-1][0]:.1f}, {centroids[-1][1]:.1f})")
            print()
    else:
        print()
        print("  NO TRANSLATING PATTERNS FOUND in tested rules/seeds.")
        print("  The 8-neighbor grid may not support glider-like motion")
        print("  with these rule families. Need broader search or different topology.")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
