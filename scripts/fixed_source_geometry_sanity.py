#!/usr/bin/env python3
"""Fixed-source geometry sanity check for the retained 3D modular family.

Goal
----
Test whether the improved distance exponents from the source-resolved and
source-projected lanes survive when nearby b values are forced to use
non-overlapping or at least clearly distinct source geometries.

This is a control-clean artifact check:
  - same retained modular family
  - fixed graph geometry per seed
  - compare a standard dense retained family to a denser family
  - track how much overlap the chosen mass windows have across b
  - report distance trends only on seeds that keep the windows distinct

PStack experiment: fixed-source-geometry-sanity
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_projected_field_pilot import (  # type: ignore  # noqa: E402
    GAP,
    K_BAND,
    MASS_COUNT_FIXED,
    N_SEEDS,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    FIXED_MASS_B,
    centroid_y,
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
    _select_fixed_mass_nodes,
)
from scripts.source_resolved_green_pilot import field_source_resolved_green  # type: ignore  # noqa: E402


FAMILIES = (
    ("retained", NODES_PER_LAYER, CONNECT_RADIUS, XYZ_RANGE, GAP),
    ("denser", 60, 4.0, 14.0, GAP),
)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _fit_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float, float] | None:
    pairs = [(x, y) for x, y in zip(xs_in, ys_in) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(x) for x, _ in pairs]
    ys = [math.log(y) for _, y in pairs]
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return slope, math.exp(intercept), r2


def _topo_layers(positions: list[tuple[float, float, float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


def _overlap_fraction(a: list[int], b: list[int]) -> float:
    if not a or not b:
        return 0.0
    inter = len(set(a) & set(b))
    return inter / min(len(a), len(b))


def _paired_seed_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    field: list[float],
) -> float:
    amps_with = propagate(positions, adj, field, src, 5.0)
    amps_without = propagate(positions, adj, [0.0] * len(positions), src, 5.0)
    return centroid_y(amps_with, positions, det_list) - centroid_y(amps_without, positions, det_list)


def _measure_family(nodes_per_layer: int, connect_radius: float, spatial_range: float, gap: float):
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    overlap_rates: list[float] = []
    overlap_maps: list[dict[float, list[int]]] = []

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=nodes_per_layer,
            xyz_range=spatial_range,
            connect_radius=connect_radius,
            rng_seed=seed * 17 + 3,
            gap=gap,
        )
        by_layer = _topo_layers(positions)
        layers = sorted(by_layer)
        if len(layers) < 7:
            continue

        src = by_layer[layers[0]]
        det_list = list(by_layer[layers[-1]])
        if not det_list:
            continue

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mid_layer = layers[len(layers) // 2]
        layer_nodes = by_layer[mid_layer]

        chosen: dict[float, list[int]] = {}
        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + b, MASS_COUNT_FIXED)
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            chosen[b] = mass_nodes

        if len(chosen) < 4:
            continue

        pair_overlaps = []
        sorted_bs = sorted(chosen)
        for i in range(len(sorted_bs) - 1):
            a = chosen[sorted_bs[i]]
            b = chosen[sorted_bs[i + 1]]
            pair_overlaps.append(_overlap_fraction(a, b))
        overlap_rates.append(_mean(pair_overlaps) if pair_overlaps else 0.0)
        overlap_maps.append(chosen)

        for b, mass_nodes in chosen.items():
            # Only keep seeds where adjacent windows are distinctly separated.
            if any(_overlap_fraction(mass_nodes, chosen[b2]) > 0.5 for b2 in chosen if b2 != b):
                continue
            field = field_source_projected(positions, adj, mass_nodes)
            delta = _paired_seed_delta(positions, adj, src, det_list, field)
            by_b[b].append(delta)

    b_pos = [b for b, vals in by_b.items() if vals and _mean(vals) > 0]
    b_shift = [_mean(by_b[b]) for b in b_pos]
    fit = _fit_power_law(b_pos, b_shift)
    return by_b, fit, overlap_rates, len(overlap_maps)


def main() -> None:
    print("=" * 78)
    print("FIXED-SOURCE GEOMETRY SANITY")
    print("  Compare retained and denser families with distinct b windows")
    print("=" * 78)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  fixed mass count: {MASS_COUNT_FIXED}")
    print(f"  k-band: {K_BAND}")
    print()

    for label, nodes_per_layer, connect_radius, spatial_range, gap in FAMILIES:
        print("=" * 78)
        print(f"{label.upper()} FAMILY")
        print("=" * 78)
        by_b, fit, overlap_rates, n_seed_maps = _measure_family(nodes_per_layer, connect_radius, spatial_range, gap)
        print(f"  accepted seed maps: {n_seed_maps}")
        print(f"  mean adjacent-window overlap: {_mean(overlap_rates):.3f}")
        for b in TARGET_BS:
            vals = by_b[b]
            if not vals:
                print(f"  b={b:>2d}: FAIL")
                continue
            shift = _mean(vals)
            se = _se(vals)
            t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
            print(f"  b={b:>2d}: shift={shift:+.4f}, t={t:+.2f}, samples={len(vals)}")
        if fit is None:
            print("  Fit: insufficient positive points")
        else:
            alpha, c, r2 = fit
            print(f"  Fit: shift ~= {c:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
        print()

    print("Interpretation:")
    print("  If the improved exponent is real, it should survive only when the")
    print("  mass windows are distinct enough that nearby b values do not reuse")
    print("  nearly identical nodes.")
    print("=" * 78)


if __name__ == "__main__":
    main()
