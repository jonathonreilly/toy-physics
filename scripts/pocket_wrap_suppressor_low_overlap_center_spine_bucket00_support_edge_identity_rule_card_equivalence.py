#!/usr/bin/env python3
"""Emit a physical-language rule card for center-spine bucket `00` add1 closure and verify nearby threshold equivalence."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from itertools import product
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
    parser.add_argument("--predicate-limit", type=int, default=36)
    parser.add_argument("--window", type=int, default=2)
    parser.add_argument("--baseline-name")
    parser.add_argument("--baseline-op", choices=("<=", ">="))
    parser.add_argument("--baseline-threshold", type=float)
    parser.add_argument("--baseline-label", default="density stays low")
    parser.add_argument("--rescue-name")
    parser.add_argument("--rescue-op", choices=("<=", ">="))
    parser.add_argument("--rescue-threshold", type=float)
    parser.add_argument(
        "--rescue-label",
        default="wide pair distance (or low open-pair mismatch)",
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


def _metrics(mask: int, target_mask: int, non_target_mask: int, total: int) -> tuple[int, int, int, int]:
    tp = (mask & target_mask).bit_count()
    fp = (mask & non_target_mask).bit_count()
    fn = (target_mask & (((1 << total) - 1) ^ mask)).bit_count()
    return tp, fp, fn, tp + ((non_target_mask & (((1 << total) - 1) ^ mask)).bit_count())


def _mask_names(rows: list[object], mask: int) -> list[str]:
    return [getattr(row, "source_name") for idx, row in enumerate(rows) if mask & (1 << idx)]


def _find_predicate(
    predicates: list[Predicate],
    *,
    name: str | None,
    op: str | None,
    threshold: float | None,
) -> Predicate | None:
    if name is None or op is None or threshold is None:
        return None
    for pred in predicates:
        if pred.name == name and pred.op == op and abs(pred.threshold - threshold) < 1e-9:
            return pred
    return None


def _equivalent_threshold_window(
    rows: list[object],
    pred: Predicate,
    *,
    radius: int,
) -> list[Predicate]:
    critical = _critical_thresholds(rows, pred.name)
    if not critical:
        return [pred]

    nearest_idx = min(range(len(critical)), key=lambda idx: abs(critical[idx] - pred.threshold))
    out: list[Predicate] = []
    for idx in range(max(0, nearest_idx - radius), min(len(critical), nearest_idx + radius + 1)):
        threshold = critical[idx]
        mask = _mask_for(rows, pred.name, pred.op, threshold)
        if mask == pred.mask:
            out.append(Predicate(name=pred.name, op=pred.op, threshold=threshold, mask=mask))
    out.sort(key=lambda item: item.threshold)
    return out or [pred]


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 rule-card equivalence started {started}", flush=True)
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
        tp, fp, fn, _correct = _metrics(pred.mask, left_mask, right_mask, len(rows))
        ranked.append((fp != 0, -tp, fn, pred.text, pred, tp, fp))
    ranked.sort(key=lambda item: item[:4])
    top_predicates = [item[4] for item in ranked[: min(args.predicate_limit, len(ranked))]]

    baseline = _find_predicate(
        predicates_all,
        name=args.baseline_name,
        op=args.baseline_op,
        threshold=args.baseline_threshold,
    )
    baseline_tp = -1
    if baseline is None:
        for pred in top_predicates:
            tp, fp, _fn, _correct = _metrics(pred.mask, left_mask, right_mask, len(rows))
            if fp == 0 and tp > baseline_tp:
                baseline = pred
                baseline_tp = tp
    if baseline is None:
        raise RuntimeError("no zero-FP baseline predicate found")

    baseline_tp, baseline_fp, baseline_fn, baseline_correct = _metrics(
        baseline.mask, left_mask, right_mask, len(rows)
    )
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline.mask)

    best_clause = _find_predicate(
        predicates_all,
        name=args.rescue_name,
        op=args.rescue_op,
        threshold=args.rescue_threshold,
    )
    best_key: tuple[int, int, str] | None = None
    best_combined_mask = baseline.mask
    if best_clause is None:
        for pred in top_predicates:
            if pred.mask & right_mask:
                continue
            if (pred.mask & miss_mask) == 0:
                continue
            combined = baseline.mask | pred.mask
            tp, fp, fn, _correct = _metrics(combined, left_mask, right_mask, len(rows))
            if fp != 0:
                continue
            key = (fn, -tp, pred.text)
            if best_key is None or key < best_key:
                best_key = key
                best_clause = pred
                best_combined_mask = combined
    else:
        best_combined_mask = baseline.mask | best_clause.mask
        tp, fp, fn, _correct = _metrics(best_combined_mask, left_mask, right_mask, len(rows))
        if fp != 0 or fn != 0:
            raise RuntimeError(
                "requested rescue clause does not produce exact zero-FP closure "
                f"(tp/fp/fn={tp}/{fp}/{fn})"
            )

    if best_clause is None:
        raise RuntimeError("no rescue clause found for baseline residual")

    final_tp, final_fp, final_fn, final_correct = _metrics(best_combined_mask, left_mask, right_mask, len(rows))

    base_window = _equivalent_threshold_window(rows, baseline, radius=args.window)
    rescue_window = _equivalent_threshold_window(rows, best_clause, radius=args.window)

    equivalent_pairs = 0
    total_pairs = 0
    for base_pred, rescue_pred in product(base_window, rescue_window):
        total_pairs += 1
        combined = base_pred.mask | rescue_pred.mask
        if combined == best_combined_mask:
            equivalent_pairs += 1

    base_interval = _stable_interval(rows, baseline)
    rescue_interval = _stable_interval(rows, best_clause)

    rescued_names = _mask_names(rows, best_clause.mask & miss_mask)

    print()
    print("Center-Spine Bucket 00 Add1 Rule Card")
    print("======================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)}")
    print()
    print("Physical-language closure card")
    print("------------------------------")
    print("state: nearest-opposite support-edge identity closure")
    print(f"baseline_clause: {args.baseline_label}")
    print(f"  {baseline.text}")
    print(f"rescue_clause: {args.rescue_label}")
    print(f"  {best_clause.text}")
    print(
        "closure: baseline OR rescue"
        + f" -> tp/fp/fn={final_tp}/{final_fp}/{final_fn} correct={final_correct}/{len(rows)}"
    )
    print(
        f"baseline_metrics: tp/fp/fn={baseline_tp}/{baseline_fp}/{baseline_fn} correct={baseline_correct}/{len(rows)}"
    )
    print(f"rescued_rows: {', '.join(rescued_names)}")
    print()
    print("Bounded threshold-equivalence windows")
    print("-------------------------------------")
    print(
        f"baseline_window ({len(base_window)} sampled thresholds, mask-stable): "
        + f"{baseline.op} interval={base_interval[3]} width={base_interval[2]:.3f}"
    )
    print(
        f"rescue_window ({len(rescue_window)} sampled thresholds, mask-stable): "
        + f"{best_clause.op} interval={rescue_interval[3]} width={rescue_interval[2]:.3f}"
    )
    print(
        f"cross_window_equivalence: {equivalent_pairs}/{total_pairs} pairs preserve exact closure mask"
    )
    print()
    print("Window thresholds")
    print("-----------------")
    print("baseline:", ", ".join(f"{pred.threshold:.3f}" for pred in base_window))
    print("rescue:", ", ".join(f"{pred.threshold:.3f}" for pred in rescue_window))
    print()
    print(
        "center-spine bucket00 rule-card equivalence completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
