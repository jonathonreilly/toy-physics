#!/usr/bin/env python3
"""Evaluate a branch-aware residual combiner for outside-gate add4 structure."""

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

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_combined_residual_add4_scan import (  # noqa: E402
    build_rows as build_combined_residual_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
    support_edge_identity_own_metrics,
)


TARGET_SUBTYPE = "add4-sensitive"
BRANCH_A_DENSITY_THRESHOLD = 1.0 / 6.0
BRANCH_A_RULE = (
    "edge_identity_event_count <= 78.000 and "
    "edge_identity_support_edge_density >= 0.166667"
)
BRANCH_B_RULE = "anchor_closure_intensity_gap >= -6.500 and mid_anchor_closure_peak >= 9.000"
COMBINED_RULE = f"({BRANCH_A_RULE}) or ({BRANCH_B_RULE})"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    return parser


def build_rows(frontier_log: Path) -> list[object]:
    residual_rows = build_combined_residual_rows(frontier_log)
    frontier_by_source = {
        row.source_name: row for row in reconstruct_low_overlap_rows(frontier_log)
    }

    row_cls = make_dataclass(
        "ResidualBranchCombinerRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("anchor_closure_intensity_gap", float),
            ("mid_anchor_closure_peak", float),
            ("edge_identity_event_count", float),
            ("edge_identity_support_edge_density", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for row in residual_rows:
        source_name = getattr(row, "source_name")
        own_metrics = support_edge_identity_own_metrics(set(frontier_by_source[source_name].nodes))
        rows.append(
            row_cls(
                source_name=source_name,
                subtype=getattr(row, "subtype"),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                edge_identity_event_count=float(own_metrics["edge_identity_event_count"]),
                edge_identity_support_edge_density=float(
                    own_metrics["edge_identity_support_edge_density"]
                ),
            )
        )
    return sorted(rows, key=lambda item: getattr(item, "source_name"))


def format_counts(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{subtype}:{counts[subtype]}" for subtype in sorted(counts))


def branch_a(row: object) -> bool:
    return (
        float(getattr(row, "edge_identity_event_count")) <= 78.0
        and float(getattr(row, "edge_identity_support_edge_density"))
        >= BRANCH_A_DENSITY_THRESHOLD
    )


def branch_b(row: object) -> bool:
    return (
        float(getattr(row, "anchor_closure_intensity_gap")) >= -6.5
        and float(getattr(row, "mid_anchor_closure_peak")) >= 9.0
    )


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


def render_rule_summary(title: str, rows: list[object], predicate) -> str:
    matched = [row for row in rows if predicate(row)]
    residual = [row for row in rows if not predicate(row)]
    tp, fp, fn = confusion(rows, predicate)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    lines = [
        title,
        "=" * len(title),
        f"tp/fp/fn={tp}/{fp}/{fn}",
        f"precision={precision:.3f} recall={recall:.3f}",
        f"matched={len(matched)} ({format_counts(matched)})",
        f"residual={len(residual)} ({format_counts(residual)})",
    ]
    return "\n".join(lines)


def render_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"edge_events={float(getattr(row, 'edge_identity_event_count')):.3f} "
            f"edge_density={float(getattr(row, 'edge_identity_support_edge_density')):.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap residual branch combiner started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)

    both = [row for row in rows if branch_a(row) and branch_b(row)]
    a_only = [row for row in rows if branch_a(row) and not branch_b(row)]
    b_only = [row for row in rows if branch_b(row) and not branch_a(row)]
    neither = [row for row in rows if not branch_a(row) and not branch_b(row)]

    print()
    print("Low-Overlap Residual Branch Combiner")
    print("====================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("residual_filter=predict_subtype == unmatched under combined-law projection")
    print(f"rows={len(rows)} ({format_counts(rows)})")
    print(f"branch_a={BRANCH_A_RULE}")
    print("branch_a_note=prior scan rounded the winning density threshold to 0.167; exact row-value threshold is 1/6")
    print(f"branch_b={BRANCH_B_RULE}")
    print(f"combined={COMBINED_RULE}")
    print()
    print(render_rule_summary("Branch A summary", rows, branch_a))
    print()
    print(render_rule_summary("Branch B summary", rows, branch_b))
    print()
    print(render_rule_summary("Combined branch summary", rows, lambda row: branch_a(row) or branch_b(row)))
    print()
    print("Branch overlap counts")
    print("=====================")
    print(f"both={len(both)} ({format_counts(both)})")
    print(f"a_only={len(a_only)} ({format_counts(a_only)})")
    print(f"b_only={len(b_only)} ({format_counts(b_only)})")
    print(f"neither={len(neither)} ({format_counts(neither)})")
    print()
    print(render_rows("Branch A only rows", a_only))
    print()
    print(render_rows("Branch B only rows", b_only))
    print()
    print(
        "low-overlap residual branch combiner completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
