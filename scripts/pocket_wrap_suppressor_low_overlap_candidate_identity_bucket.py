#!/usr/bin/env python3
"""Probe candidate-identity structure inside the hard low-overlap mixed bucket."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass, make_dataclass, fields
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
from toy_event_physics import pocket_candidate_cells  # noqa: E402


@dataclass(frozen=True)
class CandidateIdentityRow:
    source_name: str
    subtype: str
    pocket_left_fraction: float
    pocket_right_fraction: float
    deep_left_fraction: float
    deep_right_fraction: float
    pocket_x_span: float
    deep_x_span: float
    pocket_both_sides: float
    deep_both_sides: float
    pocket_mirror_occupied_left_fraction: float
    pocket_mirror_occupied_right_fraction: float
    deep_mirror_occupied_left_fraction: float
    deep_mirror_occupied_right_fraction: float
    pocket_mirror_void_left_fraction: float
    pocket_mirror_void_right_fraction: float
    deep_mirror_void_left_fraction: float
    deep_mirror_void_right_fraction: float
    event_present_count: float


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


def _mirror_x(cell: tuple[int, int], min_x: int, max_x: int) -> tuple[int, int]:
    x, y = cell
    return (min_x + max_x - x, y)


def _relative_event(cell: tuple[int, int], min_x: int, min_y: int, prefix: str) -> str:
    return f"{prefix}:dx{cell[0] - min_x}:dy{cell[1] - min_y}"


def _fraction(count: int, total: int) -> float:
    return count / total if total else 0.0


def _span(cells: set[tuple[int, int]]) -> float:
    if not cells:
        return 0.0
    xs = [cell[0] for cell in cells]
    return float(max(xs) - min(xs))


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
    event_limit: int,
) -> tuple[list[CandidateIdentityRow], tuple[str, ...], str, str]:
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
        pocket_cells, deep_pocket_cells = pocket_candidate_cells(nodes, wrap_y=False)
        if not nodes:
            continue
        min_x = min(x for x, _y in nodes)
        max_x = max(x for x, _y in nodes)
        min_y = min(y for _x, y in nodes)
        center_x = (min_x + max_x) / 2.0

        def side_counts(cells: set[tuple[int, int]]) -> tuple[int, int]:
            left = sum(cell[0] < center_x for cell in cells)
            right = sum(cell[0] > center_x for cell in cells)
            return left, right

        pocket_left, pocket_right = side_counts(pocket_cells)
        deep_left, deep_right = side_counts(deep_pocket_cells)

        event_names: set[str] = set()
        mirror_stats = {
            "pocket_occ_left": 0,
            "pocket_occ_right": 0,
            "pocket_void_left": 0,
            "pocket_void_right": 0,
            "deep_occ_left": 0,
            "deep_occ_right": 0,
            "deep_void_left": 0,
            "deep_void_right": 0,
        }

        for prefix, cells in (("pocket", pocket_cells), ("deep", deep_pocket_cells)):
            for cell in cells:
                event = _relative_event(cell, min_x, min_y, f"{prefix}_cell")
                event_names.add(event)
                mirror = _mirror_x(cell, min_x, max_x)
                side = "left" if cell[0] < center_x else "right" if cell[0] > center_x else "center"
                if mirror in nodes:
                    event_names.add(_relative_event(cell, min_x, min_y, f"{prefix}_mirror_occ"))
                    if side == "left":
                        mirror_stats[f"{prefix}_occ_left"] += 1
                    elif side == "right":
                        mirror_stats[f"{prefix}_occ_right"] += 1
                elif mirror not in pocket_cells and mirror not in deep_pocket_cells:
                    event_names.add(_relative_event(cell, min_x, min_y, f"{prefix}_mirror_void"))
                    if side == "left":
                        mirror_stats[f"{prefix}_void_left"] += 1
                    elif side == "right":
                        mirror_stats[f"{prefix}_void_right"] += 1

        for event_name in event_names:
            event_counts[event_name].add(base.subtype)

        numeric = {
            "pocket_left_fraction": _fraction(pocket_left, len(pocket_cells)),
            "pocket_right_fraction": _fraction(pocket_right, len(pocket_cells)),
            "deep_left_fraction": _fraction(deep_left, len(deep_pocket_cells)),
            "deep_right_fraction": _fraction(deep_right, len(deep_pocket_cells)),
            "pocket_x_span": _span(pocket_cells),
            "deep_x_span": _span(deep_pocket_cells),
            "pocket_both_sides": float(pocket_left > 0 and pocket_right > 0),
            "deep_both_sides": float(deep_left > 0 and deep_right > 0),
            "pocket_mirror_occupied_left_fraction": _fraction(mirror_stats["pocket_occ_left"], len(pocket_cells)),
            "pocket_mirror_occupied_right_fraction": _fraction(mirror_stats["pocket_occ_right"], len(pocket_cells)),
            "deep_mirror_occupied_left_fraction": _fraction(mirror_stats["deep_occ_left"], len(deep_pocket_cells)),
            "deep_mirror_occupied_right_fraction": _fraction(mirror_stats["deep_occ_right"], len(deep_pocket_cells)),
            "pocket_mirror_void_left_fraction": _fraction(mirror_stats["pocket_void_left"], len(pocket_cells)),
            "pocket_mirror_void_right_fraction": _fraction(mirror_stats["pocket_void_right"], len(pocket_cells)),
            "deep_mirror_void_left_fraction": _fraction(mirror_stats["deep_void_left"], len(deep_pocket_cells)),
            "deep_mirror_void_right_fraction": _fraction(mirror_stats["deep_void_right"], len(deep_pocket_cells)),
        }
        raw_rows.append((source_name, base.subtype, numeric, event_names))

    event_scores: list[tuple[tuple[int, str], str]] = []
    for event_name, labels in event_counts.items():
        if len(labels) < 2:
            continue
        support = sum(event_name in row_events for *_prefix, row_events in raw_rows)
        event_scores.append(((-support, event_name), event_name))
    event_scores.sort(key=lambda item: item[0])
    selected_events = tuple(item[1] for item in event_scores[:event_limit])

    rows: list[CandidateIdentityRow] = []
    for source_name, subtype, numeric, event_names in raw_rows:
        row_values = {
            "source_name": source_name,
            "subtype": subtype,
            **numeric,
            "event_present_count": float(sum(event in event_names for event in selected_events)),
        }
        for event_name in selected_events:
            row_values[_sanitize_event_name(event_name)] = float(event_name in event_names)
        row_cls = _candidate_row_type(selected_events)
        rows.append(row_cls(**row_values))

    rows.sort(key=lambda row: row.source_name)
    return rows, selected_events, signature_text, bucket_text


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
        ("pocket_left_fraction", float),
        ("pocket_right_fraction", float),
        ("deep_left_fraction", float),
        ("deep_right_fraction", float),
        ("pocket_x_span", float),
        ("deep_x_span", float),
        ("pocket_both_sides", float),
        ("deep_both_sides", float),
        ("pocket_mirror_occupied_left_fraction", float),
        ("pocket_mirror_occupied_right_fraction", float),
        ("deep_mirror_occupied_left_fraction", float),
        ("deep_mirror_occupied_right_fraction", float),
        ("pocket_mirror_void_left_fraction", float),
        ("pocket_mirror_void_right_fraction", float),
        ("deep_mirror_void_left_fraction", float),
        ("deep_mirror_void_right_fraction", float),
        ("event_present_count", float),
    ]
    event_fields = [(_sanitize_event_name(event_name), float) for event_name in selected_events]
    return make_dataclass(
        "CandidateIdentityExpandedRow",
        base_fields + event_fields,
        frozen=True,
    )


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
                (not candidate.exact, -candidate.correct, candidate.term_count, candidate.fp + candidate.fn, candidate.rule_text)
                < (not best.exact, -best.correct, best.term_count, best.fp + best.fn, best.rule_text)
            ):
                best = candidate
    return best


def render_event_summary(rows: list[object], selected_events: tuple[str, ...]) -> str:
    lines = [
        "Selected Candidate Identity Events",
        "==================================",
        "event | add1 | add4",
        "-----+------+-----",
    ]
    for event_name in selected_events:
        attr = _sanitize_event_name(event_name)
        add1_count = sum(
            getattr(row, attr) > 0.5 and getattr(row, "subtype") == "add1-sensitive"
            for row in rows
        )
        add4_count = sum(
            getattr(row, attr) > 0.5 and getattr(row, "subtype") == "add4-sensitive"
            for row in rows
        )
        lines.append(f"{event_name:<34.34} | {add1_count:>4} | {add4_count:>4}")
    return "\n".join(lines)


def render_numeric_summary(rows: list[object]) -> str:
    lines = [
        "Candidate Identity Envelopes",
        "============================",
        "subtype | cases | dleft~ | dright~ | dxspan~ | dboth~ | dmoccL~ | dmoccR~",
        "--------+-------+--------+---------+---------+--------+---------+--------",
    ]
    for subtype in sorted({getattr(row, "subtype") for row in rows}):
        bucket = [row for row in rows if getattr(row, "subtype") == subtype]
        lines.append(
            f"{subtype:<19.19} | {len(bucket):>5} | "
            f"{statistics.median(getattr(row, 'deep_left_fraction') for row in bucket):>6.3f} | "
            f"{statistics.median(getattr(row, 'deep_right_fraction') for row in bucket):>7.3f} | "
            f"{statistics.median(getattr(row, 'deep_x_span') for row in bucket):>7.3f} | "
            f"{statistics.median(getattr(row, 'deep_both_sides') for row in bucket):>6.3f} | "
            f"{statistics.median(getattr(row, 'deep_mirror_occupied_left_fraction') for row in bucket):>7.3f} | "
            f"{statistics.median(getattr(row, 'deep_mirror_occupied_right_fraction') for row in bucket):>6.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap candidate-identity bucket started {started}", flush=True)
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
    add1_rule = best_rule_for_target(rows, args.left_subtype, max_terms=args.max_local_terms)
    add4_rule = best_rule_for_target(rows, args.right_subtype, max_terms=args.max_local_terms)

    print()
    print("Low-Overlap Candidate Identity Bucket")
    print("=====================================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(render_event_summary(rows, selected_events))
    print()
    print(render_numeric_summary(rows))
    print()
    if add1_rule is not None:
        print(
            f"candidate_identity_best[{args.left_subtype}]: exact={'Y' if add1_rule.exact else 'n'} "
            f"correct={add1_rule.correct}/{add1_rule.total} tp/fp/fn={add1_rule.tp}/{add1_rule.fp}/{add1_rule.fn} "
            f"rule={add1_rule.rule_text}"
        )
    if add4_rule is not None:
        print(
            f"candidate_identity_best[{args.right_subtype}]: exact={'Y' if add4_rule.exact else 'n'} "
            f"correct={add4_rule.correct}/{add4_rule.total} tp/fp/fn={add4_rule.tp}/{add4_rule.fp}/{add4_rule.fn} "
            f"rule={add4_rule.rule_text}"
        )
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap candidate-identity bucket completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
