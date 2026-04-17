#!/usr/bin/env python3
"""Tiny drift basin sweep for the grown-row non-label signed-source transfer.

This script tests whether the geometry-sector / non-label connectivity idea
survives a small drift neighborhood around the retained grown row while keeping
the restore knob fixed near the promoted value.

Guard rails:
  - exact zero-source baseline
  - exact neutral +1/-1 cancellation
  - sign orientation
  - weak charge-scaling estimate

The claim surface is intentionally narrow: this is a drift-basin test, not a
family rebuild or a general transport theorem.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow


H = 0.5
K = 5.0
BETA = 0.8
NL = 25
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
MIN_EDGES = 5

DRIFTS = [0.15, 0.20, 0.25]
RESTORE = 0.70
SEEDS = [0, 1, 2]


@dataclass(frozen=True)
class RowResult:
    drift: float
    seed: int
    zero: float
    plus: float
    minus: float
    neutral: float
    double: float
    exponent: float

    @property
    def signed_ok(self) -> bool:
        return (
            abs(self.zero) < 1e-12
            and abs(self.neutral) < 1e-12
            and self.plus != 0.0
            and self.minus != 0.0
            and self.plus * self.minus < 0.0
            and abs(self.exponent - 1.0) < 0.05
        )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _nearest_node_in_layer(
    pos: list[tuple[float, float, float]],
    layer_nodes: list[int],
    x_target: float,
    y_target: float,
    z_target: float,
) -> int | None:
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _field_from_sources(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    sources: list[tuple[float, int]],
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = NL // 3
    x_target = source_layer * H
    for z_phys, charge in sources:
        node = _nearest_node_in_layer(pos, layers[source_layer], x_target, 0.0, z_phys)
        if node is None:
            continue
        mx, my, mz = pos[node]
        for i, (x, y, z) in enumerate(pos):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += charge * SOURCE_STRENGTH / (r**FIELD_POWER)
    return field


def _propagate(
    pos: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        ai = amps[i]
        if abs(ai) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1.0 + lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += ai * complex(math.cos(K * act), math.sin(K * act)) * w * hm / (L * L)
    return amps


def _centroid_z(
    amps: list[complex],
    pos: list[tuple[float, float, float]],
    det: list[int],
) -> float:
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _build_geometry_sector_grown(pos, layers):
    """Build a position-based sector stencil from the grown row itself."""

    adj: dict[int, list[int]] = {}
    for layer in range(len(layers) - 1):
        dst_nodes = layers[layer + 1]
        dst_pos = [pos[i] for i in dst_nodes]
        for src in layers[layer]:
            sx, sy, sz = pos[src]
            sector_best: dict[tuple[int, int], tuple[float, int]] = {}
            ranked: list[tuple[float, int]] = []
            for dst, (dx, dy, dz) in zip(dst_nodes, dst_pos):
                by = max(-1, min(1, int(round((dy - sy) / H))))
                bz = max(-1, min(1, int(round((dz - sz) / H))))
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                ranked.append((dist2, dst))
                key = (by, bz)
                prev = sector_best.get(key)
                if prev is None or dist2 < prev[0]:
                    sector_best[key] = (dist2, dst)

            selected = [dst for _, dst in sorted(sector_best.values(), key=lambda item: item[0])]
            for _, dst in sorted(ranked, key=lambda item: item[0]):
                if len(selected) >= MIN_EDGES:
                    break
                if dst not in selected:
                    selected.append(dst)
            adj[src] = selected
    return adj


def _measure_family(pos, adj, layers) -> tuple[float, float, float, float, float]:
    det = layers[-1]
    free = _propagate(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)

    def run(sources: list[tuple[float, int]]) -> float:
        field = _field_from_sources(pos, layers, sources)
        amps = _propagate(pos, adj, field)
        return _centroid_z(amps, pos, det) - z_free

    zero = run([])
    plus = run([(SOURCE_Z, +1)])
    minus = run([(SOURCE_Z, -1)])
    neutral = run([(SOURCE_Z, +1), (SOURCE_Z, -1)])
    double = run([(SOURCE_Z, +2)])
    exponent = math.log(abs(double / plus)) / math.log(2.0) if abs(plus) > 1e-30 and abs(double) > 1e-30 else math.nan
    return zero, plus, minus, neutral, double, exponent


def main() -> None:
    print("=" * 90)
    print("NON-LABEL GROWN DRIFT BASIN SWEEP")
    print("  question: does the geometry-sector idea survive a tiny drift basin around")
    print("  the retained grown-row fixed-field signed-source transfer?")
    print("=" * 90)
    print(f"h={H}, NL={NL}, drifts={DRIFTS}, restore={RESTORE}, seeds={SEEDS}")
    print()

    rows: list[RowResult] = []
    for drift in DRIFTS:
        for seed in SEEDS:
            pos, adj, layers = grow(drift, RESTORE, seed)
            sector_adj = _build_geometry_sector_grown(pos, layers)
            zero, plus, minus, neutral, double, exponent = _measure_family(pos, sector_adj, layers)
            rows.append(
                RowResult(
                    drift=drift,
                    seed=seed,
                    zero=zero,
                    plus=plus,
                    minus=minus,
                    neutral=neutral,
                    double=double,
                    exponent=exponent,
                )
            )

    print("drift seed | zero         plus         minus        neutral      double       exp    ok")
    print("-" * 88)
    for row in rows:
        print(
            f"{row.drift:>4.2f}   {row.seed:>2d}  | "
            f"{row.zero:+.3e}  {row.plus:+.3e}  {row.minus:+.3e}  "
            f"{row.neutral:+.3e}  {row.double:+.3e}  {row.exponent:>5.3f}  "
            f"{'YES' if row.signed_ok else 'no'}"
        )

    passed = [r for r in rows if r.signed_ok]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        print("  this is a bounded positive drift basin on the retained grown family")
        print(f"  mean exponent among passes: {_mean([r.exponent for r in passed]):.6f}")
    else:
        print("  this is a clean no-go on the drift neighborhood")


if __name__ == "__main__":
    main()
