#!/usr/bin/env python3
"""Compare the portable fixed-field package against stricter subsets.

This script is intentionally narrow: it only summarizes retained results that
already exist on main and separates the broad sign-law package from narrower
distance-law and complex-action branches.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/Users/jonreilly/Projects/Physics")


@dataclass(frozen=True)
class FamilyRow:
    family: str
    sign_portable: str
    distance_tail: str
    complex_action: str
    note: str


ROWS = [
    FamilyRow(
        family="First grown family",
        sign_portable="yes",
        distance_tail="yes",
        complex_action="yes, narrow",
        note="Retained grown transfer basin and original complex basin.",
    ),
    FamilyRow(
        family="Second grown family",
        sign_portable="yes",
        distance_tail="yes",
        complex_action="yes, tiny basin",
        note="Retained second-family sign and complex notes.",
    ),
    FamilyRow(
        family="Alt connectivity family",
        sign_portable="yes",
        distance_tail="no",
        complex_action="no",
        note="Strong sign-law + F~M transfer, but complex fails and distance tail breaks.",
    ),
    FamilyRow(
        family="Third grown family",
        sign_portable="yes",
        distance_tail="no",
        complex_action="no",
        note="Portable sign-law, but complex is boundary-only and distance tail steepens.",
    ),
    FamilyRow(
        family="Fourth family quadrant",
        sign_portable="yes",
        distance_tail="no",
        complex_action="no",
        note="Quadrant basin retains sign-law but cancels distance tail and complex branch.",
    ),
    FamilyRow(
        family="Fifth family radial",
        sign_portable="yes",
        distance_tail="partial",
        complex_action="yes, anchor-local",
        note="Distance tail flattens, but anchor-local complex crossover survives.",
    ),
    FamilyRow(
        family="Sixth family sheared",
        sign_portable="yes",
        distance_tail="no",
        complex_action="unknown",
        note="Retained sign basin only; complex companion not yet promoted as broad.",
    ),
]


def render_table(rows: list[FamilyRow]) -> str:
    headers = ["family", "sign portability", "distance law", "complex action", "note"]
    columns = [
        [row.family for row in rows],
        [row.sign_portable for row in rows],
        [row.distance_tail for row in rows],
        [row.complex_action for row in rows],
        [row.note for row in rows],
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
                    row.family,
                    row.sign_portable,
                    row.distance_tail,
                    row.complex_action,
                    row.note,
                ]
            )
        )
    return "\n".join(lines)


def main() -> int:
    print("Portable Package Extension Compare")
    print()
    print("Question:")
    print(
        "Does the portable fixed-field package extend beyond the first two grown families?"
    )
    print()
    print("Comparison:")
    print(render_table(ROWS))
    print()
    print("Read:")
    print(
        "The broad portable package is the signed-control fixed point: exact zero-source"
    )
    print(
        "cancellation, exact neutral cancellation, plus/minus antisymmetry, and near-unit"
    )
    print("weak-field response.")
    print("Distance-law portability is a stricter grown-family subset of that package.")
    print("Complex-action survival is narrower still and remains anchor-local/selective.")
    print()
    print("Verdict:")
    print(
        "Yes, the portable fixed-field package extends beyond the first two grown families,"
    )
    print(
        "but only the sign-law core is broadly portable. The distance law is portable on"
    )
    print(
        "the first two grown families and becomes selective or breaks on newer families,"
    )
    print(
        "while complex action is the most selective branch and does not track the broad"
    )
    print("portable package cleanly.")
    print()
    print(f"Source root: {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
