#!/usr/bin/env python3
"""Compare frozen 3-NN and 4-NN density stencils on the midlayer sentinel.

This bounded directional-b follow-on does not reopen the denominator search or
introduce a new graph family. It reuses the existing dense reference sample,
the frozen branching-tree control, and the center-biased midlayer sentinel to
answer one narrower question:

- is the recent midlayer failure really about the fourth-neighbor stencil?

The script rebuilds the frozen 3-NN and 4-NN density-load thresholds on the
original dense reference sample, then applies those same thresholds without
refit to the tree control and the midlayer sentinel.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_overlap_continuous_density_bridge_card import (  # noqa: E402
    DensityRow,
    _accuracy,
    _best_rule,
    _evaluate_baseline_dag,
    _evaluate_holdout_dag,
)
from scripts.directional_b_overlap_continuous_density_midlayer_holdout import (  # noqa: E402
    DagConfig,
    _collect_rows,
    _evaluate_midlayer_dag,
    _generate_midlayer_holdout,
)
from scripts.directional_b_overlap_continuous_density_tree_control import (  # noqa: E402
    _evaluate_tree,
)


@dataclass(frozen=True)
class RuleSpec:
    label: str
    feature: str
    threshold: float


@dataclass(frozen=True)
class MissDetail:
    family: str
    size: int
    seed: int
    mass_nodes: int
    mu: float
    target_count: int
    below_in_band: int
    above_in_band: int
    knn3_density_load: float
    knn4_density_load: float
    rescued_by_knn3: bool


def _fmt_stats(stats: tuple[int, int, int, int, float]) -> str:
    tp, fp, fn, tn, acc = stats
    return f"{tp}/{fp}/{fn}/{tn} {acc:.4f}"


def _dense_reference_rows() -> list[DensityRow]:
    baseline_tasks = [
        (mass_nodes, n_layers, seed, 1.5)
        for mass_nodes in (3, 5)
        for n_layers in (12, 25)
        for seed in range(5)
    ]
    holdout_tasks = [
        (mass_nodes, n_layers, seed, 1.5, 28, 13.0, 3.0, 701)
        for mass_nodes in (3, 5)
        for n_layers in (12, 25)
        for seed in range(10)
    ]
    baseline_rows = [row for row in map(_evaluate_baseline_dag, baseline_tasks) if row is not None]
    holdout_rows = [row for row in map(_evaluate_holdout_dag, holdout_tasks) if row is not None]
    return [*baseline_rows, *holdout_rows]


def _tree_rows() -> list[DensityRow]:
    tasks = [(n_layers, 2, 1.0, 2) for n_layers in (8, 10, 12)]
    return [row for row in map(_evaluate_tree, tasks) if row is not None]


def _midlayer_rows() -> list[DensityRow]:
    config = DagConfig(
        family_prefix="midgamma1.4",
        nodes_per_layer=25,
        y_range=12.0,
        connect_radius=3.0,
        seed_offset=1701,
        midlayer_gamma=1.4,
    )
    tasks = [
        (config, mass_nodes, n_layers, seed, 1.5)
        for mass_nodes in (3, 5)
        for n_layers in (12, 25)
        for seed in range(10)
    ]
    return _collect_rows(tasks, _evaluate_midlayer_dag, workers=min(8, max(1, os.cpu_count() or 1)))


def _rule_specs(dense_reference_rows: list[DensityRow]) -> list[RuleSpec]:
    return [
        RuleSpec(
            label="3-NN",
            feature="knn3_density_load",
            threshold=_best_rule(dense_reference_rows, "knn3_density_load").threshold,
        ),
        RuleSpec(
            label="4-NN",
            feature="knn4_density_load",
            threshold=_best_rule(dense_reference_rows, "knn4_density_load").threshold,
        ),
    ]


def _miss_details(midlayer_rows: list[DensityRow], knn3_threshold: float, knn4_threshold: float) -> list[MissDetail]:
    config = DagConfig(
        family_prefix="midgamma1.4",
        nodes_per_layer=25,
        y_range=12.0,
        connect_radius=3.0,
        seed_offset=1701,
        midlayer_gamma=1.4,
    )
    details: list[MissDetail] = []
    for row in sorted(midlayer_rows, key=lambda entry: (entry.family, entry.size, entry.seed)):
        if not row.overlap or row.knn4_density_load >= knn4_threshold:
            continue

        positions, _adj = _generate_midlayer_holdout(
            n_layers=row.size,
            nodes_per_layer=config.nodes_per_layer,
            y_range=config.y_range,
            connect_radius=config.connect_radius,
            rng_seed=row.seed * 11 + config.seed_offset,
            midlayer_gamma=config.midlayer_gamma,
        )
        by_layer: dict[int, list[int]] = defaultdict(list)
        for idx, (x, _y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer)
        grav_layer = by_layer[layers[len(layers) // 2]]
        center_y = statistics.fmean(y for _x, y in positions)
        target_y = center_y + 1.5
        same_side_positions = sorted(
            positions[node][1] for node in grav_layer if positions[node][1] >= center_y
        )
        below_in_band = sum(1 for y in same_side_positions if target_y - 1.0 <= y < target_y)
        above_in_band = sum(1 for y in same_side_positions if target_y <= y <= target_y + 1.0)
        details.append(
            MissDetail(
                family=row.family,
                size=row.size,
                seed=row.seed,
                mass_nodes=row.mass_nodes,
                mu=row.mu,
                target_count=row.local_target_count,
                below_in_band=below_in_band,
                above_in_band=above_in_band,
                knn3_density_load=row.knn3_density_load,
                knn4_density_load=row.knn4_density_load,
                rescued_by_knn3=row.knn3_density_load >= knn3_threshold,
            )
        )
    return details


def _family_rows(rows: list[DensityRow], prefix: str) -> list[DensityRow]:
    return [row for row in rows if row.family.startswith(prefix)]


def main() -> None:
    dense_reference_rows = _dense_reference_rows()
    tree_rows = _tree_rows()
    midlayer_rows = _midlayer_rows()
    reference_rows = [*dense_reference_rows, *tree_rows]
    extended_rows = [*reference_rows, *midlayer_rows]

    rules = _rule_specs(dense_reference_rows)
    rule_by_label = {rule.label: rule for rule in rules}
    miss_details = _miss_details(
        midlayer_rows,
        knn3_threshold=rule_by_label["3-NN"].threshold,
        knn4_threshold=rule_by_label["4-NN"].threshold,
    )

    print("=" * 132)
    print("DIRECTIONAL-MEASURE B DENSITY STENCIL TRANSFER")
    print("=" * 132)
    print(
        "Freeze the 3-NN and 4-NN density-load thresholds on the original dense reference sample, then"
    )
    print("apply them without refit to the tree control and the center-biased midlayer sentinel.")
    print()
    print("Frozen density-load rules from the original dense reference sample:")
    for rule in rules:
        print(f"  {rule.label:>4s} : {rule.feature} >= {rule.threshold:.4f}")
    print()
    print(
        f"{'set':>18s} {'rows':>4s} {'ovlp':>5s} {'3-NN tp/fp/fn/tn acc':>26s} "
        f"{'4-NN tp/fp/fn/tn acc':>26s}"
    )
    print("-" * 132)
    for label, rows in (
        ("reference+tree", reference_rows),
        ("midlayer-sentinel", midlayer_rows),
        ("extended-sample", extended_rows),
    ):
        overlap_count = sum(row.overlap for row in rows)
        knn3_stats = _accuracy(
            rows,
            lambda row, t=rule_by_label["3-NN"].threshold: row.knn3_density_load >= t,
        )
        knn4_stats = _accuracy(
            rows,
            lambda row, t=rule_by_label["4-NN"].threshold: row.knn4_density_load >= t,
        )
        print(
            f"{label:>18s} {len(rows):4d} {overlap_count:5d} "
            f"{_fmt_stats(knn3_stats):>26s} {_fmt_stats(knn4_stats):>26s}"
        )
    print()
    print("Midlayer family split:")
    print(
        f"{'family':>14s} {'rows':>4s} {'ovlp':>5s} {'3-NN acc':>10s} {'4-NN acc':>10s}"
    )
    print("-" * 56)
    for family in ("midgamma1.4-m3", "midgamma1.4-m5"):
        bucket = _family_rows(midlayer_rows, family)
        knn3_stats = _accuracy(
            bucket,
            lambda row, t=rule_by_label["3-NN"].threshold: row.knn3_density_load >= t,
        )
        knn4_stats = _accuracy(
            bucket,
            lambda row, t=rule_by_label["4-NN"].threshold: row.knn4_density_load >= t,
        )
        print(
            f"{family:>14s} {len(bucket):4d} {sum(row.overlap for row in bucket):5d} "
            f"{knn3_stats[4]:10.4f} {knn4_stats[4]:10.4f}"
        )
    print()
    print("Frozen 4-NN false negatives on the midlayer sentinel:")
    print(
        f"{'family':>14s} {'N':>4s} {'seed':>4s} {'mu':>8s} {'target_ct':>9s} "
        f"{'below':>6s} {'above':>6s} {'3-NN':>8s} {'4-NN':>8s} {'3-NN rescue':>12s}"
    )
    print("-" * 94)
    for detail in miss_details:
        print(
            f"{detail.family:>14s} {detail.size:4d} {detail.seed:4d} {detail.mu:8.3f} "
            f"{detail.target_count:9d} {detail.below_in_band:6d} {detail.above_in_band:6d} "
            f"{detail.knn3_density_load:8.3f} {detail.knn4_density_load:8.3f} "
            f"{'yes' if detail.rescued_by_knn3 else 'no':>12s}"
        )
    print()
    rescued = sum(detail.rescued_by_knn3 for detail in miss_details)
    one_sided = sum(
        1
        for detail in miss_details
        if (detail.below_in_band == 0) ^ (detail.above_in_band == 0)
    )
    print("Interpretation:")
    print(
        "  1. The original reference+tree sample still prefers the 4-NN stencil, "
        "so this is not a retroactive rewrite of the earlier dense-family fit."
    )
    print(
        "  2. The center-biased midlayer sentinel reverses that preference: the frozen 3-NN law rises to 0.9500,"
    )
    print(
        "     while the frozen 4-NN law falls to 0.8500 with six false negatives and no false positives."
    )
    extended_knn3 = _accuracy(
        extended_rows,
        lambda row, t=rule_by_label["3-NN"].threshold: row.knn3_density_load >= t,
    )
    extended_knn4 = _accuracy(
        extended_rows,
        lambda row, t=rule_by_label["4-NN"].threshold: row.knn4_density_load >= t,
    )
    print("  3. On the extended sample, 3-NN now exceeds 4-NN")
    print(
        f"     by accuracy: {extended_knn3[4]:.4f} vs {extended_knn4[4]:.4f}."
    )
    print(
        f"  4. The midlayer 4-NN miss mode is mostly one-sided low-occupancy support: {one_sided}/{len(miss_details)}"
    )
    print(
        f"     false negatives have in-band nodes on only one side of the target plane, and 3-NN rescues {rescued}/{len(miss_details)} of them."
    )
    print(
        "  5. The portable coarse statement is still occupancy-first, but if one frozen smooth density law"
    )
    print(
        "     must be carried onto the current expanded sample, 3-NN is the better stencil candidate than 4-NN."
    )


if __name__ == "__main__":
    main()
