#!/usr/bin/env python3
"""Refine the off-center interference threshold.

The coarse sweep suggested a geometry threshold in the width/slit-separation
ratio. A first pass at a simple detector-side reachability law explains most of
the boundary, but the narrow-slit/high-offset corner needs one extra regime.

This script samples even widths densely enough to determine the exact onset law
for off-center visibility on the current rectangular-grid toy.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.interference_geometry_sweep import parameterized_two_slit_distribution
from scripts.interference_offcenter_fringe_sweep import visibility


def offcenter_visibility_by_y(
    width: int,
    slit_half: int,
    screen_ys: list[int],
    *,
    height: int = 10,
    n_phases: int = 24,
) -> dict[int, float]:
    """Return V(y) for a geometry using a shared phase sweep."""

    phase_samples = {y: [] for y in screen_ys}
    phases = [2 * math.pi * i / n_phases for i in range(n_phases)]
    barrier_x = width // 2

    for phase in phases:
        distribution = parameterized_two_slit_distribution(
            screen_positions=screen_ys,
            record_created=False,
            width=width,
            height=height,
            barrier_x=barrier_x,
            slit_ys={-slit_half, slit_half},
            phase_shift_upper=phase,
            normalize=False,
        )
        for y in screen_ys:
            phase_samples[y].append(distribution[y])

    return {y: visibility(samples) for y, samples in phase_samples.items()}


def critical_width(slit_half: int, screen_y: int) -> int:
    """Exact even-width onset for off-center visibility on the sampled grid."""

    return 2 * min(slit_half + abs(screen_y), 2 * slit_half + 1)


def predicted_visibility_onset(width: int, slit_half: int, screen_y: int) -> bool:
    """Two-regime onset law for coherent off-center visibility."""

    return width >= critical_width(slit_half, screen_y)


def main() -> None:
    widths = list(range(4, 33, 2))
    slit_halves = list(range(1, 9))
    screen_ys = [1, 2, 3, 4, 5, 6, 7, 8]
    height = 10
    epsilon = 1e-6

    print("=" * 72)
    print("INTERFERENCE CRITICAL-RATIO SWEEP")
    print("=" * 72)
    print(f"even_widths: {widths}")
    print(f"slit_half_separations: {slit_halves}")
    print(f"screen_positions: {screen_ys}")
    print(f"height: {height}")
    print(f"visibility_epsilon: {epsilon}")
    print()

    rows: list[dict[str, float | int | bool]] = []

    for width in widths:
        for slit_half in slit_halves:
            if slit_half >= height:
                continue

            vis_by_y = offcenter_visibility_by_y(
                width,
                slit_half,
                screen_ys,
                height=height,
            )

            for screen_y in screen_ys:
                vis = vis_by_y[screen_y]
                predicted = predicted_visibility_onset(width, slit_half, screen_y)
                observed = vis > epsilon
                rows.append(
                    {
                        "width": width,
                        "slit_half": slit_half,
                        "slit_sep": 2 * slit_half,
                        "screen_y": screen_y,
                        "visibility": vis,
                        "predicted": predicted,
                        "observed": observed,
                    }
                )

    mismatches = [row for row in rows if row["predicted"] != row["observed"]]

    print("SUMMARY")
    print("-" * 72)
    print(f"sample_count: {len(rows)}")
    print(f"prediction_mismatches: {len(mismatches)}")
    if mismatches:
        print("mismatch_samples:")
        for row in mismatches[:20]:
            print(
                f"  width={row['width']:2d} slit_sep={row['slit_sep']:2d} "
                f"y={row['screen_y']:2d} V={row['visibility']:.6f} "
                f"predicted={int(bool(row['predicted']))} observed={int(bool(row['observed']))}"
            )
    print()

    print("CRITICAL WIDTH TABLE")
    print("-" * 72)
    print(
        f"{'slit_sep':>8s}  {'y':>3s}  {'w_pred':>6s}  {'w_obs':>6s}  "
        f"{'V@w_pred':>10s}  {'ratio_pred':>10s}"
    )
    print("-" * 72)

    for slit_half in slit_halves:
        slit_sep = 2 * slit_half
        for screen_y in screen_ys:
            predicted_width = critical_width(slit_half, screen_y)
            observed_rows = [
                row
                for row in rows
                if row["slit_half"] == slit_half and row["screen_y"] == screen_y and row["observed"]
            ]
            observed_width = min(int(row["width"]) for row in observed_rows)
            onset_row = next(
                row
                for row in rows
                if row["slit_half"] == slit_half
                and row["screen_y"] == screen_y
                and row["width"] == predicted_width
            )
            print(
                f"{slit_sep:8d}  {screen_y:3d}  {predicted_width:6d}  {observed_width:6d}  "
                f"{float(onset_row['visibility']):10.6f}  {predicted_width / slit_sep:10.3f}"
            )
        print()

    print("Y=1 RATIO REINTERPRETATION")
    print("-" * 72)
    print("For the first off-center position, the observed threshold is not universal.")
    print("It is the low-|y| edge of the exact two-regime law, so:")
    print()
    print(f"{'slit_sep':>8s}  {'critical_width':>14s}  {'critical_ratio':>14s}")
    print("-" * 72)
    for slit_half in slit_halves:
        slit_sep = 2 * slit_half
        onset_width = critical_width(slit_half, 1)
        print(f"{slit_sep:8d}  {onset_width:14d}  {onset_width / slit_sep:14.3f}")
    print()

    print("PHYSICAL TRANSLATION")
    print("-" * 72)
    print("The onset splits into two detector-side regimes.")
    print()
    print("1. Straight-transfer regime:")
    print("   while |y| <= slit_half + 1, the onset grows linearly with offset")
    print("   because the visible boundary is still set by direct detector-side reach:")
    print()
    print("     width >= slit_sep + 2|y|")
    print()
    print("2. Zig-zag saturation regime:")
    print("   once |y| exceeds slit_half + 1, narrow-slit sectors can still climb higher")
    print("   through longer causal zig-zag paths after the barrier, so the threshold")
    print("   stops moving and saturates at:")
    print()
    print("     width >= 2*slit_sep + 2")
    print()
    print("Combined exact law for the even-width sweep:")
    print()
    print("  width_crit = min(slit_sep + 2|y|, 2*slit_sep + 2)")
    print()
    print("So the old ratio band is only the y=1 edge of this two-regime boundary, not a")
    print("standalone critical ratio.")
    print()
    print("SWEEP COMPLETE")


if __name__ == "__main__":
    main()
