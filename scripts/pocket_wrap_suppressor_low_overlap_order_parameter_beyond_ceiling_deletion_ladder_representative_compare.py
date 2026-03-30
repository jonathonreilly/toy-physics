#!/usr/bin/env python3
"""Compare representative beyond-ceiling deletion rungs against the realized family."""

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

from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_dominant_packet_semantics_audit import (  # noqa: E402
    OUTSIDE_SPECS,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_near_miss_topology_compare import (  # noqa: E402
    FAMILY_SPECS,
    NEAR_MISS_SPEC,
    RowRecord,
    _fetch_row,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_packet_neighborhood_compare import (  # noqa: E402
    CandidateNeighborhood,
    _format_rel_edges,
    _format_rel_nodes,
    _missing_edges,
    _missing_nodes,
)
from toy_event_physics import _extended_ge6_dpadj_trees  # noqa: E402


REPRESENTATIVE_LABELS = {
    "realized-family": ("exa", "base", "skew-wrap", "base:skew-wrap:local-morph-k"),
    "side-deletion": ("default", "base", "skew-wrap", "base:skew-wrap:local-morph-c"),
    "hinge-deletion": ("exa", "large", "taper-wrap-large", "large:taper-wrap-large:local-morph-g"),
    "corner-deletion": ("exa", "base", "skew-hard", "base:skew-hard:local-morph-k"),
}
ROLE_NAMES = {
    (-1, 0): "hinge",
    (0, -1): "side",
    (0, 1): "side",
    (-1, -1): "corner",
    (-1, 1): "corner",
    (1, -1): "corner",
    (1, 1): "corner",
}


@dataclass(frozen=True)
class RepresentativeRow:
    rung: str
    label: str
    dominant_mid_count: int
    best_mid_cell: tuple[int, int]
    best_mid_attached: float
    best_mid_closed_edges: float
    missing_support_nodes: tuple[tuple[int, int], ...]
    missing_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    missing_roles: tuple[str, ...]
    column_signature: tuple[int, int, int]
    row_signature: tuple[int, int, int]
    dominant_column_signatures: tuple[tuple[int, int, int], ...]
    dominant_row_signatures: tuple[tuple[int, int, int], ...]
    dominant_closed_edge_counts: tuple[float, ...]


def _best_family_aligned_mid(
    reference: CandidateNeighborhood,
    neighborhoods: tuple[CandidateNeighborhood, ...],
) -> CandidateNeighborhood:
    return min(
        neighborhoods,
        key=lambda neighborhood: (
            len(_missing_nodes(reference, neighborhood))
            + len(_missing_edges(reference, neighborhood)),
            len(_missing_nodes(neighborhood, reference))
            + len(_missing_edges(neighborhood, reference)),
            neighborhood.cell,
        ),
    )


def _column_signature(
    neighborhood: CandidateNeighborhood,
) -> tuple[int, int, int]:
    left = sum(1 for x, _y in neighborhood.relative_support_nodes if x < 0)
    center = sum(1 for x, _y in neighborhood.relative_support_nodes if x == 0)
    right = sum(1 for x, _y in neighborhood.relative_support_nodes if x > 0)
    return (left, center, right)


def _row_signature(
    neighborhood: CandidateNeighborhood,
) -> tuple[int, int, int]:
    lower = sum(1 for _x, y in neighborhood.relative_support_nodes if y < 0)
    midline = sum(1 for _x, y in neighborhood.relative_support_nodes if y == 0)
    upper = sum(1 for _x, y in neighborhood.relative_support_nodes if y > 0)
    return (lower, midline, upper)


def _role_name(node: tuple[int, int]) -> str:
    return ROLE_NAMES.get(node, "other")


def _build_representative_row(
    rung: str,
    row: RowRecord,
    reference: CandidateNeighborhood,
) -> RepresentativeRow:
    best_mid = _best_family_aligned_mid(reference, row.dominant_mid_neighborhoods)
    missing_support_nodes = _missing_nodes(reference, best_mid)
    missing_closed_edges = _missing_edges(reference, best_mid)
    dominant_column_signatures = tuple(
        sorted({_column_signature(neighborhood) for neighborhood in row.dominant_mid_neighborhoods})
    )
    dominant_row_signatures = tuple(
        sorted({_row_signature(neighborhood) for neighborhood in row.dominant_mid_neighborhoods})
    )
    dominant_closed_edge_counts = tuple(
        sorted(
            {
                neighborhood.bridge_bridge_closed_pair_count
                for neighborhood in row.dominant_mid_neighborhoods
            }
        )
    )
    return RepresentativeRow(
        rung=rung,
        label=f"{row.ensemble_name}:{row.source_name}",
        dominant_mid_count=len(row.dominant_mid_neighborhoods),
        best_mid_cell=best_mid.cell,
        best_mid_attached=best_mid.attached_count,
        best_mid_closed_edges=best_mid.bridge_bridge_closed_pair_count,
        missing_support_nodes=missing_support_nodes,
        missing_closed_edges=missing_closed_edges,
        missing_roles=tuple(_role_name(node) for node in missing_support_nodes),
        column_signature=_column_signature(best_mid),
        row_signature=_row_signature(best_mid),
        dominant_column_signatures=dominant_column_signatures,
        dominant_row_signatures=dominant_row_signatures,
        dominant_closed_edge_counts=dominant_closed_edge_counts,
    )


def _render_representative_table(rows: list[RepresentativeRow]) -> str:
    lines = [
        "Representative Deletion Ladder Compare",
        "======================================",
        "rung | label | dominant_mid_count | best_mid_cell | attached | closed_edges | missing_roles | missing_support_nodes | lost_closed_edges | column_signature(l/c/r) | row_signature(l/m/u)",
        "----+-------+--------------------+--------------+----------+--------------+---------------+-----------------------+------------------+------------------------+----------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.rung} | {row.label} | {row.dominant_mid_count} | {row.best_mid_cell} | "
            f"{row.best_mid_attached:.3f} | {row.best_mid_closed_edges:.3f} | "
            f"{','.join(row.missing_roles) if row.missing_roles else 'none'} | "
            f"{_format_rel_nodes(row.missing_support_nodes)} | {len(row.missing_closed_edges)} | "
            f"{row.column_signature} | {row.row_signature}"
        )
    return "\n".join(lines)


def _render_orientation_stability(rows: list[RepresentativeRow]) -> str:
    lines = [
        "Directional Tally Stability Audit",
        "================================",
    ]
    for row in rows:
        lines.append(f"rung={row.rung} label={row.label}")
        lines.append(
            "  dominant_closed_edge_counts="
            + ", ".join(f"{value:.3f}" for value in row.dominant_closed_edge_counts)
        )
        lines.append(
            "  dominant_column_signatures="
            + ", ".join(str(signature) for signature in row.dominant_column_signatures)
        )
        lines.append(
            "  dominant_row_signatures="
            + ", ".join(str(signature) for signature in row.dominant_row_signatures)
        )
    return "\n".join(lines)


def _render_detail(row: RepresentativeRow) -> str:
    return "\n".join(
        [
            f"{row.rung} detail",
            "=" * (len(row.rung) + 7),
            f"label={row.label}",
            f"best_mid_cell={row.best_mid_cell}",
            "missing_support_nodes=" + _format_rel_nodes(row.missing_support_nodes),
            "missing_closed_edges=" + _format_rel_edges(row.missing_closed_edges),
        ]
    )


def _render_conclusion(rows: list[RepresentativeRow]) -> str:
    by_rung = {row.rung: row for row in rows}
    side = by_rung["side-deletion"]
    hinge = by_rung["hinge-deletion"]
    corner = by_rung["corner-deletion"]
    family = by_rung["realized-family"]
    column_overlap = hinge.column_signature in corner.dominant_column_signatures
    row_overlap = side.row_signature in corner.dominant_row_signatures
    lines = [
        "Conclusion",
        "==========",
        "missing_node_position_summary="
        "missing-node position is still the right mechanism label, but not the cleanest ladder scalar: "
        f"the side and hinge representatives delete different node roles ({','.join(side.missing_roles)} vs "
        f"{','.join(hinge.missing_roles)}) while staying on the same harsher rung.",
        "directional_tally_summary="
        "simple directional attachment tallies are not stable enough to carry the ladder alone. "
        f"The corner near miss keeps closed-edge completion fixed at "
        f"{corner.best_mid_closed_edges:.3f} while its tied dominant set moves across column signatures "
        f"{corner.dominant_column_signatures} and row signatures {corner.dominant_row_signatures}."
        + (
            " One hinge representative column tally is literally reused by a corner orientation."
            if column_overlap
            else ""
        )
        + (
            " One side representative row tally is also reused by a corner orientation."
            if row_overlap
            else ""
        ),
        "closed_edge_completion_summary="
        "the cleanest scalar compression is best-aligned closed-edge completion "
        f"(`mid_candidate_bridge_bridge_closed_pair_max` at row level): side/hinge = "
        f"{side.best_mid_closed_edges:.3f}/{hinge.best_mid_closed_edges:.3f}, corner = "
        f"{corner.best_mid_closed_edges:.3f}, realized family = {family.best_mid_closed_edges:.3f}.",
        "physical_translation="
        "the beyond-ceiling ladder is therefore best read as local shared-packet closure completion: "
        "four lost closures define the harsher side/hinge `7/8` rung, two lost closures define the "
        "corner `7/10` rung, and full twelve-edge completion gives the realized family.",
        "family_law_status="
        "this does not replace the exact row-level family separator; that still stays "
        "`mid_candidate_attached_max >= 7.500`.",
    ]
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
    family_reference = family_rows[0].dominant_mid_neighborhoods[0]

    outside_lookup = {
        (ensemble_name, pack_name, scenario_name, source_name): family
        for ensemble_name, pack_name, scenario_name, source_name, family in OUTSIDE_SPECS
    }
    selected_rows: list[RepresentativeRow] = []
    for rung, spec in REPRESENTATIVE_LABELS.items():
        if spec in outside_lookup:
            family = outside_lookup[spec]
        elif spec == NEAR_MISS_SPEC[:4]:
            family = NEAR_MISS_SPEC[4]
        else:
            family = "shared-family"
        row = _fetch_row(
            spec[0],
            spec[1],
            spec[2],
            spec[3],
            family,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
        )
        selected_rows.append(_build_representative_row(rung, row, family_reference))

    rung_order = {
        "side-deletion": 0,
        "hinge-deletion": 1,
        "corner-deletion": 2,
        "realized-family": 3,
    }
    selected_rows.sort(key=lambda row: rung_order[row.rung])

    print(f"beyond-ceiling deletion ladder representative compare started {started_at}")
    print()
    print(_render_representative_table(selected_rows))
    print()
    print(_render_orientation_stability(selected_rows))
    print()
    for row in selected_rows:
        print(_render_detail(row))
        print()
    print(_render_conclusion(selected_rows))
    print(
        "beyond-ceiling deletion ladder representative compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
