#!/usr/bin/env python3
"""Compare the last shared high-closure micro-case and test bounded closure rules."""

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
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
    build_rc0_ml0_c2_core_inputs,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    build_candidate_anchor_rows,
)


FEATURE_NAMES = [
    "support_load",
    "anchor_deep_share_gap",
    "edge_identity_closed_pair_count",
    "mid_candidate_closed_ratio_max",
    "high_bridge_low_count",
    "high_bridge_high_count",
    "high_bridge_right_low_count",
]

MICROCASE_FEATURES = [
    "edge_identity_closed_pair_count",
    "mid_candidate_closed_ratio_max",
    "high_bridge_low_count",
    "high_bridge_high_count",
    "high_bridge_right_low_count",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def build_rows(frontier_log: Path) -> tuple[list[object], dict[str, object]]:
    coarse_by_source, frontier_rows = build_rc0_ml0_c2_core_inputs(frontier_log)
    anchor_rows = {
        row.source_name: row
        for row in build_candidate_anchor_rows(frontier_log)
    }
    row_cls = make_dataclass(
        "HighClosureMicrocaseRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("support_load", float),
            ("anchor_deep_share_gap", float),
            ("mid_anchor_closure_peak", float),
            ("anchor_closure_intensity_gap", float),
            ("edge_identity_closed_pair_count", float),
            ("mid_candidate_closed_ratio_max", float),
            ("high_bridge_low_count", float),
            ("high_bridge_high_count", float),
            ("high_bridge_right_low_count", float),
        ],
        frozen=True,
    )

    rows = []
    for source_name in sorted(coarse_by_source):
        coarse = coarse_by_source[source_name]
        anchor = anchor_rows[source_name]
        mid_count = float(getattr(anchor, "mid_candidate_count"))
        left_count = float(getattr(anchor, "left_candidate_count"))
        mid_peak = float(getattr(anchor, "mid_candidate_bridge_bridge_closed_pair_max"))
        left_peak = float(getattr(anchor, "left_candidate_bridge_bridge_closed_pair_max"))
        intensity_gap = _ratio(mid_peak, mid_count) - _ratio(left_peak, left_count)
        if mid_peak < 11.0 or intensity_gap <= 0.0:
            continue
        deep_share_gap = _ratio(
            float(getattr(anchor, "mid_candidate_deep_count")),
            mid_count,
        ) - _ratio(
            float(getattr(anchor, "left_candidate_deep_count")),
            left_count,
        )
        rows.append(
            row_cls(
                source_name=source_name,
                subtype=coarse.subtype,
                support_load=float(coarse.support_role_bridge_count),
                anchor_deep_share_gap=deep_share_gap,
                mid_anchor_closure_peak=mid_peak,
                anchor_closure_intensity_gap=intensity_gap,
                edge_identity_closed_pair_count=float(coarse.edge_identity_closed_pair_count),
                mid_candidate_closed_ratio_max=float(getattr(anchor, "mid_candidate_closed_ratio_max")),
                high_bridge_low_count=float(coarse.high_bridge_low_count),
                high_bridge_high_count=float(coarse.high_bridge_high_count),
                high_bridge_right_low_count=float(coarse.high_bridge_right_low_count),
            )
        )
    return rows, frontier_rows


def format_membership(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    total = len(rows)
    parts = [f"{subtype}:{counts[subtype]}" for subtype in sorted(counts)]
    return f"{total} ({', '.join(parts)})"


def render_cell_rows(rows: list[object]) -> str:
    lines = [
        "High-Closure Positive Cell Rows (Expanded Basis)",
        "===============================================",
        "source | subtype | support_load | deep_gap | closed_pairs | mid_closed_ratio | low_count | high_count | right_low_count",
        "-------+---------+--------------+----------+--------------+------------------+-----------+------------+----------------",
    ]
    for row in sorted(rows, key=lambda item: (getattr(item, "subtype"), getattr(item, "source_name"))):
        lines.append(
            f"{getattr(row, 'source_name')} | {getattr(row, 'subtype')} | "
            f"{float(getattr(row, 'support_load')):>12.3f} | "
            f"{float(getattr(row, 'anchor_deep_share_gap')):>8.3f} | "
            f"{float(getattr(row, 'edge_identity_closed_pair_count')):>12.3f} | "
            f"{float(getattr(row, 'mid_candidate_closed_ratio_max')):>16.3f} | "
            f"{float(getattr(row, 'high_bridge_low_count')):>9.3f} | "
            f"{float(getattr(row, 'high_bridge_high_count')):>10.3f} | "
            f"{float(getattr(row, 'high_bridge_right_low_count')):>14.3f}"
        )
    return "\n".join(lines)


def shared_microcase_rows(rows: list[object]) -> list[object]:
    return [
        row
        for row in rows
        if float(getattr(row, "support_load")) == 13.0
        and abs(float(getattr(row, "anchor_deep_share_gap")) - (1.0 / 3.0)) < 1e-9
        and float(getattr(row, "mid_anchor_closure_peak")) == 12.0
        and float(getattr(row, "anchor_closure_intensity_gap")) == 4.0
    ]


def render_microcase_diff(rows: list[object], frontier_rows: dict[str, object]) -> str:
    lines = [
        "Shared Micro-Case Diff",
        "======================",
    ]
    if len(rows) != 2:
        lines.append(f"expected 2 rows, found {len(rows)}")
        return "\n".join(lines)

    left, right = sorted(rows, key=lambda item: getattr(item, "subtype"))
    lines.append(f"left={getattr(left, 'source_name')} ({getattr(left, 'subtype')})")
    lines.append(f"right={getattr(right, 'source_name')} ({getattr(right, 'subtype')})")
    lines.append("")
    lines.append("Differing surfaced fields")
    lines.append("------------------------")
    for feature in MICROCASE_FEATURES:
        left_value = float(getattr(left, feature))
        right_value = float(getattr(right, feature))
        if abs(left_value - right_value) <= 1e-9:
            continue
        lines.append(
            f"{feature}: {left_value:.3f} vs {right_value:.3f}"
        )

    left_nodes = set(frontier_rows[getattr(left, "source_name")].nodes)
    right_nodes = set(frontier_rows[getattr(right, "source_name")].nodes)
    only_left = sorted(left_nodes - right_nodes)
    only_right = sorted(right_nodes - left_nodes)
    lines.append("")
    lines.append(f"nodes_only_in_{getattr(left, 'subtype')}: {only_left}")
    lines.append(f"nodes_only_in_{getattr(right, 'subtype')}: {only_right}")
    return "\n".join(lines)


def render_candidate_table(title: str, rows: list[object], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | exact | corr | tp/fp/fn | matched(subtype counts) | residual(subtype counts)",
        "-----+-------+------+----------+-------------------------+-------------------------",
    ]
    for rule in rules:
        matched = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        residual = [row for row in rows if not matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {'y' if rule.exact else 'n':^5} | {rule.correct:>2}/{rule.total:<2} | "
            f"{rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{format_membership(matched)} | {format_membership(residual)}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap high-closure microcase closure scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows, frontier_rows = build_rows(frontier_log)
    microcase = shared_microcase_rows(rows)

    print()
    print("Low-Overlap High-Closure Micro-Case Closure Scan")
    print("================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("cell_filter=mid_anchor_closure_peak >= 11 and anchor_closure_intensity_gap > 0")
    print(f"rows={len(rows)}")
    print(f"features={','.join(FEATURE_NAMES)}")
    print()
    print(render_cell_rows(rows))
    print()
    print(render_microcase_diff(microcase, frontier_rows))
    print()

    for subtype in sorted({getattr(row, "subtype") for row in rows}):
        rules = evaluate_rules(
            rows,
            target_subtype=subtype,
            feature_names=FEATURE_NAMES,
            predicate_limit=args.predicate_limit,
            max_terms=2,
            row_limit=args.row_limit,
        )
        print(
            render_candidate_table(
                f"Candidate bounded separators for {subtype}",
                rows,
                rules[: args.row_limit],
            )
        )
        print()

    print(
        "low-overlap high-closure microcase closure scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
