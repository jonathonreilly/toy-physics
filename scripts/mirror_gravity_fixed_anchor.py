#!/usr/bin/env python3
"""Fixed-anchor gravity mass window on the retained mirror chokepoint pocket.

This is the mirror-only gravity follow-up requested after the mirror pocket
was retained as Born-clean, gravity-positive, and decohering through N=60.

The experiment is intentionally narrow and review-safe:

- strict mirror chokepoint graphs only
- fixed anchor on the gravity layer
- mass count M varies only by prefix of the same ordered candidate set
- fit only the declared positive window

The goal is not to claim a universal gravity law. The goal is to check whether
the retained mirror pocket gives a cleaner gravity-side mass window than the
other hard-geometry lanes.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.mirror_chokepoint_joint import generate_mirror_chokepoint_dag, compute_field_3d, propagate_3d

K_BAND = [3.0, 5.0, 7.0]


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fmt(vals, signed=False):
    mean, se = mean_se(vals)
    if math.isnan(mean):
        return "FAIL"
    if signed:
        return f"{mean:+.3f}±{se:.3f}"
    return f"{mean:.3f}±{se:.3f}"


def build_mass_window_graph(nl, seed, npl_half, xyz_range, connect_radius, layer2_prob, anchor_b):
    positions, adj, _, _ = generate_mirror_chokepoint_dag(
        n_layers=nl,
        npl_half=npl_half,
        xyz_range=xyz_range,
        connect_radius=connect_radius,
        rng_seed=seed,
        layer2_prob=layer2_prob,
    )

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
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    anchor_y = cy + anchor_b
    ordered = sorted(
        by_layer[grav_layer],
        key=lambda i: (abs(positions[i][1] - anchor_y), abs(positions[i][1] - cy)),
    )

    return {
        "positions": positions,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "mass_ordered": ordered,
        "center_y": cy,
        "grav_layer": grav_layer,
    }


def gravity_delta_for_m(graph, m_count):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked"]
    ordered = graph["mass_ordered"]

    if len(ordered) < m_count:
        return math.nan

    mass_nodes = ordered[:m_count]
    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)

    deltas = []
    for k in K_BAND:
        am = propagate_3d(positions, adj, field_m, src, k, blocked)
        af = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm <= 1e-30 or pf <= 1e-30:
            continue
        ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
        yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
        deltas.append(ym - yf)
    return math.nan if not deltas else sum(deltas) / len(deltas)


def fit_power_law(rows, fit_window):
    fit = [(m, d) for m, d in rows if m in fit_window and not math.isnan(d) and d > 0]
    if len(fit) < 3:
        return None
    xs = [math.log(m) for m, _ in fit]
    ys = [math.log(d) for _, d in fit]
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--npl-half", type=int, default=50)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--layer2-prob", type=float, default=0.0)
    parser.add_argument("--anchor-b", type=float, default=5.0)
    parser.add_argument("--m-values", nargs="+", type=int, default=[1, 2, 3, 5, 8, 12, 16])
    parser.add_argument("--fit-window", nargs="+", type=int, default=[2, 3, 5, 8])
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 104)
    print("MIRROR GRAVITY FIXED-ANCHOR MASS WINDOW")
    print("  Mirror chokepoint pocket, fixed-anchor mass prefixes, review-safe fit window")
    print(
        f"  NPL_HALF={args.npl_half} (total {2 * args.npl_half}), "
        f"layer2_prob={args.layer2_prob}, anchor_b={args.anchor_b}, seeds={args.n_seeds}"
    )
    print("=" * 104)
    print()
    print(f"  {'M':>4s}  {'delta':>10s}  {'SE':>8s}  {'t':>7s}  {'delta/M':>10s}  {'ok':>3s}")
    print(f"  {'-' * 52}")

    rows = []

    for nl in args.n_layers:
        per_seed = []
        for seed in seeds:
            graph = build_mass_window_graph(
                nl,
                seed,
                args.npl_half,
                args.xyz_range,
                args.connect_radius,
                args.layer2_prob,
                args.anchor_b,
            )
            if graph is None:
                continue
            vals = []
            for m_target in args.m_values:
                vals.append(gravity_delta_for_m(graph, m_count=m_target))
            if all(not math.isnan(v) for v in vals):
                per_seed.append(vals)

        if not per_seed:
            print(f"N = {nl}")
            print("  FAIL")
            print()
            continue

        print(f"N = {nl}")
        for idx, m in enumerate(args.m_values):
            vals = [seed_vals[idx] for seed_vals in per_seed if not math.isnan(seed_vals[idx])]
            mean, se = mean_se(vals)
            t = mean / se if not math.isnan(mean) and se > 1e-12 else math.nan
            dm = mean / m if not math.isnan(mean) and m > 0 else math.nan
            mean_s = "FAIL" if math.isnan(mean) else f"{mean:+.4f}"
            se_s = "FAIL" if math.isnan(se) else f"{se:.4f}"
            t_s = "FAIL" if math.isnan(t) else f"{t:+.2f}"
            dm_s = "FAIL" if math.isnan(dm) else f"{dm:+.4f}"
            print(f"  {m:4d}  {mean_s:>10s}  {se_s:>8s}  {t_s:>7s}  {dm_s:>10s}  {len(per_seed):3d}")
            rows.append((nl, m, mean))
        print()

        fit = fit_power_law(
            [(m, d) for _, m, d in rows if _ == nl],
            set(args.fit_window),
        )
        if fit is None:
            print("  Not enough positive points in the declared fit window.")
        else:
            alpha, coeff, r2 = fit
            window_s = ",".join(str(v) for v in args.fit_window)
            print(f"  Fixed-anchor window fit on M in {{{window_s}}}: delta ~= {coeff:.4f} * M^{alpha:.3f}")
            if not math.isnan(r2):
                print(f"  R^2 = {r2:.3f}")
        print()


if __name__ == "__main__":
    main()
