#!/usr/bin/env python3
"""Derive the corrected mechanism split map from completed benchmark logs."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    MechanismSplitAggregateRow,
    MechanismSplitRow,
    render_mechanism_split_aggregate_table,
    render_mechanism_split_table,
)


AUDIT_LOG_PATH = REPO_ROOT / "logs" / "post_fix_predictor_audit.log"
BROADER_LOG_PATH = REPO_ROOT / "logs" / "long_broader_hub_mechanism_comparison.log"

SECTION_MAP = {
    "High-Degree Decomposition Benchmark": "high-degree-decomp",
    "High-Degree Threshold Benchmark": "high-degree-threshold",
    "Soft Hub Exposure Benchmark": "soft-hub",
    "Neighbor Reach Threshold Benchmark": "neighbor-reach",
    "Neighbor Leverage Threshold Benchmark": "neighbor-leverage",
    "Threshold Exposure Decomposition Benchmark": "threshold-exposure",
}

BROADER_ROW_RE = re.compile(
    r"^(?P<name>[^:]+:[^:]+): "
    r"compact_parity=(?P<compact_parity>[^|]+) \| "
    r"compact_pre=(?P<compact_pre>[+-]?\d+\.\d+)/(?P<compact_pre_worst>[+-]?\d+\.\d+) \| "
    r"extended_parity=(?P<extended_parity>[^|]+) \| "
    r"extended_pre=(?P<extended_pre>[+-]?\d+\.\d+)/(?P<extended_pre_worst>[+-]?\d+\.\d+)"
)


def parse_parity_cell(cell: str) -> tuple[int | None, str]:
    cell = cell.strip()
    if cell in {"-", "None:-"}:
        return None, "-"
    size_text, feature_subset = cell.split(":", 1)
    return int(size_text), feature_subset


def split_class_from_sizes(
    compact_parity_size: int | None,
    extended_parity_size: int | None,
    fast_parity_size: int = 3,
) -> tuple[bool, bool, str]:
    compact_fast = compact_parity_size is not None and compact_parity_size <= fast_parity_size
    extended_fast = extended_parity_size is not None and extended_parity_size <= fast_parity_size
    if compact_fast and extended_fast:
        return compact_fast, extended_fast, "shared-fast"
    if compact_fast:
        return compact_fast, extended_fast, "compact-fast"
    if extended_fast:
        return compact_fast, extended_fast, "extended-fast"
    return compact_fast, extended_fast, "neither"


def parse_audit_section_rows(text: str, heading: str, benchmark_name: str) -> list[MechanismSplitRow]:
    heading_index = text.find(heading)
    if heading_index == -1:
        raise RuntimeError(f"missing section {heading!r} in {AUDIT_LOG_PATH}")
    next_heading_index = len(text)
    for other_heading in SECTION_MAP:
        if other_heading == heading:
            continue
        index = text.find(other_heading, heading_index + 1)
        if index != -1:
            next_heading_index = min(next_heading_index, index)
    section_text = text[heading_index:next_heading_index]
    rows: list[MechanismSplitRow] = []
    for line in section_text.splitlines():
        if "|" not in line or line.startswith("decomposition") or line.startswith("---"):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) != 8:
            continue
        mechanism_name = cells[0]
        compact_parity_size, compact_subset = parse_parity_cell(cells[4])
        extended_parity_size, extended_subset = parse_parity_cell(cells[6])
        compact_fast, extended_fast, split_class = split_class_from_sizes(
            compact_parity_size,
            extended_parity_size,
        )
        compact_pre_gap, compact_pre_worst = (
            float(part) for part in cells[5].split("/", 1)
        )
        extended_pre_gap, extended_pre_worst = (
            float(part) for part in cells[7].split("/", 1)
        )
        rows.append(
            MechanismSplitRow(
                benchmark_name=benchmark_name,
                mechanism_name=mechanism_name,
                compact_parity_size=compact_parity_size,
                compact_parity_feature_subset=compact_subset,
                extended_parity_size=extended_parity_size,
                extended_parity_feature_subset=extended_subset,
                compact_fast=compact_fast,
                extended_fast=extended_fast,
                same_feature_signature=(compact_subset == extended_subset and compact_subset != "-"),
                split_class=split_class,
                compact_best_prethreshold_gap=compact_pre_gap,
                compact_best_prethreshold_worst_gap=compact_pre_worst,
                extended_best_prethreshold_gap=extended_pre_gap,
                extended_best_prethreshold_worst_gap=extended_pre_worst,
            )
        )
    if not rows:
        raise RuntimeError(f"parsed no rows for section {heading!r}")
    return rows


def parse_broader_rows(text: str) -> list[MechanismSplitRow]:
    rows: list[MechanismSplitRow] = []
    for line in text.splitlines():
        match = BROADER_ROW_RE.match(line.strip())
        if not match:
            continue
        compact_parity_size, compact_subset = parse_parity_cell(match.group("compact_parity"))
        extended_parity_size, extended_subset = parse_parity_cell(match.group("extended_parity"))
        compact_fast, extended_fast, split_class = split_class_from_sizes(
            compact_parity_size,
            extended_parity_size,
        )
        rows.append(
            MechanismSplitRow(
                benchmark_name="broader-hub",
                mechanism_name=match.group("name"),
                compact_parity_size=compact_parity_size,
                compact_parity_feature_subset=compact_subset,
                extended_parity_size=extended_parity_size,
                extended_parity_feature_subset=extended_subset,
                compact_fast=compact_fast,
                extended_fast=extended_fast,
                same_feature_signature=(compact_subset == extended_subset and compact_subset != "-"),
                split_class=split_class,
                compact_best_prethreshold_gap=float(match.group("compact_pre")),
                compact_best_prethreshold_worst_gap=float(match.group("compact_pre_worst")),
                extended_best_prethreshold_gap=float(match.group("extended_pre")),
                extended_best_prethreshold_worst_gap=float(match.group("extended_pre_worst")),
            )
        )
    if not rows:
        raise RuntimeError(f"parsed no broader rows from {BROADER_LOG_PATH}")
    return rows


def aggregate_rows(split_rows: list[MechanismSplitRow]) -> list[MechanismSplitAggregateRow]:
    counts = defaultdict(int)
    for row in split_rows:
        counts[(row.benchmark_name, row.split_class)] += 1
    return [
        MechanismSplitAggregateRow(
            benchmark_name=benchmark_name,
            split_class=split_class,
            cases=cases,
        )
        for (benchmark_name, split_class), cases in sorted(counts.items())
    ]


def main() -> None:
    print(
        "mechanism family split analysis started "
        + datetime.now().isoformat(timespec="seconds")
    )
    audit_text = AUDIT_LOG_PATH.read_text()
    broader_text = BROADER_LOG_PATH.read_text()

    rows: list[MechanismSplitRow] = []
    for heading, benchmark_name in SECTION_MAP.items():
        rows.extend(parse_audit_section_rows(audit_text, heading, benchmark_name))
    rows.extend(parse_broader_rows(broader_text))
    rows.sort(key=lambda row: (row.benchmark_name, row.split_class, row.mechanism_name))
    aggregate = aggregate_rows(rows)

    print()
    print("Mechanism Split Aggregate")
    print("=========================")
    print(render_mechanism_split_aggregate_table(aggregate))
    print()
    print("Mechanism Split Detail")
    print("======================")
    print(render_mechanism_split_table(rows, limit_per_benchmark=32))
    print()
    print(
        "mechanism family split analysis completed "
        + datetime.now().isoformat(timespec="seconds")
    )


if __name__ == "__main__":
    main()
