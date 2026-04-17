#!/usr/bin/env python3
"""Dense 3D lattice: h^2 measure + per-node T normalization.

The interior T normalization causes boundary leakage: nodes near the lattice
edge have fewer outgoing edges than T assumes, so amplitude is lost.

Fix: compute T(node) for each node, using only the edges that actually exist
(i.e., where the destination is within the lattice). Then the kernel is:

  kernel_ij = exp(ikS) * w * h^2 / (L^2 * T_i)

where T_i = sum_{j: i->j} w * h^2 / L^2, summing only over valid destinations.

This gives per-node transfer norm = 1 EXACTLY, even at boundaries.
P_det should be O(1), not underflowing.
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
            w_raw = w * h * h / (L * L)  # h^2 measure, 1/L^2 kernel
            offsets.append((dy, dz, L, w, w_raw))
    T_interior = sum(wr for _, _, _, _, wr in offsets)
    return offsets, T_interior


def _compute_per_node_T(nw: int, hw: int, offsets: list) -> np.ndarray:
    """Compute T[yi, zi] for each node position in a layer."""
    npl = nw * nw
    T_node = np.zeros(npl)
    for yi in range(nw):
        for zi in range(nw):
            si = yi * nw + zi
            T = 0.0
            for dy, dz, L, w, w_raw in offsets:
                di_y = yi + dy
                di_z = zi + dz
                if 0 <= di_y < nw and 0 <= di_z < nw:
                    T += w_raw
            T_node[si] = T if T > 1e-300 else 1.0
    return T_node


def _build_field(nl: int, nw: int, hw: int, h: float, s: float, z_src: float):
    gl = nl // 3
    iz_src = round(z_src / h)
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


def _propagate(
    nl: int, nw: int, npl: int, hw: int,
    offsets: list, T_node: np.ndarray, field: np.ndarray, k: float,
    source_indices: list[int] | None = None,
    source_amps: list[complex] | None = None,
) -> np.ndarray:
    """Propagate with per-node T normalization."""
    amps = np.zeros((nl, npl), dtype=np.complex128)
    if source_indices is None:
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
        for dy, dz, L, w, w_raw in offsets:
            ym_s = max(0, -dy)
            yM_s = min(nw, nw - dy)
            zm_s = max(0, -dz)
            zM_s = min(nw, nw - dz)
            if ym_s >= yM_s or zm_s >= zM_s:
                continue

            y_src = np.arange(ym_s, yM_s)
            z_src_arr = np.arange(zm_s, zM_s)
            yi_grid, zi_grid = np.meshgrid(y_src, z_src_arr, indexing='ij')
            si = yi_grid.ravel() * nw + zi_grid.ravel()
            di = (yi_grid.ravel() + dy) * nw + (zi_grid.ravel() + dz)

            ai = sa[si]
            mask = np.abs(ai) > 1e-300
            if not np.any(mask):
                continue

            si_m = si[mask]
            di_m = di[mask]
            ai_m = ai[mask]

            # Per-node normalization
            T_src = T_node[si_m]
            lf = 0.5 * (sf[si_m] + df[di_m])
            act = L * (1.0 - lf)
            phase = k * act
            kernel = ai_m * (np.cos(phase) + 1j * np.sin(phase)) * w_raw / T_src
            np.add.at(amps[layer + 1], di_m, kernel)

    return amps


def _centroid_z(amps_last: np.ndarray, nw: int, hw: int, h: float) -> float:
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


def _det_prob(amps_last: np.ndarray) -> float:
    return float(np.sum(np.abs(amps_last) ** 2))


def _born_test(nl, nw, npl, hw, h, offsets, T_node, k):
    zero_field = np.zeros((nl, npl))
    slits = [-1, 0, 1]
    center_z = hw

    def _p(open_slits):
        indices = [(s + hw) * nw + center_z for s in open_slits if 0 <= (s + hw) * nw + center_z < npl]
        amps_arr = [1.0 + 0j] * len(indices)
        result = _propagate(nl, nw, npl, hw, offsets, T_node, zero_field, k,
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
    print("PER-NODE T NORMALIZATION — CONTINUUM LIMIT")
    print(f"  kernel_ij = exp(ikS) * w * h^2 / (L^2 * T_i)")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 90)
    print()

    spacings = [1.0, 0.5, 0.25, 0.125]

    print("TRANSFER NORM (interior vs boundary)")
    for h in spacings[:3]:
        offsets, T_int = _build_offsets(h)
        hw = int(PHYS_W / h)
        nw = 2 * hw + 1
        T_node = _compute_per_node_T(nw, hw, offsets)
        T_corner = T_node[0]  # (0,0) corner
        T_center = T_node[hw * nw + hw]  # center
        print(f"  h={h:.3f}: T_interior={T_int:.4f}, T_center={T_center:.4f}, "
              f"T_corner={T_corner:.4f}, ratio={T_corner/T_center:.3f}")
    print()

    print(f"  {'h':>5s}  {'nodes':>8s}  {'gravity':>12s}  {'dir':>6s}  "
          f"{'P_det':>10s}  {'Born':>10s}  {'F~M':>6s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    for h in spacings:
        t0 = time.time()
        nl = int(PHYS_L / h) + 1
        hw = int(PHYS_W / h)
        nw = 2 * hw + 1
        npl = nw * nw
        n = nl * npl
        offsets, T_int = _build_offsets(h)
        T_node = _compute_per_node_T(nw, hw, offsets)

        zero_field = np.zeros((nl, npl))
        field = _build_field(nl, nw, hw, h, STRENGTH, MASS_Z)

        free = _propagate(nl, nw, npl, hw, offsets, T_node, zero_field, K_PHYS)
        grav = _propagate(nl, nw, npl, hw, offsets, T_node, field, K_PHYS)

        z_free = _centroid_z(free[-1], nw, hw, h)
        z_grav = _centroid_z(grav[-1], nw, hw, h)
        delta = z_grav - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"

        p_det = _det_prob(free[-1])

        if n < 100000:
            born = _born_test(nl, nw, npl, hw, h, offsets, T_node, K_PHYS)
            born_s = f"{born:.2e}"
        else:
            born_s = "     skip"

        # Mass scaling
        strengths = [0.001, 0.002, 0.004, 0.008]
        deltas_m = []
        for s in strengths:
            f = _build_field(nl, nw, hw, h, s, MASS_Z)
            a = _propagate(nl, nw, npl, hw, offsets, T_node, f, K_PHYS)
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
              f"{direction:>6s}  {p_det:10.2e}  {born_s}  {fm_s}  {dt:4.0f}s")

    # Weak-field convergence
    print()
    print("WEAK-FIELD DEFLECTION CONVERGENCE (s=0.004)")
    for h in spacings:
        nl = int(PHYS_L / h) + 1
        hw = int(PHYS_W / h)
        nw = 2 * hw + 1
        npl = nw * nw
        offsets, _ = _build_offsets(h)
        T_node = _compute_per_node_T(nw, hw, offsets)
        zero_field = np.zeros((nl, npl))
        free = _propagate(nl, nw, npl, hw, offsets, T_node, zero_field, K_PHYS)
        z_free = _centroid_z(free[-1], nw, hw, h)
        field = _build_field(nl, nw, hw, h, 0.004, MASS_Z)
        grav = _propagate(nl, nw, npl, hw, offsets, T_node, field, K_PHYS)
        delta = _centroid_z(grav[-1], nw, hw, h) - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"  h={h:.3f}: delta = {delta:+.6e} {direction}")

    print()
    print("SAFE READ")
    print("  P_det should be O(1) now (no boundary leakage)")
    print("  Born < 1e-10 (per-node T is still fixed per geometry)")
    print("  F~M ~ 1.0, gravity TOWARD at all h")
    print("  weak-field deflection should converge")
    print("  if P_det stabilizes AND deflection converges: full continuum limit")


if __name__ == "__main__":
    main()
