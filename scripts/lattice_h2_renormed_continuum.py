#!/usr/bin/env python3
"""Dense 3D lattice with h^2 measure + renormalized transfer.

The h^2 measure gives T ~ 5-6 (logarithmically growing). To prevent
overflow at fine h, divide by T at each step. Since T is the same constant
for all interior nodes, this is equivalent to redefining the initial
amplitude. Centroid (gravity) is a ratio, unaffected by overall scaling.

The key insight: we can track log(P) instead of P to avoid overflow.
But for centroid computation we need the actual amplitudes. Instead,
we rescale the amplitude vector periodically to prevent overflow.

Approach: after each layer, divide all amplitudes by the layer's max
amplitude. Track the log of the cumulative scaling factor. The centroid
is unaffected because it's a ratio.
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

    T = sum(w * h * h / (L * L) for _, _, L, w in offsets)

    return {
        "nl": nl, "hw": hw, "nw": nw, "npl": npl, "n": n,
        "pos": pos, "nmap": nmap, "layer_start": layer_start,
        "offsets": offsets, "h": h, "T": T,
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


def _propagate_rescaled(lat: dict, field: list[list[float]], k: float) -> list[complex]:
    """Propagate with h^2 measure, rescaling each layer to prevent overflow.

    After propagating to each new layer, rescale all amplitudes by 1/max_amp.
    The centroid is a ratio and unaffected by this rescaling.
    """
    nl, npl, nw, n = lat["nl"], lat["npl"], lat["nw"], lat["n"]
    layer_start, offsets = lat["layer_start"], lat["offsets"]
    h2 = lat["h"] ** 2
    amps = [0j] * n
    amps[lat["nmap"][(0, 0, 0)]] = 1.0

    for layer in range(nl - 1):
        ls = layer_start[layer]
        ld = layer_start[layer + 1]
        sa = amps[ls:ls + npl]
        mx = max(abs(a) for a in sa)
        if mx < 1e-300:
            continue
        # Rescale source layer to prevent overflow
        if mx > 1e10:
            scale = 1.0 / mx
            sa = [a * scale for a in sa]
            # Also rescale all prior amplitudes (for consistency)
            for i in range(ls, ls + npl):
                amps[i] *= scale
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
    """Born test with rescaled propagator."""
    zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
    slits = [-1, 0, 1]

    def _p(open_slits: list[int]) -> float:
        amps_local = [0j] * lat["n"]
        for s in open_slits:
            node = lat["nmap"].get((0, s, 0))
            if node is not None:
                amps_local[node] = 1.0
        nl, npl, nw = lat["nl"], lat["npl"], lat["nw"]
        layer_start, offsets = lat["layer_start"], lat["offsets"]
        h2 = lat["h"] ** 2
        for layer in range(nl - 1):
            ls = layer_start[layer]
            ld = layer_start[layer + 1]
            sa = amps_local[ls:ls + npl]
            mx = max(abs(a) for a in sa)
            if mx < 1e-300:
                continue
            if mx > 1e10:
                scale = 1.0 / mx
                sa = [a * scale for a in sa]
                for i in range(ls, ls + npl):
                    amps_local[i] *= scale
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
                        act = L
                        amps_local[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w * h2 / (L * L)
        return _det_prob(amps_local, lat)

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
    print("DENSE 3D LATTICE WITH h^2 MEASURE + LAYER RESCALING — CONTINUUM LIMIT")
    print(f"  kernel = exp(ikS) * w * h^2 / L^2, amplitude rescaled each layer")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 95)
    print()

    spacings = [1.0, 0.5, 0.25, 0.125]

    print(f"  {'h':>5s}  {'nodes':>8s}  {'T':>8s}  {'gravity':>12s}  {'dir':>6s}  "
          f"{'k=0':>10s}  {'Born':>10s}  {'time':>5s}")
    print(f"  {'-' * 75}")

    for h in spacings:
        t0 = time.time()
        lat = _build_3d(PHYS_L, PHYS_W, h)
        print(f"  running h={h}...", end="", flush=True)

        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        field = _inst_field(lat, STRENGTH, MASS_Z)

        free = _propagate_rescaled(lat, zero_field, K_PHYS)
        grav = _propagate_rescaled(lat, field, K_PHYS)

        z_free = _centroid_z(free, lat)
        z_grav = _centroid_z(grav, lat)
        delta = z_grav - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"

        grav0 = _propagate_rescaled(lat, field, 0.0)
        free0 = _propagate_rescaled(lat, zero_field, 0.0)
        gk0 = _centroid_z(grav0, lat) - _centroid_z(free0, lat)

        # Born test (skip for large lattices)
        if lat["n"] < 100000:
            born = _born_test(lat, K_PHYS)
            born_s = f"{born:.2e}"
        else:
            born_s = "     skip"

        dt = time.time() - t0
        print(f"\r  {h:5.3f}  {lat['n']:8d}  {lat['T']:8.4f}  {delta:+12.6e}  "
              f"{direction:>6s}  {gk0:+10.2e}  {born_s}  {dt:4.0f}s")

    # Mass scaling at each h
    print()
    print("MASS SCALING (weak field)")
    strengths = [0.001, 0.002, 0.004, 0.008]
    for h in spacings:
        lat = _build_3d(PHYS_L, PHYS_W, h)
        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        free = _propagate_rescaled(lat, zero_field, K_PHYS)
        z_free = _centroid_z(free, lat)

        deltas = []
        for s in strengths:
            field = _inst_field(lat, s, MASS_Z)
            amps = _propagate_rescaled(lat, field, K_PHYS)
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
        d_str = "  ".join(f"{d:+.3e}" for d in deltas)
        print(f"  h={h:.3f}: F~M = {exp_val:.3f} {dir_s}  [{d_str}]")

    print()
    print("SAFE READ")
    print("  layer rescaling prevents overflow at any h (amplitudes bounded)")
    print("  centroid is a ratio: unaffected by rescaling")
    print("  gravity must be TOWARD, F~M must be ~1.0 at all h")
    print("  Born must be < 1e-10")
    print("  if all properties converge as h -> 0: CONTINUUM LIMIT EXISTS")


if __name__ == "__main__":
    main()
