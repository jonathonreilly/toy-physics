#!/usr/bin/env python3
"""Joint gravity/decoherence card for central-band geometry with stochastic collapse.

Compares, on matched seeds and the same central-band hard-geometry setup:

- linear
- LN
- collapse
- LN + |y|<2 removal
- LN + |y|<2 removal + collapse

Deterministic rows report `pur_min` and gravity delta.
Collapse rows report Monte Carlo density-matrix purity and gravity delta.
This keeps the comparison honest while still using the same underlying graph
family and seeds.
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

from scripts.central_band_layernorm_combo import build_pruned_graph, run_gravity, run_pur_min

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


def fmt(vals, signed=False):
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    if signed:
        return f"{m:+.3f}±{se:.3f}"
    return f"{m:.3f}±{se:.3f}"


def add_mass_support(graph, nl):
    """Add the fixed collapse mass support used by the stochastic-collapse lane."""
    positions = graph["positions"]
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    cy = sum(y for _, y in positions) / len(positions)
    bl_idx = len(layers) // 3
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mass_set = set()
    for layer in layers[start:stop]:
        for i in by_layer[layer]:
            if abs(positions[i][1] - cy) <= 3.0:
                mass_set.add(i)
    graph["mass_set"] = mass_set
    return graph


def collapse_propagate(positions, adj, field, src, k, blocked, mass_set, p_collapse, rng, use_ln=False):
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

            if p_collapse > 0 and i in mass_set and rng.random() < p_collapse:
                theta_rand = rng.uniform(0.0, 2.0 * math.pi)
                a_i *= cmath.exp(1j * theta_rand)
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
                theta = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                amps[j] += a_i * cmath.exp(1j * k * act) * w / L

        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def collapse_purity(graph, use_pruned, use_ln, p_collapse, n_realizations):
    adj = graph["adj_pruned"] if use_pruned else graph["adj_raw"]
    positions = graph["positions"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked"]
    sa = set(graph["sa"])
    sb = set(graph["sb"])
    mass_set = graph["mass_set"]
    field = graph["field"]
    field_flat = graph["field_flat"]

    rho = {(d1, d2): 0j for d1 in det_list for d2 in det_list}
    n_total = 0
    for k in K_BAND:
        for r in range(n_realizations):
            rng = random.Random(100000 * r + int(round(100 * k)))
            amps_a = collapse_propagate(
                positions, adj, field, src, k, blocked | sb, mass_set, p_collapse, rng, use_ln=use_ln
            )
            amps_b = collapse_propagate(
                positions, adj, field, src, k, blocked | sa, mass_set, p_collapse, rng, use_ln=use_ln
            )
            psi = [amps_a[d] + amps_b[d] for d in det_list]
            norm_sq = sum(abs(p) ** 2 for p in psi)
            if norm_sq < 1e-30:
                continue
            for i, d1 in enumerate(det_list):
                for j, d2 in enumerate(det_list):
                    rho[(d1, d2)] += psi[i].conjugate() * psi[j] / norm_sq
            n_total += 1

    if n_total == 0:
        return math.nan
    for key in rho:
        rho[key] /= n_total
    return sum(abs(v) ** 2 for v in rho.values()).real


def collapse_gravity(graph, use_pruned, use_ln, p_collapse, n_realizations):
    adj = graph["adj_pruned"] if use_pruned else graph["adj_raw"]
    positions = graph["positions"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked"]
    mass_set = graph["mass_set"]
    field = graph["field"]
    field_flat = graph["field_flat"]

    vals = []
    for k in K_BAND:
        for r in range(n_realizations):
            rng = random.Random(100000 * r + int(round(100 * k)))
            am = collapse_propagate(
                positions, adj, field, src, k, blocked, mass_set, p_collapse, rng, use_ln=use_ln
            )
            af = collapse_propagate(
                positions, adj, field_flat, src, k, blocked, mass_set, p_collapse, rng, use_ln=use_ln
            )
            pm = sum(abs(am[d]) ** 2 for d in det_list)
            pf = sum(abs(af[d]) ** 2 for d in det_list)
            if pm <= 1e-30 or pf <= 1e-30:
                continue
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            vals.append(ym - yf)
    return math.nan if not vals else sum(vals) / len(vals)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60])
    parser.add_argument("--n-seeds", type=int, default=6)
    parser.add_argument("--n-realizations", type=int, default=12)
    parser.add_argument("--npl", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 126)
    print("CENTRAL-BAND HARD-GEOMETRY + STOCHASTIC COLLAPSE JOINT CARD")
    print("  Same matched seeds / same graphs / compare linear, LN, collapse, LN+|y|, LN+|y|+collapse")
    print(
        f"  seeds={args.n_seeds}, n_realizations={args.n_realizations}, npl={args.npl}, "
        f"y_range={args.y_range}, r={args.connect_radius}, y_cut={args.y_cut}, p={args.p_collapse}"
    )
    print("=" * 126)
    print()

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'config':>18s}  {'metric':>8s}  {'decoh':>12s}  {'gravity':>14s}  "
            f"{'g/SE':>6s}  {'rem%':>6s}  {'ok':>3s}"
        )
        print("  " + "-" * 92)

        rows = [
            ("linear", False, False, False),
            ("LN", False, True, False),
            ("collapse", False, False, True),
            ("LN+|y|", True, True, False),
            ("LN+|y|+collapse", True, True, True),
        ]

        for label, use_pruned, use_ln, use_collapse in rows:
            decoh_vals = []
            grav_vals = []
            rems = []
            ok = 0
            for seed in seeds:
                graph = build_pruned_graph(nl, seed, args.y_cut, args.npl, args.y_range, args.connect_radius)
                if graph is None:
                    continue
                graph = add_mass_support(graph, nl)
                rems.append(100.0 * graph["removed_frac"])
                if use_collapse:
                    decoh = collapse_purity(graph, use_pruned, use_ln, args.p_collapse, args.n_realizations)
                    grav = collapse_gravity(graph, use_pruned, use_ln, args.p_collapse, args.n_realizations)
                    metric_name = "purity"
                else:
                    decoh = run_pur_min(graph, use_pruned, use_ln)
                    grav = run_gravity(graph, use_pruned, use_ln)
                    metric_name = "pur_min"
                if not math.isnan(decoh) and not math.isnan(grav):
                    decoh_vals.append(decoh)
                    grav_vals.append(grav)
                    ok += 1

            gmean, gse = mean_se(grav_vals)
            gsig = gmean / gse if not math.isnan(gmean) and gse > 1e-12 else math.nan
            rem_s = "  —  " if not rems else f"{sum(rems)/len(rems):5.1f}%"
            print(
                f"  {label:>18s}  {metric_name:>8s}  {fmt(decoh_vals):>12s}  "
                f"{fmt(grav_vals, signed=True):>14s}  "
                f"{('FAIL' if math.isnan(gsig) else f'{gsig:+.1f}'):>6s}  {rem_s:>6s}  {ok:3d}"
            )
        print()


if __name__ == "__main__":
    main()
