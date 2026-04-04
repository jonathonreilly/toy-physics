#!/usr/bin/env python3
"""Bounded action / geometry bridge probe.

This is a stricter replay of the action-regularity story on the same
generated DAG family.

Question:
  Does the preference between spent-delay and valley-linear shift smoothly
  as the geometry becomes more regular?

The goal is not to prove a theorem. It is to freeze a review-safe bridge
artifact that can say whether the regularity dependence is:

  - a real bridge
  - a mixed bridge
  - or still only suggestive
"""

from __future__ import annotations

import cmath
import math
import random
from collections import defaultdict, deque

BETA = 0.8
K = 5.0
N_SEEDS = 12
N_LAYERS = 20
NPL = 25
XYZ_RANGE = 8.0
CONNECT_RADIUS = 5.0
Z_MASSES = (2, 4, 6)
REGULARITIES = (0.0, 0.1, 0.2, 0.3, 0.4, 0.55, 0.7, 0.85, 0.95)


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
                y = yr * (1 - regularity) + gy * regularity + rng.gauss(0.0, jitter)
                z = zr * (1 - regularity) + gz * regularity + rng.gauss(0.0, jitter)
                idx = len(pos)
                pos.append((x, y, z))
                nodes.append(idx)
                if layers:
                    for pi in layers[-1]:
                        px, py, pz = pos[pi]
                        d = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if d <= connect_radius:
                            adj[pi].append(idx)
        layers.append(nodes)
    return pos, dict(adj), layers


def propagate(pos, adj, field, blocked, action):
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
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            if action == "valley":
                act = L * (1 - lf)
            elif action == "spent":
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0.0))
                act = dl - ret
            else:  # pragma: no cover
                raise ValueError(f"unknown action={action}")
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * K * act) * w / L
    return amps


def test_gravity(pos, adj, layers, action):
    n = len(pos)
    n_layers = len(layers)
    bl = n_layers // 3
    gl = 2 * n_layers // 3
    barrier = layers[bl]
    slits_a = [i for i in barrier if pos[i][1] >= 0.5]
    slits_b = [i for i in barrier if pos[i][1] <= -0.5]
    blocked = set(barrier) - set(slits_a + slits_b)
    det = layers[-1]

    field0 = [0.0] * n
    af = propagate(pos, adj, field0, blocked, action)
    pf = sum(abs(af[d]) ** 2 for d in det)
    if pf < 1e-30:
        return None, None, []
    zf = sum(abs(af[d]) ** 2 * pos[d][2] for d in det) / pf

    toward = 0
    total = 0
    deltas = []
    for z_mass in Z_MASSES:
        grav_layer = layers[gl]
        best = min(grav_layer, key=lambda i: abs(pos[i][2] - z_mass))
        field = [0.0] * n
        mx, my, mz = pos[best]
        for i in range(n):
            r = math.sqrt(
                (pos[i][0] - mx) ** 2 + (pos[i][1] - my) ** 2 + (pos[i][2] - mz) ** 2
            ) + 0.1
            field[i] = 0.1 / r
        am = propagate(pos, adj, field, blocked, action)
        pm = sum(abs(am[d]) ** 2 for d in det)
        if pm < 1e-30:
            continue
        zm = sum(abs(am[d]) ** 2 * pos[d][2] for d in det) / pm
        total += 1
        delta = zm - zf
        deltas.append(delta)
        if delta > 0:
            toward += 1

    return toward, total, deltas


def fit_line(xs, ys):
    if len(xs) < 2:
        return None, None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx < 1e-15:
        return None, None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = my - slope * mx
    sst = sum((y - my) ** 2 for y in ys)
    ssr = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - ssr / sst if sst > 0 else 0.0
    return slope, r2


def main():
    print("=" * 78)
    print("ACTION / GEOMETRY BRIDGE PROBE")
    print("  spent-delay vs valley-linear on the same generated DAG family")
    print("  stricter regularity interpolation than the earlier crossover replay")
    print("  bounded branch probe, not a unification theorem")
    print("=" * 78)
    print(f"  seeds={N_SEEDS}, layers={N_LAYERS}, npl={NPL}, xyz_range={XYZ_RANGE}, connect_radius={CONNECT_RADIUS}")
    print(f"  regularities={REGULARITIES}")

    rows = []
    print(f"\n{'reg':>6s}  {'valley':>12s}  {'spent':>12s}  {'delta':>9s}  {'adv':>9s}")
    print("  " + "-" * 58)

    for reg in REGULARITIES:
        v_toward = 0
        v_total = 0
        s_toward = 0
        s_total = 0
        v_deltas = []
        s_deltas = []
        for seed in range(N_SEEDS):
            pos, adj, layers = generate_dag(N_LAYERS, NPL, XYZ_RANGE, CONNECT_RADIUS, seed, reg)
            tw, tot, deltas = test_gravity(pos, adj, layers, "valley")
            if tw is not None:
                v_toward += tw
                v_total += tot
                v_deltas.extend(deltas)
            tw, tot, deltas = test_gravity(pos, adj, layers, "spent")
            if tw is not None:
                s_toward += tw
                s_total += tot
                s_deltas.extend(deltas)

        v_rate = v_toward / v_total if v_total else 0.0
        s_rate = s_toward / s_total if s_total else 0.0
        adv = v_rate - s_rate
        v_mean = sum(v_deltas) / len(v_deltas) if v_deltas else 0.0
        s_mean = sum(s_deltas) / len(s_deltas) if s_deltas else 0.0
        rows.append((reg, v_rate, s_rate, adv, v_mean, s_mean))
        print(f"{reg:6.2f}  {v_toward:2d}/{v_total:<2d} ({v_rate:6.1%})  {s_toward:2d}/{s_total:<2d} ({s_rate:6.1%})  {v_rate - s_rate:+9.1%}  {v_mean - s_mean:+9.6f}")

    regs = [r[0] for r in rows]
    advs = [r[3] for r in rows]
    slope, r2 = fit_line(regs, advs)

    zero_cross = None
    for (r0, _, _, a0, _, _), (r1, _, _, a1, _, _) in zip(rows, rows[1:]):
        if a0 == 0:
            zero_cross = r0
            break
        if a0 * a1 < 0:
            frac = abs(a0) / (abs(a0) + abs(a1))
            zero_cross = r0 + frac * (r1 - r0)
            break

    best = max(rows, key=lambda row: row[3])
    worst = min(rows, key=lambda row: row[3])

    print("\nSAFE READ")
    print(f"  best advantage at reg={best[0]:.2f}: delta={best[3]:+.1%}")
    print(f"  worst advantage at reg={worst[0]:.2f}: delta={worst[3]:+.1%}")
    if slope is not None:
        print(f"  advantage-vs-regularity fit: slope={slope:+.4f}, R²={r2:.3f}")
    if zero_cross is not None:
        print(f"  estimated crossover regularity: {zero_cross:.2f}")
    else:
        print("  estimated crossover regularity: none on this tested slice")

    print("\nINTERPRETATION")
    if zero_cross is not None and best[3] > 0 and worst[3] < 0:
        print("  - the action preference shifts with regularity on the tested family")
        print("  - the shift is real but not universal")
        print("  - safest label: mixed bridge")
    elif best[3] > 0 and worst[3] > 0:
        print("  - valley-linear dominates the tested regularity window")
        print("  - safest label: real bridge on this slice")
    else:
        print("  - the regularity dependence is present but too weak/noisy to promote")
        print("  - safest label: still suggestive")

    print("=" * 78)


if __name__ == "__main__":
    main()
