#!/usr/bin/env python3
"""Summarize finished late guardrails against the current late-branch law."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time


LATE_BRANCH_GATE = "closure_load >= 73.000"
LATE_BRANCH_SUBBRANCHES = (
    "late-outer-rect: support_load >= 24.000",
    "late-taper-hard: anchor_closure_intensity_gap >= 3.000",
    "late-skew-wrap: anchor_deep_share_gap <= -0.334",
)
BASE_DIRECT_COMPARE_LOG = Path(
    "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-base-late-branch-direct-compare.txt"
)
NON_BASE_GUARDRAIL_LOGS = (
    (
        "large:ultra|mega",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-ultra-mega.txt"
        ),
    ),
    (
        "large:giga",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-giga.txt"
        ),
    ),
    (
        "large:tera",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-large-tera.txt"
        ),
    ),
    (
        "mirror:ultra|mega",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-ultra-mega.txt"
        ),
    ),
    (
        "mirror:giga|tera",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-giga-tera.txt"
        ),
    ),
    (
        "mirror:peta",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-peta.txt"
        ),
    ),
    (
        "mirror:exa",
        Path(
            "/Users/jonreilly/Projects/Physics/logs/2026-03-29-low-overlap-order-parameter-generated-beyond-ceiling-first-nonrect-probe-mirror-exa.txt"
        ),
    ),
)


@dataclass(frozen=True)
class GuardrailRow:
    label: str
    scanned_nonrect_combinations: int
    first_nonrect_row: str
    conclusion: str


def _parse_simple_key_values(log_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in log_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("="):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.startswith("delta_"):
            continue
        values[key.strip()] = value.strip()
    return values


def _parse_guardrail_row(label: str, log_path: Path) -> GuardrailRow:
    parsed = _parse_simple_key_values(log_path)
    return GuardrailRow(
        label=label,
        scanned_nonrect_combinations=int(parsed["scanned_nonrect_combinations"]),
        first_nonrect_row=parsed["first_nonrect_row"],
        conclusion=parsed["conclusion"],
    )


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"late branch guardrail summary started {started}", flush=True)
    total_start = time.time()

    base_parsed = _parse_simple_key_values(BASE_DIRECT_COMPARE_LOG)
    guardrails = [
        _parse_guardrail_row(label, log_path)
        for label, log_path in NON_BASE_GUARDRAIL_LOGS
    ]

    total_scanned = sum(row.scanned_nonrect_combinations for row in guardrails)
    hit_rows = [row for row in guardrails if row.first_nonrect_row != "none"]

    print()
    print("Late Branch Guardrail Summary")
    print("=============================")
    print(f"base_direct_compare_log={BASE_DIRECT_COMPARE_LOG}")
    print(f"late_branch_gate={LATE_BRANCH_GATE}")
    print("late_branch_subbranches=" + "; ".join(LATE_BRANCH_SUBBRANCHES))
    print(f"observed_base_late_branch={base_parsed['late_branch_rows']}")
    print(f"observed_base_sources={base_parsed['late_branch_sources']}")
    print(f"finished_non_base_guardrails={len(guardrails)}")
    print(f"finished_non_base_scanned_nonrect_combinations={total_scanned}")
    print(f"finished_non_base_first_hits={len(hit_rows)}")
    if hit_rows:
        print(
            "finished_non_base_first_hit_labels="
            + ",".join(f"{row.label}:{row.first_nonrect_row}" for row in hit_rows)
        )
    else:
        print("finished_non_base_first_hit_labels=none")
    print()
    print("Finished non-base guardrails")
    print("===========================")
    for row in guardrails:
        print(
            f"{row.label} scanned_nonrect_combinations={row.scanned_nonrect_combinations} "
            f"first_nonrect_row={row.first_nonrect_row}"
        )
        print(f"  conclusion={row.conclusion}")
    print()
    if hit_rows:
        print(
            "conclusion=the current late-branch law already has at least one non-base late guardrail candidate to test"
        )
    else:
        print(
            "conclusion=outside the observed base peta|exa branch, no finished non-base late guardrail "
            "through large tera and mirror exa has produced any non-rect beyond-ceiling non-collapse row, "
            "so the current late-branch law has no broader-family transfer evidence and no non-base counterexample yet"
        )
    print()
    print(
        "late branch guardrail summary completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
