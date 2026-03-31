#!/usr/bin/env python3
"""Gravity on 3D causal DAGs.

In 2D: field ~ log(r), gradient ~ 1/r, Δky ~ constant (b-independent).
In 3D: field ~ 1/r, gradient ~ 1/r², deflection should ~ 1/b.

Generate 3D causal DAGs (layers of nodes in 3D space), propagate with
corrected propagator (1/L^p), measure gravitational deflection.

Test: does 3D give 1/b distance scaling and F∝M mass scaling?

PStack experiment: three-d-gravity
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_3d_causal_dag(n_layers=12, nodes_per_layer=30, xyz_range=8.0,
                           connect_radius=3.0, rng_seed=42):
    """Generate a causal DAG in 3D: layers of nodes at random (y,z) positions."""
    rng = random.Random(rng_seed)
    positions = []  # (x, y, z)
    adj = defaultdict(list)

    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
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
        nf = [0.0]*n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def pathsum_3d(positions, adj, field, src, det, k):
    """Corrected propagator on 3D graph."""
    n = len(positions)
    in_deg = [0]*n
    for i, nbs in adj.items():
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

    amps = [0.0+0.0j]*n
    for s in src:
        amps[s] = 1.0/len(src)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            L = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret
            ea = cmath.exp(1j*k*act)/(L**1.0)
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def centroid_yz(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0, 0.0
    cy = sum(positions[d][1]*p for d, p in probs.items()) / total
    cz = sum(positions[d][2]*p for d, p in probs.items()) / total
    return cy, cz


def main():
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("3D GRAVITY: does 3D give 1/b distance scaling?")
    print("=" * 70)
    print()

    # TEST 1: Basic gravity on 3D DAGs
    print("TEST 1: Gravitational attraction on 3D DAGs")
    print()

    attract_count = 0
    total = 0

    for seed in range(n_seeds):
        positions, adj, layer_indices = generate_3d_causal_dag(
            n_layers=12, nodes_per_layer=30, xyz_range=8.0,
            connect_radius=3.0, rng_seed=seed*11+7,
        )
        n = len(positions)
        src = layer_indices[0]
        det = set(layer_indices[-1])
        if not det:
            continue

        mid = len(layer_indices)//2
        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys)/len(all_ys)

        mass_idx = [i for i in layer_indices[mid] if positions[i][1] > cy+2]
        if len(mass_idx) < 3:
            continue

        mass_cy = sum(positions[i][1] for i in mass_idx)/len(mass_idx)
        field = compute_field_3d(positions, adj, mass_idx)
        free_f = [0.0]*n

        shifts = []
        for k in k_band:
            fp = pathsum_3d(positions, adj, free_f, src, det, k)
            mp = pathsum_3d(positions, adj, field, src, det, k)
            fy, _ = centroid_yz(fp, positions)
            my, _ = centroid_yz(mp, positions)
            shifts.append(my - fy)

        avg = sum(shifts)/len(shifts)
        toward = mass_cy - cy
        attracts = (toward > 0 and avg > 0.05)
        if attracts:
            attract_count += 1
        total += 1

        print(f"  seed {seed}: shift={avg:+.3f}, mass_cy={mass_cy:.1f}, "
              f"{'ATTRACT' if attracts else 'repel/neutral'}")

    print(f"\n  Gravity: {attract_count}/{total}")

    # TEST 2: Distance scaling in 3D
    print()
    print("TEST 2: Shift vs impact parameter (3D)")
    print()

    # Use one large 3D graph
    positions, adj, layer_indices = generate_3d_causal_dag(
        n_layers=15, nodes_per_layer=40, xyz_range=12.0,
        connect_radius=3.5, rng_seed=42,
    )
    n = len(positions)
    src = layer_indices[0]
    det = set(layer_indices[-1])
    mid = len(layer_indices)//2
    free_f = [0.0]*n

    print(f"  {'b':>4s}  {'shift':>8s}  {'shift×b':>8s}  {'shift×b²':>9s}")
    print(f"  {'-' * 34}")

    all_ys = [y for _, y, _ in positions]
    cy = sum(all_ys)/len(all_ys)

    for b_target in [2, 3, 4, 6, 8, 10]:
        # Mass at y ≈ b_target above center
        mass_idx = [i for i in layer_indices[mid]
                    if abs(positions[i][1] - (cy + b_target)) < 2]
        if len(mass_idx) < 2:
            continue

        field = compute_field_3d(positions, adj, mass_idx)
        shifts = []
        for k in k_band:
            fp = pathsum_3d(positions, adj, free_f, src, det, k)
            mp = pathsum_3d(positions, adj, field, src, det, k)
            fy, _ = centroid_yz(fp, positions)
            my, _ = centroid_yz(mp, positions)
            shifts.append(my - fy)

        avg = sum(shifts)/len(shifts) if shifts else 0
        print(f"  {b_target:4d}  {avg:+8.4f}  {avg*b_target:+8.3f}  {avg*b_target**2:+9.2f}")

    # TEST 3: Mass scaling in 3D
    print()
    print("TEST 3: Shift vs mass size (3D)")
    print()

    print(f"  {'n_mass':>6s}  {'shift':>8s}  {'shift/n':>8s}")
    print(f"  {'-' * 26}")

    for target_n in [2, 4, 6, 8, 12, 16]:
        candidates = [i for i in layer_indices[mid] if positions[i][1] > cy+3]
        mass_idx = candidates[:target_n]
        if len(mass_idx) < 2:
            continue

        field = compute_field_3d(positions, adj, mass_idx)
        shifts = []
        for k in k_band:
            fp = pathsum_3d(positions, adj, free_f, src, det, k)
            mp = pathsum_3d(positions, adj, field, src, det, k)
            fy, _ = centroid_yz(fp, positions)
            my, _ = centroid_yz(mp, positions)
            shifts.append(my - fy)

        avg = sum(shifts)/len(shifts) if shifts else 0
        per_n = avg/len(mass_idx) if mass_idx else 0
        print(f"  {len(mass_idx):6d}  {avg:+8.4f}  {per_n:+8.4f}")

    print()
    print("If shift×b ≈ const: θ ~ 1/b (correct 3D scaling)")
    print("If shift/n ≈ const: F ~ M (correct mass scaling)")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
