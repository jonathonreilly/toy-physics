#!/usr/bin/env python3
"""Diagnose depth-48 suppressor pair-kill rows and their deep-cell overlaps."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_candidate_cells,
    pocket_wrap_suppressor_specificity_analysis,
    procedural_geometry_variants,
    scenario_by_name,
)


SUPPRESSOR_NODES = ((1, 0), (4, 0))


def _fmt_nodes(nodes: list[tuple[int, int]]) -> str:
    if not nodes:
        return "-"
    return ",".join(f"({x},{y})" for x, y in nodes)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor pair-kill diagnostic started {started}", flush=True)
    total_start = time.time()
    variant_limit = 48

    rows = pocket_wrap_suppressor_specificity_analysis(variant_limit=variant_limit)
    pair_rows = [row for row in rows if row.pair_add_kills]

    base_nodes, wrap_y = scenario_by_name("base", "taper-wrap")
    source_nodes: dict[str, set[tuple[int, int]]] = {}
    for variant_name, perturbed_nodes, _delta in procedural_geometry_variants(
        "base",
        "taper-wrap",
        base_nodes,
        wrap_y,
        variant_limit=variant_limit,
        style="local-morph",
    ):
        source_nodes[f"base:taper-wrap:{variant_name}"] = set(perturbed_nodes)

    print()
    print("Pocket-Wrap Pair-Kill Rows (variant_limit=48)")
    print("==============================================")
    print(
        "source | pocket_sig | overlap | targets_deep | "
        "base_outcome | add_1_0 | add_4_0 | add_both | "
        "base(deep,pocket,low) | add_both(deep,pocket,low)"
    )
    print(
        "-------|------------|---------|--------------|-------------|---------|---------|---------|"
        "----------------------|--------------------------"
    )
    for row in pair_rows:
        source = row.source_name.encode("unicode_escape").decode("ascii")
        print(
            f"{source} | "
            f"{int(row.pocket_signature)} | "
            f"{row.deep_overlap_count} | "
            f"{int(row.pair_targets_deep_cells)} | "
            f"{row.base_outcome} | "
            f"{row.add_1_0_outcome} | "
            f"{row.add_4_0_outcome} | "
            f"{row.add_both_outcome} | "
            f"({row.base_deep_gap:.2f},{row.base_pocket_gap:.2f},{row.base_low_degree_gap:.2f}) | "
            f"({row.add_both_deep_gap:.2f},{row.add_both_pocket_gap:.2f},{row.add_both_low_degree_gap:.2f})"
        )

    print()
    print("Deep-Cell Mapping For Pair-Kill Rows")
    print("====================================")
    print("source | deep_cells | suppressor∩deep | pocket_cells | suppressor∩pocket")
    print("-------|------------|------------------|-------------|------------------")
    for row in pair_rows:
        analysis_nodes = source_nodes[row.source_name]
        pocket_cells, deep_cells = pocket_candidate_cells(analysis_nodes, wrap_y=wrap_y)
        deep_overlap = sorted(cell for cell in SUPPRESSOR_NODES if cell in deep_cells)
        pocket_overlap = sorted(cell for cell in SUPPRESSOR_NODES if cell in pocket_cells)
        source = row.source_name.encode("unicode_escape").decode("ascii")
        print(
            f"{source} | "
            f"{_fmt_nodes(sorted(deep_cells))} | "
            f"{_fmt_nodes(deep_overlap)} | "
            f"{_fmt_nodes(sorted(pocket_cells))} | "
            f"{_fmt_nodes(pocket_overlap)}"
        )

    print()
    print(
        "pocket-wrap suppressor pair-kill diagnostic completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
