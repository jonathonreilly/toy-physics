#!/usr/bin/env python3
"""Generated paired-chokepoint DAGs for approximate symmetry testing.

This pilot asks a narrower question than the exact mirror baseline:
can we recover some of the mirror benefit from a generated scaffold that
induces approximate left/right pairing geometrically, without explicitly
copying every mirrored edge?

The comparison set is:
  - random chokepoint DAGs
  - generated paired-chokepoint DAGs with small symmetry noise
  - exact mirror chokepoint DAGs as the strong baseline

The retained metrics are the same review-safe ones used elsewhere:
  - corrected Born `|I3|/P`
  - `d_TV`
  - `pur_cl`
  - gravity centroid delta

The hope is not to beat the exact mirror baseline immediately. The hope is
to see whether a more axiom-friendly, generated symmetry construction keeps
enough of the effect to be a live long-term vector.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.mirror_chokepoint_joint import (
    K,
    N_SEEDS,
    _mean_se,
    generate_mirror_chokepoint_dag,
    measure_joint,
)


def generate_random_chokepoint_dag(n_layers, npl_total, xyz_range, connect_radius, rng_seed):
    """Random chokepoint DAG with the same layer-1-only connectivity rule.

    This is the no-symmetry control: positions are generated independently
    on each side, but the connectivity rule is still the same chokepoint
    geometry used by the mirror baseline.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(npl_total):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

            prev = layer_indices[-1]
            for prev_idx in prev:
                px, py, pz = positions[prev_idx]
                for curr_idx in layer_nodes:
                    cx, cy, cz = positions[curr_idx]
                    dist = math.sqrt((cx - px) ** 2 + (cy - py) ** 2 + (cz - pz) ** 2)
                    if dist <= connect_radius:
                        adj[prev_idx].append(curr_idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj)


def generate_paired_chokepoint_dag(
    n_layers,
    npl_half,
    xyz_range,
    connect_radius,
    rng_seed,
    pair_noise=0.15,
):
    """Generated approximate-symmetry chokepoint DAG.

    Each layer births paired nodes from a shared latent centerline, but the
    pair is not forced to be a literal mirrored copy. A small amount of
    independent noise is added to each partner so the family stays generated
    rather than hard-coded.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(npl_half):
                y0 = rng.uniform(0.5, xyz_range)
                z0 = rng.uniform(-xyz_range, xyz_range)
                dy1 = rng.uniform(-pair_noise, pair_noise)
                dy2 = rng.uniform(-pair_noise, pair_noise)
                dz1 = rng.uniform(-pair_noise, pair_noise)
                dz2 = rng.uniform(-pair_noise, pair_noise)

                idx_up = len(positions)
                positions.append((x, y0 + dy1, z0 + dz1))
                layer_nodes.append(idx_up)

                idx_lo = len(positions)
                positions.append((x, -y0 + dy2, z0 + dz2))
                layer_nodes.append(idx_lo)

            prev = layer_indices[-1]
            for prev_idx in prev:
                px, py, pz = positions[prev_idx]
                for curr_idx in layer_nodes:
                    cx, cy, cz = positions[curr_idx]
                    dist = math.sqrt((cx - px) ** 2 + (cy - py) ** 2 + (cz - pz) ** 2)
                    if dist <= connect_radius:
                        adj[prev_idx].append(curr_idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj)


def summarize(values):
    m, se = _mean_se(values)
    if math.isnan(m):
        return "FAIL"
    return f"{m:.4f}±{se:.4f}"


def evaluate_family(label, generator, gen_kwargs, n_layers_list, n_seeds):
    print(f"FAMILY: {label}")
    print(
        f"  {'N':>4s}  {'d_TV':>8s}  {'pur_cl':>12s}  {'Born':>10s}  "
        f"{'gravity':>14s}  {'k0':>10s}  {'ok':>3s}"
    )
    print("  " + "-" * 72)

    for nl in n_layers_list:
        dtv_vals = []
        pur_vals = []
        born_vals = []
        grav_vals = []
        k0_vals = []
        ok = 0
        for seed in [s * 7 + 3 for s in range(n_seeds)]:
            out = generator(nl=nl, seed=seed, **gen_kwargs)
            if out is None:
                continue
            positions, adj = out
            r = measure_joint(positions, adj, nl, K)
            if not r:
                continue
            dtv_vals.append(r["dtv"])
            pur_vals.append(r["pur_cl"])
            born_vals.append(r["born"])
            grav_vals.append(r["gravity"])
            k0_vals.append(r["grav_k0"])
            ok += 1

        print(
            f"  {nl:4d}  {summarize(dtv_vals):>8s}  {summarize(pur_vals):>12s}  "
            f"{summarize(born_vals):>10s}  {summarize(grav_vals):>14s}  "
            f"{summarize(k0_vals):>10s}  {ok:3d}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60, 80, 100])
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--npl-half", type=int, default=25)
    parser.add_argument("--pair-noise", nargs="+", type=float, default=[0.0, 0.15, 0.35])
    args = parser.parse_args()

    print("=" * 120)
    print("SYMMETRY-GENERATED PAIRED CHOKEPOINT PILOT")
    print("  approximate symmetry vs exact mirror chokepoint vs random chokepoint")
    print(
        f"  npl_half={args.npl_half} (paired total {2 * args.npl_half}), "
        f"n_layers={args.n_layers}, seeds={args.n_seeds}, connect_radius={args.connect_radius}"
    )
    print("=" * 120)
    print()

    evaluate_family(
        "random chokepoint",
        lambda nl, seed, **kw: generate_random_chokepoint_dag(
            nl, 2 * args.npl_half, kw["xyz_range"], kw["connect_radius"], seed
        ),
        {"xyz_range": args.xyz_range, "connect_radius": args.connect_radius},
        args.n_layers,
        args.n_seeds,
    )

    evaluate_family(
        "exact mirror chokepoint",
        lambda nl, seed, **kw: generate_mirror_chokepoint_dag(
            nl, kw["npl_half"], kw["xyz_range"], kw["connect_radius"], seed
        )[:2],
        {"npl_half": args.npl_half, "xyz_range": args.xyz_range, "connect_radius": args.connect_radius},
        args.n_layers,
        args.n_seeds,
    )

    for noise in args.pair_noise:
        evaluate_family(
            f"paired-generated noise={noise}",
            lambda nl, seed, **kw: generate_paired_chokepoint_dag(
                nl, kw["npl_half"], kw["xyz_range"], kw["connect_radius"], seed, pair_noise=kw["pair_noise"]
            ),
            {
                "npl_half": args.npl_half,
                "xyz_range": args.xyz_range,
                "connect_radius": args.connect_radius,
                "pair_noise": noise,
            },
            args.n_layers,
            args.n_seeds,
        )

    print("Interpretation:")
    print("  - If the paired-generated family keeps most of the mirror gap over random")
    print("    and stays Born-clean, the symmetry idea is a live axiom-friendly lane.")
    print("  - If it collapses quickly toward random as pair_noise grows, mirror is")
    print("    likely a hard-coded symmetry effect rather than a generative one.")


if __name__ == "__main__":
    main()
