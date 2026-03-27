#!/usr/bin/env python3
"""Check whether top-cell coordinates for high local-bridge rows form a small family."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_coordinate_agnostic_local_scan import (  # noqa: E402
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
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
    parser.add_argument("--threshold", type=float, default=6.5)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 coordinate-agnostic top-cell generalization started {started}", flush=True)
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
    rows, _rescued_names = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )
    hits = [
        row for row in rows
        if float(getattr(row, "max_candidate_adj_bridge_count")) >= args.threshold
    ]

    cell_counts = Counter(
        (int(getattr(row, "top_cell_x")), int(getattr(row, "top_cell_y")))
        for row in hits
    )
    subtype_counts = Counter(getattr(row, "subtype") for row in hits)

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Coordinate-Agnostic Top-Cell Generalization")
    print("================================================================================")
    print(f"threshold=max_candidate_adj_bridge_count >= {args.threshold:.1f}")
    print(f"hit_rows={len(hits)}")
    print(f"hit_subtypes={dict(subtype_counts)}")
    print()
    print("Top-cell coordinate counts among high-local-bridge rows")
    print("-------------------------------------------------------")
    for cell, count in cell_counts.most_common():
        print(f"{cell}: {count}")
    print()
    print("Rows")
    print("----")
    for row in hits:
        print(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"top_cell=({int(getattr(row, 'top_cell_x'))},{int(getattr(row, 'top_cell_y'))}) "
            f"max_adj_bridge={float(getattr(row, 'max_candidate_adj_bridge_count')):.1f} "
            f"top_cell_is_motif={int(getattr(row, 'top_cell_is_motif'))}"
        )
    print()
    print(
        "baseline add1 coordinate-agnostic top-cell generalization completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
