#!/usr/bin/env python3
"""Reconcile Born claims on the structured-mirror growth family.

This script compares the retained structured-growth geometry under several
Born harness choices:
  - canonical joint-validator style: threshold slits + physical mass field
  - threshold slits + flat field
  - audit-style top-K barrier selection + flat field
  - audit-style top-K barrier selection + physical mass field

The point is to separate geometry effects from slit-selection and field-setup
effects. The structured geometry itself is retained; the question is whether
any retained harness is genuinely Born-clean.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import defaultdict, deque
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.structured_mirror_growth import compute_field, grow_structured_mirror

# This runner is intentionally heavier than the 120 s default when the machine
# is loaded; audit precompute needs enough time to finish the full N-grid.
AUDIT_TIMEOUT_SEC = 300

BETA = 0.8


def topo_order(adj, n):
    indeg = [0] * n
    for vs in adj.values():
        for j in vs:
            indeg[j] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            indeg[j] -= 1
            if indeg[j] == 0:
                q.append(j)
    return order


def propagate_linear(positions, adj, field, src, k, blocked):
    n = len(positions)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in topo_order(adj, n):
        if i in blocked or abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            dsq = sum((a - b) ** 2 for a, b in zip(positions[i], positions[j]))
            L = math.sqrt(dsq)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            dx = positions[j][0] - positions[i][0]
            trans = math.sqrt(max(dsq - dx * dx, 0))
            theta = math.atan2(trans, max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = complex(math.cos(k * act), math.sin(k * act)) * w / L
            amps[j] += amps[i] * ea
    return amps


def mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def sorkin_ratio(positions, adj, src, det_list, barrier_nodes, slits, field, k):
    all_slits = set(slits)
    other = set(barrier_nodes) - all_slits
    probs = {}
    for key, open_set in [
        ("abc", all_slits),
        ("ab", {slits[0], slits[1]}),
        ("ac", {slits[0], slits[2]}),
        ("bc", {slits[1], slits[2]}),
        ("a", {slits[0]}),
        ("b", {slits[1]}),
        ("c", {slits[2]}),
    ]:
        blocked = other | (all_slits - open_set)
        amps = propagate_linear(positions, adj, field, src, k, blocked)
        probs[key] = [abs(amps[d]) ** 2 for d in det_list]
    i3 = 0.0
    pabc = 0.0
    for di in range(len(det_list)):
        term = (
            probs["abc"][di]
            - probs["ab"][di]
            - probs["ac"][di]
            - probs["bc"][di]
            + probs["a"][di]
            + probs["b"][di]
            + probs["c"][di]
        )
        i3 += abs(term)
        pabc += probs["abc"][di]
    return i3 / pabc if pabc > 1e-30 else math.nan


def pick_threshold_slits(positions, barrier_nodes):
    cy = sum(p[1] for p in positions) / len(positions)
    upper = sorted([i for i in barrier_nodes if positions[i][1] > cy + 2], key=lambda i: positions[i][1])
    lower = sorted([i for i in barrier_nodes if positions[i][1] < cy - 2], key=lambda i: -positions[i][1])
    middle = sorted([i for i in barrier_nodes if abs(positions[i][1] - cy) <= 2], key=lambda i: abs(positions[i][1] - cy))
    if not upper or not lower or not middle:
        return None
    return [upper[0], lower[0], middle[0]]


def rank_barrier_nodes(positions, adj, src, barrier_nodes, field, k):
    amps = propagate_linear(positions, adj, field, src, k, blocked=set())
    ranked = sorted(
        [(i, abs(amps[i]) ** 2, positions[i][1]) for i in barrier_nodes],
        key=lambda row: -row[1],
    )
    return [i for i, _, _ in ranked]


def build_graph(n_layers, npl_half, d_growth, connect_radius, layer_jitter, seed):
    return grow_structured_mirror(
        n_layers=n_layers,
        npl_half=npl_half,
        d_growth=d_growth,
        grid_spacing=1.5,
        connect_radius=connect_radius,
        layer_jitter=layer_jitter,
        rng_seed=seed,
    )


def canonical_born(positions, adj, n_layers, k):
    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return math.nan
    src = by_layer[layers[0]]
    barrier = by_layer[layers[len(layers) // 3]]
    if len(barrier) < 6:
        return math.nan
    slits = pick_threshold_slits(positions, barrier)
    if not slits:
        return math.nan
    flat = [0.0] * len(positions)
    amps_b = propagate_linear(positions, adj, flat, src, k, blocked=set())
    mid_start = len(layers) // 2
    mid_end = min(len(layers) - 1, mid_start + 4)
    cy = sum(p[1] for p in positions) / len(positions)
    mid_upper = [
        i
        for layer in layers[mid_start:mid_end]
        for i in by_layer[layer]
        if positions[i][1] > cy
    ]
    ranked = sorted([(i, abs(amps_b[i]) ** 2) for i in mid_upper], key=lambda x: -x[1])
    mass = [i for i, _ in ranked[: max(2, len(ranked) // 5)]]
    field = compute_field(positions, mass, 0.5)
    det = list(by_layer[layers[-1]])
    return sorkin_ratio(positions, adj, src, det, barrier, slits, field, k)


def audit_style_born(positions, adj, k, top_k=6, use_mass_field=False):
    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return math.nan
    src = by_layer[layers[0]]
    barrier = by_layer[layers[len(layers) // 3]]
    det = list(by_layer[layers[-1]])
    if len(barrier) < 6 or not det:
        return math.nan

    flat = [0.0] * len(positions)
    slits = rank_barrier_nodes(positions, adj, src, barrier, flat, k)[:top_k]
    if len(slits) < 3:
        return math.nan

    field = [0.0] * len(positions)
    if use_mass_field:
        cy = sum(p[1] for p in positions) / len(positions)
        mid_start = len(layers) // 2
        mid_end = min(len(layers) - 1, mid_start + 4)
        mid_upper = [
            i
            for layer in layers[mid_start:mid_end]
            for i in by_layer[layer]
            if positions[i][1] > cy
        ]
        amps_b = propagate_linear(positions, adj, flat, src, k, blocked=set())
        ranked = sorted([(i, abs(amps_b[i]) ** 2) for i in mid_upper], key=lambda x: -x[1])
        mass = [i for i, _ in ranked[: max(2, len(ranked) // 5)]]
        field = compute_field(positions, mass, 0.5)

    ratios = []
    for trip in combinations(slits, 3):
        ratios.append(sorkin_ratio(positions, adj, src, det, barrier, list(trip), field, k))
    ratios = [r for r in ratios if not math.isnan(r)]
    if not ratios:
        return math.nan, math.nan, math.nan
    ratios.sort()
    return ratios[0], ratios[len(ratios) // 2], ratios[-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[25, 30, 40])
    parser.add_argument("--npl-half", type=int, default=20)
    parser.add_argument("--d-growth", type=int, default=2)
    parser.add_argument("--connect-radius", type=float, default=4.5)
    parser.add_argument("--layer-jitter", type=float, default=0.3)
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--k", type=float, default=5.0)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    print("=" * 108)
    print("STRUCTURED MIRROR BORN RECONCILIATION")
    print("  structured-growth geometry under canonical joint validator vs alternate Born harnesses")
    print(f"  npl_half={args.npl_half}, d_growth={args.d_growth}, r={args.connect_radius:g}, seeds={args.n_seeds}, k={args.k:g}")
    print("=" * 108)
    print()
    print(f"{'N':>4s}  {'canonical(Born)':>18s}  {'flat-threshold(Born)':>21s}  {'audit-topk-flat':>23s}  {'audit-topk-mass':>23s}")
    print("-" * 108)

    for nl in args.n_layers:
        canon_vals = []
        flat_vals = []
        audit_flat_min = []
        audit_flat_med = []
        audit_flat_max = []
        audit_mass_min = []
        audit_mass_med = []
        audit_mass_max = []
        for seed in seeds:
            positions, adj = build_graph(
                nl, args.npl_half, args.d_growth, args.connect_radius, args.layer_jitter, seed
            )
            by_layer = defaultdict(list)
            for idx, pos in enumerate(positions):
                by_layer[round(pos[0])].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 7:
                continue
            src = by_layer[layers[0]]
            barrier = by_layer[layers[len(layers) // 3]]
            det = list(by_layer[layers[-1]])
            if not det or len(barrier) < 6:
                continue

            slits = pick_threshold_slits(positions, barrier)
            if slits:
                flat_field = [0.0] * len(positions)
                canon_vals.append(canonical_born(positions, adj, nl, args.k))
                flat_vals.append(sorkin_ratio(positions, adj, src, det, barrier, slits, flat_field, args.k))

            mn, md, mx = audit_style_born(positions, adj, args.k, top_k=6, use_mass_field=False)
            if not math.isnan(mn):
                audit_flat_min.append(mn)
                audit_flat_med.append(md)
                audit_flat_max.append(mx)

            mn, md, mx = audit_style_born(positions, adj, args.k, top_k=6, use_mass_field=True)
            if not math.isnan(mn):
                audit_mass_min.append(mn)
                audit_mass_med.append(md)
                audit_mass_max.append(mx)

        canon_m, canon_se = mean_se(canon_vals)
        flat_m, flat_se = mean_se(flat_vals)
        af_m, af_se = mean_se(audit_flat_med)
        am_m, am_se = mean_se(audit_mass_med)
        print(
            f"{nl:4d}  "
            f"{canon_m:8.3e}±{canon_se:.1e}  "
            f"{flat_m:8.3e}±{flat_se:.1e}  "
            f"{af_m:8.3e}±{af_se:.1e}  "
            f"{am_m:8.3e}±{am_se:.1e}"
        )

    print()
    print("Interpretation:")
    print("  - canonical = structured-growth geometry with the joint-validator slit/mass harness")
    print("  - flat-threshold = same slits, but no mass field")
    print("  - audit-topk-flat = slit-selection harness used by the Born audit style")
    print("  - audit-topk-mass = same top-k slit selection, but with the physical mass field")
    print("  - If canonical stays O(1e-1) while audit-topk can approach O(1), the discrepancy is harness-level, not a geometry bug.")


if __name__ == "__main__":
    main()
