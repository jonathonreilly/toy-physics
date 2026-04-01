#!/usr/bin/env python3
"""Propagator power sweep: does 1/L^p with p != 1 give distance-dependent gravity?

The model uses W(i→j) = exp(i*k*S) * exp(-beta*theta^2) / L^p
Currently p=1. The gravity deflection is b-independent (no distance scaling).

In continuum field theory:
  - d=1 spatial: Green's function ~ log(r), propagator ~ 1/L^0
  - d=2 spatial: Green's function ~ 1/r,    propagator ~ 1/L^(1/2)
  - d=3 spatial: Green's function ~ 1/r^2,  propagator ~ 1/L

The "correct" p for dimension d might be (d-1)/2 or similar.

Sweep p from 0 to 2 and measure:
  1. Mass scaling alpha(p) — does it change?
  2. Distance scaling — does b-dependence appear for some p?
  3. Gravity signal strength — which p gives best t-values?

PStack experiment: propagator-power-sweep
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_3d_modular_dag(n_layers=15, nodes_per_layer=30, yz_range=10.0,
                            connect_radius=3.5, rng_seed=42, gap=5.0,
                            crosslink_prob=0.02):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)
                if gap > 0 and layer > barrier_layer:
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
                        if gap > 0 and layer > barrier_layer and round(px) > barrier_layer:
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


def propagate(positions, adj, field, src, k, p_power=1.0, blocked=None):
    """Propagator with variable attenuation power p."""
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
            ea = cmath.exp(1j * k * act) * w / (L ** p_power)
            amps[j] += amps[i] * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def measure_for_p(p_power, n_seeds=16):
    """Measure gravity signal, alpha, and b-scaling for given p."""
    k_band = [3.0, 5.0, 7.0]

    # Gravity signal
    grav_per_seed = []
    for seed in range(n_seeds):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=18, nodes_per_layer=30, rng_seed=seed*13+5, gap=5.0)
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        all_ys = [positions[i][1] for i in range(len(positions))]
        cy = sum(all_ys) / len(all_ys)
        grav_idx = 2 * len(layer_indices) // 3
        mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1][:8]
        if not mass:
            continue
        field = compute_field(positions, adj, mass)
        free_f = [0.0] * len(positions)
        deltas = []
        for k in k_band:
            am = propagate(positions, adj, field, src, k, p_power)
            af = propagate(positions, adj, free_f, src, k, p_power)
            deltas.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
        if deltas:
            grav_per_seed.append(sum(deltas) / len(deltas))

    if grav_per_seed:
        ng = len(grav_per_seed)
        gd = sum(grav_per_seed) / ng
        gse = math.sqrt(sum((d-gd)**2 for d in grav_per_seed) / ng) / math.sqrt(ng)
        gt = gd / gse if gse > 1e-10 else 0
    else:
        gd, gse, gt = 0, 0, 0

    # Mass scaling alpha
    mass_counts = [1, 2, 4, 8, 16]
    results = []
    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=15, nodes_per_layer=30, rng_seed=seed*17+3, gap=5.0)
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue
            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            candidates = sorted([i for i in layer_indices[mid] if positions[i][1] > cy+1],
                                key=lambda i: -positions[i][1])
            mn = candidates[:target_n]
            if not mn:
                continue
            field = compute_field(positions, adj, mn)
            free_f = [0.0] * len(positions)
            shifts = []
            for k in k_band:
                am = propagate(positions, adj, field, src, k, p_power)
                af = propagate(positions, adj, free_f, src, k, p_power)
                shifts.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append((len(mn), sum(shifts) / len(shifts)))

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
        np_ = len(log_n)
        sx, sy = sum(log_n), sum(log_s)
        sxy = sum(x*y for x, y in zip(log_n, log_s))
        sxx = sum(x*x for x in log_n)
        denom = np_ * sxx - sx * sx
        if abs(denom) > 1e-10:
            alpha = (np_ * sxy - sx * sy) / denom

    # Distance scaling
    b_targets = [2.0, 4.0, 6.0, 8.0]
    b_results = []
    for b in b_targets:
        per_seed = []
        for seed in range(12):
            positions, adj, layer_indices = generate_3d_modular_dag(
                n_layers=18, nodes_per_layer=30, yz_range=12.0,
                rng_seed=seed*17+3, gap=5.0)
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue
            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            mn = [i for i in layer_indices[mid] if abs(positions[i][1]-(cy+b)) < 1.5]
            if len(mn) < 2:
                continue
            field = compute_field(positions, adj, mn)
            free_f = [0.0] * len(positions)
            shifts = []
            for k in k_band:
                am = propagate(positions, adj, field, src, k, p_power)
                af = propagate(positions, adj, free_f, src, k, p_power)
                shifts.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append(sum(shifts) / len(shifts))
        if per_seed:
            avg = sum(per_seed) / len(per_seed)
            b_results.append((b, avg))

    # Check b-scaling
    b_scaling = None
    if len(b_results) >= 3:
        positive = [(b, s) for b, s in b_results if s > 0]
        if len(positive) >= 2:
            products = [s*b for b, s in positive]
            mean_p = sum(products) / len(products)
            cv = (max(products) - min(products)) / mean_p if mean_p > 0 else 999
            b_scaling = cv

    return gd, gt, alpha, b_scaling, b_results


def main():
    print("=" * 78)
    print("PROPAGATOR POWER SWEEP: 1/L^p on 3D modular gap=5")
    print("  Does varying p unlock distance-dependent gravity?")
    print("=" * 78)
    print()

    p_values = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

    print(f"  {'p':>5s}  {'grav_d':>8s}  {'grav_t':>7s}  {'alpha':>7s}  "
          f"{'b_CV':>6s}  {'b_scaling':>10s}")
    print(f"  {'-'*52}")

    for p in p_values:
        gd, gt, alpha, b_cv, b_results = measure_for_p(p, n_seeds=16)
        alpha_s = f"{alpha:.3f}" if alpha is not None else "FAIL"
        if b_cv is not None:
            b_label = "1/b!" if b_cv < 0.3 else "partial" if b_cv < 0.6 else "flat"
        else:
            b_label = "N/A"
        gv = "GRAV" if gt > 2 else "weak" if gt > 1 else "flat"
        print(f"  {p:5.2f}  {gd:+8.4f}  {gt:+7.2f}  {alpha_s:>7s}  "
              f"{b_cv if b_cv is not None else 0:6.2f}  {b_label:>10s}  {gv}")

    print()

    # Detail on best b-scaling
    print("DISTANCE SCALING DETAIL (shift vs b):")
    print()
    for p in [0.5, 1.0, 1.5]:
        _, _, _, _, b_results = measure_for_p(p, n_seeds=16)
        print(f"  p={p:.1f}:")
        for b, s in b_results:
            print(f"    b={b:.1f}: shift={s:+.4f}, shift*b={s*b:+.3f}")
        print()

    print("=" * 78)
    print("INTERPRETATION:")
    print("  p < 1: weaker attenuation → more amplitude reaches far nodes")
    print("  p = 1: current model (1/L)")
    print("  p > 1: stronger attenuation → more localized propagation")
    print()
    print("  If b-dependence appears at some p: the propagator power")
    print("  controls the distance scaling of gravity.")
    print("  If flat for all p: b-independence is structural (path topology).")
    print("=" * 78)


if __name__ == "__main__":
    main()
