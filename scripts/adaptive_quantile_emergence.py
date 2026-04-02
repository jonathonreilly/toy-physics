#!/usr/bin/env python3
"""Adaptive quantile pruning: prune bottom X% of D distribution per iteration.

The fixed-threshold self-regulation (d_min=0.1) fails at large N because
CLT narrows the D distribution — a fixed threshold catches too many nodes
at N=80, destroying the graph.

Fix: instead of a fixed threshold, always prune the bottom quantile of the
D distribution. This adapts to the distribution shape at each N, removing
a fixed FRACTION of the least-distinguishable nodes regardless of how
narrow the distribution gets.

Also tests: does the quantile rule produce a SCALING gap (gap ~ const
or gap ~ N) or a collapsing gap (gap ~ 1/N)?

PStack experiment: adaptive-quantile-emergence
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8
LAM = 10.0


def generate_3d_uniform_dag(n_layers=20, nodes_per_layer=30, yz_range=10.0,
                            connect_radius=3.5, rng_seed=42):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
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
    return positions, dict(adj), layer_indices


def propagate_3d(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def compute_field_3d(positions, adj, mass_ids, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_ids)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0] * n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def adaptive_quantile_prune(positions, adj, layer_indices, quantile=0.15,
                            max_iter=3):
    """Prune the bottom `quantile` fraction of post-barrier D distribution.

    Unlike fixed d_min, this adapts to the distribution width at each N.
    """
    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3

    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)

    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return adj, 0

    slit_set = set(slit_a + slit_b)
    base_blocked = set(barrier) - slit_set
    blocked_a = base_blocked | set(slit_b)
    blocked_b = base_blocked | set(slit_a)
    det_set = set(layer_indices[-1])
    field = [0.0] * n

    current_adj = dict(adj)
    total_removed = 0

    for iteration in range(max_iter):
        amps_a = propagate_3d(positions, current_adj, field,
                              layer_indices[0], 5.0, blocked_a)
        amps_b = propagate_3d(positions, current_adj, field,
                              layer_indices[0], 5.0, blocked_b)

        # Compute D at all surviving post-barrier nodes
        node_d = []
        for li in range(bl_idx + 1, n_layers - 1):
            for i in layer_indices[li]:
                if i in det_set:
                    continue
                # Check node is still in the graph
                if i not in current_adj and not any(i in nbs for nbs in current_adj.values()):
                    continue
                pa = abs(amps_a[i])**2
                pb = abs(amps_b[i])**2
                total = pa + pb
                D = abs(pa - pb) / total if total > 1e-30 else 0.0
                node_d.append((i, D))

        if not node_d:
            break

        # Sort by D, find quantile threshold
        node_d.sort(key=lambda x: x[1])
        n_to_remove = max(1, int(len(node_d) * quantile))
        remove_set = set(idx for idx, _ in node_d[:n_to_remove])

        new_adj = {}
        for i, nbs in current_adj.items():
            if i in remove_set:
                continue
            filtered = [j for j in nbs if j not in remove_set]
            if filtered:
                new_adj[i] = filtered

        total_removed += len(remove_set)
        current_adj = new_adj

    return current_adj, total_removed


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0
    y_min, y_max = min(ys)-0.01, max(ys)+0.01
    bw = (y_max - y_min) / N_YBINS
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS-1, int((positions[m][1] - y_min) / bw)))
        ba[b] += amps_a[m]
        bb[b] += amps_b[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S / d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (amps_a[d1]*amps_a[d2].conjugate() +
                             amps_b[d1]*amps_b[d2].conjugate() +
                             D * amps_a[d1]*amps_b[d2].conjugate() +
                             D * amps_b[d1]*amps_a[d2].conjugate())
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def measure_decoherence(positions, adj, layer_indices):
    k_band = [3.0, 5.0, 7.0]
    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    if not det_list or n_layers < 7:
        return math.nan
    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return math.nan
    blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = blocked | set(slit_b)
    blocked_b = blocked | set(slit_a)
    bath_mass = []
    for li in range(bl_idx+1, min(n_layers, bl_idx+3)):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= 3:
                bath_mass.append(i)
    grav_idx = 2 * n_layers // 3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1]
    all_mass = list(set(bath_mass) | set(grav_mass))
    field = compute_field_3d(positions, adj, all_mass) if all_mass else [0.0]*n
    mid_nodes = [i for li in range(bl_idx+1, n_layers-1)
                 for i in layer_indices[li]
                 if i not in blocked and i not in set(det_list)]
    if len(mid_nodes) < 4:
        return math.nan
    pur_list = []
    for k in k_band:
        aa = propagate_3d(positions, adj, field, src, k, blocked_a)
        ab = propagate_3d(positions, adj, field, src, k, blocked_b)
        Sn = cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM**2 * Sn)
        pur = cl_purity(aa, ab, D, det_list)
        if not math.isnan(pur):
            pur_list.append(pur)
    return sum(pur_list)/len(pur_list) if pur_list else math.nan


def gap_metric(positions, adj, layer_indices):
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    det_set = set(layer_indices[-1])
    ys = []
    for li in range(bl_idx+1, n_layers-1):
        for i in layer_indices[li]:
            if i in det_set:
                continue
            if i in adj or any(i in nbs for nbs in adj.values()):
                ys.append(positions[i][1])
    if len(ys) < 10:
        return 0.0
    ys.sort()
    return max(ys[i] - ys[i-1] for i in range(1, len(ys)))


def main():
    n_seeds = 16

    print("=" * 74)
    print("ADAPTIVE QUANTILE PRUNING: scales with CLT narrowing")
    print("  Always prune bottom X% of D distribution (not fixed threshold)")
    print("=" * 74)
    print()

    n_layers_list = [20, 25, 30, 40, 50, 60, 80]

    for quantile in [0.0, 0.10, 0.15, 0.20]:
        label = "Uniform baseline" if quantile == 0 else f"Adaptive q={quantile}"
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_cl':>8s}  {'gap':>6s}  {'removed':>8s}  {'n':>3s}")
        print(f"  {'-'*36}")

        for nl in n_layers_list:
            purs = []
            gaps = []
            removals = []

            for seed in range(n_seeds):
                positions, adj_orig, layer_indices = generate_3d_uniform_dag(
                    n_layers=nl, nodes_per_layer=30, yz_range=10.0,
                    connect_radius=3.5, rng_seed=seed*13+5)

                if quantile > 0:
                    adj_e, removed = adaptive_quantile_prune(
                        positions, adj_orig, layer_indices,
                        quantile=quantile, max_iter=3)
                    removals.append(removed)
                else:
                    adj_e = adj_orig
                    removals.append(0)

                pur = measure_decoherence(positions, adj_e, layer_indices)
                if not math.isnan(pur):
                    purs.append(pur)
                    gaps.append(gap_metric(positions, adj_e, layer_indices))

            if purs:
                mp = sum(purs) / len(purs)
                mg = sum(gaps) / len(gaps) if gaps else 0
                mr = sum(removals) / len(removals)
                print(f"  {nl:4d}  {mp:8.4f}  {mg:6.2f}  {mr:8.1f}  {len(purs):3d}")
            else:
                print(f"  {nl:4d}  FAIL")

        print()

    print("=" * 74)
    print("KEY: does adaptive quantile maintain the improvement at N=60-80?")
    print("  Fixed threshold died at N=60 (over-pruning)")
    print("  Adaptive should prune fewer nodes at large N (narrower D dist)")
    print("=" * 74)


if __name__ == "__main__":
    main()
