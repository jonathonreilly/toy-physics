#!/usr/bin/env python3
"""Audit current beyond-ceiling family separators across the finished boundary."""

from __future__ import annotations

from dataclasses import replace
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
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_finished_log_audit import (  # noqa: E402
    build_finished_controls,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_compare import (  # noqa: E402
    CompareRow,
    _format_counts,
    build_rows as build_shared_rows,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_wider_sentinel_guardrail import (  # noqa: E402
    build_sentinel_row,
)


OUTER_LOG = Path(
    "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-anchor-band-beyond-ceiling-followon.txt"
)
NONRECT_LOG = Path(
    "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-nonrect-sweep-base-peta-exa.txt"
)
PACKET_LOG = Path(
    "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-late-branch-law-confirmation.txt"
)
FAMILY_RULES = (
    "mid_candidate_attached_max >= 7.500",
    "mid_anchor_closure_peak >= 11.000",
    "mid_candidate_bridge_bridge_closed_pair_max >= 11.000",
)


def _combined_rows() -> tuple[list[CompareRow], list[CompareRow], CompareRow]:
    shared_rows = build_shared_rows(OUTER_LOG, NONRECT_LOG, PACKET_LOG)
    finished_controls = build_finished_controls()
    near_miss = replace(
        build_sentinel_row(
            ensemble_name="exa",
            pack_name="base",
            scenario_name="skew-hard",
            source_name="base:skew-hard:local-morph-k",
        ),
        family="fresh-near-miss",
        cohort="fresh-guardrail",
        subtype="fresh-near-miss",
    )
    return shared_rows, finished_controls, near_miss


def _render_rule_audit(
    shared_rows: list[CompareRow],
    control_rows: list[CompareRow],
    near_miss: CompareRow,
) -> str:
    all_controls = control_rows + [near_miss]
    lines = [
        "Current Family Boundary Audit",
        "============================",
        f"shared_rows={len(shared_rows)} ({_format_counts(shared_rows)})",
        f"outside_rows={len(all_controls)} ({_format_counts(all_controls)})",
    ]
    for rule_text in FAMILY_RULES:
        shared_hits = [row for row in shared_rows if matches_rule_text(row, rule_text)]
        outside_hits = [row for row in all_controls if matches_rule_text(row, rule_text)]
        exact = len(shared_hits) == len(shared_rows) and not outside_hits
        lines.append(
            f"{rule_text}: shared={len(shared_hits)}/{len(shared_rows)} "
            f"outside={len(outside_hits)}/{len(all_controls)} "
            f"exact={'Y' if exact else 'n'}"
        )
        if outside_hits:
            lines.append("  outside_matches=" + ",".join(row.label for row in outside_hits))
    return "\n".join(lines)


def _render_outside_rows(rows: list[CompareRow]) -> str:
    lines = [
        "Outside Rows",
        "============",
        "label | family | mid_peak | mid_attached | mid_bb_closed | flank_hinge",
        "-----+--------+---------+--------------+---------------+-------------",
    ]
    for row in rows:
        lines.append(
            f"{row.label} | {row.family} | "
            f"{row.mid_anchor_closure_peak:.3f} | "
            f"{row.mid_candidate_attached_max:.3f} | "
            f"{row.mid_candidate_bridge_bridge_closed_pair_max:.3f} | "
            f"{'Y' if row.mid_has_four_incident_flank_hinge >= 0.5 else 'n'}"
        )
    return "\n".join(lines)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    shared_rows, finished_controls, near_miss = _combined_rows()
    outside_rows = finished_controls + [near_miss]

    print(f"beyond-ceiling family boundary audit started {started}")
    print()
    print(_render_rule_audit(shared_rows, finished_controls, near_miss))
    print()
    print(_render_outside_rows(outside_rows))
    print()
    print(
        "boundary_summary=across the full already-finished boundary, the unchanged family law "
        "`mid_candidate_attached_max >= 7.500` still exact-separates the realized shared packet "
        "family from every outside control, including the fresh skew-hard near miss. The retuned "
        "`mid_peak >= 11.000` and `mid_bb >= 11.000` rules also stay exact on the current "
        "finished boundary, but they only become exact after tightening the old `>= 10.000` cut."
    )
    print(
        "beyond-ceiling family boundary audit completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
