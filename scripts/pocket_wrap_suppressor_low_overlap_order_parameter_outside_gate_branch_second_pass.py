#!/usr/bin/env python3
"""Bounded branch-aware second pass for outside-gate pair-only residuals."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
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

from pocket_wrap_suppressor_low_overlap_order_parameter_outside_gate_exception_compare import (  # noqa: E402
    build_rows,
    format_membership,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


TARGET_SUBTYPE = "pair-only-sensitive"
BASELINE_RULE = "closure_load <= 46.500"
SPILLOVER_RULE = "closure_load <= 46.500 and mid_anchor_closure_peak <= 0 and high_bridge_right_count <= 0"
SIDE_BRANCH_RULE = "high_bridge_right_low_count >= 1 and support_load <= 14.500 and mid_anchor_closure_peak <= 1"
BRANCH_RULE = (
    "(closure_load <= 46.500 and not (mid_anchor_closure_peak <= 0 and high_bridge_right_count <= 0)) "
    "or (high_bridge_right_low_count >= 1 and support_load <= 14.500 and mid_anchor_closure_peak <= 1)"
)


@dataclass(frozen=True)
class RuleResult:
    rule_text: str
    correct: int
    total: int
    tp: int
    fp: int
    fn: int
    matched: list[object]
    residual: list[object]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    return parser


def evaluate_branch_rule(rows: list[object], rule_text: str, predicate) -> RuleResult:
    matched = [row for row in rows if predicate(row)]
    residual = [row for row in rows if not predicate(row)]

    tp = sum(1 for row in matched if getattr(row, "subtype") == TARGET_SUBTYPE)
    fp = sum(1 for row in matched if getattr(row, "subtype") != TARGET_SUBTYPE)
    fn = sum(1 for row in residual if getattr(row, "subtype") == TARGET_SUBTYPE)
    total = len(rows)
    correct = total - fp - fn
    return RuleResult(
        rule_text=rule_text,
        correct=correct,
        total=total,
        tp=tp,
        fp=fp,
        fn=fn,
        matched=matched,
        residual=residual,
    )


def render_row_list(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in sorted(rows, key=lambda item: getattr(item, "source_name")):
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"support_load={float(getattr(row, 'support_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"right={float(getattr(row, 'high_bridge_right_count')):.3f} "
            f"right_low={float(getattr(row, 'high_bridge_right_low_count')):.3f} "
            f"left_candidates={float(getattr(row, 'left_candidate_count')):.3f} "
            f"mid_candidates={float(getattr(row, 'mid_candidate_count')):.3f}"
        )
    return "\n".join(lines)


def render_rule_table(title: str, results: list[RuleResult]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | corr | tp/fp/fn | matched(subtype counts) | residual(subtype counts)",
        "-----+------+----------+-------------------------+-------------------------",
    ]
    for result in results:
        lines.append(
            f"{result.rule_text} | {result.correct:>2}/{result.total:<2} | "
            f"{result.tp:>2}/{result.fp:>2}/{result.fn:>2} | "
            f"{format_membership(result.matched)} | {format_membership(result.residual)}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap outside-gate branch second pass started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)

    baseline_result = evaluate_branch_rule(
        rows,
        BASELINE_RULE,
        lambda row: float(getattr(row, "closure_load")) <= 46.5,
    )
    spillover_rows = [
        row
        for row in rows
        if (
            float(getattr(row, "closure_load")) <= 46.5
            and float(getattr(row, "mid_anchor_closure_peak")) <= 0.0
            and float(getattr(row, "high_bridge_right_count")) <= 0.0
        )
    ]
    side_branch_rows = [
        row
        for row in rows
        if (
            float(getattr(row, "high_bridge_right_low_count")) >= 1.0
            and float(getattr(row, "support_load")) <= 14.5
            and float(getattr(row, "mid_anchor_closure_peak")) <= 1.0
        )
    ]

    branch_result = evaluate_branch_rule(
        rows,
        BRANCH_RULE,
        lambda row: (
            (
                float(getattr(row, "closure_load")) <= 46.5
                and not (
                    float(getattr(row, "mid_anchor_closure_peak")) <= 0.0
                    and float(getattr(row, "high_bridge_right_count")) <= 0.0
                )
            )
            or (
                float(getattr(row, "high_bridge_right_low_count")) >= 1.0
                and float(getattr(row, "support_load")) <= 14.5
                and float(getattr(row, "mid_anchor_closure_peak")) <= 1.0
            )
        ),
    )

    print()
    print("Low-Overlap Outside-Gate Branch Second Pass")
    print("===========================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("outside_gate=not(mid_anchor_closure_peak >= 11 and anchor_closure_intensity_gap > 0)")
    print(f"rows={len(rows)} ({format_membership(rows)})")
    print()
    print(render_row_list(f"Low-closure spillover rows: {SPILLOVER_RULE}", spillover_rows))
    print()
    print(render_row_list(f"Right-low side-branch rows: {SIDE_BRANCH_RULE}", side_branch_rows))
    print()
    print(render_rule_table("Branch-aware rule comparison for pair-only-sensitive", [baseline_result, branch_result]))
    print()
    print(
        "low-overlap outside-gate branch second pass completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
