#!/usr/bin/env python3
"""Local path-count asymmetry: can nodes determine their own persistence locally?

Global path-count asymmetry requires counting all paths from source to node
through each slit — a non-local computation. For a genuine self-maintenance
rule (axiom 2), each node should decide its fate from local information.

Local proxy: for each post-barrier node i, count incoming edges from
y>0 neighbors vs y<0 neighbors. If this local "y-balance" correlates
with the global path-count asymmetry, then the global observable can
be approximated locally.

Tested proxies:
  1. y-balance: (n_edges_from_y>0 - n_edges_from_y<0) / total_edges
  2. weighted y-balance: sum of |y_parent| for y>0 parents vs y<0 parents
  3. 2-hop y-balance: same but computed over 2-hop neighborhood
  4. Simple |y| threshold: remove nodes with |y| < threshold (purely geometric)

If proxy 1 or 2 correlates with global asymmetry AND produces similar
decoherence when used for pruning, the mechanism is genuinely local.
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
N_SEEDS = 16
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


def compute_reverse_adj(adj, n):
    """Build reverse adjacency (parent pointers)."""
    rev = defaultdict(list)
    for i, nbs in adj.items():
        for j in nbs:
            rev[j].append(i)
    return dict(rev)


def compute_local_y_balance(positions, rev_adj, idx):
    """Local proxy: fraction of incoming edges from y>0 vs y<0 parents."""
    parents = rev_adj.get(idx, [])
    if not parents:
        return 0.5  # no parents → neutral
    n_pos = sum(1 for p in parents if positions[p][1] > 0)
    n_neg = sum(1 for p in parents if positions[p][1] < 0)
    total = n_pos + n_neg
    if total == 0:
        return 0.5
    return abs(n_pos - n_neg) / total


def compute_2hop_y_balance(positions, rev_adj, idx):
    """2-hop proxy: y-balance including grandparents."""
    parents = rev_adj.get(idx, [])
    grandparents = set()
    for p in parents:
        for gp in rev_adj.get(p, []):
            grandparents.add(gp)
    all_ancestors = set(parents) | grandparents
    if not all_ancestors:
        return 0.5
    n_pos = sum(1 for a in all_ancestors if positions[a][1] > 0)
    n_neg = sum(1 for a in all_ancestors if positions[a][1] < 0)
    total = n_pos + n_neg
    if total == 0:
        return 0.5
    return abs(n_pos - n_neg) / total


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


def measure(positions, adj, n_layers, k_band):
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
        "_sa": sa, "_sb": sb, "_blocked": blocked,
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
    print("=" * 100)
    print("LOCAL PATH-COUNT ASYMMETRY: IS THE MECHANISM LOCAL?")
    print(f"  NPL={NPL}, CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    # Part 1: Correlation between local proxies and global asymmetry
    print("PART 1: LOCAL vs GLOBAL CORRELATION (N=40, seed=3)")
    print()
    positions, adj, bl = generate_3d_dag_uniform(40, NPL, XYZ_RANGE, CONNECT_RADIUS, 3)
    n = len(positions)
    r0 = measure(positions, adj, 40, K_BAND)
    if r0:
        order = _topo_order(adj, n)
        sa, sb, blocked = r0["_sa"], r0["_sb"], r0["_blocked"]
        adj_a, adj_b = {}, {}
        blocked_a = blocked | set(sb)
        blocked_b = blocked | set(sa)
        for i, nbs in adj.items():
            if i not in blocked_a: adj_a[i] = [j for j in nbs if j not in blocked_a]
            if i not in blocked_b: adj_b[i] = [j for j in nbs if j not in blocked_b]
        pc_a = compute_path_count(adj_a, sa, n, order)
        pc_b = compute_path_count(adj_b, sb, n, order)
        rev_adj = compute_reverse_adj(adj, n)

        # Compute all proxies
        global_asym, local_1hop, local_2hop, abs_y = [], [], [], []
        for idx in range(n):
            x, y, z = positions[idx]
            if x <= bl:
                continue
            total = pc_a[idx] + pc_b[idx]
            ga = abs(pc_a[idx] - pc_b[idx]) / total if total > 0 else 0
            l1 = compute_local_y_balance(positions, rev_adj, idx)
            l2 = compute_2hop_y_balance(positions, rev_adj, idx)
            ay = abs(y) / XYZ_RANGE
            global_asym.append(ga)
            local_1hop.append(l1)
            local_2hop.append(l2)
            abs_y.append(ay)

        # Compute correlations
        def pearson(xs, ys):
            n = len(xs)
            mx = sum(xs) / n
            my = sum(ys) / n
            sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
            sxx = sum((x-mx)**2 for x in xs)
            syy = sum((y-my)**2 for y in ys)
            return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else 0

        r_1hop = pearson(global_asym, local_1hop)
        r_2hop = pearson(global_asym, local_2hop)
        r_absy = pearson(global_asym, abs_y)

        print(f"  Correlation with global path-count asymmetry:")
        print(f"    1-hop y-balance:  r = {r_1hop:.4f}")
        print(f"    2-hop y-balance:  r = {r_2hop:.4f}")
        print(f"    |y|/range:        r = {r_absy:.4f}")
        print()
        print(f"  If |y| correlates highly → the gap is just a geometric proxy")
        print(f"  If 1-hop >> |y| → local connectivity carries extra info")

    # Part 2: Prune by local proxies and compare to global
    print()
    print("PART 2: PRUNING BY LOCAL PROXY vs GLOBAL vs |y|")
    print()

    print(f"  {'N':>4s}  {'mode':>16s}  {'pur_cl':>10s}  {'S_norm':>8s}  "
          f"{'rem%':>5s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 62}")

    for nl in N_LAYERS_LIST:
        # Baseline
        t0 = time.time()
        pc_all, sn_all = [], []
        for seed in seeds:
            pos, adj2, _ = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
            r = measure(pos, adj2, nl, K_BAND)
            if r: pc_all.append(r["pur_cl"]); sn_all.append(r["s_norm"])
        dt = time.time() - t0
        if pc_all:
            mpc, sepc = _mean_se(pc_all); msn, _ = _mean_se(sn_all)
            print(f"  {nl:4d}  {'uniform':>16s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                  f"{'--':>5s}  {len(pc_all):3d}  {dt:4.0f}s")

        # Pruning variants (all at ~15% removal target)
        for label, prune_fn_factory in [
            ("global-0.10", lambda pos, adj2, bl, sa, sb, blk, rev:
                ("global", 0.10, None)),
            ("1hop-0.30", lambda pos, adj2, bl, sa, sb, blk, rev:
                ("1hop", 0.30, rev)),
            ("2hop-0.30", lambda pos, adj2, bl, sa, sb, blk, rev:
                ("2hop", 0.30, rev)),
            ("|y|<2.0", lambda pos, adj2, bl, sa, sb, blk, rev:
                ("absy", 2.0, None)),
            ("|y|<3.0", lambda pos, adj2, bl, sa, sb, blk, rev:
                ("absy", 3.0, None)),
        ]:
            t0 = time.time()
            pc_all, sn_all, rem_all = [], [], []
            for seed in seeds:
                pos, adj2, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                nn = len(pos)
                r0 = measure(pos, adj2, nl, K_BAND)
                if not r0:
                    continue
                sa, sb, blk = r0["_sa"], r0["_sb"], r0["_blocked"]
                rev = compute_reverse_adj(adj2, nn)
                mode, thresh, _ = prune_fn_factory(pos, adj2, bl, sa, sb, blk, rev)

                # Compute pruning observable
                protected = set(r0.get("_sa", []) + r0.get("_sb", [])) | set(sa + sb)
                by_layer2 = defaultdict(list)
                for idx2, (x, y, z) in enumerate(pos): by_layer2[round(x)].append(idx2)
                layers2 = sorted(by_layer2.keys())
                det2 = set(by_layer2[layers2[-1]])
                src2 = set(by_layer2[layers2[0]])
                protected = protected | det2 | src2

                if mode == "global":
                    order = _topo_order(adj2, nn)
                    adj_a, adj_b = {}, {}
                    blocked_a = blk | set(sb)
                    blocked_b = blk | set(sa)
                    for i, nbs in adj2.items():
                        if i not in blocked_a: adj_a[i] = [j for j in nbs if j not in blocked_a]
                        if i not in blocked_b: adj_b[i] = [j for j in nbs if j not in blocked_b]
                    pca = compute_path_count(adj_a, sa, nn, order)
                    pcb = compute_path_count(adj_b, sb, nn, order)

                removed = set()
                n_post = 0
                for idx2 in range(nn):
                    x, y, z = pos[idx2]
                    if x <= bl or idx2 in protected:
                        continue
                    n_post += 1
                    if mode == "global":
                        total = pca[idx2] + pcb[idx2]
                        obs = abs(pca[idx2] - pcb[idx2]) / total if total > 0 else 0
                        if obs < thresh:
                            removed.add(idx2)
                    elif mode == "1hop":
                        obs = compute_local_y_balance(pos, rev, idx2)
                        if obs < thresh:
                            removed.add(idx2)
                    elif mode == "2hop":
                        obs = compute_2hop_y_balance(pos, rev, idx2)
                        if obs < thresh:
                            removed.add(idx2)
                    elif mode == "absy":
                        if abs(y) < thresh:
                            removed.add(idx2)

                rem_all.append(100 * len(removed) / max(1, n_post))
                new_adj = {}
                for i, nbs in adj2.items():
                    if i in removed: continue
                    new_nbs = [j for j in nbs if j not in removed]
                    if new_nbs: new_adj[i] = new_nbs
                r = measure(pos, new_adj, nl, K_BAND)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])

            dt = time.time() - t0
            if pc_all:
                mpc, sepc = _mean_se(pc_all); msn, _ = _mean_se(sn_all)
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {nl:4d}  {label:>16s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mrem:4.1f}%  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {nl:4d}  {label:>16s}  FAIL  rem={mrem:.1f}%  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  If |y|<2 ≈ global-0.10: gap is just geometry, no topology needed")
    print("  If global >> |y|: path-count carries non-geometric info")
    print("  If 1hop ≈ global: mechanism is LOCAL (axiom 2 compatible)")


if __name__ == "__main__":
    main()
