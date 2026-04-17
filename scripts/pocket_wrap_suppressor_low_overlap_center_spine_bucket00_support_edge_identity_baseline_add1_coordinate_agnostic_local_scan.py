#!/usr/bin/env python3
"""Test whether the baseline add1 peer branch closes under coordinate-agnostic candidate-local bridge features."""

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
    MOTIF_CELLS,
    load_bucket_frontier_inputs,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_add1_row_builders import (  # noqa: E402
    build_coordinate_agnostic_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)


SHOW_COLUMNS = [
    "source_name",
    "subtype",
    "edge_identity_closed_pair_count",
    "support_role_bridge_count",
    "max_candidate_adj_bridge_count",
    "max_candidate_adj_support_count",
    "max_candidate_adj_support_edge_count",
    "max_candidate_ring_candidate_count",
    "max_candidate_ring_bridge_touch_count",
    "count_candidate_adj_bridge_ge4",
    "count_candidate_adj_bridge_ge6",
    "top_cell_x",
    "top_cell_y",
]


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


def render_rows(rows: list[object]) -> str:
    lines = [
        "Baseline-covered add1 coordinate-agnostic local rows",
        "=====================================================",
        " | ".join(SHOW_COLUMNS),
        " | ".join("-" * len(name) for name in SHOW_COLUMNS),
    ]
    for row in rows:
        values = []
        for name in SHOW_COLUMNS:
            value = getattr(row, name)
            if isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        lines.append(" | ".join(values))
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline add1 coordinate-agnostic local scan started {started}", flush=True)
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
    feature_names = [
        "edge_identity_closed_pair_count",
        "support_role_bridge_count",
        "max_candidate_adj_bridge_count",
        "max_candidate_adj_support_count",
        "max_candidate_adj_support_edge_count",
        "max_candidate_ring_candidate_count",
        "max_candidate_ring_bridge_touch_count",
        "count_candidate_adj_bridge_ge4",
        "count_candidate_adj_bridge_ge6",
        "count_candidate_adj_support_edge_ge8",
        "top_cell_is_motif",
    ]
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
    peer_count = sum(1 for row in rows if getattr(row, "subtype") == "peer_motif")
    non_peer_count = sum(1 for row in rows if getattr(row, "subtype") == "non_peer")

    print()
    print("Center-Spine Bucket 00 Baseline Add1 Coordinate-Agnostic Local Scan")
    print("===================================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(sorted(rescued_names))}")
    print(f"baseline_add1_rows={len(rows)}")
    print(f"peer_branch_rows={peer_count}")
    print(f"non_peer_core_rows={non_peer_count}")
    print()
    print(render_rows(rows))
    print()
    print(render_rules("Candidate peer-branch coordinate-agnostic local rules", peer_rules))
    print()
    print(render_rules("Candidate non-peer-core coordinate-agnostic local rules", non_peer_rules))
    print()
    print(
        "baseline add1 coordinate-agnostic local scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
