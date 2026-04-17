#!/usr/bin/env python3
"""Probe compact two-clause closures on the hard low-overlap mixed bucket."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, fields
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

from pocket_wrap_suppressor_low_overlap_local_combined_bucket import (  # noqa: E402
    BucketCombinedRow,
    build_rows as build_combined_rows,
)
from pocket_wrap_suppressor_low_overlap_local_support_topology_bucket import (  # noqa: E402
    SupportTopologyRow,
    build_rows as build_support_rows,
)


@dataclass(frozen=True)
class JoinedBucketRow:
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
    pocket_cell_fraction: float
    deep_pocket_cell_fraction: float
    pocket_neighbor_overlap_fraction: float
    deep_neighbor_overlap_fraction: float
    pocket_neighbor_support_mean: float
    deep_neighbor_support_mean: float
    pocket_boundary_neighbor_fraction: float
    deep_boundary_neighbor_fraction: float
    pocket_mirror_candidate_fraction: float
    pocket_mirror_occupied_fraction: float
    pocket_mirror_void_fraction: float
    pocket_mirror_imbalance: float
    deep_mirror_candidate_fraction: float
    deep_mirror_occupied_fraction: float
    deep_mirror_void_fraction: float
    deep_mirror_imbalance: float


@dataclass(frozen=True)
class ClauseRow:
    clause_text: str
    term_count: int
    tp: int
    fp: int
    fn: int
    correct: int


@dataclass(frozen=True)
class TwoClauseRow:
    target_subtype: str
    exact: bool
    correct: int
    total: int
    clause_count: int
    term_count: int
    tp: int
    fp: int
    fn: int
    clause_text: str


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
    parser.add_argument("--max-clause-terms", type=int, default=3)
    parser.add_argument("--clause-limit", type=int, default=8)
    parser.add_argument("--predicate-limit", type=int, default=24)
    return parser


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
) -> tuple[list[JoinedBucketRow], str, str]:
    combined_rows, signature_text, bucket_text = build_combined_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
    )
    support_rows, _support_signature, _support_bucket = build_support_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
    )
    support_by_source = {row.source_name: row for row in support_rows}

    rows: list[JoinedBucketRow] = []
    for combined in combined_rows:
        support = support_by_source[combined.source_name]
        rows.append(
            JoinedBucketRow(
                source_name=combined.source_name,
                subtype=combined.subtype,
                boundary_fraction=combined.boundary_fraction,
                core_low_degree_fraction=combined.core_low_degree_fraction,
                low_degree_gap=combined.low_degree_gap,
                core_deep_fraction=combined.core_deep_fraction,
                deep_gap=combined.deep_gap,
                boundary_gap=combined.boundary_gap,
                core_boundary_deficit_mean=combined.core_boundary_deficit_mean,
                pocket_gap=combined.pocket_gap,
                mirror_center_asymmetry=combined.mirror_center_asymmetry,
                abs_half_center_diff=combined.abs_half_center_diff,
                half_center_sum=combined.half_center_sum,
                half_span_diff=combined.half_span_diff,
                span_curvature=combined.span_curvature,
                boundary_pocket_fraction=combined.boundary_pocket_fraction,
                boundary_deep_fraction=combined.boundary_deep_fraction,
                boundary_low_degree_fraction=combined.boundary_low_degree_fraction,
                boundary_mean_neighbor_degree=combined.boundary_mean_neighbor_degree,
                pocket_low_overlap_fraction=combined.pocket_low_overlap_fraction,
                deep_low_overlap_fraction=combined.deep_low_overlap_fraction,
                boundary_pocket_low_fraction=combined.boundary_pocket_low_fraction,
                pocket_cell_fraction=support.pocket_cell_fraction,
                deep_pocket_cell_fraction=support.deep_pocket_cell_fraction,
                pocket_neighbor_overlap_fraction=support.pocket_neighbor_overlap_fraction,
                deep_neighbor_overlap_fraction=support.deep_neighbor_overlap_fraction,
                pocket_neighbor_support_mean=support.pocket_neighbor_support_mean,
                deep_neighbor_support_mean=support.deep_neighbor_support_mean,
                pocket_boundary_neighbor_fraction=support.pocket_boundary_neighbor_fraction,
                deep_boundary_neighbor_fraction=support.deep_boundary_neighbor_fraction,
                pocket_mirror_candidate_fraction=support.pocket_mirror_candidate_fraction,
                pocket_mirror_occupied_fraction=support.pocket_mirror_occupied_fraction,
                pocket_mirror_void_fraction=support.pocket_mirror_void_fraction,
                pocket_mirror_imbalance=support.pocket_mirror_imbalance,
                deep_mirror_candidate_fraction=support.deep_mirror_candidate_fraction,
                deep_mirror_occupied_fraction=support.deep_mirror_occupied_fraction,
                deep_mirror_void_fraction=support.deep_mirror_void_fraction,
                deep_mirror_imbalance=support.deep_mirror_imbalance,
            )
        )
    rows.sort(key=lambda row: row.source_name)
    return rows, signature_text, bucket_text


def candidate_predicates(rows: list[JoinedBucketRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_names = [
        field.name
        for field in fields(JoinedBucketRow)
        if field.name not in {"source_name", "subtype"}
    ]
    preferred_order = {name: index for index, name in enumerate(feature_names)}
    predicate_masks: dict[int, tuple[tuple[int, str, float], str]] = {}
    full_mask = (1 << len(rows)) - 1

    for feature_name in feature_names:
        value_to_labels: dict[float, set[str]] = {}
        for row in rows:
            value = float(getattr(row, feature_name))
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
                    value = float(getattr(row, feature_name))
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


def clause_candidates(
    predicates: list[tuple[str, int]],
    *,
    row_count: int,
    max_terms: int,
) -> list[tuple[str, int, int]]:
    full_mask = (1 << row_count) - 1
    seen_masks: set[int] = set()
    clauses: list[tuple[str, int, int]] = []
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
            clauses.append(
                (" and ".join(term[0] for term in sorted_terms), predicted_mask, term_count)
            )
    clauses.sort(key=lambda item: (item[2], item[0]))
    return clauses


def best_two_clause_rows(
    rows: list[JoinedBucketRow],
    *,
    max_clause_terms: int,
    clause_limit: int,
    predicate_limit: int,
) -> list[TwoClauseRow]:
    if not rows:
        return []

    full_mask = (1 << len(rows)) - 1
    predicates = candidate_predicates(rows)
    target_subtypes = tuple(sorted({row.subtype for row in rows}))
    results: list[TwoClauseRow] = []

    def score(mask: int, target_mask: int, non_target_mask: int) -> tuple[int, int, int, int]:
        tp = (mask & target_mask).bit_count()
        fp = (mask & non_target_mask).bit_count()
        fn = (target_mask & (full_mask ^ mask)).bit_count()
        tn = (non_target_mask & (full_mask ^ mask)).bit_count()
        return tp, fp, fn, tp + tn

    def sort_key(row: TwoClauseRow) -> tuple[bool, int, int, int, str]:
        return (
            not row.exact,
            -row.correct,
            row.clause_count,
            row.term_count,
            row.clause_text,
        )

    for target_subtype in target_subtypes:
        target_mask = 0
        for index, row in enumerate(rows):
            if row.subtype == target_subtype:
                target_mask |= 1 << index
        non_target_mask = full_mask ^ target_mask

        scored_predicates: list[tuple[tuple[bool, int, int, str], tuple[str, int]]] = []
        for predicate_text, predicate_mask in predicates:
            tp, fp, fn, correct = score(predicate_mask, target_mask, non_target_mask)
            scored_predicates.append(
                (
                    (fp != 0, -correct, -tp, predicate_text),
                    (predicate_text, predicate_mask),
                )
            )
        scored_predicates.sort(key=lambda item: item[0])
        selected_predicates = [item[1] for item in scored_predicates[:predicate_limit]]
        clauses = clause_candidates(
            selected_predicates,
            row_count=len(rows),
            max_terms=max_clause_terms,
        )

        scored_rows: list[TwoClauseRow] = []
        zero_fp_clauses: list[tuple[str, int, int]] = []
        for clause_text, clause_mask, term_count in clauses:
            tp, fp, fn, correct = score(clause_mask, target_mask, non_target_mask)
            clause_row = TwoClauseRow(
                target_subtype=target_subtype,
                exact=(fp == 0 and fn == 0),
                correct=correct,
                total=len(rows),
                clause_count=1,
                term_count=term_count,
                tp=tp,
                fp=fp,
                fn=fn,
                clause_text=clause_text,
            )
            scored_rows.append(clause_row)
            if fp == 0:
                zero_fp_clauses.append((clause_text, clause_mask, term_count))

        # Exact or near-exact two-clause unions only need zero-FP clauses.
        zero_fp_clauses.sort(
            key=lambda item: (
                -((item[1] & target_mask).bit_count()),
                item[2],
                item[0],
            )
        )
        exact_unions_seen: set[str] = set()
        for first_text, first_mask, first_terms in zero_fp_clauses:
            remaining_target_mask = target_mask & (full_mask ^ first_mask)
            if remaining_target_mask == 0:
                continue
            for second_text, second_mask, second_terms in zero_fp_clauses:
                if (remaining_target_mask & second_mask) != remaining_target_mask:
                    continue
                clause_text = (
                    first_text
                    if first_text == second_text
                    else f"({first_text}) OR ({second_text})"
                )
                if clause_text in exact_unions_seen:
                    continue
                exact_unions_seen.add(clause_text)
                union_mask = first_mask | second_mask
                tp, fp, fn, correct = score(union_mask, target_mask, non_target_mask)
                scored_rows.append(
                    TwoClauseRow(
                        target_subtype=target_subtype,
                        exact=(fp == 0 and fn == 0),
                        correct=correct,
                        total=len(rows),
                        clause_count=1 if first_text == second_text else 2,
                        term_count=first_terms + (0 if first_text == second_text else second_terms),
                        tp=tp,
                        fp=fp,
                        fn=fn,
                        clause_text=clause_text,
                    )
                )
                if fp == 0 and fn == 0:
                    break
            if any(row.exact for row in scored_rows if row.target_subtype == target_subtype):
                break

        scored_rows.sort(key=sort_key)
        unique: list[TwoClauseRow] = []
        seen_texts: set[str] = set()
        for row in scored_rows:
            if row.clause_text in seen_texts:
                continue
            seen_texts.add(row.clause_text)
            unique.append(row)
            if len(unique) >= clause_limit:
                break
        results.extend(unique)

    results.sort(
        key=lambda row: (
            row.target_subtype,
            not row.exact,
            -row.correct,
            row.clause_count,
            row.term_count,
            row.clause_text,
        )
    )
    return results


def render_rule_rows(rule_rows: list[TwoClauseRow]) -> str:
    lines = [
        "Two-Clause Bucket Closures",
        "==========================",
        "target | exact | corr | tp/fp/fn | clauses | terms | rule",
        "-------+-------+------+----------+---------+-------+-----",
    ]
    for row in rule_rows:
        lines.append(
            f"{row.target_subtype:<15.15} | {'Y' if row.exact else 'n':^5} | "
            f"{row.correct:>3}/{row.total:<3} | {row.tp:>2}/{row.fp:<2}/{row.fn:<2} | "
            f"{row.clause_count:>3} | {row.term_count:>5} | {row.clause_text}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap local two-clause closure started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
    )
    rule_rows = best_two_clause_rows(
        rows,
        max_clause_terms=args.max_clause_terms,
        clause_limit=args.clause_limit,
        predicate_limit=args.predicate_limit,
    )

    print()
    print("Low-Overlap Local Two-Clause Closure")
    print("====================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(render_rule_rows(rule_rows))
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap local two-clause closure completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
