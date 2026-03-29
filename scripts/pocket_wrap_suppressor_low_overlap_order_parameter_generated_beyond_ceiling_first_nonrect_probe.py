#!/usr/bin/env python3
"""Find the first non-rect beyond-ceiling generated row on a wider guardrail."""

from __future__ import annotations

import argparse
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


HIGH_LOAD_THRESHOLD = 75.0
REFINED_CEILING = 10.0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packs", nargs="+", default=["large"])
    parser.add_argument(
        "--ensembles",
        nargs="+",
        default=DEFAULT_NEARBY_ENSEMBLES,
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    pack_names = tuple(args.packs)
    ensemble_names = tuple(args.ensembles)
    started_at = datetime.now().isoformat(timespec="seconds")

    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()

    scanned_combinations = 0
    first_hit: tuple[str, str, str, object] | None = None

    for pack_name, scenarios in benchmark_packs():
        if pack_name not in pack_names:
            continue
        for ensemble_name in ensemble_names:
            for scenario_name, _nodes, _wrap_y in scenarios:
                if "rect" in scenario_name:
                    continue
                scanned_combinations += 1
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
                    first_hit = (pack_name, scenario_name, ensemble_name, row)
                    break
                if first_hit is not None:
                    break
            if first_hit is not None:
                break
        if first_hit is not None:
            break

    print(f"generated beyond-ceiling first non-rect probe started {started_at}")
    print()
    print("Generated Beyond-Ceiling First Non-Rect Probe")
    print("=============================================")
    print("packs=" + ",".join(pack_names))
    print("ensembles=" + ",".join(ensemble_names))
    print("refined_ceiling_rule=mid_anchor_closure_peak > 10.000")
    print("high_load_rule=closure_load >= 75.000")
    print(f"scanned_nonrect_combinations={scanned_combinations}")

    if first_hit is None:
        print("first_nonrect_row=none")
        print(
            "conclusion=no non-rect beyond-ceiling non-collapse row appeared on the scanned guardrail"
        )
        return

    pack_name, scenario_name, ensemble_name, row = first_hit
    closure_load = float(getattr(row, "closure_load"))
    support_load = float(getattr(row, "support_load"))
    mid_anchor_closure_peak = float(getattr(row, "mid_anchor_closure_peak"))
    anchor_closure_intensity_gap = float(getattr(row, "anchor_closure_intensity_gap"))
    anchor_deep_share_gap = float(getattr(row, "anchor_deep_share_gap"))
    high_bridge_right_count = float(getattr(row, "high_bridge_right_count"))
    high_bridge_right_low_count = float(getattr(row, "high_bridge_right_low_count"))
    edge_identity_event_count = float(getattr(row, "edge_identity_event_count"))
    edge_identity_support_edge_density = float(
        getattr(row, "edge_identity_support_edge_density")
    )
    predicted_subtype = guarded_predict_subtype(row)
    predicted_branch = guarded_predict_branch(row)

    print(
        "first_nonrect_row="
        + f"{pack_name}:{ensemble_name}:{getattr(row, 'source_name')}"
    )
    print(f"first_nonrect_scenario={scenario_name}")
    print(f"actual_subtype={getattr(row, 'subtype')}")
    print(f"predicted_subtype={predicted_subtype}")
    print(f"predicted_branch={predicted_branch}")
    print(f"high_load_hit={'Y' if closure_load >= HIGH_LOAD_THRESHOLD else 'n'}")
    print(f"support_load={support_load:.3f}")
    print(f"closure_load={closure_load:.3f}")
    print(f"mid_anchor_closure_peak={mid_anchor_closure_peak:.3f}")
    print(f"anchor_closure_intensity_gap={anchor_closure_intensity_gap:.3f}")
    print(f"anchor_deep_share_gap={anchor_deep_share_gap:.3f}")
    print(f"high_bridge_right_count={high_bridge_right_count:.3f}")
    print(f"high_bridge_right_low_count={high_bridge_right_low_count:.3f}")
    print(f"edge_identity_event_count={edge_identity_event_count:.3f}")
    print(
        "edge_identity_support_edge_density="
        f"{edge_identity_support_edge_density:.3f}"
    )

    if closure_load >= HIGH_LOAD_THRESHOLD:
        print(
            "conclusion=the first non-rect beyond-ceiling row keeps the current closure_load >= 75.000 clause"
        )
    else:
        print(
            "conclusion=the first non-rect beyond-ceiling row breaks the current closure_load >= 75.000 clause"
        )


if __name__ == "__main__":
    main()
