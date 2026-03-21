#!/usr/bin/env python3
"""Test whether pruning extra nodes from full transplants restores pocket-wrap defections."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_local_morph_prune_analysis,
    render_pocket_wrap_local_morph_prune_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap local-morph prune started {started}", flush=True)
    total_start = time.time()
    rows = pocket_wrap_local_morph_prune_analysis()

    print()
    print("Pocket-Wrap Local-Morph Prune")
    print("=============================")
    print(render_pocket_wrap_local_morph_prune_table(rows))
    print()
    print(
        "pocket-wrap local-morph prune completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
