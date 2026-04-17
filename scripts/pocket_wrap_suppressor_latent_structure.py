#!/usr/bin/env python3
"""Historical live latent-structure sampler for representative non-pocket checkpoints."""

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
    POCKET_WRAP_SUPPRESSOR_HISTORICAL_LIVE_VARIANT_LIMITS,
    pocket_wrap_suppressor_latent_structure_analysis,
    render_pocket_wrap_suppressor_novelty_table,
    render_pocket_wrap_suppressor_order_parameter_table,
    render_pocket_wrap_suppressor_signature_bucket_table,
    render_pocket_wrap_suppressor_signature_trajectory_table,
)


def parse_variant_limits(text: str) -> tuple[int, ...]:
    parts = [part.strip() for part in text.split(",") if part.strip()]
    if not parts:
        raise ValueError("variant limit list must not be empty")
    return tuple(int(part) for part in parts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the historical live latent-structure sampler over representative "
            "non-pocket suppressor checkpoints."
        ),
        epilog=(
            "This runner is a live historical sampler, not the canonical frozen-frontier "
            "compression workflow. For the current compression-first analysis use "
            "/Users/jonreilly/Projects/Physics/scripts/"
            "pocket_wrap_suppressor_frontier_compression.py."
        ),
    )
    parser.add_argument(
        "--variant-limits",
        default=",".join(
            str(limit) for limit in POCKET_WRAP_SUPPRESSOR_HISTORICAL_LIVE_VARIANT_LIMITS
        ),
        help=(
            "Representative live checkpoints to sample. The canonical current "
            "frozen-frontier compression workflow lives in "
            "scripts/pocket_wrap_suppressor_frontier_compression.py."
        ),
    )
    parser.add_argument("--novelty-limit", type=int, default=24)
    parser.add_argument("--order-limit", type=int, default=5)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    variant_limits = parse_variant_limits(args.variant_limits)
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor latent-structure started {started}", flush=True)
    print(
        "mode=historical-live-sampler "
        "canonical_frozen_workflow="
        "/Users/jonreilly/Projects/Physics/scripts/"
        "pocket_wrap_suppressor_frontier_compression.py",
        flush=True,
    )
    total_start = time.time()

    trajectory_rows, novelty_rows, signature_rows, pair_rows, tree_rows = (
        pocket_wrap_suppressor_latent_structure_analysis(variant_limits=variant_limits)
    )
    latest_limit = max(variant_limits)

    print()
    print("Signature Trajectory")
    print("===================")
    print(f"variant_limits={','.join(str(limit) for limit in variant_limits)}")
    print(render_pocket_wrap_suppressor_signature_trajectory_table(trajectory_rows))

    print()
    print(f"Latest Signature Buckets ({latest_limit})")
    print("================================" + "=" * len(str(latest_limit)))
    print(
        render_pocket_wrap_suppressor_signature_bucket_table(
            signature_rows,
            variant_limit=latest_limit,
        )
    )

    print()
    print("Novelty Decomposition")
    print("=====================")
    print(render_pocket_wrap_suppressor_novelty_table(novelty_rows, limit=args.novelty_limit))

    print()
    print(f"Best Two-Axis Order Parameters ({latest_limit})")
    print("=================================" + "=" * len(str(latest_limit)))
    print(render_pocket_wrap_suppressor_order_parameter_table(pair_rows, limit=args.order_limit))

    print()
    print(f"Best Small Trees ({latest_limit})")
    print("=====================" + "=" * len(str(latest_limit)))
    print(render_pocket_wrap_suppressor_order_parameter_table(tree_rows, limit=args.order_limit))

    print()
    print(
        "pocket-wrap suppressor latent-structure completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
