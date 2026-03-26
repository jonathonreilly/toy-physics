#!/usr/bin/env python3
"""Probe engineered latent axes on a completed residual-bucket case table."""

from __future__ import annotations

import argparse
import itertools
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import time


ROW_RE = re.compile(
    r"^\s*(?P<source>\S+)\s+\|\s+"
    r"(?P<subtype>add1-sensitive|add4-sensitive)\s+\|\s+"
    r"(?P<addtag>[^|]+)\|\s+"
    r"(?P<lowcore>-?\d+\.\d{3})/(?P<lowshell>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<pocket>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<rough>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<mean>[+-]?\d+\.\d{2})\s+\|\s+"
    r"(?P<absmean>-?\d+\.\d{3})\s+\|\s+"
    r"(?P<ctv>-?\d+\.\d{2})\s+\|\s+"
    r"(?P<span>\d+)\s+\|\s+"
    r"(?P<pocketgap>[+-]?\d+\.\d{3})\s+\|\s+"
    r"(?P<lowgap>[+-]?\d+\.\d{3})\s*$"
)


@dataclass(frozen=True)
class ResidualRow:
    source: str
    subtype: str
    low_core: float
    low_shell: float
    pocket: float
    rough: float
    mean_center: float
    abs_mean_center: float
    ctv: float
    span: float
    pocket_gap: float
    low_gap: float


@dataclass(frozen=True)
class RuleRow:
    target_subtype: str
    exact: bool
    correct: int
    total: int
    term_count: int
    tp: int
    fp: int
    fn: int
    rule_text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual-log", required=True)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--rule-limit", type=int, default=6)
    return parser.parse_args()


def parse_residual_rows(path: Path) -> list[ResidualRow]:
    rows: list[ResidualRow] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        rows.append(
            ResidualRow(
                source=m.group("source"),
                subtype=m.group("subtype"),
                low_core=float(m.group("lowcore")),
                low_shell=float(m.group("lowshell")),
                pocket=float(m.group("pocket")),
                rough=float(m.group("rough")),
                mean_center=float(m.group("mean")),
                abs_mean_center=float(m.group("absmean")),
                ctv=float(m.group("ctv")),
                span=float(m.group("span")),
                pocket_gap=float(m.group("pocketgap")),
                low_gap=float(m.group("lowgap")),
            )
        )
    return rows


def feature_values(row: ResidualRow) -> dict[str, float]:
    eps = 1e-6
    low_sum = row.low_core + row.low_shell
    return {
        "low_core": row.low_core,
        "low_shell": row.low_shell,
        "low_gap": row.low_gap,
        "abs_low_gap": abs(row.low_gap),
        "low_sum": low_sum,
        "low_core_share": row.low_core / (low_sum + eps),
        "pocket": row.pocket,
        "rough": row.rough,
        "mean_center": row.mean_center,
        "abs_mean_center": row.abs_mean_center,
        "ctv": row.ctv,
        "span": row.span,
        "pocket_gap": row.pocket_gap,
        "abs_pocket_gap": abs(row.pocket_gap),
        "pocket_x_rough": row.pocket * row.rough,
        "rough_x_span": row.rough * row.span,
        "pocketgap_x_lowgap": row.pocket_gap * row.low_gap,
        "absmean_x_ctv": row.abs_mean_center * row.ctv,
    }


def candidate_predicates(rows: list[ResidualRow]) -> list[tuple[str, int]]:
    full_mask = (1 << len(rows)) - 1
    feature_names = sorted(feature_values(rows[0]).keys())
    predicates: dict[int, str] = {}

    for feature in feature_names:
        values = [feature_values(row)[feature] for row in rows]
        keyed = sorted(set(values))
        thresholds: list[float] = []
        if len(keyed) == 1:
            thresholds = keyed
        else:
            for left, right in zip(keyed, keyed[1:]):
                thresholds.append((left + right) / 2.0)

        for threshold in thresholds:
            for op in ("<=", ">="):
                mask = 0
                for idx, row in enumerate(rows):
                    value = feature_values(row)[feature]
                    if (op == "<=" and value <= threshold) or (op == ">=" and value >= threshold):
                        mask |= 1 << idx
                if mask in (0, full_mask):
                    continue
                text = f"{feature} {op} {threshold:.6f}"
                prev = predicates.get(mask)
                if prev is None or text < prev:
                    predicates[mask] = text

    return sorted(((text, mask) for mask, text in predicates.items()), key=lambda item: item[0])


def search_rules(
    rows: list[ResidualRow],
    predicates: list[tuple[str, int]],
    max_terms: int,
    rule_limit: int,
) -> list[RuleRow]:
    full_mask = (1 << len(rows)) - 1
    results: list[RuleRow] = []
    targets = sorted({row.subtype for row in rows})

    for target_subtype in targets:
        target_mask = 0
        for i, row in enumerate(rows):
            if row.subtype == target_subtype:
                target_mask |= 1 << i
        non_target_mask = full_mask ^ target_mask
        seen_masks: set[int] = set()
        best: list[RuleRow] = []

        for term_count in range(1, max_terms + 1):
            combos = ((item,) for item in predicates) if term_count == 1 else itertools.combinations(predicates, term_count)
            for combo in combos:
                sorted_combo = tuple(sorted(combo, key=lambda item: item[0]))
                pred_mask = full_mask
                for _text, mask in sorted_combo:
                    pred_mask &= mask
                    if pred_mask == 0:
                        break
                if pred_mask == 0 or pred_mask in seen_masks:
                    continue
                seen_masks.add(pred_mask)
                tp = (pred_mask & target_mask).bit_count()
                fp = (pred_mask & non_target_mask).bit_count()
                fn = (target_mask & (full_mask ^ pred_mask)).bit_count()
                tn = (non_target_mask & (full_mask ^ pred_mask)).bit_count()
                best.append(
                    RuleRow(
                        target_subtype=target_subtype,
                        exact=(fp == 0 and fn == 0),
                        correct=tp + tn,
                        total=len(rows),
                        term_count=term_count,
                        tp=tp,
                        fp=fp,
                        fn=fn,
                        rule_text=" and ".join(t[0] for t in sorted_combo),
                    )
                )

        best.sort(key=lambda row: (not row.exact, -row.correct, row.term_count, row.fp + row.fn, row.rule_text))
        results.extend(best[:rule_limit])

    return results


def render_rows(rows: list[ResidualRow]) -> str:
    header = "source | subtype | low_core | low_shell | pocket | rough | mean | abs_mean | ctv | span | pocket_gap | low_gap"
    bar = "-" * len(header)
    body = [
        (
            f"{row.source} | {row.subtype} | {row.low_core:.3f} | {row.low_shell:.3f} | {row.pocket:.3f} | "
            f"{row.rough:.3f} | {row.mean_center:+.2f} | {row.abs_mean_center:.3f} | {row.ctv:.2f} | {int(row.span)} | "
            f"{row.pocket_gap:+.3f} | {row.low_gap:+.3f}"
        )
        for row in rows
    ]
    return "\n".join([header, bar, *body])


def render_rules(rows: list[RuleRow]) -> str:
    header = "target | exact | correct | terms | tp/fp/fn | rule"
    bar = "-" * len(header)
    body = [
        (
            f"{row.target_subtype} | {'y' if row.exact else 'n'} | {row.correct:>2}/{row.total:<2} | "
            f"{row.term_count:>2} | {row.tp}/{row.fp}/{row.fn} | {row.rule_text}"
        )
        for row in rows
    ]
    return "\n".join([header, bar, *body])


def main() -> None:
    args = parse_args()
    residual_log = Path(args.residual_log).resolve()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"residual latent-axis probe started {started}", flush=True)
    total_start = time.time()

    rows = parse_residual_rows(residual_log)
    if not rows:
        raise SystemExit(f"no residual rows parsed from {residual_log}")
    predicates = candidate_predicates(rows)
    rule_rows = search_rules(rows, predicates, max_terms=args.max_terms, rule_limit=args.rule_limit)
    exact_count = sum(1 for row in rule_rows if row.exact)

    print()
    print("Residual Rows (parsed)")
    print("======================")
    print(f"log={residual_log}")
    print(f"rows={len(rows)} predicates={len(predicates)}")
    print(render_rows(rows))
    print()
    print("Latent-Axis Rules")
    print("=================")
    print(f"max_terms={args.max_terms} rule_limit={args.rule_limit} exact_rows={exact_count}")
    print(render_rules(rule_rows))
    print()
    print(
        "residual latent-axis probe completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
