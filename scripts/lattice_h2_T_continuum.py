#!/usr/bin/env python3
"""Dense 3D lattice: h^2 measure + T normalization for continuum limit.

The correct kernel is: exp(ikS) * w * h^2 / (L^2 * T)

where T = sum_edges w * h^2 / L^2 (the interior transfer norm with h^2 measure).

This gives per-layer norm = T / T = 1.0 exactly for interior nodes.
No overflow, no underflow, Born preserved (normalization is fixed, not
data-dependent), centroid unaffected (ratio).

T ~ 5-6 for all h, so the kernel ~ w * h^2 / (L^2 * 5.5) is well-behaved.
"""

from __future__ import annotations

import math
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

    # Precompute kernel weight: w * h^2 / (L^2 * T)
    kernel_weights = [(dy, dz, L, w * h * h / (L * L * T)) for dy, dz, L, w in offsets]

    return {
        "nl": nl, "hw": hw, "nw": nw, "npl": npl, "n": n,
        "pos": pos, "nmap": nmap, "layer_start": layer_start,
        "offsets": offsets, "kernel_weights": kernel_weights,
        "h": h, "T": T,
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


def _propagate(
    lat: dict, field: list[list[float]], k: float,
    sources: list[tuple[int, complex]] | None = None,
) -> list[complex]:
    """Propagate with h^2/T normalized kernel."""
    nl, npl, nw, n = lat["nl"], lat["npl"], lat["nw"], lat["n"]
    layer_start = lat["layer_start"]
    kw = lat["kernel_weights"]  # (dy, dz, L, w_eff) where w_eff = w*h^2/(L^2*T)
    amps = [0j] * n
    if sources is None:
        amps[lat["nmap"][(0, 0, 0)]] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp

    for layer in range(nl - 1):
        ls = layer_start[layer]
        ld = layer_start[layer + 1]
        sa = amps[ls:ls + npl]
        if max(abs(a) for a in sa) < 1e-300:
            continue
        sf = field[layer]
        df = field[min(layer + 1, nl - 1)]
        for dy, dz, L, w_eff in kw:
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
                    if abs(ai) < 1e-300:
                        continue
                    di = (yi + dy) * nw + (zi + dz)
                    lf = 0.5 * (sf[si] + df[di])
                    act = L * (1.0 - lf)
                    amps[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w_eff
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
    """Three-slit Born test. Fixed normalization preserves linearity."""
    zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
    slits = [-1, 0, 1]

    def _p(open_slits: list[int]) -> float:
        sources = []
        for s in open_slits:
            node = lat["nmap"].get((0, s, 0))
            if node is not None:
                sources.append((node, 1.0 + 0j))
        return _det_prob(_propagate(lat, zero_field, k, sources=sources), lat)

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
    print("=" * 90)
    print("DENSE 3D LATTICE: h^2 MEASURE + T NORMALIZATION — CONTINUUM LIMIT")
    print(f"  kernel = exp(ikS) * w * h^2 / (L^2 * T), per-layer norm = 1")
    print(f"  Physical: W={PHYS_W}, L={PHYS_L}, s={STRENGTH}, z_src={MASS_Z}")
    print("=" * 90)
    print()

    spacings = [1.0, 0.5, 0.25, 0.125]

    print(f"  {'h':>5s}  {'nodes':>8s}  {'T':>8s}  {'gravity':>12s}  {'dir':>6s}  "
          f"{'k=0':>10s}  {'P_det':>10s}  {'Born':>10s}  {'time':>5s}")
    print(f"  {'-' * 82}")

    for h in spacings:
        t0 = time.time()
        lat = _build_3d(PHYS_L, PHYS_W, h)
        print(f"  running h={h}...", end="", flush=True)

        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        field = _inst_field(lat, STRENGTH, MASS_Z)

        free = _propagate(lat, zero_field, K_PHYS)
        grav = _propagate(lat, field, K_PHYS)

        z_free = _centroid_z(free, lat)
        z_grav = _centroid_z(grav, lat)
        delta = z_grav - z_free
        direction = "TOWARD" if delta > 0 else "AWAY"

        grav0 = _propagate(lat, field, 0.0)
        free0 = _propagate(lat, zero_field, 0.0)
        gk0 = _centroid_z(grav0, lat) - _centroid_z(free0, lat)

        p_det = _det_prob(free, lat)

        if lat["n"] < 50000:
            born = _born_test(lat, K_PHYS)
            born_s = f"{born:.2e}"
        else:
            born_s = "     skip"

        dt = time.time() - t0
        print(f"\r  {h:5.3f}  {lat['n']:8d}  {lat['T']:8.4f}  {delta:+12.6e}  "
              f"{direction:>6s}  {gk0:+10.2e}  {p_det:10.2e}  {born_s}  {dt:4.0f}s")

    # Mass scaling
    print()
    print("MASS SCALING (weak field, s = 0.001 to 0.008)")
    strengths = [0.001, 0.002, 0.004, 0.008]
    for h in spacings:
        lat = _build_3d(PHYS_L, PHYS_W, h)
        zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
        free = _propagate(lat, zero_field, K_PHYS)
        z_free = _centroid_z(free, lat)

        deltas = []
        for s in strengths:
            field = _inst_field(lat, s, MASS_Z)
            amps = _propagate(lat, field, K_PHYS)
            d = _centroid_z(amps, lat) - z_free
            deltas.append(d)

        abs_d = [abs(d) for d in deltas]
        lx = [math.log(x) for x in strengths]
        ly = [math.log(y) for y in abs_d if y > 1e-300]
        nn = len(ly)
        if nn >= 3:
            mx = sum(lx[:nn]) / nn
            my = sum(ly) / nn
            sxx = sum((x - mx) ** 2 for x in lx[:nn])
            sxy = sum((x - mx) * (y - my) for x, y in zip(lx[:nn], ly))
            exp_val = sxy / sxx
        else:
            exp_val = float('nan')
        dir_s = "TOWARD" if deltas[-1] > 0 else "AWAY"
        print(f"  h={h:.3f}: F~M = {exp_val:.3f} {dir_s}")

    print()
    print("SAFE READ")
    print("  per-layer norm = 1 by construction: no overflow, no underflow")
    print("  Born MUST be < 1e-10 (fixed normalization preserves linearity)")
    print("  gravity must be TOWARD, F~M must be ~1.0 at all h")
    print("  P_det should be O(1) (bounded amplitude)")
    print("  if all properties converge: CONTINUUM LIMIT EXISTS")


if __name__ == "__main__":
    main()
