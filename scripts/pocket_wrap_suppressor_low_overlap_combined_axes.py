#!/usr/bin/env python3
"""Probe combined boundary and profile observables for low-overlap suppressor families."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import statistics
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
from toy_event_physics import (  # noqa: E402
    _profile_symmetry_metrics,
    ordered_profile_centers_and_spans,
)


@dataclass(frozen=True)
class CombinedRow:
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
    crosses_midline: bool


@dataclass(frozen=True)
class PairRuleRow:
    left_subtype: str
    right_subtype: str
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
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--rule-limit", type=int, default=2)
    return parser


def _second_difference_total(values: tuple[float, ...]) -> float:
    if len(values) < 3:
        return 0.0
    return sum(
        abs(values[index + 1] - 2.0 * values[index] + values[index - 1])
        for index in range(1, len(values) - 1)
    )


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def build_rows(log_path: Path) -> list[CombinedRow]:
    rows = reconstruct_low_overlap_rows(log_path)
    result: list[CombinedRow] = []
    for row in rows:
        _xs, centers, spans = ordered_profile_centers_and_spans(set(row.nodes))
        mirror_center_asymmetry, _mirror_span_asymmetry = _profile_symmetry_metrics(
            centers,
            spans,
        )
        half = len(centers) // 2
        left_centers = list(centers[:half]) if half else list(centers)
        right_centers = list(centers[-half:]) if half else list(centers)
        left_spans = list(spans[:half]) if half else list(spans)
        right_spans = list(spans[-half:]) if half else list(spans)
        result.append(
            CombinedRow(
                source_name=row.source_name,
                subtype=row.subtype,
                boundary_fraction=row.boundary_fraction,
                core_low_degree_fraction=row.core_low_degree_fraction,
                low_degree_gap=row.shell_low_degree_fraction - row.core_low_degree_fraction,
                core_deep_fraction=row.core_deep_fraction,
                deep_gap=row.shell_deep_fraction - row.core_deep_fraction,
                boundary_gap=row.shell_boundary_deficit_mean - row.core_boundary_deficit_mean,
                core_boundary_deficit_mean=row.core_boundary_deficit_mean,
                pocket_gap=row.shell_pocket_fraction - row.core_pocket_fraction,
                mirror_center_asymmetry=mirror_center_asymmetry,
                abs_half_center_diff=abs(_mean(right_centers) - _mean(left_centers)),
                half_center_sum=_mean(left_centers) + _mean(right_centers),
                half_span_diff=_mean(right_spans) - _mean(left_spans),
                span_curvature=_second_difference_total(tuple(float(span) for span in spans)),
                crosses_midline=row.crosses_midline,
            )
        )
    result.sort(key=lambda item: item.source_name)
    return result


def candidate_predicates(rows: list[CombinedRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

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
    )
    preferred_order = {
        "core_low_degree_fraction": 0,
        "low_degree_gap": 1,
        "boundary_gap": 2,
        "core_boundary_deficit_mean": 3,
        "core_deep_fraction": 4,
        "deep_gap": 5,
        "pocket_gap": 6,
        "boundary_fraction": 7,
        "mirror_center_asymmetry": 8,
        "abs_half_center_diff": 9,
        "half_center_sum": 10,
        "half_span_diff": 11,
        "span_curvature": 12,
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

    for value, label in ((True, "crosses_midline = Y"), (False, "crosses_midline = n")):
        mask = 0
        for index, row in enumerate(rows):
            if row.crosses_midline == value:
                mask |= 1 << index
        if mask in (0, full_mask):
            continue
        sort_key = (13, "crosses_midline", 1.0 if value else 0.0)
        chosen = predicate_masks.get(mask)
        if chosen is None or (sort_key, label) < (chosen[0], chosen[1]):
            predicate_masks[mask] = (sort_key, label)

    predicates = [(text, mask) for mask, (_sort_key, text) in predicate_masks.items()]
    predicates.sort(key=lambda item: item[0])
    return predicates


def best_rule_for_target(
    rows: list[CombinedRow],
    target_subtype: str,
    *,
    max_terms: int,
) -> PairRuleRow | None:
    if not rows:
        return None

    predicates = candidate_predicates(rows)
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row.subtype == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    best: PairRuleRow | None = None
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
            candidate = PairRuleRow(
                left_subtype="",
                right_subtype="",
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


def pairwise_rules(rows: list[CombinedRow], max_terms: int) -> list[PairRuleRow]:
    subtypes = sorted({row.subtype for row in rows})
    results: list[PairRuleRow] = []
    for left_index in range(len(subtypes)):
        for right_index in range(left_index + 1, len(subtypes)):
            left = subtypes[left_index]
            right = subtypes[right_index]
            pair_rows = [row for row in rows if row.subtype in {left, right}]
            for target in (left, right):
                best = best_rule_for_target(pair_rows, target, max_terms=max_terms)
                if best is None:
                    continue
                results.append(
                    PairRuleRow(
                        left_subtype=left,
                        right_subtype=right,
                        target_subtype=target,
                        exact=best.exact,
                        correct=best.correct,
                        total=best.total,
                        term_count=best.term_count,
                        tp=best.tp,
                        fp=best.fp,
                        fn=best.fn,
                        rule_text=best.rule_text,
                    )
                )
    return results


def render_pair_rules(rows: list[PairRuleRow], limit: int) -> str:
    lines = [
        "pair | target | exact | correct | terms | tp/fp/fn | rule",
        "-----+--------+-------+---------+-------+----------+---------------------------------------------",
    ]
    grouped: dict[tuple[str, str], list[PairRuleRow]] = {}
    for row in rows:
        grouped.setdefault((row.left_subtype, row.right_subtype), []).append(row)
    for pair in sorted(grouped):
        pair_rows = sorted(
            grouped[pair],
            key=lambda row: (
                row.target_subtype,
                not row.exact,
                -row.correct,
                row.term_count,
                row.rule_text,
            ),
        )
        for row in pair_rows[:limit]:
            lines.append(
                f"{row.left_subtype}->{row.right_subtype} | {row.target_subtype:<19.19} | "
                f"{('Y' if row.exact else 'n'):<5} | {row.correct:>3}/{row.total:<3} | {row.term_count:>5} | "
                f"{row.tp:>2}/{row.fp:<2}/{row.fn:<2}     | {row.rule_text}"
            )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap combined axes started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = build_rows(log_path)
    rule_rows = pairwise_rules(rows, max_terms=args.max_terms)

    print()
    print("Low-Overlap Combined Pairwise Rules")
    print("===================================")
    print(f"log={log_path}")
    print(f"rows={len(rows)}")
    print(render_pair_rules(rule_rows, args.rule_limit))
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap combined axes completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
