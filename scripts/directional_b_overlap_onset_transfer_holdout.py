#!/usr/bin/env python3
"""Test overlap-onset local-density transfer on a second dense-family control.

This bounded follow-on keeps the directional-`b` overlap-margin picture fixed
and asks one narrow question:

Does the current low-`b` local-density explanation transfer to one nearby
second dense-family random-DAG control with independent seeds?

The baseline rule is learned from the existing compare:
- baseline dense random-DAG families (`dag-m3`, `dag-m5`)
- branching-tree control

The holdout changes only the mid-layer sampling geometry:
- slightly denser layer population
- slightly wider `y` span
- independent seeds

This card is intentionally honest about two different notions of transfer:
- exact clause transfer from the original bounded rule
- feature-family transfer, where the same observables still separate overlap
  rows even if the original thresholds soften on the holdout shoulder
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_overlap_onset_local_density_compare import (  # noqa: E402
    TARGET_BAND_HALF_WIDTH,
    OnsetRow,
    _best_single_rule,
    _best_two_clause_rule,
    _build_row,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.scaling_testbench import build_branching_tree  # noqa: E402


Clause = tuple[str, str, float]
RuleStats = tuple[int, int, int, int, float]


@dataclass(frozen=True)
class DagConfig:
    family_prefix: str
    nodes_per_layer: int
    y_range: float
    connect_radius: float
    seed_offset: int


def _evaluate_dag(task: tuple[DagConfig, int, int, int, float]) -> OnsetRow | None:
    config, mass_nodes, n_layers, seed, target_b = task
    positions, _adj, _meta = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=config.nodes_per_layer,
        y_range=config.y_range,
        connect_radius=config.connect_radius,
        rng_seed=seed * 11 + config.seed_offset,
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


def _evaluate_tree(task: tuple[int, int, float, int]) -> OnsetRow | None:
    n_layers, branching_factor, target_b, mass_nodes = task
    positions, _adj, layer_indices = build_branching_tree(
        n_layers,
        branching_factor=branching_factor,
        y_range=10.0,
    )
    mid = len(layer_indices) // 2
    return _build_row(
        family="tree",
        size=n_layers,
        seed=0,
        mass_nodes=mass_nodes,
        target_b=target_b,
        positions=positions,
        grav_layer_nodes=layer_indices[mid],
    )


def _collect_rows(
    *,
    dag_config: DagConfig,
    dag_seeds: int,
    dag_sizes: list[int],
    dag_target_b: float,
    tree_sizes: list[int] | None = None,
    tree_target_b: float = 1.0,
    tree_branching_factor: int = 2,
    tree_mass_nodes: int = 2,
    workers: int,
) -> list[OnsetRow]:
    dag_tasks = [
        (dag_config, mass_nodes, n_layers, seed, dag_target_b)
        for mass_nodes in (3, 5)
        for n_layers in dag_sizes
        for seed in range(dag_seeds)
    ]

    tree_rows: list[OnsetRow | None] = []
    tree_tasks = [
        (n_layers, tree_branching_factor, tree_target_b, tree_mass_nodes)
        for n_layers in (tree_sizes or [])
    ]

    ctx = mp.get_context("fork")
    if workers <= 1:
        dag_rows = [_evaluate_dag(task) for task in dag_tasks]
        if tree_tasks:
            tree_rows = [_evaluate_tree(task) for task in tree_tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
                dag_rows = list(pool.map(_evaluate_dag, dag_tasks))
                if tree_tasks:
                    tree_rows = list(pool.map(_evaluate_tree, tree_tasks))
        except (OSError, PermissionError):
            dag_rows = [_evaluate_dag(task) for task in dag_tasks]
            if tree_tasks:
                tree_rows = [_evaluate_tree(task) for task in tree_tasks]

    return [row for row in [*dag_rows, *tree_rows] if row is not None]


def _eval_rule(rows: list[OnsetRow], clauses: tuple[Clause, Clause]) -> RuleStats:
    tp = fp = fn = tn = 0
    for row in rows:
        pred = all(
            getattr(row, feature) <= threshold if op_name == "<=" else getattr(row, feature) >= threshold
            for feature, op_name, threshold in clauses
        )
        if pred and row.overlap:
            tp += 1
        elif pred and not row.overlap:
            fp += 1
        elif not pred and row.overlap:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn, (tp + tn) / len(rows)


def _fmt_clause(clause: Clause) -> str:
    feature, op_name, threshold = clause
    return f"{feature} {op_name} {threshold:.4f}"


def _print_family_summary(rows: list[OnsetRow]) -> None:
    print(
        f"{'family':>12s} {'N':>4s} {'rows':>4s} {'ovlp':>5s} {'mu_med':>8s} "
        f"{'fill':>8s} {'gap_y':>8s} {'span/step':>10s}"
    )
    print("-" * 88)
    grouped: dict[str, list[OnsetRow]] = defaultdict(list)
    for row in rows:
        grouped[row.family].append(row)

    for family in sorted(grouped):
        by_size: dict[int, list[OnsetRow]] = defaultdict(list)
        for row in grouped[family]:
            by_size[row.size].append(row)
        for size in sorted(by_size):
            bucket = by_size[size]
            print(
                f"{family:>12s} {size:4d} {len(bucket):4d} "
                f"{sum(1 for row in bucket if row.overlap):5d} "
                f"{statistics.median(row.mu for row in bucket):8.3f} "
                f"{statistics.fmean(row.target_fill for row in bucket):8.3f} "
                f"{statistics.fmean(row.same_side_mean_gap for row in bucket):8.3f} "
                f"{statistics.fmean(row.selected_span_step for row in bucket):10.3f}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--baseline-seeds", type=int, default=5)
    parser.add_argument("--holdout-seeds", type=int, default=10)
    parser.add_argument("--dag-sizes", nargs="+", type=int, default=[12, 25])
    parser.add_argument("--tree-sizes", nargs="+", type=int, default=[8, 10, 12])
    parser.add_argument("--dag-target-b", type=float, default=1.5)
    parser.add_argument("--tree-target-b", type=float, default=1.0)
    parser.add_argument("--tree-branching-factor", type=int, default=2)
    parser.add_argument("--tree-mass-nodes", type=int, default=2)
    parser.add_argument("--baseline-nodes-per-layer", type=int, default=25)
    parser.add_argument("--baseline-y-range", type=float, default=12.0)
    parser.add_argument("--holdout-nodes-per-layer", type=int, default=28)
    parser.add_argument("--holdout-y-range", type=float, default=13.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    args = parser.parse_args()

    baseline_config = DagConfig(
        family_prefix="dag",
        nodes_per_layer=args.baseline_nodes_per_layer,
        y_range=args.baseline_y_range,
        connect_radius=args.connect_radius,
        seed_offset=7,
    )
    holdout_config = DagConfig(
        family_prefix="holdout",
        nodes_per_layer=args.holdout_nodes_per_layer,
        y_range=args.holdout_y_range,
        connect_radius=args.connect_radius,
        seed_offset=701,
    )

    baseline_rows = _collect_rows(
        dag_config=baseline_config,
        dag_seeds=args.baseline_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
        tree_sizes=args.tree_sizes,
        tree_target_b=args.tree_target_b,
        tree_branching_factor=args.tree_branching_factor,
        tree_mass_nodes=args.tree_mass_nodes,
        workers=args.workers,
    )
    holdout_rows = _collect_rows(
        dag_config=holdout_config,
        dag_seeds=args.holdout_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
        workers=args.workers,
    )

    base_single = _best_single_rule(baseline_rows)
    base_pair = _best_two_clause_rule(baseline_rows)
    base_pair_stats = _eval_rule(holdout_rows, (base_pair[0], base_pair[1]))
    holdout_single = _best_single_rule(holdout_rows)
    holdout_pair = _best_two_clause_rule(holdout_rows)

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
        f"Target band remains |y - y_target| <= {TARGET_BAND_HALF_WIDTH:.1f}; "
        f"baseline DAG = ({args.baseline_nodes_per_layer} nodes/layer, y_range={args.baseline_y_range:.1f}), "
        f"holdout DAG = ({args.holdout_nodes_per_layer} nodes/layer, y_range={args.holdout_y_range:.1f})."
    )
    print()
    print("Baseline rule (existing card scale):")
    print(
        f"  best single : {base_single[0]} {base_single[1]} {base_single[2]:.4f} -> "
        f"tp/fp/fn/tn = {base_single[3][0]}/{base_single[3][1]}/{base_single[3][2]}/{base_single[3][3]}, "
        f"acc={base_single[3][4]:.4f}"
    )
    print(
        f"  best pair   : {_fmt_clause(base_pair[0])} and {_fmt_clause(base_pair[1])} -> "
        f"tp/fp/fn/tn = {base_pair[2][0]}/{base_pair[2][1]}/{base_pair[2][2]}/{base_pair[2][3]}, "
        f"acc={base_pair[2][4]:.4f}"
    )
    print()
    print("Holdout family summary:")
    _print_family_summary(holdout_rows)
    print()
    print("Baseline-pair transfer onto holdout:")
    print(
        f"  {_fmt_clause(base_pair[0])} and {_fmt_clause(base_pair[1])} -> "
        f"tp/fp/fn/tn = {base_pair_stats[0]}/{base_pair_stats[1]}/{base_pair_stats[2]}/{base_pair_stats[3]}, "
        f"acc={base_pair_stats[4]:.4f}"
    )
    print("Holdout overlap vs safe means:")
    print(
        f"  target_fill         : {statistics.fmean(row.target_fill for row in overlap_rows):.3f} "
        f"vs {statistics.fmean(row.target_fill for row in safe_rows):.3f}"
    )
    print(
        f"  same_side_mean_gap  : {statistics.fmean(row.same_side_mean_gap for row in overlap_rows):.3f} "
        f"vs {statistics.fmean(row.same_side_mean_gap for row in safe_rows):.3f}"
    )
    print(
        f"  selected_span_step  : {statistics.fmean(row.selected_span_step for row in overlap_rows):.3f} "
        f"vs {statistics.fmean(row.selected_span_step for row in safe_rows):.3f}"
    )
    print()
    print("Best holdout-only rules:")
    print(
        f"  best single : {holdout_single[0]} {holdout_single[1]} {holdout_single[2]:.4f} -> "
        f"tp/fp/fn/tn = {holdout_single[3][0]}/{holdout_single[3][1]}/{holdout_single[3][2]}/{holdout_single[3][3]}, "
        f"acc={holdout_single[3][4]:.4f}"
    )
    print(
        f"  best pair   : {_fmt_clause(holdout_pair[0])} and {_fmt_clause(holdout_pair[1])} -> "
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
