#!/usr/bin/env python3
"""3D modular DAG asymptotic decoherence sweep.

This is the retained 3D CL-bath lane pushed to larger N.
Primary topology: modular gap=3.
Primary outputs: pur_cl and S_norm.
Optional output: true visibility gain, if the 3D single-vs-double-slit
comparison is easy to reuse.

The goal is to test whether the 3D ceiling stays broken at large N or
whether the improvement is only delayed.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.three_d_joint_test import (
    bin_amplitudes_3d,
    compute_field_3d,
    generate_3d_dag,
    propagate_3d,
)

BETA = 0.8
LAM = 10.0
K_BAND = [3.0, 5.0, 7.0]
VIS_K = 5.0
GAP = 3.0
CROSSLINK = 0.02
CONNECT_RADIUS = 4.0
N_YBINS = 8


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


def _detector_probs(amps, det_list):
    probs = {d: abs(amps[d]) ** 2 for d in det_list}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def _profile_visibility(profile):
    if len(profile) < 3:
        return 0.0
    peaks = [
        profile[i]
        for i in range(1, len(profile) - 1)
        if profile[i] > profile[i - 1] and profile[i] > profile[i + 1]
    ]
    troughs = [
        profile[i]
        for i in range(1, len(profile) - 1)
        if profile[i] < profile[i - 1] and profile[i] < profile[i + 1]
    ]
    if not peaks or not troughs:
        return 0.0
    top = max(peaks)
    bottom = min(troughs)
    return (top - bottom) / (top + bottom) if top + bottom > 1e-30 else 0.0


def _detector_profile(probs, positions, det_list):
    by_y = defaultdict(float)
    for d in det_list:
        by_y[positions[d][1]] += probs.get(d, 0.0)
    ys = sorted(by_y)
    return [by_y[y] for y in ys]


def cl_purity_3d(amps_a, amps_b, D, det_list):
    """CL-bath purity for the large-N 3D sweep.

    The detector trace can become tiny at large N, but the normalized
    reduced density matrix is still well-defined as long as the trace is
    nonzero. Use a very small cutoff instead of the stricter helper in the
    joint-test script so the asymptotic sweep remains numerically usable.
    """

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
        if tr <= 1e-300:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real

    return _pur(D), _pur(1.0), _pur(0.0)


def true_visibility_gain_3d(positions, adj, field, src, det_list, blocked_both, slit_a, slit_b):
    """3D analogue of the true single-vs-double-slit visibility comparison."""
    amps_both = propagate_3d(positions, adj, field, src, VIS_K, blocked_both)
    amps_a = propagate_3d(positions, adj, field, src, VIS_K, blocked_both | set(slit_b))
    amps_b = propagate_3d(positions, adj, field, src, VIS_K, blocked_both | set(slit_a))

    probs_both = _detector_probs(amps_both, det_list)
    probs_a = _detector_probs(amps_a, det_list)
    probs_b = _detector_probs(amps_b, det_list)

    probs_single_avg = {
        d: 0.5 * probs_a.get(d, 0.0) + 0.5 * probs_b.get(d, 0.0)
        for d in det_list
    }

    prof_both = _detector_profile(probs_both, positions, det_list)
    prof_single = _detector_profile(probs_single_avg, positions, det_list)
    v_coh = _profile_visibility(prof_both)
    v_single = _profile_visibility(prof_single)
    return v_coh, v_single, v_coh - v_single


def run_single_graph(nl, seed):
    positions, adj = generate_3d_dag(
        n_layers=nl,
        nodes_per_layer=30,
        xyz_range=12.0,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed,
        gap=GAP,
    )[:2]

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

    cy = sum(positions[i][1] for i in range(len(positions))) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    env_depth = max(1, round(nl / 6))
    start = bl_idx + 1
    stop = min(len(layers), start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    if not mid:
        return None

    mass_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[mass_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None

    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)

    pur_min_list = []
    pur_cl_list = []
    pur_coh_list = []
    s_norm_list = []
    vis_gain_list = []

    for k in K_BAND:
        amps_m = propagate_3d(positions, adj, field_m, src, k, blocked)
        amps_f = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(amps_m[d]) ** 2 for d in det_list)
        pf = sum(abs(amps_f[d]) ** 2 for d in det_list)
        if pm <= 1e-300 or pf <= 1e-300:
            continue

        ba = bin_amplitudes_3d(amps_m, positions, mid)
        bb = bin_amplitudes_3d(amps_f, positions, mid)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-LAM ** 2 * sn)

        pc, pcoh, pmin = cl_purity_3d(amps_m, amps_f, D, det_list)
        if math.isnan(pc):
            continue
        pur_cl_list.append(pc)
        pur_coh_list.append(pcoh)
        pur_min_list.append(pmin)
        s_norm_list.append(sn)

        # Visibility is only a bonus metric; use the same retained graph instance.
        v_coh, v_single, v_gain = true_visibility_gain_3d(
            positions, adj, field_m, src, det_list, blocked, sa, sb
        )
        vis_gain_list.append(v_gain)

    if not pur_cl_list:
        return None

    return {
        "pur_min": sum(pur_min_list) / len(pur_min_list),
        "pur_cl": sum(pur_cl_list) / len(pur_cl_list),
        "pur_coh": sum(pur_coh_list) / len(pur_coh_list),
        "decoh": (sum(pur_coh_list) / len(pur_coh_list))
        - (sum(pur_cl_list) / len(pur_cl_list)),
        "S_norm": sum(s_norm_list) / len(s_norm_list),
        "vis_gain": sum(vis_gain_list) / len(vis_gain_list) if vis_gain_list else None,
    }


def main():
    print("=" * 78)
    print("3D MODULAR DAG ASYMPTOTIC DECOHERENCE")
    print(f"  topology: modular gap={GAP}, crosslink={CROSSLINK}")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 8 seeds per N")
    print(f"  visibility gain: true single-vs-double-slit comparison")
    print("=" * 78)
    print()

    n_layers_list = [12, 18, 25, 40, 60, 80, 100]
    seeds = [s * 13 + 5 for s in range(8)]
    rows = []

    header = (
        f"  {'N':>4s}  {'pur_min':>8s}  {'pur_cl':>8s}  {'decoh':>8s}  "
        f"{'S_norm':>8s}  {'V_gain':>7s}  {'n_ok':>4s}  {'time':>6s}"
    )
    print(header)
    print(f"  {'-' * (len(header) - 2)}")

    for nl in n_layers_list:
        t0 = time.time()
        pm_list = []
        pc_list = []
        pcoh_list = []
        sn_list = []
        vg_list = []

        for seed in seeds:
            r = run_single_graph(nl, seed)
            if r is None:
                continue
            pm_list.append(r["pur_min"])
            pc_list.append(r["pur_cl"])
            pcoh_list.append(r["pur_coh"])
            sn_list.append(r["S_norm"])
            if r["vis_gain"] is not None:
                vg_list.append(r["vis_gain"])

        dt = time.time() - t0
        if not pc_list:
            print(f"  {nl:4d}  FAIL")
            continue

        avg_pm = sum(pm_list) / len(pm_list)
        avg_pc = sum(pc_list) / len(pc_list)
        avg_pcoh = sum(pcoh_list) / len(pcoh_list)
        avg_sn = sum(sn_list) / len(sn_list)
        avg_vg = sum(vg_list) / len(vg_list) if vg_list else float("nan")
        decoh = avg_pcoh - avg_pc
        rows.append((nl, avg_pm, avg_pc, decoh, avg_sn, avg_vg, len(pc_list)))

        vg_text = f"{avg_vg:+7.3f}" if math.isfinite(avg_vg) else "   pending"
        print(
            f"  {nl:4d}  {avg_pm:8.4f}  {avg_pc:8.4f}  {decoh:+8.4f}  "
            f"{avg_sn:8.5f}  {vg_text:>7s}  {len(pc_list):4d}  {dt:5.0f}s"
        )

    print()
    print("=" * 78)
    print("VERDICT")
    print("=" * 78)

    if rows:
        tail = [r for r in rows if r[0] >= 40]
        if tail:
            tail_pm = sum(r[2] for r in tail) / len(tail)
            tail_sn = sum(r[4] for r in tail) / len(tail)
            print(f"  Large-N mean pur_cl (N>=40): {tail_pm:.4f}")
            print(f"  Large-N mean S_norm (N>=40): {tail_sn:.5f}")
            if tail_pm < 0.96:
                print("  Verdict: pur_cl remains bounded away from 1 at large N.")
            else:
                print("  Verdict: ceiling appears to return or remain too close to 1.")
        else:
            print("  Verdict: insufficient large-N data.")

    print("  Visibility gain: pending dedicated 3D single-vs-double-slit metric.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
