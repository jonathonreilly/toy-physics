#!/usr/bin/env python3
"""Review-safe gravity window sweep for the retained hard-geometry lanes.

This script compares the two surviving hard-geometry families on the same
Born-safe lens:

* central-band hard geometry
* generated asymmetry-persistence hard geometry

For each family it sweeps a small geometry window and a small field-strength
window, then reports:

* linear gravity delta
* layernorm gravity delta
* layernorm minimum purity (`pur_min`)
* corrected Born `|I3|/P` on the LN lane

The goal is not to claim a new universal law. The goal is to identify the
strongest review-safe gravity pocket, and whether it is central-band-like,
generated-geometry-like, or neither.
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import argparse
import copy
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.asymmetry_persistence_joint_card import build_graph as build_asymmetry_graph
from scripts.central_band_dense_joint_card import attach_field
from scripts.central_band_layernorm_combo import purity_min
from scripts.gap_topological_asymmetry_layernorm_combo import (
    K_BAND,
    propagate_3d_layernorm,
    propagate_3d_linear,
)
from scripts.stochastic_collapse_born_calibration import (
    born_metric_for_graph,
    build_graph as build_central_graph,
)


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fmt(vals, signed=False):
    mean, se = mean_se(vals)
    if math.isnan(mean):
        return "FAIL"
    if signed:
        return f"{mean:+.3f}±{se:.3f}"
    return f"{mean:.3f}±{se:.3f}"


def choose_npl(nl: int, arg_npl: int | None) -> int:
    if arg_npl is not None:
        return arg_npl
    if nl >= 100:
        return 60
    if nl >= 80:
        return 50
    return 30


def scale_graph_field(graph, scale: float):
    scaled = dict(graph)
    scaled["field"] = [v * scale for v in graph["field"]]
    if "field_flat" in graph:
        scaled["field_flat"] = [0.0 for _ in graph["field_flat"]]
    return scaled


def gravity_and_purity(graph):
    positions = graph["positions"]
    det_list = graph["det_list"]
    src = graph["src"]
    blocked = graph["base_blocked"] if "base_blocked" in graph else graph["blocked_three"]
    sa = set(graph["slit_a"]) if "slit_a" in graph else set(graph["sa3"])
    sb = set(graph["slit_b"]) if "slit_b" in graph else set(graph["sb3"])
    field = graph["field"]
    field_flat = graph.get("field_flat", [0.0] * len(positions))

    grav_lin = []
    grav_ln = []
    pmin_lin = []
    pmin_ln = []

    prop_lin = propagate_3d_linear
    prop_ln = propagate_3d_layernorm

    for k in K_BAND:
        am_lin = prop_lin(positions, graph["adj"], field, src, k, blocked)
        af_lin = prop_lin(positions, graph["adj"], field_flat, src, k, blocked)
        am_ln = prop_ln(positions, graph["adj"], field, src, k, blocked)
        af_ln = prop_ln(positions, graph["adj"], field_flat, src, k, blocked)

        pm_lin = sum(abs(am_lin[d]) ** 2 for d in det_list)
        pf_lin = sum(abs(af_lin[d]) ** 2 for d in det_list)
        pm_ln = sum(abs(am_ln[d]) ** 2 for d in det_list)
        pf_ln = sum(abs(af_ln[d]) ** 2 for d in det_list)

        if pm_lin > 1e-30 and pf_lin > 1e-30:
            ym = sum(abs(am_lin[d]) ** 2 * positions[d][1] for d in det_list) / pm_lin
            yf = sum(abs(af_lin[d]) ** 2 * positions[d][1] for d in det_list) / pf_lin
            grav_lin.append(ym - yf)
        if pm_ln > 1e-30 and pf_ln > 1e-30:
            ym = sum(abs(am_ln[d]) ** 2 * positions[d][1] for d in det_list) / pm_ln
            yf = sum(abs(af_ln[d]) ** 2 * positions[d][1] for d in det_list) / pf_ln
            grav_ln.append(ym - yf)

        aa_lin = prop_lin(positions, graph["adj"], field, src, k, blocked | sb)
        ab_lin = prop_lin(positions, graph["adj"], field, src, k, blocked | sa)
        aa_ln = prop_ln(positions, graph["adj"], field, src, k, blocked | sb)
        ab_ln = prop_ln(positions, graph["adj"], field, src, k, blocked | sa)
        pmin_lin.append(purity_min(aa_lin, ab_lin, det_list))
        pmin_ln.append(purity_min(aa_ln, ab_ln, det_list))

    def avg(vals):
        vals = [v for v in vals if not math.isnan(v)]
        return math.nan if not vals else sum(vals) / len(vals)

    return {
        "grav_lin": avg(grav_lin),
        "grav_ln": avg(grav_ln),
        "pmin_lin": avg(pmin_lin),
        "pmin_ln": avg(pmin_ln),
    }


def born_ln_central(graph, n_realizations: int, k_band):
    return born_metric_for_graph(
        graph,
        use_ln=True,
        p_collapse=0.0,
        n_realizations=n_realizations,
        k_band=k_band,
    )


def born_ln_asymmetry(graph, n_realizations: int, k_band):
    # The asymmetry graph uses the same corrected Sorkin structure as the
    # joint-card note, but we only need the LN lane here.
    sa3 = set(graph["sa3"])
    sb3 = set(graph["sb3"])
    sc3 = set(graph["sc3"])
    blocked = graph["blocked_three"]
    positions = graph["positions"]
    det_list = graph["det_list"]
    vals = []
    for k in k_band:
        for _ in range(n_realizations):
            def total_prob(open_set):
                closed = (sa3 | sb3 | sc3) - set(open_set)
                amps = propagate_3d_layernorm(
                    positions,
                    graph["adj"],
                    graph["field"],
                    graph["src"],
                    k,
                    blocked | closed,
                )
                return sum(abs(amps[d]) ** 2 for d in det_list)

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
    parser.add_argument("--n-layers", nargs="+", type=int, default=[60, 80, 100])
    parser.add_argument("--field-scales", nargs="+", type=float, default=[0.5, 1.0, 1.5])
    parser.add_argument("--central-y-cuts", nargs="+", type=float, default=[1.0, 2.0, 3.0])
    parser.add_argument("--asym-thresholds", nargs="+", type=float, default=[0.05, 0.10, 0.20])
    parser.add_argument("--n-seeds", type=int, default=6)
    parser.add_argument("--n-realizations", type=int, default=1)
    parser.add_argument("--central-npl", type=int, default=60)
    parser.add_argument("--asym-npl", type=int, default=None)
    parser.add_argument("--central-yz-range", type=float, default=12.0)
    parser.add_argument("--asym-xyz-range", type=float, default=12.0)
    parser.add_argument("--central-connect-radius", type=float, default=3.0)
    parser.add_argument("--asym-connect-radius", type=float, default=4.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    k_band = list(K_BAND)

    print("=" * 176)
    print("HARD-GEOMETRY GRAVITY WINDOW")
    print("  Compare central-band vs generated asymmetry hard-geometry lanes under the same Born-safe lens")
    print(
        f"  seeds={args.n_seeds}, field_scales={args.field_scales}, "
        f"central_y_cuts={args.central_y_cuts}, asym_thresholds={args.asym_thresholds}"
    )
    print("=" * 176)
    print()

    results = []

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'family':>10s}  {'param':>7s}  {'scale':>5s}  {'grav_lin':>13s}  "
            f"{'grav_ln':>13s}  {'pmin_ln':>10s}  {'born_ln':>11s}  {'ok':>3s}"
        )
        print("  " + "-" * 96)

        # Central-band family
        for y_cut in args.central_y_cuts:
            for scale in args.field_scales:
                grav_lin_vals = []
                grav_ln_vals = []
                pmin_ln_vals = []
                born_vals = []
                ok = 0
                for seed in seeds:
                    graph = build_central_graph(
                        nl,
                        seed,
                        args.central_npl,
                        args.central_yz_range,
                        args.central_connect_radius,
                        y_cut,
                    )
                    if graph is None:
                        continue
                    graph = attach_field(graph)
                    graph = scale_graph_field(graph, scale)
                    measures = gravity_and_purity(graph)
                    born_rows = born_ln_central(graph, args.n_realizations, k_band)
                    if math.isnan(measures["grav_ln"]) or not born_rows:
                        continue
                    grav_lin_vals.append(measures["grav_lin"])
                    grav_ln_vals.append(measures["grav_ln"])
                    pmin_ln_vals.append(measures["pmin_ln"])
                    born_vals.extend(born_rows)
                    ok += 1
                born_m, born_se = mean_se(born_vals)
                born_max = max(born_vals) if born_vals else math.nan
                print(
                    f"  {'central':>10s}  {y_cut:7.2f}  {scale:5.2f}  {fmt(grav_lin_vals, True):>13s}  "
                    f"{fmt(grav_ln_vals, True):>13s}  {fmt(pmin_ln_vals):>10s}  "
                    f"{born_max:.2e}" if born_vals else f"  {'central':>10s}  {y_cut:7.2f}  {scale:5.2f}  FAIL".ljust(96)
                )
                results.append(
                    {
                        "family": "central",
                        "param": y_cut,
                        "scale": scale,
                        "grav_ln": mean_se(grav_ln_vals)[0],
                        "grav_ln_se": mean_se(grav_ln_vals)[1],
                        "grav_lin": mean_se(grav_lin_vals)[0],
                        "pmin_ln": mean_se(pmin_ln_vals)[0],
                        "born_max": born_max,
                        "ok": ok,
                    }
                )

        # Generated asymmetry family
        npl_asym = choose_npl(nl, args.asym_npl)
        for thresh in args.asym_thresholds:
            for scale in args.field_scales:
                grav_lin_vals = []
                grav_ln_vals = []
                pmin_ln_vals = []
                born_vals = []
                ok = 0
                for seed in seeds:
                    graph = build_asymmetry_graph(
                        nl,
                        seed,
                        thresh,
                        npl_asym,
                        args.asym_xyz_range,
                        args.asym_connect_radius,
                    )
                    if graph is None:
                        continue
                    graph = scale_graph_field(graph, scale)
                    measures = gravity_and_purity(graph)
                    born_rows = born_ln_asymmetry(graph, args.n_realizations, k_band)
                    if math.isnan(measures["grav_ln"]) or not born_rows:
                        continue
                    grav_lin_vals.append(measures["grav_lin"])
                    grav_ln_vals.append(measures["grav_ln"])
                    pmin_ln_vals.append(measures["pmin_ln"])
                    born_vals.extend(born_rows)
                    ok += 1
                born_m, born_se = mean_se(born_vals)
                born_max = max(born_vals) if born_vals else math.nan
                print(
                    f"  {'asym':>10s}  {thresh:7.2f}  {scale:5.2f}  {fmt(grav_lin_vals, True):>13s}  "
                    f"{fmt(grav_ln_vals, True):>13s}  {fmt(pmin_ln_vals):>10s}  "
                    f"{born_max:.2e}" if born_vals else f"  {'asym':>10s}  {thresh:7.2f}  {scale:5.2f}  FAIL".ljust(96)
                )
                results.append(
                    {
                        "family": "asym",
                        "param": thresh,
                        "scale": scale,
                        "grav_ln": mean_se(grav_ln_vals)[0],
                        "grav_ln_se": mean_se(grav_ln_vals)[1],
                        "grav_lin": mean_se(grav_lin_vals)[0],
                        "pmin_ln": mean_se(pmin_ln_vals)[0],
                        "born_max": born_max,
                        "ok": ok,
                    }
                )
        print()

    born_safe = [r for r in results if not math.isnan(r["born_max"]) and r["born_max"] < 1e-10]
    if born_safe:
        best = max(born_safe, key=lambda r: (r["grav_ln"] if not math.isnan(r["grav_ln"]) else -1e9))
        print("Best Born-safe LN gravity pocket")
        print(
            f"  family={best['family']}, param={best['param']}, scale={best['scale']}, "
            f"grav_ln={best['grav_ln']:+.3f}±{best['grav_ln_se']:.3f}, "
            f"grav_lin={best['grav_lin']:+.3f}, pur_min={best['pmin_ln']:.3f}, "
            f"born_max={best['born_max']:.2e}, ok={best['ok']}"
        )
    else:
        print("No Born-safe LN pocket found in the scanned window.")


if __name__ == "__main__":
    main()
