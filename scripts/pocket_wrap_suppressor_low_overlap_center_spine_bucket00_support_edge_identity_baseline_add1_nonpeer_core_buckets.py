#!/usr/bin/env python3
"""Bucket the remaining non-peer baseline core using coarse high-bridge band structure."""

from __future__ import annotations

import argparse
from collections import defaultdict
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
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
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
    parser.add_argument("--show-limit", type=int, default=12)
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


def _bucket_key(row: object) -> str:
    return "|".join(
        [
            f"rc{int(float(getattr(row, 'high_bridge_right_center_count')) >= 0.5)}",
            _mid_low_bin(float(getattr(row, "high_bridge_mid_low_count"))),
            _cell_bin(float(getattr(row, "high_bridge_cell_count"))),
        ]
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 non-peer core buckets started {started}", flush=True)
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
    non_peer_rows = [row for row in rows if getattr(row, "subtype") == "non_peer"]

    buckets: dict[str, list[object]] = defaultdict(list)
    for row in non_peer_rows:
        buckets[_bucket_key(row)].append(row)

    ordered = sorted(buckets.items(), key=lambda item: (-len(item[1]), item[0]))

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Non-Peer Core Buckets")
    print("==========================================================")
    print(f"non_peer_rows={len(non_peer_rows)}")
    print()
    for idx, (key, bucket_rows0) in enumerate(ordered[: args.show_limit], start=1):
        closed = [float(getattr(row, "edge_identity_closed_pair_count")) for row in bucket_rows0]
        bridge = [float(getattr(row, "support_role_bridge_count")) for row in bucket_rows0]
        print(f"{idx}. bucket={key} count={len(bucket_rows0)}")
        print(
            f"   closed_pairs=min/max {min(closed):.1f}/{max(closed):.1f} "
            f"support_bridge=min/max {min(bridge):.1f}/{max(bridge):.1f}"
        )
        print("   rows=" + ", ".join(getattr(row, "source_name") for row in bucket_rows0))
    print()
    print(
        "baseline add1 non-peer core buckets completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
