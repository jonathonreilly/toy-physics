#!/usr/bin/env python3
"""Probe richer interaction motifs inside the shared `rc0|ml0|c2` bucket."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import make_dataclass
from datetime import datetime
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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    edge_identity_signature,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    build_rc0_ml0_c2_core_inputs,
    RC0_ML0_C2_BUCKET,
)
EVENT_RE = re.compile(
    r"^cedge:(?P<family>deep|pocket):(?P<role_pair>[^:]+:[^:]+):"
    r"cand\\((?P<x1>-?\\d+),(?P<y1>-?\\d+)\\)-\\((?P<x2>-?\\d+),(?P<y2>-?\\d+)\\):"
    r"edge\\((?P<edge_dx>-?\\d+),(?P<edge_dy>-?\\d+)\\):present(?P<present>[01])$"
)
FEATURE_NAMES = [
    "edge_identity_closed_pair_count",
    "edge_identity_open_pair_count",
    "edge_identity_closed_pair_ratio",
    "edge_identity_support_edge_density",
    "support_role_bridge_count",
    "high_bridge_left_count",
    "high_bridge_mid_count",
    "deep_present_ratio",
    "pocket_present_ratio",
    "bridge_bridge_present_ratio",
    "bridge_pocket_only_present_ratio",
    "edge_len2_present_ratio",
    "edge_len3p_present_ratio",
    "far_offset_present_ratio",
    "deep_present_count",
    "pocket_present_count",
    "bridge_bridge_present_count",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=22)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def event_metrics(events: set[str]) -> dict[str, float]:
    counters: dict[str, float] = defaultdict(float)
    for event in events:
        match = EVENT_RE.match(event)
        if not match:
            continue

        family = match.group("family")
        role_pair = match.group("role_pair")
        present = match.group("present") == "1"

        edge_dx = abs(int(match.group("edge_dx")))
        edge_dy = abs(int(match.group("edge_dy")))
        edge_len = edge_dx + edge_dy
        far_offset = max(
            abs(int(match.group("x1"))),
            abs(int(match.group("y1"))),
            abs(int(match.group("x2"))),
            abs(int(match.group("y2"))),
        )

        state = "present" if present else "absent"
        counters[f"{family}_{state}_count"] += 1.0
        counters[f"{role_pair.replace(':', '_')}_{state}_count"] += 1.0

        if edge_len == 2:
            counters[f"edge_len2_{state}_count"] += 1.0
        if edge_len >= 3:
            counters[f"edge_len3p_{state}_count"] += 1.0
        if far_offset >= 2:
            counters[f"far_offset_{state}_count"] += 1.0

    def add_ratio(base: str) -> None:
        present_count = counters[f"{base}_present_count"]
        absent_count = counters[f"{base}_absent_count"]
        counters[f"{base}_present_ratio"] = _ratio(present_count, present_count + absent_count)

    for ratio_base in (
        "deep",
        "pocket",
        "bridge_bridge",
        "bridge_pocket_only",
        "edge_len2",
        "edge_len3p",
        "far_offset",
    ):
        add_ratio(ratio_base)

    return dict(counters)


def build_bucket_rows(frontier_log: Path) -> list[object]:
    coarse_by_source, frontier_rows = build_rc0_ml0_c2_core_inputs(frontier_log)

    row_cls = make_dataclass(
        "TransferMotifRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_closed_pair_count", float),
            ("edge_identity_open_pair_count", float),
            ("edge_identity_closed_pair_ratio", float),
            ("edge_identity_support_edge_density", float),
            ("support_role_bridge_count", float),
            ("high_bridge_left_count", float),
            ("high_bridge_mid_count", float),
            ("deep_present_ratio", float),
            ("pocket_present_ratio", float),
            ("bridge_bridge_present_ratio", float),
            ("bridge_pocket_only_present_ratio", float),
            ("edge_len2_present_ratio", float),
            ("edge_len3p_present_ratio", float),
            ("far_offset_present_ratio", float),
            ("deep_present_count", float),
            ("pocket_present_count", float),
            ("bridge_bridge_present_count", float),
        ],
        frozen=True,
    )

    out = []
    for source_name in sorted(coarse_by_source):
        coarse = coarse_by_source[source_name]
        events, numeric = edge_identity_signature(set(frontier_rows[source_name].nodes))
        motifs = event_metrics(events)
        out.append(
            row_cls(
                source_name=source_name,
                subtype=coarse.subtype,
                edge_identity_closed_pair_count=coarse.edge_identity_closed_pair_count,
                edge_identity_open_pair_count=numeric.get("edge_identity_open_pair_count", 0.0),
                edge_identity_closed_pair_ratio=numeric.get("edge_identity_closed_pair_ratio", 0.0),
                edge_identity_support_edge_density=numeric.get("edge_identity_support_edge_density", 0.0),
                support_role_bridge_count=coarse.support_role_bridge_count,
                high_bridge_left_count=coarse.high_bridge_left_count,
                high_bridge_mid_count=coarse.high_bridge_mid_count,
                deep_present_ratio=motifs.get("deep_present_ratio", 0.0),
                pocket_present_ratio=motifs.get("pocket_present_ratio", 0.0),
                bridge_bridge_present_ratio=motifs.get("bridge_bridge_present_ratio", 0.0),
                bridge_pocket_only_present_ratio=motifs.get("bridge_pocket_only_present_ratio", 0.0),
                edge_len2_present_ratio=motifs.get("edge_len2_present_ratio", 0.0),
                edge_len3p_present_ratio=motifs.get("edge_len3p_present_ratio", 0.0),
                far_offset_present_ratio=motifs.get("far_offset_present_ratio", 0.0),
                deep_present_count=motifs.get("deep_present_count", 0.0),
                pocket_present_count=motifs.get("pocket_present_count", 0.0),
                bridge_bridge_present_count=motifs.get("bridge_bridge_present_count", 0.0),
            )
        )
    return out


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer rc0|ml0|c2 interaction motif scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_bucket_rows(frontier_log)

    print()
    print("Support Family Transfer rc0|ml0|c2 Interaction Motif Scan")
    print("=========================================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"bucket_rows={len(rows)}")
    print()
    for subtype in sorted({row.subtype for row in rows}):
        rules = evaluate_rules(
            rows,
            target_subtype=subtype,
            feature_names=FEATURE_NAMES,
            predicate_limit=args.predicate_limit,
            max_terms=args.max_terms,
            row_limit=args.row_limit,
        )
        print(render_rules(f"Candidate rules for {RC0_ML0_C2_BUCKET} -> {subtype}", rules))
        print()
    print(
        "support family transfer rc0|ml0|c2 interaction motif scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
