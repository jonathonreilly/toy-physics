#!/usr/bin/env python3
"""Audit Born safety on the current structured mirror growth lane.

This is intentionally narrow. The structured-growth result is scientifically
interesting because it reproduces strong decoherence and gravity on a grown,
exact-Z2 geometry. But its current propagator uses per-layer normalization, so
the Born claim should be audited directly rather than inherited.

The audit:

  - generate the current structured mirror graphs
  - identify the barrier layer and its highest-weight candidate apertures
  - run a three-slit Sorkin test over all 3-combinations from the top-K
    barrier nodes
  - report min/median/max |I3|/P across seeds

If the lane were Born-safe, these values would be near machine precision.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import defaultdict
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.structured_mirror_growth import grow_structured_mirror, propagate_ln


def _quantile(sorted_vals: list[float], q: float) -> float:
    if not sorted_vals:
        return math.nan
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    pos = q * (len(sorted_vals) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_vals[lo]
    frac = pos - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def barrier_ranked_nodes(positions, adj, src, barrier_nodes, k):
    flat = [0.0] * len(positions)
    amps = propagate_ln(positions, adj, flat, src, k)
    ranked = sorted(
        [(i, abs(amps[i]) ** 2, positions[i][1]) for i in barrier_nodes],
        key=lambda row: -row[1],
    )
    return ranked


def sorkin_ratio(positions, adj, src, det_list, base_damping, slits, k):
    flat = [0.0] * len(positions)
    all_slits = set(slits)
    combos = {
        "abc": set(slits),
        "ab": {slits[0], slits[1]},
        "ac": {slits[0], slits[2]},
        "bc": {slits[1], slits[2]},
        "a": {slits[0]},
        "b": {slits[1]},
        "c": {slits[2]},
    }

    i3 = 0.0
    p_abc = 0.0
    for key, open_set in combos.items():
        damping = list(base_damping)
        for slit in all_slits - open_set:
            damping[slit] = 0.0
        amps = propagate_ln(positions, adj, flat, src, k, damping)
        for d in det_list:
            p = abs(amps[d]) ** 2
            if key == "abc":
                p_abc += p
                i3 += p
            elif key in ("ab", "ac", "bc"):
                i3 -= p
            else:
                i3 += p
    if p_abc <= 1e-30:
        return math.nan
    return abs(i3) / p_abc


def audit_seed(n_layers, npl_half, d_growth, connect_radius, grid_spacing, layer_jitter, top_k, seed, k):
    positions, adj = grow_structured_mirror(
        n_layers=n_layers,
        npl_half=npl_half,
        d_growth=d_growth,
        grid_spacing=grid_spacing,
        connect_radius=connect_radius,
        layer_jitter=layer_jitter,
        rng_seed=seed,
    )

    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None
    barrier_nodes = by_layer[layers[len(layers) // 3]]
    if len(barrier_nodes) < 6:
        return None

    ranked = barrier_ranked_nodes(positions, adj, src, barrier_nodes, k)
    top_nodes = [idx for idx, _, _ in ranked[:top_k]]
    if len(top_nodes) < 3:
        return None

    base_damping = [1.0] * len(positions)
    for node in barrier_nodes:
        base_damping[node] = 0.0
    for node in top_nodes:
        base_damping[node] = 1.0

    ratios = []
    for slits in combinations(top_nodes, 3):
        ratio = sorkin_ratio(positions, adj, src, det_list, base_damping, slits, k)
        if math.isfinite(ratio):
            ratios.append(ratio)

    if not ratios:
        return None
    ratios.sort()
    return {
        "top_y": [positions[i][1] for i in top_nodes],
        "min": ratios[0],
        "median": _quantile(ratios, 0.5),
        "max": ratios[-1],
        "count": len(ratios),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", type=int, default=25)
    parser.add_argument("--npl-half", type=int, default=15)
    parser.add_argument("--d-growth", type=int, default=2)
    parser.add_argument("--connect-radius", type=float, default=4.5)
    parser.add_argument("--grid-spacing", type=float, default=1.5)
    parser.add_argument("--layer-jitter", type=float, default=0.3)
    parser.add_argument("--k", type=float, default=5.0)
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--n-seeds", type=int, default=5)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 96)
    print("STRUCTURED MIRROR BORN AUDIT")
    print("  three-slit Sorkin check on the current structured-growth propagator")
    print(
        f"  N={args.n_layers}, npl_half={args.npl_half}, d_growth={args.d_growth}, "
        f"r={args.connect_radius}, top_k={args.top_k}, seeds={args.n_seeds}"
    )
    print("=" * 96)
    print()
    print(f"  {'seed':>4s}  {'min |I3|/P':>12s}  {'median':>12s}  {'max':>12s}  {'combos':>6s}  {'top barrier y':>24s}")
    print("  " + "-" * 84)

    mins = []
    meds = []
    maxs = []
    for seed in seeds:
        row = audit_seed(
            n_layers=args.n_layers,
            npl_half=args.npl_half,
            d_growth=args.d_growth,
            connect_radius=args.connect_radius,
            grid_spacing=args.grid_spacing,
            layer_jitter=args.layer_jitter,
            top_k=args.top_k,
            seed=seed,
            k=args.k,
        )
        if row is None:
            print(f"  {seed:4d}  FAIL")
            continue
        mins.append(row["min"])
        meds.append(row["median"])
        maxs.append(row["max"])
        top_y = ",".join(f"{y:+.2f}" for y in row["top_y"])
        print(
            f"  {seed:4d}  {row['min']:12.6f}  {row['median']:12.6f}  {row['max']:12.6f}  "
            f"{row['count']:6d}  {top_y:>24s}"
        )

    print()
    if mins:
        print(
            f"Aggregate: min={sum(mins)/len(mins):.6f}, "
            f"median={sum(meds)/len(meds):.6f}, max={sum(maxs)/len(maxs):.6f}"
        )
    else:
        print("Aggregate: FAIL")
    print("Interpretation: machine-precision Born safety would require |I3|/P << 1.")


if __name__ == "__main__":
    main()
