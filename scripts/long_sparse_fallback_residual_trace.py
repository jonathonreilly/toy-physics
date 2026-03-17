#!/usr/bin/env python3
"""Trace sparse-fallback residual gaps by basis size on default vs broader ensembles."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    degree_profile_fallback_sets,
    render_sparse_fallback_residual_aggregate_table,
    render_sparse_fallback_residual_trace_table,
    sparse_fallback_residual_trace_benchmark,
)


ENSEMBLES = (
    ("default", 5, 3, ("walk", "mode-mix", "local-morph")),
    ("broader", 7, 4, ("walk", "mode-mix", "local-morph")),
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"sparse fallback residual trace started {started}", flush=True)
    total_start = time.time()

    detail_rows = []
    aggregate_rows = []
    route_sets = degree_profile_fallback_sets()
    step_count = len(ENSEMBLES) * len(route_sets)
    step_index = 0

    for ensemble in ENSEMBLES:
        ensemble_name, geometry_limit, procedural_limit, procedural_styles = ensemble
        print(
            f"ensemble={ensemble_name} geometry_variant_limit={geometry_limit} "
            f"procedural_variant_limit={procedural_limit} styles={procedural_styles}",
            flush=True,
        )
        for route_name, removed_features in route_sets:
            step_index += 1
            route_start = time.time()
            print(
                f"[{step_index}/{step_count}] starting {ensemble_name}:{route_name}",
                flush=True,
            )
            route_detail_rows, route_aggregate_rows = sparse_fallback_residual_trace_benchmark(
                mode_retained_weight=1.0,
                ensembles=(ensemble,),
                route_sets=((route_name, removed_features),),
            )
            detail_rows.extend(route_detail_rows)
            aggregate_rows.extend(route_aggregate_rows)
            compact_row = next(
                row
                for row in route_aggregate_rows
                if row.rule_family == "compact"
            )
            extended_row = next(
                row
                for row in route_aggregate_rows
                if row.rule_family == "extended"
            )
            print(
                f"[{step_index}/{step_count}] finished {ensemble_name}:{route_name} "
                f"compact parity={compact_row.parity_size if compact_row.parity_size is not None else '-'} "
                f"closest={compact_row.closest_size}:{compact_row.closest_feature_subset} "
                f"gap={compact_row.closest_gap_mean:+.2f}/{compact_row.closest_gap_worst:+.2f} "
                f"| extended parity={extended_row.parity_size if extended_row.parity_size is not None else '-'} "
                f"closest={extended_row.closest_size}:{extended_row.closest_feature_subset} "
                f"gap={extended_row.closest_gap_mean:+.2f}/{extended_row.closest_gap_worst:+.2f} "
                f"| elapsed={time.time() - route_start:.1f}s",
                flush=True,
            )

    print()
    print("Sparse Fallback Residual Detail")
    print("===============================")
    print(render_sparse_fallback_residual_trace_table(detail_rows))
    print()
    print("Sparse Fallback Residual Aggregate")
    print("==================================")
    print(render_sparse_fallback_residual_aggregate_table(aggregate_rows))
    print()
    print(
        "sparse fallback residual trace completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
