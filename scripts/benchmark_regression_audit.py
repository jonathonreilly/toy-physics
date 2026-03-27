#!/usr/bin/env python3
"""Cheap regression checks for benchmark-path bugs we already fixed once."""

from __future__ import annotations

from dataclasses import astuple
import inspect
from pathlib import Path
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    ExtendedAtomicRouteOverlapRow,
    POCKET_WRAP_SUPPRESSOR_HISTORICAL_LIVE_VARIANT_LIMITS,
    _named_overlap_row,
    build_cross_dataset_prediction_context,
    build_generated_geometry_prediction_context,
    centerline_feature_subset_benchmark,
    compact_threshold_proxy_bridge_sets,
    compress_redundant_mode_subset_frontier_rows,
    feature_subset_cardinality,
    generated_geometry_predictor_comparison,
    mode_only_subset_frontier_rows,
    compact_route_map_summary,
    pocket_wrap_suppressor_mixed_bucket_axis_analysis,
    pocket_wrap_suppressor_latent_structure_analysis,
    pocket_wrap_suppressor_residual_bucket_rows,
    predictor_family_comparison,
    procedural_geometry_variants,
    resolve_sparse_bridge_feature_names,
    scenario_by_name,
    sparse_fallback_access_benchmark,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD,
    PRIMARY_SUPPORT_FAMILY_BUCKETS,
    SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    edge_identity_signature,
)
from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    parse_variant_limit as parse_low_overlap_variant_limit,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan import (  # noqa: E402
    FEATURE_NAMES as ADD4_EXCEPTION_FEATURE_NAMES,
    _matches_rule_text as add4_exception_matches_rule_text,
    build_bucket_rows as build_add4_exception_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules as evaluate_support_topology_rules,
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


def check_overlap_row_lookup_reversal() -> None:
    rows = [
        ExtendedAtomicRouteOverlapRow(
            ensemble_name="default",
            left_label="pocket",
            right_label="low-degree",
            left_support_fraction=0.40,
            right_support_fraction=0.60,
            left_implies_right=0.99,
            right_implies_left=0.66,
            jaccard=0.50,
        )
    ]
    direct = _named_overlap_row(rows, "default", "pocket", "low-degree")
    reversed_row = _named_overlap_row(rows, "default", "low-degree", "pocket")
    assert direct.left_implies_right == 0.99, "direct overlap lookup drifted"
    assert (
        reversed_row.left_implies_right == 0.66
        and reversed_row.right_implies_left == 0.99
    ), "reversed overlap lookup no longer swaps implication directions correctly"


def check_route_map_summary_avoids_threshold_models() -> None:
    helper_source = inspect.getsource(compact_route_map_summary)
    assert (
        "include_models=False" in helper_source
    ), "compact route-map summary regressed to building unused threshold-core model rows"


def check_support_family_transfer_bucket_rules_exclude_peer_band() -> None:
    script_source = (
        REPO_ROOT
        / "scripts"
        / "pocket_wrap_suppressor_low_overlap_support_family_transfer_bucket_rules.py"
    ).read_text()
    assert (
        "if row.high_bridge_left_low_count >= 0.5:" in script_source
    ), "support-family bucket rules regressed to mixing peer-band rows back into shared bucket scans"


def check_edge_identity_candidate_fraction_bounds() -> None:
    base_nodes, wrap_y = scenario_by_name("base", "taper-wrap")
    checked = 0
    for variant_name, nodes, _delta in procedural_geometry_variants(
        "base",
        "taper-wrap",
        base_nodes,
        wrap_y,
        variant_limit=8,
        style="local-morph",
    ):
        _events, numeric = edge_identity_signature(set(nodes))
        for metric_name in (
            "edge_identity_candidate_closed_fraction",
            "edge_identity_candidate_open_fraction",
        ):
            value = float(numeric[metric_name])
            assert 0.0 <= value <= 1.0, f"{metric_name} escaped [0,1]: {value}"
        checked += 1
    assert checked == 8, "expected to check the first 8 local-morph variants for fraction bounds"


def check_add4_exception_scan_uses_live_rule() -> None:
    script_source = (
        REPO_ROOT
        / "scripts"
        / "pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_add4_exception_scan.py"
    ).read_text()
    assert (
        "evaluate_rules(" in script_source and "_matches_rule_text" in script_source
    ), "add4 exception scan regressed to a frozen rule instead of deriving the live add4 rule"
    assert (
        "def _matches_add4_rule" not in script_source
    ), "add4 exception scan still contains the stale hard-coded rule path"


def check_add4_exception_scan_rule_eval_consistency() -> None:
    rows = build_add4_exception_rows(
        Path(
            "/Users/jonreilly/Projects/Physics/logs/"
            "2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt"
        )
    )
    rules = evaluate_support_topology_rules(
        rows,
        target_subtype="add4-sensitive",
        feature_names=ADD4_EXCEPTION_FEATURE_NAMES,
        predicate_limit=22,
        max_terms=3,
        row_limit=1,
    )
    assert rules, "add4 exception scan produced no live add4 rules"
    top = rules[0]

    tp = sum(
        1
        for row in rows
        if getattr(row, "subtype") == "add4-sensitive"
        and add4_exception_matches_rule_text(row, top.rule_text)
    )
    fp = sum(
        1
        for row in rows
        if getattr(row, "subtype") != "add4-sensitive"
        and add4_exception_matches_rule_text(row, top.rule_text)
    )
    fn = sum(
        1
        for row in rows
        if getattr(row, "subtype") == "add4-sensitive"
        and not add4_exception_matches_rule_text(row, top.rule_text)
    )
    assert (
        tp == top.tp and fp == top.fp and fn == top.fn
    ), "add4 exception rule-text matcher diverged from evaluate_rules confusion counts"


def check_low_overlap_variant_limit_parser_handles_renamed_logs() -> None:
    source_log = (
        REPO_ROOT
        / "logs"
        / "2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt"
    )
    text = source_log.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmpdir:
        renamed_log = Path(tmpdir) / "frozen_frontier_snapshot.txt"
        renamed_log.write_text(text, encoding="utf-8")
        parsed_limit = parse_low_overlap_variant_limit(renamed_log)
    assert (
        parsed_limit == 5504
    ), "low-overlap boundary parser regressed to filename-only variant-limit inference"


def check_active_suppressor_defaults_target_frozen_5504() -> None:
    boundary_source = inspect.getsource(pocket_wrap_suppressor_mixed_bucket_axis_analysis)
    assert (
        "variant_limit: int = 5504" in boundary_source
    ), "mixed-bucket helper default regressed away from the frozen 5504 checkpoint"
    residual_source = inspect.getsource(pocket_wrap_suppressor_residual_bucket_rows)
    assert (
        "variant_limit: int = 5504" in residual_source
    ), "residual-bucket helper default regressed away from the frozen 5504 checkpoint"

    mixed_script = (
        REPO_ROOT / "scripts" / "pocket_wrap_suppressor_mixed_bucket_axes.py"
    ).read_text()
    assert (
        'default=5504' in mixed_script
    ), "mixed-bucket runner default no longer points at the frozen 5504 checkpoint"

    residual_script = (
        REPO_ROOT / "scripts" / "pocket_wrap_suppressor_residual_bucket_rules.py"
    ).read_text()
    assert (
        'default=5504' in residual_script
    ), "residual-bucket runner default no longer points at the frozen 5504 checkpoint"


def check_latent_structure_entrypoint_is_historical_live_sampler() -> None:
    helper_source = inspect.getsource(pocket_wrap_suppressor_latent_structure_analysis)
    assert (
        POCKET_WRAP_SUPPRESSOR_HISTORICAL_LIVE_VARIANT_LIMITS == (512, 672, 912, 1168)
    ), "historical live latent-structure checkpoints drifted from the intended representative sample"
    assert (
        "POCKET_WRAP_SUPPRESSOR_HISTORICAL_LIVE_VARIANT_LIMITS" in helper_source
    ), "latent-structure helper no longer uses the shared historical live sample constant"

    latent_script = (
        REPO_ROOT / "scripts" / "pocket_wrap_suppressor_latent_structure.py"
    ).read_text()
    assert (
        "historical live latent-structure sampler" in latent_script
    ), "latent-structure runner no longer identifies itself as a historical live sampler"
    assert (
        "pocket_wrap_suppressor_frontier_compression.py" in latent_script
    ), "latent-structure runner no longer points to the canonical frozen-frontier compression workflow"


def check_primary_support_family_buckets_shared() -> None:
    assert (
        PRIMARY_SUPPORT_FAMILY_BUCKETS == ("rc0|ml0|c2", "rc0|ml1|c3")
    ), "shared primary support-family bucket set drifted"
    assert (
        SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD == 19.0
        and EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD == 71.0
    ), "shared residual-bucket thresholds drifted"
    scripts = (
        REPO_ROOT / "scripts" / "pocket_wrap_suppressor_low_overlap_support_family_transfer_scan.py",
        REPO_ROOT / "scripts" / "pocket_wrap_suppressor_low_overlap_support_family_transfer_primary_bucket_profiles.py",
        REPO_ROOT / "scripts" / "pocket_wrap_suppressor_low_overlap_support_family_transfer_satellites.py",
        REPO_ROOT / "scripts" / "pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py",
    )
    for script in scripts:
        text = script.read_text()
        assert (
            "PRIMARY_SUPPORT_FAMILY_BUCKETS" in text
        ), f"{script.name} no longer uses the shared primary support-family bucket set"
        assert (
            'PRIMARY_BUCKETS = ("rc0|ml0|c2", "rc0|ml1|c3")' not in text
            and 'PRIMARY_BUCKETS = {"rc0|ml0|c2", "rc0|ml1|c3"}' not in text
        ), f"{script.name} regressed to duplicating the primary support-family bucket literals"
    residual_text = (
        REPO_ROOT
        / "scripts"
        / "pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_nonpeer_core_residual_families.py"
    ).read_text()
    assert (
        "family_bucket_key_like" in residual_text
        and "residual_bucket_key_like" in residual_text
    ), "baseline non-peer residual follow-on no longer uses shared bucket-key helpers"
    assert (
        ">= 19.0" not in residual_text and ">= 71.0" not in residual_text
    ), "baseline non-peer residual follow-on regressed to hard-coded residual bucket thresholds"


def main() -> None:
    print("benchmark regression audit: checking same-weight default", flush=True)
    check_same_weight_default()
    print("benchmark regression audit: checking mode-only candidate isolation", flush=True)
    check_mode_only_candidate_isolation()
    print("benchmark regression audit: checking sparse bridge addback visibility", flush=True)
    check_sparse_bridge_addback_visibility()
    print("benchmark regression audit: checking sparse fallback access labels", flush=True)
    check_sparse_fallback_access_labels()
    print("benchmark regression audit: checking overlap-row lookup reversal", flush=True)
    check_overlap_row_lookup_reversal()
    print("benchmark regression audit: checking route-map threshold-model avoidance", flush=True)
    check_route_map_summary_avoids_threshold_models()
    print("benchmark regression audit: checking support-family bucket peer-band exclusion", flush=True)
    check_support_family_transfer_bucket_rules_exclude_peer_band()
    print("benchmark regression audit: checking edge-identity candidate fraction bounds", flush=True)
    check_edge_identity_candidate_fraction_bounds()
    print("benchmark regression audit: checking add4 exception scan live-rule path", flush=True)
    check_add4_exception_scan_uses_live_rule()
    print("benchmark regression audit: checking add4 exception rule-eval consistency", flush=True)
    check_add4_exception_scan_rule_eval_consistency()
    print("benchmark regression audit: checking low-overlap variant-limit parser on renamed logs", flush=True)
    check_low_overlap_variant_limit_parser_handles_renamed_logs()
    print("benchmark regression audit: checking active suppressor defaults target frozen 5504", flush=True)
    check_active_suppressor_defaults_target_frozen_5504()
    print("benchmark regression audit: checking latent-structure entrypoint role", flush=True)
    check_latent_structure_entrypoint_is_historical_live_sampler()
    print("benchmark regression audit: checking shared primary support-family buckets", flush=True)
    check_primary_support_family_buckets_shared()
    print("benchmark regression audit: checking live mechanism split driver", flush=True)
    check_live_mechanism_split_driver()
    print("benchmark regression audit: ok", flush=True)


if __name__ == "__main__":
    main()
