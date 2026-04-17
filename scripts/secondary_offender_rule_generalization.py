#!/usr/bin/env python3
"""Check whether taper-wrap jump rules generalize to secondary offender families."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_secondary_offender_rule_aggregate_table,
    secondary_offender_rule_generalization_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"secondary offender rule generalization started {started}", flush=True)
    total_start = time.time()
    _rows, aggregate_rows = secondary_offender_rule_generalization_analysis()

    print()
    print("Secondary Offender Rule Generalization")
    print("=====================================")
    print(render_secondary_offender_rule_aggregate_table(aggregate_rows))
    print()
    print("Interpretation")
    print("==============")
    for row in aggregate_rows:
        print(
            f"- {row.ensemble_name} {row.scenario_name} {row.outcome}: cases={row.cases}, "
            f"taper-e matches={row.match_taper_e_rule_cases}, taper-c matches={row.match_taper_c_rule_cases}, "
            f"mean cvar={row.mean_center_variation:.2f}, brough={row.mean_boundary_roughness:.2f}, "
            f"asym={row.mean_mirror_center_asymmetry:.2f}, crossing={row.crossing_cases}."
        )

    print()
    print(
        "secondary offender rule generalization completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
