#!/usr/bin/env python3
"""Gate B grown-geometry distance-law transfer harness.

Freezes the bounded distance-law comparison between:
- exact grid geometry
- grown geometry with the retained moderate-drift row

This is a companion to gate_b_farfield_harness.py, which already freezes the
far-field sign/F~M result. The goal here is narrower: check whether the
distance-tail fit on the grown geometry remains near the fixed-grid value on
the same retained family.
"""

from __future__ import annotations

import cmath
import math
import random
import time
from dataclasses import dataclass


BETA = 0.8
K = 5.0
STRENGTH = 5e-5
MAX_D_PHYS = 3
H = 0.5
NL = 25
PW = 10
SEEDS = list(range(4))
Z_MASSES = [3, 4, 5, 6, 7]
ROWS = [
    ("exact grid", 0.0, 1.0),
    ("grown drift=0.2", 0.2, 0.7),
]


@dataclass
class DistanceRow:
    label: str
    toward: int
    total: int
    slope: float
    r2: float
    peak_z: int


def grow(drift: float, restore: float, seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    nl = NL
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, nl):
        x = layer * H
        nodes: list[int] = []
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y = iy * H
                    z = iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
                nodes.append(idx)
        layers.append(nodes)

        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                edges: list[int] = []
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            edges.append(di)
                adj[si] = adj.get(si, []) + edges

    return pos, adj, layers, nmap


def propagate(pos, adj, field, blocked):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1 - lf)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w * hm / (L * L)
    return amps


def setup_slits(pos, layers):
    bl = NL // 3
    barrier = layers[bl]
    sa = [i for i in barrier if pos[i][1] >= 0.5]
    sb = [i for i in barrier if pos[i][1] <= -0.5]
    blocked = set(barrier) - set(sa + sb)
    return barrier, sa, sb, blocked


def fit_power(b_data, d_data):
    if len(b_data) < 3:
        return None, None
    lx = [math.log(float(v)) for v in b_data]
    ly = [math.log(float(v)) for v in d_data]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None, None
    slope = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / sxx
    ss_res = sum((y - (my + slope * (x - mx))) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return slope, r2


def make_field(pos, mass_idx, strength):
    field = [0.0] * len(pos)
    mx, my, mz = pos[mass_idx]
    for i in range(len(pos)):
        r = math.sqrt(
            (pos[i][0] - mx) ** 2
            + (pos[i][1] - my) ** 2
            + (pos[i][2] - mz) ** 2
        ) + 0.1
        field[i] = strength / r
    return field


def mean_z(pos, det, amps):
    probs = [abs(amps[d]) ** 2 for d in det]
    p = sum(probs)
    if p < 1e-30:
        return float("nan")
    return sum(prob * pos[d][2] for prob, d in zip(probs, det)) / p


def measure_row(label: str, drift: float, restore: float) -> tuple[DistanceRow, dict[int, float]]:
    total = 0
    toward = 0
    z_to_deltas = {z: [] for z in Z_MASSES}

    for seed in SEEDS:
        pos, adj, layers, nmap = grow(drift, restore, seed)
        det = layers[-1]
        _, _, _, blocked = setup_slits(pos, layers)

        free = propagate(pos, adj, [0.0] * len(pos), blocked)
        z_free = mean_z(pos, det, free)

        gl = 2 * NL // 3
        for z_mass in Z_MASSES:
            iz_m = round(z_mass / H)
            mi = nmap.get((gl, 0, iz_m))
            if mi is None:
                continue
            amps = propagate(pos, adj, make_field(pos, mi, STRENGTH), blocked)
            z_mass_c = mean_z(pos, det, amps)
            if not math.isfinite(z_mass_c) or not math.isfinite(z_free):
                continue
            delta = z_mass_c - z_free
            z_to_deltas[z_mass].append(delta)
            total += 1
            if delta > 0:
                toward += 1

    mean_deltas = {z: sum(vals) / len(vals) for z, vals in z_to_deltas.items() if vals}
    b_data = [z for z in Z_MASSES if z in mean_deltas and mean_deltas[z] > 0]
    d_data = [mean_deltas[z] for z in b_data]
    if len(d_data) < 3:
        raise SystemExit(f"not enough positive mean deltas to fit distance law for {label}")
    peak_i = max(range(len(d_data)), key=lambda i: d_data[i])
    slope, r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
    if slope is None or r2 is None:
        raise SystemExit(f"distance fit failed for {label}")
    return DistanceRow(label=label, toward=toward, total=total, slope=slope, r2=r2, peak_z=b_data[peak_i]), mean_deltas


def main():
    t0 = time.time()
    print("=" * 72)
    print("GATE B GROWN-GEOMETRY DISTANCE-LAW HARNESS")
    print("  exact grid vs grown geometry on the retained h=0.5 family")
    print("=" * 72)
    print(f"h={H}, W={PW}, L={int((NL - 1) * H)}, seeds={len(SEEDS)}, z={Z_MASSES[0]}..{Z_MASSES[-1]}")
    print("growth rule: template + drift + restore + NN connectivity from grid labels")
    print()

    rows = []
    all_deltas = {}
    for label, drift, restore in ROWS:
        row, deltas = measure_row(label, drift, restore)
        rows.append(row)
        all_deltas[label] = deltas
        print(
            f"{label:18s}  {row.toward:>2d}/{row.total:<2d} TOWARD  "
            f"tail=b^({row.slope:.2f})  R^2={row.r2:.3f}  peak_z={row.peak_z}"
        )
        for z in Z_MASSES:
            if z in deltas:
                print(f"    z={z}: mean delta={deltas[z]:+.8f}")
        print()

    print("SAFE INTERPRETATION")
    print("  This harness freezes the distance-law comparison only.")
    print("  Far-field sign/F~M closure still lives in gate_b_farfield_harness.py.")
    print("  Promote only the bounded exact-vs-grown comparison measured here.")
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
