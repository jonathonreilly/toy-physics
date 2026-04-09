#!/usr/bin/env python3
"""3D hard-geometry pilot: asymmetry-based event persistence.

Instead of pruning an already-built graph, generate the post-barrier geometry
with a survival rule:

- build the DAG layer by layer
- after the barrier, maintain slit-conditioned path counts from the retained
  slit nodes
- in the first post-barrier persistence band, reject candidate nodes whose
  slit-path asymmetry is too low

This is still a bounded toy rule, but it is closer to a genuine
event-persistence / hard-geometry mechanism than post-hoc pruning.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.gap_topological_asymmetry import K_BAND, measure


def generate_3d_asymmetry_persistence_dag(
    n_layers: int,
    nodes_per_layer: int,
    xyz_range: float,
    connect_radius: float,
    rng_seed: int,
    asym_thresh: float,
    persistence_depth: int,
):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    counts_a = []
    counts_b = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        pending = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            counts_a.append(0)
            counts_b.append(0)
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                parents = []
                ca = 0
                cb = 0
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            parents.append(prev_idx)
                            ca += counts_a[prev_idx]
                            cb += counts_b[prev_idx]

                keep = True
                if barrier_layer < layer <= barrier_layer + persistence_depth and asym_thresh > 0:
                    total = ca + cb
                    asym = abs(ca - cb) / total if total > 0 else 0.0
                    keep = asym >= asym_thresh

                if keep:
                    idx = len(positions)
                    positions.append((x, y, z))
                    counts_a.append(ca)
                    counts_b.append(cb)
                    layer_nodes.append(idx)
                    pending.append((idx, parents))

            for idx, parents in pending:
                for prev_idx in parents:
                    adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

        if layer == barrier_layer:
            barrier_nodes = layer_indices[layer]
            slit_upper = [i for i in barrier_nodes if positions[i][1] > 3][:3]
            slit_lower = [i for i in barrier_nodes if positions[i][1] < -3][:3]
            slit_upper = sorted(slit_upper, key=lambda i: positions[i][1], reverse=True)[:3]
            slit_lower = sorted(slit_lower, key=lambda i: positions[i][1])[:3]
            for idx in barrier_nodes:
                counts_a[idx] = 1 if idx in slit_upper else 0
                counts_b[idx] = 1 if idx in slit_lower else 0

    return positions, dict(adj), barrier_layer


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60, 80])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.0, 0.1, 0.2])
    parser.add_argument("--npl", type=int, default=30)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--n-seeds", type=int, default=16)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 108)
    print("ASYMMETRY PERSISTENCE PILOT")
    print("  3D layer-by-layer generation with low-asymmetry post-barrier nodes rejected on creation")
    print(
        f"  npl={args.npl}, xyz_range={args.xyz_range}, r={args.connect_radius}, "
        f"seeds={args.n_seeds}, k-band={K_BAND}"
    )
    print("=" * 108)
    print()

    for nl in args.n_layers:
        persistence_depth = max(1, round(nl / 6))
        print(f"N = {nl}  (persistence depth = {persistence_depth} layers)")
        print(
            f"  {'thr':>4s}  {'pur_cl':>14s}  {'S_norm':>12s}  "
            f"{'gravity':>14s}  {'keep%':>7s}  {'ok':>3s}"
        )
        print("  " + "-" * 70)
        for thresh in args.thresholds:
            purs = []
            sns = []
            gravs = []
            keeps = []
            for seed in seeds:
                positions, adj, barrier_layer = generate_3d_asymmetry_persistence_dag(
                    nl,
                    args.npl,
                    args.xyz_range,
                    args.connect_radius,
                    seed,
                    thresh,
                    persistence_depth,
                )
                baseline_nodes = 1 + (nl - 1) * args.npl
                keeps.append(100.0 * len(positions) / baseline_nodes)
                res = measure(positions, adj, nl, K_BAND)
                if res:
                    purs.append(res["pur_cl"])
                    sns.append(res["s_norm"])
                    gravs.append(res["gravity"])
            pur_s = "FAIL" if not purs else f"{mean_se(purs)[0]:.3f}±{mean_se(purs)[1]:.3f}"
            sn_s = "FAIL" if not sns else f"{mean_se(sns)[0]:.3f}"
            grav_s = "FAIL" if not gravs else f"{mean_se(gravs)[0]:+.3f}±{mean_se(gravs)[1]:.3f}"
            keep_s = f"{(sum(keeps)/len(keeps)) if keeps else math.nan:5.1f}%"
            print(f"  {thresh:4.2f}  {pur_s:>14s}  {sn_s:>12s}  {grav_s:>14s}  {keep_s:>7s}  {len(purs):3d}")
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
