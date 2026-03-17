#!/usr/bin/env python3
"""Probe whether compact ever accesses the sparse fallback under a broader graph ensemble."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    classify_extended_proxy_family,
    degree_profile_fallback_benchmark,
    degree_profile_fallback_sets,
    render_sparse_fallback_access_aggregate_table,
    render_sparse_fallback_access_table,
    sparse_fallback_access_benchmark,
)


ENSEMBLES = (
    ("default", 5, 3, ("walk", "mode-mix", "local-morph")),
    ("broader", 7, 4, ("walk", "mode-mix", "local-morph")),
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"compact sparse fallback probe started {started}", flush=True)
    total_start = time.time()

    route_sets = degree_profile_fallback_sets()
    step_count = len(ENSEMBLES) * len(route_sets)
    step_index = 0
    for ensemble_name, geometry_limit, procedural_limit, procedural_styles in ENSEMBLES:
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
            row = degree_profile_fallback_benchmark(
                mode_retained_weight=1.0,
                geometry_variant_limit=geometry_limit,
                procedural_variant_limit=procedural_limit,
                procedural_styles=procedural_styles,
                route_sets=((route_name, removed_features),),
            )[0]
            compact_family, _compact_signature = classify_extended_proxy_family(
                row.compact_parity_feature_subset
            )
            extended_family, _extended_signature = classify_extended_proxy_family(
                row.extended_parity_feature_subset
            )
            print(
                f"[{step_index}/{step_count}] finished {ensemble_name}:{route_name} "
                f"compact={row.compact_parity_size if row.compact_parity_size is not None else '-'}:{row.compact_parity_feature_subset} "
                f"c_family={compact_family} "
                f"extended={row.extended_parity_size if row.extended_parity_size is not None else '-'}:{row.extended_parity_feature_subset} "
                f"e_family={extended_family} "
                f"elapsed={time.time() - route_start:.1f}s",
                flush=True,
            )

    rows, aggregate_rows = sparse_fallback_access_benchmark(
        mode_retained_weight=1.0,
        ensembles=ENSEMBLES,
    )
    print()
    print("Sparse Fallback Access Detail")
    print("=============================")
    print(render_sparse_fallback_access_table(rows))
    print()
    print("Sparse Fallback Access Aggregate")
    print("===============================")
    print(render_sparse_fallback_access_aggregate_table(aggregate_rows))
    print()
    print(
        "compact sparse fallback probe completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
