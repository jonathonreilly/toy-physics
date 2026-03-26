#!/usr/bin/env python3
"""Probe combined bucket-local visible and motif observables inside the hard low-overlap bucket."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_combined_axes import build_rows as build_visible_rows  # noqa: E402
from pocket_wrap_suppressor_low_overlap_local_motif_bucket import (  # noqa: E402
    build_mixed_bucket_rows,
)


@dataclass(frozen=True)
class BucketCombinedRow:
    source_name: str
    subtype: str
    boundary_fraction: float
    core_low_degree_fraction: float
    low_degree_gap: float
    core_deep_fraction: float
    deep_gap: float
    boundary_gap: float
    core_boundary_deficit_mean: float
    pocket_gap: float
    mirror_center_asymmetry: float
    abs_half_center_diff: float
    half_center_sum: float
    half_span_diff: float
    span_curvature: float
    boundary_pocket_fraction: float
    boundary_deep_fraction: float
    boundary_low_degree_fraction: float
    boundary_mean_neighbor_degree: float
    pocket_low_overlap_fraction: float
    deep_low_overlap_fraction: float
    boundary_pocket_low_fraction: float


@dataclass(frozen=True)
class RuleRow:
    target_subtype: str
    exact: bool
    correct: int
    total: int
    term_count: int
    tp: int
    fp: int
    fn: int
    rule_text: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    parser.add_argument("--signature-terms", type=int, default=2)
    parser.add_argument("--candidate-limit", type=int, default=18)
    parser.add_argument("--max-local-terms", type=int, default=3)
    return parser


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
) -> tuple[list[BucketCombinedRow], str, str]:
    source_names, motif_rows, signature_text, bucket_text = build_mixed_bucket_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
    )
    visible_by_source = {
        row.source_name: row
        for row in build_visible_rows(log_path)
        if row.subtype in {left_subtype, right_subtype}
    }
    motif_by_source = {row.source_name: row for row in motif_rows}
    rows: list[BucketCombinedRow] = []
    for source_name in source_names:
        visible = visible_by_source[source_name]
        motif = motif_by_source[source_name]
        rows.append(
            BucketCombinedRow(
                source_name=source_name,
                subtype=visible.subtype,
                boundary_fraction=visible.boundary_fraction,
                core_low_degree_fraction=visible.core_low_degree_fraction,
                low_degree_gap=visible.low_degree_gap,
                core_deep_fraction=visible.core_deep_fraction,
                deep_gap=visible.deep_gap,
                boundary_gap=visible.boundary_gap,
                core_boundary_deficit_mean=visible.core_boundary_deficit_mean,
                pocket_gap=visible.pocket_gap,
                mirror_center_asymmetry=visible.mirror_center_asymmetry,
                abs_half_center_diff=visible.abs_half_center_diff,
                half_center_sum=visible.half_center_sum,
                half_span_diff=visible.half_span_diff,
                span_curvature=visible.span_curvature,
                boundary_pocket_fraction=motif.boundary_pocket_fraction,
                boundary_deep_fraction=motif.boundary_deep_fraction,
                boundary_low_degree_fraction=motif.boundary_low_degree_fraction,
                boundary_mean_neighbor_degree=motif.boundary_mean_neighbor_degree,
                pocket_low_overlap_fraction=motif.pocket_low_overlap_fraction,
                deep_low_overlap_fraction=motif.deep_low_overlap_fraction,
                boundary_pocket_low_fraction=motif.boundary_pocket_low_fraction,
            )
        )
    rows.sort(key=lambda row: row.source_name)
    return rows, signature_text, bucket_text


def candidate_predicates(rows: list[BucketCombinedRow]) -> list[tuple[str, int]]:
    feature_defs = (
        ("boundary_fraction", lambda row: row.boundary_fraction),
        ("core_low_degree_fraction", lambda row: row.core_low_degree_fraction),
        ("low_degree_gap", lambda row: row.low_degree_gap),
        ("core_deep_fraction", lambda row: row.core_deep_fraction),
        ("deep_gap", lambda row: row.deep_gap),
        ("boundary_gap", lambda row: row.boundary_gap),
        ("core_boundary_deficit_mean", lambda row: row.core_boundary_deficit_mean),
        ("pocket_gap", lambda row: row.pocket_gap),
        ("mirror_center_asymmetry", lambda row: row.mirror_center_asymmetry),
        ("abs_half_center_diff", lambda row: row.abs_half_center_diff),
        ("half_center_sum", lambda row: row.half_center_sum),
        ("half_span_diff", lambda row: row.half_span_diff),
        ("span_curvature", lambda row: row.span_curvature),
        ("boundary_pocket_fraction", lambda row: row.boundary_pocket_fraction),
        ("boundary_deep_fraction", lambda row: row.boundary_deep_fraction),
        ("boundary_low_degree_fraction", lambda row: row.boundary_low_degree_fraction),
        ("boundary_mean_neighbor_degree", lambda row: row.boundary_mean_neighbor_degree),
        ("pocket_low_overlap_fraction", lambda row: row.pocket_low_overlap_fraction),
        ("deep_low_overlap_fraction", lambda row: row.deep_low_overlap_fraction),
        ("boundary_pocket_low_fraction", lambda row: row.boundary_pocket_low_fraction),
    )
    preferred_order = {
        "boundary_deep_fraction": 0,
        "boundary_low_degree_fraction": 1,
        "boundary_pocket_fraction": 2,
        "boundary_mean_neighbor_degree": 3,
        "core_low_degree_fraction": 4,
        "low_degree_gap": 5,
        "core_deep_fraction": 6,
        "deep_gap": 7,
        "boundary_gap": 8,
        "core_boundary_deficit_mean": 9,
        "pocket_gap": 10,
        "boundary_fraction": 11,
        "mirror_center_asymmetry": 12,
        "abs_half_center_diff": 13,
        "half_center_sum": 14,
        "half_span_diff": 15,
        "span_curvature": 16,
        "pocket_low_overlap_fraction": 17,
        "deep_low_overlap_fraction": 18,
        "boundary_pocket_low_fraction": 19,
    }
    predicate_masks: dict[int, tuple[tuple[int, str, float], str]] = {}
    full_mask = (1 << len(rows)) - 1
    for feature_name, getter in feature_defs:
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
    predicates = [(text, mask) for mask, (_sort_key, text) in predicate_masks.items()]
    predicates.sort(key=lambda item: item[0])
    return predicates


def best_rule_for_target(
    rows: list[BucketCombinedRow],
    target_subtype: str,
    *,
    max_terms: int,
) -> RuleRow | None:
    predicates = candidate_predicates(rows)
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row.subtype == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    best: RuleRow | None = None
    seen_masks: set[int] = set()
    for term_count in range(1, max_terms + 1):
        for predicate_tuple in itertools.combinations(predicates, term_count):
            sorted_terms = tuple(sorted(predicate_tuple, key=lambda item: item[0]))
            predicted_mask = full_mask
            for _text, mask in sorted_terms:
                predicted_mask &= mask
                if predicted_mask == 0:
                    break
            if predicted_mask == 0 or predicted_mask in seen_masks:
                continue
            seen_masks.add(predicted_mask)
            tp = (predicted_mask & target_mask).bit_count()
            fp = (predicted_mask & non_target_mask).bit_count()
            fn = (target_mask & (full_mask ^ predicted_mask)).bit_count()
            tn = (non_target_mask & (full_mask ^ predicted_mask)).bit_count()
            candidate = RuleRow(
                target_subtype=target_subtype,
                exact=(fp == 0 and fn == 0),
                correct=tp + tn,
                total=len(rows),
                term_count=term_count,
                tp=tp,
                fp=fp,
                fn=fn,
                rule_text=" and ".join(term[0] for term in sorted_terms),
            )
            if best is None or (
                (not candidate.exact, -candidate.correct, candidate.term_count, candidate.fp + candidate.fn, candidate.rule_text)
                < (not best.exact, -best.correct, best.term_count, best.fp + best.fn, best.rule_text)
            ):
                best = candidate
    return best


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap local combined bucket started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
    )
    add1_rule = best_rule_for_target(rows, args.left_subtype, max_terms=args.max_local_terms)
    add4_rule = best_rule_for_target(rows, args.right_subtype, max_terms=args.max_local_terms)

    print()
    print("Low-Overlap Local Combined Bucket")
    print("=================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    if add1_rule is not None:
        print(
            f"local_combined_best[{args.left_subtype}]: exact={'Y' if add1_rule.exact else 'n'} "
            f"correct={add1_rule.correct}/{add1_rule.total} tp/fp/fn={add1_rule.tp}/{add1_rule.fp}/{add1_rule.fn} "
            f"rule={add1_rule.rule_text}"
        )
    if add4_rule is not None:
        print(
            f"local_combined_best[{args.right_subtype}]: exact={'Y' if add4_rule.exact else 'n'} "
            f"correct={add4_rule.correct}/{add4_rule.total} tp/fp/fn={add4_rule.tp}/{add4_rule.fp}/{add4_rule.fn} "
            f"rule={add4_rule.rule_text}"
        )
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap local combined bucket completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
