#!/usr/bin/env python3
"""Targeted distance-law probe for the retained sixth-family sheared basin.

This runner is intentionally narrow:
- start from the retained sixth-family passing rows only
- keep the exact zero/neutral controls implicit by reusing the sheared sweep
- measure whether the near-Newtonian distance tail survives on those rows

The claim surface is small:
- if the tail survives, freeze it as a targeted positive
- if it fails, diagnose the miss against the distance-law breakpoint classifier
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from SIXTH_FAMILY_SHEARED_SWEEP import (  # type: ignore
    DRIFTS,
    SEEDS,
    SOURCE_STRENGTH,
    SOURCE_Z,
    Family,
    _build_sheared_shell_connectivity,
    _centroid_z,
    _field_from_sources,
    _mean,
    _measure_row,
    _propagate,
    grow,
)


DISTANCE_BS = [5, 6, 7, 8, 10]


@dataclass(frozen=True)
class DistanceRow:
    drift: float
    seed: int
    alpha: float
    r2: float
    toward: int
    total: int


def _fit_power(bs: list[float], deltas: list[float]) -> tuple[float, float]:
    pairs = [(b, abs(d)) for b, d in zip(bs, deltas) if b > 0 and abs(d) > 1e-30]
    if len(pairs) < 3:
        return math.nan, math.nan
    lx = [math.log(b) for b, _ in pairs]
    ly = [math.log(d) for _, d in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return math.nan, math.nan
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    alpha = sxy / sxx
    intercept = my - alpha * mx
    ss_res = sum((y - (alpha * x + intercept)) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0
    return alpha, r2


def _measure_distance_row(drift: float, seed: int) -> DistanceRow:
    pos, _adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, _adj)
    sheared = _build_sheared_shell_connectivity(fam)
    det = sheared.layers[-1]
    free = _propagate(sheared.positions, sheared.adj, [0.0] * len(sheared.positions))
    z_free = _centroid_z(free, sheared.positions, det)

    deltas: list[float] = []
    toward = 0
    total = 0
    for b in DISTANCE_BS:
        field = _field_from_sources(
            sheared.positions,
            sheared.layers,
            [(float(b), +1)],
        )
        amps = _propagate(sheared.positions, sheared.adj, field)
        z = _centroid_z(amps, sheared.positions, det)
        delta = z - z_free
        deltas.append(delta)
        total += 1
        if delta > 0:
            toward += 1

    alpha, r2 = _fit_power(DISTANCE_BS, deltas)
    return DistanceRow(
        drift=drift,
        seed=seed,
        alpha=alpha,
        r2=r2,
        toward=toward,
        total=total,
    )


def main() -> int:
    print("=" * 92)
    print("SIXTH FAMILY DISTANCE LAW TARGETED")
    print("  retained sixth-family passing rows only")
    print("=" * 92)
    print(f"drifts={DRIFTS}, seeds={SEEDS}, b={DISTANCE_BS}")
    print("gate: reuse the sixth-family sheared sweep and filter to ok rows only")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'alpha':>8s} {'r2':>7s} {'toward':>9s} {'ok':>4s}")
    print("-" * 92)

    rows: list[DistanceRow] = []
    passing = 0
    total = 0
    for drift in DRIFTS:
        for seed in SEEDS:
            sign_row = _measure_row(drift, seed)
            total += 1
            if not sign_row.ok:
                continue
            passing += 1
            row = _measure_distance_row(drift, seed)
            rows.append(row)
            ok = (
                math.isfinite(row.alpha)
                and row.r2 > 0.90
                and abs(row.alpha + 1.0) < 0.20
                and row.toward == row.total
            )
            print(
                f"{drift:5.2f} {seed:4d} {row.alpha:8.3f} {row.r2:7.3f} "
                f"{row.toward:9d}/{row.total:<3d} {'YES' if ok else 'no':>4s}"
            )

    print()
    print("SAFE READ")
    print(f"  sixth-family passing rows from sign gate: {passing}/{total}")
    if rows:
        alphas = [r.alpha for r in rows if math.isfinite(r.alpha)]
        print(f"  mean alpha across passing rows: {_mean(alphas):.6f}")
        print(f"  alpha spread across passing rows: {max(alphas) - min(alphas):.6f}")
        print(f"  mean toward fraction: {_mean([r.toward / r.total for r in rows]):.6f}")
        print("  if the mean alpha stays near -1, freeze as a targeted positive")
    else:
        print("  no sixth-family row survived the exact sign gate")
        print("  this is a diagnosed failure on the sixth-family basin")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
