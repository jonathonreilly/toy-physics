#!/usr/bin/env python3
"""Summarize overlap-positive suppressor rows and search simple pocket-signature rules."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_suppressor_overlap_context_analysis,
    pocket_wrap_suppressor_overlap_context_rule_search,
    render_pocket_wrap_suppressor_overlap_context_rule_table,
    render_pocket_wrap_suppressor_overlap_context_table,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant-limit", type=int, default=64)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor overlap-context rules started {started}", flush=True)
    total_start = time.time()

    rows = pocket_wrap_suppressor_overlap_context_analysis(variant_limit=args.variant_limit)
    rules = pocket_wrap_suppressor_overlap_context_rule_search(rows)
    exact_rules = [row for row in rules if row.fp == 0 and row.fn == 0]

    print()
    print("Pocket-Wrap Suppressor Overlap Context")
    print("======================================")
    print(f"variant_limit={args.variant_limit} rows={len(rows)} exact_rules={len(exact_rules)}")
    print(render_pocket_wrap_suppressor_overlap_context_table(rows))
    print()
    print("Pocket-Wrap Suppressor Overlap Rules")
    print("====================================")
    print(render_pocket_wrap_suppressor_overlap_context_rule_table(exact_rules or rules, limit=8))
    print()
    print(
        "pocket-wrap suppressor overlap-context rules completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
