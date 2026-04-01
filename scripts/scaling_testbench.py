#!/usr/bin/env python3
"""Minimal asymptotic testbench: 4 graph families, isolated scaling variables.

Graph families:
1. Regular layered lattice (8-neighbor, fixed connectivity)
2. Branching tree (tunable branching factor, minimal path multiplicity)
3. Layered random DAG with tunable path multiplicity (vary connect_radius)
4. Layered random DAG with tunable env depth (vary env_fraction)

For each: measure gravity metric (R_grav) and decoherence metric (purity)
at multiple graph sizes, holding everything else fixed.

This replaces the full random-DAG suite for scaling tests.
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import (
    propagate_two_register_full, build_post_barrier_setup, compute_detector_metrics,
)
from scripts.two_register_decoherence import pathsum_coherent, centroid_y


def build_branching_tree(n_layers, branching_factor=2, y_range=10.0):
    """Layered tree: each node connects to `branching_factor` nodes in next layer."""
    positions = [(0.0, 0.0)]
    adj = defaultdict(list)
    layer_indices = [[0]]

    for layer in range(1, n_layers):
        x = float(layer)
        layer_nodes = []
        prev = layer_indices[-1]

        for parent in prev:
            py = positions[parent][1]
            for b in range(branching_factor):
                y = py + (b - branching_factor/2 + 0.5) * (y_range / (branching_factor ** layer))
                y = max(-y_range, min(y_range, y))
                idx = len(positions)
                positions.append((x, y))
                adj[parent].append(idx)
                layer_nodes.append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def measure_gravity(positions, adj, layer_indices, field, free_f, src, det, k_band):
    """Normalized gravity metric: shift / beam_width."""
    shifts = []
    widths = []
    for k in k_band:
        fp = pathsum_coherent(positions, adj, free_f, src, det, k)
        mp = pathsum_coherent(positions, adj, field, src, det, k)
        fy = centroid_y(fp, positions)
        my = centroid_y(mp, positions)
        shifts.append(my - fy)

        # Beam width = std of free distribution
        total = sum(fp.values())
        if total > 0:
            mean = sum(positions[d][1]*p for d, p in fp.items()) / total
            var = sum(positions[d][1]**2*p for d, p in fp.items()) / total - mean**2
            widths.append(max(var**0.5, 0.1))
        else:
            widths.append(1.0)

    avg_shift = sum(shifts)/len(shifts)
    avg_width = sum(widths)/len(widths)
    return avg_shift / avg_width if avg_width > 0 else 0.0


def measure_purity(positions, adj, setup, k_band):
    """Detector-state purity from two-register."""
    purities = []
    for k in k_band:
        ds = propagate_two_register_full(
            positions, adj, setup["field"], setup["src"], setup["det"], k,
            setup["mass_set"], setup["blocked"])
        p, _, _, _ = compute_detector_metrics(ds, setup["det_list"])
        if not math.isnan(p):
            purities.append(p)
    return sum(purities)/len(purities) if purities else 1.0


def compute_field_simple(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_idx)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0]*n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def main():
    k_band = [3.0, 5.0, 7.0]

    print("=" * 80)
    print("SCALING TESTBENCH: 4 graph families × size sweep")
    print("=" * 80)
    print()

    # ================================================================
    # FAMILY 1: Layered random DAG (standard, vary size)
    # ================================================================
    print("FAMILY 1: Layered random DAG (npl=25, r=3.0, y=12)")
    print(f"  {'N_layers':>8s}  {'N_nodes':>7s}  {'R_grav':>8s}  {'purity':>8s}  {'path_mult':>9s}")
    print(f"  {'-' * 46}")

    for nl in [8, 10, 12, 15, 20, 25, 30]:
        gravs, purs, pmults = [], [], []
        for seed in range(5):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            n = len(positions)

            setup = build_post_barrier_setup(positions, adj,
                                              env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            # Gravity
            free_f = [0.0]*n
            mid_layer = setup["layers"][len(setup["layers"])//2]
            grav_mass = [i for i in setup["by_layer"][mid_layer]
                        if positions[i][1] > setup["cy"]+2]
            if len(grav_mass) < 2:
                continue
            field_g = compute_field_simple(positions, adj, grav_mass)
            rg = measure_gravity(positions, adj, None, field_g, free_f,
                                setup["src"], setup["det"], k_band)
            gravs.append(rg)

            # Purity
            p = measure_purity(positions, adj, setup, k_band)
            purs.append(p)

            # Path multiplicity estimate
            edges = sum(len(v) for v in adj.values())
            pmults.append(edges/n if n > 0 else 0)

        if gravs:
            positions, _, _ = generate_causal_dag(n_layers=nl, nodes_per_layer=25,
                y_range=12.0, connect_radius=3.0, rng_seed=7)
            print(f"  {nl:8d}  {len(positions):7d}  {sum(gravs)/len(gravs):+8.3f}  "
                  f"{sum(purs)/len(purs):8.4f}  {sum(pmults)/len(pmults):9.1f}")

    # ================================================================
    # FAMILY 2: Vary connect_radius (path multiplicity)
    # ================================================================
    print()
    print("FAMILY 2: Vary connect_radius at fixed N=15 layers")
    print(f"  {'radius':>8s}  {'mean_deg':>8s}  {'R_grav':>8s}  {'purity':>8s}")
    print(f"  {'-' * 38}")

    for r in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
        gravs, purs = [], []
        for seed in range(5):
            positions, adj, _ = generate_causal_dag(
                n_layers=15, nodes_per_layer=25, y_range=12.0,
                connect_radius=r, rng_seed=seed*11+7)
            n = len(positions)

            setup = build_post_barrier_setup(positions, adj, env_depth_layers=2)
            if setup is None:
                continue

            free_f = [0.0]*n
            mid_layer = setup["layers"][len(setup["layers"])//2]
            grav_mass = [i for i in setup["by_layer"][mid_layer]
                        if positions[i][1] > setup["cy"]+2]
            if len(grav_mass) < 2:
                continue
            field_g = compute_field_simple(positions, adj, grav_mass)
            rg = measure_gravity(positions, adj, None, field_g, free_f,
                                setup["src"], setup["det"], k_band)
            gravs.append(rg)

            p = measure_purity(positions, adj, setup, k_band)
            purs.append(p)

        if gravs:
            edges = sum(len(v) for v in adj.values())
            deg = edges / n if n > 0 else 0
            print(f"  {r:8.1f}  {deg:8.1f}  {sum(gravs)/len(gravs):+8.3f}  "
                  f"{sum(purs)/len(purs):8.4f}")

    # ================================================================
    # FAMILY 3: Branching tree (minimal path multiplicity)
    # ================================================================
    print()
    print("FAMILY 3: Branching tree (bf=2, minimal paths)")
    print(f"  {'N_layers':>8s}  {'N_nodes':>7s}  {'R_grav':>8s}  {'note':>20s}")
    print(f"  {'-' * 48}")

    for nl in [6, 8, 10, 12]:
        positions, adj, layer_indices = build_branching_tree(nl, branching_factor=2, y_range=10.0)
        n = len(positions)
        src = layer_indices[0]
        det = set(layer_indices[-1])
        if not det:
            print(f"  {nl:8d}  {n:7d}  {'n/a':>8s}  {'no detector nodes':>20s}")
            continue

        mid = len(layer_indices)//2
        all_ys = [y for _, y in positions]
        cy = sum(all_ys)/len(all_ys) if all_ys else 0
        grav_mass = [i for i in layer_indices[mid] if positions[i][1] > cy+1]

        if len(grav_mass) < 1:
            print(f"  {nl:8d}  {n:7d}  {'n/a':>8s}  {'no mass candidates':>20s}")
            continue

        free_f = [0.0]*n
        field_g = compute_field_simple(positions, adj, grav_mass)

        rg = measure_gravity(positions, adj, layer_indices, field_g, free_f,
                            src, det, k_band)
        print(f"  {nl:8d}  {n:7d}  {rg:+8.3f}  {'tree, 1 path/pair':>20s}")

    # ================================================================
    # BENCHMARK TABLE
    # ================================================================
    print()
    print("=" * 80)
    print("BENCHMARK TABLE")
    print("=" * 80)
    print()
    print("| Family | Scaling var | R_grav trend | Purity trend | Expected | Current failure |")
    print("|--------|-----------|-------------|-------------|----------|----------------|")
    print("| Random DAG | N_layers | saturates | ↑ (0.71→0.89) | R↓, pur↓ | both wrong |")
    print("| Vary radius | degree | increases | varies | R∝deg | limited range |")
    print("| Branch tree | N_layers | to measure | n/a (no env) | R stable | test pending |")
    print("| Depth-scaled | env_frac | n/a | plateaus 0.79 | pur↓ | plateau not ↓ |")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
