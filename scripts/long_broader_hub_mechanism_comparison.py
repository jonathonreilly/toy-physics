#!/usr/bin/env python3
"""Compare the leading hub-mechanism candidates on a broader graph ensemble."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (
    high_degree_threshold_benchmark,
    neighbor_leverage_threshold_benchmark,
    neighbor_reach_threshold_benchmark,
    soft_hub_exposure_benchmark,
    threshold_exposure_decomposition_benchmark,
)


BROADER_GEOMETRY_VARIANT_LIMIT = 7
BROADER_PROCEDURAL_VARIANT_LIMIT = 4
BROADER_PROCEDURAL_STYLES = ("walk", "mode-mix", "local-morph")


def run_row(row_index: int, row_count: int, benchmark_fn, set_name: str, set_tuple):
    start = time.time()
    print(f"[{row_index}/{row_count}] starting {set_name}", flush=True)
    row = benchmark_fn(
        geometry_variant_limit=BROADER_GEOMETRY_VARIANT_LIMIT,
        procedural_variant_limit=BROADER_PROCEDURAL_VARIANT_LIMIT,
        procedural_styles=BROADER_PROCEDURAL_STYLES,
        **set_tuple,
    )[0]
    print(
        f"{set_name}: "
        f"compact_parity={row.compact_parity_size}:{row.compact_parity_feature_subset} "
        f"| compact_pre={row.compact_best_prethreshold_gap:+.2f}/{row.compact_best_prethreshold_worst_gap:+.2f} "
        f"| extended_parity={row.extended_parity_size}:{row.extended_parity_feature_subset} "
        f"| extended_pre={row.extended_best_prethreshold_gap:+.2f}/{row.extended_best_prethreshold_worst_gap:+.2f} "
        f"| elapsed={time.time() - start:.1f}s",
        flush=True,
    )


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"broader hub mechanism comparison started {started}", flush=True)
    print(
        "geometry_variant_limit="
        f"{BROADER_GEOMETRY_VARIANT_LIMIT} "
        f"procedural_variant_limit={BROADER_PROCEDURAL_VARIANT_LIMIT} "
        f"styles={BROADER_PROCEDURAL_STYLES}",
        flush=True,
    )
    total_start = time.time()

    rows = [
        (
            high_degree_threshold_benchmark,
            "degree:full-rich",
            {"threshold_sets": (("full-rich", tuple(), tuple()),)},
        ),
        (
            high_degree_threshold_benchmark,
            "degree:ge-6",
            {
                "threshold_sets": (
                    (
                        "replace-high-with-ge-6",
                        ("motif_high_degree_neighbor_fraction",),
                        ("motif_high_degree_neighbor_ge_6_fraction",),
                    ),
                )
            },
        ),
        (
            high_degree_threshold_benchmark,
            "degree:ge-7",
            {
                "threshold_sets": (
                    (
                        "replace-high-with-ge-7",
                        ("motif_high_degree_neighbor_fraction",),
                        ("motif_high_degree_neighbor_ge_7_fraction",),
                    ),
                )
            },
        ),
        (
            threshold_exposure_decomposition_benchmark,
            "exposure:share6",
            {
                "exposure_sets": (
                    (
                        "replace-high-with-share6",
                        ("motif_high_degree_neighbor_fraction",),
                        ("motif_high_degree_neighbor_share6_fraction",),
                    ),
                )
            },
        ),
        (
            threshold_exposure_decomposition_benchmark,
            "exposure:bundle",
            {
                "exposure_sets": (
                    (
                        "replace-high-with-threshold-exposure-bundle",
                        ("motif_high_degree_neighbor_fraction",),
                        (
                            "motif_high_degree_neighbor_share6_fraction",
                            "motif_high_degree_neighbor_count6_fraction",
                            "motif_high_degree_neighbor_share7_fraction",
                            "motif_high_degree_neighbor_count7_fraction",
                        ),
                    ),
                )
            },
        ),
        (
            soft_hub_exposure_benchmark,
            "soft:linear6",
            {
                "exposure_sets": (
                    (
                        "replace-high-with-soft-linear-6",
                        ("motif_high_degree_neighbor_fraction",),
                        ("motif_hub_exposure_linear_6_8",),
                    ),
                )
            },
        ),
        (
            neighbor_reach_threshold_benchmark,
            "reach:14",
            {
                "reach_sets": (
                    (
                        "replace-high-with-reach-14",
                        ("motif_high_degree_neighbor_fraction",),
                        ("motif_neighbor_reach_ge_14_fraction",),
                    ),
                )
            },
        ),
        (
            neighbor_reach_threshold_benchmark,
            "reach:24",
            {
                "reach_sets": (
                    (
                        "replace-high-with-reach-24",
                        ("motif_high_degree_neighbor_fraction",),
                        ("motif_neighbor_reach_ge_24_fraction",),
                    ),
                )
            },
        ),
        (
            neighbor_leverage_threshold_benchmark,
            "leverage:linear90",
            {
                "leverage_sets": (
                    (
                        "replace-high-with-linear90",
                        ("motif_high_degree_neighbor_fraction",),
                        ("motif_neighbor_leverage_linear90_fraction",),
                    ),
                )
            },
        ),
        (
            neighbor_leverage_threshold_benchmark,
            "leverage:bundle",
            {
                "leverage_sets": (
                    (
                        "replace-high-with-leverage-bundle",
                        ("motif_high_degree_neighbor_fraction",),
                        (
                            "motif_neighbor_leverage_linear85_fraction",
                            "motif_neighbor_leverage_linear90_fraction",
                            "motif_neighbor_leverage_product70_fraction",
                            "motif_neighbor_leverage_product80_fraction",
                        ),
                    ),
                )
            },
        ),
    ]

    row_count = len(rows)
    for row_index, (benchmark_fn, set_name, set_kwargs) in enumerate(rows, start=1):
        run_row(row_index, row_count, benchmark_fn, set_name, set_kwargs)

    finished = datetime.now().isoformat(timespec="seconds")
    print(f"completed {finished} total_elapsed={time.time() - total_start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
