#!/usr/bin/env python3
"""Classify the currently observed extended dpadj-only offender set by trigger class."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    known_defection_trigger_coverage_analysis,
    render_known_defection_trigger_coverage_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"known defection trigger coverage started {started}", flush=True)
    total_start = time.time()
    rows = known_defection_trigger_coverage_analysis()

    print()
    print("Known Defection Trigger Coverage")
    print("================================")
    print(render_known_defection_trigger_coverage_table(rows))
    print()
    print("Interpretation")
    print("==============")
    for row in rows:
        print(
            f"- {row.ensemble_name} {row.scenario_name} {row.trigger_class}: cases={row.cases}, "
            f"styles={row.styles}, mean cvar={row.mean_center_variation:.2f}, "
            f"brough={row.mean_boundary_roughness:.2f}, asym={row.mean_mirror_center_asymmetry:.2f}, "
            f"crossing={row.crossing_cases}."
        )

    print()
    print(
        "known defection trigger coverage completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
