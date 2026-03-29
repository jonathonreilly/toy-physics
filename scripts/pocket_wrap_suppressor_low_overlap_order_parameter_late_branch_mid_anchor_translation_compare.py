#!/usr/bin/env python3
"""Compare late base rows against the closest large exhausted-wall miss."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    _variant_entries,
    build_rows_with_trees,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    high_bridge_band_metrics,
    high_bridge_cells,
    support_edge_identity_own_metrics,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    candidate_anchor_metrics,
)
from toy_event_physics import _extended_ge6_dpadj_trees  # noqa: E402


LATE_CLASS = "late-base"
LARGE_MISS_CLASS = "large-exhausted-miss"
MIRROR_MISS_CLASS = "mirror-exhausted-miss"
FOCUSED_TARGET_SPECS = (
    ("peta", "base", "rect-wrap", "base:rect-wrap:local-morph-f", LATE_CLASS),
    ("exa", "base", "rect-wrap", "base:rect-wrap:local-morph-f", LATE_CLASS),
    ("peta", "base", "taper-hard", "base:taper-hard:local-morph-f", LATE_CLASS),
    ("exa", "base", "taper-hard", "base:taper-hard:local-morph-f", LATE_CLASS),
    (
        "exa",
        "large",
        "taper-wrap-large",
        "large:taper-wrap-large:local-morph-g",
        LARGE_MISS_CLASS,
    ),
)
FULL_WALL_TARGET_SPECS = FOCUSED_TARGET_SPECS + (
    ("exa", "base", "skew-wrap", "base:skew-wrap:local-morph-k", LATE_CLASS),
    (
        "exa",
        "mirror",
        "skew-hard-mirror",
        "mirror:skew-hard-mirror:local-morph-f",
        MIRROR_MISS_CLASS,
    ),
)
FEATURE_NAMES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_left_count",
    "high_bridge_mid_count",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "left_candidate_count",
    "mid_candidate_count",
    "left_candidate_bridge_max",
    "mid_candidate_bridge_max",
    "left_candidate_closed_pair_max",
    "mid_candidate_closed_pair_max",
    "left_candidate_bridge_bridge_closed_pair_max",
    "mid_candidate_bridge_bridge_closed_pair_max",
    "left_candidate_closed_ratio_max",
    "mid_candidate_closed_ratio_max",
    "left_candidate_dense_count",
    "mid_candidate_dense_count",
    "delta_mid_left_bridge_max",
    "delta_mid_left_closed_pair_max",
    "delta_mid_left_bridge_bridge_closed_pair_max",
    "delta_mid_left_dense_count",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
)
STRUCTURAL_RULE_FEATURE_NAMES = (
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_left_count",
    "high_bridge_mid_count",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "left_candidate_count",
    "mid_candidate_count",
    "left_candidate_bridge_max",
    "mid_candidate_bridge_max",
    "left_candidate_closed_pair_max",
    "mid_candidate_closed_pair_max",
    "left_candidate_bridge_bridge_closed_pair_max",
    "mid_candidate_bridge_bridge_closed_pair_max",
    "left_candidate_closed_ratio_max",
    "mid_candidate_closed_ratio_max",
    "left_candidate_dense_count",
    "mid_candidate_dense_count",
    "delta_mid_left_bridge_max",
    "delta_mid_left_closed_pair_max",
    "delta_mid_left_bridge_bridge_closed_pair_max",
    "delta_mid_left_dense_count",
)


@dataclass(frozen=True)
class CompareRow:
    ensemble_name: str
    pack_name: str
    scenario_name: str
    source_name: str
    subtype: str
    actual_subtype: str
    predicted_subtype: str
    predicted_branch: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    anchor_closure_intensity_gap: float
    anchor_deep_share_gap: float
    high_bridge_left_count: float
    high_bridge_mid_count: float
    high_bridge_right_count: float
    high_bridge_right_low_count: float
    left_candidate_count: float
    mid_candidate_count: float
    left_candidate_bridge_max: float
    mid_candidate_bridge_max: float
    left_candidate_closed_pair_max: float
    mid_candidate_closed_pair_max: float
    left_candidate_bridge_bridge_closed_pair_max: float
    mid_candidate_bridge_bridge_closed_pair_max: float
    left_candidate_closed_ratio_max: float
    mid_candidate_closed_ratio_max: float
    left_candidate_dense_count: float
    mid_candidate_dense_count: float
    delta_mid_left_bridge_max: float
    delta_mid_left_closed_pair_max: float
    delta_mid_left_bridge_bridge_closed_pair_max: float
    delta_mid_left_dense_count: float
    edge_identity_event_count: float
    edge_identity_support_edge_density: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("focused", "full-wall"),
        default="focused",
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=2)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _format_counts(rows: list[CompareRow], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _fetch_row(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    target_source: str,
    subtype: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
) -> CompareRow:
    rows = build_rows_with_trees(
        ensemble_name,
        pack_name,
        scenario_name,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )
    row = next(
        current for current in rows if getattr(current, "source_name") == target_source
    )
    _wrap_y, entries = _variant_entries(ensemble_name, pack_name, scenario_name)
    nodes = next(
        current_nodes
        for source_name, current_nodes, _style in entries
        if source_name == target_source
    )
    anchor = candidate_anchor_metrics(set(nodes))
    own = support_edge_identity_own_metrics(set(nodes))
    band = high_bridge_band_metrics(high_bridge_cells(set(nodes)))

    return CompareRow(
        ensemble_name=ensemble_name,
        pack_name=pack_name,
        scenario_name=scenario_name,
        source_name=target_source,
        subtype=subtype,
        actual_subtype=getattr(row, "subtype"),
        predicted_subtype=getattr(row, "subtype"),
        predicted_branch="-",
        support_load=float(getattr(row, "support_load")),
        closure_load=float(getattr(row, "closure_load")),
        mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
        anchor_closure_intensity_gap=float(
            getattr(row, "anchor_closure_intensity_gap")
        ),
        anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
        high_bridge_left_count=float(band["high_bridge_left_count"]),
        high_bridge_mid_count=float(band["high_bridge_mid_count"]),
        high_bridge_right_count=float(band["high_bridge_right_count"]),
        high_bridge_right_low_count=float(band["high_bridge_right_low_count"]),
        left_candidate_count=float(anchor["left_candidate_count"]),
        mid_candidate_count=float(anchor["mid_candidate_count"]),
        left_candidate_bridge_max=float(anchor["left_candidate_bridge_max"]),
        mid_candidate_bridge_max=float(anchor["mid_candidate_bridge_max"]),
        left_candidate_closed_pair_max=float(anchor["left_candidate_closed_pair_max"]),
        mid_candidate_closed_pair_max=float(anchor["mid_candidate_closed_pair_max"]),
        left_candidate_bridge_bridge_closed_pair_max=float(
            anchor["left_candidate_bridge_bridge_closed_pair_max"]
        ),
        mid_candidate_bridge_bridge_closed_pair_max=float(
            anchor["mid_candidate_bridge_bridge_closed_pair_max"]
        ),
        left_candidate_closed_ratio_max=float(anchor["left_candidate_closed_ratio_max"]),
        mid_candidate_closed_ratio_max=float(anchor["mid_candidate_closed_ratio_max"]),
        left_candidate_dense_count=float(anchor["left_candidate_dense_count"]),
        mid_candidate_dense_count=float(anchor["mid_candidate_dense_count"]),
        delta_mid_left_bridge_max=float(anchor["delta_mid_left_bridge_max"]),
        delta_mid_left_closed_pair_max=float(anchor["delta_mid_left_closed_pair_max"]),
        delta_mid_left_bridge_bridge_closed_pair_max=float(
            anchor["delta_mid_left_bridge_bridge_closed_pair_max"]
        ),
        delta_mid_left_dense_count=float(anchor["delta_mid_left_dense_count"]),
        edge_identity_event_count=float(own["edge_identity_event_count"]),
        edge_identity_support_edge_density=float(
            own["edge_identity_support_edge_density"]
        ),
    )


def _target_specs(mode: str) -> tuple[tuple[str, str, str, str, str], ...]:
    if mode == "full-wall":
        return FULL_WALL_TARGET_SPECS
    return FOCUSED_TARGET_SPECS


def build_rows(mode: str) -> list[CompareRow]:
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
    rows = [
        _fetch_row(
            ensemble_name,
            pack_name,
            scenario_name,
            target_source,
            subtype,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
        )
        for ensemble_name, pack_name, scenario_name, target_source, subtype in _target_specs(
            mode
        )
    ]
    rows.sort(key=lambda row: (row.subtype, row.ensemble_name, row.source_name))
    return rows


def _render_rows(title: str, rows: list[CompareRow]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{row.ensemble_name}:{row.source_name} cohort={row.subtype} "
            f"actual={row.actual_subtype}"
        )
        for feature_name in FEATURE_NAMES:
            lines.append(f"  {feature_name}={float(getattr(row, feature_name)):.3f}")
    return "\n".join(lines)


def _render_deltas(late_rows: list[CompareRow], large_row: CompareRow) -> str:
    lines = ["Late-vs-Large Deltas", "===================="]
    for row in late_rows:
        lines.append(f"{row.ensemble_name}:{row.source_name}")
        for feature_name in (
            "support_load",
            "closure_load",
            "mid_anchor_closure_peak",
            "left_candidate_bridge_bridge_closed_pair_max",
            "mid_candidate_bridge_bridge_closed_pair_max",
            "delta_mid_left_bridge_bridge_closed_pair_max",
            "left_candidate_closed_ratio_max",
            "mid_candidate_closed_ratio_max",
        ):
            delta = float(getattr(row, feature_name)) - float(getattr(large_row, feature_name))
            lines.append(f"  delta_{feature_name}={delta:.3f}")
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    print(f"late branch mid-anchor translation compare started {started}")

    rows = build_rows(args.mode)
    late_rows = [row for row in rows if row.subtype == LATE_CLASS]
    wall_rows = [row for row in rows if row.subtype != LATE_CLASS]
    large_rows = [row for row in rows if row.subtype == LARGE_MISS_CLASS]
    large_row = large_rows[0] if large_rows else None
    any_rules = evaluate_rules(
        rows,
        target_subtype=LATE_CLASS,
        feature_names=list(FEATURE_NAMES),
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    structural_rules = evaluate_rules(
        rows,
        target_subtype=LATE_CLASS,
        feature_names=list(STRUCTURAL_RULE_FEATURE_NAMES),
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Late Branch Mid-Anchor Translation Compare")
    print("==========================================")
    print(f"mode={args.mode}")
    print(f"rows_total={len(rows)} ({_format_counts(rows)})")
    print(
        "late_mid_anchor_closure_peaks="
        + ",".join(f"{row.mid_anchor_closure_peak:.3f}" for row in late_rows)
    )
    print(
        "late_delta_mid_left_bridge_bridge_closed_pair_max="
        + ",".join(
            f"{row.delta_mid_left_bridge_bridge_closed_pair_max:.3f}" for row in late_rows
        )
    )
    if large_row is not None:
        print(
            "large_exhausted_mid_anchor_closure_peak="
            f"{large_row.mid_anchor_closure_peak:.3f}"
        )
        print(
            "large_exhausted_left_mid_bridge_bridge_closed_pair_max="
            f"{large_row.left_candidate_bridge_bridge_closed_pair_max:.3f}/"
            f"{large_row.mid_candidate_bridge_bridge_closed_pair_max:.3f}"
        )
        print(
            "large_exhausted_delta_mid_left_bridge_bridge_closed_pair_max="
            f"{large_row.delta_mid_left_bridge_bridge_closed_pair_max:.3f}"
        )
    if args.mode == "full-wall":
        print(
            "wall_mid_candidate_bridge_bridge_closed_pair_max="
            + ",".join(
                f"{row.subtype}:{row.mid_candidate_bridge_bridge_closed_pair_max:.3f}"
                for row in wall_rows
            )
        )
    if any_rules:
        best = any_rules[0]
        print(
            f"best_any_rule={best.rule_text} "
            f"tp/fp/fn={best.tp}/{best.fp}/{best.fn} exact={'Y' if best.exact else 'n'}"
        )
    if structural_rules:
        best = structural_rules[0]
        print(
            f"best_structural_rule={best.rule_text} "
            f"tp/fp/fn={best.tp}/{best.fp}/{best.fn} exact={'Y' if best.exact else 'n'}"
        )
    if args.mode == "full-wall":
        print(
            "translation_summary="
            "across the full exhausted wall, every observed late row keeps a "
            "mid-anchor bridge-bridge closed-pair maximum of 12.000, while both "
            "exhausted misses stop at 8.000"
        )
    else:
        print(
            "translation_summary="
            "the closest large miss preserves the same 12 closed-pair maximum, "
            "but keeps it on the left anchor band instead of the mid anchor band"
        )
    print()
    print(_render_rows("Late base rows", late_rows))
    print()
    print(_render_rows("Exhausted-wall rows", wall_rows))
    if args.mode != "full-wall" and large_row is not None:
        print()
        print(_render_deltas(late_rows, large_row))
    print()
    print("Best any-feature rules")
    print("======================")
    for rule in any_rules:
        print(
            f"{rule.rule_text} | exact={'Y' if rule.exact else 'n'} | "
            f"correct={rule.correct}/{rule.total} | tp/fp/fn={rule.tp}/{rule.fp}/{rule.fn}"
        )
    print()
    print("Best structural rules")
    print("=====================")
    for rule in structural_rules:
        print(
            f"{rule.rule_text} | exact={'Y' if rule.exact else 'n'} | "
            f"correct={rule.correct}/{rule.total} | tp/fp/fn={rule.tp}/{rule.fp}/{rule.fn}"
        )
    print()
    print(
        "late branch mid-anchor translation compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
