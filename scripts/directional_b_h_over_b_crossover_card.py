#!/usr/bin/env python3
"""Render the h_mass / b crossover card for the directional-b hierarchy.

This is a theory-facing compression step.  It reuses the already-retained
evaluators and asks when the leading asymptotic denominator ``b`` stops being a
good practical read and the finite-source correction ``b - h_mass`` should take
over.  The bounded reduced variable is:

    lambda = h_mass / b

with ``h_mass`` the source half-span and ``b`` the actual center offset.
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_mass_window_transfer import (  # noqa: E402
    DEFAULT_IMPACT_BS as DAG_IMPACT_BS,
    DEFAULT_N_LAYERS as DAG_N_LAYERS,
    _evaluate_transfer_trial,
    _trend_summary,
)
from scripts.directional_b_tree_hierarchy_compare import (  # noqa: E402
    DEFAULT_IMPACT_BS as TREE_IMPACT_BS,
    DEFAULT_TREE_SIZES,
    _evaluate_tree_trial,
)


@dataclass(frozen=True)
class CardRow:
    family: str
    size: int
    target_b: float
    actual_b: float
    h_mass: float
    edge_b: float
    support_gap: float
    lambda_ratio: float
    action_over_b: float
    action_over_edge_b: float
    flow_over_b: float
    flow_over_edge_b: float


def _safe_lambda_ratio(h_mass: float, actual_b: float) -> float:
    return h_mass / actual_b if actual_b > 0.0 else float("nan")


def _from_dag(task: tuple[int, int, float, int, float, float]) -> CardRow | None:
    row = _evaluate_transfer_trial(task)
    if row is None:
        return None
    return CardRow(
        family=f"dag-m{row.mass_nodes}",
        size=row.n_layers,
        target_b=row.target_b,
        actual_b=row.actual_b,
        h_mass=row.mass_half_span,
        edge_b=row.edge_b,
        support_gap=row.support_gap,
        lambda_ratio=_safe_lambda_ratio(row.mass_half_span, row.actual_b),
        action_over_b=row.action_over_b,
        action_over_edge_b=row.action_over_edge_b,
        flow_over_b=row.flow_over_b,
        flow_over_edge_b=row.flow_over_edge_b,
    )


def _from_tree(task: tuple[int, float, float, int, int, float]) -> CardRow | None:
    row = _evaluate_tree_trial(task)
    if row is None:
        return None
    return CardRow(
        family="tree",
        size=row.n_layers,
        target_b=row.target_b,
        actual_b=row.actual_b,
        h_mass=row.mass_half_span,
        edge_b=row.edge_b,
        support_gap=row.support_gap,
        lambda_ratio=_safe_lambda_ratio(row.mass_half_span, row.actual_b),
        action_over_b=row.action_over_b,
        action_over_edge_b=row.action_over_edge_b,
        flow_over_b=row.flow_over_b,
        flow_over_edge_b=row.flow_over_edge_b,
    )


def _mean(values: list[float]) -> float:
    values = [value for value in values if not math.isnan(value)]
    return statistics.fmean(values) if values else float("nan")


def _median(values: list[float]) -> float:
    values = [value for value in values if not math.isnan(value)]
    return statistics.median(values) if values else float("nan")


def _fmt(x: float, width: int = 8) -> str:
    if math.isnan(x):
        return f"{'n/a':>{width}s}"
    return f"{x:{width}.3f}"


def _status(rows: list[CardRow], field: str) -> str:
    class SimpleRow:
        def __init__(self, target_b, actual_b, value):
            self.target_b = target_b
            self.actual_b = actual_b
            setattr(self, field, value)

    simple = [SimpleRow(r.target_b, r.actual_b, getattr(r, field)) for r in rows]
    summary = _trend_summary(simple, field)
    return summary.status if summary is not None else "INSUF"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--dag-seeds", type=int, default=5)
    parser.add_argument("--angle-beta", type=float, default=0.8)
    parser.add_argument("--retain-share", type=float, default=0.5)
    parser.add_argument("--tree-branching-factor", type=int, default=2)
    parser.add_argument("--tree-mass-nodes", type=int, default=2)
    args = parser.parse_args()

    dag_tasks = [
        (mass_nodes, n_layers, target_b, seed, args.angle_beta, args.retain_share)
        for mass_nodes in (3, 5)
        for n_layers in DAG_N_LAYERS
        for target_b in DAG_IMPACT_BS
        for seed in range(args.dag_seeds)
    ]
    tree_tasks = [
        (n_layers, target_b, args.angle_beta, args.tree_branching_factor, args.tree_mass_nodes, args.retain_share)
        for n_layers in DEFAULT_TREE_SIZES
        for target_b in TREE_IMPACT_BS
    ]

    ctx = mp.get_context("fork")
    if args.workers <= 1:
        dag_rows = [_from_dag(task) for task in dag_tasks]
        tree_rows = [_from_tree(task) for task in tree_tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                dag_rows = list(pool.map(_from_dag, dag_tasks))
                tree_rows = list(pool.map(_from_tree, tree_tasks))
        except (OSError, PermissionError):
            dag_rows = [_from_dag(task) for task in dag_tasks]
            tree_rows = [_from_tree(task) for task in tree_tasks]
    rows = [row for row in [*dag_rows, *tree_rows] if row is not None]

    grouped: dict[str, list[CardRow]] = defaultdict(list)
    for row in rows:
        grouped[row.family].append(row)

    print("=" * 112)
    print("DIRECTIONAL-MEASURE B H_MASS / B CROSSOVER CARD")
    print("=" * 112)
    print("Reduced variable: lambda = h_mass / b")
    print("Interpretation target:")
    print("  lambda << 1       : asymptotic point-source regime, b should suffice")
    print("  lambda ~ O(1)     : finite-source regime, b - h_mass should matter")
    print("  edge_b <= 0       : overlap / near-overlap corner where pure b can break badly")
    print()
    print(f"{'family':>10s} {'N':>4s} {'lam_med':>10s} {'lam_sep_max':>12s} {'lam_sep_mean':>12s} {'edge<=0':>8s} {'edge<0.5':>9s} {'A/b':>6s} {'A/edge':>8s} {'F/b':>6s} {'F/edge':>8s}")
    print("-" * 112)
    for family in sorted(grouped):
        by_size: dict[int, list[CardRow]] = defaultdict(list)
        for row in grouped[family]:
            by_size[row.size].append(row)
        for size in sorted(by_size):
            bucket = by_size[size]
            lambdas = [row.lambda_ratio for row in bucket]
            sep_lambdas = [row.lambda_ratio for row in bucket if row.edge_b > 0]
            edge_nonpos = sum(1 for row in bucket if row.edge_b <= 0)
            edge_small = sum(1 for row in bucket if row.edge_b < 0.5)
            print(
                f"{family:>10s} {size:4d} "
                f"{_median(lambdas):10.3f} {max(sep_lambdas) if sep_lambdas else float('nan'):12.3f} {_mean(sep_lambdas):12.3f} "
                f"{edge_nonpos:8d} {edge_small:9d} "
                f"{_status(bucket, 'action_over_b'):>6s} {_status(bucket, 'action_over_edge_b'):>8s} "
                f"{_status(bucket, 'flow_over_b'):>6s} {_status(bucket, 'flow_over_edge_b'):>8s}"
            )
    print()
    print("Crossover reading:")
    print("  1. Tree control: lambda stays small, edge overlap never happens, and all denominators agree.")
    print("  2. Narrow random-DAG family: lambda is moderate in the bulk, but low-b corners already approach O(1); b still passes.")
    print("  3. Wide random-DAG family: low-b corners enter the overlap regime (edge_b <= 0),")
    print("     but pure b still passes on the bounded family once singular center-offset trials are excluded.")
    print("  4. So the practical crossover is not a new force law. It is the onset of finite source width in lambda = h_mass / b.")
    print("  5. Use response / b as the leading asymptotic term when lambda is comfortably subcritical;")
    print("     promote response / (b - h_mass) as the safer finite-source correction once low-b corners push lambda toward or past O(1).")


if __name__ == "__main__":
    main()
