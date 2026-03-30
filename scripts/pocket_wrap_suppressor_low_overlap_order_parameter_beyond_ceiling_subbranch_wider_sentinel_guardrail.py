#!/usr/bin/env python3
"""Extend the beyond-ceiling subbranch compare by one wider base sentinel."""

from __future__ import annotations

import argparse
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
    CompareRow,
    OTHER_CLASS,
    OUTER_RECT_CLASS,
    PACKET_LAW_RULES,
    SKEW_WRAP_CLASS,
    TAPER_HARD_CLASS,
    _format_counts,
    _render_packet_law,
    _render_rows,
    build_rows as build_baseline_rows,
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
from toy_event_physics import _extended_ge6_dpadj_trees  # noqa: E402


SENTINEL_COHORT = "wider-sentinel"
SENTINEL_FAMILY = "guardrail"
EXACT_BRANCH_RULES = (
    (OUTER_RECT_CLASS, "edge_identity_event_count <= 58.000"),
    (TAPER_HARD_CLASS, "anchor_closure_intensity_gap >= 1.000"),
    (SKEW_WRAP_CLASS, "anchor_deep_share_gap <= -0.334"),
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outer-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-anchor-band-beyond-ceiling-followon.txt",
    )
    parser.add_argument(
        "--nonrect-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-nonrect-sweep-base-peta-exa.txt",
    )
    parser.add_argument(
        "--packet-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-late-branch-law-confirmation.txt",
    )
    parser.add_argument("--sentinel-ensemble", default="wider")
    parser.add_argument("--sentinel-pack", default="base")
    parser.add_argument("--sentinel-scenario", default="skew-wrap")
    parser.add_argument("--sentinel-source", default="base:skew-wrap:local-morph-c")
    return parser


def build_sentinel_row(
    *,
    ensemble_name: str,
    pack_name: str,
    scenario_name: str,
    source_name: str,
) -> CompareRow:
    ge6_tree, dpadj_tree = _extended_ge6_dpadj_trees()
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
        entry_source_name: set(nodes)
        for entry_source_name, nodes, _style in entries
    }

    row = row_by_source[source_name]
    nodes = entry_by_source[source_name]
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

    return CompareRow(
        subtype=SENTINEL_FAMILY,
        cohort=SENTINEL_COHORT,
        family=SENTINEL_FAMILY,
        label=f"{ensemble_name}:{source_name}",
        actual_subtype=str(getattr(row, "subtype")),
        support_load=float(getattr(row, "support_load")),
        closure_load=float(getattr(row, "closure_load")),
        mid_anchor_closure_peak=mid_peak,
        anchor_closure_intensity_gap=float(
            getattr(row, "anchor_closure_intensity_gap")
        ),
        anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
        high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
        high_bridge_right_low_count=float(
            getattr(row, "high_bridge_right_low_count")
        ),
        edge_identity_event_count=float(getattr(row, "edge_identity_event_count")),
        edge_identity_support_edge_density=float(
            getattr(row, "edge_identity_support_edge_density")
        ),
        mid_candidate_attached_max=mid_attached,
        mid_candidate_bridge_bridge_closed_pair_max=mid_peak,
        mid_has_four_incident_flank_hinge=flank_hinge,
    )


def _render_sentinel_packet_audit(sentinel: CompareRow) -> str:
    lines = [
        "Wider Sentinel Packet Audit",
        "===========================",
        f"sentinel={sentinel.label}",
        f"actual={sentinel.actual_subtype}",
    ]
    matched_total = 0
    for rule_text in PACKET_LAW_RULES:
        matched = matches_rule_text(sentinel, rule_text)
        matched_total += int(matched)
        lines.append(f"{rule_text}: {'Y' if matched else 'n'}")
    lines.append(
        f"shared_packet_membership={matched_total}/{len(PACKET_LAW_RULES)}"
    )
    return "\n".join(lines)


def _render_branch_guardrail(rows: list[CompareRow], sentinel: CompareRow) -> str:
    combined_rows = rows + [sentinel]
    lines = [
        "Current Branch Clauses On Wider Sentinel",
        "=======================================",
        "family | rule | exact_with_sentinel | sentinel_match | tp/fp/fn | matched(family counts)",
        "------+-----+--------------------+---------------+----------+----------------------",
    ]
    for family, rule_text in EXACT_BRANCH_RULES:
        matched = [row for row in combined_rows if matches_rule_text(row, rule_text)]
        target_rows = [row for row in combined_rows if row.family == family]
        tp = sum(1 for row in matched if row.family == family)
        fp = sum(1 for row in matched if row.family != family)
        fn = len(target_rows) - tp
        exact = fp == 0 and fn == 0
        lines.append(
            f"{family} | {rule_text} | {'Y' if exact else 'n':^18} | "
            f"{'Y' if matches_rule_text(sentinel, rule_text) else 'n':^13} | "
            f"{tp:>2}/{fp:>2}/{fn:>2} | {len(matched)} ({_format_counts(matched)})"
        )
    return "\n".join(lines)


def _render_conclusion(sentinel: CompareRow) -> str:
    leaking_rules = [
        f"{family} via {rule_text}"
        for family, rule_text in EXACT_BRANCH_RULES
        if matches_rule_text(sentinel, rule_text)
    ]
    packet_hits = [
        rule_text for rule_text in PACKET_LAW_RULES if matches_rule_text(sentinel, rule_text)
    ]
    if leaking_rules:
        first_failure = "; ".join(leaking_rules)
    else:
        first_failure = "none of the three exact branch clauses light up on the wider sentinel"
    if packet_hits:
        packet_status = ", ".join(packet_hits)
    else:
        packet_status = "none"
    return "\n".join(
        [
            "Conclusion",
            "==========",
            "conclusion=the nearest wider base sentinel does not join the shared beyond-ceiling "
            "8/12 packet regime, so this guardrail does not add a fourth shared-packet subbranch.",
            "sentinel_translation=the wider skew-wrap shoulder keeps the same broader base family "
            "but stalls below the common packet lift at `mid_anchor_closure_peak = 8.000`, "
            f"`mid_candidate_attached_max = {sentinel.mid_candidate_attached_max:.3f}`, and "
            f"four-incident flank hinge = {'Y' if sentinel.mid_has_four_incident_flank_hinge >= 0.5 else 'n'}.",
            f"shared_packet_rules_hit={packet_status}.",
            f"first_clause_failure={first_failure}.",
            "branch_guardrail_read=the current taper-hard intensity clause is only exact inside "
            "the shared-packet family; once the compare steps out to the nearest wider base shoulder, "
            "that clause lights up before the packet law itself does.",
        ]
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    print(f"beyond-ceiling wider sentinel guardrail started {started}", flush=True)

    baseline_rows = build_baseline_rows(
        Path(args.outer_log).resolve(),
        Path(args.nonrect_log).resolve(),
        Path(args.packet_log).resolve(),
    )
    sentinel = build_sentinel_row(
        ensemble_name=args.sentinel_ensemble,
        pack_name=args.sentinel_pack,
        scenario_name=args.sentinel_scenario,
        source_name=args.sentinel_source,
    )
    combined_rows = baseline_rows + [sentinel]

    print()
    print("Beyond-Ceiling Wider Sentinel Guardrail")
    print("=======================================")
    print(f"outer_log={Path(args.outer_log).resolve()}")
    print(f"nonrect_log={Path(args.nonrect_log).resolve()}")
    print(f"packet_log={Path(args.packet_log).resolve()}")
    print(
        "sentinel="
        f"{args.sentinel_ensemble}:{args.sentinel_source}"
    )
    print(f"rows_total={len(combined_rows)}")
    print(f"family_counts={_format_counts(combined_rows)}")
    print()
    print(_render_rows("Baseline Shared-Packet Rows", baseline_rows))
    print()
    print(_render_rows("Extended Rows", combined_rows))
    print()
    print(_render_packet_law(combined_rows))
    print()
    print(_render_sentinel_packet_audit(sentinel))
    print()
    print(_render_branch_guardrail(baseline_rows, sentinel))
    print()
    print(_render_conclusion(sentinel))
    print()
    print(
        "beyond-ceiling wider sentinel guardrail completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
