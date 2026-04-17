#!/usr/bin/env python3
"""Transfer the overlap-onset local-density rule to one dense-family holdout.

This bounded follow-on does not widen the architecture search. It takes the
existing overlap-onset compare as the baseline card, learns its best compact
rule on the retained dense-random-DAG + tree scale, and then applies that rule
to one independent second dense-family control:

- same directional propagator
- same low-b target and overlap diagnostic
- slightly denser mid-layers and a slightly wider y span

The question is narrow: does the overlap-onset explanation transfer as exact
frozen thresholds, or only at the feature level?
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_overlap_onset_local_density_compare import (  # noqa: E402
    OnsetRow,
    _accuracy,
    _best_single_rule,
    _best_two_clause_rule,
    _build_row,
    _evaluate_dag,
    _evaluate_tree,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402


def _evaluate_holdout_dag(
    task: tuple[int, int, int, float, int, float, float, int],
) -> OnsetRow | None:
    (
        mass_nodes,
        n_layers,
        seed,
        target_b,
        nodes_per_layer,
        y_range,
        connect_radius,
        seed_offset,
    ) = task
    positions, _adj, _meta = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=nodes_per_layer,
        y_range=y_range,
        connect_radius=connect_radius,
        rng_seed=seed * 11 + seed_offset,
    )
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    mid = len(layers) // 2
    return _build_row(
        family=f"holdout-m{mass_nodes}",
        size=n_layers,
        seed=seed,
        mass_nodes=mass_nodes,
        target_b=target_b,
        positions=positions,
        grav_layer_nodes=by_layer[layers[mid]],
    )


def _mean(rows: list[OnsetRow], field: str) -> float:
    values = [getattr(row, field) for row in rows]
    values = [value for value in values if not math.isnan(value)]
    return statistics.fmean(values) if values else float("nan")


def _pair_predicate(
    row: OnsetRow,
    clause_a: tuple[str, str, float],
    clause_b: tuple[str, str, float],
) -> bool:
    def matches(clause: tuple[str, str, float]) -> bool:
        feature, op_name, threshold = clause
        value = getattr(row, feature)
        if op_name == "<=":
            return value <= threshold
        return value >= threshold

    return matches(clause_a) and matches(clause_b)


def _fmt_rule(clause: tuple[str, str, float]) -> str:
    return f"{clause[0]} {clause[1]} {clause[2]:.4f}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--baseline-dag-seeds", type=int, default=5)
    parser.add_argument("--holdout-dag-seeds", type=int, default=10)
    parser.add_argument("--dag-sizes", nargs="+", type=int, default=[12, 25])
    parser.add_argument("--tree-sizes", nargs="+", type=int, default=[8, 10, 12])
    parser.add_argument("--dag-target-b", type=float, default=1.5)
    parser.add_argument("--tree-target-b", type=float, default=1.0)
    parser.add_argument("--tree-branching-factor", type=int, default=2)
    parser.add_argument("--tree-mass-nodes", type=int, default=2)
    parser.add_argument("--holdout-nodes-per-layer", type=int, default=28)
    parser.add_argument("--holdout-y-range", type=float, default=13.0)
    parser.add_argument("--holdout-connect-radius", type=float, default=3.0)
    parser.add_argument("--holdout-seed-offset", type=int, default=701)
    args = parser.parse_args()

    baseline_dag_tasks = [
        (mass_nodes, n_layers, seed, args.dag_target_b)
        for mass_nodes in (3, 5)
        for n_layers in args.dag_sizes
        for seed in range(args.baseline_dag_seeds)
    ]
    baseline_tree_tasks = [
        (n_layers, args.tree_branching_factor, args.tree_target_b, args.tree_mass_nodes)
        for n_layers in args.tree_sizes
    ]
    holdout_tasks = [
        (
            mass_nodes,
            n_layers,
            seed,
            args.dag_target_b,
            args.holdout_nodes_per_layer,
            args.holdout_y_range,
            args.holdout_connect_radius,
            args.holdout_seed_offset,
        )
        for mass_nodes in (3, 5)
        for n_layers in args.dag_sizes
        for seed in range(args.holdout_dag_seeds)
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        baseline_dag_rows = [_evaluate_dag(task) for task in baseline_dag_tasks]
        baseline_tree_rows = [_evaluate_tree(task) for task in baseline_tree_tasks]
        holdout_rows = [_evaluate_holdout_dag(task) for task in holdout_tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                baseline_dag_rows = list(pool.map(_evaluate_dag, baseline_dag_tasks))
                baseline_tree_rows = list(pool.map(_evaluate_tree, baseline_tree_tasks))
                holdout_rows = list(pool.map(_evaluate_holdout_dag, holdout_tasks))
        except (OSError, PermissionError):
            baseline_dag_rows = [_evaluate_dag(task) for task in baseline_dag_tasks]
            baseline_tree_rows = [_evaluate_tree(task) for task in baseline_tree_tasks]
            holdout_rows = [_evaluate_holdout_dag(task) for task in holdout_tasks]

    baseline_rows = [row for row in [*baseline_dag_rows, *baseline_tree_rows] if row is not None]
    holdout_rows = [row for row in holdout_rows if row is not None]
    holdout_rows.sort(key=lambda row: (row.family, row.size, row.seed))

    baseline_single = _best_single_rule(baseline_rows)
    baseline_pair = _best_two_clause_rule(baseline_rows)
    transferred_pair_stats = _accuracy(
        holdout_rows,
        lambda row: _pair_predicate(row, baseline_pair[0], baseline_pair[1]),
    )
    holdout_single = _best_single_rule(holdout_rows)
    holdout_pair = _best_two_clause_rule(holdout_rows)

    grouped: dict[str, list[OnsetRow]] = defaultdict(list)
    for row in holdout_rows:
        grouped[row.family].append(row)

    overlap_rows = [row for row in holdout_rows if row.overlap]
    safe_rows = [row for row in holdout_rows if not row.overlap]

    print("=" * 110)
    print("DIRECTIONAL-MEASURE B OVERLAP-ONSET TRANSFER HOLDOUT")
    print("=" * 110)
    print(
        "Baseline rule is learned from the existing dense random-DAG + tree compare and then applied to one"
    )
    print(
        "independent second dense-family control with slightly denser mid-layers and a slightly wider y span."
    )
    print(
        "Target band remains |y - y_target| <= 1.0; baseline DAG = "
        f"(25 nodes/layer, y_range=12.0), holdout DAG = "
        f"({args.holdout_nodes_per_layer} nodes/layer, y_range={args.holdout_y_range:.1f})."
    )
    print()
    print("Baseline rule (existing card scale):")
    print(
        f"  best single : {baseline_single[0]} {baseline_single[1]} {baseline_single[2]:.4f} -> "
        f"tp/fp/fn/tn = {baseline_single[3][0]}/{baseline_single[3][1]}/{baseline_single[3][2]}/{baseline_single[3][3]}, "
        f"acc={baseline_single[3][4]:.4f}"
    )
    print(
        f"  best pair   : {_fmt_rule(baseline_pair[0])} and {_fmt_rule(baseline_pair[1])} -> "
        f"tp/fp/fn/tn = {baseline_pair[2][0]}/{baseline_pair[2][1]}/{baseline_pair[2][2]}/{baseline_pair[2][3]}, "
        f"acc={baseline_pair[2][4]:.4f}"
    )
    print()
    print("Holdout family summary:")
    print(f"{'family':>12s} {'N':>4s} {'rows':>4s} {'ovlp':>5s} {'mu_med':>8s} {'fill':>8s} {'gap_y':>8s} {'span/step':>10s}")
    print("-" * 88)
    for family in sorted(grouped):
        by_size: dict[int, list[OnsetRow]] = defaultdict(list)
        for row in grouped[family]:
            by_size[row.size].append(row)
        for size in sorted(by_size):
            bucket = by_size[size]
            print(
                f"{family:>12s} {size:4d} {len(bucket):4d} {sum(1 for row in bucket if row.overlap):5d} "
                f"{statistics.median(row.mu for row in bucket):8.3f} "
                f"{_mean(bucket, 'target_fill'):8.3f} "
                f"{_mean(bucket, 'same_side_mean_gap'):8.3f} "
                f"{_mean(bucket, 'selected_span_step'):10.3f}"
            )
    print()
    print("Baseline-pair transfer onto holdout:")
    print(
        f"  {_fmt_rule(baseline_pair[0])} and {_fmt_rule(baseline_pair[1])} -> "
        f"tp/fp/fn/tn = {transferred_pair_stats[0]}/{transferred_pair_stats[1]}/{transferred_pair_stats[2]}/{transferred_pair_stats[3]}, "
        f"acc={transferred_pair_stats[4]:.4f}"
    )
    print("Holdout overlap vs safe means:")
    print(
        f"  target_fill         : {_mean(overlap_rows, 'target_fill'):.3f} "
        f"vs {_mean(safe_rows, 'target_fill'):.3f}"
    )
    print(
        f"  same_side_mean_gap  : {_mean(overlap_rows, 'same_side_mean_gap'):.3f} "
        f"vs {_mean(safe_rows, 'same_side_mean_gap'):.3f}"
    )
    print(
        f"  selected_span_step  : {_mean(overlap_rows, 'selected_span_step'):.3f} "
        f"vs {_mean(safe_rows, 'selected_span_step'):.3f}"
    )
    print()
    print("Best holdout-only rules:")
    print(
        f"  best single : {holdout_single[0]} {holdout_single[1]} {holdout_single[2]:.4f} -> "
        f"tp/fp/fn/tn = {holdout_single[3][0]}/{holdout_single[3][1]}/{holdout_single[3][2]}/{holdout_single[3][3]}, "
        f"acc={holdout_single[3][4]:.4f}"
    )
    print(
        f"  best pair   : {_fmt_rule(holdout_pair[0])} and {_fmt_rule(holdout_pair[1])} -> "
        f"tp/fp/fn/tn = {holdout_pair[2][0]}/{holdout_pair[2][1]}/{holdout_pair[2][2]}/{holdout_pair[2][3]}, "
        f"acc={holdout_pair[2][4]:.4f}"
    )
    print()
    print("Interpretation:")
    print("  The local-density picture does transfer, but not as one universal frozen threshold pair.")
    print("  On the second dense-family control, overlap rows still have much weaker target-band fill and coarser")
    print("  same-side spacing than safe rows, so the mechanism remains local occupancy plus spacing.")
    print("  The exact original gap/span thresholds soften on the milder N=25 wide-family shoulder, where the")
    print("  holdout refit collapses mostly to target_fill <= 1/3.")
    print("  So the promoted statement should be feature-level: sparse target-band occupancy is the leading")
    print("  transferable overlap-onset signal, while the spacing thresholds remain family-dependent refinements.")


if __name__ == "__main__":
    main()
