#!/usr/bin/env python3
"""Numpy-accelerated h^2+T continuum limit test.

Same physics as lattice_h2_T_continuum.py but vectorized with numpy
for ~100x speedup, enabling h=0.125 in minutes instead of hours.

kernel = exp(ikS) * w * h^2 / (L^2 * T)
per-layer norm = 1 for interior nodes
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
            offsets.append((dy, dz, L, w))
    T = sum(w * h * h / (L * L) for _, _, L, w in offsets)
    # Precompute effective weight: w * h^2 / (L^2 * T)
    kernel_data = [(dy, dz, L, w * h * h / (L * L * T)) for dy, dz, L, w in offsets]
    return kernel_data, T


def _build_field(nl: int, nw: int, hw: int, h: float, s: float, z_src: float):
    """Build 1/r field as 2D array [nl, nw*nw]."""
    gl = nl // 3
    iz_src = round(z_src / h)
    sx = gl * h
    sy = 0.0
    sz = iz_src * h
    field = np.zeros((nl, nw * nw))
    for layer in range(nl):
        x = layer * h
        idx = 0
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                y_phys = iy * h
                z_phys = iz * h
                r = math.sqrt((x - sx) ** 2 + (y_phys - sy) ** 2 + (z_phys - sz) ** 2) + 0.1
                field[layer, idx] = s / r
                idx += 1
    return field


def _propagate_np(
    nl: int, nw: int, npl: int, hw: int,
    kernel_data: list, field: np.ndarray, k: float,
    source_indices: list[int] | None = None,
    source_amps: list[complex] | None = None,
) -> np.ndarray:
    """Vectorized propagation with h^2/T kernel."""
    amps = np.zeros((nl, npl), dtype=np.complex128)
    if source_indices is None:
        # Default: source at (0, 0, 0) = center of first layer
        center = hw * nw + hw
        amps[0, center] = 1.0
    else:
        for idx, amp in zip(source_indices, source_amps):
            amps[0, idx] = amp

    for layer in range(nl - 1):
        sa = amps[layer]
        if np.max(np.abs(sa)) < 1e-300:
            continue
        sf = field[layer]
        df = field[min(layer + 1, nl - 1)]
        for dy, dz, L, w_eff in kernel_data:
            # Source y-range: [ym, yM), source z-range: [zm, zM)
            # Source index: si = yi * nw + zi
            # Dest index: di = (yi + dy) * nw + (zi + dz)
            ym_s = max(0, -dy)
            yM_s = min(nw, nw - dy)
            zm_s = max(0, -dz)
            zM_s = min(nw, nw - dz)
            if ym_s >= yM_s or zm_s >= zM_s:
                continue

            # Build source and dest index arrays
            y_src = np.arange(ym_s, yM_s)
            z_src = np.arange(zm_s, zM_s)
            yi_grid, zi_grid = np.meshgrid(y_src, z_src, indexing='ij')
            si = yi_grid.ravel() * nw + zi_grid.ravel()
            di = (yi_grid.ravel() + dy) * nw + (zi_grid.ravel() + dz)

            ai = sa[si]
            mask = np.abs(ai) > 1e-300
            if not np.any(mask):
                continue

            si_m = si[mask]
            di_m = di[mask]
            ai_m = ai[mask]
            lf = 0.5 * (sf[si_m] + df[di_m])
            act = L * (1.0 - lf)
            phase = k * act
            kernel = ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_eff
            np.add.at(amps[layer + 1], di_m, kernel)

    return amps


def _centroid_z(amps_last: np.ndarray, nw: int, hw: int, h: float) -> float:
    probs = np.abs(amps_last) ** 2
    total = probs.sum()
    if total <= 0:
        return 0.0
    npl = nw * nw
    z_coords = np.zeros(npl)
    idx = 0
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            z_coords[idx] = iz * h
            idx += 1
    return float(np.dot(probs, z_coords) / total)


def _det_prob(amps_last: np.ndarray) -> float:
    return float(np.sum(np.abs(amps_last) ** 2))


def _born_test(nl, nw, npl, hw, h, kernel_data, k):
    """Three-slit Born test."""
    zero_field = np.zeros((nl, npl))
    slits = [-1, 0, 1]
    center_z = hw

    def _p(open_slits):
        indices = []
        for s in open_slits:
            # Slit at y=s, z=0 → index = (s+hw)*nw + hw
            idx = (s + hw) * nw + center_z
            if 0 <= idx < npl:
                indices.append(idx)
        amps_arr = [1.0 + 0j] * len(indices)
        result = _propagate_np(nl, nw, npl, hw, kernel_data, zero_field, k,
                               source_indices=indices, source_amps=amps_arr)
        return _det_prob(result[-1])

    s1, s2, s3 = slits
    p123 = _p([s1, s2, s3])
    p12 = _p([s1, s2])
    p13 = _p([s1, s3])
    p23 = _p([s2, s3])
    p1 = _p([s1])
    p2 = _p([s2])
    p3 = _p([s3])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    return abs(i3) / max(p123, 1e-300)


def main():
    print("=" * 90)
    print("NUMPY-ACCELERATED h^2+T CONTINUUM LIMIT")
    print(f"  kernel = exp(ikS) * w * h^2 / (L^2 * T)")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 90)
    print()

    spacings = [1.0, 0.5, 0.25, 0.125]

    # Transfer norm check
    print("TRANSFER NORM")
    for h in spacings:
        kd, T = _build_offsets(h)
        print(f"  h={h:.3f}: T = {T:.4f}, edges = {len(kd)}")
    print()

    print(f"  {'h':>5s}  {'nodes':>8s}  {'gravity':>12s}  {'dir':>6s}  "
          f"{'k=0':>10s}  {'P_det':>10s}  {'Born':>10s}  {'F~M':>6s}  {'time':>5s}")
    print(f"  {'-' * 82}")

    for h in spacings:
        t0 = time.time()
        nl = int(PHYS_L / h) + 1
        hw = int(PHYS_W / h)
        nw = 2 * hw + 1
        npl = nw * nw
        n = nl * npl
        kernel_data, T = _build_offsets(h)

        zero_field = np.zeros((nl, npl))
        field = _build_field(nl, nw, hw, h, STRENGTH, MASS_Z)

        free = _propagate_np(nl, nw, npl, hw, kernel_data, zero_field, K_PHYS)
        grav = _propagate_np(nl, nw, npl, hw, kernel_data, field, K_PHYS)

        z_free = _centroid_z(free[-1], nw, hw, h)
        z_grav = _centroid_z(grav[-1], nw, hw, h)
        delta = z_grav - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"

        grav0 = _propagate_np(nl, nw, npl, hw, kernel_data, field, 0.0)
        free0 = _propagate_np(nl, nw, npl, hw, kernel_data, zero_field, 0.0)
        gk0 = _centroid_z(grav0[-1], nw, hw, h) - _centroid_z(free0[-1], nw, hw, h)

        p_det = _det_prob(free[-1])

        # Born test (skip if very large)
        if n < 100000:
            born = _born_test(nl, nw, npl, hw, h, kernel_data, K_PHYS)
            born_s = f"{born:.2e}"
        else:
            born_s = "     skip"

        # Mass scaling (weak field)
        strengths = [0.001, 0.002, 0.004, 0.008]
        deltas_m = []
        for s in strengths:
            f = _build_field(nl, nw, hw, h, s, MASS_Z)
            a = _propagate_np(nl, nw, npl, hw, kernel_data, f, K_PHYS)
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
        fm_s = f"{fm:.3f}" if not math.isnan(fm) else "  nan"

        dt = time.time() - t0
        print(f"  {h:5.3f}  {n:8d}  {delta:+12.6e}  "
              f"{direction:>6s}  {gk0:+10.2e}  {p_det:10.2e}  {born_s}  {fm_s}  {dt:4.0f}s")

    # Detailed weak-field deflection convergence
    print()
    print("WEAK-FIELD DEFLECTION CONVERGENCE (s=0.004)")
    for h in spacings:
        nl = int(PHYS_L / h) + 1
        hw = int(PHYS_W / h)
        nw = 2 * hw + 1
        npl = nw * nw
        kernel_data, T = _build_offsets(h)
        zero_field = np.zeros((nl, npl))
        free = _propagate_np(nl, nw, npl, hw, kernel_data, zero_field, K_PHYS)
        z_free = _centroid_z(free[-1], nw, hw, h)
        field = _build_field(nl, nw, hw, h, 0.004, MASS_Z)
        grav = _propagate_np(nl, nw, npl, hw, kernel_data, field, K_PHYS)
        delta = _centroid_z(grav[-1], nw, hw, h) - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  h={h:.3f}: delta = {delta:+.6e} {direction}")

    print()
    print("SAFE READ")
    print("  T should be ~5-6 at all h (logarithmic growth)")
    print("  gravity TOWARD at all h, F~M ~ 1.0")
    print("  Born < 1e-10 (linearity preserved by fixed normalization)")
    print("  weak-field deflection should converge to a finite nonzero limit")
    print("  if all properties converge as h -> 0: CONTINUUM LIMIT EXISTS")


if __name__ == "__main__":
    main()
