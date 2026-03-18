#!/usr/bin/env python3
"""Explain why the compact threshold core prefers ge/share over count variants."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_threshold_scaling_table,
    threshold_scaling_explanation_analysis,
)


def main() -> None:
    rows = threshold_scaling_explanation_analysis()
    print("Threshold Scaling Explanation")
    print("=============================")
    print(render_threshold_scaling_table(rows))


if __name__ == "__main__":
    main()
