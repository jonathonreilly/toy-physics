#!/usr/bin/env python3
"""Sixth-family signed-source sweep for a parity-sheared shell connectivity rule.

This is a genuinely different grown-family construction from the retained
sector, quadrant, radial, and load-balanced shells:
- no-restore grown slice
- shell assignment in a layer-dependent sheared y/z coordinate system
- parity flips the shear direction between layers

Guard rails:
- exact zero-source baseline
- exact neutral +1/-1 cancellation
- sign orientation
- weak charge-scaling estimate

The claim surface stays narrow:
- this is a sixth-family scout, not a geometry-generic theorem
- if it fails, the structural miss should be diagnosed instead of softened
"""

from __future__ import annotations

import argparse
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
MIN_EDGES = 5
SHELL_COUNT = 8
SHEAR_MAG = 0.35
DRIFTS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50]
SEEDS = [0, 1, 2]


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


def _shell_metric(
    y: float,
    z: float,
    cy: float,
    cz: float,
    shear: float,
    layer_idx: int,
) -> float:
    dy = y - cy
    dz = z - cz
    sheared_y = dy + shear * dz
    sheared_z = dz - shear * dy
    stretch_y = 1.0 + 0.15 * (layer_idx % 3)
    stretch_z = 1.0 + 0.10 * ((layer_idx + 1) % 3)
    return math.sqrt((sheared_y / max(H * stretch_y, H)) ** 2 + (sheared_z / max(H * stretch_z, H)) ** 2)


def _shell_index(metric: float) -> int:
    shell = int(round(metric * (SHELL_COUNT - 1)))
    return max(0, min(SHELL_COUNT - 1, shell))


def _neighbor_shell(shell: int, layer_idx: int) -> int:
    if layer_idx % 2 == 0:
        return min(SHELL_COUNT - 1, shell + 1)
    return max(0, shell - 1)


def _build_sheared_shell_connectivity(fam: Family) -> Family:
    """Build a parity-sheared shell connectivity family."""

    pos = fam.positions
    layers = fam.layers
    centers = _layer_centers(pos, layers)
    adj: dict[int, list[int]] = {i: [] for i in range(len(pos))}

    for layer_idx in range(len(layers) - 1):
        src_layer = layers[layer_idx]
        dst_layer = layers[layer_idx + 1]
        cy_src, cz_src = centers[layer_idx]
        cy_dst, cz_dst = centers[layer_idx + 1]
        shear = SHEAR_MAG if layer_idx % 2 == 0 else -SHEAR_MAG
        dst_shear = -shear

        dst_by_shell: dict[int, list[int]] = {s: [] for s in range(SHELL_COUNT)}
        for dst in dst_layer:
            metric = _shell_metric(pos[dst][1], pos[dst][2], cy_dst, cz_dst, dst_shear, layer_idx + 1)
            dst_by_shell[_shell_index(metric)].append(dst)

        for src in src_layer:
            metric = _shell_metric(pos[src][1], pos[src][2], cy_src, cz_src, shear, layer_idx)
            shell = _shell_index(metric)
            target_shells = [shell, _neighbor_shell(shell, layer_idx)]

            chosen: list[int] = []
            for target in target_shells:
                candidates = dst_by_shell.get(target, [])
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
                best = min(
                    dst_layer,
                    key=lambda dst: (
                        pos[dst][0] - pos[src][0]
                    ) ** 2
                    + (pos[dst][1] - pos[src][1]) ** 2
                    + (pos[dst][2] - pos[src][2]) ** 2,
                )
                chosen.append(best)

            for dst in sorted(
                dst_layer,
                key=lambda d: (
                    pos[d][0] - pos[src][0]
                ) ** 2
                + (pos[d][1] - pos[src][1]) ** 2
                + (pos[d][2] - pos[src][2]) ** 2,
            ):
                if len(chosen) >= MIN_EDGES:
                    break
                if dst not in chosen:
                    chosen.append(dst)
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


def _measure_row(drift: float, seed: int) -> RowResult:
    pos, _adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, _adj)
    sheared = _build_sheared_shell_connectivity(fam)
    det = sheared.layers[-1]

    free = _propagate(sheared.positions, sheared.adj, [0.0] * len(sheared.positions))
    z_free = _centroid_z(free, sheared.positions, det)

    zero_field = [0.0] * len(sheared.positions)
    zero_amps = _propagate(sheared.positions, sheared.adj, zero_field)
    z_zero = _centroid_z(zero_amps, sheared.positions, det)

    field_plus = _field_from_sources(sheared.positions, sheared.layers, [(SOURCE_Z, +1)])
    field_minus = _field_from_sources(sheared.positions, sheared.layers, [(SOURCE_Z, -1)])
    field_neutral = _field_from_sources(
        sheared.positions, sheared.layers, [(SOURCE_Z, +1), (SOURCE_Z, -1)]
    )
    field_double = _field_from_sources(
        sheared.positions, sheared.layers, [(SOURCE_Z, +1), (SOURCE_Z, +1)]
    )

    plus = _centroid_z(_propagate(sheared.positions, sheared.adj, field_plus), sheared.positions, det) - z_free
    minus = _centroid_z(_propagate(sheared.positions, sheared.adj, field_minus), sheared.positions, det) - z_free
    neutral = _centroid_z(_propagate(sheared.positions, sheared.adj, field_neutral), sheared.positions, det) - z_zero
    double = _centroid_z(_propagate(sheared.positions, sheared.adj, field_double), sheared.positions, det) - z_free

    test_strengths = [5e-6, 5e-5, 1e-4]
    deltas: list[float] = []
    strengths: list[float] = []
    for strength in test_strengths:
        field = [v * (strength / SOURCE_STRENGTH) for v in field_plus]
        z = _centroid_z(_propagate(sheared.positions, sheared.adj, field), sheared.positions, det)
        delta = abs(z - z_free)
        if delta > 1e-15:
            deltas.append(delta)
            strengths.append(strength)
    exponent = math.nan
    if len(deltas) >= 2:
        lx = [math.log(s) for s in strengths]
        ly = [math.log(d) for d in deltas]
        mx = sum(lx) / len(lx)
        my = sum(ly) / len(ly)
        sxx = sum((x - mx) ** 2 for x in lx)
        if sxx > 1e-12:
            exponent = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sxx

    return RowResult(
        drift=drift,
        seed=seed,
        zero=z_zero - z_free,
        plus=plus,
        minus=minus,
        neutral=neutral,
        double=double,
        exponent=exponent,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--drifts", default="0.0,0.05,0.10,0.15,0.20,0.30,0.50")
    parser.add_argument("--seeds", default="0,1,2")
    args = parser.parse_args()
    drifts = [float(v) for v in args.drifts.split(",") if v]
    seeds = [int(v) for v in args.seeds.split(",") if v]

    print("=" * 96)
    print("SIXTH FAMILY SHEARED SWEEP")
    print("  parity-sheared shell connectivity on the no-restore grown slice")
    print("=" * 96)
    print(f"drifts={drifts}, seeds={seeds}")
    print("guards: exact zero-source baseline, exact neutral cancellation, sign orientation")
    print()
    print(f"{'drift':>5s} {'seed':>4s} {'zero':>12s} {'plus':>12s} {'minus':>12s} {'neutral':>12s} {'double':>12s} {'exp':>7s} {'ok':>4s}")
    print("-" * 96)

    rows: list[tuple[float, int, float, float, float, float, float, float, bool]] = []
    for drift in drifts:
        for seed in seeds:
            out = _measure_row(drift, seed)
            rows.append((drift, seed, out.zero, out.plus, out.minus, out.neutral, out.double, out.exponent, out.ok))
            print(
                f"{drift:5.2f} {seed:4d} "
                f"{out.zero:+12.3e} {out.plus:+12.3e} {out.minus:+12.3e} "
                f"{out.neutral:+12.3e} {out.double:+12.3e} {out.exponent:7.3f} "
                f"{'YES' if out.ok else 'no':>4s}"
            )

    passed = [r for r in rows if r[-1]]
    print()
    print("SAFE READ")
    print(f"  passed rows: {len(passed)}/{len(rows)}")
    if passed:
        drift_vals = sorted({r[0] for r in passed})
        print(f"  drift coverage: {drift_vals}")
        print(f"  mean exponent among passes: {_mean([r[7] for r in passed]):.6f}")
        print("  this sheared-shell family is a real sixth-family basin on the sampled rows")
    else:
        print("  no row survived the exact zero/neutral gate")
        print("  the sheared-shell rule is a diagnosed failure on this slice")


if __name__ == "__main__":
    main()
