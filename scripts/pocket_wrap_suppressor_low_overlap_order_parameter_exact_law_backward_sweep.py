#!/usr/bin/env python3
"""Sweep the exact low-overlap law backward across older frontier checkpoints."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from glob import glob
from pathlib import Path
import sys
import time

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from pocket_wrap_suppressor_frontier_compression import parse_variant_limit  # noqa: E402
from pocket_wrap_suppressor_low_overlap_order_parameter_full_bucket_exact_projection import (  # noqa: E402
    build_rows,
    predict_branch,
    predict_subtype,
)
from pocket_wrap_suppressor_low_overlap_support_family_transfer_common import (  # noqa: E402
    RC0_ML0_C2_BUCKET,
)


DEFAULT_GLOB = (
    "/Users/jonreilly/Projects/Physics/logs/"
    "*pocket-wrap-suppressor-nonpocket-subtype-rules-*.txt"
)


@dataclass(frozen=True)
class SweepResult:
    variant_limit: int
    log_path: Path
    status: str
    rows: int
    misclassified: int
    ambiguous: int
    unmatched: int
    message: str = ""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", nargs="+")
    parser.add_argument("--glob", default=DEFAULT_GLOB)
    parser.add_argument("--min-limit", type=int, default=0)
    parser.add_argument("--max-limit", type=int, default=1231)
    return parser


def format_counts(rows: list[object], attr: str = "subtype") -> str:
    counts = Counter(getattr(row, attr) for row in rows)
    if not counts:
        return "none"
    return ", ".join(f"{key}:{counts[key]}" for key in sorted(counts))


def candidate_score(path: Path) -> tuple[int, int, int, int, str]:
    name = path.name
    return (
        int("manual" not in name),
        int("rerun" not in name and "timebox" not in name),
        int("max" not in name),
        -len(name),
        name,
    )


def discovered_logs(glob_pattern: str, min_limit: int, max_limit: int) -> list[tuple[int, list[Path]]]:
    by_limit: dict[int, list[Path]] = {}
    for matched in sorted(glob(glob_pattern)):
        path = Path(matched).resolve()
        if not path.is_file():
            continue
        try:
            variant_limit = parse_variant_limit(path)
        except ValueError:
            continue
        if variant_limit < min_limit or variant_limit > max_limit:
            continue
        by_limit.setdefault(variant_limit, []).append(path)
    ordered: list[tuple[int, list[Path]]] = []
    for limit in sorted(by_limit, reverse=True):
        candidates = sorted(by_limit[limit], key=candidate_score, reverse=True)
        ordered.append((limit, candidates))
    return ordered


def resolve_logs(args: argparse.Namespace) -> list[tuple[int, list[Path]]]:
    if args.logs:
        return [
            (parse_variant_limit(Path(item).resolve()), [Path(item).resolve()])
            for item in args.logs
        ]
    return discovered_logs(args.glob, args.min_limit, args.max_limit)


def render_success_block(log_path: Path, rows: list[object]) -> str:
    variant_limit = parse_variant_limit(log_path)
    misclassified = [row for row in rows if predict_subtype(row) != getattr(row, "subtype")]
    ambiguous = [row for row in rows if predict_subtype(row) == "ambiguous"]
    unmatched = [row for row in rows if predict_subtype(row) == "unmatched"]
    lines = [
        f"variant_limit={variant_limit}",
        "-" * (14 + len(str(variant_limit))),
        f"log={log_path}",
        f"rows={len(rows)} ({format_counts(rows)})",
        f"misclassified={len(misclassified)} ({format_counts(misclassified)})",
        f"ambiguous={len(ambiguous)} ({format_counts(ambiguous)})",
        f"unmatched={len(unmatched)} ({format_counts(unmatched)})",
        "predicted_branches:",
    ]
    for branch in (
        "high-closure-add4",
        "high-closure-pair-only",
        "outside-gate-pair-only",
        "outside-gate-add4",
        "outside-gate-add1-default",
    ):
        branch_rows = [row for row in rows if predict_branch(row) == branch]
        lines.append(f"  {branch}: {len(branch_rows)} ({format_counts(branch_rows)})")
    if misclassified:
        lines.append("misclassified_rows:")
        for row in misclassified:
            lines.append(
                f"  {getattr(row, 'source_name')} actual={getattr(row, 'subtype')} "
                f"predicted={predict_subtype(row)} branch={predict_branch(row)} "
                f"mid_peak={float(getattr(row, 'mid_anchor_closure_peak')):.3f} "
                f"intensity_gap={float(getattr(row, 'anchor_closure_intensity_gap')):.3f} "
                f"closure_load={float(getattr(row, 'closure_load')):.3f}"
            )
    else:
        lines.append("misclassified_rows: none")
    return "\n".join(lines)


def evaluate_log(log_path: Path) -> tuple[SweepResult, str]:
    variant_limit = parse_variant_limit(log_path)
    try:
        rows = build_rows(log_path)
    except Exception as exc:
        return (
            SweepResult(
                variant_limit=variant_limit,
                log_path=log_path,
                status="skipped-error",
                rows=0,
                misclassified=0,
                ambiguous=0,
                unmatched=0,
                message=f"{type(exc).__name__}: {exc}",
            ),
            "\n".join(
                [
                    f"variant_limit={variant_limit}",
                    "-" * (14 + len(str(variant_limit))),
                    f"log={log_path}",
                    f"status=skipped-error ({type(exc).__name__}: {exc})",
                ]
            ),
        )
    if not rows:
        return (
            SweepResult(
                variant_limit=variant_limit,
                log_path=log_path,
                status="skipped-empty",
                rows=0,
                misclassified=0,
                ambiguous=0,
                unmatched=0,
                message="no rc0|ml0|c2 rows",
            ),
            "\n".join(
                [
                    f"variant_limit={variant_limit}",
                    "-" * (14 + len(str(variant_limit))),
                    f"log={log_path}",
                    "status=skipped-empty (no rc0|ml0|c2 rows)",
                ]
            ),
        )

    misclassified = [row for row in rows if predict_subtype(row) != getattr(row, "subtype")]
    ambiguous = [row for row in rows if predict_subtype(row) == "ambiguous"]
    unmatched = [row for row in rows if predict_subtype(row) == "unmatched"]
    return (
        SweepResult(
            variant_limit=variant_limit,
            log_path=log_path,
            status="tested",
            rows=len(rows),
            misclassified=len(misclassified),
            ambiguous=len(ambiguous),
            unmatched=len(unmatched),
        ),
        render_success_block(log_path, rows),
    )


def evaluate_limit(variant_limit: int, candidates: list[Path]) -> tuple[SweepResult, str]:
    fallback_errors: list[str] = []
    for path in candidates:
        result, block = evaluate_log(path)
        if result.status == "skipped-error":
            fallback_errors.append(f"{path.name} ({result.message})")
            continue
        if fallback_errors:
            block += (
                "\n"
                + "fallback_skipped_errors="
                + "; ".join(fallback_errors)
            )
        return result, block

    message = "; ".join(fallback_errors) if fallback_errors else "no candidates"
    return (
        SweepResult(
            variant_limit=variant_limit,
            log_path=candidates[0] if candidates else Path(f"variant-limit-{variant_limit}"),
            status="skipped-error",
            rows=0,
            misclassified=0,
            ambiguous=0,
            unmatched=0,
            message=message,
        ),
        "\n".join(
            [
                f"variant_limit={variant_limit}",
                "-" * (14 + len(str(variant_limit))),
                f"log={candidates[0] if candidates else 'none'}",
                f"status=skipped-error ({message})",
            ]
        ),
    )


def main() -> None:
    args = build_parser().parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"exact low-overlap law backward sweep started {started}", flush=True)
    total_start = time.time()

    limit_candidates = resolve_logs(args)
    results_and_blocks = [
        evaluate_limit(variant_limit, candidates)
        for variant_limit, candidates in limit_candidates
    ]
    results = [result for result, _block in results_and_blocks]
    blocks = [block for _result, block in results_and_blocks]

    tested = [result for result in results if result.status == "tested"]
    skipped = [result for result in results if result.status != "tested"]
    first_failure = next(
        (result.variant_limit for result in tested if result.misclassified > 0),
        None,
    )
    lowest_exact = None
    if tested:
        exact_limits = [result.variant_limit for result in tested if result.misclassified == 0]
        if exact_limits:
            lowest_exact = min(exact_limits)

    print()
    print("Exact Low-Overlap Law Backward Sweep")
    print("====================================")
    print(f"bucket={RC0_ML0_C2_BUCKET}")
    print(f"glob={args.glob}")
    print(f"min_limit={args.min_limit}")
    print(f"max_limit={args.max_limit}")
    print(
        "discovered_logs="
        + str(sum(len(candidates) for _variant_limit, candidates in limit_candidates))
    )
    print(f"discovered_limits={len(limit_candidates)}")
    print(f"tested_logs={len(tested)}")
    print(f"skipped_logs={len(skipped)}")
    if tested:
        print("tested_variant_limits=" + ",".join(str(result.variant_limit) for result in tested))
    else:
        print("tested_variant_limits=none")
    if lowest_exact is None:
        print("lowest_exact_limit=none")
    else:
        print(f"lowest_exact_limit={lowest_exact}")
    if first_failure is None:
        print("first_failure_limit=none within tested slice")
    else:
        print(f"first_failure_limit={first_failure}")
    if skipped:
        print(
            "skipped_variant_limits="
            + ",".join(
                f"{result.variant_limit}:{result.status}" for result in skipped
            )
        )
    else:
        print("skipped_variant_limits=none")
    print()
    print("\n\n".join(blocks))
    print()
    print(
        "exact low-overlap law backward sweep completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
