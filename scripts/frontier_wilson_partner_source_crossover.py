#!/usr/bin/env python3
"""
Wilson open-lattice partner-source crossover scan.

Goal:
  test whether the sublinear partner-source scaling seen in the open Wilson
  two-body lane moves toward linear behavior on larger surfaces, at a few
  separations, and in a small-G window.

This script is intentionally narrow:
  - open 3D Wilson lattice
  - SHARED vs SELF_ONLY only
  - early-time mutual acceleration from the separation observable
  - power-law fit |a_mut| ~ m_B^alpha

The question is not whether the channel is attractive (that is already
retained). The question is whether the source exponent alpha approaches 1.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np

import frontier_wilson_two_body_open as base


MU2 = 0.22
SIDES = (13, 15, 17)
G_VALUES = (2.0, 3.0, 5.0)
DISTANCES = (3, 4, 5, 6)
SOURCE_MASSES = (0.5, 1.0, 1.5, 2.0, 3.0)


@dataclass
class FitResult:
    side: int
    G: float
    d: int
    alpha: float
    r2: float
    n_clean: int
    n_total: int
    min_snr: float
    max_snr: float


def power_law_fit(xs, ys):
    lx = np.log(np.asarray(xs, dtype=float))
    ly = np.log(np.asarray(ys, dtype=float))
    slope, intercept = np.polyfit(lx, ly, 1)
    fit = slope * lx + intercept
    ss_res = float(np.sum((ly - fit) ** 2))
    ss_tot = float(np.sum((ly - np.mean(ly)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return slope, intercept, r2


def run_partner_point(lat, side, G_val, d, mass_b):
    center = side // 2
    x_a = center - d // 2
    x_b = center + (d - d // 2)
    center_a = (x_a, center, center)
    center_b = (x_b, center, center)

    sep_shared = lat.run_mode(
        "SHARED",
        G_val,
        MU2,
        center_a,
        center_b,
        source_mass_a=1.0,
        source_mass_b=mass_b,
    )
    sep_self = lat.run_mode(
        "SELF_ONLY",
        G_val,
        MU2,
        center_a,
        center_b,
        source_mass_a=1.0,
        source_mass_b=mass_b,
    )

    a_mut = base.acceleration(sep_shared) - base.acceleration(sep_self)
    early = slice(2, min(11, base.N_STEPS + 1))
    mean = float(np.mean(a_mut[early]))
    std = float(np.std(a_mut[early]))
    snr = abs(mean) / (std + 1e-12)
    return mean, std, snr, float(sep_shared[-1] - sep_shared[0]), float(sep_self[-1] - sep_self[0])


def label(mean, snr):
    signal = "ATTRACT" if mean < -1e-6 else ("REPEL" if mean > 1e-6 else "NULL")
    quality = "CLEAN" if snr > 2.0 else ("MARGINAL" if snr > 1.0 else "NOISY")
    return signal, quality


def main():
    base.N_STEPS = 12
    print("=" * 92)
    print("WILSON OPEN-LATTICE PARTNER-SOURCE CROSSOVER SCAN")
    print("=" * 92)
    print(f"MU2={MU2}")
    print(f"Sides={SIDES}")
    print(f"G window={G_VALUES}")
    print(f"Separations={DISTANCES}")
    print(f"Source masses={SOURCE_MASSES}")
    print()

    all_rows: list[FitResult] = []

    for side in SIDES:
        t_side = time.time()
        lat = base.OpenWilsonLattice(side)
        print(f"--- side={side} ---")

        for G_val in G_VALUES:
            for d in DISTANCES:
                if d >= side - 2:
                    continue
                mass_rows = []
                snrs = []
                for mass_b in SOURCE_MASSES:
                    mean, std, snr, dsep_shared, dsep_self = run_partner_point(lat, side, G_val, d, mass_b)
                    signal, quality = label(mean, snr)
                    if signal == "ATTRACT" and quality == "CLEAN":
                        mass_rows.append((mass_b, abs(mean)))
                    snrs.append(snr)
                    print(
                        f"  G={G_val:.1f} d={d} mB={mass_b:.1f}: "
                        f"a_mut={mean:+.6f} +/- {std:.6f} "
                        f"SNR={snr:.2f} [{signal}] [{quality}] "
                        f"dsep SH={dsep_shared:+.4f} SELF={dsep_self:+.4f}"
                    )

                if len(mass_rows) >= 3:
                    alpha, _, r2 = power_law_fit(
                        [m for m, _ in mass_rows],
                        [amp for _, amp in mass_rows],
                    )
                    fit = FitResult(
                        side=side,
                        G=G_val,
                        d=d,
                        alpha=float(alpha),
                        r2=float(r2),
                        n_clean=len(mass_rows),
                        n_total=len(SOURCE_MASSES),
                        min_snr=float(min(snrs)),
                        max_snr=float(max(snrs)),
                    )
                    all_rows.append(fit)
                    print(
                        f"    fit: |a_mut| ~ mB^{alpha:.3f} (R^2={r2:.4f}) "
                        f"clean={len(mass_rows)}/{len(SOURCE_MASSES)} "
                        f"SNR[min,max]=[{min(snrs):.2f},{max(snrs):.2f}]"
                    )
                else:
                    print(
                        f"    fit: insufficient clean attractive rows "
                        f"({len(mass_rows)}/{len(SOURCE_MASSES)})"
                    )

        elapsed_side = time.time() - t_side
        print(f"side={side} done in {elapsed_side:.1f}s")
        print()

    print("=" * 92)
    print("SUMMARY")
    print("=" * 92)
    if all_rows:
        best = max(all_rows, key=lambda r: r.r2)
        alpha_vals = [r.alpha for r in all_rows]
        print(
            f"best fit: side={best.side} G={best.G:.1f} d={best.d} "
            f"alpha={best.alpha:.3f} R^2={best.r2:.4f} "
            f"clean={best.n_clean}/{best.n_total}"
        )
        print(
            f"alpha range across clean fits: min={min(alpha_vals):.3f}, "
            f"max={max(alpha_vals):.3f}, mean={np.mean(alpha_vals):.3f}"
        )
    else:
        print("No clean attractive fits found.")


if __name__ == "__main__":
    main()
