#!/usr/bin/env python3
"""3D decoherence at large N: does the CLT ceiling survive in 3D?

The initial 3D test showed S_norm staying bounded (0.07-0.30) through N=40,
and pur_cl reaching 0.925 on modular gap=5. The 2D model died at N=80+.

This test pushes to N=60, 80, 100 to see if 3D breaks the ceiling.

PStack experiment: three-d-decoherence-large-n
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8


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
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, yz_range)
                    else:
                        y = rng.uniform(-yz_range, -gap / 2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_channel = (y * py > 0)
                            if same_channel:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                                    adj[prev_idx].append(idx)
                        else:
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
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
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


def cl_bath_contrast_3d(amps_a, amps_b, mid_nodes, positions, n_bins=N_YBINS):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0, 0.0
    y_min = min(ys) - 0.01
    y_max = max(ys) + 0.01
    bin_width = (y_max - y_min) / n_bins
    bins_a = [0j] * n_bins
    bins_b = [0j] * n_bins
    for m in mid_nodes:
        y = positions[m][1]
        b = int((y - y_min) / bin_width)
        b = max(0, min(n_bins - 1, b))
        bins_a[b] += amps_a[m]
        bins_b[b] += amps_b[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
    N_A = sum(abs(a) ** 2 for a in bins_a)
    N_B = sum(abs(b) ** 2 for b in bins_b)
    denom = N_A + N_B
    return S, S / denom if denom > 0 else 0.0


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
    return sum(abs(v) ** 2 for v in rho.values()).real


def setup_slit_3d(positions, adj, layer_indices, slit_sep=3.0):
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    if not det_list:
        return None
    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)
    barrier_nodes = layer_indices[bl_idx]
    slit_a = [i for i in barrier_nodes if positions[i][1] > cy + slit_sep][:5]
    slit_b = [i for i in barrier_nodes if positions[i][1] < cy - slit_sep][:5]
    if not slit_a or not slit_b:
        return None
    slit_set = set(slit_a + slit_b)
    blocked = set(barrier_nodes) - slit_set
    mass_nodes = []
    for li in range(bl_idx + 1, min(n_layers, bl_idx + 3)):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= slit_sep:
                mass_nodes.append(i)
    grav_idx = 2 * n_layers // 3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1]
    all_mass = set(mass_nodes) | set(grav_mass)
    field = compute_field_3d(positions, adj, list(all_mass)) if all_mass else [0.0] * len(positions)
    mid_nodes = []
    for li in range(bl_idx + 1, n_layers - 1):
        for i in layer_indices[li]:
            if i not in blocked and i not in set(det_list):
                mid_nodes.append(i)
    return {
        "src": src, "det_list": det_list, "blocked": blocked,
        "slit_a": slit_a, "slit_b": slit_b, "mid_nodes": mid_nodes,
        "field": field, "cy": cy,
    }


def main():
    k_band = [3.0, 5.0, 7.0]
    lam = 10.0  # use strong coupling to saturate

    print("=" * 74)
    print("3D DECOHERENCE: Large-N scaling test")
    print(f"  lambda={lam}, 16 seeds, k-band=[3,5,7]")
    print("  Does the CLT ceiling survive in 3D?")
    print("=" * 74)
    print()

    n_layers_list = [15, 20, 25, 30, 40, 50, 60, 80]

    for gap in [0.0, 3.0, 5.0]:
        label = f"3D Modular gap={gap}" if gap > 0 else "3D Uniform (gap=0)"
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'S_norm':>8s}  {'pur_cl':>8s}  {'pur_min':>8s}  "
              f"{'decoh':>8s}  {'n_ok':>4s}  {'nodes':>6s}")
        print(f"  {'-'*56}")

        for nl in n_layers_list:
            pur_list = []
            min_list = []
            s_list = []
            node_counts = []

            for seed in range(16):
                positions, adj, layer_indices = generate_3d_modular_dag(
                    n_layers=nl, nodes_per_layer=30, yz_range=10.0,
                    connect_radius=3.5, rng_seed=seed * 13 + 5, gap=gap,
                )

                setup = setup_slit_3d(positions, adj, layer_indices)
                if setup is None:
                    continue

                blocked_a = setup["blocked"] | set(setup["slit_b"])
                blocked_b = setup["blocked"] | set(setup["slit_a"])
                mid_nodes = setup["mid_nodes"]

                if len(mid_nodes) < 4 or len(setup["det_list"]) < 3:
                    continue

                node_counts.append(len(positions))

                for k in k_band:
                    amps_a = propagate_3d(positions, adj, setup["field"],
                                          setup["src"], k, blocked_a)
                    amps_b = propagate_3d(positions, adj, setup["field"],
                                          setup["src"], k, blocked_b)

                    _, S_norm = cl_bath_contrast_3d(
                        amps_a, amps_b, mid_nodes, positions)
                    D = math.exp(-lam**2 * S_norm)

                    pur = cl_purity(amps_a, amps_b, D, setup["det_list"])
                    pur_min = cl_purity(amps_a, amps_b, 0.0, setup["det_list"])

                    if not math.isnan(pur) and not math.isnan(pur_min):
                        pur_list.append(pur)
                        min_list.append(pur_min)
                        s_list.append(S_norm)

            if pur_list:
                mp = sum(pur_list) / len(pur_list)
                mm = sum(min_list) / len(min_list)
                ms = sum(s_list) / len(s_list)
                mn = int(sum(node_counts) / len(node_counts)) if node_counts else 0
                n_ok = len(pur_list)
                print(f"  {nl:4d}  {ms:8.5f}  {mp:8.4f}  {mm:8.4f}  "
                      f"{1-mp:+8.4f}  {n_ok:4d}  {mn:6d}")
            else:
                print(f"  {nl:4d}  FAIL")

        print()

    print("=" * 74)
    print("COMPARISON WITH 2D:")
    print("  2D at N=80: pur_min = 0.987 (uniform), 0.982 (removal)")
    print("  2D ceiling: pur_min → 1 at large N on ALL topologies")
    print()
    print("  If 3D at N=80: pur_cl < 0.97 → 3D breaks the ceiling")
    print("  If 3D at N=80: pur_cl > 0.98 → same CLT problem")
    print("=" * 74)


if __name__ == "__main__":
    main()
