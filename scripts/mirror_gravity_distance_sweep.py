#!/usr/bin/env python3
"""Fixed-geometry gravity distance sweep on the retained mirror pocket.

This is the mirror-only counterpart to the review-safe fixed-geometry distance
sweep used on the other hard-geometry lanes.

The experiment is intentionally narrow:

- strict mirror chokepoint graphs only
- one fixed graph per seed
- fixed mass count
- only the mass-anchor position moves with `b`
- fit only the falling tail beyond the observed peak

The goal is to see whether the retained mirror pocket has a cleaner
gravity-side law than the other hard-geometry lanes, without touching the core
mirror scripts.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.mirror_chokepoint_joint import generate_mirror_chokepoint_dag, compute_field_3d, propagate_3d

K_BAND = [3.0, 5.0, 7.0]


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--npl-half", type=int, default=50)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--layer2-prob", type=float, default=0.0)
    parser.add_argument("--mass-count", type=int, default=4)
    parser.add_argument("--b-values", nargs="+", type=float, default=[2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 96)
    print("MIRROR GRAVITY DISTANCE SWEEP")
    print("  Strict mirror chokepoint graphs, fixed mass count, only the anchor moves")
    print(
        f"  NPL_HALF={args.npl_half} (total {2 * args.npl_half}), "
        f"mass_count={args.mass_count}, layer2_prob={args.layer2_prob}, seeds={args.n_seeds}"
    )
    print("=" * 96)
    print()
    print(f"  {'b':>5s}  {'delta':>10s}  {'SE':>8s}  {'t':>7s}  {'ok':>3s}")
    print(f"  {'-' * 41}")

    for nl in args.n_layers:
        print(f"N = {nl}")
        rows = []
        for b in args.b_values:
            per_seed = []
            for seed in seeds:
                positions, adj, _, _ = generate_mirror_chokepoint_dag(
                    n_layers=nl,
                    npl_half=args.npl_half,
                    xyz_range=args.xyz_range,
                    connect_radius=args.connect_radius,
                    rng_seed=seed,
                    layer2_prob=args.layer2_prob,
                )

                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7:
                    continue

                src = by_layer[layers[0]]
                det_list = list(by_layer[layers[-1]])
                if not det_list:
                    continue

                cy = sum(y for _, y, _ in positions) / len(positions)
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

                field_m = compute_field_3d(positions, mass_nodes)
                field_f = [0.0] * len(positions)

                deltas = []
                for k in K_BAND:
                    am = propagate_3d(positions, adj, field_m, src, k, blocked)
                    af = propagate_3d(positions, adj, field_f, src, k, blocked)
                    pm = sum(abs(am[d]) ** 2 for d in det_list)
                    pf = sum(abs(af[d]) ** 2 for d in det_list)
                    if pm <= 1e-30 or pf <= 1e-30:
                        continue
                    ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
                    yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
                    deltas.append(ym - yf)
                if deltas:
                    per_seed.append(sum(deltas) / len(deltas))

            mean, se = mean_se(per_seed)
            t = mean / se if not math.isnan(mean) and se > 1e-12 else math.nan
            rows.append((b, mean))
            mean_s = "FAIL" if math.isnan(mean) else f"{mean:+.4f}"
            se_s = "FAIL" if math.isnan(se) else f"{se:.4f}"
            t_s = "FAIL" if math.isnan(t) else f"{t:+.2f}"
            print(f"  {b:5.1f}  {mean_s:>10s}  {se_s:>8s}  {t_s:>7s}  {len(per_seed):3d}")
            sys.stdout.flush()

        print()
        valid = [(b, d) for b, d in rows if not math.isnan(d) and d > 0]
        if len(valid) >= 3:
            peak_b, peak_d = max(valid, key=lambda row: row[1])
            print(f"  Peak mean deflection at b = {peak_b:.1f} (delta = {peak_d:.4f})")
            tail = [(b, d) for b, d in valid if b > peak_b]
            if len(tail) >= 3:
                xs = [math.log(b) for b, _ in tail]
                ys = [math.log(d) for _, d in tail]
                mx = sum(xs) / len(xs)
                my = sum(ys) / len(ys)
                sxx = sum((x - mx) ** 2 for x in xs)
                sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
                syy = sum((y - my) ** 2 for y in ys)
                if sxx > 1e-12:
                    alpha = sxy / sxx
                    r2 = (sxy * sxy) / (sxx * syy) if syy > 1e-12 else math.nan
                    if math.isnan(r2):
                        print(f"  Tail fit on strict mirror geometry: delta ~= C * b^{alpha:.3f}")
                    else:
                        print(f"  Tail fit on strict mirror geometry: delta ~= C * b^{alpha:.3f}  (R^2={r2:.3f})")
            else:
                print("  Not enough falling-tail points for a review-safe power-law fit.")
        else:
            print("  Not enough positive points for a review-safe tail fit.")
        print()


if __name__ == "__main__":
    main()
