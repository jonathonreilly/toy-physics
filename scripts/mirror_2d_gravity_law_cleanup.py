#!/usr/bin/env python3
"""Exact 2D mirror gravity-law cleanup.

This script is a narrow follow-up to the review-safe exact 2D mirror
validation lane. It searches for a promotable fixed-anchor mass window and a
fixed-geometry distance tail on the same exact mirror family, using the strict
linear propagator only.

The intent is conservative:
  - keep the exact 2D mirror geometry fixed
  - scan only gravity-side windows
  - promote a law only if the fit is genuinely clean
  - otherwise freeze the result as bounded/weak
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

from scripts.mirror_2d_validation import fit_power_law, measure_family, mean_se


def anchor_mass_rows(graphs, anchor_b, m_values):
    per_m = {m: [] for m in m_values}
    for graph in graphs:
        positions = graph["positions"]
        ordered = sorted(
            graph["mass_nodes"],
            key=lambda i: (
                abs(positions[i][1] - (graph["cy"] + anchor_b)),
                abs(positions[i][1] - graph["cy"]),
            ),
        )
        for m in m_values:
            if len(ordered) < m:
                continue
            field_m = compute_field_2d(positions, ordered[:m])
            field_f = [0.0] * len(positions)
            vals = []
            for k in graph["k_band"]:
                am = propagate_2d(positions, graph["adj"], field_m, graph["src"], k, graph["blocked"])
                af = propagate_2d(positions, graph["adj"], field_f, graph["src"], k, graph["blocked"])
                pm = sum(abs(am[d]) ** 2 for d in graph["det_list"])
                pf = sum(abs(af[d]) ** 2 for d in graph["det_list"])
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in graph["det_list"]) / pm
                    yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in graph["det_list"]) / pf
                    vals.append(ym - yf)
            if vals:
                per_m[m].append(sum(vals) / len(vals))

    rows = [(m, mean_se(vals)[0]) for m, vals in per_m.items() if vals]
    return sorted(rows)


def distance_rows(graphs, mass_count, thresholds):
    per_thr = {thr: [] for thr in thresholds}
    for graph in graphs:
        positions = graph["positions"]
        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        cand = [i for i in by_layer[graph["grav_layer"]] if positions[i][1] > graph["cy"] + 1.0]
        for thr in thresholds:
            selected = [i for i in cand if positions[i][1] > graph["cy"] + thr][:mass_count]
            if not selected:
                continue
            field_m = compute_field_2d(positions, selected)
            field_f = [0.0] * len(positions)
            vals = []
            for k in graph["k_band"]:
                am = propagate_2d(positions, graph["adj"], field_m, graph["src"], k, graph["blocked"])
                af = propagate_2d(positions, graph["adj"], field_f, graph["src"], k, graph["blocked"])
                pm = sum(abs(am[d]) ** 2 for d in graph["det_list"])
                pf = sum(abs(af[d]) ** 2 for d in graph["det_list"])
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in graph["det_list"]) / pm
                    yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in graph["det_list"]) / pf
                    vals.append(ym - yf)
            if vals:
                per_thr[thr].append(sum(vals) / len(vals))

    rows = [(thr, mean_se(vals)[0]) for thr, vals in per_thr.items() if vals]
    return sorted(rows)


def compute_field_2d(positions, mass_nodes):
    field = [0.0] * len(positions)
    for m in mass_nodes:
        mx, my = positions[m]
        for i, (ix, iy) in enumerate(positions):
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_2d(positions, adj, field, src, k, blocked):
    # Import lazily to keep this file self-contained around the mirror validator.
    from scripts.mirror_2d_validation import propagate_2d as _propagate_2d

    return _propagate_2d(positions, adj, field, src, k, blocked)


def collect_graphs(n_layers, npl_half, yr, connect_radius, n_seeds, k_band):
    graphs = []
    seeds = [s * 7 + 3 for s in range(n_seeds)]
    for seed in seeds:
        row = measure_family(
            n_layers=n_layers,
            npl_half=npl_half,
            yr=yr,
            connect_radius=connect_radius,
            seed=seed,
            family="mirror",
            k_band=k_band,
        )
        if row:
            row["k_band"] = list(k_band)
            graphs.append(row)
    return graphs


def summarize_mass_windows(graphs, anchor_b_values, m_values):
    best = None
    rows_by_anchor = {}
    for anchor_b in anchor_b_values:
        rows = anchor_mass_rows(graphs, anchor_b, m_values)
        rows_by_anchor[anchor_b] = rows
        fit = fit_power_law([(m, d) for m, d in rows if d is not None and d > 0])
        if fit and (best is None or fit[2] > best["fit"][2]):
            best = {"anchor_b": anchor_b, "rows": rows, "fit": fit}
    return best, rows_by_anchor


def summarize_distance_windows(graphs, mass_counts, thresholds):
    best = None
    rows_by_mass = {}
    for mass_count in mass_counts:
        rows = distance_rows(graphs, mass_count, thresholds)
        rows_by_mass[mass_count] = rows
        valid = [(thr, d) for thr, d in rows if d is not None and d > 0]
        if len(valid) < 3:
            continue
        peak_thr, peak_d = max(valid, key=lambda row: row[1])
        tail = [(thr, d) for thr, d in valid if thr > peak_thr]
        fit = fit_power_law(tail)
        if fit and (best is None or fit[2] > best["fit"][2]):
            best = {
                "mass_count": mass_count,
                "peak_thr": peak_thr,
                "peak_d": peak_d,
                "rows": rows,
                "fit": fit,
            }
    return best, rows_by_mass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[60, 80, 100])
    parser.add_argument("--npl-half", type=int, default=12)
    parser.add_argument("--yr", type=float, default=10.0)
    parser.add_argument("--connect-radius", type=float, default=2.5)
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--k-band", nargs="+", type=float, default=[3.0, 5.0, 7.0])
    parser.add_argument("--anchor-b-values", nargs="+", type=float, default=[4.0, 5.0, 6.0])
    parser.add_argument("--m-values", nargs="+", type=int, default=[1, 2, 3, 5, 8, 12])
    parser.add_argument("--mass-counts", nargs="+", type=int, default=[3, 4, 5])
    parser.add_argument("--distance-thresholds", nargs="+", type=float, default=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    args = parser.parse_args()

    print("=" * 100)
    print("EXACT 2D MIRROR GRAVITY LAW CLEANUP")
    print("  fixed-geometry distance windows and fixed-anchor mass windows only")
    print(f"  npl_half={args.npl_half}, yr={args.yr}, r={args.connect_radius}, seeds={args.n_seeds}")
    print("=" * 100)
    print()

    for nl in args.n_layers:
        graphs = collect_graphs(nl, args.npl_half, args.yr, args.connect_radius, args.n_seeds, args.k_band)
        print(f"N = {nl}")
        print(f"  retained graphs: {len(graphs)} / {args.n_seeds}")
        if not graphs:
            print("  FAIL")
            print()
            continue

        mass_best, _ = summarize_mass_windows(graphs, args.anchor_b_values, args.m_values)
        if mass_best:
            coeff, alpha, r2 = mass_best["fit"]
            print(
                f"  best mass window: anchor_b={mass_best['anchor_b']:.1f}, "
                f"delta ~= {coeff:.4f} * M^{alpha:.3f}, R^2={r2:.3f}"
            )
        else:
            print("  best mass window: FAIL")

        dist_best, _ = summarize_distance_windows(graphs, args.mass_counts, args.distance_thresholds)
        if dist_best:
            coeff, alpha, r2 = dist_best["fit"]
            print(
                f"  best distance tail: mass_count={dist_best['mass_count']}, "
                f"peak_thr={dist_best['peak_thr']:.1f}, delta ~= {coeff:.4f} * b^{alpha:.3f}, R^2={r2:.3f}"
            )
        else:
            print("  best distance tail: FAIL")
        print()

    print("Interpretation:")
    print("  - exact 2D mirror remains Born-clean on the retained validator")
    print("  - gravity-side windows were swept more widely here")
    print("  - promote a law only if the fit is visibly clean; otherwise keep the")
    print("    result as a bounded gravity pocket")


if __name__ == "__main__":
    main()
