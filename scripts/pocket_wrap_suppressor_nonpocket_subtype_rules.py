#!/usr/bin/env python3
"""Find exact small rules for non-pocket suppressor-response subtypes."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import signal
import sys
import time
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_suppressor_nonpocket_subtype_analysis,
)


@dataclass(frozen=True)
class LabeledNonPocketRow:
    source_name: str
    subtype: str
    deep_overlap_count: int
    add_1_0_outcome: str
    add_4_0_outcome: str
    boundary_fraction: float
    pocket_fraction: float
    boundary_roughness: float
    deep_pocket_fraction: float
    mean_center: float
    center_range: float
    center_total_variation: float
    crosses_midline: bool
    span_range: int
    shell_deep_fraction: float
    core_deep_fraction: float
    shell_pocket_fraction: float
    core_pocket_fraction: float
    shell_low_degree_fraction: float
    core_low_degree_fraction: float
    shell_boundary_deficit_mean: float
    core_boundary_deficit_mean: float


@dataclass(frozen=True)
class SubtypeRuleRow:
    target_subtype: str
    rule_text: str
    term_count: int
    tp: int
    fp: int
    fn: int


class RunTimedOutError(RuntimeError):
    """Raised when the optional wall-clock guard expires."""


def _safe_label(text: str) -> str:
    return text.encode("unicode_escape").decode("ascii")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant-limit", type=int, default=192)
    parser.add_argument("--rule-limit", type=int, default=6)
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=None,
        help="Optional wall-clock timeout for bounded automation runs.",
    )
    return parser


def label_rows(variant_limit: int) -> list[LabeledNonPocketRow]:
    analysis_rows = pocket_wrap_suppressor_nonpocket_subtype_analysis(
        variant_limit=variant_limit,
    )
    labeled_rows: list[LabeledNonPocketRow] = []
    for row in analysis_rows:
        labeled_rows.append(
            LabeledNonPocketRow(
                source_name=row.source_name,
                subtype=row.subtype,
                deep_overlap_count=row.deep_overlap_count,
                add_1_0_outcome=row.add_1_0_outcome,
                add_4_0_outcome=row.add_4_0_outcome,
                boundary_fraction=row.boundary_fraction,
                pocket_fraction=row.pocket_fraction,
                boundary_roughness=row.boundary_roughness,
                deep_pocket_fraction=row.deep_pocket_fraction,
                mean_center=row.mean_center,
                center_range=row.center_range,
                center_total_variation=row.center_total_variation,
                crosses_midline=row.crosses_midline,
                span_range=row.span_range,
                shell_deep_fraction=row.shell_deep_fraction,
                core_deep_fraction=row.core_deep_fraction,
                shell_pocket_fraction=row.shell_pocket_fraction,
                core_pocket_fraction=row.core_pocket_fraction,
                shell_low_degree_fraction=row.shell_low_degree_fraction,
                core_low_degree_fraction=row.core_low_degree_fraction,
                shell_boundary_deficit_mean=row.shell_boundary_deficit_mean,
                core_boundary_deficit_mean=row.core_boundary_deficit_mean,
            )
        )
    labeled_rows.sort(key=lambda item: item.source_name)
    return labeled_rows


def search_exact_rules(
    rows: list[LabeledNonPocketRow],
    target_subtype: str,
) -> list[SubtypeRuleRow]:
    if not rows:
        return []

    numeric_features = (
        "deep_overlap_count",
        "boundary_fraction",
        "pocket_fraction",
        "boundary_roughness",
        "deep_pocket_fraction",
        "mean_center",
        "center_range",
        "center_total_variation",
        "span_range",
        "shell_deep_fraction",
        "core_deep_fraction",
        "shell_pocket_fraction",
        "core_pocket_fraction",
        "shell_low_degree_fraction",
        "core_low_degree_fraction",
        "shell_boundary_deficit_mean",
        "core_boundary_deficit_mean",
    )
    preferred_order = {
        "crosses_midline": 0,
        "center_total_variation": 1,
        "boundary_roughness": 2,
        "pocket_fraction": 3,
        "span_range": 4,
        "deep_overlap_count": 5,
    }

    Predicate = tuple[str, Callable[[LabeledNonPocketRow], bool], tuple[int, str, float]]
    predicates: list[Predicate] = []

    for feature_name in numeric_features:
        value_to_labels: dict[float, set[bool]] = {}
        for row in rows:
            value = float(getattr(row, feature_name))
            labels = value_to_labels.setdefault(value, set())
            labels.add(row.subtype == target_subtype)

        values = sorted(value_to_labels)
        thresholds: list[float] = []
        if len(values) == 1:
            thresholds.append(values[0])
        else:
            for left, right in zip(values, values[1:]):
                # Only keep boundaries where target/non-target membership can change.
                if value_to_labels[left] != value_to_labels[right]:
                    thresholds.append((left + right) / 2.0)
        for threshold in thresholds:
            predicates.append(
                (
                    f"{feature_name} <= {threshold:.3f}",
                    lambda row, feature_name=feature_name, threshold=threshold: float(
                        getattr(row, feature_name)
                    )
                    <= threshold,
                    (preferred_order.get(feature_name, 99), feature_name, threshold),
                )
            )
            predicates.append(
                (
                    f"{feature_name} >= {threshold:.3f}",
                    lambda row, feature_name=feature_name, threshold=threshold: float(
                        getattr(row, feature_name)
                    )
                    >= threshold,
                    (preferred_order.get(feature_name, 99), feature_name, threshold),
                )
            )

    predicates.append(
        (
            "crosses_midline = Y",
            lambda row: row.crosses_midline,
            (preferred_order["crosses_midline"], "crosses_midline", 1.0),
        )
    )
    predicates.append(
        (
            "crosses_midline = n",
            lambda row: not row.crosses_midline,
            (preferred_order["crosses_midline"], "crosses_midline", 0.0),
        )
    )

    seen_rule_texts: set[str] = set()
    exact_rows: list[SubtypeRuleRow] = []
    row_count = len(rows)
    full_mask = (1 << row_count) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row.subtype == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    # Many threshold predicates collapse to the same prediction set.
    # Keep one canonical text form per mask to avoid redundant combinations.
    predicate_by_mask: dict[int, Predicate] = {}
    for predicate in predicates:
        mask = 0
        for index, row in enumerate(rows):
            if predicate[1](row):
                mask |= 1 << index
        chosen = predicate_by_mask.get(mask)
        if chosen is None or (predicate[2], predicate[0]) < (chosen[2], chosen[0]):
            predicate_by_mask[mask] = predicate

    predicate_with_masks = [(predicate, mask) for mask, predicate in predicate_by_mask.items()]

    predicate_sets = [(item,) for item in predicate_with_masks]
    predicate_sets.extend(itertools.combinations(predicate_with_masks, 2))
    for predicate_tuple in predicate_sets:
        sorted_terms = tuple(
            sorted((item[0] for item in predicate_tuple), key=lambda item: item[2])
        )
        rule_text = " and ".join(term[0] for term in sorted_terms)
        if rule_text in seen_rule_texts:
            continue
        seen_rule_texts.add(rule_text)

        predicted_mask = full_mask
        for _predicate, mask in predicate_tuple:
            predicted_mask &= mask
            if predicted_mask == 0:
                break
        tp = (predicted_mask & target_mask).bit_count()
        fp = (predicted_mask & non_target_mask).bit_count()
        fn = (target_mask & (full_mask ^ predicted_mask)).bit_count()
        if fp == 0 and fn == 0:
            exact_rows.append(
                SubtypeRuleRow(
                    target_subtype=target_subtype,
                    rule_text=rule_text,
                    term_count=len(sorted_terms),
                    tp=tp,
                    fp=fp,
                    fn=fn,
                )
            )

    exact_rows.sort(
        key=lambda row: (
            row.term_count,
            row.rule_text,
        )
    )
    return exact_rows


def render_rows(rows: list[LabeledNonPocketRow]) -> str:
    if not rows:
        return "(no non-pocket overlap-positive rows)"
    header = (
        "source_name | subtype | add1/add4 | overlap | cross | "
        "brough | pocket_frac | ctv | span"
    )
    lines = [header]
    for row in rows:
        lines.append(
            " | ".join(
                (
                    _safe_label(row.source_name),
                    row.subtype,
                    f"{row.add_1_0_outcome}/{row.add_4_0_outcome}",
                    str(row.deep_overlap_count),
                    ("Y" if row.crosses_midline else "n"),
                    f"{row.boundary_roughness:.3f}",
                    f"{row.pocket_fraction:.3f}",
                    f"{row.center_total_variation:.2f}",
                    str(row.span_range),
                )
            )
        )
    return "\n".join(lines)


def render_rules(rows: list[SubtypeRuleRow], limit: int) -> str:
    if not rows:
        return "(no exact 1-2 term rules found)"
    lines = ["subtype | terms | tp | rule"]
    for row in rows[:limit]:
        lines.append(
            f"{row.target_subtype} | {row.term_count} | {row.tp} | {row.rule_text}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"non-pocket suppressor subtype rules started {started}", flush=True)
    total_start = time.time()
    timer_enabled = args.max_seconds is not None and args.max_seconds > 0

    def _on_alarm(_signum: int, _frame: object) -> None:
        raise RunTimedOutError

    previous_handler = signal.getsignal(signal.SIGALRM)
    try:
        if timer_enabled:
            signal.signal(signal.SIGALRM, _on_alarm)
            signal.setitimer(signal.ITIMER_REAL, float(args.max_seconds))

        rows = label_rows(variant_limit=args.variant_limit)
        subtypes = sorted({row.subtype for row in rows})
        exact_rules: list[SubtypeRuleRow] = []
        for subtype in subtypes:
            exact_rules.extend(search_exact_rules(rows, subtype))
    except RunTimedOutError:
        print(
            "non-pocket suppressor subtype rules timed out "
            + datetime.now().isoformat(timespec="seconds")
            + f" elapsed={time.time() - total_start:.1f}s"
            + f" variant_limit={args.variant_limit}"
            + f" max_seconds={args.max_seconds}",
            flush=True,
        )
        raise SystemExit(124)
    except KeyboardInterrupt:
        print(
            "non-pocket suppressor subtype rules interrupted "
            + datetime.now().isoformat(timespec="seconds")
            + f" elapsed={time.time() - total_start:.1f}s"
            + f" variant_limit={args.variant_limit}",
            flush=True,
        )
        raise SystemExit(130)
    finally:
        if timer_enabled:
            try:
                signal.setitimer(signal.ITIMER_REAL, 0.0)
            except KeyboardInterrupt:
                pass
            try:
                signal.signal(signal.SIGALRM, previous_handler)
            except KeyboardInterrupt:
                pass

    print()
    print("Non-Pocket Suppressor Subtype Context")
    print("=====================================")
    print(
        f"variant_limit={args.variant_limit} nonpocket_rows={len(rows)} subtype_count={len(subtypes)}"
    )
    print(render_rows(rows))
    print()
    print("Non-Pocket Suppressor Subtype Exact Rules")
    print("=========================================")
    print(render_rules(exact_rules, limit=args.rule_limit))
    print()
    print(
        "non-pocket suppressor subtype rules completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
