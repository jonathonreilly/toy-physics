#!/usr/bin/env python3
"""Decompose the wide center-spine bucket `00` event-delta rescue into coarse event families."""

from __future__ import annotations

import argparse
from dataclasses import make_dataclass
from datetime import datetime
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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    edge_identity_signature,
    nearest_opposite_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_interval_priority_scan import (  # noqa: E402
    Predicate,
    _metrics,
    _stable_interval,
    candidate_predicates,
)
from pocket_wrap_suppressor_low_overlap_center_spine_hardest_bucket_rules import (  # noqa: E402
    load_bucket_rows,
)


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
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def _sanitize(name: str) -> str:
    text = []
    for ch in name:
        if ch.isalnum():
            text.append(ch)
        else:
            text.append("_")
    out = "".join(text).strip("_")
    return out or "f"


def _event_groups(event: str) -> dict[str, int]:
    parts = event.split(":")
    family = parts[1]
    role_pair = parts[2]
    present = parts[-1]
    return {
        f"count_family_{family}": 1,
        f"count_present_{present}": 1,
        f"count_role_{role_pair}": 1,
        f"count_family_{family}_{present}": 1,
        f"count_family_{family}_{role_pair}": 1,
        f"count_role_{role_pair}_{present}": 1,
    }


def _aggregate(events: set[str]) -> dict[str, float]:
    counts: dict[str, float] = {}
    for event in events:
        for key, value in _event_groups(event).items():
            counts[key] = counts.get(key, 0.0) + float(value)
    counts["count_total"] = float(len(events))
    return counts


def build_rows(
    frontier_rows: dict[str, object],
    bucket_rows: list[object],
    *,
    left_subtype: str,
    right_subtype: str,
) -> list[object]:
    subtype_by_source = {row.source_name: row.subtype for row in bucket_rows}
    nearest = nearest_opposite_rows(
        bucket_rows,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
    )

    signatures: dict[str, tuple[set[str], dict[str, float]]] = {}
    for source_name in sorted(subtype_by_source):
        row = frontier_rows[source_name]
        signatures[source_name] = edge_identity_signature(set(row.nodes))

    group_names: set[str] = set()
    raw_rows: list[tuple[str, str, str, dict[str, float]]] = []
    for source_name in sorted(subtype_by_source):
        subtype = subtype_by_source[source_name]
        partner_name, pair_distance = nearest[source_name]
        own_events, own_numeric = signatures[source_name]
        partner_events, partner_numeric = signatures[partner_name]

        own_counts = _aggregate(own_events)
        partner_counts = _aggregate(partner_events)
        all_group_names = set(own_counts) | set(partner_counts)
        numeric: dict[str, float] = {"pair_distance_z": pair_distance}
        for key, value in own_numeric.items():
            partner_value = partner_numeric[key]
            delta_name = f"delta_edge_identity_{key.removeprefix('edge_identity_')}"
            abs_name = f"abs_delta_edge_identity_{key.removeprefix('edge_identity_')}"
            numeric[delta_name] = value - partner_value
            numeric[abs_name] = abs(value - partner_value)
            group_names.add(delta_name)
            group_names.add(abs_name)
        for group_name in sorted(all_group_names):
            own_value = own_counts.get(group_name, 0.0)
            partner_value = partner_counts.get(group_name, 0.0)
            delta_name = f"delta_{group_name}"
            abs_name = f"abs_delta_{group_name}"
            numeric[delta_name] = own_value - partner_value
            numeric[abs_name] = abs(own_value - partner_value)
            group_names.add(delta_name)
            group_names.add(abs_name)
        raw_rows.append((source_name, subtype, partner_name, numeric))

    row_cls = make_dataclass(
        "SupportEdgeIdentityEventFamilyDeltaRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("nearest_opposite", str),
            ("pair_distance_z", float),
        ]
        + [(name, float) for name in sorted(group_names)],
        frozen=True,
    )

    rows: list[object] = []
    for source_name, subtype, partner_name, numeric in raw_rows:
        values = {name: 0.0 for name in sorted(group_names)}
        values.update(numeric)
        rows.append(
            row_cls(
                source_name=source_name,
                subtype=subtype,
                nearest_opposite=partner_name,
                **values,
            )
        )
    rows.sort(key=lambda row: getattr(row, "source_name"))
    return rows


def feature_names(row: object) -> list[str]:
    return [
        name
        for name in row.__dataclass_fields__  # type: ignore[attr-defined]
        if name not in ("source_name", "subtype", "nearest_opposite")
    ]


def _mask_names(rows: list[object], mask: int) -> list[str]:
    return [getattr(row, "source_name") for idx, row in enumerate(rows) if mask & (1 << idx)]


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 event-family decomposition started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    bucket_rows = [row for row in load_bucket_rows(bucket_log) if row.bucket_key == args.bucket_key]
    selected_sources = {row.source_name for row in bucket_rows}
    frontier_rows = {
        row.source_name: row
        for row in reconstruct_low_overlap_rows(frontier_log)
        if row.source_name in selected_sources
    }

    rows = build_rows(
        frontier_rows,
        bucket_rows,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
    )

    names = feature_names(rows[0])
    left_mask = 0
    right_mask = 0
    for idx, row in enumerate(rows):
        subtype = getattr(row, "subtype")
        if subtype == args.left_subtype:
            left_mask |= 1 << idx
        elif subtype == args.right_subtype:
            right_mask |= 1 << idx

    baseline = Predicate(
        name="delta_edge_identity_support_edge_density",
        op="<=",
        threshold=0.018,
        mask=0,
    )
    baseline = Predicate(
        name=baseline.name,
        op=baseline.op,
        threshold=baseline.threshold,
        mask=sum(
            (1 << idx)
            for idx, row in enumerate(rows)
            if float(getattr(row, baseline.name)) <= baseline.threshold
        ),
    )
    baseline_tp, baseline_fp, baseline_fn = _metrics(
        baseline.mask, left_mask, right_mask, len(rows)
    )
    miss_mask = left_mask & (((1 << len(rows)) - 1) ^ baseline.mask)

    grouped_names = [name for name in names if name != "pair_distance_z"]
    predicates = candidate_predicates(rows, grouped_names)
    exact: list[tuple[float, str, Predicate, int, tuple[float, float, float, str], list[str]]] = []
    for pred in predicates:
        if pred.mask & right_mask:
            continue
        if (pred.mask & miss_mask) == 0:
            continue
        combined = baseline.mask | pred.mask
        tp, fp, fn = _metrics(combined, left_mask, right_mask, len(rows))
        if fp != 0 or fn != 0:
            continue
        interval = _stable_interval(rows, pred)
        rescued_names = _mask_names(rows, pred.mask & miss_mask)
        exact.append((interval[2], pred.text, pred, tp, interval, rescued_names))
    exact.sort(key=lambda item: (-item[0], item[1]))

    print()
    print("Center-Spine Bucket 00 Event-Family Delta Decomposition")
    print("=======================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)}")
    print()
    print("Fixed baseline clause")
    print("---------------------")
    print(f"{baseline.name} {baseline.op} {baseline.threshold:.3f}")
    print(f"baseline_metrics: tp/fp/fn={baseline_tp}/{baseline_fp}/{baseline_fn}")
    print(f"baseline_missed_rows: {', '.join(_mask_names(rows, miss_mask))}")
    print()
    print("Top exact grouped-family rescues")
    print("--------------------------------")
    for idx, (width, _text, pred, _tp, interval, rescued_names) in enumerate(exact[: args.row_limit], start=1):
        print(
            f"{idx}. {pred.text} -> width={width:.3f} interval={interval[3]} "
            + f"rescues={', '.join(rescued_names)}"
        )
    print()
    print(
        "center-spine bucket00 event-family decomposition completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
