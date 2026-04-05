#!/usr/bin/env python3
"""Distance law on h^2+T lattice across h values.

Question:
  Does gravitational deflection fall as 1/b (b = impact parameter)?
  Does this scaling survive the continuum limit (h -> 0)?

  On a 3D lattice with source at z=z_src, the beam at z=0 has impact
  parameter b = z_src. We measure deflection vs b at multiple h values.

  If deflection ~ 1/b^alpha with alpha -> 1.0 as h -> 0: Newtonian distance law.
"""

from __future__ import annotations

import math
import time
import numpy as np

BETA = 0.8
K_PHYS = 5.0
MAX_D_PHYS = 3.0
PHYS_W = 10   # Wider lattice for distance law (need room for large b)
PHYS_L = 30
STRENGTH = 0.004  # Weak field for clean power law


def _build_offsets(h: float):
    max_d = max(1, round(MAX_D_PHYS / h))
    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp = dy * h
            dzp = dz * h
            L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
            w = math.exp(-BETA * theta * theta)
            w_raw = w * h * h / (L * L)
            offsets.append((dy, dz, L, w, w_raw))
    T = sum(wr for _, _, _, _, wr in offsets)
    kernel_data = [(dy, dz, L, w, w_raw / T) for dy, dz, L, w, w_raw in offsets]
    return kernel_data, T


def _build_field(nl: int, nw: int, hw: int, h: float, s: float, z_src: float):
    gl = nl // 3
    iz_src = round(z_src / h)
    if abs(iz_src) > hw:
        iz_src = min(hw, max(-hw, iz_src))
    sx, sy, sz = gl * h, 0.0, iz_src * h
    field = np.zeros((nl, nw * nw))
    for layer in range(nl):
        x = layer * h
        idx = 0
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                r = math.sqrt((x - sx) ** 2 + (iy * h - sy) ** 2 + (iz * h - sz) ** 2) + 0.1
                field[layer, idx] = s / r
                idx += 1
    return field


def _propagate(nl, nw, npl, hw, kernel_data, field, k):
    amps = np.zeros((nl, npl), dtype=np.complex128)
    center = hw * nw + hw
    amps[0, center] = 1.0

    for layer in range(nl - 1):
        sa = amps[layer]
        if np.max(np.abs(sa)) < 1e-300:
            continue
        sf = field[layer]
        df = field[min(layer + 1, nl - 1)]
        for dy, dz, L, w, w_eff in kernel_data:
            ym_s = max(0, -dy)
            yM_s = min(nw, nw - dy)
            zm_s = max(0, -dz)
            zM_s = min(nw, nw - dz)
            if ym_s >= yM_s or zm_s >= zM_s:
                continue
            yi_grid, zi_grid = np.meshgrid(
                np.arange(ym_s, yM_s), np.arange(zm_s, zM_s), indexing='ij')
            si = yi_grid.ravel() * nw + zi_grid.ravel()
            di = (yi_grid.ravel() + dy) * nw + (zi_grid.ravel() + dz)
            ai = sa[si]
            mask = np.abs(ai) > 1e-300
            if not np.any(mask):
                continue
            si_m, di_m, ai_m = si[mask], di[mask], ai[mask]
            lf = 0.5 * (sf[si_m] + df[di_m])
            act = L * (1.0 - lf)
            phase = k * act
            kernel = ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_eff
            np.add.at(amps[layer + 1], di_m, kernel)
    return amps


def _centroid_z(amps_last, nw, hw, h):
    probs = np.abs(amps_last) ** 2
    total = probs.sum()
    if total <= 0:
        return 0.0
    z_coords = np.zeros(nw * nw)
    idx = 0
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            z_coords[idx] = iz * h
            idx += 1
    return float(np.dot(probs, z_coords) / total)


def _fit_power(bs, deltas):
    """Fit log(|delta|) = alpha * log(b) + const."""
    pairs = [(b, abs(d)) for b, d in zip(bs, deltas) if abs(d) > 1e-300 and b > 0]
    if len(pairs) < 3:
        return float('nan')
    lx = [math.log(b) for b, _ in pairs]
    ly = [math.log(d) for _, d in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return float('nan')
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def main():
    print("=" * 85)
    print("DISTANCE LAW ON h^2+T LATTICE — CONTINUUM LIMIT")
    print(f"  kernel = exp(ikS) * w * h^2 / (L^2 * T)")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}")
    print("=" * 85)
    print()

    spacings = [1.0, 0.5, 0.25]
    z_sources = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

    for h in spacings:
        t0 = time.time()
        nl = int(PHYS_L / h) + 1
        hw = int(PHYS_W / h)
        nw = 2 * hw + 1
        npl = nw * nw
        n = nl * npl
        kernel_data, T = _build_offsets(h)

        zero_field = np.zeros((nl, npl))
        free = _propagate(nl, nw, npl, hw, kernel_data, zero_field, K_PHYS)
        z_free = _centroid_z(free[-1], nw, hw, h)

        print(f"h={h:.3f} (nodes={n}, T={T:.3f})")
        print(f"  {'b':>6s} {'deflection':>12s} {'direction':>10s}")
        print(f"  {'-' * 32}")

        bs = []
        deltas = []
        for z_src in z_sources:
            if z_src > PHYS_W - 1:
                continue
            field = _build_field(nl, nw, hw, h, STRENGTH, z_src)
            grav = _propagate(nl, nw, npl, hw, kernel_data, field, K_PHYS)
            delta = _centroid_z(grav[-1], nw, hw, h) - z_free
            direction = "TOWARD" if delta > 0 else "AWAY"
            print(f"  {z_src:6.1f} {delta:+12.6e} {direction:>10s}")
            bs.append(z_src)
            deltas.append(delta)

        # Fit power law: delta ~ b^alpha
        # Use only b >= 3 (far field)
        far_bs = [b for b in bs if b >= 3]
        far_deltas = [d for b, d in zip(bs, deltas) if b >= 3]
        alpha = _fit_power(far_bs, far_deltas)
        # Also fit all points
        alpha_all = _fit_power(bs, deltas)

        dt = time.time() - t0
        print(f"  far-field (b>=3) alpha = {alpha:.3f}")
        print(f"  all-b alpha = {alpha_all:.3f}")
        print(f"  ({dt:.0f}s)")
        print()

    # Summary table
    print("DISTANCE LAW EXPONENT CONVERGENCE")
    print(f"  {'h':>5s}  {'alpha(b>=3)':>12s}  {'alpha(all)':>12s}")
    print(f"  {'-' * 35}")
    for h in spacings:
        nl = int(PHYS_L / h) + 1
        hw = int(PHYS_W / h)
        nw = 2 * hw + 1
        npl = nw * nw
        kernel_data, T = _build_offsets(h)
        zero_field = np.zeros((nl, npl))
        free = _propagate(nl, nw, npl, hw, kernel_data, zero_field, K_PHYS)
        z_free = _centroid_z(free[-1], nw, hw, h)

        bs_s = []
        deltas_s = []
        for z_src in z_sources:
            if z_src > PHYS_W - 1:
                continue
            field = _build_field(nl, nw, hw, h, STRENGTH, z_src)
            grav = _propagate(nl, nw, npl, hw, kernel_data, field, K_PHYS)
            delta = _centroid_z(grav[-1], nw, hw, h) - z_free
            bs_s.append(z_src)
            deltas_s.append(delta)

        far_bs = [b for b in bs_s if b >= 3]
        far_deltas = [d for b, d in zip(bs_s, deltas_s) if b >= 3]
        alpha_far = _fit_power(far_bs, far_deltas)
        alpha_all = _fit_power(bs_s, deltas_s)
        print(f"  {h:5.3f}  {alpha_far:12.3f}  {alpha_all:12.3f}")

    print()
    print("SAFE READ")
    print("  alpha = -1.0 is Newtonian 1/b distance law")
    print("  alpha should converge toward -1.0 as h -> 0")
    print("  if alpha stabilizes at -1.0: distance law confirmed in continuum")
    print("  if alpha != -1.0: non-Newtonian distance scaling")


if __name__ == "__main__":
    main()
