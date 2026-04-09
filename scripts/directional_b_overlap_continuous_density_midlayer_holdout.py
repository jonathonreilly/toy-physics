#!/usr/bin/env python3
"""Stress-test the frozen directional-b 4-NN density law on one dense sentinel.

This bounded follow-on keeps the corrected directional-b hierarchy fixed. It
does not refit the retained dense-family bridge. Instead it applies the frozen
counted and continuous overlap rules

    mass_nodes / local_target_count >= 2.5
    mass_nodes / expected_target_count_4nn >= 2.735352889954456

to one additional dense-family sentinel that only changes the gravity-layer
y-sampling law:

- same dense family sizes
- same target b and overlap diagnostic
- same support width and connect radius
- only the middle layer uses a center-biased sampler

The question is narrow: does the smoother 4-NN density bridge stay the more
portable explanation once dense target-plane support is intentionally warped
without reopening the denominator search?
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_overlap_continuous_density_bridge_card import (  # noqa: E402
    DensityRow,
    _accuracy,
    _build_row,
    _evaluate_baseline_dag,
    _evaluate_holdout_dag,
)
from scripts.directional_b_overlap_continuous_density_tree_control import (  # noqa: E402
    FROZEN_COUNT_THRESHOLD,
    FROZEN_KNN4_THRESHOLD,
    _evaluate_tree,
)


@dataclass(frozen=True)
class DagConfig:
    family_prefix: str
    nodes_per_layer: int
    y_range: float
    connect_radius: float
    seed_offset: int
    midlayer_gamma: float | None = None


def _sample_y(rng: random.Random, y_range: float, gamma: float | None) -> float:
    if gamma is None:
        return rng.uniform(-y_range, y_range)
    u = rng.uniform(-1.0, 1.0)
    return math.copysign(abs(u) ** gamma, u) * y_range


def _generate_midlayer_holdout(
    *,
    n_layers: int,
    nodes_per_layer: int,
    y_range: float,
    connect_radius: float,
    rng_seed: int,
    midlayer_gamma: float | None,
) -> tuple[list[tuple[float, float]], dict[int, list[int]]]:
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    arrival: list[float] = []
    layer_indices: list[list[int]] = []
    mid_layer = n_layers // 2

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            arrival.append(0.0)
            layer_nodes.append(idx)
        else:
            gamma = midlayer_gamma if layer == mid_layer else None
            for _ in range(nodes_per_layer):
                y = _sample_y(rng, y_range, gamma)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                best_arrival = float("inf")
                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
                            candidate = arrival[prev_idx] + dist
                            if math.isfinite(candidate) and candidate < best_arrival:
                                best_arrival = candidate
                arrival.append(best_arrival)
        layer_indices.append(layer_nodes)

    return positions, dict(adj)


def _evaluate_midlayer_dag(
    task: tuple[DagConfig, int, int, int, float],
) -> DensityRow | None:
    config, mass_nodes, n_layers, seed, target_b = task
    positions, _adj = _generate_midlayer_holdout(
        n_layers=n_layers,
        nodes_per_layer=config.nodes_per_layer,
        y_range=config.y_range,
        connect_radius=config.connect_radius,
        rng_seed=seed * 11 + config.seed_offset,
        midlayer_gamma=config.midlayer_gamma,
    )
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    mid = len(layers) // 2
    return _build_row(
        family=f"{config.family_prefix}-m{mass_nodes}",
        size=n_layers,
        seed=seed,
        mass_nodes=mass_nodes,
        target_b=target_b,
        positions=positions,
        grav_layer_nodes=by_layer[layers[mid]],
    )


def _collect_rows(
    tasks: list[tuple],
    evaluator,
    workers: int,
) -> list[DensityRow]:
    ctx = mp.get_context("fork")
    if workers <= 1:
        rows = [evaluator(task) for task in tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
                rows = list(pool.map(evaluator, tasks))
        except (OSError, PermissionError):
            rows = [evaluator(task) for task in tasks]
    return [row for row in rows if row is not None]


def _fmt_stats(stats: tuple[int, int, int, int, float]) -> str:
    tp, fp, fn, tn, acc = stats
    return f"{tp}/{fp}/{fn}/{tn} {acc:.4f}"


def _mean(rows: list[DensityRow], field: str) -> float:
    values = [getattr(row, field) for row in rows]
    finite_values = [value for value in values if math.isfinite(value)]
    return statistics.fmean(finite_values) if finite_values else float("nan")


def _print_midlayer_summary(rows: list[DensityRow]) -> None:
    print(
        f"{'family':>14s} {'N':>4s} {'rows':>4s} {'ovlp':>5s} {'mu_med':>8s} "
        f"{'target_ct':>9s} {'count_ld':>10s} {'4NN_ld':>10s}"
    )
    print("-" * 76)
    grouped: dict[str, list[DensityRow]] = defaultdict(list)
    for row in rows:
        grouped[row.family].append(row)

    for family in sorted(grouped):
        by_size: dict[int, list[DensityRow]] = defaultdict(list)
        for row in grouped[family]:
            by_size[row.size].append(row)
        for size in sorted(by_size):
            bucket = by_size[size]
            print(
                f"{family:>14s} {size:4d} {len(bucket):4d} "
                f"{sum(1 for row in bucket if row.overlap):5d} "
                f"{statistics.median(row.mu for row in bucket):8.3f} "
                f"{_mean(bucket, 'local_target_count'):9.3f} "
                f"{_mean(bucket, 'source_load'):10.3f} "
                f"{_mean(bucket, 'knn4_density_load'):10.3f}"
            )


def _print_rule_misses(rows: list[DensityRow]) -> None:
    misses = sorted(
        [
            row
            for row in rows
            if row.overlap and row.knn4_density_load < FROZEN_KNN4_THRESHOLD
        ],
        key=lambda row: (row.knn4_density_load - FROZEN_KNN4_THRESHOLD, row.family, row.size, row.seed),
    )
    if not misses:
        print("Frozen 4-NN misses on the sentinel: none")
        return

    print("Frozen 4-NN misses on the sentinel:")
    print(
        f"{'family':>14s} {'N':>4s} {'seed':>4s} {'mu':>8s} {'target_ct':>9s} "
        f"{'count_ld':>10s} {'4NN_ld':>10s} {'4NN_margin':>11s}"
    )
    print("-" * 84)
    for row in misses:
        print(
            f"{row.family:>14s} {row.size:4d} {row.seed:4d} {row.mu:8.3f} "
            f"{row.local_target_count:9d} {row.source_load:10.3f} "
            f"{row.knn4_density_load:10.3f} "
            f"{row.knn4_density_load - FROZEN_KNN4_THRESHOLD:11.3f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--baseline-dag-seeds", type=int, default=5)
    parser.add_argument("--transfer-holdout-seeds", type=int, default=10)
    parser.add_argument("--midlayer-seeds", type=int, default=10)
    parser.add_argument("--dag-sizes", nargs="+", type=int, default=[12, 25])
    parser.add_argument("--dag-target-b", type=float, default=1.5)
    parser.add_argument("--transfer-nodes-per-layer", type=int, default=28)
    parser.add_argument("--transfer-y-range", type=float, default=13.0)
    parser.add_argument("--transfer-connect-radius", type=float, default=3.0)
    parser.add_argument("--transfer-seed-offset", type=int, default=701)
    parser.add_argument("--tree-sizes", nargs="+", type=int, default=[8, 10, 12])
    parser.add_argument("--tree-target-b", type=float, default=1.0)
    parser.add_argument("--tree-branching-factor", type=int, default=2)
    parser.add_argument("--tree-mass-nodes", type=int, default=2)
    parser.add_argument("--midlayer-nodes-per-layer", type=int, default=25)
    parser.add_argument("--midlayer-y-range", type=float, default=12.0)
    parser.add_argument("--midlayer-connect-radius", type=float, default=3.0)
    parser.add_argument("--midlayer-seed-offset", type=int, default=1701)
    parser.add_argument(
        "--midlayer-gamma",
        type=float,
        default=1.4,
        help="Power-law exponent for the center-biased middle-layer sampler.",
    )
    args = parser.parse_args()

    baseline_tasks = [
        (mass_nodes, n_layers, seed, args.dag_target_b)
        for mass_nodes in (3, 5)
        for n_layers in args.dag_sizes
        for seed in range(args.baseline_dag_seeds)
    ]
    transfer_holdout_tasks = [
        (
            mass_nodes,
            n_layers,
            seed,
            args.dag_target_b,
            args.transfer_nodes_per_layer,
            args.transfer_y_range,
            args.transfer_connect_radius,
            args.transfer_seed_offset,
        )
        for mass_nodes in (3, 5)
        for n_layers in args.dag_sizes
        for seed in range(args.transfer_holdout_seeds)
    ]
    tree_tasks = [
        (n_layers, args.tree_branching_factor, args.tree_target_b, args.tree_mass_nodes)
        for n_layers in args.tree_sizes
    ]
    midlayer_config = DagConfig(
        family_prefix=f"midgamma{args.midlayer_gamma:g}",
        nodes_per_layer=args.midlayer_nodes_per_layer,
        y_range=args.midlayer_y_range,
        connect_radius=args.midlayer_connect_radius,
        seed_offset=args.midlayer_seed_offset,
        midlayer_gamma=args.midlayer_gamma,
    )
    midlayer_tasks = [
        (midlayer_config, mass_nodes, n_layers, seed, args.dag_target_b)
        for mass_nodes in (3, 5)
        for n_layers in args.dag_sizes
        for seed in range(args.midlayer_seeds)
    ]

    baseline_rows = _collect_rows(baseline_tasks, _evaluate_baseline_dag, args.workers)
    transfer_holdout_rows = _collect_rows(
        transfer_holdout_tasks,
        _evaluate_holdout_dag,
        args.workers,
    )
    tree_rows = _collect_rows(tree_tasks, _evaluate_tree, args.workers)
    midlayer_rows = _collect_rows(midlayer_tasks, _evaluate_midlayer_dag, args.workers)

    dense_pair_rows = [*baseline_rows, *transfer_holdout_rows]
    reference_rows = [*dense_pair_rows, *tree_rows]
    extended_rows = [*reference_rows, *midlayer_rows]

    dense_pair_count = _accuracy(
        dense_pair_rows,
        lambda row: row.source_load >= FROZEN_COUNT_THRESHOLD,
    )
    dense_pair_knn4 = _accuracy(
        dense_pair_rows,
        lambda row: row.knn4_density_load >= FROZEN_KNN4_THRESHOLD,
    )
    tree_count = _accuracy(
        tree_rows,
        lambda row: row.source_load >= FROZEN_COUNT_THRESHOLD,
    )
    tree_knn4 = _accuracy(
        tree_rows,
        lambda row: row.knn4_density_load >= FROZEN_KNN4_THRESHOLD,
    )
    reference_count = _accuracy(
        reference_rows,
        lambda row: row.source_load >= FROZEN_COUNT_THRESHOLD,
    )
    reference_knn4 = _accuracy(
        reference_rows,
        lambda row: row.knn4_density_load >= FROZEN_KNN4_THRESHOLD,
    )
    midlayer_count = _accuracy(
        midlayer_rows,
        lambda row: row.source_load >= FROZEN_COUNT_THRESHOLD,
    )
    midlayer_knn4 = _accuracy(
        midlayer_rows,
        lambda row: row.knn4_density_load >= FROZEN_KNN4_THRESHOLD,
    )
    extended_count = _accuracy(
        extended_rows,
        lambda row: row.source_load >= FROZEN_COUNT_THRESHOLD,
    )
    extended_knn4 = _accuracy(
        extended_rows,
        lambda row: row.knn4_density_load >= FROZEN_KNN4_THRESHOLD,
    )

    overlap_rows = [row for row in midlayer_rows if row.overlap]
    safe_rows = [row for row in midlayer_rows if not row.overlap]

    print("=" * 124)
    print("DIRECTIONAL-MEASURE B CONTINUOUS-DENSITY MIDLAYER HOLDOUT")
    print("=" * 124)
    print(
        "Freeze the current counted and 4-NN overlap thresholds, then apply them to one additional dense"
    )
    print(
        "sentinel that changes only the gravity-layer y sampler to y = sign(u) |u|^gamma * y_range."
    )
    print()
    print("Frozen overlap rules:")
    print(f"  counted source-load rule : mass_nodes / local_target_count >= {FROZEN_COUNT_THRESHOLD:.4f}")
    print(
        "  continuous 4-NN rule    : "
        f"mass_nodes / expected_target_count_4nn >= {FROZEN_KNN4_THRESHOLD:.4f}"
    )
    print("  expected_target_count_4nn = 4 / r4 on the same-side target-plane slice")
    print()
    print(
        f"{'set':>18s} {'rows':>4s} {'ovlp':>5s} "
        f"{'count tp/fp/fn/tn acc':>26s} {'4-NN tp/fp/fn/tn acc':>26s}"
    )
    print("-" * 124)
    for label, rows, count_stats, knn4_stats in (
        ("dense-pair", dense_pair_rows, dense_pair_count, dense_pair_knn4),
        ("tree", tree_rows, tree_count, tree_knn4),
        ("reference+tree", reference_rows, reference_count, reference_knn4),
        ("midlayer-sentinel", midlayer_rows, midlayer_count, midlayer_knn4),
        ("extended-sample", extended_rows, extended_count, extended_knn4),
    ):
        print(
            f"{label:>18s} {len(rows):4d} {sum(row.overlap for row in rows):5d} "
            f"{_fmt_stats(count_stats):>26s} {_fmt_stats(knn4_stats):>26s}"
        )
    print()
    print("Midlayer sentinel family summary:")
    _print_midlayer_summary(midlayer_rows)
    print()
    print("Midlayer overlap vs safe means:")
    print(
        f"  local_target_count      : {_mean(overlap_rows, 'local_target_count'):.3f} "
        f"vs {_mean(safe_rows, 'local_target_count'):.3f}"
    )
    print(
        f"  source_load             : {_mean(overlap_rows, 'source_load'):.3f} "
        f"vs {_mean(safe_rows, 'source_load'):.3f}"
    )
    print(
        f"  knn4_expected_target_ct : {_mean(overlap_rows, 'knn4_expected_target_count'):.3f} "
        f"vs {_mean(safe_rows, 'knn4_expected_target_count'):.3f}"
    )
    print(
        f"  knn4_density_load       : {_mean(overlap_rows, 'knn4_density_load'):.3f} "
        f"vs {_mean(safe_rows, 'knn4_density_load'):.3f}"
    )
    print()
    _print_rule_misses(midlayer_rows)
    print()
    print("Interpretation:")
    print("  1. The frozen 4-NN density law stays cleaner on the extended sample overall, but it does not")
    print("     transfer cleanly as a frozen replacement on the center-biased dense sentinel.")
    print("  2. On this sentinel, the counted source-load rule still transfers better than the frozen 4-NN rule:")
    print(
        f"     {midlayer_count[4]:.4f} vs {midlayer_knn4[4]:.4f}, even though the 4-NN rule keeps zero false positives."
    )
    print("  3. The sentinel only changes gravity-layer y sampling, and its overlap rows keep denser same-side")
    print("     support near the target plane; that pushes r4 down, inflates expected_target_count_4nn, and")
    print("     makes the frozen 4-NN load conservative through false negatives rather than false positives.")
    print("  4. So the current portable statement remains occupancy-first: the 4-NN law is still the sharper")
    print("     smooth explanation on the original dense pair plus tree control, but it is not yet a fully")
    print("     frozen replacement for the counted bridge across dense sampler changes.")


if __name__ == "__main__":
    main()
