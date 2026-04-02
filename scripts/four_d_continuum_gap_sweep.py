#!/usr/bin/env python3
"""4D continuum limit: gap × density sweep.

The existing 4D continuum test (gap=5) shows alpha is parameter-sensitive
(0.35 to 1.64 across densities). Does a different gap give better convergence?

Sweep both gap and density to map the (gap, density) → alpha surface.
Focus on the high-R² (reliable) corner.

PStack experiment: four-d-continuum-gap-sweep
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16
N_LAYERS = 15
SPATIAL_RANGE = 8.0


def generate_4d_modular_dag(n_layers, nodes_per_layer, spatial_range,
                            connect_radius, rng_seed, gap, crosslink_prob=0.02):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for ni in range(nodes_per_layer):
                z = rng.uniform(-spatial_range, spatial_range)
                w = rng.uniform(-spatial_range, spatial_range)
                if gap > 0 and layer > barrier_layer:
                    y = rng.uniform(gap/2, spatial_range) if ni < nodes_per_layer//2 else rng.uniform(-spatial_range, -gap/2)
                else:
                    y = rng.uniform(-spatial_range, spatial_range)
                idx = len(positions)
                positions.append((x, y, z, w))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        p = positions[prev_idx]
                        dist = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], p)))
                        if gap > 0 and layer > barrier_layer and round(p[0]) > barrier_layer:
                            same_ch = (positions[idx][1] * p[1] > 0)
                            if same_ch and dist <= connect_radius:
                                adj[prev_idx].append(idx)
                            elif not same_ch and dist <= 2*connect_radius and rng.random() < crosslink_prob:
                                adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def compute_field(positions, adj, mass_ids, iterations=50):
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


def propagate(positions, adj, field, src, k):
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
        pi = positions[i]
        for j in adj.get(i, []):
            pj = positions[j]
            dx = pj[0] - pi[0]
            dsq = sum((a-b)**2 for a, b in zip(pi, pj))
            L = math.sqrt(dsq)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx/L, -1), 1))
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


def measure_alpha(npl, radius, gap, n_seeds=N_SEEDS):
    mass_counts = [1, 2, 4, 6, 8, 12, 16]
    results = []
    mean_deg = 0

    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=N_LAYERS, nodes_per_layer=npl,
                spatial_range=SPATIAL_RANGE, connect_radius=radius,
                rng_seed=seed*17+3, gap=gap)
            if seed == 0 and target_n == mass_counts[0]:
                total_edges = sum(len(nbs) for nbs in adj.values())
                mean_deg = total_edges / len(positions) if positions else 0

            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            cands = sorted([i for i in layer_indices[mid] if positions[i][1] > cy+1],
                           key=lambda i: -positions[i][1])
            mn = cands[:target_n]
            if not mn:
                continue

            field = compute_field(positions, adj, mn)
            free_f = [0.0] * len(positions)
            shifts = []
            for k in K_BAND:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(am, positions, det_list) -
                              centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append((len(mn), sum(shifts)/len(shifts)))

        if per_seed:
            actual_n = per_seed[0][0]
            vals = [v for _, v in per_seed]
            avg = sum(vals) / len(vals)
            if avg > 0:
                results.append((actual_n, avg))

    alpha = None
    r2 = 0
    if len(results) >= 3:
        log_n = [math.log(n) for n, _ in results]
        log_s = [math.log(s) for _, s in results]
        np_ = len(log_n)
        sx, sy = sum(log_n), sum(log_s)
        sxy = sum(x*y for x, y in zip(log_n, log_s))
        sxx = sum(x*x for x in log_n)
        denom = np_ * sxx - sx * sx
        if abs(denom) > 1e-10:
            alpha = (np_ * sxy - sx * sy) / denom
            intercept = (sy - alpha * sx) / np_
            ss_tot = sum((y - sy/np_)**2 for y in log_s)
            ss_res = sum((y - (alpha*x + intercept))**2 for x, y in zip(log_n, log_s))
            r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)

    return alpha, r2, mean_deg


def main():
    print("=" * 74)
    print("4D CONTINUUM: gap × density → alpha surface")
    print("  Does any (gap, density) corner give stable alpha ≈ 1.0?")
    print("=" * 74)
    print()

    configs = [
        # (npl, radius)
        (25, 4.5),
        (35, 4.8),
        (50, 5.2),
        (70, 5.6),
    ]

    gaps = [3.0, 5.0, 7.0]

    print(f"  {'gap':>4s}  {'npl':>4s}  {'radius':>6s}  {'<k>':>5s}  "
          f"{'alpha':>7s}  {'R²':>5s}  verdict")
    print(f"  {'-'*50}")

    best = None
    for gap in gaps:
        for npl, radius in configs:
            alpha, r2, deg = measure_alpha(npl, radius, gap)
            if alpha is not None:
                if r2 > 0.7:
                    if 0.8 <= alpha <= 1.2:
                        verdict = "NEAR-M"
                    elif alpha > 1.2:
                        verdict = "SUPER"
                    elif alpha < 0.5:
                        verdict = "WEAK"
                    else:
                        verdict = "SUB"
                else:
                    verdict = "LOW-R²"
                print(f"  {gap:4.1f}  {npl:4d}  {radius:6.1f}  {deg:5.1f}  "
                      f"{alpha:7.3f}  {r2:5.3f}  {verdict}")
                if r2 > 0.7 and (best is None or abs(alpha - 1.0) < abs(best[0] - 1.0)):
                    best = (alpha, r2, gap, npl, radius, deg)
            else:
                print(f"  {gap:4.1f}  {npl:4d}  {radius:6.1f}  {deg:5.1f}  "
                      f"  FAIL")

    print()
    if best:
        alpha, r2, gap, npl, radius, deg = best
        print(f"  Best alpha near 1.0: {alpha:.3f} (R²={r2:.3f})")
        print(f"    gap={gap}, npl={npl}, radius={radius}, <k>={deg:.1f}")
    print()

    # Convergence check: at best gap, does alpha settle with density?
    if best:
        best_gap = best[2]
        print(f"  Convergence at gap={best_gap}:")
        alphas_high_r2 = []
        for npl, radius in configs:
            alpha, r2, deg = measure_alpha(npl, radius, best_gap)
            if alpha is not None and r2 > 0.5:
                alphas_high_r2.append(alpha)
                print(f"    npl={npl}: alpha={alpha:.3f} (R²={r2:.3f})")

        if len(alphas_high_r2) >= 3:
            spread = max(alphas_high_r2) - min(alphas_high_r2)
            mean_a = sum(alphas_high_r2) / len(alphas_high_r2)
            print(f"  Spread: {spread:.3f}, Mean: {mean_a:.3f}")
            if spread < 0.3:
                print(f"  → CONVERGING to alpha ≈ {mean_a:.2f}")
            else:
                print(f"  → NOT CONVERGED (spread > 0.3)")

    print()
    print("=" * 74)


if __name__ == "__main__":
    main()
