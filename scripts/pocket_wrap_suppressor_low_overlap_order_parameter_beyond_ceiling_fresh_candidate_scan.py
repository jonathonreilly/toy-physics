#!/usr/bin/env python3
"""Rank fresh beyond-ceiling candidates outside the current shared-packet family."""

from __future__ import annotations

import argparse
from collections import defaultdict
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
    matches_rule_text,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_compare import (  # noqa: E402
    PACKET_LAW_RULES,
)
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
    _candidate_neighborhoods,
    _dominant_neighborhoods,
)
from toy_event_physics import (  # noqa: E402
    _extended_ge6_dpadj_trees,
    benchmark_packs,
)


EXCLUDED_SOURCE_NAMES = {
    "base:rect-wrap:local-morph-f",
    "base:taper-hard:local-morph-f",
    "base:skew-wrap:local-morph-k",
    "base:skew-wrap:local-morph-c",
    "base:skew-wrap:mode-mix-d",
    "base:taper-wrap:mode-mix-f",
    "large:taper-wrap-large:local-morph-g",
    "mirror:skew-hard-mirror:local-morph-f",
}


@dataclass(frozen=True)
class CandidateRow:
    ensemble_name: str
    pack_name: str
    scenario_name: str
    source_name: str
    actual_subtype: str
    style: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    high_bridge_right_count: float
    anchor_closure_intensity_gap: float
    anchor_deep_share_gap: float
    mid_candidate_attached_max: float
    mid_candidate_bridge_bridge_closed_pair_max: float
    mid_has_four_incident_flank_hinge: float
    shared_packet_membership: int


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ensembles",
        nargs="+",
        default=["ultra", "mega", "peta", "exa"],
    )
    parser.add_argument(
        "--packs",
        nargs="+",
        default=["base", "large", "mirror"],
    )
    parser.add_argument(
        "--scenario-specs",
        nargs="+",
        help="optional pack:scenario allow-list for targeted scans",
    )
    parser.add_argument("--top-k", type=int, default=12)
    return parser


def _candidate_sort_key(row: CandidateRow) -> tuple[float, ...]:
    return (
        float(row.shared_packet_membership),
        row.high_bridge_right_count,
        row.mid_anchor_closure_peak,
        row.mid_candidate_attached_max,
        row.closure_load,
        row.support_load,
    )


def _capture_row(
    *,
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    row: object,
    nodes: set[tuple[int, int]],
    style: str,
) -> CandidateRow:
    mid_peak = float(getattr(row, "mid_anchor_closure_peak"))
    mid_attached = 0.0
    flank_hinge = 0.0
    if mid_peak >= 8.0:
        dominant_mid = _dominant_neighborhoods(_candidate_neighborhoods(nodes), "mid")
        mid_attached = max(
            (neighborhood.attached_count for neighborhood in dominant_mid),
            default=0.0,
        )
        flank_hinge = 1.0 if any(
            _has_four_incident_flank_hinge(
                neighborhood.relative_support_nodes,
                neighborhood.relative_closed_edges,
            )
            for neighborhood in dominant_mid
        ) else 0.0

    probe = type(
        "Probe",
        (),
        {
            "mid_anchor_closure_peak": mid_peak,
            "mid_candidate_bridge_bridge_closed_pair_max": mid_peak,
            "mid_candidate_attached_max": mid_attached,
            "mid_has_four_incident_flank_hinge": flank_hinge,
        },
    )()
    shared_packet_membership = sum(
        int(matches_rule_text(probe, rule_text)) for rule_text in PACKET_LAW_RULES
    )

    return CandidateRow(
        ensemble_name=ensemble_name,
        pack_name=pack_name,
        scenario_name=scenario_name,
        source_name=str(getattr(row, "source_name")),
        actual_subtype=str(getattr(row, "subtype")),
        style=style,
        support_load=float(getattr(row, "support_load")),
        closure_load=float(getattr(row, "closure_load")),
        mid_anchor_closure_peak=mid_peak,
        high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
        anchor_closure_intensity_gap=float(
            getattr(row, "anchor_closure_intensity_gap")
        ),
        anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
        mid_candidate_attached_max=mid_attached,
        mid_candidate_bridge_bridge_closed_pair_max=mid_peak,
        mid_has_four_incident_flank_hinge=flank_hinge,
        shared_packet_membership=shared_packet_membership,
    )


def build_rows(
    ensemble_names: tuple[str, ...],
    pack_names: tuple[str, ...],
    scenario_specs: tuple[str, ...] | None,
) -> list[CandidateRow]:
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
    allowed_specs = None
    if scenario_specs:
        allowed_specs = set()
        for spec in scenario_specs:
            pack_name, scenario_name = spec.split(":", 1)
            allowed_specs.add((pack_name, scenario_name))
    out: list[CandidateRow] = []
    for pack_name, scenarios in benchmark_packs():
        if pack_name not in pack_names:
            continue
        for scenario_name, _nodes, _wrap_y in scenarios:
            if allowed_specs is not None and (pack_name, scenario_name) not in allowed_specs:
                continue
            for ensemble_name in ensemble_names:
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
                _wrap_y, entries = _variant_entries(ensemble_name, pack_name, scenario_name)
                entry_by_source = {
                    source_name: (set(nodes), style) for source_name, nodes, style in entries
                }
                for row in rows:
                    source_name = str(getattr(row, "source_name"))
                    if source_name in EXCLUDED_SOURCE_NAMES:
                        continue
                    if str(getattr(row, "subtype")) != "pair-only-sensitive":
                        continue
                    nodes, style = entry_by_source[source_name]
                    out.append(
                        _capture_row(
                            ensemble_name=ensemble_name,
                            pack_name=pack_name,
                            scenario_name=scenario_name,
                            row=row,
                            nodes=nodes,
                            style=style,
                        )
                    )
    return out


def _render_grouped_candidates(rows: list[CandidateRow], *, top_k: int) -> str:
    grouped: dict[tuple[str, str, str], list[CandidateRow]] = defaultdict(list)
    for row in rows:
        grouped[(row.pack_name, row.scenario_name, row.source_name)].append(row)

    representatives: list[tuple[CandidateRow, list[str]]] = []
    for _key, group in grouped.items():
        group.sort(key=_candidate_sort_key, reverse=True)
        representatives.append((group[0], sorted({row.ensemble_name for row in group})))
    representatives.sort(key=lambda item: _candidate_sort_key(item[0]), reverse=True)

    lines = [
        "Top Fresh Candidates",
        "====================",
    ]
    for representative, ensembles in representatives[:top_k]:
        lines.append(
            f"{representative.pack_name}:{representative.scenario_name}:{representative.source_name}"
        )
        lines.append(f"  ensembles={','.join(ensembles)}")
        lines.append(f"  style={representative.style}")
        lines.append(f"  actual={representative.actual_subtype}")
        lines.append(f"  support_load={representative.support_load:.3f}")
        lines.append(f"  closure_load={representative.closure_load:.3f}")
        lines.append(f"  mid_anchor_closure_peak={representative.mid_anchor_closure_peak:.3f}")
        lines.append(
            f"  mid_candidate_attached_max={representative.mid_candidate_attached_max:.3f}"
        )
        lines.append(
            "  mid_candidate_bridge_bridge_closed_pair_max="
            f"{representative.mid_candidate_bridge_bridge_closed_pair_max:.3f}"
        )
        lines.append(
            f"  mid_has_four_incident_flank_hinge={'Y' if representative.mid_has_four_incident_flank_hinge >= 0.5 else 'n'}"
        )
        lines.append(f"  shared_packet_membership={representative.shared_packet_membership}/4")
        lines.append(
            f"  high_bridge_right_count={representative.high_bridge_right_count:.3f}"
        )
        lines.append(
            "  anchor_closure_intensity_gap="
            f"{representative.anchor_closure_intensity_gap:.3f}"
        )
        lines.append(
            f"  anchor_deep_share_gap={representative.anchor_deep_share_gap:.3f}"
        )
    if len(representatives) > top_k:
        lines.append(f"... {len(representatives) - top_k} more grouped fresh candidates")
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    ensemble_names = tuple(dict.fromkeys(args.ensembles))
    pack_names = tuple(dict.fromkeys(args.packs))
    scenario_specs = tuple(dict.fromkeys(args.scenario_specs)) if args.scenario_specs else None
    print(f"beyond-ceiling fresh candidate scan started {started}", flush=True)
    rows = build_rows(ensemble_names, pack_names, scenario_specs)

    top_hit = max(rows, key=_candidate_sort_key) if rows else None

    print()
    print("Beyond-Ceiling Fresh Candidate Scan")
    print("===================================")
    print(f"ensembles={','.join(ensemble_names)}")
    print(f"packs={','.join(pack_names)}")
    if scenario_specs is None:
        print("scenario_specs=all benchmark scenarios for selected packs")
    else:
        print(f"scenario_specs={','.join(scenario_specs)}")
    print(f"excluded_sources={','.join(sorted(EXCLUDED_SOURCE_NAMES))}")
    print(f"rows_total={len(rows)}")
    if top_hit is None:
        print("top_candidate=none")
    else:
        print(
            "top_candidate="
            f"{top_hit.ensemble_name}:{top_hit.pack_name}:{top_hit.source_name}"
        )
        print(
            "top_candidate_summary="
            f"shared_packet_membership={top_hit.shared_packet_membership}/4, "
            f"high_bridge_right_count={top_hit.high_bridge_right_count:.3f}, "
            f"mid_anchor_closure_peak={top_hit.mid_anchor_closure_peak:.3f}, "
            f"mid_candidate_attached_max={top_hit.mid_candidate_attached_max:.3f}, "
            f"closure_load={top_hit.closure_load:.3f}"
        )
    print()
    print(_render_grouped_candidates(rows, top_k=args.top_k))
    print()
    print(
        "beyond-ceiling fresh candidate scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
