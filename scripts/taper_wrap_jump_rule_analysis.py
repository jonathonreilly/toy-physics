#!/usr/bin/env python3
"""Search small pre-jump rules for taper-wrap jump-sensitive contexts."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_taper_wrap_jump_rule_table,
    taper_wrap_jump_context_rule_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"taper-wrap jump rule analysis started {started}", flush=True)
    total_start = time.time()
    rows = taper_wrap_jump_context_rule_analysis()

    print()
    print("Taper-Wrap Jump Rules")
    print("=====================")
    print(render_taper_wrap_jump_rule_table(rows))
    print()
    print("Interpretation")
    print("==============")
    for row in rows:
        print(
            f"- {row.target_variant}: {row.rule_text} -> tp/fp/fn={row.tp}/{row.fp}/{row.fn}, "
            f"precision={row.precision:.2f}, recall={row.recall:.2f}, f1={row.f1:.2f}."
        )

    print()
    print(
        "taper-wrap jump rule analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
