#!/usr/bin/env python3
"""Triple-stack scaling pilot: LN + |y|-removal + stochastic collapse.

This script compares four modes on the same 3D central-band hard-geometry
family:

1. linear baseline
2. stochastic collapse alone
3. layer norm + |y|-removal, no collapse
4. layer norm + |y|-removal + stochastic collapse

The main question is whether the positive-exponent collapse story survives
inside the hard-geometry lane, and whether the triple stack improves purity
relative to the bounded unitary lanes.
"""

from __future__ import annotations

import argparse
import cmath
from collections import defaultdict
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.combined_gravity_scaling import compute_field, propagate_linear, propagate_ln

BETA = 0.8
K_BAND = [3.0, 5.0, 7.0]


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fit_power(ns, vals):
    pts = [(n, v) for n, v in zip(ns, vals) if not math.isnan(v) and v > 0]
    if len(pts) < 3:
        return None
    xs = [math.log(n) for n, _ in pts]
    ys = [math.log(v) for _, v in pts]
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


def build_graph(nl, seed, y_cut, npl, y_range, connect_radius):
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
    mass_env = []
    for layer in layers[start:stop]:
        mass_env.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, list(set(mass_env) | set(mass_nodes)))
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
        "adj": adj_pruned,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "sa": sa,
        "sb": sb,
        "field": field,
        "field_flat": field_flat,
        "mass_set": set(mass_env) | set(mass_nodes),
        "removed_frac": len(removed) / max(1, n_post),
    }


def make_collapse_phase_map(mass_set, p_collapse, seed_base):
    if p_collapse <= 0 or not mass_set:
        return {}
    phases = {}
    for i in sorted(mass_set):
        rr = random.Random(seed_base + 1000003 * (i + 1))
        if rr.random() < p_collapse:
            phases[i] = cmath.exp(1j * rr.uniform(0.0, 2.0 * math.pi))
    return phases


def propagate_with_collapse(positions, adj, field, src, k, blocked, collapse_phase, use_ln=False):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if i in blocked:
                continue
            a_i = amps[i]
            if a_i == 0j:
                continue

            if i in collapse_phase:
                a_i *= collapse_phase[i]
                amps[i] = a_i

            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx, dy = x2 - x1, y2 - y1
                L = math.sqrt(dx * dx + dy * dy)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                amps[j] += a_i * cmath.exp(1j * k * act) * w / L

        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def measure_purity(graph, use_ln, p_collapse, n_realizations):
    vals = []
    for k in K_BAND:
        for r in range(n_realizations):
            collapse_phase = make_collapse_phase_map(graph["mass_set"], p_collapse, r * 1000 + int(k * 100))
            aa = propagate_with_collapse(
                graph["positions"],
                graph["adj"],
                graph["field"],
                graph["src"],
                k,
                graph["blocked"] | set(graph["sb"]),
                collapse_phase,
                use_ln=use_ln,
            )
            ab = propagate_with_collapse(
                graph["positions"],
                graph["adj"],
                graph["field"],
                graph["src"],
                k,
                graph["blocked"] | set(graph["sa"]),
                collapse_phase,
                use_ln=use_ln,
            )
            norm_a = sum(abs(aa[d]) ** 2 for d in graph["det_list"])
            norm_b = sum(abs(ab[d]) ** 2 for d in graph["det_list"])
            if norm_a <= 1e-30 or norm_b <= 1e-30:
                continue
            rho = {}
            for d1 in graph["det_list"]:
                for d2 in graph["det_list"]:
                    rho[(d1, d2)] = (aa[d1].conjugate() * aa[d2] + ab[d1].conjugate() * ab[d2])
            tr = sum(rho[(d, d)] for d in graph["det_list"]).real
            if tr <= 1e-30:
                continue
            for key in rho:
                rho[key] /= tr
            vals.append(sum(abs(v) ** 2 for v in rho.values()).real)
    return math.nan if not vals else sum(vals) / len(vals)


def measure_gravity(graph, use_ln):
    prop = propagate_ln if use_ln else propagate_linear
    vals = []
    for k in K_BAND:
        am = prop(graph["positions"], graph["adj_pruned"], graph["field"], graph["src"], k, graph["blocked"])
        af = prop(graph["positions"], graph["adj_pruned"], graph["field_flat"], graph["src"], k, graph["blocked"])
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
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--n-realizations", type=int, default=10)
    parser.add_argument("--npl", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 132)
    print("TRIPLE-STACK COLLAPSE SCALING")
    print("  linear / collapse / LN+|y| / LN+|y|+collapse on the same 3D hard-geometry lane")
    print(
        f"  seeds={args.n_seeds}, n_realizations={args.n_realizations}, npl={args.npl}, "
        f"y_range={args.y_range}, r={args.connect_radius}, y_cut={args.y_cut}, p={args.p_collapse}"
    )
    print("=" * 132)
    print()

    mode_specs = [
        ("linear", False, 0.0, 0.0),
        ("collapse", False, args.p_collapse, 0.0),
        ("LN+|y|", True, 0.0, args.y_cut),
        ("LN+|y|+collapse", True, args.p_collapse, args.y_cut),
    ]

    mode_results = {name: [] for name, *_ in mode_specs}
    mode_grav = {name: [] for name, *_ in mode_specs}

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'mode':>16s}  {'purity':>12s}  {'1-pur':>10s}  {'gravity':>14s}  {'g/SE':>6s}  {'rem%':>6s}  {'ok':>3s}"
        )
        print("  " + "-" * 92)

        for name, use_ln, p_collapse, y_cut in mode_specs:
            purities = []
            gravs = []
            rems = []
            for seed in seeds:
                graph = build_graph(nl, seed, y_cut, args.npl, args.y_range, args.connect_radius)
                if graph is None:
                    continue
                pur = measure_purity(graph, use_ln, p_collapse, args.n_realizations)
                if not math.isnan(pur):
                    purities.append(pur)
                    rems.append(100.0 * graph["removed_frac"])
                if name in ("linear", "LN+|y|"):
                    grav = measure_gravity(graph, use_ln)
                    if not math.isnan(grav):
                        gravs.append(grav)
            mean_p, se_p = mean_se(purities)
            mean_g, se_g = mean_se(gravs)
            g_over_se = mean_g / se_g if not math.isnan(mean_g) and se_g > 1e-12 else math.nan
            rem_s = "  —  " if not rems else f"{sum(rems)/len(rems):5.1f}%"
            pur_s = "FAIL" if math.isnan(mean_p) else f"{mean_p:.4f}±{se_p:.4f}"
            one_minus = "FAIL" if math.isnan(mean_p) else f"{1 - mean_p:.4f}"
            grav_s = "  —  " if not gravs else f"{mean_g:+.3f}±{se_g:.3f}"
            gse_s = "  —  " if not gravs or math.isnan(g_over_se) else f"{g_over_se:+.1f}"
            print(
                f"  {name:>16s}  {pur_s:>12s}  {one_minus:>10s}  {grav_s:>14s}  {gse_s:>6s}  {rem_s:>6s}  {len(purities):3d}"
            )
            mode_results[name].append((nl, mean_p))
            if gravs:
                mode_grav[name].append((nl, mean_g))
            sys.stdout.flush()
        print()

    print("POWER-LAW FITS FOR (1 - purity):")
    print(f"  {'mode':>16s}  {'A':>9s}  {'alpha':>8s}  {'R^2':>6s}  {'N_0.90':>8s}  {'N_0.99':>8s}")
    print("  " + "-" * 68)

    for name in mode_results:
        ns = [n for n, _ in mode_results[name]]
        vals = [1 - p for _, p in mode_results[name] if not math.isnan(p)]
        fit = fit_power(ns, vals)
        if not fit:
            print(f"  {name:>16s}  FAIL")
            continue
        A, alpha, r2 = fit
        n90 = (0.10 / A) ** (1.0 / alpha) if A > 0 and alpha != 0 else math.nan
        n99 = (0.01 / A) ** (1.0 / alpha) if A > 0 and alpha != 0 else math.nan
        n90_s = "FAIL" if math.isnan(n90) else f"{n90:8.0f}"
        n99_s = "FAIL" if math.isnan(n99) else f"{n99:8.0f}"
        print(f"  {name:>16s}  {A:9.3e}  {alpha:+8.3f}  {r2:6.3f}  {n90_s}  {n99_s}")

    print()
    print("Interpretation:")
    print("- If collapse retains a positive alpha inside LN+|y|, the scalable story survives inside hard geometry.")
    print("- If LN+|y|+collapse loses the positive alpha but stays Born-clean, collapse is only a bounded helper.")
    print("- If LN+|y|+collapse improves purity but alpha turns negative, the hard-geometry lane is still unitary-ceiling-limited.")


if __name__ == "__main__":
    main()
