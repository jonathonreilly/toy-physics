#!/usr/bin/env python3
"""Guard generated support-collapse rows before projecting the low-overlap law."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
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

from pocket_wrap_suppressor_low_overlap_order_parameter_exact_law_generated_ensemble_transfer_check import (  # noqa: E402
    build_rows as build_generated_rows,
)
from pocket_wrap_suppressor_low_overlap_order_parameter_full_bucket_exact_projection import (  # noqa: E402
    build_rows as build_historical_rows,
    predict_branch,
    predict_subtype,
)


GUARD_BRANCH = "guarded-support-collapse"
GUARD_SUBTYPE = "out-of-domain"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frontier-log",
        default="/Users/jonreilly/Projects/Physics/logs/2026-03-26-pocket-wrap-suppressor-nonpocket-subtype-rules-5504-max5600.txt",
    )
    parser.add_argument("--pack-name", default="base")
    parser.add_argument("--scenario-name", default="taper-wrap")
    parser.add_argument(
        "--ensembles",
        nargs="+",
        default=("default", "broader", "wider"),
    )
    return parser


def is_support_collapse(row: object) -> bool:
    return (
        float(getattr(row, "support_load")) == 0.0
        and float(getattr(row, "closure_load")) == 0.0
        and float(getattr(row, "edge_identity_event_count")) == 0.0
    )


def guarded_predict_subtype(row: object) -> str:
    if is_support_collapse(row):
        return GUARD_SUBTYPE
    return predict_subtype(row)


def guarded_predict_branch(row: object) -> str:
    if is_support_collapse(row):
        return GUARD_BRANCH
    return predict_branch(row)


def _format_counts(rows: list[object], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def render_generated_block(ensemble_name: str, rows: list[object]) -> tuple[str, dict[str, int]]:
    guarded_rows = [row for row in rows if is_support_collapse(row)]
    modeled_rows = [row for row in rows if not is_support_collapse(row)]
    modeled_misclassified = [
        row
        for row in modeled_rows
        if guarded_predict_subtype(row) != getattr(row, "subtype")
    ]
    modeled_ambiguous = [
        row for row in modeled_rows if guarded_predict_subtype(row) == "ambiguous"
    ]
    modeled_unmatched = [
        row for row in modeled_rows if guarded_predict_subtype(row) == "unmatched"
    ]
    style_counts = Counter(getattr(row, "style") for row in rows)
    style_text = ", ".join(
        f"{style}:{style_counts[style]}" for style in sorted(style_counts)
    )

    lines = [
        f"ensemble={ensemble_name}",
        "-" * (9 + len(ensemble_name)),
        f"rows={len(rows)} ({_format_counts(rows)})",
        f"styles={style_text if style_text else 'none'}",
        f"guarded={len(guarded_rows)} ({_format_counts(guarded_rows, attr='source_name')})",
        f"modeled_rows={len(modeled_rows)} ({_format_counts(modeled_rows)})",
        f"modeled_misclassified={len(modeled_misclassified)} ({_format_counts(modeled_misclassified)})",
        f"modeled_ambiguous={len(modeled_ambiguous)} ({_format_counts(modeled_ambiguous)})",
        f"modeled_unmatched={len(modeled_unmatched)} ({_format_counts(modeled_unmatched)})",
        "guarded_branches:",
    ]
    for branch in (
        GUARD_BRANCH,
        "high-closure-add4",
        "high-closure-pair-only",
        "outside-gate-pair-only",
        "outside-gate-add4",
        "outside-gate-add1-default",
    ):
        branch_rows = [row for row in rows if guarded_predict_branch(row) == branch]
        lines.append(f"  {branch}: {len(branch_rows)} ({_format_counts(branch_rows)})")

    if guarded_rows:
        lines.append("guarded_rows:")
        for row in guarded_rows[:12]:
            lines.append(
                f"  {getattr(row, 'style')}:{getattr(row, 'source_name')} "
                f"actual={getattr(row, 'subtype')} "
                f"guarded_subtype={guarded_predict_subtype(row)} "
                f"support_load={float(getattr(row, 'support_load')):.3f} "
                f"closure_load={float(getattr(row, 'closure_load')):.3f} "
                f"edge_identity_event_count={float(getattr(row, 'edge_identity_event_count')):.3f}"
            )
        if len(guarded_rows) > 12:
            lines.append(f"  ... {len(guarded_rows) - 12} more")
    else:
        lines.append("guarded_rows: none")

    if modeled_misclassified:
        lines.append("modeled_misclassified_rows:")
        for row in modeled_misclassified[:12]:
            lines.append(
                f"  {getattr(row, 'style')}:{getattr(row, 'source_name')} "
                f"actual={getattr(row, 'subtype')} predicted={guarded_predict_subtype(row)} "
                f"branch={guarded_predict_branch(row)}"
            )
        if len(modeled_misclassified) > 12:
            lines.append(f"  ... {len(modeled_misclassified) - 12} more")
    else:
        lines.append("modeled_misclassified_rows: none")

    return "\n".join(lines), {
        "rows": len(rows),
        "guarded": len(guarded_rows),
        "modeled_rows": len(modeled_rows),
        "modeled_misclassified": len(modeled_misclassified),
        "modeled_ambiguous": len(modeled_ambiguous),
        "modeled_unmatched": len(modeled_unmatched),
    }


def render_historical_block(rows: list[object]) -> tuple[str, dict[str, int]]:
    guarded_rows = [row for row in rows if is_support_collapse(row)]
    modeled_misclassified = [
        row
        for row in rows
        if not is_support_collapse(row)
        and guarded_predict_subtype(row) != getattr(row, "subtype")
    ]
    lines = [
        "historical_frozen_bucket",
        "=======================",
        f"rows={len(rows)} ({_format_counts(rows)})",
        f"guarded={len(guarded_rows)} ({_format_counts(guarded_rows, attr='source_name')})",
        f"modeled_misclassified={len(modeled_misclassified)} ({_format_counts(modeled_misclassified)})",
    ]
    if guarded_rows:
        lines.append("guarded_rows:")
        for row in guarded_rows[:12]:
            lines.append(
                f"  {getattr(row, 'source_name')} actual={getattr(row, 'subtype')} "
                f"support_load={float(getattr(row, 'support_load')):.3f} "
                f"closure_load={float(getattr(row, 'closure_load')):.3f} "
                f"edge_identity_event_count={float(getattr(row, 'edge_identity_event_count')):.3f}"
            )
        if len(guarded_rows) > 12:
            lines.append(f"  ... {len(guarded_rows) - 12} more")
    else:
        lines.append("guarded_rows: none")
    return "\n".join(lines), {
        "rows": len(rows),
        "guarded": len(guarded_rows),
        "modeled_misclassified": len(modeled_misclassified),
    }


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"generated support-collapse guard projection started {started}", flush=True)
    total_start = time.time()

    frontier_log = Path(args.frontier_log).resolve()
    ensemble_names = list(dict.fromkeys(args.ensembles))
    generated_blocks: list[str] = []
    generated_totals = defaultdict(int)
    first_modeled_failure_ensemble = None
    for ensemble_name in ensemble_names:
        rows = build_generated_rows(ensemble_name, args.pack_name, args.scenario_name)
        block, stats = render_generated_block(ensemble_name, rows)
        generated_blocks.append(block)
        for key, value in stats.items():
            generated_totals[key] += value
        if (
            first_modeled_failure_ensemble is None
            and stats["modeled_misclassified"] > 0
        ):
            first_modeled_failure_ensemble = ensemble_name

    historical_rows = build_historical_rows(frontier_log)
    historical_block, historical_stats = render_historical_block(historical_rows)

    print()
    print("Generated Support-Collapse Guard Projection")
    print("===========================================")
    print(f"target={args.pack_name}:{args.scenario_name}")
    print("ensembles=" + ",".join(ensemble_names))
    print(f"generated_rows_total={generated_totals['rows']}")
    print(f"generated_guarded_total={generated_totals['guarded']}")
    print(f"generated_modeled_rows_total={generated_totals['modeled_rows']}")
    print(f"generated_modeled_misclassified_total={generated_totals['modeled_misclassified']}")
    print(f"generated_modeled_ambiguous_total={generated_totals['modeled_ambiguous']}")
    print(f"generated_modeled_unmatched_total={generated_totals['modeled_unmatched']}")
    if first_modeled_failure_ensemble is None:
        print("first_modeled_failure_ensemble=none within tested ensembles")
    else:
        print(f"first_modeled_failure_ensemble={first_modeled_failure_ensemble}")
    print(f"historical_guarded_total={historical_stats['guarded']}")
    print(f"historical_modeled_misclassified_total={historical_stats['modeled_misclassified']}")
    print()
    print("\n\n".join(generated_blocks))
    print()
    print(historical_block)
    print()
    print("Conclusion")
    print("==========")
    if (
        generated_totals["guarded"] > 0
        and generated_totals["guarded"] == generated_totals["rows"]
        and generated_totals["modeled_misclassified"] == 0
        and generated_totals["modeled_ambiguous"] == 0
        and generated_totals["modeled_unmatched"] == 0
        and historical_stats["guarded"] == 0
        and historical_stats["modeled_misclassified"] == 0
    ):
        print(
            "The minimal zero-support guard cleanly isolates the canonical generated failures into an out-of-domain support-collapse bucket."
        )
        print(
            "No historical frozen-bucket row is guarded, and the historical exact-close remains unchanged under the guarded projection."
        )
    else:
        print(
            "The minimal zero-support guard does not cleanly isolate the generated failures or it disturbs the historical exact-close."
        )
    print()
    print(
        "generated support-collapse guard projection completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
