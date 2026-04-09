#!/usr/bin/env python3
"""Exact 2D mirror validation: Born + MI + decoherence + gravity.

This is the review-safe 2D mirror artifact chain requested after the
exact-mirror Born audit. It uses the exact 2D mirror generator from
scripts/mirror_born_audit.py and keeps the propagator strictly linear.

The script is intentionally narrow:
  - compare exact 2D mirror vs matched 2D random chokepoint baseline
  - report slit-detector mutual information and purity on the same family
  - report d_TV and a narrow gravity read
  - probe a small fixed-anchor mass window and a small distance sweep only
    if the same family supports them cleanly

If the gravity-side fits are not clean, the note should freeze the joint
result without promoting a mass or distance law.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.mirror_born_audit import gen_2d_mirror, propagate_LINEAR

DEFAULT_K_BAND = [3.0, 5.0, 7.0]


def entropy(probs: list[float]) -> float:
    return -sum(p * math.log2(p) for p in probs if p > 1e-30)


def mean_se(vals: list[float]) -> tuple[float, float]:
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fit_power_law(points: list[tuple[int, float]]):
    usable = [(n, v) for n, v in points if n > 0 and v > 0 and not math.isnan(v)]
    if len(usable) < 3:
        return None
    xs = [math.log(n) for n, _ in usable]
    ys = [math.log(v) for _, v in usable]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 1e-12 or syy <= 1e-12:
        return None
    alpha = sxy / sxx
    coeff = math.exp(my - alpha * mx)
    r2 = (sxy * sxy) / (sxx * syy)
    return coeff, alpha, r2


def gen_random_2d_chokepoint(n_layers, npl_total, yr, cr, seed):
    rng = random.Random(seed)
    pos = []
    adj = defaultdict(list)
    li = []
    for layer in range(n_layers):
        x = float(layer)
        ln = []
        if layer == 0:
            idx = len(pos)
            pos.append((x, 0.0))
            ln.append(idx)
        else:
            for _ in range(npl_total):
                y = rng.uniform(-yr, yr)
                idx = len(pos)
                pos.append((x, y))
                ln.append(idx)
                if li:
                    for prev_idx in li[-1]:
                        px, py = pos[prev_idx]
                        if math.sqrt((x - px) ** 2 + (y - py) ** 2) <= cr:
                            adj[prev_idx].append(idx)
        li.append(ln)
    return pos, dict(adj), n_layers // 3


def propagate_2d(positions, adj, field, src, k, blocked):
    return propagate_LINEAR(positions, adj, field, src, k, blocked)


def compute_field_2d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def mutual_info_and_purity(amps_a, amps_b, det_list):
    pa = [abs(amps_a[d]) ** 2 for d in det_list]
    pb = [abs(amps_b[d]) ** 2 for d in det_list]
    na = sum(pa)
    nb = sum(pb)
    if na < 1e-30 or nb < 1e-30:
        return None

    pa = [p / na for p in pa]
    pb = [p / nb for p in pb]
    pd = [0.5 * a + 0.5 * b for a, b in zip(pa, pb)]

    h_d = entropy(pd)
    h_d_a = entropy(pa)
    h_d_b = entropy(pb)
    mi = h_d - 0.5 * (h_d_a + h_d_b)

    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2] / na
                + amps_b[d1].conjugate() * amps_b[d2] / nb
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_min = sum(abs(v) ** 2 for v in rho.values()).real

    return {"MI": mi, "pur_min": pur_min}


def sorkin_born(positions, adj, src, k, barrier_nodes, slit_a, slit_b, slit_c, det_list, field):
    all_slits = set(slit_a + slit_b + slit_c)
    other = set(barrier_nodes) - all_slits
    probs = {}
    for key, open_set in [
        ("abc", all_slits),
        ("ab", set(slit_a + slit_b)),
        ("ac", set(slit_a + slit_c)),
        ("bc", set(slit_b + slit_c)),
        ("a", set(slit_a)),
        ("b", set(slit_b)),
        ("c", set(slit_c)),
    ]:
        bl = other | (all_slits - open_set)
        amps = propagate_2d(positions, adj, field, src, k, bl)
        probs[key] = [abs(amps[d]) ** 2 for d in det_list]

    i3 = 0.0
    p_abc = 0.0
    for di in range(len(det_list)):
        term = (
            probs["abc"][di]
            - probs["ab"][di]
            - probs["ac"][di]
            - probs["bc"][di]
            + probs["a"][di]
            + probs["b"][di]
            + probs["c"][di]
        )
        i3 += abs(term)
        p_abc += probs["abc"][di]
    return i3 / p_abc if p_abc > 1e-30 else math.nan


def measure_family(n_layers, npl_half, yr, connect_radius, seed, family, k_band):
    if family == "mirror":
        positions, adj, barrier_layer = gen_2d_mirror(n_layers, npl_half, yr, connect_radius, seed)
        npl_total = 2 * npl_half
    else:
        positions, adj, barrier_layer = gen_random_2d_chokepoint(n_layers, 2 * npl_half, yr, connect_radius, seed)
        npl_total = 2 * npl_half

    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y in positions) / len(positions)
    bi = by_layer[layers[len(layers) // 3]]
    slit_a = [i for i in bi if positions[i][1] > cy + 2.0][:3]
    slit_b = [i for i in bi if positions[i][1] < cy - 2.0][:3]
    slit_c = [i for i in bi if abs(positions[i][1] - cy) <= 2.0][:3]
    if not slit_a or not slit_b or not slit_c:
        return None

    blocked = set(bi) - set(slit_a + slit_b + slit_c)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1.0]
    if not mass_nodes:
        return None

    field_m = compute_field_2d(positions, mass_nodes)
    field_f = [0.0] * len(positions)

    mi_vals = []
    pur_vals = []
    dtv_vals = []
    born_vals = []
    grav_vals = []
    grav0_vals = []

    for k in k_band:
        psi_a = propagate_2d(positions, adj, field_m, src, k, blocked | set(slit_b))
        psi_b = propagate_2d(positions, adj, field_m, src, k, blocked | set(slit_a))
        row = mutual_info_and_purity(psi_a, psi_b, det_list)
        if row:
            mi_vals.append(row["MI"])
            pur_vals.append(row["pur_min"])
            pa = {d: abs(psi_a[d]) ** 2 for d in det_list}
            pb = {d: abs(psi_b[d]) ** 2 for d in det_list}
            na = sum(pa.values())
            nb = sum(pb.values())
            if na > 1e-30 and nb > 1e-30:
                dtv_vals.append(0.5 * sum(abs(pa[d] / na - pb[d] / nb) for d in det_list))

        born_vals.append(
            sorkin_born(
                positions, adj, src, k, bi, slit_a, slit_b, slit_c, det_list, field_f
            )
        )

        am = propagate_2d(positions, adj, field_m, src, k, blocked)
        af = propagate_2d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)

        am0 = propagate_2d(positions, adj, field_m, src, 0.0, blocked)
        af0 = propagate_2d(positions, adj, field_f, src, 0.0, blocked)
        pm0 = sum(abs(am0[d]) ** 2 for d in det_list)
        pf0 = sum(abs(af0[d]) ** 2 for d in det_list)
        if pm0 > 1e-30 and pf0 > 1e-30:
            ym0 = sum(abs(am0[d]) ** 2 * positions[d][1] for d in det_list) / pm0
            yf0 = sum(abs(af0[d]) ** 2 * positions[d][1] for d in det_list) / pf0
            grav0_vals.append(ym0 - yf0)

    if not mi_vals:
        return None

    return {
        "MI": sum(mi_vals) / len(mi_vals),
        "pur_min": sum(pur_vals) / len(pur_vals),
        "dTV": sum(dtv_vals) / len(dtv_vals) if dtv_vals else math.nan,
        "born": sum(born_vals) / len(born_vals) if born_vals else math.nan,
        "gravity": sum(grav_vals) / len(grav_vals) if grav_vals else math.nan,
        "k0": sum(grav0_vals) / len(grav0_vals) if grav0_vals else math.nan,
        "npl": npl_total,
        "positions": positions,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "mass_nodes": mass_nodes,
        "cy": cy,
        "barrier_layer": barrier_layer,
        "grav_layer": grav_layer,
    }


def gravity_mass_window(graph, k_band, m_values):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked"]
    mass_nodes = graph["mass_nodes"]

    ordered = sorted(
        mass_nodes,
        key=lambda i: (
            abs(positions[i][1] - (graph["cy"] + 5.0)),
            abs(positions[i][1] - graph["cy"]),
        ),
    )
    rows = []
    for m in m_values:
        if len(ordered) < m:
            rows.append((m, math.nan))
            continue
        vals = []
        field_f = [0.0] * len(positions)
        field_m = compute_field_2d(positions, ordered[:m])
        for k in k_band:
            am = propagate_2d(positions, adj, field_m, src, k, blocked)
            af = propagate_2d(positions, adj, field_f, src, k, blocked)
            pm = sum(abs(am[d]) ** 2 for d in det_list)
            pf = sum(abs(af[d]) ** 2 for d in det_list)
            if pm > 1e-30 and pf > 1e-30:
                ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
                yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
                vals.append(ym - yf)
        rows.append((m, sum(vals) / len(vals) if vals else math.nan))
    return rows


def distance_sweep(graph, k_band, thresholds):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked"]
    grav_layer = graph["grav_layer"]
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    cand = [i for i in by_layer[grav_layer] if positions[i][1] > graph["cy"] + 1.0]
    rows = []
    for thr in thresholds:
        selected = [i for i in cand if positions[i][1] > graph["cy"] + thr][:5]
        if not selected:
            rows.append((thr, math.nan))
            continue
        field_m = compute_field_2d(positions, selected)
        field_f = [0.0] * len(positions)
        vals = []
        for k in k_band:
            am = propagate_2d(positions, adj, field_m, src, k, blocked)
            af = propagate_2d(positions, adj, field_f, src, k, blocked)
            pm = sum(abs(am[d]) ** 2 for d in det_list)
            pf = sum(abs(af[d]) ** 2 for d in det_list)
            if pm > 1e-30 and pf > 1e-30:
                ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
                yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
                vals.append(ym - yf)
        rows.append((thr, sum(vals) / len(vals) if vals else math.nan))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", nargs="+", default=["mirror", "random"])
    parser.add_argument("--n-layers", nargs="+", type=int, default=[15, 25, 40, 60, 80, 100])
    parser.add_argument("--npl-half", type=int, default=12)
    parser.add_argument("--yr", type=float, default=10.0)
    parser.add_argument("--connect-radius", type=float, default=2.5)
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--k-band", nargs="+", type=float, default=DEFAULT_K_BAND)
    parser.add_argument("--m-values", nargs="+", type=int, default=[1, 2, 3, 5, 8, 12, 16])
    parser.add_argument("--distance-thresholds", nargs="+", type=float, default=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    args = parser.parse_args()

    unknown = [fam for fam in args.families if fam not in {"mirror", "random"}]
    if unknown:
        raise SystemExit(f"Unknown family/families: {', '.join(unknown)}")

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 100)
    print("EXACT 2D MIRROR VALIDATION: Born + MI + decoherence + gravity")
    print(f"  npl_half={args.npl_half} (total {2*args.npl_half}), yr={args.yr}, r={args.connect_radius}")
    print(f"  seeds={args.n_seeds}, k-band={args.k_band}")
    print("=" * 100)
    print()

    family_summaries = {}

    for family in args.families:
        print(f"  [{family}]")
        print(f"  {'N':>4s}  {'MI(bits)':>9s}  {'1-pur':>8s}  {'d_TV':>8s}  {'gravity':>10s}  {'Born':>10s}  {'k=0':>10s}  {'n_ok':>4s}")
        print(f"  {'-' * 82}")

        mi_points = []
        pur_points = []
        grav_points = []
        born_points = []
        last_good_graph = None

        for nl in args.n_layers:
            rows = []
            for seed in seeds:
                row = measure_family(
                    n_layers=nl,
                    npl_half=args.npl_half,
                    yr=args.yr,
                    connect_radius=args.connect_radius,
                    seed=seed,
                    family=family,
                    k_band=args.k_band,
                )
                if row:
                    rows.append(row)

            if not rows:
                continue

            mmi, semi = mean_se([r["MI"] for r in rows])
            mpur, se_p = mean_se([r["pur_min"] for r in rows])
            mdtv, se_dtv = mean_se([r["dTV"] for r in rows])
            mgrav, se_grav = mean_se([r["gravity"] for r in rows])
            mborn, se_born = mean_se([r["born"] for r in rows])
            mk0, se_k0 = mean_se([r["k0"] for r in rows])

            print(
                f"  {nl:4d}  {mmi:9.6f}  {1.0-mpur:8.4f}  {mdtv:8.4f}  "
                f"{mgrav:+10.4f}  {mborn:10.2e}  {mk0:+10.2e}  {len(rows):4d}"
            )

            mi_points.append((nl, mmi))
            pur_points.append((nl, 1.0 - mpur))
            grav_points.append((nl, mgrav))
            born_points.append((nl, mborn))
            last_good_graph = rows[-1]

        if mi_points:
            fit = fit_power_law(mi_points)
            if fit:
                coeff, alpha, r2 = fit
                print(f"\n  MI scaling: MI = {coeff:.3g} * N^{alpha:+.3f}  R^2={r2:.3f}")
        if pur_points:
            fit = fit_power_law(pur_points)
            if fit:
                coeff, alpha, r2 = fit
                print(f"  decoh scaling: 1-pur_min = {coeff:.3g} * N^{alpha:+.3f}  R^2={r2:.3f}")
        if grav_points:
            fit = fit_power_law([(n, g) for n, g in grav_points if g > 0])
            if fit:
                coeff, alpha, r2 = fit
                print(f"  gravity scaling: gravity = {coeff:.3g} * N^{alpha:+.3f}  R^2={r2:.3f}")
        if born_points:
            print(f"  Born audit: max |I3|/P = {max(v for _, v in born_points):.2e}")
        print()

        family_summaries[family] = {
            "mi_points": mi_points,
            "pur_points": pur_points,
            "grav_points": grav_points,
            "last_good_graph": last_good_graph,
        }

    # Narrow gravity-side follow-up on mirror only, if available
    mirror_graph = family_summaries.get("mirror", {}).get("last_good_graph")
    if mirror_graph:
        print("=" * 100)
        print("MIRROR GRAVITY FOLLOW-UP: fixed-anchor mass window + distance sweep")
        print("=" * 100)
        print()

        m_rows = gravity_mass_window(mirror_graph, args.k_band, args.m_values)
        pos_m = [(m, d) for m, d in m_rows if not math.isnan(d) and d > 0]
        print("  Fixed-anchor mass window:")
        print(f"  {'M':>4s}  {'delta':>10s}")
        print(f"  {'-' * 18}")
        for m, d in m_rows:
            if math.isnan(d):
                print(f"  {m:4d}  {'FAIL':>10s}")
            else:
                print(f"  {m:4d}  {d:+10.4f}")
        if len(pos_m) >= 3:
            fit = fit_power_law(pos_m)
            if fit:
                coeff, alpha, r2 = fit
                print(f"  Fit: delta ~= {coeff:.4f} * M^{alpha:.3f}  R^2={r2:.3f}")
        else:
            print("  Not enough positive points for a clean mass fit.")

        d_rows = distance_sweep(mirror_graph, args.k_band, args.distance_thresholds)
        pos_d = [(b, d) for b, d in d_rows if not math.isnan(d) and d > 0]
        print()
        print("  Distance sweep:")
        print(f"  {'y_min':>6s}  {'delta':>10s}")
        print(f"  {'-' * 20}")
        for b, d in d_rows:
            if math.isnan(d):
                print(f"  {b:6.1f}  {'FAIL':>10s}")
            else:
                print(f"  {b:6.1f}  {d:+10.4f}")
        if len(pos_d) >= 3:
            fit = fit_power_law(pos_d)
            if fit:
                coeff, alpha, r2 = fit
                print(f"  Tail fit: delta ~= {coeff:.4f} * b^{alpha:.3f}  R^2={r2:.3f}")
        else:
            print("  Not enough positive tail points for a clean distance fit.")

    print()
    print("Interpretation:")
    print("  - exact 2D mirror uses the linear propagator only")
    print("  - Born safety is judged by the corrected three-slit Sorkin audit")
    print("  - MI / d_TV / purity / gravity are reported on the same family")
    print("  - mass or distance fits are retained only if the window is clean")


if __name__ == "__main__":
    main()
