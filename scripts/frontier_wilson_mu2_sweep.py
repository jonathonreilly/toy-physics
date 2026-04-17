#!/usr/bin/env python3
"""
Wilson open-lattice distance-law sweep versus mu^2.

Goal:
  Test whether the screened open-surface Wilson exponent changes as the
  screening term is reduced toward the massless limit, using the same
  open-boundary mutual-attraction harness that produced the retained
  non-Newtonian law.

Protocol:
  - open 3D Wilson lattice
  - G fixed at 5.0
  - sweep mu^2 downward
  - distance sweep on sides 11, 13, 15
  - fit only clean attractive rows
"""

from __future__ import annotations

import numpy as np

import frontier_wilson_two_body_open as base


SIDES = (11, 13, 15)
DISTANCES = (3, 4, 5, 6)
MU2_VALUES = (0.22, 0.10, 0.05, 0.01, 0.001, 0.0)
G_VAL = 5.0


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
    print("=" * 92)
    print("WILSON OPEN-LATTICE MU2 DISTANCE SWEEP")
    print("=" * 92)
    print(f"Fixed G={G_VAL}")
    print(f"Sides={SIDES}")
    print(f"Distances={DISTANCES}")
    print(f"MU2 values={MU2_VALUES}")
    print()

    summary = []
    for mu2 in MU2_VALUES:
        print("-" * 92)
        print(f"mu2={mu2}")
        print("-" * 92)
        dist_rows = []
        for side in SIDES:
            max_d = min(max(DISTANCES), side // 2)
            for d in DISTANCES:
                if d > max_d:
                    continue
                row = base.run_config(side, G_VAL, mu2, d)
                signal, quality = base.label(row["a_mutual_early_mean"], row["snr"])
                amp = abs(row["a_mutual_early_mean"])
                dist_rows.append((side, d, amp, row["snr"], signal, quality))
                print(
                    f"  side={side:2d} d={d}: "
                    f"a_mut={row['a_mutual_early_mean']:+.6f} "
                    f"SNR={row['snr']:.2f} [{signal}] [{quality}] "
                    f"dsep SH={row['dsep_shared']:+.4f} SELF={row['dsep_self']:+.4f} FREE={row['dsep_free']:+.4f}"
                )

        clean_rows = [
            (side, d, amp)
            for side, d, amp, snr, signal, quality in dist_rows
            if signal == "ATTRACT" and quality == "CLEAN"
        ]
        if len(clean_rows) >= 2:
            slope, intercept, r2 = power_law_fit(
                [d for _, d, _ in clean_rows],
                [amp for _, _, amp in clean_rows],
            )
            summary.append((mu2, slope, r2, len(clean_rows)))
            print()
            print(f"  clean fit: |a_mut| ~ d^{slope:.3f}  (R^2={r2:.4f})")
            for side in SIDES:
                side_rows = [(d, amp) for s, d, amp in clean_rows if s == side]
                if len(side_rows) >= 2:
                    slope_s, _, r2_s = power_law_fit([d for d, _ in side_rows], [amp for _, amp in side_rows])
                    print(f"    side={side}: |a_mut| ~ d^{slope_s:.3f}  (R^2={r2_s:.4f})")
        else:
            summary.append((mu2, float("nan"), float("nan"), len(clean_rows)))
            print()
            print("  clean fit unavailable: not enough clean attractive rows")
        print()

    print("=" * 92)
    print("MU2 SUMMARY")
    print("=" * 92)
    for mu2, slope, r2, n_clean in summary:
        if np.isnan(slope):
            print(f"mu2={mu2:8.3g}: no clean fit ({n_clean} clean rows)")
        else:
            print(f"mu2={mu2:8.3g}: exponent={slope:.3f}  R^2={r2:.4f}  clean={n_clean}")


if __name__ == "__main__":
    main()
