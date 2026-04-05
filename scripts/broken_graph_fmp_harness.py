#!/usr/bin/env python3
"""Broken-graph F∝M=p robustness harness.

Tests whether the F∝M = p universality class survives graph damage.
For each action power p ∈ {0.5, 1.0, 2.0}, measures F∝M on:
  1. Perfect lattice
  2. 70% edges (30% randomly deleted)
  3. 50% edges (50% randomly deleted)

If F∝M = p holds on broken graphs: the universality is REAL.
If p=1 degrades less than p≠1: Newton is the most robust class.

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
    raise SystemExit("numpy required")

BETA = 0.8
K = 5.0
STRENGTH = 5e-4
N_LAYERS = 13
HW = 4
H = 1.0
MAX_D = 2  # moderate connectivity
N_SEEDS = 4
FM_STRENGTHS = [1e-4, 5e-4, 5e-3]


def make_lattice(pos_jitter=0.0, edge_keep=1.0, seed=42):
    rng = random.Random(seed)
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
                y = iy * H + (rng.gauss(0, pos_jitter * H) if l > 0 else 0)
                z = iz * H + (rng.gauss(0, pos_jitter * H) if l > 0 else 0)
                pos.append((x, y, z))
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
                        if rng.random() > edge_keep:
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


def propagate(pos, adj, n, field, k, blocked, action_power):
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
            if lf > 0:
                act = L * (1 - lf ** action_power)
            else:
                act = L
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / (L * L)
    return amps


def measure_fm(pos, adj, n, layers, action_power):
    det = layers[-1]
    gl_nodes = layers[2 * N_LAYERS // 3]
    bl = N_LAYERS // 3
    bi = layers[bl]
    sa = [i for i in bi if pos[i][1] >= 0.5]
    sb = [i for i in bi if pos[i][1] <= -0.5]
    blocked = set(bi) - set(sa + sb)

    ff = [0.0] * n
    af = propagate(pos, adj, n, ff, K, blocked, action_power)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None
    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf

    best = min(gl_nodes, key=lambda i: abs(pos[i][2] - 3))
    mx, my, mz = pos[best]

    m_data = []
    g_data = []
    for s in FM_STRENGTHS:
        field = [0.0] * n
        for i in range(n):
            r = math.sqrt((pos[i][0]-mx)**2 + (pos[i][1]-my)**2 + (pos[i][2]-mz)**2) + 0.1
            field[i] = s / r
        am = propagate(pos, adj, n, field, K, blocked, action_power)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s)
                g_data.append(delta)

    if len(m_data) < 3:
        return None

    lx = np.log(m_data)
    ly = np.log(g_data)
    mx_l = np.mean(lx)
    my_l = np.mean(ly)
    sxx = np.sum((lx - mx_l)**2)
    sxy = np.sum((lx - mx_l) * (ly - my_l))
    return sxy / sxx if sxx > 1e-10 else None


def main():
    t_total = time.time()

    print("=" * 65)
    print("BROKEN-GRAPH F∝M=p ROBUSTNESS HARNESS")
    print(f"  Lattice: {N_LAYERS} layers, hw={HW}, h={H}, max_d={MAX_D}")
    print(f"  Seeds: {N_SEEDS}, strengths: {FM_STRENGTHS}")
    print("=" * 65)

    configs = [
        ("Perfect lattice", 0.0, 1.0),
        ("Broken (70% edges, 0.3h jitter)", 0.3, 0.7),
        ("Very broken (50% edges, 0.5h jitter)", 0.5, 0.5),
    ]

    for config_name, jitter, keep in configs:
        print(f"\n  {config_name}:")
        for action_p in [0.5, 1.0, 2.0]:
            fm_values = []
            for seed in range(N_SEEDS):
                pos, adj, n, layers, nmap = make_lattice(jitter, keep, seed)
                fm = measure_fm(pos, adj, n, layers, action_p)
                if fm is not None:
                    fm_values.append(fm)

            if fm_values:
                mean_fm = np.mean(fm_values)
                std_fm = np.std(fm_values) if len(fm_values) > 1 else 0
                error = abs(mean_fm - action_p)
                print(f"    p={action_p:.1f}: F∝M = {mean_fm:.2f} ± {std_fm:.2f} "
                      f"(predicted {action_p:.1f}, error {error:.2f})")
            else:
                print(f"    p={action_p:.1f}: too few TOWARD points across seeds")

    print(f"\nTotal time: {time.time()-t_total:.0f}s")
    print()
    print("ROBUSTNESS = F∝M matches predicted p even on broken graphs")
    print("Newton (p=1) is robust if its error is smallest under damage")


if __name__ == "__main__":
    main()
