#!/usr/bin/env python3
"""3D large-N confirmation: decoherence + gravity through N=100.

Confirms:
  1. Decoherence doesn't ceiling at N=100 on 3D modular gap=3
  2. Gravity signal persists at N=60-100
  3. Both coexist at large N

Uses 24 seeds for robust statistics.

PStack experiment: three-d-large-n-confirm
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8
LAM = 10.0


def generate_3d_modular_dag(n_layers=15, nodes_per_layer=30, yz_range=8.0,
                            connect_radius=3.5, rng_seed=42, gap=3.0,
                            crosslink_prob=0.02):
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
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)
                if use_channels and layer > barrier_layer:
                    y = rng.uniform(gap/2, yz_range) if node_i < nodes_per_layer//2 else rng.uniform(-yz_range, -gap/2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch and dist <= connect_radius:
                                adj[prev_idx].append(idx)
                            elif not same_ch and dist <= 2*connect_radius and rng.random() < crosslink_prob:
                                adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def compute_field_3d(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_idx)
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


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0, 0.0
    y_min, y_max = min(ys) - 0.01, max(ys) + 0.01
    bw = (y_max - y_min) / N_YBINS
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS-1, int((positions[m][1] - y_min) / bw)))
        ba[b] += amps_a[m]
        bb[b] += amps_b[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S, S/d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            aa = amps_a[d1] * amps_a[d2].conjugate()
            bb = amps_b[d1] * amps_b[d2].conjugate()
            ab = amps_a[d1] * amps_b[d2].conjugate()
            ba = amps_b[d1] * amps_a[d2].conjugate()
            rho[(d1, d2)] = aa + bb + D * ab + D * ba
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def main():
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 24
    gap = 3.0

    print("=" * 78)
    print("3D LARGE-N CONFIRMATION: gap=3, 24 seeds")
    print("  Gravity + Decoherence through N=100")
    print("=" * 78)
    print()

    n_layers_list = [20, 30, 40, 50, 60, 80, 100]

    print(f"  {'N':>4s}  {'grav_d':>8s}  {'grav_SE':>8s}  {'grav_t':>7s}  "
          f"{'pur_cl':>8s}  {'pur_min':>8s}  {'S_norm':>8s}  {'decoh':>8s}  "
          f"{'nodes':>6s}")
    print(f"  {'-'*80}")

    for nl in n_layers_list:
        grav_per_seed = []
        pur_list = []
        min_list = []
        s_list = []
        node_counts = []

        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=nl, nodes_per_layer=30, yz_range=10.0,
                connect_radius=3.5, rng_seed=seed*13+5, gap=gap,
            )
            node_counts.append(len(positions))

            n_actual = len(layer_indices)
            bl_idx = n_actual // 3
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list or n_actual < 7:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)

            # Barrier + slits
            barrier = layer_indices[bl_idx]
            slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
            slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
            if not slit_a or not slit_b:
                continue
            slit_set = set(slit_a + slit_b)
            blocked = set(barrier) - slit_set
            blocked_a = blocked | set(slit_b)
            blocked_b = blocked | set(slit_a)

            # Gravity mass
            grav_idx = 2 * n_actual // 3
            grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1][:8]

            # CL bath mass
            bath_mass = []
            for li in range(bl_idx+1, min(n_actual, bl_idx+3)):
                for i in layer_indices[li]:
                    if abs(positions[i][1] - cy) <= 3:
                        bath_mass.append(i)

            all_mass = set(bath_mass) | set(grav_mass)
            field = compute_field_3d(positions, adj, list(all_mass)) if all_mass else [0.0] * len(positions)
            free_field = [0.0] * len(positions)

            mid_nodes = [i for li in range(bl_idx+1, n_actual-1)
                         for i in layer_indices[li]
                         if i not in blocked and i not in set(det_list)]

            if len(mid_nodes) < 4:
                continue

            seed_grav = []
            for k in k_band:
                # Gravity
                amps_w = propagate_3d(positions, adj, field, src, k)
                amps_f = propagate_3d(positions, adj, free_field, src, k)
                seed_grav.append(centroid_y(amps_w, positions, det_list) -
                                 centroid_y(amps_f, positions, det_list))

                # Decoherence
                amps_a = propagate_3d(positions, adj, field, src, k, blocked_a)
                amps_b = propagate_3d(positions, adj, field, src, k, blocked_b)
                _, Sn = cl_contrast(amps_a, amps_b, mid_nodes, positions)
                D = math.exp(-LAM**2 * Sn)
                pur = cl_purity(amps_a, amps_b, D, det_list)
                pur_m = cl_purity(amps_a, amps_b, 0.0, det_list)
                if not math.isnan(pur):
                    pur_list.append(pur)
                    min_list.append(pur_m)
                    s_list.append(Sn)

            if seed_grav:
                grav_per_seed.append(sum(seed_grav) / len(seed_grav))

        if grav_per_seed and pur_list:
            ng = len(grav_per_seed)
            gd = sum(grav_per_seed) / ng
            gse = math.sqrt(sum((d-gd)**2 for d in grav_per_seed) / ng) / math.sqrt(ng)
            gt = gd / gse if gse > 1e-10 else 0

            mp = sum(pur_list) / len(pur_list)
            mm = sum(min_list) / len(min_list)
            ms = sum(s_list) / len(s_list)
            mn = int(sum(node_counts) / len(node_counts))

            print(f"  {nl:4d}  {gd:+8.4f}  {gse:8.4f}  {gt:+7.2f}  "
                  f"{mp:8.4f}  {mm:8.4f}  {ms:8.5f}  {1-mp:+8.4f}  "
                  f"{mn:6d}")
        else:
            print(f"  {nl:4d}  FAIL")

    print()
    print("=" * 78)
    print("COMPARISON WITH 2D (24 seeds, modular gap=3):")
    print("  2D N=40: pur_min=0.938, gravity=+1.83")
    print("  2D N=60: pur_min=0.968 (ceiling returning)")
    print("  2D N=80: pur_min=0.987 (strong ceiling)")
    print()
    print("  3D ceiling threshold: pur_cl > 0.97 at any N → ceiling")
    print("  3D no-ceiling: pur_cl stays < 0.97 through N=100")
    print("=" * 78)


if __name__ == "__main__":
    main()
