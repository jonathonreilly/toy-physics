#!/usr/bin/env python3
"""Large-N same-graph joint card for the dense central-band hard-geometry lane.

This is the continuation of the retained dense central-band same-graph card.
It fixes the geometry to the large-N pocket and checks whether the
`N=60` coexistence row survives at `N=80` and `N=100`.

The card reports, on the same graphs:
- corrected three-slit Born metric
- unitary decoherence floor (`pur_min`) or collapse purity
- gravity centroid delta

Retained rows:
- `LN + |y|` 
- `LN + |y| + collapse`
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.central_band_dense_joint_card import (
    attach_field,
    collapse_gravity,
    collapse_purity,
    unitary_pur_min,
)
from scripts.stochastic_collapse_born_calibration import (
    born_metric_for_graph,
    build_graph,
    mean_se,
)

K_BAND = [3.0, 5.0, 7.0]


def fmt(vals, signed=False):
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    if signed:
        return f"{m:+.3f}±{se:.3f}"
    return f"{m:.3f}±{se:.3f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[80, 100])
    parser.add_argument("--n-seeds", type=int, default=4)
    parser.add_argument("--n-realizations", type=int, default=8)
    parser.add_argument("--npl", type=int, default=60)
    parser.add_argument("--yz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 136)
    print("CENTRAL-BAND DENSE LARGE-N SAME-GRAPH JOINT CARD")
    print("  corrected Born + pur_min/purity + gravity on the same dense central-band graphs")
    print(
        f"  seeds={args.n_seeds}, realizations={args.n_realizations}, npl={args.npl}, "
        f"yz_range={args.yz_range}, r={args.connect_radius}, y_cut={args.y_cut}, p={args.p_collapse}"
    )
    print("=" * 136)
    print()

    rows = [
        ("LN+|y|", True, 0.0),
        ("LN+|y|+collapse", True, args.p_collapse),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'mode':>16s}  {'Born |I3|/P':>14s}  {'pur_min/purity':>16s}  "
            f"{'gravity':>14s}  {'g/SE':>6s}  {'ok':>3s}"
        )
        print("  " + "-" * 104)

        for label, use_ln, p_col in rows:
            born_vals = []
            decoh_vals = []
            grav_vals = []
            ok = 0
            for seed in seeds:
                graph = build_graph(nl, seed, args.npl, args.yz_range, args.connect_radius, args.y_cut)
                if graph is None:
                    continue
                graph = attach_field(graph)

                born_rows = born_metric_for_graph(
                    graph,
                    use_ln=use_ln,
                    p_collapse=p_col,
                    n_realizations=args.n_realizations,
                    k_band=K_BAND,
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

            gmean, gse = mean_se(grav_vals)
            gsig = gmean / gse if not math.isnan(gmean) and gse > 1e-12 else math.nan
            print(
                f"  {label:>16s}  {fmt(born_vals):>14s}  {fmt(decoh_vals):>16s}  "
                f"{fmt(grav_vals, signed=True):>14s}  {('FAIL' if math.isnan(gsig) else f'{gsig:+.1f}'):>6s}  {ok:3d}"
            )
        print()

    print("Thresholds:")
    print("  max |I3|/P < 1e-10 : machine precision")
    print("  max |I3|/P < 1e-2  : practically Born-clean")
    print("  max |I3|/P < 1e-1  : marginal")
    print("  max |I3|/P >= 1e-1 : clear Born violation")


if __name__ == "__main__":
    main()
