#!/usr/bin/env python3
"""Project the refined low-overlap subtype law onto the full frozen bucket."""

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
from pocket_wrap_suppressor_low_overlap_order_parameter_asymmetry_map import (  # noqa: E402
    build_rows as build_asymmetry_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
    build_rc0_ml0_c2_core_inputs,
    support_edge_identity_own_metrics,
)


HIGH_CLOSURE_GATE = "mid_anchor_closure_peak >= 11 and anchor_closure_intensity_gap > 0"
HIGH_CLOSURE_ADD4_RULE = (
    "anchor_deep_share_gap <= 0.450 and high_bridge_high_count >= 0.500"
)
HIGH_CLOSURE_PAIR_ONLY_RULE = (
    "edge_identity_closed_pair_count <= 56.000 and support_load <= 13.500"
)
OUTSIDE_GATE_PAIR_ONLY_RULE = (
    "(closure_load <= 46.500 and not (mid_anchor_closure_peak <= 0 and high_bridge_right_count <= 0)) "
    "or (high_bridge_right_low_count >= 1 and support_load <= 14.500 and mid_anchor_closure_peak <= 1)"
)
OUTSIDE_GATE_ADD4_RULE = (
    "edge_identity_event_count <= 78.000 and edge_identity_support_edge_density >= 0.166667 "
    "and mid_anchor_closure_peak >= 1.000 and not (closure_load <= 50.500 and edge_identity_support_edge_density <= 0.182)"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    return parser


def build_rows(frontier_log: Path) -> list[object]:
    asymmetry_by_source = {
        row.source_name: row for row in build_asymmetry_rows(frontier_log)
    }
    coarse_by_source, _ = build_rc0_ml0_c2_core_inputs(frontier_log)
    frontier_by_source = {
        row.source_name: row for row in reconstruct_low_overlap_rows(frontier_log)
    }

    row_cls = make_dataclass(
        "FullBucketExactProjectionRow",
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
            ("edge_identity_event_count", float),
            ("edge_identity_support_edge_density", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for source_name in sorted(asymmetry_by_source):
        asymmetry = asymmetry_by_source[source_name]
        coarse = coarse_by_source[source_name]
        own_metrics = support_edge_identity_own_metrics(set(frontier_by_source[source_name].nodes))
        rows.append(
            row_cls(
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
                high_bridge_right_low_count=float(
                    getattr(coarse, "high_bridge_right_low_count")
                ),
                edge_identity_event_count=float(own_metrics["edge_identity_event_count"]),
                edge_identity_support_edge_density=float(
                    own_metrics["edge_identity_support_edge_density"]
                ),
            )
        )
    return rows


def is_high_gate(row: object) -> bool:
    return (
        float(getattr(row, "mid_anchor_closure_peak")) >= 11.0
        and float(getattr(row, "anchor_closure_intensity_gap")) > 0.0
    )


def is_high_add4(row: object) -> bool:
    return (
        float(getattr(row, "anchor_deep_share_gap")) <= 0.450
        and float(getattr(row, "high_bridge_high_count")) >= 0.500
    )


def is_high_pair_only(row: object) -> bool:
    return (
        float(getattr(row, "closure_load")) <= 56.0
        and float(getattr(row, "support_load")) <= 13.5
    )


def is_outside_pair_only(row: object) -> bool:
    return (
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
    )


def is_outside_add4(row: object) -> bool:
    return (
        float(getattr(row, "edge_identity_event_count")) <= 78.0
        and float(getattr(row, "edge_identity_support_edge_density")) >= (1.0 / 6.0)
        and float(getattr(row, "mid_anchor_closure_peak")) >= 1.0
        and not (
            float(getattr(row, "closure_load")) <= 50.5
            and float(getattr(row, "edge_identity_support_edge_density")) <= 0.182
        )
    )


def predict_subtype(row: object) -> str:
    if is_high_gate(row):
        add4_hit = is_high_add4(row)
        pair_hit = is_high_pair_only(row)
        if add4_hit and not pair_hit:
            return "add4-sensitive"
        if pair_hit and not add4_hit:
            return "pair-only-sensitive"
        if add4_hit and pair_hit:
            return "ambiguous"
        return "unmatched"

    if is_outside_pair_only(row):
        return "pair-only-sensitive"
    if is_outside_add4(row):
        return "add4-sensitive"
    return "add1-sensitive"


def predict_branch(row: object) -> str:
    if is_high_gate(row):
        if is_high_add4(row) and not is_high_pair_only(row):
            return "high-closure-add4"
        if is_high_pair_only(row) and not is_high_add4(row):
            return "high-closure-pair-only"
        if is_high_add4(row) and is_high_pair_only(row):
            return "high-closure-ambiguous"
        return "high-closure-unmatched"
    if is_outside_pair_only(row):
        return "outside-gate-pair-only"
    if is_outside_add4(row):
        return "outside-gate-add4"
    return "outside-gate-add1-default"


def format_counts(rows: list[object], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def render_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{getattr(row, 'source_name')} actual={getattr(row, 'subtype')} "
            f"predicted={predict_subtype(row)} branch={predict_branch(row)} "
            f"support_load={float(getattr(row, 'support_load')):.3f} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
            f"edge_events={float(getattr(row, 'edge_identity_event_count')):.3f} "
            f"edge_density={float(getattr(row, 'edge_identity_support_edge_density')):.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"full bucket exact projection started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)

    misclassified = [
        row for row in rows if predict_subtype(row) != getattr(row, "subtype")
    ]
    ambiguous = [row for row in rows if predict_subtype(row) == "ambiguous"]
    unmatched = [row for row in rows if predict_subtype(row) == "unmatched"]

    print()
    print("Full Bucket Exact Projection")
    print("============================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"rows_total={len(rows)} ({format_counts(rows)})")
    print(f"high_closure_gate={HIGH_CLOSURE_GATE}")
    print(f"high_closure_add4_rule={HIGH_CLOSURE_ADD4_RULE}")
    print(f"high_closure_pair_only_rule={HIGH_CLOSURE_PAIR_ONLY_RULE}")
    print(f"outside_gate_pair_only_rule={OUTSIDE_GATE_PAIR_ONLY_RULE}")
    print(f"outside_gate_add4_rule={OUTSIDE_GATE_ADD4_RULE}")
    print()
    print("Predicted branch counts")
    print("=======================")
    for branch in (
        "high-closure-add4",
        "high-closure-pair-only",
        "outside-gate-pair-only",
        "outside-gate-add4",
        "outside-gate-add1-default",
    ):
        branch_rows = [row for row in rows if predict_branch(row) == branch]
        print(f"{branch}: {len(branch_rows)} ({format_counts(branch_rows)})")
    print()
    print(f"misclassified={len(misclassified)} ({format_counts(misclassified)})")
    print(f"ambiguous={len(ambiguous)} ({format_counts(ambiguous)})")
    print(f"unmatched={len(unmatched)} ({format_counts(unmatched)})")
    print()
    print(render_rows("Misclassified rows", misclassified))
    print()
    print(
        "full bucket exact projection completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
