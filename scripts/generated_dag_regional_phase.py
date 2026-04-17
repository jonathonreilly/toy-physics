#!/usr/bin/env python3
"""Interference via REGIONAL phase shift on generated DAG.

Instead of shifting one edge (which requires sparse bottlenecks),
shift ALL edges that cross the bottleneck in the upper y-region.
This is analogous to the original experiment's phase_shift_upper
and works with dense bottlenecks.

The key question: how much of the interference is from the graph
structure vs from the phase-shift region choice?

Also: test with the region boundary at different y-positions to
find the graph's "natural" interference axis.

PStack experiment: regional-phase-interference
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import causal_order, generate_causal_dag
from scripts.generated_dag_natural_bottleneck import find_bottleneck


def pathsum_regional_phase(
    positions, adj, arrival, source_idx,
    detector_x, detector_ys, detector_tol,
    barrier_x, phase_boundary_y, phase_shift,
):
    """Path-sum with phase shift on all crossings above phase_boundary_y.

    No barrier blocking. All edges pass. But edges crossing barrier_x
    with y > phase_boundary_y get a phase shift.
    """
    n = len(positions)
    order = causal_order(positions, arrival)
    amplitudes: dict[int, complex] = {source_idx: 1.0 + 0.0j}
    detector_amps: dict[float, complex] = defaultdict(complex)

    for i in order:
        if i not in amplitudes:
            continue
        amp = amplitudes[i]
        x, y = positions[i]

        if abs(x - detector_x) < 0.5:
            for dy in detector_ys:
                if abs(y - dy) < detector_tol:
                    detector_amps[dy] += amp
            continue

        for j in adj.get(i, []):
            jx, jy = positions[j]
            dist = math.dist(positions[i], positions[j])
            link_amp = cmath.exp(1j * 4.0 * dist) / max(dist, 0.01)

            # Phase shift for crossings in the upper region
            if x < barrier_x <= jx and jy > phase_boundary_y:
                link_amp *= cmath.exp(1j * phase_shift)

            if j not in amplitudes:
                amplitudes[j] = 0.0 + 0.0j
            amplitudes[j] += amp * link_amp

    return {dy: abs(detector_amps[dy]) ** 2 for dy in detector_ys}


def visibility(probs):
    pm, pn = max(probs), min(probs)
    return (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0


def main() -> None:
    n_layers = 25
    nodes_per_layer = 20
    y_range = 8.0
    detector_layer = n_layers - 1
    n_phases = 16
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    detector_tol = 1.5

    print("=" * 80)
    print("REGIONAL PHASE INTERFERENCE ON GENERATED DAG")
    print("  No barrier blocking. Phase shift on upper-y crossings at bottleneck.")
    print("=" * 80)
    print()

    # =========================================================
    # TEST 1: Regional phase at natural bottleneck, boundary at y=0
    # =========================================================
    print("TEST 1: Phase boundary at y=0, natural bottleneck position")
    print()
    print(f"{'seed':>5s}  {'bn_x':>5s}  {'V(y=0)':>8s}  {'V(y=-3)':>8s}  {'V(y=+3)':>8s}  {'mean_V':>8s}")
    print("-" * 50)

    for seed in range(20):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )
        bn_x, _ = find_bottleneck(positions, adj, n_layers)

        vis_by_y = {}
        for det_y in [-3.0, 0.0, 3.0]:
            probs = []
            for phase in phases:
                dist = pathsum_regional_phase(
                    positions, adj, arrival, 0,
                    float(detector_layer), [det_y], detector_tol,
                    bn_x, 0.0, phase,
                )
                probs.append(dist.get(det_y, 0.0))
            vis_by_y[det_y] = visibility(probs) if any(p > 0 for p in probs) else -1.0

        valid = [v for v in vis_by_y.values() if v >= 0]
        mean_v = sum(valid) / len(valid) if valid else 0

        print(f"{seed:5d}  {bn_x:5d}  {vis_by_y.get(0.0, -1):8.4f}  "
              f"{vis_by_y.get(-3.0, -1):8.4f}  {vis_by_y.get(3.0, -1):8.4f}  "
              f"{mean_v:8.4f}")

    # =========================================================
    # TEST 2: Same graph, sweep phase boundary position
    # =========================================================
    print()
    print("=" * 80)
    print("TEST 2: Sweep phase boundary y-position (seed=42)")
    print("  Which y-boundary gives strongest interference?")
    print("=" * 80)
    print()

    positions, adj, arrival = generate_causal_dag(
        n_layers=n_layers, nodes_per_layer=nodes_per_layer,
        y_range=y_range, connect_radius=2.5, rng_seed=42,
    )
    bn_x, _ = find_bottleneck(positions, adj, n_layers)

    print(f"{'boundary_y':>10s}  {'V(y=0)':>8s}  {'n_upper_crossings':>18s}")
    print("-" * 40)

    for boundary_y in [-6, -4, -2, 0, 2, 4, 6]:
        # Count how many crossings are "upper" (above boundary)
        n_upper = sum(1 for i, children in adj.items()
                      for j in children
                      if positions[i][0] < bn_x <= positions[j][0]
                      and positions[j][1] > boundary_y)

        probs = []
        for phase in phases:
            dist = pathsum_regional_phase(
                positions, adj, arrival, 0,
                float(detector_layer), [0.0], detector_tol,
                bn_x, float(boundary_y), phase,
            )
            probs.append(dist.get(0.0, 0.0))

        v = visibility(probs) if any(p > 0 for p in probs) else -1.0
        print(f"{boundary_y:10d}  {v:8.4f}  {n_upper:18d}")

    # =========================================================
    # TEST 3: No bottleneck constraint — phase at midpoint
    # =========================================================
    print()
    print("=" * 80)
    print("TEST 3: Phase at graph midpoint (layer 12), no bottleneck search")
    print("  Is the bottleneck even necessary?")
    print("=" * 80)
    print()

    print(f"{'seed':>5s}  {'V_bottleneck':>13s}  {'V_midpoint':>11s}  {'bn_x':>5s}")
    print("-" * 38)

    for seed in range(10):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )
        bn_x, _ = find_bottleneck(positions, adj, n_layers)

        for label, bx in [("bottleneck", bn_x), ("midpoint", 12)]:
            probs = []
            for phase in phases:
                dist = pathsum_regional_phase(
                    positions, adj, arrival, 0,
                    float(detector_layer), [0.0], detector_tol,
                    bx, 0.0, phase,
                )
                probs.append(dist.get(0.0, 0.0))
            v = visibility(probs) if any(p > 0 for p in probs) else -1.0
            if label == "bottleneck":
                v_bn = v
            else:
                v_mid = v

        print(f"{seed:5d}  {v_bn:13.4f}  {v_mid:11.4f}  {bn_x:5d}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
