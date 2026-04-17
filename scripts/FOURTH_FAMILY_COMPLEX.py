#!/usr/bin/env python3
"""Complex-action scout for the fourth-family quadrant basin.

This asks whether the retained quadrant-reflection family carries a narrow
complex-action companion on the same grown slice.

Guard rails:
- exact gamma=0 reduction on the anchor row
- Born proxy on a representative anchor row
- TOWARD -> AWAY crossover
- weak-field F~M near 1

The claim surface stays deliberately narrow:
- this is a fourth-family complex scout, not a family-wide theorem
- if it fails, the script should diagnose the structural miss rather than
  flattening it into vague no-go language
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

from gate_b_no_restore_farfield import grow
from FOURTH_FAMILY_QUADRANT_SWEEP import (
    Family,
    _build_quadrant_reflection_connectivity,
    _field_from_sources,
    _mean,
    H,
    K,
    NL,
    SOURCE_STRENGTH,
    SOURCE_Z,
)


DRIFTS = [0.0, 0.20, 0.50]
SEEDS = [0, 1, 2]
GAMMAS = [0.0, 0.1, 0.2, 0.5]
SOURCE_STRENGTHS = [1e-6, 1e-5]


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


def _propagate(pos, adj, field, gamma, sources=None):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    if sources is None:
        amps[0] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 - lf)
            decay = -gamma * L * lf
            damp = math.exp(max(min(decay, 50.0), -50.0))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-0.8 * theta * theta)
            amps[j] += amps[i] * complex(math.cos(K * act), math.sin(K * act)) * damp * w * h2 / (L * L)
    return amps


def _centroid_z(amps, pos, det):
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _det_prob(amps, det):
    return sum(abs(amps[i]) ** 2 for i in det)


def _born_proxy(pos, adj, layers, field, gamma):
    source_layer = layers[1]
    picks = [source_layer[0], source_layer[len(source_layer) // 2], source_layer[-1]]
    det = layers[-1]

    def _p_subset(subset):
        amps = _propagate(pos, adj, field, gamma, sources=[(idx, 1.0 + 0j) for idx in subset])
        return _det_prob(amps, det)

    p123 = _p_subset(picks)
    p12 = _p_subset(picks[:2])
    p13 = _p_subset([picks[0], picks[2]])
    p23 = _p_subset(picks[1:])
    p1 = _p_subset([picks[0]])
    p2 = _p_subset([picks[1]])
    p3 = _p_subset([picks[2]])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    return abs(i3) / max(p123, 1e-30)


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
        quad = _build_quadrant_reflection_connectivity(fam)
        det = quad.layers[-1]

        zero = [0.0] * len(pos)
        free = _propagate(quad.positions, quad.adj, zero, 0.0)
        z_free = _centroid_z(free, quad.positions, det)
        p_free = _det_prob(free, det)

        field = _field_from_sources(quad.positions, quad.layers, [(SOURCE_Z, +1)])
        gamma0 = _propagate(quad.positions, quad.adj, field, 0.0)
        gamma0_deltas.append(_centroid_z(gamma0, quad.positions, det) - z_free)

        if seed == 0 and abs(drift - 0.20) < 1e-12:
            born_vals.append(_born_proxy(quad.positions, quad.adj, quad.layers, field, 0.0))

        for gamma in [0.1, 0.2, 0.5]:
            grav = _propagate(quad.positions, quad.adj, field, gamma)
            delta = _centroid_z(grav, quad.positions, det) - z_free
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
            grav = _propagate(quad.positions, quad.adj, field, gamma)
            if gamma == 0.5:
                escape_05_vals.append(_det_prob(grav, det) / p_free if p_free > 1e-30 else 0.0)
            weak_deltas = []
            for s in SOURCE_STRENGTHS:
                weak_field = _field_from_sources(quad.positions, quad.layers, [(SOURCE_Z, +1)])
                weak_field = [v * (s / SOURCE_STRENGTHS[0]) for v in weak_field]
                amp = _propagate(quad.positions, quad.adj, weak_field, gamma)
                weak_deltas.append(abs(_centroid_z(amp, quad.positions, det) - z_free))
            d1, d2 = weak_deltas
            s1, s2 = SOURCE_STRENGTHS
            if d1 > 1e-15 and d2 > 1e-15:
                fm_bucket.append(math.log(d2 / d1) / math.log(s2 / s1))

        grav_01 = _propagate(quad.positions, quad.adj, field, 0.1)
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


def main() -> None:
    print("=" * 98)
    print("FOURTH FAMILY COMPLEX SCOUT")
    print("  quadrant-reflection grown family + complex-action companion test")
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
    print(f"  anchor retained gamma=0 + Born proxy: {anchor.anchor_ok}")
    print(f"  anchor TOWARD@0.1 -> AWAY@0.5: {anchor.crossover_ok}")
    if anchor.anchor_ok and anchor.crossover_ok:
        print("  the quadrant-reflection family carries a narrow complex-action companion")
    else:
        print("  the quadrant-reflection family does not retain the complex-action companion cleanly")


if __name__ == "__main__":
    main()
