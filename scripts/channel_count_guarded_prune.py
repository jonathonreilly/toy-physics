#!/usr/bin/env python3
"""Channel-count-preserving pruning guard.

The path cancellation audit found that effective detector channel count
(r=0.985 with gravity delta at N=100) is the diagnostic that tracks
the gravity sign flip. This guard prevents pruning from dropping
eff_ch below a threshold.

Unlike the coarse mass-path guard (which checked total reach and
either blocked everything or nothing), this guard targets the actual
vulnerable quantity identified by the mechanism audit.

PStack experiment: channel-count-guarded-prune
"""

from __future__ import annotations

import cmath
import math
import os
import random
import statistics
import sys
from collections import defaultdict, deque
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.dense_prune_q003_joint_strict import (
    GAP, K_BAND, N_SEEDS, NODES_PER_LAYER, CONNECT_RADIUS, XYZ_RANGE,
    PRUNE_ITERS, _barrier_slices, _layer_map, _prune_graph, _select_mass_nodes,
)
from scripts.causal_field_mass_scaling import field_laplacian
from scripts.three_d_joint_test import cl_purity, generate_3d_dag, propagate_3d

BETA = 0.8
N_YBINS = 8
LAM = 10.0
N120_DENSE_NODES_PER_LAYER = int(os.environ.get("CHANNEL_GUARD_N120_NPL", "80"))
N120_DENSE_CONNECT_RADIUS = float(
    os.environ.get("CHANNEL_GUARD_N120_RADIUS", f"{CONNECT_RADIUS}")
)


@dataclass(frozen=True)
class TestConfig:
    n_layers: int
    nodes_per_layer: int
    connect_radius: float
    xyz_range: float
    label: str


def _effective_channel_count(positions, adj, src, mass_nodes, det_nodes, blocked):
    """Compute effective detector channel count (the diagnostic metric)."""
    center_y = statistics.fmean(y for _, y, _ in positions)
    field_mass = field_laplacian(positions, adj, mass_nodes)
    field_flat = [0.0] * len(positions)

    eff_vals = []
    for k in K_BAND:
        amps_mass = propagate_3d(positions, adj, field_mass, src, k, blocked)
        amps_flat = propagate_3d(positions, adj, field_flat, src, k, blocked)

        signed = []
        for d in det_nodes:
            pm = abs(amps_mass[d])**2
            pf = abs(amps_flat[d])**2
            dy = positions[d][1] - center_y
            signed.append((pm - pf) * dy)

        weights = [abs(v) for v in signed]
        wsum = sum(weights)
        if wsum > 1e-30:
            probs = [w/wsum for w in weights]
            entropy = -sum(p * math.log(p) for p in probs if p > 1e-30)
            eff_vals.append(math.exp(entropy))
        else:
            eff_vals.append(0.0)

    return statistics.fmean(eff_vals) if eff_vals else 0.0


def _gravity_signal(positions, adj, mass_nodes, src, det_nodes, blocked):
    field_mass = field_laplacian(positions, adj, mass_nodes)
    field_flat = [0.0] * len(positions)
    shifts = []
    for k in K_BAND:
        am = propagate_3d(positions, adj, field_mass, src, k, blocked)
        af = propagate_3d(positions, adj, field_flat, src, k, blocked)
        total_m = sum(abs(am[d])**2 for d in det_nodes)
        total_f = sum(abs(af[d])**2 for d in det_nodes)
        if total_m > 1e-30 and total_f > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_nodes) / total_m
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_nodes) / total_f
            shifts.append(ym - yf)
    return statistics.fmean(shifts) if shifts else 0.0


def _cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys: return 0.0
    y_min, y_max = min(ys)-0.01, max(ys)+0.01
    bw = (y_max-y_min)/N_YBINS
    ba = [0j]*N_YBINS; bb = [0j]*N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS-1, int((positions[m][1]-y_min)/bw)))
        ba[b] += amps_a[m]; bb[b] += amps_b[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S/d if d > 0 else 0.0


def _measure_decoherence(positions, adj, src, det_nodes, slit_a, slit_b, blocked_base, mid_nodes, mass_all):
    field = field_laplacian(positions, adj, mass_all)
    blocked_a = blocked_base | set(slit_b)
    blocked_b = blocked_base | set(slit_a)
    pur_list = []
    for k in K_BAND:
        aa = propagate_3d(positions, adj, field, src, k, blocked_a)
        ab = propagate_3d(positions, adj, field, src, k, blocked_b)
        Sn = _cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM**2 * Sn)
        pur_cl, _, _ = cl_purity(aa, ab, D, det_nodes)
        if not math.isnan(pur_cl):
            pur_list.append(pur_cl)
    return statistics.fmean(pur_list) if pur_list else math.nan


def _make_graph(cfg: TestConfig, seed: int):
    return generate_3d_dag(
        n_layers=cfg.n_layers,
        nodes_per_layer=cfg.nodes_per_layer,
        xyz_range=cfg.xyz_range,
        connect_radius=cfg.connect_radius,
        rng_seed=seed * 7 + 3,
        gap=GAP,
    )


def channel_guarded_prune(positions, adj, layer_indices, mass_nodes, src, det_nodes,
                           blocked, quantile=0.10, max_iter=3, min_eff_ratio=0.80):
    """Prune with channel-count guard: undo if eff_ch drops below min_eff_ratio * baseline."""
    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys)/len(all_ys)

    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy+3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy-3][:5]
    if not slit_a or not slit_b:
        return adj, 0

    base_blocked = set(barrier) - set(slit_a+slit_b)
    blocked_a = base_blocked | set(slit_b)
    det_set = set(det_nodes)
    field_zero = [0.0]*n

    # Baseline eff_ch
    base_eff = _effective_channel_count(positions, adj, src, mass_nodes, det_nodes, blocked)

    current_adj = dict(adj)
    total_removed = 0

    for _ in range(max_iter):
        amps_a = propagate_3d(positions, current_adj, field_zero, src, 5.0, blocked_a)
        amps_b = propagate_3d(positions, current_adj, field_zero, src, 5.0, base_blocked|set(slit_a))

        node_d = []
        for li in range(bl_idx+1, n_layers-1):
            for i in layer_indices[li]:
                if i in det_set: continue
                pa, pb = abs(amps_a[i])**2, abs(amps_b[i])**2
                total = pa+pb
                D = abs(pa-pb)/total if total > 1e-30 else 0.0
                node_d.append((i, D))
        if not node_d: break

        node_d.sort(key=lambda x: x[1])
        n_remove = max(1, int(len(node_d)*quantile))
        remove_set = set(idx for idx, _ in node_d[:n_remove])

        tentative = {}
        for i, nbs in current_adj.items():
            if i in remove_set: continue
            filtered = [j for j in nbs if j not in remove_set]
            if filtered: tentative[i] = filtered

        # Check eff_ch
        new_eff = _effective_channel_count(positions, tentative, src, mass_nodes, det_nodes, blocked)
        if base_eff > 0 and new_eff < min_eff_ratio * base_eff:
            break  # Guard triggered

        total_removed += len(remove_set)
        current_adj = tentative

    return current_adj, total_removed


def _seed_summary(cfg: TestConfig, seed: int, use_guard: bool) -> tuple[float, float, float, float, float, float, int] | None:
    positions, adj = _make_graph(cfg, seed)
    by_layer, layers = _layer_map(positions)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_nodes = list(by_layer[layers[-1]])
    if not det_nodes:
        return None

    center_y = statistics.fmean(y for _, y, _ in positions)
    blocked_base, slit_a, slit_b, bl_idx, _, _ = _barrier_slices(positions, by_layer, layers)
    if not slit_a or not slit_b:
        return None

    mass_nodes = _select_mass_nodes(positions, by_layer, layers, center_y)
    if not mass_nodes:
        return None

    n_act = len(layers)
    bath_mass = []
    for li_idx in range(bl_idx + 1, min(n_act, bl_idx + 3)):
        for i in by_layer[layers[li_idx]]:
            if abs(positions[i][1] - center_y) <= 3:
                bath_mass.append(i)
    grav_idx = 2 * n_act // 3
    grav_mass = [i for i in by_layer[layers[grav_idx]] if positions[i][1] > center_y + 1]
    mass_all = list(set(bath_mass) | set(grav_mass))

    mid_nodes = [
        i
        for li_idx in range(bl_idx + 1, n_act - 1)
        for i in by_layer[layers[li_idx]]
        if i not in blocked_base and i not in set(det_nodes)
    ]

    gb = _gravity_signal(positions, adj, mass_nodes, src, det_nodes, blocked_base)
    pb = _measure_decoherence(positions, adj, src, det_nodes, slit_a, slit_b, blocked_base, mid_nodes, mass_all)
    eb = _effective_channel_count(positions, adj, src, mass_nodes, det_nodes, blocked_base)
    if math.isnan(pb):
        return None

    if use_guard:
        layer_list = [by_layer[l] for l in layers]
        adj_p, _ = channel_guarded_prune(
            positions,
            adj,
            layer_list,
            mass_nodes,
            src,
            det_nodes,
            blocked_base,
            quantile=0.10,
            max_iter=3,
            min_eff_ratio=0.80,
        )
    else:
        adj_p, _ = _prune_graph(positions, adj, q=0.10, n_iters=1)

    gp = _gravity_signal(positions, adj_p, mass_nodes, src, det_nodes, blocked_base)
    pp = _measure_decoherence(positions, adj_p, src, det_nodes, slit_a, slit_b, blocked_base, mid_nodes, mass_all)
    ep = _effective_channel_count(positions, adj_p, src, mass_nodes, det_nodes, blocked_base)
    if math.isnan(pp):
        return None

    flip_count = 1 if gb > 0 and gp < 0 else 0
    return gb, gp, pb, pp, eb, ep, flip_count


def main():
    n_seeds = 16
    print("=" * 74)
    print("CHANNEL-COUNT-PRESERVING PRUNING GUARD")
    print("  Guard: undo prune if eff_ch drops below 80% of baseline")
    print("  Compare: unguarded vs channel-guarded")
    print("=" * 74)
    print()
    base_cfgs = [
        TestConfig(80, NODES_PER_LAYER, CONNECT_RADIUS, XYZ_RANGE, "npl=60"),
        TestConfig(100, NODES_PER_LAYER, CONNECT_RADIUS, XYZ_RANGE, "npl=60"),
        TestConfig(120, NODES_PER_LAYER, CONNECT_RADIUS, XYZ_RANGE, "npl=60"),
        TestConfig(120, N120_DENSE_NODES_PER_LAYER, N120_DENSE_CONNECT_RADIUS, XYZ_RANGE,
                   f"npl={N120_DENSE_NODES_PER_LAYER}"),
    ]

    print(f"  default npl: {NODES_PER_LAYER}")
    print(f"  dense N=120 npl: {N120_DENSE_NODES_PER_LAYER}")
    print()

    print(f"  {'N':>4s}  {'variant':>10s}  {'grav_b':>7s}  {'grav_p':>7s}  "
          f"{'pur_b':>6s}  {'pur_p':>6s}  {'eff_b':>5s}  {'eff_p':>5s}  "
          f"{'flips':>5s}  {'n':>3s}")
    print(f"  {'-'*88}")

    for cfg in base_cfgs:
        for label, use_guard in [("Unguarded", False), ("Channel-guarded", True)]:
            grav_b_list = []; grav_p_list = []
            pur_b_list = []; pur_p_list = []
            eff_b_list = []; eff_p_list = []
            flip_count = 0

            for seed in range(n_seeds):
                row = _seed_summary(cfg, seed, use_guard)
                if row is None:
                    continue
                gb, gp, pb, pp, eb, ep, flips = row
                grav_b_list.append(gb); grav_p_list.append(gp)
                pur_b_list.append(pb); pur_p_list.append(pp)
                eff_b_list.append(eb); eff_p_list.append(ep)
                flip_count += flips

            if grav_b_list:
                n_ok = len(grav_b_list)
                print(f"  {cfg.n_layers:4d}  {cfg.label + ' ' + label:>10s}  {statistics.fmean(grav_b_list):+7.3f}  "
                      f"{statistics.fmean(grav_p_list):+7.3f}  "
                      f"{statistics.fmean(pur_b_list):6.4f}  "
                      f"{statistics.fmean(pur_p_list):6.4f}  "
                      f"{statistics.fmean(eff_b_list):5.1f}  "
                      f"{statistics.fmean(eff_p_list):5.1f}  "
                      f"{flip_count:5d}  {n_ok:3d}")

        print()

    print("=" * 74)
    print("KEY: channel-guarded should have fewer flips AND eff_p closer to eff_b")
    print("while still achieving pur_p < pur_b (decoherence improvement)")
    print("=" * 74)


if __name__ == "__main__":
    main()
