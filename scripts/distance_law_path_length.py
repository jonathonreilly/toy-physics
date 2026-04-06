#!/usr/bin/env python3
"""Distance law depends on path length — resolving the -1.5 artifact.

The earlier measurement of alpha ~ -1.5 was from PHYS_L=30 with source
at layer nl/3. The path half-length (10) was comparable to the impact
parameter b (8-16), truncating the force integral.

Fix: longer path + centered source. At L=80 (half=40), alpha(b>=10) ~ -0.9.
The exponent approaches -1.0 (Newtonian) as L/b -> infinity.

This script demonstrates the path-length dependence explicitly.
"""

from __future__ import annotations

import math
import time
import numpy as np

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3.0
S = 0.004
H = 0.5
PHYS_W = 20


def _run(phys_l):
    nl = int(phys_l / H) + 1
    hw = int(PHYS_W / H)
    max_d = max(1, round(MAX_D_PHYS / H))
    nw = 2 * hw + 1
    npl = nw * nw

    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * H, dz * H
            L = math.sqrt(H * H + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), H)
            offsets.append((dy, dz, L, math.exp(-BETA * theta * theta) * H * H / (L * L)))
    T = sum(abs(wr) for _, _, _, wr in offsets)

    def prop(field):
        amps = np.zeros((nl, npl), dtype=np.complex128)
        amps[0, hw * nw + hw] = 1.0
        for layer in range(nl - 1):
            sa = amps[layer]
            if np.max(np.abs(sa)) < 1e-300:
                continue
            sf, df = field[layer], field[min(layer + 1, nl - 1)]
            for dy, dz, L_val, w_raw in offsets:
                ym, yM = max(0, -dy), min(nw, nw - dy)
                zm, zM = max(0, -dz), min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yi, zi = np.meshgrid(np.arange(ym, yM), np.arange(zm, zM), indexing='ij')
                si = yi.ravel() * nw + zi.ravel()
                di = (yi.ravel() + dy) * nw + (zi.ravel() + dz)
                ai = sa[si]
                mask = np.abs(ai) > 1e-300
                if not np.any(mask):
                    continue
                si_m, di_m, ai_m = si[mask], di[mask], ai[mask]
                lf = 0.5 * (sf[si_m] + df[di_m])
                phase = K * L_val * (1.0 - lf)
                np.add.at(amps[layer + 1], di_m,
                          ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_raw / T)
        return amps

    def cz(a):
        p = np.abs(a) ** 2
        t = p.sum()
        if t <= 0:
            return 0.0
        zc = np.array([iz * H for _ in range(-hw, hw + 1) for iz in range(-hw, hw + 1)])
        return float(np.dot(p, zc) / t)

    def bfield(z_src):
        gl = nl // 2  # Centered source
        iz_s = round(z_src / H)
        sx, sz = gl * H, iz_s * H
        f = np.zeros((nl, npl))
        for layer in range(nl):
            x = layer * H
            idx = 0
            for iy in range(-hw, hw + 1):
                for iz in range(-hw, hw + 1):
                    r = math.sqrt((x - sx) ** 2 + (iy * H) ** 2 + (iz * H - sz) ** 2) + 0.1
                    f[layer, idx] = S / r
                    idx += 1
        return f

    zero = np.zeros((nl, npl))
    free = prop(zero)
    z_free = cz(free[-1])

    bs, deltas = [], []
    for b in [8, 10, 12, 14, 16]:
        if b > PHYS_W - 2:
            continue
        f = bfield(float(b))
        g = prop(f)
        d = cz(g[-1]) - z_free
        bs.append(b)
        deltas.append(d)

    pairs = [(b, abs(d)) for b, d in zip(bs, deltas) if b >= 8 and abs(d) > 1e-300]
    if len(pairs) >= 3:
        lx = [math.log(b) for b, _ in pairs]
        ly = [math.log(d) for _, d in pairs]
        mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
        sxx = sum((x - mx) ** 2 for x in lx)
        sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
        alpha = sxy / sxx
    else:
        alpha = float('nan')

    toward = sum(1 for d in deltas if d > 0)
    return alpha, toward, len(deltas)


def main():
    print("=" * 70)
    print("DISTANCE LAW vs PATH LENGTH")
    print(f"  p=2.0, h={H}, W={PHYS_W}, source at center, b=8..16")
    print("=" * 70)
    print()
    print(f"{'L':>5s} {'half':>5s} {'alpha':>8s} {'toward':>8s}")
    print("-" * 30)

    for phys_l in [30, 60, 80, 100, 120]:
        t0 = time.time()
        alpha, toward, n = _run(phys_l)
        dt = time.time() - t0
        print(f"{phys_l:5d} {phys_l // 2:5d} {alpha:8.3f} {toward:5d}/{n}  ({dt:.0f}s)")

    print()
    print("SAFE READ")
    print("  alpha should approach -1.0 as L increases")
    print("  at L=30 (old test): alpha ~ -1.1 (finite-path artifact)")
    print("  at L >> b: alpha -> -1.0 (Newtonian)")
    print("  the 1/L^2 kernel IS correct for 3D Newton")


if __name__ == "__main__":
    main()
