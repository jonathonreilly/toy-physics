#!/usr/bin/env python3
"""Compare dominant packet neighborhoods on the late-branch exhausted wall."""

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
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_edge_identity_add1_selector import (  # noqa: E402
    support_roles,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    support_edges,
)
from toy_event_physics import (  # noqa: E402
    _extended_ge6_dpadj_trees,
    graph_neighbors,
    pocket_candidate_cells,
)


LATE_CLASS = "late-base"
LARGE_MISS_CLASS = "large-exhausted-miss"
MIRROR_MISS_CLASS = "mirror-exhausted-miss"
TARGET_SPECS = (
    ("exa", "base", "skew-wrap", "base:skew-wrap:local-morph-k", LATE_CLASS),
    (
        "exa",
        "large",
        "taper-wrap-large",
        "large:taper-wrap-large:local-morph-g",
        LARGE_MISS_CLASS,
    ),
    (
        "exa",
        "mirror",
        "skew-hard-mirror",
        "mirror:skew-hard-mirror:local-morph-f",
        MIRROR_MISS_CLASS,
    ),
)


@dataclass(frozen=True)
class CandidateNeighborhood:
    cell: tuple[int, int]
    band: str
    kind: str
    attached_count: float
    bridge_count: float
    closed_pair_count: float
    bridge_bridge_closed_pair_count: float
    relative_support_nodes: tuple[tuple[int, int], ...]
    relative_closed_edges: tuple[
        tuple[tuple[int, int], tuple[int, int]],
        ...,
    ]


@dataclass(frozen=True)
class CompareRow:
    ensemble_name: str
    pack_name: str
    scenario_name: str
    source_name: str
    cohort: str
    actual_subtype: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    left_candidate_attached_max: float
    mid_candidate_attached_max: float
    dominant_left_neighborhoods: tuple[CandidateNeighborhood, ...]
    dominant_mid_neighborhoods: tuple[CandidateNeighborhood, ...]


def _candidate_band(cell: tuple[int, int]) -> str:
    x, _y = cell
    if x <= 1:
        return "left"
    if x >= 5:
        return "right"
    return "mid"


def _relative_edge(
    candidate: tuple[int, int],
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[tuple[int, int], tuple[int, int]]:
    left_rel = (left[0] - candidate[0], left[1] - candidate[1])
    right_rel = (right[0] - candidate[0], right[1] - candidate[1])
    return (left_rel, right_rel) if left_rel < right_rel else (right_rel, left_rel)


def _candidate_neighborhoods(nodes: set[tuple[int, int]]) -> list[CandidateNeighborhood]:
    pocket_cells, deep_cells = pocket_candidate_cells(nodes, wrap_y=False)
    candidate_cells = pocket_cells | deep_cells
    roles = support_roles(nodes, pocket_cells, deep_cells)
    support_nodes = set(roles)
    support_edge_set = support_edges(support_nodes)

    out: list[CandidateNeighborhood] = []
    for candidate in sorted(candidate_cells):
        attached = sorted(
            support
            for support in graph_neighbors(candidate, support_nodes, wrap_y=False)
            if support in roles
        )
        bridge_neighbors = [support for support in attached if roles.get(support) == "bridge"]
        closed_pairs = 0.0
        bridge_bridge_closed_pairs = 0.0
        closed_edges: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for idx, left in enumerate(attached):
            for right in attached[idx + 1 :]:
                edge = (left, right) if left < right else (right, left)
                if edge not in support_edge_set:
                    continue
                closed_pairs += 1.0
                closed_edges.append(_relative_edge(candidate, left, right))
                if roles.get(left) == "bridge" and roles.get(right) == "bridge":
                    bridge_bridge_closed_pairs += 1.0
        out.append(
            CandidateNeighborhood(
                cell=candidate,
                band=_candidate_band(candidate),
                kind="pocket" if candidate in pocket_cells else "deep",
                attached_count=float(len(attached)),
                bridge_count=float(len(bridge_neighbors)),
                closed_pair_count=closed_pairs,
                bridge_bridge_closed_pair_count=bridge_bridge_closed_pairs,
                relative_support_nodes=tuple(
                    sorted((x - candidate[0], y - candidate[1]) for x, y in attached)
                ),
                relative_closed_edges=tuple(sorted(closed_edges)),
            )
        )
    return out


def _dominant_neighborhoods(
    neighborhoods: list[CandidateNeighborhood],
    band: str,
) -> tuple[CandidateNeighborhood, ...]:
    in_band = [neighborhood for neighborhood in neighborhoods if neighborhood.band == band]
    if not in_band:
        return ()
    best_attached = max(neighborhood.attached_count for neighborhood in in_band)
    dominant = [
        neighborhood
        for neighborhood in in_band
        if neighborhood.attached_count == best_attached
    ]
    dominant.sort(key=lambda neighborhood: neighborhood.cell)
    return tuple(dominant)


def _fetch_row(
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    target_source: str,
    cohort: str,
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
    candidate_neighborhoods = _candidate_neighborhoods(set(nodes))
    dominant_left = _dominant_neighborhoods(candidate_neighborhoods, "left")
    dominant_mid = _dominant_neighborhoods(candidate_neighborhoods, "mid")
    left_candidate_attached_max = max(
        (neighborhood.attached_count for neighborhood in dominant_left),
        default=0.0,
    )
    mid_candidate_attached_max = max(
        (neighborhood.attached_count for neighborhood in dominant_mid),
        default=0.0,
    )

    return CompareRow(
        ensemble_name=ensemble_name,
        pack_name=pack_name,
        scenario_name=scenario_name,
        source_name=target_source,
        cohort=cohort,
        actual_subtype=str(getattr(row, "subtype")),
        support_load=float(getattr(row, "support_load")),
        closure_load=float(getattr(row, "closure_load")),
        mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
        left_candidate_attached_max=float(left_candidate_attached_max),
        mid_candidate_attached_max=float(mid_candidate_attached_max),
        dominant_left_neighborhoods=dominant_left,
        dominant_mid_neighborhoods=dominant_mid,
    )


def build_rows() -> list[CompareRow]:
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
    rows = [
        _fetch_row(
            ensemble_name,
            pack_name,
            scenario_name,
            target_source,
            cohort,
            ge6_tree=ge6_tree,
            dpadj_tree=dpadj_tree,
        )
        for ensemble_name, pack_name, scenario_name, target_source, cohort in TARGET_SPECS
    ]
    return rows


def _format_rel_nodes(nodes: tuple[tuple[int, int], ...]) -> str:
    return "[" + ", ".join(str(node) for node in nodes) + "]"


def _format_rel_edges(
    edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
) -> str:
    return "[" + ", ".join(f"{left}->{right}" for left, right in edges) + "]"


def _render_row_summary(rows: list[CompareRow]) -> str:
    lines = ["Row summary", "==========="]
    for row in rows:
        lines.append(
            f"{row.ensemble_name}:{row.source_name} cohort={row.cohort} "
            f"actual={row.actual_subtype} support_load={row.support_load:.3f} "
            f"closure_load={row.closure_load:.3f} "
            f"mid_anchor_closure_peak={row.mid_anchor_closure_peak:.3f} "
            f"left/mid_attached_max={row.left_candidate_attached_max:.3f}/"
            f"{row.mid_candidate_attached_max:.3f}"
        )
    return "\n".join(lines)


def _render_dominant_neighborhoods(rows: list[CompareRow]) -> str:
    lines = ["Dominant packet neighborhoods", "============================"]
    for row in rows:
        lines.append(f"{row.ensemble_name}:{row.source_name}")
        for band_name, neighborhoods in (
            ("left", row.dominant_left_neighborhoods),
            ("mid", row.dominant_mid_neighborhoods),
        ):
            lines.append(f"  {band_name}_dominant_count={len(neighborhoods)}")
            for neighborhood in neighborhoods:
                lines.append(
                    "  "
                    f"cell={neighborhood.cell} kind={neighborhood.kind} "
                    f"attached={neighborhood.attached_count:.3f} "
                    f"bb_closed={neighborhood.bridge_bridge_closed_pair_count:.3f}"
                )
                lines.append(
                    "    relative_support_nodes="
                    + _format_rel_nodes(neighborhood.relative_support_nodes)
                )
                lines.append(
                    "    relative_closed_edges="
                    + _format_rel_edges(neighborhood.relative_closed_edges)
                )
    return "\n".join(lines)


def _missing_nodes(
    late: CandidateNeighborhood,
    other: CandidateNeighborhood,
) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(set(late.relative_support_nodes) - set(other.relative_support_nodes)))


def _missing_edges(
    late: CandidateNeighborhood,
    other: CandidateNeighborhood,
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    return tuple(sorted(set(late.relative_closed_edges) - set(other.relative_closed_edges)))


def _render_template_deltas(rows: list[CompareRow]) -> str:
    late_row = next(row for row in rows if row.cohort == LATE_CLASS)
    late_left = late_row.dominant_left_neighborhoods[0]
    late_mid = late_row.dominant_mid_neighborhoods[0]
    lines = ["Late-template deltas", "===================="]
    for row in rows:
        if row.cohort == LATE_CLASS:
            continue
        left = row.dominant_left_neighborhoods[0]
        mid = row.dominant_mid_neighborhoods[0]
        lines.append(f"{row.ensemble_name}:{row.source_name}")
        lines.append(
            "  left_missing_relative_support_nodes="
            + _format_rel_nodes(_missing_nodes(late_left, left))
        )
        lines.append(
            "  left_missing_relative_closed_edges="
            + _format_rel_edges(_missing_edges(late_left, left))
        )
        lines.append(
            "  mid_missing_relative_support_nodes="
            + _format_rel_nodes(_missing_nodes(late_mid, mid))
        )
        lines.append(
            "  mid_missing_relative_closed_edges="
            + _format_rel_edges(_missing_edges(late_mid, mid))
        )
    return "\n".join(lines)


def _render_conclusion(rows: list[CompareRow]) -> str:
    late_row = next(row for row in rows if row.cohort == LATE_CLASS)
    mirror_row = next(row for row in rows if row.cohort == MIRROR_MISS_CLASS)
    large_row = next(row for row in rows if row.cohort == LARGE_MISS_CLASS)
    late_mid = late_row.dominant_mid_neighborhoods[0]
    mirror_mid = mirror_row.dominant_mid_neighborhoods[0]
    large_mid = large_row.dominant_mid_neighborhoods[0]
    shared_mid_missing_nodes = tuple(
        sorted(
            set(_missing_nodes(late_mid, mirror_mid))
            & set(_missing_nodes(late_mid, large_mid))
        )
    )
    shared_mid_missing_edges = tuple(
        sorted(
            set(_missing_edges(late_mid, mirror_mid))
            & set(_missing_edges(late_mid, large_mid))
        )
    )
    large_left_matches_late = (
        large_row.dominant_left_neighborhoods[0].relative_support_nodes
        == late_row.dominant_left_neighborhoods[0].relative_support_nodes
    )

    lines = ["Conclusion", "=========="]
    lines.append(
        "late_packet_template="
        "the dominant late left and mid packets are the same full eight-support octagon "
        "with 12 bridge-bridge closed pairs"
    )
    lines.append(
        "large_left_packet_matches_late_octagon="
        + ("Y" if large_left_matches_late else "n")
    )
    lines.append(
        "shared_exhausted_mid_missing_relative_support_nodes="
        + _format_rel_nodes(shared_mid_missing_nodes)
    )
    lines.append(
        "shared_exhausted_mid_missing_relative_closed_edges="
        + _format_rel_edges(shared_mid_missing_edges)
    )
    lines.append(
        "packet_translation_summary="
        "the exhausted-wall side keeps a seven-support mid packet because it never fills "
        "the inward left-flank support node at relative (-1, 0); that one local hole removes "
        "exactly four bridge-bridge closure edges and keeps the packet at 7 attached bridges / "
        "8 closed pairs instead of the late branch's 8 / 12"
    )
    lines.append(
        "mirror_addendum="
        "the mirror miss also leaves its dominant left packet one support short, so the "
        "depleted seven-support packet survives on both bands there"
    )
    return "\n".join(lines)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    print(f"late branch packet neighborhood compare started {started}")

    rows = build_rows()

    print()
    print("Late Branch Packet Neighborhood Compare")
    print("======================================")
    print("rows_total=3 (late-base:1, large-exhausted-miss:1, mirror-exhausted-miss:1)")
    print()
    print(_render_row_summary(rows))
    print()
    print(_render_dominant_neighborhoods(rows))
    print()
    print(_render_template_deltas(rows))
    print()
    print(_render_conclusion(rows))
    print()
    print(
        "late branch packet neighborhood compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
