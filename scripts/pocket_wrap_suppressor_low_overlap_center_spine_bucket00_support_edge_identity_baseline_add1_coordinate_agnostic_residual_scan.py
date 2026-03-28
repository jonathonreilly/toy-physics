#!/usr/bin/env python3
"""Inspect residual rows around the best coordinate-agnostic baseline add1 peer rule."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_row_builders import (  # noqa: E402
    build_coordinate_agnostic_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_branch_decomposition import (  # noqa: E402
    MOTIF_CELLS,
    load_bucket_frontier_inputs,
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
    print(f"baseline add1 coordinate-agnostic residual scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    bucket_rows, frontier_rows = load_bucket_frontier_inputs(
        frontier_log,
        bucket_log,
        bucket_key=args.bucket_key,
    )
    rows, rescued_names = build_coordinate_agnostic_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    hits = [
        row for row in rows
        if float(getattr(row, "max_candidate_adj_bridge_count")) >= args.threshold
    ]
    misses = [row for row in rows if row not in hits]

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Coordinate-Agnostic Residual Scan")
    print("======================================================================")
    print(f"threshold=max_candidate_adj_bridge_count >= {args.threshold:.1f}")
    print(f"rescued_sources={', '.join(sorted(rescued_names))}")
    print(f"motif_cells={MOTIF_CELLS}")
    print()
    print("Rule hits")
    print("---------")
    for row in hits:
        print(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"max_adj_bridge={float(getattr(row, 'max_candidate_adj_bridge_count')):.1f} "
            f"top_cell=({int(getattr(row, 'top_cell_x'))},{int(getattr(row, 'top_cell_y'))}) "
            f"top_cell_is_motif={int(getattr(row, 'top_cell_is_motif'))}"
        )
    print()
    print("Near misses (max_adj_bridge >= 4)")
    print("-------------------------------")
    for row in misses:
        if float(getattr(row, "max_candidate_adj_bridge_count")) < 4.0:
            continue
        print(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"max_adj_bridge={float(getattr(row, 'max_candidate_adj_bridge_count')):.1f} "
            f"top_cell=({int(getattr(row, 'top_cell_x'))},{int(getattr(row, 'top_cell_y'))}) "
            f"top_cell_is_motif={int(getattr(row, 'top_cell_is_motif'))} "
            f"support_bridge={float(getattr(row, 'support_role_bridge_count')):.1f} "
            f"closed_pairs={float(getattr(row, 'edge_identity_closed_pair_count')):.1f}"
        )
    print()
    print(
        "baseline add1 coordinate-agnostic residual scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
