#!/usr/bin/env python3
"""Analyze case-level shell enrichment where extended flips from ge6 to deep-pocket."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    canonical_generated_ensemble_specs,
    generated_ensemble_spec,
    render_threshold_core_shell_case_aggregate_table,
    render_threshold_core_shell_case_table,
    threshold_core_case_shell_flip_analysis,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ensembles",
        nargs="*",
        help="optional named generated ensembles; defaults to the full canonical ladder",
    )
    args = parser.parse_args()

    if args.ensembles:
        ensembles = tuple(generated_ensemble_spec(name) for name in args.ensembles)
    else:
        ensembles = canonical_generated_ensemble_specs()

    started = datetime.now().isoformat(timespec="seconds")
    print(f"threshold core shell case analysis started {started}", flush=True)
    total_start = time.time()
    case_rows, aggregate_rows = threshold_core_case_shell_flip_analysis(ensembles=ensembles)

    print()
    print("Threshold Core Shell Case Groups")
    print("===============================")
    print(render_threshold_core_shell_case_aggregate_table(aggregate_rows))
    print()
    print("Case Examples")
    print("=============")
    print(render_threshold_core_shell_case_table(case_rows))
    print()
    print("Interpretation")
    print("==============")
    for row in aggregate_rows:
        deep_gap = row.mean_shell_deep_fraction - row.mean_core_deep_fraction
        pocket_gap = row.mean_shell_pocket_fraction - row.mean_core_pocket_fraction
        low_gap = row.mean_shell_low_degree_fraction - row.mean_core_low_degree_fraction
        print(
            f"- {row.ensemble_name}/{row.outcome}: {row.cases} cases, "
            f"shell/core={row.mean_ge6_only_fraction:.2f}/{row.mean_ge7_core_fraction:.2f}, "
            f"deep gap {deep_gap:+.2f}, pocket gap {pocket_gap:+.2f}, "
            f"low-degree gap {low_gap:+.2f}, boundary gap "
            f"{row.mean_shell_boundary_deficit - row.mean_core_boundary_deficit:+.2f}."
        )

    print()
    print(
        "threshold core shell case analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
