#!/usr/bin/env python3
"""Topological asymmetry pruning + layer normalization in 3D.

This tests whether the strongest supported graph-native pruning rule from
`gap_topological_asymmetry.py` stacks with the strongest supported regulated
propagator result (per-layer normalization).

We measure pur_min, not CL-bath pur_cl, because earlier gap+norm work showed
the CL-bath proxy is largely insensitive to global amplitude normalization.
"""

from __future__ import annotations

import argparse
import cmath
from collections import defaultdict
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.gap_topological_asymmetry import (
    BETA,
    K_BAND,
    _topo_order,
    compute_field_3d,
    compute_path_count,
    generate_3d_dag_uniform,
)


def propagate_3d_layernorm(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if abs(amps[i]) < 1e-30 or i in blocked:
                continue
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1, z1 = positions[i]
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
                w = math.exp(-BETA * theta * theta)
                ea = cmath.exp(1j * k * act) * w / L
                amps[j] += amps[i] * ea

        if li + 1 < len(layers):
            next_nodes = by_layer[layers[li + 1]]
            total_sq = sum(abs(amps[i]) ** 2 for i in next_nodes)
            if total_sq > 1e-30:
                norm = math.sqrt(total_sq)
                for i in next_nodes:
                    amps[i] /= norm

    return amps


def propagate_3d_linear(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def purity_min(amps_a, amps_b, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def build_pruned_graph(nl, seed, thresh, npl, xyz_range, connect_radius):
    positions, adj_raw, bl = generate_3d_dag_uniform(nl, npl, xyz_range, connect_radius, seed)
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mid_mass = []
    for layer in layers[start:stop]:
        mid_mass.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field_3d(positions, list(set(mid_mass) | set(mass_nodes)))

    order = _topo_order(adj_raw, n)
    adj_a = {}
    blocked_a = blocked | set(sb)
    for i, nbs in adj_raw.items():
        if i not in blocked_a:
            adj_a[i] = [j for j in nbs if j not in blocked_a]
    adj_b = {}
    blocked_b = blocked | set(sa)
    for i, nbs in adj_raw.items():
        if i not in blocked_b:
            adj_b[i] = [j for j in nbs if j not in blocked_b]

    pc_a = compute_path_count(adj_a, sa, n, order)
    pc_b = compute_path_count(adj_b, sb, n, order)

    protected = set(src) | set(det_list) | set(sa + sb)
    removed = set()
    for idx in range(n):
        x, y, z = positions[idx]
        if x <= bl or idx in protected:
            continue
        total = pc_a[idx] + pc_b[idx]
        asym = abs(pc_a[idx] - pc_b[idx]) / total if total > 0 else 0.0
        if asym < thresh:
            removed.add(idx)

    pruned_adj = {}
    for i, nbs in adj_raw.items():
        if i in removed:
            continue
        kept = [j for j in nbs if j not in removed]
        if kept:
            pruned_adj[i] = kept

    return {
        "positions": positions,
        "adj_raw": adj_raw,
        "adj_pruned": pruned_adj,
        "field": field,
        "src": src,
        "det_list": det_list,
        "blocked": blocked,
        "sa": sa,
        "sb": sb,
        "removed_frac": len(removed) / max(1, sum(1 for idx, (x, _, _) in enumerate(positions) if x > bl and idx not in protected)),
    }


def run_case(graph, use_pruned, use_layernorm):
    adj = graph["adj_pruned"] if use_pruned else graph["adj_raw"]
    prop = propagate_3d_layernorm if use_layernorm else propagate_3d_linear
    vals = []
    for k in K_BAND:
        aa = prop(graph["positions"], adj, graph["field"], graph["src"], k, graph["blocked"] | set(graph["sb"]))
        ab = prop(graph["positions"], adj, graph["field"], graph["src"], k, graph["blocked"] | set(graph["sa"]))
        pm = purity_min(aa, ab, graph["det_list"])
        if not math.isnan(pm):
            vals.append(pm)
    if not vals:
        return math.nan
    return sum(vals) / len(vals)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.1, 0.2])
    parser.add_argument("--n-seeds", type=int, default=16)
    parser.add_argument("--npl", type=int, default=30)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    print("=" * 96)
    print("3D TOPOLOGICAL ASYMMETRY + LAYER NORM COMBO")
    print("  Measure pur_min on baseline/pruned graphs with linear vs layernorm propagation")
    print(f"  seeds={args.n_seeds}, npl={args.npl}, xyz_range={args.xyz_range}, r={args.connect_radius}")
    print("=" * 96)
    print()

    for nl in args.n_layers:
        for thresh in args.thresholds:
            rows = []
            t0 = time.time()
            for seed in seeds:
                graph = build_pruned_graph(nl, seed, thresh, args.npl, args.xyz_range, args.connect_radius)
                if graph is None:
                    continue
                rows.append({
                    "removed_frac": graph["removed_frac"],
                    "base_lin": run_case(graph, False, False),
                    "base_ln": run_case(graph, False, True),
                    "pruned_lin": run_case(graph, True, False),
                    "pruned_ln": run_case(graph, True, True),
                })
            dt = time.time() - t0
            valid = [r for r in rows if all(not math.isnan(r[k]) for k in ("base_lin", "base_ln", "pruned_lin", "pruned_ln"))]
            if not valid:
                print(f"N={nl} thresh={thresh:.1f} FAIL")
                continue
            def mean_key(key):
                return sum(r[key] for r in valid) / len(valid)
            print(
                f"N={nl:3d}  thr={thresh:.1f}  rem={mean_key('removed_frac')*100:4.1f}%  "
                f"base_lin={mean_key('base_lin'):.3f}  base_ln={mean_key('base_ln'):.3f}  "
                f"pruned_lin={mean_key('pruned_lin'):.3f}  pruned_ln={mean_key('pruned_ln'):.3f}  "
                f"n={len(valid):2d}  t={dt:4.0f}s"
            )


if __name__ == "__main__":
    main()
