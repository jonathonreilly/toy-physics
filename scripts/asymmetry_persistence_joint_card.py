#!/usr/bin/env python3
"""Dense same-graph joint card for generated asymmetry persistence.

Measures, on the same generated 3D graphs:
- CL-bath purity (`pur_cl`)
- minimum purity (`pur_min`)
- gravity delta
- corrected Born metric (`|I3|/P` with `-P(empty)`)

Compares baseline generated graphs (threshold 0) against the retained
asymmetry-persistence thresholds under both linear and layer-normalized
propagation.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.asymmetry_persistence_pilot import generate_3d_asymmetry_persistence_dag
from scripts.gap_topological_asymmetry import LAM, N_YBINS, bin_amplitudes_3d, cl_purity
from scripts.gap_topological_asymmetry_layernorm_combo import (
    K_BAND,
    compute_field_3d,
    propagate_3d_layernorm,
    propagate_3d_linear,
    purity_min,
)


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fmt(vals, signed=False, sci=False):
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    if sci:
        return f"{m:.2e}"
    if signed:
        return f"{m:+.3f}±{se:.3f}"
    return f"{m:.3f}±{se:.3f}"


def choose_npl(nl: int, arg_npl: int | None) -> int:
    if arg_npl is not None:
        return arg_npl
    if nl >= 100:
        return 60
    if nl >= 80:
        return 50
    return 30


def build_graph(nl, seed, thresh, npl, xyz_range, connect_radius):
    positions, adj, barrier_layer = generate_3d_asymmetry_persistence_dag(
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
    if not det_list:
        return None

    cy = sum(y for _, y, _ in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]

    slit_upper = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_lower = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_upper or not slit_lower:
        return None
    blocked_two = set(bi) - set(slit_upper + slit_lower)

    # Three-slit groups for the corrected Sorkin metric.
    sa3 = [i for i in bi if positions[i][1] > cy + 4][:2]
    sb3 = [i for i in bi if cy - 1 < positions[i][1] < cy + 1][:2]
    sc3 = [i for i in bi if positions[i][1] < cy - 4][:2]
    if not sa3 or not sb3 or not sc3:
        return None
    all_three = set(sa3 + sb3 + sc3)
    blocked_three = set(bi) - all_three

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mid = []
    mid_mass = []
    for layer in layers[start:stop]:
        layer_nodes = by_layer[layer]
        mid.extend(layer_nodes)
        mid_mass.extend(i for i in layer_nodes if abs(positions[i][1] - cy) <= 3.0)

    field = compute_field_3d(positions, list(set(mid_mass) | set(mass_nodes)))
    field_flat = [0.0] * len(positions)
    keep_frac = len(positions) / (1 + (nl - 1) * npl)

    return {
        "positions": positions,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "blocked_two": blocked_two,
        "slit_upper": slit_upper,
        "slit_lower": slit_lower,
        "blocked_three": blocked_three,
        "sa3": sa3,
        "sb3": sb3,
        "sc3": sc3,
        "mid": mid,
        "field": field,
        "field_flat": field_flat,
        "keep_frac": keep_frac,
    }


def total_prob(prop, graph, k, open_slits):
    all_three = set(graph["sa3"] + graph["sb3"] + graph["sc3"])
    blocked = graph["blocked_three"] | (all_three - set(open_slits))
    amps = prop(graph["positions"], graph["adj"], graph["field"], graph["src"], k, blocked)
    return sum(abs(amps[d]) ** 2 for d in graph["det_list"])


def measure_case(graph, use_ln):
    prop = propagate_3d_layernorm if use_ln else propagate_3d_linear
    pur_cl_vals = []
    pur_min_vals = []
    grav_vals = []
    born_vals = []

    sa3 = set(graph["sa3"])
    sb3 = set(graph["sb3"])
    sc3 = set(graph["sc3"])

    for k in K_BAND:
        # Gravity
        am = prop(graph["positions"], graph["adj"], graph["field"], graph["src"], k, graph["blocked_two"])
        af = prop(graph["positions"], graph["adj"], graph["field_flat"], graph["src"], k, graph["blocked_two"])
        pm = sum(abs(am[d]) ** 2 for d in graph["det_list"])
        pf = sum(abs(af[d]) ** 2 for d in graph["det_list"])
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * graph["positions"][d][1] for d in graph["det_list"]) / pm
            yf = sum(abs(af[d]) ** 2 * graph["positions"][d][1] for d in graph["det_list"]) / pf
            grav_vals.append(ym - yf)

        # CL-bath purity and pur_min
        aa = prop(
            graph["positions"], graph["adj"], graph["field"], graph["src"], k,
            graph["blocked_two"] | set(graph["slit_lower"])
        )
        ab = prop(
            graph["positions"], graph["adj"], graph["field"], graph["src"], k,
            graph["blocked_two"] | set(graph["slit_upper"])
        )
        ba = bin_amplitudes_3d(aa, graph["positions"], graph["mid"])
        bb = bin_amplitudes_3d(ab, graph["positions"], graph["mid"])
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM ** 2 * Sn)
        pc = cl_purity(aa, ab, D_cl, graph["det_list"])
        pmn = purity_min(aa, ab, graph["det_list"])
        if not math.isnan(pc):
            pur_cl_vals.append(pc)
        if not math.isnan(pmn):
            pur_min_vals.append(pmn)

        # Corrected Born metric
        P_abc = total_prob(prop, graph, k, sa3 | sb3 | sc3)
        P_ab = total_prob(prop, graph, k, sa3 | sb3)
        P_ac = total_prob(prop, graph, k, sa3 | sc3)
        P_bc = total_prob(prop, graph, k, sb3 | sc3)
        P_a = total_prob(prop, graph, k, sa3)
        P_b = total_prob(prop, graph, k, sb3)
        P_c = total_prob(prop, graph, k, sc3)
        P_empty = total_prob(prop, graph, k, set())
        if P_abc > 1e-30:
            I3 = P_abc - P_ab - P_ac - P_bc + P_a + P_b + P_c - P_empty
            born_vals.append(abs(I3) / P_abc)

    if not pur_cl_vals or not pur_min_vals or not grav_vals or not born_vals:
        return None
    return {
        "pur_cl": sum(pur_cl_vals) / len(pur_cl_vals),
        "pur_min": sum(pur_min_vals) / len(pur_min_vals),
        "gravity": sum(grav_vals) / len(grav_vals),
        "born": sum(born_vals) / len(born_vals),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[80, 100])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.0, 0.1, 0.2])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--npl", type=int, default=None)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 172)
    print("ASYMMETRY PERSISTENCE JOINT CARD")
    print("  Dense 3D same-graph card: pur_cl, pur_min, gravity, Born")
    print(
        f"  N={args.n_layers}, thresholds={args.thresholds}, seeds={args.n_seeds}, "
        f"xyz_range={args.xyz_range}, r={args.connect_radius}"
    )
    print("=" * 172)
    print()

    for nl in args.n_layers:
        npl = choose_npl(nl, args.npl)
        print(f"N = {nl}  (npl = {npl})")
        print(
            f"  {'thr':>4s}  {'keep%':>6s}  {'pur_cl lin':>12s}  {'pur_cl ln':>12s}  "
            f"{'pur_min lin':>13s}  {'pur_min ln':>12s}  {'grav lin':>14s}  "
            f"{'grav ln':>14s}  {'born lin':>10s}  {'born ln':>10s}  {'ok':>3s}"
        )
        print("  " + "-" * 138)
        for thresh in args.thresholds:
            keeps = []
            pcl_lin = []
            pcl_ln = []
            pmin_lin = []
            pmin_ln = []
            grav_lin = []
            grav_ln = []
            born_lin = []
            born_ln = []
            for seed in seeds:
                graph = build_graph(nl, seed, thresh, npl, args.xyz_range, args.connect_radius)
                if graph is None:
                    continue
                lin = measure_case(graph, False)
                ln = measure_case(graph, True)
                if lin is None or ln is None:
                    continue
                keeps.append(100.0 * graph["keep_frac"])
                pcl_lin.append(lin["pur_cl"])
                pcl_ln.append(ln["pur_cl"])
                pmin_lin.append(lin["pur_min"])
                pmin_ln.append(ln["pur_min"])
                grav_lin.append(lin["gravity"])
                grav_ln.append(ln["gravity"])
                born_lin.append(lin["born"])
                born_ln.append(ln["born"])

            keep_s = "FAIL" if not keeps else f"{sum(keeps)/len(keeps):5.1f}%"
            print(
                f"  {thresh:4.2f}  {keep_s:>6s}  {fmt(pcl_lin):>12s}  {fmt(pcl_ln):>12s}  "
                f"{fmt(pmin_lin):>13s}  {fmt(pmin_ln):>12s}  {fmt(grav_lin, True):>14s}  "
                f"{fmt(grav_ln, True):>14s}  {fmt(born_lin, sci=True):>10s}  "
                f"{fmt(born_ln, sci=True):>10s}  {len(pcl_lin):3d}"
            )
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
