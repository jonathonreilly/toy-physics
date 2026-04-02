#!/usr/bin/env python3
"""Gravity distance scaling v2: extend to large b to find the falloff.

v1 showed delta INCREASING with b (0.22 at b=1 → 1.15 at b=8).
This is the rising part: at small b, mass is centered on beam
(symmetric field → no net deflection). At b ~ beam_width, the
gradient across the beam peaks.

Need b >> beam_width to see the 1/b falloff.
Beam width ≈ y_range / directional_measure ≈ 12 / (1/BETA) ≈ 10.

So extend to b = 10, 12, 15, 20 to find the turnover.

Alternative approach: use a NARROW beam (large BETA or small slit
width) so the beam is thin enough that even b=3 is in the far field.
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


def compute_field_at_y(positions, grav_nodes, y_mass, strength=0.1):
    n = len(positions)
    field = [0.0] * n
    for m in grav_nodes:
        mx = positions[m][0]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - y_mass) ** 2) + 0.1
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
    print("GRAVITY DISTANCE SCALING v2: Extended to large b")
    print("  N=30, 24 seeds, k-band [3,5,7]")
    print("  y_range=12, so beam extends to ~±10")
    print("=" * 70)
    print()

    nl = 30
    n_seeds = 24
    k_band = [3.0, 5.0, 7.0]

    # Extend to very large b to see falloff
    # Also test NEGATIVE b to check symmetry
    b_values = [2.0, 4.0, 6.0, 8.0, 10.0, 15.0, 20.0, 30.0]

    print(f"  {'b':>5s}  {'delta':>8s}  {'SE':>7s}  {'d/SE':>6s}")
    print(f"  {'-' * 30}")

    results = []

    for b in b_values:
        per_seed = []

        for seed_i in range(n_seeds):
            seed = seed_i * 7 + 3
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=max(12.0, b + 5),
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

            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            cy = sum(y for _, y in positions) / len(positions)
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]
            if not sa or not sb:
                continue
            blocked = set(bi) - set(sa + sb)

            grav_layer = layers[2 * len(layers) // 3]
            grav_nodes = by_layer[grav_layer][:5]
            if not grav_nodes:
                continue

            field_m = compute_field_at_y(positions, grav_nodes, b)
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
            print(f"  {b:5.1f}  {avg:+8.4f}  {se:7.4f}  {ratio:6.2f}")
        sys.stdout.flush()

    # Fit power law to the FALLOFF region (b >= 8 where delta decreases)
    print()
    if len(results) >= 4:
        # Find peak
        peak_b = max(results, key=lambda x: x[1])[0]
        print(f"  Peak deflection at b ≈ {peak_b}")

        # Fit falloff (b > peak)
        falloff = [(b, d, s) for b, d, s in results if b > peak_b and d > 0]
        if len(falloff) >= 2:
            xs = [math.log(b) for b, d, _ in falloff]
            ys = [math.log(d) for _, d, _ in falloff]
            n = len(xs)
            mx = sum(xs) / n
            my = sum(ys) / n
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            if sxx > 1e-10:
                slope = sxy / sxx
                print(f"  Falloff exponent: delta ~ b^{slope:.2f} for b > {peak_b}")
                if -1.3 < slope < -0.7:
                    print(f"  → 1/b CONFIRMED in far field")
                elif -2.3 < slope < -1.7:
                    print(f"  → 1/b² (too steep — 3D-like)")
                elif slope > -0.3:
                    print(f"  → flat or rising (not yet in far field)")
                else:
                    print(f"  → exponent {slope:.2f}")
        else:
            print(f"  Not enough falloff points (need b > {peak_b})")

    print()
    print("Physics: beam has finite width (~10 in y_range=12)")
    print("  b < beam_width: near field, delta rises")
    print("  b ~ beam_width: peak deflection")
    print("  b >> beam_width: far field, delta ~ 1/b (expect)")


if __name__ == "__main__":
    main()
