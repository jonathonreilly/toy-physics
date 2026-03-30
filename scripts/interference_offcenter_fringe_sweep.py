#!/usr/bin/env python3
"""Measure fringe visibility V(y) at every screen position, not just y=0.

The first sweep showed contrast=1 at y=0 for all geometries, but
that is trivially guaranteed by the grid's reflection symmetry.
Off-center positions (y != 0) break that symmetry and test the
model's actual path-selection dynamics.

PStack experiment: interference-offcenter-fringe
"""

from __future__ import annotations

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.interference_geometry_sweep import parameterized_two_slit_distribution


def visibility(probs: list[float]) -> float:
    """V = (max - min) / (max + min).  0 = flat, 1 = perfect fringes."""
    p_max = max(probs)
    p_min = min(probs)
    denom = p_max + p_min
    if denom == 0:
        return 0.0
    return (p_max - p_min) / denom


def main() -> None:
    widths = [8, 12, 16, 20, 24]
    slit_half_seps = [2, 4, 6, 8]
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    height = 10
    screen_ys = list(range(-height, height + 1))

    print("=" * 72)
    print("OFF-CENTER FRINGE VISIBILITY SWEEP")
    print("=" * 72)
    print(f"widths: {widths}")
    print(f"slit_half_separations: {slit_half_seps}")
    print(f"phase_steps: {n_phases}")
    print(f"screen_positions: y = {-height} to {height}")
    print()

    all_results: list[dict] = []

    for w in widths:
        for slit_half in slit_half_seps:
            if slit_half >= height:
                continue

            barrier_x = w // 2
            slit_ys_set = {-slit_half, slit_half}

            for record in [False, True]:
                # For each screen position, sweep phase and compute visibility
                vis_by_y: dict[int, float] = {}
                for y in screen_ys:
                    probs_across_phase = []
                    for phase in phases:
                        dist = parameterized_two_slit_distribution(
                            screen_positions=[y],
                            record_created=record,
                            width=w,
                            height=height,
                            barrier_x=barrier_x,
                            slit_ys=slit_ys_set,
                            phase_shift_upper=phase,
                            normalize=False,
                        )
                        probs_across_phase.append(dist[y])
                    vis_by_y[y] = visibility(probs_across_phase)

                record_label = "RECORD" if record else "COHERENT"
                mean_vis = sum(vis_by_y.values()) / len(vis_by_y)
                nonzero_vis = [v for v in vis_by_y.values() if v > 0.001]
                min_nonzero = min(nonzero_vis) if nonzero_vis else 0.0
                max_vis = max(vis_by_y.values())

                row = {
                    "width": w,
                    "slit_half": slit_half,
                    "record": record,
                    "vis_by_y": vis_by_y,
                    "mean_vis": mean_vis,
                    "min_nonzero_vis": min_nonzero,
                    "max_vis": max_vis,
                }
                all_results.append(row)

                print(f"width={w:3d}  slit_half={slit_half}  mode={record_label:8s}  "
                      f"mean_V={mean_vis:.6f}  max_V={max_vis:.6f}  "
                      f"min_nonzero_V={min_nonzero:.6f}")

    # Detailed visibility profiles for coherent mode
    print()
    print("=" * 72)
    print("VISIBILITY PROFILES V(y) — COHERENT MODE")
    print("=" * 72)
    print()

    for row in all_results:
        if row["record"]:
            continue
        w = row["width"]
        sh = row["slit_half"]
        vis = row["vis_by_y"]
        print(f"--- width={w}, slit_sep={sh * 2} ---")
        print(f"{'y':>4s}  {'V(y)':>10s}  bar")
        for y in screen_ys:
            v = vis[y]
            bar = "#" * int(v * 60)
            marker = " <-- slit" if abs(y) == sh else ""
            print(f"{y:+4d}  {v:10.6f}  {bar}{marker}")
        print()

    # Record mode profiles (should all be ~0)
    print("=" * 72)
    print("VISIBILITY PROFILES V(y) — RECORD MODE (expect ~0 everywhere)")
    print("=" * 72)
    print()

    for row in all_results:
        if not row["record"]:
            continue
        w = row["width"]
        sh = row["slit_half"]
        vis = row["vis_by_y"]
        max_v = max(vis.values())
        print(f"width={w}, slit_sep={sh * 2}: max_V = {max_v:.10f}")

    # Summary: geometry dependence of mean visibility
    print()
    print("=" * 72)
    print("MEAN VISIBILITY vs GEOMETRY (coherent mode)")
    print("=" * 72)
    print()
    print(f"{'width':>6s}  {'slit_sep':>8s}  {'mean_V':>10s}  {'max_V':>10s}  {'min_nz_V':>10s}")
    print("-" * 52)
    for row in all_results:
        if row["record"]:
            continue
        print(f"{row['width']:6d}  {row['slit_half'] * 2:8d}  "
              f"{row['mean_vis']:10.6f}  {row['max_vis']:10.6f}  "
              f"{row['min_nonzero_vis']:10.6f}")

    # Key test: does off-center visibility vary with geometry?
    print()
    print("=" * 72)
    print("KEY TEST: V(y=1) across geometries (first off-center position)")
    print("=" * 72)
    print()
    print(f"{'width':>6s}  {'slit_sep':>8s}  {'V(y=0)':>10s}  {'V(y=1)':>10s}  {'V(y=2)':>10s}  {'V(y=3)':>10s}  {'V(y=5)':>10s}")
    print("-" * 68)
    for row in all_results:
        if row["record"]:
            continue
        vis = row["vis_by_y"]
        print(f"{row['width']:6d}  {row['slit_half'] * 2:8d}  "
              f"{vis[0]:10.6f}  {vis[1]:10.6f}  {vis[2]:10.6f}  "
              f"{vis[3]:10.6f}  {vis[5]:10.6f}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
