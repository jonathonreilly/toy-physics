#!/usr/bin/env python3
"""Compare the stubborn high-mid residual cluster with a slightly richer transfer basis."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import make_dataclass
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

from pocket_wrap_suppressor_low_overlap_boundary_axes import (  # noqa: E402
    reconstruct_low_overlap_rows,
)
from pocket_wrap_suppressor_low_overlap_center_spine_bucket00_support_topology import (  # noqa: E402
    evaluate_rules,
    matches_rule_text,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_combined_residual_add4_scan import (  # noqa: E402
    build_rows as build_combined_residual_rows,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
    support_edge_identity_own_metrics,
)


TARGET_SUBTYPE = "add4-sensitive"
TARGET_CLUSTER = (
    "base:taper-wrap:local-morph-а",
    "base:taper-wrap:local-morph-༸",
    "base:taper-wrap:local-morph-छ",
    "base:taper-wrap:local-morph-గ",
)
FEATURE_NAMES = [
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "mid_candidate_closed_ratio_max",
    "support_role_pocket_only_count",
    "edge_identity_closed_pair_count",
    "edge_identity_support_edge_density",
    "edge_identity_event_count",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--predicate-limit", type=int, default=18)
    parser.add_argument("--max-terms", type=int, default=2)
    parser.add_argument("--row-limit", type=int, default=12)
    return parser


def format_counts(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    return ", ".join(f"{subtype}:{counts[subtype]}" for subtype in sorted(counts))


def build_richer_rows(frontier_log: Path) -> tuple[list[object], list[object]]:
    residual_rows = build_combined_residual_rows(frontier_log)
    frontier_by_source = {
        row.source_name: row for row in reconstruct_low_overlap_rows(frontier_log)
    }

    row_cls = make_dataclass(
        "HighMidResidualClusterRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("closure_load", float),
            ("mid_anchor_closure_peak", float),
            ("anchor_closure_intensity_gap", float),
            ("mid_candidate_closed_ratio_max", float),
            ("support_role_pocket_only_count", float),
            ("edge_identity_closed_pair_count", float),
            ("edge_identity_support_edge_density", float),
            ("edge_identity_event_count", float),
        ],
        frozen=True,
    )

    richer_rows: list[object] = []
    for row in residual_rows:
        source_name = getattr(row, "source_name")
        own_metrics = support_edge_identity_own_metrics(set(frontier_by_source[source_name].nodes))
        richer_rows.append(
            row_cls(
                source_name=source_name,
                subtype=getattr(row, "subtype"),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(getattr(row, "anchor_closure_intensity_gap")),
                mid_candidate_closed_ratio_max=float(getattr(row, "mid_candidate_closed_ratio_max")),
                support_role_pocket_only_count=float(
                    own_metrics["support_role_pocket_only_count"]
                ),
                edge_identity_closed_pair_count=float(
                    own_metrics["edge_identity_closed_pair_count"]
                ),
                edge_identity_support_edge_density=float(
                    own_metrics["edge_identity_support_edge_density"]
                ),
                edge_identity_event_count=float(own_metrics["edge_identity_event_count"]),
            )
        )

    cluster_rows = [row for row in richer_rows if getattr(row, "source_name") in TARGET_CLUSTER]
    return richer_rows, sorted(cluster_rows, key=lambda item: getattr(item, "source_name"))


def render_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
            f"mid_closed_ratio_max={float(getattr(row, 'mid_candidate_closed_ratio_max')):.3f} "
            f"support_role_pocket_only_count={float(getattr(row, 'support_role_pocket_only_count')):.3f} "
            f"edge_closed_pairs={float(getattr(row, 'edge_identity_closed_pair_count')):.3f} "
            f"edge_density={float(getattr(row, 'edge_identity_support_edge_density')):.3f} "
            f"edge_events={float(getattr(row, 'edge_identity_event_count')):.3f}"
        )
    return "\n".join(lines)


def render_rule_table(title: str, rows: list[object], rules: list[object]) -> str:
    lines = [
        title,
        "=" * len(title),
        "rule | exact | corr | tp/fp/fn | matched(subtype counts)",
        "-----+-------+------+----------+-------------------------",
    ]
    for rule in rules:
        matched = [row for row in rows if matches_rule_text(row, rule.rule_text)]
        lines.append(
            f"{rule.rule_text} | {'Y' if rule.exact else 'n':^5} | {rule.correct:>2}/{rule.total:<2} | "
            f"{rule.tp:>2}/{rule.fp:>2}/{rule.fn:>2} | "
            f"{len(matched)} ({format_counts(matched)})"
        )
    return "\n".join(lines)


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap high-mid cluster compare started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    all_rows, cluster_rows = build_richer_rows(frontier_log)

    rules = evaluate_rules(
        cluster_rows,
        target_subtype=TARGET_SUBTYPE,
        feature_names=FEATURE_NAMES,
        predicate_limit=args.predicate_limit,
        max_terms=args.max_terms,
        row_limit=args.row_limit,
    )

    exact_rules = [rule for rule in rules if rule.exact]
    chosen_rule = exact_rules[0] if exact_rules else (rules[0] if rules else None)

    print()
    print("Low-Overlap High-Mid Cluster Compare")
    print("===================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("residual_filter=predict_subtype == unmatched under combined-law projection")
    print(f"full_residual_rows={len(all_rows)} ({format_counts(all_rows)})")
    print(f"target_cluster_rows={len(cluster_rows)} ({format_counts(cluster_rows)})")
    print(f"target_cluster={', '.join(TARGET_CLUSTER)}")
    print()
    print(render_rows("Target high-mid cluster rows", cluster_rows))
    print()
    print(render_rule_table("Candidate compact rules for add4-sensitive in target cluster", cluster_rows, rules))

    if chosen_rule is not None:
        matched_full = [row for row in all_rows if matches_rule_text(row, chosen_rule.rule_text)]
        print()
        print("Best cluster rule projected onto full residual")
        print("============================================")
        print(f"rule={chosen_rule.rule_text}")
        print(f"full_residual_match={len(matched_full)} ({format_counts(matched_full)})")

    print()
    print(
        "low-overlap high-mid cluster compare completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
