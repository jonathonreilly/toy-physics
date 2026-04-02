#!/usr/bin/env python3
"""Gravity mass scaling: does deflection scale linearly with mass?

We know: gravity exists (5.1 SE at N=30), distance scaling ~1/b².
Missing: does F∝M? This would complete the gravity story.

Test: vary the number of mass nodes (M) at fixed b and N,
measure deflection. Fit to delta ~ A × M^alpha.
alpha=1 would confirm linear mass scaling.
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


def compute_field_variable_mass(positions, mass_nodes, n_active, strength=0.1):
    """Field from first n_active mass nodes only."""
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes[:n_active]:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
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
    print("GRAVITY MASS SCALING: delta vs number of mass nodes M")
    print("  N=30, 24 seeds, k-band [3,5,7]")
    print("  Mass at y>3 (fixed b≈5), varying M from 1 to max available")
    print("=" * 70)
    print()

    nl = 30
    n_seeds = 24
    k_band = [3.0, 5.0, 7.0]
    m_values = [1, 2, 3, 5, 8, 12]

    print(f"  {'M':>4s}  {'delta':>8s}  {'SE':>7s}  {'d/SE':>6s}  "
          f"{'delta/M':>8s}")
    print(f"  {'-' * 38}")

    results = []

    for m_target in m_values:
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

            cy = sum(y for _, y in positions) / len(positions)
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]
            if not sa or not sb:
                continue
            blocked = set(bi) - set(sa + sb)

            # All available mass nodes at y > 3 in grav_layer
            grav_layer = layers[2 * len(layers) // 3]
            all_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 3]
            if len(all_mass) < m_target:
                continue

            field_m = compute_field_variable_mass(positions, all_mass, m_target)
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
            results.append((m_target, avg, se))
            dm = avg / m_target if m_target > 0 else 0
            print(f"  {m_target:4d}  {avg:+8.4f}  {se:7.4f}  {ratio:6.2f}  "
                  f"{dm:+8.4f}")
        sys.stdout.flush()

    # Fit: delta = A × M^alpha
    print()
    pos_results = [(m, d, s) for m, d, s in results if d > 0 and m > 0]
    if len(pos_results) >= 3:
        xs = [math.log(m) for m, d, _ in pos_results]
        ys = [math.log(d) for _, d, _ in pos_results]
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        syy = sum((y - my) ** 2 for y in ys)
        if sxx > 1e-10:
            alpha = sxy / sxx
            A = math.exp(my - alpha * mx)
            r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
            print(f"  Power law: delta = {A:.4f} × M^{alpha:.3f}")
            print(f"  R² = {r2:.3f}")
            print()
            if 0.7 < alpha < 1.3:
                print(f"  alpha ≈ 1 → F∝M CONFIRMED (linear mass scaling)")
            elif 0.3 < alpha < 0.7:
                print(f"  alpha ≈ 0.5 → sublinear (sqrt scaling)")
            elif alpha < 0.3:
                print(f"  alpha ≈ 0 → mass-independent (saturation)")
            else:
                print(f"  alpha = {alpha:.2f}")

    # Check linearity: is delta/M roughly constant?
    if len(pos_results) >= 2:
        dm_values = [d / m for m, d, _ in pos_results]
        mean_dm = sum(dm_values) / len(dm_values)
        std_dm = (sum((v - mean_dm) ** 2 for v in dm_values) / len(dm_values)) ** 0.5
        cv = std_dm / mean_dm if mean_dm > 0 else 999
        print(f"\n  delta/M consistency: mean={mean_dm:.4f}, CV={cv:.2f}")
        if cv < 0.3:
            print(f"  → delta/M is approximately constant (CV < 0.3)")
        else:
            print(f"  → delta/M varies significantly (CV > 0.3)")


if __name__ == "__main__":
    main()
