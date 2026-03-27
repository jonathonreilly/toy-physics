#!/usr/bin/env python3
"""Render rescued-row pocket-subfamily profiles on the frozen center-spine `00` core."""

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

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    nearest_opposite_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows,
    feature_names,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan import (  # noqa: E402
    Predicate,
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
    parser.add_argument("--top-k", type=int, default=10)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 pocket-subfamily rescue profiles started {started}", flush=True)
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
    by_source = {row.source_name: row for row in bucket_rows}
    nearest = nearest_opposite_rows(
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )
    row_map = {getattr(row, "source_name"): row for row in rows}

    baseline = Predicate(
        name="delta_edge_identity_support_edge_density",
        op="<=",
        threshold=0.018,
        mask=0,
    )
    rescued_sources = []
    for row in rows:
        if getattr(row, "subtype") != args.left_subtype:
            continue
        if float(getattr(row, baseline.name)) > baseline.threshold:
            rescued_sources.append(getattr(row, "source_name"))

    shown_features = [
        name
        for name in feature_names(rows[0])
        if name.startswith("delta_count_pocket_") or name.startswith("abs_delta_count_pocket_")
    ]

    print()
    print("Center-Spine Bucket 00 Pocket-Subfamily Rescue Profiles")
    print("=======================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rescued_sources={', '.join(rescued_sources)}")
    print()

    for source_name in rescued_sources:
        row = row_map[source_name]
        partner_name, distance = nearest[source_name]
        scored = sorted(
            (
                abs(float(getattr(row, name))),
                name,
                float(getattr(row, name)),
            )
            for name in shown_features
            if abs(float(getattr(row, name))) > 0.0
        )
        scored.sort(key=lambda item: (-item[0], item[1]))
        print(f"{source_name} ({by_source[source_name].subtype})")
        print(f"  nearest_opposite={partner_name} distance={distance:.3f}")
        print(f"  delta_edge_identity_support_edge_density={float(getattr(row, 'delta_edge_identity_support_edge_density')):.3f}")
        print(f"  delta_count_pocket_total={float(getattr(row, 'delta_count_pocket_total')):.3f}")
        print(f"  delta_count_pocket_present0={float(getattr(row, 'delta_count_pocket_present0')):.3f}")
        print(f"  delta_count_pocket_present1={float(getattr(row, 'delta_count_pocket_present1')):.3f}")
        print("  top pocket-subfamily deltas:")
        for _abs_value, name, value in scored[: args.top_k]:
            print(f"    {name} = {value:.3f}")
        print()

    print(
        "center-spine bucket00 pocket-subfamily rescue profiles completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
