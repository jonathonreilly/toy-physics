#!/usr/bin/env python3
"""Dense same-graph joint verification for q=0.03.

This is the q=0.03 follow-up to the dense-prune same-graph controls.
The scope is intentionally narrow:
  - same seed-generated dense 3D graphs
  - same graph instance for baseline vs pruned comparison
  - N in {80, 100, 120}
  - paired summaries with honest uncertainty

The question is whether a gentler distinguishability-based prune keeps a
real pur_cl gain while preserving the gravity signal better than q=0.10.

PStack experiment: dense-prune-q003-joint-strict
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.three_d_joint_test import (  # type: ignore  # noqa: E402
    cl_purity,
    compute_field_3d,
    generate_3d_dag,
    propagate_3d,
)
from scripts.three_d_modular_gravity_mass_scaling import (  # type: ignore  # noqa: E402
    select_target_centered_mass_nodes,
)

K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 16
N_LAYERS_LIST = (80, 100, 120)
NODES_PER_LAYER = 60
XYZ_RANGE = 12.0
CONNECT_RADIUS = 2.7
GAP = 3.0
PRUNE_Q = 0.03
PRUNE_ITERS = 1
FIXED_MASS_COUNT = 8
FIXED_B_OFFSET = 3.0


@dataclass(frozen=True)
class JointSummary:
    pur_base: float
    pur_pruned: float
    grav_base: float
    grav_pruned: float
    removed_total: int

    @property
    def pur_delta(self) -> float:
        return self.pur_pruned - self.pur_base

    @property
    def grav_delta(self) -> float:
        return self.grav_pruned - self.grav_base


def _layer_map(positions: list[tuple[float, float, float]]) -> tuple[dict[int, list[int]], list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    return by_layer, layers


def _mean_se_t(vals: list[float]) -> tuple[float, float, float]:
    mean = statistics.fmean(vals)
    if len(vals) > 1:
        se = statistics.stdev(vals) / math.sqrt(len(vals))
    else:
        se = 0.0
    t = mean / se if se > 1e-30 else math.nan
    return mean, se, t


def _mean_offset_y(
    positions: list[tuple[float, float, float]],
    nodes: list[int],
    center_y: float,
) -> float:
    if not nodes:
        return float("nan")
    return statistics.fmean(positions[i][1] for i in nodes) - center_y


def _select_mass_nodes(
    positions: list[tuple[float, float, float]],
    by_layer: dict[int, list[int]],
    layers: list[int],
    center_y: float,
) -> list[int] | None:
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = select_target_centered_mass_nodes(
        by_layer[grav_layer],
        positions,
        center_y,
        FIXED_B_OFFSET,
        FIXED_MASS_COUNT,
    )
    return mass_nodes or None


def _barrier_slices(
    positions: list[tuple[float, float, float]],
    by_layer: dict[int, list[int]],
    layers: list[int],
) -> tuple[set[int], list[int], list[int], int, int, int]:
    center_y = statistics.fmean(y for _, y, _ in positions)
    barrier_idx = len(layers) // 3
    barrier_layer = layers[barrier_idx]
    barrier_nodes = by_layer[barrier_layer]
    slit_upper = [i for i in barrier_nodes if positions[i][1] > center_y + 3][:3]
    slit_lower = [i for i in barrier_nodes if positions[i][1] < center_y - 3][:3]
    if not slit_upper or not slit_lower:
        return set(), [], [], barrier_idx, barrier_layer, len(layers) - 1
    blocked = set(barrier_nodes) - set(slit_upper + slit_lower)
    return blocked, slit_upper, slit_lower, barrier_idx, barrier_layer, len(layers) - 1


def _score_candidates(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    blocked_barrier: set[int],
    slit_upper: list[int],
    slit_lower: list[int],
    by_layer: dict[int, list[int]],
    layers: list[int],
) -> list[tuple[int, float]]:
    """Score post-barrier candidates by slit distinguishability.

    We keep the score simple and transparent: low score means the node
    barely distinguishes the upper vs lower slit branches.
    """
    n = len(positions)
    field_flat = [0.0] * n
    k_score = 5.0

    amps_upper = propagate_3d(
        positions,
        adj,
        field_flat,
        src,
        k_score,
        blocked_barrier | set(slit_lower),
    )
    amps_lower = propagate_3d(
        positions,
        adj,
        field_flat,
        src,
        k_score,
        blocked_barrier | set(slit_upper),
    )

    grav_layer = layers[2 * len(layers) // 3]
    detector_layer = layers[-1]
    scores: list[tuple[int, float]] = []
    for layer in layers:
        if layer <= layers[len(layers) // 3] or layer == detector_layer or layer == grav_layer:
            continue
        for node in by_layer[layer]:
            au = abs(amps_upper[node]) ** 2
            al = abs(amps_lower[node]) ** 2
            denom = au + al
            score = abs(au - al) / denom if denom > 1e-30 else 0.0
            scores.append((node, score))
    scores.sort(key=lambda item: item[1])
    return scores


def _prune_graph(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    q: float,
    n_iters: int,
) -> tuple[dict[int, list[int]], int]:
    """Iteratively prune the bottom-q distinguishability nodes."""
    current_adj = {i: list(nbs) for i, nbs in adj.items()}
    total_removed = 0

    for _ in range(n_iters):
        by_layer, layers = _layer_map(positions)
        blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
            positions, by_layer, layers
        )
        if not slit_upper or not slit_lower:
            break

        src = by_layer[layers[0]]
        candidate_scores = _score_candidates(
            positions,
            current_adj,
            src,
            blocked_barrier,
            slit_upper,
            slit_lower,
            by_layer,
            layers,
        )
        if not candidate_scores:
            break

        n_remove = int(len(candidate_scores) * q)
        if n_remove <= 0:
            break

        remove_set = {node for node, _ in candidate_scores[:n_remove]}
        if not remove_set:
            break

        new_adj: dict[int, list[int]] = {}
        for i, nbs in current_adj.items():
            if i in remove_set:
                continue
            kept = [j for j in nbs if j not in remove_set]
            if kept:
                new_adj[i] = kept
            else:
                new_adj[i] = []

        total_removed += len(remove_set)
        current_adj = new_adj

    return current_adj, total_removed


def _joint_summary(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    n_layers: int,
) -> tuple[float, float, float]:
    by_layer, layers = _layer_map(positions)
    blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
        positions, by_layer, layers
    )
    if not slit_upper or not slit_lower:
        return math.nan, math.nan, math.nan

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return math.nan, math.nan, math.nan

    env_depth = max(1, round(n_layers / 6))
    start = barrier_idx + 1
    stop = min(len(layers), start + env_depth)
    mid_nodes: list[int] = []
    for layer in layers[start:stop]:
        mid_nodes.extend(by_layer[layer])
    if not mid_nodes:
        return math.nan, math.nan, math.nan

    field_mass = compute_field_3d(positions, mass_nodes)
    field_flat = [0.0] * len(positions)

    grav_vals: list[float] = []
    pur_vals: list[float] = []
    decoh_vals: list[float] = []

    for k in K_BAND:
        amps_mass = propagate_3d(positions, adj, field_mass, src, k, blocked_barrier)
        amps_flat = propagate_3d(positions, adj, field_flat, src, k, blocked_barrier)

        prob_mass = sum(abs(amps_mass[d]) ** 2 for d in det_list)
        prob_flat = sum(abs(amps_flat[d]) ** 2 for d in det_list)
        if prob_mass > 1e-30 and prob_flat > 1e-30:
            y_mass = sum(abs(amps_mass[d]) ** 2 * positions[d][1] for d in det_list) / prob_mass
            y_flat = sum(abs(amps_flat[d]) ** 2 * positions[d][1] for d in det_list) / prob_flat
            grav_vals.append(y_mass - y_flat)

        amps_a = propagate_3d(positions, adj, field_mass, src, k, blocked_barrier | set(slit_lower))
        amps_b = propagate_3d(positions, adj, field_mass, src, k, blocked_barrier | set(slit_upper))

        bins_a = [0j] * 8
        bins_b = [0j] * 8
        bw = 24.0 / 8
        for node in mid_nodes:
            y = positions[node][1]
            idx = int((y + 12.0) / bw)
            idx = max(0, min(7, idx))
            bins_a[idx] += amps_a[node]
            bins_b[idx] += amps_b[node]

        S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
        NA = sum(abs(a) ** 2 for a in bins_a)
        NB = sum(abs(b) ** 2 for b in bins_b)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-(10.0 ** 2) * Sn)
        pc, pcoh, pmin = cl_purity(amps_a, amps_b, D_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)
            decoh_vals.append(pcoh - pc)

    if not grav_vals or not pur_vals:
        return math.nan, math.nan, math.nan

    return (
        statistics.fmean(pur_vals),
        statistics.fmean(grav_vals),
        statistics.fmean(decoh_vals),
    )


def _paired_seed_summary(n_layers: int, seed: int) -> JointSummary | None:
    positions, adj = generate_3d_dag(
        n_layers=n_layers,
        nodes_per_layer=NODES_PER_LAYER,
        xyz_range=XYZ_RANGE,
        connect_radius=CONNECT_RADIUS,
        rng_seed=seed * 7 + 3,
        gap=GAP,
    )
    by_layer, layers = _layer_map(positions)
    if len(layers) < 7:
        return None

    center_y = statistics.fmean(y for _, y, _ in positions)
    mass_nodes = _select_mass_nodes(positions, by_layer, layers, center_y)
    if not mass_nodes:
        return None

    pruned_adj, removed_total = _prune_graph(positions, adj, PRUNE_Q, PRUNE_ITERS)

    pur_base, grav_base, _ = _joint_summary(positions, adj, mass_nodes, n_layers)
    pur_pruned, grav_pruned, _ = _joint_summary(positions, pruned_adj, mass_nodes, n_layers)

    if any(math.isnan(v) for v in (pur_base, grav_base, pur_pruned, grav_pruned)):
        return None

    return JointSummary(
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        removed_total=removed_total,
    )


def main() -> None:
    print("=" * 90)
    print("DENSE + PRUNE SAME-GRAPH JOINT VERIFICATION (STRICT q=0.03)")
    print("  Same seed-generated dense 3D graphs; paired baseline/pruned summaries")
    print("=" * 90)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune quantile: {PRUNE_Q}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  fixed mass count: {FIXED_MASS_COUNT}")
    print(f"  fixed b offset: {FIXED_B_OFFSET}")
    print()
    print(
        f"{'N':>4s}  {'valid':>5s}  {'pur_base':>8s}  {'pur_pruned':>10s}  "
        f"{'pur_delta':>9s}  {'pur_SE':>8s}  {'pur_t':>7s}  "
        f"{'grav_base':>9s}  {'grav_pruned':>11s}  {'grav_delta':>10s}  "
        f"{'grav_SE':>8s}  {'grav_t':>7s}  {'removed':>8s}"
    )
    print("-" * 112)

    retained: list[tuple[int, JointSummary]] = []

    for n_layers in N_LAYERS_LIST:
        rows: list[JointSummary] = []
        for seed in range(N_SEEDS):
            row = _paired_seed_summary(n_layers, seed)
            if row is not None:
                rows.append(row)

        if not rows:
            print(
                f"{n_layers:4d}  {0:5d}  {'NA':>8s}  {'NA':>10s}  "
                f"{'NA':>9s}  {'NA':>8s}  {'NA':>7s}  "
                f"{'NA':>9s}  {'NA':>11s}  {'NA':>10s}  {'NA':>8s}  {'NA':>7s}  {'NA':>8s}"
            )
            continue

        pur_base_vals = [r.pur_base for r in rows]
        pur_pruned_vals = [r.pur_pruned for r in rows]
        grav_base_vals = [r.grav_base for r in rows]
        grav_pruned_vals = [r.grav_pruned for r in rows]
        pur_deltas = [r.pur_delta for r in rows]
        grav_deltas = [r.grav_delta for r in rows]
        removed_vals = [r.removed_total for r in rows]

        pur_base_mean = statistics.fmean(pur_base_vals)
        pur_pruned_mean = statistics.fmean(pur_pruned_vals)
        grav_base_mean = statistics.fmean(grav_base_vals)
        grav_pruned_mean = statistics.fmean(grav_pruned_vals)
        pur_delta_mean, pur_se, pur_t = _mean_se_t(pur_deltas)
        grav_delta_mean, grav_se, grav_t = _mean_se_t(grav_deltas)
        removed_mean = statistics.fmean(removed_vals)

        print(
            f"{n_layers:4d}  {len(rows):5d}  {pur_base_mean:8.4f}  {pur_pruned_mean:10.4f}  "
            f"{pur_delta_mean:+9.4f}  {pur_se:8.4f}  {pur_t:7.2f}  "
            f"{grav_base_mean:+9.4f}  {grav_pruned_mean:+11.4f}  {grav_delta_mean:+10.4f}  "
            f"{grav_se:8.4f}  {grav_t:7.2f}  {removed_mean:8.1f}"
        )
        retained.append((n_layers, rows[0]))

    print()
    print("RETAINED CLAIM")
    print("  q=0.03 still gives a same-graph pur_cl gain on the dense 3D family,")
    print("  but the gravity signal is only partially preserved and remains weaker")
    print("  than the unpruned baseline, especially at N=80 where the sign can flip.")
    print("  This is a gentler prune than q=0.10, not a full gravity repair.")
    print("=" * 90)


if __name__ == "__main__":
    main()
