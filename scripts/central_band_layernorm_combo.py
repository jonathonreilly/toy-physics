#!/usr/bin/env python3
"""Layernorm + central-band removal joint card.

This tests the simplest hard-geometry rule described by the user:
remove post-barrier nodes with |y - center| < y_cut, then measure
joint decoherence and gravity with and without per-layer normalization.

Outputs:
- pur_min under linear and layernorm propagation
- paired gravity delta under linear and layernorm propagation
- removal fraction

Designed to compare directly against the modular+layernorm lane on the same
`N=25..100` scale.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800` means the
# audit-lane precompute and live audit runner allow up to 30 min of wall
# time before recording a timeout. The 120 s default ceiling is too tight
# under concurrency contention. See `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.combined_gravity_scaling import compute_field, propagate_linear, propagate_ln

K_BAND = [3.0, 5.0, 7.0]


def purity_min(amps_a, amps_b, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def build_pruned_graph(nl, seed, y_cut, npl, y_range, connect_radius):
    positions, adj_raw, _ = generate_causal_dag(
        n_layers=nl,
        nodes_per_layer=npl,
        y_range=y_range,
        connect_radius=connect_radius,
        rng_seed=seed,
    )
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y in positions) / len(positions)
    bl_idx = len(layers) // 3
    barrier_layer = layers[bl_idx]
    bi = by_layer[barrier_layer]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None
    env_depth = max(1, round(nl / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid_mass = []
    for layer in layers[start:stop]:
        mid_mass.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, list(set(mid_mass) | set(mass_nodes)))
    field_flat = [0.0] * len(positions)

    protected = set(src) | set(det_list) | set(sa + sb)
    removed = set()
    n_post = 0
    for idx, (x, y) in enumerate(positions):
        if x <= barrier_layer or idx in protected:
            continue
        n_post += 1
        if abs(y - cy) < y_cut:
            removed.add(idx)

    adj_pruned = {}
    for i, nbs in adj_raw.items():
        if i in removed:
            continue
        kept = [j for j in nbs if j not in removed]
        if kept:
            adj_pruned[i] = kept

    return {
        "positions": positions,
        "adj_raw": adj_raw,
        "adj_pruned": adj_pruned,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "sa": sa,
        "sb": sb,
        "field": field,
        "field_flat": field_flat,
        "removed_frac": len(removed) / max(1, n_post),
    }


def run_pur_min(graph, use_pruned, use_ln):
    adj = graph["adj_pruned"] if use_pruned else graph["adj_raw"]
    prop = propagate_ln if use_ln else propagate_linear
    vals = []
    for k in K_BAND:
        aa = prop(graph["positions"], adj, graph["field"], graph["src"], k, graph["blocked"] | set(graph["sb"]))
        ab = prop(graph["positions"], adj, graph["field"], graph["src"], k, graph["blocked"] | set(graph["sa"]))
        pm = purity_min(aa, ab, graph["det_list"])
        if not math.isnan(pm):
            vals.append(pm)
    return math.nan if not vals else sum(vals) / len(vals)


def run_gravity(graph, use_pruned, use_ln):
    adj = graph["adj_pruned"] if use_pruned else graph["adj_raw"]
    prop = propagate_ln if use_ln else propagate_linear
    vals = []
    for k in K_BAND:
        am = prop(graph["positions"], adj, graph["field"], graph["src"], k, graph["blocked"])
        af = prop(graph["positions"], adj, graph["field_flat"], graph["src"], k, graph["blocked"])
        pm = sum(abs(am[d]) ** 2 for d in graph["det_list"])
        pf = sum(abs(af[d]) ** 2 for d in graph["det_list"])
        if pm <= 1e-30 or pf <= 1e-30:
            continue
        ym = sum(abs(am[d]) ** 2 * graph["positions"][d][1] for d in graph["det_list"]) / pm
        yf = sum(abs(af[d]) ** 2 * graph["positions"][d][1] for d in graph["det_list"]) / pf
        vals.append(ym - yf)
    return math.nan if not vals else sum(vals) / len(vals)


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60, 80, 100])
    parser.add_argument("--y-cuts", nargs="+", type=float, default=[1.0, 2.0, 3.0])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--npl", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 138)
    print("LAYERNORM + CENTRAL-BAND REMOVAL JOINT CARD")
    print("  Same-graph pur_min and gravity before/after pruning by |y-center| < y_cut")
    print(
        f"  seeds={args.n_seeds}, npl={args.npl}, y_range={args.y_range}, r={args.connect_radius}"
    )
    print("=" * 138)
    print()

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'ycut':>4s}  {'rem%':>6s}  {'base_ln':>14s}  {'pruned_ln':>14s}  "
            f"{'base_lin':>14s}  {'pruned_lin':>14s}  "
            f"{'grav_ln base':>14s}  {'grav_ln pr':>14s}  "
            f"{'grav_lin base':>15s}  {'grav_lin pr':>14s}  {'ok':>3s}"
        )
        print("  " + "-" * 118)

        for y_cut in args.y_cuts:
            rems = []
            base_ln = []
            pr_ln = []
            base_lin = []
            pr_lin = []
            g_base_ln = []
            g_pr_ln = []
            g_base_lin = []
            g_pr_lin = []
            for seed in seeds:
                graph = build_pruned_graph(nl, seed, y_cut, args.npl, args.y_range, args.connect_radius)
                if graph is None:
                    continue
                rems.append(graph["removed_frac"] * 100.0)
                a = run_pur_min(graph, False, True)
                b = run_pur_min(graph, True, True)
                c = run_pur_min(graph, False, False)
                d = run_pur_min(graph, True, False)
                e = run_gravity(graph, False, True)
                f = run_gravity(graph, True, True)
                g = run_gravity(graph, False, False)
                h = run_gravity(graph, True, False)
                if not any(math.isnan(v) for v in [a, b, c, d, e, f, g, h]):
                    base_ln.append(a); pr_ln.append(b)
                    base_lin.append(c); pr_lin.append(d)
                    g_base_ln.append(e); g_pr_ln.append(f)
                    g_base_lin.append(g); g_pr_lin.append(h)
            rem_s = "FAIL" if not rems else f"{sum(rems)/len(rems):5.1f}%"
            ok = min(len(base_ln), len(pr_ln), len(g_base_ln), len(g_pr_ln))
            print(
                f"  {y_cut:4.1f}  {rem_s:>6s}  {fmt(base_ln):>14s}  {fmt(pr_ln):>14s}  "
                f"{fmt(base_lin):>14s}  {fmt(pr_lin):>14s}  "
                f"{fmt(g_base_ln, True):>14s}  {fmt(g_pr_ln, True):>14s}  "
                f"{fmt(g_base_lin, True):>15s}  {fmt(g_pr_lin, True):>14s}  {ok:3d}"
            )
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
