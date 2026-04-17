#!/usr/bin/env python3
"""Translate dominant support-bridge events into coarser bridge-spine language."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import statistics
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_candidate_support_subgraph_bucket import (  # noqa: E402
    build_rows,
)

EVENT_RE = re.compile(r"bridge_node:dx(?P<dx>-?\d+):dy(?P<dy>-?\d+)")


@dataclass(frozen=True)
class BridgeTranslationRow:
    source_name: str
    subtype: str
    center_spine_pair: float
    center_spine_count: float
    center_spine_high: float
    center_spine_low: float
    near_center_spine_count: float
    left_bridge_mass: float
    right_bridge_mass: float
    bridge_vertical_span: float
    bridge_center_bias: float
    bridge_event_present_count: float


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


def translate_rows(
    log_path: Path,
    *,
    left_subtype: str,
    right_subtype: str,
    signature_terms: int,
    candidate_limit: int,
    event_limit: int,
) -> tuple[list[BridgeTranslationRow], tuple[str, ...], str, str]:
    base_rows, selected_events, signature_text, bucket_text = build_rows(
        log_path,
        left_subtype=left_subtype,
        right_subtype=right_subtype,
        signature_terms=signature_terms,
        candidate_limit=candidate_limit,
        event_limit=event_limit,
    )

    parsed_events: list[tuple[str, int, int, str]] = []
    for event_name in selected_events:
        match = EVENT_RE.fullmatch(event_name)
        if not match:
            continue
        parsed_events.append(
            (
                event_name,
                int(match.group("dx")),
                int(match.group("dy")),
                event_name.replace(":", "_"),
            )
        )

    rows: list[BridgeTranslationRow] = []
    for row in base_rows:
        present = [
            (event_name, dx, dy)
            for event_name, dx, dy, attr in parsed_events
            if float(getattr(row, attr)) > 0.5
        ]
        center_events = [(dx, dy) for _event_name, dx, dy in present if dx == 0]
        near_center_events = [(dx, dy) for _event_name, dx, dy in present if abs(dx) <= 1]
        dys = [dy for _event_name, _dx, dy in present]
        left_mass = sum(dx < 0 for _event_name, dx, _dy in present)
        right_mass = sum(dx > 0 for _event_name, dx, _dy in present)
        total_side_mass = max(left_mass + right_mass, 1)

        center_dys = {dy for _dx, dy in center_events}
        rows.append(
            BridgeTranslationRow(
                source_name=getattr(row, "source_name"),
                subtype=getattr(row, "subtype"),
                center_spine_pair=float(3 in center_dys and 4 in center_dys),
                center_spine_count=float(len(center_events)),
                center_spine_high=float(sum(dy >= 4 for _dx, dy in center_events)),
                center_spine_low=float(sum(dy <= 3 for _dx, dy in center_events)),
                near_center_spine_count=float(len(near_center_events)),
                left_bridge_mass=float(left_mass),
                right_bridge_mass=float(right_mass),
                bridge_vertical_span=float(max(dys) - min(dys)) if dys else 0.0,
                bridge_center_bias=abs(left_mass - right_mass) / total_side_mass,
                bridge_event_present_count=float(getattr(row, "bridge_event_present_count")),
            )
        )

    rows.sort(key=lambda row: row.source_name)
    return rows, selected_events, signature_text, bucket_text


def render_translation_summary(rows: list[BridgeTranslationRow]) -> str:
    lines = [
        "Bridge Translation Summary",
        "==========================",
        "subtype | cases | center_pair~ | center_ct~ | near_center~ | left_mass~ | right_mass~ | vspan~",
        "--------+-------+-------------+------------+--------------+------------+-------------+------",
    ]
    for subtype in sorted({row.subtype for row in rows}):
        bucket = [row for row in rows if row.subtype == subtype]
        lines.append(
            f"{subtype:<19.19} | {len(bucket):>5} | "
            f"{statistics.mean(row.center_spine_pair for row in bucket):>11.3f} | "
            f"{statistics.mean(row.center_spine_count for row in bucket):>10.3f} | "
            f"{statistics.mean(row.near_center_spine_count for row in bucket):>12.3f} | "
            f"{statistics.mean(row.left_bridge_mass for row in bucket):>10.3f} | "
            f"{statistics.mean(row.right_bridge_mass for row in bucket):>11.3f} | "
            f"{statistics.mean(row.bridge_vertical_span for row in bucket):>4.3f}"
        )
    return "\n".join(lines)


def render_event_groups(selected_events: tuple[str, ...]) -> str:
    grouped: dict[str, list[str]] = defaultdict(list)
    for event_name in selected_events:
        match = EVENT_RE.fullmatch(event_name)
        if not match:
            continue
        dx = int(match.group("dx"))
        dy = int(match.group("dy"))
        if dx == 0 and dy in {3, 4}:
            group = "center-spine"
        elif abs(dx) <= 1:
            group = "near-center"
        elif dx < 0:
            group = "left-lobe"
        else:
            group = "right-lobe"
        grouped[group].append(event_name)
    lines = [
        "Selected Bridge Event Groups",
        "============================",
    ]
    for group in sorted(grouped):
        lines.append(f"{group}: {', '.join(grouped[group])}")
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"bridge-event translation started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows, selected_events, signature_text, bucket_text = translate_rows(
        log_path,
        left_subtype=args.left_subtype,
        right_subtype=args.right_subtype,
        signature_terms=args.signature_terms,
        candidate_limit=args.candidate_limit,
        event_limit=args.event_limit,
    )

    print()
    print("Bridge Event Translation")
    print("========================")
    print(f"log={log_path}")
    print(f"pair={args.left_subtype} vs {args.right_subtype}")
    print()
    print(signature_text)
    print()
    print(bucket_text)
    print()
    print(render_translation_summary(rows))
    print()
    print(render_event_groups(selected_events))
    print()
    print(
        "bridge-event translation completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
