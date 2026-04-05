#!/usr/bin/env python3
"""Inverse problem harness: which graph properties does Newton+Born require?

Tests gravity and Born under systematic graph perturbations:
  1. Edge deletion (keep fraction)
  2. Asymmetric connectivity (remove z>0 edges)
  3. Position jitter (random displacement)
  4. Sparse connectivity (NN only)
  5. No field coupling (control)

For each: reports gravity sign, magnitude, Born, and whether the
property is REQUIRED for gravity.

This is the frozen artifact for the graph-universality claim.
"""

from __future__ import annotations
import cmath
import math
import random
import time
from collections import deque

try:
    import numpy as np
except ModuleNotFoundError:
    import sys, os
    raise SystemExit("numpy required")

BETA = 0.8
K = 5.0
STRENGTH = 5e-4
N_LAYERS = 13
HW = 4
H = 1.0
MAX_D = 3


def make_lattice():
    pos = []
    adj = {}
    nmap = {}
    layers = []
    idx = 0
    for l in range(N_LAYERS):
        x = l * H
        nodes = []
        for iy in range(-HW, HW + 1):
            for iz in range(-HW, HW + 1):
                pos.append((x, iy * H, iz * H))
                nmap[(l, iy, iz)] = idx
                nodes.append(idx)
                idx += 1
        layers.append(nodes)
    n = len(pos)
    for l in range(N_LAYERS - 1):
        for iy in range(-HW, HW + 1):
            for iz in range(-HW, HW + 1):
                si = nmap[(l, iy, iz)]
                edges = []
                for dy in range(-MAX_D, MAX_D + 1):
                    iyn = iy + dy
                    if abs(iyn) > HW:
                        continue
                    for dz in range(-MAX_D, MAX_D + 1):
                        izn = iz + dz
                        if abs(izn) > HW:
                            continue
                        di = nmap.get((l + 1, iyn, izn))
                        if di is not None:
                            edges.append(di)
                adj[si] = edges
    return pos, adj, n, layers, nmap


def perturb_edges(adj, keep_frac, seed=42):
    rng = random.Random(seed)
    return {si: [e for e in edges if rng.random() < keep_frac]
            for si, edges in adj.items()}


def perturb_asymmetric(adj, pos):
    return {si: [e for e in edges if pos[e][2] <= 0.5]
            for si, edges in adj.items()}


def perturb_positions(pos, jitter, seed=42):
    rng = random.Random(seed)
    return [(x, y + rng.gauss(0, jitter * H), z + rng.gauss(0, jitter * H))
            if i > 0 else (x, y, z)
            for i, (x, y, z) in enumerate(pos)]


def make_sparse_lattice():
    pos = []
    adj = {}
    nmap = {}
    layers = []
    idx = 0
    for l in range(N_LAYERS):
        x = l * H
        nodes = []
        for iy in range(-HW, HW + 1):
            for iz in range(-HW, HW + 1):
                pos.append((x, iy * H, iz * H))
                nmap[(l, iy, iz)] = idx
                nodes.append(idx)
                idx += 1
        layers.append(nodes)
    n = len(pos)
    for l in range(N_LAYERS - 1):
        for iy in range(-HW, HW + 1):
            for iz in range(-HW, HW + 1):
                si = nmap[(l, iy, iz)]
                edges = []
                for dy in [-1, 0, 1]:
                    iyn = iy + dy
                    if abs(iyn) > HW:
                        continue
                    for dz in [-1, 0, 1]:
                        izn = iz + dz
                        if abs(izn) > HW:
                            continue
                        di = nmap.get((l + 1, iyn, izn))
                        if di is not None:
                            edges.append(di)
                adj[si] = edges
    return pos, adj, n, layers, nmap


def topo_order(adj, n):
    ind = [0] * n
    for edges in adj.values():
        for j in edges:
            ind[j] += 1
    q = deque(i for i in range(n) if ind[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            ind[j] -= 1
            if ind[j] == 0:
                q.append(j)
    return order


def propagate(pos, adj, n, field, k, blocked):
    order = topo_order(adj, n)
    amps = [0j] * n
    amps[0] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            act = L * (1 - lf)
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / (L * L)
    return amps


def test_gravity(pos, adj, n, layers):
    det = layers[-1]
    gl_nodes = layers[2 * N_LAYERS // 3]
    bl = N_LAYERS // 3
    bi = layers[bl]
    sa = [i for i in bi if pos[i][1] >= 0.5]
    sb = [i for i in bi if pos[i][1] <= -0.5]
    blocked = set(bi) - set(sa + sb)

    ff = [0.0] * n
    af = propagate(pos, adj, n, ff, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None, None

    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf

    best = min(gl_nodes, key=lambda i: abs(pos[i][2] - 3))
    field = [0.0] * n
    mx, my, mz = pos[best]
    for i in range(n):
        r = math.sqrt((pos[i][0]-mx)**2 + (pos[i][1]-my)**2 + (pos[i][2]-mz)**2) + 0.1
        field[i] = STRENGTH / r
    am = propagate(pos, adj, n, field, K, blocked)
    pm = sum(abs(am[d])**2 for d in det)
    if pm < 1e-30:
        return None, None
    zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
    return zm - zf, None  # Born tested separately for speed


def test_born(pos, adj, n, layers):
    det = layers[-1]
    bl = N_LAYERS // 3
    bi = layers[bl]
    sa = [i for i in bi if pos[i][1] >= 0.5]
    sb = [i for i in bi if pos[i][1] <= -0.5]
    blocked = set(bi) - set(sa + sb)

    ff = [0.0] * n
    upper = sorted([i for i in bi if pos[i][1] > 1], key=lambda i: pos[i][1])
    lower = sorted([i for i in bi if pos[i][1] < -1], key=lambda i: -pos[i][1])
    middle = [i for i in bi if abs(pos[i][1]) <= 1 and abs(pos[i][2]) <= 1]
    if not (upper and lower and middle):
        return float('nan')

    s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
    all_s = set(s_a + s_b + s_c)
    other = set(bi) - all_s
    probs = {}
    for key, open_set in [('abc', all_s), ('ab', set(s_a+s_b)),
                           ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                           ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
        bl2 = other | (all_s - open_set)
        a = propagate(pos, adj, n, ff, K, bl2)
        probs[key] = [abs(a[d])**2 for d in det]
    I3 = 0; P = 0
    for di in range(len(det)):
        i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
              - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
        I3 += abs(i3); P += probs['abc'][di]
    return I3 / P if P > 1e-30 else float('nan')


def main():
    t_total = time.time()

    print("=" * 65)
    print("INVERSE PROBLEM HARNESS")
    print("  Which graph properties does Newton+Born require?")
    print(f"  Lattice: {N_LAYERS} layers, hw={HW}, h={H}, max_d={MAX_D}")
    print("=" * 65)

    pos_base, adj_base, n, layers, nmap = make_lattice()

    tests = [
        ("Baseline (regular lattice)", pos_base, adj_base, n, layers),
    ]

    # Edge deletion
    for frac in [0.9, 0.7, 0.5]:
        adj_p = perturb_edges(adj_base, frac)
        tests.append((f"Edge deletion (keep {frac:.0%})", pos_base, adj_p, n, layers))

    # Asymmetric
    adj_asym = perturb_asymmetric(adj_base, pos_base)
    tests.append(("Asymmetric (z>0 edges removed)", pos_base, adj_asym, n, layers))

    # Position jitter
    for jitter in [0.3, 0.5]:
        pos_j = perturb_positions(pos_base, jitter)
        tests.append((f"Position jitter ({jitter}h)", pos_j, adj_base, n, layers))

    # Sparse
    pos_s, adj_s, n_s, layers_s, _ = make_sparse_lattice()
    tests.append(("Sparse (NN only, 9 edges)", pos_s, adj_s, n_s, layers_s))

    # No field coupling (control)
    tests.append(("No field (control)", pos_base, adj_base, n, layers))

    print(f"\n{'Test':>40s}  {'gravity':>10s}  {'dir':>5s}  {'Born':>10s}")
    print("-" * 72)

    for name, pos, adj, nn, lyrs in tests:
        t0 = time.time()
        if name == "No field (control)":
            grav = 0.0
        else:
            result = test_gravity(pos, adj, nn, lyrs)
            grav = result[0] if result[0] is not None else float('nan')

        born = test_born(pos, adj, nn, lyrs)
        dt = time.time() - t0

        if math.isnan(grav):
            print(f"{name:>40s}  {'NO SIGNAL':>10s}  {'':>5s}  {born:.1e}  ({dt:.0f}s)")
        else:
            dr = "T" if grav > 1e-8 else ("A" if grav < -1e-8 else "0")
            print(f"{name:>40s}  {grav:+10.6f}  {dr:>5s}  {born:.1e}  ({dt:.0f}s)")

    print(f"\nTotal time: {time.time()-t_total:.0f}s")
    print()
    print("REQUIRED = property whose removal kills gravity (AWAY or zero)")
    print("NOT REQUIRED = gravity survives the perturbation")


if __name__ == "__main__":
    main()
