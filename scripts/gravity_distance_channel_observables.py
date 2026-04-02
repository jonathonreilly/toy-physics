#!/usr/bin/env python3
"""Channel-observable readout for the fixed-geometry gravity distance sweep.

Uses the same fixed-geometry setup as `gravity_distance_fixed_geometry.py`,
but asks whether detector-channel observables show a cleaner trend with
impact parameter than centroid shift does.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.gravity_distance_fixed_geometry import K_BAND, compute_field, propagate


def _mean(vals):
    return statistics.fmean(vals) if vals else math.nan


def _mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = statistics.fmean(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def _pearson(xs, ys):
    if len(xs) < 2 or len(ys) < 2:
        return math.nan
    xm = statistics.fmean(xs)
    ym = statistics.fmean(ys)
    num = sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - xm) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - ym) ** 2 for y in ys))
    if den_x <= 1e-30 or den_y <= 1e-30:
        return math.nan
    return num / (den_x * den_y)


def detector_metrics(positions, det_list, amps_with, amps_without):
    center_y = statistics.fmean(positions[d][1] for d in det_list)
    pm = [abs(amps_with[d]) ** 2 for d in det_list]
    pf = [abs(amps_without[d]) ** 2 for d in det_list]
    total_m = sum(pm)
    total_f = sum(pf)
    if total_m <= 1e-30 or total_f <= 1e-30:
        return math.nan, math.nan, math.nan, math.nan

    centroid_with = sum(p * positions[d][1] for p, d in zip(pm, det_list)) / total_m
    centroid_without = sum(p * positions[d][1] for p, d in zip(pf, det_list)) / total_f
    centroid = centroid_with - centroid_without

    signed = []
    for d, p_m, p_f in zip(det_list, pm, pf):
        dy = positions[d][1] - center_y
        signed.append((p_m - p_f) * dy)

    net = sum(signed)
    abs_net = sum(abs(v) for v in signed)
    if abs_net <= 1e-30:
        return centroid, 0.0, 0.0, 0.0

    bias = net / abs_net
    cancellation = 1.0 - min(1.0, abs(net) / abs_net)
    probs = [abs(v) / abs_net for v in signed if abs(v) > 1e-30]
    entropy = -sum(p * math.log(p) for p in probs)
    eff_ch = math.exp(entropy)
    return centroid, bias, cancellation, eff_ch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", type=int, default=30)
    parser.add_argument("--npl", type=int, default=90)
    parser.add_argument("--y-range", type=float, default=28.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--n-seeds", type=int, default=24)
    parser.add_argument("--mass-count", type=int, default=4)
    parser.add_argument("--b-values", nargs="+", type=float, default=[6.0, 10.0, 14.0, 18.0, 22.0, 26.0])
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 108)
    print("FIXED-GEOMETRY GRAVITY CHANNEL OBSERVABLES")
    print("  Same graph per seed; compare centroid to bundle/channel observables across b.")
    print(
        f"  N={args.n_layers}, npl={args.npl}, y_range={args.y_range}, "
        f"r={args.connect_radius}, mass_count={args.mass_count}, seeds={args.n_seeds}"
    )
    print("=" * 108)
    print()
    print(
        f"  {'b':>5s}  {'centroid':>12s}  {'bundle_bias':>12s}  "
        f"{'cancel':>10s}  {'eff_ch':>10s}  {'ok':>3s}"
    )
    print(f"  {'-' * 68}")

    xs = []
    centroids = []
    biases = []
    cancels = []
    effs = []

    for b in args.b_values:
        rows = []
        for seed in seeds:
            positions, adj, _ = generate_causal_dag(
                n_layers=args.n_layers,
                nodes_per_layer=args.npl,
                y_range=args.y_range,
                connect_radius=args.connect_radius,
                rng_seed=seed,
            )
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 7:
                continue

            src = by_layer[layers[0]]
            det_list = list(by_layer[layers[-1]])
            if not det_list:
                continue

            cy = statistics.fmean(y for _, y in positions)
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]
            if not sa or not sb:
                continue
            blocked = set(bi) - set(sa + sb)

            grav_layer = layers[2 * len(layers) // 3]
            candidates = sorted(
                by_layer[grav_layer],
                key=lambda i: abs(positions[i][1] - (cy + b)),
            )
            mass_nodes = candidates[:args.mass_count]
            if len(mass_nodes) < args.mass_count:
                continue

            field_m = compute_field(positions, mass_nodes)
            field_f = [0.0] * len(positions)

            centroid_vals = []
            bias_vals = []
            cancel_vals = []
            eff_vals = []
            for k in K_BAND:
                amps_with = propagate(positions, adj, field_m, src, k, blocked)
                amps_without = propagate(positions, adj, field_f, src, k, blocked)
                centroid, bias, cancellation, eff_ch = detector_metrics(
                    positions, det_list, amps_with, amps_without
                )
                if math.isnan(centroid):
                    continue
                centroid_vals.append(centroid)
                bias_vals.append(bias)
                cancel_vals.append(cancellation)
                eff_vals.append(eff_ch)

            if centroid_vals:
                rows.append((
                    _mean(centroid_vals),
                    _mean(bias_vals),
                    _mean(cancel_vals),
                    _mean(eff_vals),
                ))

        if not rows:
            print(f"  {b:5.1f}  FAIL")
            continue

        centroid_mean, centroid_se = _mean_se([r[0] for r in rows])
        bias_mean, _ = _mean_se([r[1] for r in rows])
        cancel_mean, _ = _mean_se([r[2] for r in rows])
        eff_mean, _ = _mean_se([r[3] for r in rows])

        print(
            f"  {b:5.1f}  {centroid_mean:+8.4f}±{centroid_se:.3f}  {bias_mean:+12.4f}  "
            f"{cancel_mean:10.4f}  {eff_mean:10.3f}  {len(rows):3d}"
        )

        xs.append(float(b))
        centroids.append(centroid_mean)
        biases.append(bias_mean)
        cancels.append(cancel_mean)
        effs.append(eff_mean)
        sys.stdout.flush()

    print()
    if len(xs) >= 3:
        print(
            "  corr(metric, b): "
            f"centroid={_pearson(xs, centroids):+.3f}, "
            f"bundle_bias={_pearson(xs, biases):+.3f}, "
            f"cancel={_pearson(xs, cancels):+.3f}, "
            f"eff_ch={_pearson(xs, effs):+.3f}"
        )


if __name__ == "__main__":
    main()
