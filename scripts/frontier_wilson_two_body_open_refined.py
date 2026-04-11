#!/usr/bin/env python3
"""
Wilson two-body open-lattice refinement sweep.

Goal:
  Extend the open-boundary Wilson two-body distance-law study to larger
  open lattices and test whether the clean non-Newtonian falloff softens
  toward d^-2 or remains stable near the smaller-box d^-3.4 result.

Protocol:
  - reuse the open-boundary two-orbital Wilson harness
  - sweep larger open sides
  - keep only clean attractive rows for the distance-law fit
  - report per-side and global power-law exponents
"""

from __future__ import annotations

import numpy as np

import frontier_wilson_two_body_open as base


def power_law_fit(xs, ys):
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2


def main():
    print("=" * 88)
    print("WILSON TWO-BODY OPEN-LATTICE REFINEMENT SWEEP")
    print("=" * 88)
    print("Surface: open 3D Wilson lattice, G=5, mu2=0.22")
    print("Sides: 11, 13, 15, 17, 19")
    print("Separation window: d=3 up to the largest interior separation on each side")
    print()

    dist_rows = []
    for side in (11, 13, 15, 17, 19):
        max_d = min(9, side // 2)
        for d in range(3, max_d + 1):
            row = base.run_config(side, 5, 0.22, d)
            signal, quality = base.label(row["a_mutual_early_mean"], row["snr"])
            amp = abs(row["a_mutual_early_mean"])
            dist_rows.append((side, d, amp, row["snr"], signal, quality, row))
            print(
                f"side={side:2d} d={d}: "
                f"a_mut={row['a_mutual_early_mean']:+.6f} "
                f"SNR={row['snr']:.2f} [{signal}] [{quality}] "
                f"dsep SH={row['dsep_shared']:+.4f} SELF={row['dsep_self']:+.4f} FREE={row['dsep_free']:+.4f}"
            )

    clean_rows = [(side, d, amp) for side, d, amp, snr, signal, quality, row in dist_rows if signal == "ATTRACT" and quality == "CLEAN"]
    if len(clean_rows) < 2:
        print("\nClean attractive fit unavailable: not enough qualifying rows.")
        return

    slope, intercept, r2 = power_law_fit([d for _, d, _ in clean_rows], [amp for _, _, amp in clean_rows])
    print()
    print(f"Global clean-attract fit: |a_mut| ~ d^{slope:.3f}  (R^2={r2:.4f})")

    for side in (11, 13, 15, 17, 19):
        side_rows = [(d, amp) for s, d, amp in clean_rows if s == side]
        if len(side_rows) >= 2:
            slope_s, _, r2_s = power_law_fit([d for d, _ in side_rows], [amp for _, amp in side_rows])
            print(f"  side={side}: |a_mut| ~ d^{slope_s:.3f}  (R^2={r2_s:.4f})")

    large_rows = [(d, amp) for side, d, amp in clean_rows if side >= 15]
    if len(large_rows) >= 2:
        slope_l, _, r2_l = power_law_fit([d for d, _ in large_rows], [amp for _, amp in large_rows])
        print(f"  sides>=15: |a_mut| ~ d^{slope_l:.3f}  (R^2={r2_l:.4f})")

    print()
    print("Clean rows:")
    for side, d, amp in clean_rows:
        print(f"  side={side:2d} d={d}: |a_mut|={amp:.6f}")


if __name__ == "__main__":
    main()
