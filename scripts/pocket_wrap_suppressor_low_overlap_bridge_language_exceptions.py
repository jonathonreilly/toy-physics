#!/usr/bin/env python3
"""Inspect the residual exceptions under the translated bridge-language rules."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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

from pocket_wrap_suppressor_low_overlap_bridge_event_translation import (  # noqa: E402
    translate_rows,
)
from pocket_wrap_suppressor_low_overlap_candidate_identity_bucket import (  # noqa: E402
    build_rows as build_candidate_identity_rows,
)


@dataclass(frozen=True)
class ExceptionRow:
    source_name: str
    subtype: str
    center_spine_pair: float
    center_spine_count: float
    deep_left_fraction: float
    pocket_left_fraction: float
    deep_mirror_occupied_right_fraction: float
    event_present_count: float


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
    return parser


def build_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
    event_limit: int,
) -> tuple[list[ExceptionRow], str, str]:
    identity_rows, _identity_events, signature_text, bucket_text = build_candidate_identity_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
        event_limit=event_limit,
    )
    bridge_rows, _selected_events, _sig2, _bucket2 = translate_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
        event_limit=event_limit,
    )
    bridge_by_source = {row.source_name: row for row in bridge_rows}
    rows: list[ExceptionRow] = []
    for identity in identity_rows:
        bridge = bridge_by_source[getattr(identity, "source_name")]
        rows.append(
            ExceptionRow(
                source_name=getattr(identity, "source_name"),
                subtype=getattr(identity, "subtype"),
                center_spine_pair=bridge.center_spine_pair,
                center_spine_count=bridge.center_spine_count,
                deep_left_fraction=getattr(identity, "deep_left_fraction"),
                pocket_left_fraction=getattr(identity, "pocket_left_fraction"),
                deep_mirror_occupied_right_fraction=getattr(identity, "deep_mirror_occupied_right_fraction"),
                event_present_count=getattr(identity, "event_present_count"),
            )
        )
    rows.sort(key=lambda row: row.source_name)
    return rows, signature_text, bucket_text


def render_bucket(title: str, rows: list[ExceptionRow]) -> str:
    lines = [
        title,
        "=" * len(title),
        "source | subtype | spine_pair | spine_ct | deep_left | pocket_left | deep_moccR | id_events",
        "------+--------+------------+----------+-----------+-------------+------------+----------",
    ]
    for row in rows:
        lines.append(
            f"{row.source_name:<28.28} | {row.subtype:<15.15} | "
            f"{row.center_spine_pair:>10.3f} | {row.center_spine_count:>8.3f} | "
            f"{row.deep_left_fraction:>9.3f} | {row.pocket_left_fraction:>11.3f} | "
            f"{row.deep_mirror_occupied_right_fraction:>10.3f} | {row.event_present_count:>8.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"bridge-language exceptions started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )

    add1_predicted = [
        row
        for row in rows
        if row.center_spine_pair >= 0.5 and row.deep_left_fraction >= 0.292
    ]
    add1_false_positives = [row for row in add1_predicted if row.subtype != args.left_subtype]
    add1_false_negatives = [
        row
        for row in rows
        if row.subtype == args.left_subtype and row not in add1_predicted
    ]
    add4_predicted = [row for row in rows if row.center_spine_pair <= 0.5]
    add4_false_negatives = [
        row
        for row in rows
        if row.subtype == args.right_subtype and row not in add4_predicted
    ]

    print()
    print("Bridge-Language Exceptions")
    print("==========================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(
        "rules:\n"
        "  add1: bridge_center_spine_pair >= 0.500 and identity_deep_left_fraction >= 0.292\n"
        "  add4: bridge_center_spine_pair <= 0.500"
    )
    print()
    print(render_bucket("Add1 False Positives", add1_false_positives))
    print()
    print(render_bucket("Add1 False Negatives", add1_false_negatives))
    print()
    print(render_bucket("Add4 False Negatives", add4_false_negatives))
    print()
    print(
        "bridge-language exceptions completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
