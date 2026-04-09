#!/usr/bin/env python3
"""Second independent grown-family signed-source sweep.

This asks whether the old geometry-sector / non-label connectivity idea can
carry the fixed-field signed-source package on a genuinely different grown
family slice: the no-restore Gate B family.

Why this is a second family:
- the current retained grown basin uses restore > 0
- this sweep fixes restore = 0 and varies drift instead
- the connectivity rule is still geometry-sector style, but the family slice is
  structurally different enough to test whether the signed-source package is
  broader than the retained drift/restore neighborhood

The guard rails stay the same:
- exact zero-source baseline
- exact neutral +1/-1 cancellation
- sign orientation
- weak charge-scaling estimate

The claim surface is intentionally narrow: this is a family test, not a
geometry-generic theorem.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.gate_b_nonlabel_connectivity_v1 import (
    Family,
    _build_geometry_sector_connectivity,
    _build_no_restore_family,
)


H = 0.5
NL = 25
HALF = 10
DRIFTS = [0.0, 0.1, 0.2, 0.3, 0.5]
SEEDS = [0, 1, 2]
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
K = 5.0
BETA = 0.8
MIN_EDGES = 5


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
    def ok(self) -> bool:
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


def _measure_family(pos, adj, layers) -> RowResult:
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
    exponent = (
        math.log(abs(double / plus)) / math.log(2.0)
        if abs(plus) > 1e-30 and abs(double) > 1e-30
        else math.nan
    )
    return RowResult(
        drift=float("nan"),
        seed=-1,
        zero=zero,
        plus=plus,
        minus=minus,
        neutral=neutral,
        double=double,
        exponent=exponent,
    )


def main() -> None:
    print("=" * 96)
    print("SECOND GROWN FAMILY SIGN SWEEP")
    print("  question: does the signed-source fixed-field package survive on the")
    print("  independent no-restore grown family with geometry-sector connectivity?")
    print("=" * 96)
    print(f"h={H}, NL={NL}, half={HALF}, drifts={DRIFTS}, seeds={SEEDS}, restore=0")
    print()

    rows: list[RowResult] = []
    for drift in DRIFTS:
        for seed in SEEDS:
            fam = _build_no_restore_family(NL, HALF, drift, seed)
            sector = _build_geometry_sector_connectivity(fam, HALF)
            out = _measure_family(sector.positions, sector.adj, sector.layers)
            rows.append(RowResult(
                drift=drift,
                seed=seed,
                zero=out.zero,
                plus=out.plus,
                minus=out.minus,
                neutral=out.neutral,
                double=out.double,
                exponent=out.exponent,
            ))

    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}")
    print("-" * 96)
    for r in rows:
        print(
            f"{r.drift:5.2f} {r.seed:4d} "
            f"{r.zero:+12.3e} {r.plus:+12.3e} {r.minus:+12.3e} "
            f"{r.neutral:+12.3e} {r.double:+12.3e} {r.exponent:7.3f} "
            f"{'YES' if r.ok else 'no':>4s}"
        )

    passed = [r for r in rows if r.ok]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        drift_vals = sorted({r.drift for r in passed})
        print(f"  drift coverage: {drift_vals}")
        print(f"  mean charge exponent among passes: {_mean([r.exponent for r in passed]):.6f}")
        print("  this is a real second grown-family basin candidate")
    else:
        print("  no second independent grown-family basin survived")
        print("  the signed-source package is still architecture-local to the retained family")


if __name__ == "__main__":
    main()
