#!/usr/bin/env python3
"""Compact classifier for the portable weak-field package hierarchy.

The retained evidence supports a nested read:

- broad portable weak-field package: the signed-control fixed point
- stricter distance tail: open directed transport subset of that package
- narrower complex-action branch: exact gamma=0 / crossover subset

This script is intentionally review-safe. It summarizes only retained family
cards and closures that already exist on main, and it does not claim a
universal geometry theorem.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class LayerRow:
    layer: str
    retained_family_cards: str
    closure_or_boundary: str
    safe_read: str


ROWS: list[LayerRow] = [
    LayerRow(
        layer="Broad portable weak-field package",
        retained_family_cards=(
            "grown transfer basin, alt connectivity family, second grown-family sign, "
            "third grown-family sign, fourth family quadrant, fifth family radial holdout"
        ),
        closure_or_boundary=(
            "exact zero-source cancellation, exact neutral same-point cancellation, "
            "plus/minus antisymmetry, weak-field response near unit slope"
        ),
        safe_read=(
            "portable across several structured families; family labels change basin width "
            "and selectivity, not the signed-control fixed point"
        ),
    ),
    LayerRow(
        layer="Stricter distance tail",
        retained_family_cards=(
            "first two grown families as the preservation anchor; alt connectivity, third "
            "family, and fourth family as breakpoints; fifth family radial as a direction-only holdout"
        ),
        closure_or_boundary=(
            "open directed transport that keeps direction and tail shape coupled; shell "
            "locking, reflection closure, deep branch routing, and radial confinement break it"
        ),
        safe_read=(
            "a narrower subset of the broad package; the near-Newtonian tail is not "
            "geometry-independent across the retained structured families"
        ),
    ),
    LayerRow(
        layer="Narrower complex-action branch",
        retained_family_cards=(
            "original grown basin, second-family complex anchor row, alt connectivity failure as a boundary check"
        ),
        closure_or_boundary=(
            "exact gamma=0 anchor plus crossover structure; boundary-sensitive and anchor-local"
        ),
        safe_read=(
            "more selective than the distance tail; it survives only on the narrow gamma "
            "surface and does not follow from sign portability alone"
        ),
    ),
]


def render_table(rows: list[LayerRow]) -> str:
    headers = ["layer", "retained family cards", "closure or boundary", "safe read"]
    columns = [
        [row.layer for row in rows],
        [row.retained_family_cards for row in rows],
        [row.closure_or_boundary for row in rows],
        [row.safe_read for row in rows],
    ]
    widths = [
        max(len(headers[i]), max(len(value) for value in col))
        for i, col in enumerate(columns)
    ]

    def fmt(values: list[str]) -> str:
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(values))

    sep = "-+-".join("-" * width for width in widths)
    lines = [fmt(headers), sep]
    for row in rows:
        lines.append(
            fmt(
                [
                    row.layer,
                    row.retained_family_cards,
                    row.closure_or_boundary,
                    row.safe_read,
                ]
            )
        )
    return "\n".join(lines)


def render_markdown(rows: list[LayerRow]) -> str:
    lines = [
        "# Portable Package Hierarchy Classifier",
        "",
        "**Date:** 2026-04-06",
        "**Status:** review-safe compact classifier",
        "",
        "## Question",
        "",
        "Can the retained nested family structure be compressed into one safe classifier: broad portable weak-field package, stricter distance tail, narrower complex-action branch?",
        "",
        "## Retained Cards",
        "",
        "- broad portable package: [`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md), [`docs/PORTABLE_PACKAGE_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PORTABLE_PACKAGE_EXTENSION_NOTE.md), [`docs/PORTABLE_CARD_EXTENSION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/PORTABLE_CARD_EXTENSION_NOTE.md)",
        "- distance-tail boundary: [`docs/DISTANCE_LAW_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_PORTABILITY_NOTE.md), [`docs/DISTANCE_LAW_BREAKPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_BREAKPOINT_NOTE.md)",
        "- complex-action branch: [`docs/COMPLEX_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/COMPLEX_ACTION_NOTE.md), [`docs/COMPLEX_SELECTIVITY_COMPARE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/COMPLEX_SELECTIVITY_COMPARE_NOTE.md)",
        "",
        "## Classifier",
        "",
        render_table(rows),
        "",
        "## Safe Read",
        "",
        "- the broad layer is the signed-control fixed point: exact zero / neutral cancellation, plus/minus antisymmetry, and weak-field response near unit slope",
        "- the distance tail is stricter because it needs open directed transport; the first two grown families preserve direction and tail together, while newer retained families break or flatten one of those pieces",
        "- the complex-action branch is narrower still because it needs the exact gamma=0 anchor and crossover structure, and it is boundary-sensitive on adjacent families",
        "",
        "## Final Verdict",
        "",
        "**review-safe classifier: broad portable weak-field package, stricter distance tail, narrower complex-action branch**",
    ]
    return "\n".join(lines)


def render_text(rows: list[LayerRow]) -> str:
    lines = [
        "Portable Package Hierarchy Classifier",
        "Date: 2026-04-06",
        "Status: review-safe compact classifier",
        "",
        "Question:",
        "Can the retained nested family structure be compressed into one safe classifier?",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"- {row.layer}",
                f"  cards: {row.retained_family_cards}",
                f"  boundary: {row.closure_or_boundary}",
                f"  safe read: {row.safe_read}",
            ]
        )
    lines.extend(
        [
            "",
            "Final verdict:",
            "review-safe classifier: broad portable weak-field package, stricter distance tail, narrower complex-action branch",
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
            "broad_portable_weak_field_package": True,
            "distance_tail_stricter": True,
            "complex_action_narrower_still": True,
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
