#!/usr/bin/env python3
"""Compare gap signatures across the currently observed extended defection families."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    known_defection_gap_signature_analysis,
    render_known_defection_gap_signature_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"known defection gap signatures started {started}", flush=True)
    total_start = time.time()
    rows = known_defection_gap_signature_analysis()

    print()
    print("Known Defection Gap Signatures")
    print("==============================")
    print(render_known_defection_gap_signature_table(rows))
    print()
    print("Interpretation")
    print("==============")
    for row in rows:
        print(
            f"- {row.ensemble_name} {row.source_name}: family={row.trigger_family}, "
            f"deep/pocket/low={row.deep_gap:+.2f}/{row.pocket_gap:+.2f}/{row.low_degree_gap:+.2f}, "
            f"brough={row.boundary_roughness:.2f}, asym={row.mirror_center_asymmetry:.2f}, "
            f"cross={row.crosses_midline}."
        )

    print()
    print(
        "known defection gap signatures completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
