#!/usr/bin/env python3
"""Compare targeted pair-kill rows for gap, candidate-cell, and shell/core context."""

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
    _evaluate_extended_ge6_dpadj_nodes,
    _extended_ge6_dpadj_trees,
    _threshold_core_shell_group_totals,
    _threshold_core_shell_summary_from_totals,
    column_profile_geometry_metrics,
    local_shape_feature_bundle,
    pocket_candidate_cells,
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
    parser.add_argument("--variant-limit", type=int, default=64)
    parser.add_argument(
        "--targets",
        nargs="+",
        default=("local-morph-a", "local-morph-v", r"local-morph-\x8e"),
        help="Variant labels in escaped form (for example local-morph-\\x8e).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor pair-kill row compare started {started}", flush=True)
    total_start = time.time()

    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees(
        retained_weight=1.0,
        mode_retained_weight=None,
    )
    base_nodes, wrap_y = scenario_by_name("base", "taper-wrap")

    source_nodes: dict[str, set[tuple[int, int]]] = {}
    for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
        "base",
        "taper-wrap",
        base_nodes,
        wrap_y,
        variant_limit=args.variant_limit,
        style="local-morph",
    ):
        escaped_variant = _safe_label(variant_name)
        source_nodes[escaped_variant] = perturbed_nodes

    def evaluate_state(
        *,
        analysis_nodes: set[tuple[int, int]],
        scenario_name: str,
    ) -> tuple[str, float, float, float]:
        (
            _actual_label,
            outcome,
            _ge6_prediction,
            _dpadj_prediction,
            _ge6_only_fraction,
            _ge7_core_fraction,
            deep_gap,
            pocket_gap,
            low_degree_gap,
            _boundary_gap,
            _crosses_midline,
            _center_variation,
            _span_range,
        ) = _evaluate_extended_ge6_dpadj_nodes(
            nodes=analysis_nodes,
            wrap_y=wrap_y,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            pack_name="base",
            scenario_name=scenario_name,
            retained_weight=1.0,
        )
        return outcome, deep_gap, pocket_gap, low_degree_gap

    print()
    print("Pocket-Wrap Suppressor Pair-Kill Row Compare")
    print("============================================")
    print(f"variant_limit={args.variant_limit} targets={','.join(args.targets)}")
    print()

    for target in args.targets:
        if target not in source_nodes:
            print(f"{target} | MISSING in variant-limit={args.variant_limit}")
            continue

        source_name = f"base:taper-wrap:{target}"
        analysis_nodes = set(source_nodes[target])

        base_outcome, base_deep, base_pocket, base_low = evaluate_state(
            analysis_nodes=analysis_nodes,
            scenario_name=source_name,
        )
        add_1_nodes = set(analysis_nodes)
        add_1_nodes.add(SUPPRESSOR_NODES[0])
        add_1_outcome, _a1_deep, _a1_pocket, _a1_low = evaluate_state(
            analysis_nodes=add_1_nodes,
            scenario_name=f"{source_name}:add-1-0",
        )
        add_4_nodes = set(analysis_nodes)
        add_4_nodes.add(SUPPRESSOR_NODES[1])
        add_4_outcome, _a4_deep, _a4_pocket, _a4_low = evaluate_state(
            analysis_nodes=add_4_nodes,
            scenario_name=f"{source_name}:add-4-0",
        )
        add_both_nodes = set(analysis_nodes)
        add_both_nodes.update(SUPPRESSOR_NODES)
        add_both_outcome, add_both_deep, add_both_pocket, add_both_low = evaluate_state(
            analysis_nodes=add_both_nodes,
            scenario_name=f"{source_name}:add-both",
        )

        base_pocket_cells, base_deep_cells = pocket_candidate_cells(analysis_nodes, wrap_y=wrap_y)
        both_pocket_cells, both_deep_cells = pocket_candidate_cells(add_both_nodes, wrap_y=wrap_y)
        overlap = set(SUPPRESSOR_NODES).intersection(base_deep_cells)

        boundary_fraction, pocket_fraction, boundary_roughness, deep_pocket_fraction, *_rest = (
            local_shape_feature_bundle(analysis_nodes, wrap_y=wrap_y)
        )
        mean_center, center_range, center_total_variation, crosses_midline, span_range = (
            column_profile_geometry_metrics(analysis_nodes)
        )

        totals = _threshold_core_shell_group_totals(analysis_nodes, wrap_y=wrap_y)
        shell_summary = _threshold_core_shell_summary_from_totals(
            ensemble_name=source_name,
            graph_count=1,
            total_nodes=int(totals["total_nodes"]),
            group_counts=totals["group_counts"],  # type: ignore[arg-type]
            deep_counts=totals["deep_counts"],  # type: ignore[arg-type]
            pocket_counts=totals["pocket_counts"],  # type: ignore[arg-type]
            low_degree_counts=totals["low_degree_counts"],  # type: ignore[arg-type]
            boundary_sums=totals["boundary_sums"],  # type: ignore[arg-type]
            neighbor_degree_sums=totals["neighbor_degree_sums"],  # type: ignore[arg-type]
        )

        pocket_signature = base_pocket > 0.0 and base_deep <= 0.0 and base_low <= 0.0

        print(source_name)
        print(
            "  outcomes base/add1/add4/both: "
            f"{base_outcome}/{add_1_outcome}/{add_4_outcome}/{add_both_outcome}"
        )
        print(
            "  base gaps d/p/l + psig: "
            f"{base_deep:+.2f}/{base_pocket:+.2f}/{base_low:+.2f} "
            f"psig={pocket_signature}"
        )
        print(
            "  both gaps d/p/l: "
            f"{add_both_deep:+.2f}/{add_both_pocket:+.2f}/{add_both_low:+.2f}"
        )
        print(
            "  base deep/pocket + overlap: "
            f"{_format_cells(base_deep_cells)} / {_format_cells(base_pocket_cells)} "
            f"overlap={_format_cells(overlap)}"
        )
        print(
            "  both deep/pocket: "
            f"{_format_cells(both_deep_cells)} / {_format_cells(both_pocket_cells)}"
        )
        print(
            "  shape boundary/pocket/rough/deep: "
            f"{boundary_fraction:.3f}/{pocket_fraction:.3f}/{boundary_roughness:.3f}/{deep_pocket_fraction:.3f}"
        )
        print(
            "  profile mean/range/tv/cross/span: "
            f"{mean_center:.2f}/{center_range:.2f}/{center_total_variation:.2f}/"
            f"{('Y' if crosses_midline else 'n')}/{span_range}"
        )
        print(
            "  shell-core deep pocket low bdef: "
            f"{shell_summary.shell_deep_fraction:.2f}/{shell_summary.core_deep_fraction:.2f} "
            f"{shell_summary.shell_pocket_fraction:.2f}/{shell_summary.core_pocket_fraction:.2f} "
            f"{shell_summary.shell_low_degree_fraction:.2f}/{shell_summary.core_low_degree_fraction:.2f} "
            f"{shell_summary.shell_boundary_deficit_mean:.2f}/{shell_summary.core_boundary_deficit_mean:.2f}"
        )
        print()

    print(
        "pocket-wrap suppressor pair-kill row compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
