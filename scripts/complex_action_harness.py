#!/usr/bin/env python3
"""Complex action harness: S = L(1-f) + i*gamma*L*f.

Question:
  Does adding an imaginary component to the action unify gravity and horizons
  in a single propagator kernel?

  Real part: S_real = L(1-f) -- standard valley-linear gravity
  Imag part: S_imag = gamma*L*f -- absorption/amplification from field

  The kernel becomes:
    exp(i*k*S) = exp(i*k*L*(1-f)) * exp(-k*gamma*L*f)

  gamma > 0: exponential suppression near source -> horizon
  gamma < 0: exponential amplification near source -> instability
  gamma = 0: standard real valley-linear action

Self-contained: no external imports beyond stdlib.
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
GAMMAS = [-0.5, -0.2, 0.0, 0.05, 0.1, 0.15, 0.2, 0.5, 1.0, 2.0]


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
    nl, npl, nw, hw = lat["nl"], lat["npl"], lat["nw"], lat["hw"]
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


def _propagate_valley(lat: dict, field: list[list[float]], k: float) -> list[complex]:
    """Standard valley-linear propagator: S = L(1-f), kernel = exp(ikS)*w/L^2."""
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


def _propagate_complex(
    lat: dict, field: list[list[float]], k: float, gamma: float,
    sources: list[tuple[int, complex]] | None = None,
) -> list[complex]:
    """Complex action propagator: S = L(1-f) + i*gamma*L*f."""
    nl, npl, nw, n = lat["nl"], lat["npl"], lat["nw"], lat["n"]
    layer_start, offsets = lat["layer_start"], lat["offsets"]
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


def _born_test(lat: dict, field: list[list[float]], k: float, gamma: float) -> float:
    """Three-slit Born test with gravitational field.

    I_3 = P(1+2+3) - P(1+2) - P(1+3) - P(2+3) + P(1) + P(2) + P(3)
    Must be 0 for any linear propagator (including non-unitary complex action).
    """
    slits = [-1, 0, 1]

    def _p(open_slits: list[int]) -> float:
        sources = []
        for s in open_slits:
            node = lat["nmap"].get((0, s, 0))
            if node is not None:
                sources.append((node, 1.0 + 0j))
        amps = _propagate_complex(lat, field, k, gamma, sources=sources)
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
    return abs(i3) / max(p123, 1e-30)


def main() -> None:
    lat = _build_lattice(NL_PHYS, PW, H)
    zero_field = [[0.0] * lat["npl"] for _ in range(lat["nl"])]
    free = _propagate_valley(lat, zero_field, K)
    z_free = _centroid_z(free, lat)
    p_free = _det_prob(free, lat)

    field = _inst_field(lat, SOURCE_STRENGTH, SOURCE_Z)

    print("=" * 88)
    print("COMPLEX ACTION HARNESS")
    print("  S = L(1-f) + i*gamma*L*f on exact 3D lattice")
    print("  Born test uses actual gravitational field (NOT zero field)")
    print("=" * 88)
    print(f"h={H}, W={PW}, L={NL_PHYS}, s={SOURCE_STRENGTH}, z_src={SOURCE_Z}")
    print()

    # Phase 1: gamma sweep (1 propagation each)
    print(f"{'gamma':>8s} {'deflection':>12s} {'direction':>10s} {'escape':>10s}")
    print("-" * 48)
    for gamma in GAMMAS:
        amps = _propagate_complex(lat, field, K, gamma)
        delta = _centroid_z(amps, lat) - z_free
        p_det = _det_prob(amps, lat)
        escape = p_det / p_free if p_free > 1e-30 else 0.0
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"{gamma:8.2f} {delta:+12.6e} {direction:>10s} {escape:10.4f}")

    # Phase 2: Born test at key gammas (7 propagations each)
    print()
    print("BORN TEST (|I3|/P with gravitational field)")
    born_gammas = [0.0, 0.5, 1.0]
    for gamma in born_gammas:
        print(f"  running gamma={gamma:.1f}...", flush=True)
        born_i3 = _born_test(lat, field, K, gamma)
        print(f"  gamma={gamma:.1f}: |I3|/P = {born_i3:.2e}")

    # Phase 3: Reduction check
    print()
    print("REDUCTION CHECK")
    std_amps = _propagate_valley(lat, field, K)
    std_delta = _centroid_z(std_amps, lat) - z_free
    cx0_amps = _propagate_complex(lat, field, K, 0.0)
    cx0_delta = _centroid_z(cx0_amps, lat) - z_free
    print(f"  standard propagator delta: {std_delta:+.6e}")
    print(f"  complex(gamma=0) delta:    {cx0_delta:+.6e}")
    print(f"  match: {abs(std_delta - cx0_delta) < 1e-12}")

    # Phase 4: Mass scaling at gamma=0.5 (horizon regime)
    print()
    print("MASS SCALING at gamma=0.5 (horizon regime)")
    gamma_test = 0.5
    strengths = [0.025, 0.05, 0.1, 0.2]
    for s in strengths:
        f = _inst_field(lat, s, SOURCE_Z)
        amps = _propagate_complex(lat, f, K, gamma_test)
        delta = _centroid_z(amps, lat) - z_free
        print(f"  s={s:.3f}: delta={delta:+.6e}")

    print()
    print("SAFE READ")
    print("  gamma=0 must recover standard valley-linear (check reduction above)")
    print("  Born |I3|/P should be ~0 for ALL gamma (propagator is linear in psi)")
    print("  complex action is non-unitary but still linear: Born holds structurally")
    print("  TOWARD->AWAY transition marks the exceptional point")
    print("  escape < 1 means net absorption (horizon-like)")
    print("  escape > 1 means net amplification (superradiance-like)")
    print("  if Born holds AND gravity+horizons coexist, this is a genuine unification")


if __name__ == "__main__":
    main()
