#!/usr/bin/env python3
"""Probe profile/asymmetry observables for low-overlap suppressor families on a frozen log."""

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
class LowOverlapProfileRow:
    source_name: str
    subtype: str
    mirror_center_asymmetry: float
    mirror_span_asymmetry: float
    endpoint_center_asymmetry: float
    endpoint_span_asymmetry: float
    half_center_sum: float
    half_center_diff: float
    half_span_diff: float
    center_slope_max: float
    span_slope_max: float
    center_curvature: float
    span_curvature: float
    crosses_midline: bool
    span_range: int
    center_total_variation: float


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


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _second_difference_total(values: tuple[float, ...]) -> float:
    if len(values) < 3:
        return 0.0
    return sum(
        abs(values[index + 1] - 2.0 * values[index] + values[index - 1])
        for index in range(1, len(values) - 1)
    )


def build_profile_rows(log_path: Path) -> list[LowOverlapProfileRow]:
    rows = reconstruct_low_overlap_rows(log_path)
    profile_rows: list[LowOverlapProfileRow] = []
    for row in rows:
        xs, centers, spans = ordered_profile_centers_and_spans(set(row.nodes))
        del xs
        mirror_center_asymmetry, mirror_span_asymmetry = _profile_symmetry_metrics(
            centers,
            spans,
        )
        endpoint_center_asymmetry = abs(centers[0] + centers[-1]) if len(centers) >= 2 else 0.0
        endpoint_span_asymmetry = abs(spans[0] - spans[-1]) if len(spans) >= 2 else 0.0
        half = len(centers) // 2
        left_centers = list(centers[:half]) if half else list(centers)
        right_centers = list(centers[-half:]) if half else list(centers)
        left_spans = list(spans[:half]) if half else list(spans)
        right_spans = list(spans[-half:]) if half else list(spans)
        half_center_sum = _mean(left_centers) + _mean(right_centers)
        half_center_diff = _mean(right_centers) - _mean(left_centers)
        half_span_diff = _mean(right_spans) - _mean(left_spans)
        center_deltas = [abs(centers[index + 1] - centers[index]) for index in range(len(centers) - 1)]
        span_deltas = [abs(spans[index + 1] - spans[index]) for index in range(len(spans) - 1)]
        profile_rows.append(
            LowOverlapProfileRow(
                source_name=row.source_name,
                subtype=row.subtype,
                mirror_center_asymmetry=mirror_center_asymmetry,
                mirror_span_asymmetry=mirror_span_asymmetry,
                endpoint_center_asymmetry=endpoint_center_asymmetry,
                endpoint_span_asymmetry=endpoint_span_asymmetry,
                half_center_sum=half_center_sum,
                half_center_diff=half_center_diff,
                half_span_diff=half_span_diff,
                center_slope_max=max(center_deltas) if center_deltas else 0.0,
                span_slope_max=max(span_deltas) if span_deltas else 0.0,
                center_curvature=_second_difference_total(centers),
                span_curvature=_second_difference_total(tuple(float(span) for span in spans)),
                crosses_midline=row.crosses_midline,
                span_range=row.span_range,
                center_total_variation=row.center_total_variation,
            )
        )
    profile_rows.sort(key=lambda item: item.source_name)
    return profile_rows


def candidate_predicates(rows: list[LowOverlapProfileRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_defs = (
        ("mirror_center_asymmetry", lambda row: row.mirror_center_asymmetry),
        ("mirror_span_asymmetry", lambda row: row.mirror_span_asymmetry),
        ("endpoint_center_asymmetry", lambda row: row.endpoint_center_asymmetry),
        ("endpoint_span_asymmetry", lambda row: row.endpoint_span_asymmetry),
        ("half_center_sum", lambda row: row.half_center_sum),
        ("abs_half_center_sum", lambda row: abs(row.half_center_sum)),
        ("half_center_diff", lambda row: row.half_center_diff),
        ("abs_half_center_diff", lambda row: abs(row.half_center_diff)),
        ("half_span_diff", lambda row: row.half_span_diff),
        ("abs_half_span_diff", lambda row: abs(row.half_span_diff)),
        ("center_slope_max", lambda row: row.center_slope_max),
        ("span_slope_max", lambda row: row.span_slope_max),
        ("center_curvature", lambda row: row.center_curvature),
        ("span_curvature", lambda row: row.span_curvature),
        ("span_range", lambda row: float(row.span_range)),
        ("center_total_variation", lambda row: row.center_total_variation),
    )
    preferred_order = {
        "mirror_center_asymmetry": 0,
        "mirror_span_asymmetry": 1,
        "endpoint_center_asymmetry": 2,
        "endpoint_span_asymmetry": 3,
        "half_center_sum": 4,
        "abs_half_center_sum": 5,
        "half_center_diff": 6,
        "abs_half_center_diff": 7,
        "half_span_diff": 8,
        "abs_half_span_diff": 9,
        "center_slope_max": 10,
        "span_slope_max": 11,
        "center_curvature": 12,
        "span_curvature": 13,
        "center_total_variation": 14,
        "span_range": 15,
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
        sort_key = (16, "crosses_midline", 1.0 if value else 0.0)
        chosen = predicate_masks.get(mask)
        if chosen is None or (sort_key, label) < (chosen[0], chosen[1]):
            predicate_masks[mask] = (sort_key, label)

    predicates = [(text, mask) for mask, (_sort_key, text) in predicate_masks.items()]
    predicates.sort(key=lambda item: item[0])
    return predicates


def best_rule_for_target(
    rows: list[LowOverlapProfileRow],
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


def pairwise_rules(rows: list[LowOverlapProfileRow], max_terms: int) -> list[PairRuleRow]:
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


def median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def render_envelopes(rows: list[LowOverlapProfileRow]) -> str:
    lines = [
        "subtype | cases | asym~ | esp~ | hcdiff~ | slope~ | curv~ | cross rate | ctv~",
        "--------+-------+-------+------+----------+--------+-------+------------+-----",
    ]
    for subtype in sorted({row.subtype for row in rows}):
        bucket = [row for row in rows if row.subtype == subtype]
        lines.append(
            f"{subtype:<19.19} | {len(bucket):>5} | "
            f"{median([row.mirror_center_asymmetry for row in bucket]):>5.3f} | "
            f"{median([row.endpoint_span_asymmetry for row in bucket]):>4.1f} | "
            f"{median([abs(row.half_center_diff) for row in bucket]):>8.3f} | "
            f"{median([row.center_slope_max for row in bucket]):>6.3f} | "
            f"{median([row.center_curvature for row in bucket]):>5.3f} | "
            f"{sum(1 for row in bucket if row.crosses_midline) / len(bucket):>10.2f} | "
            f"{median([row.center_total_variation for row in bucket]):>3.1f}"
        )
    return "\n".join(lines)


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
    print(f"low-overlap profile axes started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = build_profile_rows(log_path)
    rule_rows = pairwise_rules(rows, max_terms=args.max_terms)

    print()
    print("Low-Overlap Profile Envelopes")
    print("=============================")
    print(f"log={log_path}")
    print(f"rows={len(rows)}")
    print(render_envelopes(rows))
    print()
    print("Low-Overlap Profile Pairwise Rules")
    print("==================================")
    print(render_pair_rules(rule_rows, args.rule_limit))
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap profile axes completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
