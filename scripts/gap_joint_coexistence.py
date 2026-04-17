#!/usr/bin/env python3
"""Joint gravity + decoherence coexistence on pruned graphs.

We know path-count pruning creates decoherence through N=100.
Critical question: does gravity survive on the pruned graphs?

Also compare three gap-formation methods head-to-head at each N:
  1. Hard gap (imposed modular topology)
  2. Path-count pruning (global, threshold=0.05)
  3. |y|-removal (simple geometric proxy, |y|<2)

For each, measure BOTH gravity and decoherence on the same graphs.
Joint coexistence = gravity positive AND pur_cl < 0.98 on same seeds.

Additionally: k=0 control on pruned graphs to verify gravity is
still phase-mediated after pruning.
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
N_SEEDS = 24  # More seeds for gravity statistics
N_LAYERS_LIST = [25, 40, 60, 80]


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
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions)-1)
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


def full_measure(positions, adj, n_layers, k_list):
    """Returns (gravity, pur_cl, s_norm) or None."""
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

    if not grav_vals or not pur_vals:
        return None
    return {
        "gravity": sum(grav_vals) / len(grav_vals),
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
        "_sa": sa, "_sb": sb, "_blocked": blocked,
    }


def apply_pathcount_pruning(positions, adj, barrier_layer, sa, sb, blocked,
                             threshold, protected):
    n = len(positions)
    order = _topo_order(adj, n)
    adj_a, adj_b = {}, {}
    blocked_a = blocked | set(sb)
    blocked_b = blocked | set(sa)
    for i, nbs in adj.items():
        if i not in blocked_a: adj_a[i] = [j for j in nbs if j not in blocked_a]
        if i not in blocked_b: adj_b[i] = [j for j in nbs if j not in blocked_b]
    pc_a = compute_path_count(adj_a, sa, n, order)
    pc_b = compute_path_count(adj_b, sb, n, order)
    removed = set()
    for idx in range(n):
        x, y, z = positions[idx]
        if x <= barrier_layer or idx in protected:
            continue
        total = pc_a[idx] + pc_b[idx]
        asym = abs(pc_a[idx] - pc_b[idx]) / total if total > 0 else 0
        if asym < threshold:
            removed.add(idx)
    new_adj = {}
    for i, nbs in adj.items():
        if i in removed: continue
        new_nbs = [j for j in nbs if j not in removed]
        if new_nbs: new_adj[i] = new_nbs
    return new_adj, removed


def apply_y_removal(positions, adj, barrier_layer, y_thresh, protected):
    removed = set()
    for idx, (x, y, z) in enumerate(positions):
        if x <= barrier_layer or idx in protected:
            continue
        if abs(y) < y_thresh:
            removed.add(idx)
    new_adj = {}
    for i, nbs in adj.items():
        if i in removed: continue
        new_nbs = [j for j in nbs if j not in removed]
        if new_nbs: new_adj[i] = new_nbs
    return new_adj, removed


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
    print("JOINT GRAVITY + DECOHERENCE COEXISTENCE ON PRUNED GRAPHS")
    print(f"  NPL={NPL}, CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print("=" * 105)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    print(f"  {'N':>4s}  {'mode':>14s}  {'gravity':>12s}  {'grav_t':>7s}  {'pur_cl':>10s}  "
          f"{'S_norm':>8s}  {'joint':>5s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 82}")

    for nl in N_LAYERS_LIST:
        configs = []

        # 1. Uniform baseline
        def make_uniform(seed, _nl=nl):
            pos, adj, bl = generate_3d_dag_uniform(_nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
            return pos, adj
        configs.append(("uniform", make_uniform))

        # 2. Hard gap
        def make_hardgap(seed, _nl=nl):
            pos, adj, bl = generate_3d_dag_modular(_nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed, 4.0)
            return pos, adj
        configs.append(("hard-gap", make_hardgap))

        # 3. Path-count pruning
        def make_pathcount(seed, _nl=nl):
            pos, adj, bl = generate_3d_dag_uniform(_nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
            r0 = full_measure(pos, adj, _nl, K_BAND)
            if not r0:
                return pos, adj
            n = len(pos)
            by_layer = defaultdict(list)
            for idx, (x, y, z) in enumerate(pos): by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            protected = set(by_layer[layers[0]]) | set(by_layer[layers[-1]]) | set(r0["_sa"] + r0["_sb"])
            new_adj, _ = apply_pathcount_pruning(
                pos, adj, bl, r0["_sa"], r0["_sb"], r0["_blocked"], 0.05, protected)
            return pos, new_adj
        configs.append(("pathcount-0.05", make_pathcount))

        # 4. |y| removal
        def make_yremove(seed, _nl=nl):
            pos, adj, bl = generate_3d_dag_uniform(_nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
            n = len(pos)
            by_layer = defaultdict(list)
            for idx, (x, y, z) in enumerate(pos): by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            protected = set(by_layer[layers[0]]) | set(by_layer[layers[-1]])
            # Add barrier slits to protected
            cy = sum(pos[i][1] for i in range(n)) / n
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if pos[i][1] > cy + 3][:3]
            sb = [i for i in bi if pos[i][1] < cy - 3][:3]
            protected = protected | set(sa + sb)
            new_adj, _ = apply_y_removal(pos, adj, bl, 2.0, protected)
            return pos, new_adj
        configs.append(("|y|<2", make_yremove))

        for label, gen_fn in configs:
            t0 = time.time()
            grav_all, pur_all, sn_all = [], [], []
            n_joint = 0

            for seed in seeds:
                pos, adj = gen_fn(seed)
                r = full_measure(pos, adj, nl, K_BAND)
                if r:
                    grav_all.append(r["gravity"])
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    if r["gravity"] > 0 and r["pur_cl"] < 0.98:
                        n_joint += 1

            dt = time.time() - t0
            if grav_all:
                mg, seg = _mean_se(grav_all)
                mpc, sepc = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                grav_t = mg / seg if seg > 0 else 0
                n_ok = len(grav_all)
                print(f"  {nl:4d}  {label:>14s}  {mg:+8.4f}±{seg:.3f}  {grav_t:+6.2f}  "
                      f"{mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  {n_joint:3d}/{n_ok:<2d}  "
                      f"{n_ok:3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>14s}  FAIL  {dt:4.0f}s")

        # k=0 control for pathcount pruning
        k0_grav = []
        for seed in seeds[:8]:
            pos, adj = make_pathcount(seed)
            n = len(pos)
            by_layer = defaultdict(list)
            for idx, (x, y, z) in enumerate(pos): by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 7: continue
            src = by_layer[layers[0]]
            det_list = list(by_layer[layers[-1]])
            cy = sum(pos[i][1] for i in range(n)) / n
            bl_idx = len(layers) // 3
            bi = by_layer[layers[bl_idx]]
            sa = [i for i in bi if pos[i][1] > cy + 3][:3]
            sb = [i for i in bi if pos[i][1] < cy - 3][:3]
            if not sa or not sb: continue
            blocked = set(bi) - set(sa + sb)
            grav_layer = layers[2 * len(layers) // 3]
            mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
            if not mass_nodes: continue
            field_m = compute_field_3d(pos, mass_nodes)
            field_f = [0.0] * n
            am = propagate_3d(pos, adj, field_m, src, 0.0, blocked)
            af = propagate_3d(pos, adj, field_f, src, 0.0, blocked)
            pm = sum(abs(am[d])**2 for d in det_list)
            pf = sum(abs(af[d])**2 for d in det_list)
            if pm > 1e-30 and pf > 1e-30:
                ym = sum(abs(am[d])**2 * pos[d][1] for d in det_list) / pm
                yf = sum(abs(af[d])**2 * pos[d][1] for d in det_list) / pf
                k0_grav.append(ym - yf)
        if k0_grav:
            mk0 = sum(k0_grav) / len(k0_grav)
            print(f"  {nl:4d}  {'k=0 control':>14s}  {mk0:+8.6f}")

        print()

    print("JOINT COEXISTENCE CRITERIA:")
    print("  gravity > 0 AND pur_cl < 0.98 on same seed")
    print("  grav_t > 2.0 is statistically significant gravity")
    print("  k=0 control must be zero (phase-mediated gravity)")


if __name__ == "__main__":
    main()
