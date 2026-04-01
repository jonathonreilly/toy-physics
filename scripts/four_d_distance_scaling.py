#!/usr/bin/env python3
"""4D distance-law test on modular causal DAGs.

Question:
  Does the retained 4D modular family develop a 1/b-like falloff in the
  gravitational deflection, or does the signal stay effectively flat/topological?

Method:
  - Use the corrected 4D propagator on the retained modular family.
  - Sweep impact parameter b for gap=5 and gap=3.
  - Use paired per-seed deltas: y_with_mass - y_free.
  - Include a k=0 sanity check (must be identically zero).
  - Fit shift ~ b^alpha on positive mean shifts.

PStack experiment: four-d-distance-scaling
"""

from __future__ import annotations

import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16
N_LAYERS = 12
NODES_PER_LAYER = 25
SPATIAL_RANGE = 8.0
CONNECT_RADIUS = 4.5
GAPS = (5.0, 3.0)
TARGET_BS = (1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)
MASS_COUNT = 8
MEAN_OFFSET_TOL = 1.0


def generate_4d_modular_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = NODES_PER_LAYER,
    spatial_range: float = SPATIAL_RANGE,
    connect_radius: float = CONNECT_RADIUS,
    rng_seed: int = 42,
    gap: float = 5.0,
    crosslink_prob: float = 0.02,
):
    """4D causal DAG: x is the causal axis, y is the slit axis, z/w are transverse."""
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float, float]] = []
    adj = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            positions.append((x, 0.0, 0.0, 0.0))
            layer_nodes.append(0)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-spatial_range, spatial_range)
                w = rng.uniform(-spatial_range, spatial_range)
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, spatial_range)
                    else:
                        y = rng.uniform(-spatial_range, -gap / 2)
                else:
                    y = rng.uniform(-spatial_range, spatial_range)

                idx = len(positions)
                positions.append((x, y, z, w))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz, pw = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 + (w - pw) ** 2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                                    adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def compute_field_4d(positions, adj, mass_idx, iterations: int = 50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)

    ms = set(mass_idx)
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


def propagate_4d(positions, adj, field, src, k, blocked=None):
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
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1, w1 = positions[i]
            x2, y2, z2, w2 = positions[j]
            dx = x2 - x1
            L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2 + (w2 - w1) ** 2)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * weight / L
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


def select_mass_nodes(layer_nodes, positions, center_y, target_b, mass_count):
    """Choose a same-side y-window near the desired impact parameter."""
    target_y = center_y + target_b
    same_side = [i for i in layer_nodes if positions[i][1] >= center_y]
    ordered = sorted(same_side, key=lambda i: positions[i][1])
    if len(ordered) < mass_count:
        return []

    best_nodes: list[int] = []
    best_score: tuple[float, float, float] | None = None
    for start in range(len(ordered) - mass_count + 1):
        candidate = ordered[start:start + mass_count]
        ys = [positions[i][1] for i in candidate]
        mean_y = sum(ys) / len(ys)
        score = (
            abs(mean_y - target_y),
            max(abs(y - target_y) for y in ys),
            math.sqrt(sum((y - mean_y) ** 2 for y in ys) / len(ys)) if len(ys) > 1 else 0.0,
        )
        if best_score is None or score < best_score:
            best_score = score
            best_nodes = candidate

    if not best_nodes:
        return []
    mean_offset = sum(positions[i][1] for i in best_nodes) / len(best_nodes) - center_y
    if abs(mean_offset - target_b) > MEAN_OFFSET_TOL:
        return []
    return best_nodes


def paired_seed_delta(positions, adj, src, det_list, mass_nodes):
    """K-averaged paired delta for one seed and one mass placement."""
    field_with = compute_field_4d(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)

    seed_deltas = []
    for k in K_BAND:
        amps_with = propagate_4d(positions, adj, field_with, src, k)
        amps_without = propagate_4d(positions, adj, field_without, src, k)

        probs_with = {d: abs(amps_with[d]) ** 2 for d in det_list}
        probs_without = {d: abs(amps_without[d]) ** 2 for d in det_list}
        tot_with = sum(probs_with.values())
        tot_without = sum(probs_without.values())
        if tot_with <= 1e-30 or tot_without <= 1e-30:
            continue

        y_with = sum(positions[d][1] * p for d, p in probs_with.items()) / tot_with
        y_without = sum(positions[d][1] * p for d, p in probs_without.items()) / tot_without
        seed_deltas.append(y_with - y_without)

    if not seed_deltas:
        return None
    return sum(seed_deltas) / len(seed_deltas)


def fit_power_law(bs, deltas):
    pairs = [(b, d) for b, d in zip(bs, deltas) if b > 0 and d > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(b) for b, _ in pairs]
    ys = [math.log(d) for _, d in pairs]
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


def run_gap(gap: float):
    print(f"[4D modular gap={gap}]")
    print(f"{'b':>6s}  {'shift':>10s}  {'SE':>8s}  {'t':>6s}  {'shift*b':>10s}  {'shift*b^2':>11s}  {'n_ok':>5s}")
    print(f"{'-' * 70}")

    per_b_means: list[float] = []
    per_b_values: list[list[float]] = []

    for target_b in TARGET_BS:
        vals = []
        for seed in range(N_SEEDS):
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=NODES_PER_LAYER,
                spatial_range=SPATIAL_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed * 13 + 5,
                gap=gap,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            center_y = sum(all_ys) / len(all_ys)
            grav_idx = 2 * len(layer_indices) // 3
            mass_nodes = select_mass_nodes(
                layer_indices[grav_idx],
                positions,
                center_y,
                target_b,
                MASS_COUNT,
            )
            if not mass_nodes:
                continue

            delta = paired_seed_delta(positions, adj, src, det_list, mass_nodes)
            if delta is not None:
                vals.append(delta)

        if not vals:
            print(f"{target_b:6.2f}  FAIL")
            continue

        mean = sum(vals) / len(vals)
        if len(vals) > 1:
            se = math.sqrt(sum((v - mean) ** 2 for v in vals) / len(vals)) / math.sqrt(len(vals))
        else:
            se = 0.0
        t = mean / se if se > 1e-10 else 0.0
        print(f"{target_b:6.2f}  {mean:+10.4f}  {se:8.4f}  {t:+6.2f}  {mean * target_b:+10.4f}  {mean * target_b * target_b:+11.4f}  {len(vals):5d}")
        per_b_means.append(mean)
        per_b_values.append(vals)

    fit = fit_power_law([b for b, vals in zip(TARGET_BS, per_b_values) if vals],
                        [sum(vals) / len(vals) for vals in per_b_values if vals])
    print()
    if fit is None:
        print("Power-law fit unavailable (need at least 3 positive mean shifts).")
    else:
        alpha, coeff, r2 = fit
        print(f"Power-law fit: shift ~= {coeff:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
        if abs(alpha + 1) < 0.3:
            print("Interpretation: consistent with ~1/b falloff.")
        elif abs(alpha) < 0.2:
            print("Interpretation: effectively flat/topological.")
        else:
            print("Interpretation: nontrivial power law, but not clean 1/b.")


def k0_sanity():
    positions, adj, layer_indices = generate_4d_modular_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=NODES_PER_LAYER,
        spatial_range=SPATIAL_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=5,
        gap=5.0,
    )
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    all_ys = [positions[i][1] for i in range(len(positions))]
    center_y = sum(all_ys) / len(all_ys)
    grav_idx = 2 * len(layer_indices) // 3
    grav_layer = layer_indices[grav_idx]

    mass_nodes = []
    for target_b in (3.0, 4.0, 5.0, 6.0):
        mass_nodes = select_mass_nodes(grav_layer, positions, center_y, target_b, min(4, MASS_COUNT))
        if mass_nodes:
            break
    if not mass_nodes:
        upper = sorted([i for i in grav_layer if positions[i][1] >= center_y], key=lambda i: positions[i][1])
        mass_nodes = upper[: min(4, len(upper))]
    if not mass_nodes:
        print("k=0 sanity: unable to select a test mass window")
        return

    field = compute_field_4d(positions, adj, mass_nodes)
    free_field = [0.0] * len(positions)
    amps_m = propagate_4d(positions, adj, field, src, 0.0)
    amps_f = propagate_4d(positions, adj, free_field, src, 0.0)
    y_m = centroid_y(amps_m, positions, det_list)
    y_f = centroid_y(amps_f, positions, det_list)
    print(f"k=0 sanity: delta = {y_m - y_f:+.6e} (should be ~0)")


def main():
    print("=" * 74)
    print("4D DISTANCE SCALING")
    print("  Does the modular 4D lane develop a 1/b-like falloff?")
    print("  Paired per-seed deltas; gap=5 is the main candidate, gap=3 control.")
    print("=" * 74)
    print()

    print("SANITY CHECK:")
    k0_sanity()
    print()

    for gap in GAPS:
        run_gap(gap)
        print()

    print("=" * 74)
    print("CONCLUSION")
    print("=" * 74)
    print("  If the exponent stays near 0, the 4D retained lane is still")
    print("  effectively flat/topological in b.")
    print("  If it drifts toward -1, we have a genuine 1/b-like falloff.")
    print("  The paired per-seed deltas above are the main evidence.")
    print("=" * 74)


if __name__ == "__main__":
    main()
