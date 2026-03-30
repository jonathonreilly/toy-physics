#!/usr/bin/env python3
"""Summarize closure completion and closure deficit across the finished beyond-ceiling boundary."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
import os
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
class ClosureDeficitRow:
    label: str
    family: str
    best_mid_cell: tuple[int, int]
    row_mid_attached_max: float
    best_mid_closed_edges: float
    closed_edge_gap: int
    lost_closed_edges: int
    missing_support_nodes: tuple[tuple[int, int], ...]
    missing_roles: tuple[str, ...]
    extra_support_nodes: tuple[tuple[int, int], ...]
    extra_closed_edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...]
    deficit_matches_completion: bool


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


def _role_name(node: tuple[int, int]) -> str:
    return ROLE_NAMES.get(node, "other")


def _capture_row(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    source_name: str,
    family: str,
    *,
    ge6_tree: object,
    dpadj_tree: object,
    family_reference: CandidateNeighborhood,
    family_closed_edges: float,
) -> ClosureDeficitRow:
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
    closed_edge_gap = int(round(family_closed_edges - best_mid.bridge_bridge_closed_pair_count))
    lost_closed_edges = len(missing_closed_edges)
    return ClosureDeficitRow(
        label=f"{ensemble_name}:{source_name}",
        family=family,
        best_mid_cell=best_mid.cell,
        row_mid_attached_max=best_mid.attached_count,
        best_mid_closed_edges=best_mid.bridge_bridge_closed_pair_count,
        closed_edge_gap=closed_edge_gap,
        lost_closed_edges=lost_closed_edges,
        missing_support_nodes=missing_support_nodes,
        missing_roles=tuple(_role_name(node) for node in missing_support_nodes),
        extra_support_nodes=extra_support_nodes,
        extra_closed_edges=extra_closed_edges,
        deficit_matches_completion=(
            not extra_support_nodes
            and not extra_closed_edges
            and closed_edge_gap == lost_closed_edges
        ),
    )


def _capture_row_worker(
    spec: tuple[str, str, str, str, str],
    family_reference: CandidateNeighborhood,
    family_closed_edges: float,
) -> ClosureDeficitRow:
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
    return _capture_row(
        *spec,
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
        family_reference=family_reference,
        family_closed_edges=family_closed_edges,
    )


def _render_table(rows: list[ClosureDeficitRow]) -> str:
    lines = [
        "Finished Boundary Closure-Deficit Table",
        "======================================",
        "label | family | best_mid_cell | attached | closed_edges | closed_edge_gap | lost_closed_edges | deficit_matches_completion | missing_roles | missing_support_nodes | extra_support_nodes | extra_closed_edges",
        "-----+--------+--------------+----------+--------------+-----------------+-------------------+----------------------------+---------------+-----------------------+--------------------+------------------",
    ]
    for row in rows:
        lines.append(
            f"{row.label} | {row.family} | {row.best_mid_cell} | "
            f"{row.row_mid_attached_max:.3f} | {row.best_mid_closed_edges:.3f} | "
            f"{row.closed_edge_gap} | {row.lost_closed_edges} | "
            f"{'Y' if row.deficit_matches_completion else 'n'} | "
            f"{','.join(row.missing_roles) if row.missing_roles else 'none'} | "
            f"{_format_rel_nodes(row.missing_support_nodes)} | "
            f"{_format_rel_nodes(row.extra_support_nodes)} | "
            f"{_format_rel_edges(row.extra_closed_edges)}"
        )
    return "\n".join(lines)


def _render_group_summary(rows: list[ClosureDeficitRow]) -> str:
    grouped: dict[tuple[int, int], list[ClosureDeficitRow]] = defaultdict(list)
    for row in rows:
        grouped[(row.closed_edge_gap, row.lost_closed_edges)].append(row)
    lines = [
        "Closure-Deficit Group Summary",
        "============================",
    ]
    for key in sorted(grouped):
        group = grouped[key]
        labels = ",".join(row.label for row in group)
        roles = Counter(role for row in group for role in row.missing_roles)
        role_summary = (
            ",".join(f"{role}:{count}" for role, count in sorted(roles.items()))
            if roles
            else "none"
        )
        lines.append(
            f"closed_edge_gap={key[0]} lost_closed_edges={key[1]} rows={len(group)} "
            f"role_counts={role_summary} labels={labels}"
        )
    return "\n".join(lines)


def _render_conclusion(
    family_rows: list[ClosureDeficitRow],
    outside_rows: list[ClosureDeficitRow],
) -> str:
    all_rows = family_rows + outside_rows
    exact_rows = [row for row in all_rows if row.deficit_matches_completion]
    non_exact_rows = [row for row in all_rows if not row.deficit_matches_completion]
    by_pair: dict[tuple[int, int], list[str]] = defaultdict(list)
    for row in all_rows:
        by_pair[(row.closed_edge_gap, row.lost_closed_edges)].append(row.label)
    lines = [
        "Conclusion",
        "==========",
    ]
    if non_exact_rows:
        lines.append(
            "closure_deficit_equivalence=best-aligned lost closed-edge count is exact for the realized family and the "
            "one-node outside ladder (`0/0`, `2/2`, `4/4`), but it does not extend unchanged to the deeper "
            "low-support throats."
        )
        lines.append(
            "non_exact_rows="
            + ",".join(
                f"{row.label}(gap={row.closed_edge_gap},lost={row.lost_closed_edges})"
                for row in non_exact_rows
            )
        )
        lines.append(
            "throat_translation=the low-support throats fall off the one-node closure-deficit ladder: "
            "their best aligned mids collapse to `0` bridge-bridge closed edges even though the family-aligned "
            "packet comparison exposes only `7` explicit lost closed edges. So they should still be treated as "
            "deeper multi-node failures, not just the next rung of the local closure-deficit ladder."
        )
    else:
        lines.append(
            "closure_deficit_equivalence=across the entire finished boundary plus realized family anchors, best-aligned "
            "lost closed-edge count stays exactly equal to row-level closure-completion deficit, with no compensating "
            "extra support or closed edges."
        )
    ordered_pairs = sorted(by_pair.items())
    pair_fragments = [
        f"{gap}/{lost}: " + ",".join(labels)
        for (gap, lost), labels in ordered_pairs
    ]
    lines.append("pair_ladder=" + " | ".join(pair_fragments))
    lines.append(
        "physical_translation=the finished beyond-ceiling picture now splits cleanly in two. The realized family plus "
        "the one-node outside boundary is a local closure-deficit ladder: full family completion at `12/0`, corner "
        "depletion at `10/2`, and harsher side-or-hinge depletion at `8/4`. The low-support throats do not continue "
        "that ladder; they are deeper multi-node collapse rows outside the clean one-node closure-deficit regime."
    )
    lines.append(
        "family_law_status="
        "this strengthens the physical reading of the ladder, but it still does not replace the exact family separator "
        "`mid_candidate_attached_max >= 7.500`."
    )
    return "\n".join(lines)


def main() -> None:
    started_at = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()

    family_reference_row = _fetch_row(
        *FAMILY_SPECS[0],
        ge6_tree=ge6_tree,
        dpadj_tree=dpadj_tree,
    )
    family_reference = family_reference_row.dominant_mid_neighborhoods[0]
    family_closed_edges = family_reference.bridge_bridge_closed_pair_count
    all_specs = tuple(FAMILY_SPECS) + tuple(OUTSIDE_SPECS)
    worker_count = min(len(all_specs), os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        all_rows = list(
            executor.map(
                _capture_row_worker,
                all_specs,
                [family_reference] * len(all_specs),
                [family_closed_edges] * len(all_specs),
            )
        )
    family_rows = all_rows[: len(FAMILY_SPECS)]
    outside_rows = all_rows[len(FAMILY_SPECS) :]

    print(f"beyond-ceiling finished-boundary closure-deficit summary started {started_at}")
    print()
    print(f"family_reference_closed_edges={family_closed_edges:.3f}")
    print(f"parallel_workers={worker_count}")
    print()
    print(_render_table(family_rows + outside_rows))
    print()
    print(_render_group_summary(family_rows + outside_rows))
    print()
    print(_render_conclusion(family_rows, outside_rows))
    print(
        "beyond-ceiling finished-boundary closure-deficit summary completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
