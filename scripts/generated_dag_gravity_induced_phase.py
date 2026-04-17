#!/usr/bin/env python3
"""Endogenous interference: gravity-induced phase differences.

The regional phase shift was the last hand-imposed element. Here we
replace it with a persistent-node cluster that creates a delay-field
distortion. Paths through the distorted region accumulate different
action (= different phase) than paths through the undistorted region.

If the detector shows phase-sensitivity to the mass position/strength,
the interference is FULLY ENDOGENOUS: random graph + persistent pattern
= interference, with zero hand-imposed phase parameters.

The only remaining "measurement" is comparing probability at the
detector with vs without the mass — the mass IS the phase shifter.

PStack experiment: gravity-induced-interference
"""

from __future__ import annotations
import math
import cmath
import heapq
from collections import defaultdict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import causal_order, generate_causal_dag
from scripts.generative_dag_gravity import compute_field_on_dag


def pathsum_with_field(
    positions, adj, arrival, source_idx,
    detector_x, detector_ys, detector_tol,
    field,
):
    """Path-sum where edge amplitudes depend on the delay field.

    delay = link_length * (1 + avg_field)
    action = delay - sqrt(delay² - link_length²)
    amplitude = e^(i*k*action) / delay

    No hand-imposed phase. The field provides all phase structure.
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
    print("GRAVITY-INDUCED INTERFERENCE (fully endogenous)")
    print("  No hand-imposed phase. Mass creates delay-field distortion.")
    print("  Compare detector pattern WITH vs WITHOUT mass.")
    print("=" * 80)
    print()

    for seed in range(10):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=2.5, rng_seed=seed,
        )

        # Free field (no mass)
        free_field = {i: 0.0 for i in range(len(positions))}

        # Mass in upper region at layers 10-14
        mass_indices = frozenset(
            i for i, (x, y) in enumerate(positions)
            if 10 <= x <= 14 and 3.0 <= y <= 7.0
        )

        if len(mass_indices) < 3:
            continue

        distorted_field = compute_field_on_dag(positions, adj, mass_indices)

        # Detector pattern WITHOUT mass
        free_pattern = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol,
            free_field,
        )

        # Detector pattern WITH mass
        grav_pattern = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol,
            distorted_field,
        )

        # Measure the difference — does the mass change the detector pattern?
        total_free = sum(free_pattern.values())
        total_grav = sum(grav_pattern.values())

        # Normalized pattern difference
        diffs = []
        for dy in detector_ys:
            pf = free_pattern.get(dy, 0) / max(total_free, 1e-30)
            pg = grav_pattern.get(dy, 0) / max(total_grav, 1e-30)
            diffs.append(abs(pg - pf))

        max_diff = max(diffs)
        mean_diff = sum(diffs) / len(diffs)

        print(f"  seed={seed:2d}: {len(mass_indices)} mass nodes, "
              f"max_pattern_diff={max_diff:.6f}, mean_diff={mean_diff:.6f}")

    # Detailed pattern for one seed
    print()
    print("=" * 80)
    print("DETAILED PATTERN: seed=42")
    print("=" * 80)
    print()

    positions, adj, arrival = generate_causal_dag(
        n_layers=n_layers, nodes_per_layer=nodes_per_layer,
        y_range=y_range, connect_radius=2.5, rng_seed=42,
    )
    free_field = {i: 0.0 for i in range(len(positions))}

    # Sweep mass position to create a "phase scan" equivalent
    print("  Sweep mass y-position (mass at layers 10-14):")
    print(f"  {'mass_y_center':>13s}  {'n_mass':>7s}  {'P(y=0) free':>12s}  {'P(y=0) grav':>12s}  "
          f"{'ratio':>8s}  {'pattern_shift':>14s}")
    print(f"  {'-' * 72}")

    free_pattern = pathsum_with_field(
        positions, adj, arrival, 0,
        float(detector_layer), [0.0], detector_tol, free_field,
    )
    p_free_center = free_pattern.get(0.0, 0)

    for mass_y_center in range(-6, 7, 2):
        mass_idx = frozenset(
            i for i, (x, y) in enumerate(positions)
            if 10 <= x <= 14 and mass_y_center - 2.0 <= y <= mass_y_center + 2.0
        )
        if len(mass_idx) < 2:
            continue

        dist_field = compute_field_on_dag(positions, adj, mass_idx)
        grav_pattern = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), [0.0], detector_tol, dist_field,
        )
        p_grav_center = grav_pattern.get(0.0, 0)
        ratio = p_grav_center / p_free_center if p_free_center > 0 else 0

        # Full pattern shift
        grav_full = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol, dist_field,
        )
        free_full = pathsum_with_field(
            positions, adj, arrival, 0,
            float(detector_layer), detector_ys, detector_tol, free_field,
        )
        tf = sum(free_full.values())
        tg = sum(grav_full.values())
        max_shift = max(
            abs(grav_full.get(dy, 0)/max(tg, 1e-30) - free_full.get(dy, 0)/max(tf, 1e-30))
            for dy in detector_ys
        )

        print(f"  {mass_y_center:13d}  {len(mass_idx):7d}  {p_free_center:12.4e}  "
              f"{p_grav_center:12.4e}  {ratio:8.4f}  {max_shift:14.6f}")

    # Key test: does moving the mass change WHERE probability goes?
    print()
    print("  If pattern_shift > 0: the mass redirects probability (gravitational lensing)")
    print("  If P(y=0) ratio varies with mass position: mass acts as endogenous phase element")
    print()
    print("  This is interference WITHOUT any hand-imposed phase parameter.")
    print("  The mass's delay-field distortion IS the phase shifter.")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
