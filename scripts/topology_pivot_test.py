#!/usr/bin/env python3
"""Topology pivot test: does changing graph family remove the pur_min ceiling?

PRIMARY METRIC: pur_min (purity at D=0, maximally decohered) vs N.
  On uniform random DAGs, pur_min rises from ~0.95 to ~0.99 by N=25.
  We need pur_min to stay BOUNDED AWAY FROM 1 as N grows.

SECONDARY METRIC: CL bath decoh = pur_coh - pur_cl at lambda=10.
  Should INCREASE or stay stable with N (not reverse as on uniform DAGs).

Tests four graph families:
  1. Uniform random (baseline) — generate_causal_dag
  2. Hierarchical / channel-separated
  3. Modular two-channel with sparse crosslinks
  4. Preferential attachment (scale-free-like)

All use identical propagator, CL bath machinery, and parameters.
Only the graph generator changes.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.topology_families import (
    generate_hierarchical_dag,
    generate_modular_dag,
    generate_preferential_dag,
)

BETA = 0.8
N_YBINS = 8
LAM = 10.0  # Fixed large lambda for CL bath


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


def compute_field(positions, adj, mass_nodes):
    """Compute gravitational field (1/r potential from mass nodes)."""
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    """Propagate amplitudes with directional measure and field."""
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
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def build_setup(positions, adj, env_depth_layers=1, mass_y_half=3.0):
    """Build source/slit/mass/detector geometry — mirrors density_matrix_analysis."""
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det = set(by_layer[layers[-1]])
    det_list = list(det)
    if not det:
        return None

    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)

    bl_idx = len(layers) // 3
    bl = layers[bl_idx]
    bi = by_layer[bl]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    si = set(sa + sb)
    blocked = set(bi) - si

    start = bl_idx + 1
    stop = min(len(layers), start + max(1, env_depth_layers))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(
            i for i in by_layer[layer]
            if abs(positions[i][1] - cy) <= mass_y_half
        )
    if len(mass_nodes) < 2:
        return None

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    full_mass = set(mass_nodes) | set(grav_mass)
    field = compute_field(positions, adj, list(full_mass))

    return {
        "n": n, "by_layer": by_layer, "layers": layers,
        "src": src, "det": det, "det_list": det_list, "cy": cy,
        "blocked": blocked, "mass_set": set(mass_nodes),
        "field": field, "env_depth_layers": max(1, env_depth_layers),
    }


def bin_amplitudes(amps, positions, nodes, y_min, y_max, n_bins=N_YBINS):
    """Sum amplitudes into y-bins."""
    bw = (y_max - y_min) / n_bins
    bins = [0j] * n_bins
    for m in nodes:
        y = positions[m][1]
        b = int((y - y_min) / bw)
        b = max(0, min(n_bins - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity(amps_a, amps_b, D, det_list):
    """Purity under CL bath factor D. Returns (pur_cl, pur_coh, pur_min)."""
    def _pur(D_val):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + D_val * amps_a[d1].conjugate() * amps_b[d2]
                    + D_val * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real

    return _pur(D), _pur(1.0), _pur(0.0)


def test_family(name, generator, n_layers_list, n_seeds=4, **gen_kwargs):
    """Run the topology pivot test for one graph family."""
    k_band = [3.0, 5.0, 7.0]
    results = {}

    for nl in n_layers_list:
        pur_min_list = []
        pur_cl_list = []
        pur_coh_list = []
        s_norm_list = []
        n_det_list = []

        for seed in range(n_seeds):
            positions, adj, _ = generator(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 11 + 7, **gen_kwargs
            )

            setup = build_setup(positions, adj, env_depth_layers=max(1, round(nl / 6)))
            if setup is None:
                continue

            blocked = setup["blocked"]
            field = setup["field"]
            src = setup["src"]
            det_list = setup["det_list"]
            cy = setup["cy"]
            by_layer = setup["by_layer"]
            layers = setup["layers"]
            bl_idx = len(layers) // 3
            bl = layers[bl_idx]
            bi = by_layer[bl]
            sa = [i for i in bi if positions[i][1] > cy + 3][:3]
            sb = [i for i in bi if positions[i][1] < cy - 3][:3]

            # Accumulate over k-band
            pur_min_k = []
            pur_cl_k = []
            pur_coh_k = []
            s_norm_k = []

            for k in k_band:
                blocked_a = blocked | set(sb)
                blocked_b = blocked | set(sa)
                amps_a = propagate(positions, adj, field, src, k, blocked_a)
                amps_b = propagate(positions, adj, field, src, k, blocked_b)

                # CL bath S
                start = bl_idx + 1
                stop = min(len(layers), start + max(1, round(nl / 6)))
                mid_nodes = []
                for layer in layers[start:stop]:
                    mid_nodes.extend(by_layer[layer])

                bins_a = bin_amplitudes(amps_a, positions, mid_nodes, -12.0, 12.0)
                bins_b = bin_amplitudes(amps_b, positions, mid_nodes, -12.0, 12.0)
                S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
                NA = sum(abs(a) ** 2 for a in bins_a)
                NB = sum(abs(b) ** 2 for b in bins_b)
                denom = NA + NB
                S_norm = S / denom if denom > 0 else 0.0
                D = math.exp(-LAM ** 2 * S_norm)

                pc, pcoh, pmin = cl_purity(amps_a, amps_b, D, det_list)
                if not math.isnan(pc):
                    pur_cl_k.append(pc)
                    pur_coh_k.append(pcoh)
                    pur_min_k.append(pmin)
                    s_norm_k.append(S_norm)

            if pur_min_k:
                pur_min_list.append(sum(pur_min_k) / len(pur_min_k))
                pur_cl_list.append(sum(pur_cl_k) / len(pur_cl_k))
                pur_coh_list.append(sum(pur_coh_k) / len(pur_coh_k))
                s_norm_list.append(sum(s_norm_k) / len(s_norm_k))
                n_det_list.append(len(det_list))

        if pur_min_list:
            results[nl] = {
                "pur_min": sum(pur_min_list) / len(pur_min_list),
                "pur_cl": sum(pur_cl_list) / len(pur_cl_list),
                "pur_coh": sum(pur_coh_list) / len(pur_coh_list),
                "s_norm": sum(s_norm_list) / len(s_norm_list),
                "n_det": sum(n_det_list) / len(n_det_list),
                "n_graphs": len(pur_min_list),
            }

    return results


def main():
    print("=" * 78)
    print("TOPOLOGY PIVOT TEST")
    print("  Does changing graph family remove the pur_min ceiling?")
    print(f"  CL bath lambda={LAM}, {N_YBINS} y-bins, k-band [3,5,7], 4 seeds")
    print("=" * 78)
    print()

    n_layers_list = [8, 12, 18, 25]

    families = [
        ("Uniform (baseline)", generate_causal_dag, {}),
        ("Hierarchical (leak=0.05)", generate_hierarchical_dag,
         {"channel_leak": 0.05}),
        ("Modular (xlink=0.02)", generate_modular_dag,
         {"crosslink_prob": 0.02}),
        ("Preferential (boost=3)", generate_preferential_dag,
         {"hub_boost": 3.0}),
    ]

    all_results = {}

    for name, gen, kwargs in families:
        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'pur_cl':>8s}  {'decoh':>8s}  "
              f"{'S_norm':>8s}  {'n_det':>5s}  {'n_ok':>4s}")
        print(f"  {'-' * 55}")

        results = test_family(name, gen, n_layers_list, **kwargs)
        all_results[name] = results

        for nl in n_layers_list:
            if nl in results:
                r = results[nl]
                decoh = r["pur_coh"] - r["pur_cl"]
                print(f"  {nl:4d}  {r['pur_min']:8.4f}  {r['pur_cl']:8.4f}  "
                      f"{decoh:+8.4f}  {r['s_norm']:8.5f}  {r['n_det']:5.0f}  "
                      f"{r['n_graphs']:4d}")
            else:
                print(f"  {nl:4d}  {'FAIL':>8s}")
        print()

    # Summary: which families keep pur_min bounded?
    print("=" * 78)
    print("SUMMARY: pur_min trajectory (want: stays << 1 as N grows)")
    print(f"  {'Family':<30s}", end="")
    for nl in n_layers_list:
        print(f"  N={nl:2d}", end="")
    print("   Verdict")
    print(f"  {'-' * 72}")

    for name in all_results:
        r = all_results[name]
        print(f"  {name:<30s}", end="")
        vals = []
        for nl in n_layers_list:
            if nl in r:
                v = r[nl]["pur_min"]
                vals.append(v)
                print(f"  {v:.3f}", end="")
            else:
                print(f"  {'---':>5s}", end="")
        if len(vals) >= 3:
            if vals[-1] < vals[0] or vals[-1] < 0.95:
                print("   PASS (bounded)")
            elif vals[-1] > 0.98:
                print("   FAIL (ceiling)")
            else:
                print("   MARGINAL")
        else:
            print("   INSUFFICIENT DATA")
        print()

    print()
    print("PASS = pur_min stays bounded away from 1 → topology preserves slit separation")
    print("FAIL = pur_min approaches 1 → geometric convergence still dominates")


if __name__ == "__main__":
    main()
