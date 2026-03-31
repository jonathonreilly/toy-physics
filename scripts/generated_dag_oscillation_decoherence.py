#!/usr/bin/env python3
"""Endogenous decoherence from persistent-pattern oscillation.

The default self-maintenance rule produces period-3 oscillators.
Each oscillation phase has a different persistent-node configuration →
different delay field → different detector pattern.

A "fast" detector sees one phase (coherent). A "slow" detector
averages over all phases (incoherent mixture → decoherence).

The decoherence arises from the pattern's own dynamics — no injected
shortcuts or hand-imposed topology changes.

PStack experiment: oscillation-decoherence
"""

from __future__ import annotations
import math
import cmath
import heapq
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.generative_dag_gravity import compute_field_on_dag
from scripts.generated_dag_gravity_induced_phase import pathsum_with_field

from toy_event_physics import (
    build_rectangular_nodes,
    build_graph_neighbor_lookup,
    evolve_self_maintaining_pattern,
)


def evolve_on_generated_dag(
    positions, n_nodes,
    seed_indices: frozenset[int],
    steps: int = 12,
) -> list[frozenset[int]]:
    """Run self-maintenance on the generated graph's spatial positions.

    Uses a rectangular grid overlaid on the generated positions to run
    the cellular automaton, then maps back to graph node indices.
    """
    # Build a grid covering the generated graph's extent
    xs = [positions[i][0] for i in range(n_nodes)]
    ys = [positions[i][1] for i in range(n_nodes)]
    w = int(max(xs)) + 1
    h = int(max(abs(y) for y in ys)) + 1

    grid_nodes = build_rectangular_nodes(width=w, height=h)
    lookup = build_graph_neighbor_lookup(grid_nodes)

    # Map seed indices to nearest grid positions
    grid_seeds = set()
    for idx in seed_indices:
        gx = round(positions[idx][0])
        gy = round(positions[idx][1])
        if (gx, gy) in grid_nodes:
            grid_seeds.add((gx, gy))

    # Evolve
    history = evolve_self_maintaining_pattern(
        grid_nodes, frozenset(grid_seeds),
        survive_counts=frozenset({3, 4}),
        birth_counts=frozenset({3, 4}),
        steps=steps,
        neighbor_lookup=lookup,
    )

    # Map grid states back to graph node indices
    graph_history = []
    for state in history:
        matching = frozenset(
            i for i in range(n_nodes)
            if (round(positions[i][0]), round(positions[i][1])) in state
        )
        graph_history.append(matching)

    return graph_history


def main() -> None:
    n_layers = 25
    nodes_per_layer = 20
    y_range = 8.0
    detector_layer = n_layers - 1
    detector_ys = [float(y) for y in range(-8, 9)]
    detector_tol = 1.5

    print("=" * 80)
    print("OSCILLATION DECOHERENCE (fully endogenous)")
    print("  Persistent pattern oscillates → different fields per phase →")
    print("  slow detector averages → decoherence from dynamics alone.")
    print("=" * 80)
    print()

    for seed in [42, 123, 456]:
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )
        n = len(positions)

        print(f"\n{'=' * 60}")
        print(f"SEED = {seed}")
        print(f"{'=' * 60}")

        # Seed a persistent pattern at layers 10-14, y=3-7
        pattern_seed = frozenset(
            i for i, (x, y) in enumerate(positions)
            if 10 <= x <= 14 and 3.0 <= y <= 7.0
        )

        if len(pattern_seed) < 4:
            print(f"  Too few seed nodes ({len(pattern_seed)}), skipping")
            continue

        # Evolve the pattern
        history = evolve_on_generated_dag(positions, n, pattern_seed, steps=12)
        sizes = [len(h) for h in history]
        print(f"  Pattern evolution: sizes = {sizes[:9]}")

        # Skip transients, use steps 6-8 (one full period if period-3)
        if len(history) < 9:
            print(f"  Too few evolution steps")
            continue

        phase_states = history[6:9]
        phase_sizes = [len(s) for s in phase_states]
        print(f"  Using phases 6-8: sizes = {phase_sizes}")

        # Free field baseline
        free_field = {i: 0.0 for i in range(n)}
        free_pattern = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol, free_field,
        )
        total_free = sum(free_pattern.values())

        # Compute pattern for each oscillation phase
        phase_patterns = []
        for phase_idx, pnodes in enumerate(phase_states):
            if len(pnodes) < 2:
                # Dead pattern — use free field
                phase_patterns.append(free_pattern)
                continue

            field = compute_field_on_dag(positions, adj, pnodes)
            pattern = pathsum_with_field(
                positions, adj, arrival, 0,
                float(detector_layer), detector_ys, detector_tol, field,
            )
            phase_patterns.append(pattern)

        # "Fast" detector: sees one phase (pick phase 0)
        fast_pattern = phase_patterns[0]
        total_fast = sum(fast_pattern.values())

        # "Slow" detector: averages probability over all phases
        slow_pattern = {}
        for dy in detector_ys:
            slow_pattern[dy] = sum(p.get(dy, 0) for p in phase_patterns) / len(phase_patterns)
        total_slow = sum(slow_pattern.values())

        # Pattern difference: fast vs slow
        max_diff_fast_slow = 0
        if total_fast > 0 and total_slow > 0:
            for dy in detector_ys:
                pf = fast_pattern.get(dy, 0) / total_fast
                ps = slow_pattern.get(dy, 0) / total_slow
                max_diff_fast_slow = max(max_diff_fast_slow, abs(pf - ps))

        # Pattern difference: each phase vs free
        phase_shifts = []
        for pattern in phase_patterns:
            tp = sum(pattern.values())
            if tp > 0 and total_free > 0:
                max_shift = max(
                    abs(pattern.get(dy, 0)/tp - free_pattern.get(dy, 0)/total_free)
                    for dy in detector_ys
                )
                phase_shifts.append(max_shift)

        # Variability across phases (how much does the pattern change?)
        phase_variability = 0
        if len(phase_patterns) >= 2:
            totals = [sum(p.values()) for p in phase_patterns]
            if all(t > 0 for t in totals):
                normalized = [
                    {dy: p.get(dy, 0)/t for dy in detector_ys}
                    for p, t in zip(phase_patterns, totals)
                ]
                for dy in detector_ys:
                    vals = [n[dy] for n in normalized]
                    phase_variability = max(phase_variability, max(vals) - min(vals))

        print(f"  Phase shifts from free: {[f'{s:.4f}' for s in phase_shifts]}")
        print(f"  Phase variability (max variation across phases): {phase_variability:.6f}")
        print(f"  Fast-vs-slow diff: {max_diff_fast_slow:.6f}")
        print()
        print(f"  If phase_variability > 0: oscillation changes the interference pattern")
        print(f"  If fast-vs-slow > 0: slow detector sees different pattern = decoherence")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
