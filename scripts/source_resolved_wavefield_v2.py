#!/usr/bin/env python3
"""Wavefield v2: source-strength law for the detector-line phase ramp.

This probe keeps the retained exact-lattice wavefield family but asks one
sharper question than the original escalation note:

  - does the promoted detector-line phase-ramp observable itself obey a clean
    source-strength law, while still preserving the exact zero-source
    reduction and the weak-field sign?

The exact-lattice wavefield lane already exists.  This v2 probe tries to turn
it into a cleaner structural discriminator by fitting the phase-ramp slope
and span against source strength on the same retained family.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import cmath
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.source_resolved_wavefield_escalation as esc  # noqa: E402


H = esc.H
NL_PHYS = esc.NL_PHYS
PW = esc.PW
SOURCE_CLUSTER = esc.SOURCE_CLUSTER
SOURCE_Z = esc.SOURCE_Z
SOURCE_STRENGTHS = [0.0005, 0.001, 0.002, 0.004, 0.008]
FIELD_TARGET_MAX = esc.FIELD_TARGET_MAX
GREEN_EPS = esc.GREEN_EPS
GREEN_MU = esc.GREEN_MU
MEMORY_MIX = esc.MEMORY_MIX
WAVE_LAG_BLEND = esc.WAVE_LAG_BLEND
WAVE_SPEED2 = esc.WAVE_SPEED2
WAVE_DAMP = esc.WAVE_DAMP
WAVE_SOURCE_BLEND = esc.WAVE_SOURCE_BLEND


def _source_cluster_nodes(lat: esc.m.Lattice3D) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(SOURCE_Z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    return nodes


def _slope_metrics(
    lat: esc.m.Lattice3D,
    same_amps: list[complex],
    wave_amps: list[complex],
) -> tuple[float, float, float]:
    det_line = esc._detector_line(lat)
    return esc._phase_ramp_metrics(lat, same_amps, wave_amps, det_line)


def _run_case(
    lat: esc.m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    z_free: float,
) -> dict[str, float]:
    base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
    ref_raw = esc._green_field_layers(lat, max(SOURCE_STRENGTHS), source_nodes, base_weights)
    gain = FIELD_TARGET_MAX / esc._field_abs_max(ref_raw) if esc._field_abs_max(ref_raw) > 1e-30 else 1.0

    inst_field = esc.m._instantaneous_field_layers(lat, source_strength, SOURCE_Z)
    same_field = esc._same_site_memory_field(lat, source_strength, source_nodes)
    wave_field = esc._wavefield_layers(lat, source_strength, source_nodes)

    inst_amps = lat.propagate(inst_field, esc.m.K)
    same_amps = lat.propagate([[gain * v for v in row] for row in same_field], esc.m.K)
    wave_amps = lat.propagate([[gain * v for v in row] for row in wave_field], esc.m.K)

    inst_delta = esc.m._centroid_z(inst_amps, lat) - z_free
    same_delta = esc.m._centroid_z(same_amps, lat) - z_free
    wave_delta = esc.m._centroid_z(wave_amps, lat) - z_free

    det_line = esc._detector_line(lat)
    same_probs = [abs(same_amps[i]) ** 2 for i in det_line]
    wave_probs = [abs(wave_amps[i]) ** 2 for i in det_line]
    _, same_eff, same_top10, same_support = esc._support_metrics(same_probs)
    _, wave_eff, wave_top10, wave_support = esc._support_metrics(wave_probs)
    ramp_slope, ramp_r2, ramp_span = _slope_metrics(lat, same_amps, wave_amps)

    same_peak = max(range(len(same_probs)), key=lambda i: same_probs[i])
    wave_peak = max(range(len(wave_probs)), key=lambda i: wave_probs[i])
    same_phase = cmath.phase(same_amps[det_line[same_peak]])
    wave_phase_at_same_peak = cmath.phase(wave_amps[det_line[same_peak]])
    wave_phase_at_wave_peak = cmath.phase(wave_amps[det_line[wave_peak]])
    phase_lag = esc._wrap_phase(wave_phase_at_same_peak - same_phase)
    peak_shift = lat.pos[det_line[wave_peak]][2] - lat.pos[det_line[same_peak]][2]

    overlap_num = sum((same_amps[i].conjugate() * wave_amps[i]) for i in det_line)
    same_norm = math.sqrt(sum(abs(same_amps[i]) ** 2 for i in det_line))
    wave_norm = math.sqrt(sum(abs(wave_amps[i]) ** 2 for i in det_line))
    overlap = abs(overlap_num) / (same_norm * wave_norm) if same_norm > 1e-30 and wave_norm > 1e-30 else 0.0

    return {
        "inst": inst_delta,
        "same": same_delta,
        "wave": wave_delta,
        "same_ratio": abs(same_delta / inst_delta) if abs(inst_delta) > 1e-30 else 0.0,
        "wave_ratio": abs(wave_delta / inst_delta) if abs(inst_delta) > 1e-30 else 0.0,
        "same_eff": same_eff,
        "wave_eff": wave_eff,
        "same_top10": same_top10,
        "wave_top10": wave_top10,
        "same_support": same_support,
        "wave_support": wave_support,
        "phase_lag": phase_lag,
        "phase_ramp_slope": ramp_slope,
        "phase_ramp_r2": ramp_r2,
        "phase_ramp_span": ramp_span,
        "peak_shift": peak_shift,
        "overlap": overlap,
        "wave_phase_at_wave_peak": esc._wrap_phase(wave_phase_at_wave_peak),
    }


def main() -> None:
    lat = esc.m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, esc.m.K)
    z_free = esc.m._centroid_z(free, lat)

    print("=" * 108)
    print("SOURCE-RESOLVED WAVEFIELD V2")
    print("  exact-lattice phase-ramp law on the retained larger family")
    print("  comparison: instantaneous 1/r vs same-site vs finite-speed wavefield")
    print("=" * 108)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes")
    print(f"source_z={SOURCE_Z}, memory_mix={MEMORY_MIX}, wave_lag_blend={WAVE_LAG_BLEND}")
    print(f"wave_speed2={WAVE_SPEED2}, damp={WAVE_DAMP}, source_blend={WAVE_SOURCE_BLEND}")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    zero_same = esc._same_site_memory_field(lat, 0.0, source_nodes)
    zero_wave = esc._wavefield_layers(lat, 0.0, source_nodes)
    zero_same_amps = lat.propagate(zero_same, esc.m.K)
    zero_wave_amps = lat.propagate(zero_wave, esc.m.K)
    same_zero = esc.m._centroid_z(zero_same_amps, lat) - z_free
    wave_zero = esc.m._centroid_z(zero_wave_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source same-site shift: {same_zero:+.6e}")
    print(f"  zero-source wavefield shift: {wave_zero:+.6e}")
    print()

    print(
        f"{'s':>8s} {'inst':>12s} {'same':>12s} {'wave':>12s} "
        f"{'phase_lag':>10s} {'ramp_slope':>11s} {'ramp_R2':>8s} {'wave/same':>10s}"
    )
    print("-" * 108)

    inst_vals: list[float] = []
    same_vals: list[float] = []
    wave_vals: list[float] = []
    phase_lags: list[float] = []
    ramp_slopes: list[float] = []
    ramp_spans: list[float] = []
    ramp_r2s: list[float] = []
    overlaps: list[float] = []

    for s in SOURCE_STRENGTHS:
        row = _run_case(lat, s, source_nodes, z_free)
        inst_vals.append(row["inst"])
        same_vals.append(row["same"])
        wave_vals.append(row["wave"])
        phase_lags.append(row["phase_lag"])
        ramp_slopes.append(row["phase_ramp_slope"])
        ramp_spans.append(row["phase_ramp_span"])
        ramp_r2s.append(row["phase_ramp_r2"])
        overlaps.append(row["overlap"])
        print(
            f"{s:8.4f} {row['inst']:+12.6e} {row['same']:+12.6e} {row['wave']:+12.6e}"
            f" {row['phase_lag']:10.3f} {row['phase_ramp_slope']:11.4f}"
            f" {row['phase_ramp_r2']:8.3f} {row['wave_ratio']:10.3f}"
        )

    inst_alpha = esc._fit_power(SOURCE_STRENGTHS, inst_vals)
    same_alpha = esc._fit_power(SOURCE_STRENGTHS, same_vals)
    wave_alpha = esc._fit_power(SOURCE_STRENGTHS, wave_vals)
    slope_alpha = esc._fit_power(SOURCE_STRENGTHS, [abs(v) for v in ramp_slopes])
    span_alpha = esc._fit_power(SOURCE_STRENGTHS, [abs(v) for v in ramp_spans])

    toward = sum(1 for v in wave_vals if v > 0)
    mean_phase = sum(phase_lags) / len(phase_lags)
    mean_overlap = sum(overlaps) / len(overlaps)
    mean_ramp = sum(ramp_slopes) / len(ramp_slopes)
    mean_r2 = sum(ramp_r2s) / len(ramp_r2s)
    mean_span = sum(ramp_spans) / len(ramp_spans)
    mean_wave_same = sum(abs(w - s) for w, s in zip(wave_vals, same_vals)) / len(wave_vals)
    mean_wave_ratio = sum(abs(w / s) for w, s in zip(wave_vals, same_vals) if abs(s) > 1e-30) / len(
        [s for s in same_vals if abs(s) > 1e-30]
    )

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  same-site-memory F~M exponent: {same_alpha:.2f}" if same_alpha is not None else "  same-site-memory F~M exponent: n/a")
    print(f"  wavefield F~M exponent: {wave_alpha:.2f}" if wave_alpha is not None else "  wavefield F~M exponent: n/a")
    print(f"  phase-ramp slope exponent: {slope_alpha:.2f}" if slope_alpha is not None else "  phase-ramp slope exponent: n/a")
    print(f"  phase-ramp span exponent: {span_alpha:.2f}" if span_alpha is not None else "  phase-ramp span exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(wave_vals)}")
    print(f"  mean detector phase lag at same-site peak: {mean_phase:+.3f} rad")
    print(f"  mean detector phase-ramp slope (wave minus same): {mean_ramp:+.4f} rad / z")
    print(f"  mean detector phase-ramp R^2: {mean_r2:.3f}")
    print(f"  mean detector phase-ramp span: {mean_span:+.3f} rad")
    print(f"  mean detector overlap with same-site baseline: {mean_overlap:.3f}")
    print(f"  mean |wave-same| centroid delta: {mean_wave_same:+.6e}")
    print(f"  mean |wave/same| centroid ratio: {mean_wave_ratio:.3f}")
    print("  this is a phase-ramp law probe, not yet a continuum theorem")


if __name__ == "__main__":
    main()
