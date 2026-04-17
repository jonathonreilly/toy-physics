#!/usr/bin/env python3
"""Cross-channel penalty: penalize only edges that cross y=0, not all edges
near y=0.

Gap-as-physics investigation, Experiment 5c.

The global amplitude penalty failed at N=60 because it suppresses ALL amplitude
near y=0, including within-channel paths. The hard gap works because it
preserves within-channel connectivity while blocking cross-channel mixing.

This experiment tests a TOPOLOGY-AWARE soft penalty:
  - Edge (i,j) where y_i and y_j have SAME sign: no penalty (within-channel)
  - Edge (i,j) where y_i and y_j have DIFFERENT sign: penalty applied
    (cross-channel)

This is the continuous analogue of the hard gap's crosslink suppression.
It should preserve within-channel amplitude flow while suppressing mixing.

Also tests a smoother variant: penalty proportional to |y_i - y_j| for
cross-sign edges (wider crosses penalized more).
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
N_LAYERS_LIST = [12, 25, 40, 60]
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
    barrier_layer = n_layers // 3

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

    return positions, dict(adj), barrier_layer


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

    return positions, dict(adj), barrier_layer


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


def propagate_3d_cross_penalty(positions, adj, field, src, k, blocked,
                                penalty, barrier_layer, mode="binary"):
    """Penalize only cross-channel (y sign change) edges post-barrier.

    mode="binary": flat penalty for any sign-crossing edge
    mode="graded": penalty proportional to |y_i - y_j|
    """
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

            # Cross-channel penalty (only post-barrier)
            gap_factor = 1.0
            if x1 > barrier_layer and x2 > barrier_layer:
                cross = (y1 * y2 < 0)  # different sign = cross-channel
                if cross:
                    if mode == "binary":
                        gap_factor = math.exp(-penalty)
                    else:  # graded
                        gap_factor = math.exp(-penalty * abs(y1 - y2) / XYZ_RANGE)

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
    print("CROSS-CHANNEL PENALTY: TOPOLOGY-AWARE SOFT WALL")
    print(f"  Penalize only edges crossing y=0 (post-barrier)")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]
    penalties_binary = [0.5, 1.0, 2.0, 5.0]
    penalties_graded = [1.0, 2.0, 5.0, 10.0]

    print(f"  {'N':>4s}  {'mode':>16s}  {'pur_cl':>10s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 70}")

    for nl in N_LAYERS_LIST:
        # Baselines
        for label, gen_fn, prop_fn in [
            ("uniform", lambda s: generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s),
             lambda p, a, f, s, k, b: propagate_3d(p, a, f, s, k, b)),
            ("hard-gap", lambda s: generate_3d_dag_modular(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, HARD_GAP),
             lambda p, a, f, s, k, b: propagate_3d(p, a, f, s, k, b)),
        ]:
            t0 = time.time()
            pc_all, sn_all, grav_all = [], [], []
            for seed in seeds:
                result = gen_fn(seed)
                positions, adj = result[0], result[1]
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
                print(f"  {nl:4d}  {label:>16s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")

        # Binary cross-penalty
        for pen in penalties_binary:
            t0 = time.time()
            pc_all, sn_all, grav_all = [], [], []
            for seed in seeds:
                positions, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                prop_fn = lambda p, a, f, s, k, b, _pen=pen, _bl=bl: \
                    propagate_3d_cross_penalty(p, a, f, s, k, b, _pen, _bl, "binary")
                r = measure(positions, adj, nl, K_BAND, prop_fn)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
            dt = time.time() - t0
            label = f"cross-bin-{pen:.1f}"
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                print(f"  {nl:4d}  {label:>16s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>16s}  FAIL  {dt:4.0f}s")

        # Graded cross-penalty
        for pen in penalties_graded:
            t0 = time.time()
            pc_all, sn_all, grav_all = [], [], []
            for seed in seeds:
                positions, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                prop_fn = lambda p, a, f, s, k, b, _pen=pen, _bl=bl: \
                    propagate_3d_cross_penalty(p, a, f, s, k, b, _pen, _bl, "graded")
                r = measure(positions, adj, nl, K_BAND, prop_fn)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
            dt = time.time() - t0
            label = f"cross-grad-{pen:.0f}"
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                print(f"  {nl:4d}  {label:>16s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>16s}  FAIL  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  cross-bin-X: flat exp(-X) penalty on edges crossing y=0")
    print("  cross-grad-X: graded exp(-X * |dy|/range) on crossing edges")
    print("  If cross-penalty beats uniform and tracks hard-gap at N=60:")
    print("    → topology-aware soft wall is a viable lane")


if __name__ == "__main__":
    main()
