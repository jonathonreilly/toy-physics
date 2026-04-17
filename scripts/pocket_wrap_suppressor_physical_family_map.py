#!/usr/bin/env python3
"""Translate the stable 5504 suppressor taxonomy into coarse physical family language."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from pocket_wrap_suppressor_frontier_compression import (  # noqa: E402
    FrontierRow,
    build_envelopes,
    candidate_predicates,
    parse_rows,
    render_envelopes,
)


@dataclass(frozen=True)
class PairwiseRuleRow:
    left_subtype: str
    right_subtype: str
    target_subtype: str
    exact: bool
    correct: int
    total: int
    term_count: int
    tp: int
    fp: int
    fn: int
    rule_text: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--rule-limit", type=int, default=2)
    parser.add_argument("--max-terms", type=int, default=3)
    return parser


def best_rule_for_target(
    rows: list[FrontierRow],
    target_subtype: str,
    *,
    allow_approximate: bool,
    max_terms: int,
) -> PairwiseRuleRow | None:
    if not rows:
        return None
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row.subtype == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    best_row: PairwiseRuleRow | None = None
    seen_predicted_masks: set[int] = set()
    predicates = candidate_predicates(rows)
    predicate_sets: list[tuple[tuple[str, int], ...]] = []
    for term_count in range(1, max_terms + 1):
        predicate_sets.extend(itertools.combinations(predicates, term_count))

    for predicate_tuple in predicate_sets:
        sorted_terms = tuple(sorted(predicate_tuple, key=lambda item: item[0]))
        predicted_mask = full_mask
        for _predicate_text, mask in sorted_terms:
            predicted_mask &= mask
            if predicted_mask == 0:
                break
        if predicted_mask == 0 or predicted_mask in seen_predicted_masks:
            continue
        seen_predicted_masks.add(predicted_mask)

        tp = (predicted_mask & target_mask).bit_count()
        fp = (predicted_mask & non_target_mask).bit_count()
        fn = (target_mask & (full_mask ^ predicted_mask)).bit_count()
        tn = (non_target_mask & (full_mask ^ predicted_mask)).bit_count()
        row = PairwiseRuleRow(
            left_subtype="",
            right_subtype="",
            target_subtype=target_subtype,
            exact=(fp == 0 and fn == 0),
            correct=tp + tn,
            total=len(rows),
            term_count=len(sorted_terms),
            tp=tp,
            fp=fp,
            fn=fn,
            rule_text=" and ".join(term[0] for term in sorted_terms),
        )
        if not allow_approximate and not row.exact:
            continue
        if best_row is None or (
            (not row.exact, -row.correct, row.term_count, row.fp + row.fn, row.rule_text)
            < (not best_row.exact, -best_row.correct, best_row.term_count, best_row.fp + best_row.fn, best_row.rule_text)
        ):
            best_row = row

    return best_row


def best_pairwise_rules(rows: list[FrontierRow], *, max_terms: int) -> list[PairwiseRuleRow]:
    subtypes = sorted({row.subtype for row in rows})
    results: list[PairwiseRuleRow] = []
    for left_index in range(len(subtypes)):
        for right_index in range(left_index + 1, len(subtypes)):
            left_subtype = subtypes[left_index]
            right_subtype = subtypes[right_index]
            pair_rows = [
                row for row in rows
                if row.subtype in {left_subtype, right_subtype}
            ]
            for target_subtype in (left_subtype, right_subtype):
                best = best_rule_for_target(
                    pair_rows,
                    target_subtype,
                    allow_approximate=True,
                    max_terms=max_terms,
                )
                if best is None:
                    continue
                results.append(
                    PairwiseRuleRow(
                        left_subtype=left_subtype,
                        right_subtype=right_subtype,
                        target_subtype=target_subtype,
                        exact=best.exact,
                        correct=best.correct,
                        total=best.total,
                        term_count=best.term_count,
                        tp=best.tp,
                        fp=best.fp,
                        fn=best.fn,
                        rule_text=best.rule_text,
                    )
                )
    return results


def render_family_summary(rows: list[FrontierRow]) -> str:
    loaded = [row for row in rows if row.subtype == "both-sensitive"]
    low_overlap = [row for row in rows if row.subtype != "both-sensitive"]
    lines = [
        "family | rows | median overlap | cross rate | rough~ | pocket~ | ctv~ | span~ | interpretation",
        "------+------|----------------|------------|--------+---------+------+------|---------------",
    ]

    def summary_line(name: str, subtype_rows: list[FrontierRow], interpretation: str) -> str:
        envelopes = build_envelopes(subtype_rows, variant_limit=subtype_rows[0].variant_limit)
        envelope = envelopes[0]
        return (
            f"{name} | {len(subtype_rows):>4} | {envelope.overlap_median:>14.2f} | {envelope.cross_rate:>10.2f} | "
            f"{envelope.rough_median:>6.3f} | {envelope.pocket_median:>7.3f} | {envelope.ctv_median:>4.2f} | "
            f"{envelope.span_median:>4.1f} | {interpretation}"
        )

    if loaded:
        lines.append(summary_line("loaded-overlap", loaded, "high-overlap loaded branch"))
    if low_overlap:
        low_rows = [
            FrontierRow(
                variant_limit=low_overlap[0].variant_limit,
                source_name="low-overlap-family",
                subtype="low-overlap",
                deep_overlap_count=row.deep_overlap_count,
                crosses_midline=row.crosses_midline,
                boundary_roughness=row.boundary_roughness,
                pocket_fraction=row.pocket_fraction,
                center_total_variation=row.center_total_variation,
                span_range=row.span_range,
            )
            for row in low_overlap
        ]
        lines.append(summary_line("boundary-low", low_rows, "shared low-overlap boundary regime"))
    return "\n".join(lines)


def render_pairwise_rules(rows: list[PairwiseRuleRow], limit: int) -> str:
    lines = [
        "pair | target | exact | correct | terms | tp/fp/fn | rule",
        "-----+--------+-------+---------+-------+----------+---------------------------------------------",
    ]
    grouped: dict[tuple[str, str], list[PairwiseRuleRow]] = {}
    for row in rows:
        grouped.setdefault((row.left_subtype, row.right_subtype), []).append(row)
    for pair in sorted(grouped):
        pair_rows = sorted(
            grouped[pair],
            key=lambda row: (
                row.target_subtype,
                not row.exact,
                -row.correct,
                row.term_count,
                row.rule_text,
            ),
        )
        for row in pair_rows[:limit]:
            lines.append(
                f"{row.left_subtype}->{row.right_subtype} | {row.target_subtype:<19.19} | "
                f"{('Y' if row.exact else 'n'):<5} | {row.correct:>3}/{row.total:<3} | {row.term_count:>5} | "
                f"{row.tp:>2}/{row.fp:<2}/{row.fn:<2}     | {row.rule_text}"
            )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"physical family map started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = parse_rows(log_path)
    latest_limit = rows[0].variant_limit
    envelope_rows = build_envelopes(rows, latest_limit)
    both_sensitive_rule = best_rule_for_target(
        rows,
        "both-sensitive",
        allow_approximate=False,
        max_terms=args.max_terms,
    )
    low_overlap_rows = [row for row in rows if row.subtype != "both-sensitive"]
    pairwise_rows = best_pairwise_rules(low_overlap_rows, max_terms=args.max_terms)

    print()
    print("Physical Family Summary")
    print("=======================")
    print(f"log={log_path}")
    print(f"variant_limit={latest_limit} rows={len(rows)}")
    print(render_family_summary(rows))
    print()
    print("Subtype Envelopes")
    print("=================")
    print(render_envelopes(envelope_rows))
    print()
    print("Loaded-Family Anchor")
    print("====================")
    if both_sensitive_rule is None:
        print("(no exact coarse loaded-family rule found)")
    else:
        print(
            f"both-sensitive exact rule: {both_sensitive_rule.rule_text} "
            f"(terms={both_sensitive_rule.term_count}, tp/fp/fn={both_sensitive_rule.tp}/{both_sensitive_rule.fp}/{both_sensitive_rule.fn})"
        )
    print()
    print("Low-Overlap Pairwise Boundary Rules")
    print("===================================")
    print(render_pairwise_rules(pairwise_rows, limit=args.rule_limit))
    print()
    print(
        "physical family map completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
