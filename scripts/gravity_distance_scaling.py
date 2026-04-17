#!/usr/bin/env python3
"""Gravity distance scaling: does deflection follow 1/b?

In 2D continuum gravity:
  field ~ log(r), force ~ 1/r, deflection ~ constant (b-independent)

In 3D continuum gravity:
  field ~ 1/r, force ~ 1/r^2, deflection ~ 1/b

On our 2D DAGs with field ~ 1/r (Newtonian, not log):
  Expected: force ~ 1/r^2, deflection ~ 1/b (since field is 1/r)

Test: vary the impact parameter b (y-offset of mass from beam center)
and measure deflection. Fit to delta ~ A * b^(-alpha).
alpha=1 would confirm 1/b scaling.

Uses N=30 (peak gravity signal from 24-seed test) with 24 seeds per b.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag

BETA = 0.8


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


def compute_field_at_offset(positions, adj, grav_layer_nodes, y_offset, strength=0.1):
    """Compute field from mass at y_offset (shift mass to specific y)."""
    n = len(positions)
    field = [0.0] * n
    for m in grav_layer_nodes:
        mx, my = positions[m]
        # Shift mass y to y_offset
        my_shifted = y_offset
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my_shifted) ** 2) + 0.1
            field[i] += strength / r
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def main():
    print("=" * 70)
    print("GRAVITY DISTANCE SCALING: delta vs impact parameter b")
    print("  N=30 (peak signal), 24 seeds, k-band [3,5,7]")
    print("  Mass placed at varying y-offsets from beam center")
    print("=" * 70)
    print()

    nl = 30
    n_seeds = 24
    k_band = [3.0, 5.0, 7.0]
    # Impact parameters: y-offset of mass from beam center (y=0)
    b_values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]

    print(f"  {'b':>5s}  {'delta':>8s}  {'SE':>7s}  {'d/SE':>6s}  "
          f"{'delta*b':>8s}  {'delta*b^2':>10s}")
    print(f"  {'-' * 52}")

    results = []

    for b in b_values:
        per_seed = []

        for seed_i in range(n_seeds):
            seed = seed_i * 7 + 3
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed,
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

            # Barrier
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            cy = sum(y for _, y in positions) / len(positions)
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]
            if not sa or not sb:
                continue
            blocked = set(bi) - set(sa + sb)

            # Mass at y=b, placed at layer 2/3
            grav_layer = layers[2 * len(layers) // 3]
            grav_nodes = by_layer[grav_layer][:5]  # use first 5 nodes as mass anchors
            if not grav_nodes:
                continue

            field_m = compute_field_at_offset(positions, adj, grav_nodes, b)
            field_f = [0.0] * len(positions)

            seed_deltas = []
            for k in k_band:
                am = propagate(positions, adj, field_m, src, k, blocked)
                af = propagate(positions, adj, field_f, src, k, blocked)
                pm = sum(abs(am[d]) ** 2 for d in det_list)
                pf = sum(abs(af[d]) ** 2 for d in det_list)
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
                    yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
                    seed_deltas.append(ym - yf)

            if seed_deltas:
                per_seed.append(sum(seed_deltas) / len(seed_deltas))

        if per_seed:
            n_ok = len(per_seed)
            avg = sum(per_seed) / n_ok
            se = (sum((d - avg) ** 2 for d in per_seed) / n_ok) ** 0.5 / math.sqrt(n_ok)
            ratio = avg / se if se > 0 else 0
            results.append((b, avg, se))
            print(f"  {b:5.1f}  {avg:+8.4f}  {se:7.4f}  {ratio:6.2f}  "
                  f"{avg*b:+8.4f}  {avg*b**2:+10.4f}")
        sys.stdout.flush()

    # Fit power law: delta = A * b^(-alpha)
    print()
    if len(results) >= 3:
        # Use only points with positive delta
        pos_results = [(b, d, s) for b, d, s in results if d > 0]
        if len(pos_results) >= 3:
            xs = [math.log(b) for b, d, _ in pos_results]
            ys = [math.log(d) for _, d, _ in pos_results]
            n = len(xs)
            mx = sum(xs) / n
            my = sum(ys) / n
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            syy = sum((y - my) ** 2 for y in ys)

            if sxx > 1e-10:
                alpha = -sxy / sxx  # negative because delta decreases with b
                A = math.exp(my + alpha * mx)  # note sign
                r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0

                print(f"  Power law fit: delta = {A:.4f} * b^(-{alpha:.3f})")
                print(f"  R² = {r2:.3f}")
                print()
                if 0.8 < alpha < 1.2:
                    print(f"  alpha ≈ 1.0 → 1/b scaling CONFIRMED")
                    print(f"  Consistent with 1/r field → 1/r² force → 1/b deflection")
                elif 0.0 < alpha < 0.3:
                    print(f"  alpha ≈ 0 → constant deflection (2D log-field behavior)")
                elif 1.8 < alpha < 2.2:
                    print(f"  alpha ≈ 2 → 1/b² scaling (steeper than expected)")
                else:
                    print(f"  alpha = {alpha:.2f} — non-standard scaling")
        else:
            print("  Not enough positive-delta points for power law fit")

    print()
    print("Expected: alpha ≈ 1 (1/b) for our 1/r field on 2D DAGs")
    print("  (field is 1/r, not log(r), so gradient is 1/r², deflection is 1/b)")


if __name__ == "__main__":
    main()
