#!/usr/bin/env python3
"""5D decoherence exponent test.

Derivation predicts: alpha ~ -1.5/4 = -0.375 for d_spatial=4 (5D graphs).
This is between the 4D value (-0.22 to -0.53) and the 3D value (~-0.7).

Uses dense 5D modular DAGs (Codex infrastructure) with CL bath.
12 seeds per N point, gap=5.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.five_d_dense_pilot import generate_5d_modular_dag

BETA = 0.8
N_YBINS = 8
LAM = 10.0


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
        mp = positions[m]
        for i in range(n):
            ip = positions[i]
            r = math.sqrt(sum((a - b) ** 2 for a, b in zip(ip, mp))) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_5d(positions, adj, field, src, k, blocked=None):
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
            ip, jp = positions[i], positions[j]
            dsq = sum((a - b) ** 2 for a, b in zip(ip, jp))
            L = math.sqrt(dsq)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            dx = jp[0] - ip[0]
            trans = math.sqrt(dsq - dx * dx)
            theta = math.atan2(trans, max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def measure_pur_min(positions, adj, nl, seed_label=""):
    """Measure pur_min on one 5D graph."""
    k_band = [3.0, 5.0, 7.0]
    n = len(positions)

    by_layer = defaultdict(list)
    for idx in range(n):
        by_layer[round(positions[idx][0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    # y is positions[i][1]
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 2][:3]
    sb = [i for i in bi if positions[i][1] < cy - 2][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mn = []
    for layer in layers[start:stop]:
        mn.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 2.0)
    field = compute_field(positions, list(set(mn) | set(mass)))

    pm_vals = []
    for k in k_band:
        aa = propagate_5d(positions, adj, field, src, k, blocked | set(sb))
        ab = propagate_5d(positions, adj, field, src, k, blocked | set(sa))
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (aa[d1].conjugate() * aa[d2]
                                  + ab[d1].conjugate() * ab[d2])
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            continue
        for key in rho:
            rho[key] /= tr
        pm_vals.append(sum(abs(v) ** 2 for v in rho.values()).real)

    if not pm_vals:
        return None
    return sum(pm_vals) / len(pm_vals)


def main():
    import time

    print("=" * 70)
    print("5D DECOHERENCE EXPONENT TEST")
    print("  Prediction: alpha ≈ -0.375 (from alpha ~ 1.5/d_spatial)")
    print("  12 seeds, gap=5, dense 5D modular DAGs")
    print("=" * 70)
    print()

    n_seeds = 12
    n_list = [12, 18, 25, 30, 40]

    print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'SE':>6s}  "
          f"{'n_ok':>4s}  {'time':>5s}")
    print(f"  {'-' * 42}")

    data = {}
    for nl in n_list:
        t0 = time.time()
        pm_all = []
        for seed_i in range(n_seeds):
            seed = seed_i * 7 + 3
            positions, adj = generate_5d_modular_dag(
                n_layers=nl, nodes_per_layer=50, spatial_range=6.0,
                connect_radius=5.5, rng_seed=seed, gap=5.0)[:2]
            r = measure_pur_min(positions, adj, nl)
            if r is not None:
                pm_all.append(r)

        dt = time.time() - t0
        if pm_all:
            avg = sum(pm_all) / len(pm_all)
            se = (sum((p - avg) ** 2 for p in pm_all) / len(pm_all)) ** 0.5 / math.sqrt(len(pm_all))
            data[nl] = avg
            print(f"  {nl:4d}  {avg:8.4f}  {1-avg:7.4f}  {se:6.4f}  "
                  f"{len(pm_all):4d}  {dt:4.0f}s")
        else:
            print(f"  {nl:4d}  FAIL")
        sys.stdout.flush()

    # Fit exponent
    print()
    fit_ns = [n for n in sorted(data.keys()) if 1 - data[n] > 0.001]
    if len(fit_ns) >= 3:
        xs = [math.log(n) for n in fit_ns]
        ys = [math.log(1 - data[n]) for n in fit_ns]
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        syy = sum((y - my) ** 2 for y in ys)
        alpha = sxy / sxx
        C = math.exp(my - alpha * mx)
        r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
        print(f"  5D exponent: alpha = {alpha:.3f}, C = {C:.3f}, R² = {r2:.3f}")
        print(f"  Predicted: alpha = -0.375")
        print(f"  Measured:  alpha = {alpha:.3f}")
        if abs(alpha - (-0.375)) < 0.2:
            print(f"  → CONSISTENT with prediction (within 0.2)")
        else:
            print(f"  → INCONSISTENT (deviation > 0.2)")


if __name__ == "__main__":
    main()
