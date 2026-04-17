#!/usr/bin/env python3
"""Summarize the most physical exact one-term baseline-side separators on the zero-distance rows."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_equivalence_scan import (  # noqa: E402
    Predicate,
    _critical_thresholds,
    _mask_for,
    _metrics,
    _stable_interval,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_features import (  # noqa: E402
    load_zero_distance_feature_rows,
)


PHYSICAL_NAMES = [
    "support_node_count",
    "support_edge_count",
    "support_role_bridge_count",
    "support_edge_role_bridge__bridge_count",
    "edge_identity_closed_pair_count",
    "edge_identity_open_pair_count",
    "edge_identity_support_edge_density",
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
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline zero-distance physical rule card started {started}", flush=True)
    total_start = time.time()

    rows, rescued_names, baseline_peer_names = load_zero_distance_feature_rows(
        Path(args.frontier_log).resolve(),
        Path(args.bucket_log).resolve(),
        bucket_key=args.bucket_key,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    rescued_mask = 0
    baseline_mask = 0
    for idx, row in enumerate(rows):
        if getattr(row, "group") == "rescued":
            rescued_mask |= 1 << idx
        else:
            baseline_mask |= 1 << idx

    exact_rows = []
    for name in PHYSICAL_NAMES:
        for threshold in _critical_thresholds(rows, name):
            for op in ("<=", ">="):
                pred = Predicate(name=name, op=op, threshold=threshold, mask=_mask_for(rows, name, op, threshold))
                metrics = _metrics(pred.mask, rescued_mask, baseline_mask, len(rows))
                if metrics != (2, 0, 0):
                    continue
                interval = _stable_interval(rows, pred)
                exact_rows.append((interval[2], pred, interval))
    exact_rows.sort(key=lambda item: (-item[0], item[1].text))

    print()
    print("Center-Spine Bucket 00 Baseline Zero-Distance Physical Rule Card")
    print("================================================================")
    print(f"rescued_sources={', '.join(rescued_names)}")
    print(f"baseline_peer_sources={', '.join(baseline_peer_names)}")
    print()
    if not exact_rows:
        print("no exact physical one-term rules")
    else:
        print("Exact physical one-term rescued-vs-peer rules")
        print("---------------------------------------------")
        for idx, (width, pred, interval) in enumerate(exact_rows, start=1):
            print(f"{idx}. {pred.text} width={width:.3f} interval={interval[3]}")
    print()
    print("Row values")
    print("----------")
    for row in rows:
        print(getattr(row, "source_name"))
        for name in PHYSICAL_NAMES:
            print(f"  {name}={float(getattr(row, name)):.3f}")
    print()
    print(
        "baseline zero-distance physical rule card completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
