#!/usr/bin/env python3
"""Search compact add1 residual-closure disjunctions for bucket `00` edge-identity deltas."""

from __future__ import annotations

import argparse
from datetime import datetime
from itertools import combinations
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
    parser.add_argument("--max-clause-terms", type=int, default=2)
    parser.add_argument("--row-limit", type=int, default=10)
    return parser


def candidate_predicates(rows: list[object], names: list[str]) -> list[tuple[str, int]]:
    full_mask = (1 << len(rows)) - 1
    masks: dict[int, str] = {}
    for name in names:
        values = sorted({float(getattr(row, name)) for row in rows})
        thresholds: list[float] = []
        if len(values) == 1:
            thresholds.append(values[0])
        else:
            for left, right in zip(values, values[1:]):
                thresholds.append((left + right) / 2.0)
        for threshold in thresholds:
            for op in ("<=", ">="):
                mask = 0
                for index, row in enumerate(rows):
                    value = float(getattr(row, name))
                    if (op == "<=" and value <= threshold) or (op == ">=" and value >= threshold):
                        mask |= 1 << index
                if mask in (0, full_mask):
                    continue
                text = f"{name} {op} {threshold:.3f}"
                if mask not in masks or text < masks[mask]:
                    masks[mask] = text
    out = [(text, mask) for mask, text in masks.items()]
    out.sort(key=lambda item: item[0])
    return out


def _metrics(mask: int, target_mask: int, non_target_mask: int, total: int) -> tuple[int, int, int, int]:
    tp = (mask & target_mask).bit_count()
    fp = (mask & non_target_mask).bit_count()
    fn = (target_mask & (((1 << total) - 1) ^ mask)).bit_count()
    return tp, fp, fn, tp + ((non_target_mask & (((1 << total) - 1) ^ mask)).bit_count())


def _mask_names(rows: list[object], mask: int) -> list[str]:
    names: list[str] = []
    for idx, row in enumerate(rows):
        if mask & (1 << idx):
            names.append(getattr(row, "source_name"))
    return names


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 add1 residual closure started {started}", flush=True)
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
    for text, mask in predicates_all:
        tp, fp, fn, correct = _metrics(mask, left_mask, right_mask, len(rows))
        ranked.append((fp != 0, -tp, fn, text, mask, tp, fp, correct))
    ranked.sort()
    top_predicates = [(item[3], item[4]) for item in ranked[: min(args.predicate_limit, len(ranked))]]

    baseline_text = ""
    baseline_mask = 0
    baseline_tp = -1
    for text, mask in top_predicates:
        tp, fp, fn, _correct = _metrics(mask, left_mask, right_mask, len(rows))
        if fp == 0 and tp > baseline_tp:
            baseline_text = text
            baseline_mask = mask
            baseline_tp = tp

    if baseline_tp < 0:
        raise RuntimeError("no zero-FP baseline predicate found")

    baseline_tp, baseline_fp, baseline_fn, baseline_correct = _metrics(
        baseline_mask, left_mask, right_mask, len(rows)
    )
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline_mask)

    results: list[tuple[tuple[int, int, int, str], str, int, int, int, int, int]] = []
    for term_count in range(1, args.max_clause_terms + 1):
        for clause in combinations(top_predicates, term_count):
            clause_mask = (1 << len(rows)) - 1
            clause_terms = sorted(clause, key=lambda item: item[0])
            for _text, pred_mask in clause_terms:
                clause_mask &= pred_mask
                if clause_mask == 0:
                    break
            if clause_mask == 0:
                continue
            if clause_mask & right_mask:
                continue
            if (clause_mask & miss_mask) == 0:
                continue
            combined_mask = baseline_mask | clause_mask
            tp, fp, fn, correct = _metrics(combined_mask, left_mask, right_mask, len(rows))
            if fp != 0:
                continue
            clause_text = " and ".join(term[0] for term in clause_terms)
            key = (fn, -tp, term_count, clause_text)
            results.append((key, clause_text, tp, fp, fn, correct, clause_mask))

    results.sort(key=lambda item: item[0])
    shown = results[: args.row_limit]

    print()
    print("Center-Spine Bucket 00 Add1 Residual Closure")
    print("============================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)}")
    print()
    print("Baseline add1 zero-FP rule")
    print("--------------------------")
    print(f"rule={baseline_text}")
    print(
        f"tp/fp/fn={baseline_tp}/{baseline_fp}/{baseline_fn} correct={baseline_correct}/{len(rows)}"
    )
    miss_names = _mask_names(rows, miss_mask)
    print(f"baseline_miss_count={len(miss_names)}")
    print(f"baseline_misses={', '.join(miss_names)}")
    print()
    print("Best zero-FP disjunction closures: baseline OR clause")
    print("------------------------------------------------------")
    if not shown:
        print("no qualifying clause found")
    else:
        print("tp/fp/fn | corr | clause_terms | rescued_misses | clause")
        print("--------+------+--------------+----------------+-------")
        for _key, clause_text, tp, fp, fn, correct, clause_mask in shown:
            rescued = _mask_names(rows, clause_mask & miss_mask)
            print(
                f"{tp:>2}/{fp:>2}/{fn:>2} | {correct:>2}/{len(rows):<2} | "
                + f"{clause_text.count(' and ') + 1:>12} | "
                + f"{';'.join(rescued) if rescued else '-':<14} | {clause_text}"
            )

    print()
    print(
        "center-spine bucket00 add1 residual closure completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
