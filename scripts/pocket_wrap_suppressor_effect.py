#!/usr/bin/env python3
"""Track which local motifs reappear when the pocket-wrap suppressor nodes are pruned."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_suppressor_effect_analysis,
    render_pocket_wrap_suppressor_effect_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor effect started {started}", flush=True)
    total_start = time.time()
    rows = pocket_wrap_suppressor_effect_analysis()

    print()
    print("Pocket-Wrap Suppressor Effects")
    print("==============================")
    print(render_pocket_wrap_suppressor_effect_table(rows))
    print()
    print(
        "pocket-wrap suppressor effect completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
