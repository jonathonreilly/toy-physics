#!/usr/bin/env python3
"""Probe the final 1168 residual bucket for compact add1-vs-add4 separators."""

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
    pocket_wrap_suppressor_residual_bucket_rows,
    pocket_wrap_suppressor_residual_bucket_rule_rows,
    render_pocket_wrap_suppressor_residual_bucket_case_table,
    render_pocket_wrap_suppressor_residual_bucket_rule_table,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant-limit", type=int, default=1168)
    parser.add_argument(
        "--coarse-signature",
        default="cross=n|span=3+|low=L|pocket=H|overlap=1|rough=H",
    )
    parser.add_argument("--rule-limit", type=int, default=6)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor residual-bucket rules started {started}", flush=True)
    total_start = time.time()

    coarse_signature, residual_rows = pocket_wrap_suppressor_residual_bucket_rows(
        variant_limit=args.variant_limit,
        coarse_signature=args.coarse_signature,
    )

    print()
    print("Residual Bucket")
    print("===============")
    print(f"variant_limit={args.variant_limit}")
    print(f"coarse_signature={coarse_signature}")
    print(f"residual_rows={len(residual_rows)}")
    print(render_pocket_wrap_suppressor_residual_bucket_case_table(residual_rows))
    print(flush=True)

    rule_rows = pocket_wrap_suppressor_residual_bucket_rule_rows(
        residual_rows,
        variant_limit=args.variant_limit,
        coarse_signature=coarse_signature,
        limit=args.rule_limit,
    )
    print()
    print("Residual Bucket Rules")
    print("=====================")
    print(render_pocket_wrap_suppressor_residual_bucket_rule_table(rule_rows, limit=args.rule_limit))
    print()
    print(
        "pocket-wrap suppressor residual-bucket rules completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
