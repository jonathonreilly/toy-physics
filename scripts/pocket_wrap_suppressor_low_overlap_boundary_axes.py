#!/usr/bin/env python3
"""Probe richer boundary variables for the low-overlap suppressor families on a frozen log."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import itertools
from pathlib import Path
import statistics
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_frontier_compression import (  # noqa: E402
    FrontierRow,
    parse_rows,
    parse_variant_limit,
)
from toy_event_physics import (  # noqa: E402
    PocketWrapSuppressorSubtypeRow,
    _threshold_core_shell_group_totals,
    _threshold_core_shell_summary_from_totals,
    column_profile_geometry_metrics,
    local_shape_feature_bundle,
    procedural_geometry_variants,
    scenario_by_name,
)


@dataclass(frozen=True)
class PairRuleRow:
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
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--rule-limit", type=int, default=2)
    return parser
def decode_source_name(source_name: str) -> str:
    if "\\u" not in source_name and "\\x" not in source_name:
        return source_name
    return source_name.encode("utf-8").decode("unicode_escape")


def reconstruct_low_overlap_rows(log_path: Path) -> list[PocketWrapSuppressorSubtypeRow]:
    frozen_rows = [row for row in parse_rows(log_path) if row.subtype != "both-sensitive"]
    if not frozen_rows:
        return []

    wanted = {decode_source_name(row.source_name): row for row in frozen_rows}
    variant_limit = parse_variant_limit(log_path)
    base_nodes, wrap_y = scenario_by_name("base", "taper-wrap")
    rows: list[PocketWrapSuppressorSubtypeRow] = []

    for variant_name, perturbed_nodes, _node_delta in procedural_geometry_variants(
        "base",
        "taper-wrap",
        base_nodes,
        wrap_y,
        variant_limit=variant_limit,
        style="local-morph",
    ):
        source_name = f"base:taper-wrap:{variant_name}"
        frozen = wanted.get(source_name)
        if frozen is None:
            continue

        boundary_fraction, pocket_fraction, boundary_roughness, deep_pocket_fraction, *_rest = (
            local_shape_feature_bundle(perturbed_nodes, wrap_y=wrap_y)
        )
        mean_center, center_range, center_total_variation, crosses_midline, span_range = (
            column_profile_geometry_metrics(perturbed_nodes)
        )
        totals = _threshold_core_shell_group_totals(perturbed_nodes, wrap_y=wrap_y)
        shell_summary = _threshold_core_shell_summary_from_totals(
            ensemble_name=source_name,
            graph_count=1,
            total_nodes=int(totals["total_nodes"]),
            group_counts=totals["group_counts"],  # type: ignore[arg-type]
            deep_counts=totals["deep_counts"],  # type: ignore[arg-type]
            pocket_counts=totals["pocket_counts"],  # type: ignore[arg-type]
            low_degree_counts=totals["low_degree_counts"],  # type: ignore[arg-type]
            boundary_sums=totals["boundary_sums"],  # type: ignore[arg-type]
            neighbor_degree_sums=totals["neighbor_degree_sums"],  # type: ignore[arg-type]
        )
        rows.append(
            PocketWrapSuppressorSubtypeRow(
                variant_limit=variant_limit,
                source_name=source_name,
                subtype=frozen.subtype,
                deep_overlap_count=frozen.deep_overlap_count,
                add_1_0_outcome="-",
                add_4_0_outcome="-",
                boundary_fraction=boundary_fraction,
                pocket_fraction=pocket_fraction,
                boundary_roughness=boundary_roughness,
                deep_pocket_fraction=deep_pocket_fraction,
                mean_center=mean_center,
                center_range=center_range,
                center_total_variation=center_total_variation,
                crosses_midline=crosses_midline,
                span_range=span_range,
                shell_deep_fraction=shell_summary.shell_deep_fraction,
                core_deep_fraction=shell_summary.core_deep_fraction,
                shell_pocket_fraction=shell_summary.shell_pocket_fraction,
                core_pocket_fraction=shell_summary.core_pocket_fraction,
                shell_low_degree_fraction=shell_summary.shell_low_degree_fraction,
                core_low_degree_fraction=shell_summary.core_low_degree_fraction,
                shell_boundary_deficit_mean=shell_summary.shell_boundary_deficit_mean,
                core_boundary_deficit_mean=shell_summary.core_boundary_deficit_mean,
                nodes=frozenset(perturbed_nodes),
            )
        )

    rows.sort(key=lambda row: row.source_name)
    return rows


def candidate_predicates(rows: list[PocketWrapSuppressorSubtypeRow]) -> list[tuple[str, int]]:
    if not rows:
        return []

    feature_defs = (
        ("boundary_fraction", lambda row: row.boundary_fraction),
        ("pocket_fraction", lambda row: row.pocket_fraction),
        ("boundary_roughness", lambda row: row.boundary_roughness),
        ("deep_pocket_fraction", lambda row: row.deep_pocket_fraction),
        ("mean_center", lambda row: row.mean_center),
        ("abs_mean_center", lambda row: abs(row.mean_center)),
        ("center_range", lambda row: row.center_range),
        ("center_total_variation", lambda row: row.center_total_variation),
        ("span_range", lambda row: float(row.span_range)),
        ("deep_overlap_count", lambda row: float(row.deep_overlap_count)),
        ("shell_deep_fraction", lambda row: row.shell_deep_fraction),
        ("core_deep_fraction", lambda row: row.core_deep_fraction),
        ("deep_gap", lambda row: row.shell_deep_fraction - row.core_deep_fraction),
        ("shell_pocket_fraction", lambda row: row.shell_pocket_fraction),
        ("core_pocket_fraction", lambda row: row.core_pocket_fraction),
        ("pocket_gap", lambda row: row.shell_pocket_fraction - row.core_pocket_fraction),
        ("shell_low_degree_fraction", lambda row: row.shell_low_degree_fraction),
        ("core_low_degree_fraction", lambda row: row.core_low_degree_fraction),
        ("low_degree_gap", lambda row: row.shell_low_degree_fraction - row.core_low_degree_fraction),
        ("shell_boundary_deficit_mean", lambda row: row.shell_boundary_deficit_mean),
        ("core_boundary_deficit_mean", lambda row: row.core_boundary_deficit_mean),
        ("boundary_gap", lambda row: row.shell_boundary_deficit_mean - row.core_boundary_deficit_mean),
    )
    preferred_order = {
        "deep_overlap_count": 0,
        "core_low_degree_fraction": 1,
        "low_degree_gap": 2,
        "boundary_gap": 3,
        "core_boundary_deficit_mean": 4,
        "shell_boundary_deficit_mean": 5,
        "mean_center": 6,
        "abs_mean_center": 7,
        "center_total_variation": 8,
        "span_range": 9,
        "boundary_roughness": 10,
        "pocket_fraction": 11,
        "pocket_gap": 12,
        "deep_gap": 13,
    }

    predicate_masks: dict[int, tuple[tuple[int, str, float], str]] = {}
    full_mask = (1 << len(rows)) - 1
    for feature_name, getter in feature_defs:
        value_to_labels: dict[float, set[str]] = {}
        for row in rows:
            value = float(getter(row))
            value_to_labels.setdefault(value, set()).add(row.subtype)
        values = sorted(value_to_labels)
        thresholds: list[float] = []
        if len(values) == 1:
            thresholds.append(values[0])
        else:
            for left, right in zip(values, values[1:]):
                if value_to_labels[left] != value_to_labels[right]:
                    thresholds.append((left + right) / 2.0)
        for threshold in thresholds:
            for operator in ("<=", ">="):
                mask = 0
                for index, row in enumerate(rows):
                    value = float(getter(row))
                    if (operator == "<=" and value <= threshold) or (
                        operator == ">=" and value >= threshold
                    ):
                        mask |= 1 << index
                if mask in (0, full_mask):
                    continue
                text = f"{feature_name} {operator} {threshold:.3f}"
                sort_key = (preferred_order.get(feature_name, 99), feature_name, threshold)
                chosen = predicate_masks.get(mask)
                if chosen is None or (sort_key, text) < (chosen[0], chosen[1]):
                    predicate_masks[mask] = (sort_key, text)

    for value, label in ((True, "crosses_midline = Y"), (False, "crosses_midline = n")):
        mask = 0
        for index, row in enumerate(rows):
            if row.crosses_midline == value:
                mask |= 1 << index
        if mask in (0, full_mask):
            continue
        sort_key = (20, "crosses_midline", 1.0 if value else 0.0)
        chosen = predicate_masks.get(mask)
        if chosen is None or (sort_key, label) < (chosen[0], chosen[1]):
            predicate_masks[mask] = (sort_key, label)

    predicates = [(text, mask) for mask, (_sort_key, text) in predicate_masks.items()]
    predicates.sort(key=lambda item: item[0])
    return predicates


def best_rule_for_target(
    rows: list[PocketWrapSuppressorSubtypeRow],
    target_subtype: str,
    *,
    max_terms: int,
) -> PairRuleRow | None:
    if not rows:
        return None

    predicates = candidate_predicates(rows)
    full_mask = (1 << len(rows)) - 1
    target_mask = 0
    for index, row in enumerate(rows):
        if row.subtype == target_subtype:
            target_mask |= 1 << index
    non_target_mask = full_mask ^ target_mask

    best: PairRuleRow | None = None
    seen_masks: set[int] = set()
    for term_count in range(1, max_terms + 1):
        for predicate_tuple in itertools.combinations(predicates, term_count):
            sorted_terms = tuple(sorted(predicate_tuple, key=lambda item: item[0]))
            predicted_mask = full_mask
            for _text, mask in sorted_terms:
                predicted_mask &= mask
                if predicted_mask == 0:
                    break
            if predicted_mask == 0 or predicted_mask in seen_masks:
                continue
            seen_masks.add(predicted_mask)
            tp = (predicted_mask & target_mask).bit_count()
            fp = (predicted_mask & non_target_mask).bit_count()
            fn = (target_mask & (full_mask ^ predicted_mask)).bit_count()
            tn = (non_target_mask & (full_mask ^ predicted_mask)).bit_count()
            candidate = PairRuleRow(
                left_subtype="",
                right_subtype="",
                target_subtype=target_subtype,
                exact=(fp == 0 and fn == 0),
                correct=tp + tn,
                total=len(rows),
                term_count=term_count,
                tp=tp,
                fp=fp,
                fn=fn,
                rule_text=" and ".join(term[0] for term in sorted_terms),
            )
            if best is None or (
                (not candidate.exact, -candidate.correct, candidate.term_count, candidate.fp + candidate.fn, candidate.rule_text)
                < (not best.exact, -best.correct, best.term_count, best.fp + best.fn, best.rule_text)
            ):
                best = candidate
    return best


def pairwise_rules(rows: list[PocketWrapSuppressorSubtypeRow], max_terms: int) -> list[PairRuleRow]:
    subtypes = sorted({row.subtype for row in rows})
    results: list[PairRuleRow] = []
    for left_index in range(len(subtypes)):
        for right_index in range(left_index + 1, len(subtypes)):
            left = subtypes[left_index]
            right = subtypes[right_index]
            pair_rows = [row for row in rows if row.subtype in {left, right}]
            for target in (left, right):
                best = best_rule_for_target(pair_rows, target, max_terms=max_terms)
                if best is None:
                    continue
                results.append(
                    PairRuleRow(
                        left_subtype=left,
                        right_subtype=right,
                        target_subtype=target,
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


def median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def render_envelopes(rows: list[PocketWrapSuppressorSubtypeRow]) -> str:
    lines = [
        "subtype | cases | overlap~ | cross rate | bfrac~ | mean_center~ | low_gap~ | boundary_gap~ | pocket_gap~",
        "--------+-------+----------+------------+--------+--------------+----------+---------------+-----------",
    ]
    for subtype in sorted({row.subtype for row in rows}):
        bucket = [row for row in rows if row.subtype == subtype]
        lines.append(
            f"{subtype:<19.19} | {len(bucket):>5} | "
            f"{median([float(row.deep_overlap_count) for row in bucket]):>8.2f} | "
            f"{sum(1 for row in bucket if row.crosses_midline) / len(bucket):>10.2f} | "
            f"{median([row.boundary_fraction for row in bucket]):>6.3f} | "
            f"{median([row.mean_center for row in bucket]):>12.3f} | "
            f"{median([row.shell_low_degree_fraction - row.core_low_degree_fraction for row in bucket]):>8.3f} | "
            f"{median([row.shell_boundary_deficit_mean - row.core_boundary_deficit_mean for row in bucket]):>13.3f} | "
            f"{median([row.shell_pocket_fraction - row.core_pocket_fraction for row in bucket]):>9.3f}"
        )
    return "\n".join(lines)


def render_pair_rules(rows: list[PairRuleRow], limit: int) -> str:
    lines = [
        "pair | target | exact | correct | terms | tp/fp/fn | rule",
        "-----+--------+-------+---------+-------+----------+---------------------------------------------",
    ]
    grouped: dict[tuple[str, str], list[PairRuleRow]] = {}
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
    print(f"low-overlap boundary axes started {started}", flush=True)
    total_start = time.time()

    log_path = Path(args.log).resolve()
    rows = reconstruct_low_overlap_rows(log_path)
    rule_rows = pairwise_rules(rows, max_terms=args.max_terms)

    print()
    print("Low-Overlap Family Envelopes")
    print("============================")
    print(f"log={log_path}")
    print(f"rows={len(rows)}")
    print(render_envelopes(rows))
    print()
    print("Low-Overlap Pairwise Rules")
    print("==========================")
    print(render_pair_rules(rule_rows, args.rule_limit))
    print()
    elapsed = time.time() - total_start
    print(
        f"low-overlap boundary axes completed {datetime.now().isoformat(timespec='seconds')} total_elapsed={elapsed:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
