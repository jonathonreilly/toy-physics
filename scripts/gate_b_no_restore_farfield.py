#!/usr/bin/env python3
"""Gate B no-restore far-field harness.

Bounded companion to gate_b_farfield_harness.py.

Question:
  If we keep the same grown-geometry family but set restore=0, how much of the
  far-field gravity package survives?

This harness freezes only:
- far-field TOWARD fraction
- F~M

The goal is to keep the retained family small and reviewable.
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
PW = 8
SEEDS = list(range(12))
Z_MASSES = [3, 4, 5]
DRIFT_ROWS = [0.0, 0.1, 0.2, 0.3, 0.5]
RESTORE = 0.0


@dataclass
class FarRow:
    drift: float
    toward: int
    total: int
    fm: float


def grow(drift: float, seed: int):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = {}
    nmap: dict[tuple[int, int, int], int] = {}
    layers: list[list[int]] = []

    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    layers.append([0])

    for layer in range(1, NL):
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


def mean_z(pos, det, amps):
    probs = [abs(amps[d]) ** 2 for d in det]
    p = sum(probs)
    if p < 1e-30:
        return float("nan")
    return sum(prob * pos[d][2] for prob, d in zip(probs, det)) / p


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


def slope_loglog(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3:
        return None
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def measure_row(drift: float) -> FarRow:
    toward = 0
    total = 0
    fm_vals: list[float] = []

    for seed in SEEDS:
        pos, adj, layers, nmap = grow(drift, seed)
        det = layers[-1]
        barrier_layer = NL // 3
        gl = 2 * NL // 3
        barrier = layers[barrier_layer]
        sa = [i for i in barrier if pos[i][1] >= 0.5]
        sb = [i for i in barrier if pos[i][1] <= -0.5]
        blocked = set(barrier) - set(sa + sb)
        z_free = mean_z(pos, det, propagate(pos, adj, [0.0] * len(pos), blocked))

        for z_mass in Z_MASSES:
            mi = nmap.get((gl, 0, round(z_mass / H)))
            if mi is None:
                continue
            amps = propagate(pos, adj, make_field(pos, mi, STRENGTH), blocked)
            z_mass_c = mean_z(pos, det, amps)
            if not math.isfinite(z_mass_c) or not math.isfinite(z_free):
                continue
            delta = z_mass_c - z_free
            total += 1
            if delta > 0:
                toward += 1

        mi3 = nmap.get((gl, 0, round(3 / H)))
        if mi3 is not None:
            m_data: list[float] = []
            g_data: list[float] = []
            for s in [1e-6, 1e-5, 5e-5]:
                amps = propagate(pos, adj, make_field(pos, mi3, s), blocked)
                z_s = mean_z(pos, det, amps)
                if math.isfinite(z_s):
                    delta = z_s - z_free
                    if delta > 0:
                        m_data.append(s)
                        g_data.append(delta)
            slope = slope_loglog(m_data, g_data)
            if slope is not None:
                fm_vals.append(slope)

    fm = sum(fm_vals) / len(fm_vals) if fm_vals else float("nan")
    return FarRow(drift=drift, toward=toward, total=total, fm=fm)


def main():
    t0 = time.time()
    print("=" * 72)
    print("GATE B NO-RESTORE FAR-FIELD HARNESS")
    print("  same grown-geometry family, restore=0")
    print("=" * 72)
    print(f"h={H}, W={PW}, L={int((NL - 1) * H)}, seeds={len(SEEDS)}, z={Z_MASSES}, restore={RESTORE}")
    print("growth rule: template previous layer + drift + NN connectivity from grid labels")
    print()
    print(f"{'drift':>6} {'TOWARD':>14} {'F~M':>8}")

    for drift in DRIFT_ROWS:
        row = measure_row(drift)
        pct = row.toward / max(row.total, 1)
        fm_s = f"{row.fm:.2f}" if math.isfinite(row.fm) else "n/a"
        print(f"{drift:6.1f} {row.toward:>5d}/{row.total:<5d} ({pct:>5.0%}) {fm_s:>8}")

    print()
    print("SAFE INTERPRETATION")
    print("  This harness freezes the no-restore far-field comparison only.")
    print("  Use it to bound how much of the far-field package survives when")
    print("  the restoring force is removed from the same grown-geometry family.")
    print(f"\nTotal time: {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
