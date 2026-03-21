#!/usr/bin/env python3
"""Sweep suppressor-pair coverage over wider local-morph variant limits."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import pocket_wrap_suppressor_coverage_analysis  # noqa: E402


DEFAULT_LIMITS = (16, 24, 32, 40)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor coverage sweep started {started}", flush=True)
    total_start = time.time()

    print()
    print("Pocket-Wrap Suppressor Coverage Sweep")
    print("====================================")
    print("limit | rows | pair_present | pair_rescue | single_rescue | target_match | new sources")
    print("------+------|--------------|-------------|---------------|--------------|---------------------------")

    seen_sources: set[str] = set()
    for limit in DEFAULT_LIMITS:
        rows = pocket_wrap_suppressor_coverage_analysis(variant_limit=limit)
        pair_present = sum(1 for row in rows if row.pair_present)
        pair_rescue = sum(1 for row in rows if row.pair_rescue)
        single_rescue = sum(1 for row in rows if row.single_drop_rescue)
        target_match = sum(1 for row in rows if row.target_gap_match)

        sources = {row.source_name for row in rows}
        new_sources = sorted(sources.difference(seen_sources))
        seen_sources.update(sources)
        new_sources_text = ",".join(new_sources) if new_sources else "-"

        print(
            f"{limit:>5} | "
            f"{len(rows):>4} | "
            f"{pair_present:>12} | "
            f"{pair_rescue:>11} | "
            f"{single_rescue:>13} | "
            f"{target_match:>12} | "
            f"{new_sources_text}"
        )

    print()
    print(
        "pocket-wrap suppressor coverage sweep completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
