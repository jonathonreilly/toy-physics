#!/usr/bin/env python3
"""3D joint gravity + decoherence test.

Adapts the 2D framework to 3D causal DAGs:
  - Positions are (x, y, z) with x = causal layer
  - Barrier in y-z plane: upper slit (y > 3), lower slit (y < -3)
  - Detector: last layer
  - Mass: layer 2/3, nodes at y > 1
  - CL bath: y-bins of amplitude (same as 2D, using y coordinate)

3D modular DAG: post-barrier nodes placed at |y| > gap/2 (avoiding
the y=0 plane), creating channel separation in y.

Question: does the 2D result survive in 3D?
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def generate_3d_dag(n_layers=20, nodes_per_layer=30, xyz_range=12.0,
                    connect_radius=3.0, rng_seed=42, gap=0.0):
    """Generate 3D causal DAG. gap>0 creates y-channel separation post-barrier."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

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
                if use_channels and layer > barrier_layer:
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

                        if use_channels and layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
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
            # 3D directional measure: angle from forward (x) axis
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def bin_amplitudes_3d(amps, positions, nodes):
    """Bin by y-coordinate (same as 2D)."""
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity(amps_a, amps_b, D, det_list):
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


def run_3d_joint(positions, adj, k_band, n_layers):
    """Joint gravity + decoherence on 3D DAG."""
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

    gd, pmv, dv = [], [], []
    for k in k_band:
        am = propagate_3d(positions, adj, field_m, src, k, blocked)
        af = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            gd.append(ym - yf)

        aa = propagate_3d(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_3d(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes_3d(aa, positions, mid)
        bb = bin_amplitudes_3d(ab, positions, mid)
        S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
        NA = sum(abs(a)**2 for a in ba)
        NB = sum(abs(b)**2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM**2 * Sn)
        pc, pcoh, pmin = cl_purity(aa, ab, D_cl, det_list)
        if not math.isnan(pc):
            pmv.append(pmin)
            dv.append(pcoh - pc)

    if not gd or not pmv:
        return None
    return {"grav": sum(gd)/len(gd), "pm": sum(pmv)/len(pmv), "dec": sum(dv)/len(dv)}


def main():
    print("=" * 78)
    print("3D JOINT GRAVITY + DECOHERENCE TEST")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 16 seeds")
    print(f"  3D DAG: nodes at (x, y, z), barrier/slits in y, z free")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    for gap_val in [0.0, 2.0, 4.0]:
        label = f"3D {'uniform' if gap_val == 0 else f'modular gap={gap_val}'}"
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'decoh':>8s}  {'grav':>8s}  "
              f"{'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 44}")

        for nl in [12, 18, 25, 40]:
            t0 = time.time()
            pm_all, dec_all, grav_all = [], [], []

            for seed in seeds:
                positions, adj = generate_3d_dag(
                    n_layers=nl, nodes_per_layer=30, xyz_range=12.0,
                    connect_radius=4.0, rng_seed=seed, gap=gap_val,
                )
                r = run_3d_joint(positions, adj, k_band, nl)
                if r:
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])
                    grav_all.append(r["grav"])

            dt = time.time() - t0

            if pm_all:
                apm = sum(pm_all) / len(pm_all)
                adec = sum(dec_all) / len(dec_all)
                agrav = sum(grav_all) / len(grav_all)
                print(f"  {nl:4d}  {apm:8.4f}  {adec:+8.4f}  {agrav:+8.3f}  "
                      f"{len(pm_all):4d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  FAIL ({len(pm_all)} ok)")

        print()

    print("Does 2D result survive in 3D?")
    print("  Gravity: expect positive delta growing with N")
    print("  Decoherence: expect pur_min < 0.96 at N=25")


import time

if __name__ == "__main__":
    main()
