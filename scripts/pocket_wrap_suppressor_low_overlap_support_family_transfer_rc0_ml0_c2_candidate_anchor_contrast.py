#!/usr/bin/env python3
"""Probe candidate-anchored bridge-closure contrasts inside shared bucket `rc0|ml0|c2`."""

from __future__ import annotations

import argparse
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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    render_rules,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    build_candidate_anchor_rows,
    FEATURE_NAMES,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


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


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer rc0|ml0|c2 candidate-anchor contrast started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_candidate_anchor_rows(frontier_log)

    print()
    print("Support Family Transfer rc0|ml0|c2 Candidate-Anchor Contrast")
    print("============================================================")
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
        print(render_rules(f"Best rules for {RC0_ML0_C2_BUCKET} -> {subtype}", rules))
        print()
    print(
        "support family transfer rc0|ml0|c2 candidate-anchor contrast completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
