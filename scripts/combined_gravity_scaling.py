#!/usr/bin/env python3
"""Combined propagator: gravity + decoherence + scaling on LN+modular.

Tests:
1. Does gravity survive layer normalization? (paired per-seed delta)
2. Full combined scaling curve N=25..100 for decoherence
3. Joint gravity+decoherence on same instances
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
from scripts.topology_families import generate_modular_dag

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
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_ln(positions, adj, field, src, k, blocked=None):
    """Corrected propagator with per-layer normalization."""
    n = len(positions)
    blocked = blocked or set()
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
        if li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm
    return amps


def propagate_linear(positions, adj, field, src, k, blocked=None):
    """Standard linear propagator (no normalization)."""
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


def run_joint(positions, adj, k_band, nl, use_ln=False):
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

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    env_depth = max(1, round(nl / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mass_env = []
    for layer in layers[start:stop]:
        mass_env.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, list(set(mass_env) | set(mass_nodes)))
    field_flat = [0.0] * len(positions)

    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])

    prop = propagate_ln if use_ln else propagate_linear

    gd, pmv, dv = [], [], []
    for k in k_band:
        # Gravity (paired delta)
        am = prop(positions, adj, field, src, k, blocked)
        af = prop(positions, adj, field_flat, src, k, blocked)
        pm_m = sum(abs(am[d]) ** 2 for d in det_list)
        pm_f = sum(abs(af[d]) ** 2 for d in det_list)
        if pm_m > 1e-30 and pm_f > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm_m
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pm_f
            gd.append(ym - yf)

        # Decoherence
        aa = prop(positions, adj, field, src, k, blocked | set(sb))
        ab = prop(positions, adj, field, src, k, blocked | set(sa))
        ba = [0j] * N_YBINS
        bb = [0j] * N_YBINS
        bw = 24.0 / N_YBINS
        for m in mid:
            b_idx = int((positions[m][1] + 12.0) / bw)
            b_idx = max(0, min(N_YBINS - 1, b_idx))
            ba[b_idx] += aa[m]
            bb[b_idx] += ab[m]
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM ** 2 * Sn)

        def _pur(Dv):
            rho = {}
            for d1 in det_list:
                for d2 in det_list:
                    rho[(d1, d2)] = (
                        aa[d1].conjugate() * aa[d2]
                        + ab[d1].conjugate() * ab[d2]
                        + Dv * aa[d1].conjugate() * ab[d2]
                        + Dv * ab[d1].conjugate() * aa[d2]
                    )
            tr = sum(rho[(d, d)] for d in det_list).real
            if tr <= 1e-30:
                return math.nan
            for key in rho:
                rho[key] /= tr
            return sum(abs(v) ** 2 for v in rho.values()).real

        pmin = _pur(0.0)
        pcoh = _pur(1.0)
        pcl = _pur(D_cl)
        if not math.isnan(pmin):
            pmv.append(pmin)
            dv.append(pcoh - pcl)

    if not pmv:
        return None
    return {
        "grav": sum(gd) / len(gd) if gd else 0.0,
        "pm": sum(pmv) / len(pmv),
        "dec": sum(dv) / len(dv),
    }


def main():
    print("=" * 78)
    print("COMBINED PROPAGATOR: Gravity + Decoherence + Scaling")
    print(f"  Layer norm + modular gap=2, CL bath lambda={LAM}")
    print(f"  24 seeds, k-band [3,5,7]")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 24
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    configs = [
        ("Linear + uniform", False, 0.0),
        ("LN + modular gap=2", True, 2.0),
        ("LN + modular gap=4", True, 4.0),
    ]

    for name, use_ln, gap in configs:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'decoh':>8s}  "
              f"{'grav':>8s}  {'gSE':>7s}  {'g/SE':>5s}  {'n':>3s}  {'t':>4s}")
        print(f"  {'-' * 64}")

        for nl in [25, 30, 40, 50, 60, 80, 100]:
            t0 = time.time()
            grav_all, pm_all, dec_all = [], [], []

            for seed in seeds:
                if gap > 0:
                    positions, adj, _ = generate_modular_dag(
                        n_layers=nl, nodes_per_layer=25, y_range=12.0,
                        connect_radius=3.0, rng_seed=seed, gap=gap)
                else:
                    positions, adj, _ = generate_causal_dag(
                        n_layers=nl, nodes_per_layer=25, y_range=12.0,
                        connect_radius=3.0, rng_seed=seed)

                r = run_joint(positions, adj, k_band, nl, use_ln=use_ln)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            dt = time.time() - t0
            if grav_all:
                n_ok = len(grav_all)
                apm = sum(pm_all) / n_ok
                adec = sum(dec_all) / n_ok
                ag = sum(grav_all) / n_ok
                se_g = (sum((g - ag) ** 2 for g in grav_all) / n_ok) ** 0.5 / math.sqrt(n_ok)
                g_se = ag / se_g if se_g > 0 else 0
                print(f"  {nl:4d}  {apm:8.4f}  {1-apm:7.4f}  {adec:+8.4f}  "
                      f"{ag:+8.3f}  {se_g:7.3f}  {g_se:5.1f}  {n_ok:3d}  {dt:3.0f}s")
            else:
                print(f"  {nl:4d}  FAIL")
            sys.stdout.flush()
        print()

    # Scaling law fit
    print("=" * 78)
    print("SCALING COMPARISON")
    print("=" * 78)


if __name__ == "__main__":
    main()
