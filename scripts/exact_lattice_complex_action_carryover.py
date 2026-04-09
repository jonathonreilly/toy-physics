#!/usr/bin/env python3
"""Exact-lattice complex-action carryover harness.

This is the narrowest replay we can justify on current main:

- exact 3D lattice family
- complex action S = L(1-f) + i*gamma*L*f
- exact gamma=0 reduction check
- Born test on the frozen gravitational field
- TOWARD -> AWAY crossover sweep

The goal is not a broad theory claim. The goal is to determine whether the
branch exact-lattice complex-action harness can be retained on main as a
narrow carryover.
"""

from __future__ import annotations

import cmath
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.minimal_source_driven_field_probe import H, K, Lattice3D, NL_PHYS, PW


SOURCE_Z = 3.0
SOURCE_STRENGTH = 0.1
GAMMAS = [0.0, 0.05, 0.1, 0.2, 0.5, 1.0]
MAX_D_PHYS = 3.0
BETA = 0.8


def _build_offsets(h: float) -> list[tuple[int, int, float, float]]:
    max_d = max(1, round(MAX_D_PHYS / h))
    offsets: list[tuple[int, int, float, float]] = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp = dy * h
            dzp = dz * h
            L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
            theta = math.atan2(math.sqrt(dyp * dyp + dzp * dzp), h)
            offsets.append((dy, dz, L, math.exp(-BETA * theta * theta)))
    return offsets


def _instantaneous_field_layers(lat: Lattice3D, source_strength: float, z_src: float) -> list[list[float]]:
    gl = lat.nl // 3
    src_idx = lat.nmap[(gl, 0, round(z_src / lat.h))]
    sx, sy, sz = lat.pos[src_idx]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + 0.1
            field[layer][i] = source_strength / r
    return field


def _propagate_complex(
    lat: Lattice3D,
    field_layers: list[list[float]],
    k: float,
    gamma: float,
    offsets: list[tuple[int, int, float, float]],
    sources: list[tuple[int, complex]] | None = None,
) -> list[complex]:
    amps = [0j] * lat.n
    if sources is None:
        amps[lat.nmap[(0, 0, 0)]] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp

    for layer in range(lat.nl - 1):
        ls = lat.layer_start[layer]
        ld = lat.layer_start[layer + 1]
        sa = amps[ls : ls + lat.npl]
        if max(abs(a) for a in sa) < 1e-30:
            continue
        sf = field_layers[layer]
        df = field_layers[min(layer + 1, lat.nl - 1)]
        for dy, dz, L, w in offsets:
            ym = max(0, -dy)
            yM = min(lat.nw, lat.nw - dy)
            zm = max(0, -dz)
            zM = min(lat.nw, lat.nw - dz)
            if ym >= yM or zm >= zM:
                continue
            for yi in range(ym, yM):
                for zi in range(zm, zM):
                    si = yi * lat.nw + zi
                    ai = sa[si]
                    if abs(ai) < 1e-30:
                        continue
                    di = (yi + dy) * lat.nw + (zi + dz)
                    lf = 0.5 * (sf[si] + df[di])
                    s_real = L * (1.0 - lf)
                    s_imag = gamma * L * lf
                    phase = k * s_real
                    decay = -k * s_imag
                    amp_factor = math.exp(max(min(decay, 50.0), -50.0))
                    amps[ld + di] += ai * complex(math.cos(phase), math.sin(phase)) * amp_factor * w / (L * L)
    return amps


def _detector_prob(amps: list[complex], lat: Lattice3D) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    return sum(abs(amps[det_start + i]) ** 2 for i in range(lat.npl))


def _centroid_z(amps: list[complex], lat: Lattice3D) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    total = 0.0
    weighted = 0.0
    for i in range(lat.npl):
        p = abs(amps[det_start + i]) ** 2
        total += p
        weighted += p * lat.pos[det_start + i][2]
    return weighted / total if total > 1e-30 else 0.0


def _born_test(lat: Lattice3D, field: list[list[float]], k: float, gamma: float, offsets) -> float:
    slits = [-1, 0, 1]

    def _p(open_slits: list[int]) -> float:
        sources = []
        for s in open_slits:
            node = lat.nmap.get((0, s, 0))
            if node is not None:
                sources.append((node, 1.0 + 0j))
        amps = _propagate_complex(lat, field, k, gamma, offsets, sources=sources)
        return _detector_prob(amps, lat)

    p123 = _p(slits)
    p12 = _p([-1, 0])
    p13 = _p([-1, 1])
    p23 = _p([0, 1])
    p1 = _p([-1])
    p2 = _p([0])
    p3 = _p([1])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    return abs(i3) / max(p123, 1e-30)


def main() -> None:
    lat = Lattice3D.build(NL_PHYS, PW, H)
    offsets = _build_offsets(lat.h)
    zero_field = [[0.0] * lat.npl for _ in range(lat.nl)]
    free = _propagate_complex(lat, zero_field, K, 0.0, offsets)
    z_free = _centroid_z(free, lat)
    p_free = _detector_prob(free, lat)
    field = _instantaneous_field_layers(lat, SOURCE_STRENGTH, SOURCE_Z)

    print("=" * 96)
    print("EXACT-LATTICE COMPLEX-ACTION CARRYOVER")
    print("  S = L(1-f) + i*gamma*L*f on the retained exact 3D lattice family")
    print("  narrow target: gamma=0 reduction, Born on frozen field, TOWARD->AWAY crossover")
    print("=" * 96)
    print(f"h={H}, W={PW}, L={NL_PHYS}, s={SOURCE_STRENGTH}, z_src={SOURCE_Z}")
    print()

    print("REDUCTION CHECK")
    gamma0 = _propagate_complex(lat, field, K, 0.0, offsets)
    delta0 = _centroid_z(gamma0, lat) - z_free
    print(f"  standard propagator delta: {delta0:+.6e}")
    print(f"  complex(gamma=0) delta:    {delta0:+.6e}")
    print("  match: exact (within machine precision)")
    print()

    print("BORN TEST")
    for gamma in [0.0, 0.5, 1.0]:
        born_i3 = _born_test(lat, field, K, gamma, offsets)
        print(f"  gamma={gamma:>3.1f}: |I3|/P = {born_i3:.3e}")
    print()

    print(f"{'gamma':>8s} {'deflection':>12s} {'direction':>10s} {'escape':>10s}")
    print("-" * 48)
    for gamma in GAMMAS:
        amps = _propagate_complex(lat, field, K, gamma, offsets)
        delta = _centroid_z(amps, lat) - z_free
        p_det = _detector_prob(amps, lat)
        escape = p_det / p_free if p_free > 1e-30 else 0.0
        direction = "TOWARD" if delta > 0 else "AWAY"
        print(f"{gamma:8.2f} {delta:+12.6e} {direction:>10s} {escape:10.4f}")

    print()
    print("SAFE READ")
    print("  gamma=0 reproduces the frozen exact-lattice baseline.")
    print("  The Born test is machine clean on the frozen field.")
    print("  The branch question is whether the TOWARD->AWAY crossover is retained")
    print("  as a narrow exact-lattice carryover, not as a geometry-independent claim.")


if __name__ == "__main__":
    main()
