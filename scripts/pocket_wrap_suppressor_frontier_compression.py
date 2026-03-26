#!/usr/bin/env python3
"""Summarize non-pocket frontier growth as latent compression, not ladder chasing."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import re
import statistics
import sys
import time


ROW_RE = re.compile(
    r"^(?P<source>\S+)\s+\|\s+"
    r"(?P<subtype>both-sensitive|add1-sensitive|add4-sensitive|pair-only-sensitive)\s+\|\s+"
    r"(?P<outcomes>[^|]+)\|\s+"
    r"(?P<overlap>\d+)\s+\|\s+"
    r"(?P<cross>[Yn])\s+\|\s+"
    r"(?P<rough>\d+\.\d{3})\s+\|\s+"
    r"(?P<pocket>\d+\.\d{3})\s+\|\s+"
    r"(?P<ctv>\d+\.\d{2})\s+\|\s+"
    r"(?P<span>\d+)\s*$"
)


@dataclass(frozen=True)
class FrontierRow:
    variant_limit: int
    source_name: str
    subtype: str
    deep_overlap_count: int
    crosses_midline: bool
    boundary_roughness: float
    pocket_fraction: float
    center_total_variation: float
    span_range: int


@dataclass(frozen=True)
class TrajectoryRow:
    variant_limit: int
    row_count: int
    subtype_count: int
    signature_count: int
    new_row_count: int
    new_signature_count: int
    reused_signature_new_rows: int


@dataclass(frozen=True)
class SignatureBucketRow:
    variant_limit: int
    signature: str
    cases: int
    subtypes: str


@dataclass(frozen=True)
class EnvelopeRow:
    variant_limit: int
    subtype: str
    cases: int
    overlap_median: float
    cross_rate: float
    rough_median: float
    pocket_median: float
    ctv_median: float
    span_median: float


@dataclass(frozen=True)
class OrderParameterRow:
    model_kind: str
    exact: bool
    correct: int
    total: int
    leaf_count: int
    pure_leaf_count: int
    predicate_1: str
    predicate_2: str
    predicate_3: str
    leaf_signature: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--logs",
        nargs="+",
        default=[
            "/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.txt",
            "/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3344.txt",
            "/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt",
            "/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
        ],
    )
    parser.add_argument("--order-limit", type=int, default=5)
    parser.add_argument("--bucket-limit", type=int, default=20)
    parser.add_argument("--novelty-limit", type=int, default=20)
    return parser


def parse_variant_limit(path: Path) -> int:
    match = re.search(r"nonpocket_rows=.*", path.read_text(encoding="utf-8"))
    if match:
        text = match.group(0)
        limit_match = re.search(r"variant_limit=(\d+)", text)
        if limit_match:
            return int(limit_match.group(1))
    fallback = re.search(r"subtype-rules-(\d+)", path.name)
    if fallback:
        return int(fallback.group(1))
    raise ValueError(f"could not infer variant limit from {path}")


def parse_rows(path: Path) -> list[FrontierRow]:
    variant_limit = parse_variant_limit(path)
    rows: list[FrontierRow] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        rows.append(
            FrontierRow(
                variant_limit=variant_limit,
                source_name=match.group("source"),
                subtype=match.group("subtype"),
                deep_overlap_count=int(match.group("overlap")),
                crosses_midline=(match.group("cross") == "Y"),
                boundary_roughness=float(match.group("rough")),
                pocket_fraction=float(match.group("pocket")),
                center_total_variation=float(match.group("ctv")),
                span_range=int(match.group("span")),
            )
        )
    rows.sort(key=lambda row: row.source_name)
    if not rows:
        raise ValueError(f"no subtype rows parsed from {path}")
    return rows


def coarse_signature(row: FrontierRow) -> str:
    return "|".join(
        (
            f"cross={'Y' if row.crosses_midline else 'n'}",
            f"span={'3+' if row.span_range >= 3 else '<3'}",
            f"overlap={'2+' if row.deep_overlap_count >= 2 else '1'}",
            f"rough={'H' if row.boundary_roughness >= 0.299 else 'L'}",
            f"pocket={'H' if row.pocket_fraction >= 0.093 else 'L'}",
            f"ctv={'H' if row.center_total_variation >= 2.5 else 'L'}",
        )
    )


def candidate_predicates(rows: list[FrontierRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_getters = (
        ("deep_overlap_count", lambda row: float(row.deep_overlap_count)),
        ("boundary_roughness", lambda row: row.boundary_roughness),
        ("pocket_fraction", lambda row: row.pocket_fraction),
        ("center_total_variation", lambda row: row.center_total_variation),
        ("span_range", lambda row: float(row.span_range)),
    )
    preferred_order = {
        "deep_overlap_count": 0,
        "crosses_midline": 1,
        "boundary_roughness": 2,
        "pocket_fraction": 3,
        "center_total_variation": 4,
        "span_range": 5,
    }

    predicate_masks: dict[int, tuple[tuple[int, str, float], str]] = {}
    full_mask = (1 << len(rows)) - 1
    for feature_name, getter in feature_getters:
        value_to_labels: dict[float, set[str]] = {}
        for row in rows:
            value = float(getter(row))
            value_to_labels.setdefault(value, set()).add(row.subtype)
        values = sorted(value_to_labels)
        thresholds: list[float] = []
        if len(values) == 1:
            thresholds.append(values[0])
        else:
            for left, right in zip(values, values[1:]):
                if value_to_labels[left] != value_to_labels[right]:
                    thresholds.append((left + right) / 2.0)
        for threshold in thresholds:
            for operator in ("<=", ">="):
                mask = 0
                for index, row in enumerate(rows):
                    value = float(getter(row))
                    if (operator == "<=" and value <= threshold) or (
                        operator == ">=" and value >= threshold
                    ):
                        mask |= 1 << index
                if mask in (0, full_mask):
                    continue
                text = f"{feature_name} {operator} {threshold:.3f}"
                sort_key = (preferred_order.get(feature_name, 99), feature_name, threshold)
                chosen = predicate_masks.get(mask)
                if chosen is None or (sort_key, text) < (chosen[0], chosen[1]):
                    predicate_masks[mask] = (sort_key, text)

    for value, label in ((True, "crosses_midline = Y"), (False, "crosses_midline = n")):
        mask = 0
        for index, row in enumerate(rows):
            if row.crosses_midline == value:
                mask |= 1 << index
        if mask in (0, full_mask):
            continue
        sort_key = (preferred_order["crosses_midline"], "crosses_midline", 1.0 if value else 0.0)
        chosen = predicate_masks.get(mask)
        if chosen is None or (sort_key, label) < (chosen[0], chosen[1]):
            predicate_masks[mask] = (sort_key, label)

    predicates = [(text, mask) for mask, (_sort_key, text) in predicate_masks.items()]
    predicates.sort(key=lambda item: item[0])
    return predicates


def leaf_summary(rows: list[FrontierRow], leaves: list[tuple[str, int]]) -> tuple[int, int, str]:
    correct = 0
    pure_leaf_count = 0
    parts: list[str] = []
    for leaf_name, mask in leaves:
        if mask == 0:
            continue
        leaf_rows = [row for index, row in enumerate(rows) if mask & (1 << index)]
        subtype_counts: dict[str, int] = {}
        for row in leaf_rows:
            subtype_counts[row.subtype] = subtype_counts.get(row.subtype, 0) + 1
        majority_subtype, majority_count = max(
            subtype_counts.items(),
            key=lambda item: (item[1], item[0]),
        )
        correct += majority_count
        if len(subtype_counts) == 1:
            pure_leaf_count += 1
        parts.append(f"{leaf_name}:{majority_subtype}({len(leaf_rows)})")
    return correct, pure_leaf_count, "; ".join(parts)


def best_pair_rules(rows: list[FrontierRow], limit: int = 5) -> list[OrderParameterRow]:
    if not rows:
        return []
    full_mask = (1 << len(rows)) - 1
    predicates = candidate_predicates(rows)
    results: list[OrderParameterRow] = []
    for left_index in range(len(predicates)):
        left_text, left_mask = predicates[left_index]
        for right_index in range(left_index + 1, len(predicates)):
            right_text, right_mask = predicates[right_index]
            leaves = [
                ("00", (full_mask ^ left_mask) & (full_mask ^ right_mask)),
                ("01", (full_mask ^ left_mask) & right_mask),
                ("10", left_mask & (full_mask ^ right_mask)),
                ("11", left_mask & right_mask),
            ]
            correct, pure_leaf_count, leaf_signature = leaf_summary(rows, leaves)
            leaf_count = sum(mask != 0 for _name, mask in leaves)
            results.append(
                OrderParameterRow(
                    model_kind="pair",
                    exact=(correct == len(rows) and pure_leaf_count == leaf_count),
                    correct=correct,
                    total=len(rows),
                    leaf_count=leaf_count,
                    pure_leaf_count=pure_leaf_count,
                    predicate_1=left_text,
                    predicate_2=right_text,
                    predicate_3="-",
                    leaf_signature=leaf_signature,
                )
            )
    results.sort(
        key=lambda row: (
            not row.exact,
            -(row.correct / row.total if row.total else 0.0),
            -row.pure_leaf_count,
            row.leaf_count,
            row.predicate_1,
            row.predicate_2,
        )
    )
    return results[:limit]


def best_small_trees(rows: list[FrontierRow], limit: int = 5) -> list[OrderParameterRow]:
    if not rows:
        return []
    full_mask = (1 << len(rows)) - 1
    predicates = candidate_predicates(rows)
    results: list[OrderParameterRow] = []
    for root_text, root_mask in predicates:
        left_branch_mask = full_mask ^ root_mask
        right_branch_mask = root_mask
        for left_text, left_mask in predicates:
            for right_text, right_mask in predicates:
                leaves = [
                    ("L0", left_branch_mask & (full_mask ^ left_mask)),
                    ("L1", left_branch_mask & left_mask),
                    ("R0", right_branch_mask & (full_mask ^ right_mask)),
                    ("R1", right_branch_mask & right_mask),
                ]
                correct, pure_leaf_count, leaf_signature = leaf_summary(rows, leaves)
                leaf_count = sum(mask != 0 for _name, mask in leaves)
                results.append(
                    OrderParameterRow(
                        model_kind="tree",
                        exact=(correct == len(rows) and pure_leaf_count == leaf_count),
                        correct=correct,
                        total=len(rows),
                        leaf_count=leaf_count,
                        pure_leaf_count=pure_leaf_count,
                        predicate_1=root_text,
                        predicate_2=left_text,
                        predicate_3=right_text,
                        leaf_signature=leaf_signature,
                    )
                )
    results.sort(
        key=lambda row: (
            not row.exact,
            -(row.correct / row.total if row.total else 0.0),
            -row.pure_leaf_count,
            row.leaf_count,
            row.predicate_1,
            row.predicate_2,
            row.predicate_3,
        )
    )
    return results[:limit]


def build_trajectory(rows_by_limit: dict[int, list[FrontierRow]]) -> tuple[list[TrajectoryRow], list[SignatureBucketRow]]:
    trajectory_rows: list[TrajectoryRow] = []
    bucket_rows: list[SignatureBucketRow] = []
    seen_sources: set[str] = set()
    seen_signatures: set[str] = set()
    for variant_limit in sorted(rows_by_limit):
        rows = rows_by_limit[variant_limit]
        signature_by_source = {row.source_name: coarse_signature(row) for row in rows}
        current_signatures = set(signature_by_source.values())
        new_rows = [row for row in rows if row.source_name not in seen_sources]
        trajectory_rows.append(
            TrajectoryRow(
                variant_limit=variant_limit,
                row_count=len(rows),
                subtype_count=len({row.subtype for row in rows}),
                signature_count=len(current_signatures),
                new_row_count=len(new_rows),
                new_signature_count=len(current_signatures - seen_signatures),
                reused_signature_new_rows=sum(
                    signature_by_source[row.source_name] in seen_signatures for row in new_rows
                ),
            )
        )
        grouped: dict[str, list[FrontierRow]] = {}
        for row in rows:
            grouped.setdefault(signature_by_source[row.source_name], []).append(row)
        for signature, signature_rows in sorted(grouped.items()):
            bucket_rows.append(
                SignatureBucketRow(
                    variant_limit=variant_limit,
                    signature=signature,
                    cases=len(signature_rows),
                    subtypes=",".join(sorted({row.subtype for row in signature_rows})),
                )
            )
        seen_sources.update(row.source_name for row in rows)
        seen_signatures.update(current_signatures)
    return trajectory_rows, bucket_rows


def build_envelopes(rows: list[FrontierRow], variant_limit: int) -> list[EnvelopeRow]:
    envelopes: list[EnvelopeRow] = []
    for subtype in sorted({row.subtype for row in rows}):
        subtype_rows = [row for row in rows if row.subtype == subtype]
        envelopes.append(
            EnvelopeRow(
                variant_limit=variant_limit,
                subtype=subtype,
                cases=len(subtype_rows),
                overlap_median=statistics.median(float(row.deep_overlap_count) for row in subtype_rows),
                cross_rate=sum(row.crosses_midline for row in subtype_rows) / len(subtype_rows),
                rough_median=statistics.median(row.boundary_roughness for row in subtype_rows),
                pocket_median=statistics.median(row.pocket_fraction for row in subtype_rows),
                ctv_median=statistics.median(row.center_total_variation for row in subtype_rows),
                span_median=statistics.median(float(row.span_range) for row in subtype_rows),
            )
        )
    return envelopes


def render_trajectory(rows: list[TrajectoryRow]) -> str:
    lines = [
        "limit | rows | subtypes | signatures | new rows | new signatures | reused-signature new rows",
        "------+------|----------|------------|----------|----------------|--------------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.variant_limit:>5} | {row.row_count:>4} | {row.subtype_count:>8} | "
            f"{row.signature_count:>10} | {row.new_row_count:>8} | {row.new_signature_count:>14} | "
            f"{row.reused_signature_new_rows:>24}"
        )
    return "\n".join(lines)


def render_signature_buckets(rows: list[SignatureBucketRow], variant_limit: int, limit: int) -> str:
    lines = [
        "signature | cases | subtypes",
        "----------+-------+--------------------------------",
    ]
    bucket_rows = [row for row in rows if row.variant_limit == variant_limit]
    bucket_rows.sort(key=lambda row: (-row.cases, row.signature))
    for row in bucket_rows[:limit]:
        lines.append(f"{row.signature} | {row.cases:>5} | {row.subtypes}")
    return "\n".join(lines)


def render_envelopes(rows: list[EnvelopeRow]) -> str:
    lines = [
        "subtype | cases | overlap~ | cross rate | rough~ | pocket~ | ctv~ | span~",
        "--------+-------+----------+------------+--------+---------+------+------",
    ]
    for row in rows:
        lines.append(
            f"{row.subtype} | {row.cases:>5} | {row.overlap_median:>8.2f} | {row.cross_rate:>10.2f} | "
            f"{row.rough_median:>6.3f} | {row.pocket_median:>7.3f} | {row.ctv_median:>4.2f} | {row.span_median:>4.1f}"
        )
    return "\n".join(lines)


def render_order_parameters(rows: list[OrderParameterRow], limit: int) -> str:
    lines = [
        "model | exact | correct | leaves | pure | predicate 1 | predicate 2 | predicate 3 | leaf signature",
        "------+-------+---------+--------+------+-------------+-------------+-------------+--------------------------------------",
    ]
    for row in rows[:limit]:
        lines.append(
            f"{row.model_kind:<5} | {('Y' if row.exact else 'n'):<5} | {row.correct:>3}/{row.total:<3} | "
            f"{row.leaf_count:>6} | {row.pure_leaf_count:>4} | "
            f"{row.predicate_1:<11.11} | {row.predicate_2:<11.11} | {row.predicate_3:<11.11} | "
            f"{row.leaf_signature}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"frontier compression started {started}", flush=True)
    total_start = time.time()

    paths = [Path(text).resolve() for text in args.logs]
    rows_by_limit = {parse_variant_limit(path): parse_rows(path) for path in paths}
    trajectory_rows, bucket_rows = build_trajectory(rows_by_limit)
    latest_limit = max(rows_by_limit)
    latest_rows = rows_by_limit[latest_limit]
    envelope_rows = build_envelopes(latest_rows, latest_limit)
    pair_rows = best_pair_rules(latest_rows, limit=args.order_limit)
    tree_rows = best_small_trees(latest_rows, limit=args.order_limit)

    print()
    print("Frontier Compression Trajectory")
    print("==============================")
    print(render_trajectory(trajectory_rows))
    print()
    print(f"Largest Coarse Buckets ({latest_limit})")
    print("======================" + "=" * len(str(latest_limit)))
    print(render_signature_buckets(bucket_rows, latest_limit, limit=args.bucket_limit))
    print()
    print(f"Latest Subtype Envelopes ({latest_limit})")
    print("=========================" + "=" * len(str(latest_limit)))
    print(render_envelopes(envelope_rows))
    print()
    print(f"Best Two-Axis Order Parameters ({latest_limit})")
    print("=================================" + "=" * len(str(latest_limit)))
    print(render_order_parameters(pair_rows, limit=args.order_limit))
    print()
    print(f"Best Small Trees ({latest_limit})")
    print("=====================" + "=" * len(str(latest_limit)))
    print(render_order_parameters(tree_rows, limit=args.order_limit))
    print()
    print(
        "frontier compression completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
