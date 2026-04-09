#!/usr/bin/env python3
"""Collapse at large N: confirm positive exponent holds to N=200.

Also tests the triple combination: LN + gap + collapse.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
import random as rng_mod
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.topology_families import generate_modular_dag

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


def compute_field(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_collapse_ln(positions, adj, field, src, k, blocked,
                           mass_set, p_collapse, rng, use_ln=False):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if abs(amps[i]) < 1e-30 or i in blocked:
                continue
            if i in mass_set and p_collapse > 0 and rng.random() < p_collapse:
                amps[i] *= cmath.exp(1j * rng.uniform(0, 2 * math.pi))
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
        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm
    return amps


def mc_purity(positions, adj, field, src, det_list, k_band,
              blocked_a, blocked_b, mass_set, p_collapse,
              n_real=30, use_ln=False):
    rho = {(d1, d2): 0j for d1 in det_list for d2 in det_list}
    n_total = 0
    for k in k_band:
        for r in range(n_real):
            rng = rng_mod.Random(r * 1000 + int(k * 100))
            aa = propagate_collapse_ln(positions, adj, field, src, k,
                                        blocked_a, mass_set, p_collapse, rng, use_ln)
            rng2 = rng_mod.Random(r * 1000 + int(k * 100) + 500000)
            ab = propagate_collapse_ln(positions, adj, field, src, k,
                                        blocked_b, mass_set, p_collapse, rng2, use_ln)
            psi = [aa[d] + ab[d] for d in det_list]
            nsq = sum(abs(p) ** 2 for p in psi)
            if nsq < 1e-30:
                continue
            for i, d1 in enumerate(det_list):
                for j, d2 in enumerate(det_list):
                    rho[(d1, d2)] += psi[i].conjugate() * psi[j] / nsq
            n_total += 1
    if n_total == 0:
        return math.nan
    for key in rho:
        rho[key] /= n_total
    return sum(abs(v) ** 2 for v in rho.values()).real


def run_one(nl, seed, p_collapse, use_ln=False, gap=0.0, n_real=30):
    if gap > 0:
        positions, adj, _ = generate_modular_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=seed, gap=gap)
    else:
        positions, adj, _ = generate_causal_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=seed)

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
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    env_depth = max(1, round(nl / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mass_env = set()
    for layer in layers[start:stop]:
        mass_env.update(by_layer[layer])

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    field = compute_field(positions, list(mass_env | set(mass_nodes)))

    pur = mc_purity(positions, adj, field, src, det_list, [3.0, 5.0, 7.0],
                     blocked | set(sb), blocked | set(sa),
                     mass_env, p_collapse, n_real, use_ln)
    return pur


def main():
    print("=" * 70)
    print("COLLAPSE LARGE-N CONFIRMATION + TRIPLE STACK")
    print("  p_collapse=0.2, 30 MC realizations, 10 seeds")
    print("=" * 70)
    print()

    n_seeds = 10
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    configs = [
        ("Collapse only (uniform)", 0.2, False, 0.0),
        ("Collapse + LN (uniform)", 0.2, True, 0.0),
        ("Collapse + LN + gap=2", 0.2, True, 2.0),
        ("CL bath baseline (no collapse)", 0.0, False, 0.0),
    ]

    for name, pc, ln, gap in configs:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'purity':>8s}  {'1-pur':>7s}  {'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 36}")

        for nl in [25, 40, 60, 80, 100, 150, 200]:
            t0 = time.time()
            pur_all = []
            for seed in seeds:
                r = run_one(nl, seed, pc, ln, gap, n_real=30)
                if r is not None and not math.isnan(r):
                    pur_all.append(r)
            dt = time.time() - t0
            if pur_all:
                avg = sum(pur_all) / len(pur_all)
                print(f"  {nl:4d}  {avg:8.4f}  {1-avg:7.4f}  {len(pur_all):4d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  FAIL")
            sys.stdout.flush()
        print()

    print("KEY: Does collapse maintain positive exponent to N=200?")


if __name__ == "__main__":
    main()
