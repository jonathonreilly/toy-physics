#!/usr/bin/env python3
"""Control audit for the N=80 smart-prune emergence claim.

Goal
----
Separate the true adaptive-quantile baseline from the D/degree smart-prune
variant and the detector-protection variant on the same generator/settings.

This is a rerun-style audit, not a new claim:
  - same uniform 3D generator as the merged smart-prune result
  - same prune quantile / iteration budget
  - same decoherence metric
  - same seed count across all variants
  - explicit comparison against the unpruned baseline

The key question is whether the N=80 improvement survives when the baseline
is the real adaptive-quantile rule, not the D/degree variant in disguise.
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
from collections import defaultdict, deque


BETA = 0.8
N_YBINS = 8
LAM = 10.0
K_BAND = (3.0, 5.0, 7.0)

N_SEEDS = 16
N_LAYERS_LIST = [40, 50, 60, 80]
NPL = 30
YZ_RANGE = 10.0
CONNECT_RADIUS = 3.5
PRUNE_QUANTILE = 0.10
MAX_ITER = 3


def gen_3d(n_layers: int, npl: int = NPL, yz_range: float = YZ_RANGE, r: float = CONNECT_RADIUS, rng_seed: int = 42):
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layers: list[list[int]] = []
    for layer in range(n_layers):
        x = float(layer)
        nodes: list[int] = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            nodes.append(len(positions) - 1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                nodes.append(idx)
                for prev_layer in layers[max(0, layer - 2) :]:
                    for pi in prev_layer:
                        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r:
                            adj[pi].append(idx)
        layers.append(nodes)
    return positions, dict(adj), layers


def propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        pi = positions[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pj = positions[j]
            dx = pj[0] - pi[0]
            L = math.sqrt(sum((a - b) ** 2 for a, b in zip(pi, pj)))
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def compute_field(positions, adj, mass_ids, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_ids)
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


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0
    y_min, y_max = min(ys) - 0.01, max(ys) + 0.01
    bw = (y_max - y_min) / N_YBINS
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS - 1, int((positions[m][1] - y_min) / bw)))
        ba[b] += amps_a[m]
        bb[b] += amps_b[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    d = sum(abs(a) ** 2 for a in ba) + sum(abs(b) ** 2 for b in bb)
    return S / d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1] * amps_a[d2].conjugate()
                + amps_b[d1] * amps_b[d2].conjugate()
                + D * amps_a[d1] * amps_b[d2].conjugate()
                + D * amps_b[d1] * amps_a[d2].conjugate()
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def _measure_decoherence(positions, adj, layer_indices):
    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    if not det_list or n_layers < 7:
        return math.nan

    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return math.nan

    blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = blocked | set(slit_b)
    blocked_b = blocked | set(slit_a)

    bath_mass = []
    for li in range(bl_idx + 1, min(n_layers, bl_idx + 3)):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= 3:
                bath_mass.append(i)
    grav_idx = 2 * n_layers // 3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy + 1]
    all_mass = list(set(bath_mass) | set(grav_mass))
    field = compute_field(positions, adj, all_mass) if all_mass else [0.0] * n

    mid_nodes = [
        i
        for li in range(bl_idx + 1, n_layers - 1)
        for i in layer_indices[li]
        if i not in blocked and i not in set(det_list)
    ]
    if len(mid_nodes) < 4:
        return math.nan

    pur_list = []
    for k in K_BAND:
        aa = propagate(positions, adj, field, src, k, blocked_a)
        ab = propagate(positions, adj, field, src, k, blocked_b)
        Sn = cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM * LAM * Sn)
        pur = cl_purity(aa, ab, D, det_list)
        if not math.isnan(pur):
            pur_list.append(pur)
    return sum(pur_list) / len(pur_list) if pur_list else math.nan


def _smart_prune(positions, adj, layer_indices, quantile=PRUNE_QUANTILE, max_iter=MAX_ITER, protect_det_neighbors=False, use_degree=False):
    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)
    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return adj, 0

    base_blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = base_blocked | set(slit_b)
    det_set = set(layer_indices[-1])
    field = [0.0] * n
    current_adj = dict(adj)
    total_removed = 0

    for _ in range(max_iter):
        det_neighbors = set()
        if protect_det_neighbors:
            for i, nbs in current_adj.items():
                if any(j in det_set for j in nbs):
                    det_neighbors.add(i)

        out_deg = defaultdict(int)
        in_deg_map = defaultdict(int)
        for i, nbs in current_adj.items():
            out_deg[i] = len(nbs)
            for j in nbs:
                in_deg_map[j] += 1

        amps_a = propagate(positions, current_adj, field, layer_indices[0], 5.0, blocked_a)
        amps_b = propagate(positions, current_adj, field, layer_indices[0], 5.0, base_blocked | set(slit_a))
        node_scores = []
        for li in range(bl_idx + 1, n_layers - 1):
            for i in layer_indices[li]:
                if i in det_set or i in det_neighbors:
                    continue
                pa, pb = abs(amps_a[i]) ** 2, abs(amps_b[i]) ** 2
                total = pa + pb
                if total <= 1e-30:
                    continue
                D = abs(pa - pb) / total
                degree = out_deg.get(i, 0) + in_deg_map.get(i, 0)
                score = D / (degree + 1) if use_degree else D
                node_scores.append((i, score))
        if not node_scores:
            break

        node_scores.sort(key=lambda x: x[1])
        n_remove = max(1, int(len(node_scores) * quantile))
        remove_set = set(idx for idx, _ in node_scores[:n_remove])
        new_adj = {}
        for i, nbs in current_adj.items():
            if i in remove_set:
                continue
            filtered = [j for j in nbs if j not in remove_set]
            if filtered:
                new_adj[i] = filtered
        total_removed += len(remove_set)
        current_adj = new_adj

    return current_adj, total_removed


def _fixed_position_mass_nodes(layer_nodes, positions, target_y, count):
    ranked = sorted(layer_nodes, key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i))
    return ranked[:count] if len(ranked) >= count else []


def _active_node_set(adj, anchors=()):
    active = set(anchors)
    for i, nbs in adj.items():
        if nbs:
            active.add(i)
            active.update(nbs)
    return active


def _measure_variant(label, prune_kwargs):
    print(f"[{label}]")
    print(f"  {'N':>4s}  {'pur_cl':>8s}  {'removed':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 30}")
    for nl in N_LAYERS_LIST:
        purs = []
        removals = []
        for seed in range(N_SEEDS):
            positions, adj, layers = gen_3d(n_layers=nl, rng_seed=seed * 13 + 5)
            if prune_kwargs is None:
                adj_e = adj
                removed = 0
            else:
                adj_e, removed = _smart_prune(positions, adj, layers, **prune_kwargs)
            pur = _measure_decoherence(positions, adj_e, layers)
            if not math.isnan(pur):
                purs.append(pur)
            removals.append(removed)
        if purs:
            print(f"  {nl:4d}  {sum(purs)/len(purs):8.4f}  {sum(removals)/len(removals):8.1f}  {len(purs):4d}")
        else:
            print(f"  {nl:4d}  FAIL")
    print()


def _measure_mass_alpha(label, prune_kwargs):
    print(f"[{label}]")
    print(f"  {'n_mass':>6s}  {'shift':>8s}  {'SE':>6s}  {'n_ok':>4s}")
    print(f"  {'-' * 30}")
    mass_counts = [2, 4, 6, 8, 12, 16]
    results = []
    target_y_offset = 3.0
    for target_n in mass_counts:
        per_seed = []
        for seed in range(N_SEEDS):
            positions, adj, layers = gen_3d(n_layers=80, rng_seed=seed * 13 + 5)
            if prune_kwargs is None:
                adj_e = adj
            else:
                adj_e, _ = _smart_prune(positions, adj, layers, **prune_kwargs)

            src = layers[0]
            det_list = list(layers[-1])
            if not det_list:
                continue
            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layers) // 2
            active_nodes = _active_node_set(adj_e, anchors=src + det_list)
            layer_nodes = [
                i
                for i in layers[mid]
                if i in active_nodes and positions[i][1] > cy + 1
            ]
            ranked = _fixed_position_mass_nodes(
                layer_nodes,
                positions,
                cy + target_y_offset,
                max(mass_counts),
            )
            if len(ranked) < max(mass_counts):
                continue
            mn = ranked[:target_n]
            field = compute_field(positions, adj_e, mn)
            free_f = [0.0] * len(positions)
            shifts = []
            for k in K_BAND:
                am = propagate(positions, adj_e, field, src, k)
                af = propagate(positions, adj_e, free_f, src, k)
                shifts.append(centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append((len(mn), sum(shifts) / len(shifts)))

        if per_seed:
            vals = [v for _, v in per_seed]
            avg = sum(vals) / len(vals)
            se = statistics.stdev(vals) / math.sqrt(len(vals)) if len(vals) > 1 else 0.0
            print(f"  {target_n:6d}  {avg:+8.4f}  {se:6.4f}  {len(per_seed):4d}")
            results.append((target_n, avg))
        else:
            print(f"  {target_n:6d}  FAIL")

    alpha = None
    if len(results) == len(mass_counts) and all(avg > 0 for _, avg in results):
        log_n = [math.log(n) for n, _ in results]
        log_s = [math.log(s) for _, s in results]
        np_ = len(log_n)
        sx, sy = sum(log_n), sum(log_s)
        sxy = sum(x * y for x, y in zip(log_n, log_s))
        sxx = sum(x * x for x in log_n)
        denom = np_ * sxx - sx * sx
        if abs(denom) > 1e-10:
            alpha = (np_ * sxy - sx * sy) / denom
    if alpha is not None:
        print(f"  Alpha fit: {alpha:.3f}")
    print()
    return alpha


def main():
    print("=" * 78)
    print("SMART PRUNE CONTROL AUDIT")
    print("  true adaptive-quantile baseline vs D/degree smart prune vs detector protection")
    print("=" * 78)
    print()
    print(f"  seeds per sweep: {N_SEEDS}")
    print(f"  N layers: {N_LAYERS_LIST}")
    print(f"  prune quantile: {PRUNE_QUANTILE}")
    print(f"  max prune iterations: {MAX_ITER}")
    print(f"  k-band: {K_BAND}")
    print()

    for label, kwargs in [
        ("Uniform baseline", None),
        ("Adaptive quantile baseline", {"quantile": PRUNE_QUANTILE, "protect_det_neighbors": False, "use_degree": False}),
        ("D/degree smart prune", {"quantile": PRUNE_QUANTILE, "protect_det_neighbors": False, "use_degree": True}),
        ("Detector-protection variant", {"quantile": PRUNE_QUANTILE, "protect_det_neighbors": True, "use_degree": False}),
    ]:
        _measure_variant(label, kwargs)

    print("=" * 78)
    print("MASS-SCALING CHECK AT N=80")
    print("  Uses fixed mass position, variable count via prefixes, and surviving mass nodes only.")
    print("=" * 78)
    uniform_alpha = _measure_mass_alpha("Uniform baseline", None)
    adaptive_alpha = _measure_mass_alpha("Adaptive quantile baseline", {"quantile": PRUNE_QUANTILE, "protect_det_neighbors": False, "use_degree": False})
    smart_alpha = _measure_mass_alpha("D/degree smart prune", {"quantile": PRUNE_QUANTILE, "protect_det_neighbors": False, "use_degree": True})
    det_alpha = _measure_mass_alpha("Detector-protection variant", {"quantile": PRUNE_QUANTILE, "protect_det_neighbors": True, "use_degree": False})

    print("=" * 78)
    print("AUDIT SUMMARY")
    print(f"  Uniform baseline alpha: {'NA' if uniform_alpha is None else f'{uniform_alpha:.3f}'}")
    print(f"  Adaptive quantile alpha: {'NA' if adaptive_alpha is None else f'{adaptive_alpha:.3f}'}")
    print(f"  D/degree smart alpha: {'NA' if smart_alpha is None else f'{smart_alpha:.3f}'}")
    print(f"  Detector-protection alpha: {'NA' if det_alpha is None else f'{det_alpha:.3f}'}")
    print("  Key question: does the N=80 decoherence improvement survive when the baseline is the true adaptive-quantile rule?")
    print("=" * 78)


if __name__ == "__main__":
    main()
