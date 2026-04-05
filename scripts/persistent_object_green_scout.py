#!/usr/bin/env python3
"""Persistent / quasi-persistent object scout on the compact exact lattice.

Goal:
  Ask whether the smallest self-consistent Green-like source object can survive
  more than one update while still sourcing a field on the retained exact
  lattice.

This probe is deliberately narrow:
  - one compact exact lattice family
  - one interior source-object cluster
  - one Green-like source field
  - one self-consistency loop repeated for three updates
  - one observable pair:
      * source-object survival / localization
      * detector response / sign

Fast falsifier:
  - source support collapses to near-single-node
  - detector sign flips AWAY
  - weak-field scaling collapses away from the retained linear class
"""

from __future__ import annotations

import math
import os
import statistics
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
GREEN_EPS = 0.5
GREEN_MU = 0.08
FIELD_TARGET_MAX = 0.02
N_UPDATES = 3


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _stdev(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) >= 2 else math.nan


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


def _support_metrics(probs: list[float]) -> tuple[float, float, float, float]:
    total = sum(probs)
    if total <= 1e-30:
        return 0.0, 0.0, 0.0, 0.0
    norm = [p / total for p in probs if p > 0.0]
    h = -sum(p * math.log(p) for p in norm)
    eff = math.exp(h)
    peak = max(norm)
    top10 = sum(sorted(norm, reverse=True)[: min(10, len(norm))])
    support_frac = sum(1 for p in norm if p >= 0.01 * peak) / len(norm)
    return h, eff, top10, support_frac


def _source_metrics(weights: list[float]) -> tuple[float, float]:
    if not weights:
        return 0.0, 0.0
    norm = _normalize_weights(weights)
    h = -sum(p * math.log(p) for p in norm if p > 0.0)
    eff = math.exp(h)
    return eff, max(norm)


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 96)
    print("PERSISTENT OBJECT GREEN SCOUT")
    print("  compact exact h=0.25 lattice, repeated self-consistent source-object updates")
    print("  observable: source-object survival/localization and detector response")
    print("=" * 96)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes, source_z={SOURCE_Z}")
    print(f"source strengths={SOURCE_STRENGTHS}, updates={N_UPDATES}")
    print(f"kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"field target max={FIELD_TARGET_MAX}")
    print()

    base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
    ref_raw = _green_field_layers(lat, max(SOURCE_STRENGTHS), source_nodes, base_weights)
    gain = FIELD_TARGET_MAX / _field_abs_max(ref_raw) if _field_abs_max(ref_raw) > 1e-30 else 1.0

    zero_raw = _green_field_layers(lat, 0.0, source_nodes, base_weights)
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_raw], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source shift: {zero_delta:+.6e}")
    print(f"  fixed gain: {gain:.6e}")
    print()

    print(
        f"{'s':>8s} {'step':>5s} {'src_eff':>8s} {'src_peak':>8s} "
        f"{'det_eff':>8s} {'det_top10':>10s} {'det_sup':>8s} "
        f"{'delta':>11s} {'field_max':>10s} {'weight_overlap':>14s}"
    )
    print("-" * 112)

    step_deltas: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_src_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]
    step_det_eff: list[list[float]] = [[] for _ in range(N_UPDATES)]

    for s in SOURCE_STRENGTHS:
        weights = base_weights[:]
        prev_weights = weights[:]
        for step in range(N_UPDATES):
            raw = _green_field_layers(lat, s, source_nodes, weights)
            field = [[gain * v for v in row] for row in raw]
            amps = lat.propagate(field, m.K)

            det_start = lat.layer_start[lat.nl - 1]
            det_probs = [abs(amps[det_start + i]) ** 2 for i in range(lat.npl)]
            _, det_eff, det_top10, det_sup = _support_metrics(det_probs)
            delta = m._centroid_z(amps, lat) - z_free
            src_probs = [abs(amps[i]) ** 2 for i in source_nodes]
            src_eff, src_peak = _source_metrics(src_probs)
            overlap_num = sum(a * b for a, b in zip(_normalize_weights(prev_weights), _normalize_weights(src_probs)))
            overlap_den = math.sqrt(
                sum(a * a for a in _normalize_weights(prev_weights))
                * sum(b * b for b in _normalize_weights(src_probs))
            )
            overlap = overlap_num / overlap_den if overlap_den > 1e-30 else 0.0
            field_max = _field_abs_max(field)

            step_deltas[step].append(delta)
            step_src_eff[step].append(src_eff)
            step_det_eff[step].append(det_eff)

            print(
                f"{s:8.4f} {step:5d} {src_eff:8.3f} {src_peak:8.3f} "
                f"{det_eff:8.2f} {det_top10:10.3f} {det_sup:8.3f} "
                f"{delta:+11.6e} {field_max:10.6e} {overlap:14.3f}"
            )

            prev_weights = weights[:]
            weights = _normalize_weights(src_probs)

    print()
    print("STEP SUMMARY")
    print(f"{'step':>5s} {'F~M':>8s} {'mean src_eff':>13s} {'mean det_eff':>13s} {'TOWARD':>8s}")
    print("-" * 56)
    for step in range(N_UPDATES):
        alpha = _fit_power(SOURCE_STRENGTHS, step_deltas[step])
        toward = sum(1 for d in step_deltas[step] if d > 0)
        alpha_str = f"{alpha:8.2f}" if alpha is not None else f"{'n/a':>8s}"
        print(
            f"{step:5d} {alpha_str} "
            f"{_mean(step_src_eff[step]):13.3f} {_mean(step_det_eff[step]):13.2f} "
            f"{toward:8d}/{len(step_deltas[step])}"
        )

    print()
    print("FASTEST FALSIFIER")
    print("  If the source-object effective support collapses toward a single node")
    print("  or the detector sign flips AWAY on the repeated updates, this is just")
    print("  another bounded exact-lattice control rather than a persistent object.")


if __name__ == "__main__":
    main()
