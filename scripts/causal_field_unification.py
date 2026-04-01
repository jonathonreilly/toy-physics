#!/usr/bin/env python3
"""Causal-field unification sanity pass.

This is intentionally narrow.

It checks whether the causal-field variant is still compatible with the
retained package closely enough to be worth pursuing:

1. Does the causal field produce a genuine distance dependence on the
   random 3D DAG lane once the mass count is held fixed across b?
2. Does k=0 still give zero deflection?
3. Does a fixed DAG with a causal field still preserve linearity / Born-rule
   behavior when slits are masked as amplitude masks?
4. Does the same fixed DAG keep a bounded interference visibility signal?

The script is review-safe by design:
  - it uses a fixed mass count across b
  - it compares against the Laplacian baseline
  - it keeps the Born-rule test on a true fixed DAG
  - it does not claim a full architecture fix
"""

from __future__ import annotations

import cmath
import math
import os
import random
import statistics
import sys
from collections import defaultdict, deque
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)

# Random DAG gravity sweep
N_SEEDS = 16
N_LAYERS = 18
NODES_PER_LAYER = 40
YZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
MASS_COUNT = 8
TARGET_BS = (1, 2, 3, 4, 5, 6, 7, 8, 10)

# Fixed DAG sanity checks
LAT_NX = 16
LAT_NY = 8
LAT_NZ = 4
BARrier_X = LAT_NX // 3
DET_X = LAT_NX - 1
MASS_X = LAT_NX // 2
FIELD_DECAY = 0.5


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
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
) -> tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]:
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


def field_laplacian(positions, adj, mass_ids, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_ids)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        next_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                next_field[i] = 1.0
            elif undirected.get(i):
                next_field[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = next_field
    return field


def field_causal_sum(positions, adj, mass_ids, decay=FIELD_DECAY):
    """Forward-only field with additive propagation."""
    n = len(positions)
    order = _topo_order(adj, n)
    mass_set = set(mass_ids)
    field = [0.0] * n
    for m in mass_set:
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


def propagate(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    k: float,
    blocked: set[int] | None = None,
) -> list[complex]:
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        x1, y1, z1 = positions[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x2, y2, z2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += amps[i] * cmath.exp(1j * k * act) * weight / L
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def select_mass_nodes_fixed_count(layer_nodes, positions, target_y, count):
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def measure_distance_sweep(field_fn, label: str, decay: float | None = None) -> None:
    k_band = (3.0, 5.0, 7.0)
    results: dict[float, list[float]] = {b: [] for b in TARGET_BS}

    print(f"[{label}]")
    print(f"  {'b':>3s}  {'shift':>8s}  {'SE':>6s}  {'shift*b':>8s}")
    print(f"  {'-' * 30}")

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_dag(rng_seed=seed * 17 + 3)
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        all_ys = [positions[i][1] for i in range(len(positions))]
        center_y = sum(all_ys) / len(all_ys)
        mid = len(layer_indices) // 2

        for b in TARGET_BS:
            mass_ids = select_mass_nodes_fixed_count(
                layer_indices[mid],
                positions,
                center_y + b,
                MASS_COUNT,
            )
            if not mass_ids:
                continue

            if decay is None:
                field = field_fn(positions, adj, mass_ids)
            else:
                field = field_fn(positions, adj, mass_ids, decay=decay)

            free_field = [0.0] * len(positions)
            shifts = []
            for k in K_BAND:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_field, src, k)
                shifts.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
            if shifts:
                results[b].append(_mean(shifts))

    pos_bs = []
    pos_shifts = []
    for b in TARGET_BS:
        vals = results[b]
        if not vals:
            print(f"{b:3d}  FAIL")
            continue
        avg = _mean(vals)
        se = _se(vals)
        print(f"{b:3d}  {avg:+8.4f}  {se:6.4f}  {avg * b:+8.3f}")
        if avg > 0.01:
            pos_bs.append(b)
            pos_shifts.append(avg)

    fit = _fit_power_law(pos_bs, pos_shifts)
    if fit is not None:
        gamma, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * b^{gamma:.3f}  (R^2={r2:.3f})")
    else:
        print("  Fit: insufficient positive points for a stable power-law fit")
    print()


def k0_sanity(field_fn, label: str, decay: float | None = None) -> None:
    positions, adj, layer_indices = generate_3d_dag(rng_seed=3 * 17 + 3)
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    all_ys = [positions[i][1] for i in range(len(positions))]
    center_y = sum(all_ys) / len(all_ys)
    mid = len(layer_indices) // 2
    mass_ids = select_mass_nodes_fixed_count(layer_indices[mid], positions, center_y + 5, MASS_COUNT)
    if decay is None:
        field = field_fn(positions, adj, mass_ids)
    else:
        field = field_fn(positions, adj, mass_ids, decay=decay)
    zero_field = [0.0] * len(positions)
    a_mass = propagate(positions, adj, field, src, 0.0)
    a_zero = propagate(positions, adj, zero_field, src, 0.0)
    delta = centroid_y(a_mass, positions, det_list) - centroid_y(a_zero, positions, det_list)
    print(f"  {label}: k=0 delta = {delta:+.6e}")


def build_lattice(nx: int = LAT_NX, ny: int = LAT_NY, nz: int = LAT_NZ):
    positions = {}
    node_id = {}
    adj: dict[int, list[int]] = defaultdict(list)
    idx = 0
    for x in range(nx):
        for y in range(-ny, ny + 1):
            for z in range(-nz, nz + 1):
                positions[idx] = (float(x), float(y), float(z))
                node_id[(x, y, z)] = idx
                idx += 1

    for x in range(nx - 1):
        for y in range(-ny, ny + 1):
            for z in range(-nz, nz + 1):
                src = node_id[(x, y, z)]
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        yy = y + dy
                        zz = z + dz
                        if -ny <= yy <= ny and -nz <= zz <= nz:
                            adj[src].append(node_id[(x + 1, yy, zz)])

    layers = []
    for x in range(nx):
        layers.append([node_id[(x, y, z)] for y in range(-ny, ny + 1) for z in range(-nz, nz + 1)])

    return positions, dict(adj), layers, node_id


def field_causal_sum_lattice(positions, adj, mass_ids, decay=FIELD_DECAY):
    n = len(positions)
    order = _topo_order(adj, n)
    mass_set = set(mass_ids)
    field = [0.0] * n
    for m in mass_set:
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


def _profile_visibility(profile: list[float]) -> float:
    if len(profile) < 3:
        return 0.0
    smooth = []
    for i in range(len(profile)):
        lo = max(0, i - 1)
        hi = min(len(profile), i + 2)
        window = profile[lo:hi]
        smooth.append(sum(window) / len(window))
    peaks = [smooth[i] for i in range(1, len(smooth) - 1) if smooth[i] > smooth[i - 1] and smooth[i] > smooth[i + 1]]
    troughs = [smooth[i] for i in range(1, len(smooth) - 1) if smooth[i] < smooth[i - 1] and smooth[i] < smooth[i + 1]]
    if not peaks or not troughs:
        return 0.0
    top = max(peaks)
    bottom = min(troughs)
    return (top - bottom) / (top + bottom) if top + bottom > 1e-30 else 0.0


def lattice_born_and_visibility(field_decay: float = FIELD_DECAY) -> None:
    positions, adj, layers, node_id = build_lattice()
    n = len(positions)
    src = layers[0]
    det_list = layers[-1]
    barrier_x = LAT_NX // 3
    barrier = layers[barrier_x]

    # Causal mass region downstream of the barrier.
    mass_ids = [node_id[(LAT_NX // 2, 2, z)] for z in range(-LAT_NZ, LAT_NZ + 1) if (LAT_NX // 2, 2, z) in node_id]
    field = field_causal_sum_lattice(positions, adj, mass_ids, decay=field_decay)

    # Three-slit Born-rule check.
    slit_specs = {
        "A": {(barrier_x, y, z) for y in range(-4, -1) for z in range(-LAT_NZ, LAT_NZ + 1)},
        "B": {(barrier_x, y, z) for y in range(-1, 2) for z in range(-LAT_NZ, LAT_NZ + 1)},
        "C": {(barrier_x, y, z) for y in range(2, 5) for z in range(-LAT_NZ, LAT_NZ + 1)},
    }
    barrier_all = set(barrier)
    all_slits = set().union(*slit_specs.values())
    base_blocked = barrier_all - all_slits

    def masked_prob(open_slits: str) -> float:
        open_nodes = set().union(*(slit_specs[s] for s in open_slits))
        blocked = base_blocked | (all_slits - open_nodes)
        amps = propagate(positions, adj, field, src, 5.0, blocked=blocked)
        return sum(abs(amps[d]) ** 2 for d in det_list)

    p = {}
    for r in range(4):
        for combo in combinations("ABC", r):
            key = "".join(combo)
            p[key] = masked_prob(key)

    i3 = p["ABC"] - p["AB"] - p["AC"] - p["BC"] + p["A"] + p["B"] + p["C"] - p[""]
    p_abc = max(p["ABC"], 1e-30)
    ratio = abs(i3) / p_abc

    # Direct linearity check on a two-slit companion.
    slit_a = slit_specs["A"]
    slit_b = slit_specs["C"]
    blocked_a = barrier_all - slit_a
    blocked_b = barrier_all - slit_b
    blocked_ab = barrier_all - (slit_a | slit_b)
    amps_a = propagate(positions, adj, field, src, 5.0, blocked=blocked_a)
    amps_b = propagate(positions, adj, field, src, 5.0, blocked=blocked_b)
    amps_ab = propagate(positions, adj, field, src, 5.0, blocked=blocked_ab)

    max_rel = 0.0
    for d in det_list:
        ref = max(abs(amps_ab[d]), abs(amps_a[d] + amps_b[d]))
        if ref > 1e-30:
            max_rel = max(max_rel, abs(amps_ab[d] - (amps_a[d] + amps_b[d])) / ref)

    # Two-slit visibility sanity check.
    vis_values = []
    for k in K_BAND:
        amps_coh = propagate(positions, adj, field, src, k, blocked=barrier_all - (slit_a | slit_b))
        amps_a_only = propagate(positions, adj, field, src, k, blocked=barrier_all - slit_a)
        amps_b_only = propagate(positions, adj, field, src, k, blocked=barrier_all - slit_b)
        prof_coh = [0.0] * (2 * LAT_NY + 1)
        prof_single = [0.0] * (2 * LAT_NY + 1)
        for d in det_list:
            y = int(round(positions[d][1]))
            prof_coh[y + LAT_NY] += abs(amps_coh[d]) ** 2
            prof_single[y + LAT_NY] += 0.5 * (abs(amps_a_only[d]) ** 2 + abs(amps_b_only[d]) ** 2)
        vis_coh = _profile_visibility(prof_coh)
        vis_single = _profile_visibility(prof_single)
        vis_values.append(vis_coh - vis_single)

    print("[fixed DAG sanity]")
    print(f"  Born-rule |I3|/P = {ratio:.3e}")
    print(f"  Linearity max rel err = {max_rel:.3e}")
    print(f"  Two-slit visibility gain = {_mean(vis_values):+.4f}")


def main() -> None:
    print("=" * 78)
    print("CAUSAL-FIELD UNIFICATION SANITY PASS")
    print("  Narrow check: does the causal-field variant still preserve the")
    print("  retained package closely enough to be interesting?")
    print("=" * 78)
    print()

    print("DISTANCE-LAW SANITY (3D random DAGs, fixed mass count)")
    print("  baseline Laplacian vs causal sum fields")
    print()
    k0_sanity(field_laplacian, "Laplacian baseline")
    k0_sanity(field_causal_sum, "Causal sum decay=0.5", decay=0.5)
    print()
    measure_distance_sweep(field_laplacian, "Laplacian baseline")
    measure_distance_sweep(field_causal_sum, "Causal sum decay=0.5", decay=0.5)
    measure_distance_sweep(field_causal_sum, "Causal sum decay=0.6", decay=0.6)
    print("=" * 78)
    print("FIXED-DAG SANITY (regular 3D lattice with barrier masks)")
    lattice_born_and_visibility(field_decay=FIELD_DECAY)
    print("=" * 78)
    print("INTERPRETATION")
    print("  If the causal sum keeps k=0 at zero, preserves Born linearity on a")
    print("  fixed DAG, and gives a bounded but real interference signal while")
    print("  showing a stronger b-trend than the Laplacian baseline, then it is")
    print("  a serious alternative gravity lane.")
    print("  If the fixed-mass sweep stays flat or noisy, the apparent falloff in")
    print("  the earlier causal-field runs was likely a mass-window artifact.")


if __name__ == "__main__":
    main()
