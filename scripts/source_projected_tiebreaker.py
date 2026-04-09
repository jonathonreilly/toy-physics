#!/usr/bin/env python3
"""Apples-to-apples tiebreak for the source-projected modular seam.

Purpose
-------
Resolve the mismatch between:
  - source_projected_modular_sensitivity.py (32 seeds, modular gap=3.0, npl=40)
  - source_projected_bestcell_confirm.py (64 seeds, same nominal cell)

This script uses one shared measurement path for both seed counts and changes
only the number of seeds. The geometry, mass-selection rule, field function,
and fit gate are identical across the two runs.

Question
--------
Is the sign change in the fitted source-projected b exponent a seed-count
softening effect, or does it come from a script/path mismatch?

PStack experiment: source-projected-tiebreaker
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

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
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
)


@dataclass(frozen=True)
class SeedRun:
    seeds: int
    label: str


BEST_STRENGTH = 0.16
BEST_EPS = 1.00
FIXED_MASS_B = 3.0
SEED_RUNS = (
    SeedRun(32, "32-SEED"),
    SeedRun(64, "64-SEED"),
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


def _fit_full_positive_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float, float] | None:
    if len(xs_in) < 3 or any(y <= 0 for y in ys_in):
        return None
    return _fit_power_law(xs_in, ys_in)


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


def _measure_seed_count(seed_count: int) -> dict[str, object]:
    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    by_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}

    for seed in range(seed_count):
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
            delta = _paired_delta(
                positions,
                adj,
                src,
                det_list,
                mass_nodes,
                lambda p, a, m: field_source_projected(
                    p,
                    a,
                    m,
                    strength=BEST_STRENGTH,
                    eps=BEST_EPS,
                ),
            )
            if delta is not None:
                by_b[b].append(delta)

        ranked = _select_fixed_mass_nodes(
            mass_layer, positions, center_y + FIXED_MASS_B, max(MASS_COUNTS)
        )
        if len(ranked) < max(MASS_COUNTS):
            continue
        for m in MASS_COUNTS:
            mass_nodes = ranked[:m]
            delta = _paired_delta(
                positions,
                adj,
                src,
                det_list,
                mass_nodes,
                lambda p, a, m_: field_source_projected(
                    p,
                    a,
                    m_,
                    strength=BEST_STRENGTH,
                    eps=BEST_EPS,
                ),
            )
            if delta is not None:
                by_m[m].append(delta)

    b_fit = _fit_full_positive_power_law(list(TARGET_BS), [_mean(by_b[b]) for b in TARGET_BS])
    m_fit = _fit_full_positive_power_law(list(MASS_COUNTS), [_mean(by_m[m]) for m in MASS_COUNTS])

    return {
        "by_b": by_b,
        "by_m": by_m,
        "b_fit": b_fit,
        "m_fit": m_fit,
    }


def _fmt_fit_parts(fit: tuple[float, float, float] | None) -> tuple[str, str]:
    if fit is None:
        return "FAIL", "NA"
    alpha, _, r2 = fit
    return f"{alpha:+.3f}", f"{r2:.3f}"


def main() -> None:
    print("=" * 104)
    print("SOURCE-PROJECTED TIEBREAKER")
    print("  family: modular gap=3.0, npl=40")
    print(f"  same code path for every run; only seed count changes")
    print(f"  best cell: strength={BEST_STRENGTH:.2f}, eps={BEST_EPS:.2f}")
    print(f"  fixed mass count for b-sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass-sweep: {FIXED_MASS_B}")
    print(f"  k-band: {K_BAND}")
    print("=" * 104)
    print()

    results: dict[int, dict[str, object]] = {}
    for run in SEED_RUNS:
        print(f"[{run.label}] running {run.seeds} seeds")
        results[run.seeds] = _measure_seed_count(run.seeds)
        print()

    print("=" * 104)
    print("SIDE-BY-SIDE")
    print(
        f"{'seeds':>5s}  {'b alpha':>14s}  {'b R^2':>8s}  {'M alpha':>14s}  {'M R^2':>8s}  verdict"
    )
    print(f"{'-' * 104}")

    for run in SEED_RUNS:
        res = results[run.seeds]
        b_fit = res["b_fit"]
        m_fit = res["m_fit"]
        verdict = "undetermined"
        if b_fit is not None and m_fit is not None:
            b_alpha = b_fit[0]
            m_alpha = m_fit[0]
            if b_alpha < 0 and m_alpha > 0:
                verdict = "bounded"
            else:
                verdict = "fail"
        elif b_fit is not None or m_fit is not None:
            verdict = "partial"
        else:
            verdict = "fail"

        b_alpha_s, b_r2_s = _fmt_fit_parts(b_fit)
        m_alpha_s, m_r2_s = _fmt_fit_parts(m_fit)
        print(
            f"{run.seeds:5d}  "
            f"{b_alpha_s:>14s}  {b_r2_s:>8s}  "
            f"{m_alpha_s:>14s}  {m_r2_s:>8s}  "
            f"{verdict}"
        )

    print()
    print("INTERPRETATION")
    print("  If 32 and 64 differ in sign on the same code path, the effect is seed-count softening.")
    print("  If they agree here but differ in the existing scripts, the mismatch is wrapper-specific.")
    print("  Keep the claim narrow until this comparison is run.")
    print("=" * 104)


if __name__ == "__main__":
    main()
