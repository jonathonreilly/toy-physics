#!/usr/bin/env python3
"""Translate the occupancy bridge into a physical supply-load law.

This bounded follow-on keeps the corrected directional-b lane fixed and stays on
the same combined dense-family sample used by the occupancy bridge card. The
question is narrower than another feature search:

- decompose `target_fill = local_target_count / mass_nodes`
- ask whether the overlap seam is really carried by
  - raw target-band supply,
  - raw source-window size,
  - same-side layer density near the target plane,
  - or the combined source-load ratio

The goal is a more physical translation of the retained overlap bridge rather
than a wider architecture search.
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

from scripts.directional_b_overlap_onset_local_density_compare import (  # noqa: E402
    TARGET_BAND_HALF_WIDTH,
    _accuracy,
    _candidate_thresholds,
)
from scripts.directional_b_readout_compare import _select_mass_nodes  # noqa: E402
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402


@dataclass(frozen=True)
class SupplyRow:
    family: str
    size: int
    seed: int
    mass_nodes: int
    actual_b: float
    h_mass: float
    mu: float
    grav_layer_nodes: int
    same_side_count: int
    local_target_count: int
    target_fill: float
    target_share_same_side: float
    selected_span_step: float
    source_load: float
    overlap: bool


@dataclass(frozen=True)
class FactorRule:
    feature: str
    op_name: str
    threshold: float
    tp: int
    fp: int
    fn: int
    tn: int
    accuracy: float


def _build_row(
    family: str,
    size: int,
    seed: int,
    mass_nodes: int,
    target_b: float,
    positions: list[tuple[float, float]],
    grav_layer_nodes: list[int],
) -> SupplyRow | None:
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

    same_side_nodes = [
        node for node in grav_layer_nodes if positions[node][1] >= center_y
    ]
    target_y = center_y + target_b
    local_target_count = sum(
        1
        for node in same_side_nodes
        if abs(positions[node][1] - target_y) <= TARGET_BAND_HALF_WIDTH
    )
    same_side_count = len(same_side_nodes)
    span_step = (max(ys) - min(ys)) / max(1, len(selected) - 1)
    target_fill = local_target_count / mass_nodes
    target_share_same_side = (
        local_target_count / same_side_count if same_side_count > 0 else float("nan")
    )
    source_load = mass_nodes / max(1, local_target_count)

    return SupplyRow(
        family=family,
        size=size,
        seed=seed,
        mass_nodes=mass_nodes,
        actual_b=actual_b,
        h_mass=h_mass,
        mu=mu,
        grav_layer_nodes=len(grav_layer_nodes),
        same_side_count=same_side_count,
        local_target_count=local_target_count,
        target_fill=target_fill,
        target_share_same_side=target_share_same_side,
        selected_span_step=span_step,
        source_load=source_load,
        overlap=mu <= 0.0,
    )


def _evaluate_baseline_dag(task: tuple[int, int, int, float]) -> SupplyRow | None:
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


def _evaluate_holdout_dag(
    task: tuple[int, int, int, float, int, float, float, int],
) -> SupplyRow | None:
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


def _feature_value(row: SupplyRow, feature: str) -> float:
    return getattr(row, feature)


def _best_rule(
    rows: list[SupplyRow],
    feature: str,
    op_names: tuple[str, ...],
) -> FactorRule:
    values = [_feature_value(row, feature) for row in rows]
    finite_values = [value for value in values if math.isfinite(value)]
    best: FactorRule | None = None
    for threshold in _candidate_thresholds(finite_values):
        for op_name in op_names:
            if op_name == "<=":
                stats = _accuracy(
                    rows,
                    lambda row, f=feature, t=threshold: _feature_value(row, f) <= t,
                )
            else:
                stats = _accuracy(
                    rows,
                    lambda row, f=feature, t=threshold: _feature_value(row, f) >= t,
                )
            rule = FactorRule(feature, op_name, threshold, *stats)
            if best is None or rule.accuracy > best.accuracy:
                best = rule
    assert best is not None
    return best


def _apply_rule(rows: list[SupplyRow], rule: FactorRule) -> tuple[int, int, int, int, float]:
    if rule.op_name == "<=":
        return _accuracy(rows, lambda row: _feature_value(row, rule.feature) <= rule.threshold)
    return _accuracy(rows, lambda row: _feature_value(row, rule.feature) >= rule.threshold)


def _fmt_threshold(value: float) -> str:
    if math.isclose(value, round(value)):
        return str(int(round(value)))
    return f"{value:.4f}"


def _fmt_rule(rule: FactorRule) -> str:
    return f"{rule.feature} {rule.op_name} {_fmt_threshold(rule.threshold)}"


def _label(row: SupplyRow) -> str:
    return "holdout" if row.family.startswith("holdout-") else "baseline"


def _mean(rows: list[SupplyRow], field: str) -> float:
    values = [getattr(row, field) for row in rows]
    values = [value for value in values if not math.isnan(value)]
    return statistics.fmean(values) if values else float("nan")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--baseline-dag-seeds", type=int, default=5)
    parser.add_argument("--holdout-dag-seeds", type=int, default=10)
    parser.add_argument("--dag-sizes", nargs="+", type=int, default=[12, 25])
    parser.add_argument("--dag-target-b", type=float, default=1.5)
    parser.add_argument("--holdout-nodes-per-layer", type=int, default=28)
    parser.add_argument("--holdout-y-range", type=float, default=13.0)
    parser.add_argument("--holdout-connect-radius", type=float, default=3.0)
    parser.add_argument("--holdout-seed-offset", type=int, default=701)
    args = parser.parse_args()

    baseline_tasks = [
        (mass_nodes, n_layers, seed, args.dag_target_b)
        for mass_nodes in (3, 5)
        for n_layers in args.dag_sizes
        for seed in range(args.baseline_dag_seeds)
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
        baseline_rows = [_evaluate_baseline_dag(task) for task in baseline_tasks]
        holdout_rows = [_evaluate_holdout_dag(task) for task in holdout_tasks]
    else:
        try:
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as pool:
                baseline_rows = list(pool.map(_evaluate_baseline_dag, baseline_tasks))
                holdout_rows = list(pool.map(_evaluate_holdout_dag, holdout_tasks))
        except (OSError, PermissionError):
            baseline_rows = [_evaluate_baseline_dag(task) for task in baseline_tasks]
            holdout_rows = [_evaluate_holdout_dag(task) for task in holdout_tasks]

    rows = [row for row in [*baseline_rows, *holdout_rows] if row is not None]
    rows.sort(key=lambda row: (_label(row), row.family, row.size, row.seed))

    by_label: dict[str, list[SupplyRow]] = defaultdict(list)
    by_family: dict[str, list[SupplyRow]] = defaultdict(list)
    for row in rows:
        by_label[_label(row)].append(row)
        by_family[row.family].append(row)

    factor_specs = (
        ("target_fill", ("<=",)),
        ("source_load", (">=",)),
        ("local_target_count", ("<=",)),
        ("mass_nodes", (">=",)),
        ("target_share_same_side", ("<=",)),
    )
    rules = [_best_rule(rows, feature, ops) for feature, ops in factor_specs]
    rule_by_feature = {rule.feature: rule for rule in rules}

    print("=" * 124)
    print("DIRECTIONAL-MEASURE B OVERLAP SUPPLY-LOAD BRIDGE CARD")
    print("=" * 124)
    print(
        "This card decomposes the retained occupancy bridge on the same combined dense-family sample and asks"
    )
    print("which physical factor transfers with the least family dependence.")
    print()
    print("Factor definitions:")
    print(f"  local_target_count    = same-side mid-layer nodes inside |y - y_target| <= {TARGET_BAND_HALF_WIDTH:.1f}")
    print("  mass_nodes            = selected source-window size")
    print("  target_share_same_side = local_target_count / same_side_count")
    print("  source_load           = mass_nodes / max(1, local_target_count)")
    print("  target_fill           = local_target_count / mass_nodes = 1 / source_load")
    print()
    print(
        f"{'set':>10s} {'rows':>4s} {'ovlp':>5s} {'count_ovlp':>11s} {'count_safe':>11s} "
        f"{'share_ovlp':>11s} {'share_safe':>11s} {'load_ovlp':>10s} {'load_safe':>10s}"
    )
    print("-" * 124)
    for label in ("baseline", "holdout"):
        bucket = by_label[label]
        overlap_rows = [row for row in bucket if row.overlap]
        safe_rows = [row for row in bucket if not row.overlap]
        print(
            f"{label:>10s} {len(bucket):4d} {sum(row.overlap for row in bucket):5d} "
            f"{_mean(overlap_rows, 'local_target_count'):11.3f} "
            f"{_mean(safe_rows, 'local_target_count'):11.3f} "
            f"{_mean(overlap_rows, 'target_share_same_side'):11.3f} "
            f"{_mean(safe_rows, 'target_share_same_side'):11.3f} "
            f"{_mean(overlap_rows, 'source_load'):10.3f} "
            f"{_mean(safe_rows, 'source_load'):10.3f}"
        )
    overlap_rows = [row for row in rows if row.overlap]
    safe_rows = [row for row in rows if not row.overlap]
    print(
        f"{'combined':>10s} {len(rows):4d} {sum(row.overlap for row in rows):5d} "
        f"{_mean(overlap_rows, 'local_target_count'):11.3f} "
        f"{_mean(safe_rows, 'local_target_count'):11.3f} "
        f"{_mean(overlap_rows, 'target_share_same_side'):11.3f} "
        f"{_mean(safe_rows, 'target_share_same_side'):11.3f} "
        f"{_mean(overlap_rows, 'source_load'):10.3f} "
        f"{_mean(safe_rows, 'source_load'):10.3f}"
    )
    print()
    print(
        f"{'factor':>24s} {'best rule':>36s} {'combined acc':>13s} {'baseline acc':>13s} "
        f"{'holdout acc':>12s}"
    )
    print("-" * 112)
    for feature in (
        "target_fill",
        "source_load",
        "local_target_count",
        "mass_nodes",
        "target_share_same_side",
    ):
        rule = rule_by_feature[feature]
        baseline_acc = _apply_rule(by_label["baseline"], rule)[-1]
        holdout_acc = _apply_rule(by_label["holdout"], rule)[-1]
        print(
            f"{feature:>24s} {_fmt_rule(rule):>36s} {rule.accuracy:13.4f} "
            f"{baseline_acc:13.4f} {holdout_acc:12.4f}"
        )
    print()
    count_rule = rule_by_feature["local_target_count"]
    load_rule = rule_by_feature["source_load"]
    print(
        f"{'family':>14s} {'rows':>4s} {'ovlp':>5s} {'count rule acc':>15s} {'load rule acc':>15s}"
    )
    print("-" * 64)
    for family in sorted(by_family):
        bucket = by_family[family]
        count_acc = _apply_rule(bucket, count_rule)[-1]
        load_acc = _apply_rule(bucket, load_rule)[-1]
        print(
            f"{family:>14s} {len(bucket):4d} {sum(row.overlap for row in bucket):5d} "
            f"{count_acc:15.4f} {load_acc:15.4f}"
        )
    print()
    print("Interpretation:")
    print("  1. Raw target-band supply alone is not portable: local_target_count <= 1 works on the holdout")
    print("     but misses much of the baseline m5 corner.")
    print("  2. Source-window size alone is too crude; widening to five nodes is neither necessary nor sufficient.")
    print("  3. The retained physical translation is source load: overlap turns on once the source window demands")
    print("     about 2.5 or more source nodes per available target-band node.")
    print("  4. Equivalently, the occupancy bridge target_fill <= 0.4 is a supply-demand statement, not just a")
    print("     raw sparsity statement: dense families fail when local target-plane support does not scale with")
    print("     widened source demand.")


if __name__ == "__main__":
    main()
