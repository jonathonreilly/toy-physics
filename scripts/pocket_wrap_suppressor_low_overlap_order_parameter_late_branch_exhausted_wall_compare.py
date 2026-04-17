#!/usr/bin/env python3
"""Compare the observed base late branch against the nearest exhausted non-base misses."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
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
)
from pocket_wrap_suppressor_low_overlap_order_parameter_base_late_branch_direct_compare import (  # noqa: E402
    FEATURE_NAMES,
    LATE_BRANCH_CLASS,
    build_rows as build_base_rows,
)


EXHAUSTED_WALL_CLASS = "exhausted-wall"
KEY_VALUE_RE = re.compile(r"([A-Za-z0-9_]+)=(-?\d+(?:\.\d+)?)")


@dataclass(frozen=True)
class CompareRow:
    source_name: str
    subtype: str
    actual_subtype: str
    predicted_subtype: str
    predicted_branch: str
    support_load: float
    closure_load: float
    mid_anchor_closure_peak: float
    anchor_closure_intensity_gap: float
    anchor_deep_share_gap: float
    high_bridge_right_count: float
    high_bridge_right_low_count: float
    edge_identity_event_count: float
    edge_identity_support_edge_density: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--late-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-nonrect-sweep-base-peta-exa.txt",
    )
    parser.add_argument(
        "--reference-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-anchor-band-beyond-ceiling-followon.txt",
    )
    parser.add_argument(
        "--exhausted-logs",
        nargs="+",
        default=[
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-large-exa-exhausted-slice-compare.txt",
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-mirror-exa-exhausted-slice-compare.txt",
        ],
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=3)
    parser.add_argument("--row-limit", type=int, default=8)
    return parser


def _format_counts(rows: list[CompareRow], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def _parse_exhausted_rows(log_path: Path) -> list[CompareRow]:
    lines = log_path.read_text(encoding="utf-8").splitlines()
    rows: list[CompareRow] = []
    seen_sources: set[str] = set()
    index = 0
    while index < len(lines):
        line = lines[index]
        if " scenario=" not in line or " actual=" not in line or " predicted=" not in line:
            index += 1
            continue
        source_name, remainder = line.split(" scenario=", 1)
        _scenario_name, remainder = remainder.split(" actual=", 1)
        actual_subtype, remainder = remainder.split(" predicted=", 1)
        predicted_subtype, remainder = remainder.split(" branch=", 1)
        predicted_branch = remainder.strip()

        metrics: dict[str, float] = {}
        inner = index + 1
        while inner < len(lines) and lines[inner].startswith("  "):
            for key, value in KEY_VALUE_RE.findall(lines[inner]):
                metrics[key] = float(value)
            inner += 1

        if source_name not in seen_sources:
            seen_sources.add(source_name)
            rows.append(
                CompareRow(
                    source_name=source_name,
                    subtype=EXHAUSTED_WALL_CLASS,
                    actual_subtype=actual_subtype,
                    predicted_subtype=predicted_subtype,
                    predicted_branch=predicted_branch,
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
                )
            )
        index = inner
    return rows


def build_rows(
    *,
    late_log: Path,
    reference_log: Path,
    exhausted_logs: list[Path],
) -> list[CompareRow]:
    rows: list[CompareRow] = []
    for row in build_base_rows(late_log, reference_log):
        if row.cohort != LATE_BRANCH_CLASS:
            continue
        rows.append(
            CompareRow(
                source_name=row.label,
                subtype=LATE_BRANCH_CLASS,
                actual_subtype=row.actual_subtype,
                predicted_subtype=row.predicted_subtype,
                predicted_branch=row.predicted_branch,
                support_load=row.support_load,
                closure_load=row.closure_load,
                mid_anchor_closure_peak=row.mid_anchor_closure_peak,
                anchor_closure_intensity_gap=row.anchor_closure_intensity_gap,
                anchor_deep_share_gap=row.anchor_deep_share_gap,
                high_bridge_right_count=row.high_bridge_right_count,
                high_bridge_right_low_count=row.high_bridge_right_low_count,
                edge_identity_event_count=row.edge_identity_event_count,
                edge_identity_support_edge_density=row.edge_identity_support_edge_density,
            )
        )
    for log_path in exhausted_logs:
        rows.extend(_parse_exhausted_rows(log_path))
    rows.sort(key=lambda row: (row.subtype, row.source_name))
    return rows


def _render_rows(title: str, rows: list[CompareRow]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{row.source_name} cohort={row.subtype} actual={row.actual_subtype} "
            f"predicted={row.predicted_subtype} branch={row.predicted_branch}"
        )
        for feature_name in FEATURE_NAMES:
            lines.append(f"  {feature_name}={float(getattr(row, feature_name)):.3f}")
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    total_start = time.time()
    print(f"late branch exhausted wall compare started {started}")

    rows = build_rows(
        late_log=Path(args.late_log),
        reference_log=Path(args.reference_log),
        exhausted_logs=[Path(value) for value in args.exhausted_logs],
    )
    late_rows = [row for row in rows if row.subtype == LATE_BRANCH_CLASS]
    exhausted_rows = [row for row in rows if row.subtype == EXHAUSTED_WALL_CLASS]
    late_mid_peaks = sorted({row.mid_anchor_closure_peak for row in late_rows})
    exhausted_mid_peaks = sorted({row.mid_anchor_closure_peak for row in exhausted_rows})
    late_closure_values = sorted({row.closure_load for row in late_rows})
    exhausted_closure_values = sorted({row.closure_load for row in exhausted_rows})

    rules = evaluate_rules(
        rows,
        target_subtype=LATE_BRANCH_CLASS,
        feature_names=list(FEATURE_NAMES),
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    print()
    print("Late Branch Exhausted Wall Compare")
    print("==================================")
    print(f"late_log={args.late_log}")
    print("exhausted_logs=" + ",".join(args.exhausted_logs))
    print(f"rows_total={len(rows)} ({_format_counts(rows)})")
    print(
        "late_branch_mid_anchor_closure_peaks="
        + ",".join(f"{value:.3f}" for value in late_mid_peaks)
    )
    print(
        "exhausted_wall_mid_anchor_closure_peaks="
        + ",".join(f"{value:.3f}" for value in exhausted_mid_peaks)
    )
    print(
        "late_branch_closure_loads="
        + ",".join(f"{value:.3f}" for value in late_closure_values)
    )
    print(
        "exhausted_wall_closure_loads="
        + ",".join(f"{value:.3f}" for value in exhausted_closure_values)
    )
    if rules:
        best = rules[0]
        print(
            f"best_rule={best.rule_text} "
            f"tp/fp/fn={best.tp}/{best.fp}/{best.fn} exact={'Y' if best.exact else 'n'}"
        )
    print()
    print(_render_rows("Late branch rows", late_rows))
    print()
    print(_render_rows("Exhausted wall rows", exhausted_rows))
    print()
    print("Best rules")
    print("==========")
    for rule in rules:
        print(
            f"{rule.rule_text} | exact={'Y' if rule.exact else 'n'} | "
            f"correct={rule.correct}/{rule.total} | tp/fp/fn={rule.tp}/{rule.fp}/{rule.fn}"
        )
    print()
    print(
        "late branch exhausted wall compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s"
    )


if __name__ == "__main__":
    main()
