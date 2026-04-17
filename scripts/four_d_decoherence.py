#!/usr/bin/env python3
"""4D decoherence: does the extra dimension further delay the CLT ceiling?

3D delayed the 2D ceiling by ~2x in N. Does 4D extend this further?

PStack experiment: four-d-decoherence
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8
LAM = 10.0


def generate_4d_modular_dag(n_layers=12, nodes_per_layer=25, spatial_range=8.0,
                            connect_radius=4.5, rng_seed=42, gap=3.0,
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
            positions.append((x, 0.0, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-spatial_range, spatial_range)
                w = rng.uniform(-spatial_range, spatial_range)
                if use_channels and layer > barrier_layer:
                    y = rng.uniform(gap/2, spatial_range) if node_i < nodes_per_layer//2 else rng.uniform(-spatial_range, -gap/2)
                else:
                    y = rng.uniform(-spatial_range, spatial_range)
                idx = len(positions)
                positions.append((x, y, z, w))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        px, py, pz, pw = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2 + (w-pw)**2)
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


def compute_field_4d(positions, adj, mass_idx, iterations=50):
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


def propagate_4d(positions, adj, field, src, k, blocked=None):
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
            x1, y1, z1, w1 = positions[i]
            x2, y2, z2, w2 = positions[j]
            dx = x2-x1
            L = math.sqrt(dx*dx + (y2-y1)**2 + (z2-z1)**2 + (w2-w1)**2)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx/L, -1), 1))
            wt = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * wt / L
            amps[j] += amps[i] * ea
    return amps


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0, 0.0
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
    return S, S/d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            aa = amps_a[d1] * amps_a[d2].conjugate()
            bb = amps_b[d1] * amps_b[d2].conjugate()
            ab = amps_a[d1] * amps_b[d2].conjugate()
            ba_ = amps_b[d1] * amps_a[d2].conjugate()
            rho[(d1, d2)] = aa + bb + D * ab + D * ba_
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def main():
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16

    print("=" * 70)
    print("4D DECOHERENCE: CL bath scaling")
    print("  Does 4D further delay the CLT ceiling?")
    print("=" * 70)
    print()

    n_layers_list = [10, 12, 15, 18, 20, 25, 30]

    for gap in [0.0, 3.0, 5.0]:
        label = f"4D Modular gap={gap}" if gap > 0 else "4D Uniform"
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'S_norm':>8s}  {'pur_cl':>8s}  {'pur_min':>8s}  "
              f"{'decoh':>8s}  {'n_ok':>4s}")
        print(f"  {'-'*48}")

        for nl in n_layers_list:
            pur_list = []
            min_list = []
            s_list = []

            for seed in range(n_seeds):
                positions, adj, layer_indices = generate_4d_modular_dag(
                    n_layers=nl, nodes_per_layer=25, spatial_range=8.0,
                    connect_radius=4.5, rng_seed=seed*13+5, gap=gap,
                )

                n_actual = len(layer_indices)
                bl_idx = n_actual // 3
                src = layer_indices[0]
                det_list = list(layer_indices[-1])
                if not det_list or n_actual < 5:
                    continue

                all_ys = [positions[i][1] for i in range(len(positions))]
                cy = sum(all_ys) / len(all_ys)

                barrier = layer_indices[bl_idx]
                slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
                slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
                if not slit_a or not slit_b:
                    continue
                blocked = set(barrier) - set(slit_a + slit_b)
                blocked_a = blocked | set(slit_b)
                blocked_b = blocked | set(slit_a)

                bath_mass = []
                for li in range(bl_idx+1, min(n_actual, bl_idx+3)):
                    for i in layer_indices[li]:
                        if abs(positions[i][1] - cy) <= 3:
                            bath_mass.append(i)
                grav_idx = 2 * n_actual // 3
                grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1]
                all_mass = set(bath_mass) | set(grav_mass)
                field = compute_field_4d(positions, adj, list(all_mass)) if all_mass else [0.0]*len(positions)

                mid_nodes = [i for li in range(bl_idx+1, n_actual-1)
                             for i in layer_indices[li]
                             if i not in blocked and i not in set(det_list)]
                if len(mid_nodes) < 4:
                    continue

                for k in k_band:
                    amps_a = propagate_4d(positions, adj, field, src, k, blocked_a)
                    amps_b = propagate_4d(positions, adj, field, src, k, blocked_b)
                    _, Sn = cl_contrast(amps_a, amps_b, mid_nodes, positions)
                    D = math.exp(-LAM**2 * Sn)
                    pur = cl_purity(amps_a, amps_b, D, det_list)
                    pur_m = cl_purity(amps_a, amps_b, 0.0, det_list)
                    if not math.isnan(pur):
                        pur_list.append(pur)
                        min_list.append(pur_m)
                        s_list.append(Sn)

            if pur_list:
                mp = sum(pur_list) / len(pur_list)
                mm = sum(min_list) / len(min_list)
                ms = sum(s_list) / len(s_list)
                print(f"  {nl:4d}  {ms:8.5f}  {mp:8.4f}  {mm:8.4f}  "
                      f"{1-mp:+8.4f}  {len(pur_list):4d}")
            else:
                print(f"  {nl:4d}  FAIL")

        print()

    print("=" * 70)
    print("COMPARISON:")
    print("  2D N=80: pur_min = 0.987 (strong ceiling)")
    print("  3D N=80: pur_cl  = 0.955 (delayed ceiling)")
    print("  4D: does the ceiling delay further?")
    print("=" * 70)


if __name__ == "__main__":
    main()
