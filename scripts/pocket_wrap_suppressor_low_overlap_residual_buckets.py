#!/usr/bin/env python3
"""Decompose low-overlap pair rows into small visible-signature residual buckets."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import re
import time

from pocket_wrap_suppressor_low_overlap_combined_axes import (
    CombinedRow,
    best_rule_for_target,
    build_rows,
    candidate_predicates,
)


@dataclass(frozen=True)
class BucketSummary:
    key: tuple[bool, ...]
    counts: dict[str, int]
    rows: list[CombinedRow]


@dataclass(frozen=True)
class SignatureResult:
    predicate_texts: tuple[str, ...]
    mixed_row_count: int
    mixed_bucket_count: int
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
    parser.add_argument("--max-local-terms", type=int, default=3)
    return parser


def _feature_name(predicate_text: str) -> str:
    if predicate_text.startswith("crosses_midline"):
        return "crosses_midline"
    match = re.match(r"([a-z_]+)\s+(<=|>=)\s+[-0-9.]+", predicate_text)
    return match.group(1) if match else predicate_text


def select_visible_predicates(
    predicates: list[tuple[str, int]],
    limit: int,
) -> list[tuple[str, int]]:
    preferred_order = {
        "core_low_degree_fraction": 0,
        "low_degree_gap": 1,
        "boundary_gap": 2,
        "core_boundary_deficit_mean": 3,
        "core_deep_fraction": 4,
        "deep_gap": 5,
        "pocket_gap": 6,
        "mirror_center_asymmetry": 7,
        "abs_half_center_diff": 8,
        "half_center_sum": 9,
        "half_span_diff": 10,
        "span_curvature": 11,
        "boundary_fraction": 12,
        "crosses_midline": 13,
    }
    ranked = sorted(
        predicates,
        key=lambda item: (
            preferred_order.get(_feature_name(item[0]), 99),
            item[0],
        ),
    )
    selected: list[tuple[str, int]] = []
    seen_features: set[str] = set()
    for text, mask in ranked:
        feature_name = _feature_name(text)
        if feature_name in seen_features:
            continue
        selected.append((text, mask))
        seen_features.add(feature_name)
        if len(selected) >= limit:
            break
    return selected


def evaluate_signature(
    rows: list[CombinedRow],
    predicates: list[tuple[str, int]],
) -> SignatureResult:
    grouped: dict[tuple[bool, ...], list[CombinedRow]] = {}
    for row_index, row in enumerate(rows):
        key = tuple(bool(mask & (1 << row_index)) for _text, mask in predicates)
        grouped.setdefault(key, []).append(row)

    bucket_summaries: list[BucketSummary] = []
    mixed_rows = 0
    mixed_buckets = 0
    for key in sorted(grouped):
        bucket_rows = grouped[key]
        counts: dict[str, int] = {}
        for row in bucket_rows:
            counts[row.subtype] = counts.get(row.subtype, 0) + 1
        if len(counts) > 1:
            mixed_buckets += 1
            mixed_rows += len(bucket_rows)
        bucket_summaries.append(BucketSummary(key=key, counts=counts, rows=bucket_rows))

    return SignatureResult(
        predicate_texts=tuple(text for text, _mask in predicates),
        mixed_row_count=mixed_rows,
        mixed_bucket_count=mixed_buckets,
        buckets=bucket_summaries,
    )


def best_signature(
    rows: list[CombinedRow],
    candidate_predicates_list: list[tuple[str, int]],
    terms: int,
) -> SignatureResult:
    best: SignatureResult | None = None
    for combo in itertools.combinations(candidate_predicates_list, terms):
        candidate = evaluate_signature(rows, list(combo))
        if best is None or (
            candidate.mixed_row_count,
            candidate.mixed_bucket_count,
            len(candidate.buckets),
            candidate.predicate_texts,
        ) < (
            best.mixed_row_count,
            best.mixed_bucket_count,
            len(best.buckets),
            best.predicate_texts,
        ):
            best = candidate
    if best is None:
        raise ValueError("no signature combinations could be evaluated")
    return best


def render_signature(result: SignatureResult) -> str:
    lines = [
        "Small Visible Signature",
        "=======================",
    ]
    for index, text in enumerate(result.predicate_texts, start=1):
        lines.append(f"{index}. {text}")
    lines.append(f"mixed_row_count={result.mixed_row_count}")
    lines.append(f"mixed_bucket_count={result.mixed_bucket_count}")
    lines.append(f"bucket_count={len(result.buckets)}")
    return "\n".join(lines)


def render_buckets(result: SignatureResult) -> str:
    lines = [
        "Residual Buckets",
        "================",
        "bucket_key | rows | counts | state",
        "----------+------+--------+-------",
    ]
    for bucket in result.buckets:
        key_text = "".join("1" if value else "0" for value in bucket.key)
        counts_text = ", ".join(f"{name}:{count}" for name, count in sorted(bucket.counts.items()))
        state = "mixed" if len(bucket.counts) > 1 else "closed"
        lines.append(f"{key_text or '-':<9} | {len(bucket.rows):>4} | {counts_text:<24} | {state}")
    return "\n".join(lines)


def render_hardest_bucket(
    result: SignatureResult,
    max_local_terms: int,
) -> str:
    mixed_buckets = [bucket for bucket in result.buckets if len(bucket.counts) > 1]
    if not mixed_buckets:
        return "All buckets are subtype-pure under this signature."

    hardest = max(mixed_buckets, key=lambda bucket: (len(bucket.rows), sorted(bucket.counts.items())))
    lines = [
        "Hardest Mixed Bucket",
        "====================",
        "signature_key=" + "".join("1" if value else "0" for value in hardest.key),
        "rows=" + str(len(hardest.rows)),
        "counts=" + ", ".join(
            f"{name}:{count}" for name, count in sorted(hardest.counts.items())
        ),
        "members=" + ", ".join(row.source_name for row in hardest.rows),
    ]

    for target in sorted(hardest.counts):
        local_best = best_rule_for_target(hardest.rows, target, max_terms=max_local_terms)
        if local_best is None:
            continue
        lines.append(
            f"local_best[{target}]: exact={'Y' if local_best.exact else 'n'} "
            f"correct={local_best.correct}/{local_best.total} "
            f"tp/fp/fn={local_best.tp}/{local_best.fp}/{local_best.fn} "
            f"rule={local_best.rule_text}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap residual buckets started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = [
        row
        for row in build_rows(log_path)
        if row.subtype in {args.left_subtype, args.right_subtype}
    ]
    if not rows:
        raise SystemExit("no rows for requested subtype pair")

    predicates = candidate_predicates(rows)
    selected_predicates = select_visible_predicates(predicates, limit=args.candidate_limit)
    if len(selected_predicates) < args.signature_terms:
        raise SystemExit(
            f"not enough predicates ({len(selected_predicates)}) for signature-terms={args.signature_terms}"
        )

    signature = best_signature(rows, selected_predicates, terms=args.signature_terms)

    print()
    print("Low-Overlap Residual Bucket Decomposition")
    print("=========================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print(f"rows={len(rows)}")
    print(f"candidate_predicates={len(predicates)}")
    print(f"selected_predicates={len(selected_predicates)}")
    print()
    print(render_signature(signature))
    print()
    print(render_buckets(signature))
    print()
    print(render_hardest_bucket(signature, max_local_terms=args.max_local_terms))
    print()
    elapsed = time.time() - total_start
    print(
        "low-overlap residual buckets completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
