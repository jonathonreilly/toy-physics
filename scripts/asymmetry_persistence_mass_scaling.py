#!/usr/bin/env python3
"""Fixed-anchor mass scaling on dense generated asymmetry-persistence graphs.

This is the gravity-law follow-up for the retained generated hard-geometry lane.
Each seed uses one fixed generated graph, one fixed anchor on the gravity layer,
and a frozen ordering of gravity-layer candidates by distance to that anchor.
Varying M takes prefixes of that same ordering.

The fixed post-barrier mid-mass support used by the retained lane is kept
constant; only the gravity-layer contribution is varied.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.asymmetry_persistence_joint_card import build_graph
from scripts.gap_topological_asymmetry_layernorm_combo import (
    K_BAND,
    compute_field_3d,
    propagate_3d_layernorm,
    propagate_3d_linear,
)


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fit_power(rows, fit_window):
    pts = [(m, d) for m, d in rows if m in fit_window and not math.isnan(d) and d > 0]
    if len(pts) < 3:
        return None
    xs = [math.log(m) for m, _ in pts]
    ys = [math.log(d) for _, d in pts]
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
    return coeff, alpha, r2


def choose_npl(nl: int, arg_npl: int | None) -> int:
    if arg_npl is not None:
        return arg_npl
    if nl >= 100:
        return 60
    if nl >= 80:
        return 50
    return 30


def graph_with_mass_metadata(nl, seed, thresh, npl, xyz_range, connect_radius, anchor_b):
    graph = build_graph(nl, seed, thresh, npl, xyz_range, connect_radius)
    if graph is None:
        return None

    positions = graph["positions"]
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    cy = sum(y for _, y, _ in positions) / len(positions)
    grav_layer = layers[2 * len(layers) // 3]
    start = len(layers) // 3 + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))

    mid_mass = []
    for layer in layers[start:stop]:
        mid_mass.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)

    anchor_y = cy + anchor_b
    ordered = sorted(
        by_layer[grav_layer],
        key=lambda i: (abs(positions[i][1] - anchor_y), abs(positions[i][1] - cy)),
    )
    graph["mid_mass"] = list(set(mid_mass))
    graph["ordered_mass"] = ordered
    return graph


def gravity_delta(graph, use_ln, mass_nodes):
    prop = propagate_3d_layernorm if use_ln else propagate_3d_linear
    field = compute_field_3d(graph["positions"], list(set(graph["mid_mass"]) | set(mass_nodes)))
    flat = [0.0] * len(graph["positions"])
    vals = []
    for k in K_BAND:
        am = prop(graph["positions"], graph["adj"], field, graph["src"], k, graph["blocked_two"])
        af = prop(graph["positions"], graph["adj"], flat, graph["src"], k, graph["blocked_two"])
        pm = sum(abs(am[d]) ** 2 for d in graph["det_list"])
        pf = sum(abs(af[d]) ** 2 for d in graph["det_list"])
        if pm <= 1e-30 or pf <= 1e-30:
            continue
        ym = sum(abs(am[d]) ** 2 * graph["positions"][d][1] for d in graph["det_list"]) / pm
        yf = sum(abs(af[d]) ** 2 * graph["positions"][d][1] for d in graph["det_list"]) / pf
        vals.append(ym - yf)
    return math.nan if not vals else sum(vals) / len(vals)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", type=int, default=100)
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.0, 0.1, 0.2])
    parser.add_argument("--m-values", nargs="+", type=int, default=[1, 2, 3, 5, 8, 12])
    parser.add_argument("--fit-window", nargs="+", type=int, default=[2, 3, 5, 8])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--npl", type=int, default=None)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--anchor-b", type=float, default=6.0)
    args = parser.parse_args()

    npl = choose_npl(args.n_layers, args.npl)
    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 116)
    print("ASYMMETRY PERSISTENCE MASS SCALING")
    print(
        f"  N={args.n_layers}, thresholds={args.thresholds}, M={args.m_values}, "
        f"fit={args.fit_window}, seeds={args.n_seeds}, npl={npl}, anchor_b={args.anchor_b}"
    )
    print("=" * 116)
    print()

    for thresh in args.thresholds:
        print(f"threshold = {thresh:.2f}")
        print(f"  {'M':>4s}  {'grav_lin':>14s}  {'g/SE':>6s}  {'grav_ln':>14s}  {'g/SE':>6s}  {'ok':>3s}")
        print("  " + "-" * 62)
        lin_rows = []
        ln_rows = []
        for m_target in args.m_values:
            per_lin = []
            per_ln = []
            for seed in seeds:
                graph = graph_with_mass_metadata(
                    args.n_layers,
                    seed,
                    thresh,
                    npl,
                    args.xyz_range,
                    args.connect_radius,
                    args.anchor_b,
                )
                if graph is None or len(graph["ordered_mass"]) < m_target:
                    continue
                mass_nodes = graph["ordered_mass"][:m_target]
                g_lin = gravity_delta(graph, False, mass_nodes)
                g_ln = gravity_delta(graph, True, mass_nodes)
                if not math.isnan(g_lin):
                    per_lin.append(g_lin)
                if not math.isnan(g_ln):
                    per_ln.append(g_ln)
            m_lin, se_lin = mean_se(per_lin)
            m_ln, se_ln = mean_se(per_ln)
            t_lin = m_lin / se_lin if not math.isnan(m_lin) and se_lin > 1e-12 else math.nan
            t_ln = m_ln / se_ln if not math.isnan(m_ln) and se_ln > 1e-12 else math.nan
            lin_rows.append((m_target, m_lin))
            ln_rows.append((m_target, m_ln))
            lin_s = "FAIL" if math.isnan(m_lin) else f"{m_lin:+.3f}±{se_lin:.3f}"
            ln_s = "FAIL" if math.isnan(m_ln) else f"{m_ln:+.3f}±{se_ln:.3f}"
            tlin_s = "FAIL" if math.isnan(t_lin) else f"{t_lin:+.1f}"
            tln_s = "FAIL" if math.isnan(t_ln) else f"{t_ln:+.1f}"
            ok = min(len(per_lin), len(per_ln))
            print(f"  {m_target:4d}  {lin_s:>14s}  {tlin_s:>6s}  {ln_s:>14s}  {tln_s:>6s}  {ok:3d}")
            sys.stdout.flush()

        lin_fit = fit_power(lin_rows, set(args.fit_window))
        ln_fit = fit_power(ln_rows, set(args.fit_window))
        if lin_fit:
            coeff, alpha, r2 = lin_fit
            print(f"  linear fit: delta ~= {coeff:.4f} * M^{alpha:.3f}   R^2={r2:.3f}")
        else:
            print("  linear fit: not enough positive window points")
        if ln_fit:
            coeff, alpha, r2 = ln_fit
            print(f"  layernorm fit: delta ~= {coeff:.4f} * M^{alpha:.3f}   R^2={r2:.3f}")
        else:
            print("  layernorm fit: not enough positive window points")
        print()


if __name__ == "__main__":
    main()
