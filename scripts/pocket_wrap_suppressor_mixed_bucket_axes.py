#!/usr/bin/env python3
"""Find small latent-axis rules inside mixed add1/add4 coarse-signature buckets."""

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
    pocket_wrap_suppressor_mixed_bucket_axis_analysis,
    render_pocket_wrap_suppressor_mixed_bucket_rule_table,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant-limit", type=int, default=1168)
    parser.add_argument("--rule-limit", type=int, default=12)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor mixed-bucket axes started {started}", flush=True)
    total_start = time.time()

    rows = pocket_wrap_suppressor_mixed_bucket_axis_analysis(
        variant_limit=args.variant_limit,
        limit=args.rule_limit,
    )

    print()
    print("Mixed Add1/Add4 Bucket Rules")
    print("============================")
    print(f"variant_limit={args.variant_limit} rows={len(rows)}")
    print(render_pocket_wrap_suppressor_mixed_bucket_rule_table(rows, limit=args.rule_limit))
    print()
    print(
        "pocket-wrap suppressor mixed-bucket axes completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
