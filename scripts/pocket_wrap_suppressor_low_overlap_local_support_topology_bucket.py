#!/usr/bin/env python3
"""Probe support/candidate-topology observables inside the hard low-overlap mixed bucket."""

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
from pocket_wrap_suppressor_low_overlap_local_motif_bucket import (  # noqa: E402
    build_mixed_bucket_rows,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


@dataclass(frozen=True)
class SupportTopologyRow:
    source_name: str
    subtype: str
    pocket_cell_fraction: float
    deep_pocket_cell_fraction: float
    pocket_neighbor_overlap_fraction: float
    deep_neighbor_overlap_fraction: float
    pocket_neighbor_support_mean: float
    deep_neighbor_support_mean: float
    pocket_boundary_neighbor_fraction: float
    deep_boundary_neighbor_fraction: float
    pocket_mirror_candidate_fraction: float
    pocket_mirror_occupied_fraction: float
    pocket_mirror_void_fraction: float
    pocket_mirror_imbalance: float
    deep_mirror_candidate_fraction: float
    deep_mirror_occupied_fraction: float
    deep_mirror_void_fraction: float
    deep_mirror_imbalance: float


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


def _mirror_x(cell: tuple[int, int], min_x: int, max_x: int) -> tuple[int, int]:
    x, y = cell
    return (min_x + max_x - x, y)


def _mirror_fractions(
    candidates: set[tuple[int, int]],
    all_candidates: set[tuple[int, int]],
    nodes: set[tuple[int, int]],
    min_x: int,
    max_x: int,
) -> tuple[float, float, float, float]:
    if not candidates:
        return 0.0, 0.0, 0.0, 0.0

    mirror_candidate = 0
    mirror_occupied = 0
    mirror_void = 0
    left_count = 0
    right_count = 0
    center_x = (min_x + max_x) / 2.0

    for candidate in candidates:
        if candidate[0] < center_x:
            left_count += 1
        elif candidate[0] > center_x:
            right_count += 1
        mirror = _mirror_x(candidate, min_x, max_x)
        if mirror in all_candidates:
            mirror_candidate += 1
        elif mirror in nodes:
            mirror_occupied += 1
        else:
            mirror_void += 1

    total = float(len(candidates))
    balance_total = max(left_count + right_count, 1)
    return (
        mirror_candidate / total,
        mirror_occupied / total,
        mirror_void / total,
        abs(left_count - right_count) / balance_total,
    )


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
) -> tuple[list[SupportTopologyRow], str, str]:
    source_names, _motif_rows, signature_text, bucket_text = build_mixed_bucket_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
    )

    full_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(log_path)
        if row.subtype in {left_subtype, right_subtype}
    }

    rows: list[SupportTopologyRow] = []
    for source_name in source_names:
        base = full_rows[source_name]
        nodes = set(base.nodes)
        if not nodes:
            continue
        pocket_cells, deep_pocket_cells = pocket_candidate_cells(nodes, wrap_y=False)
        all_candidates = pocket_cells | deep_pocket_cells

        pocket_neighbor_nodes: set[tuple[int, int]] = set()
        deep_neighbor_nodes: set[tuple[int, int]] = set()
        for cell in pocket_cells:
            pocket_neighbor_nodes.update(graph_neighbors(cell, nodes | {cell}, wrap_y=False))
        for cell in deep_pocket_cells:
            deep_neighbor_nodes.update(graph_neighbors(cell, nodes | {cell}, wrap_y=False))

        min_x = min(x for x, _y in nodes)
        max_x = max(x for x, _y in nodes)

        pocket_neighbor_counts = [
            len(graph_neighbors(cell, nodes | {cell}, wrap_y=False)) / 8.0
            for cell in pocket_cells
        ]
        deep_neighbor_counts = [
            len(graph_neighbors(cell, nodes | {cell}, wrap_y=False)) / 8.0
            for cell in deep_pocket_cells
        ]

        boundary_nodes = {
            node
            for node in nodes
            if len(graph_neighbors(node, nodes, wrap_y=False)) < 8
        }

        (
            pocket_mirror_candidate_fraction,
            pocket_mirror_occupied_fraction,
            pocket_mirror_void_fraction,
            pocket_mirror_imbalance,
        ) = _mirror_fractions(pocket_cells, all_candidates, nodes, min_x, max_x)
        (
            deep_mirror_candidate_fraction,
            deep_mirror_occupied_fraction,
            deep_mirror_void_fraction,
            deep_mirror_imbalance,
        ) = _mirror_fractions(deep_pocket_cells, all_candidates, nodes, min_x, max_x)

        total_nodes = float(len(nodes))
        rows.append(
            SupportTopologyRow(
                source_name=source_name,
                subtype=base.subtype,
                pocket_cell_fraction=len(pocket_cells) / total_nodes,
                deep_pocket_cell_fraction=len(deep_pocket_cells) / total_nodes,
                pocket_neighbor_overlap_fraction=len(pocket_neighbor_nodes) / total_nodes,
                deep_neighbor_overlap_fraction=len(deep_neighbor_nodes) / total_nodes,
                pocket_neighbor_support_mean=_mean(pocket_neighbor_counts),
                deep_neighbor_support_mean=_mean(deep_neighbor_counts),
                pocket_boundary_neighbor_fraction=(
                    len(pocket_neighbor_nodes & boundary_nodes) / len(boundary_nodes)
                    if boundary_nodes
                    else 0.0
                ),
                deep_boundary_neighbor_fraction=(
                    len(deep_neighbor_nodes & boundary_nodes) / len(boundary_nodes)
                    if boundary_nodes
                    else 0.0
                ),
                pocket_mirror_candidate_fraction=pocket_mirror_candidate_fraction,
                pocket_mirror_occupied_fraction=pocket_mirror_occupied_fraction,
                pocket_mirror_void_fraction=pocket_mirror_void_fraction,
                pocket_mirror_imbalance=pocket_mirror_imbalance,
                deep_mirror_candidate_fraction=deep_mirror_candidate_fraction,
                deep_mirror_occupied_fraction=deep_mirror_occupied_fraction,
                deep_mirror_void_fraction=deep_mirror_void_fraction,
                deep_mirror_imbalance=deep_mirror_imbalance,
            )
        )

    rows.sort(key=lambda row: row.source_name)
    return rows, signature_text, bucket_text


def candidate_predicates(rows: list[SupportTopologyRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_defs = (
        ("pocket_cell_fraction", lambda row: row.pocket_cell_fraction),
        ("deep_pocket_cell_fraction", lambda row: row.deep_pocket_cell_fraction),
        ("pocket_neighbor_overlap_fraction", lambda row: row.pocket_neighbor_overlap_fraction),
        ("deep_neighbor_overlap_fraction", lambda row: row.deep_neighbor_overlap_fraction),
        ("pocket_neighbor_support_mean", lambda row: row.pocket_neighbor_support_mean),
        ("deep_neighbor_support_mean", lambda row: row.deep_neighbor_support_mean),
        ("pocket_boundary_neighbor_fraction", lambda row: row.pocket_boundary_neighbor_fraction),
        ("deep_boundary_neighbor_fraction", lambda row: row.deep_boundary_neighbor_fraction),
        ("pocket_mirror_candidate_fraction", lambda row: row.pocket_mirror_candidate_fraction),
        ("pocket_mirror_occupied_fraction", lambda row: row.pocket_mirror_occupied_fraction),
        ("pocket_mirror_void_fraction", lambda row: row.pocket_mirror_void_fraction),
        ("pocket_mirror_imbalance", lambda row: row.pocket_mirror_imbalance),
        ("deep_mirror_candidate_fraction", lambda row: row.deep_mirror_candidate_fraction),
        ("deep_mirror_occupied_fraction", lambda row: row.deep_mirror_occupied_fraction),
        ("deep_mirror_void_fraction", lambda row: row.deep_mirror_void_fraction),
        ("deep_mirror_imbalance", lambda row: row.deep_mirror_imbalance),
    )
    preferred_order = {
        "deep_pocket_cell_fraction": 0,
        "deep_neighbor_overlap_fraction": 1,
        "deep_neighbor_support_mean": 2,
        "deep_boundary_neighbor_fraction": 3,
        "pocket_cell_fraction": 4,
        "pocket_neighbor_overlap_fraction": 5,
        "pocket_neighbor_support_mean": 6,
        "pocket_boundary_neighbor_fraction": 7,
        "deep_mirror_candidate_fraction": 8,
        "deep_mirror_occupied_fraction": 9,
        "deep_mirror_void_fraction": 10,
        "deep_mirror_imbalance": 11,
        "pocket_mirror_candidate_fraction": 12,
        "pocket_mirror_occupied_fraction": 13,
        "pocket_mirror_void_fraction": 14,
        "pocket_mirror_imbalance": 15,
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
    rows: list[SupportTopologyRow],
    target_subtype: str,
    *,
    max_terms: int,
) -> RuleRow | None:
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
                (
                    not candidate.exact,
                    -candidate.correct,
                    candidate.term_count,
                    candidate.fp + candidate.fn,
                    candidate.rule_text,
                )
                < (
                    not best.exact,
                    -best.correct,
                    best.term_count,
                    best.fp + best.fn,
                    best.rule_text,
                )
            ):
                best = candidate
    return best


def render_bucket_summary(rows: list[SupportTopologyRow]) -> str:
    lines = [
        "Mixed Bucket Support/Topology Envelopes",
        "=======================================",
        "subtype | cases | pcell~ | dcell~ | povlp~ | dovlp~ | pbound~ | dbound~ | pmocc~ | dmocc~",
        "--------+-------+--------+--------+--------+--------+---------+---------+--------+-------",
    ]
    for subtype in sorted({row.subtype for row in rows}):
        bucket = [row for row in rows if row.subtype == subtype]
        lines.append(
            f"{subtype:<19.19} | {len(bucket):>5} | "
            f"{statistics.median(row.pocket_cell_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.deep_pocket_cell_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.pocket_neighbor_overlap_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.deep_neighbor_overlap_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.pocket_boundary_neighbor_fraction for row in bucket):>7.3f} | "
            f"{statistics.median(row.deep_boundary_neighbor_fraction for row in bucket):>7.3f} | "
            f"{statistics.median(row.pocket_mirror_occupied_fraction for row in bucket):>6.3f} | "
            f"{statistics.median(row.deep_mirror_occupied_fraction for row in bucket):>5.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap local support-topology bucket started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
    )
    add1_rule = best_rule_for_target(rows, args.left_subtype, max_terms=args.max_local_terms)
    add4_rule = best_rule_for_target(rows, args.right_subtype, max_terms=args.max_local_terms)

    print()
    print("Low-Overlap Local Support Topology Bucket")
    print("=========================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(render_bucket_summary(rows))
    print()
    if add1_rule is not None:
        print(
            f"local_support_topology_best[{args.left_subtype}]: exact={'Y' if add1_rule.exact else 'n'} "
            f"correct={add1_rule.correct}/{add1_rule.total} tp/fp/fn={add1_rule.tp}/{add1_rule.fp}/{add1_rule.fn} "
            f"rule={add1_rule.rule_text}"
        )
    if add4_rule is not None:
        print(
            f"local_support_topology_best[{args.right_subtype}]: exact={'Y' if add4_rule.exact else 'n'} "
            f"correct={add4_rule.correct}/{add4_rule.total} tp/fp/fn={add4_rule.tp}/{add4_rule.fp}/{add4_rule.fn} "
            f"rule={add4_rule.rule_text}"
        )
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap local support-topology bucket completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
