#!/usr/bin/env python3
"""Targeted complex-action probe for the fifth-family radial-shell slice.

This is the narrow companion check for the retained fifth-family radial basin.
It keeps the exact gamma=0 anchor explicit and only tests the rows that matter
for deciding whether a TOWARD -> AWAY companion is retained or not.
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

from CONNECTIVITY_FAMILY_V2_ELLIPTICAL_SWEEP import (
    Family,
    SOURCE_STRENGTH,
    SOURCE_Z,
    _field_from_sources,
)
from gate_b_no_restore_farfield import grow


DRIFTS = [0.05, 0.20, 0.30]
SEEDS = [0, 1]
SOURCE_STRENGTHS = [5e-5, 1e-4]
SHELL_COUNT = 8


@dataclass(frozen=True)
class RowResult:
    drift: float
    seed: int
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


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _layer_centers(pos, layers):
    centers = []
    for layer in layers:
        ys = [pos[i][1] for i in layer]
        zs = [pos[i][2] for i in layer]
        centers.append((sum(ys) / len(ys), sum(zs) / len(zs)))
    return centers


def _radial_shell(y, z, cy, cz):
    radius = math.sqrt((y - cy) ** 2 + (z - cz) ** 2)
    shell = int(round(radius / 0.5))
    return max(0, min(SHELL_COUNT - 1, shell))


def _neighbor_shell(shell: int, layer_idx: int) -> int:
    if layer_idx % 2 == 0:
        return min(SHELL_COUNT - 1, shell + 1)
    return max(0, shell - 1)


def _build_radial_shell_connectivity(fam: Family) -> Family:
    pos = fam.positions
    layers = fam.layers
    centers = _layer_centers(pos, layers)
    adj = {i: [] for i in range(len(pos))}

    for layer_idx in range(len(layers) - 1):
        src_layer = layers[layer_idx]
        dst_layer = layers[layer_idx + 1]
        cy_src, cz_src = centers[layer_idx]
        cy_dst, cz_dst = centers[layer_idx + 1]
        dst_by_shell = {s: [] for s in range(SHELL_COUNT)}
        for dst in dst_layer:
            shell = _radial_shell(pos[dst][1], pos[dst][2], cy_dst, cz_dst)
            dst_by_shell[shell].append(dst)

        for src in src_layer:
            shell = _radial_shell(pos[src][1], pos[src][2], cy_src, cz_src)
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
                if len(chosen) >= 5:
                    break
                if dst not in chosen:
                    chosen.append(dst)
            adj[src].extend(chosen)
    return Family(pos, layers, adj)


def _propagate(pos, adj, field, gamma):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    h2 = 0.5 * 0.5
    k = 5.0
    beta = 0.8
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
            act = L * (1.0 - lf)
            decay = -gamma * L * lf
            damp = 0.0 if decay < -50 else math.exp(min(decay, 50))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-beta * theta * theta)
            amps[j] += ai * complex(math.cos(k * act), math.sin(k * act)) * damp * w * h2 / (L * L)
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
    det = layers[-1]

    def _p_born(open_slits):
        n = len(pos)
        amps = [0j] * n
        source_layer = layers[0]
        for slit in open_slits:
            if slit < len(source_layer):
                amps[source_layer[slit]] = 1.0
        order = sorted(range(n), key=lambda i: pos[i][0])
        h2 = 0.5 * 0.5
        k = 5.0
        beta = 0.8
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
                act = L * (1.0 - lf)
                decay = -gamma * L * lf
                damp = 0.0 if decay < -50 else math.exp(min(decay, 50))
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-beta * theta * theta)
                amps[j] += ai * complex(math.cos(k * act), math.sin(k * act)) * damp * w * h2 / (L * L)
        return _det_prob(amps, det)

    p123 = _p_born([0, 1, 2])
    p12 = _p_born([0, 1])
    p13 = _p_born([0, 2])
    p23 = _p_born([1, 2])
    p1 = _p_born([0])
    p2 = _p_born([1])
    p3 = _p_born([2])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    return abs(i3) / max(p123, 1e-300)


def _measure_row(drift: float, seed: int) -> RowResult:
    pos, adj, layers, _nmap = grow(drift, seed)
    fam = Family(pos, layers, adj)
    radial = _build_radial_shell_connectivity(fam)
    det = radial.layers[-1]
    free = _propagate(radial.positions, radial.adj, [0.0] * len(radial.positions), 0.0)
    z_free = _centroid_z(free, radial.positions, det)
    p_free = _det_prob(free, det)

    field = _field_from_sources(radial.positions, radial.layers, [(SOURCE_Z, +1)])
    zero = _centroid_z(_propagate(radial.positions, radial.adj, field, 0.0), radial.positions, det) - z_free
    born = _born_proxy(radial.positions, radial.adj, radial.layers, field, 0.0) if abs(drift - 0.20) < 1e-12 and seed == 0 else None

    grav01 = _propagate(radial.positions, radial.adj, field, 0.1)
    grav05 = _propagate(radial.positions, radial.adj, field, 0.5)
    d01 = _centroid_z(grav01, radial.positions, det) - z_free
    d05 = _centroid_z(grav05, radial.positions, det) - z_free
    e01 = _det_prob(grav01, det) / p_free if p_free > 1e-30 else 0.0
    e05 = _det_prob(grav05, det) / p_free if p_free > 1e-30 else 0.0

    weak = []
    for s in SOURCE_STRENGTHS:
        weak_field = _field_from_sources(radial.positions, radial.layers, [(SOURCE_Z, +1)])
        scale = s / SOURCE_STRENGTH
        weak_field = [v * scale for v in weak_field]
        amp0 = _propagate(radial.positions, radial.adj, weak_field, 0.0)
        amp5 = _propagate(radial.positions, radial.adj, weak_field, 0.5)
        weak.append((_centroid_z(amp0, radial.positions, det) - z_free, _centroid_z(amp5, radial.positions, det) - z_free))
    d1, d2 = weak
    fm0 = math.log(abs(d2[0] / d1[0])) / math.log(2.0) if abs(d1[0]) > 1e-15 and abs(d2[0]) > 1e-15 else math.nan
    fm05 = math.log(abs(d2[1] / d1[1])) / math.log(2.0) if abs(d1[1]) > 1e-15 and abs(d2[1]) > 1e-15 else math.nan

    return RowResult(
        drift=drift,
        seed=seed,
        born=born,
        gamma0_delta=zero,
        delta_01=d01,
        delta_05=d05,
        escape_01=e01,
        escape_05=e05,
        fm_0=fm0,
        fm_05=fm05,
        toward_01=1 if d01 > 0 else 0,
        toward_05=1 if d05 > 0 else 0,
    )


def main() -> None:
    print("=" * 98)
    print("FIFTH FAMILY COMPLEX TARGETED")
    print("  complex-action probe on the radial-shell fifth-family slice")
    print("=" * 98)
    print(f"drifts={DRIFTS}, seeds={SEEDS}")
    print("guards: exact gamma=0 baseline, Born proxy where feasible, TOWARD -> AWAY crossover")
    print()
    print(
        f"{'drift':>5s} {'seed':>4s} {'born':>10s} {'g0':>12s} {'d01':>12s} {'d05':>12s} "
        f"{'e01':>8s} {'e05':>8s} {'fm0':>7s} {'fm05':>7s} {'t01':>5s} {'t05':>5s}"
    )
    print("-" * 118)

    rows: list[RowResult] = []
    for drift in DRIFTS:
        for seed in SEEDS:
            row = _measure_row(drift, seed)
            rows.append(row)
            born = f"{row.born:.3e}" if row.born is not None else "   n/a"
            fm0 = f"{row.fm_0:.3f}" if row.fm_0 is not None else "   n/a"
            fm05 = f"{row.fm_05:.3f}" if row.fm_05 is not None else "   n/a"
            print(
                f"{row.drift:5.2f} {row.seed:4d} {born:>10s} {row.gamma0_delta:+12.6e} "
                f"{row.delta_01:+12.6e} {row.delta_05:+12.6e} {row.escape_01:8.3f} {row.escape_05:8.3f} "
                f"{fm0:>7s} {fm05:>7s} {row.toward_01:5d} {row.toward_05:5d}"
            )

    print()
    print("SAFE READ")
    anchors = [r for r in rows if r.anchor_ok]
    companion = [r for r in rows if r.anchor_ok and r.crossover_ok]
    print(f"  anchor rows passing exact gamma=0 + Born/F~M gates: {len(anchors)}")
    print(f"  anchor rows with TOWARD -> AWAY crossover: {len(companion)}")
    if companion:
        print("  the radial-shell fifth-family slice carries a narrow complex-action companion")
    else:
        print("  the radial-shell slice does not retain the complex-action companion cleanly")


if __name__ == "__main__":
    raise SystemExit(main())
