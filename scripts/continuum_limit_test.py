#!/usr/bin/env python3
"""Test whether the model has a well-defined continuum limit.

The 8.2% Lorentz breaking comes from the discrete grid's finite
connectivity. If we measure physics at longer distances (more grid
steps between source and detector), the staircase averaging should
reduce the effective anisotropy.

Tests:
1. Signal speed anisotropy vs measurement distance
2. Action-per-distance anisotropy vs path length
3. Interference visibility convergence at larger grid sizes
4. Gravity bending convergence at larger grid sizes

If anisotropy → 0 as distance → ∞: the continuum limit exists.
If anisotropy → constant > 0: the discreteness is irreducible.

PStack experiment: continuum-limit
"""

from __future__ import annotations
import math
import sys
import os
import heapq

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates,
    build_rectangular_nodes,
    derive_local_rule,
    derive_node_field,
    stationary_action_path,
    infer_arrival_times_from_source,
    local_edge_properties,
)


def main() -> None:
    postulates = RulePostulates(phase_per_action=4.0, attenuation_power=1.0)
    free_rule = derive_local_rule(persistent_nodes=frozenset(), postulates=postulates)

    print("=" * 72)
    print("CONTINUUM LIMIT TEST")
    print("=" * 72)
    print()

    # =========================================================
    # TEST 1: Signal speed anisotropy vs distance
    # =========================================================
    print("=" * 72)
    print("TEST 1: Signal speed anisotropy vs measurement distance")
    print("=" * 72)
    print()

    grid_size = 80
    height = 80
    nodes = build_rectangular_nodes(width=grid_size, height=height)
    node_field = derive_node_field(nodes, free_rule)

    source = (0, 0)
    arrival_times = infer_arrival_times_from_source(nodes, source, free_rule)

    print(f"  {'radius':>7s}  {'speed_min':>10s}  {'speed_max':>10s}  {'anisotropy%':>12s}  {'n_points':>9s}")
    print(f"  {'-' * 52}")

    for radius in [5, 10, 15, 20, 30, 40, 50, 60, 70]:
        speeds = []
        for x in range(0, grid_size + 1):
            for y in range(-height, height + 1):
                d = math.dist(source, (x, y))
                if abs(d - radius) < 1.0 and (x, y) in arrival_times and arrival_times[(x, y)] > 0:
                    speed = d / arrival_times[(x, y)]
                    speeds.append(speed)

        if len(speeds) >= 4:
            aniso = (max(speeds) - min(speeds)) / min(speeds) * 100
            print(f"  {radius:7d}  {min(speeds):10.6f}  {max(speeds):10.6f}  {aniso:11.4f}%  {len(speeds):9d}")

    # =========================================================
    # TEST 2: Action per distance vs path length for off-axis paths
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 2: Action/distance for off-axis paths vs path length")
    print("  (30° angle — the worst case for grid anisotropy)")
    print("=" * 72)
    print()

    print(f"  {'distance':>9s}  {'target':>12s}  {'action':>10s}  {'act/dist':>10s}  {'excess%':>9s}")
    print(f"  {'-' * 56}")

    for scale in [5, 10, 15, 20, 30, 40, 50, 60]:
        # ~30 degree angle: target at (scale, scale*tan(30°)) ≈ (scale, scale*0.577)
        tx = scale
        ty = round(scale * 0.577)
        if tx > grid_size or ty > height:
            continue
        d = math.dist((0, 0), (tx, ty))
        action, _ = stationary_action_path(grid_size, height, (0, 0), (tx, ty), free_rule)
        excess = (action / d - 1.0) * 100
        print(f"  {d:9.2f}  ({tx:3d},{ty:+3d})  {action:10.4f}  {action/d:10.6f}  {excess:8.4f}%")

    # =========================================================
    # TEST 3: Key physics predictions vs grid size
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 3: Interference visibility at fixed physical setup, varying resolution")
    print("  (Same slit_sep/width RATIO at different grid sizes)")
    print("=" * 72)
    print()

    # Import the parameterized two-slit function
    from scripts.interference_geometry_sweep import parameterized_two_slit_distribution

    def vis(probs):
        pm, pn = max(probs), min(probs)
        return (pm - pn) / (pm + pn) if (pm + pn) > 0 else 0.0

    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]

    # Fixed ratio: width/slit_sep = 2.5
    print(f"  {'width':>6s}  {'slit_sep':>8s}  {'ratio':>6s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'mean_V':>10s}")
    print(f"  {'-' * 55}")

    for w in [8, 12, 16, 20, 24, 28, 32]:
        sh = max(1, w // 5)  # ratio ~ 2.5
        h = max(sh + 3, 10)
        ratio = w / (2 * sh)
        screen_ys = list(range(-h, h + 1))

        vis_by_y = {}
        for y in [0, 1]:
            probs = []
            for phase in phases:
                dist = parameterized_two_slit_distribution(
                    screen_positions=[y], record_created=False,
                    width=w, height=h, slit_ys={-sh, sh},
                    phase_shift_upper=phase, normalize=False,
                )
                probs.append(dist[y])
            vis_by_y[y] = vis(probs)

        # Mean V across all screen positions
        all_vis = []
        for y in screen_ys:
            probs = []
            for phase in phases:
                dist = parameterized_two_slit_distribution(
                    screen_positions=[y], record_created=False,
                    width=w, height=h, slit_ys={-sh, sh},
                    phase_shift_upper=phase, normalize=False,
                )
                probs.append(dist[y])
            all_vis.append(vis(probs))
        mean_v = sum(all_vis) / len(all_vis)

        print(f"  {w:6d}  {2*sh:8d}  {ratio:6.2f}  {vis_by_y[0]:10.6f}  "
              f"{vis_by_y[1]:10.6f}  {mean_v:10.6f}")

    # =========================================================
    # TEST 4: Gravity bending convergence
    # =========================================================
    print()
    print("=" * 72)
    print("TEST 4: Gravity action_diff at fixed physical ratio, varying grid size")
    print("  (Mass at center, 5 nodes, measure action at y=0)")
    print("=" * 72)
    print()

    print(f"  {'width':>6s}  {'height':>6s}  {'ad':>12s}  {'ad_normalized':>14s}")
    print(f"  {'-' * 44}")

    for w, h in [(20, 10), (30, 15), (40, 20), (60, 30), (80, 40)]:
        mass_x = w // 2
        mass_y = h // 2
        pnodes = frozenset((mass_x, y) for y in range(mass_y - 2, mass_y + 3))
        dist_rule = derive_local_rule(persistent_nodes=pnodes, postulates=postulates)

        fa, _ = stationary_action_path(w, h, (0, 0), (w, 0), free_rule)
        da, _ = stationary_action_path(w, h, (0, 0), (w, 0), dist_rule)
        ad = da - fa
        ad_norm = ad / w  # normalize by path length
        print(f"  {w:6d}  {h:6d}  {ad:12.4f}  {ad_norm:14.6f}")

    print()
    print("If ad_normalized converges: gravity effect per unit length is well-defined.")
    print("If ad_normalized → 0: gravity becomes negligible at large scale (finite range).")
    print("If ad_normalized → constant: gravity has a scale-invariant effect.")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
