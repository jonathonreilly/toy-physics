#!/usr/bin/env python3
"""Test the dimensional scaling law: alpha = (d-1)/2.

Prediction: mass scaling exponent alpha depends on spatial dimension d:
  d=1 (2D): alpha = 0.0  (threshold)    ← confirmed
  d=2 (3D): alpha = 0.5  (sqrt M)       ← confirmed (0.52)
  d=3 (4D): alpha = 1.0  (F ~ M)        ← confirmed (1.07)
  d=4 (5D): alpha = 1.5  (F ~ M^1.5)    ← PREDICTION

This script tests all four dimensions with matched parameters for a
clean comparison, then fits the formula.

PStack experiment: dimensional-scaling-law
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque

BETA = 0.8


def generate_nd_modular_dag(d_spatial, n_layers=12, nodes_per_layer=25,
                            spatial_range=8.0, connect_radius=None,
                            rng_seed=42, gap=5.0, crosslink_prob=0.02):
    """Generate a causal DAG with d_spatial transverse dimensions.

    d_spatial=1: 2D (x, y)
    d_spatial=2: 3D (x, y, z)
    d_spatial=3: 4D (x, y, z, w)
    d_spatial=4: 5D (x, y, z, w, v)

    Channel separation in y only. All other transverse dims are uniform.
    """
    # Scale connect_radius with dimension to maintain similar connectivity
    if connect_radius is None:
        connect_radius = 2.5 + 0.5 * d_spatial  # 3.0, 3.5, 4.0, 4.5

    rng = random.Random(rng_seed)
    positions = []  # list of tuples, length 1 + d_spatial
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            pos = tuple([x] + [0.0] * d_spatial)
            positions.append(pos)
            layer_nodes.append(len(positions) - 1)
        else:
            for node_i in range(nodes_per_layer):
                coords = [x]
                # y-coordinate (channel-separated post-barrier)
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, spatial_range)
                    else:
                        y = rng.uniform(-spatial_range, -gap / 2)
                else:
                    y = rng.uniform(-spatial_range, spatial_range)
                coords.append(y)
                # Remaining transverse dimensions (uniform)
                for _ in range(d_spatial - 1):
                    coords.append(rng.uniform(-spatial_range, spatial_range))

                idx = len(positions)
                positions.append(tuple(coords))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        p = positions[prev_idx]
                        dist = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], p)))
                        if use_channels and layer > barrier_layer and round(p[0]) > barrier_layer:
                            same_ch = (y * p[1] > 0)
                            if same_ch and dist <= connect_radius:
                                adj[prev_idx].append(idx)
                            elif not same_ch and dist <= 2*connect_radius and rng.random() < crosslink_prob:
                                adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices


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
            L = math.sqrt(sum((a-b)**2 for a, b in zip(pi, pj)))
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
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


def measure_alpha(d_spatial, gap=5.0, n_seeds=24, n_layers=15):
    """Measure mass scaling exponent for a given spatial dimension."""
    k_band = [3.0, 5.0, 7.0]
    mass_counts = [1, 2, 3, 4, 6, 8, 10, 12, 16]

    results = []
    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = generate_nd_modular_dag(
                d_spatial=d_spatial, n_layers=n_layers, nodes_per_layer=30,
                spatial_range=8.0, rng_seed=seed*17+3, gap=gap,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            mid = len(layer_indices) // 2
            candidates = sorted(
                [i for i in layer_indices[mid] if positions[i][1] > cy + 1],
                key=lambda i: -positions[i][1]
            )
            mass_nodes = candidates[:target_n]
            if not mass_nodes:
                continue

            field = compute_field(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                amps_m = propagate(positions, adj, field, src, k)
                amps_f = propagate(positions, adj, free_f, src, k)
                shifts.append(centroid_y(amps_m, positions, det_list) -
                              centroid_y(amps_f, positions, det_list))
            if shifts:
                per_seed.append((len(mass_nodes), sum(shifts) / len(shifts)))

        if per_seed:
            actual_n = per_seed[0][0]
            vals = [v for _, v in per_seed]
            avg = sum(vals) / len(vals)
            se = math.sqrt(sum((v-avg)**2 for v in vals) / len(vals)) / math.sqrt(len(vals))
            t = avg / se if se > 1e-10 else 0
            if avg > 0:
                results.append((actual_n, avg, se, t))

    # Fit power law
    if len(results) >= 3:
        log_n = [math.log(n) for n, s, _, _ in results]
        log_s = [math.log(s) for _, s, _, _ in results]
        n_pts = len(log_n)
        sx = sum(log_n)
        sy = sum(log_s)
        sxy = sum(x*y for x, y in zip(log_n, log_s))
        sxx = sum(x*x for x in log_n)
        denom = n_pts * sxx - sx * sx
        if abs(denom) > 1e-10:
            alpha = (n_pts * sxy - sx * sy) / denom
            return alpha, results

    return None, results


def main():
    print("=" * 74)
    print("DIMENSIONAL SCALING LAW: alpha = (d-1)/2")
    print("  Testing prediction across d=1,2,3,4 spatial dimensions")
    print("  24 seeds, gap=5, N=15 layers")
    print("=" * 74)
    print()

    predictions = {1: 0.0, 2: 0.5, 3: 1.0, 4: 1.5}
    measured = {}

    for d in [1, 2, 3, 4]:
        total_dim = d + 1  # spatial + causal
        pred = predictions[d]
        print(f"  d={d} spatial ({total_dim}D total) — predicted alpha = {pred:.1f}")

        alpha, results = measure_alpha(d, gap=5.0, n_seeds=24, n_layers=15)

        if alpha is not None:
            measured[d] = alpha
            err = abs(alpha - pred)
            status = "CONFIRMED" if err < 0.2 else "CLOSE" if err < 0.4 else "OFF"
            print(f"    measured alpha = {alpha:.3f} (predicted {pred:.1f}, error {err:.3f}) → {status}")
            print(f"    mass scaling data:")
            for n, s, se, t in results:
                print(f"      n={n:2d}: shift={s:+.4f}, SE={se:.4f}, t={t:+.2f}")
        else:
            print(f"    FAILED (insufficient positive shifts)")
        print()

    # Fit formula: alpha = a * d + b
    if len(measured) >= 3:
        dims = sorted(measured.keys())
        alphas = [measured[d] for d in dims]

        # Linear regression: alpha = slope * d + intercept
        n = len(dims)
        sx = sum(dims)
        sy = sum(alphas)
        sxy = sum(d*a for d, a in zip(dims, alphas))
        sxx = sum(d*d for d in dims)
        denom = n * sxx - sx * sx
        if abs(denom) > 1e-10:
            slope = (n * sxy - sx * sy) / denom
            intercept = (sy - slope * sx) / n

            # R² (goodness of fit)
            mean_a = sy / n
            ss_tot = sum((a - mean_a)**2 for a in alphas)
            ss_res = sum((a - (slope*d + intercept))**2 for d, a in zip(dims, alphas))
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

            print("=" * 74)
            print("FIT RESULT")
            print()
            print(f"  Best fit: alpha = {slope:.3f} * d + {intercept:.3f}")
            print(f"  R² = {r2:.4f}")
            print()
            print(f"  Theory:   alpha = 0.500 * d - 0.500  [i.e. (d-1)/2]")
            print(f"  Measured: alpha = {slope:.3f} * d + {intercept:.3f}")
            print()

            print("  Dimensional table:")
            print(f"  {'d':>3s}  {'predicted':>9s}  {'measured':>9s}  {'error':>7s}")
            print(f"  {'-'*32}")
            for d in dims:
                p = (d - 1) / 2
                m = measured[d]
                print(f"  {d:3d}  {p:9.3f}  {m:9.3f}  {abs(m-p):7.3f}")

            if 4 in measured:
                print()
                print(f"  5D PREDICTION: alpha = (4-1)/2 = 1.5")
                print(f"  5D MEASURED:   alpha = {measured[4]:.3f}")
                print(f"  {'CONFIRMED' if abs(measured[4] - 1.5) < 0.3 else 'NOT CONFIRMED'}")

            print()
            print("  If alpha = (d-1)/2:")
            print("    d=1: threshold (no mass dependence)")
            print("    d=2: F ~ sqrt(M)")
            print("    d=3: F ~ M  (Newtonian!)")
            print("    d=4: F ~ M^1.5")
            print("    d→∞: increasingly super-linear")

    print("=" * 74)


if __name__ == "__main__":
    main()
