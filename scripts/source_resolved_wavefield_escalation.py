#!/usr/bin/env python3
"""Wavefield escalation probe on a larger exact lattice family.

Moonshot goal:
  Push the exact-lattice wavefield lane beyond the compact phase-lag pocket by
  testing a larger exact family and a cleaner wave-like detector observable.

This stays narrow:
  - one larger exact lattice family
  - one exact zero-source reduction check
  - one instantaneous 1/r control
  - one same-site-memory control
  - one finite-speed wavefield candidate
  - one weak-field sign / F~M gate
  - one wave-like observable stronger than a single phase lag:
      detector-line phase-ramp slope + phase-span relative to same-site control
"""

from __future__ import annotations

import cmath
import math
import os
import sys
from typing import Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
NL_PHYS = 8
PW = 4
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SOURCE_Z = 2.5
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08
MEMORY_MIX = 0.9
WAVE_LAG_BLEND = 0.72
WAVE_SPEED2 = 0.16
WAVE_DAMP = 0.18
WAVE_SOURCE_BLEND = 0.52


def _source_cluster_nodes(lat: m.Lattice3D) -> list[int]:
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


def _green_field_layers(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    weights: Sequence[float],
) -> list[list[float]]:
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    if not source_nodes:
        return field
    source_pos = [lat.pos[i] for i in source_nodes]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for w, (mx, my, mz) in zip(weights, source_pos):
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += w * source_strength * math.exp(-GREEN_MU * r) / r
            field[layer][i] = val
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row) if layers else 0.0


def _transverse_laplacian(values: Sequence[float], lat: m.Lattice3D) -> list[float]:
    out = [0.0 for _ in range(lat.npl)]
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap[(0, iy, iz)] - lat.layer_start[0]
            center = values[idx]
            total = 0.0
            degree = 0
            for dy, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny = iy + dy
                nz = iz + dz
                if -lat.hw <= ny <= lat.hw and -lat.hw <= nz <= lat.hw:
                    nidx = lat.nmap[(0, ny, nz)] - lat.layer_start[0]
                    total += values[nidx]
                    degree += 1
            out[idx] = total - degree * center
    return out


def _same_site_memory_field(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    mix: float = MEMORY_MIX,
) -> list[list[float]]:
    green = _green_field_layers(lat, source_strength, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        if layer == 0:
            field[layer] = green[layer][:]
        else:
            prev = field[layer - 1]
            curr = green[layer]
            field[layer] = [mix * prev[i] + (1.0 - mix) * curr[i] for i in range(lat.npl)]
    return field


def _wavefield_layers(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    lag_blend: float = WAVE_LAG_BLEND,
    wave_speed2: float = WAVE_SPEED2,
    damp: float = WAVE_DAMP,
    source_blend: float = WAVE_SOURCE_BLEND,
) -> list[list[float]]:
    """Minimal finite-speed wavefield candidate on the exact lattice."""
    green = _green_field_layers(lat, source_strength, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    if lat.nl == 0:
        return field
    field[0] = green[0][:]
    if lat.nl > 1:
        field[1] = [lag_blend * field[0][i] + (1.0 - lag_blend) * green[1][i] for i in range(lat.npl)]
    for layer in range(2, lat.nl):
        prev = field[layer - 1]
        prev2 = field[layer - 2]
        lap = _transverse_laplacian(prev, lat)
        curr = [0.0 for _ in range(lat.npl)]
        for i in range(lat.npl):
            curr[i] = (
                (2.0 - damp) * prev[i]
                - (1.0 - damp) * prev2[i]
                + wave_speed2 * lap[i]
                + source_blend * green[layer][i]
            )
        field[layer] = curr
    return field


def _detector_line(lat: m.Lattice3D) -> list[int]:
    det_start = lat.layer_start[lat.nl - 1]
    return [det_start + (lat.hw * lat.nw + iz) for iz in range(lat.nw)]


def _support_metrics(probs: list[float]) -> tuple[float, float, float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    top10 = sum(sorted(norm, reverse=True)[: min(10, len(norm))])
    peak = max(norm)
    support_frac = sum(1 for p in norm if p >= 0.01 * peak) / len(norm)
    return h, eff, top10, support_frac


def _fit_power(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def _wrap_phase(delta: float) -> float:
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    while delta > math.pi:
        delta -= 2.0 * math.pi
    return delta


def _phase_ramp_metrics(
    lat: m.Lattice3D,
    same_amps: list[complex],
    wave_amps: list[complex],
    det_line: list[int],
) -> tuple[float, float, float]:
    z_vals = [lat.pos[i][2] for i in det_line]
    same_probs = [abs(same_amps[i]) ** 2 for i in det_line]
    wave_probs = [abs(wave_amps[i]) ** 2 for i in det_line]
    peak = max(max(same_probs), max(wave_probs), 1e-30)
    use = [i for i, (ps, pw) in enumerate(zip(same_probs, wave_probs)) if max(ps, pw) >= 0.02 * peak]
    if len(use) < 3:
        use = [i for i, (ps, pw) in enumerate(zip(same_probs, wave_probs)) if max(ps, pw) >= 1e-4 * peak]
    if len(use) < 3:
        use = list(range(len(det_line)))

    diffs: list[float] = []
    acc = 0.0
    prev = None
    for j in use:
        d = _wrap_phase(cmath.phase(wave_amps[det_line[j]]) - cmath.phase(same_amps[det_line[j]]))
        if prev is None:
            acc = d
        else:
            step = _wrap_phase(d - prev)
            acc += step
        diffs.append(acc)
        prev = d

    z_use = [z_vals[j] for j in use]
    mz = sum(z_use) / len(z_use)
    md = sum(diffs) / len(diffs)
    szz = sum((z - mz) ** 2 for z in z_use)
    if szz < 1e-12:
        return 0.0, 0.0, 0.0
    szd = sum((z - mz) * (d - md) for z, d in zip(z_use, diffs))
    slope = szd / szz
    ss_tot = sum((d - md) ** 2 for d in diffs)
    ss_res = sum((d - (slope * (z - mz) + md)) ** 2 for z, d in zip(z_use, diffs))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 0.0
    span = max(diffs) - min(diffs)
    return slope, r2, span


def _run_case(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    z_free: float,
) -> dict[str, float]:
    base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
    ref_raw = _green_field_layers(lat, max(SOURCE_STRENGTHS), source_nodes, base_weights)
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    inst_field = m._instantaneous_field_layers(lat, source_strength, SOURCE_Z)
    same_field = _same_site_memory_field(lat, source_strength, source_nodes)
    wave_field = _wavefield_layers(lat, source_strength, source_nodes)

    inst_amps = lat.propagate(inst_field, m.K)
    same_amps = lat.propagate([[gain * v for v in row] for row in same_field], m.K)
    wave_amps = lat.propagate([[gain * v for v in row] for row in wave_field], m.K)

    inst_delta = m._centroid_z(inst_amps, lat) - z_free
    same_delta = m._centroid_z(same_amps, lat) - z_free
    wave_delta = m._centroid_z(wave_amps, lat) - z_free

    det_line = _detector_line(lat)
    same_probs = [abs(same_amps[i]) ** 2 for i in det_line]
    wave_probs = [abs(wave_amps[i]) ** 2 for i in det_line]
    _, same_eff, same_top10, same_support = _support_metrics(same_probs)
    _, wave_eff, wave_top10, wave_support = _support_metrics(wave_probs)
    ramp_slope, ramp_r2, ramp_span = _phase_ramp_metrics(lat, same_amps, wave_amps, det_line)

    same_peak = max(range(len(same_probs)), key=lambda i: same_probs[i])
    wave_peak = max(range(len(wave_probs)), key=lambda i: wave_probs[i])
    same_phase = cmath.phase(same_amps[det_line[same_peak]])
    wave_phase_at_same_peak = cmath.phase(wave_amps[det_line[same_peak]])
    wave_phase_at_wave_peak = cmath.phase(wave_amps[det_line[wave_peak]])
    phase_lag = _wrap_phase(wave_phase_at_same_peak - same_phase)
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
        "wave_phase_at_wave_peak": _wrap_phase(wave_phase_at_wave_peak),
    }


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 108)
    print("SOURCE-RESOLVED WAVEFIELD ESCALATION")
    print("  larger exact-lattice family with detector-line phase-ramp observable")
    print("  comparison: instantaneous 1/r vs same-site vs finite-speed wavefield")
    print("=" * 108)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes")
    print(f"source_z={SOURCE_Z}, memory_mix={MEMORY_MIX}, wave_lag_blend={WAVE_LAG_BLEND}")
    print(f"wave_speed2={WAVE_SPEED2}, damp={WAVE_DAMP}, source_blend={WAVE_SOURCE_BLEND}")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    zero_same = _same_site_memory_field(lat, 0.0, source_nodes)
    zero_wave = _wavefield_layers(lat, 0.0, source_nodes)
    zero_same_amps = lat.propagate(zero_same, m.K)
    zero_wave_amps = lat.propagate(zero_wave, m.K)
    same_zero = m._centroid_z(zero_same_amps, lat) - z_free
    wave_zero = m._centroid_z(zero_wave_amps, lat) - z_free

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
    ramp_r2s: list[float] = []
    ramp_spans: list[float] = []
    overlaps: list[float] = []

    for s in SOURCE_STRENGTHS:
        row = _run_case(lat, s, source_nodes, z_free)
        inst_vals.append(row["inst"])
        same_vals.append(row["same"])
        wave_vals.append(row["wave"])
        phase_lags.append(row["phase_lag"])
        ramp_slopes.append(row["phase_ramp_slope"])
        ramp_r2s.append(row["phase_ramp_r2"])
        ramp_spans.append(row["phase_ramp_span"])
        overlaps.append(row["overlap"])
        print(
            f"{s:8.4f} {row['inst']:+12.6e} {row['same']:+12.6e} {row['wave']:+12.6e}"
            f" {row['phase_lag']:10.3f} {row['phase_ramp_slope']:11.4f}"
            f" {row['phase_ramp_r2']:8.3f} {row['wave_ratio']:10.3f}"
        )

    inst_alpha = _fit_power(SOURCE_STRENGTHS, inst_vals)
    same_alpha = _fit_power(SOURCE_STRENGTHS, same_vals)
    wave_alpha = _fit_power(SOURCE_STRENGTHS, wave_vals)
    toward = sum(1 for v in wave_vals if v > 0)
    mean_phase = sum(phase_lags) / len(phase_lags)
    mean_overlap = sum(overlaps) / len(overlaps)
    mean_ramp = sum(ramp_slopes) / len(ramp_slopes)
    mean_r2 = sum(ramp_r2s) / len(ramp_r2s)
    mean_span = sum(ramp_spans) / len(ramp_spans)
    mean_wave_same = sum(abs(w - s) for w, s in zip(wave_vals, same_vals)) / len(wave_vals)

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  same-site-memory F~M exponent: {same_alpha:.2f}" if same_alpha is not None else "  same-site-memory F~M exponent: n/a")
    print(f"  wavefield F~M exponent: {wave_alpha:.2f}" if wave_alpha is not None else "  wavefield F~M exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(wave_vals)}")
    print(f"  mean detector phase lag at same-site peak: {mean_phase:+.3f} rad")
    print(f"  mean detector phase-ramp slope (wave minus same): {mean_ramp:+.4f} rad / z")
    print(f"  mean detector phase-ramp R^2: {mean_r2:.3f}")
    print(f"  mean detector phase-ramp span: {mean_span:+.3f} rad")
    print(f"  mean detector overlap with same-site baseline: {mean_overlap:.3f}")
    print(f"  mean |wave-same| centroid delta: {mean_wave_same:+.6e}")
    print("  this is a wavefield escalation, not yet a full self-consistent field theory")


if __name__ == "__main__":
    main()
