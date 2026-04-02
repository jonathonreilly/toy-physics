#!/usr/bin/env python3
"""Joint card for topological asymmetry pruning on dense 3D DAGs.

This script puts the currently strongest supported asymmetry-lane reads on
one page:

- linear `pur_cl` before/after pruning
- layernorm `pur_min` before/after pruning
- gravity before/after pruning under both linear and layernorm propagation

All quantities are measured on the same seed-generated graphs.
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.gap_topological_asymmetry import K_BAND, measure
from scripts.gap_topological_asymmetry_layernorm_combo import (
    build_pruned_graph,
    propagate_3d_layernorm,
    run_case,
)


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def gravity_from_prop(prop, graph, use_pruned):
    adj = graph["adj_pruned"] if use_pruned else graph["adj_raw"]
    positions = graph["positions"]
    src = graph["src"]
    field = graph["field"]
    blocked = graph["blocked"]
    det_list = graph["det_list"]
    field_zero = [0.0] * len(positions)

    grav_vals = []
    for k in K_BAND:
        am = prop(positions, adj, field, src, k, blocked)
        af = prop(positions, adj, field_zero, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm <= 1e-30 or pf <= 1e-30:
            continue
        ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
        yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
        grav_vals.append(ym - yf)

    if not grav_vals:
        return math.nan
    return sum(grav_vals) / len(grav_vals)


def fmt_pair(vals):
    mean, se = mean_se(vals)
    if math.isnan(mean):
        return "FAIL"
    return f"{mean:+.3f}±{se:.3f}"


def fmt_mean(vals):
    mean, se = mean_se(vals)
    if math.isnan(mean):
        return "FAIL"
    return f"{mean:.3f}±{se:.3f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[70, 80, 100])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.1])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--npl", type=int, default=50)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 128)
    print("TOPOLOGICAL ASYMMETRY JOINT CARD")
    print("  Same-graph linear pur_cl, layernorm pur_min, and gravity before/after pruning")
    print(f"  seeds={args.n_seeds}, npl={args.npl}, xyz_range={args.xyz_range}, r={args.connect_radius}")
    print("=" * 128)
    print()

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'thr':>4s}  {'rem%':>6s}  {'pur_cl base':>14s}  {'pur_cl prune':>14s}  "
            f"{'pur_min LN base':>16s}  {'pur_min LN prune':>17s}  "
            f"{'grav lin base':>15s}  {'grav lin prune':>16s}  "
            f"{'grav LN base':>14s}  {'grav LN prune':>15s}  {'ok':>3s}"
        )
        print("  " + "-" * 122)
        for thresh in args.thresholds:
            rem_vals = []
            pur_base = []
            pur_pruned = []
            ln_base = []
            ln_pruned = []
            grav_lin_base = []
            grav_lin_pruned = []
            grav_ln_base = []
            grav_ln_pruned = []

            for seed in seeds:
                graph = build_pruned_graph(
                    nl,
                    seed,
                    thresh,
                    args.npl,
                    args.xyz_range,
                    args.connect_radius,
                )
                if graph is None:
                    continue

                base_measure = measure(graph["positions"], graph["adj_raw"], nl, K_BAND)
                pruned_measure = measure(graph["positions"], graph["adj_pruned"], nl, K_BAND)
                base_ln = run_case(graph, False, True)
                pruned_ln = run_case(graph, True, True)
                base_gln = gravity_from_prop(propagate_3d_layernorm, graph, False)
                pruned_gln = gravity_from_prop(propagate_3d_layernorm, graph, True)

                if base_measure and not math.isnan(base_ln) and not math.isnan(base_gln):
                    pur_base.append(base_measure["pur_cl"])
                    ln_base.append(base_ln)
                    grav_lin_base.append(base_measure["gravity"])
                    grav_ln_base.append(base_gln)

                if pruned_measure and not math.isnan(pruned_ln) and not math.isnan(pruned_gln):
                    pur_pruned.append(pruned_measure["pur_cl"])
                    ln_pruned.append(pruned_ln)
                    grav_lin_pruned.append(pruned_measure["gravity"])
                    grav_ln_pruned.append(pruned_gln)
                    rem_vals.append(graph["removed_frac"] * 100.0)

            ok = min(
                len(pur_base),
                len(pur_pruned),
                len(ln_base),
                len(ln_pruned),
                len(grav_lin_base),
                len(grav_lin_pruned),
                len(grav_ln_base),
                len(grav_ln_pruned),
            )
            rem = sum(rem_vals) / len(rem_vals) if rem_vals else math.nan
            rem_s = f"{rem:5.1f}%" if not math.isnan(rem) else " FAIL"
            print(
                f"  {thresh:4.2f}  {rem_s:>6s}  {fmt_mean(pur_base):>14s}  {fmt_mean(pur_pruned):>14s}  "
                f"{fmt_mean(ln_base):>16s}  {fmt_mean(ln_pruned):>17s}  "
                f"{fmt_pair(grav_lin_base):>15s}  {fmt_pair(grav_lin_pruned):>16s}  "
                f"{fmt_pair(grav_ln_base):>14s}  {fmt_pair(grav_ln_pruned):>15s}  {ok:3d}"
            )
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
