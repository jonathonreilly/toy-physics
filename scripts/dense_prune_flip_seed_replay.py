#!/usr/bin/env python3
"""Seed-level replay of the dense-prune gravity sign-flip regime.

This script replays the same dense 3D same-graph setup used by the strict
dense-prune controls, but it records the result per seed instead of only
aggregating means.

Goal
----
Identify exactly which seeds flip sign under the relevant prune settings and
compare those flip seeds against nearby non-flip seeds using simple structural
metrics:
  - mass-to-detector reach
  - mass-to-detector path support
  - path-core size

The question is whether the flips are isolated outliers or a reproducible
subpopulation with a detectable structural signature.

PStack experiment: dense-prune-flip-seed-replay
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.dense_prune_q003_joint_strict import (  # type: ignore  # noqa: E402
    GAP,
    N_LAYERS_LIST,
    N_SEEDS,
    NODES_PER_LAYER,
    CONNECT_RADIUS,
    XYZ_RANGE,
    PRUNE_ITERS,
    _barrier_slices,
    _joint_summary,
    _layer_map,
    _prune_graph,
    _select_mass_nodes,
)
from scripts.dense_prune_q003_mechanism_audit import (  # type: ignore  # noqa: E402
    _mass_to_detector_reach,
    _mass_path_support,
    _path_core_nodes,
)
from scripts.three_d_joint_test import generate_3d_dag  # type: ignore  # noqa: E402


Q_LIST = (0.03, 0.10)
FIXED_MASS_COUNT = 8
FIXED_B_OFFSET = 3.0


@dataclass(frozen=True)
class SeedRecord:
    n_layers: int
    q: float
    seed: int
    pur_base: float
    pur_pruned: float
    grav_base: float
    grav_pruned: float
    reach_base: float
    reach_pruned: float
    support_base: float
    support_pruned: float
    core_base: float
    core_pruned: float
    removed_total: int

    @property
    def pur_delta(self) -> float:
        return self.pur_pruned - self.pur_base

    @property
    def grav_delta(self) -> float:
        return self.grav_pruned - self.grav_base

    @property
    def reach_delta(self) -> float:
        return self.reach_pruned - self.reach_base

    @property
    def support_delta(self) -> float:
        return self.support_pruned - self.support_base

    @property
    def core_delta(self) -> float:
        return self.core_pruned - self.core_base

    @property
    def flipped(self) -> bool:
        return self.grav_base > 0 and self.grav_pruned < 0


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _layer_stats(positions: list[tuple[float, float, float]], nodes: list[int]) -> tuple[float, float]:
    if not nodes:
        return math.nan, math.nan
    ys = [positions[i][1] for i in nodes]
    return statistics.fmean(ys), statistics.stdev(ys) if len(ys) > 1 else 0.0


def _seed_record(n_layers: int, seed: int, q: float) -> SeedRecord | None:
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

    pruned_adj, removed_total = _prune_graph(positions, adj, q, PRUNE_ITERS)

    pur_base, grav_base, _ = _joint_summary(positions, adj, mass_nodes, n_layers)
    pur_pruned, grav_pruned, _ = _joint_summary(positions, pruned_adj, mass_nodes, n_layers)
    if any(math.isnan(v) for v in (pur_base, grav_base, pur_pruned, grav_pruned)):
        return None

    core_base = len(_path_core_nodes(adj, mass_nodes, det_nodes))
    core_pruned = len(_path_core_nodes(pruned_adj, mass_nodes, det_nodes))
    reach_base, _ = _mass_to_detector_reach(adj, mass_nodes, det_nodes)
    reach_pruned, _ = _mass_to_detector_reach(pruned_adj, mass_nodes, det_nodes)
    support_base = _mass_path_support(adj, mass_nodes, det_nodes)
    support_pruned = _mass_path_support(pruned_adj, mass_nodes, det_nodes)

    return SeedRecord(
        n_layers=n_layers,
        q=q,
        seed=seed,
        pur_base=pur_base,
        pur_pruned=pur_pruned,
        grav_base=grav_base,
        grav_pruned=grav_pruned,
        reach_base=reach_base,
        reach_pruned=reach_pruned,
        support_base=support_base,
        support_pruned=support_pruned,
        core_base=float(core_base),
        core_pruned=float(core_pruned),
        removed_total=removed_total,
    )


def _print_seed_table(rows: list[SeedRecord]) -> None:
    print(
        f"{'seed':>4s}  {'flip':>4s}  {'pur_b':>7s}  {'pur_p':>7s}  {'d_pur':>7s}  "
        f"{'grav_b':>8s}  {'grav_p':>8s}  {'d_grav':>8s}  "
        f"{'reach_b':>7s}  {'reach_p':>7s}  {'supp_b':>8s}  {'supp_p':>8s}  "
        f"{'core_b':>6s}  {'core_p':>6s}  {'removed':>7s}"
    )
    print(f"{'-' * 118}")
    for row in rows:
        print(
            f"{row.seed:4d}  {('Y' if row.flipped else 'N'):>4s}  "
            f"{row.pur_base:7.4f}  {row.pur_pruned:7.4f}  {row.pur_delta:+7.4f}  "
            f"{row.grav_base:+8.4f}  {row.grav_pruned:+8.4f}  {row.grav_delta:+8.4f}  "
            f"{row.reach_base:7.3f}  {row.reach_pruned:7.3f}  "
            f"{row.support_base:8.3f}  {row.support_pruned:8.3f}  "
            f"{row.core_base:6.0f}  {row.core_pruned:6.0f}  {row.removed_total:7d}"
        )


def _summary(rows: list[SeedRecord]) -> tuple[float, float, float, float, float, float]:
    pur_delta = statistics.fmean(r.pur_delta for r in rows)
    grav_delta = statistics.fmean(r.grav_delta for r in rows)
    reach_delta = statistics.fmean(r.reach_delta for r in rows)
    support_delta = statistics.fmean(r.support_delta for r in rows)
    core_delta = statistics.fmean(r.core_delta for r in rows)
    flips = sum(1 for r in rows if r.flipped) / len(rows)
    return pur_delta, grav_delta, reach_delta, support_delta, core_delta, flips


def _print_flip_neighbors(rows: list[SeedRecord], seed_window: int = 2) -> None:
    by_seed = {row.seed: row for row in rows}
    flip_rows = [row for row in rows if row.flipped]
    if not flip_rows:
        print("  no flip seeds in this configuration")
        return

    print("  nearby non-flip comparisons (within +/-2 seed ids):")
    for row in flip_rows:
        near = [
            other
            for other in rows
            if not other.flipped and other.seed != row.seed and abs(other.seed - row.seed) <= seed_window
        ]
        near = sorted(near, key=lambda other: abs(other.seed - row.seed))[:2]
        if not near:
            print(f"    seed {row.seed}: no nearby non-flip seeds in window")
            continue
        print(
            f"    seed {row.seed}: flip grav {row.grav_base:+.4f}->{row.grav_pruned:+.4f}, "
            f"pur {row.pur_base:.4f}->{row.pur_pruned:.4f}"
        )
        for other in near:
            print(
                f"      neighbor {other.seed}: grav {other.grav_base:+.4f}->{other.grav_pruned:+.4f}, "
                f"pur {other.pur_base:.4f}->{other.pur_pruned:.4f}, "
                f"reach {other.reach_base:.3f}->{other.reach_pruned:.3f}, "
                f"support {other.support_base:.3f}->{other.support_pruned:.3f}, "
                f"core {other.core_base:.0f}->{other.core_pruned:.0f}"
            )


def main() -> None:
    print("=" * 110)
    print("DENSE + PRUNE FLIP-SEED REPLAY")
    print("  Same dense 3D same-graph setup; identify exact flip seeds and nearby non-flips")
    print("=" * 110)
    print()
    print(f"  seeds: {N_SEEDS}")
    print(f"  n_layers: {N_LAYERS_LIST}")
    print(f"  nodes/layer: {NODES_PER_LAYER}")
    print(f"  connect_radius: {CONNECT_RADIUS}")
    print(f"  prune iterations: {PRUNE_ITERS}")
    print(f"  q sweep: {Q_LIST}")
    print(f"  fixed mass count: {FIXED_MASS_COUNT}")
    print(f"  fixed b offset: {FIXED_B_OFFSET}")
    print()

    for n_layers in N_LAYERS_LIST:
        print("=" * 110)
        print(f"N = {n_layers}")
        print("=" * 110)
        for q in Q_LIST:
            rows: list[SeedRecord] = []
            for seed in range(N_SEEDS):
                row = _seed_record(n_layers, seed, q)
                if row is not None:
                    rows.append(row)

            print()
            print(f"q = {q:.2f} | valid seeds = {len(rows)}")
            if not rows:
                print("  no valid rows")
                continue

            _print_seed_table(rows)
            print()

            flip_rows = [r for r in rows if r.flipped]
            flip_seeds = [r.seed for r in flip_rows]
            print(f"  flip seeds: {flip_seeds if flip_seeds else '[]'}")
            pur_delta, grav_delta, reach_delta, support_delta, core_delta, flip_frac = _summary(rows)
            print(
                f"  summary deltas: pur={pur_delta:+.4f}, grav={grav_delta:+.4f}, "
                f"reach={reach_delta:+.4f}, support={support_delta:+.4f}, core={core_delta:+.1f}"
            )
            print(f"  flip fraction: {flip_frac:.2f}")
            _print_flip_neighbors(rows)
            print()

    print("=" * 110)
    print("INTERPRETATION")
    print("  If flip seeds cluster around weaker support/core metrics than nearby non-flips,")
    print("  the gravity fragility is a reproducible subpopulation effect, not a pure mean artifact.")
    print("  If flip seeds do not separate structurally, the remaining explanation is finer")
    print("  routing/cancellation structure within the surviving mass-coupled channels.")
    print("=" * 110)


if __name__ == "__main__":
    main()
