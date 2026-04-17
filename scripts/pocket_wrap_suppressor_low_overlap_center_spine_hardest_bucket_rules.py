#!/usr/bin/env python3
"""Search compact visible-field rules inside the center-spine mixed add4 micro-buckets."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import re
import time


VISIBLE_FEATURES = (
    "id_pocket_left_fraction",
    "id_deep_left_fraction",
    "support_bridge_support_edge_density",
    "support_bridge_support_left_fraction",
    "support_bridge_event_present_count",
)


@dataclass(frozen=True)
class BucketRow:
    bucket_key: str
    source_name: str
    subtype: str
    id_pocket_left_fraction: float
    id_deep_left_fraction: float
    support_bridge_support_edge_density: float
    support_bridge_support_left_fraction: float
    support_bridge_event_present_count: float

    @property
    def features(self) -> dict[str, float]:
        return {
            "id_pocket_left_fraction": self.id_pocket_left_fraction,
            "id_deep_left_fraction": self.id_deep_left_fraction,
            "support_bridge_support_edge_density": self.support_bridge_support_edge_density,
            "support_bridge_support_left_fraction": self.support_bridge_support_left_fraction,
            "support_bridge_event_present_count": self.support_bridge_event_present_count,
        }


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


ROW_PATTERN = re.compile(
    r"  - (?P<source_name>.*?) \| (?P<subtype>.*?) \| "
    r"id_pocket_left=(?P<id_pocket_left>[0-9.]+) \| "
    r"id_deep_left=(?P<id_deep_left>[0-9.]+) \| "
    r"support_edge=(?P<support_edge>[0-9.]+) \| "
    r"support_left=(?P<support_left>[0-9.]+) \| "
    r"support_events=(?P<support_events>[0-9.]+)"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-micro-buckets-5504-add1-vs-add4.txt",
    )
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def load_bucket_rows(log_path: Path) -> list[BucketRow]:
    rows: list[BucketRow] = []
    bucket_key: str | None = None
    for line in log_path.read_text().splitlines():
        if line.startswith("bucket_key="):
            bucket_key = line.split()[0].split("=", 1)[1]
            continue
        match = ROW_PATTERN.match(line)
        if match is None or bucket_key is None:
            continue
        rows.append(
            BucketRow(
                bucket_key=bucket_key,
                source_name=match.group("source_name"),
                subtype=match.group("subtype").strip(),
                id_pocket_left_fraction=float(match.group("id_pocket_left")),
                id_deep_left_fraction=float(match.group("id_deep_left")),
                support_bridge_support_edge_density=float(match.group("support_edge")),
                support_bridge_support_left_fraction=float(match.group("support_left")),
                support_bridge_event_present_count=float(match.group("support_events")),
            )
        )
    return rows


def candidate_predicates(rows: list[BucketRow]) -> list[tuple[str, int]]:
    full_mask = (1 << len(rows)) - 1
    predicate_masks: dict[int, str] = {}
    for feature_name in VISIBLE_FEATURES:
        values = sorted({row.features[feature_name] for row in rows})
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
                    value = row.features[feature_name]
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


def evaluate_rules(
    rows: list[BucketRow],
    *,
    target_subtype: str,
    max_terms: int,
    row_limit: int,
) -> list[RuleRow]:
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row.subtype == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    predicates = candidate_predicates(rows)

    ranked: list[tuple[tuple[bool, int, int, str], tuple[str, int]]] = []
    for predicate_text, predicate_mask in predicates:
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
    selected = [item[1] for item in ranked[: min(12, len(ranked))]]

    seen_masks: set[int] = set()
    results: list[RuleRow] = []
    for term_count in range(1, max_terms + 1):
        for predicate_tuple in itertools.combinations(selected, term_count):
            sorted_terms = tuple(sorted(predicate_tuple, key=lambda item: item[0]))
            mask = full_mask
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


def mixed_buckets(
    rows: list[BucketRow],
    *,
    add4_subtype: str,
) -> list[tuple[str, list[BucketRow]]]:
    grouped: dict[str, list[BucketRow]] = {}
    for row in rows:
        grouped.setdefault(row.bucket_key, []).append(row)
    results: list[tuple[str, list[BucketRow]]] = []
    for bucket_key, bucket_rows in sorted(grouped.items()):
        labels = {row.subtype for row in bucket_rows}
        if add4_subtype in labels and len(labels) > 1:
            results.append((bucket_key, sorted(bucket_rows, key=lambda row: row.source_name)))
    return results


def render_rows(title: str, rows: list[BucketRow]) -> str:
    lines = [
        title,
        "=" * len(title),
        "source | subtype | id_pocket_left | id_deep_left | support_edge | support_left | support_events",
        "------+--------+----------------+--------------+--------------+--------------+---------------",
    ]
    for row in rows:
        lines.append(
            f"{row.source_name} | {row.subtype:<15.15} | "
            f"{row.id_pocket_left_fraction:>14.3f} | {row.id_deep_left_fraction:>12.3f} | "
            f"{row.support_bridge_support_edge_density:>12.3f} | {row.support_bridge_support_left_fraction:>12.3f} | "
            f"{row.support_bridge_event_present_count:>13.3f}"
        )
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


def render_bucket_summary(rows: list[BucketRow]) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.subtype] = counts.get(row.subtype, 0) + 1
    counts_text = ", ".join(f"{label}:{counts[label]}" for label in sorted(counts))
    return f"bucket_key={rows[0].bucket_key} rows={len(rows)} counts={counts_text}"


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine hardest bucket rules started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = load_bucket_rows(log_path)
    mixed = mixed_buckets(rows, add4_subtype=args.right_subtype)
    hardest_key, hardest_rows = max(
        mixed,
        key=lambda item: (len(item[1]), sum(row.subtype == args.right_subtype for row in item[1])),
    )

    print()
    print("Center-Spine Visible Mixed Buckets")
    print("==================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print(f"mixed_bucket_count={len(mixed)}")
    for bucket_key, bucket_rows in mixed:
        print(render_bucket_summary(bucket_rows))
    print()

    for bucket_key, bucket_rows in mixed:
        add4_rules = evaluate_rules(
            bucket_rows,
            target_subtype=args.right_subtype,
            max_terms=args.max_terms,
            row_limit=args.row_limit,
        )
        add1_rules = evaluate_rules(
            bucket_rows,
            target_subtype=args.left_subtype,
            max_terms=args.max_terms,
            row_limit=args.row_limit,
        )
        print(render_rows(f"Bucket {bucket_key} visible rows", bucket_rows))
        print()
        print(render_rules(f"Best visible-field rules for {args.right_subtype} in bucket {bucket_key}", add4_rules))
        print()
        print(render_rules(f"Best visible-field rules for {args.left_subtype} in bucket {bucket_key}", add1_rules))
        print()

    print(f"selected_hardest_bucket={hardest_key} rows={len(hardest_rows)}")
    print()
    print(
        "center-spine hardest bucket rules completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
