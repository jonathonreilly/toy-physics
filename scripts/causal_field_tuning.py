#!/usr/bin/env python3
"""Causal field tuning: optimize decay rate for b-dependent gravity.

The causal sum field showed shift decreasing with b. Now tune the
decay parameter to find the sweet spot between:
  - Too little decay (field spreads everywhere → b-independent)
  - Too much decay (field dies too fast → no gravity)

Also test: does the b-dependence follow 1/b, 1/b², or exponential?

PStack experiment: causal-field-tuning
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_3d_dag(n_layers=18, nodes_per_layer=40, yz_range=12.0,
                    connect_radius=3.5, rng_seed=42):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions)-1)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer-2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def field_causal_sum(positions, adj, mass_ids, decay=0.8):
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
    ms = set(mass_ids)
    field = [0.0] * n
    for m in ms:
        field[m] = 1.0
    for i in order:
        if field[i] <= 0:
            continue
        out = adj.get(i, [])
        if not out:
            continue
        for j in out:
            field[j] += decay * field[i] / len(out)
    mx = max(field) if max(field) > 0 else 1
    return [f / mx for f in field]


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
        for j in adj.get(i, []):
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


def sweep_b(decay, n_seeds=24):
    k_band = [3.0, 5.0, 7.0]
    b_targets = [1, 2, 3, 4, 5, 6, 7, 8, 10]
    results = []

    for b in b_targets:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_3d_dag(
                rng_seed=seed*17+3)
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue
            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            mass_ids = [i for i in layer_indices[mid]
                        if abs(positions[i][1] - (cy + b)) < 2.0]
            if len(mass_ids) < 2:
                continue
            field = field_causal_sum(positions, adj, mass_ids, decay=decay)
            free_f = [0.0] * len(positions)
            shifts = []
            for k in k_band:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(am, positions, det_list) -
                              centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append(sum(shifts) / len(shifts))

        if per_seed:
            avg = sum(per_seed) / len(per_seed)
            se = math.sqrt(sum((s-avg)**2 for s in per_seed) / len(per_seed)) / math.sqrt(len(per_seed))
            results.append((b, avg, se))

    return results


def main():
    print("=" * 70)
    print("CAUSAL FIELD TUNING: decay sweep for b-dependent gravity")
    print("  24 seeds per point")
    print("=" * 70)
    print()

    for decay in [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
        results = sweep_b(decay, n_seeds=24)

        print(f"  [decay={decay}]")
        print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'shift*b':>8s}")
        print(f"  {'-'*30}")

        for b, s, se in results:
            print(f"  {b:3d}  {s:+8.4f}  {se:6.4f}  {s*b:+8.3f}")

        # Check if shift decreases with b
        pos = [(b, s) for b, s, _ in results if s > 0]
        if len(pos) >= 4:
            # Fit: shift = A * b^(-gamma)
            # log(shift) = log(A) - gamma * log(b)
            log_b = [math.log(b) for b, _ in pos]
            log_s = [math.log(s) for _, s in pos]
            n = len(log_b)
            sx, sy = sum(log_b), sum(log_s)
            sxy = sum(x*y for x, y in zip(log_b, log_s))
            sxx = sum(x*x for x in log_b)
            denom = n * sxx - sx * sx
            if abs(denom) > 1e-10:
                gamma = -(n * sxy - sx * sy) / denom
                print(f"  → shift ~ b^{-gamma:.2f}")
                if gamma > 0.7:
                    print(f"  ★ DISTANCE FALLOFF: ~1/b^{gamma:.1f}")
                elif gamma > 0.3:
                    print(f"  → partial falloff (not quite 1/b)")
                else:
                    print(f"  → weak/flat")
        print()

    print("=" * 70)
    print("If any decay gives shift ~ 1/b (gamma ≈ 1): causal field")
    print("restores Newtonian distance scaling!")
    print("=" * 70)


if __name__ == "__main__":
    main()
