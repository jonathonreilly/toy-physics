#!/usr/bin/env python3
"""Distance law on grown geometry.

Question: does the 1/b distance law transfer from regular lattice to
grown (non-regular) geometry?

Result: alpha = -0.96 (all b, 5-10) — the BEST 1/b measurement in the
project. The irregular node positions smooth out wave-optics oscillations
that steepen the exponent on regular lattices.

Growth rule: template + drift(0.2) + restore(0.7) + NN connectivity.
Source centered at layer NL/2. Three seeds averaged.
"""

from __future__ import annotations
import math
import random
import time

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
H = 0.5
NL = 40
PW = 12
S = 0.004
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0, 1, 2]


def grow(seed):
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(MAX_D_PHYS / H))
    pos = []
    adj = {}
    nmap = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y, z = iy * H, iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, DRIFT * H)
                    z = pz + rng.gauss(0, DRIFT * H)
                    y = y * (1 - RESTORE) + (iy * H) * RESTORE
                    z = z * (1 - RESTORE) + (iz * H) * RESTORE
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap


def make_field(pos, nmap, s, z_src):
    n = len(pos)
    gl = NL // 2
    iz_s = round(z_src / H)
    mi = nmap.get((gl, 0, iz_s))
    if mi is None:
        return [0.0] * n
    mx, my, mz = pos[mi]
    field = [0.0] * n
    for i in range(n):
        r = math.sqrt(
            (pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2
        ) + 0.1
        field[i] = s / r
    return field


def prop(pos, adj, field, k):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
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
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(k * act), math.sin(k * act)) * w * h2 / (L * L)
    return amps


def main():
    hw = int(PW / H)
    npl_approx = (2 * hw + 1) ** 2

    def cz_det(amps, pos):
        det_start = len(pos) - npl_approx
        total = sum(abs(amps[i]) ** 2 for i in range(det_start, len(amps)))
        if total <= 0:
            return 0.0
        return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(det_start, len(amps))) / total

    print("=" * 70)
    print("DISTANCE LAW ON GROWN GEOMETRY")
    print(f"NL={NL}, W={PW}, drift={DRIFT}, restore={RESTORE}, {len(SEEDS)} seeds")
    print("=" * 70)
    print()

    z_sources = [5, 6, 7, 8, 10]
    all_bs = []
    all_deltas = []

    for b in z_sources:
        seed_deltas = []
        for seed in SEEDS:
            pos, adj, nmap = grow(seed)
            field_zero = [0.0] * len(pos)
            free = prop(pos, adj, field_zero, K)
            z_free = cz_det(free, pos)
            field = make_field(pos, nmap, S, float(b))
            grav = prop(pos, adj, field, K)
            delta = cz_det(grav, pos) - z_free
            seed_deltas.append(delta)
        mean_d = sum(seed_deltas) / len(seed_deltas)
        direction = "TOWARD" if mean_d > 0 else "AWAY"
        print(f"b={b}: mean delta = {mean_d:+.6e} {direction}")
        all_bs.append(b)
        all_deltas.append(mean_d)

    # Fit
    pairs = [(b, abs(d)) for b, d in zip(all_bs, all_deltas) if abs(d) > 1e-15]
    if len(pairs) >= 3:
        lx = [math.log(b) for b, _ in pairs]
        ly = [math.log(d) for _, d in pairs]
        mx = sum(lx) / len(lx)
        my = sum(ly) / len(ly)
        sxx = sum((x - mx) ** 2 for x in lx)
        sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
        alpha = sxy / sxx
        print(f"\nalpha (all b): {alpha:.3f}")


if __name__ == "__main__":
    main()
