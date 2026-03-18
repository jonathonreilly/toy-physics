#!/usr/bin/env python3
"""Test whether thresholded high-degree proxies can bridge the compact sparse-route gap."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    compact_sparse_bridge_benchmark,
    compact_threshold_proxy_bridge_sets,
    render_compact_sparse_bridge_table,
)


ENSEMBLES = (
    ("default", 5, 3, ("walk", "mode-mix", "local-morph")),
    ("broader", 7, 4, ("walk", "mode-mix", "local-morph")),
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"compact threshold proxy bridge analysis started {started}", flush=True)
    total_start = time.time()

    rows = []
    addback_sets = compact_threshold_proxy_bridge_sets()
    step_count = len(ENSEMBLES) * len(addback_sets)
    step_index = 0
    for ensemble in ENSEMBLES:
        ensemble_name, geometry_limit, procedural_limit, procedural_styles = ensemble
        print(
            f"ensemble={ensemble_name} geometry_variant_limit={geometry_limit} "
            f"procedural_variant_limit={procedural_limit} styles={procedural_styles}",
            flush=True,
        )
        for addback_name, added_features in addback_sets:
            step_index += 1
            step_start = time.time()
            print(
                f"[{step_index}/{step_count}] starting {ensemble_name}:{addback_name}",
                flush=True,
            )
            row = compact_sparse_bridge_benchmark(
                mode_retained_weight=1.0,
                ensembles=(ensemble,),
                addback_sets=((addback_name, added_features),),
            )[0]
            rows.append(row)
            print(
                f"[{step_index}/{step_count}] finished {ensemble_name}:{addback_name} "
                f"compact={row.compact_parity_size if row.compact_parity_size is not None else '-'}:{row.compact_parity_feature_subset} "
                f"c_pre={row.compact_best_prethreshold_gap:+.2f}/{row.compact_best_prethreshold_worst_gap:+.2f} "
                f"extended={row.extended_parity_size if row.extended_parity_size is not None else '-'}:{row.extended_parity_feature_subset} "
                f"e_fam={row.extended_proxy_family} "
                f"elapsed={time.time() - step_start:.1f}s",
                flush=True,
            )

    rows.sort(key=lambda row: (row.ensemble_name, row.addback_name))
    print()
    print("Compact Threshold Proxy Bridge Detail")
    print("====================================")
    print(render_compact_sparse_bridge_table(rows))
    print()
    print(
        "compact threshold proxy bridge analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
