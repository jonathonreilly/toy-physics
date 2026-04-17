#!/usr/bin/env python3
"""Mutual information across canonical mirror DAG families.

This extends the retained exact-mirror MI harness by measuring
I(slit_label; detector_y_bin) on the broader set of canonical 3D mirror
families used elsewhere in the repo, rather than only on the strict
chokepoint lane.

Families covered:
  1. Original Z2 mirror family from the same generator code path as
     `mirror_symmetric_dag.py` (imported from the lighter-weight
     `symmetry_spectrum_mirror_compare.py` companion to avoid the optional
     spectral `numpy` dependency)
  2. Strict mirror chokepoint family from `mirror_chokepoint_joint.py`
  3. Scaled hybrid S4 mirror family from `mirror_scaled_joint.py`

Matched random baselines are included where practical:
  - exact original random companion
  - exact strict chokepoint random companion
  - local random hybrid baseline with the same lookback rule as S4

All measurements use the same strictly linear propagator and gravity-field
construction as the review-safe mirror joint scripts.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
import time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.mirror_chokepoint_joint import (
    K,
    N_SEEDS,
    XYZ_RANGE,
    compute_field_3d,
    generate_mirror_chokepoint_dag,
    generate_random_chokepoint_dag,
    propagate_3d,
)
from scripts.mirror_scaled_joint import generate_mirror_hybrid
from scripts.symmetry_spectrum_mirror_compare import generate_mirror_dag, generate_random_dag

N_YBINS = 8


def _mean_se(vals: list[float]) -> tuple[float, float]:
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def generate_random_hybrid_dag(
    n_layers: int,
    npl_total: int,
    xyz_range: float,
    connect_radius: float,
    rng_seed: int,
    barrier_chokepoint: bool = True,
):
    """Random baseline matched to the S4 hybrid lookback rule."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            if barrier_chokepoint and layer == barrier_layer + 1:
                lookback_start = max(0, len(layer_indices) - 1)
            else:
                lookback_start = max(0, len(layer_indices) - 2)

            for _ in range(npl_total):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[lookback_start:]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), barrier_layer


def _by_layer(positions):
    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    layers = sorted(by_layer.keys())
    return by_layer, layers


def _select_slits(positions, barrier_nodes, center_y):
    slit_a = [i for i in barrier_nodes if positions[i][1] > center_y + 3][:3]
    slit_b = [i for i in barrier_nodes if positions[i][1] < center_y - 3][:3]
    return slit_a, slit_b


def _detector_bin_probs(positions, det_list, amps, y_extent):
    probs = [0.0] * N_YBINS
    bin_width = (2.0 * y_extent) / N_YBINS
    for d in det_list:
        bin_idx = int((positions[d][1] + y_extent) / bin_width)
        bin_idx = max(0, min(N_YBINS - 1, bin_idx))
        probs[bin_idx] += abs(amps[d]) ** 2
    norm = sum(probs)
    if norm <= 1e-30:
        return None
    return [p / norm for p in probs]


def measure_mi(positions, adj, barrier_layer: int, k: float):
    """Return MI, detector entropy, and conditional detector entropy."""
    by_layer, layers = _by_layer(positions)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    barrier_nodes = by_layer[layers[barrier_layer]]
    if len(barrier_nodes) < 6:
        return None

    center_y = sum(pos[1] for pos in positions) / len(positions)
    slit_a, slit_b = _select_slits(positions, barrier_nodes, center_y)
    if not slit_a or not slit_b:
        return None
    blocked = set(barrier_nodes) - set(slit_a + slit_b)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > center_y + 1]
    if not mass_nodes:
        return None

    field = compute_field_3d(positions, mass_nodes)
    psi_a = propagate_3d(positions, adj, field, src, k, blocked | set(slit_b))
    psi_b = propagate_3d(positions, adj, field, src, k, blocked | set(slit_a))

    prob_a = _detector_bin_probs(positions, det_list, psi_a, XYZ_RANGE)
    prob_b = _detector_bin_probs(positions, det_list, psi_b, XYZ_RANGE)
    if prob_a is None or prob_b is None:
        return None

    h_det = 0.0
    h_cond = 0.0
    for bin_idx in range(N_YBINS):
        p_mix = 0.5 * prob_a[bin_idx] + 0.5 * prob_b[bin_idx]
        if p_mix > 1e-30:
            h_det -= p_mix * math.log2(p_mix)
        if prob_a[bin_idx] > 1e-30:
            h_cond -= 0.5 * prob_a[bin_idx] * math.log2(prob_a[bin_idx])
        if prob_b[bin_idx] > 1e-30:
            h_cond -= 0.5 * prob_b[bin_idx] * math.log2(prob_b[bin_idx])

    return {
        "MI": h_det - h_cond,
        "H_det": h_det,
        "H_cond": h_cond,
    }


def canonical_families():
    return [
        (
            "orig-random",
            lambda seed, nl: generate_random_dag(nl, 30, XYZ_RANGE, 4.0, seed),
        ),
        (
            "orig-mirror",
            lambda seed, nl: generate_mirror_dag(nl, 15, XYZ_RANGE, 4.0, seed, 0.0)[:3],
        ),
        (
            "strict-random",
            lambda seed, nl: generate_random_chokepoint_dag(nl, 50, XYZ_RANGE, 4.0, seed, 0.0),
        ),
        (
            "strict-mirror",
            lambda seed, nl: generate_mirror_chokepoint_dag(nl, 25, XYZ_RANGE, 4.0, seed, 0.0)[:3],
        ),
        (
            "s4-random",
            lambda seed, nl: generate_random_hybrid_dag(nl, 80, XYZ_RANGE, 5.0, seed, True),
        ),
        (
            "s4-mirror",
            lambda seed, nl: generate_mirror_hybrid(nl, 40, XYZ_RANGE, 5.0, seed, True)[:3],
        ),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[15, 25, 40, 60, 80])
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--k", type=float, default=K)
    args = parser.parse_args()

    print("=" * 112)
    print("MIRROR MUTUAL INFORMATION: CANONICAL FAMILIES")
    print("  exact retained mirror generators + matched random baselines")
    print(f"  k={args.k}, seeds={args.n_seeds}, y-bins={N_YBINS}, y-range=[-{XYZ_RANGE:g}, {XYZ_RANGE:g}]")
    print("=" * 112)
    print()
    print(f"  {'family':>14s}  {'N':>4s}  {'MI(bits)':>11s}  {'H(det)':>9s}  {'H(det|s)':>10s}  {'ok':>3s}  {'time':>5s}")
    print("  " + "-" * 74)

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    for label, gen_fn in canonical_families():
        for nl in args.n_layers:
            t0 = time.time()
            mi_vals = []
            hd_vals = []
            hc_vals = []
            ok = 0
            for seed in seeds:
                positions, adj, barrier_layer = gen_fn(seed, nl)
                result = measure_mi(positions, adj, barrier_layer, args.k)
                if result is None:
                    continue
                ok += 1
                mi_vals.append(result["MI"])
                hd_vals.append(result["H_det"])
                hc_vals.append(result["H_cond"])

            elapsed = time.time() - t0
            if mi_vals:
                mi_mean, mi_se = _mean_se(mi_vals)
                hd_mean, _ = _mean_se(hd_vals)
                hc_mean, _ = _mean_se(hc_vals)
                print(
                    f"  {label:>14s}  {nl:4d}  {mi_mean:8.4f}±{mi_se:.3f}  "
                    f"{hd_mean:9.4f}  {hc_mean:10.4f}  {ok:3d}  {elapsed:4.0f}s"
                )
            else:
                print(f"  {label:>14s}  {nl:4d}  FAIL{'':>43s}  {elapsed:4.0f}s")
        print()

    print("MI = H(detector) - H(detector|slit) in bits (max = 1.0 for a binary slit label).")
    print("Mirror rows are generated by the exact canonical mirror families used elsewhere in the repo.")


if __name__ == "__main__":
    main()
