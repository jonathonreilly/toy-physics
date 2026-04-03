#!/usr/bin/env python3
"""Collapse-strength sweep for the dense central-band corrected Born pocket.

This is a small wrapper around the corrected 3D chokepoint Born calibration.
It keeps the central-band hard-geometry lane fixed and sweeps the stochastic
collapse probability `p` so we can ask whether a smaller collapse rate opens a
cleaner Born-safe pocket.
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
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60])
    parser.add_argument("--p-collapses", nargs="+", type=float, default=[0.05, 0.1, 0.2])
    parser.add_argument("--n-seeds", type=int, default=6)
    parser.add_argument("--n-realizations", type=int, default=8)
    parser.add_argument("--npl", type=int, default=60)
    parser.add_argument("--yz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    k_band = [3.0, 5.0, 7.0]

    print("=" * 124)
    print("CENTRAL-BAND COLLAPSE-STRENGTH SWEEP")
    print("  corrected three-slit I3 with -P(empty), varying stochastic-collapse p")
    print(
        f"  seeds={args.n_seeds}, realizations={args.n_realizations}, npl={args.npl}, "
        f"yz_range={args.yz_range}, r={args.connect_radius}, y_cut={args.y_cut}, p={args.p_collapses}"
    )
    print("=" * 124)
    print()

    configs = [
        ("linear", False, 0.0, False),
        ("LN", True, 0.0, False),
        ("LN+|y|", True, 0.0, False),
        ("LN+|y|+collapse", True, 0.0, True),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(f"  {'p':>5s}  {'mode':>16s}  {'|I3|/P':>28s}  {'ok':>3s}  verdict")
        print("  " + "-" * 72)

        for p_col in args.p_collapses:
            for label, use_ln, fixed_p, p_dep in configs:
                vals = []
                n_ok = 0
                for seed in seeds:
                    graph = build_graph(
                        nl,
                        seed,
                        args.npl,
                        args.yz_range,
                        args.connect_radius,
                        args.y_cut,
                    )
                    if graph is None:
                        continue
                    rows = born_metric_for_graph(
                        graph,
                        use_ln=use_ln,
                        p_collapse=p_col if p_dep else fixed_p,
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

                print(f"  {p_col:5.2f}  {label:>16s}  {metric:>28s}  {n_ok:3d}  {verdict}")
            print()
        print()

    print("Thresholds:")
    print("  max |I3|/P < 1e-10 : machine precision")
    print("  max |I3|/P < 1e-2  : practically Born-clean")
    print("  max |I3|/P < 1e-1  : marginal")
    print("  max |I3|/P >= 1e-1 : clear Born violation")


if __name__ == "__main__":
    main()
