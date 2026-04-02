#!/usr/bin/env python3
"""Topological path asymmetry: can graph-theoretic observables create a gap?

Exp 6 showed amplitude-based D=0 everywhere on uniform DAGs (CLT).
But path COUNT asymmetry is a graph property, not an amplitude property.

For each post-barrier node, compute:
  n_A = number of paths reachable from slit A
  n_B = number of paths reachable from slit B
  asymmetry = |n_A - n_B| / (n_A + n_B)

If asymmetry is spatially structured (low near y=0, high far from y=0),
then removing low-asymmetry nodes creates a gap from graph topology alone.

Two approaches:
  1. Path count asymmetry (exact, but expensive for large graphs)
  2. Reachability asymmetry (which slit can reach this node at all?)
     - Much cheaper: just BFS from each slit
     - Binary: reachable from A only, B only, or both

Then test: remove "both-reachable" or "low-asymmetry" nodes and
measure decoherence on the pruned graph.
"""

from __future__ import annotations
import argparse
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
N_LAYERS_LIST = [12, 25, 40]


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


def compute_reachability(adj, start_nodes, n):
    """BFS forward reachability from start_nodes. Returns set of reachable nodes."""
    visited = set(start_nodes)
    queue = deque(start_nodes)
    while queue:
        node = queue.popleft()
        for nb in adj.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return visited


def compute_path_count(adj, start_nodes, n, order):
    """Count paths from start_nodes to each node (forward DAG).
    Uses dynamic programming on topo order."""
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


def measure(positions, adj, n_layers, k_band):
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


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m)**2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=N_LAYERS_LIST)
    parser.add_argument("--npl", type=int, default=NPL)
    parser.add_argument("--xyz-range", type=float, default=XYZ_RANGE)
    parser.add_argument("--connect-radius", type=float, default=CONNECT_RADIUS)
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.1, 0.2, 0.3, 0.5, 0.7, 0.9])
    parser.add_argument("--skip-diagnostic", action="store_true")
    args = parser.parse_args()

    print("=" * 95)
    print("TOPOLOGICAL PATH ASYMMETRY: GRAPH-THEORETIC GAP EMERGENCE")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {args.n_seeds} seeds")
    print(f"  npl={args.npl}, xyz_range={args.xyz_range}, r={args.connect_radius}")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    # Part 1: Diagnostic — is path-count asymmetry spatially structured?
    if not args.skip_diagnostic:
        print("PART 1: PATH-COUNT ASYMMETRY DISTRIBUTION (N=25, seed=3)")
        print()
        positions, adj, bl = generate_3d_dag_uniform(25, args.npl, args.xyz_range, args.connect_radius, 3)
        n = len(positions)
        by_layer = defaultdict(list)
        for idx, (x, y, z) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        bl_idx = len(layers) // 3
        bi = by_layer[layers[bl_idx]]
        cy = sum(positions[i][1] for i in range(n)) / n
        sa = [i for i in bi if positions[i][1] > cy + 3][:3]
        sb = [i for i in bi if positions[i][1] < cy - 3][:3]
        blocked_barrier = set(bi) - set(sa + sb)

        if sa and sb:
            order = _topo_order(adj, n)
            adj_pruned_a = {}
            blocked_a = blocked_barrier | set(sb)
            for i, nbs in adj.items():
                if i not in blocked_a:
                    adj_pruned_a[i] = [j for j in nbs if j not in blocked_a]

            adj_pruned_b = {}
            blocked_b = blocked_barrier | set(sa)
            for i, nbs in adj.items():
                if i not in blocked_b:
                    adj_pruned_b[i] = [j for j in nbs if j not in blocked_b]

            pc_a = compute_path_count(adj_pruned_a, sa, n, order)
            pc_b = compute_path_count(adj_pruned_b, sb, n, order)

            y_bins = defaultdict(list)
            for idx in range(n):
                x, y, z = positions[idx]
                if x > bl:
                    total = pc_a[idx] + pc_b[idx]
                    if total > 0:
                        asym = abs(pc_a[idx] - pc_b[idx]) / total
                    else:
                        asym = 0.0
                    yb = int(y / 3) * 3
                    y_bins[yb].append((asym, pc_a[idx], pc_b[idx]))

            print(f"  {'y_bin':>8s}  {'mean_asym':>10s}  {'mean_pA':>10s}  {'mean_pB':>10s}  {'n':>5s}")
            print(f"  {'-' * 50}")
            for yb in sorted(y_bins.keys()):
                vals = y_bins[yb]
                ma = sum(v[0] for v in vals) / len(vals)
                mpa = sum(v[1] for v in vals) / len(vals)
                mpb = sum(v[2] for v in vals) / len(vals)
                print(f"  {yb:>5d}..{yb+3:<3d}  {ma:10.4f}  {mpa:10.0f}  {mpb:10.0f}  {len(vals):5d}")

            reach_a = compute_reachability(adj_pruned_a, sa, n)
            reach_b = compute_reachability(adj_pruned_b, sb, n)

            n_a_only = len(reach_a - reach_b)
            n_b_only = len(reach_b - reach_a)
            n_both = len(reach_a & reach_b)
            n_neither = n - len(reach_a | reach_b)
            post_barrier = sum(1 for idx, (x, y, z) in enumerate(positions) if x > bl)

            print()
            print(f"  Reachability (post-barrier): A-only={n_a_only}, B-only={n_b_only}, "
                  f"both={n_both}, neither={n_neither}, total={post_barrier}")

    # Part 2: Remove low-asymmetry nodes and measure decoherence
    print()
    print("PART 2: REMOVE LOW-ASYMMETRY NODES (path-count based)")
    print()

    asym_thresholds = [0.0, *args.thresholds]

    for nl in args.n_layers:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'thresh':>7s}  {'pur_cl':>10s}  {'S_norm':>8s}  {'gravity':>10s}  "
              f"{'rem%':>5s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 60}")

        # Baseline
        t0 = time.time()
        pc_all, sn_all, grav_all = [], [], []
        for seed in seeds:
            positions, adj, _ = generate_3d_dag_uniform(nl, args.npl, args.xyz_range, args.connect_radius, seed)
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
            print(f"  {'base':>7s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                  f"{mg:+7.4f}±{seg:.3f}  {'0':>5s}  {len(pc_all):3d}  {dt:4.0f}s")

        for thresh in asym_thresholds:
            if thresh == 0.0:
                continue
            t0 = time.time()
            pc_all, sn_all, grav_all, rem_all = [], [], [], []

            for seed in seeds:
                positions, adj_raw, bl = generate_3d_dag_uniform(nl, args.npl, args.xyz_range, args.connect_radius, seed)
                n = len(positions)

                # Get barrier/slit structure
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers_sorted = sorted(by_layer.keys())
                if len(layers_sorted) < 7:
                    continue
                src = by_layer[layers_sorted[0]]
                det_list = list(by_layer[layers_sorted[-1]])
                cy2 = sum(positions[i][1] for i in range(n)) / n
                bl_idx2 = len(layers_sorted) // 3
                bi2 = by_layer[layers_sorted[bl_idx2]]
                sa2 = [i for i in bi2 if positions[i][1] > cy2 + 3][:3]
                sb2 = [i for i in bi2 if positions[i][1] < cy2 - 3][:3]
                if not sa2 or not sb2:
                    continue
                blocked2 = set(bi2) - set(sa2 + sb2)

                # Compute path counts
                order = _topo_order(adj_raw, n)
                adj_a = {}
                blocked_a = blocked2 | set(sb2)
                for i, nbs in adj_raw.items():
                    if i not in blocked_a:
                        adj_a[i] = [j for j in nbs if j not in blocked_a]
                adj_b = {}
                blocked_b = blocked2 | set(sa2)
                for i, nbs in adj_raw.items():
                    if i not in blocked_b:
                        adj_b[i] = [j for j in nbs if j not in blocked_b]

                pc_a = compute_path_count(adj_a, sa2, n, order)
                pc_b = compute_path_count(adj_b, sb2, n, order)

                # Compute asymmetry and remove low-asymmetry post-barrier nodes
                protected = set(src) | set(det_list) | set(sa2 + sb2)
                removed = set()
                n_post = 0
                for idx in range(n):
                    x, y, z = positions[idx]
                    if x <= bl or idx in protected:
                        continue
                    n_post += 1
                    total = pc_a[idx] + pc_b[idx]
                    if total > 0:
                        asym = abs(pc_a[idx] - pc_b[idx]) / total
                    else:
                        asym = 0.0
                    if asym < thresh:
                        removed.add(idx)

                rem_pct = 100 * len(removed) / max(1, n_post)
                rem_all.append(rem_pct)

                # Rebuild adj
                new_adj = {}
                for i, nbs in adj_raw.items():
                    if i in removed:
                        continue
                    new_nbs = [j for j in nbs if j not in removed]
                    if new_nbs:
                        new_adj[i] = new_nbs

                r = measure(positions, new_adj, nl, K_BAND)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])

            dt = time.time() - t0
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {thresh:7.1f}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {mrem:4.1f}%  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {thresh:7.1f}  FAIL  rem={mrem:.1f}%  {dt:4.0f}s")
            sys.stdout.flush()

        print()

    print("KEY: If path-count asymmetry IS spatially structured:")
    print("  → Removing low-asymmetry nodes creates a gap from graph structure")
    print("  → This would be a TOPOLOGICAL (not amplitude) emergence mechanism")


if __name__ == "__main__":
    main()
