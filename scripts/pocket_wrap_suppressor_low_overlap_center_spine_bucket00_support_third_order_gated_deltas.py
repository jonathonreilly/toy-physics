#!/usr/bin/env python3
"""Probe nearest-opposite third-order support/candidate gated deltas in bucket `00`."""

from __future__ import annotations

import argparse
from dataclasses import make_dataclass
from datetime import datetime
from itertools import combinations
from itertools import combinations_with_replacement
from math import sqrt
from pathlib import Path
import re
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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    BucketRow,
    VISIBLE_FEATURES,
    load_bucket_rows,
)
from toy_event_physics import graph_neighbors, pocket_candidate_cells  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument(
        "--bucket-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-low-overlap-center-spine-micro-buckets-5504-add1-vs-add4.txt",
    )
    parser.add_argument("--bucket-key", default="00")
    parser.add_argument("--left-subtype", default="add1-sensitive")
    parser.add_argument("--right-subtype", default="add4-sensitive")
    parser.add_argument("--event-limit", type=int, default=24)
    parser.add_argument("--predicate-limit", type=int, default=20)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _sanitize(name: str) -> str:
    text = re.sub(r"[^0-9A-Za-z_]", "_", name)
    if text and text[0].isdigit():
        text = f"f_{text}"
    return text


def _fraction(numerator: int | float, denominator: int | float) -> float:
    return float(numerator) / float(denominator) if denominator else 0.0


def zscore_stats(rows: list[BucketRow]) -> dict[str, tuple[float, float]]:
    import statistics

    stats: dict[str, tuple[float, float]] = {}
    for feature in VISIBLE_FEATURES:
        values = [row.features[feature] for row in rows]
        mean = statistics.mean(values)
        std = statistics.pstdev(values)
        stats[feature] = (mean, std if std > 0 else 1.0)
    return stats


def zdistance(left: BucketRow, right: BucketRow, stats: dict[str, tuple[float, float]]) -> float:
    total = 0.0
    for feature in VISIBLE_FEATURES:
        _mean, std = stats[feature]
        delta = (left.features[feature] - right.features[feature]) / std
        total += delta * delta
    return sqrt(total)


def support_roles(
    nodes: set[tuple[int, int]],
    pocket_cells: set[tuple[int, int]],
    deep_cells: set[tuple[int, int]],
) -> dict[tuple[int, int], str]:
    roles: dict[tuple[int, int], str] = {}
    all_candidates = pocket_cells | deep_cells
    for node in nodes:
        neighbors = set(graph_neighbors(node, nodes | all_candidates, wrap_y=False))
        touches_pocket = bool(neighbors & pocket_cells)
        touches_deep = bool(neighbors & deep_cells)
        if touches_pocket and touches_deep:
            roles[node] = "bridge"
        elif touches_pocket:
            roles[node] = "pocket_only"
        elif touches_deep:
            roles[node] = "deep_only"
    return roles


def _support_edges(support_nodes: set[tuple[int, int]]) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for left in sorted(support_nodes):
        for right in graph_neighbors(left, support_nodes, wrap_y=False):
            if right not in support_nodes or right <= left:
                continue
            edges.add((left, right))
    return edges


def _candidate_has_edge(
    candidate_neighbors: list[tuple[int, int]],
    support_edges: set[tuple[tuple[int, int], tuple[int, int]]],
) -> bool:
    if len(candidate_neighbors) < 2:
        return False
    for left, right in combinations(sorted(candidate_neighbors), 2):
        edge = (left, right) if left < right else (right, left)
        if edge in support_edges:
            return True
    return False


def _role_pair_gated(
    left: str,
    right: str,
    role_nodes: dict[str, list[tuple[int, int]]],
    support_edges: set[tuple[tuple[int, int], tuple[int, int]]],
) -> bool:
    left_nodes = role_nodes[left]
    right_nodes = role_nodes[right]
    if left == right:
        if len(left_nodes) < 2:
            return False
        for first, second in combinations(sorted(left_nodes), 2):
            edge = (first, second) if first < second else (second, first)
            if edge in support_edges:
                return True
        return False
    for first in left_nodes:
        for second in right_nodes:
            if first == second:
                continue
            edge = (first, second) if first < second else (second, first)
            if edge in support_edges:
                return True
    return False


def third_order_signature(nodes: set[tuple[int, int]]) -> tuple[set[str], dict[str, float]]:
    if not nodes:
        return set(), {}

    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    all_candidates = pocket_cells | deep_cells
    if not all_candidates:
        return set(), {}

    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_set = set(roles)
    support_edges = _support_edges(support_set)

    events: set[str] = set()

    support_touches = 0
    candidate_touches = 0
    twohop_pair_count = 0
    gated_pair_count = 0
    ungated_pair_count = 0
    candidate_with_edge = 0
    candidate_with_twohop = 0

    for support in sorted(roles):
        role = roles[support]
        adjacent = set(graph_neighbors(support, support_set | all_candidates, wrap_y=False))
        pocket_adj = adjacent & pocket_cells
        deep_adj = adjacent & deep_cells
        support_touches += len(pocket_adj) + len(deep_adj)
        events.add(f"touch:{role}:p{len(pocket_adj)}:d{len(deep_adj)}")

    for family, candidate_cells in (("pocket", pocket_cells), ("deep", deep_cells)):
        for candidate in sorted(candidate_cells):
            candidate_neighbors = [
                support
                for support in graph_neighbors(candidate, support_set, wrap_y=False)
                if support in roles
            ]
            if not candidate_neighbors:
                continue

            candidate_touches += len(candidate_neighbors)
            if _candidate_has_edge(candidate_neighbors, support_edges):
                candidate_with_edge += 1

            role_nodes: dict[str, list[tuple[int, int]]] = {
                "bridge": [],
                "pocket_only": [],
                "deep_only": [],
            }
            for support in candidate_neighbors:
                role_nodes[roles[support]].append(support)

            role_counts = {role: len(nodes_for_role) for role, nodes_for_role in role_nodes.items()}
            candidate_has_twohop = False
            for role, count in role_counts.items():
                if count:
                    events.add(f"cand:{family}:{role}:n{count}")

            for left, right in combinations_with_replacement(("bridge", "pocket_only", "deep_only"), 2):
                if left == right:
                    qualifies = role_counts[left] >= 2
                else:
                    qualifies = role_counts[left] >= 1 and role_counts[right] >= 1
                if not qualifies:
                    continue

                candidate_has_twohop = True
                twohop_pair_count += 1
                events.add(f"twohop:{family}:{left}:{right}")

                gated = _role_pair_gated(left, right, role_nodes, support_edges)
                events.add(f"tri:{family}:{left}:{right}:edge{int(gated)}")
                if gated:
                    gated_pair_count += 1
                else:
                    ungated_pair_count += 1

            if candidate_has_twohop:
                candidate_with_twohop += 1

    numeric = {
        "third_order_event_count": float(len(events)),
        "third_order_twohop_pair_count": float(twohop_pair_count),
        "third_order_gated_pair_count": float(gated_pair_count),
        "third_order_ungated_pair_count": float(ungated_pair_count),
        "third_order_candidate_edge_fraction": _fraction(candidate_with_edge, len(all_candidates)),
        "third_order_candidate_twohop_fraction": _fraction(candidate_with_twohop, len(all_candidates)),
        "third_order_support_edge_density": _fraction(2 * len(support_edges), len(support_set) * (len(support_set) - 1)),
        "third_order_support_touch_mean": _fraction(support_touches, len(support_set)),
        "third_order_candidate_touch_mean": _fraction(candidate_touches, len(all_candidates)),
    }
    return events, numeric


def nearest_opposite_rows(
    bucket_rows: list[BucketRow],
    *,
    left_subtype: str,
    right_subtype: str,
) -> dict[str, tuple[str, float]]:
    stats = zscore_stats(bucket_rows)
    by_source = {row.source_name: row for row in bucket_rows}
    left_rows = [row for row in bucket_rows if row.subtype == left_subtype]
    right_rows = [row for row in bucket_rows if row.subtype == right_subtype]

    mapping: dict[str, tuple[str, float]] = {}
    for row in left_rows:
        partner = min(right_rows, key=lambda cand: zdistance(row, cand, stats))
        mapping[row.source_name] = (partner.source_name, zdistance(row, partner, stats))
    for row in right_rows:
        partner = min(left_rows, key=lambda cand: zdistance(row, cand, stats))
        mapping[row.source_name] = (partner.source_name, zdistance(row, partner, stats))
    return {name: mapping[name] for name in sorted(by_source)}


def build_rows(
    frontier_rows: dict[str, object],
    bucket_rows: list[BucketRow],
    *,
    event_limit: int,
    left_subtype: str,
    right_subtype: str,
) -> tuple[list[object], tuple[str, ...], tuple[tuple[str, str], ...], dict[str, tuple[str, float]]]:
    subtype_by_source = {row.source_name: row.subtype for row in bucket_rows}
    nearest = nearest_opposite_rows(
        bucket_rows,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
    )

    signatures: dict[str, tuple[set[str], dict[str, float]]] = {}
    for source_name in sorted(subtype_by_source):
        row = frontier_rows[source_name]
        signatures[source_name] = third_order_signature(set(row.nodes))

    event_counts: dict[str, dict[str, int]] = {}
    raw: list[tuple[str, str, str, float, dict[str, float], set[str]]] = []

    for source_name in sorted(subtype_by_source):
        subtype = subtype_by_source[source_name]
        partner_name, pair_distance = nearest[source_name]
        own_events, own_numeric = signatures[source_name]
        partner_events, partner_numeric = signatures[partner_name]

        own_only = own_events - partner_events
        partner_only = partner_events - own_events
        signed_events = {f"delta:+:{event}" for event in own_only}
        signed_events.update(f"delta:-:{event}" for event in partner_only)

        for event in signed_events:
            per_label = event_counts.setdefault(event, {left_subtype: 0, right_subtype: 0})
            per_label[subtype] += 1

        numeric = {
            "pair_distance_z": pair_distance,
            "pair_shared_third_order_fraction": _fraction(len(own_events & partner_events), len(own_events | partner_events)),
            "pair_own_only_count": float(len(own_only)),
            "pair_partner_only_count": float(len(partner_only)),
            "pair_delta_event_count": float(len(signed_events)),
        }
        for key, value in own_numeric.items():
            partner_value = partner_numeric[key]
            numeric[f"delta_{key}"] = value - partner_value
            numeric[f"abs_delta_{key}"] = abs(value - partner_value)

        raw.append((source_name, subtype, partner_name, pair_distance, numeric, signed_events))

    scored_events: list[tuple[tuple[int, int, str], str]] = []
    for event, counts in event_counts.items():
        left_count = counts[left_subtype]
        right_count = counts[right_subtype]
        support = left_count + right_count
        if support == 0:
            continue
        score = abs(right_count - left_count)
        scored_events.append(((-score, -support, event), event))
    scored_events.sort(key=lambda item: item[0])
    selected = tuple(event for _key, event in scored_events[:event_limit])

    selected_fields = tuple(
        (event, f"ev_{idx:02d}_{_sanitize(event)}") for idx, event in enumerate(selected, start=1)
    )

    row_cls = make_dataclass(
        "SupportThirdOrderDeltaRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("nearest_opposite", str),
            ("pair_distance_z", float),
            ("pair_shared_third_order_fraction", float),
            ("pair_own_only_count", float),
            ("pair_partner_only_count", float),
            ("pair_delta_event_count", float),
            ("delta_third_order_event_count", float),
            ("delta_third_order_twohop_pair_count", float),
            ("delta_third_order_gated_pair_count", float),
            ("delta_third_order_ungated_pair_count", float),
            ("delta_third_order_candidate_edge_fraction", float),
            ("delta_third_order_candidate_twohop_fraction", float),
            ("delta_third_order_support_edge_density", float),
            ("delta_third_order_support_touch_mean", float),
            ("delta_third_order_candidate_touch_mean", float),
            ("abs_delta_third_order_event_count", float),
            ("abs_delta_third_order_twohop_pair_count", float),
            ("abs_delta_third_order_gated_pair_count", float),
            ("abs_delta_third_order_ungated_pair_count", float),
            ("abs_delta_third_order_candidate_edge_fraction", float),
            ("abs_delta_third_order_candidate_twohop_fraction", float),
            ("abs_delta_third_order_support_edge_density", float),
            ("abs_delta_third_order_support_touch_mean", float),
            ("abs_delta_third_order_candidate_touch_mean", float),
            ("pair_selected_event_present_count", float),
        ]
        + [(field_name, float) for _event, field_name in selected_fields],
        frozen=True,
    )

    rows: list[object] = []
    for source_name, subtype, partner_name, _distance, numeric, signed_events in raw:
        values = {
            "source_name": source_name,
            "subtype": subtype,
            "nearest_opposite": partner_name,
            **numeric,
            "pair_selected_event_present_count": float(sum(event in signed_events for event in selected)),
        }
        for event, field_name in selected_fields:
            values[field_name] = float(event in signed_events)
        rows.append(row_cls(**values))

    rows.sort(key=lambda row: getattr(row, "source_name"))
    return rows, selected, selected_fields, nearest


def feature_names(row: object) -> list[str]:
    return [
        name
        for name in row.__dataclass_fields__  # type: ignore[attr-defined]
        if name not in ("source_name", "subtype", "nearest_opposite")
    ]


def render_rows(rows: list[object], selected_fields: tuple[tuple[str, str], ...]) -> str:
    shown = [
        "source_name",
        "subtype",
        "nearest_opposite",
        "pair_distance_z",
        "pair_shared_third_order_fraction",
        "pair_own_only_count",
        "pair_partner_only_count",
        "delta_third_order_gated_pair_count",
        "delta_third_order_support_edge_density",
        "pair_selected_event_present_count",
    ]
    shown += [field_name for _event, field_name in selected_fields[:4]]

    lines = [
        "Bucket 00 support third-order gated delta rows",
        "=============================================",
        " | ".join(shown),
        " | ".join("-" * len(name) for name in shown),
    ]
    for row in rows:
        values: list[str] = []
        for name in shown:
            value = getattr(row, name)
            if isinstance(value, float):
                values.append(f"{value:.3f}")
            else:
                values.append(str(value))
        lines.append(" | ".join(values))
    return "\n".join(lines)


def render_selected_events(selected_fields: tuple[tuple[str, str], ...]) -> str:
    lines = [
        "Selected signed third-order gated motifs",
        "========================================",
    ]
    for event, field_name in selected_fields:
        lines.append(f"{field_name} -> {event}")
    return "\n".join(lines)


def render_pair_map(rows: list[object]) -> str:
    lines = [
        "Nearest-opposite pairing map",
        "============================",
    ]
    for row in rows:
        lines.append(
            f"{getattr(row, 'source_name')} ({getattr(row, 'subtype')}) -> "
            + f"{getattr(row, 'nearest_opposite')} "
            + f"distance={getattr(row, 'pair_distance_z'):.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 support third-order gated deltas started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    bucket_rows = [
        row for row in load_bucket_rows(bucket_log) if row.bucket_key == args.bucket_key
    ]

    selected_sources = {row.source_name for row in bucket_rows}
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in selected_sources
    }

    rows, selected_events, selected_fields, _nearest = build_rows(
        frontier_rows,
        bucket_rows,
        event_limit=args.event_limit,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    add4_count = sum(1 for row in rows if getattr(row, "subtype") == args.right_subtype)
    add1_count = sum(1 for row in rows if getattr(row, "subtype") == args.left_subtype)

    names = feature_names(rows[0])
    add4_rules = evaluate_rules(
        rows,
        target_subtype=args.right_subtype,
        feature_names=names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    add1_rules = evaluate_rules(
        rows,
        target_subtype=args.left_subtype,
        feature_names=names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Center-Spine Bucket 00 Support Third-Order Gated Deltas")
    print("=======================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)} add1_rows={add1_count} add4_rows={add4_count}")
    print(f"selected_event_count={len(selected_events)}")
    print()
    print(render_rows(rows, selected_fields))
    print()
    print(render_selected_events(selected_fields))
    print()
    print(render_rules(f"Best support third-order gated delta rules for {args.right_subtype}", add4_rules))
    print()
    print(render_rules(f"Best support third-order gated delta rules for {args.left_subtype}", add1_rules))
    print()
    print(render_pair_map(rows))
    print()
    print(
        "center-spine bucket00 support third-order gated deltas completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
