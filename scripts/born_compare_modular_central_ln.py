#!/usr/bin/env python3
"""Corrected Born comparison for the two best bounded unitary lanes.

Compares, on the same corrected Sorkin harness:

- modular gap + layernorm
- central-band |y|-removal + layernorm

The goal is apples-to-apples:
- same N sweep
- same seed set
- same corrected I3 = ... - P(empty)
- same layernorm propagator class

We report both a two-slit purity floor (`pur_min`) and the corrected Born
ratio (`|I3|/P`) so we can see whether the lanes are Born-clean and which one
is more stable across the matched controls.
"""

from __future__ import annotations

import argparse
import cmath
from collections import defaultdict, deque
import math
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.combined_gravity_scaling import compute_field, propagate_linear, propagate_ln
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.topology_families import generate_modular_dag

BETA = 0.8
K_BAND = [3.0, 5.0, 7.0]


def _mean_se(vals: list[float]) -> tuple[float, float]:
    if not vals:
        return math.nan, math.nan
    mean = statistics.fmean(vals)
    if len(vals) < 2:
        return mean, 0.0
    return mean, statistics.stdev(vals) / math.sqrt(len(vals))


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
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


def _purity_min(amps_a, amps_b, det_list):
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


def _select_slits(barrier_nodes, positions, cy):
    upper = [i for i in barrier_nodes if positions[i][1] > cy + 2.0]
    lower = [i for i in barrier_nodes if positions[i][1] < cy - 2.0]
    middle = [i for i in barrier_nodes if abs(positions[i][1] - cy) <= 2.0]
    if not upper or not lower or not middle:
        return None
    return [upper[0]], [lower[0]], [middle[0]]


def _build_modular_graph(nl, seed, npl, y_range, connect_radius, gap):
    positions, adj_raw, layer_indices = generate_modular_dag(
        n_layers=nl,
        nodes_per_layer=npl,
        y_range=y_range,
        connect_radius=connect_radius,
        rng_seed=seed,
        crosslink_prob=0.02,
        gap=gap,
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

    cy = statistics.fmean(positions[i][1] for i in range(len(positions)))
    bl_idx = len(layers) // 3
    barrier_nodes = by_layer[layers[bl_idx]]
    slits = _select_slits(barrier_nodes, positions, cy)
    if slits is None:
        return None
    slit_a, slit_b, slit_c = slits
    base_blocked = set(barrier_nodes) - set(slit_a + slit_b + slit_c)

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mass_env = []
    for layer in layers[start:stop]:
        mass_env.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, list(set(mass_env) | set(grav_mass)))

    return {
        "positions": positions,
        "adj_raw": adj_raw,
        "adj": adj_raw,
        "src": src,
        "det_list": det_list,
        "base_blocked": base_blocked,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "slit_c": slit_c,
        "field": field,
    }


def _build_central_graph(nl, seed, npl, y_range, connect_radius, y_cut):
    positions, adj_raw, _ = generate_causal_dag(
        n_layers=nl,
        nodes_per_layer=npl,
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

    cy = statistics.fmean(positions[i][1] for i in range(len(positions)))
    bl_idx = len(layers) // 3
    barrier_nodes = by_layer[layers[bl_idx]]
    slits = _select_slits(barrier_nodes, positions, cy)
    if slits is None:
        return None
    slit_a, slit_b, slit_c = slits

    protected = set(src) | set(det_list) | set(slit_a + slit_b + slit_c)
    removed = set()
    for idx, (x, y) in enumerate(positions):
        if x <= layers[bl_idx] or idx in protected:
            continue
        if abs(y - cy) < y_cut:
            removed.add(idx)

    adj = {}
    for i, nbs in adj_raw.items():
        if i in removed:
            continue
        kept = [j for j in nbs if j not in removed]
        if kept:
            adj[i] = kept

    base_blocked = set(barrier_nodes) - set(slit_a + slit_b + slit_c)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mass_env = []
    for layer in layers[start:stop]:
        mass_env.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, list(set(mass_env) | set(mass_nodes)))

    return {
        "positions": positions,
        "adj_raw": adj_raw,
        "adj_pruned": adj,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "base_blocked": base_blocked,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "slit_c": slit_c,
        "field": field,
        "removed_frac": len(removed) / max(1, sum(1 for idx, (x, _) in enumerate(positions) if x > layers[bl_idx] and idx not in protected)),
    }


def _propagate(positions, adj, field, src, k, blocked, use_ln):
    if use_ln:
        return propagate_ln(positions, adj, field, src, k, blocked)
    return propagate_linear(positions, adj, field, src, k, blocked)


def _pur_min_for_graph(graph, use_ln):
    vals = []
    for k in K_BAND:
        aa = _propagate(
            graph["positions"],
            graph["adj"],
            graph["field"],
            graph["src"],
            k,
            graph["base_blocked"] | set(graph["slit_b"]) ,
            use_ln,
        )
        ab = _propagate(
            graph["positions"],
            graph["adj"],
            graph["field"],
            graph["src"],
            k,
            graph["base_blocked"] | set(graph["slit_a"]),
            use_ln,
        )
        pm = _purity_min(aa, ab, graph["det_list"])
        if not math.isnan(pm):
            vals.append(pm)
    return math.nan if not vals else statistics.fmean(vals)


def _born_for_graph(graph, use_ln):
    vals = []
    all_slits = set(graph["slit_a"]) | set(graph["slit_b"]) | set(graph["slit_c"])

    for k in K_BAND:
        def total_prob(open_set):
            blocked = graph["base_blocked"] | (all_slits - set(open_set))
            amps = _propagate(
                graph["positions"],
                graph["adj"],
                graph["field"],
                graph["src"],
                k,
                blocked,
                use_ln,
            )
            return sum(abs(amps[d]) ** 2 for d in graph["det_list"])

        P_abc = total_prob(all_slits)
        if P_abc <= 1e-30:
            continue
        P_ab = total_prob(set(graph["slit_a"]) | set(graph["slit_b"]))
        P_ac = total_prob(set(graph["slit_a"]) | set(graph["slit_c"]))
        P_bc = total_prob(set(graph["slit_b"]) | set(graph["slit_c"]))
        P_a = total_prob(set(graph["slit_a"]))
        P_b = total_prob(set(graph["slit_b"]))
        P_c = total_prob(set(graph["slit_c"]))
        P_empty = total_prob(set())
        I3 = P_abc - P_ab - P_ac - P_bc + P_a + P_b + P_c - P_empty
        vals.append(abs(I3) / P_abc)

    return vals


def _evaluate_family(name, builder, n_layers_list, seeds, use_ln, **kwargs):
    print(f"[{name} {'LN' if use_ln else 'linear'}]")
    print(f"  {'N':>4s}  {'pur_min':>10s}  {'Born mean':>12s}  {'Born max':>10s}  {'n_ok':>4s}  {'rem%':>6s}")
    print(f"  {'-' * 56}")

    for nl in n_layers_list:
        pur_vals = []
        born_vals = []
        rems = []
        n_ok = 0
        for seed in seeds:
            graph = builder(nl, seed, **kwargs)
            if graph is None:
                continue
            born_rows = _born_for_graph(graph, use_ln)
            if not born_rows:
                continue
            pm = _pur_min_for_graph(graph, use_ln)
            if math.isnan(pm):
                continue
            pur_vals.append(pm)
            born_vals.extend(born_rows)
            if "removed_frac" in graph:
                rems.append(100.0 * graph["removed_frac"])
            n_ok += 1

        pur_m, _ = _mean_se(pur_vals)
        born_m, born_se = _mean_se(born_vals)
        born_max = max(born_vals) if born_vals else math.nan
        rem_m = sum(rems) / len(rems) if rems else math.nan
        pur_s = "FAIL" if math.isnan(pur_m) else f"{pur_m:.3f}"
        born_m_s = "FAIL" if math.isnan(born_m) else f"{born_m:.2e}"
        born_max_s = "FAIL" if math.isnan(born_max) else f"{born_max:.2e}"
        rem_s = "  —  " if math.isnan(rem_m) else f"{rem_m:5.1f}%"
        print(f"  {nl:4d}  {pur_s:>10s}  {born_m_s:>12s}  {born_max_s:>10s}  {n_ok:4d}  {rem_s:>6s}")
        sys.stdout.flush()
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 40, 60])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--npl", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--gap", type=float, default=2.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    print("=" * 110)
    print("CORRECTED BORN COMPARISON: MODULAR GAP + LN VS CENTRAL-BAND |y|-REMOVAL + LN")
    print("  Same corrected Sorkin metric with -P(empty), matched seeds, matched N")
    print(
        f"  seeds={args.n_seeds}, npl={args.npl}, y_range={args.y_range}, r={args.connect_radius}, "
        f"gap={args.gap}, y_cut={args.y_cut}"
    )
    print("=" * 110)
    print()

    modular_builder = lambda nl, seed, npl=args.npl, y_range=args.y_range, connect_radius=args.connect_radius, gap=args.gap: _build_modular_graph(
        nl, seed, npl, y_range, connect_radius, gap
    )
    central_builder = lambda nl, seed, npl=args.npl, y_range=args.y_range, connect_radius=args.connect_radius, y_cut=args.y_cut: _build_central_graph(
        nl, seed, npl, y_range, connect_radius, y_cut
    )

    _evaluate_family(
        f"modular gap={args.gap:.1f}",
        modular_builder,
        args.n_layers,
        seeds,
        True,
    )
    _evaluate_family(
        f"central-band |y|<{args.y_cut:.1f}",
        central_builder,
        args.n_layers,
        seeds,
        True,
    )


if __name__ == "__main__":
    main()
