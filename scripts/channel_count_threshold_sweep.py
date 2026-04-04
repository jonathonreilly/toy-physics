#!/usr/bin/env python3
"""Threshold sweep for the channel-count pruning guard.

This driver reuses the same dense 3D setup as
`channel_count_guarded_prune.py` and sweeps the guard threshold
against a small set of pruning quantiles on N=80 and N=100.

The goal is deliberately narrow:
- map where the channel-count guard still preserves a decoherence gain
- check where gravity stays positive or minimizes flips
- avoid overclaiming beyond the exact threshold/q pocket

PStack experiment: channel-count-threshold-sweep
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.channel_count_guarded_prune import (  # type: ignore  # noqa: E402
    GAP,
    K_BAND,
    NODES_PER_LAYER,
    CONNECT_RADIUS,
    XYZ_RANGE,
    N120_DENSE_CONNECT_RADIUS,
    N120_DENSE_NODES_PER_LAYER,
    _barrier_slices,
    _effective_channel_count,
    _gravity_signal,
    _layer_map,
    _measure_decoherence,
    _make_graph,
    channel_guarded_prune,
)
from scripts.dense_prune_q003_joint_strict import _prune_graph  # type: ignore  # noqa: E402
from scripts.three_d_joint_test import cl_purity, generate_3d_dag, propagate_3d  # type: ignore  # noqa: E402


THRESHOLDS = (0.70, 0.75, 0.80, 0.85, 0.90)
Q_LIST = (0.03, 0.05, 0.10)
N_SEEDS = 16


@dataclass(frozen=True)
class TestConfig:
    n_layers: int
    nodes_per_layer: int
    connect_radius: float
    xyz_range: float
    label: str


def _make_cfg(n_layers: int, dense: bool = False) -> TestConfig:
    if n_layers == 120 and dense:
        return TestConfig(
            n_layers=120,
            nodes_per_layer=N120_DENSE_NODES_PER_LAYER,
            connect_radius=N120_DENSE_CONNECT_RADIUS,
            xyz_range=XYZ_RANGE,
            label=f"dense npl={N120_DENSE_NODES_PER_LAYER}",
        )
    return TestConfig(
        n_layers=n_layers,
        nodes_per_layer=NODES_PER_LAYER,
        connect_radius=CONNECT_RADIUS,
        xyz_range=XYZ_RANGE,
        label=f"npl={NODES_PER_LAYER}",
    )


def _seed_summary(cfg: TestConfig, seed: int, q: float, min_eff_ratio: float, use_guard: bool):
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

    # Same mass selection as the validated dense-prune guard path.
    from scripts.dense_prune_q003_joint_strict import _select_mass_nodes

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
            quantile=q,
            max_iter=3,
            min_eff_ratio=min_eff_ratio,
        )
    else:
        adj_p, _ = _prune_graph(positions, adj, q=q, n_iters=1)

    gp = _gravity_signal(positions, adj_p, mass_nodes, src, det_nodes, blocked_base)
    pp = _measure_decoherence(positions, adj_p, src, det_nodes, slit_a, slit_b, blocked_base, mid_nodes, mass_all)
    ep = _effective_channel_count(positions, adj_p, src, mass_nodes, det_nodes, blocked_base)
    if math.isnan(pp):
        return None

    flip_count = 1 if gb > 0 and gp < 0 else 0
    return gb, gp, pb, pp, eb, ep, flip_count


def _aggregate(cfg: TestConfig, q: float, min_eff_ratio: float, use_guard: bool):
    grav_b_list = []
    grav_p_list = []
    pur_b_list = []
    pur_p_list = []
    eff_b_list = []
    eff_p_list = []
    flip_count = 0

    for seed in range(N_SEEDS):
        row = _seed_summary(cfg, seed, q, min_eff_ratio, use_guard)
        if row is None:
            continue
        gb, gp, pb, pp, eb, ep, flips = row
        grav_b_list.append(gb)
        grav_p_list.append(gp)
        pur_b_list.append(pb)
        pur_p_list.append(pp)
        eff_b_list.append(eb)
        eff_p_list.append(ep)
        flip_count += flips

    if not grav_b_list:
        return None

    return {
        "n": len(grav_b_list),
        "grav_b": statistics.fmean(grav_b_list),
        "grav_p": statistics.fmean(grav_p_list),
        "pur_b": statistics.fmean(pur_b_list),
        "pur_p": statistics.fmean(pur_p_list),
        "eff_b": statistics.fmean(eff_b_list),
        "eff_p": statistics.fmean(eff_p_list),
        "flips": flip_count,
    }


def _fmt_row(q: float, thr: float, base: dict[str, float], guard: dict[str, float]) -> str:
    return (
        f"  q={q:0.02f} thr={thr:0.02f}  "
        f"{base['grav_b']:+7.3f}  {base['grav_p']:+7.3f}  "
        f"{base['pur_b']:6.4f}  {base['pur_p']:6.4f}  "
        f"{base['eff_b']:5.1f}  {base['eff_p']:5.1f}  "
        f"{base['flips']:5d}  "
        f"{guard['grav_p']:+7.3f}  {guard['pur_p']:6.4f}  "
        f"{guard['eff_p']:5.1f}  {guard['flips']:5d}  {guard['n']:3d}"
    )


def main():
    print("=" * 118)
    print("CHANNEL-COUNT THRESHOLD SWEEP")
    print("  Grid: thresholds 0.70, 0.75, 0.80, 0.85, 0.90")
    print("  q values: 0.03, 0.05, 0.10")
    print("  Compare on N=80 and N=100 same dense 3D seed-generated graphs")
    print("=" * 118)
    print()
    print("Columns:")
    print("  base grav_b grav_p pur_b pur_p eff_b eff_p flips | guard grav_p pur_p eff_p flips n")
    print()

    for n_layers in (80, 100):
        cfg = _make_cfg(n_layers)
        print(f"N={n_layers}  ({cfg.label})")
        for q in Q_LIST:
            base = _aggregate(cfg, q, 0.80, use_guard=False)
            if base is None:
                print(f"  q={q:0.02f}  no valid baseline rows")
                continue
            print(f"  baseline q={q:0.02f}  grav_b={base['grav_b']:+.3f}  grav_p={base['grav_p']:+.3f}  "
                  f"pur_b={base['pur_b']:.4f}  pur_p={base['pur_p']:.4f}  "
                  f"eff_b={base['eff_b']:.1f}  eff_p={base['eff_p']:.1f}  flips={base['flips']}  n={base['n']}")
            for thr in THRESHOLDS:
                guard = _aggregate(cfg, q, thr, use_guard=True)
                if guard is None:
                    print(f"  q={q:0.02f} thr={thr:0.02f}  no valid guarded rows")
                    continue
                print(_fmt_row(q, thr, base, guard))
        print()

    print("=" * 118)
    print("Interpretation guide:")
    print("  Prefer rows with guard grav_p > 0, fewer flips than baseline, and pur_p <= pur_b.")
    print("  If all rows fail at N=100 or above a threshold, the guard pocket is bounded.")
    print("=" * 118)


if __name__ == "__main__":
    main()
