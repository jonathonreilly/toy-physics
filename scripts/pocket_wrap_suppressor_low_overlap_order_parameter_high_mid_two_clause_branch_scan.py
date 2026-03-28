#!/usr/bin/env python3
"""Bounded two-clause scan seeded by high-mid event-load separation."""

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
SEED_THRESHOLD = 78.0
EXTRA_FEATURES = (
    "support_role_pocket_only_count",
    "edge_identity_support_edge_density",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--row-limit", type=int, default=16)
    return parser


def format_counts(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    return ", ".join(f"{subtype}:{counts[subtype]}" for subtype in sorted(counts))


def build_rows(frontier_log: Path) -> list[object]:
    residual_rows = build_combined_residual_rows(frontier_log)
    frontier_by_source = {
        row.source_name: row for row in reconstruct_low_overlap_rows(frontier_log)
    }

    row_cls = make_dataclass(
        "HighMidTwoClauseResidualRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_event_count", float),
            ("support_role_pocket_only_count", float),
            ("edge_identity_support_edge_density", float),
        ],
        frozen=True,
    )

    rows: list[object] = []
    for row in residual_rows:
        source_name = getattr(row, "source_name")
        own_metrics = support_edge_identity_own_metrics(set(frontier_by_source[source_name].nodes))
        rows.append(
            row_cls(
                source_name=source_name,
                subtype=getattr(row, "subtype"),
                edge_identity_event_count=float(own_metrics["edge_identity_event_count"]),
                support_role_pocket_only_count=float(
                    own_metrics["support_role_pocket_only_count"]
                ),
                edge_identity_support_edge_density=float(
                    own_metrics["edge_identity_support_edge_density"]
                ),
            )
        )
    return sorted(rows, key=lambda item: getattr(item, "source_name"))


def confusion(rows: list[object], predicate) -> tuple[int, int, int]:
    tp = fp = fn = 0
    for row in rows:
        actual = getattr(row, "subtype") == TARGET_SUBTYPE
        predicted = predicate(row)
        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif (not predicted) and actual:
            fn += 1
    return tp, fp, fn


def predicate_seed(row: object) -> bool:
    return float(getattr(row, "edge_identity_event_count")) <= SEED_THRESHOLD


def render_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"edge_events={float(getattr(row, 'edge_identity_event_count')):.3f} "
            f"support_role_pocket_only_count={float(getattr(row, 'support_role_pocket_only_count')):.3f} "
            f"edge_density={float(getattr(row, 'edge_identity_support_edge_density')):.3f}"
        )
    return "\n".join(lines)


def scan_one_extra_clause(rows: list[object], cluster_rows: list[object]) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    cluster_add4_total = sum(1 for row in cluster_rows if getattr(row, "subtype") == TARGET_SUBTYPE)

    for feature_name in EXTRA_FEATURES:
        thresholds = sorted({float(getattr(row, feature_name)) for row in rows})
        for threshold in thresholds:
            for operator in ("<=", ">="):
                if operator == "<=":
                    extra_predicate = lambda row, f=feature_name, t=threshold: float(getattr(row, f)) <= t
                else:
                    extra_predicate = lambda row, f=feature_name, t=threshold: float(getattr(row, f)) >= t

                def combined_predicate(row: object, extra=extra_predicate) -> bool:
                    return predicate_seed(row) and extra(row)

                knot_tp, knot_fp, knot_fn = confusion(cluster_rows, combined_predicate)
                if (knot_tp, knot_fp, knot_fn) != (cluster_add4_total, 0, 0):
                    continue

                tp, fp, fn = confusion(rows, combined_predicate)
                matched = [row for row in rows if combined_predicate(row)]
                precision = tp / (tp + fp) if (tp + fp) else 0.0
                recall = tp / (tp + fn) if (tp + fn) else 0.0
                candidates.append(
                    {
                        "clause": f"{feature_name} {operator} {threshold:.3f}",
                        "tp": tp,
                        "fp": fp,
                        "fn": fn,
                        "precision": precision,
                        "recall": recall,
                        "matched": len(matched),
                        "matched_counts": format_counts(matched),
                        "knot_tp": knot_tp,
                        "knot_fp": knot_fp,
                        "knot_fn": knot_fn,
                    }
                )

    candidates.sort(
        key=lambda item: (
            item["precision"],
            item["tp"],
            -item["fp"],
            item["recall"],
        ),
        reverse=True,
    )
    return candidates


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"low-overlap high-mid two-clause branch scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)
    cluster_rows = [row for row in rows if getattr(row, "source_name") in TARGET_CLUSTER]

    seed_tp, seed_fp, seed_fn = confusion(rows, predicate_seed)
    seed_matched = [row for row in rows if predicate_seed(row)]

    candidates = scan_one_extra_clause(rows, cluster_rows)

    print()
    print("Low-Overlap High-Mid Two-Clause Branch Scan")
    print("===========================================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("residual_filter=predict_subtype == unmatched under combined-law projection")
    print(f"rows={len(rows)} ({format_counts(rows)})")
    print(f"target_cluster={', '.join(TARGET_CLUSTER)}")
    print()
    print(render_rows("Target high-mid cluster rows", sorted(cluster_rows, key=lambda item: getattr(item, "source_name"))))
    print()
    print("Seed single-clause projection")
    print("============================")
    print(f"rule=edge_identity_event_count <= {SEED_THRESHOLD:.3f}")
    print(
        f"full_residual tp/fp/fn={seed_tp}/{seed_fp}/{seed_fn} "
        f"precision={seed_tp / (seed_tp + seed_fp):.3f} recall={seed_tp / (seed_tp + seed_fn):.3f} "
        f"matched={len(seed_matched)} ({format_counts(seed_matched)})"
    )
    print()

    print("Best bounded two-clause candidates (knot exactness preserved)")
    print("============================================================")
    print("rule | tp/fp/fn | precision | recall | matched(subtype counts)")
    print("-----+----------+-----------+--------+-------------------------")
    for candidate in candidates[: args.row_limit]:
        print(
            f"edge_identity_event_count <= {SEED_THRESHOLD:.3f} and {candidate['clause']}"
            f" | {candidate['tp']}/{candidate['fp']}/{candidate['fn']}"
            f" | {candidate['precision']:.3f}"
            f" | {candidate['recall']:.3f}"
            f" | {candidate['matched']} ({candidate['matched_counts']})"
        )

    print()
    print(
        "low-overlap high-mid two-clause branch scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
