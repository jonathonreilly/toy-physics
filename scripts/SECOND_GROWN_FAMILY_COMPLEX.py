#!/usr/bin/env python3
"""Complex-action probe on the second grown-family candidate.

This script tests a genuinely different grown family from the retained
drift/restore basin:

- no-restore grown geometry
- geometry-sector stencil connectivity

The question is narrow:

Can this second grown-family candidate also carry the complex-action companion
in a retained sense?

Guard rails:
- exact gamma = 0 reduction on the anchor row
- Born/Born-proxy on the anchor row
- TOWARD -> AWAY crossover
- weak-field F~M near 1

The claim surface stays small:
- drift values around the best no-restore candidate
- seed sweep over the retained family slice
- no family-wide or geometry-generic language
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gate_b_no_restore_farfield import grow
from GATE_B_NONLABEL_SIGN_GROWN_TRANSFER import (
    Family,
    _build_geometry_sector_grown,
)
from complex_action_grown_companion import (
    _born_proxy,
    _build_field,
    _centroid_z,
    _det_prob,
    _propagate,
    H,
    K,
    NL,
    SOURCE_STRENGTH,
    SOURCE_STRENGTHS,
    SOURCE_Z,
)


DRIFTS = [0.15, 0.20, 0.25]
SEEDS = [0, 1, 2]
GAMMAS = [0.0, 0.1, 0.2, 0.5]


@dataclass(frozen=True)
class RowResult:
    drift: float
    born: float | None
    gamma0_delta: float
    delta_01: float
    delta_02: float
    delta_05: float
    escape_01: float
    escape_05: float
    fm_0: float | None
    fm_05: float | None
    toward_01: int
    toward_05: int

    @property
    def anchor_ok(self) -> bool:
        return (
            self.born is not None
            and self.born < 1e-12
            and abs(self.fm_0 - 1.0) < 0.05
            and abs(self.fm_05 - 1.0) < 0.05
        )

    @property
    def crossover_ok(self) -> bool:
        return self.toward_01 > 0 and self.toward_05 == 0


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _measure_row(drift: float) -> RowResult:
    born_vals: list[float] = []
    gamma0_deltas: list[float] = []
    delta_01_vals: list[float] = []
    delta_02_vals: list[float] = []
    delta_05_vals: list[float] = []
    escape_01_vals: list[float] = []
    escape_05_vals: list[float] = []
    fm0_vals: list[float] = []
    fm05_vals: list[float] = []
    toward_01 = 0
    toward_05 = 0

    for seed in SEEDS:
        pos, adj, layers, _nmap = grow(drift, seed)
        fam = Family(pos, layers, adj)
        sector = _build_geometry_sector_grown(fam).adj
        det = layers[-1]

        zero = [0.0] * len(pos)
        free = _propagate(pos, sector, zero, 0.0)
        z_free = _centroid_z(free, pos, det)
        p_free = _det_prob(free, det)

        field = _build_field(pos, layers, SOURCE_STRENGTH, SOURCE_Z)
        gamma0 = _propagate(pos, sector, field, 0.0)
        gamma0_deltas.append(_centroid_z(gamma0, pos, det) - z_free)

        if seed == 0 and abs(drift - 0.20) < 1e-12:
            born_vals.append(_born_proxy(pos, sector, layers, field, 0.0))

        for gamma in [0.1, 0.2, 0.5]:
            grav = _propagate(pos, sector, field, gamma)
            delta = _centroid_z(grav, pos, det) - z_free
            if gamma == 0.1:
                delta_01_vals.append(delta)
                if delta > 0:
                    toward_01 += 1
            elif gamma == 0.2:
                delta_02_vals.append(delta)
            elif gamma == 0.5:
                delta_05_vals.append(delta)
                if delta > 0:
                    toward_05 += 1

        for gamma, esc_bucket, fm_bucket in [(0.0, None, fm0_vals), (0.5, escape_05_vals, fm05_vals)]:
            grav = _propagate(pos, sector, field, gamma)
            if gamma == 0.5:
                escape_05_vals.append(_det_prob(grav, det) / p_free if p_free > 1e-30 else 0.0)
            weak_deltas = []
            for s in SOURCE_STRENGTHS:
                weak_field = _build_field(pos, layers, s, SOURCE_Z)
                amp = _propagate(pos, sector, weak_field, gamma)
                weak_deltas.append(abs(_centroid_z(amp, pos, det) - z_free))
            d1, d2 = weak_deltas
            s1, s2 = SOURCE_STRENGTHS
            if d1 > 1e-15 and d2 > 1e-15:
                fm_bucket.append(math.log(d2 / d1) / math.log(s2 / s1))

        # compute escape ratio for gamma=0.1 from the same free reference
        grav_01 = _propagate(pos, sector, field, 0.1)
        escape_01_vals.append(_det_prob(grav_01, det) / p_free if p_free > 1e-30 else 0.0)

    return RowResult(
        drift=drift,
        born=born_vals[0] if born_vals else None,
        gamma0_delta=_mean(gamma0_deltas),
        delta_01=_mean(delta_01_vals),
        delta_02=_mean(delta_02_vals),
        delta_05=_mean(delta_05_vals),
        escape_01=_mean(escape_01_vals),
        escape_05=_mean(escape_05_vals),
        fm_0=_mean(fm0_vals) if fm0_vals else None,
        fm_05=_mean(fm05_vals) if fm05_vals else None,
        toward_01=toward_01,
        toward_05=toward_05,
    )


def main() -> int:
    print("=" * 98)
    print("SECOND GROWN FAMILY COMPLEX")
    print("  no-restore grown family + geometry-sector stencil")
    print("=" * 98)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print("guards: exact gamma=0 baseline, Born proxy where feasible, TOWARD -> AWAY crossover")
    print()
    print(
        f"{'drift':>5s} {'born':>10s} {'g0':>12s} {'d01':>12s} {'d02':>12s} {'d05':>12s} "
        f"{'e01':>8s} {'e05':>8s} {'fm0':>7s} {'fm05':>7s} {'t01':>5s} {'t05':>5s}"
    )
    print("-" * 118)

    rows: list[RowResult] = []
    for drift in DRIFTS:
        row = _measure_row(drift)
        rows.append(row)
        born = f"{row.born:.3e}" if row.born is not None else "   n/a"
        fm0 = f"{row.fm_0:.3f}" if row.fm_0 is not None else "   n/a"
        fm05 = f"{row.fm_05:.3f}" if row.fm_05 is not None else "   n/a"
        print(
            f"{row.drift:5.2f} {born:>10s} {row.gamma0_delta:+12.6e} "
            f"{row.delta_01:+12.6e} {row.delta_02:+12.6e} {row.delta_05:+12.6e} "
            f"{row.escape_01:8.3f} {row.escape_05:8.3f} {fm0:>7s} {fm05:>7s} "
            f"{row.toward_01:5d} {row.toward_05:5d}"
        )

    print()
    print("SAFE READ")
    anchor = next(r for r in rows if abs(r.drift - 0.20) < 1e-12)
    anchor_ok = anchor.anchor_ok
    crossover_ok = anchor.crossover_ok
    print(f"  anchor retained gamma=0 + Born proxy: {'PASS' if anchor_ok else 'FAIL'}  ({anchor_ok})")
    print(f"  anchor TOWARD@0.1 -> AWAY@0.5: {'PASS' if crossover_ok else 'FAIL'}  ({crossover_ok})")
    if anchor_ok and crossover_ok:
        print("  the retained anchor row carries the complex-action companion narrowly")
        print("OVERALL: PASS")
        return 0
    print("  the second grown-family candidate does not retain the complex-action companion cleanly")
    print("OVERALL: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
