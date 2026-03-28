#!/usr/bin/env python3
"""Compare the two high-support ml0 residual satellites inside the non-peer baseline core."""

from __future__ import annotations

import argparse
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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_row_builders import (  # noqa: E402
    build_coordinate_band_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition import (  # noqa: E402
    load_bucket_frontier_inputs,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD,
    HIGH_SUPPORT_ML0_C4P_SPLIT_THRESHOLD,
    HIGH_SUPPORT_ML0_MIN_CELL_COUNT,
    SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument(
        "--bucket-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-micro-buckets-5504-add1-vs-add4.txt",
    )
    parser.add_argument("--bucket-key", default="00")
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    parser.add_argument("--predicate-limit", type=int, default=16)
    parser.add_argument("--max-terms", type=int, default=2)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _is_target_branch(row: object) -> bool:
    return (
        getattr(row, "subtype") == "non_peer"
        and float(getattr(row, "high_bridge_right_center_count")) <= 0.5
        and float(getattr(row, "high_bridge_mid_low_count")) <= 0.5
        and float(getattr(row, "support_role_bridge_count")) >= SUPPORT_ROLE_BRIDGE_HIGH_THRESHOLD
        and float(getattr(row, "edge_identity_closed_pair_count")) >= EDGE_IDENTITY_CLOSED_PAIR_HIGH_THRESHOLD
        and float(getattr(row, "high_bridge_cell_count")) >= HIGH_SUPPORT_ML0_MIN_CELL_COUNT
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 non-peer high-support ml0 split started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    bucket_rows, frontier_rows = load_bucket_frontier_inputs(
        frontier_log,
        bucket_log,
        bucket_key=args.bucket_key,
    )
    rows = build_coordinate_band_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )
    target_rows = [row for row in rows if _is_target_branch(row)]

    row_cls = make_dataclass(
        "BaselineAdd1NonPeerHighSupportMl0SplitRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("support_role_bridge_count", float),
            ("high_bridge_cell_count", float),
            ("high_bridge_left_count", float),
            ("high_bridge_mid_low_count", float),
            ("high_bridge_right_center_count", float),
        ],
        frozen=True,
    )
    rule_rows = [
        row_cls(
            source_name=getattr(row, "source_name"),
            subtype=(
                "c4p"
                if float(getattr(row, "high_bridge_cell_count")) >= HIGH_SUPPORT_ML0_C4P_SPLIT_THRESHOLD
                else "c3"
            ),
            edge_identity_closed_pair_count=float(getattr(row, "edge_identity_closed_pair_count")),
            support_role_bridge_count=float(getattr(row, "support_role_bridge_count")),
            high_bridge_cell_count=float(getattr(row, "high_bridge_cell_count")),
            high_bridge_left_count=float(getattr(row, "high_bridge_left_count")),
            high_bridge_mid_low_count=float(getattr(row, "high_bridge_mid_low_count")),
            high_bridge_right_center_count=float(getattr(row, "high_bridge_right_center_count")),
        )
        for row in target_rows
    ]
    feature_names = [name for name in rule_rows[0].__dataclass_fields__ if name not in ("source_name", "subtype")]

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Non-Peer High-Support ml0 Split")
    print("====================================================================")
    print(f"target_rows={len(rule_rows)}")
    print("rows=" + ", ".join(f"{getattr(row, 'source_name')}:{getattr(row, 'subtype')}" for row in rule_rows))
    print()
    print(render_rules("Best rules for c3", evaluate_rules(
        rule_rows,
        target_subtype="c3",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )))
    print()
    print(render_rules("Best rules for c4p", evaluate_rules(
        rule_rows,
        target_subtype="c4p",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )))
    print()
    print(
        "baseline add1 non-peer high-support ml0 split completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
