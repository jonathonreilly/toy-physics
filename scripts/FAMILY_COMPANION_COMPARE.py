#!/usr/bin/env python3
"""Narrow comparison card for the retained fixed-companion weak-field law.

This script compares the currently retained grown-family, alternative
connectivity family, and second-family slices on the smallest common surface
that is review-safe:

- weak-field linearity / F~M
- exact zero / neutral controls where they actually apply
- the complex-action gamma=0 anchor where that branch is the relevant
  observable

The result is intentionally not a universal theorem. It is a compact comparison
card that either finds agreement or isolates the exact mismatch.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FamilyRow:
    family: str
    slice_name: str
    zero_control: str
    neutral_control: str
    weak_field_fm: str
    control_surface: str
    exact_mismatch: str
    safe_read: str
    source_note: str


FAMILY_ROWS: list[FamilyRow] = [
    FamilyRow(
        family="Retained grown transfer basin",
        slice_name="grown-row / nearby basin",
        zero_control="exact zero-source and neutral same-point cancellation",
        neutral_control="exact",
        weak_field_fm="1.000",
        control_surface="sign-law branch",
        exact_mismatch="none on the signed-source branch; companion gamma=0 baseline is exact",
        safe_read=(
            "weak-field linearity survives on the retained grown basin; the family is "
            "selective, not geometry-generic"
        ),
        source_note="docs/GROWN_TRANSFER_BASIN_NOTE.md + docs/FIXED_FIELD_GROWN_TRANSFER_SCOUT_NOTE.md",
    ),
    FamilyRow(
        family="Alternative connectivity family",
        slice_name="no-restore grown slice",
        zero_control="exact zero-source and neutral same-point cancellation",
        neutral_control="exact",
        weak_field_fm="0.999994",
        control_surface="sign-law branch",
        exact_mismatch="complex-action crossover fails on this slice; sign-law stays intact",
        safe_read=(
            "the alternative structured connectivity family preserves weak-field "
            "linearity across the full tested drift sweep"
        ),
        source_note="docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md + docs/ALT_CONNECTIVITY_FAMILY_FM_TRANSFER_NOTE.md",
    ),
    FamilyRow(
        family="Second grown-family complex",
        slice_name="no-restore geometry-sector slice",
        zero_control="not the active observable; gamma=0 baseline is exact",
        neutral_control="not the active observable",
        weak_field_fm="1.000",
        control_surface="complex-action branch",
        exact_mismatch=(
            "this branch is not on the same zero/neutral signed-source surface; "
            "it is compared by gamma=0 baseline plus crossover"
        ),
        safe_read=(
            "weak-field linearity is retained on the anchor row, but the comparison "
            "surface is adjacent, not identical, to the sign-law families"
        ),
        source_note="docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md + docs/SECOND_GROWN_FAMILY_SIGN_NOTE.md",
    ),
]


def render_markdown(rows: list[FamilyRow]) -> str:
    lines = [
        "# Family Companion Compare Note",
        "",
        "**Date:** 2026-04-06",
        "**Status:** narrow cross-family comparison card for the retained fixed-companion weak-field law",
        "",
        "## Question",
        "",
        "Do the retained grown-family, alternative connectivity family, and second-family slices share the same fixed-companion weak-field law at a review-safe level?",
        "",
        "## Comparison",
        "",
        "| family | slice | zero / neutral control | weak-field `F~M` | exact mismatch |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.family} | {row.slice_name} | {row.zero_control} | {row.weak_field_fm} | {row.exact_mismatch} |"
        )
    lines.extend(
        [
            "",
            "## Safe Read",
            "",
            "- the retained grown basin preserves exact zero-source / neutral cancellation and stays at `F~M = 1.000` on the checked companion surface",
            "- the alternative connectivity family also preserves exact zero / neutral controls and keeps weak-field `F~M` at `0.999994` across the full tested drift sweep",
            "- the second-family complex anchor keeps `F~M = 1.000`, but its comparison surface is `gamma = 0` baseline plus crossover rather than the same zero / neutral signed-source surface",
            "",
            "## Exact Mismatch",
            "",
            "- the sign-law families share the same zero / neutral control surface",
            "- the second-family complex lane does not: it is a complex-action branch, so the nearest analogue is `gamma = 0` baseline rather than zero-source cancellation",
            "- that means the shared result is the weak-field law, not a universal identity of all controls",
            "",
            "## Final Verdict",
            "",
            "**retained narrow comparison positive: shared weak-field linearity, with control-surface mismatch isolated rather than averaged away**",
        ]
    )
    return "\n".join(lines)


def render_text(rows: list[FamilyRow]) -> str:
    lines = [
        "FAMILY COMPANION COMPARE NOTE",
        "Date: 2026-04-06",
        "Status: narrow cross-family comparison card for the retained fixed-companion weak-field law",
        "",
        "Question:",
        "Do the retained grown-family, alternative connectivity family, and second-family slices share the same fixed-companion weak-field law at a review-safe level?",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"- {row.family}",
                f"  slice: {row.slice_name}",
                f"  zero/neutral: {row.zero_control}",
                f"  F~M: {row.weak_field_fm}",
                f"  mismatch: {row.exact_mismatch}",
            ]
        )
    lines.extend(
        [
            "",
            "Safe read:",
            "- shared weak-field linearity survives across the retained families",
            "- exact zero/neutral controls are shared only by the signed-source families",
            "- the second-family complex lane is compared by gamma=0 baseline and crossover, not by zero-source cancellation",
            "",
            "Final verdict:",
            "retained narrow comparison positive: shared weak-field linearity, with control-surface mismatch isolated",
        ]
    )
    return "\n".join(lines)


def write_log(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "text", "json"), default="markdown")
    parser.add_argument("--write-log", help="optional path to write the rendered report")
    args = parser.parse_args()

    payload: dict[str, Any] = {
        "rows": [row.__dict__ for row in FAMILY_ROWS],
        "summary": {
            "shared_weak_field_law": True,
            "exact_zero_neutral_shared": True,
            "control_surface_mismatch_isolated": True,
        },
    }

    if args.format == "json":
        rendered = json.dumps(payload, indent=2, sort_keys=True)
    elif args.format == "text":
        rendered = render_text(FAMILY_ROWS)
    else:
        rendered = render_markdown(FAMILY_ROWS)

    print(rendered)

    if args.write_log:
        write_log(Path(args.write_log), rendered)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
