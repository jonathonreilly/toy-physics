#!/usr/bin/env python3
"""Probe candidate-support subgraph features inside the hard low-overlap mixed bucket."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass, fields, make_dataclass
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
    parser.add_argument("--event-limit", type=int, default=18)
    parser.add_argument("--max-local-terms", type=int, default=3)
    return parser


def _fraction(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


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


def _event_name(node: tuple[int, int], min_x: int, min_y: int, prefix: str) -> str:
    return f"{prefix}:dx{node[0] - min_x}:dy{node[1] - min_y}"


def _sanitize_event_name(event_name: str) -> str:
    return (
        event_name.replace(":", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
    )


def _candidate_row_type(selected_events: tuple[str, ...]):
    base_fields = [
        ("source_name", str),
        ("subtype", str),
        ("pocket_candidate_fraction", float),
        ("deep_candidate_fraction", float),
        ("bridge_support_fraction", float),
        ("bridge_support_left_fraction", float),
        ("bridge_support_right_fraction", float),
        ("bridge_lobe_imbalance", float),
        ("pocket_only_support_fraction", float),
        ("deep_only_support_fraction", float),
        ("bridge_component_count", float),
        ("bridge_largest_component_fraction", float),
        ("bridge_support_edge_density", float),
        ("candidate_cross_lobe_fraction", float),
        ("candidate_cross_family_fraction", float),
        ("bridge_event_present_count", float),
    ]
    event_fields = [(_sanitize_event_name(event_name), float) for event_name in selected_events]
    return make_dataclass(
        "CandidateSupportSubgraphExpandedRow",
        base_fields + event_fields,
        frozen=True,
    )


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
    event_limit: int,
) -> tuple[list[object], tuple[str, ...], str, str]:
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

    raw_rows: list[tuple[str, str, dict[str, float], set[str]]] = []
    event_counts: dict[str, set[str]] = defaultdict(set)

    for source_name in source_names:
        base = full_rows[source_name]
        nodes = set(base.nodes)
        if not nodes:
            continue

        pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
        all_candidates = pocket_cells | deep_cells
        if not all_candidates:
            continue

        min_x = min(x for x, _y in nodes)
        max_x = max(x for x, _y in nodes)
        min_y = min(y for _x, y in nodes)
        center_x = (min_x + max_x) / 2.0

        bridge_support_nodes: set[tuple[int, int]] = set()
        pocket_only_nodes: set[tuple[int, int]] = set()
        deep_only_nodes: set[tuple[int, int]] = set()
        bridge_events: set[str] = set()

        for node in nodes:
            neighbors = set(graph_neighbors(node, nodes | all_candidates, wrap_y=False))
            touches_pocket = bool(neighbors & pocket_cells)
            touches_deep = bool(neighbors & deep_cells)
            if touches_pocket and touches_deep:
                bridge_support_nodes.add(node)
                bridge_events.add(_event_name(node, min_x, min_y, "bridge_node"))
            elif touches_pocket:
                pocket_only_nodes.add(node)
            elif touches_deep:
                deep_only_nodes.add(node)

        for event_name in bridge_events:
            event_counts[event_name].add(base.subtype)

        bridge_components = _component_sizes(bridge_support_nodes)
        bridge_largest = bridge_components[0] if bridge_components else 0

        bridge_edge_count = 0
        for node in bridge_support_nodes:
            bridge_edge_count += len(_neighbor_cells(node) & bridge_support_nodes)

        candidate_cross_lobe_edges = 0
        candidate_total_edges = 0
        for cell in all_candidates:
            for neighbor in _neighbor_cells(cell):
                if neighbor in all_candidates:
                    candidate_total_edges += 1
                    if (cell[0] < center_x and neighbor[0] > center_x) or (
                        cell[0] > center_x and neighbor[0] < center_x
                    ):
                        candidate_cross_lobe_edges += 1

        cross_family_edges = 0
        for cell in pocket_cells:
            for neighbor in _neighbor_cells(cell):
                if neighbor in deep_cells:
                    cross_family_edges += 1

        bridge_left = sum(node[0] < center_x for node in bridge_support_nodes)
        bridge_right = sum(node[0] > center_x for node in bridge_support_nodes)

        total_nodes = len(nodes)
        numeric = {
            "pocket_candidate_fraction": _fraction(len(pocket_cells), total_nodes),
            "deep_candidate_fraction": _fraction(len(deep_cells), total_nodes),
            "bridge_support_fraction": _fraction(len(bridge_support_nodes), total_nodes),
            "bridge_support_left_fraction": _fraction(bridge_left, len(bridge_support_nodes)),
            "bridge_support_right_fraction": _fraction(bridge_right, len(bridge_support_nodes)),
            "bridge_lobe_imbalance": _fraction(
                abs(bridge_left - bridge_right),
                max(bridge_left + bridge_right, 1),
            ),
            "pocket_only_support_fraction": _fraction(len(pocket_only_nodes), total_nodes),
            "deep_only_support_fraction": _fraction(len(deep_only_nodes), total_nodes),
            "bridge_component_count": float(len(bridge_components)),
            "bridge_largest_component_fraction": _fraction(bridge_largest, len(bridge_support_nodes)),
            "bridge_support_edge_density": _fraction(bridge_edge_count, max(8 * len(bridge_support_nodes), 1)),
            "candidate_cross_lobe_fraction": _fraction(candidate_cross_lobe_edges, candidate_total_edges),
            "candidate_cross_family_fraction": _fraction(cross_family_edges, max(candidate_total_edges, 1)),
        }
        raw_rows.append((source_name, base.subtype, numeric, bridge_events))

    event_scores: list[tuple[tuple[int, str], str]] = []
    for event_name, labels in event_counts.items():
        if len(labels) < 2:
            continue
        support = sum(event_name in row_events for *_prefix, row_events in raw_rows)
        event_scores.append(((-support, event_name), event_name))
    event_scores.sort(key=lambda item: item[0])
    selected_events = tuple(item[1] for item in event_scores[:event_limit])

    row_cls = _candidate_row_type(selected_events)
    rows: list[object] = []
    for source_name, subtype, numeric, bridge_events in raw_rows:
        row_values = {
            "source_name": source_name,
            "subtype": subtype,
            **numeric,
            "bridge_event_present_count": float(
                sum(event in bridge_events for event in selected_events)
            ),
        }
        for event_name in selected_events:
            row_values[_sanitize_event_name(event_name)] = float(event_name in bridge_events)
        rows.append(row_cls(**row_values))

    rows.sort(key=lambda row: getattr(row, "source_name"))
    return rows, selected_events, signature_text, bucket_text


def candidate_predicates(rows: list[object]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_names = [
        field.name
        for field in fields(type(rows[0]))
        if field.name not in {"source_name", "subtype"}
    ]
    preferred_order = {name: index for index, name in enumerate(feature_names)}
    predicate_masks: dict[int, tuple[tuple[int, str, float], str]] = {}
    full_mask = (1 << len(rows)) - 1

    for feature_name in feature_names:
        value_to_labels: dict[float, set[str]] = {}
        for row in rows:
            value = float(getattr(row, feature_name))
            value_to_labels.setdefault(value, set()).add(getattr(row, "subtype"))
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
                    value = float(getattr(row, feature_name))
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


def best_rule_for_target(rows: list[object], target_subtype: str, *, max_terms: int) -> RuleRow | None:
    predicates = candidate_predicates(rows)
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if getattr(row, "subtype") == target_subtype:
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
    print(f"low-overlap candidate-support subgraph bucket started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, selected_events, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )

    left_rule = best_rule_for_target(rows, args.left_subtype, max_terms=args.max_local_terms)
    right_rule = best_rule_for_target(rows, args.right_subtype, max_terms=args.max_local_terms)

    print()
    print("Low-Overlap Candidate-Support Subgraph Bucket")
    print("============================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    if left_rule is not None:
        print(
            f"candidate_support_subgraph_best[{args.left_subtype}]: exact={'Y' if left_rule.exact else 'n'} "
            f"correct={left_rule.correct}/{left_rule.total} tp/fp/fn={left_rule.tp}/{left_rule.fp}/{left_rule.fn} "
            f"rule={left_rule.rule_text}"
        )
    if right_rule is not None:
        print(
            f"candidate_support_subgraph_best[{args.right_subtype}]: exact={'Y' if right_rule.exact else 'n'} "
            f"correct={right_rule.correct}/{right_rule.total} tp/fp/fn={right_rule.tp}/{right_rule.fp}/{right_rule.fn} "
            f"rule={right_rule.rule_text}"
        )

    bridge_fracs = [float(getattr(row, "bridge_support_fraction")) for row in rows]
    pocket_only_fracs = [float(getattr(row, "pocket_only_support_fraction")) for row in rows]
    deep_only_fracs = [float(getattr(row, "deep_only_support_fraction")) for row in rows]
    if bridge_fracs:
        print()
        print(
            "support_contact_means: "
            f"bridge={statistics.mean(bridge_fracs):.3f} "
            f"pocket_only={statistics.mean(pocket_only_fracs):.3f} "
            f"deep_only={statistics.mean(deep_only_fracs):.3f}"
        )

    if selected_events:
        print()
        print("selected_bridge_events:")
        for event_name in selected_events:
            print(f"  - {event_name}")

    elapsed = time.time() - total_start
    print()
    print(
        "low-overlap candidate-support subgraph bucket completed "
        f"{datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
