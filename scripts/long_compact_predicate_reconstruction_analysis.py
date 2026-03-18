#!/usr/bin/env python3
"""Search tiny threshold-predicate combinations for compact sparse-route reconstruction."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    CompactPredicateReconstructionAggregateRow,
    compact_threshold_predicate_reconstruction_benchmark,
    compact_threshold_predicate_reconstruction_sets,
    render_compact_predicate_reconstruction_aggregate_table,
    render_compact_predicate_reconstruction_table,
)


ENSEMBLES = (
    ("default", 5, 3, ("walk", "mode-mix", "local-morph")),
    ("broader", 7, 4, ("walk", "mode-mix", "local-morph")),
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"compact predicate reconstruction analysis started {started}", flush=True)
    total_start = time.time()

    rows = []
    aggregate_rows = []
    predicate_sets = compact_threshold_predicate_reconstruction_sets(max_predicate_count=3)
    step_count = len(ENSEMBLES) * len(predicate_sets)
    step_index = 0
    for ensemble in ENSEMBLES:
        ensemble_name, geometry_limit, procedural_limit, procedural_styles = ensemble
        print(
            f"ensemble={ensemble_name} geometry_variant_limit={geometry_limit} "
            f"procedural_variant_limit={procedural_limit} styles={procedural_styles}",
            flush=True,
        )
        ensemble_rows = []
        for predicate_name, predicate_features in predicate_sets:
            step_index += 1
            step_start = time.time()
            print(
                f"[{step_index}/{step_count}] starting {ensemble_name}:{predicate_name}",
                flush=True,
            )
            predicate_rows, _unused_aggregate = compact_threshold_predicate_reconstruction_benchmark(
                mode_retained_weight=1.0,
                ensembles=(ensemble,),
                predicate_sets=((predicate_name, predicate_features),),
            )
            row = predicate_rows[0]
            rows.append(row)
            ensemble_rows.append(row)
            print(
                f"[{step_index}/{step_count}] finished {ensemble_name}:{predicate_name} "
                f"compact={row.compact_parity_size if row.compact_parity_size is not None else '-'}:{row.compact_parity_feature_subset} "
                f"c_pre={row.compact_best_prethreshold_gap:+.2f}/{row.compact_best_prethreshold_worst_gap:+.2f} "
                f"extended={row.extended_parity_size if row.extended_parity_size is not None else '-'}:{row.extended_parity_feature_subset} "
                f"e_fam={row.extended_proxy_family} "
                f"elapsed={time.time() - step_start:.1f}s",
                flush=True,
            )
        best_compact_row = max(
            ensemble_rows,
            key=lambda row: (
                row.compact_best_prethreshold_gap,
                row.compact_best_prethreshold_worst_gap,
                -(row.predicate_count if row.predicate_count > 0 else 99),
                row.predicate_subset,
            ),
        )
        aggregate_rows.append(
            CompactPredicateReconstructionAggregateRow(
                ensemble_name=ensemble_name,
                cases=len(ensemble_rows),
                restored_cases=sum(
                    row.compact_parity_size is not None for row in ensemble_rows
                ),
                fast_restored_cases=sum(
                    row.compact_parity_size == 3 for row in ensemble_rows
                ),
                best_compact_subset=best_compact_row.predicate_subset,
                best_compact_gap_mean=best_compact_row.compact_best_prethreshold_gap,
                best_compact_gap_worst=best_compact_row.compact_best_prethreshold_worst_gap,
            )
        )

    rows.sort(key=lambda row: (row.ensemble_name, row.predicate_count, row.predicate_subset))
    aggregate_rows.sort(key=lambda row: row.ensemble_name)
    print()
    print("Compact Predicate Reconstruction Detail")
    print("=======================================")
    print(render_compact_predicate_reconstruction_table(rows))
    print()
    print("Compact Predicate Reconstruction Aggregate")
    print("==========================================")
    print(render_compact_predicate_reconstruction_aggregate_table(aggregate_rows))
    print()
    print(
        "compact predicate reconstruction analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
