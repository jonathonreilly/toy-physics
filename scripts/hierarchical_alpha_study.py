#!/usr/bin/env python3
"""Hierarchical alpha study under fixed-position / variable-count control.

This local version replaces the mass-position-confounded sweep from the
merged remote script. The question stays the same, but the measurement is
now review-safe:

  - fixed target position per seed
  - variable mass count via prefixes of one ranked list
  - full-sweep-positive gate before reporting alpha
"""

from __future__ import annotations

import math
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_projected_cross_family_pilot import (  # type: ignore  # noqa: E402
    generate_3d_hierarchical_dag,
    generate_3d_modular_dag,
)
from scripts.source_projected_field_pilot import (  # type: ignore  # noqa: E402
    K_BAND,
    XYZ_RANGE,
    centroid_y,
    field_laplacian,
    propagate,
)


N_LAYERS = 15
TARGET_B = 3.0
MASS_LAYER_OFFSET = N_LAYERS // 2
MASS_COUNTS = (1, 2, 4, 6, 8, 12, 16)


def gen_3d_hierarchical(*, rng_seed: int, npl: int = 30, r: float = 3.5, leak: float = 0.05):
    return generate_3d_hierarchical_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=npl,
        yz_range=XYZ_RANGE,
        connect_radius=r,
        rng_seed=rng_seed,
        gap=3.0,
        channel_leak=leak,
    )


def gen_3d_modular(*, rng_seed: int, npl: int = 30, r: float = 3.5, gap: float = 5.0):
    return generate_3d_modular_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=npl,
        xyz_range=XYZ_RANGE,
        connect_radius=r,
        rng_seed=rng_seed,
        gap=gap,
    )


def _select_fixed_position_mass_nodes(layer_nodes, positions, target_y, count):
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _fit_power_law(xs_in, ys_in):
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


def _measure_alpha(gen_fn, n_seeds=20, **kwargs):
    by_count = {n: [] for n in MASS_COUNTS}
    max_count = max(MASS_COUNTS)

    for seed in range(n_seeds):
        positions, adj, layers = gen_fn(rng_seed=seed * 17 + 3, **kwargs)
        src = list(layers[0])
        det_list = list(layers[-1])
        if not src or not det_list or len(layers) <= MASS_LAYER_OFFSET:
            continue

        center_y = statistics.fmean(pos[1] for pos in positions)
        mass_layer = [i for i in layers[MASS_LAYER_OFFSET] if positions[i][1] > center_y + 1]
        ranked = _select_fixed_position_mass_nodes(mass_layer, positions, center_y + TARGET_B, max_count)
        if len(ranked) < max_count:
            continue

        for m in MASS_COUNTS:
            subset = ranked[:m]
            field = field_laplacian(positions, adj, subset)
            free = [0.0] * len(positions)
            deltas = []
            for k in K_BAND:
                amps_mass = propagate(positions, adj, field, src, k)
                amps_free = propagate(positions, adj, free, src, k)
                deltas.append(centroid_y(amps_mass, positions, det_list) - centroid_y(amps_free, positions, det_list))
            if deltas:
                by_count[m].append(sum(deltas) / len(deltas))

    xs = []
    ys = []
    for m in MASS_COUNTS:
        vals = by_count[m]
        if not vals:
            return None
        mean_shift = sum(vals) / len(vals)
        if mean_shift <= 0:
            return None
        xs.append(float(m))
        ys.append(mean_shift)

    fit = _fit_power_law(xs, ys)
    return fit[0] if fit is not None else None


def main():
    print("=" * 70)
    print("HIERARCHICAL ALPHA STUDY (FIXED-POSITION CONTROL)")
    print("=" * 70)
    print()

    print("TEST 1: Alpha vs leak parameter (3D hierarchical, 20 seeds)")
    print(f"  {'leak':>6s}  {'alpha':>7s}")
    print(f"  {'-' * 16}")
    for leak in [0.01, 0.02, 0.05, 0.10, 0.15, 0.20, 0.50, 1.00]:
        alpha = _measure_alpha(gen_3d_hierarchical, n_seeds=20, leak=leak)
        print(f"  {leak:6.2f}  {alpha:7.3f}" if alpha is not None else f"  {leak:6.2f}  FAIL")
    print()

    print("TEST 2: Alpha vs density at leak=0.05 (convergence check)")
    print(f"  {'npl':>5s}  {'radius':>6s}  {'alpha':>7s}")
    print(f"  {'-' * 22}")
    configs = [(15, 5.0), (25, 4.0), (40, 3.2), (60, 2.7), (80, 2.4)]
    alphas = []
    for npl, r in configs:
        alpha = _measure_alpha(gen_3d_hierarchical, n_seeds=20, npl=npl, r=r, leak=0.05)
        if alpha is not None:
            alphas.append(alpha)
            print(f"  {npl:5d}  {r:6.1f}  {alpha:7.3f}")
        else:
            print(f"  {npl:5d}  {r:6.1f}  FAIL")

    if len(alphas) >= 3:
        last3 = alphas[-3:]
        spread = max(last3) - min(last3)
        mean_a = sum(last3) / len(last3)
        print(f"\n  Last 3: {', '.join(f'{a:.3f}' for a in last3)}")
        print(f"  Spread: {spread:.3f}, Mean: {mean_a:.3f}")
        if spread < 0.15:
            print(f"  -> converging to alpha ~= {mean_a:.2f}")
        else:
            print("  -> not converged")
    print()

    print("TEST 3: Hierarchical vs modular at matched density (npl=30, 20 seeds)")
    print(f"  {'family':>25s}  {'alpha':>7s}")
    print(f"  {'-' * 35}")
    families = [
        ("Modular gap=3", gen_3d_modular, {"gap": 3.0}),
        ("Modular gap=5", gen_3d_modular, {"gap": 5.0}),
        ("Hierarchical leak=0.02", gen_3d_hierarchical, {"leak": 0.02}),
        ("Hierarchical leak=0.05", gen_3d_hierarchical, {"leak": 0.05}),
        ("Hierarchical leak=0.10", gen_3d_hierarchical, {"leak": 0.10}),
    ]
    for name, gen_fn, kwargs in families:
        alpha = _measure_alpha(gen_fn, n_seeds=20, **kwargs)
        print(f"  {name:>25s}  {alpha:7.3f}" if alpha is not None else f"  {name:>25s}  FAIL")

    print()
    print("=" * 70)
    print("KEY QUESTION: does hierarchical alpha survive the fixed-position control?")
    print("=" * 70)


if __name__ == "__main__":
    main()
