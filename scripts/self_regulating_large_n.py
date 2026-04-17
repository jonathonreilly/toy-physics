#!/usr/bin/env python3
"""Large-N test: does self-regulating gap survive at N=60-80?

The initial test showed d_min=0.1 improves decoherence by 5pp at N=30.
In 2D, node removal was marginal at N=40 and dead at N=80.
In 3D, the CLT delay should give more room.

This test pushes to N=50, 60, 80 to check asymptotic behavior.
Uses d_min=0.1 (sweet spot from initial test).

PStack experiment: self-regulating-large-n
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.self_regulating_gap_3d import (
    generate_3d_uniform_dag, measure_decoherence,
    self_regulating_prune, gap_metric,
)


def main():
    n_seeds = 16
    d_min = 0.1

    print("=" * 70)
    print("SELF-REGULATING GAP: Large-N sustainability test")
    print(f"  d_min={d_min}, 3D uniform → self-regulated")
    print("=" * 70)
    print()

    n_layers_list = [20, 25, 30, 40, 50, 60, 80]

    for label, use_prune in [("Uniform baseline", False), (f"Self-regulated d_min={d_min}", True)]:
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_cl':>8s}  {'gap':>6s}  {'removed':>8s}  {'n':>3s}")
        print(f"  {'-'*36}")

        for nl in n_layers_list:
            purs = []
            gaps = []
            removals = []

            for seed in range(n_seeds):
                positions, adj_orig, layer_indices = generate_3d_uniform_dag(
                    n_layers=nl, nodes_per_layer=30, yz_range=10.0,
                    connect_radius=3.5, rng_seed=seed*13+5)

                if use_prune:
                    adj_e, stats = self_regulating_prune(
                        positions, adj_orig, layer_indices,
                        d_min=d_min, max_iter=5)
                    removals.append(stats["removed"])
                else:
                    adj_e = adj_orig
                    removals.append(0)

                pur = measure_decoherence(positions, adj_e, layer_indices)
                if not math.isnan(pur):
                    purs.append(pur)
                    gaps.append(gap_metric(positions, adj_e, layer_indices))

            if purs:
                mp = sum(purs) / len(purs)
                mg = sum(gaps) / len(gaps) if gaps else 0
                mr = sum(removals) / len(removals)
                print(f"  {nl:4d}  {mp:8.4f}  {mg:6.2f}  {mr:8.1f}  {len(purs):3d}")
            else:
                print(f"  {nl:4d}  FAIL")

        print()

    print("=" * 70)
    print("KEY QUESTION: does self-regulated pur_cl stay below uniform")
    print("at N=60-80? If yes: 3D emergence is viable. If no: same CLT fate.")
    print("=" * 70)


if __name__ == "__main__":
    main()
