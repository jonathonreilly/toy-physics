#!/usr/bin/env python3
"""Targeted basin diagnostic for the grown-row non-label signed-source transfer.

Checks the retained drift=0.2 row with nearby restore values to see whether the
geometry-sector transfer has a real local basin or only a single retained point.
"""

from __future__ import annotations

import math
import os
import sys

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
DRIFT = 0.20
RESTORES = [0.60, 0.70, 0.80]
SEED = 0


def _nearest_node_in_layer(pos, layer_nodes, x_target, y_target, z_target):
    best = None
    best_d = float("inf")
    for idx in layer_nodes:
        x, y, z = pos[idx]
        d = (x - x_target) ** 2 + (y - y_target) ** 2 + (z - z_target) ** 2
        if d < best_d:
            best = idx
            best_d = d
    return best


def _field_from_sources(pos, layers, sources):
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


def _propagate(pos, adj, field):
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


def _centroid_z(amps, pos, det):
    total = 0.0
    weighted = 0.0
    for i in det:
        p = abs(amps[i]) ** 2
        total += p
        weighted += p * pos[i][2]
    return weighted / total if total > 1e-30 else 0.0


def _build_geometry_sector_grown(pos, layers):
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


def _measure(pos, adj, layers):
    det = layers[-1]
    free = _propagate(pos, adj, [0.0] * len(pos))
    z_free = _centroid_z(free, pos, det)

    def run(sources):
        field = _field_from_sources(pos, layers, sources)
        amps = _propagate(pos, adj, field)
        return _centroid_z(amps, pos, det) - z_free

    zero = run([])
    plus = run([(SOURCE_Z, +1)])
    minus = run([(SOURCE_Z, -1)])
    neutral = run([(SOURCE_Z, +1), (SOURCE_Z, -1)])
    double = run([(SOURCE_Z, +2)])
    exponent = math.log(abs(double / plus)) / math.log(2.0) if abs(plus) > 1e-30 and abs(double) > 1e-30 else math.nan
    ok = (
        abs(zero) < 1e-12
        and abs(neutral) < 1e-12
        and plus != 0.0
        and minus != 0.0
        and plus * minus < 0.0
        and abs(exponent - 1.0) < 0.05
    )
    return zero, plus, minus, neutral, double, exponent, ok


def main() -> None:
    print("=" * 90)
    print("NON-LABEL GROWN BASIN TARGETED")
    print(f"  drift={DRIFT}, restore values={RESTORES}, seed={SEED}")
    print("=" * 90)
    passed = 0
    for restore in RESTORES:
        pos, adj, layers = grow(DRIFT, restore, SEED)
        sector_adj = _build_geometry_sector_grown(pos, layers)
        zero, plus, minus, neutral, double, exponent, ok = _measure(pos, sector_adj, layers)
        passed += int(ok)
        print(
            f"restore={restore:.2f} | zero={zero:+.3e} plus={plus:+.3e} "
            f"minus={minus:+.3e} neutral={neutral:+.3e} double={double:+.3e} "
            f"exp={exponent:>5.3f} {'YES' if ok else 'no'}"
        )
    print()
    print("SAFE READ")
    print(f"  passed rows: {passed}/{len(RESTORES)}")
    if passed:
        print("  this is a bounded positive basin around the retained row")
    else:
        print("  this is a clean no-go at the nearest restore neighborhood")


if __name__ == "__main__":
    main()
