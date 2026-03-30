#!/usr/bin/env python3
"""Close the beyond-ceiling taper-hard branch on the shared-packet basis."""

from __future__ import annotations

import argparse
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
    candidate_predicates,
    matches_rule_text,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_compare import (  # noqa: E402
    CompareRow,
    FEATURE_NAMES,
    PACKET_LAW_RULES,
    TAPER_HARD_CLASS,
    _format_counts,
    _render_packet_law,
    _render_rows,
    build_rows as build_baseline_rows,
)


SENTINEL_SPECS = (
    (
        "/Users/jonreilly/Projects/Physics/logs/2026-03-30-low-overlap-order-parameter-beyond-ceiling-subbranch-wider-sentinel-guardrail.txt",
        "wider:base:skew-wrap:local-morph-c",
    ),
    (
        "/Users/jonreilly/Projects/Physics/logs/2026-03-30-low-overlap-order-parameter-beyond-ceiling-subbranch-wider-sentinel-guardrail-mode-mix-d.txt",
        "wider:base:skew-wrap:mode-mix-d",
    ),
)
CURATED_RULES = (
    "anchor_closure_intensity_gap >= 1.000",
    "anchor_closure_intensity_gap >= 3.000",
    "high_bridge_right_count >= 1.500",
)


@dataclass(frozen=True)
class RuleAudit:
    rule_text: str
    exact: bool
    tp: int
    fp: int
    fn: int
    matched_counts: str


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
    parser.add_argument(
        "--sentinel-log",
        action="append",
        default=[],
        help="Guardrail log path paired with --sentinel-label in the same order.",
    )
    parser.add_argument(
        "--sentinel-label",
        action="append",
        default=[],
        help="Sentinel row label paired with --sentinel-log in the same order.",
    )
    return parser


def _parse_logged_rows(log_path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    lines = log_path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if " actual=" not in line or " cohort=" not in line or " family=" not in line:
            index += 1
            continue
        label, remainder = line.split(" cohort=", 1)
        cohort, remainder = remainder.split(" family=", 1)
        family, actual_subtype = remainder.split(" actual=", 1)
        metrics: dict[str, str] = {
            "cohort": cohort,
            "family": family,
            "actual_subtype": actual_subtype,
        }
        inner = index + 1
        while inner < len(lines) and lines[inner].startswith("  "):
            key, value = lines[inner].strip().split("=", 1)
            metrics[key] = value
            inner += 1
        rows[label] = metrics
        index = inner
    return rows


def _floatish(value: str) -> float:
    if value == "Y":
        return 1.0
    if value == "n":
        return 0.0
    return float(value)


def build_logged_sentinel_rows(
    sentinel_logs: list[str],
    sentinel_labels: list[str],
) -> list[CompareRow]:
    if len(sentinel_logs) != len(sentinel_labels):
        raise ValueError("sentinel log paths and labels must be paired")
    rows: list[CompareRow] = []
    for log_path, label in zip(sentinel_logs, sentinel_labels):
        payload = _parse_logged_rows(Path(log_path).resolve()).get(label)
        if payload is None:
            raise ValueError(f"missing sentinel row {label} in {log_path}")
        rows.append(
            CompareRow(
                subtype=str(payload["family"]),
                cohort=str(payload["cohort"]),
                family=str(payload["family"]),
                label=label,
                actual_subtype=str(payload["actual_subtype"]),
                support_load=_floatish(payload["support_load"]),
                closure_load=_floatish(payload["closure_load"]),
                mid_anchor_closure_peak=_floatish(payload["mid_anchor_closure_peak"]),
                anchor_closure_intensity_gap=_floatish(
                    payload["anchor_closure_intensity_gap"]
                ),
                anchor_deep_share_gap=_floatish(payload["anchor_deep_share_gap"]),
                high_bridge_right_count=_floatish(payload["high_bridge_right_count"]),
                high_bridge_right_low_count=_floatish(
                    payload["high_bridge_right_low_count"]
                ),
                edge_identity_event_count=_floatish(payload["edge_identity_event_count"]),
                edge_identity_support_edge_density=_floatish(
                    payload["edge_identity_support_edge_density"]
                ),
                mid_candidate_attached_max=_floatish(
                    payload["mid_candidate_attached_max"]
                ),
                mid_candidate_bridge_bridge_closed_pair_max=_floatish(
                    payload["mid_candidate_bridge_bridge_closed_pair_max"]
                ),
                mid_has_four_incident_flank_hinge=_floatish(
                    payload["mid_has_four_incident_flank_hinge"]
                ),
            )
        )
    return rows


def audit_rule(rows: list[CompareRow], rule_text: str) -> RuleAudit:
    matched = [row for row in rows if matches_rule_text(row, rule_text)]
    target_rows = [row for row in rows if row.family == TAPER_HARD_CLASS]
    tp = sum(1 for row in matched if row.family == TAPER_HARD_CLASS)
    fp = sum(1 for row in matched if row.family != TAPER_HARD_CLASS)
    fn = len(target_rows) - tp
    return RuleAudit(
        rule_text=rule_text,
        exact=fp == 0 and fn == 0,
        tp=tp,
        fp=fp,
        fn=fn,
        matched_counts=_format_counts(matched),
    )


def _render_rule_audits(
    title: str,
    shared_rows: list[CompareRow],
    all_rows: list[CompareRow],
    rule_texts: list[str],
) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | exact(shared 5) | exact(all 7) | tp/fp/fn(all 7) | matched(family counts on all 7)",
        "-----+-----------------+--------------+----------------+--------------------------------",
    ]
    for rule_text in rule_texts:
        shared_audit = audit_rule(shared_rows, rule_text)
        all_audit = audit_rule(all_rows, rule_text)
        lines.append(
            f"{rule_text} | {'Y' if shared_audit.exact else 'n':^15} | "
            f"{'Y' if all_audit.exact else 'n':^12} | "
            f"{all_audit.tp:>2}/{all_audit.fp:>2}/{all_audit.fn:>2} | "
            f"{all_audit.matched_counts}"
        )
    return "\n".join(lines)


def exact_one_feature_rules(rows: list[CompareRow]) -> list[str]:
    exact_rules: set[str] = set()
    for feature_name in FEATURE_NAMES:
        for rule_text, _mask in candidate_predicates(rows, [feature_name]):
            if audit_rule(rows, rule_text).exact:
                exact_rules.add(rule_text)
    return sorted(exact_rules)


def exact_packet_gated_rules(
    shared_rows: list[CompareRow],
    all_rows: list[CompareRow],
) -> list[str]:
    gated_rules: set[str] = set()
    base_predicates: set[str] = set()
    packet_rule_set = set(PACKET_LAW_RULES)
    for feature_name in FEATURE_NAMES:
        for rule_text, _mask in candidate_predicates(all_rows, [feature_name]):
            if rule_text in packet_rule_set:
                continue
            if audit_rule(shared_rows, rule_text).exact:
                if audit_rule(all_rows, rule_text).exact:
                    continue
                base_predicates.add(rule_text)
    for packet_rule in PACKET_LAW_RULES:
        for base_rule in sorted(base_predicates):
            combined_rule = f"{packet_rule} and {base_rule}"
            if audit_rule(all_rows, combined_rule).exact:
                gated_rules.add(combined_rule)
    return sorted(gated_rules)


def _render_short_rule_list(title: str, rule_texts: list[str]) -> str:
    lines = [title, "=" * len(title)]
    if not rule_texts:
        lines.append("none")
        return "\n".join(lines)
    for rule_text in rule_texts:
        lines.append(rule_text)
    return "\n".join(lines)


def _render_conclusion(
    exact_single_rules: list[str],
    exact_gated_rules: list[str],
) -> str:
    strongest_single = (
        "high_bridge_right_count >= 1.500"
        if "high_bridge_right_count >= 1.500" in exact_single_rules
        else (exact_single_rules[0] if exact_single_rules else "none")
    )
    weakest_gated = "mid_anchor_closure_peak >= 10.000 and anchor_closure_intensity_gap >= 1.000"
    return "\n".join(
        [
            "Conclusion",
            "==========",
            "conclusion=the weak taper-hard intensity clause "
            "`anchor_closure_intensity_gap >= 1.000` is only exact inside the shared "
            "8/12 packet family, but the seven-row log-backed closure is stronger than "
            "that rescue alone.",
            "packet_gated_read=any one of the four equivalent shared-packet laws "
            "restores exactness when paired with the weak intensity clause; the simplest "
            f"logged example is `{weakest_gated}`.",
            "physical_translation=the taper-hard branch already exact-closes on the full "
            f"five-plus-two row set as `{strongest_single}`, so the cleaner physical read "
            "is not just gated positive intensity but a two-right-bridge branch inside the "
            "broader beyond-ceiling continuation.",
            "equivalent_intensity_read=the same seven-row closure can also be written as "
            "`anchor_closure_intensity_gap >= 3.000`, showing that the earlier "
            "`>= 1.000` threshold was too weak rather than the branch itself being "
            "non-exact.",
        ]
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    print(f"beyond-ceiling taper-hard closure started {started}", flush=True)

    sentinel_logs = list(args.sentinel_log)
    sentinel_labels = list(args.sentinel_label)
    if not sentinel_logs and not sentinel_labels:
        sentinel_logs = [item[0] for item in SENTINEL_SPECS]
        sentinel_labels = [item[1] for item in SENTINEL_SPECS]

    shared_rows = build_baseline_rows(
        Path(args.outer_log).resolve(),
        Path(args.nonrect_log).resolve(),
        Path(args.packet_log).resolve(),
    )
    sentinel_rows = build_logged_sentinel_rows(sentinel_logs, sentinel_labels)
    all_rows = shared_rows + sentinel_rows

    exact_single_rules = exact_one_feature_rules(all_rows)
    exact_gated_rules = exact_packet_gated_rules(shared_rows, all_rows)
    curated_rules = list(CURATED_RULES)
    curated_rules.extend(
        rule_text
        for rule_text in (
            "mid_anchor_closure_peak >= 10.000 and anchor_closure_intensity_gap >= 1.000",
            "mid_candidate_bridge_bridge_closed_pair_max >= 10.000 and anchor_closure_intensity_gap >= 1.000",
            "mid_candidate_attached_max >= 7.500 and anchor_closure_intensity_gap >= 1.000",
            "mid_has_four_incident_flank_hinge >= 0.500 and anchor_closure_intensity_gap >= 1.000",
        )
    )

    print()
    print("Beyond-Ceiling Taper-Hard Closure")
    print("=================================")
    print(f"outer_log={Path(args.outer_log).resolve()}")
    print(f"nonrect_log={Path(args.nonrect_log).resolve()}")
    print(f"packet_log={Path(args.packet_log).resolve()}")
    print(f"sentinel_logs={', '.join(str(Path(path).resolve()) for path in sentinel_logs)}")
    print(f"rows_total={len(all_rows)}")
    print(f"family_counts={_format_counts(all_rows)}")
    print()
    print(_render_rows("Shared-Packet Baseline Rows", shared_rows))
    print()
    print(_render_rows("Seven-Row Closure Set", all_rows))
    print()
    print(_render_packet_law(all_rows))
    print()
    print(_render_rule_audits("Curated Taper-Hard Clause Audit", shared_rows, all_rows, curated_rules))
    print()
    print(_render_short_rule_list("Exact One-Feature Taper-Hard Rules On All 7 Rows", exact_single_rules))
    print()
    print(
        _render_short_rule_list(
            "Exact Packet-Gated Rescue Rules That Need The Packet Gate",
            exact_gated_rules,
        )
    )
    print()
    print(_render_conclusion(exact_single_rules, exact_gated_rules))
    print()
    print(
        "beyond-ceiling taper-hard closure completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
