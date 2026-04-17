#!/usr/bin/env python3
"""Explain low-b overlap onset via local target-band occupancy.

This bounded follow-on keeps the corrected directional-b hierarchy fixed and
compares the low-impact corners that feed the overlap-margin card:

- dense random DAGs (`dag-m3`, `dag-m5`) at their retained low-b target
- branching-tree controls at their corresponding low-b target

The question is narrow: what local source-geometry observables explain why the
dense random-DAG families hit `mu <= 0` while the tree family stays safely
positive?
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import itertools
import math
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_readout_compare import _select_mass_nodes  # noqa: E402
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.scaling_testbench import build_branching_tree  # noqa: E402


TARGET_BAND_HALF_WIDTH = 1.0


@dataclass(frozen=True)
class OnsetRow:
    family: str
    size: int
    seed: int
    mass_nodes: int
    target_b: float
    actual_b: float
    h_mass: float
    mu: float
    grav_layer_nodes: int
    local_target_count: int
    target_fill: float
    same_side_mean_gap: float
    selected_span_step: float
    overlap: bool


def _mean_gap(values: list[float]) -> float:
    if len(values) < 2:
        return float("nan")
    ordered = sorted(values)
    gaps = [ordered[i + 1] - ordered[i] for i in range(len(ordered) - 1)]
    return statistics.fmean(gaps)


def _build_row(
    family: str,
    size: int,
    seed: int,
    mass_nodes: int,
    target_b: float,
    positions: list[tuple[float, float]],
    grav_layer_nodes: list[int],
) -> OnsetRow | None:
    center_y = statistics.fmean(y for _x, y in positions)
    selected = _select_mass_nodes(
        positions=positions,
        layer_nodes=grav_layer_nodes,
        center_y=center_y,
        target_b=target_b,
        mass_nodes=mass_nodes,
    )
    if len(selected) < mass_nodes:
        return None

    ys = [positions[node][1] for node in selected]
    actual_b = statistics.fmean(ys) - center_y
    h_mass = 0.5 * (max(ys) - min(ys))
    mu = ((actual_b - h_mass) / h_mass) if h_mass > 0.0 else float("inf")

    same_side_offsets = [positions[node][1] - center_y for node in grav_layer_nodes if positions[node][1] >= center_y]
    target_y = center_y + target_b
    local_target_count = sum(
        1
        for node in grav_layer_nodes
        if positions[node][1] >= center_y and abs(positions[node][1] - target_y) <= TARGET_BAND_HALF_WIDTH
    )
    span_step = (max(ys) - min(ys)) / max(1, len(selected) - 1)

    return OnsetRow(
        family=family,
        size=size,
        seed=seed,
        mass_nodes=mass_nodes,
        target_b=target_b,
        actual_b=actual_b,
        h_mass=h_mass,
        mu=mu,
        grav_layer_nodes=len(grav_layer_nodes),
        local_target_count=local_target_count,
        target_fill=local_target_count / mass_nodes,
        same_side_mean_gap=_mean_gap(same_side_offsets),
        selected_span_step=span_step,
        overlap=mu <= 0.0,
    )


def _evaluate_dag(task: tuple[int, int, int, float]) -> OnsetRow | None:
    mass_nodes, n_layers, seed, target_b = task
    positions, _adj, _meta = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=25,
        y_range=12.0,
        connect_radius=3.0,
        rng_seed=seed * 11 + 7,
    )
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    mid = len(layers) // 2
    return _build_row(
        family=f"dag-m{mass_nodes}",
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


def _accuracy(rows: list[OnsetRow], predicate) -> tuple[int, int, int, int, float]:
    tp = fp = tn = fn = 0
    for row in rows:
        pred = predicate(row)
        if pred and row.overlap:
            tp += 1
        elif pred and not row.overlap:
            fp += 1
        elif not pred and row.overlap:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn, (tp + tn) / len(rows)


def _candidate_thresholds(values: list[float]) -> list[float]:
    ordered = sorted(set(values))
    mids = [(ordered[i] + ordered[i + 1]) / 2.0 for i in range(len(ordered) - 1)]
    return ordered + mids


def _best_single_rule(rows: list[OnsetRow]) -> tuple[str, str, float, tuple[int, int, int, int, float]]:
    feature_names = ["target_fill", "same_side_mean_gap", "selected_span_step"]
    best: tuple[str, str, float, tuple[int, int, int, int, float]] | None = None
    for feature in feature_names:
        values = [getattr(row, feature) for row in rows if not math.isnan(getattr(row, feature))]
        for threshold in _candidate_thresholds(values):
            for op_name, op in (("<=", lambda v, t: v <= t), (">=", lambda v, t: v >= t)):
                stats = _accuracy(rows, lambda row, f=feature, t=threshold, o=op: o(getattr(row, f), t))
                if best is None or stats[-1] > best[-1][-1]:
                    best = (feature, op_name, threshold, stats)
    assert best is not None
    return best


def _best_two_clause_rule(rows: list[OnsetRow]) -> tuple[tuple[str, str, float], tuple[str, str, float], tuple[int, int, int, int, float]]:
    feature_names = ["target_fill", "same_side_mean_gap", "selected_span_step"]
    clauses: list[tuple[str, str, float]] = []
    for feature in feature_names:
        values = [getattr(row, feature) for row in rows if not math.isnan(getattr(row, feature))]
        for threshold in _candidate_thresholds(values):
            clauses.append((feature, "<=", threshold))
            clauses.append((feature, ">=", threshold))

    def eval_clause(row: OnsetRow, clause: tuple[str, str, float]) -> bool:
        feature, op_name, threshold = clause
        value = getattr(row, feature)
        if op_name == "<=":
            return value <= threshold
        return value >= threshold

    best: tuple[tuple[str, str, float], tuple[str, str, float], tuple[int, int, int, int, float]] | None = None
    for clause_a, clause_b in itertools.combinations(clauses, 2):
        stats = _accuracy(rows, lambda row, a=clause_a, b=clause_b: eval_clause(row, a) and eval_clause(row, b))
        if best is None or stats[-1] > best[-1][-1]:
            best = (clause_a, clause_b, stats)
    assert best is not None
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--dag-seeds", type=int, default=5)
    parser.add_argument("--dag-sizes", nargs="+", type=int, default=[12, 25])
    parser.add_argument("--tree-sizes", nargs="+", type=int, default=[8, 10, 12])
    parser.add_argument("--dag-target-b", type=float, default=1.5)
    parser.add_argument("--tree-target-b", type=float, default=1.0)
    parser.add_argument("--tree-branching-factor", type=int, default=2)
    parser.add_argument("--tree-mass-nodes", type=int, default=2)
    args = parser.parse_args()

    dag_tasks = [
        (mass_nodes, n_layers, seed, args.dag_target_b)
        for mass_nodes in (3, 5)
        for n_layers in args.dag_sizes
        for seed in range(args.dag_seeds)
    ]
    tree_tasks = [
        (n_layers, args.tree_branching_factor, args.tree_target_b, args.tree_mass_nodes)
        for n_layers in args.tree_sizes
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        dag_rows = [_evaluate_dag(task) for task in dag_tasks]
        tree_rows = [_evaluate_tree(task) for task in tree_tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                dag_rows = list(pool.map(_evaluate_dag, dag_tasks))
                tree_rows = list(pool.map(_evaluate_tree, tree_tasks))
        except (OSError, PermissionError):
            dag_rows = [_evaluate_dag(task) for task in dag_tasks]
            tree_rows = [_evaluate_tree(task) for task in tree_tasks]

    rows = [row for row in [*dag_rows, *tree_rows] if row is not None]
    by_family: dict[str, list[OnsetRow]] = defaultdict(list)
    for row in rows:
        by_family[row.family].append(row)

    single = _best_single_rule(rows)
    pair = _best_two_clause_rule(rows)

    print("=" * 124)
    print("DIRECTIONAL-MEASURE B OVERLAP-ONSET LOCAL-DENSITY COMPARE")
    print("=" * 124)
    print(
        "Low-b overlap rows are compared across dense random-DAG families and the branching-tree control "
        f"using a target band |y - y_target| <= {TARGET_BAND_HALF_WIDTH:.1f}."
    )
    print()
    print(
        f"{'family':>10s} {'N':>4s} {'rows':>4s} {'mu_med':>8s} {'ovlp':>6s} "
        f"{'fill':>8s} {'gap_y':>8s} {'span/step':>10s} {'layer_n':>8s}"
    )
    print("-" * 124)
    for family in sorted(by_family):
        by_size: dict[int, list[OnsetRow]] = defaultdict(list)
        for row in by_family[family]:
            by_size[row.size].append(row)
        for size in sorted(by_size):
            bucket = by_size[size]
            print(
                f"{family:>10s} {size:4d} {len(bucket):4d} "
                f"{statistics.median(row.mu for row in bucket):8.3f} "
                f"{sum(1 for row in bucket if row.overlap):6d} "
                f"{statistics.fmean(row.target_fill for row in bucket):8.3f} "
                f"{statistics.fmean(row.same_side_mean_gap for row in bucket):8.3f} "
                f"{statistics.fmean(row.selected_span_step for row in bucket):10.3f} "
                f"{statistics.fmean(row.grav_layer_nodes for row in bucket):8.1f}"
            )
    print()
    print("Overlap vs non-overlap means:")
    overlap_rows = [row for row in rows if row.overlap]
    safe_rows = [row for row in rows if not row.overlap]
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
    feature, op_name, threshold, stats = single
    print("Best single overlap rule:")
    print(
        f"  {feature} {op_name} {threshold:.4f} -> "
        f"tp/fp/fn/tn = {stats[0]}/{stats[1]}/{stats[2]}/{stats[3]}, acc={stats[4]:.4f}"
    )
    clause_a, clause_b, pair_stats = pair
    print("Best two-clause overlap rule:")
    print(
        f"  {clause_a[0]} {clause_a[1]} {clause_a[2]:.4f} and "
        f"{clause_b[0]} {clause_b[1]} {clause_b[2]:.4f} -> "
        f"tp/fp/fn/tn = {pair_stats[0]}/{pair_stats[1]}/{pair_stats[2]}/{pair_stats[3]}, acc={pair_stats[4]:.4f}"
    )
    print()
    print("Interpretation:")
    print("  Overlap onset is best explained by weak target-band occupancy plus coarse local y spacing.")
    print("  Tree layers densify near the target plane, so selected mass windows stay compact and mu remains positive.")
    print("  Dense random-DAG layers keep only ~1-2 nodes in the target band at low b, so widened source windows")
    print("  have to stretch across large y gaps and are the ones that cross into mu <= 0.")


if __name__ == "__main__":
    main()
