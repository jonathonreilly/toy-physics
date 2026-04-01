#!/usr/bin/env python3
"""Confirm node-removal emergence with 24 seeds and N up to 80.

prune=0.10 showed pur_min=0.912 at N=40 with 16 seeds.
Need to confirm this isn't noise and check scaling behavior.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.node_removal_emergence import (
    generate_removal_dag, run_joint, measure_effective_gap,
)
from scripts.generative_causal_dag_interference import generate_causal_dag

LAM = 10.0


def main():
    print("=" * 78)
    print("REMOVAL SCALING CONFIRMATION: 24 seeds, N=12..80")
    print(f"  prune=0.10 vs uniform baseline")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 24
    n_layers_list = [12, 18, 25, 30, 40, 50, 60, 80]

    for name, gen_fn in [
        ("Uniform (baseline)", lambda nl, s: generate_causal_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=s)),
        ("Removal prune=0.10", lambda nl, s: generate_removal_dag(
            n_layers=nl, nodes_per_layer=25, y_range=12.0,
            connect_radius=3.0, rng_seed=s, prune_frac=0.10)),
    ]:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'SE':>6s}  {'decoh':>8s}  "
              f"{'grav':>8s}  {'grav_SE':>7s}  {'n_ok':>4s}  {'time':>5s}")
        print(f"  {'-' * 60}")

        for nl in n_layers_list:
            t0 = time.time()
            grav_all, pm_all, dec_all = [], [], []

            for seed_i in range(n_seeds):
                seed = seed_i * 7 + 3
                positions, adj, _ = gen_fn(nl, seed)
                r = run_joint(positions, adj, k_band, nl)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            dt = time.time() - t0

            if grav_all:
                n_ok = len(grav_all)
                avg_pm = sum(pm_all) / n_ok
                se_pm = (sum((p - avg_pm)**2 for p in pm_all) / n_ok)**0.5 / math.sqrt(n_ok)
                avg_g = sum(grav_all) / n_ok
                se_g = (sum((g - avg_g)**2 for g in grav_all) / n_ok)**0.5 / math.sqrt(n_ok)
                avg_dec = sum(dec_all) / n_ok

                print(f"  {nl:4d}  {avg_pm:8.4f}  {se_pm:6.4f}  {avg_dec:+8.4f}  "
                      f"{avg_g:+8.3f}  {se_g:7.3f}  {n_ok:4d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  FAIL")

            sys.stdout.flush()

        print()

    # Difference test
    print("DIFFERENCE (Removal - Uniform) at each N:")
    print(f"  {'N':>4s}  {'delta_pm':>9s}  {'better?':>7s}")
    print(f"  {'-' * 24}")

    # Rerun both to get paired comparison
    for nl in [25, 40, 60, 80]:
        pm_uniform = []
        pm_removal = []
        for seed_i in range(n_seeds):
            seed = seed_i * 7 + 3
            pos_u, adj_u, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed)
            pos_r, adj_r, _ = generate_removal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed, prune_frac=0.10)

            ru = run_joint(pos_u, adj_u, k_band, nl)
            rr = run_joint(pos_r, adj_r, k_band, nl)
            if ru and rr:
                pm_uniform.append(ru["pm"])
                pm_removal.append(rr["pm"])

        if pm_uniform:
            # Paired difference
            diffs = [r - u for u, r in zip(pm_uniform, pm_removal)]
            avg_diff = sum(diffs) / len(diffs)
            se_diff = (sum((d - avg_diff)**2 for d in diffs) / len(diffs))**0.5 / math.sqrt(len(diffs))
            sig = "YES" if avg_diff < -1.5 * se_diff else "marginal" if avg_diff < 0 else "no"
            print(f"  {nl:4d}  {avg_diff:+9.4f}  {sig:>7s}")

    print()
    print("delta_pm < 0 means removal is BETTER (lower pur_min)")
    print("YES = significant improvement (|delta| > 1.5 SE)")


if __name__ == "__main__":
    main()
