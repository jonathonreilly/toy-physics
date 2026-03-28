#!/usr/bin/env python3
"""Transfer scan for the solved add1 support-family map across low-overlap subtypes."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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

from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    PRIMARY_SUPPORT_FAMILY_BUCKETS,
    SupportFamilyTransferRow,
    build_rows,
    is_peer_band_like,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--show-limit", type=int, default=8)
    return parser

def _family_label(row: SupportFamilyTransferRow) -> str:
    if is_peer_band_like(row):
        return "peer-band"
    if row.family_bucket_key in PRIMARY_SUPPORT_FAMILY_BUCKETS:
        return f"primary:{row.family_bucket_key}"
    return f"satellite:{row.residual_bucket_key}"


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"support family transfer scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    by_subtype: dict[str, list[SupportFamilyTransferRow]] = defaultdict(list)
    for row in rows:
        by_subtype[row.subtype].append(row)

    print()
    print("Low-Overlap Support Family Transfer Scan")
    print("=======================================")
    print(f"frontier_log={frontier_log}")
    print(f"total_rows={len(rows)}")
    print(f"subtypes={dict(sorted((key, len(value)) for key, value in by_subtype.items()))}")
    print()

    print("Family-label transfer")
    print("---------------------")
    for subtype in sorted(by_subtype):
        counter = Counter(_family_label(row) for row in by_subtype[subtype])
        print(f"{subtype}: {dict(counter.most_common())}")
    print()

    print("Raw family buckets by subtype")
    print("-----------------------------")
    for subtype in sorted(by_subtype):
        counter = Counter(row.family_bucket_key for row in by_subtype[subtype])
        print(f"{subtype}: {dict(counter.most_common(args.show_limit))}")
    print()

    shared_primary_rows = [
        row
        for row in rows
        if row.family_bucket_key in PRIMARY_SUPPORT_FAMILY_BUCKETS and not is_peer_band_like(row)
    ]
    print("Shared primary-bucket occupancy")
    print("-------------------------------")
    for bucket_key in PRIMARY_SUPPORT_FAMILY_BUCKETS:
        bucket_rows = [row for row in shared_primary_rows if row.family_bucket_key == bucket_key]
        counter = Counter(row.subtype for row in bucket_rows)
        print(f"{bucket_key}: count={len(bucket_rows)} subtype_counts={dict(counter)}")
    print()

    print("Peer-band transfer rows")
    print("-----------------------")
    peer_rows = [row for row in rows if is_peer_band_like(row)]
    for row in peer_rows[: args.show_limit]:
        print(
            f"{row.source_name} subtype={row.subtype} "
            f"closed_pairs={row.edge_identity_closed_pair_count:.1f} "
            f"support_bridge={row.support_role_bridge_count:.1f} "
            f"left_low={row.high_bridge_left_low_count:.1f} "
            f"bucket={row.family_bucket_key}"
        )
    if len(peer_rows) > args.show_limit:
        print(f"... {len(peer_rows) - args.show_limit} more peer-band rows")
    print()

    print("Subtype-exclusive satellites")
    print("---------------------------")
    family_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        if is_peer_band_like(row) or row.family_bucket_key in PRIMARY_SUPPORT_FAMILY_BUCKETS:
            continue
        family_counts[row.residual_bucket_key][row.subtype] += 1
    for key, counts in sorted(
        family_counts.items(),
        key=lambda item: (-sum(item[1].values()), item[0]),
    )[: args.show_limit]:
        if len(counts) == 1:
            print(f"{key}: {dict(counts)}")
    print()
    print(
        "support family transfer scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
