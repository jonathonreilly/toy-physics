#!/usr/bin/env python3
"""Complex action horizon radius test.

Question:
  For the complex action with gamma > 0, is there a characteristic radius
  r_h(s, gamma) where escape drops to 50%?  Does r_h scale with source
  strength s in a physically meaningful way (r_h ~ s = Schwarzschild-like)?

  If r_h ~ s, this would be an analog of rs = 2GM/c^2.
"""

from __future__ import annotations

import math

BETA = 0.8
K = 5.0
H = 0.5
MAX_D_PHYS = 3.0
NL_PHYS = 30
PW = 6


def _build_lattice(phys_l: int, phys_w: int, h: float) -> dict:
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

    return {
        "nl": nl, "hw": hw, "nw": nw, "npl": npl, "n": n,
        "pos": pos, "nmap": nmap, "layer_start": layer_start,
        "offsets": offsets, "h": h,
    }


def _inst_field(lat: dict, s: float, z_src: float) -> list[list[float]]:
    nl, npl = lat["nl"], lat["npl"]
    layer_start, pos = lat["layer_start"], lat["pos"]
    gl = nl // 3
    src_node = lat["nmap"][(gl, 0, round(z_src / lat["h"]))]
    sx, sy, sz = pos[src_node]
    field = [[0.0] * npl for _ in range(nl)]
    for layer in range(nl):
        ls = layer_start[layer]
        for i in range(npl):
            x, y, z = pos[ls + i]
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
            field[layer][i] = s / r
    return field


def _propagate_complex(lat: dict, field: list[list[float]], k: float, gamma: float) -> list[complex]:
    nl, npl, nw, n = lat["nl"], lat["npl"], lat["nw"], lat["n"]
    layer_start, offsets = lat["layer_start"], lat["offsets"]
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
                    s_real = L * (1.0 - lf)
                    s_imag = gamma * L * lf
                    phase = k * s_real
                    decay = -k * s_imag
                    if decay < -50:
                        amp_factor = 0.0
                    elif decay > 50:
                        amp_factor = math.exp(50)
                    else:
                        amp_factor = math.exp(decay)
                    amps[ld + di] += ai * complex(math.cos(phase), math.sin(phase)) * amp_factor * w / (L * L)
    return amps


def _det_prob(amps: list[complex], lat: dict) -> float:
    det_start = lat["layer_start"][lat["nl"] - 1]
    return sum(abs(amps[det_start + i]) ** 2 for i in range(lat["npl"]))


def main() -> None:
    lat = _build_lattice(NL_PHYS, PW, H)
    zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
    free = _propagate_complex(lat, zero_field, K, 0.0)
    p_free = _det_prob(free, lat)

    print("=" * 80)
    print("COMPLEX ACTION HORIZON RADIUS")
    print("  escape fraction vs source distance b, for different gamma and s")
    print("=" * 80)
    print(f"h={H}, W={PW}, L={NL_PHYS}")
    print()

    gamma = 0.5
    strengths = [0.05, 0.1, 0.2, 0.4]
    z_sources = [1.0, 2.0, 3.0, 4.0, 5.0]

    print(f"ESCAPE vs DISTANCE at gamma={gamma}")
    header = f"{'b':>6s}" + "".join(f"{'s='+str(s):>12s}" for s in strengths)
    print(header)
    print("-" * (6 + 12 * len(strengths)))

    # For each distance b (impact parameter = z_src), measure escape
    for b in z_sources:
        row = f"{b:6.1f}"
        for s in strengths:
            field = _inst_field(lat, s, b)
            amps = _propagate_complex(lat, field, K, gamma)
            p_det = _det_prob(amps, lat)
            escape = p_det / p_free if p_free > 1e-30 else 0.0
            row += f"{escape:12.4f}"
        print(row)

    # Find r_50 (distance where escape = 50%) for each s
    print()
    print("HORIZON RADIUS (b where escape = 50%)")
    print(f"{'s':>8s} {'r_50':>8s}")
    print("-" * 20)

    for s in strengths:
        # Bisection to find b where escape = 0.5
        b_lo, b_hi = 0.5, 6.0
        for _ in range(20):
            b_mid = (b_lo + b_hi) / 2
            field = _inst_field(lat, s, b_mid)
            amps = _propagate_complex(lat, field, K, gamma)
            escape = _det_prob(amps, lat) / p_free
            if escape < 0.5:
                b_lo = b_mid
            else:
                b_hi = b_mid
        r_50 = (b_lo + b_hi) / 2
        print(f"{s:8.3f} {r_50:8.3f}")

    # Check r_50 scaling with s
    print()
    print("SCALING CHECK")
    print("  if r_50 ~ s, this is Schwarzschild-like (r_s ~ GM)")
    print("  if r_50 ~ sqrt(s), this is something else")
    print("  if r_50 ~ log(s), this is logarithmic")

    # Also test gamma dependence
    print()
    print("GAMMA DEPENDENCE of r_50 at s=0.1")
    gammas = [0.2, 0.5, 1.0, 2.0]
    for gamma in gammas:
        b_lo, b_hi = 0.5, 6.0
        for _ in range(20):
            b_mid = (b_lo + b_hi) / 2
            field = _inst_field(lat, 0.1, b_mid)
            amps = _propagate_complex(lat, field, K, gamma)
            escape = _det_prob(amps, lat) / p_free
            if escape < 0.5:
                b_lo = b_mid
            else:
                b_hi = b_mid
        r_50 = (b_lo + b_hi) / 2
        print(f"  gamma={gamma:.1f}: r_50 = {r_50:.3f}")

    print()
    print("SAFE READ")
    print("  r_50 ~ s would mean the horizon radius is proportional to mass")
    print("  (Schwarzschild-like). Any other scaling is non-GR.")
    print("  gamma sets the strength of absorption; larger gamma -> larger r_50.")


if __name__ == "__main__":
    main()
