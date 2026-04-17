#!/usr/bin/env python3
"""Mirror-specific mutual information on the retained exact chokepoint family.

This is the canonical mirror MI harness for the review-safe exact mirror
family. It measures I(slit_label; detector_y_bin) and CL-bath purity on the
same linear propagator / same slit-detector geometry as the retained mirror
chokepoint pocket, and compares it against the matched random chokepoint
baseline.

The goal is not to force an asymptotic law. The goal is to freeze the exact
mirror-vs-random MI chain on the retained family and report honestly whether
mirror preserves which-slit information more slowly than random in this
harness.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.mirror_chokepoint_joint import (
    K,
    LAM,
    N_SEEDS,
    XYZ_RANGE,
    compute_field_3d,
    generate_mirror_chokepoint_dag,
    generate_random_chokepoint_dag,
    propagate_3d,
)

N_YBINS = 8


def _mean_se(vals: list[float]) -> tuple[float, float]:
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def _fit_power_law(ns: list[int], ys: list[float]) -> tuple[float, float, float]:
    pairs = [(n, y) for n, y in zip(ns, ys) if n > 0 and y > 0 and not math.isnan(y)]
    if len(pairs) < 2:
        return math.nan, math.nan, math.nan
    xs = [math.log(n) for n, _ in pairs]
    ls = [math.log(y) for _, y in pairs]
    mx = sum(xs) / len(xs)
    my = sum(ls) / len(ls)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx <= 1e-30:
        return math.nan, math.nan, math.nan
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ls))
    alpha = sxy / sxx
    intercept = my - alpha * mx
    pred = [intercept + alpha * x for x in xs]
    ss_res = sum((y - p) ** 2 for y, p in zip(ls, pred))
    ss_tot = sum((y - my) ** 2 for y in ls)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-30 else math.nan
    return math.exp(intercept), alpha, r2


def _by_layer(positions):
    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    layers = sorted(by_layer.keys())
    return by_layer, layers


def _select_slits(positions, barrier_nodes, center_y):
    slit_a = [i for i in barrier_nodes if positions[i][1] > center_y + 3][:3]
    slit_b = [i for i in barrier_nodes if positions[i][1] < center_y - 3][:3]
    return slit_a, slit_b


def _detector_bin_probs(positions, det_list, amps, y_extent):
    probs = [0.0] * N_YBINS
    bin_width = (2.0 * y_extent) / N_YBINS
    for d in det_list:
        bin_idx = int((positions[d][1] + y_extent) / bin_width)
        bin_idx = max(0, min(N_YBINS - 1, bin_idx))
        probs[bin_idx] += abs(amps[d]) ** 2
    norm = sum(probs)
    if norm <= 1e-30:
        return None
    return [p / norm for p in probs]


def _bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 2.0 * XYZ_RANGE / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + XYZ_RANGE) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def measure_record(positions, adj, barrier_layer: int, k: float):
    by_layer, layers = _by_layer(positions)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    barrier_nodes = by_layer[layers[barrier_layer]]
    if len(barrier_nodes) < 6:
        return None

    center_y = sum(pos[1] for pos in positions) / len(positions)
    slit_a, slit_b = _select_slits(positions, barrier_nodes, center_y)
    if not slit_a or not slit_b:
        return None
    blocked = set(barrier_nodes) - set(slit_a + slit_b)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > center_y + 1]
    if not mass_nodes:
        return None

    field = compute_field_3d(positions, mass_nodes)
    psi_a = propagate_3d(positions, adj, field, src, k, blocked | set(slit_b))
    psi_b = propagate_3d(positions, adj, field, src, k, blocked | set(slit_a))

    prob_a = _detector_bin_probs(positions, det_list, psi_a, XYZ_RANGE)
    prob_b = _detector_bin_probs(positions, det_list, psi_b, XYZ_RANGE)
    if prob_a is None or prob_b is None:
        return None

    h_det = 0.0
    h_cond = 0.0
    d_tv = 0.0
    for bin_idx in range(N_YBINS):
        p_mix = 0.5 * prob_a[bin_idx] + 0.5 * prob_b[bin_idx]
        if p_mix > 1e-30:
            h_det -= p_mix * math.log2(p_mix)
        if prob_a[bin_idx] > 1e-30:
            h_cond -= 0.5 * prob_a[bin_idx] * math.log2(prob_a[bin_idx])
        if prob_b[bin_idx] > 1e-30:
            h_cond -= 0.5 * prob_b[bin_idx] * math.log2(prob_b[bin_idx])
        d_tv += abs(prob_a[bin_idx] - prob_b[bin_idx])
    d_tv *= 0.5

    env_depth = max(1, round(len(layers) / 6))
    start = barrier_layer + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid_nodes = []
    for layer in layers[start:stop]:
        mid_nodes.extend(by_layer[layer])

    bins_a = _bin_amplitudes(psi_a, positions, mid_nodes)
    bins_b = _bin_amplitudes(psi_b, positions, mid_nodes)
    sn_num = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
    na = sum(abs(a) ** 2 for a in bins_a)
    nb = sum(abs(b) ** 2 for b in bins_b)
    sn = sn_num / (na + nb) if (na + nb) > 0 else 0.0
    d_cl = math.exp(-LAM * LAM * sn)

    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                psi_a[d1].conjugate() * psi_a[d2]
                + psi_b[d1].conjugate() * psi_b[d2]
                + d_cl * psi_a[d1].conjugate() * psi_b[d2]
                + d_cl * psi_b[d1].conjugate() * psi_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr < 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_cl = sum(abs(v) ** 2 for v in rho.values()).real

    return {
        "MI": h_det - h_cond,
        "H_det": h_det,
        "H_cond": h_cond,
        "d_TV": d_tv,
        "pur_cl": pur_cl,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60, 80, 100])
    parser.add_argument("--npl-half", type=int, default=60)
    parser.add_argument("--xyz-range", type=float, default=XYZ_RANGE)
    parser.add_argument("--connect-radius", type=float, default=5.0)
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--k", type=float, default=K)
    args = parser.parse_args()

    print("=" * 118)
    print("MIRROR MUTUAL INFORMATION: RETAINED EXACT CHOKEPOINT FAMILY")
    print("  exact mirror chokepoint + matched random chokepoint baseline")
    print(f"  npl_half={args.npl_half} (total {2 * args.npl_half}), connect_radius={args.connect_radius:g}")
    print(f"  k={args.k}, seeds={args.n_seeds}, y-bins={N_YBINS}, y-range=[-{XYZ_RANGE:g}, {XYZ_RANGE:g}]")
    print("=" * 118)
    print()
    print(f"  {'family':>12s}  {'N':>4s}  {'MI(bits)':>11s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'H(det)':>9s}  {'H(det|s)':>10s}  {'ok':>3s}  {'time':>5s}")
    print("  " + "-" * 94)

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    fit_ns = []
    fit_mirror_mi = []
    fit_random_mi = []
    fit_mirror_purity = []
    fit_random_purity = []

    for nl in args.n_layers:
        for label, kind in (("random", "random"), ("mirror", "mirror")):
            t0 = time.time()
            mi_vals = []
            dtv_vals = []
            pur_vals = []
            hd_vals = []
            hc_vals = []
            ok = 0
            for seed in seeds:
                if kind == "mirror":
                    positions, adj, barrier_layer, _ = generate_mirror_chokepoint_dag(
                        nl, args.npl_half, args.xyz_range, args.connect_radius, seed, 0.0
                    )
                else:
                    positions, adj, barrier_layer = generate_random_chokepoint_dag(
                        nl, 2 * args.npl_half, args.xyz_range, args.connect_radius, seed, 0.0
                    )
                result = measure_record(positions, adj, barrier_layer, args.k)
                if result is None:
                    continue
                ok += 1
                mi_vals.append(result["MI"])
                dtv_vals.append(result["d_TV"])
                pur_vals.append(result["pur_cl"])
                hd_vals.append(result["H_det"])
                hc_vals.append(result["H_cond"])

            elapsed = time.time() - t0
            if mi_vals:
                mi_mean, mi_se = _mean_se(mi_vals)
                dtv_mean, _ = _mean_se(dtv_vals)
                pur_mean, pur_se = _mean_se(pur_vals)
                hd_mean, _ = _mean_se(hd_vals)
                hc_mean, _ = _mean_se(hc_vals)
                print(
                    f"  {label:>12s}  {nl:4d}  {mi_mean:8.4f}±{mi_se:.3f}  {dtv_mean:8.4f}  {pur_mean:7.4f}±{pur_se:.02f}  "
                    f"{hd_mean:9.4f}  {hc_mean:10.4f}  {ok:3d}  {elapsed:4.0f}s"
                )
                if label == "mirror":
                    fit_ns.append(nl)
                    fit_mirror_mi.append(mi_mean)
                    fit_mirror_purity.append(1.0 - pur_mean)
                else:
                    fit_random_mi.append(mi_mean)
                    fit_random_purity.append(1.0 - pur_mean)
            else:
                print(f"  {label:>12s}  {nl:4d}  FAIL{'':>68s}  {elapsed:4.0f}s")
        print()

    print("MI = H(detector) - H(detector|slit) in bits (max = 1.0 for a binary slit label).")
    print("pur_cl is the CL-bath purity on the same retained linear chokepoint harness.")

    if len(fit_ns) >= 3:
        am, alpha_m, r2_m = _fit_power_law(fit_ns, fit_mirror_mi)
        ar, alpha_r, r2_r = _fit_power_law(fit_ns, fit_random_mi)
        apm, alphap_m, r2pm = _fit_power_law(fit_ns, fit_mirror_purity)
        apr, alphap_r, r2pr = _fit_power_law(fit_ns, fit_random_purity)
        print()
        print("POWER-LAW SUMMARIES (descriptive, not forced):")
        print(f"  mirror MI      ~= {am:.4f} × N^{alpha_m:.3f}   R²={r2_m:.3f}")
        print(f"  random MI      ~= {ar:.4f} × N^{alpha_r:.3f}   R²={r2_r:.3f}")
        print(f"  mirror 1-pur   ~= {apm:.4f} × N^{alphap_m:.3f}  R²={r2pm:.3f}")
        print(f"  random 1-pur   ~= {apr:.4f} × N^{alphap_r:.3f}  R²={r2pr:.3f}")
        print("  Note: if these exponents disagree across N windows, treat them as bounded summaries, not laws.")


if __name__ == "__main__":
    main()
