#!/usr/bin/env python3
"""Amplitude penalty scaling test: does the soft domain wall survive at large N?

Gap-as-physics investigation, Experiment 5b.

The soft penalty exp(-pen * exp(-y²/2σ²)) on edges near y=0 creates decoherence
comparable to hard gap at N=40. Critical question: does this hit the same CLT
wall as all previous approaches at N=60-80+?

Also: head-to-head with hard-gap modular at every N for direct comparison.
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
NPL = 30
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 16
N_LAYERS_LIST = [12, 25, 40, 60, 80]

# Best penalty settings from Exp 5
PENALTY = 0.5
SIGMA = 2.0
HARD_GAP = 4.0


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


def generate_3d_dag_uniform(n_layers, nodes_per_layer, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
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

    return positions, dict(adj)


def generate_3d_dag_modular(n_layers, nodes_per_layer, xyz_range, connect_radius, rng_seed, gap):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-xyz_range, xyz_range)
                if layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, xyz_range)
                    else:
                        y = rng.uniform(-xyz_range, -gap / 2)
                else:
                    y = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < 0.02:
                                    adj[prev_idx].append(idx)
                        else:
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj)


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


def propagate_3d_penalty(positions, adj, field, src, k, blocked, penalty, sigma):
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
            y_mid = 0.5 * (y1 + y2)
            gap_factor = math.exp(-penalty * math.exp(-y_mid**2 / (2 * sigma**2)))
            ea = cmath.exp(1j * k * act) * w * gap_factor / L
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


def measure(positions, adj, n_layers, k_band, prop_fn):
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(positions[i][1] for i in range(len(positions))) / len(positions)
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
    stop = min(len(layers) - 1, start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])

    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)

    grav_vals, pur_vals, sn_vals = [], [], []

    for k in k_band:
        am = prop_fn(positions, adj, field_m, src, k, blocked)
        af = prop_fn(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)

        aa = prop_fn(positions, adj, field_m, src, k, blocked | set(sb))
        ab = prop_fn(positions, adj, field_m, src, k, blocked | set(sa))
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

    if not grav_vals or not pur_vals:
        return None
    return {
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
        "gravity": sum(grav_vals) / len(grav_vals),
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
    print("=" * 95)
    print("AMPLITUDE PENALTY SCALING TEST")
    print(f"  Penalty={PENALTY}, sigma={SIGMA} vs hard-gap modular gap={HARD_GAP}")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print(f"  N = {N_LAYERS_LIST}")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    # Also sweep penalty to find best at each N
    penalty_sweep = [0.25, 0.5, 1.0, 2.0]

    print("HEAD-TO-HEAD: penalty vs hard-gap vs uniform baseline")
    print()
    print(f"  {'N':>4s}  {'mode':>12s}  {'pur_cl':>10s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 65}")

    for nl in N_LAYERS_LIST:
        for mode in ["uniform", "hard-gap", "penalty-0.25", "penalty-0.50", "penalty-1.00", "penalty-2.00"]:
            t0 = time.time()
            pc_all, sn_all, grav_all = [], [], []

            for seed in seeds:
                if mode == "uniform":
                    positions, adj = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                    prop_fn = lambda p, a, f, s, k, b: propagate_3d(p, a, f, s, k, b)
                elif mode == "hard-gap":
                    positions, adj = generate_3d_dag_modular(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed, HARD_GAP)
                    prop_fn = lambda p, a, f, s, k, b: propagate_3d(p, a, f, s, k, b)
                else:
                    pen = float(mode.split("-")[1])
                    positions, adj = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                    prop_fn = lambda p, a, f, s, k, b, _pen=pen: propagate_3d_penalty(
                        p, a, f, s, k, b, _pen, SIGMA)

                r = measure(positions, adj, nl, K_BAND, prop_fn)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])

            dt = time.time() - t0
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                print(f"  {nl:4d}  {mode:>12s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {mode:>12s}  FAIL  {dt:4.0f}s")

        print()

    print()
    print("KEY QUESTION: Does penalty pur_cl stay bounded or converge to 1.0 at large N?")
    print("  If penalty tracks hard-gap through N=60-80: soft wall survives CLT")
    print("  If penalty converges to uniform: soft wall is cosmetic, CLT still wins")


if __name__ == "__main__":
    main()
