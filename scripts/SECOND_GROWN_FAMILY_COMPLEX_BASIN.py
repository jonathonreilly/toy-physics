#!/usr/bin/env python3
"""Basin-width probe for the second grown-family complex-action candidate.

This extends the retained anchor-row positive into a wider local scan.

Question:
  Is the no-restore geometry-sector complex-action result a tiny basin or
  just a single retained row?

Guard rails:
  - exact gamma=0 baseline on the anchor row
  - Born proxy where feasible
  - TOWARD -> AWAY crossover on the anchor row
  - weak-field F~M near 1

The claim surface stays narrow: only nearby drifts and a few retained seeds.
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

from SECOND_GROWN_FAMILY_COMPLEX import (  # type: ignore
    _born_proxy,
    _build_field,
    _centroid_z,
    _det_prob,
    _propagate,
    H,
    NL,
    SOURCE_STRENGTH,
    SOURCE_STRENGTHS,
    SOURCE_Z,
)
from GATE_B_NONLABEL_SIGN_GROWN_TRANSFER import (  # type: ignore
    Family,
    _build_geometry_sector_grown,
)
from gate_b_no_restore_farfield import grow  # type: ignore


DRIFTS = [0.10, 0.15, 0.20, 0.25, 0.30]
SEEDS = [0, 1, 2, 3]
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
            and self.fm_0 is not None
            and self.fm_05 is not None
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

        grav_01 = _propagate(pos, sector, field, 0.1)
        grav_05 = _propagate(pos, sector, field, 0.5)
        delta_01 = _centroid_z(grav_01, pos, det) - z_free
        delta_05 = _centroid_z(grav_05, pos, det) - z_free
        delta_02 = _centroid_z(_propagate(pos, sector, field, 0.2), pos, det) - z_free
        delta_01_vals.append(delta_01)
        delta_02_vals.append(delta_02)
        delta_05_vals.append(delta_05)
        if delta_01 > 0:
            toward_01 += 1
        if delta_05 > 0:
            toward_05 += 1

        escape_01_vals.append(_det_prob(grav_01, det) / p_free if p_free > 1e-30 else 0.0)
        escape_05_vals.append(_det_prob(grav_05, det) / p_free if p_free > 1e-30 else 0.0)

        weak_deltas_0 = []
        weak_deltas_05 = []
        for s in SOURCE_STRENGTHS:
            weak_field = _build_field(pos, layers, s, SOURCE_Z)
            amp0 = _propagate(pos, sector, weak_field, 0.0)
            amp05 = _propagate(pos, sector, weak_field, 0.5)
            weak_deltas_0.append(abs(_centroid_z(amp0, pos, det) - z_free))
            weak_deltas_05.append(abs(_centroid_z(amp05, pos, det) - z_free))

        s1, s2 = SOURCE_STRENGTHS
        if weak_deltas_0[0] > 1e-15 and weak_deltas_0[1] > 1e-15:
            fm0_vals.append(math.log(weak_deltas_0[1] / weak_deltas_0[0]) / math.log(s2 / s1))
        if weak_deltas_05[0] > 1e-15 and weak_deltas_05[1] > 1e-15:
            fm05_vals.append(math.log(weak_deltas_05[1] / weak_deltas_05[0]) / math.log(s2 / s1))

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


def main() -> None:
    print("=" * 102)
    print("SECOND GROWN FAMILY COMPLEX BASIN")
    print("  no-restore grown family + geometry-sector stencil")
    print("=" * 102)
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
    print(f"  anchor retained gamma=0 + Born proxy: {anchor.anchor_ok}")
    print(f"  anchor TOWARD@0.1 -> AWAY@0.5: {anchor.crossover_ok}")
    if anchor.anchor_ok and anchor.crossover_ok:
        print("  this second grown-family candidate carries the complex-action companion narrowly")
    else:
        print("  the second grown-family candidate does not retain the complex-action companion cleanly")


if __name__ == "__main__":
    main()
