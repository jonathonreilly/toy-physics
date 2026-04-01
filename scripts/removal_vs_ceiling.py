#!/usr/bin/env python3
"""Node removal vs the fundamental ceiling.

The ceiling diagnosis showed pur_min itself → 1 at N=80 (CLT on detector
distributions). No bath can fix this.

But node removal changes the GRAPH, which changes pur_min.
Can pruning low-distinguishability nodes keep pur_min bounded at N=80-100?

This is the definitive test: if removal keeps pur_min < 0.96 at N=100,
we've found a constructive mechanism that beats the CLT ceiling.

Also tests: does removal need to scale (prune more at larger N)?
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.node_removal_emergence import generate_removal_dag, run_joint

BETA = 0.8
LAM = 10.0


def main():
    print("=" * 78)
    print("NODE REMOVAL VS FUNDAMENTAL CEILING")
    print("  Can pruning keep pur_min < 0.96 at N=80-100?")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 16 seeds")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    # Part 1: Fixed prune=0.10 across N range (including N=80, 100)
    print("PART 1: prune=0.10 vs N (does removal beat the ceiling at large N?)")
    print(f"  {'N':>4s}  {'pur_min':>8s}  {'pur_cl':>8s}  {'decoh':>8s}  "
          f"{'grav':>8s}  {'n_ok':>4s}  {'time':>5s}")
    print(f"  {'-' * 50}")

    for nl in [25, 40, 60, 80, 100]:
        t0 = time.time()
        pm_all, pc_all, dec_all, grav_all = [], [], [], []

        for seed in seeds:
            positions, adj, _ = generate_removal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed, prune_frac=0.10,
            )
            r = run_joint(positions, adj, k_band, nl)
            if r:
                pm_all.append(r["pm"])
                grav_all.append(r["grav"])
                dec_all.append(r["dec"])

        dt = time.time() - t0
        if pm_all:
            apm = sum(pm_all) / len(pm_all)
            adec = sum(dec_all) / len(dec_all)
            agrav = sum(grav_all) / len(grav_all)
            # pur_cl ≈ pur_min when lambda=10 and S_norm>0.1 (bath saturated)
            print(f"  {nl:4d}  {apm:8.4f}  {'≈pm':>8s}  {adec:+8.4f}  "
                  f"{agrav:+8.3f}  {len(pm_all):4d}  {dt:4.0f}s")
        else:
            print(f"  {nl:4d}  FAIL")
        sys.stdout.flush()

    # Part 2: Prune fraction sweep at N=80
    print()
    print("PART 2: Prune fraction sweep at N=80")
    print(f"  {'prune':>6s}  {'pur_min':>8s}  {'decoh':>8s}  {'grav':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 42}")

    for prune in [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40]:
        pm_all, dec_all, grav_all = [], [], []

        for seed in seeds:
            positions, adj, _ = generate_removal_dag(
                n_layers=80, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed, prune_frac=prune,
            )
            r = run_joint(positions, adj, k_band, 80)
            if r:
                pm_all.append(r["pm"])
                grav_all.append(r["grav"])
                dec_all.append(r["dec"])

        if pm_all:
            apm = sum(pm_all) / len(pm_all)
            adec = sum(dec_all) / len(dec_all)
            agrav = sum(grav_all) / len(grav_all)
            beat = " <<<" if apm < 0.96 else ""
            print(f"  {prune:6.2f}  {apm:8.4f}  {adec:+8.4f}  {agrav:+8.3f}  "
                  f"{len(pm_all):4d}{beat}")
        sys.stdout.flush()

    # Part 3: Adaptive pruning — scale prune fraction with N
    print()
    print("PART 3: Adaptive pruning (prune_frac = 0.005 * N)")
    print(f"  {'N':>4s}  {'prune':>6s}  {'pur_min':>8s}  {'decoh':>8s}  "
          f"{'grav':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 46}")

    for nl in [25, 40, 60, 80, 100]:
        prune = min(0.005 * nl, 0.50)
        pm_all, dec_all, grav_all = [], [], []

        for seed in seeds:
            positions, adj, _ = generate_removal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed, prune_frac=prune,
            )
            r = run_joint(positions, adj, k_band, nl)
            if r:
                pm_all.append(r["pm"])
                grav_all.append(r["grav"])
                dec_all.append(r["dec"])

        if pm_all:
            apm = sum(pm_all) / len(pm_all)
            adec = sum(dec_all) / len(dec_all)
            agrav = sum(grav_all) / len(grav_all)
            beat = " <<<" if apm < 0.96 else ""
            print(f"  {nl:4d}  {prune:6.2f}  {apm:8.4f}  {adec:+8.4f}  "
                  f"{agrav:+8.3f}  {len(pm_all):4d}{beat}")
        sys.stdout.flush()

    print()
    print("<<< = pur_min < 0.96 (beats the ceiling)")
    print()
    print("VERDICT:")
    print("  If removal keeps pur_min < 0.96 at N=80-100:")
    print("    → Pruning breaks the CLT ceiling at the fundamental level")
    print("  If pur_min still climbs despite removal:")
    print("    → CLT on detector distributions is truly inescapable")


if __name__ == "__main__":
    main()
