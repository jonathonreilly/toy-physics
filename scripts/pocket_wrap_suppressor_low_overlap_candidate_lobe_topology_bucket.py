#!/usr/bin/env python3
"""Probe candidate-lobe / support-graph topology inside the hard low-overlap mixed bucket."""

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

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_local_motif_bucket import (  # noqa: E402
    build_mixed_bucket_rows,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


@dataclass(frozen=True)
class CandidateLobeRow:
    source_name: str
    subtype: str
    pocket_component_count: float
    deep_component_count: float
    all_component_count: float
    pocket_largest_component_fraction: float
    deep_largest_component_fraction: float
    all_largest_component_fraction: float
    pocket_left_component_count: float
    pocket_right_component_count: float
    deep_left_component_count: float
    deep_right_component_count: float
    lobe_component_imbalance: float
    side_occupancy_imbalance: float
    bridge_edge_density: float
    pocket_bridge_fraction: float
    deep_bridge_fraction: float
    support_bridge_fraction: float


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


def _neighbor_cells(cell: tuple[int, int]) -> set[tuple[int, int]]:
    x, y = cell
    return {
        (x + dx, y + dy)
        for dx in (-1, 0, 1)
        for dy in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    }


def _component_sizes(cells: set[tuple[int, int]]) -> list[int]:
    remaining = set(cells)
    sizes: list[int] = []
    while remaining:
        start = next(iter(remaining))
        stack = [start]
        remaining.remove(start)
        size = 0
        while stack:
            cell = stack.pop()
            size += 1
            for neighbor in _neighbor_cells(cell):
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    stack.append(neighbor)
        sizes.append(size)
    sizes.sort(reverse=True)
    return sizes


def _fraction(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def _bridge_edge_count(left_cells: set[tuple[int, int]], right_cells: set[tuple[int, int]]) -> int:
    count = 0
    for cell in left_cells:
        for neighbor in _neighbor_cells(cell):
            if neighbor in right_cells:
                count += 1
    return count


def _side_component_counts(cells: set[tuple[int, int]], center_x: float) -> tuple[int, int]:
    left = {cell for cell in cells if cell[0] < center_x}
    right = {cell for cell in cells if cell[0] > center_x}
    return len(_component_sizes(left)), len(_component_sizes(right))


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
) -> tuple[list[CandidateLobeRow], str, str]:
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

    rows: list[CandidateLobeRow] = []
    for source_name in source_names:
        base = full_rows[source_name]
        nodes = set(base.nodes)
        if not nodes:
            continue

        pocket_cells, deep_pocket_cells = pocket_candidate_cells(nodes, wrap_y=False)
        all_candidates = pocket_cells | deep_pocket_cells
        if not all_candidates:
            continue

        min_x = min(x for x, _y in nodes)
        max_x = max(x for x, _y in nodes)
        center_x = (min_x + max_x) / 2.0

        pocket_sizes = _component_sizes(pocket_cells)
        deep_sizes = _component_sizes(deep_pocket_cells)
        all_sizes = _component_sizes(all_candidates)

        pocket_left_components, pocket_right_components = _side_component_counts(pocket_cells, center_x)
        deep_left_components, deep_right_components = _side_component_counts(deep_pocket_cells, center_x)

        pocket_side_count = sum(cell[0] < center_x for cell in pocket_cells) + sum(
            cell[0] > center_x for cell in pocket_cells
        )
        deep_side_count = sum(cell[0] < center_x for cell in deep_pocket_cells) + sum(
            cell[0] > center_x for cell in deep_pocket_cells
        )

        pocket_left_count = sum(cell[0] < center_x for cell in pocket_cells)
        pocket_right_count = sum(cell[0] > center_x for cell in pocket_cells)
        deep_left_count = sum(cell[0] < center_x for cell in deep_pocket_cells)
        deep_right_count = sum(cell[0] > center_x for cell in deep_pocket_cells)

        bridge_edges = _bridge_edge_count(pocket_cells, deep_pocket_cells)
        pocket_total_edges = _bridge_edge_count(pocket_cells, pocket_cells) + bridge_edges
        deep_total_edges = _bridge_edge_count(deep_pocket_cells, deep_pocket_cells) + bridge_edges

        support_bridge_nodes = 0
        for node in nodes:
            neighbors = set(graph_neighbors(node, nodes | all_candidates, wrap_y=False))
            touches_pocket = bool(neighbors & pocket_cells)
            touches_deep = bool(neighbors & deep_pocket_cells)
            if touches_pocket and touches_deep:
                support_bridge_nodes += 1

        total_components = (
            pocket_left_components
            + pocket_right_components
            + deep_left_components
            + deep_right_components
        )
        left_components = pocket_left_components + deep_left_components
        right_components = pocket_right_components + deep_right_components

        rows.append(
            CandidateLobeRow(
                source_name=source_name,
                subtype=base.subtype,
                pocket_component_count=float(len(pocket_sizes)),
                deep_component_count=float(len(deep_sizes)),
                all_component_count=float(len(all_sizes)),
                pocket_largest_component_fraction=_fraction(
                    pocket_sizes[0] if pocket_sizes else 0,
                    len(pocket_cells),
                ),
                deep_largest_component_fraction=_fraction(
                    deep_sizes[0] if deep_sizes else 0,
                    len(deep_pocket_cells),
                ),
                all_largest_component_fraction=_fraction(
                    all_sizes[0] if all_sizes else 0,
                    len(all_candidates),
                ),
                pocket_left_component_count=float(pocket_left_components),
                pocket_right_component_count=float(pocket_right_components),
                deep_left_component_count=float(deep_left_components),
                deep_right_component_count=float(deep_right_components),
                lobe_component_imbalance=_fraction(abs(left_components - right_components), total_components),
                side_occupancy_imbalance=_fraction(
                    abs((pocket_left_count + deep_left_count) - (pocket_right_count + deep_right_count)),
                    pocket_side_count + deep_side_count,
                ),
                bridge_edge_density=_fraction(
                    bridge_edges,
                    pocket_total_edges + deep_total_edges,
                ),
                pocket_bridge_fraction=_fraction(bridge_edges, pocket_total_edges),
                deep_bridge_fraction=_fraction(bridge_edges, deep_total_edges),
                support_bridge_fraction=_fraction(support_bridge_nodes, len(nodes)),
            )
        )

    rows.sort(key=lambda row: row.source_name)
    return rows, signature_text, bucket_text


def candidate_predicates(rows: list[CandidateLobeRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_defs = (
        ("pocket_component_count", lambda row: row.pocket_component_count),
        ("deep_component_count", lambda row: row.deep_component_count),
        ("all_component_count", lambda row: row.all_component_count),
        ("pocket_largest_component_fraction", lambda row: row.pocket_largest_component_fraction),
        ("deep_largest_component_fraction", lambda row: row.deep_largest_component_fraction),
        ("all_largest_component_fraction", lambda row: row.all_largest_component_fraction),
        ("pocket_left_component_count", lambda row: row.pocket_left_component_count),
        ("pocket_right_component_count", lambda row: row.pocket_right_component_count),
        ("deep_left_component_count", lambda row: row.deep_left_component_count),
        ("deep_right_component_count", lambda row: row.deep_right_component_count),
        ("lobe_component_imbalance", lambda row: row.lobe_component_imbalance),
        ("side_occupancy_imbalance", lambda row: row.side_occupancy_imbalance),
        ("bridge_edge_density", lambda row: row.bridge_edge_density),
        ("pocket_bridge_fraction", lambda row: row.pocket_bridge_fraction),
        ("deep_bridge_fraction", lambda row: row.deep_bridge_fraction),
        ("support_bridge_fraction", lambda row: row.support_bridge_fraction),
    )

    preferred_order = {
        "bridge_edge_density": 0,
        "pocket_bridge_fraction": 1,
        "deep_bridge_fraction": 2,
        "support_bridge_fraction": 3,
        "all_largest_component_fraction": 4,
        "all_component_count": 5,
        "pocket_largest_component_fraction": 6,
        "deep_largest_component_fraction": 7,
        "pocket_component_count": 8,
        "deep_component_count": 9,
        "side_occupancy_imbalance": 10,
        "lobe_component_imbalance": 11,
        "pocket_left_component_count": 12,
        "pocket_right_component_count": 13,
        "deep_left_component_count": 14,
        "deep_right_component_count": 15,
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
    rows: list[CandidateLobeRow],
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


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap candidate-lobe topology bucket started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
    )
    left_rule = best_rule_for_target(rows, args.left_subtype, max_terms=args.max_local_terms)
    right_rule = best_rule_for_target(rows, args.right_subtype, max_terms=args.max_local_terms)

    print()
    print("Low-Overlap Candidate-Lobe Topology Bucket")
    print("==========================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    if left_rule is not None:
        print(
            f"candidate_lobe_best[{args.left_subtype}]: exact={'Y' if left_rule.exact else 'n'} "
            f"correct={left_rule.correct}/{left_rule.total} tp/fp/fn={left_rule.tp}/{left_rule.fp}/{left_rule.fn} "
            f"rule={left_rule.rule_text}"
        )
    if right_rule is not None:
        print(
            f"candidate_lobe_best[{args.right_subtype}]: exact={'Y' if right_rule.exact else 'n'} "
            f"correct={right_rule.correct}/{right_rule.total} tp/fp/fn={right_rule.tp}/{right_rule.fp}/{right_rule.fn} "
            f"rule={right_rule.rule_text}"
        )

    pocket_bridge_values = [row.pocket_bridge_fraction for row in rows]
    deep_bridge_values = [row.deep_bridge_fraction for row in rows]
    support_bridge_values = [row.support_bridge_fraction for row in rows]
    if pocket_bridge_values:
        print()
        print(
            "bridge_means: "
            f"pocket={sum(pocket_bridge_values)/len(pocket_bridge_values):.3f} "
            f"deep={sum(deep_bridge_values)/len(deep_bridge_values):.3f} "
            f"support={sum(support_bridge_values)/len(support_bridge_values):.3f}"
        )

    elapsed = time.time() - total_start
    print()
    print(
        f"low-overlap candidate-lobe topology bucket completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
