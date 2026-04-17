#!/usr/bin/env python3
"""Head-to-head comparison of the best bounded geometry lanes.

Compares, on matched seeds and N values:
- modular gap=2 + layernorm
- modular gap=4 + layernorm
- central-band |y-center|<1 + layernorm
- central-band |y-center|<2 + layernorm

Readouts:
- pur_min
- gravity delta
- gravity significance estimate (mean / SE)
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.central_band_layernorm_combo import build_pruned_graph, run_gravity, run_pur_min
from scripts.combined_gravity_scaling import run_joint
from scripts.topology_families import generate_modular_dag


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


def g_over_se(vals):
    m, se = mean_se(vals)
    if math.isnan(m) or se <= 1e-12:
        return math.nan
    return m / se


def run_modular(nl, gap, seeds, npl, y_range, radius):
    pms = []
    gravs = []
    for seed in seeds:
        positions, adj, _ = generate_modular_dag(
            n_layers=nl,
            nodes_per_layer=npl,
            y_range=y_range,
            connect_radius=radius,
            rng_seed=seed,
            gap=gap,
        )
        r = run_joint(positions, adj, [3.0, 5.0, 7.0], nl, use_ln=True)
        if r:
            pms.append(r["pm"])
            gravs.append(r["grav"])
    return pms, gravs


def run_central(nl, y_cut, seeds, npl, y_range, radius):
    pms = []
    gravs = []
    rems = []
    for seed in seeds:
        graph = build_pruned_graph(nl, seed, y_cut, npl, y_range, radius)
        if graph is None:
            continue
        pm = run_pur_min(graph, True, True)
        grav = run_gravity(graph, True, True)
        if not math.isnan(pm) and not math.isnan(grav):
            pms.append(pm)
            gravs.append(grav)
            rems.append(graph["removed_frac"] * 100.0)
    return pms, gravs, rems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--npl", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 122)
    print("GEOMETRY LANE HEAD-TO-HEAD")
    print("  Same N / same seeds / same layernorm readout across the best bounded geometry lanes")
    print(
        f"  seeds={args.n_seeds}, npl={args.npl}, y_range={args.y_range}, r={args.connect_radius}"
    )
    print("=" * 122)
    print()

    configs = [
        ("mod_gap2", "modular gap=2", None),
        ("mod_gap4", "modular gap=4", None),
        ("central1", "|y-center|<1", 1.0),
        ("central2", "|y-center|<2", 2.0),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'config':>15s}  {'pur_min':>14s}  {'1-pm':>8s}  "
            f"{'gravity':>14s}  {'g/SE':>6s}  {'rem%':>6s}  {'ok':>3s}"
        )
        print("  " + "-" * 84)
        for key, label, y_cut in configs:
            if key == "mod_gap2":
                pms, gravs = run_modular(nl, 2.0, seeds, args.npl, args.y_range, args.connect_radius)
                rems = []
            elif key == "mod_gap4":
                pms, gravs = run_modular(nl, 4.0, seeds, args.npl, args.y_range, args.connect_radius)
                rems = []
            else:
                pms, gravs, rems = run_central(nl, y_cut, seeds, args.npl, args.y_range, args.connect_radius)

            pm_s = fmt(pms)
            one_minus = "FAIL"
            if pms:
                one_minus = f"{1 - (sum(pms)/len(pms)):.3f}"
            g_s = fmt(gravs, signed=True)
            gsig = g_over_se(gravs)
            gsig_s = "FAIL" if math.isnan(gsig) else f"{gsig:+.1f}"
            rem_s = "  —  " if not rems else f"{sum(rems)/len(rems):5.1f}%"
            print(
                f"  {label:>15s}  {pm_s:>14s}  {one_minus:>8s}  "
                f"{g_s:>14s}  {gsig_s:>6s}  {rem_s:>6s}  {len(pms):3d}"
            )
        print()
        sys.stdout.flush()


if __name__ == "__main__":
    main()
