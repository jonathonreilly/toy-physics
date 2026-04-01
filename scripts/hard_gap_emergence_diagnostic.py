#!/usr/bin/env python3
"""Hard-gap emergence diagnostic.

This is a bounded placement-only diagnostic for the remaining emergence
question: can a local node-placement rule create and maintain a real node
absence region of the useful size and location?

Scope:
- placement rules only
- no connection-feedback sweeps
- no soft pruning variants
- score gap size, gap center, connectivity survival, pur_cl, pur_min,
  and gravity delta

The script is intentionally small and opinionated. If no placement rule
hits the hard-gap target, it reports the needed observable/control law for
the next session instead of broadening the search.
"""

from __future__ import annotations

import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.node_placement_emergence import (
    BETA,
    LAM,
    compute_field,
    generate_placement_dag,
    propagate_full,
    cl_purity_triple,
)


K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 8
N_LAYERS = 40
NODES_PER_LAYER = 25
Y_RANGE = 12.0
CONNECT_RADIUS = 3.0
TARGET_GAP = 2.0
TARGET_GAP_CENTER = 0.0


def _gap_profile(positions, n_layers):
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    barrier_layer = layers[len(layers) // 3]

    post_ys = [positions[i][1] for layer in layers if layer > barrier_layer for i in by_layer[layer]]
    if len(post_ys) < 2:
        return 0.0, float("nan")

    post_ys.sort()
    best_gap = 0.0
    best_center = float("nan")
    for i in range(1, len(post_ys)):
        gap = post_ys[i] - post_ys[i - 1]
        if gap > best_gap:
            best_gap = gap
            best_center = 0.5 * (post_ys[i] + post_ys[i - 1])
    return best_gap, best_center


def _run_seed(positions, adj, n_layers):
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

    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)
    barrier_layer = layers[len(layers) // 3]
    bi = by_layer[barrier_layer]

    upper = [i for i in bi if positions[i][1] > cy + 3][:3]
    lower = [i for i in bi if positions[i][1] < cy - 3][:3]
    blocked = set(bi) - set(upper + lower)
    if not upper or not lower:
        return None

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    env_depth = max(1, round(n_layers / 6))
    start = len(layers) // 3 + 1
    stop = min(len(layers), start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])

    field_mass = compute_field(positions, mass_nodes, strength=0.1)
    field_flat = [0.0] * len(positions)

    grav_deltas = []
    pmins = []
    pcls = []
    decohs = []

    for k in K_BAND:
        amps_mass = propagate_full(positions, adj, field_mass, src, k, blocked)
        amps_flat = propagate_full(positions, adj, field_flat, src, k, blocked)

        pm = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        pf = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / pf
            grav_deltas.append(ym - yf)

        amps_a = propagate_full(positions, adj, field_mass, src, k, blocked | set(lower))
        amps_b = propagate_full(positions, adj, field_mass, src, k, blocked | set(upper))
        bins_a = [0j] * 8
        bins_b = [0j] * 8
        bw = 24.0 / 8
        for m in mid:
            ba = int((positions[m][1] + 12.0) / bw)
            ba = max(0, min(7, ba))
            bins_a[ba] += amps_a[m]
            bins_b[ba] += amps_b[m]

        S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
        NA = sum(abs(a) ** 2 for a in bins_a)
        NB = sum(abs(b) ** 2 for b in bins_b)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-(LAM ** 2) * Sn)
        pur_cl, pur_coh, pur_min = cl_purity_triple(amps_a, amps_b, D, det_list)
        if not math.isnan(pur_cl):
            pcls.append(pur_cl)
            pmins.append(pur_min)
            decohs.append(pur_coh - pur_cl)

    if not grav_deltas or not pcls:
        return None

    return {
        "grav": sum(grav_deltas) / len(grav_deltas),
        "pur_cl": sum(pcls) / len(pcls),
        "pur_min": sum(pmins) / len(pmins),
        "decoh": sum(decohs) / len(decohs),
        "gap": _gap_profile(positions, n_layers),
    }


def main():
    print("=" * 86)
    print("HARD-GAP EMERGENCE DIAGNOSTIC")
    print("  Placement-only sweep. No soft connection rules. No pruning sweeps.")
    print(f"  N={N_LAYERS}, seeds={N_SEEDS}, k-band={K_BAND}, beta={BETA}, lambda={LAM}")
    print("=" * 86)
    print()

    alphas = [0.0, 1.0, 2.0, 4.0, 8.0]
    print(f"{'alpha':>5s}  {'n_ok':>4s}  {'gap':>7s}  {'gap_ctr':>8s}  "
          f"{'pur_cl':>8s}  {'pur_min':>8s}  {'decoh':>8s}  {'grav':>8s}  verdict")
    print("-" * 92)

    verdicts = []
    for alpha in alphas:
        records = []
        for seed in range(N_SEEDS):
            positions, adj, _ = generate_placement_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=NODES_PER_LAYER,
                y_range=Y_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed * 7 + 3,
                alpha=alpha,
            )
            r = _run_seed(positions, adj, N_LAYERS)
            if r is not None:
                gap, gap_ctr = r["gap"]
                records.append((gap, gap_ctr, r["pur_cl"], r["pur_min"], r["decoh"], r["grav"]))

        if records:
            n_ok = len(records)
            gap = sum(x[0] for x in records) / n_ok
            gap_ctr = sum(abs(x[1]) for x in records if math.isfinite(x[1])) / max(
                1, sum(1 for x in records if math.isfinite(x[1]))
            )
            pur_cl = sum(x[2] for x in records) / n_ok
            pur_min = sum(x[3] for x in records) / n_ok
            decoh = sum(x[4] for x in records) / n_ok
            grav = sum(x[5] for x in records) / n_ok

            hard_gap_ok = gap >= 2.0 and gap <= 4.0 and gap_ctr <= 1.5 and pur_cl < 0.95 and grav > 0
            verdict = "retained" if hard_gap_ok else "provisional"
            verdicts.append(hard_gap_ok)
            print(f"{alpha:5.1f}  {n_ok:4d}  {gap:7.2f}  {gap_ctr:8.2f}  "
                  f"{pur_cl:8.4f}  {pur_min:8.4f}  {decoh:+8.4f}  {grav:+8.3f}  {verdict}")
        else:
            verdicts.append(False)
            print(f"{alpha:5.1f}  {'FAIL':>4s}")

    if any(verdicts):
        print()
        print("VERDICT: retained")
        print("A placement rule produced a hard-gap candidate in the target band.")
    else:
        print()
        print("VERDICT: not-ready")
        print("No local placement rule produced a stable hard gap in the target band.")
        print("Needed next: a control law that directly regulates gap width and center,")
        print("not just distinguishability-biased placement.")


if __name__ == "__main__":
    main()
