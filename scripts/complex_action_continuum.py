#!/usr/bin/env python3
"""Complex action on the h^2+T continuum lattice.

Question: Does the gamma sweep (gravity -> horizon transition) survive
as h -> 0? If the exceptional point, escape fraction, and F~M all
converge, complex action is a continuum-level phenomenon.
"""

from __future__ import annotations

import math
import time
import numpy as np

BETA = 0.8
K_PHYS = 5.0
MAX_D_PHYS = 3.0
PHYS_W = 6
PHYS_L = 30
MASS_Z = 3.0
STRENGTH = 0.1
GAMMAS = [0.0, 0.1, 0.2, 0.5, 1.0]


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


def _build_field(nl, nw, hw, h, s, z_src):
    gl = nl // 3
    iz_s = round(z_src / h)
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


def _propagate_complex(nl, nw, npl, hw, offsets, T, field, k, gamma):
    """Complex action: S = L(1-f) + i*gamma*L*f."""
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
            s_real = L * (1.0 - lf)
            s_imag = gamma * L * lf
            phase = k * s_real
            decay = -k * s_imag
            decay_clamped = np.clip(decay, -50, 50)
            amp_factor = np.exp(decay_clamped)
            kernel = ai_m * (np.cos(phase) + 1j * np.sin(phase)) * amp_factor * w_raw / T
            np.add.at(amps[layer + 1], di_m, kernel)
    return amps


def _centroid_z(a, nw, hw, h):
    p = np.abs(a) ** 2
    t = p.sum()
    if t <= 0:
        return 0.0
    zc = np.array([iz * h for _ in range(-hw, hw + 1) for iz in range(-hw, hw + 1)])
    return float(np.dot(p, zc) / t)


def _det_prob(a):
    return float(np.sum(np.abs(a) ** 2))


def main():
    print("=" * 85)
    print("COMPLEX ACTION ON h^2+T CONTINUUM LATTICE")
    print(f"  S = L(1-f) + i*gamma*L*f, kernel normalized by T")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 85)
    print()

    spacings = [1.0, 0.5, 0.25]

    for h in spacings:
        t0 = time.time()
        nl, hw, nw, npl, offsets, T = _build(h)
        n = nl * npl
        print(f"h={h:.3f} (nodes={n:,})", flush=True)

        zero_field = np.zeros((nl, npl))
        field = _build_field(nl, nw, hw, h, STRENGTH, MASS_Z)

        # Free propagation (gamma=0, no field) for reference
        free = _propagate_complex(nl, nw, npl, hw, offsets, T, zero_field, K_PHYS, 0.0)
        z_free = _centroid_z(free[-1], nw, hw, h)
        p_free = _det_prob(free[-1])

        print(f"  {'gamma':>6s} {'deflection':>12s} {'dir':>6s} {'escape':>8s}")
        print(f"  {'-' * 38}")

        for gamma in GAMMAS:
            grav = _propagate_complex(nl, nw, npl, hw, offsets, T, field, K_PHYS, gamma)
            delta = _centroid_z(grav[-1], nw, hw, h) - z_free
            direction = "TOWARD" if delta > 0 else "AWAY"
            p_grav = _det_prob(grav[-1])
            escape = p_grav / p_free if p_free > 0 else 0.0
            print(f"  {gamma:6.2f} {delta:+12.6e} {direction:>6s} {escape:8.4f}")

        # Weak-field F~M at gamma=0 and gamma=0.5
        for gamma in [0.0, 0.5]:
            strengths = [0.001, 0.002, 0.004, 0.008]
            deltas_m = []
            for s in strengths:
                f = _build_field(nl, nw, hw, h, s, MASS_Z)
                a = _propagate_complex(nl, nw, npl, hw, offsets, T, f, K_PHYS, gamma)
                d = _centroid_z(a[-1], nw, hw, h) - z_free
                deltas_m.append(d)
            abs_d = [abs(d) for d in deltas_m]
            lx = [math.log(x) for x in strengths]
            ly = [math.log(y) for y in abs_d if y > 1e-300]
            nn = len(ly)
            if nn >= 3:
                mx = sum(lx[:nn]) / nn
                my = sum(ly) / nn
                sxx = sum((x - mx) ** 2 for x in lx[:nn])
                sxy = sum((x - mx) * (y - my) for x, y in zip(lx[:nn], ly))
                fm = sxy / sxx
            else:
                fm = float('nan')
            print(f"  F~M(gamma={gamma:.1f}) = {fm:.3f}")

        dt = time.time() - t0
        print(f"  ({dt:.0f}s)")
        print()

    print("SAFE READ")
    print("  if TOWARD->AWAY transition exists at all h: continuum phenomenon")
    print("  if escape fraction pattern converges: horizon physics survives")
    print("  if F~M ~ 1.0 at all h for both gamma=0 and gamma=0.5: mass scaling robust")


if __name__ == "__main__":
    main()
