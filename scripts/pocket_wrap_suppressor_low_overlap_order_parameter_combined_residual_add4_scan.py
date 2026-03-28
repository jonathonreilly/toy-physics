#!/usr/bin/env python3
"""Scan the combined-law residual for compact outside-gate add4 structure."""

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
from pocket_wrap_suppressor_low_overlap_order_parameter_asymmetry_map import (  # noqa: E402
    build_rows as build_asymmetry_rows,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_combined_law_projection import (  # noqa: E402
    predict_subtype,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
    build_rc0_ml0_c2_core_inputs,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    build_candidate_anchor_rows,
)


TARGET_SUBTYPE = "add4-sensitive"
FEATURE_NAMES = [
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_high_count",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "high_bridge_low_count",
    "high_bridge_left_count",
    "left_candidate_count",
    "mid_candidate_count",
    "mid_candidate_closed_ratio_max",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def build_rows(frontier_log: Path) -> list[object]:
    asymmetry_by_source = {
        row.source_name: row for row in build_asymmetry_rows(frontier_log)
    }
    coarse_by_source, _ = build_rc0_ml0_c2_core_inputs(frontier_log)
    anchor_by_source = {
        row.source_name: row for row in build_candidate_anchor_rows(frontier_log)
    }
    row_cls = make_dataclass(
        "CombinedResidualAdd4Row",
        [
            ("source_name", str),
            ("subtype", str),
            ("support_load", float),
            ("closure_load", float),
            ("mid_anchor_closure_peak", float),
            ("anchor_closure_intensity_gap", float),
            ("anchor_deep_share_gap", float),
            ("high_bridge_high_count", float),
            ("high_bridge_right_count", float),
            ("high_bridge_right_low_count", float),
            ("high_bridge_low_count", float),
            ("high_bridge_left_count", float),
            ("left_candidate_count", float),
            ("mid_candidate_count", float),
            ("mid_candidate_closed_ratio_max", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for source_name in sorted(asymmetry_by_source):
        asymmetry = asymmetry_by_source[source_name]
        coarse = coarse_by_source[source_name]
        anchor = anchor_by_source[source_name]
        row = row_cls(
            source_name=source_name,
            subtype=getattr(asymmetry, "subtype"),
            support_load=float(getattr(asymmetry, "support_load")),
            closure_load=float(getattr(asymmetry, "closure_load")),
            mid_anchor_closure_peak=float(getattr(asymmetry, "mid_anchor_closure_peak")),
            anchor_closure_intensity_gap=float(
                getattr(asymmetry, "anchor_closure_intensity_gap")
            ),
            anchor_deep_share_gap=float(getattr(asymmetry, "anchor_deep_share_gap")),
            high_bridge_high_count=float(getattr(coarse, "high_bridge_high_count")),
            high_bridge_right_count=float(getattr(coarse, "high_bridge_right_count")),
            high_bridge_right_low_count=float(getattr(coarse, "high_bridge_right_low_count")),
            high_bridge_low_count=float(getattr(coarse, "high_bridge_low_count")),
            high_bridge_left_count=float(getattr(coarse, "high_bridge_left_count")),
            left_candidate_count=float(getattr(anchor, "left_candidate_count")),
            mid_candidate_count=float(getattr(anchor, "mid_candidate_count")),
            mid_candidate_closed_ratio_max=float(
                getattr(anchor, "mid_candidate_closed_ratio_max")
            ),
        )
        if predict_subtype(row) == "unmatched":
            rows.append(row)
    return rows


def format_counts(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    return ", ".join(f"{subtype}:{counts[subtype]}" for subtype in sorted(counts))


def render_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in sorted(rows, key=lambda item: (getattr(item, "subtype"), getattr(item, "source_name"))):
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"support_load={float(getattr(row, 'support_load')):.3f} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
            f"deep_gap={float(getattr(row, 'anchor_deep_share_gap')):.3f} "
            f"high_bridge_high_count={float(getattr(row, 'high_bridge_high_count')):.3f} "
            f"high_bridge_right_count={float(getattr(row, 'high_bridge_right_count')):.3f} "
            f"high_bridge_right_low_count={float(getattr(row, 'high_bridge_right_low_count')):.3f} "
            f"left_candidate_count={float(getattr(row, 'left_candidate_count')):.3f} "
            f"mid_candidate_count={float(getattr(row, 'mid_candidate_count')):.3f} "
            f"mid_candidate_closed_ratio_max={float(getattr(row, 'mid_candidate_closed_ratio_max')):.3f}"
        )
    return "\n".join(lines)


def render_rule_table(title: str, rows: list[object], rules: list[object]) -> str:
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
            f"{rule.rule_text} | {'Y' if rule.exact else 'n':^5} | {rule.correct:>2}/{rule.total:<2} | "
            f"{rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{len(matched)} ({format_counts(matched)}) | {len(residual)} ({format_counts(residual)})"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap combined residual add4 scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    add4_rows = [row for row in rows if getattr(row, "subtype") == TARGET_SUBTYPE]
    add1_rows = [row for row in rows if getattr(row, "subtype") != TARGET_SUBTYPE]
    rules = evaluate_rules(
        rows,
        target_subtype=TARGET_SUBTYPE,
        feature_names=FEATURE_NAMES,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Low-Overlap Combined Residual Add4 Scan")
    print("=======================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("residual_filter=predict_subtype == unmatched under combined-law projection")
    print(f"rows={len(rows)} ({format_counts(rows)})")
    print()
    print(render_rows("Residual add4 rows", add4_rows))
    print()
    print(render_rows("Residual non-add4 rows", add1_rows))
    print()
    print(
        render_rule_table(
            f"Candidate compact rules for residual {TARGET_SUBTYPE}",
            rows,
            rules,
        )
    )
    print()
    print(
        "low-overlap combined residual add4 scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
