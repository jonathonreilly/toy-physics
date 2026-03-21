#!/usr/bin/env python3
"""Dump the deeper pair-kill rows and their pocket/deep support cells."""

from __future__ import annotations

import argparse
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


def _safe_label(text: str) -> str:
    return text.encode("unicode_escape").decode("ascii")


def _format_cells(cells: set[tuple[int, int]]) -> str:
    return ",".join(f"({x},{y})" for x, y in sorted(cells)) or "-"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant-limit", type=int, default=56)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor pair-kill diagnostic started {started}", flush=True)
    total_start = time.time()

    rows = pocket_wrap_suppressor_specificity_analysis(variant_limit=args.variant_limit)
    pair_rows = [row for row in rows if row.pair_add_kills]

    nodes, wrap_y = scenario_by_name("base", "taper-wrap")
    source_nodes: dict[str, set[tuple[int, int]]] = {}
    for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
        "base",
        "taper-wrap",
        nodes,
        wrap_y,
        variant_limit=args.variant_limit,
        style="local-morph",
    ):
        source_nodes[f"base:taper-wrap:{variant_name}"] = perturbed_nodes

    print()
    print("Pocket-Wrap Suppressor Pair-Kill Diagnostic")
    print("===========================================")
    print(
        f"variant_limit={args.variant_limit} rows={len(rows)} pair_kill={len(pair_rows)} "
        f"with_zero_overlap={sum(1 for row in pair_rows if row.deep_overlap_count == 0)}"
    )
    print(
        "source                                 | psig | dov | add1/add4/both          | "
        "base deep/pocket       | both deep/pocket       | overlap"
    )
    print(
        "---------------------------------------+------+-----+-------------------------+"
        "------------------------+------------------------+----------------"
    )

    for row in pair_rows:
        analysis_nodes = set(source_nodes[row.source_name])
        base_pocket_cells, base_deep_cells = pocket_candidate_cells(analysis_nodes, wrap_y=wrap_y)
        add_both_nodes = set(analysis_nodes)
        add_both_nodes.update(SUPPRESSOR_NODES)
        both_pocket_cells, both_deep_cells = pocket_candidate_cells(add_both_nodes, wrap_y=wrap_y)
        overlap = sorted(set(SUPPRESSOR_NODES).intersection(base_deep_cells))
        overlap_text = ",".join(f"({x},{y})" for x, y in overlap) or "-"
        print(
            f"{_safe_label(row.source_name):<39.39} | "
            f"{('Y' if row.pocket_signature else 'n'):<4} | "
            f"{row.deep_overlap_count:>3} | "
            f"{row.add_1_0_outcome:<7.7}/{row.add_4_0_outcome:<7.7}/{row.add_both_outcome:<7.7} | "
            f"{_format_cells(base_deep_cells):<22.22} / {_format_cells(base_pocket_cells):<22.22} | "
            f"{_format_cells(both_deep_cells):<22.22} / {_format_cells(both_pocket_cells):<22.22} | "
            f"{overlap_text:<16.16}"
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
