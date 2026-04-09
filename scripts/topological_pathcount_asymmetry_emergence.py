#!/usr/bin/env python3
"""Topological path-count asymmetry as an emergence rule.

Idea:
  1. Build a uniform causal DAG.
  2. Count the number of directed paths to each post-barrier node from the
     source with only the upper slit open and with only the lower slit open.
  3. Compute a graph-native asymmetry score
         A(i) = |p_upper(i) - p_lower(i)| / (p_upper(i) + p_lower(i))
  4. Remove post-barrier nodes with low asymmetry and measure whether that
     creates decoherence.

This is deliberately topological: no amplitudes are used in the pruning rule.
"""

from __future__ import annotations

import argparse
import math
from collections import defaultdict, deque
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.node_removal_emergence import (
    BETA,
    LAM,
    N_YBINS,
    bin_amplitudes,
    cl_purity_triple,
    compute_field,
    propagate_full,
)


def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def _build_setup(n_layers, nodes_per_layer, y_range, connect_radius, seed, candidate_depth_frac):
    positions, adj, _ = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=nodes_per_layer,
        y_range=y_range,
        connect_radius=connect_radius,
        rng_seed=seed,
    )
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y in positions) / len(positions)
    bl_idx = len(layers) // 3
    barrier_layer = layers[bl_idx]
    bi = by_layer[barrier_layer]
    slit_upper = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_lower = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_upper or not slit_lower:
        return None

    blocked = set(bi) - set(slit_upper + slit_lower)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers), start + env_depth)
    mid = []
    post_nodes = []
    candidate_post_nodes = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    post_layers = [layer for layer in layers if layer > barrier_layer and layer != layers[-1]]
    candidate_stop = max(1, math.ceil(len(post_layers) * candidate_depth_frac))
    candidate_layers = set(post_layers[:candidate_stop])
    for layer in post_layers:
        if layer <= barrier_layer or layer == layers[-1]:
            continue
        post_nodes.extend(by_layer[layer])
        if layer in candidate_layers:
            candidate_post_nodes.extend(by_layer[layer])

    return {
        "positions": positions,
        "adj": adj,
        "by_layer": by_layer,
        "layers": layers,
        "src": src,
        "det_list": det_list,
        "cy": cy,
        "blocked": blocked,
        "slit_upper": slit_upper,
        "slit_lower": slit_lower,
        "mass_nodes": mass_nodes,
        "mid": mid,
        "post_nodes": post_nodes,
        "candidate_post_nodes": candidate_post_nodes,
        "barrier_layer": barrier_layer,
    }


def _path_counts(adj, n, src, blocked):
    counts = [0] * n
    order = _topo_order(adj, n)
    for s in src:
        if s not in blocked:
            counts[s] = 1
    for i in order:
        if counts[i] == 0 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            counts[j] += counts[i]
    return counts


def _remove_low_asymmetry(adj, asymmetry_by_node, threshold):
    remove = {i for i, a in asymmetry_by_node.items() if a < threshold}
    new_adj = {}
    for i, nbs in adj.items():
        if i in remove:
            continue
        new_adj[i] = [j for j in nbs if j not in remove]
    return new_adj, remove


def _measure_pur_cl(positions, adj, setup, k_band):
    src = setup["src"]
    det_list = setup["det_list"]
    blocked = setup["blocked"]
    sa = setup["slit_upper"]
    sb = setup["slit_lower"]
    mid = setup["mid"]
    field_m = compute_field(positions, setup["mass_nodes"], 0.1)

    pur_cl_vals = []
    s_norm_vals = []
    pur_min_vals = []
    for k in k_band:
        aa = propagate_full(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_full(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes(aa, positions, mid)
        bb = bin_amplitudes(ab, positions, mid)
        s_raw = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        na = sum(abs(a) ** 2 for a in ba)
        nb = sum(abs(b) ** 2 for b in bb)
        s_norm = s_raw / (na + nb) if (na + nb) > 0 else 0.0
        d_cl = math.exp(-LAM ** 2 * s_norm)
        pur_cl, _pur_coh, pur_min = cl_purity_triple(aa, ab, d_cl, det_list)
        if not math.isnan(pur_cl):
            pur_cl_vals.append(pur_cl)
            pur_min_vals.append(pur_min)
            s_norm_vals.append(s_norm)

    if not pur_cl_vals:
        return None
    return {
        "pur_cl": sum(pur_cl_vals) / len(pur_cl_vals),
        "pur_min": sum(pur_min_vals) / len(pur_min_vals),
        "s_norm": sum(s_norm_vals) / len(s_norm_vals),
    }


def run_one(n_layers, seed, threshold, candidate_depth_frac):
    setup = _build_setup(
        n_layers=n_layers,
        nodes_per_layer=25,
        y_range=12.0,
        connect_radius=3.0,
        seed=seed,
        candidate_depth_frac=candidate_depth_frac,
    )
    if setup is None:
        return None

    positions = setup["positions"]
    adj = setup["adj"]
    n = len(positions)
    blocked = setup["blocked"]
    upper_only = blocked | set(setup["slit_lower"])
    lower_only = blocked | set(setup["slit_upper"])

    counts_u = _path_counts(adj, n, setup["src"], upper_only)
    counts_l = _path_counts(adj, n, setup["src"], lower_only)

    asymmetry_by_node = {}
    near_vals = []
    far_vals = []
    for i in setup["post_nodes"]:
        cu = counts_u[i]
        cl = counts_l[i]
        total = cu + cl
        if total > 0:
            asym = abs(cu - cl) / total
        else:
            asym = 0.0
        asymmetry_by_node[i] = asym
        ay = abs(positions[i][1] - setup["cy"])
        if ay <= 1.0:
            near_vals.append(asym)
        if ay >= 5.0:
            far_vals.append(asym)

    metrics_base = _measure_pur_cl(positions, adj, setup, [3.0, 5.0, 7.0])
    if metrics_base is None:
        return None

    candidate_asymmetry = {
        i: asymmetry_by_node[i] for i in setup["candidate_post_nodes"]
    }
    pruned_adj, removed = _remove_low_asymmetry(adj, candidate_asymmetry, threshold)
    metrics_pruned = _measure_pur_cl(positions, pruned_adj, setup, [3.0, 5.0, 7.0])
    if metrics_pruned is None:
        return None

    return {
        "near_asym": sum(near_vals) / len(near_vals) if near_vals else math.nan,
        "far_asym": sum(far_vals) / len(far_vals) if far_vals else math.nan,
        "removed_frac": len(removed) / max(1, len(setup["post_nodes"])),
        "pur_cl_base": metrics_base["pur_cl"],
        "pur_cl_pruned": metrics_pruned["pur_cl"],
        "pur_min_base": metrics_base["pur_min"],
        "pur_min_pruned": metrics_pruned["pur_min"],
        "s_norm_base": metrics_base["s_norm"],
        "s_norm_pruned": metrics_pruned["s_norm"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-list", nargs="+", type=int, default=[40, 60])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.10, 0.20])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--candidate-depth-frac", type=float, default=1.0)
    args = parser.parse_args()

    print("=" * 88)
    print("TOPOLOGICAL PATH-COUNT ASYMMETRY EMERGENCE")
    print("  Remove low-asymmetry post-barrier nodes using pure path counts")
    print("=" * 88)
    print()

    print("PART 1: spatial asymmetry diagnostic (baseline graphs)")
    print(f"  {'N':>4s}  {'near(|y-c|<=1)':>16s}  {'far(|y-c|>=5)':>16s}  {'n_ok':>4s}")
    print(f"  {'-' * 48}")
    for nl in args.n_list:
        near_all, far_all = [], []
        for seed in range(args.n_seeds):
            r = run_one(nl, seed * 7 + 3, 0.0, args.candidate_depth_frac)
            if r is None:
                continue
            if not math.isnan(r["near_asym"]):
                near_all.append(r["near_asym"])
            if not math.isnan(r["far_asym"]):
                far_all.append(r["far_asym"])
        if near_all and far_all:
            print(f"  {nl:4d}  {sum(near_all)/len(near_all):16.3f}  {sum(far_all)/len(far_all):16.3f}  {len(near_all):4d}")
        else:
            print(f"  {nl:4d}  FAIL")

    print()
    print("PART 2: threshold pruning by path-count asymmetry")
    print(f"  {'N':>4s}  {'thr':>5s}  {'removed':>8s}  {'pur_cl b/p':>17s}  {'S_norm b/p':>17s}  {'n_ok':>4s}")
    print(f"  {'-' * 72}")
    for nl in args.n_list:
        for threshold in args.thresholds:
            removed_all = []
            pur_b, pur_p = [], []
            sn_b, sn_p = [], []
            for seed in range(args.n_seeds):
                r = run_one(nl, seed * 7 + 3, threshold, args.candidate_depth_frac)
                if r is None:
                    continue
                removed_all.append(r["removed_frac"])
                pur_b.append(r["pur_cl_base"])
                pur_p.append(r["pur_cl_pruned"])
                sn_b.append(r["s_norm_base"])
                sn_p.append(r["s_norm_pruned"])
            if pur_b:
                print(
                    f"  {nl:4d}  {threshold:5.2f}  {sum(removed_all)/len(removed_all):8.3f}  "
                    f"{sum(pur_b)/len(pur_b):8.3f}/{sum(pur_p)/len(pur_p):8.3f}  "
                    f"{sum(sn_b)/len(sn_b):8.3f}/{sum(sn_p)/len(sn_p):8.3f}  {len(pur_b):4d}"
                )
            else:
                print(f"  {nl:4d}  {threshold:5.2f}  FAIL")


if __name__ == "__main__":
    main()
