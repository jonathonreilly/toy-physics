#!/usr/bin/env python3
"""Optimize between-slit geometry for endogenous two-register decoherence.

The bug fix revealed D=2/12 when mass is traversable between slits.
Now sweep geometry parameters to maximize decoherence:
- Slit separation (wider = more spatial selectivity)
- Mass layer offset (how far past barrier)
- Mass y-range (how much of the center is mass)

PStack experiment: between-slit-geometry-sweep
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


def run_config(n_layers, npl, y_range, radius, slit_sep, mass_offset,
               mass_y_half, n_seeds, k_band):
    """Run one geometry config, return (G%, I%, D%, ALL%)."""
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

        bl_idx = len(layers) // 3
        bl = layers[bl_idx]
        bi = by_layer[bl]

        sa = [i for i in bi if positions[i][1] > cy + slit_sep][:3]
        sb = [i for i in bi if positions[i][1] < cy - slit_sep][:3]
        if not sa or not sb:
            continue
        si = set(sa + sb)
        blocked = set(bi) - si

        # Mass in post-barrier layer(s), between slits
        mass_nodes = []
        for offset in range(1, mass_offset + 1):
            if bl_idx + offset >= len(layers):
                continue
            ml = layers[bl_idx + offset]
            for i in by_layer[ml]:
                if abs(positions[i][1] - cy) <= mass_y_half:
                    mass_nodes.append(i)

        if len(mass_nodes) < 2:
            continue
        mass_set = set(mass_nodes)

        # Gravity mass downstream
        grav_layer = layers[2 * len(layers) // 3]
        grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
        full_mass = mass_set | set(grav_mass)
        field = compute_field(positions, adj, list(full_mass))
        free_f = [0.0]*n

        # Gravity
        grav_shifts = []
        for k in k_band:
            fp = pathsum_coherent(positions, adj, free_f, src, det, k)
            mp = pathsum_two_register(positions, adj, field, src, det, k,
                                     mass_set, env_mode="fine")
            grav_shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))
        avg_grav = sum(grav_shifts)/len(grav_shifts)
        if grav_mass:
            grav_cy = sum(positions[i][1] for i in grav_mass)/len(grav_mass)
            attracts = (grav_cy - cy > 0 and avg_grav > 0.05)
        else:
            attracts = False

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

    if nv == 0:
        return 0, 0, 0, 0, 0
    return 100*gy//nv, 100*iy//nv, 100*dy//nv, 100*a3//nv, nv


def main():
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 10

    print("=" * 70)
    print("BETWEEN-SLIT GEOMETRY SWEEP FOR DECOHERENCE")
    print(f"  Two-register fine env, {n_seeds} seeds per config")
    print("=" * 70)
    print()

    # Sweep slit separation
    print("SWEEP 1: Slit separation (mass_offset=1, mass_y_half=3)")
    print(f"  {'slit_sep':>8s}  {'G%':>4s}  {'I%':>4s}  {'D%':>4s}  {'ALL%':>5s}  {'n':>3s}")
    print(f"  {'-' * 30}")
    for sep in [1, 2, 3, 4, 5, 6, 8]:
        g, i, d, a, nv = run_config(15, 25, 12.0, 3.0, sep, 1, 3.0, n_seeds, k_band)
        if nv > 0:
            print(f"  {sep:8d}  {g:3d}%  {i:3d}%  {d:3d}%  {a:4d}%  {nv:3d}")

    # Sweep mass layer offset
    print()
    print("SWEEP 2: Mass layer offset (slit_sep=3, mass_y_half=3)")
    print(f"  {'offset':>8s}  {'G%':>4s}  {'I%':>4s}  {'D%':>4s}  {'ALL%':>5s}  {'n':>3s}")
    print(f"  {'-' * 30}")
    for off in [1, 2, 3, 4, 5]:
        g, i, d, a, nv = run_config(15, 25, 12.0, 3.0, 3, off, 3.0, n_seeds, k_band)
        if nv > 0:
            print(f"  {off:8d}  {g:3d}%  {i:3d}%  {d:3d}%  {a:4d}%  {nv:3d}")

    # Sweep mass y-range
    print()
    print("SWEEP 3: Mass y-range (slit_sep=3, mass_offset=2)")
    print(f"  {'y_half':>8s}  {'G%':>4s}  {'I%':>4s}  {'D%':>4s}  {'ALL%':>5s}  {'n':>3s}")
    print(f"  {'-' * 30}")
    for yh in [1.0, 2.0, 3.0, 4.0, 6.0, 8.0]:
        g, i, d, a, nv = run_config(15, 25, 12.0, 3.0, 3, 2, yh, n_seeds, k_band)
        if nv > 0:
            print(f"  {yh:8.1f}  {g:3d}%  {i:3d}%  {d:3d}%  {a:4d}%  {nv:3d}")

    # Sweep graph density
    print()
    print("SWEEP 4: Connect radius (slit_sep=3, mass_offset=2, mass_y_half=3)")
    print(f"  {'radius':>8s}  {'G%':>4s}  {'I%':>4s}  {'D%':>4s}  {'ALL%':>5s}  {'n':>3s}")
    print(f"  {'-' * 30}")
    for r in [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]:
        g, i, d, a, nv = run_config(15, 25, 12.0, r, 3, 2, 3.0, n_seeds, k_band)
        if nv > 0:
            print(f"  {r:8.1f}  {g:3d}%  {i:3d}%  {d:3d}%  {a:4d}%  {nv:3d}")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
