#!/usr/bin/env python3
"""Dense 3D lattice with h^2 measure for continuum limit.

The correctly discretized 3D path integral has:
  integral d^2 y_perp -> sum * h^2

So the kernel should be: exp(ikS) * w * h^2 / L^2

The transfer norm T = sum_edges w * h^2 / L^2 should converge to a
finite h-independent constant as h -> 0. If it does, the amplitude
neither overflows nor underflows.

Test: T(h), gravity, Born, F~M at h = 1.0, 0.5, 0.25, 0.125.
"""

from __future__ import annotations

import math
import cmath
import time

BETA = 0.8
K_PHYS = 5.0
MAX_D_PHYS = 3.0
PHYS_W = 6
PHYS_L = 30
MASS_Z = 3.0
STRENGTH = 0.1


def _build_3d(phys_l: int, phys_w: int, h: float) -> dict:
    nl = int(phys_l / h) + 1
    hw = int(phys_w / h)
    max_d = max(1, round(MAX_D_PHYS / h))
    nw = 2 * hw + 1
    npl = nw * nw
    n = nl * npl

    pos: list[tuple[float, float, float]] = []
    nmap: dict[tuple[int, int, int], int] = {}
    layer_start = [0] * nl

    idx = 0
    for layer in range(nl):
        layer_start[layer] = idx
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                pos.append((x, iy * h, iz * h))
                nmap[(layer, iy, iz)] = idx
                idx += 1

    offsets: list[tuple[int, int, float, float]] = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp = dy * h
            dzp = dz * h
            L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
            offsets.append((dy, dz, L, math.exp(-BETA * theta * theta)))

    # Transfer norm with h^2 measure
    T = sum(w * h * h / (L * L) for _, _, L, w in offsets)

    return {
        "nl": nl, "hw": hw, "nw": nw, "npl": npl, "n": n,
        "pos": pos, "nmap": nmap, "layer_start": layer_start,
        "offsets": offsets, "h": h, "T": T, "max_d": max_d,
    }


def _inst_field(lat: dict, s: float, z_src: float) -> list[list[float]]:
    nl, npl = lat["nl"], lat["npl"]
    layer_start, pos = lat["layer_start"], lat["pos"]
    gl = nl // 3
    h = lat["h"]
    src_node = lat["nmap"][(gl, 0, round(z_src / h))]
    sx, sy, sz = pos[src_node]
    field = [[0.0] * npl for _ in range(nl)]
    for layer in range(nl):
        ls = layer_start[layer]
        for i in range(npl):
            x, y, z = pos[ls + i]
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
            field[layer][i] = s / r
    return field


def _propagate_h2(lat: dict, field: list[list[float]], k: float) -> list[complex]:
    """Propagate with h^2 measure: kernel = exp(ikS) * w * h^2 / L^2."""
    nl, npl, nw, n = lat["nl"], lat["npl"], lat["nw"], lat["n"]
    layer_start, offsets = lat["layer_start"], lat["offsets"]
    h = lat["h"]
    h2 = h * h
    amps = [0j] * n
    amps[lat["nmap"][(0, 0, 0)]] = 1.0

    for layer in range(nl - 1):
        ls = layer_start[layer]
        ld = layer_start[layer + 1]
        sa = amps[ls:ls + npl]
        if max(abs(a) for a in sa) < 1e-30:
            continue
        sf = field[layer]
        df = field[min(layer + 1, nl - 1)]
        for dy, dz, L, w in offsets:
            ym = max(0, -dy)
            yM = min(nw, nw - dy)
            zm = max(0, -dz)
            zM = min(nw, nw - dz)
            if ym >= yM or zm >= zM:
                continue
            for yi in range(ym, yM):
                for zi in range(zm, zM):
                    si = yi * nw + zi
                    ai = sa[si]
                    if abs(ai) < 1e-30:
                        continue
                    di = (yi + dy) * nw + (zi + dz)
                    lf = 0.5 * (sf[si] + df[di])
                    act = L * (1.0 - lf)
                    amps[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w * h2 / (L * L)
    return amps


def _centroid_z(amps: list[complex], lat: dict) -> float:
    det_start = lat["layer_start"][lat["nl"] - 1]
    npl = lat["npl"]
    total = 0.0
    weighted = 0.0
    for i in range(npl):
        p = abs(amps[det_start + i]) ** 2
        total += p
        weighted += p * lat["pos"][det_start + i][2]
    return weighted / total if total > 0 else 0.0


def _det_prob(amps: list[complex], lat: dict) -> float:
    det_start = lat["layer_start"][lat["nl"] - 1]
    return sum(abs(amps[det_start + i]) ** 2 for i in range(lat["npl"]))


def _born_test(lat: dict, k: float) -> float:
    """Three-slit Born test with zero field (structural test)."""
    zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
    slits = [-1, 0, 1]

    def _p(open_slits: list[int]) -> float:
        amps = [0j] * lat["n"]
        for s in open_slits:
            node = lat["nmap"].get((0, s, 0))
            if node is not None:
                amps[node] = 1.0
        nl, npl, nw = lat["nl"], lat["npl"], lat["nw"]
        layer_start, offsets = lat["layer_start"], lat["offsets"]
        h2 = lat["h"] ** 2
        for layer in range(nl - 1):
            ls = layer_start[layer]
            ld = layer_start[layer + 1]
            sa = amps[ls:ls + npl]
            if max(abs(a) for a in sa) < 1e-30:
                continue
            for dy, dz, L, w in offsets:
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                for yi in range(ym, yM):
                    for zi in range(zm, zM):
                        si = yi * nw + zi
                        ai = sa[si]
                        if abs(ai) < 1e-30:
                            continue
                        di = (yi + dy) * nw + (zi + dz)
                        amps[ld + di] += ai * complex(math.cos(k * L), math.sin(k * L)) * w * h2 / (L * L)
        return _det_prob(amps, lat)

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


def main() -> None:
    print("=" * 95)
    print("DENSE 3D LATTICE WITH h^2 MEASURE — CONTINUUM LIMIT TEST")
    print(f"  kernel = exp(ikS) * w * h^2 / L^2")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 95)
    print()

    spacings = [1.0, 0.5, 0.25]

    # First: check transfer norm convergence
    print("TRANSFER NORM (should converge to finite constant)")
    for h in spacings + [0.125]:
        nl = int(PHYS_L / h) + 1
        max_d = max(1, round(MAX_D_PHYS / h))
        offsets = []
        for dy in range(-max_d, max_d + 1):
            for dz in range(-max_d, max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
                offsets.append((L, math.exp(-BETA * theta * theta)))
        T = sum(w * h * h / (L * L) for L, w in offsets)
        print(f"  h={h:.3f}: T = {T:.6f}, n_edges = {len(offsets)}")

    print()
    print(f"  {'h':>5s}  {'nodes':>8s}  {'T':>8s}  {'gravity':>12s}  {'dir':>6s}  "
          f"{'k=0':>10s}  {'P_det':>10s}  {'Born':>10s}  {'time':>5s}")
    print(f"  {'-' * 85}")

    for h in spacings:
        t0 = time.time()
        lat = _build_3d(PHYS_L, PHYS_W, h)

        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        field = _inst_field(lat, STRENGTH, MASS_Z)

        free = _propagate_h2(lat, zero_field, K_PHYS)
        grav = _propagate_h2(lat, field, K_PHYS)

        z_free = _centroid_z(free, lat)
        z_grav = _centroid_z(grav, lat)
        delta = z_grav - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"

        grav0 = _propagate_h2(lat, field, 0.0)
        free0 = _propagate_h2(lat, zero_field, 0.0)
        gk0 = _centroid_z(grav0, lat) - _centroid_z(free0, lat)

        p_det = _det_prob(free, lat)

        born = _born_test(lat, K_PHYS) if h >= 0.5 else float('nan')

        dt = time.time() - t0
        born_s = f"{born:.2e}" if not math.isnan(born) else "      skip"
        print(f"  {h:5.3f}  {lat['n']:8d}  {lat['T']:8.4f}  {delta:+12.6e}  "
              f"{direction:>6s}  {gk0:+10.2e}  {p_det:10.2e}  {born_s}  {dt:4.0f}s")

    # Mass scaling
    print()
    print("MASS SCALING (weak field)")
    strengths = [0.001, 0.002, 0.004, 0.008]
    for h in spacings:
        lat = _build_3d(PHYS_L, PHYS_W, h)
        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        free = _propagate_h2(lat, zero_field, K_PHYS)
        z_free = _centroid_z(free, lat)

        deltas = []
        for s in strengths:
            field = _inst_field(lat, s, MASS_Z)
            amps = _propagate_h2(lat, field, K_PHYS)
            d = _centroid_z(amps, lat) - z_free
            deltas.append(d)

        abs_d = [abs(d) for d in deltas]
        lx = [math.log(x) for x in strengths]
        ly = [math.log(y) for y in abs_d if y > 1e-300]
        n = len(ly)
        if n >= 3:
            mx = sum(lx[:n]) / n
            my = sum(ly) / n
            sxx = sum((x - mx) ** 2 for x in lx[:n])
            sxy = sum((x - mx) * (y - my) for x, y in zip(lx[:n], ly))
            exp_val = sxy / sxx
        else:
            exp_val = float('nan')
        dir_s = "TOWARD" if deltas[-1] > 0 else "AWAY"
        print(f"  h={h:.3f}: F~M = {exp_val:.3f}, direction = {dir_s}")

    print()
    print("SAFE READ")
    print("  T should converge: if T(h) -> const, the measure is correct")
    print("  gravity should converge to nonzero TOWARD limit")
    print("  Born < 1e-10 at all h")
    print("  P_det should be finite (not overflow, not underflow to 0)")
    print("  F~M ~ 1.0 at all h")


if __name__ == "__main__":
    main()
