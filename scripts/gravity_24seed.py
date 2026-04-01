#!/usr/bin/env python3
"""Gravity with 24 seeds on uniform DAGs: resolve the signal.

The 8-seed test showed FLAT on uniform DAGs. The corrected paired SE
was ~2x larger. With 24 seeds, SE shrinks by sqrt(3), which should
resolve whether gravity exists on uniform DAGs or requires channels.

Also tests 3D uniform with 24 seeds.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
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


def compute_field(positions, mass_nodes, dim=2):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mp = positions[m]
        for i in range(n):
            ip = positions[i]
            if dim == 2:
                r = math.sqrt((ip[0]-mp[0])**2 + (ip[1]-mp[1])**2) + 0.1
            else:
                r = math.sqrt((ip[0]-mp[0])**2 + (ip[1]-mp[1])**2 + (ip[2]-mp[2])**2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_2d(positions, adj, field, src, k, blocked=None):
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
            dx, dy = x2-x1, y2-y1
            L = math.sqrt(dx*dx + dy*dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def test_gravity_2d(n_layers_list, n_seeds=24):
    """Paired per-seed gravity test on 2D uniform DAGs."""
    k_band = [3.0, 5.0, 7.0]

    print("  2D UNIFORM DAG (24 seeds, paired per-seed SE)")
    print(f"  {'N':>4s}  {'delta':>8s}  {'SE':>7s}  {'d/SE':>6s}  "
          f"{'n_ok':>4s}  {'verdict'}")
    print(f"  {'-' * 48}")

    for nl in n_layers_list:
        per_seed_deltas = []

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
            grav_layer = layers[2 * len(layers) // 3]
            mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
            if not mass_nodes:
                continue

            field_m = compute_field(positions, mass_nodes, dim=2)
            field_f = [0.0] * len(positions)

            # Barrier for interference
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]
            if not sa or not sb:
                continue
            blocked = set(bi) - set(sa + sb)

            seed_deltas = []
            for k in k_band:
                am = propagate_2d(positions, adj, field_m, src, k, blocked)
                af = propagate_2d(positions, adj, field_f, src, k, blocked)
                pm = sum(abs(am[d])**2 for d in det_list)
                pf = sum(abs(af[d])**2 for d in det_list)
                if pm > 1e-30 and pf > 1e-30:
                    ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
                    yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
                    seed_deltas.append(ym - yf)

            if seed_deltas:
                per_seed_deltas.append(sum(seed_deltas) / len(seed_deltas))

        if per_seed_deltas:
            n_ok = len(per_seed_deltas)
            delta = sum(per_seed_deltas) / n_ok
            se = (sum((d - delta)**2 for d in per_seed_deltas) / n_ok)**0.5 / math.sqrt(n_ok)
            ratio = delta / se if se > 0 else 0
            verdict = "GRAVITY" if ratio > 2 else "MARGINAL" if ratio > 1 else "FLAT"
            print(f"  {nl:4d}  {delta:+8.4f}  {se:7.4f}  {ratio:6.2f}  {n_ok:4d}  {verdict}")
        else:
            print(f"  {nl:4d}  FAIL")

        sys.stdout.flush()


def main():
    print("=" * 78)
    print("GRAVITY: 24-SEED RESOLUTION TEST")
    print("  Does gravity exist on uniform DAGs, or does it require channels?")
    print("=" * 78)
    print()

    test_gravity_2d([12, 18, 25, 30, 40, 60, 80])

    print()
    print("d/SE > 2 = statistically significant gravitational deflection")
    print("If FLAT at all N: gravity requires channel separation")
    print("If GRAVITY at large N: gravity works on uniform DAGs (just noisy)")


if __name__ == "__main__":
    main()
