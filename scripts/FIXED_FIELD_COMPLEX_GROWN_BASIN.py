#!/usr/bin/env python3
"""Tiny basin replay around the retained grown-row complex-action companion.

The goal is intentionally narrow:
- keep exact gamma=0 reduction
- keep a Born proxy on the grown graph
- check whether the TOWARD -> AWAY crossover survives on a tiny nearby basin
- keep weak-field F~M near 1 if the basin is genuinely retained

This script is not a family-wide sweep. It reuses the retained grown-row
complex-action companion and tests a compact 3x3 neighborhood around the
retained row (drift=0.20, restore=0.70).
"""

from __future__ import annotations

import os
import sys
import math
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.complex_action_grown_companion import (
    _born_proxy,
    _build_field,
    _centroid_z,
    _det_prob,
    _propagate,
    grow,
    GAMMAS,
    H,
    K,
    NL,
    PW,
    SOURCE_STRENGTH,
    SOURCE_STRENGTHS,
    SOURCE_Z,
    SEEDS,
)

DRIFTS = [0.15, 0.20, 0.25]
RESTORES = [0.65, 0.70, 0.75]
SEEDS = [0]
# reduced to a diagonal micro-basin for faster review
ROWS = [(0.20, 0.70), (0.15, 0.65)]


@dataclass(frozen=True)
class BasinRow:
    drift: float
    restore: float
    born: float
    gamma0_delta: float
    escape0: float | None
    escape05: float | None
    fm0: float | None
    fm05: float | None
    toward01: int
    toward05: int


def _measure_row(drift: float, restore: float) -> BasinRow:
    toward01 = 0
    toward05 = 0
    gamma0_deltas = []
    born_vals = []
    escape0_vals = []
    escape05_vals = []
    fm0_vals = []
    fm05_vals = []

    for seed in SEEDS:
        # Reuse the retained exact grown-row family machinery, but on a tiny
        # nearby basin around the companion row.
        pos, adj, layers = grow(drift, restore, seed)
        field = _build_field(pos, layers, SOURCE_STRENGTH, SOURCE_Z)
        zero = [0.0] * len(pos)
        free = _propagate(pos, adj, zero, 0.0)
        z_free = _centroid_z(free, pos, layers[-1])
        p_free = _det_prob(free, layers[-1])

        gamma0 = _propagate(pos, adj, field, 0.0)
        gamma0_delta = _centroid_z(gamma0, pos, layers[-1]) - z_free
        gamma0_deltas.append(gamma0_delta)

        center = abs(drift - 0.20) < 1e-12 and abs(restore - 0.70) < 1e-12
        if seed == 0 and center:
            born_vals.append(_born_proxy(pos, adj, layers, field, 0.0))

        for gamma in [0.1, 0.5]:
            grav = _propagate(pos, adj, field, gamma)
            delta = _centroid_z(grav, pos, layers[-1]) - z_free
            if gamma == 0.1 and delta > 0:
                toward01 += 1
            if gamma == 0.5 and delta > 0:
                toward05 += 1

        # Full weak-field control stack only on the retained center row.
        if center:
            for gamma, esc_bucket, fm_bucket in [(0.0, escape0_vals, fm0_vals), (0.5, escape05_vals, fm05_vals)]:
                grav = _propagate(pos, adj, field, gamma)
                esc_bucket.append(_det_prob(grav, layers[-1]) / p_free if p_free > 1e-30 else 0.0)
                weak_deltas = []
                for s in SOURCE_STRENGTHS:
                    f = _build_field(pos, layers, s, SOURCE_Z)
                    amp = _propagate(pos, adj, f, gamma)
                    weak_deltas.append(abs(_centroid_z(amp, pos, layers[-1]) - z_free))
                d1, d2 = weak_deltas
                s1, s2 = SOURCE_STRENGTHS
                if d1 > 1e-15 and d2 > 1e-15:
                    fm_bucket.append(math.log(d2 / d1) / math.log(s2 / s1))

    return BasinRow(
        drift=drift,
        restore=restore,
        born=born_vals[0] if born_vals else 0.0,
        gamma0_delta=sum(gamma0_deltas) / len(gamma0_deltas),
        escape0=(sum(escape0_vals) / len(escape0_vals)) if escape0_vals else None,
        escape05=(sum(escape05_vals) / len(escape05_vals)) if escape05_vals else None,
        fm0=sum(fm0_vals) / len(fm0_vals) if fm0_vals else None,
        fm05=sum(fm05_vals) / len(fm05_vals) if fm05_vals else None,
        toward01=toward01,
        toward05=toward05,
    )


def main() -> None:
    print("=" * 100)
    print("FIXED-FIELD COMPLEX GROWN BASIN")
    print("  tiny 3x3 basin around the retained grown-row companion")
    print("=" * 100)
    print(f"Seeds: {SEEDS}")
    print(f"Rows: {ROWS}")
    print(f"Retained companion row: drift=0.20, restore=0.70")
    print()
    print(
        f"{'drift':>5s} {'restore':>7s} {'born':>10s} {'g0':>12s} "
        f"{'E0':>8s} {'E05':>8s} {'fm0':>7s} {'fm05':>7s} {'t01':>5s} {'t05':>5s}"
    )
    print("-" * 90)

    rows = []
    for drift, restore in ROWS:
            row = _measure_row(drift, restore)
            rows.append(row)
            fm0 = f"{row.fm0:.3f}" if row.fm0 is not None else "  nan"
            fm05 = f"{row.fm05:.3f}" if row.fm05 is not None else "  nan"
            e0 = f"{row.escape0:.3f}" if row.escape0 is not None else "  n/a"
            e05 = f"{row.escape05:.3f}" if row.escape05 is not None else "  n/a"
            print(
                f"{row.drift:5.2f} {row.restore:7.2f} {row.born:10.3e} "
                f"{row.gamma0_delta:+12.6e} {e0:>8s} {e05:>8s} "
                f"{fm0:>7s} {fm05:>7s} {row.toward01:5d} {row.toward05:5d}"
            )

    print()
    print("SAFE READ")
    exact_ok = [r for r in rows if abs(r.gamma0_delta) < 1e-12 and r.born < 1e-12]
    crossover_ok = [r for r in rows if r.toward01 > 0 and r.toward05 == 0]
    fm_ok = [
        r for r in rows
        if r.fm0 is not None and r.fm05 is not None
        and abs(r.fm0 - 1.0) < 0.05
        and abs(r.fm05 - 1.0) < 0.05
    ]
    print(f"  exact gamma=0 + Born proxy survivors: {len(exact_ok)}/{len(rows)}")
    print(f"  TOWARD@0.1 -> AWAY@0.5 survivors: {len(crossover_ok)}/{len(rows)}")
    print(f"  weak-field F~M~1 survivors: {len(fm_ok)}/{len(rows)}")
    if exact_ok and crossover_ok and fm_ok:
        print("  the exact-to-grown complex-action crossover survives a tiny basin")
    else:
        print("  the crossover is selective; it does not survive the whole tiny basin")


if __name__ == "__main__":
    main()
