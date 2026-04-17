#!/usr/bin/env python3
"""Evaluate bounded two-clause order-parameter separators with residual subtype membership."""

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

RESTRICTED_FEATURES = [
    "support_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=24)
    parser.add_argument("--row-limit", type=int, default=10)
    return parser


def format_membership(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    total = len(rows)
    parts = [f"{subtype}:{counts[subtype]}" for subtype in sorted(counts)]
    return f"{total} ({', '.join(parts)})"


def render_candidate_table(title: str, rows: list[object], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | corr | tp/fp/fn | matched(subtype counts) | residual(subtype counts)",
        "-----+------+----------+-------------------------+-------------------------",
    ]
    for rule in rules:
        matched_rows = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        residual_rows = [row for row in rows if not matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {rule.correct:>3}/{rule.total:<3} | "
            f"{rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{format_membership(matched_rows)} | {format_membership(residual_rows)}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap two-clause residual evaluator started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    subtypes = sorted({getattr(row, "subtype") for row in rows})

    print()
    print("Low-Overlap Two-Clause Residual Evaluator")
    print("=========================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"rows={len(rows)}")
    print(f"restricted_features={','.join(RESTRICTED_FEATURES)}")
    print()

    for subtype in subtypes:
        all_rules = evaluate_rules(
            rows,
            target_subtype=subtype,
            feature_names=RESTRICTED_FEATURES,
            predicate_limit=args.predicate_limit,
            max_terms=2,
            row_limit=max(args.row_limit * 3, args.row_limit),
        )
        two_clause_rules = [rule for rule in all_rules if rule.term_count == 2][: args.row_limit]
        print(
            render_candidate_table(
                f"Candidate two-clause separators for {subtype}",
                rows,
                two_clause_rules,
            )
        )
        print()

    print(
        "low-overlap two-clause residual evaluator completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
