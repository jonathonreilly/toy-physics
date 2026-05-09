#!/usr/bin/env python3
"""Corrected Born calibration for the generated asymmetry-persistence lane.

This is the review-safe Born harness for the same dense 3D generated graphs
used by the asymmetry-persistence joint card.

It compares, on matched seeds and the same graph family:

- baseline generated geometry
- asymmetry persistence
- asymmetry persistence + layer normalization
- asymmetry persistence + layer normalization + stochastic collapse

The Born metric is the corrected 3-slit Sorkin quantity with the required
`-P(empty)` term.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys

# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800` means the
# audit-lane precompute and live audit runner allow up to 30 min of wall
# time before recording a timeout. The 120 s default ceiling is too tight
# under concurrency contention. See `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.asymmetry_persistence_collapse_pilot import (
    make_collapse_phase_map,
    propagate_with_collapse,
)
from scripts.asymmetry_persistence_joint_card import build_graph
from scripts.gap_topological_asymmetry_layernorm_combo import (
    K_BAND,
    propagate_3d_layernorm,
    propagate_3d_linear,
)


def choose_npl(nl: int, arg_npl: int | None) -> int:
    if arg_npl is not None:
        return arg_npl
    if nl >= 100:
        return 60
    if nl >= 80:
        return 50
    return 30


def choose_mass_set(graph) -> set[int]:
    positions = graph["positions"]
    by_layer: dict[int, list[int]] = {}
    for idx, (x, y, z) in enumerate(positions):
        by_layer.setdefault(round(x), []).append(idx)
    layers = sorted(by_layer.keys())
    cy = sum(y for _, y, _ in positions) / len(positions)
    bl_idx = len(layers) // 3
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(len(layers) / 6)))
    mass_set: set[int] = set()
    for layer in layers[start:stop]:
        for i in by_layer[layer]:
            if abs(positions[i][1] - cy) <= 3.0:
                mass_set.add(i)
    return mass_set


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fmt(vals):
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    return f"{m:.2e}±{se:.1e}"


def total_prob_linear(prop, graph, k, open_set):
    all_three = set(graph["sa3"] + graph["sb3"] + graph["sc3"])
    blocked = graph["blocked_three"] | (all_three - set(open_set))
    amps = prop(graph["positions"], graph["adj"], graph["field"], graph["src"], k, blocked)
    return sum(abs(amps[d]) ** 2 for d in graph["det_list"])


def total_prob_collapse(graph, k, open_set, use_ln, collapse_phase):
    all_three = set(graph["sa3"] + graph["sb3"] + graph["sc3"])
    blocked = graph["blocked_three"] | (all_three - set(open_set))
    amps = propagate_with_collapse(
        graph["positions"],
        graph["adj"],
        graph["field"],
        graph["src"],
        k,
        blocked,
        collapse_phase,
        use_ln=use_ln,
    )
    return sum(abs(amps[d]) ** 2 for d in graph["det_list"])


def born_rows_for_graph(graph, *, use_ln: bool, p_collapse: float, n_realizations: int, k_band):
    sa3 = set(graph["sa3"])
    sb3 = set(graph["sb3"])
    sc3 = set(graph["sc3"])

    vals = []
    for k in k_band:
        for r in range(n_realizations):
            seed_base = 100000 * r + int(round(100 * k))

            if p_collapse > 0:
                if "mass_set" not in graph:
                    graph["mass_set"] = choose_mass_set(graph)
                collapse_phase = make_collapse_phase_map(graph["mass_set"], p_collapse, seed_base)

                def total_prob(open_set):
                    return total_prob_collapse(
                        graph,
                        k,
                        open_set,
                        use_ln,
                        collapse_phase,
                    )
            else:
                prop = propagate_3d_layernorm if use_ln else propagate_3d_linear

                def total_prob(open_set):
                    return total_prob_linear(prop, graph, k, open_set)

            P_abc = total_prob(sa3 | sb3 | sc3)
            if P_abc <= 1e-30:
                continue
            P_ab = total_prob(sa3 | sb3)
            P_ac = total_prob(sa3 | sc3)
            P_bc = total_prob(sb3 | sc3)
            P_a = total_prob(sa3)
            P_b = total_prob(sb3)
            P_c = total_prob(sc3)
            P_empty = total_prob(set())
            I3 = P_abc - P_ab - P_ac - P_bc + P_a + P_b + P_c - P_empty
            vals.append(abs(I3) / P_abc)

    return vals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[80, 100])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.0, 0.1, 0.2])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--n-realizations", type=int, default=12)
    parser.add_argument("--npl", type=int, default=None)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--collapse-p", type=float, default=0.2)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 132)
    print("ASYMMETRY PERSISTENCE CORRECTED BORN CALIBRATION")
    print("  Same dense graphs / corrected Sorkin I3 with -P(empty)")
    print(
        f"  N={args.n_layers}, thresholds={args.thresholds}, seeds={args.n_seeds}, "
        f"n_realizations={args.n_realizations}, collapse_p={args.collapse_p}"
    )
    print("=" * 132)
    print()

    configs = [
        ("linear", False, 0.0),
        ("persistence", False, 0.0),
        ("persistence+LN", True, 0.0),
        ("persistence+LN+collapse", True, args.collapse_p),
    ]

    for nl in args.n_layers:
        npl = choose_npl(nl, args.npl)
        print(f"N = {nl}  (npl = {npl})")
        print(f"  {'thr':>4s}  {'keep%':>6s}  {'linear':>14s}  {'persist':>14s}  {'persist+LN':>14s}  {'persist+LN+coll':>18s}  {'ok':>3s}")
        print("  " + "-" * 118)

        for thresh in args.thresholds:
            keep_vals = []
            rows = {label: [] for label, _, _ in configs}
            valid = 0

            for seed in seeds:
                base_graph = build_graph(nl, seed, 0.0, npl, args.xyz_range, args.connect_radius)
                if base_graph is None:
                    continue
                pers_graph = base_graph if thresh == 0.0 else build_graph(
                    nl, seed, thresh, npl, args.xyz_range, args.connect_radius
                )
                if pers_graph is None:
                    continue
                keep_vals.append(100.0 * pers_graph["keep_frac"])

                vals = born_rows_for_graph(
                    base_graph,
                    use_ln=False,
                    p_collapse=0.0,
                    n_realizations=args.n_realizations,
                    k_band=K_BAND,
                )
                if vals:
                    rows["linear"].extend(vals)

                for label, use_ln, p_col in configs[1:]:
                    vals = born_rows_for_graph(
                        pers_graph,
                        use_ln=use_ln,
                        p_collapse=p_col,
                        n_realizations=args.n_realizations,
                        k_band=K_BAND,
                    )
                    if vals:
                        rows[label].extend(vals)
                valid += 1

            keep_s = "FAIL" if not keep_vals else f"{sum(keep_vals)/len(keep_vals):5.1f}%"
            out = [
                f"{fmt(rows['linear']):>14s}",
                f"{fmt(rows['persistence']):>14s}",
                f"{fmt(rows['persistence+LN']):>14s}",
                f"{fmt(rows['persistence+LN+collapse']):>18s}",
            ]
            print(f"  {thresh:4.2f}  {keep_s:>6s}  " + "  ".join(out) + f"  {valid:3d}")
            sys.stdout.flush()
        print()

    print("Thresholds:")
    print("  max |I3|/P < 1e-10 : machine precision")
    print("  max |I3|/P < 1e-2  : practically Born-clean")
    print("  max |I3|/P < 1e-1  : marginal")
    print("  max |I3|/P >= 1e-1 : clear Born violation")


if __name__ == "__main__":
    main()
