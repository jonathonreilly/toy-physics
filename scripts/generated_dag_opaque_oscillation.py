#!/usr/bin/env python3
"""Strong endogenous decoherence: oscillating pattern blocks paths.

The pattern's evolution makes nodes opaque (amplitude = 0) during
phases when they're "active" in the self-maintenance rule. During
other phases, the nodes are transparent.

This creates TIME-VARYING TOPOLOGY from the pattern's own dynamics.
Different oscillation phases have different path structures → different
detector patterns. Averaging over phases = decoherence.

The mechanism: a persistent pattern that maintains itself by
periodically blocking different paths through its region.

PStack experiment: opaque-oscillation-decoherence
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
from scripts.generated_dag_oscillation_decoherence import evolve_on_generated_dag


def pathsum_with_opaque_nodes(
    positions, adj, arrival, source_idx,
    detector_x, detector_ys, detector_tol,
    opaque_nodes: frozenset[int],
):
    """Path-sum where opaque_nodes have amplitude zeroed (topology change)."""
    n = len(positions)
    order = sorted(range(n), key=lambda i: arrival[i])
    amplitudes: dict[int, complex] = {source_idx: 1.0 + 0.0j}
    detector_amps: dict[float, complex] = defaultdict(complex)

    for i in order:
        if i not in amplitudes:
            continue
        if i in opaque_nodes:
            continue  # Blocked — no propagation through this node
        amp = amplitudes[i]
        x, y = positions[i]

        if abs(x - detector_x) < 0.5:
            for dy in detector_ys:
                if abs(y - dy) < detector_tol:
                    detector_amps[dy] += amp
            continue

        for j in adj.get(i, []):
            if j in opaque_nodes:
                continue  # Can't reach opaque nodes
            jx, jy = positions[j]
            dist = math.dist(positions[i], positions[j])
            link_amp = cmath.exp(1j * 4.0 * dist) / max(dist, 0.01)

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
    print("OPAQUE OSCILLATION DECOHERENCE")
    print("  Pattern nodes block paths during active phases.")
    print("  Different phases → different topology → averaging = decoherence.")
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

        # Seed pattern
        pattern_seed = frozenset(
            i for i, (x, y) in enumerate(positions)
            if 10 <= x <= 14 and 2.0 <= y <= 6.0
        )

        if len(pattern_seed) < 4:
            print(f"  Too few seed nodes ({len(pattern_seed)})")
            continue

        # Evolve
        history = evolve_on_generated_dag(positions, n, pattern_seed, steps=12)
        sizes = [len(h) for h in history]
        print(f"  Evolution: sizes = {sizes[:9]}")

        if len(history) < 9:
            continue

        phase_states = history[6:9]

        # Free pattern (no opaque nodes)
        free_pattern = pathsum_with_opaque_nodes(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol,
            frozenset(),
        )
        total_free = sum(free_pattern.values())

        if total_free == 0:
            print(f"  No signal in free pattern")
            continue

        # Pattern for each oscillation phase (active nodes are opaque)
        phase_patterns = []
        for phase_idx, opaque in enumerate(phase_states):
            pattern = pathsum_with_opaque_nodes(
                positions, adj, arrival, 0,
                float(detector_layer), detector_ys, detector_tol,
                opaque,
            )
            phase_patterns.append(pattern)
            tp = sum(pattern.values())
            # Pattern shift from free
            if tp > 0:
                max_shift = max(
                    abs(pattern.get(dy, 0)/tp - free_pattern.get(dy, 0)/total_free)
                    for dy in detector_ys
                )
            else:
                max_shift = 1.0  # Total blockage
            print(f"  Phase {phase_idx}: {len(opaque)} opaque nodes, "
                  f"signal={tp:.2e}, shift_from_free={max_shift:.4f}")

        # Slow detector: average probabilities over phases
        slow_pattern = {}
        for dy in detector_ys:
            slow_pattern[dy] = sum(p.get(dy, 0) for p in phase_patterns) / len(phase_patterns)
        total_slow = sum(slow_pattern.values())

        # Fast detector: sees one phase
        fast_pattern = phase_patterns[0]
        total_fast = sum(fast_pattern.values())

        # Phase variability (how much pattern changes between phases)
        phase_var = 0
        totals = [sum(p.values()) for p in phase_patterns]
        if all(t > 0 for t in totals):
            normalized = [{dy: p.get(dy, 0)/t for dy in detector_ys}
                         for p, t in zip(phase_patterns, totals)]
            for dy in detector_ys:
                vals = [nm[dy] for nm in normalized]
                phase_var = max(phase_var, max(vals) - min(vals))

        # Fast-vs-slow difference
        fast_slow_diff = 0
        if total_fast > 0 and total_slow > 0:
            for dy in detector_ys:
                pf = fast_pattern.get(dy, 0) / total_fast
                ps = slow_pattern.get(dy, 0) / total_slow
                fast_slow_diff = max(fast_slow_diff, abs(pf - ps))

        print(f"  Phase variability: {phase_var:.6f}")
        print(f"  Fast-vs-slow diff: {fast_slow_diff:.6f}")
        print(f"  (cf. field-only oscillation decoherence was ~0.015 / ~0.005)")

    print()
    print("If phase_var >> 0.015: opaque oscillation produces MUCH stronger")
    print("decoherence than field-only oscillation.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
