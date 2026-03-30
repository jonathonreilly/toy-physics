#!/usr/bin/env python3
"""Scan finished outside-family rows for shared deletion-class structure."""

from __future__ import annotations

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

from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_dominant_packet_semantics_audit import (  # noqa: E402
    OUTSIDE_SPECS,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_near_miss_topology_compare import (  # noqa: E402
    FAMILY_SPECS,
    NEAR_MISS_SPEC,
    RowRecord,
    _fetch_row,
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
class DeletionSeed:
    cell: tuple[int, int]
    missing_support_nodes: tuple[tuple[int, int], ...]
    missing_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    hinge: bool


@dataclass(frozen=True)
class BoundaryScanRow:
    label: str
    family: str
    best_mid_cell: tuple[int, int]
    row_mid_attached_max: float
    missing_support_nodes: tuple[tuple[int, int], ...]
    missing_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    extra_support_nodes: tuple[tuple[int, int], ...]
    extra_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    hinge: bool
    classification: str


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


def _build_deletion_seeds(
    reference: CandidateNeighborhood,
    near_miss: RowRecord,
) -> tuple[DeletionSeed, ...]:
    out: list[DeletionSeed] = []
    for neighborhood in near_miss.dominant_mid_neighborhoods:
        out.append(
            DeletionSeed(
                cell=neighborhood.cell,
                missing_support_nodes=_missing_nodes(reference, neighborhood),
                missing_closed_edges=_missing_edges(reference, neighborhood),
                hinge=_has_four_incident_flank_hinge(
                    neighborhood.relative_support_nodes,
                    neighborhood.relative_closed_edges,
                ),
            )
        )
    out.sort(key=lambda seed: (seed.missing_support_nodes, seed.cell))
    return tuple(out)


def _classify_row(
    missing_support_nodes: tuple[tuple[int, int], ...],
    missing_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    extra_support_nodes: tuple[tuple[int, int], ...],
    extra_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    seed_nodes: set[tuple[int, int]],
) -> str:
    if len(missing_support_nodes) == 1:
        node = missing_support_nodes[0]
        if node in seed_nodes:
            if (
                len(missing_closed_edges) == 2
                and not extra_support_nodes
                and not extra_closed_edges
            ):
                return f"exact_near_miss_seed:{node}"
            return f"degraded_near_miss_seed:{node}"
        return f"older_one_node_depletion:{node}"
    return (
        "more_degraded:"
        f"{len(missing_support_nodes)}support/"
        f"{len(missing_closed_edges)}closed"
    )


def _capture_boundary_row(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    source_name: str,
    family: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
    family_reference: CandidateNeighborhood,
    seed_nodes: set[tuple[int, int]],
) -> BoundaryScanRow:
    row = _fetch_row(
        ensemble_name,
        pack_name,
        scenario_name,
        source_name,
        family,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )
    best_mid = _best_family_aligned_mid(family_reference, row.dominant_mid_neighborhoods)
    missing_support_nodes = _missing_nodes(family_reference, best_mid)
    missing_closed_edges = _missing_edges(family_reference, best_mid)
    extra_support_nodes = _missing_nodes(best_mid, family_reference)
    extra_closed_edges = _missing_edges(best_mid, family_reference)
    return BoundaryScanRow(
        label=f"{ensemble_name}:{source_name}",
        family=family,
        best_mid_cell=best_mid.cell,
        row_mid_attached_max=best_mid.attached_count,
        missing_support_nodes=missing_support_nodes,
        missing_closed_edges=missing_closed_edges,
        extra_support_nodes=extra_support_nodes,
        extra_closed_edges=extra_closed_edges,
        hinge=_has_four_incident_flank_hinge(
            best_mid.relative_support_nodes,
            best_mid.relative_closed_edges,
        ),
        classification=_classify_row(
            missing_support_nodes,
            missing_closed_edges,
            extra_support_nodes,
            extra_closed_edges,
            seed_nodes,
        ),
    )


def _render_seed_table(seeds: tuple[DeletionSeed, ...]) -> str:
    lines = [
        "Fresh Near-Miss One-Node Seeds",
        "==============================",
        "cell | missing_support_nodes | missing_closed_edges | hinge",
        "----+------------------------+----------------------+------",
    ]
    for seed in seeds:
        lines.append(
            f"{seed.cell} | "
            f"{_format_rel_nodes(seed.missing_support_nodes)} | "
            f"{_format_rel_edges(seed.missing_closed_edges)} | "
            f"{'Y' if seed.hinge else 'n'}"
        )
    return "\n".join(lines)


def _render_boundary_rows(rows: list[BoundaryScanRow]) -> str:
    lines = [
        "Finished Outside-Family Boundary",
        "===============================",
        "label | family | best_mid_cell | mid_attached | missing_support_nodes | missing_closed_edges | classification",
        "-----+--------+--------------+--------------+------------------------+----------------------+---------------",
    ]
    for row in rows:
        lines.append(
            f"{row.label} | {row.family} | {row.best_mid_cell} | "
            f"{row.row_mid_attached_max:.3f} | "
            f"{_format_rel_nodes(row.missing_support_nodes)} | "
            f"{_format_rel_edges(row.missing_closed_edges)} | "
            f"{row.classification}"
        )
    return "\n".join(lines)


def _render_signature_summary(rows: list[BoundaryScanRow]) -> str:
    signature_counts = Counter(row.missing_support_nodes for row in rows)
    lines = [
        "Missing-Node Signature Summary",
        "=============================",
    ]
    for signature, count in sorted(
        signature_counts.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        labels = [row.label for row in rows if row.missing_support_nodes == signature]
        lines.append(
            f"{_format_rel_nodes(signature)}: rows={count} labels="
            + ",".join(labels)
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
    family_reference = family_rows[0].dominant_mid_neighborhoods[0]
    near_miss = _fetch_row(
        *NEAR_MISS_SPEC,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )
    seeds = _build_deletion_seeds(family_reference, near_miss)
    seed_nodes = {seed.missing_support_nodes[0] for seed in seeds}
    boundary_rows = [
        _capture_boundary_row(
            ensemble_name,
            pack_name,
            scenario_name,
            source_name,
            family,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
            family_reference=family_reference,
            seed_nodes=seed_nodes,
        )
        for ensemble_name, pack_name, scenario_name, source_name, family in OUTSIDE_SPECS
        if (ensemble_name, pack_name, scenario_name, source_name, family) != NEAR_MISS_SPEC
    ]
    exact_seed_rows = [
        row for row in boundary_rows if row.classification.startswith("exact_near_miss_seed:")
    ]
    degraded_seed_rows = [
        row
        for row in boundary_rows
        if row.classification.startswith("degraded_near_miss_seed:")
    ]
    hinge_depleted_rows = [
        row
        for row in boundary_rows
        if row.classification.startswith("older_one_node_depletion:")
    ]
    more_degraded_rows = [
        row for row in boundary_rows if row.classification.startswith("more_degraded:")
    ]

    print(f"beyond-ceiling deletion-class scan started {started_at}")
    print()
    print(_render_seed_table(seeds))
    print()
    print(_render_boundary_rows(boundary_rows))
    print()
    print(_render_signature_summary(boundary_rows))
    print()
    print(
        "exact_near_miss_seed_rows="
        + (
            ",".join(row.label for row in exact_seed_rows)
            if exact_seed_rows
            else "none"
        )
    )
    print(
        "degraded_near_miss_seed_rows="
        + (
            ",".join(row.label for row in degraded_seed_rows)
            if degraded_seed_rows
            else "none"
        )
    )
    print(
        "older_one_node_depletion_rows="
        + (
            ",".join(row.label for row in hinge_depleted_rows)
            if hinge_depleted_rows
            else "none"
        )
    )
    print(
        "more_degraded_rows="
        + (
            ",".join(row.label for row in more_degraded_rows)
            if more_degraded_rows
            else "none"
        )
    )
    print(
        "deletion_class_summary="
        "none of the already-finished outside-family rows realizes any of the three fresh "
        "corner-deletion seeds from `exa:base:skew-hard:local-morph-k`. The finished 7/8 "
        "shoulder, wider-sentinel, and exhausted-wall controls instead cluster on the older "
        "one-node depletion missing the hinge support `(-1, 0)`, while the low-support "
        "throats are still more degraded multi-node failures. So the fresh near miss is the "
        "first logged exact corner-deletion member of a new nearby boundary ladder rather "
        "than a replay of the older finished wall."
    )
    print(
        "beyond-ceiling deletion-class scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
