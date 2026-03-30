#!/usr/bin/env python3
"""Sweep the self-maintenance rule space to map which rules produce
stable persistent patterns.

The self-maintenance rule is a cellular automaton on the 8-neighbor
grid with two sets: survive_counts and birth_counts. A node survives
if its active-neighbor count is in survive_counts; a dead node is
born if its active-neighbor count is in birth_counts.

We test all reasonable survive/birth combinations with several seed
patterns to classify: stable (reaches fixed point), oscillating
(periodic), growing (unbounded), or dying (goes to zero).

PStack experiment: self-maintenance-rule-sweep
"""

from __future__ import annotations
import sys
import os
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    build_rectangular_nodes,
    evolve_self_maintaining_pattern,
    build_graph_neighbor_lookup,
)


def classify_orbit(history: list[frozenset]) -> tuple[str, int, int]:
    """Classify an orbit as DEAD, STABLE, OSCILLATING, or GROWING."""
    sizes = [len(h) for h in history]

    if sizes[-1] == 0:
        return "DEAD", 0, 0

    # Check for fixed point (last 4 states identical)
    if len(set(history[-4:])) == 1:
        return "STABLE", sizes[-1], 0

    # Check for period-2 oscillation
    if len(history) >= 4 and history[-1] == history[-3] and history[-2] == history[-4]:
        return "PERIOD-2", sizes[-1], sizes[-2]

    # Check for period-3
    if len(history) >= 6 and history[-1] == history[-4]:
        return "PERIOD-3", sizes[-1], 0

    # Check if growing
    if sizes[-1] > sizes[0] * 3:
        return "GROWING", sizes[-1], sizes[0]

    # Check if shrinking
    if sizes[-1] < sizes[0] // 3 and sizes[-1] > 0:
        return "SHRINKING", sizes[-1], sizes[0]

    return "COMPLEX", sizes[-1], sizes[0]


def main() -> None:
    width = 30
    height = 12
    nodes = build_rectangular_nodes(width=width, height=height)
    lookup = build_graph_neighbor_lookup(nodes)
    steps = 40

    print("=" * 72)
    print("SELF-MAINTENANCE RULE SWEEP")
    print("=" * 72)
    print(f"Grid: {width}x{2*height+1}, steps={steps}")
    print()

    # Seed patterns to test
    seeds = {
        "3x3_block": frozenset((15+dx, dy) for dx in range(-1, 2) for dy in range(-1, 2)),
        "5_cross": frozenset([(15, 0), (16, 0), (14, 0), (15, 1), (15, -1)]),
        "line_5": frozenset((15+i, 0) for i in range(5)),
        "2x3_rect": frozenset((15+dx, dy) for dx in range(2) for dy in range(3)),
        "glider_try": frozenset([(15, 0), (16, 0), (17, 0), (17, 1), (16, 2)]),
    }

    # Test survive/birth rule combinations
    # Survive: subsets of {1,2,3,4,5,6,7,8}
    # Birth: subsets of {1,2,3,4,5,6,7,8}
    # Too many combinations — test the most interesting ones

    survive_options = [
        frozenset({2, 3}),       # Standard Life
        frozenset({3, 4}),       # Model default
        frozenset({2, 3, 4}),    # Wider survive
        frozenset({1, 2, 3}),    # Low-count survive
        frozenset({3, 4, 5}),    # Mid-count survive
        frozenset({2, 3, 4, 5}), # Broad survive
        frozenset({4, 5, 6}),    # High-count survive
        frozenset({1, 2}),       # Very low
        frozenset({3}),          # Minimal
        frozenset({2}),          # Minimal low
    ]

    birth_options = [
        frozenset({3}),          # Standard Life
        frozenset({3, 4}),       # Model default
        frozenset({2, 3}),       # Easy birth
        frozenset({3, 4, 5}),    # Easy birth extended
        frozenset({2}),          # Very easy birth
        frozenset({4}),          # Hard birth
        frozenset({3, 6}),       # Sparse birth
        frozenset({2, 3, 4}),    # Broad birth
    ]

    print(f"{'survive':>20s}  {'birth':>15s}  ", end="")
    for seed_name in seeds:
        print(f"  {seed_name[:10]:>10s}", end="")
    print()
    print("-" * (40 + 12 * len(seeds)))

    interesting_rules = []

    for survive in survive_options:
        for birth in birth_options:
            s_str = "{" + ",".join(str(x) for x in sorted(survive)) + "}"
            b_str = "{" + ",".join(str(x) for x in sorted(birth)) + "}"
            print(f"{s_str:>20s}  {b_str:>15s}  ", end="")

            results = {}
            for seed_name, seed_nodes in seeds.items():
                history = evolve_self_maintaining_pattern(
                    nodes, seed_nodes,
                    survive_counts=survive, birth_counts=birth,
                    steps=steps, neighbor_lookup=lookup,
                )
                classification, final_size, extra = classify_orbit(history)
                results[seed_name] = (classification, final_size)
                tag = f"{classification[:5]}({final_size})"
                print(f"  {tag:>10s}", end="")

            print()

            # Track rules that produce stable patterns
            stable_count = sum(1 for c, _ in results.values() if c == "STABLE")
            if stable_count >= 2:
                interesting_rules.append((s_str, b_str, stable_count, results))

    print()
    print("=" * 72)
    print(f"RULES PRODUCING STABLE PATTERNS (>= 2 seeds)")
    print("=" * 72)
    print()

    for s_str, b_str, count, results in sorted(interesting_rules, key=lambda x: -x[2]):
        stable_seeds = [(name, size) for name, (cls, size) in results.items() if cls == "STABLE"]
        print(f"  S={s_str} B={b_str}: {count} stable seeds")
        for name, size in stable_seeds:
            print(f"    {name}: {size} nodes")

    # Model default detailed analysis
    print()
    print("=" * 72)
    print("MODEL DEFAULT RULE S={3,4} B={3,4}: Detailed orbit")
    print("=" * 72)
    print()

    for seed_name, seed_nodes in seeds.items():
        history = evolve_self_maintaining_pattern(
            nodes, seed_nodes,
            survive_counts=frozenset({3, 4}), birth_counts=frozenset({3, 4}),
            steps=steps, neighbor_lookup=lookup,
        )
        sizes = [len(h) for h in history]
        cls, final, _ = classify_orbit(history)
        print(f"  {seed_name}: {cls}, sizes = {sizes[:15]}{'...' if len(sizes)>15 else ''}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
