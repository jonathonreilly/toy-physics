#!/usr/bin/env python3
"""Fixed-anchor gravity mass scaling on generated DAGs.

This is the review-safe replacement for earlier mass sweeps that let the
effective mass position drift with `M`. Here each seed uses one fixed graph and
one fixed anchor `y = center + b_anchor`; the mass set is a frozen ordering of
nodes on the gravity layer ranked by distance to that anchor. Varying `M` takes
prefixes of that same ordered set.

The main fit is reported on a declared non-saturating window. Higher `M`
values are still printed so saturation can be seen explicitly.
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
    parser.add_argument("--npl", type=int, default=30)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--n-seeds", type=int, default=24)
    parser.add_argument("--anchor-b", type=float, default=5.0)
    parser.add_argument("--m-values", nargs="+", type=int, default=[1, 2, 3, 5, 8, 12])
    parser.add_argument("--fit-window", nargs="+", type=int, default=[2, 3, 5, 8, 12])
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 96)
    print("FIXED-ANCHOR GRAVITY MASS SCALING")
    print("  One fixed graph per seed; one fixed mass anchor; M varies by prefix of the same ordered set.")
    print(
        f"  N={args.n_layers}, npl={args.npl}, y_range={args.y_range}, "
        f"r={args.connect_radius}, anchor_b={args.anchor_b}, seeds={args.n_seeds}"
    )
    print("=" * 96)
    print()
    print(f"  {'M':>4s}  {'delta':>10s}  {'SE':>8s}  {'t':>7s}  {'delta/M':>10s}  {'ok':>3s}")
    print(f"  {'-' * 52}")

    rows = []

    for m_target in args.m_values:
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
            anchor_y = cy + args.anchor_b
            ordered = sorted(
                by_layer[grav_layer],
                key=lambda i: (abs(positions[i][1] - anchor_y), abs(positions[i][1] - cy)),
            )
            if len(ordered) < m_target:
                continue
            mass_nodes = ordered[:m_target]

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
        rows.append((m_target, mean, se, len(per_seed)))
        dm = mean / m_target if not math.isnan(mean) and m_target > 0 else math.nan
        mean_s = "FAIL" if math.isnan(mean) else f"{mean:+.4f}"
        se_s = "FAIL" if math.isnan(se) else f"{se:.4f}"
        t_s = "FAIL" if math.isnan(t) else f"{t:+.2f}"
        dm_s = "FAIL" if math.isnan(dm) else f"{dm:+.4f}"
        print(f"  {m_target:4d}  {mean_s:>10s}  {se_s:>8s}  {t_s:>7s}  {dm_s:>10s}  {len(per_seed):3d}")
        sys.stdout.flush()

    print()
    fit_rows = [(m, d) for m, d, _, _ in rows if m in set(args.fit_window) and not math.isnan(d) and d > 0]
    if len(fit_rows) >= 3:
        xs = [math.log(m) for m, _ in fit_rows]
        ys = [math.log(d) for _, d in fit_rows]
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        syy = sum((y - my) ** 2 for y in ys)
        if sxx > 1e-12:
            alpha = sxy / sxx
            coeff = math.exp(my - alpha * mx)
            r2 = (sxy * sxy) / (sxx * syy) if syy > 1e-12 else math.nan
            window_s = ",".join(str(v) for v in args.fit_window)
            print(f"  Fixed-anchor window fit on M in {{{window_s}}}: delta ~= {coeff:.4f} * M^{alpha:.3f}")
            if not math.isnan(r2):
                print(f"  R^2 = {r2:.3f}")
    else:
        print("  Not enough positive points in the declared fit window.")


if __name__ == "__main__":
    main()
