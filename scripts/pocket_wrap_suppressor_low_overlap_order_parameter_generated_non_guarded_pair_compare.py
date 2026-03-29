#!/usr/bin/env python3
"""Compare non-guarded generated pair-only failures against historical frozen pair-only rows."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import make_dataclass
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
    build_rows as build_generated_rows,
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


TARGET_CLASS = "generated-transfer-failure"
HISTORICAL_CLASS = "historical-pair-only"
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--pack-name", default="base")
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--row-limit", type=int, default=12)
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


def build_generated_target_rows(pack_name: str) -> list[object]:
    target_rows: list[object] = []
    for scenario_name, ensembles, target_sources in TARGET_SPECS:
        source_set = set(target_sources)
        for ensemble_name in ensembles:
            rows = build_generated_rows(ensemble_name, pack_name, scenario_name)
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


def build_comparison_rows(
    generated_rows: list[object],
    historical_rows: list[object],
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
                origin="generated",
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
    for row in historical_rows:
        rows.append(
            row_cls(
                origin="historical",
                source_name=getattr(row, "source_name"),
                subtype=HISTORICAL_CLASS,
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
    return rows


def render_feature_ranges(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    lines.append(f"rows={len(rows)} ({_format_counts(rows, attr='actual_subtype')})")
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


def render_target_rows(
    title: str,
    target_rows: list[object],
    historical_rows: list[object],
    historical_ranges: dict[str, tuple[float, float]],
) -> str:
    lines = [title, "=" * len(title)]
    if not target_rows:
        lines.append("none")
        return "\n".join(lines)
    for row in target_rows:
        nearest_hist, distance = _nearest_row(row, historical_rows)
        out_of_range = []
        for feature in FEATURES:
            feature_min, feature_max = historical_ranges[feature]
            value = float(getattr(row, feature))
            if value < feature_min:
                out_of_range.append(f"{feature}<min")
            elif value > feature_max:
                out_of_range.append(f"{feature}>max")
        lines.append(
            f"{getattr(row, 'ensemble_name')}:{getattr(row, 'source_name')} "
            f"style={getattr(row, 'style')} actual={getattr(row, 'actual_subtype')} "
            f"predicted={getattr(row, 'predicted_subtype')} branch={getattr(row, 'predicted_branch')} "
            f"nearest_hist_pair={getattr(nearest_hist, 'source_name')} distance={distance:.3f} "
            f"out_of_range={'none' if not out_of_range else ','.join(out_of_range)}"
        )
        for feature in FEATURES:
            lines.append(f"  {feature}={float(getattr(row, feature)):.3f}")
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


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"generated non-guarded pair compare started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    historical_rows = [
        row
        for row in build_historical_rows(frontier_log)
        if getattr(row, "subtype") == "pair-only-sensitive"
    ]
    generated_rows = build_generated_target_rows(args.pack_name)
    rows = build_comparison_rows(generated_rows, historical_rows)
    historical_ranges = _feature_ranges(historical_rows)

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
        max_terms=2,
        row_limit=args.row_limit,
    )

    hist_pair_hits = [
        row
        for row in historical_rows
        if predict_subtype(row) == "pair-only-sensitive"
    ]
    generated_pair_hits = [
        row
        for row in generated_rows
        if guarded_predict_subtype(row) == "pair-only-sensitive"
    ]

    print()
    print("Generated Non-Guarded Pair Compare")
    print("==================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"historical_pair_rows={len(historical_rows)}")
    print(f"generated_target_rows={len(generated_rows)} ({_format_counts(generated_rows)})")
    print(
        "generated_targets="
        + ",".join(
            f"{scenario}:{'/'.join(ensembles)}:{'/'.join(source_names)}"
            for scenario, ensembles, source_names in TARGET_SPECS
        )
    )
    print(f"outside_gate_pair_only_rule={OUTSIDE_GATE_PAIR_ONLY_RULE}")
    print(
        f"historical_pair_rule_hits={len(hist_pair_hits)}/{len(historical_rows)} "
        f"generated_pair_rule_hits={len(generated_pair_hits)}/{len(generated_rows)}"
    )
    print()
    print(render_feature_ranges("Historical pair-only ranges", rows=[row for row in rows if row.origin == "historical"]))
    print()
    print(render_feature_ranges("Generated non-guarded target ranges", rows=[row for row in rows if row.origin == "generated"]))
    print()
    print(
        render_shared_out_of_range(
            "Generated rows outside historical pair-only ranges",
            [row for row in rows if row.origin == "generated"],
            historical_ranges,
        )
    )
    print()
    print(
        render_target_rows(
            "Generated target rows",
            [row for row in rows if row.origin == "generated"],
            [row for row in rows if row.origin == "historical"],
            historical_ranges,
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
    print("Conclusion")
    print("==========")
    if exact_one_feature is not None:
        print(
            "The non-guarded generated failures share an exact one-feature separator from historical frozen pair-only rows."
        )
        print(f"best_exact_one_feature={exact_one_feature.rule_text}")
    elif exact_compact is not None:
        print(
            "The non-guarded generated failures do not exact-close with one feature, but they do exact-close with a compact two-clause separator."
        )
        print(f"best_exact_compact={exact_compact.rule_text}")
    else:
        print(
            "The non-guarded generated failures do not exact-close away from historical frozen pair-only rows on the current bounded feature basis."
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
