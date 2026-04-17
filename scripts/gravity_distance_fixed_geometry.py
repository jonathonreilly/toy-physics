#!/usr/bin/env python3
"""Fixed-geometry gravity distance sweep on generated DAGs.

This is the review-safe replacement for earlier `b` sweeps that changed the
graph geometry with the impact parameter. Here each seed uses one fixed graph;
only the mass-anchor position moves.

For each seed:
  - generate one graph at fixed `(N, nodes_per_layer, y_range, connect_radius)`
  - define a fixed barrier/slit geometry
  - for each impact parameter `b`, choose a fixed-count mass set on the same
    gravity layer nearest to `y = center + b`
  - measure centroid shift with and without the field on the same graph

We report the raw `delta(b)` curve and fit a power law only on the falling
tail beyond the observed peak.
"""

from __future__ import annotations

import argparse
import cmath
from collections import defaultdict, deque
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag

BETA = 0.8
K_BAND = [3.0, 5.0, 7.0]


def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def propagate(positions, adj, field, src, k, blocked):
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def compute_field(positions, mass_nodes, strength=0.1):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += strength / r
    return field


def _mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", type=int, default=30)
    parser.add_argument("--npl", type=int, default=60)
    parser.add_argument("--y-range", type=float, default=18.0)
    parser.add_argument("--connect-radius", type=float, default=3.5)
    parser.add_argument("--n-seeds", type=int, default=24)
    parser.add_argument("--mass-count", type=int, default=4)
    parser.add_argument("--b-values", nargs="+", type=float, default=[2.0, 4.0, 6.0, 8.0, 10.0, 12.0])
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 92)
    print("FIXED-GEOMETRY GRAVITY DISTANCE SWEEP")
    print("  One fixed graph per seed; only the mass-anchor position moves.")
    print(
        f"  N={args.n_layers}, npl={args.npl}, y_range={args.y_range}, "
        f"r={args.connect_radius}, mass_count={args.mass_count}, seeds={args.n_seeds}"
    )
    print("=" * 92)
    print()
    print(f"  {'b':>5s}  {'delta':>10s}  {'SE':>8s}  {'t':>7s}  {'ok':>3s}")
    print(f"  {'-' * 41}")

    rows = []

    for b in args.b_values:
        per_seed = []
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

            cy = sum(y for _, y in positions) / len(positions)
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

            deltas = []
            for k in K_BAND:
                am = propagate(positions, adj, field_m, src, k, blocked)
                af = propagate(positions, adj, field_f, src, k, blocked)
                pm = sum(abs(am[d]) ** 2 for d in det_list)
                pf = sum(abs(af[d]) ** 2 for d in det_list)
                if pm <= 1e-30 or pf <= 1e-30:
                    continue
                ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
                yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
                deltas.append(ym - yf)
            if deltas:
                per_seed.append(sum(deltas) / len(deltas))

        mean, se = _mean_se(per_seed)
        t = mean / se if not math.isnan(mean) and se > 1e-12 else math.nan
        rows.append((b, mean, se, len(per_seed)))
        mean_s = "FAIL" if math.isnan(mean) else f"{mean:+.4f}"
        se_s = "FAIL" if math.isnan(se) else f"{se:.4f}"
        t_s = "FAIL" if math.isnan(t) else f"{t:+.2f}"
        print(f"  {b:5.1f}  {mean_s:>10s}  {se_s:>8s}  {t_s:>7s}  {len(per_seed):3d}")
        sys.stdout.flush()

    print()
    valid = [(b, d) for b, d, _, _ in rows if not math.isnan(d) and d > 0]
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
                    print(f"  Tail fit on fixed geometry: delta ~= C * b^{alpha:.3f}")
                else:
                    print(f"  Tail fit on fixed geometry: delta ~= C * b^{alpha:.3f}  (R^2={r2:.3f})")
        else:
            print("  Not enough falling-tail points for a review-safe power-law fit.")
    else:
        print("  Not enough positive points for a review-safe tail fit.")


if __name__ == "__main__":
    main()
