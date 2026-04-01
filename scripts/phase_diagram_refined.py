#!/usr/bin/env python3
"""Refined phase diagram: fine gap sweep around sweet spot with 24 seeds.

The joint test showed gap=2.0 as the unification sweet spot.
This script does a fine sweep from gap=1.0 to gap=5.0 in steps of 0.5
with 24 seeds per point to pin down the window precisely.

Also extends to N=40 to check stability of the sweet spot.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity_triple(amps_a, amps_b, D, det_list):
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


def run_joint(positions, adj, k_band, n_layers):
    """Joint gravity + decoherence on one graph."""
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

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers), start + env_depth)
    mid_nodes = []
    for layer in layers[start:stop]:
        mid_nodes.extend(by_layer[layer])

    field_mass = compute_field(positions, mass_nodes, 0.1)
    field_flat = [0.0] * len(positions)

    grav_d, pm_v, dec_v = [], [], []

    for k in k_band:
        # Gravity
        am = propagate(positions, adj, field_mass, src, k, blocked)
        af = propagate(positions, adj, field_flat, src, k, blocked)
        pm_m = sum(abs(am[d]) ** 2 for d in det_list)
        pm_f = sum(abs(af[d]) ** 2 for d in det_list)
        if pm_m > 1e-30 and pm_f > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm_m
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pm_f
            grav_d.append(ym - yf)

        # Decoherence
        aa = propagate(positions, adj, field_mass, src, k, blocked | set(sb))
        ab = propagate(positions, adj, field_mass, src, k, blocked | set(sa))
        ba = bin_amplitudes(aa, positions, mid_nodes)
        bb = bin_amplitudes(ab, positions, mid_nodes)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-LAM ** 2 * Sn)
        pc, pcoh, pmin = cl_purity_triple(aa, ab, D, det_list)
        if not math.isnan(pc):
            pm_v.append(pmin)
            dec_v.append(pcoh - pc)

    if not grav_d or not pm_v:
        return None
    return {
        "grav": sum(grav_d) / len(grav_d),
        "pm": sum(pm_v) / len(pm_v),
        "dec": sum(dec_v) / len(dec_v),
    }


def main():
    print("=" * 78)
    print("REFINED PHASE DIAGRAM: gap=1.0..5.0 step 0.5, 24 seeds")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7]")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 24
    gaps = [0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    for nl in [25, 40]:
        print(f"  N={nl}")
        print(f"  {'gap':>5s}  {'grav_d':>8s}  {'grav_SE':>7s}  {'pur_min':>8s}  "
              f"{'pm_SE':>6s}  {'decoh':>8s}  {'n_ok':>4s}  {'both':>7s}")
        print(f"  {'-' * 62}")

        for gap in gaps:
            t0 = time.time()
            grav_all, pm_all, dec_all = [], [], []

            for seed in range(n_seeds):
                positions, adj, _ = generate_modular_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 7 + 3,
                    crosslink_prob=0.02, gap=gap,
                )
                r = run_joint(positions, adj, k_band, nl)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            if grav_all:
                n_ok = len(grav_all)
                ag = sum(grav_all) / n_ok
                se_g = (sum((g - ag) ** 2 for g in grav_all) / n_ok) ** 0.5 / math.sqrt(n_ok)
                apm = sum(pm_all) / n_ok
                se_pm = (sum((p - apm) ** 2 for p in pm_all) / n_ok) ** 0.5 / math.sqrt(n_ok)
                adec = sum(dec_all) / n_ok

                grav_ok = ag > 2 * se_g and ag > 0
                dec_ok = apm < 0.96
                both = "YES" if grav_ok and dec_ok else "grav" if grav_ok else "decoh" if dec_ok else "neither"

                print(f"  {gap:5.1f}  {ag:+8.3f}  {se_g:7.3f}  {apm:8.4f}  "
                      f"{se_pm:6.4f}  {adec:+8.4f}  {n_ok:4d}  {both:>7s}")
            else:
                print(f"  {gap:5.1f}  FAIL")

        print()

    print("=" * 78)
    print("CRITERION: grav_delta > 2*SE AND pur_min < 0.96")
    print("The sweet spot is the gap range where both criteria are met.")


if __name__ == "__main__":
    main()
