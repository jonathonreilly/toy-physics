#!/usr/bin/env python3
"""Freeze one exact-lattice weak-field recovery pocket for the source-driven field."""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as msf  # noqa: E402


C_FIELD = 0.40
DAMP = 0.35
TARGET_MAX = 0.01


def main() -> None:
    msf.C_FIELD = C_FIELD
    msf.DAMP = DAMP

    lat = msf.Lattice3D.build(msf.NL_PHYS, msf.PW, msf.H)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, msf.K)
    z_free = msf._centroid_z(free, lat)

    ref_raw = msf._source_driven_field_layers_raw(lat, max(msf.SOURCE_STRENGTHS), msf.SOURCE_Z)
    ref_max = msf._field_abs_max(ref_raw)
    gain = TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    zero_dynamic = msf._scale_field_layers(msf._source_driven_field_layers_raw(lat, 0.0, msf.SOURCE_Z), gain)
    zero_amps = lat.propagate(zero_dynamic, msf.K)
    zero_delta = msf._centroid_z(zero_amps, lat) - z_free

    print("=" * 88)
    print("SOURCE-DRIVEN FIELD RECOVERY POCKET")
    print("  exact 3D lattice, telegraph-style field, one conservative weak-field row")
    print("=" * 88)
    print(f"h={msf.H}, W={msf.PW}, L={msf.NL_PHYS}, c_field={C_FIELD}, damp={DAMP}, target_max={TARGET_MAX}")
    print()
    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print(f"  calibration gain: {gain:.6e}")
    print()
    print(f"{'s':>8s} {'inst':>12s} {'dynamic':>12s} {'dyn/inst':>10s} {'max|f_dyn|':>12s}")
    print("-" * 68)

    inst_vals = []
    dyn_vals = []
    ratios = []

    for s in msf.SOURCE_STRENGTHS:
        inst_field = msf._instantaneous_field_layers(lat, s, msf.SOURCE_Z)
        dyn_field = msf._scale_field_layers(msf._source_driven_field_layers_raw(lat, s, msf.SOURCE_Z), gain)

        inst_amps = lat.propagate(inst_field, msf.K)
        dyn_amps = lat.propagate(dyn_field, msf.K)

        inst_delta = msf._centroid_z(inst_amps, lat) - z_free
        dyn_delta = msf._centroid_z(dyn_amps, lat) - z_free
        ratio = dyn_delta / inst_delta if abs(inst_delta) > 1e-30 else float("nan")
        dyn_max = max(abs(v) for row in dyn_field for v in row)

        inst_vals.append(inst_delta)
        dyn_vals.append(dyn_delta)
        ratios.append(abs(ratio))

        print(f"{s:8.4f} {inst_delta:+12.6e} {dyn_delta:+12.6e} {ratio:10.3f} {dyn_max:12.6e}")

    inst_alpha = msf._fit_power(list(msf.SOURCE_STRENGTHS), inst_vals)
    dyn_alpha = msf._fit_power(list(msf.SOURCE_STRENGTHS), dyn_vals)
    toward = sum(1 for v in dyn_vals if v > 0)
    mean_ratio = sum(ratios) / len(ratios)

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  dynamic F~M exponent: {dyn_alpha:.2f}" if dyn_alpha is not None else "  dynamic F~M exponent: n/a")
    print(f"  dynamic TOWARD rows: {toward}/{len(dyn_vals)}")
    print(f"  mean |dyn/inst| ratio: {mean_ratio:.3f}")
    print("  this pocket only counts as a real weak-field recovery if sign stays all-TOWARD,")
    print("  the dynamic exponent stays near 1.00, and the amplitude remains nontrivial.")


if __name__ == "__main__":
    main()
