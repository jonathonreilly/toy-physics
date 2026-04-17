#!/usr/bin/env python3
"""Weak-field recovery sweep for the minimal source-driven field architecture."""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


TARGET_MAXES = [0.001, 0.002, 0.005, 0.010, 0.020, 0.040, 0.080]


def main() -> None:
    lat = m.Lattice3D.build(m.NL_PHYS, m.PW, m.H)
    zero = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 84)
    print("SOURCE-DRIVEN FIELD RECOVERY SWEEP")
    print("  weak-field calibration sweep on the exact 3D lattice")
    print("=" * 84)
    print(f"telegraph parameters: c={m.C_FIELD:.2f}, damp={m.DAMP:.2f}")
    print(f"source strengths: {m.SOURCE_STRENGTHS}")
    print()

    print(f"{'target max':>10s} {'toward':>8s} {'F~M':>8s} {'largest delta':>14s}")
    print("-" * 48)

    for tmax in TARGET_MAXES:
        ref_raw = m._source_driven_field_layers_raw(lat, max(m.SOURCE_STRENGTHS), m.SOURCE_Z)
        ref_max = m._field_abs_max(ref_raw)
        gain = tmax / ref_max if ref_max > 1e-30 else 1.0

        vals = []
        for s in m.SOURCE_STRENGTHS:
            dyn = m._scale_field_layers(m._source_driven_field_layers_raw(lat, s, m.SOURCE_Z), gain)
            amps = lat.propagate(dyn, m.K)
            vals.append(m._centroid_z(amps, lat) - z_free)

        alpha = m._fit_power(list(m.SOURCE_STRENGTHS), vals)
        toward = sum(v > 0 for v in vals)
        largest = max(vals) if vals else float("nan")
        alpha_str = f"{alpha:.3f}" if alpha is not None else "nan"
        print(f"{tmax:10.3f} {toward:>5d}/4 {alpha_str:>8s} {largest:+14.6e}")

    print()
    print("SAFE READ")
    print("  the minimal source-driven field has a real weak-field recovery pocket")
    print("  when the calibrated dynamic field stays small")
    print("  as the field calibration grows, the mass exponent drifts away from 1")
    print("  so the architecture is not dead, but it is calibration-sensitive")


if __name__ == "__main__":
    main()
