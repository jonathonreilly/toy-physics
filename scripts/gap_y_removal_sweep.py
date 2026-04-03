#!/usr/bin/env python3
"""Optimal |y|-removal threshold sweep.

|y|<2 removal gave the best joint coexistence at N=80. Sweep the
threshold to find the optimum and characterize the gravity-decoherence
trade-off.

Thresholds: |y| < {0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0}
N = {25, 40, 60, 80, 100}

At each (N, threshold): measure gravity, decoherence, joint count.
Find the threshold that maximizes joint coexistence at each N.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
N_YBINS = 8
LAM = 10.0
CONNECT_RADIUS = 4.0
XYZ_RANGE = 12.0
NPL = 50
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 24
N_LAYERS_LIST = [25, 40, 60, 80, 100]
Y_THRESHOLDS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]


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


def generate_3d_dag_uniform(n_layers, npl, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


def propagate_3d(positions, adj, field, src, k, blocked=None):
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
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def compute_field_3d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2) + 0.1
            field[i] += 0.1 / r
    return field


def bin_amplitudes_3d(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
                + D * amps_a[d1].conjugate() * amps_b[d2]
                + D * amps_b[d1].conjugate() * amps_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def full_measure(positions, adj, n_layers, k_list):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7: return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list: return None
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb: return None
    blocked = set(bi) - set(sa + sb)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes: return None
    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * n
    grav_vals, pur_vals, sn_vals = [], [], []
    for k in k_list:
        am = propagate_3d(positions, adj, field_m, src, k, blocked)
        af = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)
        aa = propagate_3d(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_3d(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes_3d(aa, positions, mid)
        bb = bin_amplitudes_3d(ab, positions, mid)
        S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
        NA = sum(abs(a)**2 for a in ba)
        NB = sum(abs(b)**2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM**2 * Sn)
        pc = cl_purity(aa, ab, D_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)
            sn_vals.append(Sn)
    if not grav_vals or not pur_vals: return None
    return {
        "gravity": sum(grav_vals) / len(grav_vals),
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
    }


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m)**2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 105)
    print("|y|-REMOVAL THRESHOLD SWEEP")
    print(f"  NPL={NPL}, CL bath lambda={LAM}, {N_SEEDS} seeds")
    print(f"  Thresholds: {Y_THRESHOLDS}")
    print("=" * 105)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    print(f"  {'N':>4s}  {'|y|<':>5s}  {'rem%':>5s}  {'gravity':>12s}  {'grav_t':>7s}  "
          f"{'pur_cl':>10s}  {'S_norm':>8s}  {'joint':>5s}  {'ok':>3s}")
    print(f"  {'-' * 75}")

    for nl in N_LAYERS_LIST:
        for yt in Y_THRESHOLDS:
            grav_all, pur_all, sn_all, rem_all = [], [], [], []
            n_joint = 0

            for seed in seeds:
                pos, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)

                if yt > 0:
                    by_layer = defaultdict(list)
                    for idx, (x, y, z) in enumerate(pos):
                        by_layer[round(x)].append(idx)
                    layers = sorted(by_layer.keys())
                    protected = set(by_layer[layers[0]]) | set(by_layer[layers[-1]])
                    cy = sum(pos[i][1] for i in range(n)) / n
                    bl_idx = len(layers) // 3
                    bi = by_layer[layers[bl_idx]]
                    sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                    sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                    protected = protected | set(sa + sb)

                    removed = set()
                    n_post = 0
                    for idx, (x, y, z) in enumerate(pos):
                        if x <= bl or idx in protected:
                            continue
                        n_post += 1
                        if abs(y) < yt:
                            removed.add(idx)
                    rem_all.append(100 * len(removed) / max(1, n_post))

                    new_adj = {}
                    for i, nbs in adj.items():
                        if i in removed: continue
                        new_nbs = [j for j in nbs if j not in removed]
                        if new_nbs: new_adj[i] = new_nbs
                    adj = new_adj

                r = full_measure(pos, adj, nl, K_BAND)
                if r:
                    grav_all.append(r["gravity"])
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    if r["gravity"] > 0 and r["pur_cl"] < 0.98:
                        n_joint += 1

            if grav_all:
                mg, seg = _mean_se(grav_all)
                mpc, sepc = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                gt = mg / seg if seg > 0 else 0
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                n_ok = len(grav_all)
                label = f"{yt:.1f}" if yt > 0 else "none"
                print(f"  {nl:4d}  {label:>5s}  {mrem:4.1f}%  {mg:+8.4f}±{seg:.3f}  {gt:+6.2f}  "
                      f"{mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  {n_joint:3d}/{n_ok:<2d}  {n_ok:3d}")
        print()

    print("TRADE-OFF MAP:")
    print("  Small |y| threshold: weak decoherence, strong gravity")
    print("  Large |y| threshold: strong decoherence, reduced connectivity")
    print("  Optimum: max joint seeds at each N")


if __name__ == "__main__":
    main()
