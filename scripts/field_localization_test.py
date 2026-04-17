#!/usr/bin/env python3
"""Field localization diagnostic for the b-independence mechanism.

This script compares the retained graph-wide Laplacian field against more
localized alternatives on the same 4D modular family.

The point is narrow:
  - a sharply localized field weakens the gravity signal
  - but it does not recover a clean 1/b distance law
  - the smooth, graph-wide field is what best supports the phase-valley
    picture on the retained modular lane

Review-safe result language:
  - localized fields can reduce signal strength and make the sweep noisier
  - they do not rescue distance falloff on the retained modular family
"""

from __future__ import annotations

import cmath
import math
import os
import statistics
import sys
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.four_d_distance_scaling import (  # noqa: E402
    K_BAND,
    compute_field_4d,
    generate_4d_modular_dag,
    propagate_4d,
    select_mass_nodes,
)

N_SEEDS = 8
N_LAYERS = 18
NODES_PER_LAYER = 40
SPATIAL_RANGE = 8.0
CONNECT_RADIUS = 4.5
GAP = 5.0
TARGET_BS = (1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
MASS_COUNT = 8
MEAN_OFFSET_TOL = 1.0


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _topo_layers(positions: list[tuple[float, float, float, float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


def _weighted_y(amps: list[complex], positions: list[tuple[float, float, float, float]], nodes: list[int]) -> float:
    total = 0.0
    wy = 0.0
    for i in nodes:
        p = abs(amps[i]) ** 2
        total += p
        wy += p * positions[i][1]
    return wy / total if total > 1e-30 else 0.0


def _field_sharp(positions, adj, mass_nodes, strength=0.1):
    field = [0.0] * len(positions)
    mass_set = set(mass_nodes)
    for i in mass_set:
        field[i] = strength
    return field


def _field_gaussian(positions, adj, mass_nodes, sigma=2.0, strength=0.1):
    field = [0.0] * len(positions)
    for m in mass_nodes:
        mx, my, mz, mw = positions[m]
        for i, (x, y, z, w) in enumerate(positions):
            r2 = (x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2 + (w - mw) ** 2
            field[i] += strength * math.exp(-r2 / (2.0 * sigma * sigma))
    return field


def _field_inverse_distance(positions, adj, mass_nodes, cutoff=6.0, strength=0.1):
    field = [0.0] * len(positions)
    for m in mass_nodes:
        mx, my, mz, mw = positions[m]
        for i, (x, y, z, w) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2 + (w - mw) ** 2)
            if r <= cutoff:
                field[i] += strength / (r + 0.1)
    return field


def _field_exponential(positions, adj, mass_nodes, lam=0.5, cutoff=8.0, strength=0.1):
    field = [0.0] * len(positions)
    for m in mass_nodes:
        mx, my, mz, mw = positions[m]
        for i, (x, y, z, w) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2 + (w - mw) ** 2)
            if r <= cutoff:
                field[i] += strength * math.exp(-lam * r)
    return field


def _fit_power_law(bs: list[float], deltas: list[float]) -> tuple[float, float, float] | None:
    pairs = [(b, d) for b, d in zip(bs, deltas) if b > 0 and d > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(b) for b, _ in pairs]
    ys = [math.log(d) for _, d in pairs]
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    alpha = (n * sxy - sx * sy) / denom
    intercept = (sy - alpha * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ys)
    ss_res = sum((y - (alpha * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return alpha, math.exp(intercept), r2


def _paired_seed_delta(
    positions: list[tuple[float, float, float, float]],
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
        amps_with = propagate_4d(positions, adj, field_with, src, k)
        amps_without = propagate_4d(positions, adj, field_without, src, k)
        y_with = _weighted_y(amps_with, positions, det_list)
        y_without = _weighted_y(amps_without, positions, det_list)
        deltas.append(y_with - y_without)
    return _mean(deltas) if deltas else None


def _support_fraction(field: list[float], threshold: float = 1e-4) -> float:
    if not field:
        return 0.0
    return sum(1 for v in field if abs(v) > threshold) / len(field)


def run_family(label: str, field_fn) -> None:
    print(f"[{label}]")
    print(
        f"{'b':>6s}  {'shift':>10s}  {'SE':>8s}  {'t':>6s}  {'shift/b':>9s}  "
        f"{'field_support':>13s}  {'n_ok':>5s}"
    )
    print(f"{'-' * 74}")

    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    support_vals: list[float] = []

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_4d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            spatial_range=SPATIAL_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 13 + 5,
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
        grav_layer = layers[2 * len(layers) // 3]

        for target_b in TARGET_BS:
            mass_nodes = select_mass_nodes(
                by_layer[grav_layer],
                positions,
                center_y,
                target_b,
                MASS_COUNT,
            )
            if not mass_nodes:
                continue
            delta = _paired_seed_delta(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_b[target_b].append(delta)
                support_vals.append(_support_fraction(field_fn(positions, adj, mass_nodes)))

    for target_b in TARGET_BS:
        vals = by_b[target_b]
        if not vals:
            print(f"{target_b:6.2f}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(
            f"{target_b:6.2f}  {shift:+10.4f}  {se:8.4f}  {t:+6.2f}  "
            f"{shift / target_b:+9.4f}  {_mean(support_vals):13.3f}  {len(vals):5d}"
        )

    positive_bs = [b for b, vals in by_b.items() if vals and _mean(vals) > 0]
    positive_shifts = [_mean(by_b[b]) for b in positive_bs]
    fit = _fit_power_law(positive_bs, positive_shifts)
    if fit is not None:
        alpha, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
    else:
        print("  Fit: insufficient positive points for a stable power-law fit")
    print()


def main() -> None:
    print("=" * 78)
    print("FIELD LOCALIZATION TEST")
    print("  Does a more localized field rescue the distance law?")
    print("  Retained family: 4D modular DAGs")
    print("=" * 78)
    print()

    families = [
        ("Laplacian relaxed (baseline)", lambda p, a, m: compute_field_4d(p, a, m)),
        ("Sharp (mass nodes only)", _field_sharp),
        ("Gaussian sigma=2", lambda p, a, m: _field_gaussian(p, a, m, sigma=2.0)),
        ("Gaussian sigma=1", lambda p, a, m: _field_gaussian(p, a, m, sigma=1.0)),
        ("Local 1/r, cutoff=6", lambda p, a, m: _field_inverse_distance(p, a, m, cutoff=6.0)),
        ("Exponential, lambda=0.5", lambda p, a, m: _field_exponential(p, a, m, lam=0.5)),
    ]

    for label, fn in families:
        run_family(label, fn)

    print("=" * 78)
    print("INTERPRETATION")
    print("  Localizing the field can weaken the signal or make it noisier, but")
    print("  the retained modular family still does not recover a clean 1/b law.")
    print("  The smooth graph-wide field remains the best retained explanation")
    print("  for why the phase-valley response is broad and topological rather than")
    print("  geometrically decaying in the current linear path-sum architecture.")
    print("=" * 78)


if __name__ == "__main__":
    main()
