#!/usr/bin/env python3
"""Compact row-table verdict for the grown-row complex-action basin.

This V2 is intentionally narrower than the first basin draft:
- center row plus one immediate neighbor
- exact gamma=0 reduction on the center row
- Born proxy on the center row
- crossover survival in the nearby row
- weak-field F~M where measured

The goal is to get an actual row-table verdict without broadening the claim
surface beyond the retained grown-row neighborhood.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys
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
    H,
    K,
    NL,
    SOURCE_STRENGTH,
    SOURCE_STRENGTHS,
    SOURCE_Z,
)


CENTER = (0.20, 0.70)
ROWS = [
    CENTER,
    (0.20, 0.60),
]
SEEDS = [0]


@dataclass(frozen=True)
class RowResult:
    drift: float
    restore: float
    center: bool
    born: float | None
    gamma0_delta: float
    escape0: float
    escape05: float
    fm0: float | None
    fm05: float | None
    toward01: int
    toward05: int


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _measure_row(drift: float, restore: float) -> RowResult:
    toward01 = 0
    toward05 = 0
    gamma0_deltas: list[float] = []
    born_vals: list[float] = []
    escape0_vals: list[float] = []
    escape05_vals: list[float] = []
    fm0_vals: list[float] = []
    fm05_vals: list[float] = []

    for seed in SEEDS:
        pos, adj, layers = grow(drift, restore, seed)
        field = _build_field(pos, layers, SOURCE_STRENGTH, SOURCE_Z)
        det = layers[-1]
        zero = [0.0] * len(pos)
        free = _propagate(pos, adj, zero, 0.0)
        z_free = _centroid_z(free, pos, det)
        p_free = _det_prob(free, det)
        center = abs(drift - CENTER[0]) < 1e-12 and abs(restore - CENTER[1]) < 1e-12

        gamma0 = _propagate(pos, adj, field, 0.0)
        gamma0_deltas.append(_centroid_z(gamma0, pos, det) - z_free)

        if seed == 0 and center:
            born_vals.append(_born_proxy(pos, adj, layers, field, 0.0))

        for gamma in [0.1, 0.5]:
            grav = _propagate(pos, adj, field, gamma)
            delta = _centroid_z(grav, pos, det) - z_free
            if gamma == 0.1 and delta > 0:
                toward01 += 1
            if gamma == 0.5 and delta > 0:
                toward05 += 1

        for gamma, esc_bucket, fm_bucket in [
            (0.0, escape0_vals, fm0_vals),
            (0.5, escape05_vals, fm05_vals),
        ]:
            grav = _propagate(pos, adj, field, gamma)
            esc_bucket.append(_det_prob(grav, det) / p_free if p_free > 1e-30 else 0.0)
            weak_deltas = []
            for s in SOURCE_STRENGTHS:
                f = _build_field(pos, layers, s, SOURCE_Z)
                amp = _propagate(pos, adj, f, gamma)
                weak_deltas.append(abs(_centroid_z(amp, pos, det) - z_free))
            d1, d2 = weak_deltas
            s1, s2 = SOURCE_STRENGTHS
            if d1 > 1e-15 and d2 > 1e-15:
                fm_bucket.append(math.log(d2 / d1) / math.log(s2 / s1))

    return RowResult(
        drift=drift,
        restore=restore,
        center=abs(drift - CENTER[0]) < 1e-12 and abs(restore - CENTER[1]) < 1e-12,
        born=born_vals[0] if born_vals else None,
        gamma0_delta=_mean(gamma0_deltas),
        escape0=_mean(escape0_vals),
        escape05=_mean(escape05_vals),
        fm0=_mean(fm0_vals) if fm0_vals else None,
        fm05=_mean(fm05_vals) if fm05_vals else None,
        toward01=toward01,
        toward05=toward05,
    )


def main() -> None:
    print("=" * 96)
    print("FIXED-FIELD COMPLEX GROWN BASIN V2")
    print("  center row plus one immediate neighbor")
    print("=" * 96)
    print(f"Seeds: {SEEDS}")
    print(f"Rows: {ROWS}")
    print(f"Center row: drift={CENTER[0]:.2f}, restore={CENTER[1]:.2f}")
    print()
    print(
        f"{'drift':>5s} {'restore':>7s} {'born':>10s} {'g0':>12s} "
        f"{'E0':>8s} {'E05':>8s} {'fm0':>7s} {'fm05':>7s} {'t01':>5s} {'t05':>5s}"
    )
    print("-" * 94)

    rows: list[RowResult] = []
    for drift, restore in ROWS:
        row = _measure_row(drift, restore)
        rows.append(row)
        born = f"{row.born:.3e}" if row.born is not None else "   n/a"
        fm0 = f"{row.fm0:.3f}" if row.fm0 is not None else "   n/a"
        fm05 = f"{row.fm05:.3f}" if row.fm05 is not None else "   n/a"
        print(
            f"{row.drift:5.2f} {row.restore:7.2f} {born:>10s} "
            f"{row.gamma0_delta:+12.6e} {row.escape0:8.3f} {row.escape05:8.3f} "
            f"{fm0:>7s} {fm05:>7s} {row.toward01:5d} {row.toward05:5d}"
        )

    center_row = next(r for r in rows if r.center)
    neighbor_rows = [r for r in rows if not r.center]

    center_born_ok = center_row.born is not None and center_row.born < 1e-12
    center_fm_ok = (
        center_row.fm0 is not None
        and center_row.fm05 is not None
        and abs(center_row.fm0 - 1.0) < 0.05
        and abs(center_row.fm05 - 1.0) < 0.05
    )
    neighbor_crossover_ok = any(r.toward01 > 0 and r.toward05 == 0 for r in neighbor_rows)
    neighbor_fm_ok = any(
        r.fm0 is not None
        and r.fm05 is not None
        and abs(r.fm0 - 1.0) < 0.05
        and abs(r.fm05 - 1.0) < 0.05
        for r in neighbor_rows
    )

    print()
    print("SAFE READ")
    print(
        "  center exact gamma=0 reduction: retained in the grown-row companion "
        "note"
    )
    print(f"  center Born proxy: {center_born_ok}")
    print(f"  center weak-field F~M~1: {center_fm_ok}")
    print(f"  nearby crossover survives: {neighbor_crossover_ok}")
    print(f"  nearby weak-field F~M~1: {neighbor_fm_ok}")
    if center_born_ok and center_fm_ok and neighbor_crossover_ok and neighbor_fm_ok:
        print("  the exact-to-grown complex-action crossover survives the tiny basin")
    else:
        print("  the crossover is selective; it does not survive the tiny basin cleanly")


if __name__ == "__main__":
    main()
