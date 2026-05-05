#!/usr/bin/env python3
"""Quick boundary probe for the second grown-family complex-action candidate.

This is the fastest diagnostic: one retained seed, three nearby drifts.
It is meant to answer whether the basin survives immediately off the anchor row.
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

from SECOND_GROWN_FAMILY_COMPLEX import (  # type: ignore
    _born_proxy,
    _build_field,
    _centroid_z,
    _det_prob,
    _propagate,
    SOURCE_STRENGTH,
    SOURCE_STRENGTHS,
    SOURCE_Z,
)
from GATE_B_NONLABEL_SIGN_GROWN_TRANSFER import (  # type: ignore
    Family,
    _build_geometry_sector_grown,
)
from gate_b_no_restore_farfield import grow  # type: ignore


DRIFTS = [0.18, 0.20, 0.22]
SEEDS = [0]


@dataclass(frozen=True)
class RowResult:
    drift: float
    born: float | None
    gamma0_delta: float
    delta_01: float
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


def _measure_row(drift: float) -> RowResult:
    pos, adj, layers, _nmap = grow(drift, 0)
    fam = Family(pos, layers, adj)
    sector = _build_geometry_sector_grown(fam).adj
    det = layers[-1]

    zero = [0.0] * len(pos)
    free = _propagate(pos, sector, zero, 0.0)
    z_free = _centroid_z(free, pos, det)
    p_free = _det_prob(free, det)

    field = _build_field(pos, layers, SOURCE_STRENGTH, SOURCE_Z)
    gamma0 = _propagate(pos, sector, field, 0.0)
    gamma0_delta = _centroid_z(gamma0, pos, det) - z_free

    born = _born_proxy(pos, sector, layers, field, 0.0) if abs(drift - 0.20) < 1e-12 else None

    grav_01 = _propagate(pos, sector, field, 0.1)
    grav_05 = _propagate(pos, sector, field, 0.5)
    delta_01 = _centroid_z(grav_01, pos, det) - z_free
    delta_05 = _centroid_z(grav_05, pos, det) - z_free
    escape_01 = _det_prob(grav_01, det) / p_free if p_free > 1e-30 else 0.0
    escape_05 = _det_prob(grav_05, det) / p_free if p_free > 1e-30 else 0.0

    weak_deltas_0 = []
    weak_deltas_05 = []
    for s in SOURCE_STRENGTHS:
        weak_field = _build_field(pos, layers, s, SOURCE_Z)
        amp0 = _propagate(pos, sector, weak_field, 0.0)
        amp05 = _propagate(pos, sector, weak_field, 0.5)
        weak_deltas_0.append(abs(_centroid_z(amp0, pos, det) - z_free))
        weak_deltas_05.append(abs(_centroid_z(amp05, pos, det) - z_free))

    s1, s2 = SOURCE_STRENGTHS
    fm0 = math.log(weak_deltas_0[1] / weak_deltas_0[0]) / math.log(s2 / s1) if weak_deltas_0[0] > 1e-15 and weak_deltas_0[1] > 1e-15 else None
    fm05 = math.log(weak_deltas_05[1] / weak_deltas_05[0]) / math.log(s2 / s1) if weak_deltas_05[0] > 1e-15 and weak_deltas_05[1] > 1e-15 else None

    return RowResult(
        drift=drift,
        born=born,
        gamma0_delta=gamma0_delta,
        delta_01=delta_01,
        delta_05=delta_05,
        escape_01=escape_01,
        escape_05=escape_05,
        fm_0=fm0,
        fm_05=fm05,
        toward_01=1 if delta_01 > 0 else 0,
        toward_05=1 if delta_05 > 0 else 0,
    )


def main() -> None:
    print("=" * 98)
    print("SECOND GROWN FAMILY COMPLEX QUICK")
    print("  no-restore grown family + geometry-sector stencil")
    print("=" * 98)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print("guards: exact gamma=0 baseline, Born proxy where feasible, TOWARD -> AWAY crossover")
    print()
    print(f"{'drift':>5s} {'born':>10s} {'g0':>12s} {'d01':>12s} {'d05':>12s} {'e01':>8s} {'e05':>8s} {'fm0':>7s} {'fm05':>7s} {'t01':>5s} {'t05':>5s}")
    print("-" * 114)

    rows = [_measure_row(drift) for drift in DRIFTS]
    for row in rows:
        born = f"{row.born:.3e}" if row.born is not None else "   n/a"
        fm0 = f"{row.fm_0:.3f}" if row.fm_0 is not None else "   n/a"
        fm05 = f"{row.fm_05:.3f}" if row.fm_05 is not None else "   n/a"
        print(
            f"{row.drift:5.2f} {born:>10s} {row.gamma0_delta:+12.6e} {row.delta_01:+12.6e} {row.delta_05:+12.6e} "
            f"{row.escape_01:8.3f} {row.escape_05:8.3f} {fm0:>7s} {fm05:>7s} {row.toward_01:5d} {row.toward_05:5d}"
        )

    anchor = next(r for r in rows if abs(r.drift - 0.20) < 1e-12)
    print()
    print("SAFE READ")
    print(f"  anchor retained gamma=0 + Born proxy: {anchor.anchor_ok}")
    print(f"  anchor TOWARD@0.1 -> AWAY@0.5: {anchor.crossover_ok}")
    if anchor.anchor_ok and anchor.crossover_ok:
        print("  this second grown-family candidate carries the complex-action companion narrowly")
    else:
        print("  the second grown-family candidate does not retain the complex-action companion cleanly")


if __name__ == "__main__":
    main()
