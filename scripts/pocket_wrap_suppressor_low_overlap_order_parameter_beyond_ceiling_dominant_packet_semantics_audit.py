#!/usr/bin/env python3
"""Audit whether row law or dominant-packet semantics best express the family boundary."""

from __future__ import annotations

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

from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_near_miss_topology_compare import (  # noqa: E402
    FAMILY_SPECS,
    NEAR_MISS_SPEC,
    _fetch_row,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_law_confirmation import (  # noqa: E402
    _has_four_incident_flank_hinge,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_packet_neighborhood_compare import (  # noqa: E402
    CandidateNeighborhood,
    _missing_edges,
    _missing_nodes,
)
from toy_event_physics import _extended_ge6_dpadj_trees  # noqa: E402


OUTSIDE_SPECS = (
    ("default", "base", "skew-wrap", "base:skew-wrap:local-morph-c", "nearby-shoulder"),
    ("broader", "base", "skew-wrap", "base:skew-wrap:mode-mix-d", "nearby-shoulder"),
    ("ultra", "base", "taper-wrap", "base:taper-wrap:mode-mix-f", "low-support-throat"),
    ("mega", "base", "taper-wrap", "base:taper-wrap:mode-mix-f", "low-support-throat"),
    ("wider", "base", "skew-wrap", "base:skew-wrap:local-morph-c", "wider-sentinel"),
    ("wider", "base", "skew-wrap", "base:skew-wrap:mode-mix-d", "wider-sentinel"),
    ("exa", "large", "taper-wrap-large", "large:taper-wrap-large:local-morph-g", "exhausted-wall"),
    ("exa", "mirror", "skew-hard-mirror", "mirror:skew-hard-mirror:local-morph-f", "exhausted-wall"),
    NEAR_MISS_SPEC,
)


@dataclass(frozen=True)
class PacketSemanticsRow:
    label: str
    family: str
    any_hinge: bool
    any_exact_family_template: bool
    best_aligned_missing_support_nodes: int
    best_aligned_missing_closed_edges: int
    row_mid_attached_max: float


def _best_alignment_counts(
    reference: CandidateNeighborhood,
    neighborhoods: tuple[CandidateNeighborhood, ...],
) -> tuple[int, int]:
    best = min(
        neighborhoods,
        key=lambda neighborhood: (
            len(_missing_nodes(reference, neighborhood))
            + len(_missing_edges(reference, neighborhood)),
            len(_missing_nodes(neighborhood, reference))
            + len(_missing_edges(neighborhood, reference)),
            neighborhood.cell,
        ),
    )
    return len(_missing_nodes(reference, best)), len(_missing_edges(reference, best))


def _capture_semantics_row(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    source_name: str,
    family: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
    family_reference: CandidateNeighborhood,
) -> PacketSemanticsRow:
    row = _fetch_row(
        ensemble_name,
        pack_name,
        scenario_name,
        source_name,
        family,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )
    any_hinge = any(
        _has_four_incident_flank_hinge(
            neighborhood.relative_support_nodes,
            neighborhood.relative_closed_edges,
        )
        for neighborhood in row.dominant_mid_neighborhoods
    )
    any_exact_family_template = any(
        neighborhood.relative_support_nodes == family_reference.relative_support_nodes
        and neighborhood.relative_closed_edges == family_reference.relative_closed_edges
        for neighborhood in row.dominant_mid_neighborhoods
    )
    missing_nodes, missing_edges = _best_alignment_counts(
        family_reference,
        row.dominant_mid_neighborhoods,
    )
    return PacketSemanticsRow(
        label=f"{ensemble_name}:{source_name}",
        family=family,
        any_hinge=any_hinge,
        any_exact_family_template=any_exact_family_template,
        best_aligned_missing_support_nodes=missing_nodes,
        best_aligned_missing_closed_edges=missing_edges,
        row_mid_attached_max=row.dominant_mid_neighborhoods[0].attached_count,
    )


def _render_rule_line(
    rows: list[PacketSemanticsRow],
    *,
    title: str,
    match_fn,
) -> str:
    family_rows = [row for row in rows if row.family == "shared-family"]
    outside_rows = [row for row in rows if row.family != "shared-family"]
    family_hits = [row for row in family_rows if match_fn(row)]
    outside_hits = [row for row in outside_rows if match_fn(row)]
    exact = len(family_hits) == len(family_rows) and not outside_hits
    line = (
        f"{title}: family={len(family_hits)}/{len(family_rows)} "
        f"outside={len(outside_hits)}/{len(outside_rows)} exact={'Y' if exact else 'n'}"
    )
    if outside_hits:
        line += " outside_matches=" + ",".join(row.label for row in outside_hits)
    return line


def main() -> None:
    started_at = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
    family_rows = [
        _fetch_row(
            ensemble_name,
            pack_name,
            scenario_name,
            source_name,
            "shared-family",
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
        )
        for ensemble_name, pack_name, scenario_name, source_name, _family in FAMILY_SPECS
    ]
    family_reference = family_rows[0].dominant_mid_neighborhoods[0]
    rows = [
        _capture_semantics_row(
            row.ensemble_name,
            row.pack_name,
            row.scenario_name,
            row.source_name,
            "shared-family",
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            family_reference=family_reference,
        )
        for row in family_rows
    ]
    rows.extend(
        _capture_semantics_row(
            ensemble_name,
            pack_name,
            scenario_name,
            source_name,
            family,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            family_reference=family_reference,
        )
        for ensemble_name, pack_name, scenario_name, source_name, family in OUTSIDE_SPECS
    )

    print(f"dominant packet semantics audit started {started_at}")
    print()
    print("Dominant Packet Semantics Audit")
    print("================================")
    print(
        "label | family | any_hinge | any_exact_family_template | "
        "best_aligned_missing_support_nodes | best_aligned_missing_closed_edges | row_mid_attached_max"
    )
    print(
        "-----+--------+-----------+---------------------------+"
        "------------------------------------+-----------------------------------+---------------------"
    )
    for row in rows:
        print(
            f"{row.label} | {row.family} | "
            f"{'Y' if row.any_hinge else 'n'} | "
            f"{'Y' if row.any_exact_family_template else 'n'} | "
            f"{row.best_aligned_missing_support_nodes} | "
            f"{row.best_aligned_missing_closed_edges} | "
            f"{row.row_mid_attached_max:.3f}"
        )
    print()
    print(
        _render_rule_line(
            rows,
            title="any_dominant_hinge",
            match_fn=lambda row: row.any_hinge,
        )
    )
    print(
        _render_rule_line(
            rows,
            title="any_dominant_exact_family_template",
            match_fn=lambda row: row.any_exact_family_template,
        )
    )
    print(
        _render_rule_line(
            rows,
            title="best_aligned_missing_support_nodes <= 0",
            match_fn=lambda row: row.best_aligned_missing_support_nodes <= 0,
        )
    )
    print(
        _render_rule_line(
            rows,
            title="best_aligned_missing_closed_edges <= 0",
            match_fn=lambda row: row.best_aligned_missing_closed_edges <= 0,
        )
    )
    print(
        _render_rule_line(
            rows,
            title="row_mid_attached_max >= 7.500",
            match_fn=lambda row: row.row_mid_attached_max >= 7.5,
        )
    )
    print()
    print(
        "semantics_summary=the row-level attachment law remains the cleanest family statement. "
        "An `any dominant packet has hinge` reading leaks on the fresh near miss, while exact "
        "family-template or zero-missing-node formulations also stay exact but are more brittle "
        "and more combinatorial than the unchanged scalar attachment rule."
    )
    print(
        "dominant packet semantics audit completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
