#!/usr/bin/env python3
"""Fine sweep of the critical width/slit_sep ratio for off-center visibility.

Determines the exact threshold where V(y) transitions from 0 to nonzero.
PStack experiment: critical-ratio-threshold
"""

from __future__ import annotations
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.interference_geometry_sweep import parameterized_two_slit_distribution


def visibility(probs: list[float]) -> float:
    p_max, p_min = max(probs), min(probs)
    denom = p_max + p_min
    return (p_max - p_min) / denom if denom > 0 else 0.0


def main() -> None:
    n_phases = 24
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    height = 10
    test_ys = [1, 2, 3, 5]

    # Fine sweep: width 4-40 step 2, slit_half 1-12 step 1
    widths = list(range(4, 42, 2))
    slit_halves = list(range(1, 13))

    print("=" * 72)
    print("CRITICAL RATIO FINE SWEEP")
    print("=" * 72)
    print(f"widths: {widths}")
    print(f"slit_half_seps: {slit_halves}")
    print(f"test_positions: y = {test_ys}")
    print()

    # Collect: for each (width, slit_half, y), is V > 0?
    results = []

    for w in widths:
        for sh in slit_halves:
            if sh >= height:
                continue
            barrier_x = w // 2
            if barrier_x < 2:
                continue
            slit_ys_set = {-sh, sh}
            ratio = w / (2 * sh)

            vis_row = {"width": w, "slit_half": sh, "ratio": ratio}
            for y in test_ys:
                if y > height:
                    vis_row[f"V_{y}"] = None
                    continue
                probs = []
                for phase in phases:
                    dist = parameterized_two_slit_distribution(
                        screen_positions=[y],
                        record_created=False,
                        width=w, height=height,
                        barrier_x=barrier_x, slit_ys=slit_ys_set,
                        phase_shift_upper=phase, normalize=False,
                    )
                    probs.append(dist[y])
                vis_row[f"V_{y}"] = visibility(probs)
            results.append(vis_row)

            v_strs = "  ".join(
                f"V(y={y})={vis_row[f'V_{y}']:.6f}" if vis_row[f"V_{y}"] is not None else f"V(y={y})=N/A"
                for y in test_ys
            )
            print(f"w={w:3d} sh={sh:2d} R={ratio:5.2f}  {v_strs}")

    # Threshold analysis: for each y, find the critical ratio
    print()
    print("=" * 72)
    print("THRESHOLD ANALYSIS: first nonzero V by ratio")
    print("=" * 72)
    print()

    for y in test_ys:
        # Group by slit_half, find first width where V > 0
        print(f"--- y = {y} ---")
        for sh in slit_halves:
            rows = [r for r in results if r["slit_half"] == sh and r[f"V_{y}"] is not None]
            rows.sort(key=lambda r: r["width"])
            first_nz = None
            last_zero = None
            for r in rows:
                if r[f"V_{y}"] == 0.0:
                    last_zero = r
                elif first_nz is None:
                    first_nz = r
            if first_nz and last_zero:
                print(f"  slit_half={sh:2d}: last_zero w={last_zero['width']:3d} R={last_zero['ratio']:.2f}"
                      f"  first_nz w={first_nz['width']:3d} R={first_nz['ratio']:.2f}"
                      f"  V_jump={first_nz[f'V_{y}']:.6f}")
            elif first_nz:
                print(f"  slit_half={sh:2d}: always nonzero from w={first_nz['width']:3d} R={first_nz['ratio']:.2f}")
            else:
                print(f"  slit_half={sh:2d}: always zero in tested range")
        print()

    # Summary: is the transition sharp?
    print("=" * 72)
    print("TRANSITION SHARPNESS: V value at first nonzero point")
    print("=" * 72)
    print()
    print(f"{'slit_half':>9s}  {'y':>3s}  {'R_threshold':>11s}  {'V_at_threshold':>14s}  {'sharp?':>6s}")
    print("-" * 52)
    for sh in slit_halves:
        for y in test_ys:
            rows = [r for r in results if r["slit_half"] == sh and r[f"V_{y}"] is not None]
            rows.sort(key=lambda r: r["width"])
            first_nz = None
            for r in rows:
                if r[f"V_{y}"] > 0:
                    first_nz = r
                    break
            if first_nz:
                v = first_nz[f"V_{y}"]
                sharp = "YES" if v > 0.01 else "gradual"
                print(f"{sh:9d}  {y:3d}  {first_nz['ratio']:11.2f}  {v:14.6f}  {sharp:>6s}")

    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
