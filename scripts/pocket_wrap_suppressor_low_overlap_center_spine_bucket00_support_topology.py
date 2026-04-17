#!/usr/bin/env python3
"""Probe support-topology closure inside the dominant center-spine `00` mixed bucket."""

from __future__ import annotations

import argparse
from datetime import datetime
import itertools
from pathlib import Path
import re
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_candidate_support_subgraph_bucket import (  # noqa: E402
    build_rows as build_support_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    RuleRow,
    load_bucket_rows,
)

RULE_TERM_RE = re.compile(
    r"^(?P<feature>[A-Za-z0-9_]+) (?P<operator><=|>=) (?P<threshold>-?\d+(?:\.\d+)?)$"
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
    parser.add_argument("--signature-terms", type=int, default=2)
    parser.add_argument("--candidate-limit", type=int, default=18)
    parser.add_argument("--event-limit", type=int, default=18)
    parser.add_argument("--predicate-limit", type=int, default=12)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def bucket_source_names(bucket_log: Path, bucket_key: str) -> set[str]:
    return {
        row.source_name
        for row in load_bucket_rows(bucket_log)
        if row.bucket_key == bucket_key
    }


def dataclass_feature_names(row: object) -> list[str]:
    return [
        name
        for name in row.__dataclass_fields__  # type: ignore[attr-defined]
        if name not in ("source_name", "subtype")
    ]


def candidate_predicates(rows: list[object], feature_names: list[str]) -> list[tuple[str, int]]:
    full_mask = (1 << len(rows)) - 1
    predicate_masks: dict[int, str] = {}
    for feature_name in feature_names:
        values = sorted({float(getattr(row, feature_name)) for row in rows})
        thresholds: list[float] = []
        if len(values) == 1:
            thresholds.append(values[0])
        else:
            for left, right in zip(values, values[1:]):
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
                if mask not in predicate_masks or text < predicate_masks[mask]:
                    predicate_masks[mask] = text
    predicates = [(text, mask) for mask, text in predicate_masks.items()]
    predicates.sort(key=lambda item: item[0])
    return predicates


def matches_rule_text(row: object, rule_text: str) -> bool:
    for term in rule_text.split(" and "):
        match = RULE_TERM_RE.fullmatch(term.strip())
        if match is None:
            raise ValueError(f"unsupported rule term: {term}")
        feature = match.group("feature")
        operator = match.group("operator")
        threshold = float(match.group("threshold"))
        value = float(getattr(row, feature))
        if operator == "<=" and value > threshold:
            return False
        if operator == ">=" and value < threshold:
            return False
    return True


def evaluate_rules(
    rows: list[object],
    *,
    target_subtype: str,
    feature_names: list[str],
    predicate_limit: int,
    max_terms: int,
    row_limit: int,
) -> list[RuleRow]:
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if getattr(row, "subtype") == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    ranked: list[tuple[tuple[bool, int, int, str], tuple[str, int]]] = []
    for predicate_text, predicate_mask in candidate_predicates(rows, feature_names):
        tp = (predicate_mask & target_mask).bit_count()
        fp = (predicate_mask & non_target_mask).bit_count()
        fn = (target_mask & (full_mask ^ predicate_mask)).bit_count()
        tn = (non_target_mask & (full_mask ^ predicate_mask)).bit_count()
        ranked.append(
            (
                (fp != 0, -(tp + tn), fn, predicate_text),
                (predicate_text, predicate_mask),
            )
        )
    ranked.sort(key=lambda item: item[0])
    selected = [item[1] for item in ranked[: min(predicate_limit, len(ranked))]]

    seen_masks: set[int] = set()
    results: list[RuleRow] = []
    for term_count in range(1, max_terms + 1):
        for predicate_tuple in itertools.combinations(selected, term_count):
            mask = full_mask
            sorted_terms = tuple(sorted(predicate_tuple, key=lambda item: item[0]))
            for _text, predicate_mask in sorted_terms:
                mask &= predicate_mask
                if mask == 0:
                    break
            if mask == 0 or mask in seen_masks:
                continue
            seen_masks.add(mask)
            tp = (mask & target_mask).bit_count()
            fp = (mask & non_target_mask).bit_count()
            fn = (target_mask & (full_mask ^ mask)).bit_count()
            tn = (non_target_mask & (full_mask ^ mask)).bit_count()
            results.append(
                RuleRow(
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
            )
    results.sort(
        key=lambda row: (
            not row.exact,
            -row.correct,
            row.term_count,
            row.rule_text,
        )
    )
    return results[:row_limit]


def best_rule_for_target(
    rows: list[object],
    *,
    target_subtype: str,
    feature_names: list[str],
    predicate_limit: int,
    max_terms: int,
) -> RuleRow:
    rules = evaluate_rules(
        rows,
        target_subtype=target_subtype,
        feature_names=feature_names,
        predicate_limit=predicate_limit,
        max_terms=max_terms,
        row_limit=1,
    )
    if not rules:
        raise ValueError(f"no rules found for target subtype {target_subtype}")
    return rules[0]


def render_rows(rows: list[object], feature_names: list[str]) -> str:
    shown = [
        "source_name",
        "subtype",
        "bridge_support_fraction",
        "bridge_support_left_fraction",
        "bridge_support_edge_density",
        "candidate_cross_lobe_fraction",
        "candidate_cross_family_fraction",
        "bridge_event_present_count",
    ]
    shown += [name for name in feature_names if name.startswith("bridge_node_dx0_dy")][:4]
    lines = [
        "Bucket 00 support-topology rows",
        "===============================",
        " | ".join(shown),
        " | ".join("-" * len(name) for name in shown),
    ]
    for row in rows:
        values: list[str] = []
        for name in shown:
            value = getattr(row, name)
            if isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        lines.append(" | ".join(values))
    return "\n".join(lines)


def render_rules(title: str, rules: list[RuleRow]) -> str:
    lines = [
        title,
        "=" * len(title),
        "target | exact | corr | tp/fp/fn | terms | rule",
        "-------+-------+------+----------+-------+-----",
    ]
    for row in rules:
        lines.append(
            f"{row.target_subtype:<15.15} | {'Y' if row.exact else 'n':^5} | "
            f"{row.correct:>3}/{row.total:<3} | {row.tp:>2}/{row.fp:>2}/{row.fn:>2} | "
            f"{row.term_count:>5} | {row.rule_text}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 support topology started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    target_names = bucket_source_names(bucket_log, args.bucket_key)

    support_rows, _selected_events, _signature_text, _bucket_text = build_support_rows(
        frontier_log,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )
    rows = [row for row in support_rows if row.source_name in target_names]
    rows.sort(key=lambda row: row.source_name)
    feature_names = dataclass_feature_names(rows[0])

    add4_rules = evaluate_rules(
        rows,
        target_subtype=args.right_subtype,
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    add1_rules = evaluate_rules(
        rows,
        target_subtype=args.left_subtype,
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    add4_count = sum(1 for row in rows if row.subtype == args.right_subtype)
    add1_count = sum(1 for row in rows if row.subtype == args.left_subtype)

    print()
    print("Center-Spine Bucket 00 Support-Topology Closure")
    print("===============================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)} add1_rows={add1_count} add4_rows={add4_count}")
    print()
    print(render_rows(rows, feature_names))
    print()
    print(render_rules(f"Best support-topology rules for {args.right_subtype}", add4_rules))
    print()
    print(render_rules(f"Best support-topology rules for {args.left_subtype}", add1_rules))
    print()
    print(
        "center-spine bucket00 support topology completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
