#!/usr/bin/env python3
"""Causal-field mass-scaling check on retained 3D modular DAGs.

This is the bounded mass-scaling companion to the causal-field distance-law
work. The goal is narrow:

  - compare a forward-only causal field against a Laplacian relaxation
    baseline on the same retained 3D modular DAG family
  - test whether gravity-like deflection still grows with mass count
  - keep the setup honest enough that we can say if it is not yet trustworthy

The retained family here is the same 3D modular DAG lane used elsewhere in the
repo: post-barrier channel separation via `gap > 0`.

This script is intentionally conservative:
  - same graph generator for both fields
  - same mass placement rule
  - same detector-side metric
  - same k-band
  - causal field is forward-only and decays along edges, but is not normalized
    away across mass-count sweeps

If the causal field does not show a stable mass-scaling trend, the log says so
plainly.
"""

from __future__ import annotations

import math
import os
import random
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BETA = 0.8
DECAY = 0.5
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 8
N_LAYERS = 18
NODES_PER_LAYER = 40
XYZ_RANGE = 12.0
CONNECT_RADIUS = 3.5
GAP = 5.0
MASS_COUNTS = (2, 4, 6, 8, 12, 16)
MASS_LAYER_OFFSET = 2 * N_LAYERS // 3
MASS_Y_THRESHOLD = 1.0


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


def generate_3d_modular_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = NODES_PER_LAYER,
    xyz_range: float = XYZ_RANGE,
    connect_radius: float = CONNECT_RADIUS,
    rng_seed: int = 42,
    gap: float = GAP,
):
    """Generate the retained 3D modular DAG family with layer bookkeeping."""

    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float]] = []
    adj = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-xyz_range, xyz_range)
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, xyz_range)
                    else:
                        y = rng.uniform(-xyz_range, -gap / 2)
                else:
                    y = rng.uniform(-xyz_range, xyz_range)

                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = y * py > 0
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < 0.02:
                                    adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def field_laplacian(positions, adj, mass_nodes, iterations: int = 50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)

    ms = set(mass_nodes)
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


def field_causal_forward(positions, adj, mass_nodes, decay: float = DECAY):
    """Forward-only causal field.

    The field is propagated along DAG order and decays on each edge.
    Unlike the branch-distance tuning probe, we do not normalize the field
    away at the end because this script is meant to test mass scaling.
    """

    n = len(positions)
    order = _topo_order(adj, n)
    ms = set(mass_nodes)
    field = [0.0] * n
    for m in ms:
        field[m] = 1.0

    for i in order:
        if field[i] <= 0:
            continue
        out = adj.get(i, [])
        if not out:
            continue
        for j in out:
            field[j] += decay * field[i] / len(out)
    return field


def propagate(positions, adj, field, src, k):
    n = len(positions)
    order = _topo_order(adj, n)
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
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            ea = complex(math.cos(k * act), math.sin(k * act)) * weight / L
            amps[j] += amps[i] * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def _pick_mass_nodes(layer_nodes, positions, center_y, target_n):
    ordered = sorted(
        [i for i in layer_nodes if positions[i][1] > center_y + MASS_Y_THRESHOLD],
        key=lambda i: positions[i][1],
        reverse=True,
    )
    if len(ordered) < target_n:
        return []
    return ordered[:target_n]


def _seed_shift(positions, adj, src, det_list, mass_nodes, field_fn):
    field = field_fn(positions, adj, mass_nodes)
    free = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_mass = propagate(positions, adj, field, src, k)
        amps_free = propagate(positions, adj, free, src, k)
        deltas.append(
            centroid_y(amps_mass, positions, det_list)
            - centroid_y(amps_free, positions, det_list)
        )
    return _mean(deltas) if deltas else None


def _fit_alpha(counts: list[int], shifts: list[float]):
    pairs = [(n, s) for n, s in zip(counts, shifts) if s > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(n) for n, _ in pairs]
    ys = [math.log(s) for _, s in pairs]
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    alpha = (n * sxy - sx * sy) / denom
    intercept = (sy - alpha * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ys)
    ss_res = sum((y - (alpha * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return alpha, math.exp(intercept), r2


def _run_field(label: str, field_fn):
    print(f"[{label}]")
    print(f"  {'n_mass':>6s}  {'shift':>8s}  {'SE':>6s}  {'t':>5s}  {'shift/n':>8s}")
    print(f"  {'-' * 36}")

    by_count: dict[int, list[float]] = {n: [] for n in MASS_COUNTS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_3d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            xyz_range=XYZ_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 13 + 5,
            gap=GAP,
        )

        if len(layer_indices) <= MASS_LAYER_OFFSET or not layer_indices[-1]:
            continue

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        center_y = sum(p[1] for p in positions) / len(positions)
        mass_layer = layer_indices[MASS_LAYER_OFFSET]

        for target_n in MASS_COUNTS:
            mass_nodes = _pick_mass_nodes(mass_layer, positions, center_y, target_n)
            if len(mass_nodes) < target_n:
                continue
            delta = _seed_shift(positions, adj, src, det_list, mass_nodes, field_fn)
            if delta is not None:
                by_count[target_n].append(delta)

    counts = []
    shifts = []
    for target_n in MASS_COUNTS:
        vals = by_count[target_n]
        if not vals:
            print(f"  {target_n:6d}  FAIL")
            continue
        avg = _mean(vals)
        se = _se(vals)
        t = avg / se if se and math.isfinite(se) and se > 1e-12 else 0.0
        print(f"  {target_n:6d}  {avg:+8.4f}  {se:6.4f}  {t:+5.2f}  {avg/target_n:+8.4f}")
        counts.append(target_n)
        shifts.append(avg)

    fit = _fit_alpha(counts, shifts)
    if fit is not None:
        alpha, c, r2 = fit
        print(f"  Fit: shift ~= {c:.4f} * n^{alpha:.3f}  (R^2={r2:.3f})")
    else:
        print("  Fit: insufficient positive points for a stable power-law fit")
    print()
    return counts, shifts, fit


def main() -> None:
    print("=" * 78)
    print("CAUSAL FIELD MASS SCALING")
    print("  Retained 3D modular DAG family, gap=5")
    print("  Compare forward-only causal field against Laplacian relaxation")
    print("=" * 78)
    print()
    print("Setup:")
    print(f"  seeds per count: {N_SEEDS}")
    print(f"  k-band: {K_BAND}")
    print(f"  causal decay: {DECAY}")
    print(f"  graph: 3D modular DAG, N_LAYERS={N_LAYERS}, NODES_PER_LAYER={NODES_PER_LAYER}")
    print(f"  connect_radius={CONNECT_RADIUS}, gap={GAP}")
    print()

    # Quick sanity on a representative retained graph.
    positions, adj, layer_indices = generate_3d_modular_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        xyz_range=XYZ_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=5,
        gap=GAP,
    )
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    center_y = sum(p[1] for p in positions) / len(positions)
    mass_nodes = _pick_mass_nodes(layer_indices[MASS_LAYER_OFFSET], positions, center_y, 8)
    if mass_nodes:
        lap = field_laplacian(positions, adj, mass_nodes)
        causal = field_causal_forward(positions, adj, mass_nodes, decay=DECAY)
        free = [0.0] * len(positions)
        d0_lap = _seed_shift(positions, adj, src, det_list, mass_nodes, lambda *_: lap)
        d0_causal = _seed_shift(positions, adj, src, det_list, mass_nodes, lambda *_: causal)
        d0_free = _seed_shift(positions, adj, src, det_list, mass_nodes, lambda *_: free)
        print("Sanity check on representative graph:")
        print(f"  Laplacian shift: {d0_lap:+.4f}")
        print(f"  Causal shift:    {d0_causal:+.4f}")
        print(f"  Free shift:      {d0_free:+.4f}")
        print()

    lap_counts, lap_shifts, lap_fit = _run_field("Laplacian baseline", field_laplacian)
    causal_counts, causal_shifts, causal_fit = _run_field(
        f"Causal forward field (decay={DECAY})",
        lambda p, a, m: field_causal_forward(p, a, m, decay=DECAY),
    )

    print("=" * 78)
    print("SIDE-BY-SIDE SUMMARY")
    if lap_fit is not None:
        print(f"  Laplacian alpha = {lap_fit[0]:.3f} (R^2={lap_fit[2]:.3f})")
    else:
        print("  Laplacian alpha = NA")
    if causal_fit is not None:
        print(f"  Causal alpha    = {causal_fit[0]:.3f} (R^2={causal_fit[2]:.3f})")
    else:
        print("  Causal alpha    = NA")

    if lap_fit is not None and causal_fit is not None:
        if causal_fit[0] > lap_fit[0] + 0.1:
            print("  Causal field strengthens mass scaling relative to Laplacian.")
        elif causal_fit[0] < lap_fit[0] - 0.1:
            print("  Causal field weakens mass scaling relative to Laplacian.")
        else:
            print("  Causal and Laplacian mass scaling are broadly similar.")
    print()
    print("INTERPRETATION")
    print("  If the causal field shows a stable positive alpha on the retained")
    print("  modular family, then it is a credible mass-scaling candidate.")
    print("  If the fit is weak, noisy, or much smaller than the Laplacian lane,")
    print("  the causal-field idea is not yet a retained improvement.")


if __name__ == "__main__":
    main()
