#!/usr/bin/env python3
"""Wavefield mechanism probe on the retained larger exact family.

This probe keeps the exact-lattice wavefield lane but asks a more
mechanistic question than the phase-ramp law alone:

  - does the detector-line phase-ramp coefficient depend systematically on
    source-detector depth, while still preserving exact zero-source reduction
    and near-linear weak-field scaling?

The goal is not another law fit for its own sake.  The goal is to separate a
true propagating-field mechanism from a mere source-strength rescaling by
scanning the source layer while keeping the same retained exact family.
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
from typing import Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.source_resolved_wavefield_escalation as esc  # noqa: E402


H = esc.H
NL_PHYS = esc.NL_PHYS
PW = esc.PW
SOURCE_CLUSTER = esc.SOURCE_CLUSTER
SOURCE_Z = esc.SOURCE_Z
SOURCE_STRENGTHS = [0.0005, 0.001, 0.002, 0.004, 0.008]
SOURCE_LAYER_VALUES = [1, 2, 3, 4]
REFERENCE_STRENGTH = 0.004
FIELD_TARGET_MAX = esc.FIELD_TARGET_MAX
GREEN_EPS = esc.GREEN_EPS
GREEN_MU = esc.GREEN_MU
MEMORY_MIX = esc.MEMORY_MIX
WAVE_LAG_BLEND = esc.WAVE_LAG_BLEND
WAVE_SPEED2 = esc.WAVE_SPEED2
WAVE_DAMP = esc.WAVE_DAMP
WAVE_SOURCE_BLEND = esc.WAVE_SOURCE_BLEND


def _source_cluster_nodes(lat: esc.m.Lattice3D, source_layer: int) -> list[int]:
    src_y = lat.hw
    src_z = lat.hw + round(SOURCE_Z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw and 0 <= source_layer < lat.nl:
            nodes.append(lat.nmap[(source_layer, y - lat.hw, z - lat.hw)])
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
    gain: float,
) -> dict[str, float]:
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
    }


def _source_depth_fit(depths: list[float], values: list[float]) -> float | None:
    pairs = [(d, abs(v)) for d, v in zip(depths, values) if d > 0 and abs(v) > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(d) for d, _ in pairs]
    ly = [math.log(v) for _, v in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def main() -> None:
    lat = esc.m.Lattice3D.build(NL_PHYS, PW, H)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, esc.m.K)
    z_free = esc.m._centroid_z(free, lat)
    detector_layer = lat.nl - 1

    print("=" * 108)
    print("SOURCE-RESOLVED WAVEFIELD MECHANISM")
    print("  exact-lattice phase-ramp law as a source-depth mechanism")
    print("  comparison: instantaneous 1/r vs same-site vs finite-speed wavefield")
    print("=" * 108)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(SOURCE_CLUSTER)} nodes")
    print(f"source_z={SOURCE_Z}, memory_mix={MEMORY_MIX}, wave_lag_blend={WAVE_LAG_BLEND}")
    print(f"wave_speed2={WAVE_SPEED2}, damp={WAVE_DAMP}, source_blend={WAVE_SOURCE_BLEND}")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"source layers: {SOURCE_LAYER_VALUES} (detector layer={detector_layer})")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    print("REDUCTION CHECK")
    zero_same_all = []
    zero_wave_all = []
    for layer in SOURCE_LAYER_VALUES:
        source_nodes = _source_cluster_nodes(lat, layer)
        zero_same = esc._same_site_memory_field(lat, 0.0, source_nodes)
        zero_wave = esc._wavefield_layers(lat, 0.0, source_nodes)
        zero_same_amps = lat.propagate(zero_same, esc.m.K)
        zero_wave_amps = lat.propagate(zero_wave, esc.m.K)
        zero_same_all.append(esc.m._centroid_z(zero_same_amps, lat) - z_free)
        zero_wave_all.append(esc.m._centroid_z(zero_wave_amps, lat) - z_free)
    print(f"  zero-source same-site shift span: {min(zero_same_all):+.6e} .. {max(zero_same_all):+.6e}")
    print(f"  zero-source wavefield shift span: {min(zero_wave_all):+.6e} .. {max(zero_wave_all):+.6e}")
    print()

    header = (
        f"{'layer':>5s} {'depth':>6s} {'inst':>10s} {'same':>10s} {'wave':>10s} "
        f"{'phase_lag':>10s} {'ramp_slope':>11s} {'ramp_R2':>8s} {'wave/same':>10s}"
    )
    print(header)
    print("-" * len(header))

    layer_rows: list[dict[str, float]] = []

    for source_layer in SOURCE_LAYER_VALUES:
        source_nodes = _source_cluster_nodes(lat, source_layer)
        if not source_nodes:
            continue
        base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
        ref_raw = esc._green_field_layers(lat, max(SOURCE_STRENGTHS), source_nodes, base_weights)
        gain = FIELD_TARGET_MAX / esc._field_abs_max(ref_raw) if esc._field_abs_max(ref_raw) > 1e-30 else 1.0
        z_depth = float(detector_layer - source_layer)

        inst_vals: list[float] = []
        same_vals: list[float] = []
        wave_vals: list[float] = []
        phase_lags: list[float] = []
        ramp_slopes: list[float] = []
        ramp_spans: list[float] = []
        ramp_r2s: list[float] = []
        overlaps: list[float] = []

        ref_row: dict[str, float] | None = None
        for s in SOURCE_STRENGTHS:
            row = _run_case(lat, s, source_nodes, z_free, gain)
            inst_vals.append(row["inst"])
            same_vals.append(row["same"])
            wave_vals.append(row["wave"])
            phase_lags.append(row["phase_lag"])
            ramp_slopes.append(row["phase_ramp_slope"])
            ramp_spans.append(row["phase_ramp_span"])
            ramp_r2s.append(row["phase_ramp_r2"])
            overlaps.append(row["overlap"])
            if abs(s - REFERENCE_STRENGTH) < 1e-12:
                ref_row = row

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
        wave_same_ratio = sum(
            abs(w / s) for w, s in zip(wave_vals, same_vals) if abs(s) > 1e-30
        ) / len([s for s in same_vals if abs(s) > 1e-30])

        layer_rows.append(
            {
                "layer": float(source_layer),
                "depth": z_depth,
                "ramp_ref": ref_row["phase_ramp_slope"] if ref_row else 0.0,
                "span_ref": ref_row["phase_ramp_span"] if ref_row else 0.0,
                "phase_ref": ref_row["phase_lag"] if ref_row else 0.0,
                "inst_alpha": inst_alpha if inst_alpha is not None else float("nan"),
                "same_alpha": same_alpha if same_alpha is not None else float("nan"),
                "wave_alpha": wave_alpha if wave_alpha is not None else float("nan"),
                "slope_alpha": slope_alpha if slope_alpha is not None else float("nan"),
                "span_alpha": span_alpha if span_alpha is not None else float("nan"),
                "toward": float(toward),
                "mean_phase": mean_phase,
                "mean_overlap": mean_overlap,
                "mean_ramp": mean_ramp,
                "mean_r2": mean_r2,
                "mean_span": mean_span,
                "mean_wave_same": mean_wave_same,
                "wave_same_ratio": wave_same_ratio,
            }
        )

        print(
            f"{source_layer:5d} {z_depth:6.1f} "
            f"{inst_alpha:10.2f} {same_alpha:10.2f} {wave_alpha:10.2f} "
            f"{mean_phase:10.3f} {mean_ramp:11.4f} {mean_r2:8.3f} {wave_same_ratio:10.3f}"
        )

    depth_alpha = _source_depth_fit(
        [row["depth"] for row in layer_rows],
        [row["ramp_ref"] for row in layer_rows],
    )
    span_depth_alpha = _source_depth_fit(
        [row["depth"] for row in layer_rows],
        [row["span_ref"] for row in layer_rows],
    )

    print()
    print("MECHANISM READ")
    if depth_alpha is not None:
        print(f"  source-depth scaling of ramp slope: {depth_alpha:.2f}")
    else:
        print("  source-depth scaling of ramp slope: n/a")
    if span_depth_alpha is not None:
        print(f"  source-depth scaling of ramp span: {span_depth_alpha:.2f}")
    else:
        print("  source-depth scaling of ramp span: n/a")
    print("  the phase-ramp observable stays coherent while the source layer moves")
    print("  this is a depth-mechanism probe, not a continuum theorem")


if __name__ == "__main__":
    main()
