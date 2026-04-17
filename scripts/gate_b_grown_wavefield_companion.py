#!/usr/bin/env python3
"""Gate B grown wavefield companion.

This is the fixed-field grown-row companion to the exact-lattice wavefield
mechanism.  It is intentionally narrow:

- retained Gate B grown row only: drift=0.2, restore=0.7
- fixed field, no self-consistent graph update
- exact zero-source reduction check
- same promoted observable as the exact wavefield lane when possible:
  detector-line phase-ramp slope/span relative to the same-site control

The point is to test whether the exact-lattice wavefield mechanism survives as
a narrow grown-row companion without turning into a geometry-generic claim.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.gate_b_grown_joint_package import grow


H = 0.5
NL = 25
PW = 8
DRIFT = 0.2
RESTORE = 0.7
SEEDS = [0, 1]

SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SOURCE_Z = 3.0
SOURCE_LAYERS = [2, 4]
SOURCE_STRENGTHS = [0.001, 0.004, 0.008]
GREEN_EPS = 0.5
GREEN_MU = 0.08
FIELD_TARGET_MAX = 0.02
MEMORY_MIX = 0.9
WAVE_LAG_BLEND = 0.72
WAVE_SPEED2 = 0.16
WAVE_DAMP = 0.18
WAVE_SOURCE_BLEND = 0.52


@dataclass(frozen=True)
class RowResult:
    layer: int
    depth: float
    inst_alpha: float | None
    same_alpha: float | None
    wave_alpha: float | None
    phase_lag: float
    ramp_slope: float
    ramp_r2: float
    ramp_span: float
    wave_same_ratio: float


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


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


def _build_source_nodes(nmap, source_layer: int) -> list[int]:
    src_y = 0
    src_z = round(SOURCE_Z / H)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        key = (source_layer, src_y + dy, src_z + dz)
        idx = nmap.get(key)
        if idx is not None:
            nodes.append(idx)
    return nodes


def _rebuild_nmap(layers: list[list[int]]) -> dict[tuple[int, int, int], int]:
    hw = int(PW / H)
    nmap: dict[tuple[int, int, int], int] = {(0, 0, 0): layers[0][0]}
    for layer_idx in range(1, len(layers)):
        local = 0
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                nmap[(layer_idx, iy, iz)] = layers[layer_idx][local]
                local += 1
    return nmap


def _green_field_layers(
    pos: list[tuple[float, float, float]],
    layers: list[list[int]],
    source_nodes: list[int],
    source_strength: float,
) -> list[list[float]]:
    field: list[list[float]] = [[0.0 for _ in layer_nodes] for layer_nodes in layers]
    if not source_nodes:
        return field
    weights = [1.0 / len(source_nodes)] * len(source_nodes)
    source_pos = [pos[i] for i in source_nodes]
    for layer_idx, layer_nodes in enumerate(layers):
        for local_idx, idx in enumerate(layer_nodes):
            x, y, z = pos[idx]
            val = 0.0
            for w, (mx, my, mz) in zip(weights, source_pos):
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += w * source_strength * math.exp(-GREEN_MU * r) / r
            field[layer_idx][local_idx] = val
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max((abs(v) for row in layers for v in row), default=0.0)


def _same_site_memory_field(green: list[list[float]], mix: float = MEMORY_MIX) -> list[list[float]]:
    field = [[0.0 for _ in row] for row in green]
    if not green:
        return field
    field[0] = green[0][:]
    for layer in range(1, len(green)):
        prev = field[layer - 1]
        curr = green[layer]
        seed = prev[0] if len(prev) == 1 else 0.0
        if layer == 1:
            field[layer] = [mix * seed + (1.0 - mix) * curr[i] for i in range(len(curr))]
        else:
            field[layer] = [mix * prev[i] + (1.0 - mix) * curr[i] for i in range(len(curr))]
    return field


def _transverse_laplacian(values: list[float], hw: int) -> list[float]:
    grid_n = 2 * hw + 1
    out = [0.0 for _ in range(len(values))]
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            k = (iy + hw) * grid_n + (iz + hw)
            center = values[k]
            total = 0.0
            degree = 0
            for dy, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny = iy + dy
                nz = iz + dz
                if -hw <= ny <= hw and -hw <= nz <= hw:
                    nk = (ny + hw) * grid_n + (nz + hw)
                    total += values[nk]
                    degree += 1
            out[k] = total - degree * center
    return out


def _wavefield_layers(green: list[list[float]]) -> list[list[float]]:
    hw = int(PW / H)
    field = [[0.0 for _ in row] for row in green]
    if not green:
        return field
    field[0] = green[0][:]
    if len(green) > 1:
        seed = field[0][0] if field[0] else 0.0
        field[1] = [WAVE_LAG_BLEND * seed + (1.0 - WAVE_LAG_BLEND) * green[1][i] for i in range(len(green[1]))]
    for layer in range(2, len(green)):
        prev = field[layer - 1]
        prev2 = field[layer - 2]
        lap = _transverse_laplacian(prev, hw)
        curr = [0.0 for _ in prev]
        for i in range(len(prev)):
            prev2_i = prev2[i] if len(prev2) > 1 else prev2[0]
            curr[i] = (
                (2.0 - WAVE_DAMP) * prev[i]
                - (1.0 - WAVE_DAMP) * prev2_i
                + WAVE_SPEED2 * lap[i]
                + WAVE_SOURCE_BLEND * green[layer][i]
            )
        field[layer] = curr
    return field


def _flatten_layers(layer_values: list[list[float]], layers: list[list[int]], n: int) -> list[float]:
    out = [0.0 for _ in range(n)]
    for layer_idx, layer_nodes in enumerate(layers):
        row = layer_values[layer_idx]
        for k, idx in enumerate(layer_nodes):
            out[idx] = row[k]
    return out


def _propagate(pos, adj, field_flat: list[float]) -> list[complex]:
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    hm = H * H
    beta = 0.8
    k = 5.0

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field_flat[i] + field_flat[j])
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-beta * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * L * (1.0 - lf)) * w * hm / (L * L)
    return amps


def _detector_line(nmap) -> list[int]:
    row = int(PW / H)
    layer = NL - 1
    out = []
    for iz in range(-row, row + 1):
        idx = nmap.get((layer, 0, iz))
        if idx is not None:
            out.append(idx)
    return out


def _wrap_phase(delta: float) -> float:
    while delta <= -math.pi:
        delta += 2.0 * math.pi
    while delta > math.pi:
        delta -= 2.0 * math.pi
    return delta


def _phase_ramp_metrics(pos, det, same_amps, wave_amps) -> tuple[float, float, float]:
    z_vals = [pos[i][2] for i in det]
    same_probs = [abs(same_amps[i]) ** 2 for i in det]
    wave_probs = [abs(wave_amps[i]) ** 2 for i in det]
    peak = max(max(same_probs), max(wave_probs), 1e-30)
    use = [i for i, (ps, pw) in enumerate(zip(same_probs, wave_probs)) if max(ps, pw) >= 0.02 * peak]
    if len(use) < 3:
        use = [i for i, (ps, pw) in enumerate(zip(same_probs, wave_probs)) if max(ps, pw) >= 1e-4 * peak]
    if len(use) < 3:
        use = list(range(len(det)))

    diffs: list[float] = []
    prev = None
    acc = 0.0
    for j in use:
        d = _wrap_phase(cmath.phase(wave_amps[det[j]]) - cmath.phase(same_amps[det[j]]))
        if prev is None:
            acc = d
        else:
            acc += _wrap_phase(d - prev)
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


def _run_case(pos, adj, layers, nmap, source_layer: int, source_strength: float, z_free: float) -> dict[str, float]:
    source_nodes = _build_source_nodes(nmap, source_layer)
    if not source_nodes:
        raise RuntimeError(f"no source nodes on layer {source_layer}")

    raw_green = _green_field_layers(pos, layers, source_nodes, max(SOURCE_STRENGTHS))
    gain = FIELD_TARGET_MAX / _field_abs_max(raw_green) if _field_abs_max(raw_green) > 1e-30 else 1.0

    inst_green = _green_field_layers(pos, layers, source_nodes, source_strength)
    same_green = _same_site_memory_field(inst_green)
    wave_green = _wavefield_layers(inst_green)

    inst_field = _flatten_layers(inst_green, layers, len(pos))
    same_field = _flatten_layers([[gain * v for v in row] for row in same_green], layers, len(pos))
    wave_field = _flatten_layers([[gain * v for v in row] for row in wave_green], layers, len(pos))

    inst_amps = _propagate(pos, adj, inst_field)
    same_amps = _propagate(pos, adj, same_field)
    wave_amps = _propagate(pos, adj, wave_field)

    det = _detector_line(nmap)
    inst_delta = sum(abs(inst_amps[i]) ** 2 * pos[i][2] for i in det) / max(
        sum(abs(inst_amps[i]) ** 2 for i in det), 1e-30
    ) - z_free
    same_delta = sum(abs(same_amps[i]) ** 2 * pos[i][2] for i in det) / max(
        sum(abs(same_amps[i]) ** 2 for i in det), 1e-30
    ) - z_free
    wave_delta = sum(abs(wave_amps[i]) ** 2 * pos[i][2] for i in det) / max(
        sum(abs(wave_amps[i]) ** 2 for i in det), 1e-30
    ) - z_free

    same_probs = [abs(same_amps[i]) ** 2 for i in det]
    wave_probs = [abs(wave_amps[i]) ** 2 for i in det]
    same_peak = max(range(len(same_probs)), key=lambda i: same_probs[i])
    phase_lag = _wrap_phase(cmath.phase(wave_amps[det[same_peak]]) - cmath.phase(same_amps[det[same_peak]]))
    slope, r2, span = _phase_ramp_metrics(pos, det, same_amps, wave_amps)

    overlap_num = sum((same_amps[i].conjugate() * wave_amps[i]) for i in det)
    same_norm = math.sqrt(sum(abs(same_amps[i]) ** 2 for i in det))
    wave_norm = math.sqrt(sum(abs(wave_amps[i]) ** 2 for i in det))
    overlap = abs(overlap_num) / (same_norm * wave_norm) if same_norm > 1e-30 and wave_norm > 1e-30 else 0.0

    return {
        "inst": inst_delta,
        "same": same_delta,
        "wave": wave_delta,
        "phase_lag": phase_lag,
        "ramp_slope": slope,
        "ramp_r2": r2,
        "ramp_span": span,
        "wave_same_ratio": abs(wave_delta / same_delta) if abs(same_delta) > 1e-30 else 0.0,
        "overlap": overlap,
    }


def main() -> None:
    print("=" * 108)
    print("GATE B GROWN WAVEFIELD COMPANION")
    print("  fixed-field grown-row companion to the exact-lattice wavefield mechanism")
    print("  comparison: instantaneous 1/r vs same-site vs finite-speed wavefield")
    print("  guardrail: exact zero-source reduction must survive")
    print("=" * 108)
    print(f"row: drift={DRIFT}, restore={RESTORE}, seeds={SEEDS}")
    print(f"source_z={SOURCE_Z}, source layers={SOURCE_LAYERS}")
    print(
        f"wavefield constants: memory_mix={MEMORY_MIX}, lag_blend={WAVE_LAG_BLEND}, "
        f"speed2={WAVE_SPEED2}, damp={WAVE_DAMP}, source_blend={WAVE_SOURCE_BLEND}"
    )
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    zero_same_spans: list[float] = []
    zero_wave_spans: list[float] = []
    rows: list[RowResult] = []

    for layer in SOURCE_LAYERS:
        inst_vals: list[float] = []
        same_vals: list[float] = []
        wave_vals: list[float] = []
        phase_lags: list[float] = []
        ramp_slopes: list[float] = []
        ramp_r2s: list[float] = []
        ramp_spans: list[float] = []
        wave_same_ratios: list[float] = []

        for seed in SEEDS:
            pos, adj, layers = grow(DRIFT, RESTORE, seed)
            nmap = _rebuild_nmap(layers)
            det = _detector_line(nmap)
            free = _propagate(pos, adj, [0.0] * len(pos))
            p_free = sum(abs(free[i]) ** 2 for i in det)
            z_free = (
                sum(abs(free[i]) ** 2 * pos[i][2] for i in det) / p_free if p_free > 1e-30 else 0.0
            )

            zero = _run_case(pos, adj, layers, nmap, layer, 0.0, z_free)
            zero_same_spans.append(zero["same"])
            zero_wave_spans.append(zero["wave"])

            for s in SOURCE_STRENGTHS:
                row = _run_case(pos, adj, layers, nmap, layer, s, z_free)
                inst_vals.append(abs(row["inst"]))
                same_vals.append(abs(row["same"]))
                wave_vals.append(abs(row["wave"]))
                phase_lags.append(row["phase_lag"])
                ramp_slopes.append(row["ramp_slope"])
                ramp_r2s.append(row["ramp_r2"])
                ramp_spans.append(row["ramp_span"])
                wave_same_ratios.append(row["wave_same_ratio"])

        repeated_strengths = SOURCE_STRENGTHS * len(SEEDS)
        inst_alpha = _fit_power(repeated_strengths, inst_vals)
        same_alpha = _fit_power(repeated_strengths, same_vals)
        wave_alpha = _fit_power(repeated_strengths, wave_vals)
        depth = (NL - 1 - layer)
        rows.append(
            RowResult(
                layer=layer,
                depth=float(depth),
                inst_alpha=inst_alpha,
                same_alpha=same_alpha,
                wave_alpha=wave_alpha,
                phase_lag=_mean(phase_lags),
                ramp_slope=_mean(ramp_slopes),
                ramp_r2=_mean(ramp_r2s),
                ramp_span=_mean(ramp_spans),
                wave_same_ratio=_mean(wave_same_ratios),
            )
        )

    print("REDUCTION CHECK")
    print(f"  zero-source same-site shift span: {min(zero_same_spans):+.6e} .. {max(zero_same_spans):+.6e}")
    print(f"  zero-source wavefield shift span: {min(zero_wave_spans):+.6e} .. {max(zero_wave_spans):+.6e}")
    print()

    header = (
        f"{'layer':>5s} {'depth':>6s} {'inst F~M':>10s} {'same F~M':>10s} {'wave F~M':>10s} "
        f"{'phase_lag':>10s} {'ramp_slope':>11s} {'ramp_R2':>8s} {'wave/same':>10s}"
    )
    print(header)
    print("-" * len(header))
    for r in rows:
        print(
            f"{r.layer:5d} {r.depth:6.1f} "
            f"{(f'{r.inst_alpha:.3f}' if r.inst_alpha is not None else '  n/a'):>10s} "
            f"{(f'{r.same_alpha:.3f}' if r.same_alpha is not None else '  n/a'):>10s} "
            f"{(f'{r.wave_alpha:.3f}' if r.wave_alpha is not None else '  n/a'):>10s} "
            f"{r.phase_lag:10.3f} {r.ramp_slope:11.4f} {r.ramp_r2:8.3f} {r.wave_same_ratio:10.3f}"
        )

    print()
    print("SAFE READ")
    print("  This is a fixed-field grown-row companion only.")
    print("  Exact zero-source reduction survives if the printed zero spans are zero.")
    print("  The promoted observable is the detector-line phase ramp relative to the same-site control.")
    print("  If the ramp is flat or the wavefield fails to beat the same-site control,")
    print("  this should be written up as a bounded no-go instead of a transfer claim.")


if __name__ == "__main__":
    main()
