#!/usr/bin/env python3
"""Explain the ge6-only threshold shell against the ge7 core on generated families."""

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
    render_threshold_core_shell_context_table,
    render_threshold_core_shell_table,
    threshold_core_shell_mechanism_analysis,
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
    print(f"threshold core shell analysis started {started}", flush=True)
    total_start = time.time()
    rows = threshold_core_shell_mechanism_analysis(ensembles=ensembles)

    print()
    print("Threshold Core Shell")
    print("====================")
    print(render_threshold_core_shell_table(rows))
    print()
    print("Shell Context")
    print("=============")
    print(render_threshold_core_shell_context_table(rows))
    print()
    print("Interpretation")
    print("==============")
    for row in rows:
        deep_ratio = (
            row.shell_deep_fraction / row.core_deep_fraction
            if row.core_deep_fraction > 0.0
            else 0.0
        )
        pocket_ratio = (
            row.shell_pocket_fraction / row.core_pocket_fraction
            if row.core_pocket_fraction > 0.0
            else 0.0
        )
        low_ratio = (
            row.shell_low_degree_fraction / row.core_low_degree_fraction
            if row.core_low_degree_fraction > 0.0
            else 0.0
        )
        print(
            f"- {row.ensemble_name}: the ge6-only shell is {row.ge6_only_fraction:.2f} of nodes "
            f"vs {row.ge7_core_fraction:.2f} in the ge7 core. "
            f"Deep-pocket adjacency is {deep_ratio:.2f}x core "
            f"({row.shell_deep_fraction:.2f} vs {row.core_deep_fraction:.2f}), "
            f"pocket adjacency is {pocket_ratio:.2f}x core "
            f"({row.shell_pocket_fraction:.2f} vs {row.core_pocket_fraction:.2f}), "
            f"and low-degree exposure is {low_ratio:.2f}x core "
            f"({row.shell_low_degree_fraction:.2f} vs {row.core_low_degree_fraction:.2f}). "
            f"The shell carries {row.deep_in_shell_fraction:.2f} of all deep-pocket-adjacent nodes."
        )
        print(
            f"  boundary deficit {row.shell_boundary_deficit_mean:.2f} vs {row.core_boundary_deficit_mean:.2f}; "
            f"mean neighbor degree {row.shell_mean_neighbor_degree:.2f} vs {row.core_mean_neighbor_degree:.2f}."
        )

    print()
    print(
        "threshold core shell analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
