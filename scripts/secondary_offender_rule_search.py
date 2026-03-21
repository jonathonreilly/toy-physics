#!/usr/bin/env python3
"""Learn tiny rules for secondary offender families like skew-wrap."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_secondary_offender_rule_search_table,
    secondary_offender_rule_search_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"secondary offender rule search started {started}", flush=True)
    total_start = time.time()
    rows = secondary_offender_rule_search_analysis()

    print()
    print("Secondary Offender Rules")
    print("========================")
    print(render_secondary_offender_rule_search_table(rows))
    print()
    print("Interpretation")
    print("==============")
    for row in rows:
        print(
            f"- {row.ensemble_name} {row.scenario_name}: {row.rule_text} -> "
            f"tp/fp/fn={row.tp}/{row.fp}/{row.fn}, precision={row.precision:.2f}, "
            f"recall={row.recall:.2f}, f1={row.f1:.2f}."
        )

    print()
    print(
        "secondary offender rule search completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
