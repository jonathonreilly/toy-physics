#!/usr/bin/env python3
"""Spatial profile of complex action propagator.

Question:
  At intermediate gamma, does the beam show a photon-sphere-like feature:
  amplitude concentration at a specific radius from the source?

  At gamma=0: beam passes through, deflected TOWARD source
  At gamma>>1: beam is completely absorbed near source
  At intermediate gamma: do we see amplitude buildup at a characteristic radius?

Self-contained. Measures the z-profile of detector probability at each layer.
"""

from __future__ import annotations

import math

BETA = 0.8
K = 5.0
H = 0.5
MAX_D_PHYS = 3.0
NL_PHYS = 30
PW = 6
SOURCE_Z = 3.0
SOURCE_STRENGTH = 0.1


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


def _propagate_complex(
    lat: dict, field: list[list[float]], k: float, gamma: float,
) -> list[complex]:
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


def main() -> None:
    lat = _build_lattice(NL_PHYS, PW, H)
    field = _inst_field(lat, SOURCE_STRENGTH, SOURCE_Z)
    nl, npl, nw = lat["nl"], lat["npl"], lat["nw"]
    layer_start, pos = lat["layer_start"], lat["pos"]
    hw = lat["hw"]
    h = lat["h"]

    # Source is at layer gl, z=SOURCE_Z
    gl = nl // 3

    print("=" * 80)
    print("COMPLEX ACTION SPATIAL PROFILE")
    print("  z-distribution of amplitude at detector layer for different gamma")
    print("=" * 80)
    print(f"h={H}, W={PW}, L={NL_PHYS}, s={SOURCE_STRENGTH}, z_src={SOURCE_Z}")
    print(f"source at layer {gl} (x={gl*H:.1f}), z={SOURCE_Z}")
    print()

    gammas_test = [0.0, 0.1, 0.2, 0.5, 1.0]

    # For each gamma, compute z-profile at detector (last layer)
    det_layer = nl - 1
    det_start = layer_start[det_layer]

    for gamma in gammas_test:
        amps = _propagate_complex(lat, field, K, gamma)

        # Bin detector probabilities by z-distance from source
        z_bins: dict[float, float] = {}
        total_p = 0.0
        for i in range(npl):
            p = abs(amps[det_start + i]) ** 2
            z = pos[det_start + i][2]
            if z not in z_bins:
                z_bins[z] = 0.0
            z_bins[z] += p
            total_p += p

        # Find peak z
        peak_z = max(z_bins, key=z_bins.get) if z_bins else 0.0
        peak_p = z_bins.get(peak_z, 0.0) / total_p if total_p > 1e-30 else 0.0

        # Compute centroid z and z-width
        mean_z = sum(z * p for z, p in z_bins.items()) / total_p if total_p > 1e-30 else 0.0
        var_z = sum((z - mean_z) ** 2 * p for z, p in z_bins.items()) / total_p if total_p > 1e-30 else 0.0
        sigma_z = math.sqrt(var_z)

        print(f"gamma={gamma:.1f}: peak_z={peak_z:.1f}, centroid_z={mean_z:.3f}, "
              f"sigma_z={sigma_z:.3f}, total_P={total_p:.4e}")

    # Detailed z-profile at gamma=0.5 (horizon regime)
    print()
    print("DETAILED Z-PROFILE at gamma=0.5")
    amps = _propagate_complex(lat, field, K, 0.5)
    z_vals = sorted(set(pos[det_start + i][2] for i in range(npl)))
    total_p = sum(abs(amps[det_start + i]) ** 2 for i in range(npl))
    # Sum over y for each z
    print(f"{'z':>6s} {'P(z)/P_total':>12s}")
    print("-" * 22)
    for z in z_vals:
        pz = 0.0
        for iy in range(-hw, hw + 1):
            iz = round(z / h)
            idx = det_start + (iy + hw) * nw + (iz + hw)
            if 0 <= idx - det_start < npl:
                pz += abs(amps[idx]) ** 2
        frac = pz / total_p if total_p > 1e-30 else 0.0
        if frac > 0.001:
            print(f"{z:6.1f} {frac:12.4f}")

    # Layer-by-layer total probability (amplitude survival vs x)
    print()
    print("LAYER PROBABILITY (amplitude survival vs propagation distance)")
    print(f"{'layer':>6s} {'x':>6s} {'P_layer':>12s} {'P/P_free':>10s}")
    print("-" * 40)

    free_field = [[0.0] * npl for _ in range(nl)]
    free_amps = _propagate_complex(lat, free_field, K, 0.0)

    for gamma in [0.0, 0.5, 1.0]:
        print(f"\n  gamma={gamma:.1f}")
        amps = _propagate_complex(lat, field, K, gamma)
        for layer in [0, gl // 2, gl, gl + gl // 2, nl - 1]:
            ls = layer_start[layer]
            p_layer = sum(abs(amps[ls + i]) ** 2 for i in range(npl))
            p_free_layer = sum(abs(free_amps[ls + i]) ** 2 for i in range(npl))
            ratio = p_layer / p_free_layer if p_free_layer > 1e-30 else 0.0
            print(f"  {layer:6d} {layer * H:6.1f} {p_layer:12.4e} {ratio:10.4f}")

    print()
    print("SAFE READ")
    print("  if the beam concentrates at a specific z != 0 at intermediate gamma,")
    print("  that is a photon-sphere-like feature (orbiting radius)")
    print("  if the beam simply broadens and decays, no photon sphere signature")


if __name__ == "__main__":
    main()
