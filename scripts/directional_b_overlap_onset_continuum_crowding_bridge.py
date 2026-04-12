#!/usr/bin/env python3
"""Test a continuum-style target-band crowding proxy for overlap onset.

This bounded follow-on reuses the completed dense-family overlap-onset cards:

- the original local-density compare
- the denser/wider transfer holdout
- the mid-layer sampling-law holdout

The retained coarse bridge is still the discrete occupancy law

  occupancy_load = mass_nodes / max(local_target_count, 1)

The next narrow question is whether that can be translated into one smoother
same-side target-band crowding variable without reopening any wider search.

The tested proxy is:

  continuum_crowding = mass_nodes * local_target_gap / (2 * target_band_half_width)

where ``local_target_gap`` is the mean gap among same-side target-band sites,
falling back to the nearest bracketing same-side gap when the fixed band holds
fewer than two sites.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import argparse
import math
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.directional_b_overlap_onset_local_density_compare import (  # noqa: E402
    TARGET_BAND_HALF_WIDTH,
)
from scripts.directional_b_readout_compare import _select_mass_nodes  # noqa: E402
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.directional_b_overlap_onset_midlayer_sampling_holdout import (  # noqa: E402
    _generate_midlayer_holdout,
)


BAND_WIDTH = 2.0 * TARGET_BAND_HALF_WIDTH


@dataclass(frozen=True)
class CrowdingRow:
    dataset: str
    size: int
    seed: int
    mass_nodes: int
    mu: float
    overlap: bool
    local_target_count: int
    occupancy_load: float
    local_target_gap: float
    continuum_crowding: float


def _median(values: list[float]) -> float:
    return statistics.median(values)


def _mean_gap(values: list[float]) -> float:
    if len(values) < 2:
        return float("nan")
    ordered = sorted(values)
    return statistics.fmean(ordered[i + 1] - ordered[i] for i in range(len(ordered) - 1))


def _bracketing_gap(values: list[float], target: float) -> float:
    if len(values) < 2:
        return float("nan")
    insert = 0
    while insert < len(values) and values[insert] < target:
        insert += 1
    below = values[insert - 1] if insert - 1 >= 0 else None
    above = values[insert] if insert < len(values) else None
    if below is not None and above is not None:
        return above - below
    if below is None:
        return values[1] - values[0]
    return values[-1] - values[-2]


def _occupancy_regime(load: float) -> str:
    if load <= 1.0:
        return "load <= 1"
    if load <= 2.0:
        return "1 < load <= 2"
    return "load > 2"


def _continuum_regime(crowding: float) -> str:
    if crowding <= 1.0:
        return "crowd <= 1"
    if crowding <= 2.0:
        return "1 < crowd <= 2"
    return "crowd > 2"


def _build_row(
    *,
    dataset: str,
    size: int,
    seed: int,
    mass_nodes: int,
    target_b: float,
    positions: list[tuple[float, float]],
    grav_layer_nodes: list[int],
) -> CrowdingRow | None:
    center_y = statistics.fmean(y for _x, y in positions)
    selected = _select_mass_nodes(
        positions=positions,
        layer_nodes=grav_layer_nodes,
        center_y=center_y,
        target_b=target_b,
        mass_nodes=mass_nodes,
    )
    if len(selected) < mass_nodes:
        return None

    ys = [positions[node][1] for node in selected]
    h_mass = 0.5 * (max(ys) - min(ys))
    mu = ((statistics.fmean(ys) - center_y - h_mass) / h_mass) if h_mass > 0.0 else float("inf")

    same_side = sorted(positions[node][1] for node in grav_layer_nodes if positions[node][1] >= center_y)
    target_y = center_y + target_b
    local_target_ys = [y for y in same_side if abs(y - target_y) <= TARGET_BAND_HALF_WIDTH]
    local_target_count = len(local_target_ys)
    occupancy_load = (mass_nodes / local_target_count) if local_target_count > 0 else float("inf")

    band_gap = _mean_gap(local_target_ys)
    local_target_gap = band_gap if math.isfinite(band_gap) else _bracketing_gap(same_side, target_y)
    continuum_crowding = (
        mass_nodes * local_target_gap / BAND_WIDTH
        if math.isfinite(local_target_gap) and local_target_gap > 0.0
        else float("inf")
    )

    return CrowdingRow(
        dataset=dataset,
        size=size,
        seed=seed,
        mass_nodes=mass_nodes,
        mu=mu,
        overlap=mu <= 0.0,
        local_target_count=local_target_count,
        occupancy_load=occupancy_load,
        local_target_gap=local_target_gap,
        continuum_crowding=continuum_crowding,
    )


def _collect_baseline_rows(*, dag_seeds: int, dag_sizes: list[int], dag_target_b: float) -> list[CrowdingRow]:
    rows: list[CrowdingRow] = []
    for mass_nodes in (3, 5):
        for n_layers in dag_sizes:
            for seed in range(dag_seeds):
                positions, _adj, _meta = generate_causal_dag(
                    n_layers=n_layers,
                    nodes_per_layer=25,
                    y_range=12.0,
                    connect_radius=3.0,
                    rng_seed=seed * 11 + 7,
                )
                by_layer: dict[int, list[int]] = defaultdict(list)
                for idx, (x, _y) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer)
                mid = len(layers) // 2
                row = _build_row(
                    dataset="baseline",
                    size=n_layers,
                    seed=seed,
                    mass_nodes=mass_nodes,
                    target_b=dag_target_b,
                    positions=positions,
                    grav_layer_nodes=by_layer[layers[mid]],
                )
                if row is not None:
                    rows.append(row)
    return rows


def _collect_transfer_rows(*, dag_seeds: int, dag_sizes: list[int], dag_target_b: float) -> list[CrowdingRow]:
    rows: list[CrowdingRow] = []
    for mass_nodes in (3, 5):
        for n_layers in dag_sizes:
            for seed in range(dag_seeds):
                positions, _adj, _meta = generate_causal_dag(
                    n_layers=n_layers,
                    nodes_per_layer=28,
                    y_range=13.0,
                    connect_radius=3.0,
                    rng_seed=seed * 11 + 701,
                )
                by_layer: dict[int, list[int]] = defaultdict(list)
                for idx, (x, _y) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer)
                mid = len(layers) // 2
                row = _build_row(
                    dataset="transfer",
                    size=n_layers,
                    seed=seed,
                    mass_nodes=mass_nodes,
                    target_b=dag_target_b,
                    positions=positions,
                    grav_layer_nodes=by_layer[layers[mid]],
                )
                if row is not None:
                    rows.append(row)
    return rows


def _collect_midlayer_rows(*, dag_seeds: int, dag_sizes: list[int], dag_target_b: float) -> list[CrowdingRow]:
    rows: list[CrowdingRow] = []
    for mass_nodes in (3, 5):
        for n_layers in dag_sizes:
            for seed in range(dag_seeds):
                positions, _adj = _generate_midlayer_holdout(
                    n_layers=n_layers,
                    nodes_per_layer=25,
                    y_range=12.0,
                    connect_radius=3.0,
                    rng_seed=seed * 11 + 1701,
                    midlayer_gamma=1.4,
                )
                by_layer: dict[int, list[int]] = defaultdict(list)
                for idx, (x, _y) in enumerate(positions):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer)
                mid = len(layers) // 2
                row = _build_row(
                    dataset="midlayer",
                    size=n_layers,
                    seed=seed,
                    mass_nodes=mass_nodes,
                    target_b=dag_target_b,
                    positions=positions,
                    grav_layer_nodes=by_layer[layers[mid]],
                )
                if row is not None:
                    rows.append(row)
    return rows


def _print_dataset_summary(rows_by_dataset: dict[str, list[CrowdingRow]]) -> None:
    print(
        f"{'dataset':>12s} {'rows':>4s} {'ovlp':>5s} {'mu_med':>8s} "
        f"{'occ_med':>8s} {'crowd_med':>10s} {'safe_leaks':>10s}"
    )
    print("-" * 76)
    for dataset in ("baseline", "transfer", "midlayer"):
        rows = rows_by_dataset[dataset]
        safe_leaks = sum(1 for row in rows if row.continuum_crowding <= 1.0 and row.overlap)
        print(
            f"{dataset:>12s} {len(rows):4d} {sum(1 for row in rows if row.overlap):5d} "
            f"{_median([row.mu for row in rows]):8.3f} "
            f"{_median([row.occupancy_load for row in rows if not math.isinf(row.occupancy_load)]):8.3f} "
            f"{_median([row.continuum_crowding for row in rows if not math.isinf(row.continuum_crowding)]):10.3f} "
            f"{safe_leaks:10d}"
        )


def _print_regime_summary(
    rows: list[CrowdingRow],
    *,
    title: str,
    key,
    regime_name,
) -> None:
    print(title)
    print(
        f"{'regime':>18s} {'rows':>4s} {'ovlp':>5s} {'ovlp%':>7s} "
        f"{'mu_med':>8s} {'value_med':>10s}"
    )
    print("-" * 64)
    grouped: dict[str, list[CrowdingRow]] = defaultdict(list)
    for row in rows:
        grouped[regime_name(key(row))].append(row)
    ordered = ("load <= 1", "1 < load <= 2", "load > 2") if regime_name is _occupancy_regime else (
        "crowd <= 1",
        "1 < crowd <= 2",
        "crowd > 2",
    )
    for regime in ordered:
        bucket = grouped.get(regime, [])
        if not bucket:
            continue
        values = [key(row) for row in bucket if not math.isinf(key(row))]
        print(
            f"{regime:>18s} {len(bucket):4d} {sum(1 for row in bucket if row.overlap):5d} "
            f"{100.0 * sum(1 for row in bucket if row.overlap) / len(bucket):7.1f} "
            f"{_median([row.mu for row in bucket]):8.3f} "
            f"{(_median(values) if values else float('inf')):10.3f}"
        )
    print()


def _print_safe_leak_summary(rows: list[CrowdingRow]) -> None:
    leaks = [row for row in rows if row.continuum_crowding <= 1.0 and row.overlap]
    print("Continuum-safe overlap leaks:")
    print(
        f"  rows with continuum_crowding <= 1 but mu <= 0: {len(leaks)}/{len(rows)}"
    )
    print(
        f"  dataset counts: {dict(sorted(Counter(row.dataset for row in leaks).items()))}"
    )
    print(
        f"  local_target_count counts: {dict(sorted(Counter(row.local_target_count for row in leaks).items()))}"
    )
    print(
        "  These leaks are the discrete phase/alignment failure mode: the local same-side spacing can look"
    )
    print(
        "  smooth enough for low crowding even when the fixed target band itself still exposes only 0-2"
    )
    print(
        "  usable same-side sites."
    )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-seeds", type=int, default=5)
    parser.add_argument("--holdout-seeds", type=int, default=10)
    parser.add_argument("--dag-sizes", nargs="+", type=int, default=[12, 25])
    parser.add_argument("--dag-target-b", type=float, default=1.5)
    args = parser.parse_args()

    baseline_rows = _collect_baseline_rows(
        dag_seeds=args.baseline_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
    )
    transfer_rows = _collect_transfer_rows(
        dag_seeds=args.holdout_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
    )
    midlayer_rows = _collect_midlayer_rows(
        dag_seeds=args.holdout_seeds,
        dag_sizes=args.dag_sizes,
        dag_target_b=args.dag_target_b,
    )

    rows_by_dataset = {
        "baseline": baseline_rows,
        "transfer": transfer_rows,
        "midlayer": midlayer_rows,
    }
    pooled_rows = [*baseline_rows, *transfer_rows, *midlayer_rows]

    print("=" * 108)
    print("DIRECTIONAL-MEASURE B CONTINUUM CROWDING BRIDGE")
    print("=" * 108)
    print(
        "Tested continuum proxy: continuum_crowding = mass_nodes * local_target_gap / band_width,"
    )
    print(
        "with local_target_gap taken from in-band same-side spacing and falling back to the nearest"
    )
    print(
        "bracketing same-side gap when the fixed target band contains fewer than two sites."
    )
    print()
    print("Dense-family cards pooled into the bridge:")
    _print_dataset_summary(rows_by_dataset)
    print()

    _print_regime_summary(
        pooled_rows,
        title="Reference occupancy-load regimes:",
        key=lambda row: row.occupancy_load,
        regime_name=_occupancy_regime,
    )
    _print_regime_summary(
        pooled_rows,
        title="Continuum crowding regimes:",
        key=lambda row: row.continuum_crowding,
        regime_name=_continuum_regime,
    )

    _print_safe_leak_summary(pooled_rows)

    occupancy_safe = [row for row in pooled_rows if row.occupancy_load <= 1.0]
    continuum_safe = [row for row in pooled_rows if row.continuum_crowding <= 1.0]
    print("Interpretation:")
    print(
        f"  The smooth crowding proxy preserves the broad monotone ordering of median mu "
        f"({_median([row.mu for row in continuum_safe]):.3f} on crowd <= 1, "
        f"{_median([row.mu for row in pooled_rows if 1.0 < row.continuum_crowding <= 2.0]):.3f} "
        f"on 1 < crowd <= 2, "
        f"{_median([row.mu for row in pooled_rows if row.continuum_crowding > 2.0]):.3f} on crowd > 2)."
    )
    print(
        f"  But it is not yet a clean replacement for occupancy_load: the occupancy-safe bucket has "
        f"{sum(1 for row in occupancy_safe if row.overlap)}/{len(occupancy_safe)} overlap, while the "
        f"continuum-safe bucket still leaks {sum(1 for row in continuum_safe if row.overlap)}/{len(continuum_safe)}."
    )
    print(
        "  So the retained bridge stays discrete target-band site availability, not a promoted smooth"
    )
    print(
        "  density law. Any later continuum translation will need one extra phase/offset term that knows"
    )
    print(
        "  whether the fixed target band actually captures those nearby same-side sites."
    )


if __name__ == "__main__":
    main()
