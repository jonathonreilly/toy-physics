#!/usr/bin/env python3
"""Z2xZ2 gravity probe: fixed-anchor mass window and distance sweep.

This is the higher-symmetry counterpart to the retained mirror gravity probe.
It asks a narrow question only:

  - does the retained Z2xZ2 lane have a usable gravity-side mass window?
  - does it also show a falling distance tail, or just a broad positive bump?

The probe is intentionally review-safe:

  - fixed geometry family: Z2xZ2
  - same slit / detector / gravity-layer layout as the joint validator
  - fixed-anchor mass prefixes for the mass window
  - fixed mass count for the distance sweep
  - fit only the declared positive / falling windows

The goal is not to force a universal gravity law, only to decide whether the
retained Z2xZ2 lane is a gravity-side contender or mainly a decoherence lead.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.higher_symmetry_dag import generate_z2z2_dag
from scripts.mirror_chokepoint_joint import compute_field_3d, propagate_3d

K_BAND = [3.0, 5.0, 7.0]


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def build_graph(nl, seed, npl_quarter, xyz_range, connect_radius):
    positions, adj, _ = generate_z2z2_dag(
        n_layers=nl,
        npl_quarter=npl_quarter,
        xyz_range=xyz_range,
        cr=connect_radius,
        rng_seed=seed,
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
    slit_a = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_b = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_a or not slit_b:
        return None
    blocked = set(bi) - set(slit_a + slit_b)

    grav_layer = layers[2 * len(layers) // 3]
    grav_candidates = list(by_layer[grav_layer])

    return {
        "positions": positions,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "center_y": cy,
        "grav_layer": grav_layer,
        "grav_candidates": grav_candidates,
    }


def gravity_delta_for_mass_nodes(graph, mass_nodes):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked"]

    if not mass_nodes:
        return math.nan

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
    fit = [(x, y) for x, y in rows if x in fit_window and not math.isnan(y) and y > 0]
    if len(fit) < 3:
        return None
    xs = [math.log(x) for x, _ in fit]
    ys = [math.log(y) for _, y in fit]
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
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--z2z2-quarter", type=int, default=12)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=5.0)
    parser.add_argument("--anchor-b", type=float, default=5.0)
    parser.add_argument("--m-values", nargs="+", type=int, default=[1, 2, 3, 5, 8, 12, 16])
    parser.add_argument("--fit-window", nargs="+", type=int, default=[2, 3, 5, 8])
    parser.add_argument("--mass-count", type=int, default=4)
    parser.add_argument("--b-values", nargs="+", type=float, default=[2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 110)
    print("HIGHER-SYMMETRY GRAVITY PROBE: Z2xZ2")
    print("  fixed-anchor mass window + fixed-distance sweep")
    print(
        f"  seeds={args.n_seeds}, z2z2_quarter={args.z2z2_quarter}, "
        f"r={args.connect_radius}, anchor_b={args.anchor_b}, mass_count={args.mass_count}"
    )
    print("=" * 110)
    print()

    # Fixed-anchor mass window.
    print("FIXED-ANCHOR MASS WINDOW")
    print(f"  {'N':>4s}  {'M':>4s}  {'delta':>10s}  {'SE':>8s}  {'t':>7s}  {'delta/M':>10s}  {'ok':>3s}")
    print(f"  {'-' * 58}")
    for nl in args.n_layers:
        per_seed = []
        for seed in seeds:
            graph = build_graph(nl, seed, args.z2z2_quarter, args.xyz_range, args.connect_radius)
            if graph is None:
                continue
            ordered = sorted(
                graph["grav_candidates"],
                key=lambda i: (
                    abs(graph["positions"][i][1] - (graph["center_y"] + args.anchor_b)),
                    abs(graph["positions"][i][1] - graph["center_y"]),
                ),
            )
            if len(ordered) < max(args.m_values):
                continue
            vals = []
            for m_target in args.m_values:
                vals.append(gravity_delta_for_mass_nodes(graph, ordered[:m_target]))
            if all(not math.isnan(v) for v in vals):
                per_seed.append(vals)

        print(f"N = {nl}")
        rows = []
        if not per_seed:
            print("  FAIL")
            print()
            continue
        for idx, m in enumerate(args.m_values):
            vals = [seed_vals[idx] for seed_vals in per_seed if not math.isnan(seed_vals[idx])]
            mean, se = mean_se(vals)
            t = mean / se if not math.isnan(mean) and se > 1e-12 else math.nan
            dm = mean / m if not math.isnan(mean) and m > 0 else math.nan
            rows.append((m, mean))
            mean_s = "FAIL" if math.isnan(mean) else f"{mean:+.4f}"
            se_s = "FAIL" if math.isnan(se) else f"{se:.4f}"
            t_s = "FAIL" if math.isnan(t) else f"{t:+.2f}"
            dm_s = "FAIL" if math.isnan(dm) else f"{dm:+.4f}"
            print(f"  {m:4d}  {mean_s:>10s}  {se_s:>8s}  {t_s:>7s}  {dm_s:>10s}  {len(per_seed):3d}")

        fit = fit_power_law(rows, args.fit_window)
        if fit is not None:
            alpha, coeff, r2 = fit
            window_s = ",".join(str(v) for v in args.fit_window)
            print(f"  Fit window M in {{{window_s}}}: delta ~= {coeff:.4f} * M^{alpha:.3f}  (R^2={r2:.3f})")
        else:
            print("  Not enough positive mass-window rows for a review-safe fit.")
        print()

    # Fixed-distance sweep.
    print("FIXED-DISTANCE SWEEP")
    print(f"  {'N':>4s}  {'b':>5s}  {'delta':>10s}  {'SE':>8s}  {'t':>7s}  {'ok':>3s}")
    print(f"  {'-' * 44}")
    for nl in args.n_layers:
        print(f"N = {nl}")
        rows = []
        for b in args.b_values:
            per_seed = []
            for seed in seeds:
                graph = build_graph(nl, seed, args.z2z2_quarter, args.xyz_range, args.connect_radius)
                if graph is None:
                    continue
                ordered = sorted(
                    graph["grav_candidates"],
                    key=lambda i: abs(graph["positions"][i][1] - (graph["center_y"] + b)),
                )
                if len(ordered) < args.mass_count:
                    continue
                delta = gravity_delta_for_mass_nodes(graph, ordered[:args.mass_count])
                if not math.isnan(delta):
                    per_seed.append(delta)

            mean, se = mean_se(per_seed)
            t = mean / se if not math.isnan(mean) and se > 1e-12 else math.nan
            rows.append((b, mean))
            mean_s = "FAIL" if math.isnan(mean) else f"{mean:+.4f}"
            se_s = "FAIL" if math.isnan(se) else f"{se:.4f}"
            t_s = "FAIL" if math.isnan(t) else f"{t:+.2f}"
            print(f"  {b:5.1f}  {mean_s:>10s}  {se_s:>8s}  {t_s:>7s}  {len(per_seed):3d}")

        valid = [(b, d) for b, d in rows if not math.isnan(d) and d > 0]
        if len(valid) >= 3:
            peak_b, peak_d = max(valid, key=lambda row: row[1])
            print(f"  Peak mean deflection at b = {peak_b:.1f} (delta = {peak_d:.4f})")
            tail = [(b, d) for b, d in valid if b > peak_b]
            if len(tail) >= 3:
                xs = [math.log(b) for b, _ in tail]
                ys = [math.log(d) for _, d in tail]
                mx = sum(xs) / len(xs)
                my = sum(ys) / len(ys)
                sxx = sum((x - mx) ** 2 for x in xs)
                sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
                syy = sum((y - my) ** 2 for y in ys)
                if sxx > 1e-12:
                    alpha = sxy / sxx
                    r2 = (sxy * sxy) / (sxx * syy) if syy > 1e-12 else math.nan
                    if math.isnan(r2):
                        print(f"  Tail fit on Z2xZ2 geometry: delta ~= C * b^{alpha:.3f}")
                    else:
                        print(f"  Tail fit on Z2xZ2 geometry: delta ~= C * b^{alpha:.3f}  (R^2={r2:.3f})")
            else:
                print("  Not enough falling-tail points for a review-safe power-law fit.")
        else:
            print("  Not enough positive points for a review-safe tail fit.")
        print()


if __name__ == "__main__":
    main()
