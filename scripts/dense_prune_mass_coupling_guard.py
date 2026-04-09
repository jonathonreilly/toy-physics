#!/usr/bin/env python3
"""Mass-coupling-aware prune guard on the dense same-graph control.

The pruning sign flip appears when pruning severs the graph support that
lets the mass-region field reach the detector region. A better guard than
"total detector reach" is to protect the current mass-to-detector path core:

  core_support = |Forward(mass_nodes) ∩ Reverse(detector_nodes)| / |post-barrier nodes|

This is a conservative proxy for mass-coupled detector support. The guard
below blocks pruning of nodes in that core, while still allowing pruning of
non-core nodes. We compare guarded vs plain pruning at q=0.05 and q=0.10
on the same dense 3D seed-generated graphs.

PStack experiment: dense-prune-mass-coupling-guard
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.dense_prune_q003_joint_strict import (  # type: ignore  # noqa: E402
    GAP,
    K_BAND,
    N_LAYERS_LIST,
    N_SEEDS,
    NODES_PER_LAYER,
    CONNECT_RADIUS,
    XYZ_RANGE,
    _barrier_slices,
    _joint_summary,
    _layer_map,
    _prune_graph,
    _score_candidates,
    _select_mass_nodes,
)
from scripts.dense_prune_q003_mechanism_audit import (  # type: ignore  # noqa: E402
    _mass_to_detector_reach,
    _path_core_nodes,
)
from scripts.three_d_joint_test import generate_3d_dag  # type: ignore  # noqa: E402


PRUNE_ITERS = 1
FIXED_MASS_COUNT = 8
FIXED_B_OFFSET = 3.0
Q_LIST = (0.05, 0.10)


@dataclass(frozen=True)
class Summary:
    q: float
    mode: str
    pur_base: float
    pur_pruned: float
    grav_base: float
    grav_pruned: float
    core_base: float
    core_pruned: float
    reach_base: float
    reach_pruned: float
    removed_total: int
    flip_count: int

    @property
    def pur_delta(self) -> float:
        return self.pur_pruned - self.pur_base

    @property
    def grav_delta(self) -> float:
        return self.grav_pruned - self.grav_base


def _mean_se_t(vals: list[float]) -> tuple[float, float, float]:
    mean = statistics.fmean(vals)
    if len(vals) > 1:
        se = statistics.stdev(vals) / math.sqrt(len(vals))
    else:
        se = 0.0
    t = mean / se if se > 1e-30 else math.nan
    return mean, se, t


def _support_metrics(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
) -> tuple[float, float]:
    by_layer, layers = _layer_map(positions)
    post_nodes = [
        i
        for layer in layers[len(layers) // 3 + 1 : -1]
        for i in by_layer[layer]
    ]
    if not post_nodes:
        return 0.0, 0.0

    core_nodes = _path_core_nodes(adj, mass_nodes, det_nodes)
    reach_frac, _ = _mass_to_detector_reach(adj, mass_nodes, det_nodes)
    core_frac = len(core_nodes) / len(post_nodes)
    return core_frac, reach_frac


def _mass_guarded_prune_graph(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    det_nodes: list[int],
    q: float,
    n_iters: int,
) -> tuple[dict[int, list[int]], int]:
    """Prune only non-core nodes.

    The protected set is the current mass-to-detector path core, i.e. nodes
    that lie on at least one path from the mass region to the detector region.
    """

    current_adj = deepcopy(adj)
    total_removed = 0

    for _ in range(n_iters):
        by_layer, layers = _layer_map(positions)
        blocked_barrier, slit_upper, slit_lower, barrier_idx, barrier_layer, detector_layer = _barrier_slices(
            positions, by_layer, layers
        )
        if not slit_upper or not slit_lower:
            break

        candidate_scores = _score_candidates(
            positions,
            current_adj,
            by_layer[layers[0]],
            blocked_barrier,
            slit_upper,
            slit_lower,
            by_layer,
            layers,
        )
        if not candidate_scores:
            break

        protected = _path_core_nodes(current_adj, mass_nodes, det_nodes)
        candidate_scores = [(node, score) for node, score in candidate_scores if node not in protected]
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
            new_adj[i] = kept

        current_adj = new_adj
        total_removed += len(remove_set)

    return current_adj, total_removed


def _paired_summary(
    n_layers: int,
    seed: int,
    q: float,
    guarded: bool,
) -> Summary | None:
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
    det_nodes = list(by_layer[layers[-1]])
    if not det_nodes:
        return None

    if guarded:
        pruned_adj, removed_total = _mass_guarded_prune_graph(
            positions, adj, mass_nodes, det_nodes, q, PRUNE_ITERS
        )
        mode = "guarded"
    else:
        pruned_adj, removed_total = _prune_graph(positions, adj, q, PRUNE_ITERS)
        mode = "plain"

    pur_base, grav_base, _ = _joint_summary(positions, adj, mass_nodes, n_layers)
    pur_pruned, grav_pruned, _ = _joint_summary(positions, pruned_adj, mass_nodes, n_layers)
    if any(math.isnan(v) for v in (pur_base, grav_base, pur_pruned, grav_pruned)):
        return None

    core_base, reach_base = _support_metrics(positions, adj, mass_nodes, det_nodes)
    core_pruned, reach_pruned = _support_metrics(positions, pruned_adj, mass_nodes, det_nodes)
    flip_count = 1 if grav_base > 0 and grav_pruned < 0 else 0

    return Summary(
        q=q,
        mode=mode,
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        core_base=core_base,
        core_pruned=core_pruned,
        reach_base=reach_base,
        reach_pruned=reach_pruned,
        removed_total=removed_total,
        flip_count=flip_count,
    )


def main() -> None:
    print("=" * 98)
    print("DENSE + PRUNE MASS-COUPLING GUARD")
    print("  Same dense 3D same-graph setup; guard protects mass-to-detector path core")
    print("=" * 98)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  fixed mass count: {FIXED_MASS_COUNT}")
    print(f"  fixed b offset: {FIXED_B_OFFSET}")
    print(f"  k-band: {K_BAND}")
    print(
        "  core_support proxy = |Forward(mass) ∩ Reverse(detectors)| / |post-barrier nodes|"
    )
    print()
    print(
        f"{'N':>4s}  {'mode':>8s}  {'q':>5s}  {'valid':>5s}  "
        f"{'pur_b':>8s}  {'pur_p':>8s}  {'d_pur':>8s}  "
        f"{'grav_b':>8s}  {'grav_p':>8s}  {'d_grav':>8s}  "
        f"{'core_b':>7s}  {'core_p':>7s}  {'reach_b':>7s}  {'reach_p':>7s}  "
        f"{'flips':>5s}  {'removed':>8s}"
    )
    print("-" * 142)

    for n_layers in N_LAYERS_LIST:
        for q in Q_LIST:
            for guarded in (False, True):
                rows: list[Summary] = []
                for seed in range(N_SEEDS):
                    row = _paired_summary(n_layers, seed, q, guarded)
                    if row is not None:
                        rows.append(row)

                mode = "guarded" if guarded else "plain"
                if not rows:
                    print(
                        f"{n_layers:4d}  {mode:>8s}  {q:5.2f}  {0:5d}  "
                        f"{'NA':>8s}  {'NA':>8s}  {'NA':>8s}  "
                        f"{'NA':>8s}  {'NA':>8s}  {'NA':>8s}  "
                        f"{'NA':>7s}  {'NA':>7s}  {'NA':>7s}  {'NA':>7s}  "
                        f"{'NA':>5s}  {'NA':>8s}"
                    )
                    continue

                pur_base = statistics.fmean(r.pur_base for r in rows)
                pur_pruned = statistics.fmean(r.pur_pruned for r in rows)
                grav_base = statistics.fmean(r.grav_base for r in rows)
                grav_pruned = statistics.fmean(r.grav_pruned for r in rows)
                core_base = statistics.fmean(r.core_base for r in rows)
                core_pruned = statistics.fmean(r.core_pruned for r in rows)
                reach_base = statistics.fmean(r.reach_base for r in rows)
                reach_pruned = statistics.fmean(r.reach_pruned for r in rows)
                d_pur, pur_se, pur_t = _mean_se_t([r.pur_pruned - r.pur_base for r in rows])
                d_grav, grav_se, grav_t = _mean_se_t([r.grav_pruned - r.grav_base for r in rows])
                removed_mean = statistics.fmean(r.removed_total for r in rows)
                flips = sum(r.flip_count for r in rows)

                print(
                    f"{n_layers:4d}  {mode:>8s}  {q:5.2f}  {len(rows):5d}  "
                    f"{pur_base:8.4f}  {pur_pruned:8.4f}  {d_pur:+8.4f}  "
                    f"{grav_base:+8.4f}  {grav_pruned:+8.4f}  {d_grav:+8.4f}  "
                    f"{core_base:7.3f}  {core_pruned:7.3f}  {reach_base:7.3f}  {reach_pruned:7.3f}  "
                    f"{flips:5d}  {removed_mean:8.1f}"
                )
            print()

    print("INTERPRETATION")
    print("  The guard is meant to protect mass-coupled detector support, not total")
    print("  detector reach. If it reduces sign flips without destroying pur_cl, the")
    print("  gravity flip is better explained as loss of mass-region-to-detector")
    print("  connectivity than as generic pruning damage.")
    print("=" * 98)


if __name__ == "__main__":
    main()
