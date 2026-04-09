#!/usr/bin/env python3
"""Distance law on wide h^2+T lattice — far-field 1/b test.

The beam has sigma_z ~ 2.7 at the source layer. To measure the 1/b distance
law, we need b >> sigma, so b >= 8. This requires PHYS_W >= 20.

Tests far-field distance exponent convergence as h -> 0.
"""

from __future__ import annotations

import math
import time
import numpy as np

BETA = 0.8
K_PHYS = 5.0
MAX_D_PHYS = 3.0
PHYS_W = 20
PHYS_L = 30
STRENGTH = 0.004
Z_SOURCES = [5, 6, 7, 8, 9, 10, 12, 14, 16]


def _build(h):
    nl = int(PHYS_L / h) + 1
    hw = int(PHYS_W / h)
    max_d = max(1, round(MAX_D_PHYS / h))
    nw = 2 * hw + 1
    npl = nw * nw
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp, dzp = dy * h, dz * h
            L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
            w = math.exp(-BETA * theta * theta)
            offsets.append((dy, dz, L, w * h * h / (L * L)))
    T = sum(wr for _, _, _, wr in offsets)
    return nl, hw, nw, npl, offsets, T


def _propagate(nl, nw, npl, hw, offsets, T, field, k):
    amps = np.zeros((nl, npl), dtype=np.complex128)
    amps[0, hw * nw + hw] = 1.0
    for layer in range(nl - 1):
        sa = amps[layer]
        if np.max(np.abs(sa)) < 1e-300:
            continue
        sf = field[layer]
        df = field[min(layer + 1, nl - 1)]
        for dy, dz, L, w_raw in offsets:
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
            act = L * (1.0 - lf)
            np.add.at(amps[layer + 1], di_m,
                      ai_m * (np.cos(k * act) + 1j * np.sin(k * act)) * w_raw / T)
    return amps


def _centroid_z(a, nw, hw, h):
    p = np.abs(a) ** 2
    t = p.sum()
    if t <= 0:
        return 0.0
    zc = np.array([iz * h for _ in range(-hw, hw + 1) for iz in range(-hw, hw + 1)])
    return float(np.dot(p, zc) / t)


def _build_field(nl, nw, hw, h, s, z_src):
    gl = nl // 3
    iz_s = min(hw, max(-hw, round(z_src / h)))
    sx, sz = gl * h, iz_s * h
    f = np.zeros((nl, nw * nw))
    for layer in range(nl):
        x = layer * h
        idx = 0
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                r = math.sqrt((x - sx) ** 2 + (iy * h) ** 2 + (iz * h - sz) ** 2) + 0.1
                f[layer, idx] = s / r
                idx += 1
    return f


def _fit_power(bs, deltas, b_min=8):
    pairs = [(b, abs(d)) for b, d in zip(bs, deltas) if b >= b_min and abs(d) > 1e-300]
    if len(pairs) < 3:
        return float('nan')
    lx = [math.log(b) for b, _ in pairs]
    ly = [math.log(d) for _, d in pairs]
    mx, my = sum(lx) / len(lx), sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return float('nan')
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def main():
    print("=" * 80)
    print("DISTANCE LAW ON WIDE h^2+T LATTICE — CONTINUUM LIMIT")
    print(f"  W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, far-field b>=8")
    print("=" * 80)
    print()

    spacings = [1.0, 0.5, 0.25]

    for h in spacings:
        t0 = time.time()
        nl, hw, nw, npl, offsets, T = _build(h)
        n = nl * npl
        print(f"h={h:.3f} (nodes={n:,}, T={T:.3f})", flush=True)

        zero = np.zeros((nl, npl))
        free = _propagate(nl, nw, npl, hw, offsets, T, zero, K_PHYS)
        z_free = _centroid_z(free[-1], nw, hw, h)

        bs, deltas = [], []
        for b in Z_SOURCES:
            if b > PHYS_W - 2:
                continue
            field = _build_field(nl, nw, hw, h, STRENGTH, float(b))
            grav = _propagate(nl, nw, npl, hw, offsets, T, field, K_PHYS)
            d = _centroid_z(grav[-1], nw, hw, h) - z_free
            bs.append(b)
            deltas.append(d)
            direction = "TOWARD" if d > 0 else "AWAY"
            print(f"  b={b:3d}: {d:+.6e} {direction}")

        alpha_8 = _fit_power(bs, deltas, 8)
        alpha_6 = _fit_power(bs, deltas, 6)
        dt = time.time() - t0
        print(f"  alpha(b>=8) = {alpha_8:.3f}, alpha(b>=6) = {alpha_6:.3f}  ({dt:.0f}s)")
        print()

    # Summary
    print("DISTANCE EXPONENT CONVERGENCE")
    print(f"  {'h':>5s}  {'alpha(b>=8)':>12s}  {'alpha(b>=6)':>12s}")
    print(f"  {'-' * 33}")
    for h in spacings:
        nl, hw, nw, npl, offsets, T = _build(h)
        zero = np.zeros((nl, npl))
        free = _propagate(nl, nw, npl, hw, offsets, T, zero, K_PHYS)
        z_free = _centroid_z(free[-1], nw, hw, h)
        bs, deltas = [], []
        for b in Z_SOURCES:
            if b > PHYS_W - 2:
                continue
            field = _build_field(nl, nw, hw, h, STRENGTH, float(b))
            grav = _propagate(nl, nw, npl, hw, offsets, T, field, K_PHYS)
            d = _centroid_z(grav[-1], nw, hw, h) - z_free
            bs.append(b)
            deltas.append(d)
        a8 = _fit_power(bs, deltas, 8)
        a6 = _fit_power(bs, deltas, 6)
        print(f"  {h:5.3f}  {a8:12.3f}  {a6:12.3f}")

    print()
    print("SAFE READ")
    print("  alpha = -1.0 is Newtonian 1/b distance law")
    print("  far-field (b>=8) avoids beam-width contamination (sigma~2.7)")
    print("  if alpha -> -1.0 as h -> 0: distance law confirmed in continuum")


if __name__ == "__main__":
    main()
