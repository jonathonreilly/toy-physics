#!/usr/bin/env python3
"""Fixed-mass causal-field distance-law verification.

This is the stricter version of the causal-field distance test:

* the source geometry is selected with a fixed mass count in a fixed mid-layer
* the same source/detector graph instances are used across all b values
* the mass window is chosen by nearest transverse y distance, so the apparent
  falloff cannot come from occupancy changes

The goal is narrow:
  - check whether the causal-field falloff survives once mass-window
    occupancy is fixed
  - compare the causal field against the retained Laplacian baseline

Review-safe claim discipline:
  - if the causal field still shows falloff, say it explicitly
  - if it flattens out, do not overstate it
  - always report that the mass count is fixed
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
from collections import defaultdict, deque


BETA = 0.8
N_SEEDS = 24
N_LAYERS = 18
NODES_PER_LAYER = 40
YZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
MASS_COUNT = 8
K_BAND = (3.0, 5.0, 7.0)
TARGET_BS = (1, 2, 3, 4, 5, 6, 7, 8, 10)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _fit_power_law(bs: list[float], shifts: list[float]) -> tuple[float, float, float] | None:
    pairs = [(b, s) for b, s in zip(bs, shifts) if b > 0 and s > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(b) for b, _ in pairs]
    ys = [math.log(s) for _, s in pairs]
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return slope, math.exp(intercept), r2


def generate_3d_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = NODES_PER_LAYER,
    yz_range: float = YZ_RANGE,
    connect_radius: float = CONNECT_RADIUS,
    rng_seed: int = 42,
):
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


def field_laplacian(positions, adj, mass_ids, iterations: int = 50):
    n = len(positions)
    undirected: dict[int, set[int]] = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)

    mass_set = set(mass_ids)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0] * n
        for i in range(n):
            if i in mass_set:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def field_causal_sum(positions, adj, mass_ids, decay: float = 0.5):
    n = len(positions)
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1

    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    field = [0.0] * n
    for m in mass_ids:
        field[m] = 1.0

    for i in order:
        if field[i] <= 0:
            continue
        out = adj.get(i, [])
        if not out:
            continue
        for j in out:
            field[j] += decay * field[i] / len(out)

    mx = max(field) if max(field) > 0 else 1.0
    return [f / mx for f in field]


def propagate(positions, adj, field, src, k):
    n = len(positions)
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
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
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += amps[i] * (cmath.exp(1j * k * act) * w / L)
    return amps


def centroid_y(amps, positions, det_list):
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def select_fixed_mass_nodes(layer_nodes, positions, target_y, count):
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count]


def measure_family(field_fn, label):
    print(f"[{label}]")
    print(
        f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift*b':>8s}  {'samples':>7s}"
    )
    print(f"  {'-' * 44}")

    by_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    mass_counts: list[int] = []

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_dag(rng_seed=seed * 17 + 3)
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        ys = [positions[i][1] for i in range(len(positions))]
        cy = sum(ys) / len(ys)
        mid = len(layer_indices) // 2
        layer_nodes = layer_indices[mid]

        for b in TARGET_BS:
            mass_ids = select_fixed_mass_nodes(layer_nodes, positions, cy + b, MASS_COUNT)
            if len(mass_ids) != MASS_COUNT:
                continue
            mass_counts.append(len(mass_ids))

            field = field_fn(positions, adj, mass_ids)
            free_field = [0.0] * len(positions)
            deltas = []
            for k in K_BAND:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_field, src, k)
                deltas.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
            if deltas:
                by_b[b].append(_mean(deltas))

    positive_bs = []
    positive_shifts = []
    for b in TARGET_BS:
        vals = by_b[b]
        if not vals:
            print(f"  {b:3d}  FAIL")
            continue
        shift = _mean(vals)
        se = _se(vals)
        t = shift / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"  {b:3d}  {shift:+8.4f}  {se:6.4f}  {t:+6.2f}  {shift * b:+8.3f}  {len(vals):7d}")
        if shift > 0.01:
            positive_bs.append(b)
            positive_shifts.append(shift)

    fit = _fit_power_law(positive_bs, positive_shifts)
    if fit is not None:
        gamma, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * b^{gamma:.3f}  (R^2={r2:.3f})")
    else:
        print("  Fit: insufficient positive points for a stable power-law fit")
    if mass_counts:
        print(f"  Mass count fixed at {mass_counts[0]} nodes per source window")
    print()


def main():
    print("=" * 78)
    print("CAUSAL FIELD FIXED-MASS VERIFICATION")
    print("  Fixed source geometry across b; fixed mass count per window")
    print("  Goal: test whether the causal-field falloff survives occupancy control")
    print("=" * 78)
    print()
    print(f"  seeds per point: {N_SEEDS}")
    print(f"  mass count: {MASS_COUNT}")
    print(f"  k-band: {K_BAND}")
    print()

    families = [
        ("Laplacian relaxed (baseline)", lambda p, a, m: field_laplacian(p, a, m)),
        ("Causal sum decay=0.5", lambda p, a, m: field_causal_sum(p, a, m, decay=0.5)),
    ]

    for label, fn in families:
        measure_family(fn, label)

    print("=" * 78)
    print("INTERPRETATION")
    print("  The key question is whether the causal-field falloff persists when")
    print("  the source window is held at a fixed count and nearest-neighbor")
    print("  geometry across b. If the causal field still falls off, the claim")
    print("  survives the occupancy control. If it flattens, the earlier result")
    print("  was likely driven by changing mass-window occupancy.")
    print("=" * 78)


if __name__ == "__main__":
    main()
