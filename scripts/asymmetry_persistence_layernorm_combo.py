#!/usr/bin/env python3
"""Generated hard geometry + layer norm combo card.

Tests whether the asymmetry-persistence geometry rule stacks with the
Born-clean per-layer normalization propagator on the same generated graphs.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.asymmetry_persistence_pilot import generate_3d_asymmetry_persistence_dag
from scripts.gap_topological_asymmetry_layernorm_combo import (
    compute_field_3d,
    propagate_3d_layernorm,
    propagate_3d_linear,
    purity_min,
)

K_BAND = [3.0, 5.0, 7.0]


def build_graph(nl, seed, thresh, npl, xyz_range, connect_radius):
    positions, adj, bl = generate_3d_asymmetry_persistence_dag(
        nl,
        npl,
        xyz_range,
        connect_radius,
        seed,
        thresh,
        max(1, round(nl / 6)),
    )
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mid_mass = []
    for layer in layers[start:stop]:
        mid_mass.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field_3d(positions, list(set(mid_mass) | set(mass_nodes)))

    return {
        "positions": positions,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "sa": sa,
        "sb": sb,
        "field": field,
        "keep_frac": len(positions) / (1 + (nl - 1) * npl),
    }


def run_case(graph, use_layernorm):
    prop = propagate_3d_layernorm if use_layernorm else propagate_3d_linear
    vals = []
    for k in K_BAND:
        aa = prop(graph["positions"], graph["adj"], graph["field"], graph["src"], k, graph["blocked"] | set(graph["sb"]))
        ab = prop(graph["positions"], graph["adj"], graph["field"], graph["src"], k, graph["blocked"] | set(graph["sa"]))
        pm = purity_min(aa, ab, graph["det_list"])
        if not math.isnan(pm):
            vals.append(pm)
    if not vals:
        return math.nan
    return sum(vals) / len(vals)


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[80, 100])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.1, 0.2])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--npl", type=int, default=50)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 118)
    print("ASYMMETRY PERSISTENCE + LAYERNORM COMBO")
    print("  Compare linear vs layernorm on generated hard-geometry graphs")
    print(
        f"  npl={args.npl}, xyz_range={args.xyz_range}, r={args.connect_radius}, "
        f"seeds={args.n_seeds}"
    )
    print("=" * 118)
    print()

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'thr':>4s}  {'keep%':>6s}  {'base_lin':>14s}  {'base_ln':>14s}  "
            f"{'persist_lin':>14s}  {'persist_ln':>14s}  {'ok':>3s}"
        )
        print("  " + "-" * 78)

        base_lin = []
        base_ln = []
        base_valid = 0
        base_graphs = {}
        for seed in seeds:
            graph = build_graph(nl, seed, 0.0, args.npl, args.xyz_range, args.connect_radius)
            if graph is None:
                continue
            base_graphs[seed] = graph
            lin = run_case(graph, False)
            ln = run_case(graph, True)
            if not math.isnan(lin) and not math.isnan(ln):
                base_lin.append(lin)
                base_ln.append(ln)
                base_valid += 1

        base_lin_s = "FAIL" if not base_lin else f"{mean_se(base_lin)[0]:.3f}±{mean_se(base_lin)[1]:.3f}"
        base_ln_s = "FAIL" if not base_ln else f"{mean_se(base_ln)[0]:.3f}±{mean_se(base_ln)[1]:.3f}"

        for thresh in args.thresholds:
            pers_lin = []
            pers_ln = []
            keeps = []
            valid = 0
            for seed in seeds:
                graph = build_graph(nl, seed, thresh, args.npl, args.xyz_range, args.connect_radius)
                if graph is None:
                    continue
                lin = run_case(graph, False)
                ln = run_case(graph, True)
                if not math.isnan(lin) and not math.isnan(ln):
                    pers_lin.append(lin)
                    pers_ln.append(ln)
                    keeps.append(100.0 * graph["keep_frac"])
                    valid += 1

            keep_s = "FAIL" if not keeps else f"{sum(keeps)/len(keeps):5.1f}%"
            pers_lin_s = "FAIL" if not pers_lin else f"{mean_se(pers_lin)[0]:.3f}±{mean_se(pers_lin)[1]:.3f}"
            pers_ln_s = "FAIL" if not pers_ln else f"{mean_se(pers_ln)[0]:.3f}±{mean_se(pers_ln)[1]:.3f}"
            print(
                f"  {thresh:4.2f}  {keep_s:>6s}  {base_lin_s:>14s}  {base_ln_s:>14s}  "
                f"{pers_lin_s:>14s}  {pers_ln_s:>14s}  {valid:3d}"
            )
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
