#!/usr/bin/env python3
"""Compare bounded robustness of top 1-term corridor clauses versus the interpretable 2-term role clause."""

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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_subfamily_decomposition import (  # noqa: E402
    build_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_pocket_corridor_equivalence_scan import (  # noqa: E402
    _interval_from_values,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_rule_card_rescue_window_scan import (  # noqa: E402
    _metrics,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)


@dataclass(frozen=True)
class ClauseSpec:
    label: str
    weights: dict[str, int]
    op: str
    threshold: float


CLAUSES = [
    ClauseSpec(
        label="1-term bridge-present1",
        weights={"delta_count_pocket_joined_bridge__pocket_only__present1": 1},
        op="<=",
        threshold=-2.5,
    ),
    ClauseSpec(
        label="1-term pocket-only-present0",
        weights={"delta_count_pocket_joined_pocket_only__pocket_only__present0": 1},
        op="<=",
        threshold=-6.5,
    ),
    ClauseSpec(
        label="1-term pocket-only role",
        weights={"delta_count_pocket_role_pocket_only__pocket_only": 1},
        op="<=",
        threshold=-11.5,
    ),
    ClauseSpec(
        label="2-term role clause",
        weights={
            "delta_count_pocket_role_bridge__pocket_only": 1,
            "delta_count_pocket_role_pocket_only__pocket_only": 1,
        },
        op="<=",
        threshold=-14.5,
    ),
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


def _clause_values(rows: list[object], weights: dict[str, int]) -> list[float]:
    values: list[float] = []
    for row in rows:
        total = 0.0
        for name, weight in weights.items():
            total += float(getattr(row, name)) * weight
        values.append(total)
    return values


def _mask_for(values: list[float], op: str, threshold: float) -> int:
    mask = 0
    for idx, value in enumerate(values):
        if (op == "<=" and value <= threshold) or (op == ">=" and value >= threshold):
            mask |= 1 << idx
    return mask


def _critical_thresholds(values: list[float]) -> list[float]:
    unique = sorted(set(values))
    if len(unique) == 1:
        return [unique[0]]
    return [(left + right) / 2.0 for left, right in zip(unique, unique[1:])]


def _mask_names(rows: list[object], mask: int) -> list[str]:
    return [getattr(row, "source_name") for idx, row in enumerate(rows) if mask & (1 << idx)]


def _family_mask(rows: list[object]) -> tuple[int, int, int]:
    left_mask = 0
    right_mask = 0
    baseline_mask = 0
    family_mask = 0
    for idx, row in enumerate(rows):
        if getattr(row, "subtype") == "add1-sensitive":
            left_mask |= 1 << idx
        elif getattr(row, "subtype") == "add4-sensitive":
            right_mask |= 1 << idx
        if float(getattr(row, "delta_edge_identity_support_edge_density")) <= 0.018:
            baseline_mask |= 1 << idx
        if float(getattr(row, "delta_count_pocket_total")) <= -14.5:
            family_mask |= 1 << idx
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline_mask)
    return left_mask, right_mask, family_mask & miss_mask


def _clause_exact_family_match(rows: list[object], spec: ClauseSpec) -> tuple[bool, int, tuple[int, int, int]]:
    left_mask, right_mask, family_rescue = _family_mask(rows)
    values = _clause_values(rows, spec.weights)
    clause_mask = _mask_for(values, spec.op, spec.threshold)
    rescue_mask = clause_mask & (left_mask & (((1 << len(rows)) - 1) ^ 0))
    combined = (
        sum((1 << idx) for idx, row in enumerate(rows) if float(getattr(row, "delta_edge_identity_support_edge_density")) <= 0.018)
        | clause_mask
    )
    tp, fp, fn = _metrics(combined, left_mask, right_mask, len(rows))
    exact = fp == 0 and fn == 0 and (clause_mask & (left_mask & (((1 << len(rows)) - 1) ^ combined ^ clause_mask))) == 0
    return exact and rescue_mask == family_rescue, family_rescue, (tp, fp, fn)


def _family_rescue_mask(rows: list[object]) -> tuple[int, int, int, int]:
    left_mask = 0
    right_mask = 0
    baseline_mask = 0
    family_mask = 0
    for idx, row in enumerate(rows):
        subtype = getattr(row, "subtype")
        if subtype == "add1-sensitive":
            left_mask |= 1 << idx
        elif subtype == "add4-sensitive":
            right_mask |= 1 << idx
        if float(getattr(row, "delta_edge_identity_support_edge_density")) <= 0.018:
            baseline_mask |= 1 << idx
        if float(getattr(row, "delta_count_pocket_total")) <= -14.5:
            family_mask |= 1 << idx
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline_mask)
    return left_mask, right_mask, baseline_mask, family_mask & miss_mask


def _drop_row(rows: list[object], drop_idx: int) -> list[object]:
    return [row for idx, row in enumerate(rows) if idx != drop_idx]


def _same_threshold_match(rows: list[object], spec: ClauseSpec) -> tuple[bool, int]:
    left_mask, right_mask, baseline_mask, family_rescue = _family_rescue_mask(rows)
    values = _clause_values(rows, spec.weights)
    clause_mask = _mask_for(values, spec.op, spec.threshold)
    combined = baseline_mask | clause_mask
    tp, fp, fn = _metrics(combined, left_mask, right_mask, len(rows))
    rescue_mask = clause_mask & (left_mask & (((1 << len(rows)) - 1) ^ baseline_mask))
    return fp == 0 and fn == 0 and rescue_mask == family_rescue, family_rescue


def _retuned_match(rows: list[object], spec: ClauseSpec) -> tuple[bool, float]:
    left_mask, right_mask, baseline_mask, family_rescue = _family_rescue_mask(rows)
    values = _clause_values(rows, spec.weights)
    best_width = -1.0
    found = False
    for threshold in _critical_thresholds(values):
        clause_mask = _mask_for(values, spec.op, threshold)
        combined = baseline_mask | clause_mask
        tp, fp, fn = _metrics(combined, left_mask, right_mask, len(rows))
        rescue_mask = clause_mask & (left_mask & (((1 << len(rows)) - 1) ^ baseline_mask))
        if fp == 0 and fn == 0 and rescue_mask == family_rescue:
            found = True
            width = _interval_from_values(values, spec.op, threshold)[2]
            if width > best_width:
                best_width = width
    return found, best_width if found else 0.0


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 corridor clause robustness started {started}", flush=True)
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
    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    print()
    print("Center-Spine Bucket 00 Corridor Clause Robustness")
    print("=================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)}")
    print()

    for spec in CLAUSES:
        values = _clause_values(rows, spec.weights)
        full_interval = _interval_from_values(values, spec.op, spec.threshold)
        same_survive = 0
        retuned_survive = 0
        best_retuned_widths: list[float] = []
        failures: list[str] = []
        for idx, row in enumerate(rows):
            reduced = _drop_row(rows, idx)
            same_ok, _family_mask = _same_threshold_match(reduced, spec)
            if same_ok:
                same_survive += 1
            else:
                failures.append(getattr(row, "source_name"))
            retuned_ok, best_width = _retuned_match(reduced, spec)
            if retuned_ok:
                retuned_survive += 1
                best_retuned_widths.append(best_width)
        mean_retuned = sum(best_retuned_widths) / len(best_retuned_widths) if best_retuned_widths else 0.0
        print(spec.label)
        print(f"  clause={spec.op} {spec.threshold:.3f} on {spec.weights}")
        print(f"  full_interval={full_interval[3]} width={full_interval[2]:.3f}")
        print(f"  same_threshold_rowdrop_survival={same_survive}/{len(rows)}")
        print(f"  retuned_rowdrop_survival={retuned_survive}/{len(rows)}")
        print(f"  mean_best_retuned_width={mean_retuned:.3f}")
        if failures:
            print(f"  same-threshold failures: {', '.join(failures[:8])}")
        print()

    print(
        "center-spine bucket00 corridor clause robustness completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
