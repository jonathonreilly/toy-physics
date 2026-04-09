#!/usr/bin/env python3
"""Sanity check: 3D gravity should vanish at k=0.

If gravity is a pure phase effect, then at k=0 (no phase),
there should be zero deflection. This confirms the signal
isn't an artifact of the graph geometry or field computation.

Also checks: does the directional measure matter?
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


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


def propagate_3d(positions, adj, field, src, k, beta=BETA):
    n = len(positions)
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
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-beta * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    if total < 1e-30:
        return 0.0
    return wy / total


def run_sanity(label, k_values, n_seeds=16, gap=5.0, beta=BETA):
    print(f"  [{label}]")
    print(f"  {'k':>5s}  {'delta':>8s}  {'SE':>6s}  {'t':>5s}  verdict")
    print(f"  {'-'*36}")

    for k in k_values:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=18, nodes_per_layer=35, yz_range=10.0,
                connect_radius=3.5, rng_seed=seed * 17 + 3, gap=gap,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            mass_nodes = [i for i in layer_indices[mid] if positions[i][1] > cy + 1][:8]
            if not mass_nodes:
                continue

            field = compute_field_3d(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            amps_m = propagate_3d(positions, adj, field, src, k, beta=beta)
            amps_f = propagate_3d(positions, adj, free_f, src, k, beta=beta)
            per_seed.append(
                centroid_y(amps_m, positions, det_list) -
                centroid_y(amps_f, positions, det_list)
            )

        if per_seed:
            n_ok = len(per_seed)
            avg = sum(per_seed) / n_ok
            se = math.sqrt(sum((v-avg)**2 for v in per_seed) / n_ok) / math.sqrt(n_ok)
            t = avg / se if se > 1e-10 else 0
            if abs(t) < 1.5:
                v = "ZERO (good)" if k == 0 else "FLAT"
            elif t > 2:
                v = "GRAVITY"
            else:
                v = "WEAK"
            print(f"  {k:5.1f}  {avg:+8.4f}  {se:6.4f}  {t:+5.2f}  {v}")

    print()


def main():
    print("=" * 60)
    print("SANITY CHECK: 3D gravity controls")
    print("=" * 60)
    print()

    # 1. k=0 should give zero deflection
    print("CHECK 1: k=0 → zero deflection (gravity = phase effect)")
    run_sanity("k sweep", [0.0, 1.0, 3.0, 5.0, 7.0, 10.0])

    # 2. Without directional measure (beta=0) — should still work
    print("CHECK 2: no directional measure (beta=0) vs with (beta=0.8)")
    run_sanity("beta=0", [3.0, 5.0, 7.0], beta=0.0)
    run_sanity("beta=0.8", [3.0, 5.0, 7.0], beta=0.8)

    # 3. Reversed field sign → should give repulsion
    print("CHECK 3: field sign (negative field → repulsion?)")
    print("  [Checking via shifted mass placement at y < 0]")

    per_seed_above = []
    per_seed_below = []
    k_band = [3.0, 5.0, 7.0]

    for seed in range(16):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=18, nodes_per_layer=35, yz_range=10.0,
            connect_radius=3.5, rng_seed=seed * 17 + 3, gap=5.0,
        )
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        all_ys = [positions[i][1] for i in range(len(positions))]
        cy = sum(all_ys) / len(all_ys)
        mid = len(layer_indices) // 2

        mass_above = [i for i in layer_indices[mid] if positions[i][1] > cy + 1][:8]
        mass_below = [i for i in layer_indices[mid] if positions[i][1] < cy - 1][:8]

        if not mass_above or not mass_below:
            continue

        free_f = [0.0] * len(positions)

        for k in k_band:
            amps_f = propagate_3d(positions, adj, free_f, src, k)
            y_free = centroid_y(amps_f, positions, det_list)

            field_a = compute_field_3d(positions, adj, mass_above)
            amps_a = propagate_3d(positions, adj, field_a, src, k)
            per_seed_above.append(centroid_y(amps_a, positions, det_list) - y_free)

            field_b = compute_field_3d(positions, adj, mass_below)
            amps_b = propagate_3d(positions, adj, field_b, src, k)
            per_seed_below.append(centroid_y(amps_b, positions, det_list) - y_free)

    for label, data in [("Mass above (y>0)", per_seed_above), ("Mass below (y<0)", per_seed_below)]:
        if data:
            avg = sum(data) / len(data)
            se = math.sqrt(sum((v-avg)**2 for v in data) / len(data)) / math.sqrt(len(data))
            t = avg / se if se > 1e-10 else 0
            print(f"  {label}: delta={avg:+.4f}, SE={se:.4f}, t={t:+.2f}")

    print()
    print("  Mass above → delta > 0 = attraction upward (correct)")
    print("  Mass below → delta < 0 = attraction downward (correct)")
    print()
    print("SANITY CHECKS COMPLETE")


if __name__ == "__main__":
    main()
