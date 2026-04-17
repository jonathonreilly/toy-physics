#!/usr/bin/env python3
"""Local hard-geometry pilot using only event-persistence style support.

This script asks a narrower question than the path-count asymmetry lane:
can a node decide whether to persist from purely local incoming support,
without using any global path-count machinery?

We compare:
  - baseline uniform graph
  - local 1-hop same-side support pruning
  - local 2-hop same-side support pruning
  - hard-gap |y| exclusion as a geometric comparator

The retained hard-geometry insight is that the first third of the
post-barrier region is the relevant place to act.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.gap_local_asymmetry import K_BAND, generate_3d_dag_uniform, measure


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def _support_1hop(positions, rev_adj, idx):
    y = positions[idx][1]
    if abs(y) < 1e-12:
        return 0.5
    sign = 1.0 if y > 0 else -1.0
    parents = rev_adj.get(idx, [])
    if not parents:
        return 0.5
    same = sum(1 for p in parents if positions[p][1] * sign > 0)
    return same / len(parents)


def _support_2hop(positions, rev_adj, idx):
    y = positions[idx][1]
    if abs(y) < 1e-12:
        return 0.5
    sign = 1.0 if y > 0 else -1.0
    ancestors = set(rev_adj.get(idx, []))
    for p in list(ancestors):
        ancestors.update(rev_adj.get(p, []))
    if not ancestors:
        return 0.5
    same = sum(1 for a in ancestors if positions[a][1] * sign > 0)
    return same / len(ancestors)


def compute_reverse_adj(adj):
    rev = defaultdict(list)
    for i, nbs in adj.items():
        for j in nbs:
            rev[j].append(i)
    return dict(rev)


def build_pruned_graph(positions, adj, n_layers, rule, thresh, support_region_frac):
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    barrier_layer = len(layers) // 3
    prune_start = barrier_layer + 1
    prune_stop = min(len(layers), prune_start + max(1, round((len(layers) - prune_start) * support_region_frac)))
    src = set(by_layer[layers[0]])
    det = set(by_layer[layers[-1]])

    protected = set(src) | set(det)
    # Keep the slit layer itself intact; only prune the downstream region.
    protected |= set(by_layer[layers[barrier_layer]])

    rev_adj = compute_reverse_adj(adj)
    removed = set()
    eligible = 0
    for layer in layers[prune_start:prune_stop]:
        for idx in by_layer[layer]:
            if idx in protected:
                continue
            eligible += 1
            if rule == "1hop":
                obs = _support_1hop(positions, rev_adj, idx)
            elif rule == "2hop":
                obs = _support_2hop(positions, rev_adj, idx)
            elif rule == "absy":
                obs = abs(positions[idx][1])
            else:
                raise ValueError(f"unknown rule {rule}")
            if obs < thresh:
                removed.add(idx)

    pruned_adj = {}
    for i, nbs in adj.items():
        if i in removed:
            continue
        kept = [j for j in nbs if j not in removed]
        if kept:
            pruned_adj[i] = kept

    return {
        "adj": pruned_adj,
        "removed_frac": len(removed) / max(1, eligible),
        "removed": len(removed),
        "eligible": eligible,
    }


def run_case(positions, adj, n_layers):
    r = measure(positions, adj, n_layers, K_BAND)
    return r


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60, 80])
    parser.add_argument("--n-seeds", type=int, default=4)
    parser.add_argument("--npl", type=int, default=60)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--support-thresh", type=float, default=0.65)
    parser.add_argument("--absy-thresh", type=float, default=2.0)
    parser.add_argument("--support-region-frac", type=float, default=0.33)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 128)
    print("HARD-GEOMETRY LOCAL SUPPORT PILOT")
    print("  local event-persistence rules vs hard-gap comparator")
    print(f"  npl={args.npl}, connect_radius={args.connect_radius}, xyz_range={args.xyz_range}")
    print(f"  support_thresh={args.support_thresh}, |y|_thresh={args.absy_thresh}, seeds={args.n_seeds}")
    print("=" * 128)
    print()
    print(f"  {'N':>4s}  {'mode':>16s}  {'pur_cl':>10s}  {'S_norm':>8s}  {'grav':>10s}  {'rem%':>6s}  {'ok':>3s}")
    print(f"  {'-' * 74}")

    for nl in args.n_layers:
        # baseline
        base_pur, base_sn, base_gr, base_ok = [], [], [], 0
        rows = []
        for seed in seeds:
            pos, adj, _ = generate_3d_dag_uniform(nl, args.npl, args.xyz_range, args.connect_radius, seed)
            r = run_case(pos, adj, nl)
            if r:
                base_pur.append(r["pur_cl"])
                base_sn.append(r["s_norm"])
                base_gr.append(r["gravity"])
                base_ok += 1
        if base_pur:
            mp, sep = _mean_se(base_pur)
            ms, _ = _mean_se(base_sn)
            mg, _ = _mean_se(base_gr)
            print(f"  {nl:4d}  {'baseline':>16s}  {mp:7.4f}±{sep:.3f}  {ms:8.4f}  {mg:+10.4f}  {'--':>6s}  {base_ok:3d}")

        for rule, thresh, label in [
            ("1hop", args.support_thresh, "local-1hop"),
            ("2hop", args.support_thresh, "local-2hop"),
            ("absy", args.absy_thresh, "|y|<2.0"),
        ]:
            pur_vals, sn_vals, gr_vals, rem_vals, ok = [], [], [], [], 0
            for seed in seeds:
                pos, adj, _ = generate_3d_dag_uniform(nl, args.npl, args.xyz_range, args.connect_radius, seed)
                pr = build_pruned_graph(pos, adj, nl, rule, thresh, args.support_region_frac)
                if not pr:
                    continue
                r = run_case(pos, pr["adj"], nl)
                if not r:
                    continue
                pur_vals.append(r["pur_cl"])
                sn_vals.append(r["s_norm"])
                gr_vals.append(r["gravity"])
                rem_vals.append(pr["removed_frac"] * 100.0)
                ok += 1
            if pur_vals:
                mp, sep = _mean_se(pur_vals)
                ms, _ = _mean_se(sn_vals)
                mg, _ = _mean_se(gr_vals)
                mr, _ = _mean_se(rem_vals)
                print(f"  {nl:4d}  {label:>16s}  {mp:7.4f}±{sep:.3f}  {ms:8.4f}  {mg:+10.4f}  {mr:5.1f}%  {ok:3d}")
            else:
                print(f"  {nl:4d}  {label:>16s}  FAIL")
        print()

    print("READ:")
    print("  local-1hop / local-2hop near hard-gap => local persistence may be enough")
    print("  hard-gap still best => geometry remains the main ingredient")
    print("  all local rules weak => nonlocal path structure still needed")


if __name__ == "__main__":
    main()
