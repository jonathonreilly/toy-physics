#!/usr/bin/env python3
"""Narrow predictor scan for complex-action companions on structured families.

This is a review-safe comparison card, not a theorem. It compares the retained
complex-positive slices against diagnosed complex boundaries and asks whether a
simple low-dimensional predictor exists.

The retained conclusion in this repo is that the smallest stable discriminator
is an anchor-local crossover: exact gamma=0 baseline plus TOWARD -> AWAY on the
same retained row. Coarser metrics such as basin width, seed selectivity, and
sign-law portability are useful context but do not separate the complex-positive
families from the diagnosed boundaries by themselves.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FamilyRow:
    family: str
    retained_complex: str
    exact_gamma0: str
    anchor_crossover: str
    basin_shape: str
    discriminator_note: str
    source_notes: str


ROWS: list[FamilyRow] = [
    FamilyRow(
        family="Original grown basin",
        retained_complex="yes",
        exact_gamma0="yes",
        anchor_crossover="yes on nearby rows",
        basin_shape="narrow and selective",
        discriminator_note="anchor-local crossover survives on a nearby row neighborhood",
        source_notes="docs/GROWN_TRANSFER_BASIN_NOTE.md; docs/CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md",
    ),
    FamilyRow(
        family="Second-family complex",
        retained_complex="yes",
        exact_gamma0="yes",
        anchor_crossover="yes on the anchor row",
        basin_shape="tiny basin",
        discriminator_note="exact gamma=0 + Born proxy + crossover survive narrowly",
        source_notes="docs/SECOND_GROWN_FAMILY_COMPLEX_NOTE.md; docs/SECOND_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md",
    ),
    FamilyRow(
        family="Alt connectivity family",
        retained_complex="no",
        exact_gamma0="yes",
        anchor_crossover="no",
        basin_shape="bounded sign-law basin only",
        discriminator_note="sign-law survives, complex branch does not",
        source_notes="docs/ALT_CONNECTIVITY_FAMILY_BASIN_NOTE.md; docs/ALT_CONNECTIVITY_FAMILY_COMPLEX_FAILURE_NOTE.md",
    ),
    FamilyRow(
        family="Third grown family",
        retained_complex="no",
        exact_gamma0="yes",
        anchor_crossover="not stable across drift window",
        basin_shape="bounded drift basin",
        discriminator_note="crossover is seed-selective and drift-sensitive; not retained",
        source_notes="docs/THIRD_GROWN_FAMILY_COMPLEX_BOUNDARY_NOTE.md; docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md",
    ),
    FamilyRow(
        family="Fourth family quadrant",
        retained_complex="no",
        exact_gamma0="yes",
        anchor_crossover="no",
        basin_shape="narrow seed-selective sign basin",
        discriminator_note="complex response stays boundary-like despite clean controls",
        source_notes="docs/FOURTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md; docs/FOURTH_FAMILY_QUADRANT_NOTE.md",
    ),
    FamilyRow(
        family="Fifth family radial",
        retained_complex="yes",
        exact_gamma0="yes",
        anchor_crossover="yes on the anchor row",
        basin_shape="narrow anchor-row basin",
        discriminator_note="anchor-local crossover survives, but only at the center row",
        source_notes="docs/FIFTH_FAMILY_COMPLEX_NOTE.md; docs/FIFTH_FAMILY_COMPLEX_BOUNDARY_NOTE.md",
    ),
]


def render_markdown(rows: list[FamilyRow]) -> str:
    lines = [
        "# Complex Selectivity Predictor Note",
        "",
        "**Date:** 2026-04-06",
        "**Status:** retained narrow predictor card for complex-action survival on structured families",
        "",
        "## Question",
        "",
        "What is the smallest review-safe discriminator for when a complex-action companion survives on a structured family?",
        "",
        "## Comparison",
        "",
        "| family | retained complex | exact gamma=0 | anchor crossover | basin shape | discriminator note |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.family} | {row.retained_complex} | {row.exact_gamma0} | {row.anchor_crossover} | {row.basin_shape} | {row.discriminator_note} |"
        )
    lines.extend(
        [
            "",
            "## Safe Read",
            "",
            "- exact gamma=0 baseline is necessary, but not sufficient",
            "- signed-source portability and weak-field linearity do not predict complex survival by themselves",
            "- support width and seed selectivity are useful context, but they do not separate the positive families from the diagnosed boundaries cleanly",
            "- the smallest stable discriminator we found is the anchor-local crossover: exact gamma=0 baseline plus TOWARD -> AWAY on the retained anchor row",
            "",
            "## Exact Mismatch",
            "",
            "- the original grown basin and the fifth-family radial slice retain the crossover only in a narrow local neighborhood",
            "- the second-family complex slice retains it on the anchor row but loses it in the tighter boundary window",
            "- the alt, third, and fourth families all fail the same crossover test in structurally different ways",
            "",
            "## Final Verdict",
            "",
            "**retained narrow predictor: complex-action survival requires an anchor-local crossover; coarser basin geometry does not predict it**",
        ]
    )
    return "\n".join(lines)


def render_text(rows: list[FamilyRow]) -> str:
    lines = [
        "COMPLEX SELECTIVITY PREDICTOR NOTE",
        "Date: 2026-04-06",
        "Status: retained narrow predictor card for complex-action survival on structured families",
        "",
        "Question:",
        "What is the smallest review-safe discriminator for when a complex-action companion survives on a structured family?",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"- {row.family}",
                f"  retained complex: {row.retained_complex}",
                f"  exact gamma=0: {row.exact_gamma0}",
                f"  anchor crossover: {row.anchor_crossover}",
                f"  basin shape: {row.basin_shape}",
            ]
        )
    lines.extend(
        [
            "",
            "Safe read:",
            "- exact gamma=0 baseline is necessary, but not sufficient",
            "- anchor-local crossover is the smallest stable discriminator",
            "- basin width and seed selectivity do not predict complex survival cleanly",
            "",
            "Final verdict:",
            "retained narrow predictor: complex-action survival requires an anchor-local crossover; coarser basin geometry does not predict it",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("markdown", "text", "json"), default="markdown")
    parser.add_argument("--write-log", help="optional path to write the rendered report")
    args = parser.parse_args()

    payload = {
        "rows": [row.__dict__ for row in ROWS],
        "summary": {
            "predictor": "anchor-local crossover",
            "exact_gamma0_necessary": True,
            "coarser_predictor_found": False,
            "shared_result": "complex-action survival is anchor-local and boundary-sensitive",
        },
    }

    if args.format == "json":
        rendered = json.dumps(payload, indent=2, sort_keys=True)
    elif args.format == "text":
        rendered = render_text(ROWS)
    else:
        rendered = render_markdown(ROWS)

    print(rendered)

    if args.write_log:
        path = Path(args.write_log)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
