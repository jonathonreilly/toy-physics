#!/usr/bin/env python3
"""Compare the fresh skew-hard near miss against the realized shared packet template."""

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

from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    _variant_entries,
    build_rows_with_trees,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_generated_support_collapse_guard_projection import (  # noqa: E402
    is_support_collapse,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_law_confirmation import (  # noqa: E402
    _has_four_incident_flank_hinge,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_packet_neighborhood_compare import (  # noqa: E402
    CandidateNeighborhood,
    _candidate_neighborhoods,
    _dominant_neighborhoods,
    _format_rel_edges,
    _format_rel_nodes,
    _missing_edges,
    _missing_nodes,
)
from toy_event_physics import _extended_ge6_dpadj_trees  # noqa: E402


FAMILY_SPECS = (
    ("ultra", "base", "rect-wrap", "base:rect-wrap:local-morph-f", "outer-rect"),
    ("mega", "base", "rect-wrap", "base:rect-wrap:local-morph-f", "outer-rect"),
    ("peta", "base", "taper-hard", "base:taper-hard:local-morph-f", "taper-hard"),
    ("exa", "base", "taper-hard", "base:taper-hard:local-morph-f", "taper-hard"),
    ("exa", "base", "skew-wrap", "base:skew-wrap:local-morph-k", "skew-wrap"),
)
NEAR_MISS_SPEC = ("exa", "base", "skew-hard", "base:skew-hard:local-morph-k", "near-miss")


@dataclass(frozen=True)
class RowRecord:
    ensemble_name: str
    pack_name: str
    scenario_name: str
    source_name: str
    family: str
    actual_subtype: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    dominant_mid_neighborhoods: tuple[CandidateNeighborhood, ...]


def _fetch_row(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    source_name: str,
    family: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
) -> RowRecord:
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
    row = next(current for current in rows if getattr(current, "source_name") == source_name)
    _wrap_y, entries = _variant_entries(ensemble_name, pack_name, scenario_name)
    nodes = next(
        set(current_nodes)
        for current_source_name, current_nodes, _style in entries
        if current_source_name == source_name
    )
    dominant_mid = _dominant_neighborhoods(_candidate_neighborhoods(nodes), "mid")
    return RowRecord(
        ensemble_name=ensemble_name,
        pack_name=pack_name,
        scenario_name=scenario_name,
        source_name=source_name,
        family=family,
        actual_subtype=str(getattr(row, "subtype")),
        support_load=float(getattr(row, "support_load")),
        closure_load=float(getattr(row, "closure_load")),
        mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
        dominant_mid_neighborhoods=dominant_mid,
    )


def _find_hinge_nodes(neighborhood: CandidateNeighborhood) -> tuple[tuple[int, int], ...]:
    adjacency = {node: set() for node in neighborhood.relative_support_nodes}
    for left, right in neighborhood.relative_closed_edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    out: list[tuple[int, int]] = []
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
            out.append(node)
    return tuple(sorted(out))


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

    family_template_uniform = len(
        {
            (
                row.dominant_mid_neighborhoods[0].relative_support_nodes,
                row.dominant_mid_neighborhoods[0].relative_closed_edges,
            )
            for row in family_rows
        }
    ) == 1
    family_reference = family_rows[0].dominant_mid_neighborhoods[0]
    near_miss_best_mid = min(
        near_miss.dominant_mid_neighborhoods,
        key=lambda neighborhood: (
            len(_missing_nodes(family_reference, neighborhood))
            + len(_missing_edges(family_reference, neighborhood)),
            neighborhood.cell,
        ),
    )
    missing_nodes = _missing_nodes(family_reference, near_miss_best_mid)
    missing_edges = _missing_edges(family_reference, near_miss_best_mid)
    extra_nodes = _missing_nodes(near_miss_best_mid, family_reference)
    extra_edges = _missing_edges(near_miss_best_mid, family_reference)
    family_hinges = _find_hinge_nodes(family_reference)
    near_miss_hinges = tuple(
        sorted(
            {
                hinge_node
                for neighborhood in near_miss.dominant_mid_neighborhoods
                for hinge_node in _find_hinge_nodes(neighborhood)
            }
        )
    )
    shared_hinges = tuple(sorted(set(family_hinges) & set(near_miss_hinges)))
    near_miss_hinge_present = any(
        _has_four_incident_flank_hinge(
            neighborhood.relative_support_nodes,
            neighborhood.relative_closed_edges,
        )
        for neighborhood in near_miss.dominant_mid_neighborhoods
    )

    print(f"beyond-ceiling near-miss topology compare started {started_at}")
    print()
    print("Beyond-Ceiling Near-Miss Topology Compare")
    print("========================================")
    print(f"family_rows={len(family_rows)}")
    print(
        "family_labels="
        + ",".join(f"{row.ensemble_name}:{row.source_name}" for row in family_rows)
    )
    print(f"near_miss={near_miss.ensemble_name}:{near_miss.source_name}")
    print(f"family_template_uniform={'Y' if family_template_uniform else 'n'}")
    print(
        f"family_mid_attached={family_reference.attached_count:.3f} "
        f"family_mid_bb_closed={family_reference.bridge_bridge_closed_pair_count:.3f}"
    )
    print(
        f"near_miss_dominant_mid_count={len(near_miss.dominant_mid_neighborhoods)}"
    )
    for neighborhood in near_miss.dominant_mid_neighborhoods:
        print(
            "near_miss_dominant_mid="
            f"cell={neighborhood.cell} attached={neighborhood.attached_count:.3f} "
            f"bb_closed={neighborhood.bridge_bridge_closed_pair_count:.3f} "
            f"hinge={'Y' if _has_four_incident_flank_hinge(neighborhood.relative_support_nodes, neighborhood.relative_closed_edges) else 'n'}"
        )
    print(
        "near_miss_best_family_aligned_mid="
        f"cell={near_miss_best_mid.cell} attached={near_miss_best_mid.attached_count:.3f} "
        f"bb_closed={near_miss_best_mid.bridge_bridge_closed_pair_count:.3f}"
    )
    print(
        "family_relative_support_nodes="
        + _format_rel_nodes(family_reference.relative_support_nodes)
    )
    print(
        "family_relative_closed_edges="
        + _format_rel_edges(family_reference.relative_closed_edges)
    )
    print(
        "near_miss_relative_support_nodes="
        + _format_rel_nodes(near_miss_best_mid.relative_support_nodes)
    )
    print(
        "near_miss_relative_closed_edges="
        + _format_rel_edges(near_miss_best_mid.relative_closed_edges)
    )
    print("missing_relative_support_nodes=" + _format_rel_nodes(missing_nodes))
    print("missing_relative_closed_edges=" + _format_rel_edges(missing_edges))
    print("extra_relative_support_nodes=" + _format_rel_nodes(extra_nodes))
    print("extra_relative_closed_edges=" + _format_rel_edges(extra_edges))
    print("family_hinge_nodes=" + _format_rel_nodes(family_hinges))
    print("near_miss_hinge_nodes=" + _format_rel_nodes(near_miss_hinges))
    print("shared_hinge_nodes=" + _format_rel_nodes(shared_hinges))
    print(
        "near_miss_hinge_present="
        + ("Y" if near_miss_hinge_present else "n")
    )
    print(
        "topology_translation_summary="
        + (
            "the fresh skew-hard near miss still has a hinged dominant mid packet somewhere in "
            "its tied dominant set, but its best family-aligned packet remains short by "
            f"{len(missing_nodes)} support node(s) and {len(missing_edges)} closed edge(s) "
            "relative to the realized family template. So hinge presence alone is not enough; "
            "the present family boundary is the missing completion that lifts the dominant mid "
            "packet from seven attachments to eight."
            if near_miss_hinge_present
            else "the fresh skew-hard near miss loses the shared hinge entirely and remains "
            f"short by {len(missing_nodes)} support node(s) and {len(missing_edges)} closed "
            "edge(s) relative to the realized family template."
        )
    )
    print(
        "beyond-ceiling near-miss topology compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
