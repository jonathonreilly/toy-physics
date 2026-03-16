#!/usr/bin/env python3
"""Cheap static self-checks for feature registry and tuple alignment."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    GeometryPredictionRow,
    decision_feature_value,
    degree_basis_feature_names,
    expanded_geometry_candidate_features,
    geometry_candidate_features,
    high_degree_decomposition_feature_names,
    high_degree_threshold_feature_names,
    local_neighborhood_motif_feature_names,
    neighbor_leverage_threshold_feature_names,
    neighbor_reach_threshold_feature_names,
    rich_neighborhood_basis_feature_names,
    soft_hub_exposure_feature_names,
    threshold_exposure_decomposition_feature_names,
)


def build_dummy_row() -> GeometryPredictionRow:
    return GeometryPredictionRow(
        dataset_name="dummy",
        source_name="dummy",
        rule_family="compact",
        retained_weight=1.0,
        regime="single-selected",
        center_range=1.0,
        center_variation=2.0,
        span_range=3.0,
        turning_points=1,
        max_step_fraction=0.5,
        crosses_midline=True,
        boundary_fraction=0.25,
        pocket_fraction=0.125,
        boundary_roughness=0.375,
        deep_pocket_fraction=0.0625,
        degree_fractions=tuple(float(index) for index in range(len(degree_basis_feature_names()))),
        motif_fractions=tuple(
            float(index)
            for index in range(len(local_neighborhood_motif_feature_names()))
        ),
        high_degree_decomposition=tuple(
            float(index)
            for index in range(len(high_degree_decomposition_feature_names()))
        ),
        high_degree_threshold_fractions=tuple(
            float(index)
            for index in range(len(high_degree_threshold_feature_names()))
        ),
        soft_hub_exposure=tuple(
            float(index)
            for index in range(len(soft_hub_exposure_feature_names()))
        ),
        neighbor_reach_threshold_fractions=tuple(
            float(index)
            for index in range(len(neighbor_reach_threshold_feature_names()))
        ),
        neighbor_leverage_threshold_fractions=tuple(
            float(index)
            for index in range(len(neighbor_leverage_threshold_feature_names()))
        ),
        threshold_exposure_decomposition=tuple(
            float(index)
            for index in range(len(threshold_exposure_decomposition_feature_names()))
        ),
    )


def main() -> None:
    row = build_dummy_row()
    feature_groups = {
        "geometry": geometry_candidate_features(),
        "expanded": expanded_geometry_candidate_features(),
        "degree": degree_basis_feature_names(),
        "rich": rich_neighborhood_basis_feature_names(),
        "high_degree_decomposition": high_degree_decomposition_feature_names(),
        "high_degree_threshold": high_degree_threshold_feature_names(),
        "soft_hub_exposure": soft_hub_exposure_feature_names(),
        "neighbor_reach_threshold": neighbor_reach_threshold_feature_names(),
        "neighbor_leverage_threshold": neighbor_leverage_threshold_feature_names(),
        "threshold_exposure": threshold_exposure_decomposition_feature_names(),
    }

    all_features: set[str] = set()
    for group_name, feature_names in feature_groups.items():
        duplicates = len(feature_names) - len(set(feature_names))
        if duplicates:
            raise AssertionError(f"{group_name} contains duplicate feature names")
        all_features.update(feature_names)

    values = {feature: decision_feature_value(row, feature) for feature in sorted(all_features)}
    if len(values) != len(all_features):
        raise AssertionError("Feature-value map dropped entries unexpectedly")

    expected_lengths = {
        "degree_fractions": len(degree_basis_feature_names()),
        "motif_fractions": len(local_neighborhood_motif_feature_names()),
        "high_degree_decomposition": len(high_degree_decomposition_feature_names()),
        "high_degree_threshold_fractions": len(high_degree_threshold_feature_names()),
        "soft_hub_exposure": len(soft_hub_exposure_feature_names()),
        "neighbor_reach_threshold_fractions": len(neighbor_reach_threshold_feature_names()),
        "neighbor_leverage_threshold_fractions": len(neighbor_leverage_threshold_feature_names()),
        "threshold_exposure_decomposition": len(threshold_exposure_decomposition_feature_names()),
    }
    actual_lengths = {
        "degree_fractions": len(row.degree_fractions),
        "motif_fractions": len(row.motif_fractions),
        "high_degree_decomposition": len(row.high_degree_decomposition),
        "high_degree_threshold_fractions": len(row.high_degree_threshold_fractions),
        "soft_hub_exposure": len(row.soft_hub_exposure),
        "neighbor_reach_threshold_fractions": len(row.neighbor_reach_threshold_fractions),
        "neighbor_leverage_threshold_fractions": len(row.neighbor_leverage_threshold_fractions),
        "threshold_exposure_decomposition": len(row.threshold_exposure_decomposition),
    }
    if actual_lengths != expected_lengths:
        raise AssertionError(
            f"Tuple-length mismatch: expected={expected_lengths} actual={actual_lengths}"
        )

    print(
        "feature registry alignment ok "
        f"groups={len(feature_groups)} features={len(all_features)}"
    )


if __name__ == "__main__":
    main()
