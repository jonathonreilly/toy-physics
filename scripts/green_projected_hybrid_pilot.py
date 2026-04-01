#!/usr/bin/env python3
"""Green + projected hybrid pilot on retained 3D modular DAGs.

Goal
----
Test whether mixing the source-resolved Green lane with the source-projected
lane can improve the distance / mass tradeoff on the retained 3D modular
family.

This is intentionally narrow:
  - same retained 3D modular family
  - fixed mass count across the b sweep
  - fixed graph geometry per seed
  - same detector readout and k-band
  - compare Laplacian baseline, Green-only, projected-only, and blends

PStack experiment: green-projected-hybrid-pilot
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
    MASS_COUNTS,
    MASS_COUNT_FIXED,
    N_SEEDS,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    FIXED_MASS_B,
    centroid_y,
    field_laplacian,
    generate_3d_modular_dag,
    propagate,
    _select_fixed_mass_nodes,
)
from scripts.source_resolved_green_pilot import field_source_resolved_green  # type: ignore  # noqa: E402
from scripts.source_projected_field_pilot import field_source_projected  # type: ignore  # noqa: E402

MIXES = (0.0, 0.25, 0.5, 0.75, 1.0)


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


def _projected_field(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
) -> list[float]:
    return field_source_projected(positions, adj, mass_nodes)


def _hybrid_field(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    mix: float,
) -> list[float]:
    green = field_source_resolved_green(positions, adj, mass_nodes)
    proj = field_source_projected(positions, adj, mass_nodes)
    return [(1.0 - mix) * g + mix * p for g, p in zip(green, proj)]


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


def _measure(field_builder, label: str):
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    by_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
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

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + b, MASS_COUNT_FIXED)
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            field = field_builder(positions, adj, mass_nodes)
            delta = _paired_seed_delta(positions, adj, src, det_list, field)
            if delta is not None:
                by_b[b].append(delta)

        mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS))
        if len(mass_nodes) == max(MASS_COUNTS):
            for m in MASS_COUNTS:
                field = field_builder(positions, adj, mass_nodes[:m])
                delta = _paired_seed_delta(positions, adj, src, det_list, field)
                if delta is not None:
                    by_m[m].append(delta)

    b_pos = [b for b, vals in by_b.items() if vals and _mean(vals) > 0]
    b_shift = [_mean(by_b[b]) for b in b_pos]
    m_pos = [m for m, vals in by_m.items() if vals and _mean(vals) > 0]
    m_shift = [_mean(by_m[m]) for m in m_pos]
    b_fit = _fit_power_law(b_pos, b_shift)
    m_fit = _fit_power_law(m_pos, m_shift)
    return by_b, by_m, b_fit, m_fit


def main() -> None:
    print("=" * 78)
    print("GREEN + PROJECTED HYBRID PILOT")
    print("  Retained 3D modular DAG family")
    print("  Question: can Green + projection beat either alone?")
    print("=" * 78)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass sweep: {FIXED_MASS_B}")
    print(f"  mixes: {MIXES}")
    print()

    modes = [
        ("Laplacian", lambda p, a, m: field_laplacian(p, a, m)),
        ("Green only", lambda p, a, m: field_source_resolved_green(p, a, m)),
        ("Projected only", lambda p, a, m: _projected_field(p, a, m)),
    ]

    for mix in MIXES:
        modes.append((f"Hybrid mix={mix:.2f}", lambda p, a, m, mix=mix: _hybrid_field(p, a, m, mix)))

    summary = []
    for label, fn in modes:
        print("=" * 78)
        print(label.upper())
        print("=" * 78)
        by_b, by_m, b_fit, m_fit = _measure(fn, label)
        print("  b-sweep summary")
        for b in TARGET_BS:
            vals = by_b[b]
            if not vals:
                print(f"    b={b:>2d}: FAIL")
                continue
            shift = _mean(vals)
            se = _se(vals)
            t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
            print(f"    b={b:>2d}: shift={shift:+.4f}, t={t:+.2f}, samples={len(vals)}")
        print("  mass-sweep summary")
        for m in MASS_COUNTS:
            vals = by_m[m]
            if not vals:
                print(f"    M={m:>2d}: FAIL")
                continue
            shift = _mean(vals)
            se = _se(vals)
            t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
            print(f"    M={m:>2d}: shift={shift:+.4f}, t={t:+.2f}, samples={len(vals)}")
        summary.append(
            (
                label,
                None if b_fit is None else b_fit[0],
                None if m_fit is None else m_fit[0],
            )
        )
        print()

    print("=" * 78)
    print("COMPARISON")
    for label, b_alpha, m_alpha in summary:
        print(
            f"  {label}: b alpha={'NA' if b_alpha is None else f'{b_alpha:.3f}'} | "
            f"M alpha={'NA' if m_alpha is None else f'{m_alpha:.3f}'}"
        )
    print("  Verdict: the hybrid only counts if it beats both endpoints on both axes.")
    print("=" * 78)


if __name__ == "__main__":
    main()
