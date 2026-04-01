#!/usr/bin/env python3
"""4D continuum-limit study on the retained modular lane.

Question:
  Does the 4D mass-scaling exponent alpha converge as graph density increases,
  or does it remain parameter-sensitive across density?

Science scope:
  - Stay on the retained 4D modular lane (gap=5)
  - Sweep density by increasing nodes_per_layer and connect_radius together
  - Report nodes_per_layer, connect_radius, mean degree, and fitted alpha

This is intentionally narrow: it is not a general 4D search, just a
continuum-style density check for the current best modular family.
"""

from __future__ import annotations

import cmath
import math
import random
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16
N_LAYERS = 15
SPATIAL_RANGE = 8.0
GAP = 5.0
MASS_COUNTS = (1, 2, 3, 4, 6, 8, 10, 12, 16)


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
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


def generate_4d_modular_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = 40,
    spatial_range: float = SPATIAL_RANGE,
    connect_radius: float = 5.0,
    rng_seed: int = 42,
    gap: float = GAP,
    crosslink_prob: float = 0.02,
):
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            positions.append((x, 0.0, 0.0, 0.0))
            layer_nodes.append(0)
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

                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py, pz, pw = positions[prev_idx]
                        dist = math.sqrt(
                            (x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 + (w - pw) ** 2
                        )
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
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


def propagate_4d(positions, adj, field, src, k):
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        x1, y1, z1, w1 = positions[i]
        for j in adj.get(i, []):
            x2, y2, z2, w2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            dw = w2 - w1
            L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += amps[i] * cmath.exp(1j * k * act) * weight / L
    return amps


def centroid_y(amps, positions, det_list):
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def mean_degree(adj, n):
    return sum(len(nbs) for nbs in adj.values()) / n if n > 0 else 0.0


def fit_power_law(pairs):
    positive = [(n, s) for n, s in pairs if n > 0 and s > 0]
    if len(positive) < 3:
        return None
    xs = [math.log(n) for n, _ in positive]
    ys = [math.log(s) for _, s in positive]
    n_pts = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n_pts * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    alpha = (n_pts * sxy - sx * sy) / denom
    intercept = (sy - alpha * sx) / n_pts
    ss_tot = sum((y - sy / n_pts) ** 2 for y in ys)
    ss_res = sum((y - (alpha * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return alpha, math.exp(intercept), r2


def measure_alpha(nodes_per_layer, connect_radius, n_seeds=N_SEEDS):
    mass_counts = MASS_COUNTS
    results = []
    degree_samples = []

    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=nodes_per_layer,
                spatial_range=SPATIAL_RANGE,
                connect_radius=connect_radius,
                rng_seed=seed * 17 + 3,
                gap=GAP,
            )
            degree_samples.append(mean_degree(adj, len(positions)))

            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            candidates = sorted(
                [i for i in layer_indices[mid] if positions[i][1] > cy + 1],
                key=lambda i: -positions[i][1],
            )
            mass_nodes = candidates[:target_n]
            if not mass_nodes:
                continue

            field = compute_field_4d(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)
            shifts = []
            for k in K_BAND:
                amps_m = propagate_4d(positions, adj, field, src, k)
                amps_f = propagate_4d(positions, adj, free_f, src, k)
                shifts.append(
                    centroid_y(amps_m, positions, det_list)
                    - centroid_y(amps_f, positions, det_list)
                )
            if shifts:
                per_seed.append((len(mass_nodes), sum(shifts) / len(shifts)))

        if per_seed:
            actual_n = per_seed[0][0]
            vals = [v for _, v in per_seed]
            avg = sum(vals) / len(vals)
            se = math.sqrt(sum((v - avg) ** 2 for v in vals) / len(vals)) / math.sqrt(len(vals))
            t = avg / se if se > 1e-10 else 0.0
            if avg > 0:
                results.append((actual_n, avg, se, t))

    alpha_fit = fit_power_law([(n, s) for n, s, _, _ in results])
    mean_degree_val = sum(degree_samples) / len(degree_samples) if degree_samples else 0.0
    return results, alpha_fit, mean_degree_val


def main():
    print("=" * 78)
    print("4D CONTINUUM LIMIT: density sweep on retained modular lane")
    print("  Question: does alpha trend toward ~1 or remain parameter-sensitive?")
    print("=" * 78)
    print()
    print(f"  retained lane: gap={GAP}, k-band={list(K_BAND)}, seeds={N_SEEDS}")
    print()

    configs = [
        (24, 4.5, "sparse"),
        (32, 4.8, "low"),
        (40, 5.1, "medium"),
        (60, 5.4, "dense"),
        (80, 5.8, "very dense"),
    ]

    print(f"  {'nodes':>5s}  {'radius':>6s}  {'<k>':>7s}  {'alpha':>7s}  {'SE':>6s}  {'t':>5s}  {'R^2':>6s}  verdict")
    print(f"  {'-' * 78}")

    rows = []
    for nodes_per_layer, connect_radius, label in configs:
        per_seed_rows, alpha_fit, mean_deg = measure_alpha(nodes_per_layer, connect_radius)
        if alpha_fit is None or not per_seed_rows:
            print(f"  {nodes_per_layer:5d}  {connect_radius:6.2f}  {mean_deg:7.2f}  {'FAIL':>7s}  {'NA':>6s}  {'NA':>5s}  {'NA':>6s}  {label}")
            continue

        alpha, coeff, r2 = alpha_fit
        vals = [a for _, a, _, _ in per_seed_rows]
        avg = sum(vals) / len(vals)
        se = math.sqrt(sum((v - avg) ** 2 for v in vals) / len(vals)) / math.sqrt(len(vals))
        t = avg / se if se > 1e-10 else 0.0
        if alpha > 0.8:
            verdict = "NEAR-M" if alpha < 1.2 else "SUPER"
        elif alpha > 0.4:
            verdict = "MID"
        else:
            verdict = "WEAK"
        rows.append((nodes_per_layer, connect_radius, mean_deg, alpha, se, t, r2, verdict))
        print(
            f"  {nodes_per_layer:5d}  {connect_radius:6.2f}  {mean_deg:7.2f}  "
            f"{alpha:7.3f}  {se:6.4f}  {t:+5.2f}  {r2:6.3f}  {verdict}"
        )

    print()
    if rows:
        alphas = [row[3] for row in rows]
        if len(alphas) >= 3:
            spread = max(alphas) - min(alphas)
            mean_alpha = sum(alphas) / len(alphas)
            print(f"  Alpha range across densities: {min(alphas):.3f} .. {max(alphas):.3f}")
            print(f"  Mean alpha across densities: {mean_alpha:.3f}")
            if spread < 0.12:
                print("  → alpha is converging across density")
            elif spread < 0.35:
                print("  → alpha is drifting but still somewhat stable")
            else:
                print("  → alpha remains parameter-sensitive across density")
        print()

    print("=" * 78)
    print("INTERPRETATION")
    print("  If alpha converges near 1: the 4D mass law is approaching Newtonian")
    print("  If alpha stays spread out: the 4D exponent remains parameter-sensitive")
    print("  If alpha drifts away: density is not rescuing the law")
    print("=" * 78)


if __name__ == "__main__":
    main()
