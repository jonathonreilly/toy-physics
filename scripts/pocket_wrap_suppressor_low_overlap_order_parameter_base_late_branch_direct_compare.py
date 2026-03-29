#!/usr/bin/env python3
"""Compare the broadened base late branch using recorded row blocks from current logs."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, replace
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
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


HIGH_LOAD_THRESHOLD = 75.0
HIGH_LOAD_RULE = "closure_load >= 75.000"
LATE_BRANCH_CLASS = "late-branch"
REFERENCE_CLASS = "reference"
OTHER_CLASS = "other"
FEATURE_NAMES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
)
DELTA_FEATURES = (
    "support_load",
    "closure_load",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
)
LATE_ROW_SPECS = (
    (
        "late-outer-rect",
        "base:peta:base:rect-wrap:local-morph-f",
    ),
    (
        "late-outer-rect",
        "base:exa:base:rect-wrap:local-morph-f",
    ),
    (
        "late-taper-hard",
        "base:peta:base:taper-hard:local-morph-f",
    ),
    (
        "late-taper-hard",
        "base:exa:base:taper-hard:local-morph-f",
    ),
    (
        "late-skew-wrap",
        "base:exa:base:skew-wrap:local-morph-k",
    ),
)
REFERENCE_ROW_SPECS = (
    (
        "shoulder",
        "default:base:skew-wrap:local-morph-c",
    ),
    (
        "shoulder",
        "broader:base:skew-wrap:mode-mix-d",
    ),
    (
        "throat",
        "ultra:base:taper-wrap:mode-mix-f",
    ),
    (
        "knot",
        "historical:base:taper-wrap:local-morph-ዦ",
    ),
    (
        "knot",
        "historical:base:taper-wrap:local-morph-ᓭ",
    ),
)
FAMILY_ORDER = {
    "late-outer-rect": 0,
    "late-taper-hard": 1,
    "late-skew-wrap": 2,
    "shoulder": 3,
    "throat": 4,
    "knot": 5,
}
ENSEMBLE_ORDER = {
    "historical": -1,
    "default": 0,
    "broader": 1,
    "wider": 2,
    "ultra": 3,
    "mega": 4,
    "giga": 5,
    "tera": 6,
    "peta": 7,
    "exa": 8,
}


@dataclass(frozen=True)
class CompareRow:
    subtype: str
    cohort: str
    family: str
    label: str
    ensemble_name: str
    actual_subtype: str
    predicted_subtype: str
    predicted_branch: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    anchor_closure_intensity_gap: float
    anchor_deep_share_gap: float
    high_bridge_right_count: float
    high_bridge_right_low_count: float
    edge_identity_event_count: float
    edge_identity_support_edge_density: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--late-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-nonrect-sweep-base-peta-exa.txt",
    )
    parser.add_argument(
        "--reference-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-anchor-band-beyond-ceiling-followon.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=24)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def _sort_key(row: CompareRow) -> tuple[int, int, int, str]:
    return (
        0 if row.cohort == LATE_BRANCH_CLASS else 1,
        FAMILY_ORDER.get(row.family, len(FAMILY_ORDER)),
        ENSEMBLE_ORDER.get(row.ensemble_name, len(ENSEMBLE_ORDER)),
        row.label,
    )


def _format_counts(rows: list[CompareRow], attr: str = "family") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _parse_row_blocks(log_path: Path) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    lines = log_path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if " actual=" not in line or " predicted=" not in line or " branch=" not in line:
            index += 1
            continue
        label, remainder = line.split(" actual=", 1)
        if " style=" in label:
            label, _style = label.split(" style=", 1)
        actual_subtype, remainder = remainder.split(" predicted=", 1)
        predicted_subtype, remainder = remainder.split(" branch=", 1)
        predicted_branch = remainder.split()[0]
        metrics: dict[str, float] = {}
        inner = index + 1
        while inner < len(lines) and lines[inner].startswith("  "):
            metric_line = lines[inner].strip()
            if "=" not in metric_line:
                break
            key, value = metric_line.split("=", 1)
            metrics[key] = float(value)
            inner += 1
        rows[label] = {
            "actual_subtype": actual_subtype,
            "predicted_subtype": predicted_subtype,
            "predicted_branch": predicted_branch,
            **metrics,
        }
        index = inner
    return rows


def _capture_row(
    *,
    family: str,
    cohort: str,
    label: str,
    parsed_rows: dict[str, dict[str, object]],
) -> CompareRow:
    payload = parsed_rows.get(label)
    if payload is None:
        raise ValueError(f"missing recorded row block for {label}")
    ensemble_name = label.split(":", 1)[0]
    return CompareRow(
        subtype=family,
        cohort=cohort,
        family=family,
        label=label,
        ensemble_name=ensemble_name,
        actual_subtype=str(payload["actual_subtype"]),
        predicted_subtype=str(payload["predicted_subtype"]),
        predicted_branch=str(payload["predicted_branch"]),
        support_load=float(payload["support_load"]),
        closure_load=float(payload["closure_load"]),
        mid_anchor_closure_peak=float(payload["mid_anchor_closure_peak"]),
        anchor_closure_intensity_gap=float(payload["anchor_closure_intensity_gap"]),
        anchor_deep_share_gap=float(payload["anchor_deep_share_gap"]),
        high_bridge_right_count=float(payload["high_bridge_right_count"]),
        high_bridge_right_low_count=float(payload["high_bridge_right_low_count"]),
        edge_identity_event_count=float(payload["edge_identity_event_count"]),
        edge_identity_support_edge_density=float(
            payload["edge_identity_support_edge_density"]
        ),
    )


def build_rows(late_log: Path, reference_log: Path) -> list[CompareRow]:
    late_rows = _parse_row_blocks(late_log)
    reference_rows = _parse_row_blocks(reference_log)
    rows: list[CompareRow] = []
    for family, label in LATE_ROW_SPECS:
        rows.append(
            _capture_row(
                family=family,
                cohort=LATE_BRANCH_CLASS,
                label=label,
                parsed_rows=late_rows,
            )
        )
    for family, label in REFERENCE_ROW_SPECS:
        rows.append(
            _capture_row(
                family=family,
                cohort=REFERENCE_CLASS,
                label=label,
                parsed_rows=reference_rows,
            )
        )
    rows.sort(key=_sort_key)
    return rows


def _nearest_reference(target: CompareRow, candidates: list[CompareRow]) -> tuple[CompareRow, float]:
    best_row = candidates[0]
    best_distance = sum(
        abs(float(getattr(target, feature)) - float(getattr(best_row, feature)))
        for feature in FEATURE_NAMES
    )
    for candidate in candidates[1:]:
        distance = sum(
            abs(float(getattr(target, feature)) - float(getattr(candidate, feature)))
            for feature in FEATURE_NAMES
        )
        if distance < best_distance:
            best_row = candidate
            best_distance = distance
    return best_row, best_distance


def _render_rows(title: str, rows: list[CompareRow]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in sorted(rows, key=_sort_key):
        lines.append(
            f"{row.label} family={row.family} actual={row.actual_subtype} "
            f"predicted={row.predicted_subtype} branch={row.predicted_branch} "
            f"high_load={'Y' if row.closure_load >= HIGH_LOAD_THRESHOLD else 'n'}"
        )
        lines.append(f"  support_load={row.support_load:.3f}")
        lines.append(f"  closure_load={row.closure_load:.3f}")
        lines.append(f"  mid_anchor_closure_peak={row.mid_anchor_closure_peak:.3f}")
        lines.append(
            f"  anchor_closure_intensity_gap={row.anchor_closure_intensity_gap:.3f}"
        )
        lines.append(f"  anchor_deep_share_gap={row.anchor_deep_share_gap:.3f}")
        lines.append(f"  high_bridge_right_count={row.high_bridge_right_count:.3f}")
        lines.append(
            f"  high_bridge_right_low_count={row.high_bridge_right_low_count:.3f}"
        )
        lines.append(f"  edge_identity_event_count={row.edge_identity_event_count:.3f}")
        lines.append(
            "  edge_identity_support_edge_density="
            f"{row.edge_identity_support_edge_density:.3f}"
        )
    return "\n".join(lines)


def _render_high_load_projection(rows: list[CompareRow]) -> str:
    lines = [
        "Late-Branch High-Load Projection",
        "===============================",
        f"rule={HIGH_LOAD_RULE}",
    ]
    family_names = []
    for row in rows:
        if row.family not in family_names:
            family_names.append(row.family)
    for family in family_names:
        family_rows = [row for row in rows if row.family == family]
        hits = sum(1 for row in family_rows if row.closure_load >= HIGH_LOAD_THRESHOLD)
        lines.append(
            f"{family}: {hits}/{len(family_rows)} "
            f"({_format_counts(family_rows, attr='actual_subtype')})"
        )
    overall_hits = sum(1 for row in rows if row.closure_load >= HIGH_LOAD_THRESHOLD)
    lines.append(
        f"overall: {overall_hits}/{len(rows)} ({_format_counts(rows, attr='family')})"
    )
    return "\n".join(lines)


def _render_nearest_reference_matches(
    branch_rows: list[CompareRow],
    reference_rows: list[CompareRow],
) -> str:
    lines = [
        "Nearest Representative Matches",
        "=============================",
    ]
    for row in sorted(branch_rows, key=_sort_key):
        nearest, distance = _nearest_reference(row, reference_rows)
        lines.append(
            f"{row.label} -> {nearest.label} distance={distance:.3f} "
            f"nearest_family={nearest.family}"
        )
        for feature in DELTA_FEATURES:
            delta = float(getattr(row, feature)) - float(getattr(nearest, feature))
            lines.append(
                f"  delta_{feature}={delta:+.3f} "
                f"({float(getattr(row, feature)):.3f} vs {float(getattr(nearest, feature)):.3f})"
            )
    return "\n".join(lines)


def _render_rule_table(title: str, rows: list[CompareRow], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | exact | corr | tp/fp/fn | matched(family counts)",
        "-----+-------+------+----------+----------------------",
    ]
    for rule in rules:
        matched = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {'Y' if rule.exact else 'n':^5} | "
            f"{rule.correct:>2}/{rule.total:<2} | {rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{len(matched)} ({_format_counts(matched)})"
        )
    return "\n".join(lines)


def _relabel_overall(rows: list[CompareRow]) -> list[CompareRow]:
    return [
        replace(
            row,
            subtype=LATE_BRANCH_CLASS if row.cohort == LATE_BRANCH_CLASS else REFERENCE_CLASS,
        )
        for row in rows
    ]


def _relabel_family(rows: list[CompareRow], target_family: str) -> list[CompareRow]:
    return [
        replace(row, subtype=target_family if row.family == target_family else OTHER_CLASS)
        for row in rows
    ]


def _one_feature_rules(
    rows: list[CompareRow],
    *,
    target_subtype: str,
    predicate_limit: int,
    row_limit: int,
) -> list[object]:
    return evaluate_rules(
        rows,
        target_subtype=target_subtype,
        feature_names=list(FEATURE_NAMES),
        predicate_limit=predicate_limit,
        max_terms=1,
        row_limit=row_limit,
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"base late branch direct compare started {started}", flush=True)
    total_start = time.time()

    late_log = Path(args.late_log).resolve()
    reference_log = Path(args.reference_log).resolve()
    rows = build_rows(late_log, reference_log)
    branch_rows = [row for row in rows if row.cohort == LATE_BRANCH_CLASS]
    reference_rows = [row for row in rows if row.cohort == REFERENCE_CLASS]

    overall_rows = _relabel_overall(rows)
    overall_rules = _one_feature_rules(
        overall_rows,
        target_subtype=LATE_BRANCH_CLASS,
        predicate_limit=args.predicate_limit,
        row_limit=args.row_limit,
    )

    outer_rows = _relabel_family(rows, "late-outer-rect")
    outer_rules = _one_feature_rules(
        outer_rows,
        target_subtype="late-outer-rect",
        predicate_limit=args.predicate_limit,
        row_limit=args.row_limit,
    )

    taper_rows = _relabel_family(rows, "late-taper-hard")
    taper_rules = _one_feature_rules(
        taper_rows,
        target_subtype="late-taper-hard",
        predicate_limit=args.predicate_limit,
        row_limit=args.row_limit,
    )

    skew_rows = _relabel_family(rows, "late-skew-wrap")
    skew_rules = _one_feature_rules(
        skew_rows,
        target_subtype="late-skew-wrap",
        predicate_limit=args.predicate_limit,
        row_limit=args.row_limit,
    )

    print()
    print("Base Late Branch Direct Compare")
    print("==============================")
    print(f"late_log={late_log}")
    print(f"reference_log={reference_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"rows_total={len(rows)}")
    print(
        f"late_branch_rows={len(branch_rows)} ({_format_counts(branch_rows, attr='family')})"
    )
    print(
        f"reference_rows={len(reference_rows)} ({_format_counts(reference_rows, attr='family')})"
    )
    print("late_branch_sources=" + ",".join(row.label for row in sorted(branch_rows, key=_sort_key)))
    print("reference_sources=" + ",".join(row.label for row in sorted(reference_rows, key=_sort_key)))
    print()
    print(_render_rows("Late branch rows", branch_rows))
    print()
    print(_render_rows("Reference rows", reference_rows))
    print()
    print(_render_high_load_projection(rows))
    print()
    print(_render_nearest_reference_matches(branch_rows, reference_rows))
    print()
    print(_render_rule_table("Late branch vs reference one-feature separators", overall_rows, overall_rules))
    print()
    print(_render_rule_table("Late outer-rect one-feature separators", outer_rows, outer_rules))
    print()
    print(_render_rule_table("Late taper-hard one-feature separators", taper_rows, taper_rules))
    print()
    print(_render_rule_table("Late skew-wrap one-feature separators", skew_rows, skew_rules))
    print()
    print(
        "base late branch direct compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
