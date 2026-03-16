#!/usr/bin/env python3
"""Re-run predictor-side findings after benchmark-default fixes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    cross_dataset_subset_pareto_benchmark,
    cross_dataset_transfer_benchmark,
    generated_geometry_feature_expansion_benchmark,
    generated_geometry_predictor_comparison,
    high_degree_decomposition_benchmark,
    high_degree_threshold_benchmark,
    neighbor_leverage_threshold_benchmark,
    neighbor_reach_threshold_benchmark,
    neighborhood_basis_benchmark,
    neighborhood_basis_residual_benchmark,
    ordinal_variant_comparison,
    predictor_family_comparison,
    render_cross_dataset_subset_pareto_table,
    render_cross_dataset_transfer_table,
    render_generated_feature_expansion_table,
    render_generated_geometry_predictor_table,
    render_high_degree_decomposition_table,
    render_neighborhood_basis_benchmark_table,
    render_neighborhood_basis_feature_table,
    render_neighborhood_basis_residual_table,
    render_ordinal_variant_comparison_table,
    render_predictor_family_comparison_table,
    soft_hub_exposure_benchmark,
    threshold_exposure_decomposition_benchmark,
)


def banner(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def top_rows_per_family(rows, family_attr: str = "rule_family", per_family: int = 8):
    kept = []
    counts: dict[str, int] = {}
    for row in rows:
        family = getattr(row, family_attr)
        seen = counts.get(family, 0)
        if seen >= per_family:
            continue
        counts[family] = seen + 1
        kept.append(row)
    return kept


def reduced_same_weight_regression_check() -> None:
    banner("Reduced Same-Weight Regression Checks")

    generated_default = generated_geometry_predictor_comparison(
        retained_weight=1.0,
        mode_retained_weight=None,
        geometry_variant_limit=1,
        procedural_variant_limit=1,
        procedural_styles=("walk",),
        max_subset_size=2,
        top_k_subset_rows=2,
    )
    generated_explicit = generated_geometry_predictor_comparison(
        retained_weight=1.0,
        mode_retained_weight=1.0,
        geometry_variant_limit=1,
        procedural_variant_limit=1,
        procedural_styles=("walk",),
        max_subset_size=2,
        top_k_subset_rows=2,
    )
    generated_match = [
        (
            row.rule_family,
            row.feature_subset,
            row.model_family,
            round(row.generated_mean_accuracy, 6),
            round(row.generated_worst_accuracy, 6),
        )
        for row in generated_default
    ] == [
        (
            row.rule_family,
            row.feature_subset,
            row.model_family,
            round(row.generated_mean_accuracy, 6),
            round(row.generated_worst_accuracy, 6),
        )
        for row in generated_explicit
    ]
    print(f"generated_geometry_predictor_comparison default-vs-explicit match: {generated_match}")

    predictor_default = predictor_family_comparison(
        retained_weight=1.0,
        mode_retained_weight=None,
        procedural_variant_limit=1,
        max_subset_size=2,
        top_k_subset_rows=1,
    )
    predictor_explicit = predictor_family_comparison(
        retained_weight=1.0,
        mode_retained_weight=1.0,
        procedural_variant_limit=1,
        max_subset_size=2,
        top_k_subset_rows=1,
    )
    predictor_match = [
        (
            row.rule_family,
            row.feature_subset,
            row.model_family,
            round(row.mean_transfer_accuracy, 6),
            round(row.worst_transfer_accuracy, 6),
        )
        for row in predictor_default
    ] == [
        (
            row.rule_family,
            row.feature_subset,
            row.model_family,
            round(row.mean_transfer_accuracy, 6),
            round(row.worst_transfer_accuracy, 6),
        )
        for row in predictor_explicit
    ]
    print(f"predictor_family_comparison default-vs-explicit match: {predictor_match}")


def timed_section(title: str, fn):
    banner(title)
    started = time.time()
    result = fn()
    print(f"[elapsed {time.time() - started:.1f}s]")
    return result


def main() -> None:
    print(
        "post-fix predictor audit started "
        + datetime.now().isoformat(timespec="seconds")
    )
    print("This reruns predictor-side findings on the corrected same-weight, mode-only-selection path.")

    reduced_same_weight_regression_check()

    transfer_rows = timed_section(
        "Cross-Dataset Transfer Benchmark",
        cross_dataset_transfer_benchmark,
    )
    print(render_cross_dataset_transfer_table(top_rows_per_family(transfer_rows, per_family=8)))

    subset_rows = timed_section(
        "Cross-Dataset Subset Pareto Benchmark",
        cross_dataset_subset_pareto_benchmark,
    )
    print(render_cross_dataset_subset_pareto_table(subset_rows, limit_per_family=8))

    predictor_rows = timed_section(
        "Predictor Family Comparison",
        predictor_family_comparison,
    )
    print(render_predictor_family_comparison_table(top_rows_per_family(predictor_rows, per_family=8)))

    ordinal_rows = timed_section(
        "Ordinal Variant Comparison",
        ordinal_variant_comparison,
    )
    print(render_ordinal_variant_comparison_table(top_rows_per_family(ordinal_rows, per_family=8)))

    generated_rows = timed_section(
        "Generated-Geometry Predictor Comparison",
        generated_geometry_predictor_comparison,
    )
    print(render_generated_geometry_predictor_table(top_rows_per_family(generated_rows, per_family=8)))

    generated_feature_rows = timed_section(
        "Generated-Geometry Feature Expansion Benchmark",
        generated_geometry_feature_expansion_benchmark,
    )
    print(render_generated_feature_expansion_table(generated_feature_rows, top_k_per_family=8))

    basis_rows, neighborhood_rows = timed_section(
        "Neighborhood Basis Benchmark",
        neighborhood_basis_benchmark,
    )
    print(render_neighborhood_basis_feature_table(basis_rows))
    print()
    print(render_neighborhood_basis_benchmark_table(neighborhood_rows, top_k_per_family=8))

    residual_rows = timed_section(
        "Neighborhood Basis Residual Benchmark",
        neighborhood_basis_residual_benchmark,
    )
    print(render_neighborhood_basis_residual_table(residual_rows))

    high_degree_rows = timed_section(
        "High-Degree Decomposition Benchmark",
        high_degree_decomposition_benchmark,
    )
    print(render_high_degree_decomposition_table(high_degree_rows))

    threshold_rows = timed_section(
        "High-Degree Threshold Benchmark",
        high_degree_threshold_benchmark,
    )
    print(render_high_degree_decomposition_table(threshold_rows))

    soft_rows = timed_section(
        "Soft Hub Exposure Benchmark",
        soft_hub_exposure_benchmark,
    )
    print(render_high_degree_decomposition_table(soft_rows))

    reach_rows = timed_section(
        "Neighbor Reach Threshold Benchmark",
        neighbor_reach_threshold_benchmark,
    )
    print(render_high_degree_decomposition_table(reach_rows))

    leverage_rows = timed_section(
        "Neighbor Leverage Threshold Benchmark",
        neighbor_leverage_threshold_benchmark,
    )
    print(render_high_degree_decomposition_table(leverage_rows))

    exposure_rows = timed_section(
        "Threshold Exposure Decomposition Benchmark",
        threshold_exposure_decomposition_benchmark,
    )
    print(render_high_degree_decomposition_table(exposure_rows))

    print()
    print(
        "post-fix predictor audit completed "
        + datetime.now().isoformat(timespec="seconds")
    )


if __name__ == "__main__":
    main()
