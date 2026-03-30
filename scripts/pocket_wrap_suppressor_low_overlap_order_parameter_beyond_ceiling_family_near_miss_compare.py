#!/usr/bin/env python3
"""Compare the shared beyond-ceiling family against the fresh skew-hard near miss."""

from __future__ import annotations

import argparse
from dataclasses import replace
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
    matches_rule_text,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_compare import (  # noqa: E402
    CompareRow,
    FEATURE_NAMES,
    OTHER_CLASS,
    PACKET_LAW_RULES,
    _format_counts,
    _render_rows,
    build_rows as build_baseline_rows,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_wider_sentinel_guardrail import (  # noqa: E402
    build_sentinel_row,
)


SHARED_FAMILY_CLASS = "shared-family"
NEAR_MISS_CLASS = "near-miss"
PACKET_FEATURE_NAMES = (
    "mid_anchor_closure_peak",
    "mid_candidate_bridge_bridge_closed_pair_max",
    "mid_candidate_attached_max",
    "mid_has_four_incident_flank_hinge",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outer-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-anchor-band-beyond-ceiling-followon.txt",
    )
    parser.add_argument(
        "--nonrect-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-nonrect-sweep-base-peta-exa.txt",
    )
    parser.add_argument(
        "--packet-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-late-branch-law-confirmation.txt",
    )
    parser.add_argument("--sentinel-ensemble", default="exa")
    parser.add_argument("--sentinel-pack", default="base")
    parser.add_argument("--sentinel-scenario", default="skew-hard")
    parser.add_argument("--sentinel-source", default="base:skew-hard:local-morph-k")
    parser.add_argument("--predicate-limit", type=int, default=48)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def _combined_rows(args: argparse.Namespace) -> tuple[list[CompareRow], CompareRow]:
    family_rows = build_baseline_rows(
        Path(args.outer_log).resolve(),
        Path(args.nonrect_log).resolve(),
        Path(args.packet_log).resolve(),
    )
    sentinel = replace(
        build_sentinel_row(
            ensemble_name=args.sentinel_ensemble,
            pack_name=args.sentinel_pack,
            scenario_name=args.sentinel_scenario,
            source_name=args.sentinel_source,
        ),
        subtype=NEAR_MISS_CLASS,
        family=NEAR_MISS_CLASS,
        cohort="fresh-guardrail",
    )
    return family_rows + [sentinel], sentinel


def _family_labeled_rows(rows: list[CompareRow]) -> list[CompareRow]:
    return [
        replace(
            row,
            subtype=SHARED_FAMILY_CLASS if row.family != NEAR_MISS_CLASS else OTHER_CLASS,
        )
        for row in rows
    ]


def _iter_one_feature_predicates(
    rows: list[CompareRow],
    feature_names: tuple[str, ...],
) -> list[str]:
    predicates: list[str] = []
    for feature_name in feature_names:
        values = sorted({float(getattr(row, feature_name)) for row in rows})
        if len(values) == 1:
            thresholds = [values[0]]
        else:
            thresholds = [(left + right) / 2.0 for left, right in zip(values, values[1:])]
        for threshold in thresholds:
            for operator in ("<=", ">="):
                predicates.append(f"{feature_name} {operator} {threshold:.3f}")
    return predicates


def _exact_threshold_rules(
    rows: list[CompareRow],
    *,
    feature_names: tuple[str, ...],
) -> list[str]:
    family_rows = [row for row in rows if row.family != NEAR_MISS_CLASS]
    near_miss_rows = [row for row in rows if row.family == NEAR_MISS_CLASS]
    exact_rules: list[str] = []
    for rule_text in _iter_one_feature_predicates(rows, feature_names):
        family_match = all(matches_rule_text(row, rule_text) for row in family_rows)
        near_miss_match = any(matches_rule_text(row, rule_text) for row in near_miss_rows)
        if family_match and not near_miss_match:
            exact_rules.append(rule_text)
    return exact_rules


def _render_packet_rule_audit(rows: list[CompareRow], sentinel: CompareRow) -> str:
    family_rows = [row for row in rows if row.family != NEAR_MISS_CLASS]
    lines = [
        "Shared Family Packet Audit",
        "=========================",
        f"rows_total={len(rows)}",
        f"family_rows={len(family_rows)} ({_format_counts(family_rows)})",
        f"near_miss={sentinel.label}",
    ]
    for rule_text in PACKET_LAW_RULES:
        family_match = all(matches_rule_text(row, rule_text) for row in family_rows)
        sentinel_match = matches_rule_text(sentinel, rule_text)
        exact = family_match and not sentinel_match
        lines.append(
            f"{rule_text}: family_all={'Y' if family_match else 'n'} "
            f"near_miss={'Y' if sentinel_match else 'n'} "
            f"exact_family_separator={'Y' if exact else 'n'}"
        )
    return "\n".join(lines)


def _render_exact_threshold_slice(
    title: str,
    rows: list[CompareRow],
    *,
    feature_names: tuple[str, ...],
    limit: int,
) -> str:
    exact_rules = _exact_threshold_rules(rows, feature_names=feature_names)
    lines = [title, "=" * len(title)]
    if not exact_rules:
        lines.append("none")
        return "\n".join(lines)
    for rule_text in exact_rules[:limit]:
        matched = [row for row in rows if matches_rule_text(row, rule_text)]
        lines.append(
            f"{rule_text}: matched={len(matched)} ({_format_counts(matched)})"
        )
    return "\n".join(lines)


def _render_conclusion(rows: list[CompareRow], sentinel: CompareRow) -> str:
    family_rows = [row for row in rows if row.family != NEAR_MISS_CLASS]
    unchanged_packet_rules = [
        rule_text
        for rule_text in PACKET_LAW_RULES
        if all(matches_rule_text(row, rule_text) for row in family_rows)
        and not matches_rule_text(sentinel, rule_text)
    ]
    retuned_packet_rules = _exact_threshold_rules(rows, feature_names=PACKET_FEATURE_NAMES)
    lines = [
        "Conclusion",
        "==========",
        "family_summary=the fresh skew-hard row does not break the current shared family, "
        "but it does split the old four-rule packet equivalence into an unchanged-rule layer "
        "and a retuned-threshold layer.",
    ]
    if unchanged_packet_rules:
        lines.append(
            "unchanged_exact_packet_family_rules=" + ", ".join(unchanged_packet_rules)
        )
    else:
        lines.append("unchanged_exact_packet_family_rules=none")
    if retuned_packet_rules:
        lines.append(
            "retuned_exact_packet_family_rules=" + ", ".join(retuned_packet_rules)
        )
    else:
        lines.append("retuned_exact_packet_family_rules=none")
    lines.append(
        "near_miss_profile="
        f"mid_peak={sentinel.mid_anchor_closure_peak:.3f}, "
        f"mid_attached={sentinel.mid_candidate_attached_max:.3f}, "
        f"mid_bb={sentinel.mid_candidate_bridge_bridge_closed_pair_max:.3f}, "
        f"hinge={'Y' if sentinel.mid_has_four_incident_flank_hinge >= 0.5 else 'n'}"
    )
    lines.append(
        "boundary_read=the missing eighth attachment is the only exact separator that survives "
        "unchanged from the original packet-law quartet, while `mid_peak` and `mid_bb` regain "
        "exactness only after tightening their thresholds from `>= 10.000` to `>= 11.000`."
    )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started_at = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    rows, sentinel = _combined_rows(args)

    print(f"beyond-ceiling family near-miss compare started {started_at}")
    print()
    print("Beyond-Ceiling Family Near-Miss Compare")
    print("=======================================")
    print(f"rows_total={len(rows)}")
    print(f"family_counts={_format_counts(rows)}")
    print(f"near_miss={sentinel.label}")
    print()
    print(_render_rows("Combined Rows", rows))
    print()
    print(_render_packet_rule_audit(rows, sentinel))
    print()
    print(
        _render_exact_threshold_slice(
            "packet-metric exact one-feature threshold separators",
            rows,
            feature_names=PACKET_FEATURE_NAMES,
            limit=args.row_limit,
        )
    )
    print()
    print(
        _render_exact_threshold_slice(
            "all-feature exact one-feature threshold separators",
            rows,
            feature_names=FEATURE_NAMES,
            limit=args.row_limit,
        )
    )
    print()
    print(_render_conclusion(rows, sentinel))
    print()
    print(
        "beyond-ceiling family near-miss compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
