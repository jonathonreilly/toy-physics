#!/usr/bin/env python3
"""3D modular gravity mass-scaling follow-up.

This script keeps the corrected propagator fixed, holds the modular gap in the
retained 3D regime, fixes the impact parameter b, and varies the mass count M.
It compares gap=3 and gap=5 under the same paired per-seed delta logic:

  delta(seed, M) = mean_k[ y_with_mass - y_without_mass ]

Then it reports mean delta, paired SE, a 95% CI, delta/M, and a log-log fit
for delta ~ M^alpha when there are enough positive mean-delta points.

The goal is narrow:
- keep b fixed
- keep the modular 3D family fixed
- test whether the retained gravity response scales approximately with mass
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.three_d_joint_test import (  # noqa: E402
    compute_field_3d,
    generate_3d_dag,
    propagate_3d,
)


K_BAND = (3.0, 5.0, 7.0)
GAPS = (3.0, 5.0)
N_SEEDS = 24
MASS_COUNTS = (2, 4, 6, 8, 12)


def centroid_y(probs: dict[int, float], positions: list[tuple[float, float, float]]) -> float:
    total = sum(probs.values())
    if total <= 0:
        return 0.0
    return sum(positions[d][1] * p for d, p in probs.items()) / total


def paired_seed_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
) -> float | None:
    """Return the k-averaged paired delta for one seed and one mass selection."""
    n = len(positions)
    field_with = compute_field_3d(positions, mass_nodes)
    field_without = [0.0] * n

    seed_deltas = []
    for k in K_BAND:
        amps_with = propagate_3d(positions, adj, field_with, src, k)
        amps_without = propagate_3d(positions, adj, field_without, src, k)

        probs_with = {d: abs(amps_with[d]) ** 2 for d in det_list}
        probs_without = {d: abs(amps_without[d]) ** 2 for d in det_list}
        tot_with = sum(probs_with.values())
        tot_without = sum(probs_without.values())
        if tot_with <= 1e-30 or tot_without <= 1e-30:
            continue

        y_with = sum(positions[d][1] * p for d, p in probs_with.items()) / tot_with
        y_without = sum(positions[d][1] * p for d, p in probs_without.items()) / tot_without
        seed_deltas.append(y_with - y_without)

    if not seed_deltas:
        return None
    return sum(seed_deltas) / len(seed_deltas)


def fit_power_law(masses: list[int], deltas: list[float]) -> tuple[float, float, float, float] | None:
    """Fit delta ~= c * M^alpha on positive mean deltas.

    Returns (alpha, alpha_se, c, r2) when there are enough points.
    """
    pairs = [(m, d) for m, d in zip(masses, deltas) if m > 0 and d > 0]
    if len(pairs) < 2:
        return None

    xs = [math.log(m) for m, _ in pairs]
    ys = [math.log(d) for _, d in pairs]
    xbar = statistics.fmean(xs)
    ybar = statistics.fmean(ys)

    ss_xx = sum((x - xbar) ** 2 for x in xs)
    ss_xy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    if ss_xx <= 1e-30:
        return None

    alpha = ss_xy / ss_xx
    intercept = ybar - alpha * xbar
    c = math.exp(intercept)

    ss_tot = sum((y - ybar) ** 2 for y in ys)
    ss_res = sum((y - (intercept + alpha * x)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)

    alpha_se = 0.0
    if len(pairs) >= 3 and ss_xx > 1e-30:
        dof = len(pairs) - 2
        alpha_se = math.sqrt((ss_res / dof) / ss_xx) if dof > 0 else 0.0

    return alpha, alpha_se, c, r2


def mean_se_ci(vals: list[float]) -> tuple[float, float, tuple[float, float]]:
    """Return mean, SE, and an approximate 95% CI."""
    mean = statistics.fmean(vals)
    if len(vals) > 1:
        se = statistics.stdev(vals) / math.sqrt(len(vals))
    else:
        se = 0.0
    ci = (mean - 1.96 * se, mean + 1.96 * se)
    return mean, se, ci


def main() -> None:
    n_layers = 25
    nodes_per_layer = 30
    xyz_range = 12.0
    connect_radius = 4.0
    b = 3.0

    print("=" * 78)
    print("3D MODULAR GRAVITY MASS SCALING")
    print("=" * 78)
    print("  family: 3D modular DAG")
    print(f"  gap sweep: {GAPS}")
    print(f"  fixed impact parameter b: {b}")
    print(f"  k-band: {K_BAND}")
    print(f"  seeds: {N_SEEDS}")
    print("=" * 78)
    print()

    for gap in GAPS:
        by_mass: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}

        for seed in range(N_SEEDS):
            positions, adj = generate_3d_dag(
                n_layers=n_layers,
                nodes_per_layer=nodes_per_layer,
                xyz_range=xyz_range,
                connect_radius=connect_radius,
                rng_seed=seed * 11 + 7,
                gap=gap,
            )

            by_layer = defaultdict(list)
            for idx, (x, y, z) in enumerate(positions):
                by_layer[round(x)].append(idx)

            layers = sorted(by_layer.keys())
            if len(layers) < 7:
                continue

            src = by_layer[layers[0]]
            det_list = list(by_layer[layers[-1]])
            if not det_list:
                continue

            all_ys = [y for _, y, _ in positions]
            cy = statistics.fmean(all_ys)
            grav_layer = layers[2 * len(layers) // 3]
            candidates = [
                i for i in by_layer[grav_layer]
                if positions[i][1] > cy + b
            ]
            candidates.sort(key=lambda i: positions[i][1])
            if not candidates:
                continue

            for mcount in MASS_COUNTS:
                if len(candidates) < mcount:
                    continue
                mass_nodes = candidates[:mcount]
                delta = paired_seed_delta(positions, adj, src, det_list, mass_nodes)
                if delta is not None:
                    by_mass[mcount].append(delta)

        rows: list[tuple[int, float, float, tuple[float, float], float, int]] = []
        for mcount in MASS_COUNTS:
            vals = by_mass[mcount]
            if not vals:
                continue
            mean_delta, se, ci = mean_se_ci(vals)
            rows.append((mcount, mean_delta, se, ci, mean_delta / mcount, len(vals)))

        print(f"  gap={gap:.1f}")
        print(f"  {'M':>4s}  {'mean_delta':>10s}  {'SE':>8s}  {'95% CI':>22s}  {'delta/M':>10s}  {'n_ok':>5s}")
        print(f"  {'-' * 68}")
        for mcount, mean_delta, se, ci, ratio, n_ok in rows:
            print(
                f"  {mcount:4d}  {mean_delta:+10.4f}  {se:8.4f}  "
                f"[{ci[0]:+7.4f}, {ci[1]:+7.4f}]  {ratio:+10.4f}  {n_ok:5d}"
            )

        fit = fit_power_law([r[0] for r in rows], [r[1] for r in rows])
        print()
        if fit is None:
            print("  Power-law fit unavailable (need at least two positive mean-delta points).")
        else:
            alpha, alpha_se, c, r2 = fit
            if alpha_se > 0:
                print(f"  Fit: delta ~= {c:.4f} * M^{alpha:.3f} ± {1.96 * alpha_se:.3f}  (R^2={r2:.3f})")
            else:
                print(f"  Fit: delta ~= {c:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
            print("  Interpretation:")
            print("    alpha ~ 1 would support approximately mass-linear scaling")
            print("    alpha << 1 would indicate sublinear response")
            print("    alpha < 0 would indicate the retained lane fails under mass growth")

        print()

    print("  Summary:")
    print("    - paired per-seed deltas only")
    print("    - fixed modular 3D lanes")
    print("    - fixed impact parameter b")
    print("    - corrected propagator unchanged")


if __name__ == "__main__":
    main()
