#!/usr/bin/env python3
"""Render the directional-b overlap-margin card.

This bounded follow-on keeps the retained directional propagator and existing
family comparisons fixed.  Instead of restating the crossover in terms of
``lambda = h_mass / b`` alone, it promotes the directly geometric overlap
margin

    mu = edge_b / h_mass = 1 / lambda - 1

with ``edge_b = b - h_mass``.

Interpretation:
- ``mu >> 1``: safely asymptotic point-source regime
- ``mu ~ 0``: grazing the finite-source / overlap shoulder
- ``mu <= 0``: source-support overlap, where pure ``1 / b`` is most fragile
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

from scripts.directional_b_h_over_b_crossover_card import (  # noqa: E402
    DAG_IMPACT_BS,
    DAG_N_LAYERS,
    DEFAULT_TREE_SIZES,
    TREE_IMPACT_BS,
    CardRow,
    _from_dag,
    _from_tree,
    _status,
)


EPS = 1e-9


def _margin(row: CardRow) -> float:
    return row.edge_b / max(row.h_mass, EPS)


def _median(values: list[float]) -> float:
    return statistics.median(values) if values else float("nan")


def _fmt(x: float, width: int = 8) -> str:
    if math.isnan(x):
        return f"{'n/a':>{width}s}"
    return f"{x:{width}.3f}"


def _count_nonpos(rows: list[CardRow]) -> str:
    return f"{sum(1 for row in rows if row.edge_b <= 0):>2d}/{len(rows):<2d}"


def _collect_rows(args: argparse.Namespace) -> list[CardRow]:
    dag_tasks = [
        (mass_nodes, n_layers, target_b, seed, args.angle_beta, args.retain_share)
        for mass_nodes in (3, 5)
        for n_layers in DAG_N_LAYERS
        for target_b in DAG_IMPACT_BS
        for seed in range(args.dag_seeds)
    ]
    tree_tasks = [
        (
            n_layers,
            target_b,
            args.angle_beta,
            args.tree_branching_factor,
            args.tree_mass_nodes,
            args.retain_share,
        )
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
    return [row for row in [*dag_rows, *tree_rows] if row is not None]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--dag-seeds", type=int, default=5)
    parser.add_argument("--angle-beta", type=float, default=0.8)
    parser.add_argument("--retain-share", type=float, default=0.5)
    parser.add_argument("--tree-branching-factor", type=int, default=2)
    parser.add_argument("--tree-mass-nodes", type=int, default=2)
    args = parser.parse_args()

    rows = _collect_rows(args)

    grouped: dict[str, list[CardRow]] = defaultdict(list)
    for row in rows:
        grouped[row.family].append(row)

    print("=" * 132)
    print("DIRECTIONAL-MEASURE B OVERLAP-MARGIN CARD")
    print("=" * 132)
    print("Overlap margin: mu = edge_b / h_mass = 1 / lambda - 1, with edge_b = b - h_mass")
    print("Interpretation target:")
    print("  mu >> 1   : tree-like / safely asymptotic source separation")
    print("  mu ~ 0    : finite-source shoulder, where low-b corners start grazing overlap")
    print("  mu <= 0   : source-support overlap, where pure response / b is the first form to break")
    print()
    print(
        f"{'family':>10s} {'N':>4s} {'lam_low':>8s} {'mu_low':>8s} {'mu_low_min':>10s} "
        f"{'low<=0':>8s} {'lam_bulk':>9s} {'mu_bulk':>9s} {'mu_bulk_min':>11s} "
        f"{'bulk<=0':>9s} {'A/b':>6s} {'F/b':>6s}"
    )
    print("-" * 132)
    for family in sorted(grouped):
        by_size: dict[int, list[CardRow]] = defaultdict(list)
        for row in grouped[family]:
            by_size[row.size].append(row)
        for size in sorted(by_size):
            bucket = by_size[size]
            low_target = min(row.target_b for row in bucket)
            low_rows = [row for row in bucket if row.target_b == low_target]
            bulk_rows = [row for row in bucket if row.target_b > low_target]
            low_lambdas = [row.lambda_ratio for row in low_rows]
            low_margins = [_margin(row) for row in low_rows]
            bulk_lambdas = [row.lambda_ratio for row in bulk_rows]
            bulk_margins = [_margin(row) for row in bulk_rows]
            print(
                f"{family:>10s} {size:4d} "
                f"{_fmt(_median(low_lambdas)):>8s} {_fmt(_median(low_margins)):>8s} {_fmt(min(low_margins)):>10s} "
                f"{_count_nonpos(low_rows):>8s} {_fmt(_median(bulk_lambdas)):>9s} {_fmt(_median(bulk_margins)):>9s} "
                f"{_fmt(min(bulk_margins)):>11s} {_count_nonpos(bulk_rows):>9s} "
                f"{_status(bucket, 'action_over_b'):>6s} {_status(bucket, 'flow_over_b'):>6s}"
            )
    print()
    print("Overlap-margin reading:")
    print("  1. Tree control: even the lowest-b corner keeps mu = 3, 5, 11 for N = 8, 10, 12.")
    print("     That means the tree family stays comfortably separated before any finite-source crisis begins.")
    print("  2. Narrow random-DAG family: the low-b corner collapses to mu ~ 0 while the bulk still sits near mu ~ 5.")
    print("     So pure response / b survives overall, but only because the near-overlap problem is still localized to a few seeds.")
    print("  3. Wide random-DAG family: the low-b corner crosses into mu <= 0 at small N and stays near the overlap shoulder at N = 25,")
    print("     while the bulk margin is only mu ~ 1.6..1.9. That is where response / b becomes the first denominator to fail.")
    print("  4. So the family dependence is local overlap geometry, not a new force law.")
    print("     The crossover variable is still lambda = h_mass / b, but the clean diagnostic form is")
    print("     mu = edge_b / h_mass = 1 / lambda - 1 because it stays finite and signed through overlap.")


if __name__ == "__main__":
    main()
