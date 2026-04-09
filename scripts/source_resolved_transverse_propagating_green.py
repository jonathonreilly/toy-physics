#!/usr/bin/env python3
"""Transverse-propagating Green field on the exact lattice.

Moonshot goal:
  Go one step beyond same-site memory by adding the smallest local transverse
  transport rule to the exact-lattice Green pocket, then compare it directly
  against the same-site-memory control.

This stays narrow:
  - one compact exact lattice family
  - one source-resolved Green control
  - one same-site memory baseline
  - one transverse-smoothing candidate
  - one reduction check: zero source must recover free propagation exactly
  - one observable: detector support localization vs the same-site control
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SOURCE_Z = 2.0
SOURCE_STRENGTHS = [0.001, 0.002, 0.004, 0.008]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08
MEMORY_MIX = 0.9
TRANSVERSE_MIX = 0.25


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
    weights: list[float],
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


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _transverse_smooth_layer(values: list[float], lat: m.Lattice3D, mix: float) -> list[float]:
    """One transverse local averaging step on the yz grid."""
    out = values[:]
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap[(0, iy, iz)] - lat.layer_start[0]
            nb_vals = [values[idx]]
            if iy > -lat.hw:
                nb_vals.append(values[lat.nmap[(0, iy - 1, iz)] - lat.layer_start[0]])
            if iy < lat.hw:
                nb_vals.append(values[lat.nmap[(0, iy + 1, iz)] - lat.layer_start[0]])
            if iz > -lat.hw:
                nb_vals.append(values[lat.nmap[(0, iy, iz - 1)] - lat.layer_start[0]])
            if iz < lat.hw:
                nb_vals.append(values[lat.nmap[(0, iy, iz + 1)] - lat.layer_start[0]])
            avg = sum(nb_vals) / len(nb_vals)
            out[idx] = (1.0 - mix) * values[idx] + mix * avg
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


def _transverse_propagating_field(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    memory_mix: float = MEMORY_MIX,
    transverse_mix: float = TRANSVERSE_MIX,
) -> list[list[float]]:
    green = _green_field_layers(lat, source_strength, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        if layer == 0:
            field[layer] = green[layer][:]
        else:
            prev = field[layer - 1]
            prev_smooth = _transverse_smooth_layer(prev, lat, transverse_mix)
            curr = green[layer]
            field[layer] = [memory_mix * prev_smooth[i] + (1.0 - memory_mix) * curr[i] for i in range(lat.npl)]
    return field


def _detector_probs(amps: list[complex], lat: m.Lattice3D) -> list[float]:
    det_start = lat.layer_start[lat.nl - 1]
    return [abs(amps[det_start + i]) ** 2 for i in range(lat.npl)]


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


def _run_case(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    zero_free_delta: float,
) -> dict[str, float]:
    base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
    ref_raw = _green_field_layers(lat, max(SOURCE_STRENGTHS), source_nodes, base_weights)
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    inst_field = m._instantaneous_field_layers(lat, source_strength, SOURCE_Z)
    same_field = _same_site_memory_field(lat, source_strength, source_nodes)
    trans_field = _transverse_propagating_field(lat, source_strength, source_nodes)

    inst_amps = lat.propagate(inst_field, m.K)
    same_amps = lat.propagate([[gain * v for v in row] for row in same_field], m.K)
    trans_amps = lat.propagate([[gain * v for v in row] for row in trans_field], m.K)

    inst_delta = m._centroid_z(inst_amps, lat) - zero_free_delta
    same_delta = m._centroid_z(same_amps, lat) - zero_free_delta
    trans_delta = m._centroid_z(trans_amps, lat) - zero_free_delta

    same_probs = _detector_probs(same_amps, lat)
    trans_probs = _detector_probs(trans_amps, lat)
    _, same_eff, same_top10, same_support = _support_metrics(same_probs)
    _, trans_eff, trans_top10, trans_support = _support_metrics(trans_probs)

    return {
        "inst": inst_delta,
        "same": same_delta,
        "trans": trans_delta,
        "same_ratio": abs(same_delta / inst_delta) if abs(inst_delta) > 1e-30 else 0.0,
        "trans_ratio": abs(trans_delta / inst_delta) if abs(inst_delta) > 1e-30 else 0.0,
        "trans_minus_same": trans_delta - same_delta,
        "same_eff": same_eff,
        "trans_eff": trans_eff,
        "same_top10": same_top10,
        "trans_top10": trans_top10,
        "same_support": same_support,
        "trans_support": trans_support,
    }


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 96)
    print("SOURCE-RESOLVED TRANSVERSE PROPAGATING GREEN")
    print("  exact h=0.25 lattice, same-site memory vs transverse-smoothing control")
    print("  comparison: instantaneous 1/r vs same-site vs transverse transport")
    print("=" * 96)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes")
    print(f"source_z={SOURCE_Z}, memory_mix={MEMORY_MIX}, transverse_mix={TRANSVERSE_MIX}")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    zero_same = _same_site_memory_field(lat, 0.0, source_nodes)
    zero_trans = _transverse_propagating_field(lat, 0.0, source_nodes)
    zero_same_amps = lat.propagate(zero_same, m.K)
    zero_trans_amps = lat.propagate(zero_trans, m.K)
    same_zero = m._centroid_z(zero_same_amps, lat) - z_free
    trans_zero = m._centroid_z(zero_trans_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source same-site shift: {same_zero:+.6e}")
    print(f"  zero-source transverse shift: {trans_zero:+.6e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'same':>12s} {'trans':>12s} {'trans/same':>11s} {'trans-same':>12s}")
    print("-" * 80)

    inst_vals: list[float] = []
    same_vals: list[float] = []
    trans_vals: list[float] = []
    support_deltas: list[float] = []

    for s in SOURCE_STRENGTHS:
        row = _run_case(lat, s, source_nodes, z_free)
        inst_vals.append(row["inst"])
        same_vals.append(row["same"])
        trans_vals.append(row["trans"])
        support_deltas.append(row["trans_support"] - row["same_support"])
        print(
            f"{s:8.4f} {row['inst']:+12.6e} {row['same']:+12.6e} {row['trans']:+12.6e}"
            f" {row['trans_ratio']:11.3f} {row['trans_minus_same']:+12.6e}"
        )

    inst_alpha = _fit_power(SOURCE_STRENGTHS, inst_vals)
    same_alpha = _fit_power(SOURCE_STRENGTHS, same_vals)
    trans_alpha = _fit_power(SOURCE_STRENGTHS, trans_vals)
    toward = sum(1 for v in trans_vals if v > 0)

    print()
    print("SUPPORT COMPARISON")
    print(f"  mean (trans support - same support): {sum(support_deltas) / len(support_deltas):+.3e}")
    print("  positive means transverse transport broadens detector support relative to same-site memory")
    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  same-site memory F~M exponent: {same_alpha:.2f}" if same_alpha is not None else "  same-site memory F~M exponent: n/a")
    print(f"  transverse F~M exponent: {trans_alpha:.2f}" if trans_alpha is not None else "  transverse F~M exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(trans_vals)}")
    print("  this is a transverse-transport pocket, not a full propagating field theory")


if __name__ == "__main__":
    main()
