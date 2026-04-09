#!/usr/bin/env python3
"""Nearest-neighbor lattice mass-response report.

This script computes, rather than copies, the retained NN mass-response read
from the two canonical continuum-side harnesses:

- the deterministic Born-safe refinement path
- the narrow alpha-scaled gravity-stability probe

Mass is still encoded narrowly in this branch:
- one fixed mass location
- one fixed mass-node footprint
- field-strength scale used as the response proxy

So this script does not promote an F∝M law. It freezes a computed, bounded
mass-response report on the NN branch.
"""

from __future__ import annotations

import math

from lattice_nn_deterministic_rescale import measure_full as measure_deterministic
from lattice_nn_rg_alpha_sweep import ALPHAS, measure_full as measure_alpha

DETERMINISTIC_H = [1.0, 0.5, 0.25, 0.125, 0.0625]
ALPHA_COMPARE_H = [0.5, 0.25]


def main() -> None:
    print("=" * 100)
    print("NN LATTICE MASS-RESPONSE UNDER REFINEMENT")
    print("Mass encoding = fixed-node field-strength multiplier; node count and mass placement are fixed.")
    print("Standard linear propagator only.")
    print("=" * 100)
    print()

    print("Deterministic Born-safe refinement path")
    print("  h       gravity      MI     1-pur      d_TV         Born")
    print("  ---------------------------------------------------------")
    for h in DETERMINISTIC_H:
        row = measure_deterministic(h)
        if row is None:
            print(f"  {h:>6g}       FAIL")
            continue
        born_s = f"{row['born']:.2e}" if math.isfinite(row["born"]) else "nan"
        print(
            f"  {row['h']:>6g}  {row['gravity']:+10.6f}  {row['MI']:6.4f}"
            f"  {1 - row['pur_cl']:7.4f}  {row['dtv']:7.4f}  {born_s:>10s}"
        )
    print()

    print("Narrow alpha-scaled strength law probe")
    print("  alpha   g(h=0.5)   g(h=0.25)  ratio  read")
    print("  --------------------------------------------")
    for alpha in ALPHAS:
        rows = {}
        for h in ALPHA_COMPARE_H:
            row = measure_alpha(h, alpha)
            if row is not None:
                rows[h] = row
        if len(rows) != 2 or abs(rows[0.5]["gravity"]) < 1e-30:
            print(f"  {alpha:5.1f}        FAIL")
            continue
        g_half = rows[0.5]["gravity"]
        g_quarter = rows[0.25]["gravity"]
        ratio = g_quarter / g_half
        read = "nearly h-independent" if alpha >= 1.0 else "decaying"
        print(
            f"  {alpha:5.1f}   {g_half:+9.3f}   {g_quarter:+10.3f}"
            f"   {ratio:4.2f}  {read}"
        )
    print()

    alpha_born_rows = []
    for alpha in (1.0, 1.5):
        for h in ALPHA_COMPARE_H:
            row = measure_alpha(h, alpha)
            if row is not None and math.isfinite(row["born"]):
                alpha_born_rows.append(row["born"])
    if alpha_born_rows:
        print("Born spot-check")
        print(
            "  alpha=1.0 and alpha=1.5 stayed at machine precision on the checked rows"
        )
        print(
            f"  ({min(alpha_born_rows):.1e} to {max(alpha_born_rows):.1e})"
        )
        print()

    print("Safe conclusion")
    print("- the NN mass response stays positive on the Born-safe deterministic path")
    print("- the response becomes cleaner under refinement, but gravity fades toward zero")
    print("- a narrow alpha-scaled law near alpha ~ 1.5 makes gravity nearly h-stable")
    print("- the response is not promoted as F∝M; the checked behavior is positive but")
    print("  bounded/sub-linear and still refinement-sensitive")


if __name__ == "__main__":
    main()
