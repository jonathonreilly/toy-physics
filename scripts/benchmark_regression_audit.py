#!/usr/bin/env python3
"""Cheap regression checks for benchmark-path bugs we already fixed once."""

from __future__ import annotations

from dataclasses import astuple
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    build_generated_geometry_prediction_context,
    compact_threshold_proxy_bridge_sets,
    feature_subset_cardinality,
    resolve_sparse_bridge_feature_names,
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


def main() -> None:
    print("benchmark regression audit: checking same-weight default", flush=True)
    check_same_weight_default()
    print("benchmark regression audit: checking sparse bridge addback visibility", flush=True)
    check_sparse_bridge_addback_visibility()
    print("benchmark regression audit: ok", flush=True)


if __name__ == "__main__":
    main()
