#!/usr/bin/env python3
"""Inspect false positives and misses for the current best add4 anchored-contrast rule."""

from __future__ import annotations

import argparse
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

from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    FEATURE_NAMES,
    build_candidate_anchor_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    best_rule_for_target,
    matches_rule_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=22)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer rc0|ml0|c2 add4 exception scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_candidate_anchor_rows(frontier_log)
    best_rule = best_rule_for_target(
        rows,
        target_subtype="add4-sensitive",
        feature_names=FEATURE_NAMES,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
    )

    tp = [
        row
        for row in rows
        if getattr(row, "subtype") == "add4-sensitive"
        and matches_rule_text(row, best_rule.rule_text)
    ]
    fp = [
        row
        for row in rows
        if getattr(row, "subtype") != "add4-sensitive"
        and matches_rule_text(row, best_rule.rule_text)
    ]
    fn = [
        row
        for row in rows
        if getattr(row, "subtype") == "add4-sensitive"
        and not matches_rule_text(row, best_rule.rule_text)
    ]

    print()
    print("Support Family Transfer rc0|ml0|c2 Add4 Exception Scan")
    print("======================================================")
    print(f"frontier_log={frontier_log}")
    print(f"rule={best_rule.rule_text}")
    print(f"tp={len(tp)} fp={len(fp)} fn={len(fn)}")
    print()

    def render(title: str, items: list[object]) -> None:
        print(title)
        print("-" * len(title))
        for row in items:
            print(
                f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
                f"mid_bb={float(getattr(row, 'mid_candidate_bridge_bridge_closed_pair_max')):.1f} "
                f"delta_mid_left_bb={float(getattr(row, 'delta_mid_left_bridge_bridge_closed_pair_max')):.1f} "
                f"mid_dense={float(getattr(row, 'mid_candidate_dense_count')):.1f} "
                f"left_dense={float(getattr(row, 'left_candidate_dense_count')):.1f} "
                f"closed_pairs={float(getattr(row, 'edge_identity_closed_pair_count')):.1f} "
                f"support_bridge={float(getattr(row, 'support_role_bridge_count')):.1f}"
            )
        print()

    render("True positives", tp)
    render("False positives", fp)
    render("False negatives", fn)
    print(
        "support family transfer rc0|ml0|c2 add4 exception scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
