#!/usr/bin/env python3
"""Dense lattice with normalized transfer for continuum limit.

The dense 3D lattice (max_d_phys=3) gives correct gravity, Born, MI,
decoherence at h=0.5 and h=1.0, but overflows at h=0.25 because the
per-node transfer norm T ~ 1/h^4.

Fix: normalize each edge by T_node, making per-layer norm exactly 1.
Gravity is measured as a centroid ratio, so normalization should not
affect it. The action phases are unchanged.

Key test: do the 10 observables converge as h -> 0?
"""

from __future__ import annotations

import math
import cmath
import time

BETA = 0.8
K_PHYS = 5.0
PHYS_W = 6
PHYS_L = 30
MAX_D_PHYS = 3.0
MASS_Z = 3.0
STRENGTH = 0.1


def _build_3d_normed(phys_l: int, phys_w: int, h: float) -> dict:
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

    # Compute interior transfer norm (same for all interior nodes)
    T_interior = sum(w / (L * L) for _, _, L, w in offsets)

    return {
        "nl": nl, "hw": hw, "nw": nw, "npl": npl, "n": n,
        "pos": pos, "nmap": nmap, "layer_start": layer_start,
        "offsets": offsets, "h": h, "T": T_interior, "max_d": max_d,
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


def _propagate_normed(lat: dict, field: list[list[float]], k: float) -> list[complex]:
    """Valley-linear propagator with normalized transfer: kernel = exp(ikS)*w/(L^2*T)."""
    nl, npl, nw, n = lat["nl"], lat["npl"], lat["nw"], lat["n"]
    layer_start, offsets = lat["layer_start"], lat["offsets"]
    T = lat["T"]
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
                    amps[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w / (L * L * T)
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
    return weighted / total if total > 0.0 else 0.0


def _det_prob(amps: list[complex], lat: dict) -> float:
    det_start = lat["layer_start"][lat["nl"] - 1]
    return sum(abs(amps[det_start + i]) ** 2 for i in range(lat["npl"]))


def main() -> None:
    print("=" * 95)
    print("DENSE NORMED-TRANSFER 3D CONTINUUM LIMIT")
    print(f"  max_d_phys={MAX_D_PHYS}, valley-linear action S=L(1-f)")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 95)
    print()

    spacings = [1.0, 0.5, 0.25]

    print(f"  {'h':>5s}  {'nodes':>8s}  {'T':>10s}  {'gravity':>10s}  {'direction':>10s}  "
          f"{'k=0':>10s}  {'amp_max':>10s}  {'time':>5s}")
    print(f"  {'-' * 80}")

    for h in spacings:
        t0 = time.time()
        lat = _build_3d_normed(PHYS_L, PHYS_W, h)
        print(f"  building h={h}... nodes={lat['n']}, T={lat['T']:.2e}", flush=True)

        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        field = _inst_field(lat, STRENGTH, MASS_Z)

        free = _propagate_normed(lat, zero_field, K_PHYS)
        grav = _propagate_normed(lat, field, K_PHYS)

        z_free = _centroid_z(free, lat)
        z_grav = _centroid_z(grav, lat)
        delta = z_grav - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"

        # k=0 test
        grav0 = _propagate_normed(lat, field, 0.0)
        free0 = _propagate_normed(lat, zero_field, 0.0)
        z_free0 = _centroid_z(free0, lat)
        z_grav0 = _centroid_z(grav0, lat)
        gk0 = z_grav0 - z_free0

        amp_max = max(abs(a) for a in free)
        dt = time.time() - t0

        print(f"  {h:5.3f}  {lat['n']:8d}  {lat['T']:10.2e}  {delta:+10.6f}  "
              f"{direction:>10s}  {gk0:+10.2e}  {amp_max:10.2e}  {dt:4.0f}s")

    # Mass scaling at each h
    print()
    print("MASS SCALING (F~M exponent)")
    strengths = [0.001, 0.002, 0.004, 0.008]
    for h in spacings:
        lat = _build_3d_normed(PHYS_L, PHYS_W, h)
        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        free = _propagate_normed(lat, zero_field, K_PHYS)
        z_free = _centroid_z(free, lat)

        deltas = []
        for s in strengths:
            field = _inst_field(lat, s, MASS_Z)
            amps = _propagate_normed(lat, field, K_PHYS)
            delta = _centroid_z(amps, lat) - z_free
            deltas.append(abs(delta))

        # Fit power law
        lx = [math.log(x) for x in strengths]
        ly = [math.log(y) for y in deltas if y > 1e-15]
        n = len(ly)
        if n >= 3:
            mx = sum(lx[:n]) / n
            my = sum(ly) / n
            sxx = sum((x - mx) ** 2 for x in lx[:n])
            sxy = sum((x - mx) * (y - my) for x, y in zip(lx[:n], ly))
            exp = sxy / sxx
        else:
            exp = float('nan')
        print(f"  h={h:.3f}: F~M = {exp:.3f}")

    print()
    print("SAFE READ")
    print("  if gravity TOWARD and F~M~1.0 converge at all h: continuum limit works")
    print("  if gravity vanishes or sign flips: normalization kills the physics")
    print("  k=0 must be ~0 (phase-mediated gravity)")
    print("  amp_max < 1e10 means no overflow")


if __name__ == "__main__":
    main()
