#!/usr/bin/env python3
"""Decoherence-interference trade-off across connectivity spectrum.

Prediction: sparse graphs (deg<3) allow slit-selective env coupling
but don't support interference. Connected graphs (deg≥3) support
interference but defeat env selectivity. If true: the model has a
fundamental decoherence-interference incompatibility at fixed topology.

Sweep connect_radius from 1.5 (sparse) to 5.0 (dense).
At each, measure: interference V, decoherence V_drop, gravity shift.

Uses two-register with fine env (last mass node) + slit-adjacent mass.

PStack experiment: connectivity-decoherence-tradeoff
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
    n_seeds = 8
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("CONNECTIVITY vs DECOHERENCE TRADE-OFF")
    print(f"  Sweep connect_radius, measure V, V_drop, gravity")
    print("=" * 70)
    print()

    print(f"  {'radius':>6s}  {'deg':>5s}  {'V_coh':>7s}  {'V_2reg':>7s}  "
          f"{'V_drop':>7s}  {'grav':>7s}  {'I%':>4s}  {'D%':>4s}  {'G%':>4s}")
    print(f"  {'-' * 60}")

    for radius in [1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
        v_cohs = []
        v_2regs = []
        gravs = []
        degrees = []
        i_count = d_count = g_count = valid = 0

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            edges = sum(len(v) for v in adj.values())
            degrees.append(edges/n if n > 0 else 0)

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

            # Barrier
            bl_idx = len(layers) // 3
            bl = layers[bl_idx]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy + 2][:3]
            sb = [i for i in bi if positions[i][1] < cy - 2][:3]
            if not sa or not sb:
                continue
            si = set(sa + sb)
            blocked = set(bi) - si

            # Mass: post-barrier, near upper slit
            post_bl = layers[bl_idx + 1]
            pb_nodes = by_layer[post_bl]
            sa_ys = [positions[i][1] for i in sa]
            if not sa_ys:
                continue
            sa_cy = sum(sa_ys)/len(sa_ys)
            mass_nodes = [i for i in pb_nodes
                          if abs(positions[i][1] - sa_cy) < 3]
            if len(mass_nodes) < 1:
                continue
            mass_set = set(mass_nodes)
            mass_cy = sum(positions[i][1] for i in mass_nodes)/len(mass_nodes)
            field = compute_field(positions, adj, mass_nodes)
            free_f = [0.0]*n

            # Gravity
            grav_shifts = []
            for k in k_band:
                fp = pathsum_coherent(positions, adj, free_f, src, det, k)
                mp = pathsum_two_register(positions, adj, field, src, det, k, mass_set)
                grav_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))
            avg_grav = sum(grav_shifts)/len(grav_shifts)
            attracts = (mass_cy - cy > 0 and avg_grav > 0.05)

            # Interference + decoherence
            avg_coh = defaultdict(float)
            avg_2reg = defaultdict(float)
            for k in k_band:
                pc = pathsum_coherent(positions, adj, field, src, det, k, blocked)
                p2 = pathsum_two_register(positions, adj, field, src, det, k,
                                           mass_set, blocked)
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

            v_cohs.append(vc)
            v_2regs.append(v2)
            gravs.append(avg_grav)

            if vc > 0.1: i_count += 1
            if vd > 0.02: d_count += 1
            if attracts: g_count += 1
            valid += 1

        if valid > 0 and degrees:
            deg = sum(degrees)/len(degrees)
            mvc = sum(v_cohs)/len(v_cohs) if v_cohs else 0
            mv2 = sum(v_2regs)/len(v_2regs) if v_2regs else 0
            mvd = mvc - mv2
            mg = sum(gravs)/len(gravs) if gravs else 0
            ip = f"{100*i_count//valid}%"
            dp = f"{100*d_count//valid}%"
            gp = f"{100*g_count//valid}%"
            print(f"  {radius:6.1f}  {deg:5.1f}  {mvc:7.3f}  {mv2:7.3f}  "
                  f"{mvd:+7.3f}  {mg:+7.2f}  {ip:>4s}  {dp:>4s}  {gp:>4s}")

    print()
    print("PREDICTION:")
    print("  If D% peaks at low connectivity where I% is low:")
    print("    → Decoherence and interference are mutually exclusive")
    print("    → The model needs DYNAMIC topology to have both")
    print()
    print("  If D% and I% can both be >0 at some connectivity:")
    print("    → A sweet spot exists for all three phenomena")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
