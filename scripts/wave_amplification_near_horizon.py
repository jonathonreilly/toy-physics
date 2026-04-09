#!/usr/bin/env python3
"""Wave amplification near the absorptive threshold on the exact lattice.

Question:
  Does the oscillating retarded-source signal become genuinely amplified near
  the absorptive trapping threshold, or are the large ratios mostly caused by a
  vanishing static denominator?

This is intentionally narrow:
  - one family: exact 3D lattice
  - one comparison: static retarded source vs oscillating retarded source
  - one absorber sweep: alpha
  - one safety check: report the raw static denominator alongside the ratio
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.minimal_source_driven_field_probe import (  # noqa: E402
    H,
    K,
    Lattice3D,
    _centroid_z,
)


PW = 6
NL_PHYS = 30
SOURCE_Z = 3.0
SOURCE_STRENGTH = 0.1
ALPHAS = [0.0, 0.5, 0.8, 1.0, 2.0]
C_FIELD = 0.8
PERIOD = 8.0
A_OSC = 2.0


def _build_retarded_field_layers(
    lat: Lattice3D,
    source_strength: float,
    *,
    c_field: float,
    z_base: float,
    period: float | None = None,
    amplitude: float = 0.0,
) -> list[list[float]]:
    gl = lat.nl // 3
    fields = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            node = ls + i
            _x, y_n, z_n = lat.pos[node]
            r_approx = math.sqrt(y_n * y_n + (z_n - z_base) ** 2) + 0.1
            t_ret = layer - r_approx / (c_field * H)
            if t_ret < gl or t_ret >= lat.nl:
                continue
            z_src = z_base
            if period is not None and amplitude != 0.0:
                z_src += amplitude * math.sin(2.0 * math.pi * t_ret / period)
            r_ret = math.sqrt(y_n * y_n + (z_n - z_src) ** 2) + 0.1
            fields[layer][i] = source_strength / r_ret
    return fields


def _propagate_with_absorption(
    lat: Lattice3D,
    field_layers: list[list[float]],
    *,
    alpha: float,
    field_scale: float,
) -> list[complex]:
    amps = [0j] * lat.n
    src = lat.nmap[(0, 0, 0)]
    amps[src] = 1.0

    for layer in range(lat.nl - 1):
        ls = lat.layer_start[layer]
        ld = lat.layer_start[layer + 1]
        sa = amps[ls : ls + lat.npl]
        if max(abs(a) for a in sa) < 1e-30:
            continue
        sf = field_layers[layer]
        df = field_layers[min(layer + 1, lat.nl - 1)]
        for dy, dz, L, w in lat.offsets:
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
                    act = L * (1.0 - lf)
                    absorb = math.exp(-alpha * max(lf, 0.0) / max(field_scale, 1e-12))
                    amps[ld + di] += ai * complex(math.cos(K * act), math.sin(K * act)) * w * absorb / (L * L)
    return amps


def _detector_prob(amps: list[complex], lat: Lattice3D) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    return sum(abs(amps[d]) ** 2 for d in range(det_start, det_start + lat.npl))


def main() -> None:
    lat = Lattice3D.build(NL_PHYS, PW, H)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, K)
    z_free = _centroid_z(free, lat)
    p_free = _detector_prob(free, lat)

    static_fields = _build_retarded_field_layers(
        lat, SOURCE_STRENGTH, c_field=C_FIELD, z_base=SOURCE_Z, period=None, amplitude=0.0
    )
    wave_fields = _build_retarded_field_layers(
        lat, SOURCE_STRENGTH, c_field=C_FIELD, z_base=SOURCE_Z, period=PERIOD, amplitude=A_OSC
    )

    print("=" * 84)
    print("WAVE AMPLIFICATION NEAR HORIZON")
    print("  exact 3D lattice, static vs oscillating retarded source under absorption")
    print("=" * 84)
    print(f"h={H}, W={PW}, L={NL_PHYS}, s={SOURCE_STRENGTH}, c={C_FIELD}, T={PERIOD}, A={A_OSC}")
    print()
    print(f"{'alpha':>8s} {'static':>12s} {'wave':>12s} {'|wave/static|':>14s} {'escape':>10s}")
    print("-" * 64)

    best_ratio = -1.0
    best_alpha = None

    for alpha in ALPHAS:
        static_amps = _propagate_with_absorption(lat, static_fields, alpha=alpha, field_scale=SOURCE_STRENGTH)
        wave_amps = _propagate_with_absorption(lat, wave_fields, alpha=alpha, field_scale=SOURCE_STRENGTH)

        static_delta = _centroid_z(static_amps, lat) - z_free
        wave_delta = _centroid_z(wave_amps, lat) - z_free
        ratio = abs(wave_delta) / max(abs(static_delta), 1e-12)
        escape = _detector_prob(static_amps, lat) / p_free if p_free > 1e-30 else 0.0
        print(f"{alpha:8.2f} {static_delta:+12.6e} {wave_delta:+12.6e} {ratio:14.3f} {escape:10.3f}")

        if ratio > best_ratio:
            best_ratio = ratio
            best_alpha = alpha

    print()
    print("SAFE READ")
    print(f"  largest ratio in this sweep: {best_ratio:.3f} at alpha={best_alpha:.2f}")
    print("  interpret large ratios only together with the raw static denominator")
    print("  if the static row crosses near zero, the ratio can look dramatic without")
    print("  implying a correspondingly large absolute wave signal")


if __name__ == "__main__":
    main()
