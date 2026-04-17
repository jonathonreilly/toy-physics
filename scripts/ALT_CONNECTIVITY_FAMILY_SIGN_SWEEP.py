#!/usr/bin/env python3
"""Alternative structured connectivity family sign sweep.

This tests a new sector-style connectivity family on the no-restore grown
geometry slice without reusing the current geometry-sector rule.

Family idea:
- partition each layer into angular sectors in the y/z plane
- connect each node to the next layer through a fixed sector-transition map
- alternate the transition map with layer parity so the rule is structured
  but not a local nearest-neighbor rename

Guard rails:
- exact zero-source baseline
- exact neutral +1/-1 cancellation
- sign orientation
- weak charge-scaling estimate

The claim surface stays narrow:
- this is a connectivity-family test, not a geometry-generic theorem
- if it fails, we freeze the failure mechanism rather than broaden the claim
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
DRIFTS = [0.0, 0.1, 0.2, 0.3, 0.5]
SEEDS = [0, 1, 2]
SOURCE_Z = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_POWER = 1
K = 5.0
BETA = 0.8
SECTOR_COUNT = 8


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
    def ok(self) -> bool:
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


def _layer_centers(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
) -> list[tuple[float, float]]:
    centers = []
    for layer in layers:
        ys = [pos[i][1] for i in layer]
        zs = [pos[i][2] for i in layer]
        centers.append((sum(ys) / len(ys), sum(zs) / len(zs)))
    return centers


def _sector_index(y: float, z: float, cy: float, cz: float) -> int:
    ang = math.atan2(z - cz, y - cy)
    if ang < 0:
        ang += 2 * math.pi
    return int((ang / (2 * math.pi)) * SECTOR_COUNT) % SECTOR_COUNT


def _build_alt_connectivity(fam: Family) -> Family:
    """Build a parity-rotated sector-transition connectivity family."""
    pos = fam.positions
    layers = fam.layers
    centers = _layer_centers(pos, layers)
    adj: dict[int, list[int]] = {i: [] for i in range(len(pos))}

    for layer_idx in range(len(layers) - 1):
        src_layer = layers[layer_idx]
        dst_layer = layers[layer_idx + 1]
        cy_src, cz_src = centers[layer_idx]
        cy_dst, cz_dst = centers[layer_idx + 1]

        dst_by_sector: dict[int, list[int]] = {s: [] for s in range(SECTOR_COUNT)}
        for dst in dst_layer:
            s = _sector_index(pos[dst][1], pos[dst][2], cy_dst, cz_dst)
            dst_by_sector[s].append(dst)

        for src in src_layer:
            sy = _sector_index(pos[src][1], pos[src][2], cy_src, cz_src)
            if layer_idx % 2 == 0:
                target_sectors = [sy, (sy + 1) % SECTOR_COUNT, (sy - 1) % SECTOR_COUNT]
            else:
                target_sectors = [sy, (sy + 2) % SECTOR_COUNT, (sy - 2) % SECTOR_COUNT]

            chosen: list[int] = []
            for sec in target_sectors:
                candidates = dst_by_sector.get(sec, [])
                if not candidates:
                    continue
                best = min(
                    candidates,
                    key=lambda dst: (
                        pos[dst][0] - pos[src][0]
                    ) ** 2
                    + (pos[dst][1] - pos[src][1]) ** 2
                    + (pos[dst][2] - pos[src][2]) ** 2,
                )
                if best not in chosen:
                    chosen.append(best)

            if not chosen:
                # Structured fallback: choose the nearest node on the next layer.
                best = min(
                    dst_layer,
                    key=lambda dst: (
                        pos[dst][0] - pos[src][0]
                    ) ** 2
                    + (pos[dst][1] - pos[src][1]) ** 2
                    + (pos[dst][2] - pos[src][2]) ** 2,
                )
                chosen.append(best)

            adj[src].extend(chosen)

    return Family(pos, layers, adj)


def _field_from_sources(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    sources: list[tuple[float, int]],
) -> list[float]:
    field = [0.0] * len(pos)
    source_layer = NL // 3
    x_target = source_layer * H
    layer_nodes = layers[source_layer]
    for z_phys, charge in sources:
        best = None
        best_d = float("inf")
        for idx in layer_nodes:
            x, y, z = pos[idx]
            d = (x - x_target) ** 2 + y**2 + (z - z_phys) ** 2
            if d < best_d:
                best = idx
                best_d = d
        if best is None:
            continue
        mx, my, mz = pos[best]
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


def _measure_family(pos: list[tuple[float, float, float]], adj: dict[int, list[int]], layers: list[list[int]]) -> RowResult:
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
    print("ALT CONNECTIVITY FAMILY SIGN SWEEP")
    print("  sector-transition family on the no-restore grown slice")
    print("=" * 96)
    print(f"h={H}, NL={NL}, drifts={DRIFTS}, seeds={SEEDS}")
    print("guards: exact zero-source baseline, exact neutral cancellation, sign orientation")
    print()

    rows: list[RowResult] = []
    for drift in DRIFTS:
        for seed in SEEDS:
            pos, adj, layers, _nmap = grow(drift, seed)
            fam = Family(pos, layers, adj)
            alt = _build_alt_connectivity(fam)
            out = _measure_family(alt.positions, alt.adj, alt.layers)
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
        print(f"  mean exponent among passes: {_mean([r.exponent for r in passed]):.6f}")
        print("  this alternative connectivity family is a real bounded positive candidate")
    else:
        print("  no alternative connectivity family row survived the exact zero/neutral gate")
        print("  the structured sector-transition rule is a diagnosed failure on this slice")


if __name__ == "__main__":
    main()
