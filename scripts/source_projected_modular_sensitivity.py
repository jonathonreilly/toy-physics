#!/usr/bin/env python3
"""Sensitivity sweep for the reopened source-projected modular seam.

Question
--------
Is the source-projected modular partial mover just one exact retained
geometry, or does it persist across a bounded modular class?

This script keeps the controls strict and narrow:
  - modular family only
  - fixed-position / fixed-count mass selection
  - full-sweep-positive fit gate
  - best stable source-projected cell as the main candidate
  - compact sweep over modular family settings only

We vary the modular family geometry a little:
  - gap=3.0 vs gap=5.0
  - lower / higher node density at fixed gap

If the source-projected lane survives these nearby settings, it is a bounded
modular class. If it only works at one exact setting, it is geometry-specific.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_resolved_green_pilot import (  # type: ignore  # noqa: E402
    CONNECT_RADIUS,
    GAP,
    K_BAND,
    MASS_COUNTS,
    MASS_COUNT_FIXED,
    MASS_LAYER_OFFSET,
    N_LAYERS,
    TARGET_BS,
    centroid_y,
    field_laplacian,
    generate_3d_modular_dag,
    propagate,
)
from scripts.source_projected_field_reaudit import field_source_projected  # type: ignore  # noqa: E402


N_SEEDS = 32
PROJECTED_STRENGTH = 0.16
PROJECTED_EPS = 1.00
FIXED_MASS_B = 3.0


@dataclass(frozen=True)
class FamilyConfig:
    label: str
    gap: float
    nodes_per_layer: int
    connect_radius: float = CONNECT_RADIUS


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


def _fit_full_sweep_positive(
    means_by_key: dict[float | int, list[float]],
    keys: list[float | int],
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


def _measure_family(cfg: FamilyConfig) -> dict[str, object]:
    lap_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    lap_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    proj_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    proj_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    accepted_seeds = 0

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=cfg.nodes_per_layer,
            xyz_range=12.0,
            connect_radius=cfg.connect_radius,
            rng_seed=seed * 17 + 3,
            gap=cfg.gap,
        )
        if len(layer_indices) < 7:
            continue

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        accepted_seeds += 1

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        mass_layer = layer_indices[MASS_LAYER_OFFSET]

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(mass_layer, positions, center_y + b, MASS_COUNT_FIXED)
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            lap_delta = _paired_delta(positions, adj, src, det_list, mass_nodes, field_laplacian)
            proj_delta = _paired_delta(
                positions,
                adj,
                src,
                det_list,
                mass_nodes,
                lambda p, a, m: field_source_projected(
                    p,
                    a,
                    m,
                    strength=PROJECTED_STRENGTH,
                    eps=PROJECTED_EPS,
                ),
            )
            if lap_delta is not None:
                lap_b[b].append(lap_delta)
            if proj_delta is not None:
                proj_b[b].append(proj_delta)

        ranked = _select_fixed_mass_nodes(mass_layer, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS))
        if len(ranked) < max(MASS_COUNTS):
            continue
        for m in MASS_COUNTS:
            mass_nodes = ranked[:m]
            lap_delta = _paired_delta(positions, adj, src, det_list, mass_nodes, field_laplacian)
            proj_delta = _paired_delta(
                positions,
                adj,
                src,
                det_list,
                mass_nodes,
                lambda p, a, m_: field_source_projected(
                    p,
                    a,
                    m_,
                    strength=PROJECTED_STRENGTH,
                    eps=PROJECTED_EPS,
                ),
            )
            if lap_delta is not None:
                lap_m[m].append(lap_delta)
            if proj_delta is not None:
                proj_m[m].append(proj_delta)

    lap_b_fit = _fit_full_sweep_positive(lap_b, list(TARGET_BS))
    proj_b_fit = _fit_full_sweep_positive(proj_b, list(TARGET_BS))
    lap_m_fit = _fit_full_sweep_positive(lap_m, list(MASS_COUNTS))
    proj_m_fit = _fit_full_sweep_positive(proj_m, list(MASS_COUNTS))

    return {
        "accepted_seeds": accepted_seeds,
        "lap_b": lap_b_fit,
        "proj_b": proj_b_fit,
        "lap_m": lap_m_fit,
        "proj_m": proj_m_fit,
        "lap_b_means": lap_b,
        "proj_b_means": proj_b,
        "lap_m_means": lap_m,
        "proj_m_means": proj_m,
    }


def _fmt_fit(fit: tuple[float, float, float] | None) -> str:
    if fit is None:
        return "FAIL"
    alpha, coeff, r2 = fit
    return f"{alpha:+.3f} / R^2={r2:.3f}"


def main() -> None:
    configs = [
        FamilyConfig("modular gap=3.0, npl=40", gap=3.0, nodes_per_layer=40),
        FamilyConfig("modular gap=5.0, npl=40", gap=5.0, nodes_per_layer=40),
        FamilyConfig("modular gap=3.0, npl=32", gap=3.0, nodes_per_layer=32),
        FamilyConfig("modular gap=3.0, npl=48", gap=3.0, nodes_per_layer=48),
    ]

    print("=" * 96)
    print("SOURCE-PROJECTED MODULAR SENSITIVITY")
    print("  Best stable candidate: strength=0.16, eps=1.00")
    print("  Controls: fixed-position / fixed-count, full-sweep-positive fit gate")
    print("  Question: bounded modular class or exact retained geometry?")
    print("=" * 96)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count for b-sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass-sweep: {FIXED_MASS_B}")
    print(f"  mass counts: {MASS_COUNTS}")
    print(f"  source-projected cell: strength={PROJECTED_STRENGTH}, eps={PROJECTED_EPS}")
    print()
    print(
        f"{'family':>26s}  {'acc':>3s}  "
        f"{'lap_b':>16s}  {'proj_b':>16s}  {'lap_m':>16s}  {'proj_m':>16s}  verdict"
    )
    print(f"{'-' * 96}")

    for cfg in configs:
        stats = _measure_family(cfg)
        lap_b = stats["lap_b"]
        proj_b = stats["proj_b"]
        lap_m = stats["lap_m"]
        proj_m = stats["proj_m"]
        acc = int(stats["accepted_seeds"])

        proj_ok = proj_b is not None and proj_m is not None
        lap_ok = lap_b is not None and lap_m is not None
        if proj_ok:
            pb = proj_b[0]
            pm = proj_m[0]
            if pb < 0 and pm > 0:
                verdict = "bounded"
            elif pb < 0 or pm > 0:
                verdict = "partial"
            else:
                verdict = "fail"
        else:
            verdict = "fail"

        print(
            f"{cfg.label:>26s}  {acc:3d}  "
            f"{_fmt_fit(lap_b):>16s}  {_fmt_fit(proj_b):>16s}  "
            f"{_fmt_fit(lap_m):>16s}  {_fmt_fit(proj_m):>16s}  {verdict}"
        )

    print()
    print("Interpretation:")
    print("  bounded = source-projected keeps negative b and positive M under strict controls")
    print("  partial = only one axis survives")
    print("  fail = no full-sweep-positive fit survives")
    print("=" * 96)


if __name__ == "__main__":
    main()
