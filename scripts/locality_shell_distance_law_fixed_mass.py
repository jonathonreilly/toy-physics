#!/usr/bin/env python3
"""Locality-shell distance-law diagnostic with fixed mass count.

Goal:
  Test whether explicit locality shells in the graph architecture can
  recover anything closer to a 1/b gravity falloff.

Review-safe discipline:
  - Keep source/detector geometry fixed for the run family.
  - Keep the mass count fixed across the impact-parameter sweep.
  - Only the mass-center target b changes.

Families tested:
  - Sharp radius cutoff baseline
  - Soft Gaussian shell
  - Exponential shell
  - Inverse-square shell

If all sufficiently connected families remain effectively flat in b,
that is evidence that distance-law failure is structural to the
path-sum DAG model rather than just a graph-family artifact.
"""

from __future__ import annotations

import cmath
import math
import random
from collections import defaultdict, deque

BETA = 0.8
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16
N_LAYERS = 18
NODES_PER_LAYER = 40
YZ_RANGE = 12.0
FORWARD_WINDOW = 2.5
TARGET_BS = (1.5, 3.0, 5.0, 7.0, 9.0)
MASS_COUNT = 8
MEAN_OFFSET_TOL = 1.25


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


def _make_dag(n_layers: int, npl: int, yz_range: float, rng_seed: int, connect_fn):
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        if connect_fn(positions[prev_idx], positions[idx], rng):
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def gen_sharp(n_layers=N_LAYERS, npl=NODES_PER_LAYER, yz_range=YZ_RANGE,
              rng_seed=42, r=3.5):
    def connect(p1, p2, rng):
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
        return dist <= r

    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


def gen_gaussian_shell(n_layers=N_LAYERS, npl=NODES_PER_LAYER, yz_range=YZ_RANGE,
                       rng_seed=42, sigma=2.0):
    def connect(p1, p2, rng):
        dx = p2[0] - p1[0]
        if dx <= 0 or dx > FORWARD_WINDOW:
            return False
        dy, dz = p2[1] - p1[1], p2[2] - p1[2]
        d_t = math.sqrt(dy * dy + dz * dz)
        return rng.random() < math.exp(-(d_t * d_t) / (sigma * sigma))

    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


def gen_exponential_shell(n_layers=N_LAYERS, npl=NODES_PER_LAYER, yz_range=YZ_RANGE,
                          rng_seed=42, lam=1.0):
    def connect(p1, p2, rng):
        dx = p2[0] - p1[0]
        if dx <= 0 or dx > FORWARD_WINDOW:
            return False
        dy, dz = p2[1] - p1[1], p2[2] - p1[2]
        d_t = math.sqrt(dy * dy + dz * dz)
        return rng.random() < math.exp(-lam * d_t)

    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


def gen_inverse_square_shell(n_layers=N_LAYERS, npl=NODES_PER_LAYER, yz_range=YZ_RANGE,
                             rng_seed=42, scale=2.0, max_r=5.0):
    def connect(p1, p2, rng):
        dx = p2[0] - p1[0]
        if dx <= 0 or dx > FORWARD_WINDOW:
            return False
        dy, dz = p2[1] - p1[1], p2[2] - p1[2]
        d_t = math.sqrt(dy * dy + dz * dz)
        if d_t > max_r:
            return False
        prob = (scale * scale) / (scale * scale + d_t * d_t)
        return rng.random() < prob

    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


def compute_field(positions, adj, mass_idx, iterations: int = 50):
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


def propagate(positions, adj, field, src, k):
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        x1, y1, z1 = positions[i]
        for j in adj.get(i, []):
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
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def mean_degree(adj, n):
    return sum(len(nbs) for nbs in adj.values()) / n if n > 0 else 0.0


def select_mass_nodes(layer_nodes, positions, center_y, target_b, mass_count):
    """Select a fixed-count same-side mass block near the desired impact parameter."""
    target_y = center_y + target_b
    same_side = [i for i in layer_nodes if positions[i][1] >= center_y]
    ordered = sorted(same_side, key=lambda i: positions[i][1])
    if len(ordered) < mass_count:
        return []

    best_nodes = []
    best_score = None
    for start in range(len(ordered) - mass_count + 1):
        cand = ordered[start:start + mass_count]
        ys = [positions[i][1] for i in cand]
        mean_y = sum(ys) / len(ys)
        spread = math.sqrt(sum((y - mean_y) ** 2 for y in ys) / len(ys)) if len(ys) > 1 else 0.0
        score = (
            abs(mean_y - target_y),
            max(abs(y - target_y) for y in ys),
            spread,
        )
        if best_score is None or score < best_score:
            best_score = score
            best_nodes = cand

    if not best_nodes:
        return []

    mean_offset = sum(positions[i][1] for i in best_nodes) / len(best_nodes) - center_y
    if abs(mean_offset - target_b) > MEAN_OFFSET_TOL:
        return []

    return best_nodes


def paired_seed_delta(positions, adj, src, det_list, mass_nodes):
    field_with = compute_field(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)

    deltas = []
    for k in K_BAND:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)
        y_with = centroid_y(amps_with, positions, det_list)
        y_without = centroid_y(amps_without, positions, det_list)
        deltas.append(y_with - y_without)

    return sum(deltas) / len(deltas) if deltas else None


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


def run_family(name, gen_fn, gen_kwargs):
    mean_deg = None

    print(f"{'b':>5s}  {'shift':>8s}  {'SE':>6s}  {'t':>6s}  {'shift*b':>9s}  {'shift*b²':>10s}  {'n_ok':>5s}")
    print(f"{'-' * 68}")

    bs = []
    means = []

    for b_target in TARGET_BS:
        vals = []
        for seed in range(N_SEEDS):
            positions, adj, layer_indices = gen_fn(rng_seed=seed * 17 + 3, **gen_kwargs)
            if seed == 0 and b_target == TARGET_BS[0] and mean_deg is None:
                mean_deg = mean_degree(adj, len(positions))

            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            center_y = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            mass_nodes = select_mass_nodes(layer_indices[mid], positions, center_y, b_target, MASS_COUNT)
            if len(mass_nodes) != MASS_COUNT:
                continue

            delta = paired_seed_delta(positions, adj, src, det_list, mass_nodes)
            if delta is not None:
                vals.append(delta)

        if not vals:
            print(f"{b_target:5.1f}  FAIL")
            continue

        avg = sum(vals) / len(vals)
        se = math.sqrt(sum((v - avg) ** 2 for v in vals) / len(vals)) / math.sqrt(len(vals)) if len(vals) > 1 else 0.0
        t = avg / se if se > 1e-10 else 0.0
        print(f"{b_target:5.1f}  {avg:+8.4f}  {se:6.4f}  {t:+6.2f}  {avg * b_target:+9.4f}  {avg * b_target * b_target:+10.4f}  {len(vals):5d}")
        bs.append(b_target)
        means.append(avg)

    fit = fit_power_law(bs, means)
    print()
    if fit is None:
        print("Power-law fit unavailable (need >= 3 positive mean shifts).")
    else:
        alpha, coeff, r2 = fit
        print(f"Power-law fit: shift ~= {coeff:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")
        if abs(alpha + 1) < 0.3:
            print("Interpretation: consistent with ~1/b falloff.")
        elif abs(alpha) < 0.2:
            print("Interpretation: effectively flat/topological.")
        else:
            print("Interpretation: nontrivial power law, but not clean 1/b.")
    print()

    return mean_deg


def main():
    print("=" * 78)
    print("LOCALITY-SHELL DISTANCE LAW: FIXED MASS COUNT")
    print("  Review-safe diagnostic: mass count fixed across b, source geometry fixed")
    print("=" * 78)
    print()

    # Sanity check: no gravity at k=0.
    positions, adj, layer_indices = gen_sharp(rng_seed=5)
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    all_ys = [positions[i][1] for i in range(len(positions))]
    center_y = sum(all_ys) / len(all_ys)
    mass_nodes = select_mass_nodes(layer_indices[len(layer_indices) // 2], positions, center_y, 5.0, MASS_COUNT)
    if mass_nodes and det_list:
        field = compute_field(positions, adj, mass_nodes)
        field0 = [0.0] * len(positions)
        am = propagate(positions, adj, field, src, 0.0)
        af = propagate(positions, adj, field0, src, 0.0)
        delta0 = centroid_y(am, positions, det_list) - centroid_y(af, positions, det_list)
        print(f"SANITY CHECK: k=0 delta = {delta0:+.6e} (should be ~0)")
    print()

    families = [
        ("Sharp baseline", gen_sharp, {"r": 3.5}),
        ("Gaussian sigma=2.0", gen_gaussian_shell, {"sigma": 2.0}),
        ("Gaussian sigma=1.0", gen_gaussian_shell, {"sigma": 1.0}),
        ("Exponential lam=0.5", gen_exponential_shell, {"lam": 0.5}),
        ("Exponential lam=1.0", gen_exponential_shell, {"lam": 1.0}),
        ("Inverse-square scale=2.0", gen_inverse_square_shell, {"scale": 2.0}),
        ("Inverse-square scale=1.0", gen_inverse_square_shell, {"scale": 1.0}),
    ]

    for name, gen_fn, kwargs in families:
        deg = run_family(name, gen_fn, kwargs)
        if deg is not None:
            print(f"  [family mean degree: {deg:.1f}]")
            print()

    print("=" * 78)
    print("INTERPRETATION")
    print("  Flat: distance falloff is structural to the DAG path ensemble.")
    print("  1/b:  locality shells restore Newtonian-like falloff.")
    print("  1/b²: stronger locality than needed for Newtonian scaling.")
    print("=" * 78)


if __name__ == "__main__":
    main()
