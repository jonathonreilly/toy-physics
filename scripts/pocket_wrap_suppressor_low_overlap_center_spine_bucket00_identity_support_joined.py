#!/usr/bin/env python3
"""Join bucket00 candidate-identity and support-topology features in one bounded closure pass."""

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

from pocket_wrap_suppressor_low_overlap_candidate_identity_bucket import (  # noqa: E402
    build_rows as build_identity_rows,
)
from pocket_wrap_suppressor_low_overlap_candidate_support_subgraph_bucket import (  # noqa: E402
    build_rows as build_support_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    dataclass_feature_names,
    evaluate_rules,
    render_rules,
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
    parser.add_argument("--signature-terms", type=int, default=2)
    parser.add_argument("--candidate-limit", type=int, default=18)
    parser.add_argument("--event-limit", type=int, default=18)
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def bucket_source_names(bucket_log: Path, bucket_key: str) -> set[str]:
    return {
        row.source_name
        for row in load_bucket_rows(bucket_log)
        if row.bucket_key == bucket_key
    }


def joined_row_type(identity_fields: list[str], support_fields: list[str]):
    fields = [("source_name", str), ("subtype", str)]
    fields += [(f"id_{name}", float) for name in identity_fields]
    fields += [(f"sup_{name}", float) for name in support_fields]
    return make_dataclass("CenterSpineBucket00JoinedRow", fields, frozen=True)


def render_rows(rows: list[object]) -> str:
    shown = [
        "source_name",
        "subtype",
        "id_event_present_count",
        "id_pocket_x_span",
        "id_deep_x_span",
        "sup_bridge_event_present_count",
        "sup_bridge_support_left_fraction",
        "sup_bridge_support_edge_density",
    ]
    lines = [
        "Bucket 00 joined identity+support rows",
        "======================================",
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


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"center-spine bucket00 identity+support joined started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    bucket_log = Path(args.bucket_log).resolve()
    target_names = bucket_source_names(bucket_log, args.bucket_key)

    identity_rows, _identity_events, _sig1, _bucket1 = build_identity_rows(
        frontier_log,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )
    support_rows, _support_events, _sig2, _bucket2 = build_support_rows(
        frontier_log,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )

    identity_rows = [row for row in identity_rows if row.source_name in target_names]
    support_rows = [row for row in support_rows if row.source_name in target_names]
    identity_rows.sort(key=lambda row: row.source_name)
    support_rows.sort(key=lambda row: row.source_name)

    identity_fields = dataclass_feature_names(identity_rows[0])
    support_fields = dataclass_feature_names(support_rows[0])
    row_cls = joined_row_type(identity_fields, support_fields)

    support_by_name = {row.source_name: row for row in support_rows}
    rows: list[object] = []
    for identity_row in identity_rows:
        support_row = support_by_name[identity_row.source_name]
        values = {
            "source_name": identity_row.source_name,
            "subtype": identity_row.subtype,
        }
        values.update({f"id_{name}": float(getattr(identity_row, name)) for name in identity_fields})
        values.update({f"sup_{name}": float(getattr(support_row, name)) for name in support_fields})
        rows.append(row_cls(**values))

    rows.sort(key=lambda row: row.source_name)
    feature_names = dataclass_feature_names(rows[0])

    add4_rules = evaluate_rules(
        rows,
        target_subtype=args.right_subtype,
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    add1_rules = evaluate_rules(
        rows,
        target_subtype=args.left_subtype,
        feature_names=feature_names,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    add4_count = sum(1 for row in rows if row.subtype == args.right_subtype)
    add1_count = sum(1 for row in rows if row.subtype == args.left_subtype)

    print()
    print("Center-Spine Bucket 00 Identity+Support Joined Closure")
    print("======================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket_log={bucket_log}")
    print(f"bucket_key={args.bucket_key}")
    print(f"rows={len(rows)} add1_rows={add1_count} add4_rows={add4_count}")
    print()
    print(render_rows(rows))
    print()
    print(render_rules(f"Best joined rules for {args.right_subtype}", add4_rules))
    print()
    print(render_rules(f"Best joined rules for {args.left_subtype}", add1_rules))
    print()
    print(
        "center-spine bucket00 identity+support joined completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
