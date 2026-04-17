#!/usr/bin/env python3
"""Slit-adjacent mass: env distinguishes slits via asymmetric coupling.

Mass adjacent to slit-A but NOT slit-B:
- Slit-A paths pass through mass → env=mass_node
- Slit-B paths don't touch mass → env=-1
- Partial trace: P = |ψ_A(mass)|² + |ψ_B(no_mass)|² → no cross-term
- This should give FULL decoherence for paths that go through mass

On generated DAGs: place mass nodes in the layer just after the barrier,
adjacent to the upper slit group but far from the lower slit group.

PStack experiment: slit-adjacent-decoherence
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
    n_seeds = 12
    k_band = [3.0, 5.0, 7.0]

    print("=" * 70)
    print("SLIT-ADJACENT MASS DECOHERENCE")
    print(f"  Mass just after barrier, near upper slit only")
    print(f"  Two-register: env = last mass node, partial trace")
    print("=" * 70)
    print()

    print(f"  {'seed':>4s}  {'grav':>7s}  {'V_2reg':>7s}  {'V_coh':>7s}  "
          f"{'V_drop':>7s}  {'n_mass':>6s}  {'attr':>4s}  {'dcoh':>4s}  {'all3':>4s}")
    print(f"  {'-' * 60}")

    gy = iy = dy = a3 = nv = 0

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
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

        # Barrier at 1/3
        bl_idx = len(layers) // 3
        bl = layers[bl_idx]
        bi = by_layer[bl]

        # Slits: wide separation
        sa = [i for i in bi if positions[i][1] > cy + 3][:3]
        sb = [i for i in bi if positions[i][1] < cy - 3][:3]
        if not sa or not sb:
            continue
        si = set(sa + sb)
        blocked = set(bi) - si

        # Mass: in the layer JUST AFTER barrier, near upper slit ONLY
        post_barrier = layers[bl_idx + 1]
        pb_nodes = by_layer[post_barrier]

        # Upper slit y range
        sa_ys = [positions[i][1] for i in sa]
        sa_min_y = min(sa_ys) - 2
        sa_max_y = max(sa_ys) + 2

        # Mass = nodes in post-barrier layer near upper slit
        mass_nodes = [i for i in pb_nodes
                      if sa_min_y <= positions[i][1] <= sa_max_y]
        if len(mass_nodes) < 2:
            continue
        mass_set = set(mass_nodes)

        field = compute_field(positions, adj, mass_nodes)
        free_f = [0.0]*n

        # ---- GRAVITY ----
        grav_shifts = []
        for k in k_band:
            fp = pathsum_coherent(positions, adj, free_f, src, det, k)
            mp = pathsum_two_register(positions, adj, field, src, det, k, mass_set)
            grav_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))
        avg_grav = sum(grav_shifts)/len(grav_shifts)
        mass_cy = sum(positions[i][1] for i in mass_nodes)/len(mass_nodes)
        attracts = (mass_cy - cy > 0 and avg_grav > 0.05)

        # ---- INTERFERENCE + DECOHERENCE ----
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

        v_coh = visibility(dict(avg_coh), positions, list(det))
        v_2reg = visibility(dict(avg_2reg), positions, list(det))
        v_drop = v_coh - v_2reg
        has_interf = v_2reg > 0.05
        has_decoh = v_drop > 0.02
        has_all3 = attracts and has_interf and has_decoh

        if attracts: gy += 1
        if has_interf: iy += 1
        if has_decoh: dy += 1
        if has_all3: a3 += 1
        nv += 1

        print(f"  {seed:4d}  {avg_grav:+7.2f}  {v_2reg:7.3f}  {v_coh:7.3f}  "
              f"{v_drop:+7.3f}  {len(mass_nodes):6d}  "
              f"{'Y' if attracts else 'n':>4s}  "
              f"{'Y' if has_decoh else 'n':>4s}  "
              f"{'Y' if has_all3 else 'n':>4s}")

    if nv > 0:
        print(f"  ---")
        print(f"  G:{gy}/{nv} I:{iy}/{nv} D:{dy}/{nv} ALL:{a3}/{nv}")

    print()
    print("If D > 0 and G > 0:")
    print("  → Slit-selective environment coupling produces endogenous decoherence")
    print("  → Mass adjacent to one slit records which-slit info")
    print("  → The model's decoherence comes from ASYMMETRIC mass-slit geometry")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
