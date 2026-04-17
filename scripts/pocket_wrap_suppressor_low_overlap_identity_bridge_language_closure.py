#!/usr/bin/env python3
"""Probe compact closures using candidate identity plus translated bridge language."""

from __future__ import annotations

import argparse
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

from pocket_wrap_suppressor_low_overlap_bridge_event_translation import (  # noqa: E402
    translate_rows,
)
from pocket_wrap_suppressor_low_overlap_candidate_identity_bucket import (  # noqa: E402
    build_rows as build_candidate_identity_rows,
)


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
    parser.add_argument("--event-limit", type=int, default=18)
    parser.add_argument("--predicate-limit", type=int, default=24)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _prefixed_features(row: object, prefix: str) -> dict[str, float]:
    features: dict[str, float] = {}
    for name, value in vars(row).items():
        if name in {"source_name", "subtype"}:
            continue
        features[f"{prefix}_{name}"] = float(value)
    return features


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
    event_limit: int,
) -> tuple[list[dict[str, object]], str, str]:
    identity_rows, _identity_events, signature_text, bucket_text = build_candidate_identity_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
        event_limit=event_limit,
    )
    bridge_rows, _selected_events, _sig2, _bucket2 = translate_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
        event_limit=event_limit,
    )
    bridge_by_source = {row.source_name: row for row in bridge_rows}
    rows: list[dict[str, object]] = []
    for identity in identity_rows:
        source_name = getattr(identity, "source_name")
        bridge = bridge_by_source[source_name]
        features = {}
        features.update(_prefixed_features(identity, "identity"))
        features.update(_prefixed_features(bridge, "bridge"))
        rows.append(
            {
                "source_name": source_name,
                "subtype": getattr(identity, "subtype"),
                "features": features,
            }
        )
    rows.sort(key=lambda row: str(row["source_name"]))
    return rows, signature_text, bucket_text


def candidate_predicates(rows: list[dict[str, object]]) -> list[tuple[str, int]]:
    if not rows:
        return []
    feature_names = sorted(rows[0]["features"].keys())  # type: ignore[index]
    full_mask = (1 << len(rows)) - 1
    predicate_masks: dict[int, str] = {}
    for feature_name in feature_names:
        value_to_labels: dict[float, set[str]] = {}
        for row in rows:
            value = float(row["features"][feature_name])  # type: ignore[index]
            value_to_labels.setdefault(value, set()).add(str(row["subtype"]))
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
                    value = float(row["features"][feature_name])  # type: ignore[index]
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


def best_rows(
    rows: list[dict[str, object]],
    *,
    predicate_limit: int,
    max_terms: int,
    row_limit: int,
) -> list[dict[str, object]]:
    full_mask = (1 << len(rows)) - 1
    predicates = candidate_predicates(rows)
    target_subtypes = tuple(sorted({str(row["subtype"]) for row in rows}))
    results: list[dict[str, object]] = []

    def score(mask: int, target_mask: int, non_target_mask: int) -> tuple[int, int, int, int]:
        tp = (mask & target_mask).bit_count()
        fp = (mask & non_target_mask).bit_count()
        fn = (target_mask & (full_mask ^ mask)).bit_count()
        tn = (non_target_mask & (full_mask ^ mask)).bit_count()
        return tp, fp, fn, tp + tn

    for target_subtype in target_subtypes:
        target_mask = 0
        for index, row in enumerate(rows):
            if row["subtype"] == target_subtype:
                target_mask |= 1 << index
        non_target_mask = full_mask ^ target_mask
        ranked_predicates: list[tuple[tuple[bool, int, int, str], tuple[str, int]]] = []
        for predicate_text, predicate_mask in predicates:
            tp, fp, fn, correct = score(predicate_mask, target_mask, non_target_mask)
            ranked_predicates.append(
                (
                    (fp != 0, -correct, -tp, predicate_text),
                    (predicate_text, predicate_mask),
                )
            )
        ranked_predicates.sort(key=lambda item: item[0])
        selected_predicates = [item[1] for item in ranked_predicates[:predicate_limit]]

        seen_masks: set[int] = set()
        scored_rows: list[dict[str, object]] = []
        for term_count in range(1, max_terms + 1):
            for predicate_tuple in itertools.combinations(selected_predicates, term_count):
                sorted_terms = tuple(sorted(predicate_tuple, key=lambda item: item[0]))
                predicted_mask = full_mask
                for _text, mask in sorted_terms:
                    predicted_mask &= mask
                    if predicted_mask == 0:
                        break
                if predicted_mask == 0 or predicted_mask in seen_masks:
                    continue
                seen_masks.add(predicted_mask)
                tp, fp, fn, correct = score(predicted_mask, target_mask, non_target_mask)
                scored_rows.append(
                    {
                        "target_subtype": target_subtype,
                        "exact": fp == 0 and fn == 0,
                        "correct": correct,
                        "total": len(rows),
                        "term_count": term_count,
                        "tp": tp,
                        "fp": fp,
                        "fn": fn,
                        "rule_text": " and ".join(term[0] for term in sorted_terms),
                    }
                )
        scored_rows.sort(
            key=lambda row: (
                not bool(row["exact"]),
                -int(row["correct"]),
                int(row["term_count"]),
                str(row["rule_text"]),
            )
        )
        results.extend(scored_rows[:row_limit])
    return results


def render_rows(rule_rows: list[dict[str, object]]) -> str:
    lines = [
        "Identity+Bridge-Language Closures",
        "=================================",
        "target | exact | corr | tp/fp/fn | terms | rule",
        "-------+-------+------+----------+-------+-----",
    ]
    for row in rule_rows:
        lines.append(
            f"{str(row['target_subtype']):<15.15} | {'Y' if row['exact'] else 'n':^5} | "
            f"{int(row['correct']):>3}/{int(row['total']):<3} | {int(row['tp']):>2}/{int(row['fp']):<2}/{int(row['fn']):<2} | "
            f"{int(row['term_count']):>5} | {row['rule_text']}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"identity+bridge-language closure started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )
    rule_rows = best_rows(
        rows,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Identity+Bridge-Language Closure")
    print("================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(render_rows(rule_rows))
    print()
    print(
        "identity+bridge-language closure completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
