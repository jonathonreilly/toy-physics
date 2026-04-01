#!/usr/bin/env python3
"""Diagnose the N=80 decoherence ceiling.

Three hypotheses:
  H1: CLT is universal — pur_min approaches 1 regardless of bath params
  H2: env_depth too shallow — need more post-barrier layers in bath
  H3: lambda too small — need lambda to grow with N

Tests:
  1. pur_min vs N (the floor — bath-independent)
  2. S_norm vs N (bath contrast — does it shrink?)
  3. pur_cl vs N at multiple lambda values
  4. pur_cl vs N at multiple env_depth fractions
  5. pur_cl with ALL post-barrier layers as env (max depth)

If pur_min itself approaches 1, the ceiling is fundamental (H1).
If pur_min stays low but pur_cl climbs, the bath params need tuning (H2/H3).
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
N_YBINS = 8


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


def compute_field(positions, adj, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
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


def build_setup(positions, adj, env_depth_layers=1):
    n = len(positions)
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
    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    # Mass/field
    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, env_depth_layers))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    full_mass = set(mass_nodes) | set(grav_mass)
    field = compute_field(positions, adj, list(full_mass))
    # Mid nodes for bath (using env_depth_layers)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    return {
        "by_layer": by_layer, "layers": layers, "src": src,
        "det_list": det_list, "cy": cy, "blocked": blocked,
        "field": field, "sa": sa, "sb": sb, "bl_idx": bl_idx,
        "mid": mid,
    }


def bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity(amps_a, amps_b, D, det_list):
    """Returns (pur_cl, pur_coh, pur_min)."""
    def _pur(Dv):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + Dv * amps_a[d1].conjugate() * amps_b[d2]
                    + Dv * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real
    return _pur(D), _pur(1.0), _pur(0.0)


def run_diagnosis(nl, env_depth, lam, seed):
    """Run one graph at specified env_depth and lambda."""
    k_band = [3.0, 5.0, 7.0]

    positions, adj, _ = generate_causal_dag(
        n_layers=nl, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=seed,
    )
    setup = build_setup(positions, adj, env_depth_layers=env_depth)
    if setup is None:
        return None

    blocked = setup["blocked"]
    field = setup["field"]
    src = setup["src"]
    det_list = setup["det_list"]
    by_layer = setup["by_layer"]
    layers = setup["layers"]
    bl_idx = setup["bl_idx"]
    sa = setup["sa"]
    sb = setup["sb"]

    # Get mid nodes for this env_depth
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, env_depth))
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])

    pm_k, pc_k, pmin_k, sn_k = [], [], [], []
    for k in k_band:
        amps_a = propagate(positions, adj, field, src, k, blocked | set(sb))
        amps_b = propagate(positions, adj, field, src, k, blocked | set(sa))

        ba = bin_amplitudes(amps_a, positions, mid)
        bb = bin_amplitudes(amps_b, positions, mid)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-lam ** 2 * Sn)

        pc, pcoh, pmin = cl_purity(amps_a, amps_b, D, det_list)
        if not math.isnan(pc):
            pc_k.append(pc)
            pmin_k.append(pmin)
            sn_k.append(Sn)

    if not pc_k:
        return None
    return {
        "pc": sum(pc_k) / len(pc_k),
        "pmin": sum(pmin_k) / len(pmin_k),
        "sn": sum(sn_k) / len(sn_k),
    }


def main():
    print("=" * 78)
    print("CEILING DIAGNOSIS: Why does pur_cl climb at N=80?")
    print("=" * 78)
    print()

    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]
    n_list = [12, 18, 25, 40, 60, 80, 100]

    # ─── Test 1: pur_min vs N (bath-independent floor) ─────────────
    print("TEST 1: pur_min vs N (bath-independent — the fundamental floor)")
    print(f"  env_depth = N/6 (standard), lambda irrelevant for pur_min")
    print(f"  {'N':>4s}  {'pur_min':>8s}  {'SE':>6s}  {'n_ok':>4s}")
    print(f"  {'-' * 28}")

    for nl in n_list:
        vals = []
        for seed in seeds:
            r = run_diagnosis(nl, max(1, round(nl/6)), 10.0, seed)
            if r:
                vals.append(r["pmin"])
        if vals:
            avg = sum(vals) / len(vals)
            se = (sum((v - avg)**2 for v in vals) / len(vals))**0.5 / math.sqrt(len(vals))
            print(f"  {nl:4d}  {avg:8.4f}  {se:6.4f}  {len(vals):4d}")
        sys.stdout.flush()

    # ─── Test 2: S_norm vs N (does bath contrast shrink?) ──────────
    print()
    print("TEST 2: S_norm vs N (bath contrast — does it shrink at large N?)")
    print(f"  {'N':>4s}  {'S_norm':>8s}  {'SE':>6s}")
    print(f"  {'-' * 22}")

    for nl in n_list:
        vals = []
        for seed in seeds:
            r = run_diagnosis(nl, max(1, round(nl/6)), 10.0, seed)
            if r:
                vals.append(r["sn"])
        if vals:
            avg = sum(vals) / len(vals)
            se = (sum((v - avg)**2 for v in vals) / len(vals))**0.5 / math.sqrt(len(vals))
            print(f"  {nl:4d}  {avg:8.5f}  {se:6.5f}")
        sys.stdout.flush()

    # ─── Test 3: pur_cl vs lambda at N=80 ──────────────────────────
    print()
    print("TEST 3: pur_cl vs lambda at N=80 (can stronger bath beat ceiling?)")
    print(f"  {'lam':>6s}  {'pur_cl':>8s}  {'pur_min':>8s}  {'D_avg':>8s}")
    print(f"  {'-' * 36}")

    for lam in [5.0, 10.0, 20.0, 50.0, 100.0]:
        pc_all, pm_all, sn_all = [], [], []
        for seed in seeds:
            r = run_diagnosis(80, max(1, round(80/6)), lam, seed)
            if r:
                pc_all.append(r["pc"])
                pm_all.append(r["pmin"])
                sn_all.append(r["sn"])
        if pc_all:
            avg_pc = sum(pc_all) / len(pc_all)
            avg_pm = sum(pm_all) / len(pm_all)
            avg_sn = sum(sn_all) / len(sn_all)
            avg_D = math.exp(-lam**2 * avg_sn)
            print(f"  {lam:6.0f}  {avg_pc:8.4f}  {avg_pm:8.4f}  {avg_D:8.6f}")
        sys.stdout.flush()

    # ─── Test 4: pur_cl vs env_depth at N=80 ──────────────────────
    print()
    print("TEST 4: pur_cl vs env_depth at N=80, lambda=10")
    print(f"  {'depth':>6s}  {'pur_cl':>8s}  {'pur_min':>8s}  {'S_norm':>8s}  {'n_mid':>6s}")
    print(f"  {'-' * 44}")

    for depth_frac in [1/6, 1/3, 1/2, 2/3]:
        depth = max(1, round(80 * depth_frac))
        pc_all, pm_all, sn_all = [], [], []
        for seed in seeds:
            r = run_diagnosis(80, depth, 10.0, seed)
            if r:
                pc_all.append(r["pc"])
                pm_all.append(r["pmin"])
                sn_all.append(r["sn"])
        if pc_all:
            avg_pc = sum(pc_all) / len(pc_all)
            avg_pm = sum(pm_all) / len(pm_all)
            avg_sn = sum(sn_all) / len(sn_all)
            print(f"  {depth:6d}  {avg_pc:8.4f}  {avg_pm:8.4f}  {avg_sn:8.5f}  {'~'+str(depth*25):>6s}")
        sys.stdout.flush()

    print()
    print("=" * 78)
    print("DIAGNOSIS SUMMARY")
    print("  If pur_min → 1 at N=80: H1 confirmed (CLT fundamental)")
    print("  If pur_min stays low but pur_cl → 1: bath params need tuning")
    print("  If lambda=100 or full-depth beats ceiling: H2/H3 confirmed")


if __name__ == "__main__":
    main()
