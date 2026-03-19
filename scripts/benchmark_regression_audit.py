#!/usr/bin/env python3
"""Cheap regression checks for benchmark-path bugs we already fixed once."""

from __future__ import annotations

from dataclasses import astuple
import inspect
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    build_cross_dataset_prediction_context,
    build_generated_geometry_prediction_context,
    centerline_feature_subset_benchmark,
    compact_threshold_proxy_bridge_sets,
    compress_redundant_mode_subset_frontier_rows,
    feature_subset_cardinality,
    generated_geometry_predictor_comparison,
    mode_only_subset_frontier_rows,
    predictor_family_comparison,
    resolve_sparse_bridge_feature_names,
    sparse_fallback_access_benchmark,
)


def context_signature(
    context: tuple[list[object], list[object], list[object], list[object], list[object]],
) -> tuple[tuple[tuple[object, ...], ...], ...]:
    return tuple(tuple(astuple(row) for row in rows) for rows in context)


def check_same_weight_default() -> None:
    context_kwargs = dict(
        retained_weight=1.0,
        geometry_variant_limit=1,
        procedural_variant_limit=1,
        procedural_rediscovery_limit=1,
        procedural_styles=("walk",),
    )
    default_context = build_generated_geometry_prediction_context(
        mode_retained_weight=None,
        **context_kwargs,
    )
    explicit_context = build_generated_geometry_prediction_context(
        mode_retained_weight=1.0,
        **context_kwargs,
    )
    default_signature = context_signature(default_context)
    explicit_signature = context_signature(explicit_context)
    assert (
        default_signature == explicit_signature
    ), "mode_retained_weight=None diverged from explicit same-weight mode training"


def check_sparse_bridge_addback_visibility() -> None:
    addback_map = dict(compact_threshold_proxy_bridge_sets())
    removed_features = (
        "degree_8_fraction",
        "degree_7_fraction",
        "degree_6_fraction",
        "degree_5_fraction",
        "degree_4_fraction",
        "degree_3_fraction",
        "degree_2_fraction",
        "degree_1_fraction",
        "motif_mean_neighbor_degree",
        "motif_neighbor_degree_variation",
        "motif_two_hop_open_fraction",
        "motif_two_hop_occupied_fraction",
    )
    baseline_names = resolve_sparse_bridge_feature_names(removed_features, tuple())
    ge6_names = resolve_sparse_bridge_feature_names(
        removed_features,
        addback_map["add-ge-6"],
    )
    count6_names = resolve_sparse_bridge_feature_names(
        removed_features,
        addback_map["add-count6"],
    )

    assert (
        "motif_high_degree_neighbor_ge_6_fraction" not in baseline_names
    ), "baseline sparse-bridge vocabulary unexpectedly already contains ge_6"
    assert (
        "motif_high_degree_neighbor_ge_6_fraction" in ge6_names
    ), "ge_6 addback did not reach the sparse-bridge feature vocabulary"
    assert (
        "motif_high_degree_neighbor_count6_fraction" in count6_names
    ), "count6 addback did not reach the sparse-bridge feature vocabulary"
    assert (
        feature_subset_cardinality(", ".join(addback_map["add-ge-6"])) == 1
    ), "ge_6 addback should still be a one-feature predicate"


def _parse_feature_signature(feature_subset: str) -> tuple[str, ...]:
    stripped = feature_subset.strip()
    if not stripped or stripped == "-":
        return tuple()
    return tuple(part.strip() for part in stripped.split(","))


def _manual_mode_only_candidate_map(
    top_k_subset_rows: int = 2,
) -> dict[str, list[tuple[str, ...]]]:
    mode_core_rows, _mode_rows, _roughness_rows, _procedural_rows = (
        build_cross_dataset_prediction_context(
            retained_weight=1.0,
            mode_retained_weight=1.0,
            procedural_variant_limit=1,
            procedural_rediscovery_limit=1,
        )
    )
    subset_rows = centerline_feature_subset_benchmark(
        mode_core_rows,
        max_subset_size=2,
        max_depth=2,
    )
    mode_frontier_rows = compress_redundant_mode_subset_frontier_rows(
        mode_only_subset_frontier_rows(subset_rows)
    )

    candidate_map: dict[str, list[tuple[str, ...]]] = {"compact": [], "extended": []}
    for rule_family in ("compact", "extended"):
        signatures: list[tuple[str, ...]] = []
        family_frontier = [
            row for row in mode_frontier_rows if row.rule_family == rule_family
        ]
        family_subset_rows = [
            row for row in subset_rows if row.rule_family == rule_family
        ]
        for row in family_frontier:
            signatures.append(_parse_feature_signature(row.feature_subset))
        for row in family_subset_rows[:top_k_subset_rows]:
            signatures.append(_parse_feature_signature(row.feature_subset))
        signatures.append(("center_variation",))

        deduped: list[tuple[str, ...]] = []
        seen: set[tuple[str, ...]] = set()
        for signature in signatures:
            if signature in seen:
                continue
            seen.add(signature)
            deduped.append(signature)
        candidate_map[rule_family] = deduped
    return candidate_map


def check_mode_only_candidate_isolation() -> None:
    expected = {
        rule_family: {", ".join(signature) if signature else "-" for signature in signatures}
        for rule_family, signatures in _manual_mode_only_candidate_map().items()
    }

    predictor_rows = predictor_family_comparison(
        retained_weight=1.0,
        mode_retained_weight=1.0,
        procedural_variant_limit=1,
        procedural_rediscovery_limit=1,
        max_subset_size=2,
        top_k_subset_rows=2,
    )
    generated_rows = generated_geometry_predictor_comparison(
        retained_weight=1.0,
        mode_retained_weight=1.0,
        geometry_variant_limit=1,
        procedural_variant_limit=1,
        procedural_rediscovery_limit=1,
        procedural_styles=("walk",),
        max_subset_size=2,
        top_k_subset_rows=2,
    )

    predictor_feature_sets = {
        rule_family: {
            row.feature_subset
            for row in predictor_rows
            if row.rule_family == rule_family
        }
        for rule_family in ("compact", "extended")
    }
    generated_feature_sets = {
        rule_family: {
            row.feature_subset
            for row in generated_rows
            if row.rule_family == rule_family
        }
        for rule_family in ("compact", "extended")
    }

    assert (
        predictor_feature_sets == expected
    ), "predictor_family_comparison candidate subsets diverged from the intended mode-only candidate map"
    assert (
        generated_feature_sets == expected
    ), "generated_geometry_predictor_comparison candidate subsets diverged from the intended mode-only candidate map"


def check_live_mechanism_split_driver() -> None:
    driver_source = (
        REPO_ROOT / "scripts" / "long_mechanism_family_split_analysis.py"
    ).read_text()
    assert (
        "mechanism_family_split_benchmark" in driver_source
    ), "mechanism split driver no longer calls the live helper"
    for stale_marker in (
        "AUDIT_LOG_PATH",
        "BROADER_LOG_PATH",
        "parse_parity_cell",
        "read_text(",
    ):
        assert (
            stale_marker not in driver_source
        ), f"mechanism split driver still contains stale log-parsing marker {stale_marker}"


def check_sparse_fallback_access_labels() -> None:
    helper_source = inspect.getsource(sparse_fallback_access_benchmark)
    assert (
        '== "sparse-structure"' in helper_source
    ), "sparse fallback access helper no longer keys off the corrected sparse-structure label"
    assert (
        '== "degree-profile"' not in helper_source
    ), "sparse fallback access helper regressed to the stale degree-profile label"


def main() -> None:
    print("benchmark regression audit: checking same-weight default", flush=True)
    check_same_weight_default()
    print("benchmark regression audit: checking mode-only candidate isolation", flush=True)
    check_mode_only_candidate_isolation()
    print("benchmark regression audit: checking sparse bridge addback visibility", flush=True)
    check_sparse_bridge_addback_visibility()
    print("benchmark regression audit: checking sparse fallback access labels", flush=True)
    check_sparse_fallback_access_labels()
    print("benchmark regression audit: checking live mechanism split driver", flush=True)
    check_live_mechanism_split_driver()
    print("benchmark regression audit: ok", flush=True)


if __name__ == "__main__":
    main()
