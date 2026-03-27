#!/usr/bin/env python3
"""Rank exact bucket `00` rescue clauses by actual mask-stable interval width."""

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
    build_rows,
    feature_names,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan import (  # noqa: E402
    Predicate,
    _critical_thresholds,
    _mask_for,
    _metrics,
    _stable_interval,
    _sampled_mask_stable_thresholds,
    candidate_predicates,
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
    parser.add_argument("--event-limit", type=int, default=28)
    parser.add_argument("--predicate-limit", type=int, default=128)
    parser.add_argument("--baseline-name", default="delta_edge_identity_support_edge_density")
    parser.add_argument("--baseline-op", choices=["<=", ">="], default="<=")
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def _field_lookup(rows: list[object]) -> dict[str, str]:
    rows0 = rows[0]
    return {
        name: value
        for name, value in getattr(rows0, "__dataclass_fields__", {}).items()  # type: ignore[attr-defined]
    }


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 interval-priority scan started {started}", flush=True)
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

    rows, selected_events, selected_fields, _nearest = build_rows(
        frontier_rows,
        bucket_rows,
        event_limit=args.event_limit,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        selector_target="left",
    )
    event_lookup = {field_name: event for event, field_name in selected_fields}

    names = feature_names(rows[0])
    allowed = [
        name
        for name in names
        if name.startswith("delta_edge_identity_")
        or name.startswith("abs_delta_edge_identity_")
        or name.startswith("pair_")
        or name.startswith("ev_")
    ]

    left_mask = 0
    right_mask = 0
    for idx, row in enumerate(rows):
        subtype = getattr(row, "subtype")
        if subtype == args.left_subtype:
            left_mask |= 1 << idx
        elif subtype == args.right_subtype:
            right_mask |= 1 << idx

    predicates_all = candidate_predicates(rows, allowed)
    baseline_candidates = [
        pred
        for pred in predicates_all
        if pred.name == args.baseline_name and pred.op == args.baseline_op and (pred.mask & right_mask) == 0
    ]
    if not baseline_candidates:
        raise RuntimeError("no fixed baseline predicate found")
    baseline = max(
        baseline_candidates,
        key=lambda pred: (_metrics(pred.mask, left_mask, right_mask, len(rows))[0], pred.text),
    )
    baseline_tp, baseline_fp, baseline_fn = _metrics(baseline.mask, left_mask, right_mask, len(rows))
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline.mask)

    exact_rescues: list[tuple[float, int, int, str, Predicate, tuple[float, float, float, str]]] = []
    for pred in predicates_all:
        if (pred.mask & right_mask) != 0:
            continue
        if (pred.mask & miss_mask) == 0:
            continue
        combined = baseline.mask | pred.mask
        tp, fp, fn = _metrics(combined, left_mask, right_mask, len(rows))
        if fp != 0 or fn != 0:
            continue
        interval = _stable_interval(rows, pred)
        sampled = _sampled_mask_stable_thresholds(rows, pred)
        exact_rescues.append((interval[2], len(sampled), tp, pred.text, pred, interval))

    exact_rescues.sort(key=lambda item: (-item[0], -item[1], item[3]))

    print()
    print("Center-Spine Bucket 00 Interval-Priority Exact Rescue Scan")
    print("==========================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)}")
    print()
    print("Fixed baseline clause")
    print("---------------------")
    print(f"{baseline.text}")
    print(f"baseline_metrics: tp/fp/fn={baseline_tp}/{baseline_fp}/{baseline_fn}")
    print()
    print("Top exact rescues by actual interval width")
    print("-----------------------------------------")
    if not exact_rescues:
        print("none")
    else:
        for idx, (width, sampled_count, tp, _text, pred, interval) in enumerate(exact_rescues[: args.row_limit], start=1):
            event_text = event_lookup.get(pred.name)
            print(
                f"{idx}. {pred.text} -> closure tp/fp/fn={tp}/0/0 "
                + f"width={width:.3f} sampled_thresholds={sampled_count} interval={interval[3]}"
            )
            if event_text is not None:
                print(f"   event={event_text}")
    print()
    print("Best exact numeric rescues")
    print("--------------------------")
    numeric = [item for item in exact_rescues if not item[4].name.startswith('ev_')]
    if not numeric:
        print("none")
    else:
        for idx, (width, sampled_count, tp, _text, pred, interval) in enumerate(numeric[:8], start=1):
            print(
                f"{idx}. {pred.text} -> closure tp/fp/fn={tp}/0/0 "
                + f"width={width:.3f} sampled_thresholds={sampled_count} interval={interval[3]}"
            )
    print()
    print("Best exact event rescues")
    print("------------------------")
    events = [item for item in exact_rescues if item[4].name.startswith('ev_')]
    if not events:
        print("none")
    else:
        for idx, (width, sampled_count, tp, _text, pred, interval) in enumerate(events[:8], start=1):
            print(
                f"{idx}. {pred.text} -> closure tp/fp/fn={tp}/0/0 "
                + f"width={width:.3f} sampled_thresholds={sampled_count} interval={interval[3]}"
            )
            print(f"   event={event_lookup.get(pred.name, pred.name)}")
    print()
    print(
        "center-spine bucket00 interval-priority scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
