#!/usr/bin/env python3
"""Compare the deepest exhausted large slice against the current base late branch floors."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
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

from pocket_wrap_suppressor_low_overlap_order_parameter_base_late_branch_direct_compare import (  # noqa: E402
    LATE_BRANCH_CLASS,
    build_rows as build_base_late_compare_rows,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    build_rows_with_trees,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_generated_support_collapse_guard_projection import (  # noqa: E402
    guarded_predict_branch,
    guarded_predict_subtype,
    is_support_collapse,
)
from toy_event_physics import _extended_ge6_dpadj_trees, benchmark_packs  # noqa: E402


BASE_LATE_LOG = Path(
    "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-nonrect-sweep-base-peta-exa.txt"
)
BASE_REFERENCE_LOG = Path(
    "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-anchor-band-beyond-ceiling-followon.txt"
)


@dataclass(frozen=True)
class ExhaustedSliceRow:
    scenario_name: str
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
    support_gap: float
    closure_gap: float
    mid_peak_gap: float
    total_gap: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pack-name", default="large")
    parser.add_argument("--ensemble-name", default="exa")
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _format_counts(rows: list[ExhaustedSliceRow], attr: str = "actual_subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _candidate_scenarios(pack_name: str) -> list[str]:
    for current_pack_name, scenarios in benchmark_packs():
        if current_pack_name != pack_name:
            continue
        return [
            scenario_name
            for scenario_name, _nodes, _wrap_y in scenarios
            if "rect" not in scenario_name
        ]
    raise KeyError(f"unknown benchmark pack {pack_name}")


def _late_branch_floors() -> tuple[float, float, float]:
    base_rows = build_base_late_compare_rows(BASE_LATE_LOG, BASE_REFERENCE_LOG)
    late_rows = [row for row in base_rows if row.cohort == LATE_BRANCH_CLASS]
    return (
        min(row.support_load for row in late_rows),
        min(row.closure_load for row in late_rows),
        min(row.mid_anchor_closure_peak for row in late_rows),
    )


def build_rows(pack_name: str, ensemble_name: str) -> tuple[list[ExhaustedSliceRow], tuple[float, float, float]]:
    support_floor, closure_floor, mid_peak_floor = _late_branch_floors()
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
    rows: list[ExhaustedSliceRow] = []
    for scenario_name in _candidate_scenarios(pack_name):
        generated_rows = build_rows_with_trees(
            ensemble_name,
            pack_name,
            scenario_name,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
        )
        for row in generated_rows:
            if is_support_collapse(row):
                continue
            support_gap = max(0.0, support_floor - float(getattr(row, "support_load")))
            closure_gap = max(0.0, closure_floor - float(getattr(row, "closure_load")))
            mid_peak_gap = max(
                0.0,
                mid_peak_floor - float(getattr(row, "mid_anchor_closure_peak")),
            )
            rows.append(
                ExhaustedSliceRow(
                    scenario_name=scenario_name,
                    source_name=getattr(row, "source_name"),
                    actual_subtype=getattr(row, "subtype"),
                    predicted_subtype=guarded_predict_subtype(row),
                    predicted_branch=guarded_predict_branch(row),
                    support_load=float(getattr(row, "support_load")),
                    closure_load=float(getattr(row, "closure_load")),
                    mid_anchor_closure_peak=float(
                        getattr(row, "mid_anchor_closure_peak")
                    ),
                    anchor_closure_intensity_gap=float(
                        getattr(row, "anchor_closure_intensity_gap")
                    ),
                    anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                    high_bridge_right_count=float(
                        getattr(row, "high_bridge_right_count")
                    ),
                    high_bridge_right_low_count=float(
                        getattr(row, "high_bridge_right_low_count")
                    ),
                    edge_identity_event_count=float(
                        getattr(row, "edge_identity_event_count")
                    ),
                    edge_identity_support_edge_density=float(
                        getattr(row, "edge_identity_support_edge_density")
                    ),
                    support_gap=support_gap,
                    closure_gap=closure_gap,
                    mid_peak_gap=mid_peak_gap,
                    total_gap=support_gap + closure_gap + mid_peak_gap,
                )
            )
    rows.sort(
        key=lambda row: (
            row.total_gap,
            row.mid_peak_gap,
            row.closure_gap,
            row.support_gap,
            row.source_name,
        )
    )
    return rows, (support_floor, closure_floor, mid_peak_floor)


def _render_rows(title: str, rows: list[ExhaustedSliceRow]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{row.source_name} scenario={row.scenario_name} actual={row.actual_subtype} "
            f"predicted={row.predicted_subtype} branch={row.predicted_branch}"
        )
        lines.append(
            f"  support_load={row.support_load:.3f} closure_load={row.closure_load:.3f} "
            f"mid_anchor_closure_peak={row.mid_anchor_closure_peak:.3f}"
        )
        lines.append(
            "  gaps="
            f"support:{row.support_gap:.3f} "
            f"closure:{row.closure_gap:.3f} "
            f"mid_peak:{row.mid_peak_gap:.3f} "
            f"total:{row.total_gap:.3f}"
        )
        lines.append(
            f"  anchor_closure_intensity_gap={row.anchor_closure_intensity_gap:.3f} "
            f"anchor_deep_share_gap={row.anchor_deep_share_gap:.3f} "
            f"high_bridge_right_count={row.high_bridge_right_count:.3f} "
            f"high_bridge_right_low_count={row.high_bridge_right_low_count:.3f}"
        )
        lines.append(
            "  edge_identity_event_count="
            f"{row.edge_identity_event_count:.3f} "
            f"edge_identity_support_edge_density={row.edge_identity_support_edge_density:.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"large exhausted slice compare started {started}", flush=True)
    total_start = time.time()

    rows, (support_floor, closure_floor, mid_peak_floor) = build_rows(
        args.pack_name,
        args.ensemble_name,
    )
    closure_gate_rows = [row for row in rows if row.closure_load >= closure_floor]
    beyond_ceiling_rows = [
        row for row in rows if row.mid_anchor_closure_peak > 10.0
    ]
    top_gap_rows = rows[: args.row_limit]
    top_closure_rows = sorted(
        rows,
        key=lambda row: (
            -row.closure_load,
            -row.mid_anchor_closure_peak,
            -row.support_load,
            row.source_name,
        ),
    )[: args.row_limit]
    top_mid_peak_rows = sorted(
        rows,
        key=lambda row: (
            -row.mid_anchor_closure_peak,
            -row.closure_load,
            -row.support_load,
            row.source_name,
        ),
    )[: args.row_limit]

    print()
    print("Large Exhausted Slice Compare")
    print("============================")
    print(f"pack={args.pack_name}")
    print(f"ensemble={args.ensemble_name}")
    print(
        "late_branch_floors="
        f"support_load>={support_floor:.3f}, "
        f"closure_load>={closure_floor:.3f}, "
        f"mid_anchor_closure_peak>={mid_peak_floor:.3f}"
    )
    print(f"rows_total={len(rows)} ({_format_counts(rows)})")
    print(
        f"closure_gate_rows={len(closure_gate_rows)} ({_format_counts(closure_gate_rows)})"
    )
    print(
        f"beyond_ceiling_rows={len(beyond_ceiling_rows)} ({_format_counts(beyond_ceiling_rows)})"
    )
    if rows:
        best = rows[0]
        print(
            "best_total_gap_row="
            f"{best.source_name} total_gap={best.total_gap:.3f} "
            f"(support_gap={best.support_gap:.3f}, closure_gap={best.closure_gap:.3f}, "
            f"mid_peak_gap={best.mid_peak_gap:.3f})"
        )
    print()
    print(_render_rows("Lowest total-gap rows", top_gap_rows))
    print()
    print(_render_rows("Highest closure-load rows", top_closure_rows))
    print()
    print(_render_rows("Highest mid-anchor-closure rows", top_mid_peak_rows))
    print()
    print(
        "large exhausted slice compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
