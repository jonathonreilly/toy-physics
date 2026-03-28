#!/usr/bin/env python3
"""Test whether the baseline add1 peer branch compresses to coarse position bands over high-bridge candidate cells."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition import (  # noqa: E402
    load_bucket_frontier_inputs,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_row_builders import (  # noqa: E402
    build_coordinate_band_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
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
    parser.add_argument("--predicate-limit", type=int, default=24)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=10)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 coordinate band scan started {started}", flush=True)
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

    feature_names = [name for name in rows[0].__dataclass_fields__ if name not in ("source_name", "subtype")]
    peer_rules = evaluate_rules(
        rows,
        target_subtype="peer_motif",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    non_peer_rules = evaluate_rules(
        rows,
        target_subtype="non_peer",
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Coordinate Band Scan")
    print("=========================================================")
    print(f"baseline_add1_rows={len(rows)}")
    print(f"peer_motif_rows={sum(1 for row in rows if getattr(row, 'subtype') == 'peer_motif')}")
    print()
    print(render_rules("Candidate peer-motif coordinate-band rules", peer_rules))
    print()
    print(render_rules("Candidate non-peer coordinate-band rules", non_peer_rules))
    print()
    print("Rows")
    print("----")
    for row in rows:
        print(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"left_low={float(getattr(row, 'high_bridge_left_low_count')):.1f} "
            f"left_center={float(getattr(row, 'high_bridge_left_center_count')):.1f} "
            f"right_center={float(getattr(row, 'high_bridge_right_center_count')):.1f} "
            f"mid_low={float(getattr(row, 'high_bridge_mid_low_count')):.1f} "
            f"cells={float(getattr(row, 'high_bridge_cell_count')):.1f}"
        )
    print()
    print(
        "baseline add1 coordinate band scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
