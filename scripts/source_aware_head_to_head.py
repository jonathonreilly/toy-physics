#!/usr/bin/env python3
"""Strict head-to-head on the retained 3D modular source-aware lanes.

This comparison keeps the control discipline aligned with the current review
standard:
  - retained 3D modular family only (gap=3.0)
  - same graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - 32 seeds
  - full-sweep-positive fit gate before reporting a power-law exponent

Modes compared:
  - Laplacian baseline
  - source-resolved Green
  - source-projected node field
  - one bounded additive combination (Laplacian + projected mix=0.25)

The goal is narrow: rank the surviving gravity-side partial movers without
mixing in stale pilot gates or positive-only fit truncation.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.hybrid_field_reaudit import field_laplacian  # type: ignore  # noqa: E402
from scripts.source_projected_field_reaudit import (  # type: ignore  # noqa: E402
    GAP,
    K_BAND,
    MASS_COUNTS,
    MASS_COUNT_FIXED,
    MASS_LAYER_OFFSET,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    _select_fixed_mass_nodes,
    field_source_projected,
)
from scripts.source_resolved_green_pilot import (  # type: ignore  # noqa: E402
    centroid_y,
    generate_3d_modular_dag,
    propagate,
)
from scripts.source_resolved_green_reaudit import field_source_resolved_green  # type: ignore  # noqa: E402


N_SEEDS = 32
MIX = 0.25


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


def _fit_full_positive_power_law(
    keys: list[float | int],
    means_by_key: dict[float | int, list[float]],
) -> tuple[float, float, float] | None:
    xs: list[float] = []
    ys: list[float] = []
    for key in keys:
        vals = means_by_key[key]
        if not vals:
            return None
        mean = _mean(vals)
        if not math.isfinite(mean) or mean <= 0.0:
            return None
        xs.append(float(key))
        ys.append(mean)
    if len(xs) < 3:
        return None
    return _fit_power_law(xs, ys)


def _topo_layers(positions: list[tuple[float, float, float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


def _paired_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_fn,
) -> float | None:
    field_with = field_fn(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)
        deltas.append(
            centroid_y(amps_with, positions, det_list)
            - centroid_y(amps_without, positions, det_list)
        )
    return _mean(deltas) if deltas else None


def _measure_mode(label: str, field_fn) -> dict[str, object]:
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    by_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    valid_seeds = 0

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 17 + 3,
            gap=GAP,
        )
        if len(layer_indices) < 7:
            continue

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        valid_seeds += 1

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mass_layer = layer_indices[MASS_LAYER_OFFSET]

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(
                mass_layer, positions, center_y + b, MASS_COUNT_FIXED
            )
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            delta = _paired_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_b[b].append(delta)

        ranked = _select_fixed_mass_nodes(
            mass_layer, positions, center_y + 3.0, max(MASS_COUNTS)
        )
        if len(ranked) == max(MASS_COUNTS):
            for m in MASS_COUNTS:
                mass_nodes = ranked[:m]
                delta = _paired_delta(positions, adj, src, det_list, mass_nodes, field_fn)
                if delta is not None:
                    by_m[m].append(delta)

    b_fit = _fit_full_positive_power_law(list(TARGET_BS), by_b)
    m_fit = _fit_full_positive_power_law(list(MASS_COUNTS), by_m)

    b_alpha, b_r2 = (b_fit[0], b_fit[2]) if b_fit else (None, None)
    m_alpha, m_r2 = (m_fit[0], m_fit[2]) if m_fit else (None, None)

    return {
        "label": label,
        "valid_seeds": valid_seeds,
        "b_alpha": b_alpha,
        "b_r2": b_r2,
        "m_alpha": m_alpha,
        "m_r2": m_r2,
        "by_b": by_b,
        "by_m": by_m,
    }


def _field_combo(positions, adj, mass_nodes):
    lap = field_laplacian(positions, adj, mass_nodes)
    proj = field_source_projected(positions, adj, mass_nodes)
    return [(1.0 - MIX) * l + MIX * p for l, p in zip(lap, proj)]


def _fmt(val: float | None, width: int = 8) -> str:
    if val is None:
        return f"{'NA':>{width}s}"
    return f"{val:+{width}.3f}"


def _verdict(row: dict[str, object]) -> str:
    b_alpha = row["b_alpha"]
    m_alpha = row["m_alpha"]
    if b_alpha is not None and m_alpha is not None and b_alpha < 0 and m_alpha > 0:
        return "stable"
    if b_alpha is not None and b_alpha < 0:
        return "b-only"
    return "fail"


def main() -> None:
    print("=" * 102)
    print("SOURCE-AWARE HEAD-TO-HEAD")
    print("  retained 3D modular family: gap=3.0")
    print(f"  seeds={N_SEEDS}, full-sweep-positive gate")
    print("  modes: Laplacian, source-resolved Green, source-projected, Laplacian+projected mix=0.25")
    print("=" * 102)
    print()

    rows = [
        _measure_mode("Laplacian", field_laplacian),
        _measure_mode("Source-resolved Green", field_source_resolved_green),
        _measure_mode("Source-projected", field_source_projected),
        _measure_mode("Combo mix=0.25", _field_combo),
    ]

    print(
        f"{'mode':>22s}  {'valid':>5s}  {'b_alpha':>8s}  {'b_R2':>6s}  "
        f"{'M_alpha':>8s}  {'M_R2':>6s}  verdict"
    )
    print(f"{'-' * 92}")

    ranked_rows = []
    for row in rows:
        verdict = _verdict(row)
        ranked_rows.append((verdict, row))
        print(
            f"{row['label']:>22s}  {row['valid_seeds']:5d}  "
            f"{_fmt(row['b_alpha'])}  {_fmt(row['b_r2'], 6)}  "
            f"{_fmt(row['m_alpha'])}  {_fmt(row['m_r2'], 6)}  {verdict}"
        )

    print()
    print("RANKING")
    def sort_key(item):
        verdict, row = item
        b_alpha = row["b_alpha"] if row["b_alpha"] is not None else 999.0
        m_alpha = row["m_alpha"] if row["m_alpha"] is not None else -999.0
        return (0 if verdict == "stable" else 1 if verdict == "b-only" else 2, b_alpha, -m_alpha)

    for idx, (verdict, row) in enumerate(sorted(ranked_rows, key=sort_key), start=1):
        print(
            f"  {idx}. {row['label']}: {verdict}, "
            f"b alpha={_fmt(row['b_alpha'])}, M alpha={_fmt(row['m_alpha'])}"
        )

    print()
    print("REVIEW-SAFE TAKEAWAY")
    print("  Use the ranking above as the current order of surviving source-aware partial movers.")
    print("  Keep anything that is only b-only or modular-specific narrow until a new mechanism changes the result.")
    print("=" * 102)


if __name__ == "__main__":
    main()
