#!/usr/bin/env python3
"""Derive the corrected mechanism split map from live benchmark helpers."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    mechanism_family_split_benchmark,
    render_mechanism_split_aggregate_table,
    render_mechanism_split_table,
)


def main() -> None:
    print(
        "mechanism family split analysis started "
        + datetime.now().isoformat(timespec="seconds")
    )
    rows, aggregate = mechanism_family_split_benchmark()

    print()
    print("Mechanism Split Aggregate")
    print("=========================")
    print(render_mechanism_split_aggregate_table(aggregate))
    print()
    print("Mechanism Split Detail")
    print("======================")
    print(render_mechanism_split_table(rows, limit_per_benchmark=32))
    print()
    print(
        "mechanism family split analysis completed "
        + datetime.now().isoformat(timespec="seconds")
    )


if __name__ == "__main__":
    main()
