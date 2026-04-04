#!/usr/bin/env python3
"""Test: does 1/L^(d-1) kernel fix gravity on random/mirror DAGs?

If 1/L^2 gives TOWARD on 3D random DAGs where 1/L gives AWAY,
the kernel story unifies lattices AND grown geometries.

Test 3D random DAGs and mirror DAGs at multiple kernel powers.
"""

from __future__ import annotations
import math
import cmath
import random
import time
from collections import defaultdict, deque

import numpy as np

BETA = 0.8
K = 5.0
N_YBINS = 8
N_SEEDS = 8


def _topo_order(adj, n):
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


def generate_random_3d_dag(n_layers, npl, xyz_range, connect_radius, seed):
    rng = random.Random(seed)
    pos = []
    adj = defaultdict(list)
    layer_idx = []
    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            pos.append((x, 0.0, 0.0))
            nodes.append(len(pos) - 1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(pos)
                pos.append((x, y, z))
                nodes.append(idx)
                for prev in layer_idx[max(0, layer-2):]:
                    for pi in prev:
                        px, py, pz = pos[pi]
                        d = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if d <= connect_radius:
                            adj[pi].append(idx)
            layer_idx.append(nodes)
            continue
        layer_idx.append(nodes)
    return pos, dict(adj), layer_idx


def generate_mirror_3d_dag(n_layers, npl_half, xyz_range, connect_radius, seed):
    rng = random.Random(seed)
    pos = []
    adj = defaultdict(list)
    layer_idx = []
    mirror = {}

    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            idx = len(pos)
            pos.append((x, 0.0, 0.0))
            nodes.append(idx)
            mirror[idx] = idx
        else:
            up = []; lo = []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                iu = len(pos); pos.append((x, y, z)); up.append(iu)
                il = len(pos); pos.append((x, -y, z)); lo.append(il)
                mirror[iu] = il; mirror[il] = iu

            nodes = up + lo
            for prev in layer_idx[max(0, layer-2):]:
                for pi in prev:
                    px, py, pz = pos[pi]
                    for ci in up:
                        cx, cy, cz = pos[ci]
                        d = math.sqrt((cx-px)**2 + (cy-py)**2 + (cz-pz)**2)
                        if d <= connect_radius:
                            adj[pi].append(ci)
                            adj[mirror[pi]].append(mirror[ci])
        layer_idx.append(nodes)
    return pos, dict(adj), layer_idx


def propagate(pos, adj, field, k, blocked, power):
    n = len(pos)
    order = _topo_order(adj, n)
    amps = [0j] * n
    # Source: first node
    amps[0] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = pos[i]
            x2, y2, z2 = pos[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / (L ** power)
    return amps


def test_gravity(pos, adj, layer_idx, n_layers, power, strength, z_mass):
    n = len(pos)
    bl = n_layers // 3
    if bl >= len(layer_idx):
        return None

    # Barrier + slits
    barrier_nodes = layer_idx[bl]
    sa = [i for i in barrier_nodes if pos[i][1] >= 0.5]
    sb = [i for i in barrier_nodes if pos[i][1] <= -0.5]
    blocked = set(barrier_nodes) - set(sa + sb)

    # Detector: last layer
    det = layer_idx[-1] if layer_idx else []
    if not det:
        return None

    # Free field
    field_f = [0.0] * n
    af = propagate(pos, adj, field_f, K, blocked, power)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None
    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf

    # Mass field at z=z_mass in the gravity layer
    gl = 2 * n_layers // 3
    if gl >= len(layer_idx):
        return None
    grav_layer = layer_idx[gl]
    # Find node closest to z=z_mass in gravity layer
    best = None
    best_dist = float('inf')
    for gi in grav_layer:
        d = abs(pos[gi][2] - z_mass)
        if d < best_dist:
            best_dist = d
            best = gi
    if best is None:
        return None

    field_m = [0.0] * n
    mx, my, mz = pos[best]
    for i in range(n):
        r = math.sqrt((pos[i][0]-mx)**2 + (pos[i][1]-my)**2 + (pos[i][2]-mz)**2) + 0.1
        field_m[i] = strength / r

    am = propagate(pos, adj, field_m, K, blocked, power)
    pm = sum(abs(am[d])**2 for d in det)
    if pm < 1e-30:
        return None
    zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
    return zm - zf


def run_test(name, gen_fn, n_layers, npl, xyz_range, connect_radius, strengths, z_masses):
    print(f"\n{name}")
    print("-" * 60)

    for power in [1, 2, 3]:
        toward_counts = {s: 0 for s in strengths}
        total_counts = {s: 0 for s in strengths}
        mean_delta = {s: [] for s in strengths}

        for seed in range(N_SEEDS):
            if 'mirror' in name.lower():
                pos, adj, layer_idx = gen_fn(n_layers, npl, xyz_range,
                                              connect_radius, seed)
            else:
                pos, adj, layer_idx = gen_fn(n_layers, npl, xyz_range,
                                              connect_radius, seed)

            for s in strengths:
                for z in z_masses:
                    delta = test_gravity(pos, adj, layer_idx, n_layers,
                                        power, s, z)
                    if delta is not None:
                        total_counts[s] += 1
                        if delta > 0:
                            toward_counts[s] += 1
                        mean_delta[s].append(delta)

        print(f"  1/L^{power}:")
        for s in strengths:
            tc = total_counts[s]
            tw = toward_counts[s]
            md = np.mean(mean_delta[s]) if mean_delta[s] else 0
            print(f"    s={s:.0e}: {tw}/{tc} TOWARD, mean_delta={md:+.4f}")


def main():
    print("=" * 60)
    print("KERNEL TRANSFER TEST: Does 1/L^(d-1) fix gravity on DAGs?")
    print("  If YES: kernel story unifies lattices AND random graphs")
    print("=" * 60)

    strengths = [0.1, 0.01]
    z_masses = [3, 5, 8]

    # 3D Random DAG
    run_test("3D RANDOM DAG (30 nodes/layer, N=25, r=4)",
             generate_random_3d_dag,
             n_layers=25, npl=30, xyz_range=12.0,
             connect_radius=4.0,
             strengths=strengths, z_masses=z_masses)

    # 3D Mirror DAG
    run_test("3D MIRROR DAG (15 per half, N=25, r=4)",
             generate_mirror_3d_dag,
             n_layers=25, npl=15, xyz_range=12.0,
             connect_radius=4.0,
             strengths=strengths, z_masses=z_masses)

    # Smaller random DAG (fewer paths, less depletion)
    run_test("3D RANDOM DAG (15 nodes/layer, N=15, r=5)",
             generate_random_3d_dag,
             n_layers=15, npl=15, xyz_range=12.0,
             connect_radius=5.0,
             strengths=strengths, z_masses=z_masses)

    # Ultra-weak field
    run_test("3D MIRROR DAG ultra-weak (15 per half, N=25, r=4)",
             generate_mirror_3d_dag,
             n_layers=25, npl=15, xyz_range=12.0,
             connect_radius=4.0,
             strengths=[0.001, 0.0001], z_masses=z_masses)

    print("\n" + "=" * 60)
    print("If 1/L^2 gives more TOWARD than 1/L on 3D DAGs:")
    print("  → kernel story transfers from lattices to random graphs")
    print("=" * 60)


if __name__ == "__main__":
    main()
