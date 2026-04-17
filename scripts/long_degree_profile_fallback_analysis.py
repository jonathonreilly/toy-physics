#!/usr/bin/env python3
"""Test whether the final extended sparse-structure fallback is a real separate route."""

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
    render_degree_profile_fallback_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"sparse-structure fallback analysis started {started}", flush=True)
    total_start = time.time()

    rows = []
    route_sets = degree_profile_fallback_sets()
    for index, (route_name, removed_features) in enumerate(route_sets, start=1):
        route_start = time.time()
        print(f"[{index}/{len(route_sets)}] starting {route_name}", flush=True)
        row = degree_profile_fallback_benchmark(
            route_sets=((route_name, removed_features),),
            mode_retained_weight=1.0,
        )[0]
        proxy_family, _proxy_signature = classify_extended_proxy_family(
            row.extended_parity_feature_subset
        )
        rows.append(row)
        print(
            f"[{index}/{len(route_sets)}] finished {route_name} "
            f"compact={row.compact_parity_size if row.compact_parity_size is not None else '-'}:{row.compact_parity_feature_subset} "
            f"extended={row.extended_parity_size if row.extended_parity_size is not None else '-'}:{row.extended_parity_feature_subset} "
            f"proxy={proxy_family} elapsed={time.time() - route_start:.1f}s",
            flush=True,
        )

    rows.sort(key=lambda row: row.route_name)
    print()
    print("Sparse-Structure Fallback Detail")
    print("================================")
    print(render_degree_profile_fallback_table(rows))
    print()
    print(
        "sparse-structure fallback analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
