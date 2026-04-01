#!/usr/bin/env python3
"""Gradient-coupled phase pilot on retained 3D modular DAGs.

Goal
----
Test whether coupling phase to local edge-wise field gradients, rather than
to absolute scalar field values, improves the distance-law tradeoff on the
retained 3D modular family under fixed-mass controls.

The pilot is intentionally narrow:
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - same detector readout and k-band as the retained 3D lanes
  - one retained scalar field (Laplace-relaxed), but phase accumulation uses
    edge-to-edge field differences

Interpretation discipline:
  - if the gradient-coupled mode lowers the b exponent without wrecking the
    mass trend, that is a partial move
  - if it only weakens the gravity signal or leaves the distance law flat, it
    is not a retained rescue

PStack experiment: gradient-coupled-phase-pilot
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
    BETA,
    centroid_y,
    field_laplacian,
    generate_3d_modular_dag,
    propagate,
)

N_SEEDS = 16
N_LAYERS = 18
NODES_PER_LAYER = 40
XYZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
GAP = 3.0
K_BAND = (3.0, 5.0, 7.0)
TARGET_BS = (1, 2, 3, 4, 5, 6, 7, 8, 10)
MASS_COUNTS = (2, 4, 6, 8, 12, 16)
MASS_COUNT_FIXED = 8
FIXED_MASS_B = 3.0
GAIN_VALUES = (0.5, 1.0, 2.0, 4.0, 8.0)


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


def propagate_gradient_phase(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    k: float,
    gradient_gain: float,
) -> list[complex]:
    """Propagate amplitude with phase tied to local field gradients."""
    n = len(positions)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    # Use the same retained directional attenuation as the baseline lane, but
    # make the phase itself depend on the edge-wise field difference.
    order = sorted(range(n), key=lambda i: positions[i][0])
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        x1, y1, z1 = positions[i]
        for j in adj.get(i, []):
            x2, y2, z2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            weight = math.exp(-BETA * theta * theta)
            delta_f = field[j] - field[i]
            phase = k * gradient_gain * delta_f
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * weight / L
    return amps


def _paired_seed_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_fn,
    *,
    gradient_gain: float | None = None,
) -> float | None:
    field_with = field_fn(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        if gradient_gain is None:
            amps_with = propagate(positions, adj, field_with, src, k)
            amps_without = propagate(positions, adj, field_without, src, k)
        else:
            amps_with = propagate_gradient_phase(
                positions, adj, field_with, src, k, gradient_gain
            )
            amps_without = propagate_gradient_phase(
                positions, adj, field_without, src, k, gradient_gain
            )
        deltas.append(
            centroid_y(amps_with, positions, det_list)
            - centroid_y(amps_without, positions, det_list)
        )
    return _mean(deltas) if deltas else None


def _measure_b_sweep(
    label: str,
    field_fn,
    *,
    gradient_gain: float | None = None,
    gap: float = GAP,
) -> tuple[float | None, float | None]:
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

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(
                layer_nodes, positions, center_y + b, MASS_COUNT_FIXED
            )
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            delta = _paired_seed_delta(
                positions,
                adj,
                src,
                det_list,
                mass_nodes,
                field_fn,
                gradient_gain=gradient_gain,
            )
            if delta is not None:
                by_b[b].append(delta)

    positive_bs = []
    positive_shifts = []
    for b in TARGET_BS:
        vals = by_b[b]
        if not vals:
            print(f"{b:3d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"{b:3d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / b:+8.3f}  {len(vals):7d}")
        if shift > 0:
            positive_bs.append(b)
            positive_shifts.append(shift)

    fit = _fit_power_law(positive_bs, positive_shifts)
    if fit is None:
        print("  Fit: insufficient positive points for a stable power-law fit")
        return None, None
    alpha, c, r2 = fit
    print(f"  Fit: shift ~= {c:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
    return alpha, r2


def _measure_mass_sweep(
    label: str,
    field_fn,
    *,
    gradient_gain: float | None = None,
    gap: float = GAP,
) -> tuple[float | None, float | None]:
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
        mass_nodes = _select_fixed_mass_nodes(
            layer_nodes, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS)
        )
        if not mass_nodes:
            continue

        for m in MASS_COUNTS:
            subset = mass_nodes[:m]
            if len(subset) != m:
                continue
            delta = _paired_seed_delta(
                positions,
                adj,
                src,
                det_list,
                subset,
                field_fn,
                gradient_gain=gradient_gain,
            )
            if delta is not None:
                by_m[m].append(delta)

    positive_ms = []
    positive_shifts = []
    for m in MASS_COUNTS:
        vals = by_m[m]
        if not vals:
            print(f"{m:4d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"{m:4d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift / m:+8.3f}  {len(vals):7d}")
        if shift > 0:
            positive_ms.append(m)
            positive_shifts.append(shift)

    fit = _fit_power_law(positive_ms, positive_shifts)
    if fit is None:
        print("  Fit: insufficient positive points for a stable power-law fit")
        return None, None
    alpha, c, r2 = fit
    print(f"  Fit: shift ~= {c:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
    return alpha, r2


def main() -> None:
    print("=" * 78)
    print("GRADIENT-COUPLED PHASE PILOT")
    print("  Retained 3D modular DAG family")
    print("  Goal: tie phase to local edge-wise field gradients instead of absolute field")
    print("=" * 78)
    print()
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  gap: {GAP}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count for b sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass sweep: {FIXED_MASS_B}")
    print(f"  gradient gains: {GAIN_VALUES}")
    print()

    base_b_alpha, base_b_r2 = _measure_b_sweep("Laplacian baseline", field_laplacian)
    print()
    base_m_alpha, base_m_r2 = _measure_mass_sweep("Laplacian baseline", field_laplacian)
    print()

    rows = []
    for gain in GAIN_VALUES:
        label = f"Gradient-coupled gain={gain:.1f}"
        b_alpha, b_r2 = _measure_b_sweep(
            label,
            field_laplacian,
            gradient_gain=gain,
        )
        print()
        m_alpha, m_r2 = _measure_mass_sweep(
            label,
            field_laplacian,
            gradient_gain=gain,
        )
        print()
        rows.append((gain, b_alpha, b_r2, m_alpha, m_r2))

    print("=" * 78)
    print("SUMMARY")
    print(
        f"  Laplacian baseline: b alpha={base_b_alpha if base_b_alpha is not None else 'NA'}, "
        f"M alpha={base_m_alpha if base_m_alpha is not None else 'NA'}"
    )
    for gain, b_alpha, _b_r2, m_alpha, _m_r2 in rows:
        print(
            f"  gain={gain:.1f}: b alpha={b_alpha if b_alpha is not None else 'NA'}, "
            f"M alpha={m_alpha if m_alpha is not None else 'NA'}"
        )

    finite_rows = [(gain, b_alpha, m_alpha) for gain, b_alpha, _b_r2, m_alpha, _m_r2 in rows if b_alpha is not None and m_alpha is not None]
    if finite_rows:
        best = min(
            finite_rows,
            key=lambda row: (row[1], -row[2]),
        )
        print(
            f"  Best distance trend = gain {best[0]:.1f} with b alpha {best[1]:.3f} "
            f"and mass alpha {best[2]:.3f}"
        )
    print("=" * 78)


if __name__ == "__main__":
    main()
