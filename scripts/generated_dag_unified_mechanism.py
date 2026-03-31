#!/usr/bin/env python3
"""Unified mechanism: one oscillating pattern produces gravity,
interference, AND decoherence simultaneously.

On the same generated DAG, with the same evolving pattern:
1. GRAVITY: the pattern's field distortion bends paths
2. INTERFERENCE: the field creates phase structure at the detector
3. DECOHERENCE: the pattern's oscillation creates time-varying topology

If all three emerge from one dynamical process, the model has a
unified mechanism for persistence, gravity, and decoherence.

PStack experiment: unified-mechanism
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
from scripts.generated_dag_opaque_oscillation import pathsum_with_opaque_nodes
from scripts.generated_dag_oscillation_decoherence import evolve_on_generated_dag


def pathsum_gravity_and_opaque(
    positions, adj, arrival, source_idx,
    detector_x, detector_ys, detector_tol,
    field, opaque_nodes,
):
    """Path-sum with BOTH gravity (field) AND opacity (topology change)."""
    n = len(positions)
    order = sorted(range(n), key=lambda i: arrival[i])
    amplitudes: dict[int, complex] = {source_idx: 1.0 + 0.0j}
    detector_amps: dict[float, complex] = defaultdict(complex)

    for i in order:
        if i not in amplitudes:
            continue
        if i in opaque_nodes:
            continue
        amp = amplitudes[i]
        x, y = positions[i]

        if abs(x - detector_x) < 0.5:
            for dy in detector_ys:
                if abs(y - dy) < detector_tol:
                    detector_amps[dy] += amp
            continue

        for j in adj.get(i, []):
            if j in opaque_nodes:
                continue
            jx, jy = positions[j]
            link_len = math.dist(positions[i], positions[j])
            avg_field = 0.5 * (field.get(i, 0) + field.get(j, 0))
            delay = link_len * (1.0 + avg_field)
            retained = math.sqrt(max(delay ** 2 - link_len ** 2, 0.0))
            action = delay - retained
            link_amp = cmath.exp(1j * 4.0 * action) / max(delay, 0.01)

            if j not in amplitudes:
                amplitudes[j] = 0.0 + 0.0j
            amplitudes[j] += amp * link_amp

    return {dy: abs(detector_amps[dy]) ** 2 for dy in detector_ys}


def main() -> None:
    n_layers = 25
    nodes_per_layer = 20
    y_range = 8.0
    detector_layer = n_layers - 1
    detector_ys = [float(y) for y in range(-8, 9)]
    detector_tol = 1.5

    print("=" * 80)
    print("UNIFIED MECHANISM: One pattern → gravity + interference + decoherence")
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

        pattern_seed = frozenset(
            i for i, (x, y) in enumerate(positions)
            if 10 <= x <= 14 and 2.0 <= y <= 6.0
        )
        if len(pattern_seed) < 4:
            print(f"  Too few seed nodes")
            continue

        history = evolve_on_generated_dag(positions, n, pattern_seed, steps=12)
        if len(history) < 9:
            print(f"  Too few steps")
            continue

        phase_states = history[6:9]
        phase_sizes = [len(s) for s in phase_states]
        print(f"  Pattern phases: sizes = {phase_sizes}")

        if all(s == 0 for s in phase_sizes):
            print(f"  Pattern died")
            continue

        # ===== BASELINE: no pattern at all =====
        free_field = {i: 0.0 for i in range(n)}
        baseline = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol, free_field,
        )
        total_baseline = sum(baseline.values())

        # ===== GRAVITY ONLY: field from time-averaged pattern, no opacity =====
        avg_persistent = set()
        for state in phase_states:
            avg_persistent |= state
        avg_field = compute_field_on_dag(positions, adj, frozenset(avg_persistent))

        gravity_only = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol, avg_field,
        )
        total_grav = sum(gravity_only.values())

        # ===== FULL MECHANISM: gravity + opacity at each phase =====
        phase_patterns = []
        for opaque in phase_states:
            if len(opaque) == 0:
                phase_patterns.append(gravity_only)
                continue
            field = compute_field_on_dag(positions, adj, opaque)
            pattern = pathsum_gravity_and_opaque(
                positions, adj, arrival, 0,
                float(detector_layer), detector_ys, detector_tol,
                field, opaque,
            )
            phase_patterns.append(pattern)

        # Slow detector averages over phases
        slow_pattern = {dy: sum(p.get(dy, 0) for p in phase_patterns) / len(phase_patterns)
                       for dy in detector_ys}
        total_slow = sum(slow_pattern.values())

        # ===== MEASURE THREE PHENOMENA =====

        # 1. GRAVITY: pattern shift from baseline
        gravity_shift = 0
        if total_baseline > 0 and total_grav > 0:
            gravity_shift = max(
                abs(gravity_only.get(dy, 0)/total_grav - baseline.get(dy, 0)/total_baseline)
                for dy in detector_ys
            )

        # 2. INTERFERENCE (phase sensitivity): how much does the pattern
        # change across oscillation phases?
        phase_var = 0
        totals = [sum(p.values()) for p in phase_patterns]
        if all(t > 0 for t in totals):
            normalized = [{dy: p.get(dy, 0)/t for dy in detector_ys}
                         for p, t in zip(phase_patterns, totals)]
            for dy in detector_ys:
                vals = [nm[dy] for nm in normalized]
                phase_var = max(phase_var, max(vals) - min(vals))

        # 3. DECOHERENCE: fast vs slow detector difference
        fast_pattern = phase_patterns[0]
        total_fast = sum(fast_pattern.values())
        decoherence = 0
        if total_fast > 0 and total_slow > 0:
            decoherence = max(
                abs(fast_pattern.get(dy, 0)/total_fast - slow_pattern.get(dy, 0)/total_slow)
                for dy in detector_ys
            )

        print(f"\n  GRAVITY (pattern shift from baseline): {gravity_shift:.4f}")
        print(f"  INTERFERENCE (phase variability):       {phase_var:.4f}")
        print(f"  DECOHERENCE (fast-vs-slow):              {decoherence:.4f}")
        print()

        all_present = gravity_shift > 0.01 and phase_var > 0.001 and decoherence > 0.001
        print(f"  ALL THREE PRESENT: {'YES' if all_present else 'NO'}")
        if all_present:
            print(f"  → One oscillating pattern produces gravity, interference,")
            print(f"    and decoherence simultaneously on this random DAG.")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
