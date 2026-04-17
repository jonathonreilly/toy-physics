#!/usr/bin/env python3
"""Scan exact one-term baseline-side separators on the zero-distance rescued/peer rows."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_baseline_zero_distance_features import (  # noqa: E402
    dataclass_feature_names,
    load_zero_distance_feature_rows,
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
    parser.add_argument("--row-limit", type=int, default=16)
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
    if len(values) <= 1:
        return values
    return [(left + right) / 2.0 for left, right in zip(values, values[1:])]


def _stable_interval(rows: list[object], pred: Predicate) -> tuple[float, float, float, str]:
    values = sorted({float(getattr(row, pred.name)) for row in rows})
    if pred.op == "<=":
        included = [value for value in values if value <= pred.threshold]
        excluded = [value for value in values if value > pred.threshold]
        if not included or not excluded:
            return pred.threshold, pred.threshold, 0.0, f"[{pred.threshold:.3f}, {pred.threshold:.3f}]"
        lower = max(included)
        upper = min(excluded)
        return lower, upper, upper - lower, f"[{lower:.3f}, {upper:.3f})"
    included = [value for value in values if value >= pred.threshold]
    excluded = [value for value in values if value < pred.threshold]
    if not included or not excluded:
        return pred.threshold, pred.threshold, 0.0, f"[{pred.threshold:.3f}, {pred.threshold:.3f}]"
    lower = max(excluded)
    upper = min(included)
    return lower, upper, upper - lower, f"({lower:.3f}, {upper:.3f}]"


def _metrics(mask: int, target_mask: int, non_target_mask: int, total: int) -> tuple[int, int, int]:
    tp = (mask & target_mask).bit_count()
    fp = (mask & non_target_mask).bit_count()
    fn = (target_mask & (((1 << total) - 1) ^ mask)).bit_count()
    return tp, fp, fn


def _mask_names(rows: list[object], mask: int) -> list[str]:
    return [getattr(row, "source_name") for idx, row in enumerate(rows) if mask & (1 << idx)]


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"baseline zero-distance equivalence scan started {started}", flush=True)
    total_start = time.time()

    rows, rescued_names, baseline_peer_names = load_zero_distance_feature_rows(
        Path(args.frontier_log).resolve(),
        Path(args.bucket_log).resolve(),
        bucket_key=args.bucket_key,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )
    feature_names = dataclass_feature_names(rows[0])

    rescued_mask = 0
    baseline_mask = 0
    for idx, row in enumerate(rows):
        if getattr(row, "group") == "rescued":
            rescued_mask |= 1 << idx
        else:
            baseline_mask |= 1 << idx

    exact_predicates: list[tuple[float, Predicate, tuple[int, int, int], tuple[float, float, float, str]]] = []
    for name in feature_names:
        for threshold in _critical_thresholds(rows, name):
            for op in ("<=", ">="):
                pred = Predicate(name=name, op=op, threshold=threshold, mask=_mask_for(rows, name, op, threshold))
                metrics = _metrics(pred.mask, rescued_mask, baseline_mask, len(rows))
                if metrics != (2, 0, 0):
                    continue
                interval = _stable_interval(rows, pred)
                exact_predicates.append((interval[2], pred, metrics, interval))

    exact_predicates.sort(key=lambda item: (-item[0], item[1].text))

    print()
    print("Center-Spine Bucket 00 Baseline Zero-Distance Exact Equivalence")
    print("==============================================================")
    print(f"rescued_sources={', '.join(rescued_names)}")
    print(f"baseline_peer_sources={', '.join(baseline_peer_names)}")
    print()
    print("Top exact rescued-vs-peer one-term predicates")
    print("--------------------------------------------")
    if not exact_predicates:
        print("none")
    else:
        for idx, (width, pred, metrics, interval) in enumerate(exact_predicates[: args.row_limit], start=1):
            print(
                f"{idx}. {pred.text} -> tp/fp/fn={metrics[0]}/{metrics[1]}/{metrics[2]} "
                + f"width={width:.3f} interval={interval[3]}"
            )
    print()
    print("Unique exact masks")
    print("------------------")
    masks = {}
    for _width, pred, _metrics0, _interval in exact_predicates:
        masks.setdefault(pred.mask, []).append(pred.text)
    for idx, (mask, texts) in enumerate(sorted(masks.items(), key=lambda item: item[1][0]), start=1):
        print(f"{idx}. matched_rows={', '.join(_mask_names(rows, mask))}")
        for text in texts[:8]:
            print(f"   {text}")
        if len(texts) > 8:
            print(f"   ... {len(texts) - 8} more")
    print()
    print(
        "baseline zero-distance equivalence scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
