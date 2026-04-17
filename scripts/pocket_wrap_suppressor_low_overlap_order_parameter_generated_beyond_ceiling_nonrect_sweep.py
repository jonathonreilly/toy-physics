#!/usr/bin/env python3
"""Scan generated families for the first non-rect beyond-ceiling continuation."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_low_overlap_order_parameter_generated_non_guarded_pair_compare import (  # noqa: E402
    DEFAULT_NEARBY_ENSEMBLES,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_generated_support_collapse_guard_projection import (  # noqa: E402
    guarded_predict_branch,
    guarded_predict_subtype,
    is_support_collapse,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    build_rows_with_trees,
)
from toy_event_physics import _extended_ge6_dpadj_trees, benchmark_packs  # noqa: E402


CURRENT_RECT_PACK = "base"
CURRENT_RECT_SCENARIOS = ("rect-wrap", "rect-hard")
CURRENT_RECT_ENSEMBLES = ("wider", "ultra", "mega")
REFINED_CEILING = 10.0
HIGH_LOAD_THRESHOLD = 75.0
ENSEMBLE_ORDER = {
    ensemble_name: index for index, ensemble_name in enumerate(DEFAULT_NEARBY_ENSEMBLES)
}


@dataclass(frozen=True)
class ScanRow:
    pack_name: str
    scenario_name: str
    ensemble_name: str
    source_name: str
    actual_subtype: str
    predicted_subtype: str
    predicted_branch: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    anchor_closure_intensity_gap: float
    anchor_deep_share_gap: float
    high_bridge_right_count: float
    high_bridge_right_low_count: float
    edge_identity_event_count: float
    edge_identity_support_edge_density: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packs", nargs="+")
    parser.add_argument(
        "--ensembles",
        nargs="+",
        default=DEFAULT_NEARBY_ENSEMBLES,
    )
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def _capture_row(pack_name: str, scenario_name: str, row: object) -> ScanRow:
    return ScanRow(
        pack_name=pack_name,
        scenario_name=scenario_name,
        ensemble_name=getattr(row, "ensemble_name"),
        source_name=getattr(row, "source_name"),
        actual_subtype=getattr(row, "subtype"),
        predicted_subtype=guarded_predict_subtype(row),
        predicted_branch=guarded_predict_branch(row),
        support_load=float(getattr(row, "support_load")),
        closure_load=float(getattr(row, "closure_load")),
        mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
        anchor_closure_intensity_gap=float(getattr(row, "anchor_closure_intensity_gap")),
        anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
        high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
        high_bridge_right_low_count=float(getattr(row, "high_bridge_right_low_count")),
        edge_identity_event_count=float(getattr(row, "edge_identity_event_count")),
        edge_identity_support_edge_density=float(
            getattr(row, "edge_identity_support_edge_density")
        ),
    )


def _sort_key(row: ScanRow) -> tuple[int, str, str, str]:
    return (
        ENSEMBLE_ORDER.get(row.ensemble_name, len(ENSEMBLE_ORDER)),
        row.pack_name,
        row.scenario_name,
        row.source_name,
    )


def _row_label(row: ScanRow) -> str:
    return f"{row.pack_name}:{row.ensemble_name}:{row.source_name}"


def _format_counter(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}:{counter[key]}" for key in sorted(counter))


def _format_row_names(rows: list[ScanRow]) -> str:
    if not rows:
        return "none"
    return ",".join(_row_label(row) for row in sorted(rows, key=_sort_key))


def _append_sample(rows: list[ScanRow], row: ScanRow, *, limit: int) -> None:
    if len(rows) < limit:
        rows.append(row)


def _render_rows(title: str, rows: list[ScanRow]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in sorted(rows, key=_sort_key):
        lines.append(
            f"{_row_label(row)} actual={row.actual_subtype} predicted={row.predicted_subtype} "
            f"branch={row.predicted_branch} high_load={'Y' if row.closure_load >= HIGH_LOAD_THRESHOLD else 'n'}"
        )
        lines.append(f"  support_load={row.support_load:.3f}")
        lines.append(f"  closure_load={row.closure_load:.3f}")
        lines.append(f"  mid_anchor_closure_peak={row.mid_anchor_closure_peak:.3f}")
        lines.append(
            f"  anchor_closure_intensity_gap={row.anchor_closure_intensity_gap:.3f}"
        )
        lines.append(f"  anchor_deep_share_gap={row.anchor_deep_share_gap:.3f}")
        lines.append(f"  high_bridge_right_count={row.high_bridge_right_count:.3f}")
        lines.append(
            f"  high_bridge_right_low_count={row.high_bridge_right_low_count:.3f}"
        )
        lines.append(f"  edge_identity_event_count={row.edge_identity_event_count:.3f}")
        lines.append(
            "  edge_identity_support_edge_density="
            f"{row.edge_identity_support_edge_density:.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    pack_names = tuple(args.packs) if args.packs else None
    ensemble_names = tuple(args.ensembles)
    row_limit = args.row_limit
    started_at = datetime.now().isoformat(timespec="seconds")

    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()

    baseline_rect_count = 0
    baseline_rect_high_load_hits = 0
    baseline_rect_rows: list[ScanRow] = []

    other_rect_count = 0
    other_rect_high_load_hits = 0
    other_rect_rows: list[ScanRow] = []

    nonrect_count = 0
    nonrect_high_load_hits = 0
    nonrect_rows: list[ScanRow] = []
    nonrect_actual_counter: Counter[str] = Counter()
    nonrect_predicted_counter: Counter[str] = Counter()
    nonrect_scenario_counter: Counter[str] = Counter()

    nonrect_pair_only_failure_count = 0
    nonrect_pair_only_failure_high_load_hits = 0
    nonrect_pair_only_failure_rows: list[ScanRow] = []

    first_nonrect_row: ScanRow | None = None

    for pack_name, scenarios in benchmark_packs():
        if pack_names is not None and pack_name not in pack_names:
            continue
        for ensemble_name in ensemble_names:
            for scenario_name, _nodes, _wrap_y in scenarios:
                rows = build_rows_with_trees(
                    ensemble_name,
                    pack_name,
                    scenario_name,
                    ge6_tree=ge6_tree,
                    dpadj_tree=dpadj_tree,
                )
                for row in rows:
                    if is_support_collapse(row):
                        continue
                    if float(getattr(row, "mid_anchor_closure_peak")) <= REFINED_CEILING:
                        continue

                    captured = _capture_row(pack_name, scenario_name, row)
                    is_high_load = captured.closure_load >= HIGH_LOAD_THRESHOLD

                    if (
                        pack_name == CURRENT_RECT_PACK
                        and scenario_name in CURRENT_RECT_SCENARIOS
                        and ensemble_name in CURRENT_RECT_ENSEMBLES
                    ):
                        baseline_rect_count += 1
                        if is_high_load:
                            baseline_rect_high_load_hits += 1
                        _append_sample(baseline_rect_rows, captured, limit=row_limit)
                        continue

                    if "rect" in scenario_name:
                        other_rect_count += 1
                        if is_high_load:
                            other_rect_high_load_hits += 1
                        _append_sample(other_rect_rows, captured, limit=row_limit)
                        continue

                    nonrect_count += 1
                    if is_high_load:
                        nonrect_high_load_hits += 1
                    nonrect_actual_counter[captured.actual_subtype] += 1
                    nonrect_predicted_counter[captured.predicted_subtype] += 1
                    nonrect_scenario_counter[captured.scenario_name] += 1
                    _append_sample(nonrect_rows, captured, limit=row_limit)

                    if first_nonrect_row is None or _sort_key(captured) < _sort_key(first_nonrect_row):
                        first_nonrect_row = captured

                    if (
                        captured.actual_subtype == "pair-only-sensitive"
                        and captured.predicted_subtype == "add1-sensitive"
                    ):
                        nonrect_pair_only_failure_count += 1
                        if is_high_load:
                            nonrect_pair_only_failure_high_load_hits += 1
                        _append_sample(
                            nonrect_pair_only_failure_rows,
                            captured,
                            limit=row_limit,
                        )

    print(f"generated beyond-ceiling non-rect sweep started {started_at}")
    print()
    print("Generated Beyond-Ceiling Non-Rect Sweep")
    print("=======================================")
    print(
        "packs="
        + ",".join(
            pack_name
            for pack_name, _scenarios in benchmark_packs()
            if pack_names is None or pack_name in pack_names
        )
    )
    print("ensembles=" + ",".join(ensemble_names))
    print("refined_ceiling_rule=mid_anchor_closure_peak > 10.000")
    print("high_load_rule=closure_load >= 75.000")
    print(
        f"baseline_current_rect_rows={baseline_rect_count} "
        f"high_load_hits={baseline_rect_high_load_hits}/{baseline_rect_count}"
    )
    print("baseline_current_rect_samples=" + _format_row_names(baseline_rect_rows))
    print(
        f"other_rect_beyond_ceiling_rows={other_rect_count} "
        f"high_load_hits={other_rect_high_load_hits}/{other_rect_count}"
    )
    print("other_rect_beyond_ceiling_samples=" + _format_row_names(other_rect_rows))
    print(
        f"nonrect_beyond_ceiling_rows={nonrect_count} "
        f"high_load_hits={nonrect_high_load_hits}/{nonrect_count}"
    )
    print("nonrect_beyond_ceiling_samples=" + _format_row_names(nonrect_rows))
    print("nonrect_beyond_ceiling_actual_counts=" + _format_counter(nonrect_actual_counter))
    print(
        "nonrect_beyond_ceiling_predicted_counts="
        + _format_counter(nonrect_predicted_counter)
    )
    print(
        "nonrect_beyond_ceiling_scenario_counts="
        + _format_counter(nonrect_scenario_counter)
    )
    print(
        f"nonrect_pair_only_failure_rows={nonrect_pair_only_failure_count} "
        f"high_load_hits={nonrect_pair_only_failure_high_load_hits}/"
        f"{nonrect_pair_only_failure_count}"
    )
    print(
        "nonrect_pair_only_failure_samples="
        + _format_row_names(nonrect_pair_only_failure_rows)
    )
    print(
        "first_nonrect_row="
        + (_row_label(first_nonrect_row) if first_nonrect_row is not None else "none")
    )

    if nonrect_count == 0:
        print(
            "conclusion=no non-rect beyond-ceiling non-collapse row appears in the scanned guardrail, "
            "so the current closure_load >= 75.000 continuation stays rect-local on this slice"
        )
    elif nonrect_high_load_hits == nonrect_count:
        print(
            "conclusion=non-rect beyond-ceiling rows do appear, and all of them keep the current "
            "closure_load >= 75.000 clause"
        )
    elif nonrect_high_load_hits > 0:
        print(
            "conclusion=non-rect beyond-ceiling rows do appear, but only part of that continuation "
            "keeps closure_load >= 75.000"
        )
    else:
        print(
            "conclusion=non-rect beyond-ceiling rows do appear, and they all break the current "
            "closure_load >= 75.000 clause"
        )

    print()
    print(_render_rows("Current rect baseline samples", baseline_rect_rows))
    print()
    print(_render_rows("Other rect-family beyond-ceiling samples", other_rect_rows))
    print()
    print(_render_rows("Non-rect beyond-ceiling samples", nonrect_rows))
    print()
    print(_render_rows("Non-rect pair-only transfer-failure samples", nonrect_pair_only_failure_rows))


if __name__ == "__main__":
    main()
