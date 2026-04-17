#!/usr/bin/env python3
"""Confirm late-branch laws on a bounded adjacent generated holdout set."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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

from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    _variant_entries,
    build_rows_with_trees,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_generated_support_collapse_guard_projection import (  # noqa: E402
    is_support_collapse,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_packet_neighborhood_compare import (  # noqa: E402
    LATE_CLASS,
    LARGE_MISS_CLASS,
    MIRROR_MISS_CLASS,
    _candidate_neighborhoods,
    _dominant_neighborhoods,
)
from toy_event_physics import (  # noqa: E402
    _extended_ge6_dpadj_trees,
    canonical_generated_ensemble_specs,
)


HIGH_LOAD_THRESHOLD = 73.0
LAW_ORDER = (
    ("mid-anchor-peak", "mid_anchor_closure_peak >= 10.000"),
    (
        "bridge-packet",
        "mid_candidate_bridge_bridge_closed_pair_max >= 10.000",
    ),
    ("attached-packet", "mid_candidate_attached_max >= 7.500"),
    ("flank-hinge", "mid_has_four_incident_flank_hinge = Y"),
)
ENSEMBLE_ORDER = {
    name: index for index, name in enumerate(spec[0] for spec in canonical_generated_ensemble_specs())
}
CONFIRM_TARGET_SPECS = (
    ("peta", "base", "rect-wrap", "base:rect-wrap:local-morph-f", LATE_CLASS, "late-outer-rect"),
    ("exa", "base", "rect-wrap", "base:rect-wrap:local-morph-f", LATE_CLASS, "late-outer-rect"),
    ("peta", "base", "taper-hard", "base:taper-hard:local-morph-f", LATE_CLASS, "late-taper-hard"),
    ("exa", "base", "taper-hard", "base:taper-hard:local-morph-f", LATE_CLASS, "late-taper-hard"),
    ("exa", "base", "skew-wrap", "base:skew-wrap:local-morph-k", LATE_CLASS, "late-skew-wrap"),
    (
        "exa",
        "large",
        "taper-wrap-large",
        "large:taper-wrap-large:local-morph-g",
        LARGE_MISS_CLASS,
        "exhausted-large",
    ),
    (
        "exa",
        "mirror",
        "skew-hard-mirror",
        "mirror:skew-hard-mirror:local-morph-f",
        MIRROR_MISS_CLASS,
        "exhausted-mirror",
    ),
    (
        "default",
        "base",
        "skew-wrap",
        "base:skew-wrap:local-morph-c",
        "holdout",
        "shoulder",
    ),
    (
        "broader",
        "base",
        "skew-wrap",
        "base:skew-wrap:mode-mix-d",
        "holdout",
        "shoulder",
    ),
    (
        "ultra",
        "base",
        "taper-wrap",
        "base:taper-wrap:mode-mix-f",
        "holdout",
        "throat",
    ),
    (
        "mega",
        "base",
        "taper-wrap",
        "base:taper-wrap:mode-mix-f",
        "holdout",
        "throat",
    ),
    (
        "ultra",
        "base",
        "rect-wrap",
        "base:rect-wrap:local-morph-f",
        "holdout",
        "outer-rect",
    ),
    (
        "mega",
        "base",
        "rect-wrap",
        "base:rect-wrap:local-morph-f",
        "holdout",
        "outer-rect",
    ),
)


@dataclass(frozen=True)
class ConfirmationRow:
    cohort: str
    family: str
    ensemble_name: str
    pack_name: str
    scenario_name: str
    source_name: str
    style: str
    actual_subtype: str
    closure_load: float
    mid_anchor_closure_peak: float
    mid_candidate_attached_max: float
    mid_candidate_bridge_bridge_closed_pair_max: float
    mid_has_four_incident_flank_hinge: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--example-limit", type=int, default=8)
    return parser


def _row_sort_key(row: ConfirmationRow) -> tuple[int, int, float, str, str, str]:
    cohort_order = {
        LATE_CLASS: 0,
        LARGE_MISS_CLASS: 1,
        MIRROR_MISS_CLASS: 2,
        "holdout": 3,
    }
    return (
        cohort_order.get(row.cohort, 99),
        ENSEMBLE_ORDER.get(row.ensemble_name, len(ENSEMBLE_ORDER)),
        -row.closure_load,
        row.pack_name,
        row.scenario_name,
        row.source_name,
    )


def _holdout_sort_key(row: ConfirmationRow) -> tuple[int, float, float, int, str, str]:
    return (
        0 if row.closure_load >= HIGH_LOAD_THRESHOLD else 1,
        -row.mid_candidate_attached_max,
        -row.mid_candidate_bridge_bridge_closed_pair_max,
        ENSEMBLE_ORDER.get(row.ensemble_name, len(ENSEMBLE_ORDER)),
        row.family,
        row.source_name,
    )


def _format_counts(rows: list[ConfirmationRow], attr: str) -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _format_row_names(rows: list[ConfirmationRow], limit: int) -> str:
    if not rows:
        return "none"
    return ",".join(
        f"{row.ensemble_name}:{row.pack_name}:{row.source_name}" for row in rows[:limit]
    )


def _has_four_incident_flank_hinge(
    relative_nodes: tuple[tuple[int, int], ...],
    relative_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
) -> bool:
    adjacency = {node: set() for node in relative_nodes}
    for left, right in relative_edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)

    for node, neighbors in adjacency.items():
        if node[0] >= 0:
            continue
        if len(neighbors) != 4:
            continue
        same_column = sum(1 for neighbor in neighbors if neighbor[0] == node[0])
        inward = sum(1 for neighbor in neighbors if neighbor[0] > node[0])
        outward = sum(1 for neighbor in neighbors if neighbor[0] < node[0])
        upper = sum(1 for neighbor in neighbors if neighbor[1] > node[1])
        lower = sum(1 for neighbor in neighbors if neighbor[1] < node[1])
        if (
            same_column == 2
            and inward == 2
            and outward == 0
            and upper == 2
            and lower == 2
        ):
            return True
    return False


def _capture_row(
    *,
    cohort: str,
    family: str,
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    row: object,
    nodes: set[tuple[int, int]],
    style: str,
) -> ConfirmationRow:
    mid_candidate_bridge_bridge_closed_pair_max = float(
        getattr(row, "mid_anchor_closure_peak")
    )
    mid_candidate_attached_max = 0.0
    mid_has_four_incident_flank_hinge = False
    if mid_candidate_bridge_bridge_closed_pair_max >= 8.0:
        dominant_mid = _dominant_neighborhoods(_candidate_neighborhoods(nodes), "mid")
        mid_candidate_attached_max = max(
            (neighborhood.attached_count for neighborhood in dominant_mid),
            default=0.0,
        )
        mid_has_four_incident_flank_hinge = any(
            _has_four_incident_flank_hinge(
                neighborhood.relative_support_nodes,
                neighborhood.relative_closed_edges,
            )
            for neighborhood in dominant_mid
        )
    return ConfirmationRow(
        cohort=cohort,
        family=family,
        ensemble_name=ensemble_name,
        pack_name=pack_name,
        scenario_name=scenario_name,
        source_name=str(getattr(row, "source_name")),
        style=style,
        actual_subtype=str(getattr(row, "subtype")),
        closure_load=float(getattr(row, "closure_load")),
        mid_anchor_closure_peak=mid_candidate_bridge_bridge_closed_pair_max,
        mid_candidate_attached_max=float(mid_candidate_attached_max),
        mid_candidate_bridge_bridge_closed_pair_max=float(
            mid_candidate_bridge_bridge_closed_pair_max
        ),
        mid_has_four_incident_flank_hinge=mid_has_four_incident_flank_hinge,
    )


def build_rows() -> list[ConfirmationRow]:
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
    grouped: dict[tuple[str, str, str], list[tuple[str, str, str]]] = defaultdict(list)
    for ensemble_name, pack_name, scenario_name, source_name, cohort, family in CONFIRM_TARGET_SPECS:
        grouped[(ensemble_name, pack_name, scenario_name)].append((source_name, cohort, family))

    out: list[ConfirmationRow] = []
    for (ensemble_name, pack_name, scenario_name), wanted_rows in grouped.items():
        rows = [
            row
            for row in build_rows_with_trees(
                ensemble_name,
                pack_name,
                scenario_name,
                ge6_tree=ge6_tree,
                dpadj_tree=dpadj_tree,
            )
            if not is_support_collapse(row)
        ]
        row_by_source = {str(getattr(row, "source_name")): row for row in rows}
        _wrap_y, entries = _variant_entries(ensemble_name, pack_name, scenario_name)
        entry_by_source = {
            source_name: (set(nodes), style) for source_name, nodes, style in entries
        }
        for source_name, cohort, family in wanted_rows:
            row = row_by_source[source_name]
            nodes, style = entry_by_source[source_name]
            out.append(
                _capture_row(
                    cohort=cohort,
                    family=family,
                    ensemble_name=ensemble_name,
                    pack_name=pack_name,
                    scenario_name=scenario_name,
                    row=row,
                    nodes=nodes,
                    style=style,
                )
            )
    out.sort(key=_row_sort_key)
    return out


def _law_match(row: ConfirmationRow, law_name: str) -> bool:
    if law_name == "mid-anchor-peak":
        return row.mid_anchor_closure_peak >= 10.0
    if law_name == "bridge-packet":
        return row.mid_candidate_bridge_bridge_closed_pair_max >= 10.0
    if law_name == "attached-packet":
        return row.mid_candidate_attached_max >= 7.5
    if law_name == "flank-hinge":
        return row.mid_has_four_incident_flank_hinge
    raise KeyError(law_name)


def _render_law_block(
    rows: list[ConfirmationRow],
    law_name: str,
    law_text: str,
    *,
    example_limit: int,
) -> str:
    late_rows = [row for row in rows if row.cohort == LATE_CLASS]
    wall_rows = [row for row in rows if row.cohort in {LARGE_MISS_CLASS, MIRROR_MISS_CLASS}]
    holdout_rows = [row for row in rows if row.cohort == "holdout"]
    holdout_matches = sorted(
        [row for row in holdout_rows if _law_match(row, law_name)],
        key=_holdout_sort_key,
    )
    holdout_high_load_matches = [
        row for row in holdout_matches if row.closure_load >= HIGH_LOAD_THRESHOLD
    ]
    tp = sum(1 for row in late_rows if _law_match(row, law_name))
    fp = sum(1 for row in wall_rows if _law_match(row, law_name))
    fn = sum(1 for row in late_rows if not _law_match(row, law_name))
    discovery_exact = fp == 0 and fn == 0
    lines = [
        f"law={law_text}",
        f"discovery_wall=tp/fp/fn={tp}/{fp}/{fn} exact={'Y' if discovery_exact else 'n'}",
        "holdout_matches_total="
        + f"{len(holdout_matches)} ({_format_counts(holdout_matches, 'family')})",
        "holdout_matches_high_load="
        + f"{len(holdout_high_load_matches)} ({_format_counts(holdout_high_load_matches, 'family')})",
        "holdout_match_rows=" + _format_row_names(holdout_matches, example_limit),
    ]
    return "\n".join(lines)


def _render_divergence(rows: list[ConfirmationRow], *, example_limit: int) -> str:
    bridge_only = sorted(
        [
            row
            for row in rows
            if _law_match(row, "bridge-packet") and not _law_match(row, "attached-packet")
        ],
        key=_holdout_sort_key,
    )
    attached_only = sorted(
        [
            row
            for row in rows
            if _law_match(row, "attached-packet") and not _law_match(row, "flank-hinge")
        ],
        key=_holdout_sort_key,
    )
    lines = [
        "Law Divergence",
        "==============",
        "bridge_without_attached_total="
        + f"{len(bridge_only)} ({_format_counts(bridge_only, 'cohort')})",
        "bridge_without_attached_examples="
        + _format_row_names(bridge_only, example_limit),
        "attached_without_hinge_total="
        + f"{len(attached_only)} ({_format_counts(attached_only, 'cohort')})",
        "attached_without_hinge_examples="
        + _format_row_names(attached_only, example_limit),
    ]
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started_at = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    rows = build_rows()

    late_rows = [row for row in rows if row.cohort == LATE_CLASS]
    wall_rows = [row for row in rows if row.cohort in {LARGE_MISS_CLASS, MIRROR_MISS_CLASS}]
    holdout_rows = [row for row in rows if row.cohort == "holdout"]
    holdout_high_load_rows = [
        row for row in holdout_rows if row.closure_load >= HIGH_LOAD_THRESHOLD
    ]

    print(f"late branch law confirmation started {started_at}")
    print()
    print("Late Branch Law Confirmation")
    print("============================")
    print(
        "confirmation_targets="
        + ",".join(
            f"{ensemble}:{pack}:{scenario}:{source}:{cohort}:{family}"
            for ensemble, pack, scenario, source, cohort, family in CONFIRM_TARGET_SPECS
        )
    )
    print(f"rows_total={len(rows)}")
    print(f"late_rows={len(late_rows)} ({_format_counts(late_rows, 'family')})")
    print(f"wall_rows={len(wall_rows)} ({_format_counts(wall_rows, 'cohort')})")
    print(f"holdout_rows={len(holdout_rows)} ({_format_counts(holdout_rows, 'family')})")
    print(
        "holdout_high_load_rows="
        + f"{len(holdout_high_load_rows)} ({_format_counts(holdout_high_load_rows, 'family')})"
    )
    print()
    print("Selected Rows")
    print("=============")
    for row in rows:
        print(
            f"{row.cohort}:{row.family}:{row.ensemble_name}:{row.pack_name}:{row.source_name} "
            f"actual={row.actual_subtype} "
            f"closure_load={row.closure_load:.3f} "
            f"mid_peak={row.mid_anchor_closure_peak:.3f} "
            f"mid_attached={row.mid_candidate_attached_max:.3f} "
            f"mid_bb_closed={row.mid_candidate_bridge_bridge_closed_pair_max:.3f} "
            f"flank_hinge={'Y' if row.mid_has_four_incident_flank_hinge else 'n'}"
        )
    print()
    print("Candidate Laws")
    print("==============")
    for law_name, law_text in LAW_ORDER:
        print(_render_law_block(rows, law_name, law_text, example_limit=args.example_limit))
        print()
    print(_render_divergence(rows, example_limit=args.example_limit))
    print()
    print(
        "late branch law confirmation completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
