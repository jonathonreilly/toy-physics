#!/usr/bin/env python3
"""Compress overlap-onset occupancy into a coarser asymptotic bridge variable.

This bounded follow-on pools the completed dense-family overlap-onset cards:

- the original local-density compare
- the denser/wider transfer holdout
- the mid-layer sampling-law holdout

The question is narrow: can the transferable `target_fill` signal be restated
as one coarser variable that orders the signed overlap diagnostic `mu`
without introducing another fitted threshold table?

The candidate bridge is:

  occupancy_load = mass_nodes / max(local_target_count, 1)

This is the number of selected source nodes that must share each same-side
target-band site near the low-`b` probe.
"""

from __future__ import annotations

from collections import defaultdict
import argparse
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_overlap_onset_local_density_compare import (  # noqa: E402
    OnsetRow,
    _evaluate_dag as _evaluate_baseline_dag,
)
from scripts.directional_b_overlap_onset_midlayer_sampling_holdout import (  # noqa: E402
    DagConfig as MidlayerDagConfig,
    _collect_rows as _collect_midlayer_rows,
)
from scripts.directional_b_overlap_onset_transfer_holdout import (  # noqa: E402
    DagConfig as TransferDagConfig,
    _collect_rows as _collect_transfer_rows,
)


def _median(values: list[float]) -> float:
    return statistics.median(values)


def _occupancy_load(row: OnsetRow) -> float:
    if row.local_target_count <= 0:
        return float("inf")
    return row.mass_nodes / row.local_target_count


def _load_regime(load: float) -> str:
    if load <= 1.0:
        return "load <= 1"
    if load <= 2.0:
        return "1 < load <= 2"
    return "load > 2"


def _fmt_load(load: float) -> str:
    if math.isinf(load):
        return "inf"
    return f"{load:.3f}"


def _collect_baseline_rows(*, dag_seeds: int, dag_sizes: list[int], dag_target_b: float) -> list[OnsetRow]:
    rows: list[OnsetRow] = []
    for mass_nodes in (3, 5):
        for n_layers in dag_sizes:
            for seed in range(dag_seeds):
                row = _evaluate_baseline_dag((mass_nodes, n_layers, seed, dag_target_b))
                if row is not None:
                    rows.append(row)
    return rows


def _print_dataset_summary(rows_by_dataset: dict[str, list[OnsetRow]]) -> None:
    print(
        f"{'dataset':>12s} {'rows':>4s} {'ovlp':>5s} {'mu_med':>8s} "
        f"{'fill_mean':>10s} {'count_med':>10s} {'load_med':>8s}"
    )
    print("-" * 72)
    for dataset in ("baseline", "transfer", "midlayer"):
        rows = rows_by_dataset[dataset]
        loads = [_occupancy_load(row) for row in rows]
        print(
            f"{dataset:>12s} {len(rows):4d} {sum(1 for row in rows if row.overlap):5d} "
            f"{_median([row.mu for row in rows]):8.3f} "
            f"{statistics.fmean(row.target_fill for row in rows):10.3f} "
            f"{_median([float(row.local_target_count) for row in rows]):10.3f} "
            f"{_median(loads):8.3f}"
        )


def _print_regime_summary(rows: list[OnsetRow], *, title: str) -> None:
    print(title)
    print(
        f"{'regime':>16s} {'rows':>4s} {'ovlp':>5s} {'ovlp%':>7s} "
        f"{'mu_med':>8s} {'fill_mean':>10s} {'load_med':>8s}"
    )
    print("-" * 76)
    grouped: dict[str, list[OnsetRow]] = defaultdict(list)
    for row in rows:
        grouped[_load_regime(_occupancy_load(row))].append(row)
    for regime in ("load <= 1", "1 < load <= 2", "load > 2"):
        bucket = grouped.get(regime, [])
        if not bucket:
            continue
        loads = [_occupancy_load(row) for row in bucket if not math.isinf(_occupancy_load(row))]
        print(
            f"{regime:>16s} {len(bucket):4d} {sum(1 for row in bucket if row.overlap):5d} "
            f"{100.0 * sum(1 for row in bucket if row.overlap) / len(bucket):7.1f} "
            f"{_median([row.mu for row in bucket]):8.3f} "
            f"{statistics.fmean(row.target_fill for row in bucket):10.3f} "
            f"{(_median(loads) if loads else float('inf')):8.3f}"
        )
    print()


def _print_exact_load_classes(rows: list[OnsetRow], *, min_rows: int) -> None:
    buckets: dict[float, list[OnsetRow]] = defaultdict(list)
    for row in rows:
        buckets[_occupancy_load(row)].append(row)

    print(f"Exact occupancy-load classes with at least {min_rows} rows:")
    print(
        f"{'load':>8s} {'rows':>4s} {'ovlp':>5s} {'ovlp%':>7s} "
        f"{'mu_med':>8s} {'fill_mean':>10s}"
    )
    print("-" * 56)
    for load in sorted(buckets, key=lambda value: (math.isinf(value), value)):
        bucket = buckets[load]
        if len(bucket) < min_rows:
            continue
        print(
            f"{_fmt_load(load):>8s} {len(bucket):4d} {sum(1 for row in bucket if row.overlap):5d} "
            f"{100.0 * sum(1 for row in bucket if row.overlap) / len(bucket):7.1f} "
            f"{_median([row.mu for row in bucket]):8.3f} "
            f"{statistics.fmean(row.target_fill for row in bucket):10.3f}"
        )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=min(8, max(1, os.cpu_count() or 1)))
    parser.add_argument("--baseline-seeds", type=int, default=5)
    parser.add_argument("--holdout-seeds", type=int, default=10)
    parser.add_argument("--dag-sizes", nargs="+", type=int, default=[12, 25])
    parser.add_argument("--dag-target-b", type=float, default=1.5)
    parser.add_argument("--min-class-rows", type=int, default=4)
    args = parser.parse_args()

    baseline_rows = _collect_baseline_rows(
        dag_seeds=args.baseline_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
    )
    transfer_rows = _collect_transfer_rows(
        dag_config=TransferDagConfig(
            family_prefix="holdout",
            nodes_per_layer=28,
            y_range=13.0,
            connect_radius=3.0,
            seed_offset=701,
        ),
        dag_seeds=args.holdout_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
        workers=args.workers,
    )
    midlayer_rows = _collect_midlayer_rows(
        dag_config=MidlayerDagConfig(
            family_prefix="midholdout",
            nodes_per_layer=25,
            y_range=12.0,
            connect_radius=3.0,
            seed_offset=1701,
            midlayer_gamma=1.4,
        ),
        dag_seeds=args.holdout_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
        workers=args.workers,
    )

    rows_by_dataset = {
        "baseline": baseline_rows,
        "transfer": transfer_rows,
        "midlayer": midlayer_rows,
    }
    pooled_rows = [*baseline_rows, *transfer_rows, *midlayer_rows]

    print("=" * 108)
    print("DIRECTIONAL-MEASURE B OVERLAP-ONSET OCCUPANCY-LOAD BRIDGE")
    print("=" * 108)
    print(
        "Candidate bridge: occupancy_load = mass_nodes / max(local_target_count, 1), "
        "the number of selected source nodes that must share each same-side target-band site."
    )
    print(
        "No new fitted threshold table is used below; the check is whether this load variable orders "
        "the signed overlap diagnostic mu across the completed dense-family cards."
    )
    print()
    print("Dense-family cards pooled into the bridge:")
    _print_dataset_summary(rows_by_dataset)
    print()

    _print_regime_summary(pooled_rows, title="Pooled occupancy-load regimes:")

    for dataset in ("baseline", "transfer", "midlayer"):
        _print_regime_summary(rows_by_dataset[dataset], title=f"{dataset.capitalize()} occupancy-load regimes:")

    _print_exact_load_classes(pooled_rows, min_rows=args.min_class_rows)

    safe_rows = [row for row in pooled_rows if _occupancy_load(row) <= 1.0]
    shoulder_rows = [row for row in pooled_rows if 1.0 < _occupancy_load(row) <= 2.0]
    overloaded_rows = [row for row in pooled_rows if _occupancy_load(row) > 2.0]

    print("Interpretation:")
    print(
        f"  Load <= 1 is the safely asymptotic regime on the pooled dense-family rows: "
        f"{sum(1 for row in safe_rows if row.overlap)}/{len(safe_rows)} overlap, "
        f"median mu = {_median([row.mu for row in safe_rows]):.3f}."
    )
    print(
        f"  The shoulder sits at 1 < load <= 2: only "
        f"{sum(1 for row in shoulder_rows if row.overlap)}/{len(shoulder_rows)} rows overlap, "
        f"but median mu drops to {_median([row.mu for row in shoulder_rows]):.3f}."
    )
    print(
        f"  Once load > 2, overlap becomes the default: "
        f"{sum(1 for row in overloaded_rows if row.overlap)}/{len(overloaded_rows)} rows overlap and "
        f"median mu falls to {_median([row.mu for row in overloaded_rows]):.3f}."
    )
    print(
        "  So the transferable occupancy-floor statement compresses into a source-per-target-band-site "
        "crowding law: dense low-b families approach or cross mu <= 0 when multiple selected source nodes "
        "must share each same-side target-band site. Exact spacing cuts still matter on the shoulder, but "
        "they act as local refinements rather than the leading bridge variable."
    )


if __name__ == "__main__":
    main()
