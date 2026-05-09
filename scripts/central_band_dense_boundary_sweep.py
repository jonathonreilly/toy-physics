#!/usr/bin/env python3
"""Boundary sweep for the dense central-band same-graph joint card.

This explores whether the dense central-band coexistence pocket at
`connect_radius = 3.0` is a sharp boundary or whether there is a nearby
radius window where gravity improves while Born cleanliness is retained.
"""

from __future__ import annotations

import argparse
import math
import os
import sys

# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800` means the
# audit-lane precompute and live audit runner allow up to 30 min of wall
# time before recording a timeout. The 120 s default ceiling is too tight
# under concurrency contention. See `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

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
    parser.add_argument("--connect-radii", nargs="+", type=float, default=[2.8, 3.0, 3.2, 3.4])
    parser.add_argument("--y-cut", type=float, default=2.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    rows = [
        ("LN+|y|", True, 0.0),
        ("LN+|y|+collapse", True, args.p_collapse),
    ]

    print("=" * 136)
    print("CENTRAL-BAND DENSE BOUNDARY SWEEP")
    print("  probe the connect-radius edge of the dense central-band joint pocket")
    print(
        f"  seeds={args.n_seeds}, realizations={args.n_realizations}, npl={args.npl}, "
        f"yz_range={args.yz_range}, y_cut={args.y_cut}, p={args.p_collapse}"
    )
    print("=" * 136)
    print()

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'r':>4s}  {'mode':>16s}  {'Born |I3|/P':>14s}  {'pur_min/purity':>16s}  "
            f"{'gravity':>14s}  {'g/SE':>6s}  {'ok':>3s}"
        )
        print("  " + "-" * 116)

        for r in args.connect_radii:
            for label, use_ln, p_col in rows:
                born_vals = []
                decoh_vals = []
                grav_vals = []
                ok = 0
                for seed in seeds:
                    graph = build_graph(nl, seed, args.npl, args.yz_range, r, args.y_cut)
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
                    f"  {r:4.1f}  {label:>16s}  {fmt(born_vals):>14s}  {fmt(decoh_vals):>16s}  "
                    f"{fmt(grav_vals, signed=True):>14s}  {('FAIL' if math.isnan(gsig) else f'{gsig:+.1f}'):>6s}  {ok:3d}"
                )
            print()
        print()


if __name__ == "__main__":
    main()
