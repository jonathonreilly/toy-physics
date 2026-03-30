#!/usr/bin/env python3
"""Project the exact low-overlap branch law onto generated-family ensembles."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import make_dataclass
from datetime import datetime
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_order_parameter_full_bucket_exact_projection import (  # noqa: E402
    predict_branch,
    predict_subtype,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    edge_identity_signature,
    support_roles,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    high_bridge_band_metrics,
    high_bridge_cells,
    support_edge_identity_own_metrics,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    candidate_anchor_metrics,
)
from toy_event_physics import (  # noqa: E402
    _evaluate_extended_ge6_dpadj_nodes,
    _extended_ge6_dpadj_trees,
    canonical_generated_ensemble_specs,
    generated_ensemble_spec,
    pocket_candidate_cells,
    pocket_wrap_suppressor_subtype_from_outcomes,
    procedural_geometry_variants,
    randomized_geometry_variants,
    scenario_by_name,
)


SUPPRESSOR_NODES = ((1, 0), (4, 0))


def _ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def _support_edge_identity_metrics(nodes: set[tuple[int, int]]) -> dict[str, float]:
    try:
        return support_edge_identity_own_metrics(nodes)
    except KeyError:
        pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
        roles = support_roles(nodes, pocket_cells, deep_cells)
        _events, numeric = edge_identity_signature(nodes)
        return {
            "support_role_bridge_count": float(
                sum(1 for role in roles.values() if role == "bridge")
            ),
            "edge_identity_closed_pair_count": float(
                numeric.get("edge_identity_closed_pair_count", 0.0)
            ),
            "edge_identity_event_count": float(
                numeric.get("edge_identity_event_count", 0.0)
            ),
            "edge_identity_support_edge_density": float(
                numeric.get("edge_identity_support_edge_density", 0.0)
            ),
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack-name", default="base")
    parser.add_argument("--scenario-name", default="taper-wrap")
    parser.add_argument(
        "--ensembles",
        nargs="+",
        default=[spec[0] for spec in canonical_generated_ensemble_specs()[:3]],
    )
    return parser


def _evaluate_outcome(
    *,
    nodes: set[tuple[int, int]],
    wrap_y: bool,
    ge6_tree: object,
    dpadj_tree: object,
    pack_name: str,
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
        nodes=nodes,
        wrap_y=wrap_y,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
        pack_name=pack_name,
        scenario_name=scenario_name,
        retained_weight=1.0,
    )
    return outcome, deep_gap, pocket_gap, low_degree_gap


def _variant_entries(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
) -> tuple[bool, list[tuple[str, set[tuple[int, int]], str]]]:
    _name, geometry_limit, procedural_limit, procedural_styles = generated_ensemble_spec(
        ensemble_name
    )
    base_nodes, wrap_y = scenario_by_name(pack_name, scenario_name)
    entries: list[tuple[str, set[tuple[int, int]], str]] = []
    for variant_name, perturbed_nodes, _node_delta in randomized_geometry_variants(
        pack_name,
        scenario_name,
        base_nodes,
        wrap_y,
        variant_limit=geometry_limit,
    ):
        entries.append(
            (f"{pack_name}:{scenario_name}:{variant_name}", set(perturbed_nodes), "geometry")
        )
    for style in tuple(dict.fromkeys(procedural_styles)):
        for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
            pack_name,
            scenario_name,
            base_nodes,
            wrap_y,
            variant_limit=procedural_limit,
            style=style,
        ):
            entries.append(
                (f"{pack_name}:{scenario_name}:{variant_name}", set(perturbed_nodes), style)
            )
    entries.sort(key=lambda item: (item[2], item[0]))
    return wrap_y, entries


def build_rows_with_trees(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
) -> list[object]:
    wrap_y, entries = _variant_entries(ensemble_name, pack_name, scenario_name)
    row_cls = make_dataclass(
        "GeneratedEnsembleExactLawRow",
        [
            ("ensemble_name", str),
            ("style", str),
            ("source_name", str),
            ("subtype", str),
            ("support_load", float),
            ("closure_load", float),
            ("mid_anchor_closure_peak", float),
            ("anchor_closure_intensity_gap", float),
            ("anchor_deep_share_gap", float),
            ("high_bridge_high_count", float),
            ("high_bridge_right_count", float),
            ("high_bridge_right_low_count", float),
            ("edge_identity_event_count", float),
            ("edge_identity_support_edge_density", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for source_name, nodes, style in entries:
        base_outcome, deep_gap, pocket_gap, low_degree_gap = _evaluate_outcome(
            nodes=nodes,
            wrap_y=wrap_y,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            pack_name=pack_name,
            scenario_name=f"{ensemble_name}:{source_name}:base",
        )
        if base_outcome != "dpadj-only":
            continue
        pocket_signature = pocket_gap > 0.0 and deep_gap <= 0.0 and low_degree_gap <= 0.0
        if pocket_signature:
            continue

        add1_nodes = set(nodes)
        add1_nodes.add(SUPPRESSOR_NODES[0])
        add4_nodes = set(nodes)
        add4_nodes.add(SUPPRESSOR_NODES[1])
        add1_outcome, _d1, _p1, _l1 = _evaluate_outcome(
            nodes=add1_nodes,
            wrap_y=wrap_y,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            pack_name=pack_name,
            scenario_name=f"{ensemble_name}:{source_name}:add-1-0",
        )
        add4_outcome, _d4, _p4, _l4 = _evaluate_outcome(
            nodes=add4_nodes,
            wrap_y=wrap_y,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            pack_name=pack_name,
            scenario_name=f"{ensemble_name}:{source_name}:add-4-0",
        )
        subtype = pocket_wrap_suppressor_subtype_from_outcomes(
            add_1_0_outcome=add1_outcome,
            add_4_0_outcome=add4_outcome,
        )

        own_metrics = _support_edge_identity_metrics(nodes)
        band_metrics = high_bridge_band_metrics(high_bridge_cells(nodes))
        anchor = candidate_anchor_metrics(nodes)
        mid_count = float(anchor["mid_candidate_count"])
        left_count = float(anchor["left_candidate_count"])
        mid_peak = float(anchor["mid_candidate_bridge_bridge_closed_pair_max"])
        left_peak = float(anchor["left_candidate_bridge_bridge_closed_pair_max"])

        rows.append(
            row_cls(
                ensemble_name=ensemble_name,
                style=style,
                source_name=source_name,
                subtype=subtype,
                support_load=float(own_metrics["support_role_bridge_count"]),
                closure_load=float(own_metrics["edge_identity_closed_pair_count"]),
                mid_anchor_closure_peak=mid_peak,
                anchor_closure_intensity_gap=_ratio(mid_peak, mid_count)
                - _ratio(left_peak, left_count),
                anchor_deep_share_gap=_ratio(
                    float(anchor["mid_candidate_deep_count"]), mid_count
                )
                - _ratio(float(anchor["left_candidate_deep_count"]), left_count),
                high_bridge_high_count=float(band_metrics["high_bridge_high_count"]),
                high_bridge_right_count=float(band_metrics["high_bridge_right_count"]),
                high_bridge_right_low_count=float(band_metrics["high_bridge_right_low_count"]),
                edge_identity_event_count=float(own_metrics["edge_identity_event_count"]),
                edge_identity_support_edge_density=float(
                    own_metrics["edge_identity_support_edge_density"]
                ),
            )
        )

    rows.sort(key=lambda item: (item.style, item.source_name))
    return rows


def build_rows(ensemble_name: str, pack_name: str, scenario_name: str) -> list[object]:
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees(retained_weight=1.0)
    return build_rows_with_trees(
        ensemble_name,
        pack_name,
        scenario_name,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )


def _format_counts(rows: list[object], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def render_ensemble_block(ensemble_name: str, rows: list[object]) -> tuple[str, int]:
    misclassified = [row for row in rows if predict_subtype(row) != getattr(row, "subtype")]
    ambiguous = [row for row in rows if predict_subtype(row) == "ambiguous"]
    unmatched = [row for row in rows if predict_subtype(row) == "unmatched"]

    style_counts = Counter(getattr(row, "style") for row in rows)
    style_text = ", ".join(
        f"{style}:{style_counts[style]}" for style in sorted(style_counts)
    )

    lines = [
        f"ensemble={ensemble_name}",
        "-" * (9 + len(ensemble_name)),
        f"rows={len(rows)} ({_format_counts(rows)})",
        f"styles={style_text if style_text else 'none'}",
        f"misclassified={len(misclassified)} ({_format_counts(misclassified)})",
        f"ambiguous={len(ambiguous)} ({_format_counts(ambiguous)})",
        f"unmatched={len(unmatched)} ({_format_counts(unmatched)})",
        "predicted_branches:",
    ]
    for branch in (
        "high-closure-add4",
        "high-closure-pair-only",
        "outside-gate-pair-only",
        "outside-gate-add4",
        "outside-gate-add1-default",
    ):
        branch_rows = [row for row in rows if predict_branch(row) == branch]
        lines.append(f"  {branch}: {len(branch_rows)} ({_format_counts(branch_rows)})")

    if misclassified:
        lines.append("misclassified_rows:")
        for row in misclassified[:12]:
            lines.append(
                f"  {getattr(row, 'style')}:{getattr(row, 'source_name')} "
                f"actual={getattr(row, 'subtype')} predicted={predict_subtype(row)} "
                f"branch={predict_branch(row)} mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
                f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
                f"closure_load={float(getattr(row, 'closure_load')):.3f}"
            )
        if len(misclassified) > 12:
            lines.append(f"  ... {len(misclassified) - 12} more")
    else:
        lines.append("misclassified_rows: none")

    return "\n".join(lines), len(misclassified)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(
        f"exact low-overlap generated-ensemble transfer check started {started}",
        flush=True,
    )
    total_start = time.time()

    ensemble_names = list(dict.fromkeys(args.ensembles))
    blocks: list[str] = []
    failures: dict[str, int] = {}
    rows_by_ensemble: dict[str, list[object]] = {}
    for ensemble_name in ensemble_names:
        rows = build_rows(ensemble_name, args.pack_name, args.scenario_name)
        rows_by_ensemble[ensemble_name] = rows
        block, miscount = render_ensemble_block(ensemble_name, rows)
        blocks.append(block)
        failures[ensemble_name] = miscount

    first_failure_ensemble = next(
        (name for name in ensemble_names if failures.get(name, 0) > 0),
        None,
    )
    totals = defaultdict(int)
    for rows in rows_by_ensemble.values():
        totals["rows"] += len(rows)
        totals["misclassified"] += sum(
            1 for row in rows if predict_subtype(row) != getattr(row, "subtype")
        )
        totals["ambiguous"] += sum(1 for row in rows if predict_subtype(row) == "ambiguous")
        totals["unmatched"] += sum(1 for row in rows if predict_subtype(row) == "unmatched")

    print()
    print("Exact Low-Overlap Law Generated-Ensemble Transfer Check")
    print("=======================================================")
    print(f"target={args.pack_name}:{args.scenario_name}")
    print("ensembles=" + ",".join(ensemble_names))
    print(f"rows_total={totals['rows']}")
    print(f"misclassified_total={totals['misclassified']}")
    print(f"ambiguous_total={totals['ambiguous']}")
    print(f"unmatched_total={totals['unmatched']}")
    if first_failure_ensemble is None:
        print("first_failure_ensemble=none within tested ensembles")
    else:
        print(f"first_failure_ensemble={first_failure_ensemble}")
    print()
    print("\n\n".join(blocks))
    print()
    print(
        "exact low-overlap generated-ensemble transfer check completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
