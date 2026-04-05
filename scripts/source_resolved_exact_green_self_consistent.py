#!/usr/bin/env python3
"""Self-consistent source-resolved Green pocket on the compact exact lattice.

Moonshot goal:
  Take the exact Green pocket and let the source-cluster weights update from
  the propagated wave once, instead of keeping the source profile fixed by
  hand. This is the smallest serious refinement of the exact-lattice pocket.

This is intentionally narrow:
  - one compact exact lattice family at h = 0.25
  - one source-resolved Green-like kernel
  - one self-consistency update from source-cluster amplitudes
  - one comparison against the instantaneous 1/r comparator
  - one reduction check: zero source must recover free propagation exactly
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
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08


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
    weights: list[float],
) -> list[list[float]]:
    """Source-resolved Green-like field with cluster weights."""
    if not source_nodes:
        return [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    source_pos = [lat.pos[i] for i in source_nodes]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
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
    return max(abs(v) for row in layers for v in row)


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 84)
    print("SOURCE-RESOLVED EXACT GREEN SELF-CONSISTENT")
    print("  compact exact h=0.25 refinement family, one self-consistency update")
    print("  comparison: self-consistent field vs instantaneous 1/r field")
    print("=" * 84)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {m.SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
    ref_raw = _source_resolved_green_field(lat, max(m.SOURCE_STRENGTHS), source_nodes, base_weights)
    ref_max = _field_abs_max(ref_raw)
    gain = FIELD_TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    zero_dyn = _source_resolved_green_field(lat, 0.0, source_nodes, base_weights)
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_dyn], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print(f"  calibration gain: {gain:.6e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'green':>12s} {'green/inst':>11s} {'max|f|':>12s}")
    print("-" * 70)

    inst_vals: list[float] = []
    green_vals: list[float] = []
    ratios: list[float] = []

    for s in m.SOURCE_STRENGTHS:
        inst_field = m._instantaneous_field_layers(lat, s, m.SOURCE_Z)

        # One self-consistency update: build a Green field, propagate once,
        # then reweight the source cluster from the propagated amplitudes.
        green0 = [[gain * v for v in row] for row in _source_resolved_green_field(lat, s, source_nodes, base_weights)]
        amps0 = lat.propagate(green0, m.K)
        cluster_power = [abs(amps0[i]) ** 2 for i in source_nodes]
        weights_sc = _normalize_weights(cluster_power)
        green_field = [[gain * v for v in row] for row in _source_resolved_green_field(lat, s, source_nodes, weights_sc)]

        inst_amps = lat.propagate(inst_field, m.K)
        green_amps = lat.propagate(green_field, m.K)

        inst_delta = m._centroid_z(inst_amps, lat) - z_free
        green_delta = m._centroid_z(green_amps, lat) - z_free
        ratio = green_delta / inst_delta if abs(inst_delta) > 1e-30 else float("nan")

        inst_vals.append(inst_delta)
        green_vals.append(green_delta)
        ratios.append(abs(ratio))

        print(
            f"{s:8.4f} {inst_delta:+12.6e} {green_delta:+12.6e} "
            f"{ratio:11.3f} {max(abs(v) for row in green_field for v in row):12.6e}"
        )

    inst_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), inst_vals)
    green_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), green_vals)
    toward = sum(1 for v in green_vals if v > 0)
    mean_ratio = sum(ratios) / len(ratios)

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  self-consistent Green F~M exponent: {green_alpha:.2f}" if green_alpha is not None else "  self-consistent Green F~M exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(green_vals)}")
    print(f"  mean |green/inst| ratio: {mean_ratio:.3f}")
    print("  this is a refinement-positive pocket, not yet a self-consistent")
    print("  field theory")


if __name__ == "__main__":
    main()
