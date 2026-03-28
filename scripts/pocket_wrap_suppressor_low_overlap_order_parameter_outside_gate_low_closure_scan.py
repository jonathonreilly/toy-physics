#!/usr/bin/env python3
"""Scan the outside-gate residual for a compact low-closure separator."""

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
    FEATURE_NAMES,
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


TARGET_SUBTYPE = "pair-only-sensitive"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=22)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def outside_gate_rows(rows: list[object]) -> list[object]:
    return [
        row
        for row in rows
        if not (
            float(getattr(row, "mid_anchor_closure_peak")) >= 11.0
            and float(getattr(row, "anchor_closure_intensity_gap")) > 0.0
        )
    ]


def format_membership(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    total = len(rows)
    parts = [f"{subtype}:{counts[subtype]}" for subtype in sorted(counts)]
    return f"{total} ({', '.join(parts)})"


def render_rule_table(title: str, rows: list[object], rules: list[object]) -> str:
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


def select_low_closure_rule(rules: list[object]) -> object:
    for rule in rules:
        if "closure_load" in rule.rule_text:
            return rule
    return rules[0]


def render_row_list(title: str, rows: list[object]) -> str:
    lines = [
        title,
        "-" * len(title),
    ]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in sorted(rows, key=lambda item: getattr(item, "source_name")):
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"support_load={float(getattr(row, 'support_load')):.3f} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap outside-gate low-closure scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = outside_gate_rows(build_rows(frontier_log))
    rules = evaluate_rules(
        rows,
        target_subtype=TARGET_SUBTYPE,
        feature_names=FEATURE_NAMES,
        predicate_limit=args.predicate_limit,
        max_terms=2,
        row_limit=args.row_limit,
    )
    best_rule = select_low_closure_rule(rules)
    matched = [row for row in rows if matches_rule_text(row, best_rule.rule_text)]
    residual = [row for row in rows if not matches_rule_text(row, best_rule.rule_text)]
    misclassified = [row for row in matched if getattr(row, "subtype") != TARGET_SUBTYPE]
    unmatched = [row for row in residual if getattr(row, "subtype") == TARGET_SUBTYPE]

    print()
    print("Low-Overlap Outside-Gate Low-Closure Scan")
    print("=========================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("outside_gate=not(mid_anchor_closure_peak >= 11 and anchor_closure_intensity_gap > 0)")
    print(f"rows={len(rows)} ({format_membership(rows)})")
    print(f"target_subtype={TARGET_SUBTYPE}")
    print()
    print(render_rule_table(f"Candidate outside-gate rules for {TARGET_SUBTYPE}", rows, rules[: args.row_limit]))
    print()
    print("Best low-closure separator")
    print("==========================")
    print(f"rule={best_rule.rule_text}")
    print(f"corr={best_rule.correct}/{best_rule.total}")
    print(f"tp/fp/fn={best_rule.tp}/{best_rule.fp}/{best_rule.fn}")
    print(f"matched={format_membership(matched)}")
    print(f"residual={format_membership(residual)}")
    print()
    print(render_row_list("Misclassified matched rows", misclassified))
    print()
    print(render_row_list("Unmatched target rows", unmatched))
    print()
    print(
        "low-overlap outside-gate low-closure scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
