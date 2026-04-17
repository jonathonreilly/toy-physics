#!/usr/bin/env python3
"""Probe role-conditioned support-cell identity motifs in center-spine bucket `00`."""

from __future__ import annotations

import argparse
from dataclasses import make_dataclass
from datetime import datetime
from math import sqrt
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
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _sanitize(name: str) -> str:
    return (
        name.replace(":", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace(",", "_")
        .replace("[", "_")
        .replace("]", "_")
    )


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


def _offset_signature(cells: set[tuple[int, int]], anchor: tuple[int, int]) -> str:
    if not cells:
        return "none"
    ax, ay = anchor
    tokens = [f"{x-ax}:{y-ay}" for x, y in sorted(cells)]
    return "[" + ";".join(tokens) + "]"


def build_support_identity(
    nodes: set[tuple[int, int]],
) -> tuple[set[str], dict[str, float]]:
    if not nodes:
        return set(), {}

    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    all_candidates = pocket_cells | deep_cells
    if not all_candidates:
        return set(), {}

    min_x = min(x for x, _ in nodes)
    min_y = min(y for _, y in nodes)

    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = sorted(roles)
    support_set = set(support_nodes)

    event_set: set[str] = set()
    role_counts = {"bridge": 0, "pocket_only": 0, "deep_only": 0}
    degree_total = 0
    same_role_edge_count = 0
    edge_count = 0
    local_pattern_count = 0

    for support in support_nodes:
        role = roles[support]
        role_counts[role] += 1
        adjacent = set(graph_neighbors(support, support_set | all_candidates, wrap_y=False))
        adj_support = adjacent & support_set
        adj_pocket = adjacent & pocket_cells
        adj_deep = adjacent & deep_cells
        degree_total += len(adj_support)

        # Role-conditioned candidate-family identity pattern around a support anchor.
        pocket_sig = _offset_signature(adj_pocket, support)
        deep_sig = _offset_signature(adj_deep, support)
        pattern = f"r{role}:p{pocket_sig}:d{deep_sig}"
        local_pattern_count += 1

        ax = support[0] - min_x
        ay = support[1] - min_y
        event_set.add(f"rid:{pattern}")
        event_set.add(f"arid:{pattern}:a{ax}:{ay}")
        event_set.add(f"count:{role}:p{len(adj_pocket)}:d{len(adj_deep)}")

    for left in support_nodes:
        for right in graph_neighbors(left, support_set, wrap_y=False):
            if right not in support_set or right <= left:
                continue
            edge_count += 1
            if roles[left] == roles[right]:
                same_role_edge_count += 1

    numeric = {
        "support_role_bridge_fraction": _fraction(role_counts["bridge"], len(support_nodes)),
        "support_role_pocket_only_fraction": _fraction(role_counts["pocket_only"], len(support_nodes)),
        "support_role_deep_only_fraction": _fraction(role_counts["deep_only"], len(support_nodes)),
        "support_degree_mean": _fraction(degree_total, len(support_nodes)),
        "support_same_role_edge_fraction": _fraction(same_role_edge_count, edge_count),
        "support_identity_pattern_count": float(local_pattern_count),
    }
    return event_set, numeric


def build_rows(
    frontier_rows: dict[str, object],
    bucket_rows: list[BucketRow],
    *,
    event_limit: int,
) -> tuple[list[object], tuple[str, ...]]:
    subtype_by_source = {row.source_name: row.subtype for row in bucket_rows}
    event_support: dict[str, set[str]] = {}
    raw: list[tuple[str, str, dict[str, float], set[str]]] = []

    for source_name in sorted(subtype_by_source):
        row = frontier_rows[source_name]
        events, numeric = build_support_identity(set(row.nodes))
        subtype = subtype_by_source[source_name]
        for event in events:
            event_support.setdefault(event, set()).add(subtype)
        raw.append((source_name, subtype, numeric, events))

    scored_events: list[tuple[tuple[int, str], str]] = []
    for event, labels in event_support.items():
        if len(labels) < 2:
            continue
        support = sum(event in events for *_prefix, events in raw)
        scored_events.append(((-support, event), event))
    scored_events.sort(key=lambda item: item[0])
    selected = tuple(event for _key, event in scored_events[:event_limit])

    row_cls = make_dataclass(
        "SupportRoleIdentityRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("support_role_bridge_fraction", float),
            ("support_role_pocket_only_fraction", float),
            ("support_role_deep_only_fraction", float),
            ("support_degree_mean", float),
            ("support_same_role_edge_fraction", float),
            ("support_identity_pattern_count", float),
            ("identity_event_present_count", float),
        ]
        + [(_sanitize(event), float) for event in selected],
        frozen=True,
    )

    rows: list[object] = []
    for source_name, subtype, numeric, events in raw:
        row_values = {
            "source_name": source_name,
            "subtype": subtype,
            **numeric,
            "identity_event_present_count": float(sum(event in events for event in selected)),
        }
        for event in selected:
            row_values[_sanitize(event)] = float(event in events)
        rows.append(row_cls(**row_values))

    rows.sort(key=lambda row: getattr(row, "source_name"))
    return rows, selected


def feature_names(row: object) -> list[str]:
    return [
        name
        for name in row.__dataclass_fields__  # type: ignore[attr-defined]
        if name not in ("source_name", "subtype")
    ]


def render_rows(rows: list[object], selected_events: tuple[str, ...]) -> str:
    shown = [
        "source_name",
        "subtype",
        "support_role_bridge_fraction",
        "support_role_pocket_only_fraction",
        "support_role_deep_only_fraction",
        "support_degree_mean",
        "support_same_role_edge_fraction",
        "support_identity_pattern_count",
        "identity_event_present_count",
    ]
    shown += [_sanitize(event) for event in selected_events[:4]]

    lines = [
        "Bucket 00 support role-identity rows",
        "====================================",
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


def render_neighbor_deltas(
    bucket_rows: list[BucketRow],
    frontier_rows: dict[str, object],
    selected_events: tuple[str, ...],
    *,
    left_subtype: str,
    right_subtype: str,
) -> str:
    stats = zscore_stats(bucket_rows)
    add4_rows = [row for row in bucket_rows if row.subtype == right_subtype]
    add1_rows = [row for row in bucket_rows if row.subtype == left_subtype]

    lines = [
        "Nearest-neighbor support role-identity deltas (add4 vs add1)",
        "=======================================================",
    ]

    for add4_row in add4_rows:
        nearest = min(add1_rows, key=lambda row: zdistance(add4_row, row, stats))
        add4_events, _numeric = build_support_identity(set(frontier_rows[add4_row.source_name].nodes))
        add1_events, _numeric = build_support_identity(set(frontier_rows[nearest.source_name].nodes))
        add4_selected = {event for event in selected_events if event in add4_events}
        add1_selected = {event for event in selected_events if event in add1_events}
        lines.append(
            f"add4={add4_row.source_name} nearest_add1={nearest.source_name} distance={zdistance(add4_row, nearest, stats):.3f}"
        )
        lines.append(
            "  add4_only_selected="
            + str(sorted(_sanitize(event) for event in (add4_selected - add1_selected))[:12])
        )
        lines.append(
            "  add1_only_selected="
            + str(sorted(_sanitize(event) for event in (add1_selected - add4_selected))[:12])
        )

    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 support role-identity started {started}", flush=True)
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

    rows, selected_events = build_rows(
        frontier_rows,
        bucket_rows,
        event_limit=args.event_limit,
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
    print("Center-Spine Bucket 00 Support Role-Identity Context")
    print("====================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)} add1_rows={add1_count} add4_rows={add4_count}")
    print(f"selected_event_count={len(selected_events)}")
    print()
    print(render_rows(rows, selected_events))
    print()
    print(render_rules(f"Best support role-identity rules for {args.right_subtype}", add4_rules))
    print()
    print(render_rules(f"Best support role-identity rules for {args.left_subtype}", add1_rules))
    print()
    print(
        render_neighbor_deltas(
            bucket_rows,
            frontier_rows,
            selected_events,
            left_subtype=args.left_subtype,
            right_subtype=args.right_subtype,
        )
    )
    print()
    print(
        "center-spine bucket00 support role-identity completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
