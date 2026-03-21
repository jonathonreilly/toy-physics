#!/usr/bin/env python3
"""Inject suppressor nodes into the pocket-wrap target to test reverse causality."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_suppressor_injection_analysis,
    render_pocket_wrap_suppressor_injection_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor injection started {started}", flush=True)
    total_start = time.time()
    rows = pocket_wrap_suppressor_injection_analysis()

    dpadj_only = sum(1 for row in rows if row.outcome == "dpadj-only")
    neither = sum(1 for row in rows if row.outcome == "neither")

    print()
    print("Pocket-Wrap Suppressor Injection")
    print("===============================")
    print(f"rows={len(rows)} dpadj_only={dpadj_only} neither={neither}")
    print(render_pocket_wrap_suppressor_injection_table(rows))
    print()
    print(
        "pocket-wrap suppressor injection completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
