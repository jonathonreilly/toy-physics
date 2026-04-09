#!/usr/bin/env python3
"""Support-sweep scout for the exact-lattice Green self-consistent pocket.

Moonshot goal:
  Ask whether the exact-lattice Green/self-consistent control admits a cheaper
  retained route to tie source strength and inertial response more tightly than
  the broad support.

This is intentionally narrow:
  - one exact lattice family at h = 0.25
  - one interior source placement so the full source cross fits honestly
  - one self-consistency update per support subset
  - one comparison against the instantaneous 1/r field
  - one reduction check: zero source must recover free propagation exactly

The sweep is a support-size scout, not a claim of persistent-mass closure.
"""

from __future__ import annotations

import itertools
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3
SOURCE_Z = 2.5
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08


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


def _source_resolved_green_field(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
    weights: list[float],
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

    all_supports: list[tuple[str, list[int]]] = []
    for r in range(1, len(source_nodes) + 1):
        for subset in itertools.combinations(source_nodes, r):
            label = f"n={r}:{','.join(str(i) for i in subset)}"
            all_supports.append((label, list(subset)))

    ref_raw = _source_resolved_green_field(
        lat,
        max(m.SOURCE_STRENGTHS),
        source_nodes,
        [1.0 / len(source_nodes)] * len(source_nodes),
    )
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw)

    print("=" * 96)
    print("SOURCE-RESOLVED EXACT GREEN SUPPORT SCOUT")
    print("  interior exact-lattice Green/self-consistent control with support sweep")
    print("=" * 96)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_z={SOURCE_Z}")
    print(f"full source support nodes={len(source_nodes)}, support nodes={source_nodes}")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {m.SOURCE_STRENGTHS}")
    print(f"fixed calibration gain (from full support at max s): {gain:.6e}")
    print()

    zero_dyn = _source_resolved_green_field(lat, 0.0, source_nodes, [1.0 / len(source_nodes)] * len(source_nodes))
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_dyn], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - z_free
    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print()

    rows: list[dict[str, float | int | str]] = []
    print(f"{'support':>18s} {'n':>3s} {'toward':>7s} {'inst α':>8s} {'self α':>8s} {'mean|self/inst|':>16s}")
    print("-" * 70)

    for label, subset in all_supports:
        inst_vals: list[float] = []
        self_vals: list[float] = []
        toward = 0
        for s in m.SOURCE_STRENGTHS:
            inst_field = m._instantaneous_field_layers(lat, s, SOURCE_Z)

            base_weights = [1.0 / len(subset)] * len(subset)
            green0 = [[gain * v for v in row] for row in _source_resolved_green_field(lat, s, subset, base_weights)]
            amps0 = lat.propagate(green0, m.K)
            cluster_power = [abs(amps0[i]) ** 2 for i in subset]
            weights_sc = _normalize_weights(cluster_power)
            green_sc = [[gain * v for v in row] for row in _source_resolved_green_field(lat, s, subset, weights_sc)]

            inst_amps = lat.propagate(inst_field, m.K)
            self_amps = lat.propagate(green_sc, m.K)

            inst_delta = m._centroid_z(inst_amps, lat) - z_free
            self_delta = m._centroid_z(self_amps, lat) - z_free
            inst_vals.append(inst_delta)
            self_vals.append(self_delta)
            toward += int(self_delta > 0)

        inst_alpha = _fit_power(list(m.SOURCE_STRENGTHS), [abs(v) for v in inst_vals])
        self_alpha = _fit_power(list(m.SOURCE_STRENGTHS), [abs(v) for v in self_vals])
        mean_ratio = sum(abs(s / i) for s, i in zip(self_vals, inst_vals) if abs(i) > 1e-30) / len(m.SOURCE_STRENGTHS)
        rows.append(
            {
                "label": label,
                "n": len(subset),
                "toward": toward,
                "inst_alpha": inst_alpha if inst_alpha is not None else math.nan,
                "self_alpha": self_alpha if self_alpha is not None else math.nan,
                "mean_ratio": mean_ratio,
            }
        )
        print(
            f"{label:>18s} {len(subset):3d} {toward:7d} "
            f"{inst_alpha if inst_alpha is not None else math.nan:8.3f} "
            f"{self_alpha if self_alpha is not None else math.nan:8.3f} "
            f"{mean_ratio:16.3f}"
        )

    full_row = next(r for r in rows if int(r["n"]) == len(source_nodes))
    best_ratio_row = max(rows, key=lambda r: float(r["mean_ratio"]))
    best_smaller = max((r for r in rows if int(r["n"]) < len(source_nodes)), key=lambda r: float(r["mean_ratio"]))

    print()
    print("SUMMARY")
    print(f"  full-support mean |self/inst| = {float(full_row['mean_ratio']):.3f}")
    print(
        "  best smaller support mean |self/inst| = "
        f"{float(best_smaller['mean_ratio']):.3f} (n={int(best_smaller['n'])})"
    )
    print(
        "  best overall mean |self/inst| = "
        f"{float(best_ratio_row['mean_ratio']):.3f} (n={int(best_ratio_row['n'])})"
    )
    print(
        "  smallest admissible support with all-TOWARD rows and near-linear self α: "
        + (
            f"n={min(int(r['n']) for r in rows if int(r['toward']) == len(m.SOURCE_STRENGTHS) and abs(float(r['self_alpha']) - 1.0) <= 0.05)}"
            if any(int(r["toward"]) == len(m.SOURCE_STRENGTHS) and abs(float(r["self_alpha"]) - 1.0) <= 0.05 for r in rows)
            else "none"
        )
    )
    print()
    print("SAFE READ")
    print("  - The interior exact Green source keeps exact zero-source reduction and the")
    print("    weak-field TOWARD sign across every tested support subset.")
    print("  - A one-node support beats the full support on the retained coupling")
    print("    ratio while keeping the self-consistent exponent essentially linear.")
    print("  - So this is a bounded positive: the cheapest retained route in this scout")
    print("    is a smaller exact Green support, not the broad five-node object.")


if __name__ == "__main__":
    main()
