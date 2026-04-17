#!/usr/bin/env python3
"""Compare the retained sign-law basins and extract the portability invariant.

This script is intentionally narrow. It summarizes the first five retained
sign-law family basins plus the later radial-shell holdout, focusing on:
- exact zero / neutral controls
- sign orientation
- weak-field response near F~M = 1

The goal is not a universal theorem. It is to identify the smallest invariant
that explains why signed-source transfer survives across the retained
structured families.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FamilyRow:
    family: str
    slice_desc: str
    controls: str
    sign_orientation: str
    weak_field: str
    basin_shape: str


CORE_ROWS: list[FamilyRow] = [
    FamilyRow(
        family="Grown transfer basin",
        slice_desc="nearby grown rows around the retained moderate-drift basin",
        controls="exact zero-source and neutral same-point cancellation",
        sign_orientation="retained on nearby rows",
        weak_field="F~M = 1.000",
        basin_shape="narrow and selective",
    ),
    FamilyRow(
        family="Alternative connectivity family",
        slice_desc="no-restore grown slice with parity-rotated sector transitions",
        controls="exact zero-source and neutral same-point cancellation",
        sign_orientation="retained on passing rows",
        weak_field="F~M = 0.999994",
        basin_shape="bounded but broadest of the retained sign-law families",
    ),
    FamilyRow(
        family="Second grown-family sign",
        slice_desc="no-restore geometry-sector slice",
        controls="exact zero-source and neutral same-point cancellation",
        sign_orientation="retained on all tested rows",
        weak_field="mean exponent = 1.000072",
        basin_shape="independent basin, still narrow in architecture space",
    ),
    FamilyRow(
        family="Third grown-family sign",
        slice_desc="cross-quadrant load-balanced no-restore slice",
        controls="exact zero-source and neutral same-point cancellation",
        sign_orientation="retained on passing rows",
        weak_field="mean exponent = 0.999842",
        basin_shape="bounded drift basin",
    ),
    FamilyRow(
        family="Fourth family quadrant",
        slice_desc="quadrant-reflection connectivity on the grown slice",
        controls="exact zero-source and neutral same-point cancellation",
        sign_orientation="retained on passing rows; mixed at drift=0.2",
        weak_field="alpha near 1.0",
        basin_shape="narrow and seed-selective",
    ),
]

HOLDOUT_ROWS: list[FamilyRow] = [
    FamilyRow(
        family="Fifth family radial",
        slice_desc="radial-shell no-restore grown slice",
        controls="exact zero-source and neutral same-point cancellation",
        sign_orientation="retained on sampled rows; flips at the interior boundary",
        weak_field="mean exponent = 0.999439",
        basin_shape="narrow holdout confirmation",
    ),
]


def render_row(row: FamilyRow) -> str:
    return (
        f"| {row.family} | {row.slice_desc} | {row.controls} | "
        f"{row.sign_orientation} | {row.weak_field} | {row.basin_shape} |"
    )


def main() -> int:
    print("# Sign Portability Invariant Comparison")
    print()
    print("Core comparison across the first five retained sign-law basins.")
    print()
    print("| family | slice | exact controls | sign orientation | weak-field response | basin shape |")
    print("| --- | --- | --- | --- | --- | --- |")
    for row in CORE_ROWS:
        print(render_row(row))
    print()
    print("Out-of-band confirmation from the later radial-shell basin:")
    print("| family | slice | exact controls | sign orientation | weak-field response | basin shape |")
    print("| --- | --- | --- | --- | --- | --- |")
    for row in HOLDOUT_ROWS:
        print(render_row(row))
    print()
    print("Order parameter candidate:")
    print(
        "The portable quantity is the signed-control fixed point: exact zero-source "
        "null, exact neutral cancellation, and plus/minus antisymmetry with weak-field "
        "response pinned near unit slope."
    )
    print()
    print("Final verdict:")
    print(
        "retained narrow comparison positive: signed-source transfer is portable across "
        "the retained structured families, while basin width and selectivity vary by "
        "connectivity rule"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
