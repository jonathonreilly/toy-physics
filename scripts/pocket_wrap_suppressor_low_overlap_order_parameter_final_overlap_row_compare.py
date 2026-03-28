#!/usr/bin/env python3
"""Compare the final overlap row against the retained add4 set and test exact exclusion."""

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
from pocket_wrap_suppressor_low_overlap_order_parameter_branch_a_leakage_carve_scan import (  # noqa: E402
    build_rows,
    branch_a,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


TARGET_SUBTYPE = "add4-sensitive"
OVERLAP_SUBTYPE = "add1-sensitive"
BASE_CARVE_RULE = (
    "edge_identity_event_count <= 78.000 and "
    "edge_identity_support_edge_density >= 0.166667 and "
    "mid_anchor_closure_peak >= 1.000"
)
FEATURE_NAMES = [
    "support_role_pocket_only_count",
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "mid_candidate_closed_ratio_max",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=2)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def base_carve(row: object) -> bool:
    return branch_a(row) and float(getattr(row, "mid_anchor_closure_peak")) >= 1.0


def format_counts(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{subtype}:{counts[subtype]}" for subtype in sorted(counts))


def confusion(rows: list[object], predicate) -> tuple[int, int, int]:
    tp = fp = fn = 0
    for row in rows:
        actual = getattr(row, "subtype") == TARGET_SUBTYPE
        predicted = predicate(row)
        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif (not predicted) and actual:
            fn += 1
    return tp, fp, fn


def render_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"edge_events={float(getattr(row, 'edge_identity_event_count')):.3f} "
            f"edge_density={float(getattr(row, 'edge_identity_support_edge_density')):.3f} "
            f"support_role_pocket_only_count={float(getattr(row, 'support_role_pocket_only_count')):.3f} "
            f"support_load={float(getattr(row, 'support_load')):.3f} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
            f"deep_gap={float(getattr(row, 'anchor_deep_share_gap')):.3f} "
            f"high_bridge_right_count={float(getattr(row, 'high_bridge_right_count')):.3f} "
            f"high_bridge_right_low_count={float(getattr(row, 'high_bridge_right_low_count')):.3f} "
            f"mid_candidate_closed_ratio_max={float(getattr(row, 'mid_candidate_closed_ratio_max')):.3f}"
        )
    return "\n".join(lines)


def render_rule_table(title: str, rows: list[object], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | exact | corr | tp/fp/fn | matched(subtype counts)",
        "-----+-------+------+----------+-------------------------",
    ]
    for rule in rules:
        matched = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {'Y' if rule.exact else 'n':^5} | {rule.correct:>2}/{rule.total:<2} | "
            f"{rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | {len(matched)} ({format_counts(matched)})"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"final overlap row compare started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    carve_rows = [row for row in rows if base_carve(row)]
    overlap_rows = [row for row in carve_rows if getattr(row, "subtype") == OVERLAP_SUBTYPE]
    add4_rows = [row for row in carve_rows if getattr(row, "subtype") == TARGET_SUBTYPE]

    exclusion_rules = evaluate_rules(
        carve_rows,
        target_subtype=OVERLAP_SUBTYPE,
        feature_names=FEATURE_NAMES,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    exact_exclusion = next((rule for rule in exclusion_rules if rule.exact), None)

    print()
    print("Final Overlap Row Compare")
    print("=========================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("residual_filter=predict_subtype == unmatched under combined-law projection")
    print(f"rows_total={len(rows)} ({format_counts(rows)})")
    print(f"base_carve={BASE_CARVE_RULE}")
    print(f"base_carve_rows={len(carve_rows)} ({format_counts(carve_rows)})")
    print()
    print(render_rows("Final overlap row", overlap_rows))
    print()
    print(render_rows("Retained add4 rows", add4_rows))
    print()
    print(render_rule_table("Candidate exact exclusion rules for the overlap row", carve_rows, exclusion_rules))

    if exact_exclusion is not None:
        refined = lambda row: base_carve(row) and not matches_rule_text(row, exact_exclusion.rule_text)
        tp, fp, fn = confusion(rows, refined)
        matched = [row for row in rows if refined(row)]
        print()
        print("Best exact exclusion projected onto full residual")
        print("==============================================")
        print(f"exclude={exact_exclusion.rule_text}")
        print(
            f"refined_rule=({BASE_CARVE_RULE}) and not ({exact_exclusion.rule_text})"
        )
        print(
            f"tp/fp/fn={tp}/{fp}/{fn} matched={len(matched)} ({format_counts(matched)})"
        )
    else:
        print()
        print("Best exact exclusion projected onto full residual")
        print("==============================================")
        print("none")

    print()
    print(
        "final overlap row compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
