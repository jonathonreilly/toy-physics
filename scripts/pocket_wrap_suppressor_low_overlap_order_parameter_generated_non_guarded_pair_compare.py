#!/usr/bin/env python3
"""Project the generated anchor-balance boundary onto broader historical cohorts."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import make_dataclass, replace
from datetime import datetime
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    matches_rule_text,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    build_rows_with_trees,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_full_bucket_exact_projection import (  # noqa: E402
    OUTSIDE_GATE_PAIR_ONLY_RULE,
    build_rows as build_historical_rows,
    predict_branch,
    predict_subtype,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_generated_support_collapse_guard_projection import (  # noqa: E402
    guarded_predict_branch,
    guarded_predict_subtype,
    is_support_collapse,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)
from toy_event_physics import _extended_ge6_dpadj_trees, benchmark_packs  # noqa: E402


TARGET_CLASS = "generated-transfer-failure"
HISTORICAL_PAIR_CLASS = "historical-pair-only"
HISTORICAL_ADD1_CLASS = "historical-add1"
HISTORICAL_ADD4_CLASS = "historical-add4"
GENERATED_STABLE_CLASS = "generated-stable-nearby"
OUTER_GUARDRAIL_CLASS = "generated-outer-guardrail"
ANCHOR_BAND_RULE = (
    "anchor_closure_intensity_gap <= 2.333 and anchor_closure_intensity_gap >= -2.000"
)
REFINED_ANCHOR_BAND_RULE = f"{ANCHOR_BAND_RULE} and mid_anchor_closure_peak <= 10.000"
SHOULDER_RULE = "anchor_deep_share_gap >= 0.250"
THROAT_RULE = "closure_load <= 24.500"
DEFAULT_NEARBY_ENSEMBLES = ("default", "broader", "wider", "ultra", "mega")
SPARSE_GUARDRAIL_SPECS = (
    ("rect-wrap", ("ultra", "mega")),
    ("rect-hard", ("ultra", "mega")),
)
FEATURES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_high_count",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
)
TARGET_SPECS = (
    ("taper-wrap", ("ultra", "mega"), ("base:taper-wrap:mode-mix-f",)),
    (
        "skew-wrap",
        ("default", "broader", "wider", "ultra", "mega"),
        ("base:skew-wrap:local-morph-c", "base:skew-wrap:mode-mix-d"),
    ),
)
FOCUSED_ADD4_SOURCES = (
    "base:taper-wrap:local-morph-ዦ",
    "base:taper-wrap:local-morph-ᓭ",
)
FOCUSED_GENERATED_SOURCES = (
    "base:skew-wrap:local-morph-c",
    "base:skew-wrap:mode-mix-d",
)
FOCUSED_MODE_MIX_F_SOURCE = "base:taper-wrap:mode-mix-f"
FOCUSED_MODE_MIX_F_CLASS = "generated-mode-mix-f-focus"
FOCUSED_OUTER_RECT_SOURCE = "base:rect-wrap:local-morph-f"
FOCUSED_OUTER_RECT_CLASS = "generated-outer-rect-focus"
FOCUSED_SUPPORT_LAYOUT_FEATURES = (
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "high_bridge_high_count",
    "edge_identity_support_edge_density",
)
FOCUSED_MODE_MIX_F_FEATURES = (
    "support_load",
    "closure_load",
    "edge_identity_event_count",
)
FOCUSED_OUTER_RECT_FEATURES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "edge_identity_event_count",
)
FOCUSED_DELTA_FEATURES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "edge_identity_support_edge_density",
)
FOCUSED_MODE_MIX_F_DELTA_FEATURES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
)
FOCUSED_OUTER_RECT_DELTA_FEATURES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "edge_identity_event_count",
)
ENSEMBLE_ORDER = {name: index for index, name in enumerate(DEFAULT_NEARBY_ENSEMBLES)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--pack-name", default="base")
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--row-limit", type=int, default=12)
    parser.add_argument("--nearby-limit", type=int, default=12)
    parser.add_argument(
        "--nearby-ensembles",
        nargs="+",
        default=DEFAULT_NEARBY_ENSEMBLES,
    )
    return parser


def _format_counts(rows: list[object], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _format_membership(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    if not counts:
        return "0 (none)"
    return f"{len(rows)} ({', '.join(f'{key}:{counts[key]}' for key in sorted(counts))})"


def _feature_ranges(rows: list[object]) -> dict[str, tuple[float, float]]:
    return {
        feature: (
            min(float(getattr(row, feature)) for row in rows),
            max(float(getattr(row, feature)) for row in rows),
        )
        for feature in FEATURES
    }


def _nearest_row(target: object, candidates: list[object]) -> tuple[object, float]:
    best_row = candidates[0]
    best_distance = sum(
        abs(float(getattr(target, feature)) - float(getattr(best_row, feature)))
        for feature in FEATURES
    )
    for candidate in candidates[1:]:
        distance = sum(
            abs(float(getattr(target, feature)) - float(getattr(candidate, feature)))
            for feature in FEATURES
        )
        if distance < best_distance:
            best_row = candidate
            best_distance = distance
    return best_row, best_distance


def _row_key(row: object) -> tuple[str, str]:
    return getattr(row, "ensemble_name"), getattr(row, "source_name")


def _actual_subtype(row: object) -> str:
    return getattr(row, "actual_subtype", getattr(row, "subtype"))


def _predicted_subtype(row: object) -> str:
    if hasattr(row, "predicted_subtype"):
        return getattr(row, "predicted_subtype")
    return guarded_predict_subtype(row)


def _predicted_branch(row: object) -> str:
    if hasattr(row, "predicted_branch"):
        return getattr(row, "predicted_branch")
    return guarded_predict_branch(row)


def _pick_representative_rows(
    rows: list[object],
    source_names: tuple[str, ...],
) -> list[object]:
    selected: list[object] = []
    for source_name in source_names:
        source_rows = [
            row for row in rows if getattr(row, "source_name") == source_name
        ]
        if not source_rows:
            continue
        source_rows.sort(
            key=lambda row: (
                ENSEMBLE_ORDER.get(
                    getattr(row, "ensemble_name"),
                    len(ENSEMBLE_ORDER),
                ),
                getattr(row, "ensemble_name"),
            )
        )
        selected.append(source_rows[0])
    return selected


def generated_scenarios(pack_name: str) -> list[str]:
    for current_pack_name, scenarios in benchmark_packs():
        if current_pack_name == pack_name:
            return [scenario_name for scenario_name, _nodes, _wrap_y in scenarios]
    raise KeyError(f"unknown benchmark pack: {pack_name}")


def prioritized_generated_scenarios(pack_name: str) -> list[str]:
    scenario_names = generated_scenarios(pack_name)
    ordered: list[str] = []
    for scenario_name, _ensembles, _targets in TARGET_SPECS:
        if scenario_name in scenario_names and scenario_name not in ordered:
            ordered.append(scenario_name)
    for scenario_name, _ensembles, _targets in TARGET_SPECS:
        if "-" not in scenario_name:
            continue
        root, suffix = scenario_name.rsplit("-", 1)
        alternate = f"{root}-{'hard' if suffix == 'wrap' else 'wrap'}"
        if alternate in scenario_names and alternate not in ordered:
            ordered.append(alternate)
    return ordered


def build_generated_target_rows(
    pack_name: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
) -> list[object]:
    target_rows: list[object] = []
    for scenario_name, ensembles, target_sources in TARGET_SPECS:
        source_set = set(target_sources)
        for ensemble_name in ensembles:
            rows = build_rows_with_trees(
                ensemble_name,
                pack_name,
                scenario_name,
                ge6_tree=ge6_tree,
                dpadj_tree=dpadj_tree,
            )
            target_rows.extend(
                row
                for row in rows
                if getattr(row, "source_name") in source_set and not is_support_collapse(row)
            )
    target_rows.sort(
        key=lambda row: (
            getattr(row, "source_name"),
            getattr(row, "ensemble_name"),
        )
    )
    return target_rows


def build_generated_stable_rows(
    pack_name: str,
    target_rows: list[object],
    *,
    ge6_tree: object,
    dpadj_tree: object,
    ensemble_names: tuple[str, ...],
    limit: int,
) -> tuple[list[object], list[str], int]:
    target_keys = {_row_key(row) for row in target_rows}
    candidate_rows: list[tuple[float, object]] = []
    scenarios_scanned: list[str] = []

    for scenario_name in prioritized_generated_scenarios(pack_name):
        scenarios_scanned.append(scenario_name)
        for ensemble_name in ensemble_names:
            rows = build_rows_with_trees(
                ensemble_name,
                pack_name,
                scenario_name,
                ge6_tree=ge6_tree,
                dpadj_tree=dpadj_tree,
            )
            for row in rows:
                if _row_key(row) in target_keys or is_support_collapse(row):
                    continue
                if guarded_predict_subtype(row) != getattr(row, "subtype"):
                    continue
                _nearest_target, distance = _nearest_row(row, target_rows)
                candidate_rows.append((distance, row))
        if limit > 0 and len(candidate_rows) >= limit:
            break

    candidate_rows.sort(
        key=lambda item: (
            item[0],
            getattr(item[1], "source_name"),
            getattr(item[1], "ensemble_name"),
        )
    )
    selected_rows = [row for _distance, row in candidate_rows[:limit]] if limit > 0 else []
    return selected_rows, scenarios_scanned, len(candidate_rows)


def build_sparse_guardrail_rows(
    pack_name: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
) -> tuple[list[object], list[object], list[str], int]:
    selected_rows: list[object] = []
    noncollapse_rows: list[object] = []
    scanned_specs: list[str] = []
    noncollapse_total = 0

    for scenario_name, ensembles in SPARSE_GUARDRAIL_SPECS:
        scanned_specs.append(f"{scenario_name}:{'/'.join(ensembles)}")
        for ensemble_name in ensembles:
            rows = build_rows_with_trees(
                ensemble_name,
                pack_name,
                scenario_name,
                ge6_tree=ge6_tree,
                dpadj_tree=dpadj_tree,
            )
            for row in rows:
                if is_support_collapse(row):
                    continue
                noncollapse_total += 1
                noncollapse_rows.append(row)
                if matches_rule_text(row, REFINED_ANCHOR_BAND_RULE):
                    selected_rows.append(row)

    selected_rows.sort(
        key=lambda row: (
            getattr(row, "source_name"),
            getattr(row, "ensemble_name"),
        )
    )
    noncollapse_rows.sort(
        key=lambda row: (
            getattr(row, "source_name"),
            getattr(row, "ensemble_name"),
        )
    )
    return selected_rows, noncollapse_rows, scanned_specs, noncollapse_total


def build_comparison_rows(
    generated_rows: list[object],
    historical_pair_rows: list[object],
    historical_add1_rows: list[object],
    historical_add4_rows: list[object],
    generated_stable_rows: list[object],
    outer_guardrail_rows: list[object],
) -> list[object]:
    row_cls = make_dataclass(
        "GeneratedHistoricalPairCompareRow",
        [
            ("origin", str),
            ("source_name", str),
            ("subtype", str),
            ("actual_subtype", str),
            ("predicted_subtype", str),
            ("predicted_branch", str),
            ("ensemble_name", str),
            ("style", str),
            ("support_load", float),
            ("closure_load", float),
            ("mid_anchor_closure_peak", float),
            ("anchor_closure_intensity_gap", float),
            ("anchor_deep_share_gap", float),
            ("high_bridge_high_count", float),
            ("high_bridge_right_count", float),
            ("high_bridge_right_low_count", float),
            ("edge_identity_event_count", float),
            ("edge_identity_support_edge_density", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for row in generated_rows:
        rows.append(
            row_cls(
                origin="generated-failure",
                source_name=getattr(row, "source_name"),
                subtype=TARGET_CLASS,
                actual_subtype=getattr(row, "subtype"),
                predicted_subtype=guarded_predict_subtype(row),
                predicted_branch=guarded_predict_branch(row),
                ensemble_name=getattr(row, "ensemble_name"),
                style=getattr(row, "style"),
                support_load=float(getattr(row, "support_load")),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                high_bridge_high_count=float(getattr(row, "high_bridge_high_count")),
                high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
                high_bridge_right_low_count=float(
                    getattr(row, "high_bridge_right_low_count")
                ),
                edge_identity_event_count=float(
                    getattr(row, "edge_identity_event_count")
                ),
                edge_identity_support_edge_density=float(
                    getattr(row, "edge_identity_support_edge_density")
                ),
            )
        )
    for row in historical_pair_rows:
        rows.append(
            row_cls(
                origin="historical-pair",
                source_name=getattr(row, "source_name"),
                subtype=HISTORICAL_PAIR_CLASS,
                actual_subtype=getattr(row, "subtype"),
                predicted_subtype=predict_subtype(row),
                predicted_branch=predict_branch(row),
                ensemble_name="historical",
                style="historical",
                support_load=float(getattr(row, "support_load")),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                high_bridge_high_count=float(getattr(row, "high_bridge_high_count")),
                high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
                high_bridge_right_low_count=float(
                    getattr(row, "high_bridge_right_low_count")
                ),
                edge_identity_event_count=float(
                    getattr(row, "edge_identity_event_count")
                ),
                edge_identity_support_edge_density=float(
                    getattr(row, "edge_identity_support_edge_density")
                ),
            )
        )
    for row in historical_add1_rows:
        rows.append(
            row_cls(
                origin="historical-add1",
                source_name=getattr(row, "source_name"),
                subtype=HISTORICAL_ADD1_CLASS,
                actual_subtype=getattr(row, "subtype"),
                predicted_subtype=predict_subtype(row),
                predicted_branch=predict_branch(row),
                ensemble_name="historical",
                style="historical",
                support_load=float(getattr(row, "support_load")),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                high_bridge_high_count=float(getattr(row, "high_bridge_high_count")),
                high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
                high_bridge_right_low_count=float(
                    getattr(row, "high_bridge_right_low_count")
                ),
                edge_identity_event_count=float(
                    getattr(row, "edge_identity_event_count")
                ),
                edge_identity_support_edge_density=float(
                    getattr(row, "edge_identity_support_edge_density")
                ),
            )
        )
    for row in historical_add4_rows:
        rows.append(
            row_cls(
                origin="historical-add4",
                source_name=getattr(row, "source_name"),
                subtype=HISTORICAL_ADD4_CLASS,
                actual_subtype=getattr(row, "subtype"),
                predicted_subtype=predict_subtype(row),
                predicted_branch=predict_branch(row),
                ensemble_name="historical",
                style="historical",
                support_load=float(getattr(row, "support_load")),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                high_bridge_high_count=float(getattr(row, "high_bridge_high_count")),
                high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
                high_bridge_right_low_count=float(
                    getattr(row, "high_bridge_right_low_count")
                ),
                edge_identity_event_count=float(
                    getattr(row, "edge_identity_event_count")
                ),
                edge_identity_support_edge_density=float(
                    getattr(row, "edge_identity_support_edge_density")
                ),
            )
        )
    for row in generated_stable_rows:
        rows.append(
            row_cls(
                origin="generated-stable",
                source_name=getattr(row, "source_name"),
                subtype=GENERATED_STABLE_CLASS,
                actual_subtype=getattr(row, "subtype"),
                predicted_subtype=guarded_predict_subtype(row),
                predicted_branch=guarded_predict_branch(row),
                ensemble_name=getattr(row, "ensemble_name"),
                style=getattr(row, "style"),
                support_load=float(getattr(row, "support_load")),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                high_bridge_high_count=float(getattr(row, "high_bridge_high_count")),
                high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
                high_bridge_right_low_count=float(
                    getattr(row, "high_bridge_right_low_count")
                ),
                edge_identity_event_count=float(
                    getattr(row, "edge_identity_event_count")
                ),
                edge_identity_support_edge_density=float(
                    getattr(row, "edge_identity_support_edge_density")
                ),
            )
        )
    for row in outer_guardrail_rows:
        rows.append(
            row_cls(
                origin="generated-outer-guardrail",
                source_name=getattr(row, "source_name"),
                subtype=OUTER_GUARDRAIL_CLASS,
                actual_subtype=getattr(row, "subtype"),
                predicted_subtype=guarded_predict_subtype(row),
                predicted_branch=guarded_predict_branch(row),
                ensemble_name=getattr(row, "ensemble_name"),
                style=getattr(row, "style"),
                support_load=float(getattr(row, "support_load")),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                high_bridge_high_count=float(getattr(row, "high_bridge_high_count")),
                high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
                high_bridge_right_low_count=float(
                    getattr(row, "high_bridge_right_low_count")
                ),
                edge_identity_event_count=float(
                    getattr(row, "edge_identity_event_count")
                ),
                edge_identity_support_edge_density=float(
                    getattr(row, "edge_identity_support_edge_density")
                ),
            )
        )
    return rows


def render_feature_ranges(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    label_attr = "actual_subtype" if rows and hasattr(rows[0], "actual_subtype") else "subtype"
    lines.append(f"rows={len(rows)} ({_format_counts(rows, attr=label_attr)})")
    for feature, (feature_min, feature_max) in _feature_ranges(rows).items():
        lines.append(f"{feature}: min={feature_min:.3f} max={feature_max:.3f}")
    return "\n".join(lines)


def render_shared_out_of_range(
    title: str,
    target_rows: list[object],
    historical_ranges: dict[str, tuple[float, float]],
) -> str:
    lines = [title, "=" * len(title)]
    for feature in FEATURES:
        below = 0
        above = 0
        feature_min, feature_max = historical_ranges[feature]
        for row in target_rows:
            value = float(getattr(row, feature))
            if value < feature_min:
                below += 1
            if value > feature_max:
                above += 1
        lines.append(
            f"{feature}: below_hist_min={below} above_hist_max={above} of {len(target_rows)}"
        )
    return "\n".join(lines)


def render_rows(
    title: str,
    rows: list[object],
    *,
    reference_rows: list[object],
    reference_label: str,
    band_rule: str,
    historical_ranges: dict[str, tuple[float, float]] | None = None,
) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        nearest_reference, distance = _nearest_row(row, reference_rows)
        out_of_range: list[str] = []
        if historical_ranges is not None:
            for feature in FEATURES:
                feature_min, feature_max = historical_ranges[feature]
                value = float(getattr(row, feature))
                if value < feature_min:
                    out_of_range.append(f"{feature}<min")
                elif value > feature_max:
                    out_of_range.append(f"{feature}>max")
        lines.append(
            f"{getattr(row, 'ensemble_name')}:{getattr(row, 'source_name')} "
            f"style={getattr(row, 'style')} actual={_actual_subtype(row)} "
            f"predicted={_predicted_subtype(row)} branch={_predicted_branch(row)} "
            f"anchor_band={'Y' if matches_rule_text(row, band_rule) else 'n'} "
            f"nearest_{reference_label}={getattr(nearest_reference, 'source_name')} distance={distance:.3f} "
            f"out_of_range={'none' if not out_of_range else ','.join(out_of_range)}"
        )
        for feature in FEATURES:
            lines.append(f"  {feature}={float(getattr(row, feature)):.3f}")
    return "\n".join(lines)


def render_rule_projection(title: str, rows: list[object], rule_text: str) -> str:
    lines = [title, "=" * len(title), f"rule={rule_text}"]
    for cohort in (
        TARGET_CLASS,
        HISTORICAL_PAIR_CLASS,
        HISTORICAL_ADD1_CLASS,
        HISTORICAL_ADD4_CLASS,
        GENERATED_STABLE_CLASS,
        OUTER_GUARDRAIL_CLASS,
    ):
        cohort_rows = [row for row in rows if getattr(row, "subtype") == cohort]
        if not cohort_rows:
            continue
        matched_rows = [row for row in cohort_rows if matches_rule_text(row, rule_text)]
        lines.append(
            f"{cohort}: hits={len(matched_rows)}/{len(cohort_rows)} "
            f"matched={_format_counts(matched_rows, attr='actual_subtype')}"
        )
        if matched_rows:
            shown = ", ".join(
                f"{getattr(row, 'ensemble_name')}:{getattr(row, 'source_name')}"
                for row in matched_rows[:6]
            )
            lines.append(f"  examples={shown}")
    return "\n".join(lines)


def render_rule_table(title: str, rows: list[object], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | exact | corr | tp/fp/fn | matched(class counts) | residual(class counts)",
        "-----+-------+------+----------+------------------------+-------------------------",
    ]
    for rule in rules:
        matched = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        residual = [row for row in rows if not matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {'Y' if rule.exact else 'n':^5} | "
            f"{rule.correct:>2}/{rule.total:<2} | {rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{_format_membership(matched)} | {_format_membership(residual)}"
        )
    return "\n".join(lines)


def render_pairwise_deltas(
    title: str,
    left_rows: list[object],
    right_rows: list[object],
    *,
    delta_features: tuple[str, ...],
) -> str:
    lines = [title, "=" * len(title)]
    if not left_rows or not right_rows:
        lines.append("none")
        return "\n".join(lines)
    for left in left_rows:
        for right in right_rows:
            distance = sum(
                abs(float(getattr(left, feature)) - float(getattr(right, feature)))
                for feature in FEATURES
            )
            lines.append(
                f"{getattr(left, 'ensemble_name')}:{getattr(left, 'source_name')} "
                f"minus {getattr(right, 'ensemble_name')}:{getattr(right, 'source_name')} "
                f"distance={distance:.3f}"
            )
            for feature in delta_features:
                left_value = float(getattr(left, feature))
                right_value = float(getattr(right, feature))
                lines.append(
                    f"  {feature}={left_value - right_value:+.3f} "
                    f"({left_value:.3f} vs {right_value:.3f})"
                )
    return "\n".join(lines)


def _translation_label(row: object) -> str:
    if matches_rule_text(row, THROAT_RULE):
        return "low-support-throat"
    if matches_rule_text(row, SHOULDER_RULE):
        return "right/deep-shoulder"
    return "outside-current-translation"


def render_translation_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    counts = Counter(_translation_label(row) for row in rows)
    lines.append(
        "translation_counts="
        + ", ".join(f"{label}:{counts[label]}" for label in sorted(counts))
    )
    for row in rows:
        lines.append(
            f"{getattr(row, 'ensemble_name')}:{getattr(row, 'source_name')} "
            f"actual={_actual_subtype(row)} predicted={_predicted_subtype(row)} "
            f"translation={_translation_label(row)}"
        )
        for feature in (
            "support_load",
            "closure_load",
            "mid_anchor_closure_peak",
            "anchor_closure_intensity_gap",
            "anchor_deep_share_gap",
            "high_bridge_right_count",
            "edge_identity_event_count",
        ):
            lines.append(f"  {feature}={float(getattr(row, feature)):.3f}")
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"generated non-guarded pair compare started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    historical_rows = build_historical_rows(frontier_log)
    historical_pair_rows = [
        row
        for row in historical_rows
        if getattr(row, "subtype") == "pair-only-sensitive"
    ]
    historical_add1_rows = [
        row for row in historical_rows if getattr(row, "subtype") == "add1-sensitive"
    ]
    historical_add4_rows = [
        row for row in historical_rows if getattr(row, "subtype") == "add4-sensitive"
    ]

    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees(retained_weight=1.0)
    generated_rows = build_generated_target_rows(
        args.pack_name,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )
    generated_stable_rows, nearby_scenarios_scanned, generated_stable_candidate_total = (
        build_generated_stable_rows(
            args.pack_name,
            generated_rows,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            ensemble_names=tuple(dict.fromkeys(args.nearby_ensembles)),
            limit=args.nearby_limit,
        )
    )
    (
        outer_guardrail_rows,
        outer_guardrail_noncollapse_rows,
        outer_guardrail_scanned,
        outer_guardrail_noncollapse_total,
    ) = (
        build_sparse_guardrail_rows(
            args.pack_name,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
        )
    )
    rows = build_comparison_rows(
        generated_rows,
        historical_pair_rows,
        historical_add1_rows,
        historical_add4_rows,
        generated_stable_rows,
        outer_guardrail_rows,
    )
    historical_pair_ranges = _feature_ranges(historical_pair_rows)
    generated_ranges = _feature_ranges(generated_rows)

    one_feature_rules = evaluate_rules(
        rows,
        target_subtype=TARGET_CLASS,
        feature_names=list(FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=1,
        row_limit=args.row_limit,
    )
    compact_rules = evaluate_rules(
        rows,
        target_subtype=TARGET_CLASS,
        feature_names=list(FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=3,
        row_limit=args.row_limit,
    )

    hist_pair_hits = [
        row
        for row in historical_pair_rows
        if predict_subtype(row) == "pair-only-sensitive"
    ]
    hist_add1_hits = [
        row for row in historical_add1_rows if predict_subtype(row) == "add1-sensitive"
    ]
    hist_add4_hits = [
        row for row in historical_add4_rows if predict_subtype(row) == "add4-sensitive"
    ]
    generated_pair_hits = [
        row
        for row in generated_rows
        if guarded_predict_subtype(row) == "pair-only-sensitive"
    ]
    anchor_band_hits = [
        row for row in rows if matches_rule_text(row, ANCHOR_BAND_RULE)
    ]
    anchor_band_false_positives = [
        row
        for row in rows
        if getattr(row, "subtype") != TARGET_CLASS
        and matches_rule_text(row, ANCHOR_BAND_RULE)
    ]
    anchor_band_false_negatives = [
        row
        for row in rows
        if getattr(row, "subtype") == TARGET_CLASS
        and not matches_rule_text(row, ANCHOR_BAND_RULE)
    ]
    anchor_band_add4_rows = [
        row
        for row in rows
        if getattr(row, "subtype") == HISTORICAL_ADD4_CLASS
        and matches_rule_text(row, ANCHOR_BAND_RULE)
    ]
    anchor_band_focus_rows = [
        row
        for row in rows
        if matches_rule_text(row, ANCHOR_BAND_RULE)
        and getattr(row, "subtype") in (TARGET_CLASS, HISTORICAL_ADD4_CLASS)
    ]
    anchor_band_focus_one_feature_rules = evaluate_rules(
        anchor_band_focus_rows,
        target_subtype=TARGET_CLASS,
        feature_names=list(FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=1,
        row_limit=args.row_limit,
    )
    anchor_band_focus_compact_rules = evaluate_rules(
        anchor_band_focus_rows,
        target_subtype=TARGET_CLASS,
        feature_names=list(FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=3,
        row_limit=args.row_limit,
    )
    focused_generated_rows = _pick_representative_rows(
        [
            row
            for row in rows
            if getattr(row, "subtype") == TARGET_CLASS
            and getattr(row, "source_name") in FOCUSED_GENERATED_SOURCES
        ],
        FOCUSED_GENERATED_SOURCES,
    )
    focused_add4_rows = _pick_representative_rows(
        [
            row
            for row in rows
            if getattr(row, "subtype") == HISTORICAL_ADD4_CLASS
            and getattr(row, "source_name") in FOCUSED_ADD4_SOURCES
        ],
        FOCUSED_ADD4_SOURCES,
    )
    focused_mode_mix_f_rows = _pick_representative_rows(
        [
            row
            for row in rows
            if getattr(row, "subtype") == TARGET_CLASS
            and getattr(row, "source_name") == FOCUSED_MODE_MIX_F_SOURCE
        ],
        (FOCUSED_MODE_MIX_F_SOURCE,),
    )
    focused_support_layout_rows = focused_generated_rows + focused_add4_rows
    focused_support_layout_one_feature_rules = evaluate_rules(
        focused_support_layout_rows,
        target_subtype=TARGET_CLASS,
        feature_names=list(FOCUSED_SUPPORT_LAYOUT_FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=1,
        row_limit=args.row_limit,
    )
    focused_support_layout_compact_rules = evaluate_rules(
        focused_support_layout_rows,
        target_subtype=TARGET_CLASS,
        feature_names=list(FOCUSED_SUPPORT_LAYOUT_FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=3,
        row_limit=args.row_limit,
    )
    focused_mode_mix_f_focus_rows = [
        replace(row, subtype=FOCUSED_MODE_MIX_F_CLASS)
        for row in focused_mode_mix_f_rows
    ] + focused_generated_rows + focused_add4_rows
    focused_mode_mix_f_one_feature_rules = evaluate_rules(
        focused_mode_mix_f_focus_rows,
        target_subtype=FOCUSED_MODE_MIX_F_CLASS,
        feature_names=list(FOCUSED_MODE_MIX_F_FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=1,
        row_limit=args.row_limit,
    )
    focused_mode_mix_f_compact_rules = evaluate_rules(
        focused_mode_mix_f_focus_rows,
        target_subtype=FOCUSED_MODE_MIX_F_CLASS,
        feature_names=list(FOCUSED_MODE_MIX_F_FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=3,
        row_limit=args.row_limit,
    )
    focused_outer_rect_rows = [
        row
        for row in outer_guardrail_noncollapse_rows
        if getattr(row, "source_name") == FOCUSED_OUTER_RECT_SOURCE
    ]
    focused_outer_rect_focus_rows = [
        replace(row, subtype=FOCUSED_OUTER_RECT_CLASS)
        for row in focused_outer_rect_rows
    ] + focused_generated_rows + focused_add4_rows + focused_mode_mix_f_rows
    focused_outer_rect_one_feature_rules = evaluate_rules(
        focused_outer_rect_focus_rows,
        target_subtype=FOCUSED_OUTER_RECT_CLASS,
        feature_names=list(FOCUSED_OUTER_RECT_FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=1,
        row_limit=args.row_limit,
    )
    focused_outer_rect_compact_rules = evaluate_rules(
        focused_outer_rect_focus_rows,
        target_subtype=FOCUSED_OUTER_RECT_CLASS,
        feature_names=list(FOCUSED_OUTER_RECT_FEATURES),
        predicate_limit=args.predicate_limit,
        max_terms=3,
        row_limit=args.row_limit,
    )

    print()
    print("Generated Non-Guarded Pair Compare")
    print("==================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"historical_pair_rows={len(historical_pair_rows)}")
    print(f"historical_add1_rows={len(historical_add1_rows)}")
    print(f"historical_add4_rows={len(historical_add4_rows)}")
    print(f"generated_target_rows={len(generated_rows)} ({_format_counts(generated_rows)})")
    print(
        f"generated_stable_nearby_rows={len(generated_stable_rows)} "
        f"from_candidates={generated_stable_candidate_total}"
    )
    print("generated_nearby_ensembles=" + ",".join(dict.fromkeys(args.nearby_ensembles)))
    print("generated_nearby_scenarios_scanned=" + ",".join(nearby_scenarios_scanned))
    print(
        f"generated_outer_guardrail_rows={len(outer_guardrail_rows)} "
        f"from_noncollapse={outer_guardrail_noncollapse_total}"
    )
    print("generated_outer_guardrail_scanned=" + ",".join(outer_guardrail_scanned))
    print(
        "generated_targets="
        + ",".join(
            f"{scenario}:{'/'.join(ensembles)}:{'/'.join(source_names)}"
            for scenario, ensembles, source_names in TARGET_SPECS
        )
    )
    print(f"outside_gate_pair_only_rule={OUTSIDE_GATE_PAIR_ONLY_RULE}")
    print(
        f"historical_pair_rule_hits={len(hist_pair_hits)}/{len(historical_pair_rows)} "
        f"historical_add1_rule_hits={len(hist_add1_hits)}/{len(historical_add1_rows)} "
        f"historical_add4_rule_hits={len(hist_add4_hits)}/{len(historical_add4_rows)} "
        f"generated_pair_rule_hits={len(generated_pair_hits)}/{len(generated_rows)}"
    )
    print(
        f"anchor_band_hits={len(anchor_band_hits)}/{len(rows)} "
        f"anchor_band_add4_hits={len(anchor_band_add4_rows)}/{len(historical_add4_rows)} "
        f"anchor_band_false_positives={len(anchor_band_false_positives)} "
        f"anchor_band_false_negatives={len(anchor_band_false_negatives)}"
    )
    print()
    print(render_feature_ranges("Historical pair-only ranges", historical_pair_rows))
    print()
    print(render_feature_ranges("Historical add1 ranges", historical_add1_rows))
    print()
    print(render_feature_ranges("Historical add4 ranges", historical_add4_rows))
    print()
    print(render_feature_ranges("Generated non-guarded target ranges", generated_rows))
    print()
    print(
        render_shared_out_of_range(
            "Generated rows outside historical pair-only ranges",
            generated_rows,
            historical_pair_ranges,
        )
    )
    if generated_stable_rows:
        print()
        print(render_feature_ranges("Generated stable nearby ranges", generated_stable_rows))
    if outer_guardrail_rows:
        print()
        print(render_feature_ranges("Generated outer guardrail ranges", outer_guardrail_rows))
    print()
    print(render_rule_projection("Anchor-band projection", rows, ANCHOR_BAND_RULE))
    print()
    print(render_rule_projection("Refined anchor-band projection", rows, REFINED_ANCHOR_BAND_RULE))
    print()
    print(
        render_rows(
            "Generated target rows",
            generated_rows,
            reference_rows=historical_pair_rows,
            reference_label="hist_pair",
            band_rule=ANCHOR_BAND_RULE,
            historical_ranges=historical_pair_ranges,
        )
    )
    if generated_stable_rows:
        print()
        print(
            render_rows(
                "Generated stable nearby rows",
                generated_stable_rows,
                reference_rows=generated_rows,
                reference_label="target",
                band_rule=ANCHOR_BAND_RULE,
            )
        )
    if outer_guardrail_rows:
        print()
        print(
            render_rows(
                "Generated outer guardrail rows",
                outer_guardrail_rows,
                reference_rows=generated_rows,
                reference_label="target",
                band_rule=REFINED_ANCHOR_BAND_RULE,
            )
        )
        print()
        print(
            render_translation_rows(
                "Generated outer guardrail shoulder/throat translation",
                outer_guardrail_rows,
            )
        )
    if anchor_band_false_positives:
        print()
        print(
            render_rows(
                "Anchor-band false positives",
                anchor_band_false_positives,
                reference_rows=generated_rows,
                reference_label="target",
                band_rule=ANCHOR_BAND_RULE,
                historical_ranges=generated_ranges,
            )
        )
        print()
        print(
            render_rule_table(
                f"Anchor-band overlap one-feature separators for {TARGET_CLASS}",
                anchor_band_focus_rows,
                anchor_band_focus_one_feature_rules,
            )
        )
        print()
        print(
            render_rule_table(
                f"Anchor-band overlap compact separators for {TARGET_CLASS}",
                anchor_band_focus_rows,
                anchor_band_focus_compact_rules,
            )
        )
    if focused_support_layout_rows:
        print()
        print(
            render_pairwise_deltas(
                "Focused add4 vs skew-wrap representative deltas",
                focused_add4_rows,
                focused_generated_rows,
                delta_features=FOCUSED_DELTA_FEATURES,
            )
        )
        print()
        print(
            render_rule_table(
                f"Focused support-layout one-feature separators for {TARGET_CLASS}",
                focused_support_layout_rows,
                focused_support_layout_one_feature_rules,
            )
        )
        print()
        print(
            render_rule_table(
                f"Focused support-layout compact separators for {TARGET_CLASS}",
                focused_support_layout_rows,
                focused_support_layout_compact_rules,
            )
        )
    if focused_mode_mix_f_focus_rows:
        print()
        print(
            render_pairwise_deltas(
                "Focused mode-mix-f vs representative shoulder/knot deltas",
                focused_mode_mix_f_rows,
                focused_generated_rows + focused_add4_rows,
                delta_features=FOCUSED_MODE_MIX_F_DELTA_FEATURES,
            )
        )
        print()
        print(
            render_rule_table(
                f"Focused mode-mix-f low-support one-feature separators for {FOCUSED_MODE_MIX_F_CLASS}",
                focused_mode_mix_f_focus_rows,
                focused_mode_mix_f_one_feature_rules,
            )
        )
        print()
        print(
            render_rule_table(
                f"Focused mode-mix-f low-support compact separators for {FOCUSED_MODE_MIX_F_CLASS}",
                focused_mode_mix_f_focus_rows,
                focused_mode_mix_f_compact_rules,
            )
        )
    if focused_outer_rect_focus_rows:
        print()
        print(
            render_pairwise_deltas(
                "Focused outer rect vs representative shoulder/throat/knot deltas",
                focused_outer_rect_rows,
                focused_generated_rows + focused_add4_rows + focused_mode_mix_f_rows,
                delta_features=FOCUSED_OUTER_RECT_DELTA_FEATURES,
            )
        )
        print()
        print(
            render_rule_table(
                f"Focused outer rect one-feature separators for {FOCUSED_OUTER_RECT_CLASS}",
                focused_outer_rect_focus_rows,
                focused_outer_rect_one_feature_rules,
            )
        )
        print()
        print(
            render_rule_table(
                f"Focused outer rect compact separators for {FOCUSED_OUTER_RECT_CLASS}",
                focused_outer_rect_focus_rows,
                focused_outer_rect_compact_rules,
            )
        )
    print()
    print(
        render_rule_table(
            f"Candidate one-feature separators for {TARGET_CLASS}",
            rows,
            one_feature_rules,
        )
    )
    print()
    print(
        render_rule_table(
            f"Candidate compact separators for {TARGET_CLASS}",
            rows,
            compact_rules,
        )
    )
    print()
    exact_one_feature = next((rule for rule in one_feature_rules if rule.exact), None)
    exact_compact = next((rule for rule in compact_rules if rule.exact), None)
    exact_anchor_band_focus_one_feature = next(
        (rule for rule in anchor_band_focus_one_feature_rules if rule.exact),
        None,
    )
    exact_anchor_band_focus_compact = next(
        (rule for rule in anchor_band_focus_compact_rules if rule.exact),
        None,
    )
    exact_focused_support_layout_one_feature = next(
        (rule for rule in focused_support_layout_one_feature_rules if rule.exact),
        None,
    )
    exact_focused_support_layout_compact = next(
        (rule for rule in focused_support_layout_compact_rules if rule.exact),
        None,
    )
    exact_focused_mode_mix_f_one_feature = next(
        (rule for rule in focused_mode_mix_f_one_feature_rules if rule.exact),
        None,
    )
    exact_focused_mode_mix_f_compact = next(
        (rule for rule in focused_mode_mix_f_compact_rules if rule.exact),
        None,
    )
    exact_focused_outer_rect_one_feature = next(
        (rule for rule in focused_outer_rect_one_feature_rules if rule.exact),
        None,
    )
    exact_focused_outer_rect_compact = next(
        (rule for rule in focused_outer_rect_compact_rules if rule.exact),
        None,
    )
    outer_guardrail_escape_rows = [
        row
        for row in outer_guardrail_rows
        if _translation_label(row) == "outside-current-translation"
    ]
    outer_guardrail_shoulder_rows = [
        row
        for row in outer_guardrail_rows
        if _translation_label(row) == "right/deep-shoulder"
    ]
    outer_guardrail_throat_rows = [
        row
        for row in outer_guardrail_rows
        if _translation_label(row) == "low-support-throat"
    ]
    print("Conclusion")
    print("==========")
    if not generated_stable_rows:
        print(
            "The bounded nearby generated scan again found no guard-surviving correctly classified comparison rows, so this pass mainly tests the anchor band against the historical add1/add4 cohorts."
        )
    if not anchor_band_false_positives and not anchor_band_false_negatives:
        print(
            "The anchor-balance band remains exact after adding the historical frozen add1 and add4 cohorts plus the bounded nearby generated comparison basin."
        )
        print(f"best_exact_compact={ANCHOR_BAND_RULE}")
    elif (
        len(anchor_band_false_positives) == len(anchor_band_add4_rows)
        and not anchor_band_false_negatives
        and exact_anchor_band_focus_one_feature is not None
    ):
        print(
            "The anchor-balance band broadens only onto a small historical add4 pocket, and one extra in-band clause exact-separates those add4 rows from the generated failures without reopening the pair-only/add1 boundary."
        )
        print(f"best_exact_compact={ANCHOR_BAND_RULE} and {exact_anchor_band_focus_one_feature.rule_text}")
        if exact_focused_support_layout_one_feature is not None:
            print(
                "Within the two-row add4 pocket versus the representative skew-wrap generated failures, one compact support-layout observable already exact-separates the rows."
            )
            print(
                f"focused_exact_support_layout={exact_focused_support_layout_one_feature.rule_text}"
            )
            print(
                "support_layout_translation=the generated skew-wrap failures carry a right/deep bridge shoulder "
                "(anchor_deep_share_gap=0.500, high_bridge_right_count=1.000) that the in-band add4 pocket lacks "
                "(0.000, 0.000), so anchor balance stays similar while the frozen add4 rows trap more closure at the mid anchor "
                "(mid_anchor_closure_peak=12.000 versus 8.000)."
            )
        if exact_focused_mode_mix_f_one_feature is not None:
            print(
                "On the same representative row set, one compact low-support observable exact-separates mode-mix-f from both the skew-wrap shoulder and the in-band add4 knot."
            )
            print(
                f"focused_exact_mode_mix_f={exact_focused_mode_mix_f_one_feature.rule_text}"
            )
            print(
                "mode_mix_f_translation=mode-mix-f stays inside the anchor band by collapsing to a zero-support, low-closure floor "
                "(support_load=0.000, closure_load=5.000, edge_identity_event_count=10.000) rather than by carrying the skew-wrap "
                "right/deep bridge shoulder (anchor_deep_share_gap=0.500, high_bridge_right_count=1.000); on the current bounded basis "
                "the refined band therefore admits two generated realizations, a right/deep bridge shoulder and a nearly empty low-support throat, "
                "both distinct from the frozen add4 mid-anchor knot (mid_anchor_closure_peak=12.000)."
            )
        if outer_guardrail_rows:
            if not outer_guardrail_escape_rows:
                print(
                    "One sparse outer guardrail slice adds only in-band generated rows that still fit the current shoulder/throat translation."
                )
                print(
                    "outer_guardrail_translation="
                    + f"shoulder:{len(outer_guardrail_shoulder_rows)} "
                    + f"throat:{len(outer_guardrail_throat_rows)} "
                    + f"outside:{len(outer_guardrail_escape_rows)}"
                )
            else:
                print(
                    "One sparse outer guardrail slice reveals in-band generated rows outside the current shoulder/throat translation."
                )
                print(
                    "outer_guardrail_translation="
                    + f"shoulder:{len(outer_guardrail_shoulder_rows)} "
                    + f"throat:{len(outer_guardrail_throat_rows)} "
                    + f"outside:{len(outer_guardrail_escape_rows)}"
                )
        if exact_focused_outer_rect_one_feature is not None:
            print(
                "On the focused outer rect versus shoulder/throat/knot set, one compact load observable exact-separates the outer rect pair from the current representatives."
            )
            print(
                f"focused_exact_outer_rect={exact_focused_outer_rect_one_feature.rule_text}"
            )
            print(
                "outer_rect_translation=the outer rect pair shares the knot-side ceiling "
                "(mid_anchor_closure_peak=12.000, anchor_deep_share_gap=0.000) with the frozen add4 pocket, "
                "but it keeps high_bridge_right_count=1.000 and rises to a much heavier load "
                "(support_load=26.000, closure_load=80.000), so it reads as a loaded knot-side continuation "
                "beyond the refined ceiling rather than as the same frozen knot pocket."
            )
        elif exact_focused_outer_rect_compact is not None:
            print(
                "On the focused outer rect versus shoulder/throat/knot set, a compact load-sensitive clause exact-separates the outer rect pair from the current representatives."
            )
            print(
                f"focused_exact_outer_rect={exact_focused_outer_rect_compact.rule_text}"
            )
    elif (
        len(anchor_band_false_positives) == len(anchor_band_add4_rows)
        and not anchor_band_false_negatives
        and exact_anchor_band_focus_compact is not None
    ):
        print(
            "The anchor-balance band broadens only onto a small historical add4 pocket, and a compact in-band clause exact-separates those add4 rows from the generated failures without reopening the pair-only/add1 boundary."
        )
        print(f"best_exact_compact={ANCHOR_BAND_RULE} and {exact_anchor_band_focus_compact.rule_text}")
        if exact_focused_support_layout_one_feature is not None:
            print(
                "Within the two-row add4 pocket versus the representative skew-wrap generated failures, one compact support-layout observable already exact-separates the rows."
            )
            print(
                f"focused_exact_support_layout={exact_focused_support_layout_one_feature.rule_text}"
            )
            print(
                "support_layout_translation=the generated skew-wrap failures carry a right/deep bridge shoulder "
                "(anchor_deep_share_gap=0.500, high_bridge_right_count=1.000) that the in-band add4 pocket lacks "
                "(0.000, 0.000), so anchor balance stays similar while the frozen add4 rows trap more closure at the mid anchor "
                "(mid_anchor_closure_peak=12.000 versus 8.000)."
            )
        elif exact_focused_support_layout_compact is not None:
            print(
                "Within the two-row add4 pocket versus the representative skew-wrap generated failures, a compact support-layout separator already exact-separates the rows."
            )
            print(
                f"focused_exact_support_layout={exact_focused_support_layout_compact.rule_text}"
            )
        if exact_focused_mode_mix_f_one_feature is not None:
            print(
                "On the same representative row set, one compact low-support observable exact-separates mode-mix-f from both the skew-wrap shoulder and the in-band add4 knot."
            )
            print(
                f"focused_exact_mode_mix_f={exact_focused_mode_mix_f_one_feature.rule_text}"
            )
            print(
                "mode_mix_f_translation=mode-mix-f stays inside the anchor band by collapsing to a zero-support, low-closure floor "
                "(support_load=0.000, closure_load=5.000, edge_identity_event_count=10.000) rather than by carrying the skew-wrap "
                "right/deep bridge shoulder (anchor_deep_share_gap=0.500, high_bridge_right_count=1.000); on the current bounded basis "
                "the refined band therefore admits two generated realizations, a right/deep bridge shoulder and a nearly empty low-support throat, "
                "both distinct from the frozen add4 mid-anchor knot (mid_anchor_closure_peak=12.000)."
            )
        elif exact_focused_mode_mix_f_compact is not None:
            print(
                "On the same representative row set, a compact low-support clause exact-separates mode-mix-f from both the skew-wrap shoulder and the in-band add4 knot."
            )
            print(
                f"focused_exact_mode_mix_f={exact_focused_mode_mix_f_compact.rule_text}"
            )
        if outer_guardrail_rows:
            if not outer_guardrail_escape_rows:
                print(
                    "One sparse outer guardrail slice adds only in-band generated rows that still fit the current shoulder/throat translation."
                )
                print(
                    "outer_guardrail_translation="
                    + f"shoulder:{len(outer_guardrail_shoulder_rows)} "
                    + f"throat:{len(outer_guardrail_throat_rows)} "
                    + f"outside:{len(outer_guardrail_escape_rows)}"
                )
            else:
                print(
                    "One sparse outer guardrail slice reveals in-band generated rows outside the current shoulder/throat translation."
                )
                print(
                    "outer_guardrail_translation="
                    + f"shoulder:{len(outer_guardrail_shoulder_rows)} "
                    + f"throat:{len(outer_guardrail_throat_rows)} "
                    + f"outside:{len(outer_guardrail_escape_rows)}"
                )
        if exact_focused_outer_rect_one_feature is not None:
            print(
                "On the focused outer rect versus shoulder/throat/knot set, one compact load observable exact-separates the outer rect pair from the current representatives."
            )
            print(
                f"focused_exact_outer_rect={exact_focused_outer_rect_one_feature.rule_text}"
            )
            print(
                "outer_rect_translation=the outer rect pair shares the knot-side ceiling "
                "(mid_anchor_closure_peak=12.000, anchor_deep_share_gap=0.000) with the frozen add4 pocket, "
                "but it keeps high_bridge_right_count=1.000 and rises to a much heavier load "
                "(support_load=26.000, closure_load=80.000), so it reads as a loaded knot-side continuation "
                "beyond the refined ceiling rather than as the same frozen knot pocket."
            )
        elif exact_focused_outer_rect_compact is not None:
            print(
                "On the focused outer rect versus shoulder/throat/knot set, a compact load-sensitive clause exact-separates the outer rect pair from the current representatives."
            )
            print(
                f"focused_exact_outer_rect={exact_focused_outer_rect_compact.rule_text}"
            )
    elif exact_one_feature is not None:
        print(
            "The prior anchor-balance band leaks on the broadened comparison set, but an exact one-feature separator still exists on the full bounded basis."
        )
        print(f"best_exact_one_feature={exact_one_feature.rule_text}")
    elif exact_compact is not None:
        print(
            "The prior anchor-balance band leaks on the broadened comparison set, but the generated failures still exact-close with a compact separator on the current bounded basis."
        )
        print(f"best_exact_compact={exact_compact.rule_text}")
    else:
        print(
            "Once the comparison set is broadened to historical add1 and nearby stable generated rows, the generated failures no longer exact-close on the current bounded feature basis."
        )
        if compact_rules:
            print(f"best_partial_compact={compact_rules[0].rule_text}")
    print()
    print(
        "generated non-guarded pair compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
