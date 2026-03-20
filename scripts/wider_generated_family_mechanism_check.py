#!/usr/bin/env python3
"""Widen the generated graph family and test whether the corrected mechanism split survives."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    aggregate_mechanism_split_rows,
    broader_hub_mechanism_specs,
    degree_profile_fallback_benchmark,
    extended_atomic_route_overlap_benchmark,
    extended_proxy_route_benchmark,
    generated_ensemble_spec,
    hub_mechanism_split_rows,
    MechanismSplitRow,
    render_degree_profile_fallback_table,
    render_extended_atomic_route_overlap_table,
    render_extended_proxy_route_aggregate_table,
    render_extended_proxy_route_table,
    render_mechanism_split_aggregate_table,
    render_mechanism_split_table,
    render_threshold_core_model_table,
    render_threshold_core_overlap_table,
    threshold_core_overlap_analysis,
    _mechanism_split_class,
)


WIDER_ENSEMBLE = (generated_ensemble_spec("wider"),)
_WIDER_NAME, WIDER_GEOMETRY_LIMIT, WIDER_PROCEDURAL_LIMIT, WIDER_STYLES = WIDER_ENSEMBLE[0]
WIDER_FAST_HUB_ANCHORS = (
    "degree:ge-6",
    "degree:ge-7",
    "exposure:share6",
    "exposure:bundle",
)
WIDER_SLOW_HUB_ANCHORS = ("degree:full-rich",)


def banner(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"wider generated-family mechanism check started {started}", flush=True)
    print(
        f"ensemble={_WIDER_NAME} "
        f"geometry_variant_limit={WIDER_GEOMETRY_LIMIT} "
        f"procedural_variant_limit={WIDER_PROCEDURAL_LIMIT} "
        f"styles={WIDER_STYLES}",
        flush=True,
    )
    total_start = time.time()

    banner("Threshold Core Overlap")
    overlap_rows, model_rows = threshold_core_overlap_analysis(
        mode_retained_weight=1.0,
        ensembles=WIDER_ENSEMBLE,
        include_models=False,
    )
    print(render_threshold_core_overlap_table(overlap_rows))
    if model_rows:
        print()
        print(render_threshold_core_model_table(model_rows))

    def run_hub_section(
        title: str,
        benchmark_name: str,
        mechanism_names: tuple[str, ...],
    ) -> list[MechanismSplitRow]:
        banner(title)
        split_rows: list[MechanismSplitRow] = []
        wider_specs = broader_hub_mechanism_specs(mechanism_names=mechanism_names)
        for index, (mechanism_name, benchmark_fn, extra_kwargs) in enumerate(
            wider_specs,
            start=1,
        ):
            started = time.time()
            print(
                f"[{index}/{len(wider_specs)}] starting {mechanism_name}",
                flush=True,
            )
            row = benchmark_fn(
                mode_retained_weight=1.0,
                geometry_variant_limit=WIDER_GEOMETRY_LIMIT,
                procedural_variant_limit=WIDER_PROCEDURAL_LIMIT,
                procedural_styles=WIDER_STYLES,
                basis_sizes=(3,),
                **extra_kwargs,
            )[0]
            compact_fast, extended_fast, same_feature_signature, split_class = (
                _mechanism_split_class(
                    row.compact_parity_size,
                    row.compact_parity_feature_subset,
                    row.extended_parity_size,
                    row.extended_parity_feature_subset,
                    fast_parity_size=3,
                )
            )
            split_row = MechanismSplitRow(
                benchmark_name=benchmark_name,
                mechanism_name=mechanism_name,
                compact_parity_size=row.compact_parity_size,
                compact_parity_feature_subset=row.compact_parity_feature_subset,
                extended_parity_size=row.extended_parity_size,
                extended_parity_feature_subset=row.extended_parity_feature_subset,
                compact_fast=compact_fast,
                extended_fast=extended_fast,
                same_feature_signature=same_feature_signature,
                split_class=split_class,
                compact_best_prethreshold_gap=row.compact_best_prethreshold_gap,
                compact_best_prethreshold_worst_gap=row.compact_best_prethreshold_worst_gap,
                extended_best_prethreshold_gap=row.extended_best_prethreshold_gap,
                extended_best_prethreshold_worst_gap=row.extended_best_prethreshold_worst_gap,
            )
            split_rows.append(split_row)
            print(
                f"[{index}/{len(wider_specs)}] finished {mechanism_name} "
                f"class={split_class} "
                f"compact={row.compact_parity_size}:{row.compact_parity_feature_subset} "
                f"extended={row.extended_parity_size}:{row.extended_parity_feature_subset} "
                f"elapsed={time.time() - started:.1f}s",
                flush=True,
            )
        split_rows.sort(key=lambda row: (row.benchmark_name, row.split_class, row.mechanism_name))
        print(render_mechanism_split_aggregate_table(aggregate_mechanism_split_rows(split_rows)))
        print()
        print(render_mechanism_split_table(split_rows, limit_per_benchmark=16))
        return split_rows

    run_hub_section(
        "Wider Hub Mechanism Split",
        "wider-hub-fast",
        WIDER_FAST_HUB_ANCHORS,
    )

    banner("Extended Proxy Routes")
    proxy_rows, proxy_aggregate_rows = extended_proxy_route_benchmark(
        mode_retained_weight=1.0,
        geometry_variant_limit=WIDER_GEOMETRY_LIMIT,
        procedural_variant_limit=WIDER_PROCEDURAL_LIMIT,
        procedural_styles=WIDER_STYLES,
    )
    print(render_extended_proxy_route_aggregate_table(proxy_aggregate_rows))
    print()
    print(render_extended_proxy_route_table(proxy_rows))

    banner("Extended Atomic Overlap")
    _score_rows, atomic_overlap_rows = extended_atomic_route_overlap_benchmark(
        mode_retained_weight=1.0,
        ensembles=("wider",),
        include_scores=False,
    )
    print(render_extended_atomic_route_overlap_table(atomic_overlap_rows))

    banner("Sparse Fallback")
    fallback_rows = degree_profile_fallback_benchmark(
        mode_retained_weight=1.0,
        geometry_variant_limit=WIDER_GEOMETRY_LIMIT,
        procedural_variant_limit=WIDER_PROCEDURAL_LIMIT,
        procedural_styles=WIDER_STYLES,
    )
    print(render_degree_profile_fallback_table(fallback_rows))

    run_hub_section(
        "Wider Full-Rich Anchor",
        "wider-hub-full-rich",
        WIDER_SLOW_HUB_ANCHORS,
    )

    print()
    print(
        "wider generated-family mechanism check completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
