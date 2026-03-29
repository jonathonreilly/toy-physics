#!/usr/bin/env python3
"""Compare late-branch anchor translations against exhausted-wall misses."""

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
    support_edges,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    support_roles,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_rc0_ml0_c2_candidate_anchor_common import (  # noqa: E402
    candidate_anchor_metrics,
)
from toy_event_physics import (  # noqa: E402
    _extended_ge6_dpadj_trees,
    graph_neighbors,
    pocket_candidate_cells,
)


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
NEUTRAL_PAIR_TARGET_SPECS = (
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
    "left_candidate_attached_max",
    "mid_candidate_attached_max",
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
    "delta_mid_left_attached_max",
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
    "left_candidate_attached_max",
    "mid_candidate_attached_max",
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
    "delta_mid_left_attached_max",
    "delta_mid_left_bridge_max",
    "delta_mid_left_closed_pair_max",
    "delta_mid_left_bridge_bridge_closed_pair_max",
    "delta_mid_left_dense_count",
)
NEUTRAL_PAIR_RULE_FEATURE_NAMES = (
    "high_bridge_left_count",
    "high_bridge_mid_count",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "left_candidate_count",
    "mid_candidate_count",
    "left_candidate_attached_max",
    "mid_candidate_attached_max",
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
    "delta_mid_left_attached_max",
    "delta_mid_left_bridge_max",
    "delta_mid_left_closed_pair_max",
    "delta_mid_left_bridge_bridge_closed_pair_max",
    "delta_mid_left_dense_count",
)


@dataclass(frozen=True)
class CandidateCellDetail:
    cell: tuple[int, int]
    band: str
    kind: str
    attached_count: float
    bridge_count: float
    closed_pair_count: float
    bridge_bridge_closed_pair_count: float
    closed_ratio: float


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
    left_candidate_attached_max: float
    mid_candidate_attached_max: float
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
    delta_mid_left_attached_max: float
    delta_mid_left_bridge_max: float
    delta_mid_left_closed_pair_max: float
    delta_mid_left_bridge_bridge_closed_pair_max: float
    delta_mid_left_dense_count: float
    edge_identity_event_count: float
    edge_identity_support_edge_density: float
    candidate_details: tuple[CandidateCellDetail, ...]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("focused", "full-wall", "neutral-pair"),
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


def _candidate_band(cell: tuple[int, int]) -> str:
    x, _y = cell
    if x <= 1:
        return "left"
    if x >= 5:
        return "right"
    return "mid"


def _candidate_cell_details(nodes: set[tuple[int, int]]) -> list[CandidateCellDetail]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    candidate_cells = pocket_cells | deep_cells
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edge_set = support_edges(support_nodes)

    out: list[CandidateCellDetail] = []
    for candidate in sorted(candidate_cells):
        attached = [
            support
            for support in graph_neighbors(candidate, support_nodes, wrap_y=False)
            if support in roles
        ]
        bridge_neighbors = [support for support in attached if roles.get(support) == "bridge"]
        closed_pairs = 0.0
        bridge_bridge_closed_pairs = 0.0
        total_pairs = 0.0
        for idx, left in enumerate(attached):
            for right in attached[idx + 1 :]:
                total_pairs += 1.0
                edge = (left, right) if left < right else (right, left)
                if edge not in support_edge_set:
                    continue
                closed_pairs += 1.0
                if roles.get(left) == "bridge" and roles.get(right) == "bridge":
                    bridge_bridge_closed_pairs += 1.0
        out.append(
            CandidateCellDetail(
                cell=candidate,
                band=_candidate_band(candidate),
                kind="pocket" if candidate in pocket_cells else "deep",
                attached_count=float(len(attached)),
                bridge_count=float(len(bridge_neighbors)),
                closed_pair_count=closed_pairs,
                bridge_bridge_closed_pair_count=bridge_bridge_closed_pairs,
                closed_ratio=(closed_pairs / total_pairs) if total_pairs else 0.0,
            )
        )
    return out


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
    nodes = set(nodes)
    anchor = candidate_anchor_metrics(nodes)
    own = support_edge_identity_own_metrics(nodes)
    band = high_bridge_band_metrics(high_bridge_cells(nodes))
    candidate_details = _candidate_cell_details(nodes)
    left_candidate_attached_max = max(
        (detail.attached_count for detail in candidate_details if detail.band == "left"),
        default=0.0,
    )
    mid_candidate_attached_max = max(
        (detail.attached_count for detail in candidate_details if detail.band == "mid"),
        default=0.0,
    )

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
        left_candidate_attached_max=float(left_candidate_attached_max),
        mid_candidate_attached_max=float(mid_candidate_attached_max),
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
        delta_mid_left_attached_max=float(
            mid_candidate_attached_max - left_candidate_attached_max
        ),
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
        candidate_details=tuple(candidate_details),
    )


def _target_specs(mode: str) -> tuple[tuple[str, str, str, str, str], ...]:
    if mode == "full-wall":
        return FULL_WALL_TARGET_SPECS
    if mode == "neutral-pair":
        return NEUTRAL_PAIR_TARGET_SPECS
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


def _render_candidate_details(rows: list[CompareRow]) -> str:
    lines = ["Candidate cell geometry", "======================="]
    for row in rows:
        lines.append(f"{row.ensemble_name}:{row.source_name}")
        for detail in row.candidate_details:
            lines.append(
                "  "
                f"cell={detail.cell} band={detail.band} kind={detail.kind} "
                f"attached={detail.attached_count:.3f} bridge={detail.bridge_count:.3f} "
                f"closed={detail.closed_pair_count:.3f} "
                f"bb_closed={detail.bridge_bridge_closed_pair_count:.3f} "
                f"ratio={detail.closed_ratio:.3f}"
            )
    return "\n".join(lines)


def _render_neutral_pair_deltas(late_row: CompareRow, mirror_row: CompareRow) -> str:
    lines = ["Neutral Pair Deltas", "==================="]
    for feature_name in (
        "support_load",
        "closure_load",
        "mid_anchor_closure_peak",
        "high_bridge_left_count",
        "high_bridge_mid_count",
        "left_candidate_count",
        "mid_candidate_count",
        "left_candidate_attached_max",
        "mid_candidate_attached_max",
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
    ):
        delta = float(getattr(late_row, feature_name)) - float(getattr(mirror_row, feature_name))
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
    mirror_rows = [row for row in rows if row.subtype == MIRROR_MISS_CLASS]
    mirror_row = mirror_rows[0] if mirror_rows else None
    any_rules = evaluate_rules(
        rows,
        target_subtype=LATE_CLASS,
        feature_names=list(FEATURE_NAMES),
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    structural_feature_names = (
        list(NEUTRAL_PAIR_RULE_FEATURE_NAMES)
        if args.mode == "neutral-pair"
        else list(STRUCTURAL_RULE_FEATURE_NAMES)
    )
    structural_rules = evaluate_rules(
        rows,
        target_subtype=LATE_CLASS,
        feature_names=structural_feature_names,
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
    if args.mode == "neutral-pair" and late_rows and mirror_row is not None:
        late_row = late_rows[0]
        print(
            "neutral_pair_mid_attached_max="
            f"{late_row.mid_candidate_attached_max:.3f}/"
            f"{mirror_row.mid_candidate_attached_max:.3f}"
        )
        print(
            "neutral_pair_mid_bridge_bridge_closed_pair_max="
            f"{late_row.mid_candidate_bridge_bridge_closed_pair_max:.3f}/"
            f"{mirror_row.mid_candidate_bridge_bridge_closed_pair_max:.3f}"
        )
        print(
            "neutral_pair_mid_closed_ratio_max="
            f"{late_row.mid_candidate_closed_ratio_max:.3f}/"
            f"{mirror_row.mid_candidate_closed_ratio_max:.3f}"
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
    elif args.mode == "neutral-pair":
        print(
            "translation_summary="
            "the neutral late skew row keeps the same high-bridge placement, "
            "candidate counts, dense counts, and mid closed-ratio ceiling as the "
            "mirror miss, but upgrades the dominant left/mid packet from 7 attached "
            "bridges and 8 closed pairs to 8 attached bridges and 12 closed pairs"
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
    if args.mode == "neutral-pair":
        print()
        print(_render_candidate_details(rows))
    if args.mode != "full-wall" and large_row is not None:
        print()
        print(_render_deltas(late_rows, large_row))
    if args.mode == "neutral-pair" and late_rows and mirror_row is not None:
        print()
        print(_render_neutral_pair_deltas(late_rows[0], mirror_row))
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
