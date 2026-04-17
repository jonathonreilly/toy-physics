#!/usr/bin/env python3
"""Higher-seed confirmation of the best source-projected stability-map cell.

This is a narrow rerun of the strongest stable cell from the source-projected
stability map:
  - strength = 0.16
  - eps = 1.00

Controls
--------
  - retained 3D modular family only (gap=3.0)
  - same graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - larger seed count than the stability map
  - full-sweep-positive fit gate before reporting a power law

Goal
----
Check whether the best cell keeps the negative-b / positive-M behavior
under stronger statistics, or whether it softens materially.

PStack experiment: source-projected-bestcell-confirm
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

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
    centroid_y,
    field_laplacian,
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
)


N_SEEDS = 64
BEST_STRENGTH = 0.16
BEST_EPS = 1.00
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


def _fit_full_positive_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float, float] | None:
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


def _measure_mode(label: str, field_fn) -> tuple[float | None, float | None]:
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

    print(f"[{label}] b-sweep, fixed mass count = {MASS_COUNT_FIXED}")
    print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/b':>8s}  {'samples':>7s}")
    print(f"  {'-' * 44}")
    fit_bs: list[float] = []
    fit_b_shifts: list[float] = []
    saw_nonpositive_b = False
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
        fit_b_shifts.append(shift)
        if shift <= 0:
            saw_nonpositive_b = True

    b_fit = _fit_full_positive_power_law(fit_bs, fit_b_shifts)
    if b_fit is None:
        if saw_nonpositive_b:
            print("  Fit: not reported because the full sweep includes non-positive mean shifts")
        else:
            print("  Fit: insufficient positive points for a stable power-law fit")
        b_alpha = None
        b_r2 = None
    else:
        b_alpha, _, b_r2 = b_fit
        print(f"  Fit: shift ~= C * b^{b_alpha:.3f}  (R^2={b_r2:.3f})")

    print()
    print(f"[{label}] mass-sweep, fixed b = {FIXED_MASS_B}")
    print(f"  {'M':>4s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift/M':>8s}  {'samples':>7s}")
    print(f"  {'-' * 46}")
    fit_ms: list[float] = []
    fit_m_shifts: list[float] = []
    saw_nonpositive_m = False
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
        fit_m_shifts.append(shift)
        if shift <= 0:
            saw_nonpositive_m = True

    m_fit = _fit_full_positive_power_law(fit_ms, fit_m_shifts)
    if m_fit is None:
        if saw_nonpositive_m:
            print("  Fit: not reported because the full sweep includes non-positive mean shifts")
        else:
            print("  Fit: insufficient positive points for a stable power-law fit")
        m_alpha = None
        m_r2 = None
    else:
        m_alpha, _, m_r2 = m_fit
        print(f"  Fit: shift ~= C * M^{m_alpha:.3f}  (R^2={m_r2:.3f})")

    return b_alpha, m_alpha


def main() -> None:
    print("=" * 86)
    print("SOURCE-PROJECTED BEST-CELL CONFIRMATION")
    print("  retained 3D modular family: gap=3.0")
    print(f"  seeds={N_SEEDS}, full-sweep-positive gate")
    print(f"  best cell: strength={BEST_STRENGTH:.2f}, eps={BEST_EPS:.2f}")
    print("=" * 86)
    print()

    baseline_b, baseline_m = _measure_mode(
        "LAPLACIAN BASELINE",
        lambda positions, adj, mass_nodes: field_laplacian(positions, adj, mass_nodes),
    )
    print()
    best_b, best_m = _measure_mode(
        f"SOURCE-PROJECTED best cell (strength={BEST_STRENGTH:.2f}, eps={BEST_EPS:.2f})",
        lambda positions, adj, mass_nodes: field_source_projected(
            positions, adj, mass_nodes, strength=BEST_STRENGTH, eps=BEST_EPS
        ),
    )

    print()
    print("=" * 86)
    print("COMPARISON")
    print(f"  Laplacian baseline: b alpha = {baseline_b if baseline_b is not None else 'NA'}")
    print(f"  Source-projected best cell: b alpha = {best_b if best_b is not None else 'NA'}")
    print(f"  Laplacian baseline: M alpha = {baseline_m if baseline_m is not None else 'NA'}")
    print(f"  Source-projected best cell: M alpha = {best_m if best_m is not None else 'NA'}")
    print()
    print("REVIEW-SAFE INTERPRETATION")
    if best_b is not None and best_m is not None:
        print("  If the best cell stays negative in b and positive in M, it is a")
        print("  robust modular partial mover; otherwise it is only a narrow pocket.")
    elif best_b is not None:
        print("  The best cell keeps the distance-side move but does not support a")
        print("  full mass-law fit under the stricter gate.")
    else:
        print("  The best cell does not survive the stricter confirm cleanly.")
    print("=" * 86)


if __name__ == "__main__":
    main()
