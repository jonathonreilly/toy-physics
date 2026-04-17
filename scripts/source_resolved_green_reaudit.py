#!/usr/bin/env python3
"""Source-resolved Green re-audit under stricter retained controls.

Goal
----
Recheck the source-resolved Green seam on the retained 3D modular family
using the stricter control discipline now used elsewhere in the repo:
  - retained 3D modular DAGs only
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - fixed-position / fixed-count mass sweep
  - larger seed count than the original pilot
  - full-sweep-positive fit gate before reporting a power-law exponent

The question is whether the earlier partial distance-trend improvement
survives honest controls or collapses to an exploratory lane.

PStack experiment: source-resolved-green-reaudit
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.hybrid_field_fixed_mass_pilot import (  # type: ignore  # noqa: E402
    K_BAND,
    MASS_COUNTS,
    MASS_COUNT_FIXED,
    MASS_LAYER_OFFSET,
    N_LAYERS,
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    centroid_y,
    field_laplacian,
    generate_3d_modular_dag,
    propagate,
)
from scripts.source_resolved_green_pilot import (  # type: ignore  # noqa: E402
    GREEN_EPS,
    GREEN_STRENGTH,
    GAP,
    field_source_resolved_green,
)

N_SEEDS = 32
FIXED_MASS_B = 3.0


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
    xs_in: list[float],
    ys_in: list[float],
) -> tuple[float, float, float] | None:
    if len(xs_in) < 3 or any(y <= 0 for y in ys_in):
        return None
    return _fit_power_law(xs_in, ys_in)


def _topo_layers(positions: list[tuple[float, float, float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


def _select_fixed_mass_nodes(
    layer_nodes: list[int],
    positions: list[tuple[float, float, float]],
    target_y: float,
    count: int,
) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _paired_seed_delta(
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


def _measure_b_sweep(label: str, field_fn) -> tuple[float | None, float | None]:
    print(f"[{label}] b-sweep, fixed mass count = {MASS_COUNT_FIXED}")
    print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/b':>8s}  {'samples':>7s}")
    print(f"  {'-' * 44}")

    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
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

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mass_layer = layer_indices[MASS_LAYER_OFFSET]

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(
                mass_layer, positions, center_y + b, MASS_COUNT_FIXED
            )
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            delta = _paired_seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_b[b].append(delta)

    fit_bs: list[float] = []
    fit_shifts: list[float] = []
    saw_nonpositive = False
    for b in TARGET_BS:
        vals = by_b[b]
        if not vals:
            print(f"{b:3d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"{b:3d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / b:+8.3f}  {len(vals):7d}")
        fit_bs.append(float(b))
        fit_shifts.append(shift)
        if shift <= 0:
            saw_nonpositive = True

    fit = _fit_full_positive_power_law(fit_bs, fit_shifts)
    if fit is None:
        if saw_nonpositive:
            print("  Fit: not reported because the full sweep includes non-positive mean shifts")
        else:
            print("  Fit: insufficient positive points for a stable power-law fit")
        return None, None
    alpha, c, r2 = fit
    print(f"  Fit: shift ~= {c:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
    return alpha, r2


def _measure_mass_sweep(label: str, field_fn) -> tuple[float | None, float | None]:
    print(f"[{label}] mass-sweep, fixed b = {FIXED_MASS_B}")
    print(f"  {'M':>4s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/M':>8s}  {'samples':>7s}")
    print(f"  {'-' * 46}")

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
        if len(layer_indices) < 7:
            continue

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mass_layer = layer_indices[MASS_LAYER_OFFSET]
        ranked = _select_fixed_mass_nodes(
            mass_layer, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS)
        )
        if len(ranked) < max(MASS_COUNTS):
            continue

        for m in MASS_COUNTS:
            mass_nodes = ranked[:m]
            delta = _paired_seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_m[m].append(delta)

    fit_ms: list[float] = []
    fit_shifts: list[float] = []
    saw_nonpositive = False
    for m in MASS_COUNTS:
        vals = by_m[m]
        if not vals:
            print(f"{m:4d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"{m:4d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / m:+8.3f}  {len(vals):7d}")
        fit_ms.append(float(m))
        fit_shifts.append(shift)
        if shift <= 0:
            saw_nonpositive = True

    fit = _fit_full_positive_power_law(fit_ms, fit_shifts)
    if fit is None:
        if saw_nonpositive:
            print("  Fit: not reported because the full sweep includes non-positive mean shifts")
        else:
            print("  Fit: insufficient positive points for a stable power-law fit")
        return None, None
    alpha, c, r2 = fit
    print(f"  Fit: shift ~= {c:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
    return alpha, r2


def _sanity_check(field_fn) -> float:
    positions, adj, layer_indices = generate_3d_modular_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        xyz_range=XYZ_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=11,
        gap=GAP,
    )
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
    mass_nodes = _select_fixed_mass_nodes(
        layer_indices[MASS_LAYER_OFFSET], positions, center_y + FIXED_MASS_B, MASS_COUNT_FIXED
    )
    field = field_fn(positions, adj, mass_nodes)
    free = [0.0] * len(positions)
    deltas = []
    for k in (0.0,):
        am = propagate(positions, adj, field, src, k)
        af = propagate(positions, adj, free, src, k)
        deltas.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
    return deltas[0] if deltas else 0.0


def main() -> None:
    print("=" * 78)
    print("SOURCE-RESOLVED GREEN RE-AUDIT")
    print("  Retained 3D modular DAG family")
    print("  Stricter fixed-position / fixed-count controls")
    print("  Full-sweep-positive fit gate")
    print("=" * 78)
    print()
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  k-band: {K_BAND}")
    print(f"  source kernel: sum_m strength/(r + eps), strength={GREEN_STRENGTH}, eps={GREEN_EPS}")
    print(f"  fixed mass count for b-sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass-sweep: {FIXED_MASS_B}")
    print(f"  mass counts: {MASS_COUNTS}")
    print()

    print("K=0 SANITY")
    lap_k0 = _sanity_check(field_laplacian)
    print(f"  baseline Laplacian: k=0 delta = {lap_k0:+.6e}")
    green_k0 = _sanity_check(field_source_resolved_green)
    print(f"  source-resolved Green: k=0 delta = {green_k0:+.6e}")
    print()

    print("=" * 78)
    print("BASELINE (LAPLACIAN RELAXED)")
    print("=" * 78)
    lap_b_alpha, lap_b_r2 = _measure_b_sweep("Laplacian relaxed", field_laplacian)
    print()
    lap_m_alpha, lap_m_r2 = _measure_mass_sweep("Laplacian relaxed", field_laplacian)
    print()

    print("=" * 78)
    print("SOURCE-RESOLVED GREEN")
    print("=" * 78)
    green_b_alpha, green_b_r2 = _measure_b_sweep("Source-resolved Green", field_source_resolved_green)
    print()
    green_m_alpha, green_m_r2 = _measure_mass_sweep("Source-resolved Green", field_source_resolved_green)
    print()

    print("=" * 78)
    print("COMPARISON")
    print(
        f"  Laplacian: b alpha={lap_b_alpha if lap_b_alpha is not None else 'NA'}, "
        f"M alpha={lap_m_alpha if lap_m_alpha is not None else 'NA'}"
    )
    print(
        f"  Green:     b alpha={green_b_alpha if green_b_alpha is not None else 'NA'}, "
        f"M alpha={green_m_alpha if green_m_alpha is not None else 'NA'}"
    )
    if lap_b_alpha is not None and green_b_alpha is not None:
        if green_b_alpha < lap_b_alpha and green_m_alpha is not None and green_m_alpha > 0:
            verdict = "distance trend improved, but mass scaling still survives"
        elif green_b_alpha < lap_b_alpha:
            verdict = "distance trend improved, but the gravity tradeoff is still unclear"
        else:
            verdict = "no distance-law improvement over the Laplacian baseline"
    else:
        verdict = "insufficient data for a stable comparison"
    print(f"  Verdict: {verdict}")
    print("=" * 78)


if __name__ == "__main__":
    main()
