#!/usr/bin/env python3
"""Source-projected stability map on the retained 3D modular family.

Question
--------
Is the source-projected node-field lane a robust modular regime, or only a
small parameter pocket? This map sweeps the two main source-projected controls:

  - strength
  - eps

under the current control-clean standard:
  - retained 3D modular DAGs only (gap=3.0)
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - larger seed count than the original pilot
  - full-sweep-positive fit gate before reporting a power-law exponent

The goal is narrow: determine whether the negative-b + positive-M result is
robust across a bounded region, or whether it collapses to a narrow pocket.

PStack experiment: source-projected-stability-map
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
    _select_fixed_mass_nodes,
    field_source_projected,
)
from scripts.source_resolved_green_pilot import (  # type: ignore  # noqa: E402
    centroid_y,
    generate_3d_modular_dag,
    propagate,
)


N_SEEDS = 32
STRENGTHS = (0.04, 0.08, 0.12, 0.16)
EPS_VALUES = (0.25, 0.50, 1.00, 2.00)
DEFAULT_STRENGTH = 0.08
DEFAULT_EPS = 0.50


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
    strength: float,
    eps: float,
) -> float | None:
    field_with = field_source_projected(positions, adj, mass_nodes, strength=strength, eps=eps)
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


def _measure_combo(strength: float, eps: float) -> dict[str, object]:
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
            delta = _paired_delta(positions, adj, src, det_list, mass_nodes, strength, eps)
            if delta is not None:
                by_b[b].append(delta)

        ranked = _select_fixed_mass_nodes(
            mass_layer, positions, center_y + 3.0, max(MASS_COUNTS)
        )
        if len(ranked) == max(MASS_COUNTS):
            for m in MASS_COUNTS:
                mass_nodes = ranked[:m]
                delta = _paired_delta(positions, adj, src, det_list, mass_nodes, strength, eps)
                if delta is not None:
                    by_m[m].append(delta)

    b_fit = _fit_full_positive_power_law(list(TARGET_BS), by_b)
    m_fit = _fit_full_positive_power_law(list(MASS_COUNTS), by_m)

    b_alpha, b_r2 = (b_fit[0], b_fit[2]) if b_fit else (None, None)
    m_alpha, m_r2 = (m_fit[0], m_fit[2]) if m_fit else (None, None)

    return {
        "strength": strength,
        "eps": eps,
        "valid_seeds": valid_seeds,
        "b_alpha": b_alpha,
        "b_r2": b_r2,
        "m_alpha": m_alpha,
        "m_r2": m_r2,
        "by_b": by_b,
        "by_m": by_m,
    }


def _fmt(val: float | None, width: int = 8) -> str:
    if val is None:
        return f"{'NA':>{width}s}"
    return f"{val:+{width}.3f}"


def main() -> None:
    print("=" * 100)
    print("SOURCE-PROJECTED STABILITY MAP")
    print("  retained 3D modular family: gap=3.0")
    print(f"  seeds={N_SEEDS}, full-sweep-positive gate")
    print(f"  strength sweep={STRENGTHS}")
    print(f"  eps sweep={EPS_VALUES}")
    print("=" * 100)
    print()

    rows: list[dict[str, object]] = []
    for eps in EPS_VALUES:
        for strength in STRENGTHS:
            rows.append(_measure_combo(strength, eps))

    print(
        f"{'strength':>8s}  {'eps':>5s}  {'valid':>5s}  "
        f"{'b_alpha':>8s}  {'b_R2':>6s}  {'M_alpha':>8s}  {'M_R2':>6s}  verdict"
    )
    print(f"{'-' * 92}")

    stable_rows = []
    distance_only_rows = []
    for row in rows:
        strength = row["strength"]
        eps = row["eps"]
        valid = row["valid_seeds"]
        b_alpha = row["b_alpha"]
        b_r2 = row["b_r2"]
        m_alpha = row["m_alpha"]
        m_r2 = row["m_r2"]

        if b_alpha is not None and m_alpha is not None and b_alpha < 0 and m_alpha > 0:
            verdict = "stable"
            stable_rows.append(row)
        elif b_alpha is not None and b_alpha < 0:
            verdict = "b-only"
            distance_only_rows.append(row)
        else:
            verdict = "fail"

        print(
            f"{strength:8.2f}  {eps:5.2f}  {valid:5d}  "
            f"{_fmt(b_alpha)}  {_fmt(b_r2, 6)}  {_fmt(m_alpha)}  {_fmt(m_r2, 6)}  {verdict}"
        )

    print()
    if stable_rows:
        best = min(stable_rows, key=lambda r: (r["b_alpha"], -r["m_alpha"]))
        print("BEST STABLE REGION")
        print(
            f"  strength={best['strength']:.2f}, eps={best['eps']:.2f}, "
            f"b alpha={best['b_alpha']:+.3f}, M alpha={best['m_alpha']:+.3f}, "
            f"R^2=({best['b_r2']:.3f}, {best['m_r2']:.3f})"
        )
    elif distance_only_rows:
        best = min(distance_only_rows, key=lambda r: r["b_alpha"])
        print("BEST DISTANCE-ONLY REGION")
        print(
            f"  strength={best['strength']:.2f}, eps={best['eps']:.2f}, "
            f"b alpha={best['b_alpha']:+.3f}, M alpha={best['m_alpha'] if best['m_alpha'] is not None else 'NA'}"
        )
    else:
        print("NO NEGATIVE-b REGION SURVIVED")

    print()
    print("REVIEW-SAFE INTERPRETATION")
    print("  Treat the source-projected lane as a bounded modular partial mover only if")
    print("  the stable region above is non-empty. Otherwise it is a narrow pocket.")
    print("=" * 100)


if __name__ == "__main__":
    main()
