#!/usr/bin/env python3
"""Test how much the discrete grid breaks Lorentz symmetry.

The local edge formula has exact Lorentz invariance, but the
rectangular grid has a preferred frame (horizontal/vertical axes).
This tests observable consequences:

1. Is the action from (0,0) to (R,0) the same as to (R/√2, R/√2)?
   (Same distance, different grid direction)
2. Does a mass at (20,5) bend horizontal and diagonal paths equally?
3. Does the gravitational time dilation depend on direction?

PStack experiment: lorentz-breaking
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
    infer_arrival_times_from_source,
)


def main() -> None:
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)

    print("=" * 72)
    print("LORENTZ BREAKING ON DISCRETE GRID")
    print("=" * 72)
    print()

    # =========================================================
    # TEST 1: Free action vs direction
    # =========================================================
    print("=" * 72)
    print("TEST 1: Free action vs path direction")
    print("  Same start, same Euclidean distance, different grid direction")
    print("=" * 72)
    print()

    width = 30
    height = 30
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)

    source = (0, 0)
    # Targets at approximately the same Euclidean distance but different angles
    targets = [
        ((20, 0), "horizontal (0°)"),
        ((14, 14), "diagonal (45°)"),
        ((0, 20), "vertical (90°)"),
        ((10, 17), "~60°"),
        ((17, 10), "~30°"),
    ]

    print(f"  {'target':>12s}  {'direction':>20s}  {'euclid_dist':>12s}  {'action':>10s}  "
          f"{'action/dist':>12s}  {'steps':>6s}")
    print(f"  {'-' * 78}")

    for target, direction in targets:
        dist = math.dist(source, target)
        action, path = stationary_action_path(width, height, source, target, free_rule)
        print(f"  {str(target):>12s}  {direction:>20s}  {dist:12.4f}  {action:10.4f}  "
              f"{action/dist:12.6f}  {len(path):6d}")

    # =========================================================
    # TEST 2: Arrival time isotropy
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 2: Arrival time isotropy (is speed of light direction-independent?)")
    print("=" * 72)
    print()

    nodes = build_rectangular_nodes(width=width, height=height)
    arrival_times = infer_arrival_times_from_source(nodes, source, free_rule)

    # Measure arrival time at points equidistant from source
    radius = 15
    print(f"  Points at Euclidean distance ≈ {radius} from source:")
    print(f"  {'point':>12s}  {'euclid_dist':>12s}  {'arrival_time':>12s}  {'signal_speed':>12s}")
    print(f"  {'-' * 52}")

    test_points = []
    for x in range(0, width + 1):
        for y in range(-height, height + 1):
            d = math.dist(source, (x, y))
            if abs(d - radius) < 0.5 and (x, y) in arrival_times:
                test_points.append((x, y, d))

    test_points.sort(key=lambda p: math.atan2(p[1], p[0]))

    for x, y, d in test_points[:16]:  # Sample around the circle
        t = arrival_times[(x, y)]
        speed = d / t if t > 0 else 0
        angle = math.degrees(math.atan2(y, x))
        print(f"  ({x:2d},{y:+3d}) {angle:+6.1f}°  {d:12.4f}  {t:12.4f}  {speed:12.6f}")

    # Compute signal speed anisotropy
    speeds = [math.dist(source, (x, y)) / arrival_times[(x, y)]
              for x, y, _ in test_points if arrival_times[(x, y)] > 0]
    if speeds:
        print(f"\n  Signal speed range: [{min(speeds):.6f}, {max(speeds):.6f}]")
        print(f"  Anisotropy: {(max(speeds)-min(speeds))/min(speeds)*100:.2f}%")

    # =========================================================
    # TEST 3: Gravitational bending direction-dependence
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 3: Gravitational bending vs path direction")
    print("  Same mass, paths at different angles — is bending direction-dependent?")
    print("=" * 72)
    print()

    mass = frozenset((15, y) for y in [12, 13, 14, 15, 16])
    dist_rule = derive_local_rule(persistent_nodes=mass, postulates=postulates)

    # Paths passing at similar closest-approach distances but different directions
    path_configs = [
        ((0, 8), (30, 8), "horizontal, y=8"),
        ((0, 5), (30, 5), "horizontal, y=5"),
        ((0, 0), (30, 0), "horizontal, y=0"),
        ((5, 0), (5, 30), "vertical, x=5"),
        ((10, 0), (10, 30), "vertical, x=10"),
        ((0, 0), (30, 30), "diagonal"),
    ]

    print(f"  {'direction':>25s}  {'free_action':>12s}  {'dist_action':>12s}  {'action_diff':>12s}")
    print(f"  {'-' * 65}")

    for s, t, direction in path_configs:
        fa, _ = stationary_action_path(width, height, s, t, free_rule)
        da, dp = stationary_action_path(width, height, s, t, dist_rule)
        ad = da - fa
        print(f"  {direction:>25s}  {fa:12.4f}  {da:12.4f}  {ad:12.4f}")

    # =========================================================
    # TEST 4: Action per unit distance in different directions
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 4: Action per unit distance — the 'discreteness cost'")
    print("=" * 72)
    print()

    print("  If the grid were isotropic, action/distance would be constant.")
    print("  Deviations measure how much the grid breaks rotational symmetry.")
    print()

    for dist_target in [10, 15, 20]:
        print(f"  Paths of Euclidean length ≈ {dist_target}:")
        targets_at_dist = []
        for x in range(1, width + 1):
            for y in range(-height, height + 1):
                d = math.dist(source, (x, y))
                if abs(d - dist_target) < 1.0:
                    targets_at_dist.append((x, y, d))

        targets_at_dist.sort(key=lambda p: math.atan2(p[1], p[0]))
        sampled = targets_at_dist[::max(1, len(targets_at_dist) // 8)]

        ratios = []
        for x, y, d in sampled:
            action, _ = stationary_action_path(width, height, source, (x, y), free_rule)
            ratio = action / d
            ratios.append(ratio)
            angle = math.degrees(math.atan2(y, x))
            print(f"    ({x:2d},{y:+3d}) {angle:+6.1f}°: action/dist = {ratio:.6f}")

        if ratios:
            print(f"    Range: [{min(ratios):.6f}, {max(ratios):.6f}], "
                  f"anisotropy = {(max(ratios)-min(ratios))/min(ratios)*100:.2f}%")
        print()

    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
