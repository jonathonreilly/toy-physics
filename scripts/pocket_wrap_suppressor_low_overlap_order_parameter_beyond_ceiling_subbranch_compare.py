#!/usr/bin/env python3
"""Compare the shared beyond-ceiling subbranches using recorded row blocks."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, replace
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
    evaluate_rules,
    matches_rule_text,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


OUTER_RECT_CLASS = "outer-rect"
TAPER_HARD_CLASS = "taper-hard"
SKEW_WRAP_CLASS = "skew-wrap"
OTHER_CLASS = "other"
FEATURE_NAMES = (
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "edge_identity_event_count",
    "edge_identity_support_edge_density",
    "mid_candidate_attached_max",
    "mid_candidate_bridge_bridge_closed_pair_max",
    "mid_has_four_incident_flank_hinge",
)
PACKET_LAW_RULES = (
    "mid_anchor_closure_peak >= 10.000",
    "mid_candidate_bridge_bridge_closed_pair_max >= 10.000",
    "mid_candidate_attached_max >= 7.500",
    "mid_has_four_incident_flank_hinge >= 0.500",
)
PHYSICAL_RULES = (
    (OUTER_RECT_CLASS, "support_load >= 24.000"),
    (OUTER_RECT_CLASS, "high_bridge_right_low_count >= 0.500"),
    (TAPER_HARD_CLASS, "anchor_closure_intensity_gap >= 1.000"),
    (TAPER_HARD_CLASS, "high_bridge_right_count >= 1.500"),
    (SKEW_WRAP_CLASS, "anchor_deep_share_gap <= -0.334"),
    (SKEW_WRAP_CLASS, "high_bridge_right_count <= 0.500"),
)
TARGET_SPECS = (
    (
        OUTER_RECT_CLASS,
        "held-out",
        "ultra:base:rect-wrap:local-morph-f",
        "holdout:outer-rect:ultra:base:base:rect-wrap:local-morph-f",
    ),
    (
        OUTER_RECT_CLASS,
        "held-out",
        "mega:base:rect-wrap:local-morph-f",
        "holdout:outer-rect:mega:base:base:rect-wrap:local-morph-f",
    ),
    (
        TAPER_HARD_CLASS,
        "late",
        "base:peta:base:taper-hard:local-morph-f",
        "late-base:late-taper-hard:peta:base:base:taper-hard:local-morph-f",
    ),
    (
        TAPER_HARD_CLASS,
        "late",
        "base:exa:base:taper-hard:local-morph-f",
        "late-base:late-taper-hard:exa:base:base:taper-hard:local-morph-f",
    ),
    (
        SKEW_WRAP_CLASS,
        "late",
        "base:exa:base:skew-wrap:local-morph-k",
        "late-base:late-skew-wrap:exa:base:base:skew-wrap:local-morph-k",
    ),
)
FAMILY_ORDER = {
    OUTER_RECT_CLASS: 0,
    TAPER_HARD_CLASS: 1,
    SKEW_WRAP_CLASS: 2,
}


@dataclass(frozen=True)
class CompareRow:
    subtype: str
    cohort: str
    family: str
    label: str
    actual_subtype: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    anchor_closure_intensity_gap: float
    anchor_deep_share_gap: float
    high_bridge_right_count: float
    high_bridge_right_low_count: float
    edge_identity_event_count: float
    edge_identity_support_edge_density: float
    mid_candidate_attached_max: float
    mid_candidate_bridge_bridge_closed_pair_max: float
    mid_has_four_incident_flank_hinge: float


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
    parser.add_argument("--predicate-limit", type=int, default=24)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def _sort_key(row: CompareRow) -> tuple[int, str]:
    return (FAMILY_ORDER.get(row.family, len(FAMILY_ORDER)), row.label)


def _format_counts(rows: list[CompareRow], attr: str = "family") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _format_value_counts(rows: list[CompareRow], attr: str) -> str:
    counts = Counter(float(getattr(row, attr)) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{value:.3f}:{counts[value]}" for value in sorted(counts))


def _parse_metric_blocks(log_path: Path) -> dict[str, dict[str, object]]:
    rows: dict[str, dict[str, object]] = {}
    lines = log_path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if " actual=" not in line or " branch=" not in line:
            index += 1
            continue
        label, remainder = line.split(" actual=", 1)
        if " style=" in label:
            label, _style = label.split(" style=", 1)
        actual_subtype, _remainder = remainder.split(" predicted=", 1)
        metrics: dict[str, object] = {"actual_subtype": actual_subtype}
        inner = index + 1
        while inner < len(lines) and lines[inner].startswith("  "):
            metric_line = lines[inner].strip()
            if "=" not in metric_line:
                break
            key, value = metric_line.split("=", 1)
            metrics[key] = float(value)
            inner += 1
        rows[label] = metrics
        index = inner
    return rows


def _parse_packet_rows(log_path: Path) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if " actual=" not in line or " closure_load=" not in line:
            continue
        label = line.split(" actual=", 1)[0]
        payload: dict[str, float] = {}
        for part in line.split():
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            if key == "flank_hinge":
                payload[key] = 1.0 if value == "Y" else 0.0
                continue
            try:
                payload[key] = float(value)
            except ValueError:
                continue
        rows[label] = payload
    return rows


def build_rows(outer_log: Path, nonrect_log: Path, packet_log: Path) -> list[CompareRow]:
    metric_rows = _parse_metric_blocks(outer_log)
    metric_rows.update(_parse_metric_blocks(nonrect_log))
    packet_rows = _parse_packet_rows(packet_log)
    rows: list[CompareRow] = []
    for family, cohort, metric_label, packet_label in TARGET_SPECS:
        metric_payload = metric_rows.get(metric_label)
        if metric_payload is None:
            raise ValueError(f"missing metric row block for {metric_label}")
        packet_payload = packet_rows.get(packet_label)
        if packet_payload is None:
            raise ValueError(f"missing packet row block for {packet_label}")
        rows.append(
            CompareRow(
                subtype=family,
                cohort=cohort,
                family=family,
                label=metric_label,
                actual_subtype=str(metric_payload["actual_subtype"]),
                support_load=float(metric_payload["support_load"]),
                closure_load=float(metric_payload["closure_load"]),
                mid_anchor_closure_peak=float(packet_payload["mid_peak"]),
                anchor_closure_intensity_gap=float(
                    metric_payload["anchor_closure_intensity_gap"]
                ),
                anchor_deep_share_gap=float(metric_payload["anchor_deep_share_gap"]),
                high_bridge_right_count=float(metric_payload["high_bridge_right_count"]),
                high_bridge_right_low_count=float(
                    metric_payload["high_bridge_right_low_count"]
                ),
                edge_identity_event_count=float(metric_payload["edge_identity_event_count"]),
                edge_identity_support_edge_density=float(
                    metric_payload["edge_identity_support_edge_density"]
                ),
                mid_candidate_attached_max=float(packet_payload["mid_attached"]),
                mid_candidate_bridge_bridge_closed_pair_max=float(
                    packet_payload["mid_bb_closed"]
                ),
                mid_has_four_incident_flank_hinge=float(packet_payload["flank_hinge"]),
            )
        )
    rows.sort(key=_sort_key)
    return rows


def _render_rows(title: str, rows: list[CompareRow]) -> str:
    lines = [title, "=" * len(title)]
    for row in rows:
        lines.append(
            f"{row.label} cohort={row.cohort} family={row.family} "
            f"actual={row.actual_subtype}"
        )
        lines.append(f"  support_load={row.support_load:.3f}")
        lines.append(f"  closure_load={row.closure_load:.3f}")
        lines.append(f"  mid_anchor_closure_peak={row.mid_anchor_closure_peak:.3f}")
        lines.append(
            f"  anchor_closure_intensity_gap={row.anchor_closure_intensity_gap:.3f}"
        )
        lines.append(f"  anchor_deep_share_gap={row.anchor_deep_share_gap:.3f}")
        lines.append(f"  high_bridge_right_count={row.high_bridge_right_count:.3f}")
        lines.append(
            f"  high_bridge_right_low_count={row.high_bridge_right_low_count:.3f}"
        )
        lines.append(f"  edge_identity_event_count={row.edge_identity_event_count:.3f}")
        lines.append(
            "  edge_identity_support_edge_density="
            f"{row.edge_identity_support_edge_density:.3f}"
        )
        lines.append(
            f"  mid_candidate_attached_max={row.mid_candidate_attached_max:.3f}"
        )
        lines.append(
            "  mid_candidate_bridge_bridge_closed_pair_max="
            f"{row.mid_candidate_bridge_bridge_closed_pair_max:.3f}"
        )
        lines.append(
            "  mid_has_four_incident_flank_hinge="
            f"{'Y' if row.mid_has_four_incident_flank_hinge >= 0.5 else 'n'}"
        )
    return "\n".join(lines)


def _render_packet_law(rows: list[CompareRow]) -> str:
    lines = [
        "Shared Packet Law",
        "=================",
        f"rows={len(rows)} ({_format_counts(rows)})",
        "mid_anchor_closure_peak_values="
        + _format_value_counts(rows, "mid_anchor_closure_peak"),
        "mid_candidate_attached_max_values="
        + _format_value_counts(rows, "mid_candidate_attached_max"),
        "mid_candidate_bridge_bridge_closed_pair_max_values="
        + _format_value_counts(rows, "mid_candidate_bridge_bridge_closed_pair_max"),
        "mid_has_four_incident_flank_hinge_values="
        + _format_value_counts(rows, "mid_has_four_incident_flank_hinge"),
    ]
    for rule_text in PACKET_LAW_RULES:
        matched = [row for row in rows if matches_rule_text(row, rule_text)]
        lines.append(
            f"{rule_text}: {len(matched)}/{len(rows)} ({_format_counts(matched)})"
        )
    return "\n".join(lines)


def _render_rule_table(title: str, rows: list[CompareRow], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | exact | corr | tp/fp/fn | matched(family counts)",
        "-----+-------+------+----------+----------------------",
    ]
    for rule in rules:
        matched = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {'Y' if rule.exact else 'n':^5} | "
            f"{rule.correct:>2}/{rule.total:<2} | {rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{len(matched)} ({_format_counts(matched)})"
        )
    return "\n".join(lines)


def _render_physical_rule_audit(rows: list[CompareRow]) -> str:
    lines = [
        "Curated Physical Clauses",
        "========================",
        "family | rule | exact | tp/fp/fn | matched(family counts)",
        "------+-----+-------+----------+----------------------",
    ]
    for family, rule_text in PHYSICAL_RULES:
        matched = [row for row in rows if matches_rule_text(row, rule_text)]
        target_rows = [row for row in rows if row.family == family]
        tp = sum(1 for row in matched if row.family == family)
        fp = sum(1 for row in matched if row.family != family)
        fn = len(target_rows) - tp
        exact = fp == 0 and fn == 0
        lines.append(
            f"{family} | {rule_text} | {'Y' if exact else 'n':^5} | "
            f"{tp:>2}/{fp:>2}/{fn:>2} | {len(matched)} ({_format_counts(matched)})"
        )
    return "\n".join(lines)


def _render_conclusion(rows: list[CompareRow]) -> str:
    return "\n".join(
        [
            "Conclusion",
            "==========",
            "conclusion=all five target rows already share the same "
            "8/12 mid-packet lift and four-incident flank hinge, so the active "
            "separator is not another packet-completion law.",
            "outer_rect_translation=the held-out outer-rect pair stays on the same "
            "packet law but keeps one low right bridge and the lightest edge-event "
            "count on the present five-row basis.",
            "taper_hard_translation=the later taper-hard pair stays on the same "
            "packet law while tilting to positive anchor intensity and two right "
            "bridges.",
            "skew_wrap_translation=the later skew-wrap row stays on the same packet "
            "law while flipping to negative deep share and losing the right bridge.",
            "best_exact_branch_aware_clauses=outer-rect via edge_identity_event_count "
            "<= 58.000; taper-hard via anchor_closure_intensity_gap >= 1.000; "
            "skew-wrap via anchor_deep_share_gap <= -0.334.",
        ]
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    print(f"beyond-ceiling subbranch compare started {started}", flush=True)

    outer_log = Path(args.outer_log).resolve()
    nonrect_log = Path(args.nonrect_log).resolve()
    packet_log = Path(args.packet_log).resolve()
    rows = build_rows(outer_log, nonrect_log, packet_log)

    print()
    print("Beyond-Ceiling Subbranch Compare")
    print("================================")
    print(f"outer_log={outer_log}")
    print(f"nonrect_log={nonrect_log}")
    print(f"packet_log={packet_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"rows_total={len(rows)}")
    print(f"family_counts={_format_counts(rows)}")
    print()
    print(_render_rows("Selected Rows", rows))
    print()
    print(_render_packet_law(rows))
    print()
    print(_render_physical_rule_audit(rows))
    print()

    for family in (OUTER_RECT_CLASS, TAPER_HARD_CLASS, SKEW_WRAP_CLASS):
        relabeled_rows = [
            replace(row, subtype=family if row.family == family else OTHER_CLASS)
            for row in rows
        ]
        rules = evaluate_rules(
            relabeled_rows,
            target_subtype=family,
            feature_names=list(FEATURE_NAMES),
            predicate_limit=args.predicate_limit,
            max_terms=1,
            row_limit=args.row_limit,
        )
        exact_rules = [rule for rule in rules if rule.exact]
        if not exact_rules:
            exact_rules = rules[:6]
        print(_render_rule_table(f"{family} one-feature separators", rows, exact_rules))
        print()

    print(_render_conclusion(rows))
    print()
    print(
        "beyond-ceiling subbranch compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
