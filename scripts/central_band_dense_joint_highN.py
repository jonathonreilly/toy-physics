#!/usr/bin/env python3
"""High-N dense central-band joint card.

This is a review-safe wrapper around the dense central-band same-graph lane.
It focuses on the higher-N extension that matters for the retained pocket:

- N = 80, 100
- corrected Born on the same graphs
- unitary pur_min / collapse purity
- gravity centroid delta

The wrapper sweeps the dense central-band family across a small set of
candidate densities and prints the retained rows directly. It is meant to
freeze the high-N comparison without changing the underlying graph family.
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.central_band_dense_joint_card import (
    attach_field,
    born_metric_for_graph,
    build_graph,
    collapse_gravity,
    collapse_purity,
    mean_se,
    unitary_pur_min,
)


def fmt(vals, signed=False):
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    if signed:
        return f"{m:+.3f}±{se:.3f}"
    return f"{m:.3f}±{se:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[80, 100])
    parser.add_argument("--npl", nargs="+", type=int, default=[60, 70, 80])
    parser.add_argument("--n-seeds", type=int, default=4)
    parser.add_argument("--n-realizations", type=int, default=8)
    parser.add_argument("--yz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 138)
    print("CENTRAL-BAND HIGH-N SAME-GRAPH JOINT CARD")
    print("  review-safe high-N extension of the dense central-band hard-geometry lane")
    print(
        f"  seeds={args.n_seeds}, realizations={args.n_realizations}, npl={args.npl}, "
        f"yz_range={args.yz_range}, r={args.connect_radius}, y_cut={args.y_cut}, p={args.p_collapse}"
    )
    print("=" * 138)
    print()

    rows = [
        ("LN+|y|", True, 0.0),
        ("LN+|y|+collapse", True, args.p_collapse),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'npl':>4s}  {'mode':>16s}  {'Born |I3|/P':>14s}  {'pur_min/purity':>16s}  "
            f"{'gravity':>14s}  {'g/SE':>6s}  {'ok':>3s}"
        )
        print("  " + "-" * 106)

        for npl in args.npl:
            for label, use_ln, p_col in rows:
                born_vals = []
                decoh_vals = []
                grav_vals = []
                ok = 0
                for seed in seeds:
                    graph = build_graph(nl, seed, npl, args.yz_range, args.connect_radius, args.y_cut)
                    if graph is None:
                        continue
                    graph = attach_field(graph)

                    born_rows = born_metric_for_graph(
                        graph,
                        use_ln=use_ln,
                        p_collapse=p_col,
                        n_realizations=args.n_realizations,
                        k_band=[3.0, 5.0, 7.0],
                    )
                    if born_rows:
                        born_vals.extend(born_rows)

                    if p_col > 0:
                        decoh = collapse_purity(graph, use_ln, p_col, args.n_realizations)
                        grav = collapse_gravity(graph, use_ln, p_col, args.n_realizations)
                    else:
                        decoh = unitary_pur_min(graph, use_ln)
                        grav = collapse_gravity(graph, use_ln, 0.0, args.n_realizations)

                    if not math.isnan(decoh) and not math.isnan(grav):
                        decoh_vals.append(decoh)
                        grav_vals.append(grav)
                        ok += 1

                if not decoh_vals or not grav_vals:
                    born = "FAIL"
                    metric = "FAIL"
                    gsig = "FAIL"
                else:
                    born = fmt(born_vals)
                    metric = fmt(decoh_vals)
                    gmean, gse = mean_se(grav_vals)
                    gsig = "FAIL" if math.isnan(gmean) or gse <= 1e-12 else f"{(gmean / gse):+.1f}"

                print(
                    f"  {npl:4d}  {label:>16s}  {born:>14s}  {metric:>16s}  "
                    f"{fmt(grav_vals, signed=True):>14s}  {gsig:>6s}  {ok:3d}"
                )
            print()
        print()


if __name__ == "__main__":
    main()
