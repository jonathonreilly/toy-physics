#!/usr/bin/env python3
"""Probe the two residual frozen 3-NN misses on the directional-b seam.

This bounded follow-on keeps the fixed directional-measure propagator and the
frozen 3-NN threshold from the original dense reference sample. It does not
refit thresholds or reopen the denominator search. Instead it asks a narrower
question:

- can the last two midlayer-sentinel 3-NN misses be rescued by equally local,
  miss-shaped clauses without breaking the older controls?
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_density_stencil_transfer import (  # noqa: E402
    _dense_reference_rows,
    _midlayer_rows,
    _rule_specs,
    _tree_rows,
)
from scripts.directional_b_overlap_continuous_density_bridge_card import (  # noqa: E402
    DensityRow,
    _accuracy,
)
from scripts.directional_b_overlap_continuous_density_midlayer_holdout import (  # noqa: E402
    _generate_midlayer_holdout,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.scaling_testbench import build_branching_tree  # noqa: E402


MIDLAYER_TARGET_B = 1.5
TREE_TARGET_B = 1.0


@dataclass(frozen=True)
class LocalDetail:
    family: str
    size: int
    seed: int
    mass_nodes: int
    mu: float
    target_count: int
    below_in_band: int
    above_in_band: int
    d1: float
    d2: float
    d3: float
    d4: float
    local_gap_density_load: float
    knn3_density_load: float
    knn4_density_load: float


def _fmt_stats(stats: tuple[int, int, int, int, float]) -> str:
    tp, fp, fn, tn, acc = stats
    return f"{tp}/{fp}/{fn}/{tn} {acc:.4f}"


def _row_key(row: DensityRow) -> tuple[str, int, int]:
    return row.family, row.size, row.seed


def _row_layout(
    row: DensityRow,
) -> tuple[list[tuple[float, float]], list[int], float]:
    if row.family == "tree":
        positions, _adj, layer_indices = build_branching_tree(
            row.size,
            branching_factor=2,
            y_range=10.0,
        )
        return positions, layer_indices[len(layer_indices) // 2], TREE_TARGET_B

    if row.family.startswith("dag-m"):
        positions, _adj, _meta = generate_causal_dag(
            n_layers=row.size,
            nodes_per_layer=25,
            y_range=12.0,
            connect_radius=3.0,
            rng_seed=row.seed * 11 + 7,
        )
    elif row.family.startswith("holdout-m"):
        positions, _adj, _meta = generate_causal_dag(
            n_layers=row.size,
            nodes_per_layer=28,
            y_range=13.0,
            connect_radius=3.0,
            rng_seed=row.seed * 11 + 701,
        )
    elif row.family.startswith("midgamma1.4"):
        positions, _adj = _generate_midlayer_holdout(
            n_layers=row.size,
            nodes_per_layer=25,
            y_range=12.0,
            connect_radius=3.0,
            rng_seed=row.seed * 11 + 1701,
            midlayer_gamma=1.4,
        )
    else:
        raise ValueError(f"unsupported family: {row.family}")

    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, _y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    return positions, by_layer[layers[len(layers) // 2]], MIDLAYER_TARGET_B


def _detail_for_row(row: DensityRow) -> LocalDetail:
    positions, grav_layer_nodes, target_b = _row_layout(row)
    center_y = statistics.fmean(y for _x, y in positions)
    target_y = center_y + target_b
    same_side_positions = sorted(
        positions[node][1] for node in grav_layer_nodes if positions[node][1] >= center_y
    )
    below_in_band = sum(1 for y in same_side_positions if target_y - 1.0 <= y < target_y)
    above_in_band = sum(1 for y in same_side_positions if target_y <= y <= target_y + 1.0)
    distances = sorted(abs(y - target_y) for y in same_side_positions)
    while len(distances) < 4:
        distances.append(float("nan"))
    return LocalDetail(
        family=row.family,
        size=row.size,
        seed=row.seed,
        mass_nodes=row.mass_nodes,
        mu=row.mu,
        target_count=row.local_target_count,
        below_in_band=below_in_band,
        above_in_band=above_in_band,
        d1=distances[0],
        d2=distances[1],
        d3=distances[2],
        d4=distances[3],
        local_gap_density_load=row.local_gap_density_load,
        knn3_density_load=row.knn3_density_load,
        knn4_density_load=row.knn4_density_load,
    )


def main() -> None:
    dense_reference_rows = _dense_reference_rows()
    tree_rows = _tree_rows()
    midlayer_rows = _midlayer_rows()
    reference_rows = [*dense_reference_rows, *tree_rows]
    extended_rows = [*reference_rows, *midlayer_rows]

    rule_by_label = {rule.label: rule for rule in _rule_specs(dense_reference_rows)}
    knn3_threshold = rule_by_label["3-NN"].threshold

    all_rows = [*reference_rows, *midlayer_rows]
    detail_by_key = {_row_key(row): _detail_for_row(row) for row in all_rows}
    residual_details = [
        detail_by_key[_row_key(row)]
        for row in sorted(midlayer_rows, key=lambda item: (item.family, item.size, item.seed))
        if row.overlap and row.knn3_density_load < knn3_threshold
    ]

    sparse_residual = max(residual_details, key=lambda detail: detail.d1)
    upper_residual = max(
        residual_details,
        key=lambda detail: (detail.above_in_band, detail.local_gap_density_load),
    )

    def base_knn3(row: DensityRow) -> bool:
        return row.knn3_density_load >= knn3_threshold

    def sparse_clause(row: DensityRow) -> bool:
        detail = detail_by_key[_row_key(row)]
        return detail.d1 >= sparse_residual.d1

    def upper_clause(row: DensityRow) -> bool:
        detail = detail_by_key[_row_key(row)]
        return (
            detail.above_in_band >= upper_residual.above_in_band
            and detail.local_gap_density_load >= upper_residual.local_gap_density_load
        )

    def hybrid_clause(row: DensityRow) -> bool:
        return base_knn3(row) or sparse_clause(row) or upper_clause(row)

    new_safe_false_positives = [
        detail_by_key[_row_key(row)]
        for row in sorted(reference_rows, key=lambda item: (item.family, item.size, item.seed))
        if hybrid_clause(row) and not row.overlap and not base_knn3(row)
    ]

    print("=" * 132)
    print("DIRECTIONAL-MEASURE B DENSITY RESIDUAL PROBE")
    print("=" * 132)
    print("Freeze the original dense-reference 3-NN threshold, then inspect only the two remaining")
    print("midlayer-sentinel overlap misses. No threshold refit or denominator widening is allowed.")
    print()
    print("Frozen base rule:")
    print(f"  3-NN : knn3_density_load >= {knn3_threshold:.4f}")
    print()
    print("Residual frozen 3-NN misses on the midlayer sentinel:")
    print(
        f"{'family':>14s} {'N':>4s} {'seed':>4s} {'mu':>8s} {'target_ct':>9s} "
        f"{'below':>6s} {'above':>6s} {'d1':>7s} {'d2':>7s} {'d3':>7s} {'d4':>7s} "
        f"{'gap_ld':>8s} {'3-NN':>8s} {'4-NN':>8s}"
    )
    print("-" * 132)
    for detail in residual_details:
        print(
            f"{detail.family:>14s} {detail.size:4d} {detail.seed:4d} {detail.mu:8.3f} "
            f"{detail.target_count:9d} {detail.below_in_band:6d} {detail.above_in_band:6d} "
            f"{detail.d1:7.3f} {detail.d2:7.3f} {detail.d3:7.3f} {detail.d4:7.3f} "
            f"{detail.local_gap_density_load:8.3f} {detail.knn3_density_load:8.3f} {detail.knn4_density_load:8.3f}"
        )
    print()
    print("Minimal miss-local rescue clauses:")
    print(
        f"  sparse-shoulder: first same-side support still far from the target plane, d1 >= {sparse_residual.d1:.4f}"
    )
    print(
        "  upper-shelf    : dense upper-side shelf, "
        f"above_in_band >= {upper_residual.above_in_band} and "
        f"local_gap_density_load >= {upper_residual.local_gap_density_load:.4f}"
    )
    print()
    print(
        f"{'rule':>18s} {'reference+tree tp/fp/fn/tn acc':>31s} "
        f"{'midlayer tp/fp/fn/tn acc':>27s} {'extended tp/fp/fn/tn acc':>27s}"
    )
    print("-" * 132)
    for label, predicate in (
        ("frozen-3NN", base_knn3),
        ("sparse-shoulder", lambda row: base_knn3(row) or sparse_clause(row)),
        ("upper-shelf", lambda row: base_knn3(row) or upper_clause(row)),
        ("combined-hybrid", hybrid_clause),
    ):
        print(
            f"{label:>18s} "
            f"{_fmt_stats(_accuracy(reference_rows, predicate)):>31s} "
            f"{_fmt_stats(_accuracy(midlayer_rows, predicate)):>27s} "
            f"{_fmt_stats(_accuracy(extended_rows, predicate)):>27s}"
        )
    print()
    print("New safe-side false positives under the combined hybrid:")
    if not new_safe_false_positives:
        print("  none")
    else:
        print(
            f"{'family':>14s} {'N':>4s} {'seed':>4s} {'mu':>8s} {'target_ct':>9s} "
            f"{'below':>6s} {'above':>6s} {'d1':>7s} {'gap_ld':>8s}"
        )
        print("-" * 78)
        for detail in new_safe_false_positives:
            print(
                f"{detail.family:>14s} {detail.size:4d} {detail.seed:4d} {detail.mu:8.3f} "
                f"{detail.target_count:9d} {detail.below_in_band:6d} {detail.above_in_band:6d} "
                f"{detail.d1:7.3f} {detail.local_gap_density_load:8.3f}"
            )
    print()
    print("Interpretation:")
    print("  1. The two remaining 3-NN misses split into different local geometries:")
    print("     one sparse shoulder with only one in-band node, and one asymmetric upper shelf with two nodes above the target plane.")
    print("  2. Miss-local clauses can close the current midlayer sentinel, but they are not portable:")
    print("     the combined hybrid reaches 10/0/0/30 on the midlayer rows while degrading the old reference+tree control to 24/8/0/31.")
    print("  3. So the current residual gap is no longer a fourth-neighbor problem, but it is also not solved by a clean frozen rescue law.")
    print("  4. The portable statement stays occupancy-first, and 3-NN remains the best single frozen smooth law on the current extended sample.")


if __name__ == "__main__":
    main()
