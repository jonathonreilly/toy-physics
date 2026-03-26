#!/usr/bin/env python3
"""Probe local/topological observables inside the dominant low-overlap mixed bucket."""

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

from pocket_wrap_suppressor_low_overlap_residual_buckets import (  # noqa: E402
    best_signature,
    render_buckets,
    render_signature,
    select_visible_predicates,
)
from pocket_wrap_suppressor_low_overlap_combined_axes import (  # noqa: E402
    build_rows,
    candidate_predicates as combined_candidate_predicates,
)
from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from toy_event_physics import node_local_motif_profiles  # noqa: E402


@dataclass(frozen=True)
class LocalMotifBucketRow:
    source_name: str
    subtype: str
    pocket_adjacent_fraction: float
    deep_pocket_adjacent_fraction: float
    low_degree_neighbor_fraction: float
    boundary_deficit_mean: float
    mean_neighbor_degree_mean: float
    boundary_node_fraction: float
    boundary_pocket_fraction: float
    boundary_deep_fraction: float
    boundary_low_degree_fraction: float
    boundary_mean_neighbor_degree: float
    pocket_low_overlap_fraction: float
    deep_low_overlap_fraction: float
    boundary_pocket_low_fraction: float


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


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def build_mixed_bucket_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
) -> tuple[tuple[str, ...], list[LocalMotifBucketRow], str, str]:
    combined_rows = [
        row
        for row in build_rows(log_path)
        if row.subtype in {left_subtype, right_subtype}
    ]
    predicates = combined_candidate_predicates(combined_rows)
    selected_predicates = select_visible_predicates(predicates, limit=candidate_limit)
    signature = best_signature(combined_rows, selected_predicates, terms=signature_terms)
    mixed_buckets = [bucket for bucket in signature.buckets if len(bucket.counts) > 1]
    hardest = max(mixed_buckets, key=lambda bucket: (len(bucket.rows), sorted(bucket.counts.items())))
    source_names = tuple(sorted(row.source_name for row in hardest.rows))

    full_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(log_path)
        if row.subtype in {left_subtype, right_subtype}
    }
    motif_rows: list[LocalMotifBucketRow] = []
    for source_name in source_names:
        base_row = full_rows[source_name]
        profiles = node_local_motif_profiles(set(base_row.nodes), wrap_y=False)
        values = list(profiles.values())
        boundary_values = [item for item in values if item["boundary_deficit"] > 0.0]
        motif_rows.append(
            LocalMotifBucketRow(
                source_name=source_name,
                subtype=base_row.subtype,
                pocket_adjacent_fraction=_mean([item["pocket_adjacent"] for item in values]),
                deep_pocket_adjacent_fraction=_mean([item["deep_pocket_adjacent"] for item in values]),
                low_degree_neighbor_fraction=_mean([item["low_degree_neighbor"] for item in values]),
                boundary_deficit_mean=_mean([item["boundary_deficit"] for item in values]),
                mean_neighbor_degree_mean=_mean([item["mean_neighbor_degree"] for item in values]),
                boundary_node_fraction=len(boundary_values) / len(values) if values else 0.0,
                boundary_pocket_fraction=_mean([item["pocket_adjacent"] for item in boundary_values]),
                boundary_deep_fraction=_mean([item["deep_pocket_adjacent"] for item in boundary_values]),
                boundary_low_degree_fraction=_mean([item["low_degree_neighbor"] for item in boundary_values]),
                boundary_mean_neighbor_degree=_mean([item["mean_neighbor_degree"] for item in boundary_values]),
                pocket_low_overlap_fraction=_mean(
                    [item["pocket_adjacent"] * item["low_degree_neighbor"] for item in values]
                ),
                deep_low_overlap_fraction=_mean(
                    [item["deep_pocket_adjacent"] * item["low_degree_neighbor"] for item in values]
                ),
                boundary_pocket_low_fraction=_mean(
                    [item["pocket_adjacent"] * item["low_degree_neighbor"] for item in boundary_values]
                ),
            )
        )
    motif_rows.sort(key=lambda row: row.source_name)
    return source_names, motif_rows, render_signature(signature), render_buckets(signature)


def candidate_predicates(rows: list[LocalMotifBucketRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_defs = (
        ("pocket_adjacent_fraction", lambda row: row.pocket_adjacent_fraction),
        ("deep_pocket_adjacent_fraction", lambda row: row.deep_pocket_adjacent_fraction),
        ("low_degree_neighbor_fraction", lambda row: row.low_degree_neighbor_fraction),
        ("boundary_deficit_mean", lambda row: row.boundary_deficit_mean),
        ("mean_neighbor_degree_mean", lambda row: row.mean_neighbor_degree_mean),
        ("boundary_node_fraction", lambda row: row.boundary_node_fraction),
        ("boundary_pocket_fraction", lambda row: row.boundary_pocket_fraction),
        ("boundary_deep_fraction", lambda row: row.boundary_deep_fraction),
        ("boundary_low_degree_fraction", lambda row: row.boundary_low_degree_fraction),
        ("boundary_mean_neighbor_degree", lambda row: row.boundary_mean_neighbor_degree),
        ("pocket_low_overlap_fraction", lambda row: row.pocket_low_overlap_fraction),
        ("deep_low_overlap_fraction", lambda row: row.deep_low_overlap_fraction),
        ("boundary_pocket_low_fraction", lambda row: row.boundary_pocket_low_fraction),
    )
    preferred_order = {
        "boundary_deep_fraction": 0,
        "boundary_pocket_fraction": 1,
        "boundary_low_degree_fraction": 2,
        "boundary_mean_neighbor_degree": 3,
        "boundary_deficit_mean": 4,
        "pocket_adjacent_fraction": 5,
        "deep_pocket_adjacent_fraction": 6,
        "low_degree_neighbor_fraction": 7,
        "pocket_low_overlap_fraction": 8,
        "deep_low_overlap_fraction": 9,
        "boundary_pocket_low_fraction": 10,
        "boundary_node_fraction": 11,
        "mean_neighbor_degree_mean": 12,
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

    predicates = [(text, mask) for mask, (_sort_key, text) in predicate_masks.items()]
    predicates.sort(key=lambda item: item[0])
    return predicates


def best_rule_for_target(
    rows: list[LocalMotifBucketRow],
    target_subtype: str,
    *,
    max_terms: int,
) -> RuleRow | None:
    if not rows:
        return None
    predicates = candidate_predicates(rows)
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row.subtype == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    best: RuleRow | None = None
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
            candidate = RuleRow(
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


def render_bucket_summary(rows: list[LocalMotifBucketRow]) -> str:
    lines = [
        "Mixed Bucket Motif Envelopes",
        "===========================",
        "subtype | cases | padj~ | dpadj~ | lowN~ | bpadj~ | bdpadj~ | blowN~ | bp+low~ | bmeanN~",
        "--------+-------+-------+--------+-------+--------+---------+--------+---------+--------",
    ]
    for subtype in sorted({row.subtype for row in rows}):
        bucket = [row for row in rows if row.subtype == subtype]
        lines.append(
            f"{subtype:<19.19} | {len(bucket):>5} | "
            f"{statistics.median(row.pocket_adjacent_fraction for row in bucket):>5.3f} | "
            f"{statistics.median(row.deep_pocket_adjacent_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.low_degree_neighbor_fraction for row in bucket):>5.3f} | "
            f"{statistics.median(row.boundary_pocket_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.boundary_deep_fraction for row in bucket):>7.3f} | "
            f"{statistics.median(row.boundary_low_degree_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.boundary_pocket_low_fraction for row in bucket):>7.3f} | "
            f"{statistics.median(row.boundary_mean_neighbor_degree for row in bucket):>6.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap local motif bucket started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    source_names, motif_rows, signature_text, bucket_text = build_mixed_bucket_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
    )
    del source_names
    add1_rule = best_rule_for_target(motif_rows, args.left_subtype, max_terms=args.max_local_terms)
    add4_rule = best_rule_for_target(motif_rows, args.right_subtype, max_terms=args.max_local_terms)

    print()
    print("Low-Overlap Local Motif Bucket")
    print("==============================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(render_bucket_summary(motif_rows))
    print()
    if add1_rule is not None:
        print(
            f"local_motif_best[{args.left_subtype}]: exact={'Y' if add1_rule.exact else 'n'} "
            f"correct={add1_rule.correct}/{add1_rule.total} tp/fp/fn={add1_rule.tp}/{add1_rule.fp}/{add1_rule.fn} "
            f"rule={add1_rule.rule_text}"
        )
    if add4_rule is not None:
        print(
            f"local_motif_best[{args.right_subtype}]: exact={'Y' if add4_rule.exact else 'n'} "
            f"correct={add4_rule.correct}/{add4_rule.total} tp/fp/fn={add4_rule.tp}/{add4_rule.fp}/{add4_rule.fn} "
            f"rule={add4_rule.rule_text}"
        )
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap local motif bucket completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
