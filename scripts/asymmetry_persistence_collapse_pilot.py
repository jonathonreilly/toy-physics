#!/usr/bin/env python3
"""Generated asymmetry-persistence geometry combined with stochastic collapse.

This bounded pilot compares four cases on the same generated 3D graphs:

1. baseline generated geometry
2. asymmetry persistence only
3. stochastic collapse only
4. asymmetry persistence + stochastic collapse

When feasible, each case is measured with and without layer normalization.
The unitary rows report ``pur_min``. The collapse rows report averaged
detector density-matrix purity from Monte Carlo realizations.
"""

from __future__ import annotations

import argparse
import cmath
from collections import defaultdict
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.asymmetry_persistence_pilot import generate_3d_asymmetry_persistence_dag
from scripts.gap_topological_asymmetry_layernorm_combo import (
    K_BAND,
    compute_field_3d,
    propagate_3d_layernorm,
    propagate_3d_linear,
    purity_min,
)

BETA = 0.8


def mean_se(vals):
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return mean, math.sqrt(var / len(vals))


def fmt(vals, signed=False):
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    if signed:
        return f"{m:+.3f}±{se:.3f}"
    return f"{m:.3f}±{se:.3f}"


def choose_npl(nl: int, arg_npl: int | None) -> int:
    if arg_npl is not None:
        return arg_npl
    if nl >= 100:
        return 60
    if nl >= 80:
        return 50
    return 30


def build_graph(nl, seed, thresh, npl, xyz_range, connect_radius):
    positions, adj, barrier_layer = generate_3d_asymmetry_persistence_dag(
        nl,
        npl,
        xyz_range,
        connect_radius,
        seed,
        thresh,
        max(1, round(nl / 6)),
    )
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y, _ in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]

    slit_upper = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_lower = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not slit_upper or not slit_lower:
        return None
    blocked_two = set(bi) - set(slit_upper + slit_lower)

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mid_mass = []
    for layer in layers[start:stop]:
        mid_mass.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)

    field = compute_field_3d(positions, list(set(mid_mass) | set(mass_nodes)))

    return {
        "positions": positions,
        "adj": adj,
        "src": src,
        "det_list": det_list,
        "blocked_two": blocked_two,
        "slit_upper": slit_upper,
        "slit_lower": slit_lower,
        "field": field,
        "mass_set": set(mid_mass) | set(mass_nodes),
        "keep_frac": len(positions) / (1 + (nl - 1) * npl),
        "barrier_layer": barrier_layer,
    }


def propagate_with_collapse(positions, adj, field, src, k, blocked, mass_set, p_collapse, rng, use_ln=False):
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


def unitary_pur_min(graph, use_ln):
    prop = propagate_3d_layernorm if use_ln else propagate_3d_linear
    vals = []
    for k in K_BAND:
        aa = prop(graph["positions"], graph["adj"], graph["field"], graph["src"], k, graph["blocked_two"] | set(graph["slit_lower"]))
        ab = prop(graph["positions"], graph["adj"], graph["field"], graph["src"], k, graph["blocked_two"] | set(graph["slit_upper"]))
        pm = purity_min(aa, ab, graph["det_list"])
        if not math.isnan(pm):
            vals.append(pm)
    return math.nan if not vals else sum(vals) / len(vals)


def collapse_detector_purity(graph, use_ln, p_collapse, n_realizations):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["blocked_two"]
    mass_set = graph["mass_set"]
    slit_upper = set(graph["slit_upper"])
    slit_lower = set(graph["slit_lower"])

    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = 0j

    n_total = 0
    for k in K_BAND:
        for r in range(n_realizations):
            rng = random.Random(r * 1000 + int(k * 100))
            amps_a = propagate_with_collapse(
                positions, adj, graph["field"], src, k, blocked | slit_lower,
                mass_set, p_collapse, rng, use_ln
            )
            amps_b = propagate_with_collapse(
                positions, adj, graph["field"], src, k, blocked | slit_upper,
                mass_set, p_collapse, rng, use_ln
            )
            psi = [amps_a[d] + amps_b[d] for d in det_list]
            norm_sq = sum(abs(p) ** 2 for p in psi)
            if norm_sq < 1e-30:
                continue
            for i, d1 in enumerate(det_list):
                for j, d2 in enumerate(det_list):
                    rho[(d1, d2)] += psi[i].conjugate() * psi[j] / norm_sq
            n_total += 1

    if n_total == 0:
        return math.nan

    for key in rho:
        rho[key] /= n_total
    return sum(abs(v) ** 2 for v in rho.values()).real


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[80, 100])
    parser.add_argument("--thresholds", nargs="+", type=float, default=[0.0, 0.1, 0.2])
    parser.add_argument("--n-seeds", type=int, default=8)
    parser.add_argument("--npl", type=int, default=None)
    parser.add_argument("--xyz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=4.0)
    parser.add_argument("--collapse-p", type=float, default=0.2)
    parser.add_argument("--n-realizations", type=int, default=12)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]
    print("=" * 164)
    print("ASYMMETRY PERSISTENCE + STOCHASTIC COLLAPSE PILOT")
    print("  Compare baseline generated geometry, persistence only, collapse only, and persistence+collapse")
    print("  Unitary rows report pur_min; collapse rows report averaged detector purity")
    print(
        f"  N={args.n_layers}, thresholds={args.thresholds}, seeds={args.n_seeds}, "
        f"collapse_p={args.collapse_p}, realizations={args.n_realizations}"
    )
    print("=" * 164)
    print()

    for nl in args.n_layers:
        npl = choose_npl(nl, args.npl)
        print(f"N = {nl}  (npl = {npl})")
        print(
            f"  {'thr':>4s}  {'keep%':>6s}  {'base_pmin':>10s}  {'pers_pmin':>10s}  "
            f"{'base_col':>10s}  {'pers_col':>10s}  {'base_LN':>10s}  {'pers_LN':>10s}  "
            f"{'col_LN':>10s}  {'persCol_LN':>12s}  {'ok':>3s}"
        )
        print("  " + "-" * 132)

        for thresh in args.thresholds:
            keeps = []
            base_pmin = []
            pers_pmin = []
            base_col = []
            pers_col = []
            base_ln = []
            pers_ln = []
            col_ln = []
            pers_col_ln = []
            ok = 0

            for seed in seeds:
                base_graph = build_graph(nl, seed, 0.0, npl, args.xyz_range, args.connect_radius)
                pers_graph = build_graph(nl, seed, thresh, npl, args.xyz_range, args.connect_radius)
                if base_graph is None or pers_graph is None:
                    continue

                keeps.append(100.0 * pers_graph["keep_frac"])

                base_pmin.append(unitary_pur_min(base_graph, False))
                pers_pmin.append(unitary_pur_min(pers_graph, False))
                base_ln.append(unitary_pur_min(base_graph, True))
                pers_ln.append(unitary_pur_min(pers_graph, True))

                base_col.append(collapse_detector_purity(base_graph, False, args.collapse_p, args.n_realizations))
                pers_col.append(collapse_detector_purity(pers_graph, False, args.collapse_p, args.n_realizations))
                col_ln.append(collapse_detector_purity(base_graph, True, args.collapse_p, args.n_realizations))
                pers_col_ln.append(collapse_detector_purity(pers_graph, True, args.collapse_p, args.n_realizations))
                ok += 1

            keep_s = "FAIL" if not keeps else f"{sum(keeps)/len(keeps):5.1f}%"
            print(
                f"  {thresh:4.2f}  {keep_s:>6s}  {fmt(base_pmin):>10s}  {fmt(pers_pmin):>10s}  "
                f"{fmt(base_col):>10s}  {fmt(pers_col):>10s}  {fmt(base_ln):>10s}  {fmt(pers_ln):>10s}  "
                f"{fmt(col_ln):>10s}  {fmt(pers_col_ln):>12s}  {ok:3d}"
            )
            sys.stdout.flush()
        print()


if __name__ == "__main__":
    main()
