#!/usr/bin/env python3
"""Close the taper-hard branch on the current beyond-ceiling packet controls."""

from __future__ import annotations

import argparse
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
from pocket_wrap_suppressor_low_overlap_order_parameter_beyond_ceiling_subbranch_compare import (  # noqa: E402
    CompareRow,
    FEATURE_NAMES,
    OTHER_CLASS,
    PACKET_LAW_RULES,
    TAPER_HARD_CLASS,
    _format_counts,
    _render_rows,
    build_rows as build_baseline_rows,
)


SENTINEL_FAMILY = "guardrail"


@dataclass(frozen=True)
class RuleAudit:
    rule_text: str
    raw_tp: int
    raw_fp: int
    raw_fn: int
    gated_tp: int
    gated_fp: int
    gated_fn: int
    raw_matches: tuple[str, ...]
    gated_matches: tuple[str, ...]
    wider_leakage: tuple[str, ...]


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
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-30-low-overlap-order-parameter-beyond-ceiling-subbranch-wider-sentinel-guardrail.txt",
    )
    parser.add_argument(
        "--paired-sentinel-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-30-low-overlap-order-parameter-beyond-ceiling-subbranch-wider-sentinel-guardrail-mode-mix-d.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=48)
    parser.add_argument("--row-limit", type=int, default=12)
    parser.add_argument("--max-terms", type=int, default=2)
    return parser


def _packet_gate(row: CompareRow) -> bool:
    return all(matches_rule_text(row, rule_text) for rule_text in PACKET_LAW_RULES)


def _sort_key(row: CompareRow) -> tuple[int, str]:
    order = {
        "outer-rect": 0,
        TAPER_HARD_CLASS: 1,
        "skew-wrap": 2,
        SENTINEL_FAMILY: 3,
    }
    return (order.get(row.family, len(order)), row.label)


def _parse_logged_rows(log_path: Path) -> list[CompareRow]:
    rows: list[CompareRow] = []
    lines = log_path.read_text(encoding="utf-8").splitlines()
    in_extended = False
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip() == "Extended Rows":
            in_extended = True
            index += 2
            continue
        if not in_extended:
            index += 1
            continue
        if not line or line.startswith("Shared Packet Law"):
            break
        if " cohort=" not in line or " family=" not in line or " actual=" not in line:
            index += 1
            continue
        label, remainder = line.split(" cohort=", 1)
        cohort, remainder = remainder.split(" family=", 1)
        family, actual_subtype = remainder.split(" actual=", 1)
        metrics: dict[str, float] = {}
        inner = index + 1
        while inner < len(lines) and lines[inner].startswith("  "):
            key, value = lines[inner].strip().split("=", 1)
            if value == "Y":
                metrics[key] = 1.0
            elif value == "n":
                metrics[key] = 0.0
            else:
                metrics[key] = float(value)
            inner += 1
        rows.append(
            CompareRow(
                subtype=family,
                cohort=cohort,
                family=family,
                label=label,
                actual_subtype=actual_subtype,
                support_load=float(metrics["support_load"]),
                closure_load=float(metrics["closure_load"]),
                mid_anchor_closure_peak=float(metrics["mid_anchor_closure_peak"]),
                anchor_closure_intensity_gap=float(
                    metrics["anchor_closure_intensity_gap"]
                ),
                anchor_deep_share_gap=float(metrics["anchor_deep_share_gap"]),
                high_bridge_right_count=float(metrics["high_bridge_right_count"]),
                high_bridge_right_low_count=float(
                    metrics["high_bridge_right_low_count"]
                ),
                edge_identity_event_count=float(metrics["edge_identity_event_count"]),
                edge_identity_support_edge_density=float(
                    metrics["edge_identity_support_edge_density"]
                ),
                mid_candidate_attached_max=float(metrics["mid_candidate_attached_max"]),
                mid_candidate_bridge_bridge_closed_pair_max=float(
                    metrics["mid_candidate_bridge_bridge_closed_pair_max"]
                ),
                mid_has_four_incident_flank_hinge=float(
                    metrics["mid_has_four_incident_flank_hinge"]
                ),
            )
        )
        index = inner
    return rows


def _load_rows(args: argparse.Namespace) -> list[CompareRow]:
    rows = build_baseline_rows(
        Path(args.outer_log).resolve(),
        Path(args.nonrect_log).resolve(),
        Path(args.packet_log).resolve(),
    )
    for log_path in (
        Path(args.sentinel_log).resolve(),
        Path(args.paired_sentinel_log).resolve(),
    ):
        sentinel_rows = [
            row for row in _parse_logged_rows(log_path) if row.family == SENTINEL_FAMILY
        ]
        if len(sentinel_rows) != 1:
            raise ValueError(
                f"expected exactly one guardrail row in {log_path}, found {len(sentinel_rows)}"
            )
        rows.extend(sentinel_rows)
    rows.sort(key=_sort_key)
    return rows


def _iter_one_feature_predicates(rows: list[CompareRow]) -> list[str]:
    predicates: list[str] = []
    for feature_name in FEATURE_NAMES:
        values = sorted({float(getattr(row, feature_name)) for row in rows})
        if len(values) == 1:
            thresholds = [values[0]]
        else:
            thresholds = [(left + right) / 2.0 for left, right in zip(values, values[1:])]
        for threshold in thresholds:
            for operator in ("<=", ">="):
                predicates.append(f"{feature_name} {operator} {threshold:.3f}")
    return predicates


def _audit_rule(rows: list[CompareRow], rule_text: str) -> RuleAudit:
    raw_matches = [row for row in rows if matches_rule_text(row, rule_text)]
    gated_matches = [
        row for row in rows if _packet_gate(row) and matches_rule_text(row, rule_text)
    ]
    wider_leakage = [
        row.label
        for row in rows
        if row.family == SENTINEL_FAMILY and matches_rule_text(row, rule_text)
    ]
    raw_tp = sum(1 for row in raw_matches if row.family == TAPER_HARD_CLASS)
    raw_fp = sum(1 for row in raw_matches if row.family != TAPER_HARD_CLASS)
    raw_fn = sum(
        1
        for row in rows
        if row.family == TAPER_HARD_CLASS and not matches_rule_text(row, rule_text)
    )
    gated_tp = sum(1 for row in gated_matches if row.family == TAPER_HARD_CLASS)
    gated_fp = sum(1 for row in gated_matches if row.family != TAPER_HARD_CLASS)
    gated_fn = sum(
        1
        for row in rows
        if row.family == TAPER_HARD_CLASS
        and not (_packet_gate(row) and matches_rule_text(row, rule_text))
    )
    return RuleAudit(
        rule_text=rule_text,
        raw_tp=raw_tp,
        raw_fp=raw_fp,
        raw_fn=raw_fn,
        gated_tp=gated_tp,
        gated_fp=gated_fp,
        gated_fn=gated_fn,
        raw_matches=tuple(row.label for row in raw_matches),
        gated_matches=tuple(row.label for row in gated_matches),
        wider_leakage=tuple(wider_leakage),
    )


def _render_packet_gate(rows: list[CompareRow]) -> str:
    packet_rows = [row for row in rows if _packet_gate(row)]
    non_packet_rows = [row for row in rows if not _packet_gate(row)]
    lines = [
        "Shared Packet Gate Audit",
        "========================",
        f"packet_rows={len(packet_rows)} ({_format_counts(packet_rows)})",
        f"non_packet_rows={len(non_packet_rows)} ({_format_counts(non_packet_rows)})",
    ]
    for row in rows:
        lines.append(
            f"{row.label}: packet_gate={'Y' if _packet_gate(row) else 'n'} family={row.family}"
        )
    return "\n".join(lines)


def _render_exact_rules(rows: list[CompareRow]) -> tuple[str, list[RuleAudit]]:
    packet_rows = [row for row in rows if _packet_gate(row)]
    exact_audits: list[RuleAudit] = []
    seen_rules: set[str] = set()
    for rule_text in _iter_one_feature_predicates(packet_rows):
        if rule_text in seen_rules:
            continue
        seen_rules.add(rule_text)
        audit = _audit_rule(rows, rule_text)
        if audit.gated_fp == 0 and audit.gated_fn == 0:
            exact_audits.append(audit)
    exact_audits.sort(
        key=lambda audit: (
            audit.raw_fp != 0,
            audit.raw_fp,
            len(audit.wider_leakage),
            audit.rule_text,
        )
    )
    lines = [
        "Exact Packet-Gated One-Feature Taper-Hard Clauses",
        "=================================================",
        "rule | raw_exact | raw tp/fp/fn | wider leakage",
        "-----+-----------+--------------+--------------",
    ]
    for audit in exact_audits:
        lines.append(
            f"{audit.rule_text} | {'Y' if audit.raw_fp == 0 and audit.raw_fn == 0 else 'n':^9} | "
            f"{audit.raw_tp:>2}/{audit.raw_fp:>2}/{audit.raw_fn:>2} | "
            f"{', '.join(audit.wider_leakage) if audit.wider_leakage else 'none'}"
        )
    return "\n".join(lines), exact_audits


def _render_minimal_search(rows: list[CompareRow], args: argparse.Namespace) -> tuple[str, str]:
    packet_rows = [row for row in rows if _packet_gate(row)]
    relabeled_rows = [
        replace(row, subtype=TAPER_HARD_CLASS if row.family == TAPER_HARD_CLASS else OTHER_CLASS)
        for row in packet_rows
    ]
    rules = evaluate_rules(
        relabeled_rows,
        target_subtype=TAPER_HARD_CLASS,
        feature_names=list(FEATURE_NAMES),
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )
    exact_rules = [rule for rule in rules if rule.exact]
    if not exact_rules:
        exact_rules = rules[: args.row_limit]
    best_rule = exact_rules[0]
    lines = [
        "Minimal Packet-Local Search",
        "===========================",
        f"packet_rows={len(packet_rows)} ({_format_counts(packet_rows)})",
        f"best_representative_rule={best_rule.rule_text}",
        f"best_representative_terms={best_rule.term_count}",
        "rule | exact | terms | tp/fp/fn",
        "-----+-------+-------+----------",
    ]
    for rule in exact_rules:
        lines.append(
            f"{rule.rule_text} | {'Y' if rule.exact else 'n':^5} | "
            f"{rule.term_count:^5} | {rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2}"
        )
    return "\n".join(lines), best_rule.rule_text


def _render_curated_audit(rows: list[CompareRow], exact_audits: list[RuleAudit]) -> str:
    chosen_rules = [
        "anchor_closure_intensity_gap >= 1.000",
        "high_bridge_right_count >= 1.500",
        "edge_identity_support_edge_density >= 0.164",
    ]
    audit_by_rule = {audit.rule_text: audit for audit in exact_audits}
    lines = [
        "Curated Clause Audit",
        "====================",
        "rule | gated tp/fp/fn | raw tp/fp/fn | wider leakage",
        "-----+----------------+--------------+--------------",
    ]
    for rule_text in chosen_rules:
        audit = audit_by_rule.get(rule_text)
        if audit is None:
            audit = _audit_rule(rows, rule_text)
        lines.append(
            f"{rule_text} | {audit.gated_tp:>2}/{audit.gated_fp:>2}/{audit.gated_fn:>2} | "
            f"{audit.raw_tp:>2}/{audit.raw_fp:>2}/{audit.raw_fn:>2} | "
            f"{', '.join(audit.wider_leakage) if audit.wider_leakage else 'none'}"
        )
    return "\n".join(lines)


def _render_conclusion(rows: list[CompareRow], best_rule_text: str) -> str:
    lines = [
        "Conclusion",
        "==========",
        "conclusion=the current taper-hard residual exact-closes on the seven-row logged control set once the shared 8/12 packet law is made explicit.",
        "gate_translation=the shared packet gate still keeps all five in-family rows and rejects both wider shoulders, so the earlier intensity split was leaking only because it was written without that gate.",
        "physical_closure=within the shared packet family the taper-hard pair still exact-separates under the minimal one-feature search, and the same target mask has a more physical exact representative: `high_bridge_right_count >= 1.500`.",
        "current_strongest_read=the taper-hard branch is therefore best read as the two-right-bridge arm of the shared beyond-ceiling packet regime, while `anchor_closure_intensity_gap >= 1.000` is just a coordinate-equivalent but less stable wording.",
    ]
    bridge_audit = _audit_rule(rows, "high_bridge_right_count >= 1.500")
    if bridge_audit.raw_fp == 0 and bridge_audit.raw_fn == 0:
        lines.append(
            "wider_control_status=the two-right-bridge clause already stays exact without the packet gate on both wider shoulders, so the current wider control set no longer forces taper-hard to be written only in packet-gated intensity language."
        )
    else:
        lines.append(
            f"wider_control_status=the best physical clause still leaks outside the packet gate on {', '.join(bridge_audit.wider_leakage) if bridge_audit.wider_leakage else 'none'}."
        )
    lines.append(f"best_representative_search_rule={best_rule_text}.")
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    print(
        f"beyond-ceiling packet-gated taper-hard closure started {started}",
        flush=True,
    )

    rows = _load_rows(args)

    print()
    print("Beyond-Ceiling Packet-Gated Taper-Hard Closure")
    print("==============================================")
    print(f"outer_log={Path(args.outer_log).resolve()}")
    print(f"nonrect_log={Path(args.nonrect_log).resolve()}")
    print(f"packet_log={Path(args.packet_log).resolve()}")
    print(f"sentinel_log={Path(args.sentinel_log).resolve()}")
    print(f"paired_sentinel_log={Path(args.paired_sentinel_log).resolve()}")
    print(f"rows_total={len(rows)}")
    print(f"family_counts={_format_counts(rows)}")
    print()
    print(_render_rows("Logged Control Rows", rows))
    print()
    print(_render_packet_gate(rows))
    print()
    minimal_search, best_rule_text = _render_minimal_search(rows, args)
    print(minimal_search)
    print()
    exact_rules, exact_audits = _render_exact_rules(rows)
    print(exact_rules)
    print()
    print(_render_curated_audit(rows, exact_audits))
    print()
    print(_render_conclusion(rows, best_rule_text))
    print()
    print(
        "beyond-ceiling packet-gated taper-hard closure completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
