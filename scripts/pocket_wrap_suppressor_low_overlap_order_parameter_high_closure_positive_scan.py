#!/usr/bin/env python3
"""Probe one-threshold separators inside the high-closure positive-asymmetry residual cell."""

from __future__ import annotations

import argparse
from collections import Counter
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
from pocket_wrap_suppressor_low_overlap_order_parameter_asymmetry_map import (  # noqa: E402
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


FEATURE_NAMES = [
    "support_load",
    "anchor_deep_share_gap",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=16)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def target_rows(rows: list[object]) -> list[object]:
    return [
        row
        for row in rows
        if float(getattr(row, "mid_anchor_closure_peak")) >= 11.0
        and float(getattr(row, "anchor_closure_intensity_gap")) > 0.0
    ]


def format_membership(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    total = len(rows)
    parts = [f"{subtype}:{counts[subtype]}" for subtype in sorted(counts)]
    return f"{total} ({', '.join(parts)})"


def render_row_table(rows: list[object]) -> str:
    lines = [
        "Target Cell Rows",
        "================",
        "source | subtype | support_load | anchor_deep_share_gap | mid_anchor_closure_peak | anchor_closure_intensity_gap",
        "-------+---------+--------------+-----------------------+-------------------------+------------------------------",
    ]
    for row in sorted(rows, key=lambda item: (getattr(item, "subtype"), getattr(item, "source_name"))):
        lines.append(
            f"{getattr(row, 'source_name')} | {getattr(row, 'subtype')} | "
            f"{float(getattr(row, 'support_load')):>12.3f} | "
            f"{float(getattr(row, 'anchor_deep_share_gap')):>21.3f} | "
            f"{float(getattr(row, 'mid_anchor_closure_peak')):>23.3f} | "
            f"{float(getattr(row, 'anchor_closure_intensity_gap')):>28.3f}"
        )
    return "\n".join(lines)


def render_candidate_table(title: str, rows: list[object], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | corr | tp/fp/fn | matched(subtype counts) | residual(subtype counts)",
        "-----+------+----------+-------------------------+-------------------------",
    ]
    for rule in rules:
        matched = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        residual = [row for row in rows if not matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {rule.correct:>2}/{rule.total:<2} | "
            f"{rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{format_membership(matched)} | {format_membership(residual)}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap high-closure positive-asymmetry scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = target_rows(build_rows(frontier_log))
    subtypes = sorted({getattr(row, "subtype") for row in rows})

    print()
    print("Low-Overlap High-Closure Positive-Asymmetry Scan")
    print("================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("cell_filter=mid_anchor_closure_peak >= 11 and anchor_closure_intensity_gap > 0")
    print(f"rows={len(rows)}")
    print(f"features={','.join(FEATURE_NAMES)}")
    print()
    print(render_row_table(rows))
    print()

    for subtype in subtypes:
        rules = evaluate_rules(
            rows,
            target_subtype=subtype,
            feature_names=FEATURE_NAMES,
            predicate_limit=args.predicate_limit,
            max_terms=1,
            row_limit=args.row_limit,
        )
        one_term_rules = [rule for rule in rules if rule.term_count == 1][: args.row_limit]
        print(
            render_candidate_table(
                f"Candidate one-threshold separators for {subtype}",
                rows,
                one_term_rules,
            )
        )
        print()

    print(
        "low-overlap high-closure positive-asymmetry scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
