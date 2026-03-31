#!/usr/bin/env python3
"""Dual mass clusters for higher decoherence rate.

Current best: D=40% with single mass cluster between slits.
Idea: place TWO mass clusters, one near each slit (post-barrier).
Each slit's amplitude preferentially passes through its nearby cluster.
The env labels become more slit-discriminating → higher D.

Asymmetric sizing: cluster near slit-A has N nodes, cluster near slit-B
has M ≠ N nodes. This creates different env state spaces per slit,
maximizing the partial-trace decoherence.

PStack experiment: dual-mass-decoherence
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.two_register_decoherence import (
    compute_field, pathsum_two_register, pathsum_coherent,
    visibility, centroid_y,
)


def main():
    n_layers = 15
    npl = 25
    y_range = 12.0
    radius = 3.0
    n_seeds = 15
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("DUAL MASS CLUSTERS FOR HIGHER DECOHERENCE")
    print("=" * 70)
    print()

    configs = [
        ("single center", "center", 3.0),
        ("dual symmetric", "dual_sym", 3.0),
        ("dual near slits", "dual_near", 1.0),
        ("dual wide", "dual_wide", 5.0),
    ]

    for label, mode, mass_y_half in configs:
        print(f"  Config: {label}")
        print(f"    {'seed':>4s}  {'grav':>7s}  {'V_2reg':>7s}  {'V_coh':>7s}  "
              f"{'V_drop':>7s}  {'n_mass':>6s}  {'attr':>4s}  {'dcoh':>4s}  {'all3':>4s}")
        print(f"    {'-' * 60}")

        gy = iy = dy = a3 = nv = 0

        for seed in range(n_seeds):
            positions, adj, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 7:
                continue

            src = by_layer[layers[0]]
            det = set(by_layer[layers[-1]])
            if not det:
                continue

            all_ys = [y for _, y in positions]
            cy = sum(all_ys)/len(all_ys)

            bl_idx = len(layers)//3
            bl = layers[bl_idx]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy+3][:3]
            sb = [i for i in bi if positions[i][1] < cy-3][:3]
            if not sa or not sb:
                continue
            si = set(sa+sb)
            blocked = set(bi) - si

            sa_cy = sum(positions[i][1] for i in sa)/len(sa)
            sb_cy = sum(positions[i][1] for i in sb)/len(sb)

            # Mass placement depends on mode
            post_bl = layers[bl_idx+1]
            pb_nodes = by_layer[post_bl]

            if mode == "center":
                mass_nodes = [i for i in pb_nodes if abs(positions[i][1]-cy) <= mass_y_half]
            elif mode == "dual_sym":
                # Two clusters: one near each slit center
                cluster_a = [i for i in pb_nodes if abs(positions[i][1]-sa_cy) <= 2]
                cluster_b = [i for i in pb_nodes if abs(positions[i][1]-sb_cy) <= 2]
                mass_nodes = cluster_a + cluster_b
            elif mode == "dual_near":
                # Close to slits
                cluster_a = [i for i in pb_nodes if abs(positions[i][1]-sa_cy) <= mass_y_half]
                cluster_b = [i for i in pb_nodes if abs(positions[i][1]-sb_cy) <= mass_y_half]
                mass_nodes = cluster_a + cluster_b
            elif mode == "dual_wide":
                # Wide spread around each slit
                cluster_a = [i for i in pb_nodes if abs(positions[i][1]-sa_cy) <= mass_y_half]
                cluster_b = [i for i in pb_nodes if abs(positions[i][1]-sb_cy) <= mass_y_half]
                mass_nodes = cluster_a + cluster_b
            else:
                mass_nodes = []

            if len(mass_nodes) < 2:
                continue
            mass_set = set(mass_nodes)

            grav_layer = layers[2*len(layers)//3]
            grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy+1]
            full_mass = mass_set | set(grav_mass)
            field = compute_field(positions, adj, list(full_mass))
            free_f = [0.0]*n

            # Gravity
            grav_shifts = []
            for k in k_band:
                fp = pathsum_coherent(positions, adj, free_f, src, det, k)
                mp = pathsum_two_register(positions, adj, field, src, det, k,
                                         mass_set, env_mode="fine")
                grav_shifts.append(centroid_y(mp, positions)-centroid_y(fp, positions))
            avg_grav = sum(grav_shifts)/len(grav_shifts)
            attracts = False
            if grav_mass:
                gc = sum(positions[i][1] for i in grav_mass)/len(grav_mass)
                attracts = (gc-cy > 0 and avg_grav > 0.05)

            # Interference + decoherence
            avg_coh = defaultdict(float)
            avg_2reg = defaultdict(float)
            for k in k_band:
                pc = pathsum_coherent(positions, adj, field, src, det, k, blocked)
                p2 = pathsum_two_register(positions, adj, field, src, det, k,
                                           mass_set, blocked, env_mode="fine")
                for d in det:
                    avg_coh[d] += pc.get(d, 0)
                    avg_2reg[d] += p2.get(d, 0)

            for avg in [avg_coh, avg_2reg]:
                t = sum(avg.values())
                if t > 0:
                    for d in avg:
                        avg[d] /= t

            vc = visibility(dict(avg_coh), positions, list(det))
            v2 = visibility(dict(avg_2reg), positions, list(det))
            vd = vc - v2

            if attracts: gy += 1
            if v2 > 0.05: iy += 1
            if vd > 0.02: dy += 1
            if attracts and v2 > 0.05 and vd > 0.02: a3 += 1
            nv += 1

            print(f"    {seed:4d}  {avg_grav:+7.2f}  {v2:7.3f}  {vc:7.3f}  "
                  f"{vd:+7.3f}  {len(mass_nodes):6d}  "
                  f"{'Y' if attracts else 'n':>4s}  "
                  f"{'Y' if vd > 0.02 else 'n':>4s}  "
                  f"{'Y' if attracts and v2 > 0.05 and vd > 0.02 else 'n':>4s}")

        if nv > 0:
            print(f"    ---")
            print(f"    G:{gy}/{nv} I:{iy}/{nv} D:{dy}/{nv} ALL:{a3}/{nv}")
        print()

    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
