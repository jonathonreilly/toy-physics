#!/usr/bin/env python3
"""Locality-constrained graph architecture: does distance falloff appear?

Current 3D graphs use a fixed connect_radius — every node within r
gets an edge with equal probability. This gives b-independent gravity
because all paths sample the full transverse extent equally.

Locality shells: connection probability decays with transverse distance,
creating a graph where nearby paths are dense and distant paths are sparse.
This mimics spatial locality in the continuum.

Graph architectures tested:
  1. SHARP SHELL: edges only within r, transverse distance < shell_width
     (current model — baseline)
  2. SOFT SHELL: P(connect) ~ exp(-d_transverse^2 / sigma^2)
     Gaussian decay in transverse distance
  3. LAYERED SHELL: different connect_radius for forward (dx) vs
     transverse (dy, dz) components
  4. INVERSE-SQUARE SHELL: P(connect) ~ 1/d_transverse^2
     Mimics 3D spatial locality directly

If any of these gives shift ~ 1/b: the graph topology controls
distance scaling, and locality structure is the missing ingredient.

PStack experiment: locality-shell-gravity
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def _make_dag(n_layers, nodes_per_layer, yz_range, rng_seed, connect_fn):
    """Generic DAG generator with custom connection function."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
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

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        if connect_fn(positions[prev_idx], positions[idx], rng):
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def gen_sharp(n_layers=18, npl=40, yz_range=12.0, rng_seed=42, r=3.5):
    """Baseline: sharp radius cutoff."""
    def connect(p1, p2, rng):
        dist = math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))
        return dist <= r
    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


def gen_soft_shell(n_layers=18, npl=40, yz_range=12.0, rng_seed=42,
                   forward_r=2.5, sigma_t=2.0):
    """Soft shell: Gaussian decay in transverse distance.

    P(connect) = 1 if forward_dist < forward_r AND
                 exp(-d_t^2 / sigma_t^2) > uniform(0,1)
    where d_t = sqrt(dy^2 + dz^2) is the transverse distance.
    """
    def connect(p1, p2, rng):
        dx = p2[0] - p1[0]
        if dx <= 0 or dx > 2.5:
            return False
        dy, dz = p2[1]-p1[1], p2[2]-p1[2]
        d_t = math.sqrt(dy*dy + dz*dz)
        prob = math.exp(-d_t*d_t / (sigma_t*sigma_t))
        return rng.random() < prob
    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


def gen_inverse_sq_shell(n_layers=18, npl=40, yz_range=12.0, rng_seed=42,
                         max_r=5.0, scale=2.0):
    """Inverse-square shell: P(connect) ~ scale^2 / (scale^2 + d_t^2).

    Mimics 3D spatial locality where field ~ 1/r^2.
    Forward connections always happen if dx < 2.5.
    """
    def connect(p1, p2, rng):
        dx = p2[0] - p1[0]
        if dx <= 0 or dx > 2.5:
            return False
        dy, dz = p2[1]-p1[1], p2[2]-p1[2]
        d_t = math.sqrt(dy*dy + dz*dz)
        if d_t > max_r:
            return False
        prob = scale*scale / (scale*scale + d_t*d_t)
        return rng.random() < prob
    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


def gen_exponential_shell(n_layers=18, npl=40, yz_range=12.0, rng_seed=42,
                          lam=1.0):
    """Exponential shell: P(connect) ~ exp(-lam * d_t).

    Stronger locality than Gaussian at large distances.
    """
    def connect(p1, p2, rng):
        dx = p2[0] - p1[0]
        if dx <= 0 or dx > 2.5:
            return False
        dy, dz = p2[1]-p1[1], p2[2]-p1[2]
        d_t = math.sqrt(dy*dy + dz*dz)
        prob = math.exp(-lam * d_t)
        return rng.random() < prob
    return _make_dag(n_layers, npl, yz_range, rng_seed, connect)


# ─── Physics ───

def compute_field(positions, adj, mass_idx, iterations=50):
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
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def centroid_y(amps, positions, det_list):
    total = wy = 0.0
    for d in det_list:
        p = abs(amps[d])**2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def mean_degree(adj, n):
    return sum(len(nbs) for nbs in adj.values()) / n if n > 0 else 0


def measure_b_scaling(gen_fn, n_seeds=16, **gen_kwargs):
    """Measure shift vs impact parameter b for a graph family."""
    k_band = [3.0, 5.0, 7.0]
    b_targets = [1.5, 3.0, 5.0, 7.0, 9.0]

    results = []
    avg_deg = 0

    for b_target in b_targets:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = gen_fn(rng_seed=seed*17+3, **gen_kwargs)
            if seed == 0 and b_target == b_targets[0]:
                avg_deg = mean_degree(adj, len(positions))

            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            mass = [i for i in layer_indices[mid]
                    if abs(positions[i][1] - (cy + b_target)) < 2.0]
            if len(mass) < 2:
                continue

            field = compute_field(positions, adj, mass)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                am = propagate(positions, adj, field, src, k)
                af = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(am, positions, det_list) -
                              centroid_y(af, positions, det_list))
            if shifts:
                per_seed.append(sum(shifts) / len(shifts))

        if per_seed:
            avg = sum(per_seed) / len(per_seed)
            se = math.sqrt(sum((s-avg)**2 for s in per_seed) / len(per_seed)) / math.sqrt(len(per_seed))
            results.append((b_target, avg, se))

    return results, avg_deg


def main():
    print("=" * 78)
    print("LOCALITY-CONSTRAINED GRAPH ARCHITECTURE")
    print("  Does distance falloff appear when the graph enforces locality shells?")
    print("=" * 78)
    print()

    families = [
        ("Sharp r=3.5 (baseline)", gen_sharp, {"r": 3.5}),
        ("Soft Gaussian sigma=2.0", gen_soft_shell, {"sigma_t": 2.0}),
        ("Soft Gaussian sigma=1.0", gen_soft_shell, {"sigma_t": 1.0}),
        ("Exponential lam=0.5", gen_exponential_shell, {"lam": 0.5}),
        ("Exponential lam=1.0", gen_exponential_shell, {"lam": 1.0}),
        ("Inverse-square scale=2", gen_inverse_sq_shell, {"scale": 2.0}),
        ("Inverse-square scale=1", gen_inverse_sq_shell, {"scale": 1.0}),
    ]

    for name, gen_fn, kwargs in families:
        results, deg = measure_b_scaling(gen_fn, n_seeds=16, **kwargs)

        if not results:
            print(f"  [{name}] — FAIL (no signal)")
            print()
            continue

        print(f"  [{name}] — <k>={deg:.1f}")
        print(f"  {'b':>5s}  {'shift':>8s}  {'SE':>6s}  {'shift*b':>8s}  {'shift*b²':>9s}")
        print(f"  {'-'*42}")

        for b, s, se in results:
            print(f"  {b:5.1f}  {s:+8.4f}  {se:6.4f}  {s*b:+8.3f}  {s*b*b:+9.2f}")

        # Check scaling
        positive = [(b, s) for b, s, _ in results if s > 0]
        if len(positive) >= 3:
            # shift*b constant → 1/b
            products = [s*b for b, s in positive]
            mean_p = sum(products) / len(products)
            cv_1b = (max(products) - min(products)) / mean_p if mean_p > 0 else 999

            # shift constant → b-independent
            shifts = [s for _, s in positive]
            mean_s = sum(shifts) / len(shifts)
            cv_flat = (max(shifts) - min(shifts)) / mean_s if mean_s > 0 else 999

            # shift*b^2 constant → 1/b^2
            products2 = [s*b*b for b, s in positive]
            mean_p2 = sum(products2) / len(products2)
            cv_1b2 = (max(products2) - min(products2)) / mean_p2 if mean_p2 > 0 else 999

            best = min((cv_flat, "FLAT (b-indep)"), (cv_1b, "1/b"), (cv_1b2, "1/b²"))
            print(f"  → Best fit: {best[1]} (CV={best[0]:.2f})")
            if best[0] < 0.4:
                print(f"  ★ DISTANCE SCALING DETECTED: {best[1]}")
        print()

    print("=" * 78)
    print("INTERPRETATION:")
    print("  FLAT: graph topology doesn't enforce distance scaling")
    print("  1/b:  Newtonian-like falloff from locality structure")
    print("  1/b²: steeper falloff from strong locality")
    print("=" * 78)


if __name__ == "__main__":
    main()
