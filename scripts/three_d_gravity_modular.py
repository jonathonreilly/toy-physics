#!/usr/bin/env python3
"""3D gravity on modular causal DAGs with corrected propagator.

The 2D model gives:
  - field ~ log(r), gradient ~ 1/r, deflection ~ constant (b-independent)
  - F NOT proportional to M (threshold effect)

In 3D we expect:
  - field ~ 1/r, gradient ~ 1/r^2, deflection ~ 1/b
  - Possibly F ~ M if the extra path diversity breaks the threshold

This script tests:
  1. Basic gravitational attraction on 3D DAGs (uniform + modular)
  2. Distance scaling: shift vs impact parameter b
  3. Mass scaling: shift vs number of mass nodes
  4. Paired per-seed statistics with SE for significance

Uses the full corrected propagator: 1/L^p, directional measure, field-dependent action.

PStack experiment: three-d-gravity-modular
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque
import sys

BETA = 0.8  # directional measure width (same as 2D)


# ─────────────────────────────────────────────────────────────────────
# 3D DAG generators
# ─────────────────────────────────────────────────────────────────────

def generate_3d_uniform_dag(n_layers=15, nodes_per_layer=30, yz_range=8.0,
                            connect_radius=3.5, rng_seed=42):
    """Uniform random 3D causal DAG. Nodes placed randomly in (y,z) plane per layer."""
    rng = random.Random(rng_seed)
    positions = []  # (x, y, z)
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def generate_3d_modular_dag(n_layers=15, nodes_per_layer=30, yz_range=8.0,
                            connect_radius=3.5, rng_seed=42, gap=3.0,
                            crosslink_prob=0.02):
    """3D modular DAG with channel separation in y-dimension.

    Post-barrier, nodes are placed in two y-bands:
      Upper: y in [+gap/2, +yz_range]
      Lower: y in [-yz_range, -gap/2]
    z is uniform in [-yz_range, +yz_range] for both channels.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []

    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-yz_range, yz_range)

                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, yz_range)
                    else:
                        y = rng.uniform(-yz_range, -gap / 2)
                else:
                    y = rng.uniform(-yz_range, yz_range)

                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)

                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_channel = (y * py > 0)
                            if same_channel:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                                    adj[prev_idx].append(idx)
                        else:
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


# ─────────────────────────────────────────────────────────────────────
# Physics: field, propagator, measurement
# ─────────────────────────────────────────────────────────────────────

def compute_field_3d(positions, adj, mass_idx, iterations=50):
    """Laplacian-relaxed scalar field from mass sources on undirected graph."""
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


def propagate_3d(positions, adj, field, src, k):
    """Corrected propagator on 3D graph with directional measure.

    W(i→j) = exp(i*k*S) * exp(-beta*theta^2) / L^p
    where theta = angle between edge and forward (x) direction.
    """
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
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue

            # Directional measure: theta = angle from forward (x-axis)
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-BETA * theta * theta)

            # Field-dependent action
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret

            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea

    return amps


def centroid_y(amps, positions, det_list):
    """Amplitude-weighted mean y at detectors."""
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    if total < 1e-30:
        return 0.0
    return wy / total


# ─────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────

def test_attraction(name, gen_func, n_layers_list, n_seeds=16, k_band=None, **gen_kwargs):
    """Test 1: does gravity attract? Paired per-seed statistics."""
    if k_band is None:
        k_band = [3.0, 5.0, 7.0]

    print(f"  [{name}]")
    print(f"  {'N':>4s}  {'delta':>8s}  {'SE':>6s}  {'n':>4s}  {'t':>5s}  verdict")
    print(f"  {'-'*42}")

    for nl in n_layers_list:
        per_seed_deltas = []

        for seed in range(n_seeds):
            positions, adj, layer_indices = gen_func(
                n_layers=nl, nodes_per_layer=30, yz_range=8.0,
                connect_radius=3.5, rng_seed=seed * 13 + 5, **gen_kwargs,
            )

            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            # Mass at y > center, around 2/3 depth
            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)
            grav_layer_idx = 2 * len(layer_indices) // 3
            mass_nodes = [i for i in layer_indices[grav_layer_idx]
                          if positions[i][1] > cy + 1]
            if not mass_nodes:
                continue

            field_with = compute_field_3d(positions, adj, mass_nodes)
            field_without = [0.0] * len(positions)

            seed_deltas = []
            for k in k_band:
                amps_with = propagate_3d(positions, adj, field_with, src, k)
                amps_without = propagate_3d(positions, adj, field_without, src, k)
                y_with = centroid_y(amps_with, positions, det_list)
                y_without = centroid_y(amps_without, positions, det_list)
                seed_deltas.append(y_with - y_without)

            if seed_deltas:
                per_seed_deltas.append(sum(seed_deltas) / len(seed_deltas))

        if per_seed_deltas:
            n_ok = len(per_seed_deltas)
            delta = sum(per_seed_deltas) / n_ok
            var = sum((d - delta)**2 for d in per_seed_deltas) / n_ok
            se = math.sqrt(var) / math.sqrt(n_ok)
            t = delta / se if se > 1e-10 else 0
            if delta > 0 and t > 2:
                verdict = "GRAVITY"
            elif delta > 0 and t > 1:
                verdict = "WEAK"
            elif abs(t) < 1:
                verdict = "FLAT"
            else:
                verdict = "REPULSION?"
            print(f"  {nl:4d}  {delta:+8.4f}  {se:6.4f}  {n_ok:4d}  {t:+5.2f}  {verdict}")
        else:
            print(f"  {nl:4d}  FAIL (no valid seeds)")

    print()


def test_distance_scaling(name, gen_func, n_seeds=12, **gen_kwargs):
    """Test 2: shift vs impact parameter b. Does 3D give 1/b scaling?"""
    k_band = [3.0, 5.0, 7.0]
    n_layers = 18
    b_targets = [1.5, 2.5, 3.5, 5.0, 7.0]

    print(f"  [{name}] — distance scaling (N={n_layers}, {n_seeds} seeds)")
    print(f"  {'b':>5s}  {'shift':>8s}  {'SE':>6s}  {'shift*b':>8s}  {'shift*b²':>9s}  {'n':>3s}")
    print(f"  {'-'*48}")

    for b_target in b_targets:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = gen_func(
                n_layers=n_layers, nodes_per_layer=35, yz_range=12.0,
                connect_radius=3.5, rng_seed=seed * 17 + 3, **gen_kwargs,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)

            mid = len(layer_indices) // 2
            mass_nodes = [i for i in layer_indices[mid]
                          if abs(positions[i][1] - (cy + b_target)) < 1.5]
            if len(mass_nodes) < 2:
                continue

            field = compute_field_3d(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                amps_m = propagate_3d(positions, adj, field, src, k)
                amps_f = propagate_3d(positions, adj, free_f, src, k)
                shifts.append(centroid_y(amps_m, positions, det_list) -
                              centroid_y(amps_f, positions, det_list))

            if shifts:
                per_seed.append(sum(shifts) / len(shifts))

        if per_seed:
            n_ok = len(per_seed)
            avg = sum(per_seed) / n_ok
            se = math.sqrt(sum((s-avg)**2 for s in per_seed) / n_ok) / math.sqrt(n_ok)
            print(f"  {b_target:5.1f}  {avg:+8.4f}  {se:6.4f}  {avg*b_target:+8.3f}  "
                  f"{avg*b_target**2:+9.2f}  {n_ok:3d}")
        else:
            print(f"  {b_target:5.1f}  FAIL")

    print()
    print("  Interpretation:")
    print("    shift*b ≈ const  → θ ~ 1/b  (3D Newtonian)")
    print("    shift*b² ≈ const → θ ~ 1/b² (stronger falloff)")
    print("    shift ≈ const    → b-independent (like 2D)")
    print()


def test_mass_scaling(name, gen_func, n_seeds=12, **gen_kwargs):
    """Test 3: shift vs number of mass nodes. Does F scale with M?"""
    k_band = [3.0, 5.0, 7.0]
    n_layers = 18
    mass_counts = [2, 4, 6, 8, 12, 16]

    print(f"  [{name}] — mass scaling (N={n_layers}, {n_seeds} seeds)")
    print(f"  {'n_mass':>6s}  {'shift':>8s}  {'SE':>6s}  {'shift/n':>8s}  {'n':>3s}")
    print(f"  {'-'*38}")

    for target_n in mass_counts:
        per_seed = []
        for seed in range(n_seeds):
            positions, adj, layer_indices = gen_func(
                n_layers=n_layers, nodes_per_layer=35, yz_range=12.0,
                connect_radius=3.5, rng_seed=seed * 17 + 3, **gen_kwargs,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            cy = sum(all_ys) / len(all_ys)

            mid = len(layer_indices) // 2
            candidates = sorted(
                [i for i in layer_indices[mid] if positions[i][1] > cy + 2],
                key=lambda i: -positions[i][1]
            )
            mass_nodes = candidates[:target_n]
            if len(mass_nodes) < 2:
                continue

            field = compute_field_3d(positions, adj, mass_nodes)
            free_f = [0.0] * len(positions)

            shifts = []
            for k in k_band:
                amps_m = propagate_3d(positions, adj, field, src, k)
                amps_f = propagate_3d(positions, adj, free_f, src, k)
                shifts.append(centroid_y(amps_m, positions, det_list) -
                              centroid_y(amps_f, positions, det_list))

            if shifts:
                per_seed.append((len(mass_nodes), sum(shifts) / len(shifts)))

        if per_seed:
            n_ok = len(per_seed)
            actual_n = per_seed[0][0]
            vals = [v for _, v in per_seed]
            avg = sum(vals) / n_ok
            se = math.sqrt(sum((v-avg)**2 for v in vals) / n_ok) / math.sqrt(n_ok)
            per_mass = avg / actual_n if actual_n > 0 else 0
            print(f"  {actual_n:6d}  {avg:+8.4f}  {se:6.4f}  {per_mass:+8.4f}  {n_ok:3d}")
        else:
            print(f"  {target_n:6d}  FAIL")

    print()
    print("  Interpretation:")
    print("    shift/n ≈ const  → F ~ M  (Newtonian mass scaling)")
    print("    shift ≈ const    → F independent of M (threshold, like 2D)")
    print()


def main():
    print("=" * 74)
    print("3D GRAVITY ON MODULAR CAUSAL DAGs")
    print("  Full corrected propagator: 1/L^p, directional measure, phase valley")
    print("  Questions: does 3D give 1/b scaling and F~M?")
    print("=" * 74)
    print()

    # ── TEST 1: Basic attraction ──
    print("TEST 1: Gravitational attraction")
    print()

    families = [
        ("3D Uniform", generate_3d_uniform_dag, {}),
        ("3D Modular gap=3", generate_3d_modular_dag, {"gap": 3.0}),
        ("3D Modular gap=5", generate_3d_modular_dag, {"gap": 5.0}),
    ]

    for fname, gen, kwargs in families:
        test_attraction(fname, gen, [12, 18, 25], n_seeds=16, **kwargs)

    # ── TEST 2: Distance scaling ──
    print("TEST 2: Distance scaling (shift vs impact parameter)")
    print()
    test_distance_scaling("3D Uniform", generate_3d_uniform_dag)
    test_distance_scaling("3D Modular gap=3", generate_3d_modular_dag, gap=3.0)

    # ── TEST 3: Mass scaling ──
    print("TEST 3: Mass scaling (shift vs number of mass nodes)")
    print()
    test_mass_scaling("3D Uniform", generate_3d_uniform_dag)
    test_mass_scaling("3D Modular gap=3", generate_3d_modular_dag, gap=3.0)

    # ── TEST 4: 2D vs 3D comparison ──
    print("TEST 4: 2D vs 3D comparison summary")
    print()
    print("  Expected physics:")
    print("    2D: field ~ log(r)  → gradient ~ 1/r   → deflection ~ const(b)")
    print("    3D: field ~ 1/r     → gradient ~ 1/r²  → deflection ~ 1/b")
    print()
    print("  If 3D shows 1/b: the model correctly captures dimensionality.")
    print("  If 3D shows const(b): the discrete graph washes out the 3D signature.")
    print()
    print("EXPERIMENT COMPLETE")


if __name__ == "__main__":
    main()
