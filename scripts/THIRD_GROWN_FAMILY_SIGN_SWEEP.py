#!/usr/bin/env python3
"""Third grown-family signed-source sweep.

This tests a genuinely different grown-family slice from the retained
geometry-sector and parity-rotated sector families:

- geometry: no-restore grown slice
- connectivity: cross-quadrant forward matching with local load balancing

The question is narrow:

Can a third independent grown-family slice preserve the signed-source package
under exact zero and neutral controls?

Guard rails:
- exact zero-source baseline
- exact neutral +1/-1 cancellation
- sign orientation
- weak charge-scaling estimate

The claim surface is intentionally small:
- this is a family search, not a geometry-generic theorem
- if it fails, we freeze the failure mechanism rather than broadening the claim
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


H = 0.5
NL = 25
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
K = 5.0
BETA = 0.8
LOAD_ALPHA = 0.02
DRIFTS = [0.0, 0.1, 0.2, 0.3, 0.5]
SEEDS = [0, 1, 2]
QUADRANTS = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]


@dataclass(frozen=True)
class Family:
    positions: list[tuple[float, float, float]]
    layers: list[list[int]]
    adj: dict[int, list[int]]


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
            and self.plus > 0.0
            and self.minus < 0.0
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


def _build_third_connectivity(fam: Family) -> Family:
    """Build a cross-quadrant load-balanced connectivity family.

    This is intentionally different from the sector-transition and sector
    stencil rules already retained on main. Each source selects one candidate
    from each signed quadrant in the y/z plane and then fills any missing slots
    with the nearest remaining nodes, while applying a small target-load
    penalty so the rule is not just a renamed nearest-neighbor graph.
    """

    pos = fam.positions
    layers = fam.layers
    adj: dict[int, list[int]] = {i: [] for i in range(len(pos))}

    for layer in range(len(layers) - 1):
        src_layer = layers[layer]
        dst_layer = layers[layer + 1]
        target_load = {dst: 0 for dst in dst_layer}

        for src in src_layer:
            sx, sy, sz = pos[src]
            quadrant_best: dict[tuple[int, int], tuple[float, int]] = {}
            ranked: list[tuple[float, int]] = []
            for dst in dst_layer:
                dx, dy, dz = pos[dst]
                qy = +1 if (dy - sy) >= 0 else -1
                qz = +1 if (dz - sz) >= 0 else -1
                dist2 = (dx - sx) ** 2 + (dy - sy) ** 2 + (dz - sz) ** 2
                score = dist2 + LOAD_ALPHA * target_load[dst]
                ranked.append((score, dst))
                key = (qy, qz)
                prev = quadrant_best.get(key)
                if prev is None or score < prev[0]:
                    quadrant_best[key] = (score, dst)

            selected = [dst for _, dst in sorted(quadrant_best.values(), key=lambda item: item[0])]
            for _, dst in sorted(ranked, key=lambda item: (item[0], item[1])):
                if len(selected) >= 5:
                    break
                if dst not in selected:
                    selected.append(dst)
            for dst in selected:
                target_load[dst] += 1
            adj[src] = selected

    return Family(pos, layers, adj)


def _measure_row(drift: float, seed: int) -> RowResult:
    pos, _adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, {})
    third = _build_third_connectivity(fam)
    det = third.layers[-1]

    free = _propagate(third.positions, third.adj, [0.0] * len(third.positions))
    z_free = _centroid_z(free, third.positions, det)

    def run(sources: list[tuple[float, int]]) -> float:
        field = _field_from_sources(third.positions, third.layers, sources)
        amps = _propagate(third.positions, third.adj, field)
        return _centroid_z(amps, third.positions, det) - z_free

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
        drift=drift,
        seed=seed,
        zero=zero,
        plus=plus,
        minus=minus,
        neutral=neutral,
        double=double,
        exponent=exponent,
    )


def main() -> None:
    print("=" * 94)
    print("THIRD GROWN FAMILY SIGN SWEEP")
    print("  cross-quadrant load-balanced connectivity on the no-restore grown slice")
    print("=" * 94)
    print(f"h={H}, NL={NL}, drifts={DRIFTS}, seeds={SEEDS}")
    print("guards: exact zero-source baseline, exact neutral +1/-1 cancellation")
    print()
    print(
        f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} "
        f"{'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}"
    )
    print("-" * 94)

    rows: list[RowResult] = []
    for drift in DRIFTS:
        for seed in SEEDS:
            row = _measure_row(drift, seed)
            rows.append(row)
            print(
                f"{drift:5.2f} {seed:4d} "
                f"{row.zero:+12.3e} {row.plus:+12.3e} {row.minus:+12.3e} "
                f"{row.neutral:+12.3e} {row.double:+12.3e} {row.exponent:7.3f} "
                f"{'YES' if row.signed_ok else 'no':>4s}"
            )

    passed = [r for r in rows if r.signed_ok]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        drift_vals = sorted({r.drift for r in passed})
        print(f"  drift coverage: {drift_vals}")
        print(f"  mean exponent among passes: {_mean([r.exponent for r in passed]):.6f}")
        print("  this third grown-family slice has a real bounded basin")
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  this third grown-family slice is a clean no-go on the tested window")


if __name__ == "__main__":
    main()
