#!/usr/bin/env python3
"""Project the combined low-overlap law onto the full frozen rc0|ml0|c2 bucket."""

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

from pocket_wrap_suppressor_low_overlap_order_parameter_asymmetry_map import (  # noqa: E402
    build_rows as build_asymmetry_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
    build_rc0_ml0_c2_core_inputs,
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
    row_cls = make_dataclass(
        "CombinedLawProjectionRow",
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
        ],
        frozen=True,
    )

    rows: list[object] = []
    for source_name in sorted(asymmetry_by_source):
        asymmetry = asymmetry_by_source[source_name]
        coarse = coarse_by_source[source_name]
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
            )
        )
    return rows


def is_high_closure_gate(row: object) -> bool:
    return (
        float(getattr(row, "mid_anchor_closure_peak")) >= 11.0
        and float(getattr(row, "anchor_closure_intensity_gap")) > 0.0
    )


def is_high_closure_add4(row: object) -> bool:
    return (
        float(getattr(row, "anchor_deep_share_gap")) <= 0.450
        and float(getattr(row, "high_bridge_high_count")) >= 0.500
    )


def is_high_closure_pair_only(row: object) -> bool:
    return (
        float(getattr(row, "closure_load")) <= 56.0
        and float(getattr(row, "support_load")) <= 13.5
    )


def is_outside_gate_pair_only(row: object) -> bool:
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


def predict_subtype(row: object) -> str:
    if is_high_closure_gate(row):
        add4_hit = is_high_closure_add4(row)
        pair_hit = is_high_closure_pair_only(row)
        if add4_hit and not pair_hit:
            return "add4-sensitive"
        if pair_hit and not add4_hit:
            return "pair-only-sensitive"
        if add4_hit and pair_hit:
            return "ambiguous"
        return "unmatched"
    if is_outside_gate_pair_only(row):
        return "pair-only-sensitive"
    return "unmatched"


def predict_branch(row: object) -> str:
    if is_high_closure_gate(row):
        add4_hit = is_high_closure_add4(row)
        pair_hit = is_high_closure_pair_only(row)
        if add4_hit and not pair_hit:
            return "high-closure-add4"
        if pair_hit and not add4_hit:
            return "high-closure-pair-only"
        if add4_hit and pair_hit:
            return "high-closure-ambiguous"
        return "high-closure-unmatched"
    if is_outside_gate_pair_only(row):
        return "outside-gate-pair-only"
    return "outside-gate-unmatched"


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
    for row in sorted(rows, key=lambda item: (getattr(item, "subtype"), getattr(item, "source_name"))):
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"branch={predict_branch(row)} "
            f"support_load={float(getattr(row, 'support_load')):.3f} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
            f"deep_gap={float(getattr(row, 'anchor_deep_share_gap')):.3f} "
            f"high_bridge_high_count={float(getattr(row, 'high_bridge_high_count')):.3f} "
            f"high_bridge_right_count={float(getattr(row, 'high_bridge_right_count')):.3f} "
            f"high_bridge_right_low_count={float(getattr(row, 'high_bridge_right_low_count')):.3f}"
        )
    return "\n".join(lines)


def render_coverage(rows: list[object]) -> str:
    lines = [
        "Actual subtype coverage",
        "=======================",
        "subtype | total | correct | misclassified | unmatched",
        "-------+-------+---------+---------------+----------",
    ]
    for subtype in sorted({getattr(row, "subtype") for row in rows}):
        subtype_rows = [row for row in rows if getattr(row, "subtype") == subtype]
        correct = sum(1 for row in subtype_rows if predict_subtype(row) == subtype)
        misclassified = sum(
            1
            for row in subtype_rows
            if predict_subtype(row) not in {subtype, "unmatched", "ambiguous"}
        )
        unmatched = sum(
            1 for row in subtype_rows if predict_subtype(row) in {"unmatched", "ambiguous"}
        )
        lines.append(
            f"{subtype} | {len(subtype_rows):>5} | {correct:>7} | {misclassified:>13} | {unmatched:>8}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap combined-law projection started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    predicted_add4 = [row for row in rows if predict_subtype(row) == "add4-sensitive"]
    predicted_pair = [row for row in rows if predict_subtype(row) == "pair-only-sensitive"]
    ambiguous = [row for row in rows if predict_subtype(row) == "ambiguous"]
    unmatched = [row for row in rows if predict_subtype(row) == "unmatched"]
    misclassified = [
        row
        for row in rows
        if predict_subtype(row) not in {"unmatched", "ambiguous"}
        and predict_subtype(row) != getattr(row, "subtype")
    ]

    print()
    print("Low-Overlap Combined Law Projection")
    print("===================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"rows_total={len(rows)} ({format_counts(rows)})")
    print(f"high_closure_gate={HIGH_CLOSURE_GATE}")
    print(f"high_closure_add4_rule={HIGH_CLOSURE_ADD4_RULE}")
    print(f"high_closure_pair_only_rule={HIGH_CLOSURE_PAIR_ONLY_RULE}")
    print(f"outside_gate_pair_only_rule={OUTSIDE_GATE_PAIR_ONLY_RULE}")
    print()
    print("Predicted branch counts")
    print("=======================")
    print(
        f"high-closure-add4: {sum(1 for row in rows if predict_branch(row) == 'high-closure-add4')} "
        f"({format_counts([row for row in rows if predict_branch(row) == 'high-closure-add4'])})"
    )
    print(
        f"high-closure-pair-only: {sum(1 for row in rows if predict_branch(row) == 'high-closure-pair-only')} "
        f"({format_counts([row for row in rows if predict_branch(row) == 'high-closure-pair-only'])})"
    )
    print(
        f"outside-gate-pair-only: {sum(1 for row in rows if predict_branch(row) == 'outside-gate-pair-only')} "
        f"({format_counts([row for row in rows if predict_branch(row) == 'outside-gate-pair-only'])})"
    )
    print(
        f"unmatched: {len(unmatched)} ({format_counts(unmatched)})"
    )
    print(
        f"ambiguous: {len(ambiguous)} ({format_counts(ambiguous)})"
    )
    print()
    print(render_coverage(rows))
    print()
    print("Projected hits")
    print("==============")
    print(f"predicted_add4={len(predicted_add4)} ({format_counts(predicted_add4)})")
    print(f"predicted_pair_only={len(predicted_pair)} ({format_counts(predicted_pair)})")
    print()
    print(render_rows("Misclassified rows", misclassified))
    print()
    print(render_rows("Unmatched rows", unmatched))
    print()
    print(
        "low-overlap combined-law projection completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
