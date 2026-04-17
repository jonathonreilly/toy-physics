#!/usr/bin/env python3
"""Scan wrapped generated scenarios for pocket-driven extended defection subtypes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_subtype_scan_analysis,
    render_pocket_wrap_subtype_aggregate_table,
    render_pocket_wrap_subtype_scan_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap subtype scan started {started}", flush=True)
    total_start = time.time()
    rows, aggregate_rows = pocket_wrap_subtype_scan_analysis()

    print()
    print("Pocket-Wrap Subtype Aggregate")
    print("=============================")
    print(render_pocket_wrap_subtype_aggregate_table(aggregate_rows))
    print()
    print("Pocket-Wrap Subtype Cases")
    print("=========================")
    print(render_pocket_wrap_subtype_scan_table(rows))
    print()
    print("Interpretation")
    print("==============")
    pocket_rows = [row for row in rows if row.pocket_signature]
    if not pocket_rows:
        print("- No wrapped generated dpadj-only cases match the current pocket-signature rule.")
    else:
        scenario_summary = {}
        for row in pocket_rows:
            scenario_summary.setdefault((row.ensemble_name, row.scenario_key), set()).add(row.style)
        for (ensemble_name, scenario_key), styles in sorted(scenario_summary.items()):
            print(
                f"- {ensemble_name} {scenario_key}: pocket-signature cases via "
                + ",".join(sorted(styles))
                + "."
            )

    print()
    print(
        "pocket-wrap subtype scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
