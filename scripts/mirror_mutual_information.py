#!/usr/bin/env python3
"""Mirror-specific mutual-information comparison on the retained chokepoint lane.

This script freezes the mirror MI question on the exact linear propagator.
It compares the retained exact mirror chokepoint family against a matched
random chokepoint baseline using the same slit/detector geometry as the
review-safe mirror joint card.

Question:
  Does the exact mirror lane retain which-slit information more slowly than
  the matched random baseline, and does the corresponding purity floor stay
  lower over the retained window?

The script is intentionally narrow:
  - exact mirror chokepoint family only
  - matched random chokepoint baseline
  - linear propagator only
  - slit MI and CL-bath purity on the same graphs
  - fit only the retained bounded window
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.mirror_chokepoint_joint import (
    compute_field_3d,
    generate_mirror_chokepoint_dag,
    generate_random_chokepoint_dag,
    propagate_3d,
)

BETA = 0.8
DEFAULT_K_BAND = [3.0, 5.0, 7.0]


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def entropy(probs):
    return -sum(p * math.log2(p) for p in probs if p > 1e-30)


def mutual_info_slit_detector(amps_a, amps_b, det_list):
    pa = [abs(amps_a[d]) ** 2 for d in det_list]
    pb = [abs(amps_b[d]) ** 2 for d in det_list]
    na = sum(pa)
    nb = sum(pb)
    if na < 1e-30 or nb < 1e-30:
        return None

    pa = [p / na for p in pa]
    pb = [p / nb for p in pb]
    pd = [0.5 * a + 0.5 * b for a, b in zip(pa, pb)]

    h_d = entropy(pd)
    h_d_a = entropy(pa)
    h_d_b = entropy(pb)
    mi = h_d - 0.5 * (h_d_a + h_d_b)

    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2] / na
                + amps_b[d1].conjugate() * amps_b[d2] / nb
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_min = sum(abs(v) ** 2 for v in rho.values()).real
    return {"MI": mi, "pur_min": pur_min}


def fit_power_law(points):
    usable = [(n, y) for n, y in points if n > 0 and y > 0 and not math.isnan(y)]
    if len(usable) < 3:
        return None
    xs = [math.log(n) for n, _ in usable]
    ys = [math.log(y) for _, y in usable]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 1e-12:
        return None
    alpha = sxy / sxx
    coeff = math.exp(my - alpha * mx)
    r2 = (sxy * sxy) / (sxx * syy) if syy > 1e-12 else math.nan
    return alpha, coeff, r2


def compute_mi_for_graph(positions, adj, n_layers, k_band):
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y, _ in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    slit_a = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_b = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_a or not slit_b:
        return None
    blocked = set(bi) - set(slit_a + slit_b)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])

    field = compute_field_3d(positions, mass_nodes)

    mi_vals, pm_vals = [], []
    for k in k_band:
        amp_a = propagate_3d(positions, adj, field, src, k, blocked | set(slit_b))
        amp_b = propagate_3d(positions, adj, field, src, k, blocked | set(slit_a))
        r = mutual_info_slit_detector(amp_a, amp_b, det_list)
        if r:
            mi_vals.append(r["MI"])
            pm_vals.append(r["pur_min"])

    if not mi_vals:
        return None

    return {
        "MI": sum(mi_vals) / len(mi_vals),
        "pur_min": sum(pm_vals) / len(pm_vals),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[15, 25, 40, 60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--npl-half", type=int, default=25)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--layer2-prob", type=float, default=0.0)
    parser.add_argument("--k-band", nargs="+", type=float, default=DEFAULT_K_BAND)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 90)
    print("MIRROR MUTUAL INFORMATION: exact mirror vs matched random baseline")
    print(f"  seeds={args.n_seeds}, npl_half={args.npl_half}, r={args.connect_radius}, layer2_prob={args.layer2_prob}")
    print(f"  k-band={args.k_band}")
    print("=" * 90)
    print()

    family_rows = {"random": [], "mirror": []}

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(f"  {'family':>8s}  {'MI(bits)':>9s}  {'pur_min':>8s}  {'1-pur':>7s}  {'ok':>3s}")
        print(f"  {'-' * 42}")
        for family in ("random", "mirror"):
            mi_all, pm_all = [], []
            for seed in seeds:
                if family == "mirror":
                    pos, adj, _, _ = generate_mirror_chokepoint_dag(
                        n_layers=nl,
                        npl_half=args.npl_half,
                        xyz_range=args.xyz_range,
                        connect_radius=args.connect_radius,
                        rng_seed=seed,
                        layer2_prob=args.layer2_prob,
                    )
                else:
                    pos, adj, _ = generate_random_chokepoint_dag(
                        n_layers=nl,
                        npl_total=2 * args.npl_half,
                        xyz_range=args.xyz_range,
                        connect_radius=args.connect_radius,
                        rng_seed=seed,
                        layer2_prob=args.layer2_prob,
                    )
                r = compute_mi_for_graph(pos, adj, nl, args.k_band)
                if r:
                    mi_all.append(r["MI"])
                    pm_all.append(r["pur_min"])
            if mi_all:
                mi_mean, mi_se = _mean_se(mi_all)
                pm_mean, pm_se = _mean_se(pm_all)
                family_rows[family].append((nl, mi_mean, pm_mean))
                print(
                    f"  {family:>8s}  {mi_mean:9.6f}  {pm_mean:8.4f}  {1.0 - pm_mean:7.4f}  {len(mi_all):3d}"
                )
            else:
                print(f"  {family:>8s}  FAIL")
        print()

    for family in ("random", "mirror"):
        mi_fit = fit_power_law([(n, mi) for n, mi, _ in family_rows[family]])
        pm_fit = fit_power_law([(n, 1.0 - pm) for n, _, pm in family_rows[family]])
        print(f"[{family}]")
        if mi_fit:
            alpha, coeff, r2 = mi_fit
            print(f"  MI fit: MI ~= {coeff:.4f} * N^{alpha:+.3f}  (R^2={r2:.3f})")
        else:
            print("  MI fit: insufficient data")
        if pm_fit:
            alpha, coeff, r2 = pm_fit
            print(f"  1-pur fit: (1-pur_min) ~= {coeff:.4f} * N^{alpha:+.3f}  (R^2={r2:.3f})")
        else:
            print("  1-pur fit: insufficient data")
        print()


if __name__ == "__main__":
    main()
