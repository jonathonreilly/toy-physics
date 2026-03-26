#!/usr/bin/env python3
"""Probe the center-spine residual bucket for compact add1-vs-add4 closure."""

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
from pocket_wrap_suppressor_low_overlap_identity_lobe_support_joined_closure import (  # noqa: E402
    build_rows as build_joined_rows,
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
    parser.add_argument("--spine-threshold", type=float, default=0.5)
    parser.add_argument("--predicate-limit", type=int, default=32)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=10)
    return parser


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


def evaluate_rules(
    rows: list[dict[str, object]],
    *,
    target_subtype: str,
    predicate_limit: int,
    max_terms: int,
    row_limit: int,
) -> list[dict[str, object]]:
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row["subtype"] == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    predicates = candidate_predicates(rows)

    def score(mask: int) -> tuple[int, int, int, int]:
        tp = (mask & target_mask).bit_count()
        fp = (mask & non_target_mask).bit_count()
        fn = (target_mask & (full_mask ^ mask)).bit_count()
        tn = (non_target_mask & (full_mask ^ mask)).bit_count()
        return tp, fp, fn, tp + tn

    ranked: list[tuple[tuple[bool, int, int, str], tuple[str, int]]] = []
    for predicate_text, predicate_mask in predicates:
        tp, fp, fn, correct = score(predicate_mask)
        ranked.append(((fp != 0, -correct, -tp, predicate_text), (predicate_text, predicate_mask)))
    ranked.sort(key=lambda item: item[0])
    selected_predicates = [item[1] for item in ranked[:predicate_limit]]

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
            tp, fp, fn, correct = score(predicted_mask)
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
    return scored_rows[:row_limit]


def render_bucket(rows: list[dict[str, object]], *, target_subtype: str) -> str:
    lines = [
        f"Center-spine residual bucket rows (target={target_subtype})",
        "=====================================================",
        "source | subtype | deep_left | id_events | bridge_dx0_dy3 | bridge_dx0_dy4 | support_edge_density",
        "------+--------+-----------+-----------+----------------+----------------+----------------------",
    ]
    for row in rows:
        feats = row["features"]  # type: ignore[index]
        lines.append(
            f"{str(row['source_name']):<28.28} | {str(row['subtype']):<15.15} | "
            f"{float(feats['identity_deep_left_fraction']):>9.3f} | {float(feats['identity_event_present_count']):>9.3f} | "
            f"{float(feats['support_bridge_node_dx0_dy3']):>14.3f} | {float(feats['support_bridge_node_dx0_dy4']):>14.3f} | "
            f"{float(feats['support_bridge_support_edge_density']):>20.3f}"
        )
    return "\n".join(lines)


def render_rules(title: str, rules: list[dict[str, object]]) -> str:
    lines = [
        title,
        "=" * len(title),
        "target | exact | corr | tp/fp/fn | terms | rule",
        "-------+-------+------+----------+-------+-----",
    ]
    for row in rules:
        lines.append(
            f"{str(row['target_subtype']):<15.15} | {'Y' if row['exact'] else 'n':^5} | "
            f"{int(row['correct']):>3}/{int(row['total']):<3} | {int(row['tp']):>2}/{int(row['fp']):<2}/{int(row['fn']):<2} | "
            f"{int(row['term_count']):>5} | {row['rule_text']}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine residual bucket started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    joined_rows, signature_text, bucket_text = build_joined_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )
    bridge_rows, _selected_events, _sig2, _bucket2 = translate_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )
    bridge_by_source = {row.source_name: row for row in bridge_rows}

    residual_rows: list[dict[str, object]] = []
    for row in joined_rows:
        source_name = str(row["source_name"])
        bridge = bridge_by_source[source_name]
        if bridge.center_spine_pair >= args.spine_threshold:
            residual_rows.append(row)

    residual_rows.sort(key=lambda row: str(row["source_name"]))

    add4_rules = evaluate_rules(
        residual_rows,
        target_subtype=args.right_subtype,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    add1_rules = evaluate_rules(
        residual_rows,
        target_subtype=args.left_subtype,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    add4_count = sum(1 for row in residual_rows if row["subtype"] == args.right_subtype)
    add1_count = sum(1 for row in residual_rows if row["subtype"] == args.left_subtype)

    print()
    print("Center-Spine Residual Bucket")
    print("============================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print(f"spine_threshold={args.spine_threshold:.3f}")
    print(f"residual_rows={len(residual_rows)} add1_rows={add1_count} add4_rows={add4_count}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(render_bucket(residual_rows, target_subtype=args.right_subtype))
    print()
    print(render_rules(f"Best residual rules for {args.right_subtype}", add4_rules))
    print()
    print(render_rules(f"Best residual rules for {args.left_subtype}", add1_rules))
    print()
    print(
        "center-spine residual bucket completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
