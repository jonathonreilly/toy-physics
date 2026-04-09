#!/usr/bin/env python3
"""Central-band gravity mass-window summary.

This is the gravity-side follow-up to the central-band hard-geometry lane.
It uses the same matched graphs as the central-band joint card, but focuses
on one question:

Does the best retained hard-geometry row give a cleaner mass-response window
than the plain baseline?

To keep the comparison review-safe and bounded, this script:
- uses the same central-band graph generator and matched seeds
- fixes one anchor position on the gravity layer
- varies only the mass count M by taking prefixes of the same ordered set
- compares baseline linear propagation against the layernorm hard-geometry row

Collapse is intentionally excluded here because the mass-response fit is meant
to stay deterministic and directly comparable to the plain baseline.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.central_band_layernorm_combo import build_pruned_graph
from scripts.combined_gravity_scaling import compute_field, propagate_linear, propagate_ln

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
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    if signed:
        return f"{m:+.3f}±{se:.3f}"
    return f"{m:.3f}±{se:.3f}"


def build_mass_window_graph(nl, seed, y_cut, npl, y_range, connect_radius, anchor_b):
    graph = build_pruned_graph(nl, seed, y_cut, npl, y_range, connect_radius)
    if graph is None:
        return None

    positions = graph["positions"]
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    grav_layer = layers[2 * len(layers) // 3]
    cy = sum(y for _, y in positions) / len(positions)
    anchor_y = cy + anchor_b
    ordered = sorted(
        by_layer[grav_layer],
        key=lambda i: (abs(positions[i][1] - anchor_y), abs(positions[i][1] - cy)),
    )

    graph["mass_ordered"] = ordered
    graph["center_y"] = cy
    graph["grav_layer"] = grav_layer
    return graph


def gravity_delta_for_m(graph, use_pruned, use_ln, m_count):
    positions = graph["positions"]
    adj = graph["adj_pruned"] if use_pruned else graph["adj_raw"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked"]
    ordered = graph["mass_ordered"]

    if len(ordered) < m_count:
        return math.nan

    mass_nodes = ordered[:m_count]
    field_m = compute_field(positions, mass_nodes)
    field_f = [0.0] * len(positions)
    prop = propagate_ln if use_ln else propagate_linear

    deltas = []
    for k in K_BAND:
        am = prop(positions, adj, field_m, src, k, blocked)
        af = prop(positions, adj, field_f, src, k, blocked)
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
    parser.add_argument("--n-layers", nargs="+", type=int, default=[60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--npl", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    parser.add_argument("--anchor-b", type=float, default=5.0)
    parser.add_argument("--m-values", nargs="+", type=int, default=[1, 2, 3, 5, 8, 12])
    parser.add_argument("--fit-window", nargs="+", type=int, default=[2, 3, 5, 8])
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 118)
    print("CENTRAL-BAND MASS WINDOW SUMMARY")
    print("  Compare the plain baseline against the best retained hard-geometry row on the same graphs")
    print(
        f"  seeds={args.n_seeds}, npl={args.npl}, y_range={args.y_range}, r={args.connect_radius}, "
        f"y_cut={args.y_cut}, anchor_b={args.anchor_b}"
    )
    print("=" * 118)
    print()

    modes = [
        ("linear", False, False),
        ("LN", False, True),
        ("pruned_linear", True, False),
        ("pruned_LN", True, True),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(f"  {'M':>4s}  {'linear':>12s}  {'LN':>12s}  {'pruned_lin':>12s}  {'pruned_LN':>12s}  {'ok':>3s}")
        print("  " + "-" * 72)

        rows_by_mode = {name: [] for name, _, _ in modes}
        rems = []
        ok = 0
        for seed in seeds:
            graph = build_mass_window_graph(
                nl, seed, args.y_cut, args.npl, args.y_range, args.connect_radius, args.anchor_b
            )
            if graph is None:
                continue
            rems.append(100.0 * graph["removed_frac"])
            per_seed = {}
            for name, use_pruned, use_ln in modes:
                vals = []
                for m in args.m_values:
                    vals.append(
                        gravity_delta_for_m(graph, use_pruned=use_pruned, use_ln=use_ln, m_count=m)
                    )
                per_seed[name] = vals
            if all(any(not math.isnan(v) for v in per_seed[name]) for name in per_seed):
                for name in per_seed:
                    rows_by_mode[name].append(per_seed[name])
                ok += 1

        if ok == 0:
            print("  FAIL")
            print()
            continue

        for idx, m in enumerate(args.m_values):
            cols = []
            for name, _, _ in modes:
                vals = [seed_vals[idx] for seed_vals in rows_by_mode[name] if not math.isnan(seed_vals[idx])]
                cols.append(fmt(vals, signed=True))
            print(f"  {m:4d}  {cols[0]:>12s}  {cols[1]:>12s}  {cols[2]:>12s}  {cols[3]:>12s}  {ok:3d}")
        print(f"  removed fraction: {mean_se(rems)[0]:.1f}%")
        print()

        fit_window = set(args.fit_window)
        print("  Power-law fits for gravity delta on the declared fit window")
        for name, _, _ in modes:
            mode_rows = []
            for idx, m in enumerate(args.m_values):
                vals = [seed_vals[idx] for seed_vals in rows_by_mode[name] if not math.isnan(seed_vals[idx])]
                if vals:
                    mode_rows.append((m, sum(vals) / len(vals)))
            fit = fit_power_law(mode_rows, fit_window)
            if fit is None:
                print(f"    {name:>12s}: not enough positive points for a stable fit")
                continue
            alpha, coeff, r2 = fit
            print(f"    {name:>12s}: delta ~= {coeff:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
        print()


if __name__ == "__main__":
    main()
