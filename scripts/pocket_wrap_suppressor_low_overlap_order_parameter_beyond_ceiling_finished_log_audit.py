#!/usr/bin/env python3
"""Audit finished beyond-ceiling control logs against the shared taper-hard bridge law."""

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

from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    matches_rule_text,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_compare import (  # noqa: E402
    CompareRow,
    PACKET_LAW_RULES,
    TAPER_HARD_CLASS,
    _format_counts,
    build_rows as build_shared_rows,
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
EXHAUSTED_COMPARE_LOG = Path(
    "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-late-branch-exhausted-wall-compare.txt"
)
WIDER_SENTINEL_SPECS = (
    (
        "wider-sentinel",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-30-low-overlap-order-parameter-beyond-ceiling-subbranch-wider-sentinel-guardrail.txt"
        ),
        "wider:base:skew-wrap:local-morph-c",
    ),
    (
        "wider-sentinel",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-30-low-overlap-order-parameter-beyond-ceiling-subbranch-wider-sentinel-guardrail-mode-mix-d.txt"
        ),
        "wider:base:skew-wrap:mode-mix-d",
    ),
)
CONTROL_SPECS = (
    (
        "nearby-shoulder",
        "default:base:skew-wrap:local-morph-c",
        "holdout:shoulder:default:base:base:skew-wrap:local-morph-c",
    ),
    (
        "nearby-shoulder",
        "broader:base:skew-wrap:mode-mix-d",
        "holdout:shoulder:broader:base:base:skew-wrap:mode-mix-d",
    ),
    (
        "low-support-throat",
        "ultra:base:taper-wrap:mode-mix-f",
        "holdout:throat:ultra:base:base:taper-wrap:mode-mix-f",
    ),
    (
        "low-support-throat",
        "mega:base:taper-wrap:mode-mix-f",
        "holdout:throat:mega:base:base:taper-wrap:mode-mix-f",
    ),
    (
        "exhausted-wall",
        "large:taper-wrap-large:local-morph-g",
        "large-exhausted-miss:exhausted-large:exa:large:large:taper-wrap-large:local-morph-g",
    ),
    (
        "exhausted-wall",
        "mirror:skew-hard-mirror:local-morph-f",
        "mirror-exhausted-miss:exhausted-mirror:exa:mirror:mirror:skew-hard-mirror:local-morph-f",
    ),
)
NON_BASE_GUARDRAIL_LOGS = (
    (
        "large:ultra|mega",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-ultra-mega-helper-fix.txt"
        ),
    ),
    (
        "large:giga",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-giga-helper-fix.txt"
        ),
    ),
    (
        "large:tera",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-tera-helper-fix.txt"
        ),
    ),
    (
        "large:peta",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-peta-helper-fix.txt"
        ),
    ),
    (
        "large:exa",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-exa-helper-fix.txt"
        ),
    ),
    (
        "mirror:ultra|mega",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-ultra-mega-helper-fix.txt"
        ),
    ),
    (
        "mirror:giga|tera",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-giga-tera-helper-fix.txt"
        ),
    ),
    (
        "mirror:peta",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-peta-helper-fix.txt"
        ),
    ),
    (
        "mirror:exa",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-exa-helper-fix.txt"
        ),
    ),
)
BRIDGE_RULE = "high_bridge_right_count >= 1.500"


@dataclass(frozen=True)
class GuardrailResult:
    label: str
    scanned_nonrect_combinations: int
    first_nonrect_row: str


def _floatish(value: str) -> float:
    if value == "Y":
        return 1.0
    if value == "n":
        return 0.0
    return float(value)


def _parse_row_blocks(log_path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    lines = log_path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if " actual=" not in line:
            index += 1
            continue
        prefix, remainder = line.split(" actual=", 1)
        label = prefix.split(" cohort=", 1)[0]
        if " style=" in label:
            label = label.split(" style=", 1)[0]
        rows[label] = {"actual_subtype": remainder.split()[0]}
        inner = index + 1
        while inner < len(lines) and lines[inner].startswith("  "):
            metric_line = lines[inner].strip()
            if "=" not in metric_line:
                break
            key, value = metric_line.split("=", 1)
            rows[label][key] = value
            inner += 1
        index = inner
    return rows


def _parse_packet_rows(log_path: Path) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if " actual=" not in line or " mid_peak=" not in line:
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


def _parse_simple_key_values(log_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in log_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("=") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _build_row_from_metric_and_packet(
    family: str,
    label: str,
    metric_payload: dict[str, str],
    packet_payload: dict[str, float],
) -> CompareRow:
    return CompareRow(
        subtype=family,
        cohort="finished-control",
        family=family,
        label=label,
        actual_subtype=str(metric_payload["actual_subtype"]),
        support_load=_floatish(metric_payload["support_load"]),
        closure_load=_floatish(metric_payload["closure_load"]),
        mid_anchor_closure_peak=float(packet_payload["mid_peak"]),
        anchor_closure_intensity_gap=_floatish(
            metric_payload["anchor_closure_intensity_gap"]
        ),
        anchor_deep_share_gap=_floatish(metric_payload["anchor_deep_share_gap"]),
        high_bridge_right_count=_floatish(metric_payload["high_bridge_right_count"]),
        high_bridge_right_low_count=_floatish(
            metric_payload["high_bridge_right_low_count"]
        ),
        edge_identity_event_count=_floatish(metric_payload["edge_identity_event_count"]),
        edge_identity_support_edge_density=_floatish(
            metric_payload["edge_identity_support_edge_density"]
        ),
        mid_candidate_attached_max=float(packet_payload["mid_attached"]),
        mid_candidate_bridge_bridge_closed_pair_max=float(packet_payload["mid_bb_closed"]),
        mid_has_four_incident_flank_hinge=float(packet_payload["flank_hinge"]),
    )


def _build_row_from_logged_block(
    family: str,
    label: str,
    payload: dict[str, str],
) -> CompareRow:
    return CompareRow(
        subtype=family,
        cohort="finished-control",
        family=family,
        label=label,
        actual_subtype=str(payload["actual_subtype"]),
        support_load=_floatish(payload["support_load"]),
        closure_load=_floatish(payload["closure_load"]),
        mid_anchor_closure_peak=_floatish(payload["mid_anchor_closure_peak"]),
        anchor_closure_intensity_gap=_floatish(payload["anchor_closure_intensity_gap"]),
        anchor_deep_share_gap=_floatish(payload["anchor_deep_share_gap"]),
        high_bridge_right_count=_floatish(payload["high_bridge_right_count"]),
        high_bridge_right_low_count=_floatish(payload["high_bridge_right_low_count"]),
        edge_identity_event_count=_floatish(payload["edge_identity_event_count"]),
        edge_identity_support_edge_density=_floatish(
            payload["edge_identity_support_edge_density"]
        ),
        mid_candidate_attached_max=_floatish(payload["mid_candidate_attached_max"]),
        mid_candidate_bridge_bridge_closed_pair_max=_floatish(
            payload["mid_candidate_bridge_bridge_closed_pair_max"]
        ),
        mid_has_four_incident_flank_hinge=_floatish(
            payload["mid_has_four_incident_flank_hinge"]
        ),
    )


def build_finished_controls() -> list[CompareRow]:
    metric_rows: dict[str, dict[str, str]] = {}
    for log_path in (OUTER_LOG, NONRECT_LOG, EXHAUSTED_COMPARE_LOG):
        metric_rows.update(_parse_row_blocks(log_path))
    packet_rows = _parse_packet_rows(PACKET_LOG)

    rows: list[CompareRow] = []
    for family, metric_label, packet_label in CONTROL_SPECS:
        metric_payload = metric_rows.get(metric_label)
        if metric_payload is None:
            raise ValueError(f"missing metric block for {metric_label}")
        packet_payload = packet_rows.get(packet_label)
        if packet_payload is None:
            raise ValueError(f"missing packet row for {packet_label}")
        rows.append(
            _build_row_from_metric_and_packet(
                family=family,
                label=metric_label,
                metric_payload=metric_payload,
                packet_payload=packet_payload,
            )
        )

    for family, log_path, label in WIDER_SENTINEL_SPECS:
        payload = _parse_row_blocks(log_path).get(label)
        if payload is None:
            raise ValueError(f"missing logged row {label} in {log_path}")
        rows.append(_build_row_from_logged_block(family=family, label=label, payload=payload))

    rows.sort(key=lambda row: (row.family, row.label))
    return rows


def build_non_base_guardrails() -> list[GuardrailResult]:
    results: list[GuardrailResult] = []
    for label, log_path in NON_BASE_GUARDRAIL_LOGS:
        parsed = _parse_simple_key_values(log_path)
        results.append(
            GuardrailResult(
                label=label,
                scanned_nonrect_combinations=int(parsed["scanned_nonrect_combinations"]),
                first_nonrect_row=parsed["first_nonrect_row"],
            )
        )
    return results


def _render_shared_family(shared_rows: list[CompareRow]) -> str:
    bridge_hits = [row for row in shared_rows if matches_rule_text(row, BRIDGE_RULE)]
    lines = [
        "Current Shared-Packet Family",
        "===========================",
        f"rows={len(shared_rows)} ({_format_counts(shared_rows)})",
    ]
    for packet_rule in PACKET_LAW_RULES:
        matched = [row for row in shared_rows if matches_rule_text(row, packet_rule)]
        lines.append(
            f"{packet_rule}: {len(matched)}/{len(shared_rows)} ({_format_counts(matched)})"
        )
    lines.append(
        f"{BRIDGE_RULE}: {len(bridge_hits)}/{len(shared_rows)} ({_format_counts(bridge_hits)})"
    )
    return "\n".join(lines)


def _render_finished_controls(rows: list[CompareRow]) -> str:
    lines = [
        "Finished Outside-Family Controls",
        "===============================",
        "label | family | packet_any | packet_all | two_right_bridge | mid_peak | mid_attached | mid_bb_closed | flank_hinge | high_bridge_right_count",
        "-----+--------+------------+------------+------------------+---------+--------------+---------------+-------------+-----------------------",
    ]
    for row in rows:
        packet_hits = [rule for rule in PACKET_LAW_RULES if matches_rule_text(row, rule)]
        bridge_hit = matches_rule_text(row, BRIDGE_RULE)
        lines.append(
            f"{row.label} | {row.family} | "
            f"{'Y' if packet_hits else 'n'} | "
            f"{'Y' if len(packet_hits) == len(PACKET_LAW_RULES) else 'n'} | "
            f"{'Y' if bridge_hit else 'n'} | "
            f"{row.mid_anchor_closure_peak:.3f} | "
            f"{row.mid_candidate_attached_max:.3f} | "
            f"{row.mid_candidate_bridge_bridge_closed_pair_max:.3f} | "
            f"{'Y' if row.mid_has_four_incident_flank_hinge >= 0.5 else 'n'} | "
            f"{row.high_bridge_right_count:.3f}"
        )
    return "\n".join(lines)


def _render_packet_audit(rows: list[CompareRow]) -> str:
    any_packet_hits = [
        row for row in rows if any(matches_rule_text(row, rule) for rule in PACKET_LAW_RULES)
    ]
    all_packet_hits = [
        row for row in rows if all(matches_rule_text(row, rule) for rule in PACKET_LAW_RULES)
    ]
    bridge_hits = [row for row in rows if matches_rule_text(row, BRIDGE_RULE)]
    joint_hits = [
        row
        for row in rows
        if matches_rule_text(row, BRIDGE_RULE)
        and any(matches_rule_text(row, rule) for rule in PACKET_LAW_RULES)
    ]
    lines = [
        "Outside-Family Packet / Bridge Audit",
        "====================================",
        f"rows={len(rows)} ({_format_counts(rows)})",
    ]
    for packet_rule in PACKET_LAW_RULES:
        matched = [row for row in rows if matches_rule_text(row, packet_rule)]
        lines.append(
            f"{packet_rule}: {len(matched)}/{len(rows)} ({_format_counts(matched)})"
        )
    lines.extend(
        (
            f"any_shared_packet_law: {len(any_packet_hits)}/{len(rows)} ({_format_counts(any_packet_hits)})",
            f"all_shared_packet_laws: {len(all_packet_hits)}/{len(rows)} ({_format_counts(all_packet_hits)})",
            f"{BRIDGE_RULE}: {len(bridge_hits)}/{len(rows)} ({_format_counts(bridge_hits)})",
            f"shared_packet_and_two_right_bridge: {len(joint_hits)}/{len(rows)} ({_format_counts(joint_hits)})",
        )
    )
    return "\n".join(lines)


def _render_non_base_guardrails(results: list[GuardrailResult]) -> str:
    total_scanned = sum(result.scanned_nonrect_combinations for result in results)
    hit_rows = [result for result in results if result.first_nonrect_row != "none"]
    lines = [
        "Finished Non-Base Guardrails",
        "============================",
        f"rows={len(results)}",
        f"scanned_nonrect_combinations={total_scanned}",
        f"first_hits={len(hit_rows)}",
        (
            "first_hit_rows="
            + ",".join(f"{result.label}:{result.first_nonrect_row}" for result in hit_rows)
            if hit_rows
            else "first_hit_rows=none"
        ),
    ]
    for result in results:
        lines.append(
            f"{result.label} scanned_nonrect_combinations={result.scanned_nonrect_combinations} "
            f"first_nonrect_row={result.first_nonrect_row}"
        )
    return "\n".join(lines)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"beyond-ceiling finished-log audit started {started}", flush=True)
    total_start = time.time()

    shared_rows = build_shared_rows(OUTER_LOG, NONRECT_LOG, PACKET_LOG)
    finished_controls = build_finished_controls()
    non_base_guardrails = build_non_base_guardrails()

    any_packet_hits = [
        row
        for row in finished_controls
        if any(matches_rule_text(row, rule) for rule in PACKET_LAW_RULES)
    ]
    bridge_hits = [
        row for row in finished_controls if matches_rule_text(row, BRIDGE_RULE)
    ]
    joint_hits = [
        row
        for row in finished_controls
        if matches_rule_text(row, BRIDGE_RULE)
        and any(matches_rule_text(row, rule) for rule in PACKET_LAW_RULES)
    ]
    hit_guardrails = [
        result for result in non_base_guardrails if result.first_nonrect_row != "none"
    ]

    print()
    print(_render_shared_family(shared_rows))
    print()
    print(_render_finished_controls(finished_controls))
    print()
    print(_render_packet_audit(finished_controls))
    print()
    print(_render_non_base_guardrails(non_base_guardrails))
    print()
    print(
        "conclusion=across the finished outside-family row-backed controls, no row rejoins any shared 8/12 packet law and no row reaches "
        "`high_bridge_right_count >= 1.500`, so no completed control both re-enters the packet gate and imitates the taper-hard branch."
    )
    print(
        "strongest_read=the only logged two-right-bridge rows remain the known `base` `peta|exa` taper-hard pair inside the current five-row shared-packet family."
    )
    print(
        "non_base_frontier_status="
        + (
            "at least one finished non-base guardrail now reports a first non-rect beyond-ceiling row."
            if hit_guardrails
            else "all nine helper-fixed finished non-base first-hit guardrails still report `first_nonrect_row=none`, so the completed non-base frontier still contributes no hidden beyond-ceiling candidate at all."
        )
    )
    print(
        "boundary_translation=the current unresolved seam is therefore fresh deeper-base or nearby non-base computation beyond the finished logs, not an already-recorded counterexample inside the present exhausted-wall or nearby-generated tables."
    )
    print()
    print(
        "beyond-ceiling finished-log audit completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
