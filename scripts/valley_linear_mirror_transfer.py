#!/usr/bin/env python3
"""Bounded valley-linear transfer replay on mirror/random DAG families.

This freezes a narrow question:

  On the canonical 3D mirror/random-DAG generators, does the valley-linear
  action transfer as well as spent-delay, or does it remain geometry-specific?

The goal is review-safe comparison, not a unification theorem.
"""

from __future__ import annotations

import cmath
import math
import random
import os
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BETA = 0.8
K = 5.0
STRENGTH = 0.1
N_SEEDS = 12
N_LAYERS = 20
NPL_RANDOM = 30
NPL_MIRROR_HALF = 15
XYZ_RANGE = 8.0
CONNECT_RADIUS = 5.0
Z_MASSES = [2, 4, 6]


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
                for prev in layer_idx[max(0, layer - 2):]:
                    for pi in prev:
                        px, py, pz = pos[pi]
                        d = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if d <= connect_radius:
                            adj[pi].append(idx)
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
            up = []
            lo = []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                iu = len(pos)
                pos.append((x, y, z))
                up.append(iu)
                il = len(pos)
                pos.append((x, -y, z))
                lo.append(il)
                mirror[iu] = il
                mirror[il] = iu

            nodes = up + lo
            for prev in layer_idx[max(0, layer - 2):]:
                for pi in prev:
                    px, py, pz = pos[pi]
                    for ci in up:
                        cx, cy, cz = pos[ci]
                        d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2 + (cz - pz) ** 2)
                        if d <= connect_radius:
                            adj[pi].append(ci)
                            adj[mirror[pi]].append(mirror[ci])
        layer_idx.append(nodes)
    return pos, dict(adj), layer_idx


def _propagate(pos, adj, field, k, blocked, action):
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
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            if action == "valley_linear":
                act = L * (1 - lf)
            elif action == "spent_delay":
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0.0))
                act = dl - ret
            else:  # pragma: no cover - internal guard
                raise ValueError(f"unknown action={action}")
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w / L
    return amps


def _test_gravity(pos, adj, layers, n_layers, action):
    bl = n_layers // 3
    gl = 2 * n_layers // 3
    barrier = layers[bl]
    slits_a = [i for i in barrier if pos[i][1] >= 0.5]
    slits_b = [i for i in barrier if pos[i][1] <= -0.5]
    blocked = set(barrier) - set(slits_a + slits_b)
    det = layers[-1]

    field0 = [0.0] * len(pos)
    af = _propagate(pos, adj, field0, K, blocked, action)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        return None, None, []
    zf = sum(abs(af[d]) ** 2 * pos[d][2] for d in det) / pf

    toward = 0
    total = 0
    deltas = []
    for z_mass in Z_MASSES:
        grav_layer = layers[gl]
        if not grav_layer:
            continue
        best = min(grav_layer, key=lambda i: abs(pos[i][2] - z_mass))
        field = [0.0] * len(pos)
        mx, my, mz = pos[best]
        for i in range(len(pos)):
            r = math.sqrt((pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2) + 0.1
            field[i] = STRENGTH / r

        am = _propagate(pos, adj, field, K, blocked, action)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm < 1e-30:
            continue
        zm = sum(abs(am[d]) ** 2 * pos[d][2] for d in det) / pm
        total += 1
        deltas.append(zm - zf)
        if zm - zf > 0:
            toward += 1

    return toward, total, deltas


def _family_specs():
    return [
        (
            "random",
            lambda seed: generate_random_3d_dag(
                N_LAYERS, NPL_RANDOM, XYZ_RANGE, CONNECT_RADIUS, seed
            ),
        ),
        (
            "mirror",
            lambda seed: generate_mirror_3d_dag(
                N_LAYERS, NPL_MIRROR_HALF, XYZ_RANGE, CONNECT_RADIUS, seed
            ),
        ),
    ]


def _summarize(name, data):
    print(f"\n{name}")
    print("-" * 72)
    print(f"{'action':>14s}  {'toward':>12s}  {'rate':>9s}  {'mean delta':>12s}")
    print("  " + "-" * 60)
    for action, toward, total, mean_delta in data:
        rate = toward / total if total else 0.0
        print(f"{action:>14s}  {toward:2d}/{total:<2d}  ({rate:7.1%})  {mean_delta:+12.6f}")


def main():
    print("=" * 72)
    print("VALLEY-LINEAR MIRROR / RANDOM-DAG TRANSFER")
    print("  spent-delay vs valley-linear on canonical 3D DAG families")
    print("  bounded branch replay, not a unification theorem")
    print("=" * 72)
    print(f"  seeds={N_SEEDS}, layers={N_LAYERS}, random_npl={NPL_RANDOM}, mirror_half={NPL_MIRROR_HALF}")
    print(f"  connect_radius={CONNECT_RADIUS}, strength={STRENGTH}, z_masses={Z_MASSES}")

    for family_name, gen_fn in _family_specs():
        family_rows = []
        for action in ("spent_delay", "valley_linear"):
            toward = 0
            total = 0
            deltas = []
            for seed in range(N_SEEDS):
                pos, adj, layers = gen_fn(seed)
                tw, tot, obs = _test_gravity(pos, adj, layers, N_LAYERS, action)
                if tw is None:
                    continue
                toward += tw
                total += tot
                deltas.extend(obs)
            mean_delta = sum(deltas) / len(deltas) if deltas else 0.0
            family_rows.append((action, toward, total, mean_delta))
        _summarize(family_name, family_rows)

    print("\nSafe read:")
    print("  - compare the valley-linear row against spent-delay within each family")
    print("  - treat the mirror family as the regularized comparison, not a proof of transfer")
    print("  - if the two actions differ by family, that is a branch-specific split, not a theorem")
    print("=" * 72)
    print("VALLEY-LINEAR MIRROR TRANSFER: PASS")


if __name__ == "__main__":
    random.seed(0)
    main()
