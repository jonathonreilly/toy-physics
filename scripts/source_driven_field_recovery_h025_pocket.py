#!/usr/bin/env python3
"""Exact h=0.25 weak-field pocket probe for the source-driven field branch.

This is the smallest serious refinement test for the retained source-driven
field architecture.

Question:
  Does the exact weak-field recovery pocket survive one refinement step to
  h = 0.25, while keeping exact zero-source reduction and nontrivial amplitude?
"""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


# Smallest serious exact-lattice refinement test.
m.H = 0.25
m.NL_PHYS = 12
m.PW = 3
m.MAX_D_PHYS = 2.0
m.C_FIELD = 0.40
m.DAMP = 0.35

TARGET_MAX = 0.010


def main() -> None:
    lat = m.Lattice3D.build(m.NL_PHYS, m.PW, m.H)
    zero = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 88)
    print("SOURCE-DRIVEN FIELD RECOVERY H=0.25 POCKET")
    print("  smallest serious refinement test for the source-driven field branch")
    print("=" * 88)
    print(f"h={m.H}, W={m.PW}, L={m.NL_PHYS}, c={m.C_FIELD:.2f}, damp={m.DAMP:.2f}, target_max={TARGET_MAX:.3f}")
    print()

    ref_raw = m._source_driven_field_layers_raw(lat, max(m.SOURCE_STRENGTHS), m.SOURCE_Z)
    ref_max = m._field_abs_max(ref_raw)
    gain = TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    zero_dynamic = m._scale_field_layers(m._source_driven_field_layers_raw(lat, 0.0, m.SOURCE_Z), gain)
    zero_amps = lat.propagate(zero_dynamic, m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print(f"  calibration gain: {gain:.6e}")
    print()
    print(f"{'s':>8s} {'inst':>12s} {'dynamic':>12s} {'dyn/inst':>10s} {'max|f_dyn|':>12s}")
    print("-" * 68)

    inst_vals: list[float] = []
    dyn_vals: list[float] = []
    ratios: list[float] = []

    for s in m.SOURCE_STRENGTHS:
        inst_field = m._instantaneous_field_layers(lat, s, m.SOURCE_Z)
        dyn_field = m._scale_field_layers(m._source_driven_field_layers_raw(lat, s, m.SOURCE_Z), gain)

        inst_amps = lat.propagate(inst_field, m.K)
        dyn_amps = lat.propagate(dyn_field, m.K)

        inst_delta = m._centroid_z(inst_amps, lat) - z_free
        dyn_delta = m._centroid_z(dyn_amps, lat) - z_free
        ratio = dyn_delta / inst_delta if abs(inst_delta) > 1e-30 else float("nan")
        dyn_max = max(abs(v) for row in dyn_field for v in row)

        inst_vals.append(inst_delta)
        dyn_vals.append(dyn_delta)
        ratios.append(abs(ratio))

        print(f"{s:8.4f} {inst_delta:+12.6e} {dyn_delta:+12.6e} {ratio:10.3f} {dyn_max:12.6e}")

    inst_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), inst_vals)
    dyn_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), dyn_vals)
    toward = sum(1 for v in dyn_vals if v > 0)
    mean_ratio = sum(ratios) / len(ratios)

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  dynamic F~M exponent: {dyn_alpha:.2f}" if dyn_alpha is not None else "  dynamic F~M exponent: n/a")
    print(f"  dynamic TOWARD rows: {toward}/{len(dyn_vals)}")
    print(f"  mean |dyn/inst| ratio: {mean_ratio:.3f}")
    print("  if the pocket survives refinement, freeze it as a bounded positive")
    print("  otherwise freeze it as the smallest serious refinement falsifier")


if __name__ == "__main__":
    main()
