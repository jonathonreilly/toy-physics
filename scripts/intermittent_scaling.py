#!/usr/bin/env python3
"""Does intermittent normalization (K=10) beat the 1/N ceiling at large N?

K=10 gave pur_min=0.928 at N=60 vs 0.965 linear (Born preserved).
Push to N=80, 100, 120 to see if the improvement persists or if
CLT eventually wins anyway.

If (1-pur_min) stops decaying (plateaus), the ceiling IS broken.
If it still decays as 1/N but with a larger prefactor, it's just shifted.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.nonlinear_pareto import propagate_mixed, cl_purity_min

BETA = 0.8


def compute_field(positions, adj, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def run_one(nl, seed, K):
    k_band = [3.0, 5.0, 7.0]
    positions, adj, _ = generate_causal_dag(
        n_layers=nl, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=seed,
    )
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))

    pm_vals = []
    for k in k_band:
        amps_a = propagate_mixed(positions, adj, field, src, k,
                                  blocked | set(sb), "layer_norm", 1.0, K)
        amps_b = propagate_mixed(positions, adj, field, src, k,
                                  blocked | set(sa), "layer_norm", 1.0, K)
        pm = cl_purity_min(amps_a, amps_b, det_list)
        if not math.isnan(pm):
            pm_vals.append(pm)

    if not pm_vals:
        return None
    return sum(pm_vals) / len(pm_vals)


def main():
    print("=" * 70)
    print("INTERMITTENT NORMALIZATION SCALING (K=10)")
    print("  Does it beat the 1/N ceiling at large N?")
    print("  16 seeds per N point")
    print("=" * 70)
    print()

    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]
    n_list = [25, 30, 40, 50, 60, 80, 100]

    print(f"  {'':>4s}  {'--- Linear ---':>16s}  {'-- K=10 norm --':>16s}  {'improvement':>11s}")
    print(f"  {'N':>4s}  {'pur_min':>8s}  {'1-pm':>7s}  {'pur_min':>8s}  {'1-pm':>7s}  {'delta':>11s}")
    print(f"  {'-' * 58}")

    for nl in n_list:
        t0 = time.time()
        lin_pm, nl_pm = [], []

        for seed in seeds:
            # Linear
            r_lin = run_one(nl, seed, K=999999)  # K huge = never normalize
            # K=10
            r_nl = run_one(nl, seed, K=10)

            if r_lin is not None:
                lin_pm.append(r_lin)
            if r_nl is not None:
                nl_pm.append(r_nl)

        dt = time.time() - t0

        if lin_pm and nl_pm:
            al = sum(lin_pm) / len(lin_pm)
            an = sum(nl_pm) / len(nl_pm)
            delta = an - al
            print(f"  {nl:4d}  {al:8.4f}  {1-al:7.4f}  {an:8.4f}  {1-an:7.4f}  "
                  f"{delta:+11.4f}  ({dt:.0f}s)")
        sys.stdout.flush()

    # Fit power law for both
    print()
    print("If K=10 has a FLATTER slope than linear, it's genuinely breaking the ceiling.")
    print("If same slope but larger prefactor, it's just shifted.")


if __name__ == "__main__":
    main()
