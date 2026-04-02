#!/usr/bin/env python3
"""Slit-conditioned 3D growth: per-slit amplitude guides two-channel placement.

Fix for PR #26: total-amplitude growth creates one beam (y-symmetric).
Slit-conditioned growth uses PER-SLIT amplitude → two separate channels.

PStack experiment: slit-guided-3d-growth
"""

import cmath, math, random, os, sys
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.geometric_growth_emergence import (
    gen_uniform, compute_field, propagate, cl_contrast, cl_purity,
    measure_decoherence, gap_metric, propagate_partial,
    amplitude_density_ybins as amplitude_density,
    sample_from_density as sample_y,
    BETA, N_YBINS, LAM, K_BAND,
)


def generate_slit_grown_dag(n_layers=20, npl=30, yz_range=10.0, r=3.5,
                             rng_seed=42, sharpness=2.0):
    rng = random.Random(rng_seed)
    positions = []; adj = defaultdict(list); layer_indices = []
    bl = n_layers // 3

    for layer in range(bl + 1):
        x = float(layer); nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0)); nodes.append(len(positions)-1)
        else:
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range); z = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layer_indices[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r: adj[pi].append(idx)
        layer_indices.append(nodes)

    barrier = layer_indices[bl]
    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]

    if not slit_a or not slit_b:
        for layer in range(bl + 1, n_layers):
            x = float(layer); nodes = []
            for _ in range(npl):
                y = rng.uniform(-yz_range, yz_range); z = rng.uniform(-yz_range, yz_range)
                idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
                for pl in layer_indices[max(0, layer-2):]:
                    for pi in pl:
                        d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                        if d <= r: adj[pi].append(idx)
            layer_indices.append(nodes)
        return positions, dict(adj), layer_indices

    barrier_blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = barrier_blocked | set(slit_b)
    blocked_b = barrier_blocked | set(slit_a)

    for layer in range(bl + 1, n_layers):
        x = float(layer); nodes = []
        src = layer_indices[0]
        field_zero = [0.0] * len(positions)
        amps_a = propagate(positions, adj, field_zero, src, 5.0, blocked_a)
        amps_b = propagate(positions, adj, field_zero, src, 5.0, blocked_b)
        prev = layer_indices[-1]
        density_a = amplitude_density(amps_a, positions, prev, yz_range)
        density_b = amplitude_density(amps_b, positions, prev, yz_range)

        n_a = npl // 2; n_b = npl - n_a
        for _ in range(n_a):
            y = sample_y(density_a, yz_range, rng, sharpness)
            z = rng.uniform(-yz_range, yz_range)
            idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
            for pl in layer_indices[max(0, layer-2):]:
                for pi in pl:
                    d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                    if d <= r: adj[pi].append(idx)
        for _ in range(n_b):
            y = sample_y(density_b, yz_range, rng, sharpness)
            z = rng.uniform(-yz_range, yz_range)
            idx = len(positions); positions.append((x, y, z)); nodes.append(idx)
            for pl in layer_indices[max(0, layer-2):]:
                for pi in pl:
                    d = math.sqrt(sum((a-b)**2 for a, b in zip(positions[idx], positions[pi])))
                    if d <= r: adj[pi].append(idx)
        layer_indices.append(nodes)

    return positions, dict(adj), layer_indices


def main():
    n_seeds = 16
    print("=" * 74)
    print("SLIT-CONDITIONED 3D GROWTH")
    print("  Per-slit amplitude → two-channel node placement")
    print("=" * 74)
    print()

    n_layers_list = [20, 25, 30, 40, 50, 60]

    for label, gen_fn, kwargs in [
        ("Uniform baseline", gen_uniform, {}),
        ("Slit-grown s=1.5", generate_slit_grown_dag, {"sharpness": 1.5}),
        ("Slit-grown s=2.0", generate_slit_grown_dag, {"sharpness": 2.0}),
        ("Slit-grown s=3.0", generate_slit_grown_dag, {"sharpness": 3.0}),
    ]:
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_cl':>8s}  {'gap':>6s}  {'n':>3s}")
        print(f"  {'-'*24}")
        for nl in n_layers_list:
            purs = []; gaps = []
            for seed in range(n_seeds):
                positions, adj, layers = gen_fn(n_layers=nl, rng_seed=seed*13+5, **kwargs)
                pur = measure_decoherence(positions, adj, layers)
                if not math.isnan(pur):
                    purs.append(pur)
                    gaps.append(gap_metric(positions, layers))
            if purs:
                print(f"  {nl:4d}  {sum(purs)/len(purs):8.4f}  "
                      f"{sum(gaps)/len(gaps):6.2f}  {len(purs):3d}")
            else: print(f"  {nl:4d}  FAIL")
        print()

    print("=" * 74)
    print("KEY: pur_cl < uniform = slit-guided growth creates good topology")
    print("=" * 74)


if __name__ == "__main__":
    main()
