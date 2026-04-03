#!/usr/bin/env python3
"""Corrected Born calibration for stochastic collapse on a 3D chokepoint harness.

This is the review-safe replacement for older branch-local Born checks on
collapse / LN / |y|-removal combinations. It uses:

- a strict 3D chokepoint barrier (no bypass around the slit layer)
- exact propagation (no amplitude threshold)
- corrected Sorkin metric with the required -P(empty) term

The main goal is to answer one question:
does stochastic collapse remain Born-clean enough to be a serious scalable lane,
especially when combined with layer normalization and central-band removal?
"""

from __future__ import annotations

import argparse
import cmath
from collections import defaultdict, deque
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8


def generate_3d_dag_chokepoint(
    n_layers: int,
    nodes_per_layer: int,
    yz_range: float,
    connect_radius: float,
    rng_seed: int,
):
    """3D DAG with barrier as a true chokepoint.

    Only previous-layer edges are allowed, so every path that reaches the
    detector must pass through the barrier layer.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(0)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                if layer_indices:
                    prev = layer_indices[-1]
                    for prev_idx in prev:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)
    return positions, dict(adj), layer_indices, barrier_layer


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
            if j >= 0 and in_deg[j] == 0:
                q.append(j)
    return order


def apply_y_removal(positions, adj, barrier_layer, y_cut, protected):
    if y_cut <= 0:
        return adj, set()
    removed = set()
    for idx, (x, y, z) in enumerate(positions):
        if x <= barrier_layer or idx in protected:
            continue
        if abs(y) < y_cut:
            removed.add(idx)
    new_adj = {}
    for i, nbs in adj.items():
        if i in removed:
            continue
        kept = [j for j in nbs if j not in removed]
        if kept:
            new_adj[i] = kept
    return new_adj, removed


def choose_mass_set(positions, layer_indices, n_layers):
    """Choose post-barrier mass/collapse sites on the same retained style as other lanes."""
    cy = sum(y for _, y, _ in positions) / len(positions)
    start = n_layers // 3 + 1
    stop = min(len(layer_indices) - 1, start + max(1, round(n_layers / 6)))
    mass_set = set()
    for li in range(start, stop):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= 3.0:
                mass_set.add(i)
    return mass_set


def propagate_variant(
    positions,
    adj,
    src,
    k,
    blocked,
    *,
    use_ln: bool,
    p_collapse: float,
    mass_set,
    rng,
):
    """Exact 3D propagation with optional layer norm and stochastic collapse."""
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
            if i in blocked:
                continue
            a_i = amps[i]
            if a_i == 0j:
                continue

            if p_collapse > 0 and i in mass_set and rng.random() < p_collapse:
                theta_rand = rng.uniform(0.0, 2.0 * math.pi)
                a_i *= cmath.exp(1j * theta_rand)
                amps[i] = a_i

            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1, z1 = positions[i]
                x2, y2, z2 = positions[j]
                dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
                L = math.sqrt(dx * dx + dy * dy + dz * dz)
                if L < 1e-10:
                    continue
                cos_theta = dx / L
                theta = math.acos(min(max(cos_theta, -1.0), 1.0))
                w = math.exp(-BETA * theta * theta)
                amps[j] += a_i * cmath.exp(1j * k * L) * w / L

        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def born_metric_for_graph(graph, *, use_ln: bool, p_collapse: float, n_realizations: int, k_band):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    barrier_nodes = graph["barrier_nodes"]
    slit_a = set(graph["slit_a"])
    slit_b = set(graph["slit_b"])
    slit_c = set(graph["slit_c"])
    base_blocked = graph["base_blocked"]
    mass_set = graph["mass_set"]

    all_slits = slit_a | slit_b | slit_c

    vals = []
    for k in k_band:
        for r in range(n_realizations):
            seed_base = 100000 * r + int(round(100 * k))

            def total_prob(open_set):
                blocked = base_blocked | (all_slits - set(open_set))
                rng = random.Random(seed_base)
                amps = propagate_variant(
                    positions,
                    adj,
                    src,
                    k,
                    blocked,
                    use_ln=use_ln,
                    p_collapse=p_collapse,
                    mass_set=mass_set,
                    rng=rng,
                )
                return sum(abs(amps[d]) ** 2 for d in det_list)

            P_abc = total_prob(slit_a | slit_b | slit_c)
            if P_abc <= 1e-30:
                continue
            P_ab = total_prob(slit_a | slit_b)
            P_ac = total_prob(slit_a | slit_c)
            P_bc = total_prob(slit_b | slit_c)
            P_a = total_prob(slit_a)
            P_b = total_prob(slit_b)
            P_c = total_prob(slit_c)
            P_empty = total_prob(set())
            I3 = P_abc - P_ab - P_ac - P_bc + P_a + P_b + P_c - P_empty
            vals.append(abs(I3) / P_abc)

    return vals


def build_graph(nl, seed, npl, yz_range, connect_radius, y_cut):
    positions, adj, layer_indices, barrier_layer = generate_3d_dag_chokepoint(
        nl, npl, yz_range, connect_radius, seed
    )
    if len(layer_indices) < 7:
        return None

    src = layer_indices[0]
    det_list = layer_indices[-1]
    if not det_list:
        return None

    barrier_nodes = layer_indices[barrier_layer]
    cy = sum(y for _, y, _ in positions) / len(positions)
    upper = sorted([i for i in barrier_nodes if positions[i][1] > cy + 2], key=lambda i: positions[i][1])
    lower = sorted([i for i in barrier_nodes if positions[i][1] < cy - 2], key=lambda i: -positions[i][1])
    middle = sorted([i for i in barrier_nodes if abs(positions[i][1] - cy) <= 2], key=lambda i: abs(positions[i][1] - cy))
    if not upper or not lower or not middle:
        return None

    slit_a = [upper[0]]
    slit_b = [lower[0]]
    slit_c = [middle[0]]
    protected = set(src) | set(det_list) | set(slit_a + slit_b + slit_c)

    adj2, removed = apply_y_removal(positions, adj, barrier_layer, y_cut, protected)

    return {
        "positions": positions,
        "adj": adj2,
        "src": src,
        "det_list": det_list,
        "barrier_nodes": barrier_nodes,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "slit_c": slit_c,
        "base_blocked": set(barrier_nodes) - set(slit_a + slit_b + slit_c),
        "mass_set": choose_mass_set(positions, layer_indices, nl),
        "removed_frac": len(removed) / max(1, sum(1 for i, (x, _, _) in enumerate(positions) if x > barrier_layer and i not in protected)),
    }


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
    parser.add_argument("--n-layers", nargs="+", type=int, default=[15, 25, 40])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--n-realizations", type=int, default=30)
    parser.add_argument("--npl", type=int, default=30)
    parser.add_argument("--yz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    parser.add_argument("--y-cut", type=float, default=2.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    k_band = [3.0, 5.0, 7.0]

    print("=" * 126)
    print("STOCHASTIC COLLAPSE: CORRECTED BORN CALIBRATION")
    print("  exact 3D chokepoint harness, corrected I3 with -P(empty)")
    print(
        f"  seeds={args.n_seeds}, realizations={args.n_realizations}, npl={args.npl}, "
        f"yz_range={args.yz_range}, r={args.connect_radius}, p={args.p_collapse}, y_cut={args.y_cut}"
    )
    print("=" * 126)
    print()

    configs = [
        ("linear", False, 0.0, 0.0),
        ("LN", True, 0.0, 0.0),
        ("collapse", False, args.p_collapse, 0.0),
        ("LN+collapse", True, args.p_collapse, 0.0),
        ("LN+|y|", True, 0.0, args.y_cut),
        ("LN+|y|+collapse", True, args.p_collapse, args.y_cut),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(f"  {'mode':>16s}  {'|I3|/P':>14s}  {'SE':>10s}  {'max':>10s}  {'rem%':>6s}  {'ok':>3s}  verdict")
        print("  " + "-" * 88)

        for label, use_ln, p_col, y_cut in configs:
            vals = []
            rems = []
            n_ok = 0
            for seed in seeds:
                graph = build_graph(nl, seed, args.npl, args.yz_range, args.connect_radius, y_cut)
                if graph is None:
                    continue
                rows = born_metric_for_graph(
                    graph,
                    use_ln=use_ln,
                    p_collapse=p_col,
                    n_realizations=args.n_realizations,
                    k_band=k_band,
                )
                if rows:
                    vals.extend(rows)
                    rems.append(100.0 * graph["removed_frac"])
                    n_ok += 1

            mean, se = mean_se(vals)
            mx = max(vals) if vals else math.nan
            rem_s = "  —  " if not rems else f"{sum(rems)/len(rems):5.1f}%"
            if math.isnan(mean):
                verdict = "FAIL"
                mean_s = se_s = max_s = "FAIL"
            else:
                mean_s = f"{mean:.2e}"
                se_s = f"{se:.1e}"
                max_s = f"{mx:.2e}"
                verdict = "PASS" if mx < 1e-2 else ("MARGINAL" if mx < 1e-1 else "FAIL")

            print(f"  {label:>16s}  {mean_s:>14s}  {se_s:>10s}  {max_s:>10s}  {rem_s:>6s}  {n_ok:3d}  {verdict}")
            sys.stdout.flush()
        print()

    print("Thresholds:")
    print("  max |I3|/P < 1e-10 : machine precision")
    print("  max |I3|/P < 1e-2  : practically Born-clean")
    print("  max |I3|/P < 1e-1  : marginal")
    print("  max |I3|/P >= 1e-1 : clear Born violation")


if __name__ == "__main__":
    main()
