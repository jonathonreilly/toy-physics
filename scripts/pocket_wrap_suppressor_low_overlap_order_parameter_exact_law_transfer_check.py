#!/usr/bin/env python3
"""Project the exact frozen low-overlap law onto nearby frontier limits."""

from __future__ import annotations

import argparse
from collections import Counter
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

from pocket_wrap_suppressor_frontier_compression import parse_variant_limit  # noqa: E402
from pocket_wrap_suppressor_low_overlap_order_parameter_full_bucket_exact_projection import (  # noqa: E402
    build_rows,
    predict_branch,
    predict_subtype,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


DEFAULT_LOGS = (
    "/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1232.txt",
    "/Users/jonreilly/Projects/Physics/logs/2026-03-23-pocket-wrap-suppressor-nonpocket-subtype-rules-1488.txt",
    "/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-3344.txt",
    "/Users/jonreilly/Projects/Physics/logs/2026-03-24-pocket-wrap-suppressor-nonpocket-subtype-rules-4112.txt",
    "/Users/jonreilly/Projects/Physics/logs/2026-03-25-pocket-wrap-suppressor-nonpocket-subtype-rules-4992-max5600.txt",
    "/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", nargs="+", default=list(DEFAULT_LOGS))
    return parser


def format_counts(rows: list[object], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def render_limit_block(log_path: Path) -> tuple[str, int]:
    rows = build_rows(log_path)
    variant_limit = parse_variant_limit(log_path)
    misclassified = [row for row in rows if predict_subtype(row) != getattr(row, "subtype")]
    ambiguous = [row for row in rows if predict_subtype(row) == "ambiguous"]
    unmatched = [row for row in rows if predict_subtype(row) == "unmatched"]

    lines = [
        f"variant_limit={variant_limit}",
        "-" * (14 + len(str(variant_limit))),
        f"log={log_path}",
        f"rows={len(rows)} ({format_counts(rows)})",
        f"misclassified={len(misclassified)} ({format_counts(misclassified)})",
        f"ambiguous={len(ambiguous)} ({format_counts(ambiguous)})",
        f"unmatched={len(unmatched)} ({format_counts(unmatched)})",
        "predicted_branches:",
    ]
    for branch in (
        "high-closure-add4",
        "high-closure-pair-only",
        "outside-gate-pair-only",
        "outside-gate-add4",
        "outside-gate-add1-default",
    ):
        branch_rows = [row for row in rows if predict_branch(row) == branch]
        lines.append(f"  {branch}: {len(branch_rows)} ({format_counts(branch_rows)})")

    if misclassified:
        lines.append("misclassified_rows:")
        for row in misclassified:
            lines.append(
                f"  {getattr(row, 'source_name')} actual={getattr(row, 'subtype')} "
                f"predicted={predict_subtype(row)} branch={predict_branch(row)} "
                f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
                f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
                f"closure_load={float(getattr(row, 'closure_load')):.3f}"
            )
    else:
        lines.append("misclassified_rows: none")

    return "\n".join(lines), len(misclassified)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"exact low-overlap law transfer check started {started}", flush=True)
    total_start = time.time()

    log_paths = [Path(item).resolve() for item in args.logs]
    blocks: list[str] = []
    failures: list[tuple[int, int]] = []
    for log_path in log_paths:
        block, miscount = render_limit_block(log_path)
        blocks.append(block)
        failures.append((parse_variant_limit(log_path), miscount))

    first_failure = next((limit for limit, miscount in failures if miscount > 0), None)

    print()
    print("Exact Low-Overlap Law Transfer Check")
    print("====================================")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"logs={len(log_paths)}")
    print(
        "tested_variant_limits="
        + ",".join(str(parse_variant_limit(path)) for path in log_paths)
    )
    if first_failure is None:
        print("first_failure_limit=none within tested slice")
    else:
        print(f"first_failure_limit={first_failure}")
    print()
    print("\n\n".join(blocks))
    print()
    print(
        "exact low-overlap law transfer check completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
