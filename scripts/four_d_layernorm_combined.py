#!/usr/bin/env python3
"""4D modular DAGs with layer normalization: do the benefits stack?

This reconstructs the missing 4D+LN artifact chain behind the older synthesis
claim. It keeps the retained 4D modular generator fixed and adds per-layer
normalization in the propagator, then fits the finite-N purity ceiling.

The key question is whether layer norm on the retained 4D modular family
changes the scaling law or just improves the prefactor.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.four_d_decoherence_large_n import (  # type: ignore
    BETA,
    CONNECT_RADIUS,
    NODES_PER_LAYER,
    SPATIAL_RANGE,
    cl_purity,
    compute_field_4d,
    generate_4d_modular_dag,
)

K_BAND = [3.0, 5.0, 7.0]


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fit_power_law(ns, vals):
    pairs = [(n, v) for n, v in zip(ns, vals) if n > 0 and v > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(n) for n, _ in pairs]
    ys = [math.log(v) for _, v in pairs]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return None
    alpha = sxy / sxx
    intercept = my - alpha * mx
    r2 = (sxy * sxy) / (sxx * syy)
    return math.exp(intercept), alpha, r2


def propagate_4d_layernorm(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    by_layer = defaultdict(list)
    for idx, (x, y, z, w) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if i in blocked or abs(amps[i]) < 1e-30:
                continue
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1, z1, w1 = positions[i]
                x2, y2, z2, w2 = positions[j]
                dx = x2 - x1
                dy, dz, dw = y2 - y1, z2 - z1, w2 - w1
                L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
                if L < 1e-10:
                    continue
                cos_theta = dx / L
                theta = math.acos(min(max(cos_theta, -1.0), 1.0))
                wt = math.exp(-BETA * theta * theta)
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                ea = math.exp(0.0) * complex(math.cos(k * act), math.sin(k * act)) * wt / L
                amps[j] += amps[i] * ea

        if li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def run_family(label, gap, n_layers_list, n_seeds):
    print(f"[{label}]")
    print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'n_ok':>4s}")
    print(f"  {'-' * 28}")

    rows = []
    seeds = [s * 13 + 5 for s in range(n_seeds)]
    for nl in n_layers_list:
        per_seed = []
        for seed in seeds:
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=nl,
                nodes_per_layer=NODES_PER_LAYER,
                spatial_range=SPATIAL_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed,
                gap=gap,
            )
            n_actual = len(layer_indices)
            bl_idx = n_actual // 3
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list or n_actual < 5:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            barrier = layer_indices[bl_idx]
            slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
            slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
            if not slit_a or not slit_b:
                continue

            blocked = set(barrier) - set(slit_a + slit_b)
            blocked_a = blocked | set(slit_b)
            blocked_b = blocked | set(slit_a)

            bath_mass = []
            for li in range(bl_idx + 1, min(n_actual, bl_idx + 3)):
                for i in layer_indices[li]:
                    if abs(positions[i][1] - cy) <= 3:
                        bath_mass.append(i)
            grav_idx = 2 * n_actual // 3
            grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1]
            all_mass = set(bath_mass) | set(grav_mass)
            field = compute_field_4d(positions, adj, list(all_mass)) if all_mass else [0.0] * len(positions)

            pm_vals = []
            for k in K_BAND:
                aa = propagate_4d_layernorm(positions, adj, field, src, k, blocked_a)
                ab = propagate_4d_layernorm(positions, adj, field, src, k, blocked_b)
                pm = cl_purity(aa, ab, 0.0, det_list)
                if not math.isnan(pm):
                    pm_vals.append(pm)

            if pm_vals:
                per_seed.append(sum(pm_vals) / len(pm_vals))

        if per_seed:
            mean, se = mean_se(per_seed)
            rows.append((nl, mean, len(per_seed)))
            print(f"  {nl:4d}  {mean:8.4f}  {1-mean:7.4f}  {len(per_seed):4d}")
        else:
            print(f"  {nl:4d}  FAIL")

    if rows:
        fit = fit_power_law([r[0] for r in rows], [1 - r[1] for r in rows])
        if fit:
            A, alpha, r2 = fit
            n90 = (0.10 / A) ** (1.0 / alpha) if alpha != 0 else math.nan
            n99 = (0.01 / A) ** (1.0 / alpha) if alpha != 0 else math.nan
            print()
            print(f"  Fit: (1-pur_min) = {A:.3g} * N^({alpha:+.3f})   R^2={r2:.3f}")
            print(f"  pur_min=0.90 at N≈{n90:,.0f}")
            print(f"  pur_min=0.99 at N≈{n99:,.0f}")
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=12)
    parser.add_argument("--gap", type=float, default=3.0)
    args = parser.parse_args()

    print("=" * 74)
    print("4D + LAYER NORM COMBINED")
    print(f"  retained modular family, gap={args.gap}, seeds={args.n_seeds}")
    print(f"  nodes/layer={NODES_PER_LAYER}, spatial_range={SPATIAL_RANGE}, connect_radius={CONNECT_RADIUS}")
    print("=" * 74)
    print()

    run_family(f"4D modular gap={args.gap} + layernorm", args.gap, args.n_layers, args.n_seeds)


if __name__ == "__main__":
    main()
