#!/usr/bin/env python3
"""Translate the late-branch exhausted-wall packet completion into topology terms."""

from __future__ import annotations

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

from pocket_wrap_suppressor_low_overlap_order_parameter_late_branch_packet_neighborhood_compare import (  # noqa: E402
    LATE_CLASS,
    _missing_edges,
    _missing_nodes,
    build_rows,
)


def _format_rel_nodes(nodes: tuple[tuple[int, int], ...]) -> str:
    return "[" + ", ".join(str(node) for node in nodes) + "]"


def _format_rel_edges(
    edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
) -> str:
    return "[" + ", ".join(f"{left}->{right}" for left, right in edges) + "]"


def _other_endpoint(
    node: tuple[int, int],
    edge: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    left, right = edge
    if left == node:
        return right
    if right == node:
        return left
    raise ValueError(f"edge {edge} does not contain node {node}")


def main() -> None:
    started_at = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    rows = build_rows()

    late_rows = [row for row in rows if row.cohort == LATE_CLASS]
    exhausted_rows = [row for row in rows if row.cohort != LATE_CLASS]
    exhausted_mid = exhausted_rows[0].dominant_mid_neighborhoods[0]

    late_completion_node_sets = [
        set(_missing_nodes(row.dominant_mid_neighborhoods[0], exhausted_mid))
        for row in late_rows
    ]
    late_completion_edge_sets = [
        set(_missing_edges(row.dominant_mid_neighborhoods[0], exhausted_mid))
        for row in late_rows
    ]
    shared_completion_nodes = tuple(sorted(set.intersection(*late_completion_node_sets)))
    shared_completion_edges = tuple(sorted(set.intersection(*late_completion_edge_sets)))
    completion_uniform = (
        len({frozenset(node_set) for node_set in late_completion_node_sets}) == 1
        and len({frozenset(edge_set) for edge_set in late_completion_edge_sets}) == 1
    )

    hinge_node = shared_completion_nodes[0]
    hinge_edges = tuple(
        sorted(edge for edge in shared_completion_edges if hinge_node in edge)
    )
    hinge_neighbors = tuple(
        sorted(_other_endpoint(hinge_node, edge) for edge in hinge_edges)
    )

    same_column_neighbors = sum(1 for x, _y in hinge_neighbors if x == hinge_node[0])
    inward_neighbors = sum(1 for x, _y in hinge_neighbors if x > hinge_node[0])
    outward_neighbors = sum(1 for x, _y in hinge_neighbors if x < hinge_node[0])
    upper_neighbors = sum(1 for _x, y in hinge_neighbors if y > hinge_node[1])
    lower_neighbors = sum(1 for _x, y in hinge_neighbors if y < hinge_node[1])

    print(f"late branch packet topology translation started {started_at}")
    print()
    print("Late Branch Packet Topology Translation")
    print("======================================")
    print(f"rows_total={len(rows)}")
    print("late_rows=" + ",".join(f"{row.ensemble_name}:{row.source_name}" for row in late_rows))
    print(
        "exhausted_rows="
        + ",".join(f"{row.ensemble_name}:{row.source_name}" for row in exhausted_rows)
    )
    print("late_completion_uniform=" + ("Y" if completion_uniform else "n"))
    print(
        "shared_completion_relative_support_nodes="
        + _format_rel_nodes(shared_completion_nodes)
    )
    print(
        "shared_completion_relative_closed_edges="
        + _format_rel_edges(shared_completion_edges)
    )
    print(f"completion_hinge_relative_node={hinge_node}")
    print(f"completion_hinge_incident_closed_edge_count={len(hinge_edges)}")
    print("completion_hinge_incident_closed_edges=" + _format_rel_edges(hinge_edges))
    print("completion_hinge_neighbor_nodes=" + _format_rel_nodes(hinge_neighbors))
    print(f"completion_hinge_same_column_neighbor_count={same_column_neighbors}")
    print(f"completion_hinge_inward_neighbor_count={inward_neighbors}")
    print(f"completion_hinge_outward_neighbor_count={outward_neighbors}")
    print(f"completion_hinge_upper_neighbor_count={upper_neighbors}")
    print(f"completion_hinge_lower_neighbor_count={lower_neighbors}")
    print(
        "topology_translation_summary="
        "the late branch repairs the exhausted seven-support mid packet by inserting one "
        "four-incident flank hinge. That hinge touches two same-column neighbors and two "
        "inward neighbors, so it simultaneously restores the local vertical flank ladder "
        "and the two inward bridge-bridge closures into the packet interior."
    )
    print(
        "late branch packet topology translation completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
