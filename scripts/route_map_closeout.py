#!/usr/bin/env python3
"""Render the corrected compact and extended mechanism route maps."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_route_map_table,
    route_map_summary,
)


def main() -> None:
    print(
        "route map closeout started "
        + datetime.now().isoformat(timespec="seconds"),
        flush=True,
    )
    compact_rows, extended_rows = route_map_summary(mode_retained_weight=1.0)
    print()
    print("Compact Route Map")
    print("=================")
    print(render_route_map_table(compact_rows))
    print()
    print("Extended Route Map")
    print("==================")
    print(render_route_map_table(extended_rows))
    print()
    print(
        "route map closeout completed "
        + datetime.now().isoformat(timespec="seconds"),
        flush=True,
    )


if __name__ == "__main__":
    main()
