#!/usr/bin/env python3
"""Test whether complex action emerges from retarded moving sources.

Question:
  When a source moves at velocity v, the retarded field at a point includes
  both the 1/r potential AND a velocity-dependent correction. In GR, a
  moving mass has gravitomagnetic effects that look like an imaginary
  potential in the frequency domain.

  On the lattice: if the source moves in z at speed v, the field at
  layer x seen by a node at (x, y, z) comes from the retarded source
  position z_src(x_ret) = z_0 + v * x_ret, where x_ret accounts for
  the light-travel delay.

  Can we show that the effective action for a moving source is equivalent
  to S = L(1-f) + i*gamma_eff*L*f where gamma_eff depends on v?

  If so, complex action is NOT an additional parameter — it EMERGES from
  source motion.

Test:
  1. Build field from moving source (v != 0)
  2. Propagate with REAL action S = L(1-f) through this field
  3. Compare deflection and escape to complex action at gamma_eff
  4. If they match, the moving-source field effectively generates gamma
"""

from __future__ import annotations

import math

BETA = 0.8
K = 5.0
H = 0.5
MAX_D_PHYS = 3.0
NL_PHYS = 30
PW = 6
SOURCE_Z0 = 3.0
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


def _static_field(lat: dict, s: float, z_src: float) -> list[list[float]]:
    """Instantaneous field from static source at z_src, placed at layer gl."""
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


def _moving_field(lat: dict, s: float, z0: float, v: float, c_field: float = 0.8) -> list[list[float]]:
    """Retarded field from source moving at velocity v in z-direction.

    Source position: z_src(x) = z0 + v * x
    At layer x, the retarded source position accounts for light-travel delay.
    """
    nl, npl = lat["nl"], lat["npl"]
    layer_start, pos = lat["layer_start"], lat["pos"]
    gl = nl // 3
    h = lat["h"]
    field = [[0.0] * npl for _ in range(nl)]

    for layer in range(nl):
        ls = layer_start[layer]
        # Source starts at layer gl, moves at v in z per layer
        x_src = gl * h
        z_src_current = z0 + v * (layer - gl) * h  # source position at this layer's "time"

        for i in range(npl):
            x, y, z = pos[ls + i]
            # Distance from current source position
            dx = x - x_src
            dy = y - 0.0
            dz = z - z_src_current
            dist_yz = math.sqrt(dy * dy + dz * dz)

            # Retardation: the field at (x,y,z) comes from where the source WAS
            # The light-travel time from source to this point is dist/c
            # During that time, the source moved by v * dist/c in z
            # Iterative approximation for retarded position
            z_src_ret = z_src_current
            for _ in range(5):
                r_try = math.sqrt(dx * dx + dy * dy + (z - z_src_ret) ** 2) + 0.1
                t_delay = r_try / (c_field * h)  # delay in layer units
                z_src_ret = z0 + v * (layer - gl - t_delay) * h

            r_ret = math.sqrt(dx * dx + dy * dy + (z - z_src_ret) ** 2) + 0.1
            if layer >= gl:
                field[layer][i] = s / r_ret
    return field


def _propagate_real(lat: dict, field: list[list[float]], k: float) -> list[complex]:
    """Standard valley-linear: S = L(1-f), real action only."""
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
                    act = L * (1.0 - lf)
                    amps[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w / (L * L)
    return amps


def _propagate_complex(lat: dict, field: list[list[float]], k: float, gamma: float) -> list[complex]:
    """Complex action: S = L(1-f) + i*gamma*L*f."""
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


def _centroid_z(amps: list[complex], lat: dict) -> float:
    det_start = lat["layer_start"][lat["nl"] - 1]
    npl = lat["npl"]
    total = 0.0
    weighted = 0.0
    for i in range(npl):
        p = abs(amps[det_start + i]) ** 2
        total += p
        weighted += p * lat["pos"][det_start + i][2]
    return weighted / total if total > 1e-30 else 0.0


def _det_prob(amps: list[complex], lat: dict) -> float:
    det_start = lat["layer_start"][lat["nl"] - 1]
    return sum(abs(amps[det_start + i]) ** 2 for i in range(lat["npl"]))


def main() -> None:
    lat = _build_lattice(NL_PHYS, PW, H)
    zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
    free = _propagate_real(lat, zero_field, K)
    z_free = _centroid_z(free, lat)
    p_free = _det_prob(free, lat)

    print("=" * 80)
    print("EMERGENT GAMMA FROM MOVING SOURCE")
    print("  Does a moving source's retarded field act like a complex action?")
    print("=" * 80)
    print(f"h={H}, W={PW}, L={NL_PHYS}, s={SOURCE_STRENGTH}, z0={SOURCE_Z0}")
    print()

    # Phase 1: Moving source with real action
    velocities = [0.0, 0.1, 0.2, 0.5, -0.1, -0.2, -0.5]
    print("MOVING SOURCE (real action, retarded field)")
    print(f"{'v':>6s} {'deflection':>12s} {'direction':>10s} {'escape':>10s}")
    print("-" * 44)
    for v in velocities:
        if v == 0.0:
            field = _static_field(lat, SOURCE_STRENGTH, SOURCE_Z0)
        else:
            field = _moving_field(lat, SOURCE_STRENGTH, SOURCE_Z0, v)
        amps = _propagate_real(lat, field, K)
        delta = _centroid_z(amps, lat) - z_free
        escape = _det_prob(amps, lat) / p_free
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"{v:6.2f} {delta:+12.6e} {direction:>10s} {escape:10.4f}")

    # Phase 2: Try to match each moving-source result to a complex action gamma
    print()
    print("MATCHING: moving-source escape -> equivalent gamma")
    print(f"{'v':>6s} {'escape_mov':>12s} {'gamma_eff':>10s} {'escape_cx':>12s} {'defl_mov':>12s} {'defl_cx':>12s}")
    print("-" * 72)

    static_field = _static_field(lat, SOURCE_STRENGTH, SOURCE_Z0)

    for v in [0.1, 0.2, 0.5]:
        mov_field = _moving_field(lat, SOURCE_STRENGTH, SOURCE_Z0, v)
        mov_amps = _propagate_real(lat, mov_field, K)
        mov_escape = _det_prob(mov_amps, lat) / p_free
        mov_delta = _centroid_z(mov_amps, lat) - z_free

        # Bisect to find gamma that matches escape
        g_lo, g_hi = -1.0, 5.0
        for _ in range(30):
            g_mid = (g_lo + g_hi) / 2
            cx_amps = _propagate_complex(lat, static_field, K, g_mid)
            cx_escape = _det_prob(cx_amps, lat) / p_free
            if cx_escape > mov_escape:
                g_lo = g_mid
            else:
                g_hi = g_mid
        gamma_eff = (g_lo + g_hi) / 2
        cx_amps = _propagate_complex(lat, static_field, K, gamma_eff)
        cx_escape = _det_prob(cx_amps, lat) / p_free
        cx_delta = _centroid_z(cx_amps, lat) - z_free
        print(f"{v:6.2f} {mov_escape:12.4f} {gamma_eff:10.4f} {cx_escape:12.4f} {mov_delta:+12.6e} {cx_delta:+12.6e}")

    print()
    print("SAFE READ")
    print("  if gamma_eff ~ v, the complex action emerges naturally from source motion")
    print("  if the deflections also match, the correspondence is complete")
    print("  if they dont match, the moving-source physics is richer than complex action")


if __name__ == "__main__":
    main()
