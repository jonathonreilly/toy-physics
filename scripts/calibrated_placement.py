#!/usr/bin/env python3
"""Calibrated placement: can we find the alpha that produces the right gap?

The distinguishability placement at alpha=1 gives eff_gap~2.3 (close to
the sweet spot of 2.0). But decoherence was worse than uniform.

This test does two things:
1. Fine-sweep alpha to find the value that produces eff_gap~2.0
2. Check whether that specific alpha also improves decoherence

If alpha~0.5-0.8 produces gap~2 AND better decoherence than uniform,
then the emergence story is: "a mild distinguishability bias in node
placement naturally creates the optimal topology."

Also tests: what if we ONLY bias placement at the barrier layer
(where the gap matters most) and leave all other layers uniform?
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.node_placement_emergence import (
    generate_placement_dag, run_joint, measure_gap,
)
from scripts.generative_causal_dag_interference import generate_causal_dag

BETA = 0.8
N_YBINS = 8
LAM = 10.0


def generate_barrier_only_placement(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    alpha: float = 2.0,
    barrier_width: int = 3,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """Like generate_placement_dag but ONLY applies distinguishability
    bias to the barrier_width layers immediately after the barrier.
    All other post-barrier layers use uniform placement.

    This tests whether the gap needs to persist everywhere or just
    at the critical transition point.
    """
    from scripts.node_placement_emergence import (
        _propagate_quick, _slit_distinguishability_profile, _topo_order,
    )

    rng = __import__("random").Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    barrier_layer = n_layers // 3
    slit_upper = []
    slit_lower = []
    barrier_blocked = set()

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
        else:
            # Determine if this layer gets biased placement
            post_barrier = layer > barrier_layer
            near_barrier = post_barrier and (layer - barrier_layer) <= barrier_width
            use_bias = near_barrier and alpha > 0 and slit_upper and slit_lower

            if use_bias:
                n = len(positions)
                profile = _slit_distinguishability_profile(
                    positions, adj, n,
                    layer_indices[0], slit_upper, slit_lower,
                    barrier_blocked, y_range,
                )
                max_d = max(d for _, d in profile)

                for _ in range(nodes_per_layer):
                    for _ in range(50):
                        y_cand = rng.uniform(-y_range, y_range)
                        bw = 2 * y_range / len(profile)
                        b = int((y_cand + y_range) / bw)
                        b = max(0, min(len(profile) - 1, b))
                        _, d_val = profile[b]
                        if max_d > 0:
                            p_accept = (max(d_val, 0.01) / max(max_d, 0.01)) ** alpha
                        else:
                            p_accept = 1.0
                        if rng.random() < p_accept:
                            break
                    else:
                        y_cand = rng.uniform(-y_range, y_range)

                    idx = len(positions)
                    positions.append((x, y_cand))
                    layer_nodes.append(idx)

                    for prev_layer in layer_indices[max(0, layer - 2):]:
                        for prev_idx in prev_layer:
                            if prev_idx in barrier_blocked:
                                continue
                            px, py = positions[prev_idx]
                            dist = math.sqrt((x - px) ** 2 + (y_cand - py) ** 2)
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)
            else:
                # Uniform placement
                for _ in range(nodes_per_layer):
                    y = rng.uniform(-y_range, y_range)
                    idx = len(positions)
                    positions.append((x, y))
                    layer_nodes.append(idx)

                    for prev_layer in layer_indices[max(0, layer - 2):]:
                        for prev_idx in prev_layer:
                            if post_barrier and prev_idx in barrier_blocked:
                                continue
                            px, py = positions[prev_idx]
                            dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)

            # At barrier: identify slits
            if layer == barrier_layer:
                all_ys = [yy for _, yy in positions]
                cy = sum(all_ys) / len(all_ys)
                for idx in layer_nodes:
                    y = positions[idx][1]
                    if y > cy + 3:
                        slit_upper.append(idx)
                    elif y < cy - 3:
                        slit_lower.append(idx)
                    else:
                        barrier_blocked.add(idx)
                slit_upper = slit_upper[:3]
                slit_lower = slit_lower[:3]

        layer_indices.append(layer_nodes)

    # Arrival
    n = len(positions)
    arrival = [float("inf")] * n
    for i in range(n):
        if positions[i][0] == 0.0:
            arrival[i] = 0.0
    order = sorted(range(n), key=lambda i: (positions[i][0], i))
    for i in order:
        if not math.isfinite(arrival[i]):
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            cand = arrival[i] + dist
            if cand < arrival[j]:
                arrival[j] = cand

    return positions, dict(adj), arrival


def main():
    print("=" * 78)
    print("CALIBRATED PLACEMENT: Fine alpha sweep + barrier-only variant")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 16 seeds")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16

    # Part 1: Fine alpha sweep to find gap~2.0
    print("PART 1: Alpha sweep at N=25 and N=40")
    print(f"  {'alpha':>6s}  {'N':>3s}  {'eff_gap':>7s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'grav':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 54}")

    for alpha in [0.0, 0.3, 0.5, 0.7, 1.0, 1.5]:
        for nl in [25, 40]:
            grav_all, pm_all, dec_all, gap_all = [], [], [], []
            for seed in range(n_seeds):
                positions, adj, _ = generate_placement_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 7 + 3, alpha=alpha,
                )
                gap_all.append(measure_gap(positions, nl))
                r = run_joint(positions, adj, k_band, nl)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            if grav_all:
                ag = sum(grav_all) / len(grav_all)
                apm = sum(pm_all) / len(pm_all)
                adec = sum(dec_all) / len(dec_all)
                agap = sum(gap_all) / len(gap_all)
                print(f"  {alpha:6.1f}  {nl:3d}  {agap:7.2f}  {apm:8.4f}  "
                      f"{adec:+8.4f}  {ag:+8.3f}  {len(grav_all):4d}")

    print()

    # Part 2: Barrier-only placement
    print("PART 2: Barrier-only placement (bias only first 3 post-barrier layers)")
    print(f"  {'alpha':>6s}  {'N':>3s}  {'eff_gap':>7s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'grav':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 54}")

    for alpha in [1.0, 2.0, 4.0]:
        for nl in [25, 40]:
            grav_all, pm_all, dec_all, gap_all = [], [], [], []
            for seed in range(n_seeds):
                positions, adj, _ = generate_barrier_only_placement(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 7 + 3,
                    alpha=alpha, barrier_width=3,
                )
                gap_all.append(measure_gap(positions, nl))
                r = run_joint(positions, adj, k_band, nl)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            if grav_all:
                ag = sum(grav_all) / len(grav_all)
                apm = sum(pm_all) / len(pm_all)
                adec = sum(dec_all) / len(dec_all)
                agap = sum(gap_all) / len(gap_all)
                print(f"  {alpha:6.1f}  {nl:3d}  {agap:7.2f}  {apm:8.4f}  "
                      f"{adec:+8.4f}  {ag:+8.3f}  {len(grav_all):4d}")

    print()
    print("PASS = pur_min < uniform baseline AND eff_gap > 1.5")
    print("This would mean calibrated placement improves decoherence")


if __name__ == "__main__":
    main()
