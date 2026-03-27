#!/usr/bin/env python3
"""Scan fixed-baseline rescue clauses for non-fragile two-clause closure windows."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)


@dataclass(frozen=True)
class Predicate:
    name: str
    op: str
    threshold: float
    mask: int

    @property
    def text(self) -> str:
        return f"{self.name} {self.op} {self.threshold:.3f}"


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
    parser.add_argument("--predicate-limit", type=int, default=64)
    parser.add_argument("--baseline-name", default="delta_edge_identity_support_edge_density")
    parser.add_argument("--baseline-op", choices=["<=", ">="], default="<=")
    parser.add_argument(
        "--rescue-names",
        nargs="+",
        default=["pair_distance_z", "abs_delta_edge_identity_open_pair_count"],
    )
    return parser


def _mask_for(rows: list[object], name: str, op: str, threshold: float) -> int:
    mask = 0
    for idx, row in enumerate(rows):
        value = float(getattr(row, name))
        if (op == "<=" and value <= threshold) or (op == ">=" and value >= threshold):
            mask |= 1 << idx
    return mask


def _critical_thresholds(rows: list[object], name: str) -> list[float]:
    values = sorted({float(getattr(row, name)) for row in rows})
    if len(values) == 1:
        return [values[0]]
    return [(left + right) / 2.0 for left, right in zip(values, values[1:])]


def candidate_predicates(rows: list[object], names: list[str]) -> list[Predicate]:
    full_mask = (1 << len(rows)) - 1
    unique_by_mask: dict[int, Predicate] = {}
    for name in names:
        for threshold in _critical_thresholds(rows, name):
            for op in ("<=", ">="):
                mask = _mask_for(rows, name, op, threshold)
                if mask in (0, full_mask):
                    continue
                pred = Predicate(name=name, op=op, threshold=threshold, mask=mask)
                if mask not in unique_by_mask or pred.text < unique_by_mask[mask].text:
                    unique_by_mask[mask] = pred
    out = list(unique_by_mask.values())
    out.sort(key=lambda pred: pred.text)
    return out


def _metrics(mask: int, target_mask: int, non_target_mask: int, total: int) -> tuple[int, int, int]:
    tp = (mask & target_mask).bit_count()
    fp = (mask & non_target_mask).bit_count()
    fn = (target_mask & (((1 << total) - 1) ^ mask)).bit_count()
    return tp, fp, fn


def _stable_window(rows: list[object], pred: Predicate) -> list[float]:
    thresholds = _critical_thresholds(rows, pred.name)
    out = []
    for threshold in thresholds:
        if _mask_for(rows, pred.name, pred.op, threshold) == pred.mask:
            out.append(threshold)
    return out or [pred.threshold]


def _mask_names(rows: list[object], mask: int) -> list[str]:
    return [getattr(row, "source_name") for idx, row in enumerate(rows) if mask & (1 << idx)]


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 rescue-window scan started {started}", flush=True)
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

    rows, _selected_events, _selected_fields, _nearest = build_rows(
        frontier_rows,
        bucket_rows,
        event_limit=args.event_limit,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        selector_target="left",
    )

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
    ranked = []
    for pred in predicates_all:
        tp, fp, fn = _metrics(pred.mask, left_mask, right_mask, len(rows))
        ranked.append((fp != 0, -tp, fn, pred.text, pred))
    ranked.sort(key=lambda item: item[:4])
    top_predicates = [item[4] for item in ranked[: min(args.predicate_limit, len(ranked))]]

    baseline_candidates = [
        pred
        for pred in top_predicates
        if pred.name == args.baseline_name and pred.op == args.baseline_op and (pred.mask & right_mask) == 0
    ]
    if not baseline_candidates:
        raise RuntimeError("no matching fixed-baseline predicate found in candidate set")
    baseline = max(baseline_candidates, key=lambda pred: (_metrics(pred.mask, left_mask, right_mask, len(rows))[0], pred.text))

    baseline_tp, baseline_fp, baseline_fn = _metrics(baseline.mask, left_mask, right_mask, len(rows))
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline.mask)
    miss_names = _mask_names(rows, miss_mask)

    exact_rescues: list[tuple[int, float, str, Predicate, int, list[float]]] = []
    for pred in top_predicates:
        if (pred.mask & right_mask) != 0:
            continue
        if (pred.mask & miss_mask) == 0:
            continue
        combined = baseline.mask | pred.mask
        tp, fp, fn = _metrics(combined, left_mask, right_mask, len(rows))
        if not (fp == 0 and fn == 0):
            continue
        window = _stable_window(rows, pred)
        width = max(window) - min(window)
        exact_rescues.append((len(window), width, pred.text, pred, tp, window))

    exact_rescues.sort(key=lambda item: (-item[0], -item[1], item[2]))
    named_rescues = [row for row in exact_rescues if row[3].name in set(args.rescue_names)]

    print()
    print("Center-Spine Bucket 00 Fixed-Baseline Rescue Scan")
    print("=================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)}")
    print()
    print("Fixed baseline clause")
    print("---------------------")
    print(f"{baseline.text}")
    print(f"baseline_metrics: tp/fp/fn={baseline_tp}/{baseline_fp}/{baseline_fn}")
    print(f"baseline_missed_rows: {', '.join(miss_names)}")
    print()
    print("Named rescue-coordinate closures")
    print("-------------------------------")
    if not named_rescues:
        print("none")
    else:
        for count, width, _text, pred, tp, window in named_rescues:
            print(
                f"{pred.text} -> closure tp/fp/fn={tp}/0/0 "
                + f"stable_thresholds={count} width={width:.3f} "
                + f"window=[{min(window):.3f}, {max(window):.3f}]"
            )
    print()
    print("Best exact two-clause alternates (baseline OR rescue)")
    print("------------------------------------------------------")
    if not exact_rescues:
        print("none")
    else:
        for idx, (count, width, _text, pred, tp, window) in enumerate(exact_rescues[:8], start=1):
            print(
                f"{idx}. {pred.text} -> closure tp/fp/fn={tp}/0/0 "
                + f"stable_thresholds={count} width={width:.3f} "
                + f"window=[{min(window):.3f}, {max(window):.3f}]"
            )
    print()
    non_fragile = [item for item in exact_rescues if item[0] > 1]
    print("Non-fragile exact closures")
    print("--------------------------")
    if not non_fragile:
        print("none (all exact rescue windows are single-threshold)")
    else:
        for count, width, _text, pred, _tp, window in non_fragile:
            print(
                f"{pred.text} stable_thresholds={count} width={width:.3f} "
                + f"window=[{min(window):.3f}, {max(window):.3f}]"
            )
    print()
    print(
        "center-spine bucket00 rescue-window scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
