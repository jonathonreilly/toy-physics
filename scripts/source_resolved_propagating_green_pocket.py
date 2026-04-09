#!/usr/bin/env python3
"""Source-resolved propagating Green pocket on an exact lattice.

Moonshot goal:
  Turn the exact-lattice source-resolved Green pocket into the smallest causal
  propagating-field harness that can still be compared directly against the
  static Green control and the instantaneous 1/r comparator.

This is intentionally narrow:
  - one exact lattice family
  - one source-resolved Green control
  - one propagating Green-like recurrence with a single memory parameter
  - one comparison against the instantaneous 1/r field
  - one reduction check: zero source must recover free propagation exactly

The propagating field is linear in source strength. The question is whether it
keeps the weak-field sign, stays near-linear in source strength, and remains
nontrivial compared with both the static Green control and the instantaneous
comparator.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.5
NL_PHYS = 20
PW = 3
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08
MEMORY_MIX = 0.9


def _source_cluster_nodes(lat: m.Lattice3D) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(m.SOURCE_Z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    return nodes


def _source_resolved_green_field(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
) -> list[list[float]]:
    if not source_nodes:
        return [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    source_pos = [lat.pos[i] for i in source_nodes]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for mx, my, mz in source_pos:
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += source_strength * math.exp(-GREEN_MU * r) / r
            field[layer][i] = val / len(source_pos)
    return field


def _propagating_green_field(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    mix: float = MEMORY_MIX,
) -> list[list[float]]:
    """Causal recurrence: current layer remembers the previous one."""
    green = _source_resolved_green_field(lat, source_strength, source_nodes)
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        if layer == 0:
            field[layer] = green[layer][:]
        else:
            prev = field[layer - 1]
            curr = green[layer]
            field[layer] = [mix * prev[i] + (1.0 - mix) * curr[i] for i in range(lat.npl)]
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row)


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


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 92)
    print("SOURCE-RESOLVED PROPAGATING GREEN POCKET")
    print("  exact 3D lattice, source-resolved Green control, causal memory recurrence")
    print("  comparison: propagating Green vs static Green vs instantaneous 1/r")
    print("=" * 92)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes, mix={MEMORY_MIX}")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {m.SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    ref_raw = _source_resolved_green_field(lat, max(m.SOURCE_STRENGTHS), source_nodes)
    ref_max = _field_abs_max(ref_raw)
    gain = FIELD_TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    zero_dyn = _propagating_green_field(lat, 0.0, source_nodes, MEMORY_MIX)
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_dyn], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print(f"  calibration gain: {gain:.6e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'green':>12s} {'prop':>12s} {'prop/inst':>11s} {'prop/green':>11s}")
    print("-" * 80)

    inst_vals: list[float] = []
    green_vals: list[float] = []
    prop_vals: list[float] = []
    inst_ratios: list[float] = []
    green_ratios: list[float] = []

    for s in m.SOURCE_STRENGTHS:
        inst_field = m._instantaneous_field_layers(lat, s, m.SOURCE_Z)
        green_field = _source_resolved_green_field(lat, s, source_nodes)
        prop_field = _propagating_green_field(lat, s, source_nodes, MEMORY_MIX)

        inst_amps = lat.propagate(inst_field, m.K)
        green_amps = lat.propagate([[gain * v for v in row] for row in green_field], m.K)
        prop_amps = lat.propagate([[gain * v for v in row] for row in prop_field], m.K)

        inst_delta = m._centroid_z(inst_amps, lat) - z_free
        green_delta = m._centroid_z(green_amps, lat) - z_free
        prop_delta = m._centroid_z(prop_amps, lat) - z_free

        inst_vals.append(inst_delta)
        green_vals.append(green_delta)
        prop_vals.append(prop_delta)
        inst_ratios.append(abs(prop_delta / inst_delta))
        green_ratios.append(abs(prop_delta / green_delta))

        print(
            f"{s:8.4f} {inst_delta:+12.6e} {green_delta:+12.6e} {prop_delta:+12.6e}"
            f" {prop_delta / inst_delta:11.3f} {prop_delta / green_delta:11.3f}"
        )

    inst_alpha = _fit_power(list(m.SOURCE_STRENGTHS), inst_vals)
    green_alpha = _fit_power(list(m.SOURCE_STRENGTHS), green_vals)
    prop_alpha = _fit_power(list(m.SOURCE_STRENGTHS), prop_vals)
    toward = sum(1 for v in prop_vals if v > 0)
    mean_inst_ratio = sum(inst_ratios) / len(inst_ratios)
    mean_green_ratio = sum(green_ratios) / len(green_ratios)
    causal_memory = sum(p - g for p, g in zip(prop_vals, green_vals)) / len(prop_vals)

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  static Green F~M exponent: {green_alpha:.2f}" if green_alpha is not None else "  static Green F~M exponent: n/a")
    print(f"  propagating Green F~M exponent: {prop_alpha:.2f}" if prop_alpha is not None else "  propagating Green F~M exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(prop_vals)}")
    print(f"  mean |prop/inst| ratio: {mean_inst_ratio:.3f}")
    print(f"  mean |prop/green| ratio: {mean_green_ratio:.3f}")
    print(f"  causal memory observable (prop - green): {causal_memory:+.6e}")
    print("  this is a bounded propagating-field pocket, not a full self-consistent GR sector")


if __name__ == "__main__":
    main()
