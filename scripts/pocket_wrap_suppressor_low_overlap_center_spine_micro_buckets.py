#!/usr/bin/env python3
"""Decompose the central-bridge-spine residual into smaller add4-focused micro-buckets."""

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

from pocket_wrap_suppressor_low_overlap_bridge_event_translation import (  # noqa: E402
    translate_rows,
)
from pocket_wrap_suppressor_low_overlap_identity_lobe_support_joined_closure import (  # noqa: E402
    build_rows as build_joined_rows,
)


@dataclass(frozen=True)
class BucketSummary:
    key: tuple[bool, ...]
    counts: dict[str, int]
    rows: list[dict[str, object]]


@dataclass(frozen=True)
class SignatureResult:
    predicate_texts: tuple[str, ...]
    mixed_add4_row_count: int
    mixed_add4_bucket_count: int
    add4_bucket_count: int
    buckets: list[BucketSummary]


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
    parser.add_argument("--predicate-limit", type=int, default=16)
    parser.add_argument("--max-local-terms", type=int, default=3)
    return parser


def build_residual_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
    event_limit: int,
    spine_threshold: float,
) -> list[dict[str, object]]:
    joined_rows, _signature_text, _bucket_text = build_joined_rows(
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

    residual_rows: list[dict[str, object]] = []
    for row in joined_rows:
        bridge = bridge_by_source[str(row["source_name"])]
        if bridge.center_spine_pair < spine_threshold:
            continue
        residual_rows.append(row)
    residual_rows.sort(key=lambda row: str(row["source_name"]))
    return residual_rows


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


def select_predicates(
    rows: list[dict[str, object]],
    predicates: list[tuple[str, int]],
    *,
    target_subtype: str,
    limit: int,
) -> list[tuple[str, int]]:
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row["subtype"] == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    ranked: list[tuple[tuple[bool, int, int, str], tuple[str, int]]] = []
    for predicate_text, predicate_mask in predicates:
        tp = (predicate_mask & target_mask).bit_count()
        fp = (predicate_mask & non_target_mask).bit_count()
        fn = (target_mask & (full_mask ^ predicate_mask)).bit_count()
        correct = tp + ((non_target_mask & (full_mask ^ predicate_mask)).bit_count())
        ranked.append(
            (
                (fp != 0, -correct, fn, predicate_text),
                (predicate_text, predicate_mask),
            )
        )
    ranked.sort(key=lambda item: item[0])
    return [item[1] for item in ranked[:limit]]


def evaluate_signature(
    rows: list[dict[str, object]],
    predicates: list[tuple[str, int]],
    *,
    add4_subtype: str,
) -> SignatureResult:
    grouped: dict[tuple[bool, ...], list[dict[str, object]]] = {}
    for row_index, row in enumerate(rows):
        key = tuple(bool(mask & (1 << row_index)) for _text, mask in predicates)
        grouped.setdefault(key, []).append(row)

    mixed_add4_rows = 0
    mixed_add4_buckets = 0
    add4_bucket_count = 0
    bucket_summaries: list[BucketSummary] = []

    for key in sorted(grouped):
        bucket_rows = grouped[key]
        counts: dict[str, int] = {}
        for row in bucket_rows:
            subtype = str(row["subtype"])
            counts[subtype] = counts.get(subtype, 0) + 1
        if add4_subtype in counts:
            add4_bucket_count += 1
            if len(counts) > 1:
                mixed_add4_buckets += 1
                mixed_add4_rows += len(bucket_rows)
        bucket_summaries.append(BucketSummary(key=key, counts=counts, rows=bucket_rows))

    return SignatureResult(
        predicate_texts=tuple(text for text, _mask in predicates),
        mixed_add4_row_count=mixed_add4_rows,
        mixed_add4_bucket_count=mixed_add4_buckets,
        add4_bucket_count=add4_bucket_count,
        buckets=bucket_summaries,
    )


def best_signature(
    rows: list[dict[str, object]],
    predicates: list[tuple[str, int]],
    *,
    terms: int,
    add4_subtype: str,
) -> SignatureResult:
    best: SignatureResult | None = None
    for combo in itertools.combinations(predicates, terms):
        candidate = evaluate_signature(rows, list(combo), add4_subtype=add4_subtype)
        if best is None or (
            candidate.mixed_add4_row_count,
            candidate.mixed_add4_bucket_count,
            candidate.add4_bucket_count,
            candidate.predicate_texts,
        ) < (
            best.mixed_add4_row_count,
            best.mixed_add4_bucket_count,
            best.add4_bucket_count,
            best.predicate_texts,
        ):
            best = candidate
    if best is None:
        raise ValueError("no signature combinations evaluated")
    return best


def render_signature(result: SignatureResult) -> str:
    lines = [
        "Center-Spine Micro Signature",
        "============================",
    ]
    for index, text in enumerate(result.predicate_texts, start=1):
        lines.append(f"{index}. {text}")
    lines.append(f"mixed_add4_row_count={result.mixed_add4_row_count}")
    lines.append(f"mixed_add4_bucket_count={result.mixed_add4_bucket_count}")
    lines.append(f"add4_bucket_count={result.add4_bucket_count}")
    lines.append(f"bucket_count={len(result.buckets)}")
    return "\n".join(lines)


def render_buckets(result: SignatureResult) -> str:
    lines = [
        "Center-Spine Micro Buckets",
        "==========================",
        "bucket_key | rows | counts | state",
        "----------+------+--------+-------",
    ]
    for bucket in result.buckets:
        key_text = "".join("1" if value else "0" for value in bucket.key)
        counts_text = ", ".join(f"{name}:{count}" for name, count in sorted(bucket.counts.items()))
        if len(bucket.counts) == 1:
            state = "closed"
        elif "add4-sensitive" in bucket.counts:
            state = "mixed-add4"
        else:
            state = "mixed"
        lines.append(f"{key_text or '-':<9} | {len(bucket.rows):>4} | {counts_text:<24} | {state}")
    return "\n".join(lines)


def render_add4_buckets(result: SignatureResult) -> str:
    lines = [
        "Add4-Containing Buckets",
        "=======================",
    ]
    for bucket in result.buckets:
        if "add4-sensitive" not in bucket.counts:
            continue
        key_text = "".join("1" if value else "0" for value in bucket.key)
        lines.append(f"bucket_key={key_text} rows={len(bucket.rows)} counts={bucket.counts}")
        for row in bucket.rows:
            feats = row["features"]  # type: ignore[index]
            lines.append(
                f"  - {row['source_name']} | {row['subtype']} | "
                f"id_pocket_left={float(feats['identity_pocket_left_fraction']):.3f} | "
                f"id_deep_left={float(feats['identity_deep_left_fraction']):.3f} | "
                f"support_edge={float(feats['support_bridge_support_edge_density']):.3f} | "
                f"support_left={float(feats['support_bridge_support_left_fraction']):.3f} | "
                f"support_events={float(feats['support_bridge_event_present_count']):.3f}"
            )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine micro-buckets started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = build_residual_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
        spine_threshold=args.spine_threshold,
    )
    predicates = candidate_predicates(rows)
    selected = select_predicates(
        rows,
        predicates,
        target_subtype=args.right_subtype,
        limit=args.predicate_limit,
    )
    signature = best_signature(
        rows,
        selected,
        terms=args.signature_terms,
        add4_subtype=args.right_subtype,
    )

    print()
    print("Center-Spine Micro-Bucket Decomposition")
    print("=======================================")
    print(f"log={log_path}")
    print(f"rows={len(rows)} pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(render_signature(signature))
    print()
    print(render_buckets(signature))
    print()
    print(render_add4_buckets(signature))
    print()
    print(
        "center-spine micro-buckets completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
