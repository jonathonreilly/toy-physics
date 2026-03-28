#!/usr/bin/env python3
"""Scan one-clause carve-outs inside the best branch-A residual add4 rule."""

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
BRANCH_A_EVENT_THRESHOLD = 78.0
BRANCH_A_DENSITY_THRESHOLD = 1.0 / 6.0
SCAN_FEATURES = (
    "support_role_pocket_only_count",
    "support_load",
    "closure_load",
    "mid_anchor_closure_peak",
    "anchor_closure_intensity_gap",
    "anchor_deep_share_gap",
    "high_bridge_right_count",
    "high_bridge_right_low_count",
    "mid_candidate_closed_ratio_max",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--row-limit", type=int, default=20)
    return parser


def build_rows(frontier_log: Path) -> list[object]:
    residual_rows = build_combined_residual_rows(frontier_log)
    frontier_by_source = {
        row.source_name: row for row in reconstruct_low_overlap_rows(frontier_log)
    }

    row_cls = make_dataclass(
        "BranchALeakageRow",
        [
            ("source_name", str),
            ("subtype", str),
            ("edge_identity_event_count", float),
            ("edge_identity_support_edge_density", float),
            ("support_role_pocket_only_count", float),
            ("support_load", float),
            ("closure_load", float),
            ("mid_anchor_closure_peak", float),
            ("anchor_closure_intensity_gap", float),
            ("anchor_deep_share_gap", float),
            ("high_bridge_right_count", float),
            ("high_bridge_right_low_count", float),
            ("mid_candidate_closed_ratio_max", float),
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
                edge_identity_support_edge_density=float(
                    own_metrics["edge_identity_support_edge_density"]
                ),
                support_role_pocket_only_count=float(
                    own_metrics["support_role_pocket_only_count"]
                ),
                support_load=float(getattr(row, "support_load")),
                closure_load=float(getattr(row, "closure_load")),
                mid_anchor_closure_peak=float(getattr(row, "mid_anchor_closure_peak")),
                anchor_closure_intensity_gap=float(
                    getattr(row, "anchor_closure_intensity_gap")
                ),
                anchor_deep_share_gap=float(getattr(row, "anchor_deep_share_gap")),
                high_bridge_right_count=float(getattr(row, "high_bridge_right_count")),
                high_bridge_right_low_count=float(
                    getattr(row, "high_bridge_right_low_count")
                ),
                mid_candidate_closed_ratio_max=float(
                    getattr(row, "mid_candidate_closed_ratio_max")
                ),
            )
        )
    return sorted(rows, key=lambda item: getattr(item, "source_name"))


def format_counts(rows: list[object]) -> str:
    counts = Counter(getattr(row, "subtype") for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{name}:{counts[name]}" for name in sorted(counts))


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


def branch_a(row: object) -> bool:
    return (
        float(getattr(row, "edge_identity_event_count")) <= BRANCH_A_EVENT_THRESHOLD
        and float(getattr(row, "edge_identity_support_edge_density"))
        >= BRANCH_A_DENSITY_THRESHOLD
    )


def render_rows(title: str, rows: list[object]) -> str:
    lines = [title, "=" * len(title)]
    if not rows:
        lines.append("none")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"{getattr(row, 'source_name')} subtype={getattr(row, 'subtype')} "
            f"edge_events={float(getattr(row, 'edge_identity_event_count')):.3f} "
            f"edge_density={float(getattr(row, 'edge_identity_support_edge_density')):.3f} "
            f"support_role_pocket_only_count={float(getattr(row, 'support_role_pocket_only_count')):.3f} "
            f"support_load={float(getattr(row, 'support_load')):.3f} "
            f"closure_load={float(getattr(row, 'closure_load')):.3f} "
            f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
            f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
            f"deep_gap={float(getattr(row, 'anchor_deep_share_gap')):.3f} "
            f"high_bridge_right_count={float(getattr(row, 'high_bridge_right_count')):.3f} "
            f"high_bridge_right_low_count={float(getattr(row, 'high_bridge_right_low_count')):.3f} "
            f"mid_candidate_closed_ratio_max={float(getattr(row, 'mid_candidate_closed_ratio_max')):.3f}"
        )
    return "\n".join(lines)


def scan_carve_clauses(rows: list[object], base_predicate) -> list[dict[str, object]]:
    add4_total = sum(1 for row in rows if getattr(row, "subtype") == TARGET_SUBTYPE)
    candidates: list[dict[str, object]] = []

    for feature_name in SCAN_FEATURES:
        thresholds = sorted({float(getattr(row, feature_name)) for row in rows})
        for threshold in thresholds:
            for operator in ("<=", ">="):
                if operator == "<=":
                    extra = lambda row, f=feature_name, t=threshold: float(getattr(row, f)) <= t
                else:
                    extra = lambda row, f=feature_name, t=threshold: float(getattr(row, f)) >= t

                def predicate(row: object, e=extra) -> bool:
                    return base_predicate(row) and e(row)

                tp, fp, fn = confusion(rows, predicate)
                matched = [row for row in rows if predicate(row)]
                residual = [row for row in rows if not predicate(row)]
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
                        "residual": len(residual),
                        "residual_counts": format_counts(residual),
                        "preserves_recall": tp == add4_total and fn == 0,
                    }
                )

    candidates.sort(
        key=lambda item: (
            item["preserves_recall"],
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
    print(f"branch-a leakage carve scan started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    rows = build_rows(frontier_log)

    branch_a_rows = [row for row in rows if branch_a(row)]
    branch_a_add1_rows = [row for row in branch_a_rows if getattr(row, "subtype") != TARGET_SUBTYPE]
    base_tp, base_fp, base_fn = confusion(rows, branch_a)
    base_precision = base_tp / (base_tp + base_fp) if (base_tp + base_fp) else 0.0
    base_recall = base_tp / (base_tp + base_fn) if (base_tp + base_fn) else 0.0

    candidates = scan_carve_clauses(rows, branch_a)
    preserving = [item for item in candidates if item["preserves_recall"]]

    print()
    print("Branch-A Leakage Carve Scan")
    print("===========================")
    print(f"frontier_log={frontier_log}")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print("residual_filter=predict_subtype == unmatched under combined-law projection")
    print(f"rows={len(rows)} ({format_counts(rows)})")
    print(
        "branch_a=edge_identity_event_count <= 78.000 "
        "and edge_identity_support_edge_density >= 0.166667"
    )
    print()
    print("Branch-A baseline on full residual")
    print("===============================")
    print(
        f"tp/fp/fn={base_tp}/{base_fp}/{base_fn} precision={base_precision:.3f} "
        f"recall={base_recall:.3f} matched={len(branch_a_rows)} ({format_counts(branch_a_rows)})"
    )
    print()
    print(render_rows("Branch-A add1 leak rows", branch_a_add1_rows))
    print()

    print("Best one-clause carve candidates")
    print("===============================")
    print("rule | recall-preserved | tp/fp/fn | precision | recall | matched(subtype counts)")
    print("-----+------------------+----------+-----------+--------+-------------------------")
    for item in candidates[: args.row_limit]:
        print(
            "edge_identity_event_count <= 78.000 and "
            "edge_identity_support_edge_density >= 0.166667 and "
            f"{item['clause']}"
            f" | {'Y' if item['preserves_recall'] else 'n':^16}"
            f" | {item['tp']}/{item['fp']}/{item['fn']}"
            f" | {item['precision']:.3f}"
            f" | {item['recall']:.3f}"
            f" | {item['matched']} ({item['matched_counts']})"
        )
    print()

    if preserving:
        best = preserving[0]
        print("Best recall-preserving carve")
        print("===========================")
        print(
            "edge_identity_event_count <= 78.000 and "
            "edge_identity_support_edge_density >= 0.166667 and "
            f"{best['clause']}"
        )
        print(
            f"tp/fp/fn={best['tp']}/{best['fp']}/{best['fn']} "
            f"precision={best['precision']:.3f} recall={best['recall']:.3f}"
        )
    else:
        print("Best recall-preserving carve")
        print("===========================")
        print("none")

    print()
    print(
        "branch-a leakage carve scan completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
