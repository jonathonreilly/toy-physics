#!/usr/bin/env python3
"""4D gravity on causal DAGs (3 spatial + 1 causal dimension).

Dimensional progression:
  2D: field ~ log(r), F mass-independent (threshold), deflection ~ const(b)
  3D: field ~ 1/r,    F ~ sqrt(M) (alpha=0.52),      deflection ~ const(b)
  4D: field ~ 1/r²,   F ~ M? (alpha=1.0?),           deflection ~ 1/b?

If 4D gives F~M: the model correctly captures Newtonian gravity
in the appropriate number of spatial dimensions (3).

Tests:
  1. Basic attraction on 4D DAGs (uniform + modular)
  2. Mass scaling: does alpha approach 1.0?
  3. Distance scaling: does b-dependence appear?

PStack experiment: four-d-gravity
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_4d_modular_dag(n_layers=12, nodes_per_layer=25, spatial_range=8.0,
                            connect_radius=4.0, rng_seed=42, gap=3.0,
                            crosslink_prob=0.02):
    """4D causal DAG: layers in x, spatial coords (y, z, w).

    Modular: post-barrier, y is channeled (gap in y), z and w are uniform.
    """
    rng = random.Random(rng_seed)
    positions = []  # (x, y, z, w)
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
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, spatial_range)
                    else:
                        y = rng.uniform(-spatial_range, -gap / 2)
                else:
                    y = rng.uniform(-spatial_range, spatial_range)

                idx = len(positions)
                positions.append((x, y, z, w))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz, pw = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2 + (w-pw)**2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch and dist <= connect_radius:
                                adj[prev_idx].append(idx)
                            elif not same_ch and dist <= 2 * connect_radius and rng.random() < crosslink_prob:
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
            dy, dz, dw = y2-y1, z2-z1, w2-w1
            L = math.sqrt(dx*dx + dy*dy + dz*dz + dw*dw)
            if L < 1e-10:
                continue
            # Directional: angle from forward (x-axis) in 4D
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * weight / L
            amps[j] += amps[i] * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def test_attraction(gap, n_layers_list, n_seeds=16):
    k_band = [3.0, 5.0, 7.0]
    label = f"4D Modular gap={gap}" if gap > 0 else "4D Uniform"
    print(f"  [{label}]")
    print(f"  {'N':>4s}  {'delta':>8s}  {'SE':>6s}  {'t':>5s}  {'n':>3s}  verdict")
    print(f"  {'-'*38}")

    for nl in n_layers_list:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=nl, nodes_per_layer=25, spatial_range=8.0,
                connect_radius=4.5, rng_seed=seed*13+5, gap=gap,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            grav_idx = 2 * len(layer_indices) // 3
            mass_nodes = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1][:8]
            if not mass_nodes:
                continue

            field = compute_field_4d(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            deltas = []
            for k in k_band:
                amps_m = propagate_4d(positions, adj, field, src, k)
                amps_f = propagate_4d(positions, adj, free_f, src, k)
                deltas.append(centroid_y(amps_m, positions, det_list) -
                              centroid_y(amps_f, positions, det_list))
            if deltas:
                per_seed.append(sum(deltas) / len(deltas))

        if per_seed:
            n_ok = len(per_seed)
            avg = sum(per_seed) / n_ok
            se = math.sqrt(sum((d-avg)**2 for d in per_seed) / n_ok) / math.sqrt(n_ok)
            t = avg / se if se > 1e-10 else 0
            v = "GRAVITY" if avg > 0 and t > 2 else "WEAK" if avg > 0 else "FLAT"
            print(f"  {nl:4d}  {avg:+8.4f}  {se:6.4f}  {t:+5.2f}  {n_ok:3d}  {v}")
        else:
            print(f"  {nl:4d}  FAIL")
    print()


def test_mass_scaling(gap, n_seeds=24):
    k_band = [3.0, 5.0, 7.0]
    nl = 15
    mass_counts = [1, 2, 3, 4, 6, 8, 10, 12, 16]

    label = f"4D Modular gap={gap}" if gap > 0 else "4D Uniform"
    print(f"  [{label}] — {n_seeds} seeds, N={nl}")
    print(f"  {'n_mass':>6s}  {'shift':>8s}  {'SE':>6s}  {'t':>5s}  "
          f"{'shift/n':>8s}  {'shift/sqrt(n)':>13s}")
    print(f"  {'-'*55}")

    results = []
    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=nl, nodes_per_layer=30, spatial_range=8.0,
                connect_radius=4.5, rng_seed=seed*17+3, gap=gap,
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
            if not mass_nodes:
                continue

            field = compute_field_4d(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                amps_m = propagate_4d(positions, adj, field, src, k)
                amps_f = propagate_4d(positions, adj, free_f, src, k)
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
            per_m = avg / actual_n if actual_n > 0 else 0
            per_sq = avg / math.sqrt(actual_n) if actual_n > 0 else 0
            print(f"  {actual_n:6d}  {avg:+8.4f}  {se:6.4f}  {t:+5.2f}  "
                  f"{per_m:+8.4f}  {per_sq:+13.4f}")
            if avg > 0:
                results.append((actual_n, avg))

    # Power law fit
    if len(results) >= 3:
        log_n = [math.log(n) for n, _ in results]
        log_s = [math.log(s) for _, s in results]
        n_pts = len(log_n)
        sx = sum(log_n)
        sy = sum(log_s)
        sxy = sum(x*y for x, y in zip(log_n, log_s))
        sxx = sum(x*x for x in log_n)
        denom = n_pts * sxx - sx * sx
        if abs(denom) > 1e-10:
            alpha = (n_pts * sxy - sx * sy) / denom
            print(f"\n  Power law: shift ~ n^{alpha:.3f}")
            print(f"    2D: alpha ≈ 0 (threshold)")
            print(f"    3D: alpha ≈ 0.5 (sqrt(M))")
            print(f"    4D: alpha = {alpha:.3f} {'→ F~M!' if alpha > 0.8 else '→ sub-linear'}")
    print()


def test_k0_sanity(gap=3.0):
    """k=0 should give zero deflection."""
    positions, adj, layer_indices = generate_4d_modular_dag(
        n_layers=15, nodes_per_layer=25, spatial_range=8.0,
        connect_radius=4.5, rng_seed=42, gap=gap,
    )
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)
    grav_idx = 2 * len(layer_indices) // 3
    mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1][:8]
    field = compute_field_4d(positions, adj, mass)
    free_f = [0.0] * len(positions)

    amps_m = propagate_4d(positions, adj, field, src, 0.0)
    amps_f = propagate_4d(positions, adj, free_f, src, 0.0)
    d0 = centroid_y(amps_m, positions, det_list) - centroid_y(amps_f, positions, det_list)
    print(f"  k=0 sanity: delta = {d0:+.6e} (should be ~0)")


def main():
    print("=" * 74)
    print("4D GRAVITY ON CAUSAL DAGs (3 spatial + 1 causal)")
    print("  Does 4D give F~M (Newtonian mass scaling)?")
    print("  Dimensional progression: 2D→threshold, 3D→sqrt(M), 4D→?")
    print("=" * 74)
    print()

    # Sanity
    print("SANITY CHECK:")
    test_k0_sanity()
    print()

    # Test 1: Attraction
    print("TEST 1: Gravitational attraction")
    print()
    test_attraction(0.0, [10, 12, 15, 18], n_seeds=16)
    test_attraction(3.0, [10, 12, 15, 18], n_seeds=16)

    # Test 2: Mass scaling
    print("TEST 2: Mass scaling")
    print()
    test_mass_scaling(0.0, n_seeds=24)
    test_mass_scaling(3.0, n_seeds=24)
    test_mass_scaling(5.0, n_seeds=24)

    print("=" * 74)
    print("DIMENSIONAL PROGRESSION:")
    print("  2D: alpha ≈ 0.0 (mass-independent threshold)")
    print("  3D: alpha ≈ 0.5 (F ~ sqrt(M))")
    print("  4D: alpha = ??? (F ~ M if alpha ≈ 1.0)")
    print("=" * 74)


if __name__ == "__main__":
    main()
