#!/usr/bin/env python3
"""Same-graph joint card for the dense central-band Born-safe pocket.

This script keeps one graph family fixed and reports:

- corrected three-slit Born metric
- unitary decoherence floor (`pur_min`)
- gravity centroid delta

The intent is to compare the best dense central-band pocket on the same
graphs, especially the retained rows for `LN + |y|` versus
`LN + |y| + collapse`.
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

from scripts.central_band_layernorm_combo import purity_min
from scripts.gap_topological_asymmetry_layernorm_combo import (
    compute_field_3d,
    propagate_3d_layernorm,
    propagate_3d_linear,
)
from scripts.stochastic_collapse_born_calibration import (
    born_metric_for_graph,
    build_graph,
    mean_se,
)

BETA = 0.8
K_BAND = [3.0, 5.0, 7.0]


def fmt(vals, signed=False):
    m, se = mean_se(vals)
    if math.isnan(m):
        return "FAIL"
    if signed:
        return f"{m:+.3f}±{se:.3f}"
    return f"{m:.3f}±{se:.3f}"


def attach_field(graph):
    positions = graph["positions"]
    field = compute_field_3d(positions, list(graph["mass_set"]))
    graph["field"] = field
    graph["field_flat"] = [0.0] * len(positions)
    return graph


def make_collapse_phase_map(mass_set, p_collapse, seed_base):
    if p_collapse <= 0 or not mass_set:
        return {}
    phases = {}
    for i in sorted(mass_set):
        rr = random.Random(seed_base + 1000003 * (i + 1))
        if rr.random() < p_collapse:
            phases[i] = cmath.exp(1j * rr.uniform(0.0, 2.0 * math.pi))
    return phases


def propagate_field_3d(positions, adj, field, src, k, blocked=None, *, use_ln=False, collapse_phase=None):
    n = len(positions)
    blocked = blocked or set()
    collapse_phase = collapse_phase or {}

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

            if i in collapse_phase:
                a_i *= collapse_phase[i]
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
                lf = 0.5 * (field[i] + field[j])
                dl = L * (1 + lf)
                ret = math.sqrt(max(dl * dl - L * L, 0))
                act = dl - ret
                theta = math.acos(min(max(dx / L, -1.0), 1.0))
                w = math.exp(-BETA * theta * theta)
                amps[j] += a_i * cmath.exp(1j * k * act) * w / L

        if use_ln and li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def unitary_pur_min(graph, use_ln):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["base_blocked"]
    sa = set(graph["slit_a"])
    sb = set(graph["slit_b"])
    sc = set(graph["slit_c"])
    field = graph["field"]

    prop = propagate_3d_layernorm if use_ln else propagate_3d_linear
    vals = []
    for k in K_BAND:
        aa = prop(positions, adj, field, src, k, blocked | sb | sc)
        ab = prop(positions, adj, field, src, k, blocked | sa | sc)
        pm = purity_min(aa, ab, det_list)
        if not math.isnan(pm):
            vals.append(pm)
    return math.nan if not vals else sum(vals) / len(vals)


def collapse_purity(graph, use_ln, p_collapse, n_realizations):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["base_blocked"]
    sa = set(graph["slit_a"])
    sb = set(graph["slit_b"])
    sc = set(graph["slit_c"])
    mass_set = graph["mass_set"]
    field = graph["field"]

    rho = {(d1, d2): 0j for d1 in det_list for d2 in det_list}
    n_total = 0
    for k in K_BAND:
        for r in range(n_realizations):
            collapse_phase = make_collapse_phase_map(mass_set, p_collapse, 100000 * r + int(round(100 * k)))
            amps_a = propagate_field_3d(
                positions,
                adj,
                field,
                src,
                k,
                blocked | sb | sc,
                use_ln=use_ln,
                collapse_phase=collapse_phase,
            )
            amps_b = propagate_field_3d(
                positions,
                adj,
                field,
                src,
                k,
                blocked | sa | sc,
                use_ln=use_ln,
                collapse_phase=collapse_phase,
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


def collapse_gravity(graph, use_ln, p_collapse, n_realizations):
    positions = graph["positions"]
    adj = graph["adj"]
    src = graph["src"]
    det_list = graph["det_list"]
    blocked = graph["base_blocked"]
    mass_set = graph["mass_set"]
    field = graph["field"]
    field_flat = graph["field_flat"]

    vals = []
    for k in K_BAND:
        for r in range(n_realizations):
            collapse_phase = make_collapse_phase_map(mass_set, p_collapse, 100000 * r + int(round(100 * k)))
            am = propagate_field_3d(
                positions,
                adj,
                field,
                src,
                k,
                blocked,
                use_ln=use_ln,
                collapse_phase=collapse_phase,
            )
            af = propagate_field_3d(
                positions,
                adj,
                field_flat,
                src,
                k,
                blocked,
                use_ln=use_ln,
                collapse_phase=collapse_phase,
            )
            pm = sum(abs(am[d]) ** 2 for d in det_list)
            pf = sum(abs(af[d]) ** 2 for d in det_list)
            if pm <= 1e-30 or pf <= 1e-30:
                continue
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            vals.append(ym - yf)
    return math.nan if not vals else sum(vals) / len(vals)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[40, 60])
    parser.add_argument("--n-seeds", type=int, default=4)
    parser.add_argument("--n-realizations", type=int, default=8)
    parser.add_argument("--npl", type=int, default=60)
    parser.add_argument("--yz-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    parser.add_argument("--y-cut", type=float, default=2.0)
    parser.add_argument("--p-collapse", type=float, default=0.2)
    args = parser.parse_args()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print("=" * 136)
    print("CENTRAL-BAND DENSE SAME-GRAPH JOINT CARD")
    print("  corrected Born + pur_min + gravity on the same dense central-band graphs")
    print(
        f"  seeds={args.n_seeds}, realizations={args.n_realizations}, npl={args.npl}, "
        f"yz_range={args.yz_range}, r={args.connect_radius}, y_cut={args.y_cut}, p={args.p_collapse}"
    )
    print("=" * 136)
    print()

    rows = [
        ("linear", False, 0.0),
        ("LN+|y|", True, 0.0),
        ("LN+|y|+collapse", True, args.p_collapse),
    ]

    for nl in args.n_layers:
        print(f"N = {nl}")
        print(
            f"  {'mode':>16s}  {'Born |I3|/P':>14s}  {'pur_min/purity':>16s}  "
            f"{'gravity':>14s}  {'g/SE':>6s}  {'ok':>3s}"
        )
        print("  " + "-" * 104)

        for label, use_ln, p_col in rows:
            born_vals = []
            decoh_vals = []
            grav_vals = []
            ok = 0
            for seed in seeds:
                graph = build_graph(nl, seed, args.npl, args.yz_range, args.connect_radius, args.y_cut)
                if graph is None:
                    continue
                graph = attach_field(graph)

                born_rows = born_metric_for_graph(
                    graph,
                    use_ln=use_ln,
                    p_collapse=p_col,
                    n_realizations=args.n_realizations,
                    k_band=K_BAND,
                )
                if born_rows:
                    born_vals.extend(born_rows)

                if p_col > 0:
                    decoh = collapse_purity(graph, use_ln, p_col, args.n_realizations)
                    grav = collapse_gravity(graph, use_ln, p_col, args.n_realizations)
                else:
                    decoh = unitary_pur_min(graph, use_ln)
                    grav = collapse_gravity(graph, use_ln, 0.0, args.n_realizations)

                if not math.isnan(decoh) and not math.isnan(grav):
                    decoh_vals.append(decoh)
                    grav_vals.append(grav)
                    ok += 1

            gmean, gse = mean_se(grav_vals)
            gsig = gmean / gse if not math.isnan(gmean) and gse > 1e-12 else math.nan
            metric = fmt(decoh_vals)
            born = fmt(born_vals)
            print(
                f"  {label:>16s}  {born:>14s}  {metric:>16s}  {fmt(grav_vals, signed=True):>14s}  "
                f"{('FAIL' if math.isnan(gsig) else f'{gsig:+.1f}'):>6s}  {ok:3d}"
            )
        print()

    print("Thresholds:")
    print("  max |I3|/P < 1e-10 : machine precision")
    print("  max |I3|/P < 1e-2  : practically Born-clean")
    print("  max |I3|/P < 1e-1  : marginal")
    print("  max |I3|/P >= 1e-1 : clear Born violation")


if __name__ == "__main__":
    main()
