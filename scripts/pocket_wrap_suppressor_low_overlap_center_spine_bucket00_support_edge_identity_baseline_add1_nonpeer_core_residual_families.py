#!/usr/bin/env python3
"""Map the residual non-peer baseline-core rows after removing the two dominant families."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_band_scan import (  # noqa: E402
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    PRIMARY_SUPPORT_FAMILY_BUCKETS,
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
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _mid_low_bin(value: float) -> str:
    if value <= 0.5:
        return "ml0"
    if value <= 1.5:
        return "ml1"
    return "ml2p"


def _cell_bin(value: float) -> str:
    if value <= 2.5:
        return "c2"
    if value <= 3.5:
        return "c3"
    return "c4p"


def _primary_key(row: object) -> str:
    return "|".join(
        [
            f"rc{int(float(getattr(row, 'high_bridge_right_center_count')) >= 0.5)}",
            _mid_low_bin(float(getattr(row, "high_bridge_mid_low_count"))),
            _cell_bin(float(getattr(row, "high_bridge_cell_count"))),
        ]
    )


def _residual_key(row: object) -> str:
    return "|".join(
        [
            f"rc{int(float(getattr(row, 'high_bridge_right_center_count')) >= 0.5)}",
            f"sbh{int(float(getattr(row, 'support_role_bridge_count')) >= 19.0)}",
            f"cp_hi{int(float(getattr(row, 'edge_identity_closed_pair_count')) >= 71.0)}",
            _mid_low_bin(float(getattr(row, "high_bridge_mid_low_count"))),
            _cell_bin(float(getattr(row, "high_bridge_cell_count"))),
        ]
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 non-peer residual families started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    bucket_rows = [row for row in load_bucket_rows(bucket_log) if row.bucket_key == args.bucket_key]
    selected_sources = {row.source_name for row in bucket_rows}
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in selected_sources
    }
    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )
    non_peer_rows = [
        row
        for row in rows
        if getattr(row, "subtype") == "non_peer"
        and _primary_key(row) not in PRIMARY_SUPPORT_FAMILY_BUCKETS
    ]

    grouped: dict[str, list[object]] = defaultdict(list)
    for row in non_peer_rows:
        grouped[_residual_key(row)].append(row)

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Non-Peer Residual Families")
    print("================================================================")
    print(f"residual_rows={len(non_peer_rows)}")
    print(f"primary_buckets={sorted(PRIMARY_SUPPORT_FAMILY_BUCKETS)}")
    print()
    for idx, (key, bucket_rows0) in enumerate(sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])), start=1):
        print(f"{idx}. bucket={key} count={len(bucket_rows0)}")
        print("   rows=" + ", ".join(getattr(row, "source_name") for row in bucket_rows0))
    print()

    kept_keys = {key for key, bucket_rows0 in grouped.items() if len(bucket_rows0) >= 2}
    if kept_keys:
        row_cls = make_dataclass(
            "BaselineAdd1NonPeerResidualFamilyRow",
            [
                ("source_name", str),
                ("subtype", str),
                ("edge_identity_closed_pair_count", float),
                ("support_role_bridge_count", float),
                ("high_bridge_left_count", float),
                ("high_bridge_mid_low_count", float),
                ("high_bridge_right_center_count", float),
                ("high_bridge_cell_count", float),
                ("high_bridge_mid_count", float),
                ("high_bridge_low_count", float),
            ],
            frozen=True,
        )
        rule_rows = [
            row_cls(
                source_name=getattr(row, "source_name"),
                subtype=_residual_key(row),
                edge_identity_closed_pair_count=float(getattr(row, "edge_identity_closed_pair_count")),
                support_role_bridge_count=float(getattr(row, "support_role_bridge_count")),
                high_bridge_left_count=float(getattr(row, "high_bridge_left_count")),
                high_bridge_mid_low_count=float(getattr(row, "high_bridge_mid_low_count")),
                high_bridge_right_center_count=float(getattr(row, "high_bridge_right_center_count")),
                high_bridge_cell_count=float(getattr(row, "high_bridge_cell_count")),
                high_bridge_mid_count=float(getattr(row, "high_bridge_mid_count")),
                high_bridge_low_count=float(getattr(row, "high_bridge_low_count")),
            )
            for row in non_peer_rows
            if _residual_key(row) in kept_keys
        ]
        feature_names = [name for name in rule_rows[0].__dataclass_fields__ if name not in ("source_name", "subtype")]
        print(f"kept_residual_buckets={Counter(_residual_key(row) for row in non_peer_rows if _residual_key(row) in kept_keys)}")
        print()
        for key in sorted(kept_keys):
            rules = evaluate_rules(
                rule_rows,
                target_subtype=key,
                feature_names=feature_names,
                predicate_limit=args.predicate_limit,
                max_terms=args.max_terms,
                row_limit=args.row_limit,
            )
            print(f"Bucket {key}")
            print(render_rules(f"Best rules for {key}", rules))
            print()

    print(
        "baseline add1 non-peer residual families completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
