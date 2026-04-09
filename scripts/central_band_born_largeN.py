#!/usr/bin/env python3
"""Large-N corrected Born sweep for the dense central-band hard-geometry lane.

This is a small, review-safe wrapper around the corrected three-slit Born
calibration. It fixes the target regime to the large-N extension that actually
survives the corrected harness:

- N = 80, 100
- dense setting around npl = 60
- central-band |y| removal after the barrier
- optional stochastic collapse on top of LN / LN+|y|

The goal is to make the surviving large-N pocket easy to rerun and compare.
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.stochastic_collapse_born_calibration import (
    born_metric_for_graph,
    build_graph,
    mean_se,
)


def fmt(vals):
    mean, se = mean_se(vals)
    if math.isnan(mean):
        return "FAIL"
    mx = max(vals) if vals else math.nan
    return f"{mean:.2e}±{se:.1e} (max {mx:.2e})"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[80, 100])
    parser.add_argument("--npl", nargs="+", type=int, default=[60])
    parser.add_argument("--n-seeds", type=int, default=4)
    parser.add_argument("--n-realizations", type=int, default=8)
    parser.add_argument("--yz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    parser.add_argument("--y-cut", type=float, default=2.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    k_band = [3.0, 5.0, 7.0]

    print("=" * 126)
    print("CENTRAL-BAND LARGE-N CORRECTED BORN SWEEP")
    print("  dense large-N extension of the central-band hard-geometry lane")
    print(
        f"  seeds={args.n_seeds}, realizations={args.n_realizations}, npl={args.npl}, "
        f"yz_range={args.yz_range}, r={args.connect_radius}, p={args.p_collapse}, y_cut={args.y_cut}"
    )
    print("=" * 126)
    print()

    configs = [
        ("linear", False, 0.0),
        ("LN", True, 0.0),
        ("collapse", False, args.p_collapse),
        ("LN+|y|", True, 0.0),
        ("LN+|y|+collapse", True, args.p_collapse),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(f"  {'npl':>4s}  {'mode':>16s}  {'|I3|/P':>28s}  {'ok':>3s}  verdict")
        print("  " + "-" * 72)

        for npl in args.npl:
            for label, use_ln, p_col in configs:
                vals = []
                n_ok = 0
                for seed in seeds:
                    graph = build_graph(
                        nl,
                        seed,
                        npl,
                        args.yz_range,
                        args.connect_radius,
                        args.y_cut,
                    )
                    if graph is None:
                        continue
                    rows = born_metric_for_graph(
                        graph,
                        use_ln=use_ln,
                        p_collapse=p_col,
                        n_realizations=args.n_realizations,
                        k_band=k_band,
                    )
                    if rows:
                        vals.extend(rows)
                        n_ok += 1

                if not vals:
                    metric = "FAIL"
                    verdict = "FAIL"
                else:
                    metric = fmt(vals)
                    mx = max(vals)
                    verdict = "PASS" if mx < 1e-10 else ("MARGINAL" if mx < 1e-2 else "FAIL")

                print(f"  {npl:4d}  {label:>16s}  {metric:>28s}  {n_ok:3d}  {verdict}")
            print()
        print()


if __name__ == "__main__":
    main()
