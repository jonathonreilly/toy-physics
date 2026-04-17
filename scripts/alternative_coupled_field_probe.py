#!/usr/bin/env python3
"""Alternative minimal coupled-field probe via edge-carried transport.

This is intentionally distinct from the telegraph-style source-driven field:

- no local wave-equation / telegraph recurrence
- instead, a one-way edge-carried transport rule moves field forward through
  the exact 3D lattice

Question:
  Can this smallest alternative field architecture still recover the weak-field
  gravity lane with exact zero-source reduction, TOWARD sign, and near-linear
  mass scaling?
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.minimal_source_driven_field_probe import (  # noqa: E402
    H,
    K,
    Lattice3D,
    _centroid_z,
)


NL_PHYS = 30
PW = 6
SOURCE_Z = 3.0
SOURCE_STRENGTHS = (0.001, 0.002, 0.004, 0.008)
FIELD_TARGET_MAX = 0.08
TRANSPORT_DECAY = 0.72
TRANSPORT_GAMMA = 0.85


def _field_for_mass(positions: list[tuple[float, float, float]], mass_idx: int, strength: float) -> list[float]:
    mx, my, mz = positions[mass_idx]
    field = []
    for x, y, z in positions:
        r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
        field.append(strength / r)
    return field


def _build_edge_carried_field_layers(
    lat: Lattice3D,
    source_strength: float,
    source_layer: int,
    source_idx: int,
) -> list[list[float]]:
    """Forward edge-carried transport with no second-order time recurrence."""
    fields = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    src_local = source_idx - lat.layer_start[source_layer]
    fields[source_layer][src_local] = source_strength

    for layer in range(source_layer, lat.nl - 1):
        curr = fields[layer]
        nxt = fields[layer + 1]
        for iy in range(-lat.hw, lat.hw + 1):
            for iz in range(-lat.hw, lat.hw + 1):
                src_local = (iy + lat.hw) * lat.nw + (iz + lat.hw)
                amp = curr[src_local]
                if abs(amp) < 1e-30:
                    continue
                for dy, dz, L, w in lat.offsets:
                    jy = iy + dy
                    jz = iz + dz
                    if jy < -lat.hw or jy > lat.hw or jz < -lat.hw or jz > lat.hw:
                        continue
                    dst_local = (jy + lat.hw) * lat.nw + (jz + lat.hw)
                    path_gain = TRANSPORT_DECAY * w / max(L, 1e-12) ** TRANSPORT_GAMMA
                    nxt[dst_local] += amp * path_gain
    return fields


def _scale_field_layers(layers: list[list[float]], scale: float) -> list[list[float]]:
    return [[scale * v for v in row] for row in layers]


def _field_abs_max(layers: list[list[float]]) -> float:
    mx = 0.0
    for row in layers:
        for v in row:
            mx = max(mx, abs(v))
    return mx


def _propagate_with_field(lat: Lattice3D, field_layers: list[list[float]], k: float) -> list[complex]:
    amps = [0j] * lat.n
    src = lat.nmap[(0, 0, 0)]
    amps[src] = 1.0

    for layer in range(lat.nl - 1):
        ls = lat.layer_start[layer]
        ld = lat.layer_start[layer + 1]
        sa = amps[ls : ls + lat.npl]
        if max(abs(a) for a in sa) < 1e-30:
            continue
        sf = field_layers[layer]
        df = field_layers[min(layer + 1, lat.nl - 1)]
        for dy, dz, L, w in lat.offsets:
            ym = max(0, -dy)
            yM = min(lat.nw, lat.nw - dy)
            zm = max(0, -dz)
            zM = min(lat.nw, lat.nw - dz)
            if ym >= yM or zm >= zM:
                continue
            for yi in range(ym, yM):
                for zi in range(zm, zM):
                    si = yi * lat.nw + zi
                    ai = sa[si]
                    if abs(ai) < 1e-30:
                        continue
                    di = (yi + dy) * lat.nw + (zi + dz)
                    lf = 0.5 * (sf[si] + df[di])
                    act = L * (1.0 - lf)
                    amps[ld + di] += ai * complex(math.cos(k * act), math.sin(k * act)) * w / (L * L)
    return amps


def _detector_shift(lat: Lattice3D, amps: list[complex], free: list[complex]) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    det_nodes = range(det_start, det_start + lat.npl)
    def c_z(v: list[complex]) -> float:
        total = 0.0
        weighted = 0.0
        for d in det_nodes:
            p = abs(v[d]) ** 2
            total += p
            weighted += p * lat.pos[d][2]
        return weighted / total if total > 1e-30 else 0.0
    return c_z(amps) - c_z(free)


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
    lat = Lattice3D.build(NL_PHYS, PW, H)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, K)
    z_free = _centroid_z(free, lat)

    gl = lat.nl // 3
    source_layer = gl
    source_idx = min(
        range(lat.layer_start[source_layer], lat.layer_start[source_layer] + lat.npl),
        key=lambda i: (lat.pos[i][1]) ** 2 + (lat.pos[i][2] - SOURCE_Z) ** 2,
    )

    # Precompute a calibration so the source-strength sweep stays in weak field.
    ref_raw = _build_edge_carried_field_layers(lat, max(SOURCE_STRENGTHS), source_layer, source_idx)
    ref_max = _field_abs_max(ref_raw)
    gain = FIELD_TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    print("=" * 82)
    print("ALTERNATIVE COUPLED-FIELD PROBE")
    print("  exact 3D lattice, edge-carried field transport")
    print("  comparison: edge-carried field vs instantaneous 1/r field")
    print("=" * 82)
    print(f"h={H}, W={PW}, L={NL_PHYS}, gain={gain:.6e}, decay={TRANSPORT_DECAY}, gamma={TRANSPORT_GAMMA}")
    print()

    zero_dynamic = _scale_field_layers(_build_edge_carried_field_layers(lat, 0.0, source_layer, source_idx), gain)
    zero_amps = lat.propagate(zero_dynamic, K)
    zero_delta = _centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print()
    print(f"{'s':>8s} {'inst':>12s} {'edge':>12s} {'edge/inst':>10s} {'max|f_edge|':>12s}")
    print("-" * 66)

    inst_vals: list[float] = []
    edge_vals: list[float] = []

    for s in SOURCE_STRENGTHS:
        inst_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
        mx, my, mz = lat.pos[source_idx]
        for layer in range(lat.nl):
            ls = lat.layer_start[layer]
            for i in range(lat.npl):
                x, y, z = lat.pos[ls + i]
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
                inst_field[layer][i] = s / r

        edge_field = _scale_field_layers(
            _build_edge_carried_field_layers(lat, s, source_layer, source_idx), gain
        )

        inst_amps = lat.propagate(inst_field, K)
        edge_amps = lat.propagate(edge_field, K)
        inst_delta = _centroid_z(inst_amps, lat) - z_free
        edge_delta = _centroid_z(edge_amps, lat) - z_free
        ratio = edge_delta / inst_delta if abs(inst_delta) > 1e-30 else math.nan
        max_edge = _field_abs_max(edge_field)

        inst_vals.append(inst_delta)
        edge_vals.append(edge_delta)
        print(f"{s:8.4f} {inst_delta:+12.6e} {edge_delta:+12.6e} {ratio:10.3f} {max_edge:12.6e}")

    inst_alpha = _fit_power(list(SOURCE_STRENGTHS), inst_vals)
    edge_alpha = _fit_power(list(SOURCE_STRENGTHS), edge_vals)

    print()
    print("SAFE READ")
    print(f"  zero-source dynamic field recovers free propagation exactly")
    print(f"  instantaneous TOWARD rows: {sum(1 for v in inst_vals if v > 0)}/{len(inst_vals)}")
    print(f"  edge-carried TOWARD rows: {sum(1 for v in edge_vals if v > 0)}/{len(edge_vals)}")
    if inst_alpha is not None:
        print(f"  instantaneous F~M exponent: {inst_alpha:.2f}")
    if edge_alpha is not None:
        print(f"  edge-carried F~M exponent: {edge_alpha:.2f}")
    print("  if the edge-carried field keeps sign but misses F~M≈1, freeze it as")
    print("  a bounded no-go for the minimal coupled-field architecture")


if __name__ == "__main__":
    main()
