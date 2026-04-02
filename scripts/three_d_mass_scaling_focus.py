#!/usr/bin/env python3
"""Focused mass scaling test in 3D modular DAGs.

The main experiment showed shift growing with n_mass on modular 3D DAGs,
but shift/n wasn't perfectly constant. This follow-up uses 24 seeds
and a wider mass range to determine whether F~M or threshold.

Also tests: does the 3D modular DAG give F~M while 2D doesn't?
This would be the first dimensionality-dependent physics result.

PStack experiment: three-d-mass-scaling-focus
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


def propagate_3d(positions, adj, field, src, k):
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
            w = math.exp(-BETA * theta * theta)
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


def run_mass_scaling(gap, n_seeds=24):
    k_band = [3.0, 5.0, 7.0]
    n_layers = 18
    mass_counts = [1, 2, 3, 4, 6, 8, 10, 12, 16, 20]

    label = f"3D Modular gap={gap}" if gap > 0 else "3D Uniform (gap=0)"
    print(f"  [{label}] — {n_seeds} seeds, N={n_layers}")
    print(f"  {'n_mass':>6s}  {'shift':>8s}  {'SE':>6s}  {'t':>5s}  "
          f"{'shift/n':>8s}  {'shift/sqrt(n)':>13s}  {'n_ok':>4s}")
    print(f"  {'-'*62}")

    results = []
    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=n_layers, nodes_per_layer=35, yz_range=10.0,
                connect_radius=3.5, rng_seed=seed * 17 + 3, gap=gap,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)

            mid = len(layer_indices) // 2
            candidates = sorted(
                [i for i in layer_indices[mid] if positions[i][1] > cy + 1],
                key=lambda i: -positions[i][1]
            )
            mass_nodes = candidates[:target_n]
            if len(mass_nodes) < 1:
                continue

            field = compute_field_3d(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                amps_m = propagate_3d(positions, adj, field, src, k)
                amps_f = propagate_3d(positions, adj, free_f, src, k)
                shifts.append(centroid_y(amps_m, positions, det_list) -
                              centroid_y(amps_f, positions, det_list))

            if shifts:
                per_seed.append((len(mass_nodes), sum(shifts) / len(shifts)))

        if per_seed:
            n_ok = len(per_seed)
            actual_n = per_seed[0][0]
            vals = [v for _, v in per_seed]
            avg = sum(vals) / n_ok
            se = math.sqrt(sum((v-avg)**2 for v in vals) / n_ok) / math.sqrt(n_ok)
            t = avg / se if se > 1e-10 else 0
            per_mass = avg / actual_n if actual_n > 0 else 0
            per_sqrt = avg / math.sqrt(actual_n) if actual_n > 0 else 0
            print(f"  {actual_n:6d}  {avg:+8.4f}  {se:6.4f}  {t:+5.2f}  "
                  f"{per_mass:+8.4f}  {per_sqrt:+13.4f}  {n_ok:4d}")
            results.append((actual_n, avg, se))
        else:
            print(f"  {target_n:6d}  FAIL")

    print()

    # Fit power law: shift = a * n^alpha (log-log linear regression)
    positive = [(r[0], r[1]) for r in results if r[0] > 0 and r[1] > 0]
    if len(positive) >= 3:
        log_n = [math.log(n) for n, _ in positive]
        log_s = [math.log(s) for _, s in positive]
        n_pts = len(log_n)
        sum_x = sum(log_n)
        sum_y = sum(log_s)
        sum_xy = sum(x*y for x, y in zip(log_n, log_s))
        sum_xx = sum(x*x for x in log_n)
        denom = n_pts * sum_xx - sum_x * sum_x
        if abs(denom) > 1e-10:
            alpha = (n_pts * sum_xy - sum_x * sum_y) / denom
            print(f"  Power law fit: shift ~ n^{alpha:.3f}")
            print(f"    alpha=1.0 → F~M, alpha=0.5 → F~sqrt(M), alpha=0 → threshold")
            print()

    return results


def main():
    print("=" * 74)
    print("3D MASS SCALING: Focused test with 24 seeds")
    print("  Does F scale with M in 3D? (2D has threshold / mass-independent)")
    print("=" * 74)
    print()

    # Test modular DAGs at several gap values
    for gap in [0.0, 3.0, 5.0]:
        run_mass_scaling(gap, n_seeds=24)

    print("=" * 74)
    print("INTERPRETATION")
    print("  alpha ≈ 1.0: F ~ M (Newtonian)")
    print("  alpha ≈ 0.5: F ~ sqrt(M) (sub-linear but present)")
    print("  alpha ≈ 0.0: mass-independent threshold (like 2D)")
    print("  This would be the FIRST dimensionality-dependent result")
    print("  in the model if 3D differs from 2D.")
    print("=" * 74)


if __name__ == "__main__":
    main()
