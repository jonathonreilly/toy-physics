#!/usr/bin/env python3
"""Path-count pruning at large N with higher node density.

NPL=30 fails at N>=70 due to graph sparsity. Test with NPL=50 to get
reliable amplitude throughput at N=60-100.

Also test: is the path-count asymmetry a LOCAL observable?
For each node, compute the asymmetry using only paths through its
immediate neighborhood (2-hop). If local asymmetry is still spatially
structured, the pruning rule could be implemented as a local
self-maintenance check (axiom 2).
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
NPL = 50  # Higher density for large N
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 16
N_LAYERS_LIST = [25, 40, 60, 80, 100]


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
    barrier_layer = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
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
    return positions, dict(adj), barrier_layer


def generate_3d_dag_modular(n_layers, npl, xyz_range, connect_radius, rng_seed, gap):
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
            for node_i in range(npl):
                z = rng.uniform(-xyz_range, xyz_range)
                if gap > 0 and layer > barrier_layer:
                    if node_i < npl // 2:
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
                        if gap > 0 and layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
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


def compute_path_count(adj, start_nodes, n, order):
    counts = [0] * n
    for s in start_nodes:
        counts[s] = 1
    for i in order:
        if counts[i] == 0:
            continue
        for j in adj.get(i, []):
            counts[j] += counts[i]
    return counts


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


def get_barrier_info(positions, adj, n_layers):
    """Extract barrier/slit/mass structure."""
    n = len(positions)
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
    cy = sum(positions[i][1] for i in range(n)) / n
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
    return {
        "src": src, "det": det_list, "sa": sa, "sb": sb,
        "blocked": blocked, "mass": mass_nodes, "mid": mid,
        "bl": bl_idx, "layers": layers, "by_layer": by_layer,
    }


def measure(positions, adj, n_layers, k_band, info=None):
    if info is None:
        info = get_barrier_info(positions, adj, n_layers)
    if info is None:
        return None
    src, det_list = info["src"], info["det"]
    sa, sb, blocked = info["sa"], info["sb"], info["blocked"]
    mass_nodes, mid = info["mass"], info["mid"]
    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)
    grav_vals, pur_vals, sn_vals = [], [], []
    for k in k_band:
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
    if not grav_vals or not pur_vals:
        return None
    return {
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
        "gravity": sum(grav_vals) / len(grav_vals),
    }


def prune_by_pathcount(positions, adj, barrier_layer, sa, sb, blocked,
                        threshold, protected):
    """Remove post-barrier nodes with path-count asymmetry < threshold."""
    n = len(positions)
    order = _topo_order(adj, n)

    # Compute path counts from each slit
    adj_a, adj_b = {}, {}
    blocked_a = blocked | set(sb)
    blocked_b = blocked | set(sa)
    for i, nbs in adj.items():
        if i not in blocked_a:
            adj_a[i] = [j for j in nbs if j not in blocked_a]
        if i not in blocked_b:
            adj_b[i] = [j for j in nbs if j not in blocked_b]

    pc_a = compute_path_count(adj_a, sa, n, order)
    pc_b = compute_path_count(adj_b, sb, n, order)

    removed = set()
    n_post = 0
    for idx in range(n):
        x, y, z = positions[idx]
        if x <= barrier_layer or idx in protected:
            continue
        n_post += 1
        total = pc_a[idx] + pc_b[idx]
        if total > 0:
            asym = abs(pc_a[idx] - pc_b[idx]) / total
        else:
            asym = 0.0
        if asym < threshold:
            removed.add(idx)

    new_adj = {}
    for i, nbs in adj.items():
        if i in removed:
            continue
        new_nbs = [j for j in nbs if j not in removed]
        if new_nbs:
            new_adj[i] = new_nbs

    return new_adj, removed, n_post


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m)**2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 100)
    print("PATH-COUNT PRUNING AT LARGE N (NPL=50)")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print(f"  N = {N_LAYERS_LIST}")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]
    thresholds = [0.05, 0.10, 0.15, 0.20]

    print(f"  {'N':>4s}  {'mode':>14s}  {'pur_cl':>10s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'rem%':>5s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    for nl in N_LAYERS_LIST:
        # Uniform baseline
        t0 = time.time()
        pc_all, sn_all, grav_all = [], [], []
        for seed in seeds:
            positions, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
            r = measure(positions, adj, nl, K_BAND)
            if r:
                pc_all.append(r["pur_cl"])
                sn_all.append(r["s_norm"])
                grav_all.append(r["gravity"])
        dt = time.time() - t0
        if pc_all:
            mpc, sepc = _mean_se(pc_all)
            msn, _ = _mean_se(sn_all)
            mg, seg = _mean_se(grav_all)
            print(f"  {nl:4d}  {'uniform':>14s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                  f"{mg:+7.4f}±{seg:.3f}  {'--':>5s}  {len(pc_all):3d}  {dt:4.0f}s")
        else:
            print(f"  {nl:4d}  {'uniform':>14s}  FAIL  {dt:4.0f}s")

        # Hard-gap baseline
        t0 = time.time()
        pc_all, sn_all, grav_all = [], [], []
        for seed in seeds:
            positions, adj, bl = generate_3d_dag_modular(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed, 4.0)
            r = measure(positions, adj, nl, K_BAND)
            if r:
                pc_all.append(r["pur_cl"])
                sn_all.append(r["s_norm"])
                grav_all.append(r["gravity"])
        dt = time.time() - t0
        if pc_all:
            mpc, sepc = _mean_se(pc_all)
            msn, _ = _mean_se(sn_all)
            mg, seg = _mean_se(grav_all)
            print(f"  {nl:4d}  {'hard-gap':>14s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                  f"{mg:+7.4f}±{seg:.3f}  {'--':>5s}  {len(pc_all):3d}  {dt:4.0f}s")
        else:
            print(f"  {nl:4d}  {'hard-gap':>14s}  FAIL  {dt:4.0f}s")

        # Path-count pruning
        for thresh in thresholds:
            t0 = time.time()
            pc_all, sn_all, grav_all, rem_all = [], [], [], []
            for seed in seeds:
                positions, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                info = get_barrier_info(positions, adj, nl)
                if info is None:
                    continue
                protected = set(info["src"]) | set(info["det"]) | set(info["sa"] + info["sb"])
                new_adj, removed, n_post = prune_by_pathcount(
                    positions, adj, bl, info["sa"], info["sb"],
                    info["blocked"], thresh, protected)
                rem_all.append(100 * len(removed) / max(1, n_post))
                r = measure(positions, new_adj, nl, K_BAND)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
            dt = time.time() - t0
            label = f"prune-{thresh:.2f}"
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {nl:4d}  {label:>14s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {mrem:4.1f}%  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {nl:4d}  {label:>14s}  FAIL  rem={mrem:.1f}%  {dt:4.0f}s")

        print()

    print("SCALING SUMMARY:")
    print("  Watch (1-pur_cl) at prune-0.10 across N:")
    print("    If stable → mechanism beats CLT")
    print("    If shrinking → CLT still wins asymptotically")


if __name__ == "__main__":
    main()
