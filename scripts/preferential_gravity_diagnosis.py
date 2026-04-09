#!/usr/bin/env python3
"""Why does preferential attachment break gravity?

Cross-family test showed gravity fails on preferential DAGs at N>=20.
Hypothesis: hub nodes concentrate amplitude, breaking the distributed
phase-valley mechanism.

Tests:
  1. Hub concentration: what fraction of total amplitude sits in top-k nodes?
  2. Hub_boost sweep: at what threshold does gravity break?
  3. Does the amplitude distribution differ between families?

PStack experiment: preferential-gravity-diagnosis
"""

from __future__ import annotations

import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16


def generate_3d_preferential(n_layers=20, npl=30, yz_range=10.0, r=3.5,
                              rng_seed=42, hub_boost=3.0):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    out_deg = defaultdict(int)
    layers = []
    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                candidates = []
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r:
                            w = 1.0 + hub_boost * out_deg[pi]
                            candidates.append((pi, w))
                if candidates:
                    max_w = max(c[1] for c in candidates)
                    for pi, w in candidates:
                        if rng.random() < w / max_w:
                            adj[pi].append(idx)
                            out_deg[pi] += 1
        layers.append(nodes)
    return positions, dict(adj), layers


def generate_3d_uniform(n_layers=20, npl=30, yz_range=10.0, r=3.5, rng_seed=42):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layers = []
    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                for pl in layers[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r:
                            adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


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
            L = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pj)))
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


def amplitude_concentration(amps, layer_nodes, top_k=3):
    """What fraction of total probability is in the top-k nodes of a layer?"""
    probs = sorted([abs(amps[i])**2 for i in layer_nodes], reverse=True)
    total = sum(probs)
    if total < 1e-30:
        return 0.0
    return sum(probs[:top_k]) / total


def measure_gravity(gen_fn, nl=25, **kwargs):
    grav_seeds = []
    for seed in range(N_SEEDS):
        positions, adj, layers = gen_fn(n_layers=nl, rng_seed=seed*13+5, **kwargs)
        src = layers[0]
        det_list = list(layers[-1])
        if not det_list:
            continue
        all_ys = [positions[i][1] for i in range(len(positions))]
        cy = sum(all_ys) / len(all_ys)
        grav_idx = 2 * len(layers) // 3
        mass = [i for i in layers[grav_idx] if positions[i][1] > cy+1][:8]
        if not mass:
            continue
        field = compute_field(positions, adj, mass)
        free_f = [0.0] * len(positions)
        deltas = []
        for k in K_BAND:
            am = propagate(positions, adj, field, src, k)
            af = propagate(positions, adj, free_f, src, k)
            deltas.append(centroid_y(am, positions, det_list) -
                          centroid_y(af, positions, det_list))
        if deltas:
            grav_seeds.append(sum(deltas)/len(deltas))
    if grav_seeds:
        avg = sum(grav_seeds) / len(grav_seeds)
        se = (sum((d-avg)**2 for d in grav_seeds) / len(grav_seeds))**0.5 / len(grav_seeds)**0.5
        return avg, avg/se if se > 1e-10 else 0, len(grav_seeds)
    return 0, 0, 0


def measure_concentration(gen_fn, nl=25, **kwargs):
    concs = []
    for seed in range(N_SEEDS):
        positions, adj, layers = gen_fn(n_layers=nl, rng_seed=seed*13+5, **kwargs)
        src = layers[0]
        field = [0.0] * len(positions)
        amps = propagate(positions, adj, field, src, 5.0)
        mid = len(layers) // 2
        c = amplitude_concentration(amps, layers[mid], top_k=3)
        concs.append(c)
    return sum(concs)/len(concs) if concs else 0


def main():
    print("=" * 70)
    print("PREFERENTIAL ATTACHMENT: Why does gravity break?")
    print("=" * 70)
    print()

    # Test 1: Hub boost sweep
    print("TEST 1: Gravity vs hub_boost (N=25)")
    print(f"  {'boost':>6s}  {'grav_d':>8s}  {'t':>5s}  {'conc_top3':>10s}  {'n':>3s}")
    print(f"  {'-'*38}")

    for boost in [0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
        gd, gt, ng = measure_gravity(generate_3d_preferential, nl=25, hub_boost=boost)
        conc = measure_concentration(generate_3d_preferential, nl=25, hub_boost=boost)
        v = "GRAV" if gd > 0 and gt > 2 else "weak" if gd > 0 else "flat"
        print(f"  {boost:6.1f}  {gd:+8.4f}  {gt:+5.2f}  {conc:10.3f}  {ng:3d}  {v}")

    print()

    # Test 2: Compare concentration across families
    print("TEST 2: Amplitude concentration at mid-layer (N=25)")
    print(f"  {'family':>25s}  {'conc_top3':>10s}  {'grav_d':>8s}  {'t':>5s}")
    print(f"  {'-'*54}")

    families = [
        ("Uniform", generate_3d_uniform, {}),
        ("Preferential boost=1", generate_3d_preferential, {"hub_boost": 1.0}),
        ("Preferential boost=3", generate_3d_preferential, {"hub_boost": 3.0}),
        ("Preferential boost=10", generate_3d_preferential, {"hub_boost": 10.0}),
    ]

    for name, gen_fn, kwargs in families:
        gd, gt, _ = measure_gravity(gen_fn, nl=25, **kwargs)
        conc = measure_concentration(gen_fn, nl=25, **kwargs)
        print(f"  {name:>25s}  {conc:10.3f}  {gd:+8.4f}  {gt:+5.2f}")

    print()
    print("=" * 70)
    print("INTERPRETATION:")
    print("  If high conc correlates with gravity failure:")
    print("    hub concentration breaks the distributed phase valley")
    print("  If no correlation: something else about hub structure kills gravity")
    print("=" * 70)


if __name__ == "__main__":
    main()
