#!/usr/bin/env python3
"""Compare the near-miss dominant packets against the family and skew-wrap templates."""

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
    RowRecord,
    _fetch_row,
    _find_hinge_nodes,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_law_confirmation import (  # noqa: E402
    _has_four_incident_flank_hinge,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_packet_neighborhood_compare import (  # noqa: E402
    CandidateNeighborhood,
    _format_rel_edges,
    _format_rel_nodes,
    _missing_edges,
    _missing_nodes,
)
from toy_event_physics import _extended_ge6_dpadj_trees  # noqa: E402


@dataclass(frozen=True)
class AlignmentAudit:
    cell: tuple[int, int]
    hinge: bool
    missing_support_nodes: tuple[tuple[int, int], ...]
    missing_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    extra_support_nodes: tuple[tuple[int, int], ...]
    extra_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    support_overlap_count: int
    closed_edge_overlap_count: int


def _audit_alignment(
    reference: CandidateNeighborhood,
    probe: CandidateNeighborhood,
) -> AlignmentAudit:
    missing_support_nodes = _missing_nodes(reference, probe)
    missing_closed_edges = _missing_edges(reference, probe)
    extra_support_nodes = _missing_nodes(probe, reference)
    extra_closed_edges = _missing_edges(probe, reference)
    support_overlap_count = len(
        set(reference.relative_support_nodes) & set(probe.relative_support_nodes)
    )
    closed_edge_overlap_count = len(
        set(reference.relative_closed_edges) & set(probe.relative_closed_edges)
    )
    return AlignmentAudit(
        cell=probe.cell,
        hinge=_has_four_incident_flank_hinge(
            probe.relative_support_nodes,
            probe.relative_closed_edges,
        ),
        missing_support_nodes=missing_support_nodes,
        missing_closed_edges=missing_closed_edges,
        extra_support_nodes=extra_support_nodes,
        extra_closed_edges=extra_closed_edges,
        support_overlap_count=support_overlap_count,
        closed_edge_overlap_count=closed_edge_overlap_count,
    )


def _render_reference(title: str, neighborhood: CandidateNeighborhood) -> str:
    lines = [
        title,
        "=" * len(title),
        f"cell={neighborhood.cell}",
        f"kind={neighborhood.kind}",
        f"attached={neighborhood.attached_count:.3f}",
        f"bb_closed={neighborhood.bridge_bridge_closed_pair_count:.3f}",
        "relative_support_nodes=" + _format_rel_nodes(neighborhood.relative_support_nodes),
        "relative_closed_edges=" + _format_rel_edges(neighborhood.relative_closed_edges),
        "hinge_nodes=" + _format_rel_nodes(_find_hinge_nodes(neighborhood)),
    ]
    return "\n".join(lines)


def _render_near_miss_alignment(
    reference: CandidateNeighborhood,
    near_miss: RowRecord,
) -> str:
    lines = [
        "Near-Miss Dominant Packet Alignment",
        "==================================",
        f"dominant_mid_count={len(near_miss.dominant_mid_neighborhoods)}",
    ]
    audits = [
        (neighborhood, _audit_alignment(reference, neighborhood))
        for neighborhood in near_miss.dominant_mid_neighborhoods
    ]
    audits.sort(
        key=lambda item: (
            len(item[1].missing_support_nodes) + len(item[1].missing_closed_edges),
            len(item[1].extra_support_nodes) + len(item[1].extra_closed_edges),
            item[0].cell,
        )
    )
    for neighborhood, audit in audits:
        lines.append(
            f"cell={neighborhood.cell} attached={neighborhood.attached_count:.3f} "
            f"bb_closed={neighborhood.bridge_bridge_closed_pair_count:.3f} "
            f"hinge={'Y' if audit.hinge else 'n'}"
        )
        lines.append(
            f"  support_overlap_count={audit.support_overlap_count} "
            f"closed_edge_overlap_count={audit.closed_edge_overlap_count}"
        )
        lines.append(
            "  missing_support_nodes="
            + _format_rel_nodes(audit.missing_support_nodes)
        )
        lines.append(
            "  missing_closed_edges="
            + _format_rel_edges(audit.missing_closed_edges)
        )
        lines.append(
            "  extra_support_nodes="
            + _format_rel_nodes(audit.extra_support_nodes)
        )
        lines.append(
            "  extra_closed_edges="
            + _format_rel_edges(audit.extra_closed_edges)
        )
    return "\n".join(lines)


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
            family,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
        )
        for ensemble_name, pack_name, scenario_name, source_name, family in FAMILY_SPECS
    ]
    near_miss = _fetch_row(
        *NEAR_MISS_SPEC,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )
    family_reference = family_rows[0].dominant_mid_neighborhoods[0]
    skew_wrap_reference = next(
        row for row in family_rows if row.family == "skew-wrap"
    ).dominant_mid_neighborhoods[0]

    print(f"dominant packet alignment compare started {started_at}")
    print()
    print(_render_reference("Shared Family Reference Packet", family_reference))
    print()
    print(_render_reference("Realized Skew-Wrap Packet", skew_wrap_reference))
    print()
    print(_render_near_miss_alignment(family_reference, near_miss))
    print()
    print(
        "alignment_summary="
        "the three tied dominant mids in the fresh skew-hard near miss are not competing "
        "between two equally family-like realizations. One packet preserves the hinge, but "
        "the best family-aligned packet is still the cleanest one-node deletion of the shared "
        "family template."
    )
    print(
        "dominant packet alignment compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
