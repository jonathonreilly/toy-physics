#!/usr/bin/env python3
"""
Wilson two-body post-selected law characterizations on the open-boundary
surface.

Checks:
  1. distance falloff characterization of the early mutual acceleration
  2. partner-source scaling characterization at fixed separation

Important boundary:
  - the fitted rows are the subset already labeled ATTRACT and CLEAN by the
    audited open-surface runner
  - this script is therefore a bounded calibration/characterization surface,
    not a blind law-estimate theorem runner
"""

from __future__ import annotations

import math

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
    print("WILSON TWO-BODY LAW SWEEPS")
    print("=" * 88)
    print("Surface: open 3D Wilson lattice, G=5, mu2=0.22")
    print("Fit surface: post-selected ATTRACT + CLEAN rows only")
    print()

    # Distance sweep
    print("Distance sweep")
    dist_rows = []
    for side in (11, 13, 15):
        max_d = min(7, side // 2)
        for d in range(3, max_d + 1):
            row = base.run_config(side, 5, 0.22, d)
            signal, quality = base.label(row["a_mutual_early_mean"], row["snr"])
            amp = abs(row["a_mutual_early_mean"])
            dist_rows.append((side, d, amp, row["snr"], signal, quality))
            print(
                f"  side={side:2d} d={d}: "
                f"a_mut={row['a_mutual_early_mean']:+.6f} "
                f"SNR={row['snr']:.2f} [{signal}] [{quality}] "
                f"dsep SH={row['dsep_shared']:+.4f} SELF={row['dsep_self']:+.4f} FREE={row['dsep_free']:+.4f}"
            )

    fit_rows = [(d, amp) for _, d, amp, snr, signal, quality in dist_rows if signal == "ATTRACT" and quality == "CLEAN"]
    slope, intercept, r2 = power_law_fit([d for d, _ in fit_rows], [amp for _, amp in fit_rows])
    print()
    print(
        f"Global post-selected clean-attract characterization: "
        f"|a_mut| ~ d^{slope:.3f}  (R^2={r2:.4f})"
    )

    # Per-side fits
    for side in (11, 13, 15):
        side_rows = [(d, amp) for s, d, amp, snr, signal, quality in dist_rows if s == side and signal == "ATTRACT" and quality == "CLEAN"]
        if len(side_rows) >= 2:
            slope_s, _, r2_s = power_law_fit([d for d, _ in side_rows], [amp for _, amp in side_rows])
            print(
                f"  side={side}: post-selected |a_mut| ~ d^{slope_s:.3f}  "
                f"(R^2={r2_s:.4f})"
            )

    # Mass/source sweep
    print("\nPartner-source sweep  (side=13, d=4)")
    mass_rows = []
    for mass_b in (0.5, 1.0, 1.5, 2.0, 3.0):
        row = base.run_config(13, 5, 0.22, 4, source_mass_a=1.0, source_mass_b=mass_b)
        signal, quality = base.label(row["a_mutual_early_mean"], row["snr"])
        amp = abs(row["a_mutual_early_mean"])
        mass_rows.append((mass_b, amp, row["snr"], signal, quality))
        print(
            f"  mB={mass_b:.1f}: "
            f"a_mut={row['a_mutual_early_mean']:+.6f} "
            f"SNR={row['snr']:.2f} [{signal}] [{quality}] "
            f"dsep SH={row['dsep_shared']:+.4f} SELF={row['dsep_self']:+.4f} FREE={row['dsep_free']:+.4f}"
        )

    slope_m, intercept_m, r2_m = power_law_fit(
        [m for m, amp, snr, signal, quality in mass_rows if signal == "ATTRACT" and quality == "CLEAN"],
        [amp for m, amp, snr, signal, quality in mass_rows if signal == "ATTRACT" and quality == "CLEAN"],
    )
    print()
    print(
        f"Mass characterization at side=13,d=4: |a_mut| ~ mB^{slope_m:.3f}  "
        f"(R^2={r2_m:.4f})"
    )


if __name__ == "__main__":
    main()
