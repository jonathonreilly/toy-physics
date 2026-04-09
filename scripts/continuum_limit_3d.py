#!/usr/bin/env python3
"""Continuum limit study: 3D (d=2 spatial) with increasing node density.

Fix spatial dimension d=2 (3D total). Increase nodes_per_layer while
scaling connect_radius to maintain roughly constant mean degree.

Questions:
  1. Does alpha converge to a fixed value as density → infinity?
  2. Does distance scaling (b-dependence) emerge at high density?

If alpha converges: the model has a proper continuum limit.
If not: alpha is a finite-size artifact.

Mean degree scales roughly as: <k> ~ nodes_per_layer * (r/L)^d
where L = spatial_range, r = connect_radius, d = spatial dim.
To keep <k> constant as N grows, we need r ~ L * (k_target / N)^(1/d).

PStack experiment: continuum-limit-3d
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_3d_modular_dag(n_layers=15, nodes_per_layer=30, yz_range=8.0,
                            connect_radius=3.5, rng_seed=42, gap=5.0,
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


def compute_field(positions, adj, mass_idx, iterations=50):
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


def propagate(positions, adj, field, src, k, blocked=None):
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


def mean_degree(adj, n):
    total = sum(len(nbs) for nbs in adj.values())
    return total / n if n > 0 else 0


def measure_alpha(nodes_per_layer, connect_radius, gap=5.0, n_seeds=16,
                  n_layers=15, yz_range=10.0):
    k_band = [3.0, 5.0, 7.0]
    mass_counts = [1, 2, 4, 6, 8, 12, 16]
    results = []
    degrees = []

    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                yz_range=yz_range, connect_radius=connect_radius,
                rng_seed=seed*17+3, gap=gap,
            )
            if target_n == mass_counts[0] and seed == 0:
                degrees.append(mean_degree(adj, len(positions)))

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
            if not mass_nodes:
                continue

            field = compute_field(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                amps_m = propagate(positions, adj, field, src, k)
                amps_f = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(amps_m, positions, det_list) -
                              centroid_y(amps_f, positions, det_list))
            if shifts:
                per_seed.append((len(mass_nodes), sum(shifts) / len(shifts)))

        if per_seed:
            actual_n = per_seed[0][0]
            vals = [v for _, v in per_seed]
            avg = sum(vals) / len(vals)
            if avg > 0:
                results.append((actual_n, avg))

    alpha = None
    if len(results) >= 3:
        log_n = [math.log(n) for n, _ in results]
        log_s = [math.log(s) for _, s in results]
        n_pts = len(log_n)
        sx, sy = sum(log_n), sum(log_s)
        sxy = sum(x*y for x, y in zip(log_n, log_s))
        sxx = sum(x*x for x in log_n)
        denom = n_pts * sxx - sx * sx
        if abs(denom) > 1e-10:
            alpha = (n_pts * sxy - sx * sy) / denom

    return alpha, degrees[0] if degrees else 0


def measure_b_scaling(nodes_per_layer, connect_radius, gap=5.0, n_seeds=12,
                      n_layers=18, yz_range=12.0):
    """Measure shift vs impact parameter b at given density."""
    k_band = [3.0, 5.0, 7.0]
    b_targets = [1.5, 3.0, 5.0, 7.0, 9.0]
    results = []

    for b in b_targets:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                yz_range=yz_range, connect_radius=connect_radius,
                rng_seed=seed*17+3, gap=gap,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            mass_nodes = [i for i in layer_indices[mid]
                          if abs(positions[i][1] - (cy + b)) < 1.5]
            if len(mass_nodes) < 2:
                continue

            field = compute_field(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                amps_m = propagate(positions, adj, field, src, k)
                amps_f = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(amps_m, positions, det_list) -
                              centroid_y(amps_f, positions, det_list))
            if shifts:
                per_seed.append(sum(shifts) / len(shifts))

        if per_seed:
            avg = sum(per_seed) / len(per_seed)
            results.append((b, avg))

    return results


def main():
    print("=" * 74)
    print("CONTINUUM LIMIT: 3D (d=2 spatial) with increasing node density")
    print("  Fix dimension, sweep nodes_per_layer, scale connect_radius")
    print("=" * 74)
    print()

    # Density sweep configurations
    # Target: mean degree ~ 8-12 for all densities
    # <k> ~ N * pi * r^2 / (2*yz_range)^2 for 2D transverse
    yz_range = 10.0
    configs = [
        # (nodes_per_layer, connect_radius, label)
        (15,  5.0, "sparse"),
        (25,  4.0, "low"),
        (40,  3.2, "medium"),
        (60,  2.7, "high"),
        (80,  2.4, "dense"),
        (120, 2.0, "very dense"),
    ]

    print("TEST 1: Mass scaling alpha vs node density")
    print(f"  {'npl':>5s}  {'radius':>6s}  {'<k>':>6s}  {'alpha':>7s}  {'label':>12s}")
    print(f"  {'-'*42}")

    alphas = []
    for npl, r, label in configs:
        alpha, deg = measure_alpha(npl, r, gap=5.0, n_seeds=16, yz_range=yz_range)
        if alpha is not None:
            alphas.append((npl, alpha))
            print(f"  {npl:5d}  {r:6.1f}  {deg:6.1f}  {alpha:7.3f}  {label:>12s}")
        else:
            print(f"  {npl:5d}  {r:6.1f}  {deg:6.1f}  {'FAIL':>7s}  {label:>12s}")

    print()

    if alphas:
        # Check convergence
        if len(alphas) >= 3:
            last3 = [a for _, a in alphas[-3:]]
            spread = max(last3) - min(last3)
            mean_last3 = sum(last3) / 3
            print(f"  Last 3 alphas: {', '.join(f'{a:.3f}' for a in last3)}")
            print(f"  Spread: {spread:.3f}")
            print(f"  Mean: {mean_last3:.3f}")
            if spread < 0.1:
                print(f"  → CONVERGING to alpha ≈ {mean_last3:.2f}")
            elif spread < 0.2:
                print(f"  → TRENDING toward convergence")
            else:
                print(f"  → NOT YET CONVERGED")
        print()

    # Test 2: Distance scaling at high density
    print("TEST 2: Distance scaling (shift vs b) at different densities")
    print()

    for npl, r, label in [(25, 4.0, "low"), (60, 2.7, "high"), (120, 2.0, "very dense")]:
        results = measure_b_scaling(npl, r, gap=5.0, n_seeds=12, yz_range=yz_range)
        if results:
            print(f"  [{label} (npl={npl})]")
            print(f"  {'b':>5s}  {'shift':>8s}  {'shift*b':>8s}")
            print(f"  {'-'*24}")
            for b, s in results:
                print(f"  {b:5.1f}  {s:+8.4f}  {s*b:+8.3f}")
            # Check if shift*b is constant (1/b scaling)
            products = [s*b for b, s in results if s > 0]
            if len(products) >= 3:
                cv = (max(products) - min(products)) / (sum(products)/len(products)) if sum(products) > 0 else 999
                if cv < 0.3:
                    print(f"  → shift*b ≈ const (CV={cv:.2f}): 1/b scaling EMERGING!")
                else:
                    print(f"  → shift*b varies (CV={cv:.2f}): still b-independent")
            print()

    print("=" * 74)
    print("INTERPRETATION")
    print("  If alpha converges: model has proper continuum limit")
    print("  If shift*b → const at high density: 1/b emerges from finer grid")
    print("=" * 74)


if __name__ == "__main__":
    main()
