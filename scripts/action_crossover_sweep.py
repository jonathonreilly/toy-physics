#!/usr/bin/env python3
"""Frozen action crossover sweep: spent-delay vs valley-linear on DAGs
with tunable regularity.

regularity=0: random node placement
regularity=1: grid node placement (lattice-like)
Intermediate: linear interpolation.

Tests both actions at each regularity level across multiple seeds.
"""

from __future__ import annotations
import math
import cmath
import random
import time
from collections import defaultdict, deque

BETA = 0.8
K = 5.0
N_SEEDS = 12
STRENGTH = 0.1


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


def generate_dag(n_layers, npl, xyz_range, connect_radius, seed, regularity):
    rng = random.Random(seed)
    pos = []
    adj = defaultdict(list)
    layers = []
    grid_side = int(math.ceil(math.sqrt(npl)))
    spacing = 2 * xyz_range / (grid_side + 1)

    for layer in range(n_layers):
        x = float(layer)
        nodes = []
        if layer == 0:
            pos.append((x, 0.0, 0.0))
            nodes.append(len(pos) - 1)
        else:
            gi = 0
            for _ in range(npl):
                yr = rng.uniform(-xyz_range, xyz_range)
                zr = rng.uniform(-xyz_range, xyz_range)
                gy = -xyz_range + spacing * (gi % grid_side + 1)
                gz = -xyz_range + spacing * (gi // grid_side + 1)
                gi += 1
                jitter = 0.1 * (1 - regularity) + 0.01
                y = yr * (1 - regularity) + gy * regularity + rng.gauss(0, jitter)
                z = zr * (1 - regularity) + gz * regularity + rng.gauss(0, jitter)
                idx = len(pos)
                pos.append((x, y, z))
                nodes.append(idx)
                if layers:
                    for pi in layers[-1]:
                        px, py, pz = pos[pi]
                        d = math.sqrt((x - px)**2 + (y - py)**2 + (z - pz)**2)
                        if d <= connect_radius:
                            adj[pi].append(idx)
        layers.append(nodes)
    return pos, dict(adj), layers


def propagate(pos, adj, field, k, blocked, action):
    n = len(pos)
    order = _topo_order(adj, n)
    amps = [0j] * n
    amps[0] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = pos[i]
            x2, y2, z2 = pos[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            if action == 'valley':
                act = L * (1 - lf)
            else:
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl*dl - L*L, 0))
                act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def test_gravity(pos, adj, layers, n_layers, action):
    n = len(pos)
    bl = n_layers // 3
    gl = 2 * n_layers // 3
    barrier = layers[bl]
    sa = [i for i in barrier if pos[i][1] >= 0.5]
    sb = [i for i in barrier if pos[i][1] <= -0.5]
    blocked = set(barrier) - set(sa + sb)
    det = layers[-1]
    ff = [0.0] * n
    af = propagate(pos, adj, ff, K, blocked, action)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None, None
    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf
    tw = 0
    tot = 0
    for z_mass in [2, 4, 6]:
        grav_layer = layers[gl]
        if not grav_layer:
            continue
        best = min(grav_layer, key=lambda i: abs(pos[i][2] - z_mass))
        field = [0.0] * n
        mx, my, mz = pos[best]
        for i in range(n):
            r = math.sqrt((pos[i][0]-mx)**2 + (pos[i][1]-my)**2 + (pos[i][2]-mz)**2) + 0.1
            field[i] = STRENGTH / r
        am = propagate(pos, adj, field, K, blocked, action)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            tot += 1
            if zm - zf > 0:
                tw += 1
    return tw, tot


def main():
    print("=" * 60)
    print("ACTION CROSSOVER SWEEP")
    print("  Spent-delay vs valley-linear at tunable regularity")
    print("=" * 60)

    n_layers = 20
    npl = 25
    xyz_range = 8.0
    connect_radius = 5.0

    print(f"\n  {'reg':>5s}  {'valley':>12s}  {'spent':>12s}  {'delta':>8s}")
    print("  " + "-" * 45)

    for reg in [0.0, 0.2, 0.4, 0.6, 0.8, 0.95]:
        v_tw = 0; v_tot = 0; s_tw = 0; s_tot = 0
        for seed in range(N_SEEDS):
            pos, adj, layers = generate_dag(n_layers, npl, xyz_range,
                                             connect_radius, seed, reg)
            tw, tot = test_gravity(pos, adj, layers, n_layers, 'valley')
            if tw is not None:
                v_tw += tw; v_tot += tot
            tw, tot = test_gravity(pos, adj, layers, n_layers, 'spent')
            if tw is not None:
                s_tw += tw; s_tot += tot

        v_r = v_tw / v_tot if v_tot else 0
        s_r = s_tw / s_tot if s_tot else 0
        delta = v_r - s_r
        print(f"  {reg:5.2f}  {v_tw:2d}/{v_tot:2d} ({v_r:4.0%})  "
              f"{s_tw:2d}/{s_tot:2d} ({s_r:4.0%})  {delta:+5.0%}")


if __name__ == "__main__":
    main()
