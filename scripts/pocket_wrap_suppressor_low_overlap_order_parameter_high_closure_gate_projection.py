#!/usr/bin/env python3
"""Project high-closure exact cell rules onto the full frozen rc0|ml0|c2 bucket."""

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

from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
    build_rc0_ml0_c2_core_inputs,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    build_candidate_anchor_rows,
)


ADD4_RULE = "anchor_deep_share_gap <= 0.450 and high_bridge_high_count >= 0.500"
PAIR_ONLY_RULE = "edge_identity_closed_pair_count <= 56.000 and support_load <= 13.500"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    return parser


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _is_add4_rule(row: object) -> bool:
    return (
        float(getattr(row, "anchor_deep_share_gap")) <= 0.450
        and float(getattr(row, "high_bridge_high_count")) >= 0.500
    )


def _is_pair_only_rule(row: object) -> bool:
    return (
        float(getattr(row, "edge_identity_closed_pair_count")) <= 56.0
        and float(getattr(row, "support_load")) <= 13.5
    )


def _classify(row: object) -> str:
    add4 = _is_add4_rule(row)
    pair_only = _is_pair_only_rule(row)
    if add4 and not pair_only:
        return "add4-sensitive"
    if pair_only and not add4:
        return "pair-only-sensitive"
    if add4 and pair_only:
        return "ambiguous"
    return "unmatched"


def _format_counts(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    return ", ".join(f"{k}:{counts[k]}" for k in sorted(counts))


def build_rows(frontier_log: Path) -> list[object]:
    coarse_by_source, _ = build_rc0_ml0_c2_core_inputs(frontier_log)
    anchor_by_source = {
        row.source_name: row for row in build_candidate_anchor_rows(frontier_log)
    }
    row_cls = make_dataclass(
        "HighClosureGateProjectionRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("support_load", float),
            ("mid_anchor_closure_peak", float),
            ("anchor_closure_intensity_gap", float),
            ("anchor_deep_share_gap", float),
            ("high_bridge_high_count", float),
            ("edge_identity_closed_pair_count", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for source_name in sorted(coarse_by_source):
        coarse = coarse_by_source[source_name]
        anchor = anchor_by_source[source_name]
        mid_count = float(getattr(anchor, "mid_candidate_count"))
        left_count = float(getattr(anchor, "left_candidate_count"))
        mid_peak = float(getattr(anchor, "mid_candidate_bridge_bridge_closed_pair_max"))
        left_peak = float(getattr(anchor, "left_candidate_bridge_bridge_closed_pair_max"))
        intensity_gap = _ratio(mid_peak, mid_count) - _ratio(left_peak, left_count)
        deep_share_gap = _ratio(
            float(getattr(anchor, "mid_candidate_deep_count")),
            mid_count,
        ) - _ratio(
            float(getattr(anchor, "left_candidate_deep_count")),
            left_count,
        )
        rows.append(
            row_cls(
                source_name=source_name,
                subtype=coarse.subtype,
                support_load=float(coarse.support_role_bridge_count),
                mid_anchor_closure_peak=mid_peak,
                anchor_closure_intensity_gap=intensity_gap,
                anchor_deep_share_gap=deep_share_gap,
                high_bridge_high_count=float(coarse.high_bridge_high_count),
                edge_identity_closed_pair_count=float(coarse.edge_identity_closed_pair_count),
            )
        )
    return rows


def render(rows: list[object]) -> str:
    gated = [
        row
        for row in rows
        if float(getattr(row, "mid_anchor_closure_peak")) >= 11.0
        and float(getattr(row, "anchor_closure_intensity_gap")) > 0.0
    ]
    nongated = [row for row in rows if row not in gated]

    add4_hits = [row for row in gated if _classify(row) == "add4-sensitive"]
    pair_only_hits = [row for row in gated if _classify(row) == "pair-only-sensitive"]
    ambiguous_hits = [row for row in gated if _classify(row) == "ambiguous"]
    unmatched_hits = [row for row in gated if _classify(row) == "unmatched"]
    misclassified = [
        row
        for row in gated
        if _classify(row) in {"add4-sensitive", "pair-only-sensitive"}
        and _classify(row) != getattr(row, "subtype")
    ]

    lines = [
        "Low-Overlap High-Closure Gate Projection",
        "========================================",
        f"bucket={RC0_ML0_C2_BUCKET}",
        f"rows_total={len(rows)}",
        f"rows_gated={len(gated)} ({_format_counts(gated)})",
        f"rows_outside_gate={len(nongated)} ({_format_counts(nongated)})",
        f"gate=mid_anchor_closure_peak >= 11 and anchor_closure_intensity_gap > 0",
        f"rule_add4={ADD4_RULE}",
        f"rule_pair_only={PAIR_ONLY_RULE}",
        "",
        "Gated classification counts",
        "--------------------------",
        f"add4-sensitive: {len(add4_hits)} ({_format_counts(add4_hits) if add4_hits else 'none'})",
        f"pair-only-sensitive: {len(pair_only_hits)} ({_format_counts(pair_only_hits) if pair_only_hits else 'none'})",
        f"ambiguous: {len(ambiguous_hits)} ({_format_counts(ambiguous_hits) if ambiguous_hits else 'none'})",
        f"unmatched: {len(unmatched_hits)} ({_format_counts(unmatched_hits) if unmatched_hits else 'none'})",
        "",
        "Gated misclassifications",
        "-----------------------",
    ]
    if not misclassified:
        lines.append("none")
    else:
        for row in misclassified:
            lines.append(
                f"{getattr(row, 'source_name')} actual={getattr(row, 'subtype')} predicted={_classify(row)}"
            )

    lines.extend(
        [
            "",
            "Gated unmatched rows",
            "-------------------",
        ]
    )
    if not unmatched_hits:
        lines.append("none")
    else:
        for row in unmatched_hits:
            lines.append(
                f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
                f"support_load={float(getattr(row, 'support_load')):.3f} "
                f"deep_gap={float(getattr(row, 'anchor_deep_share_gap')):.3f} "
                f"high_bridge_high_count={float(getattr(row, 'high_bridge_high_count')):.3f} "
                f"closed_pairs={float(getattr(row, 'edge_identity_closed_pair_count')):.3f}"
            )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap high-closure gate projection started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    print()
    print(f"frontier_log={frontier_log}")
    print(render(rows))
    print()
    print(
        "low-overlap high-closure gate projection completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
