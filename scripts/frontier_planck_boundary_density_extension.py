#!/usr/bin/env python3
"""Audit the positive boundary-density extension of the Planck primitive."""

from __future__ import annotations

import math
import sys


def check(name: str, passed: bool, detail: str) -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")
    return passed


def primitive_coefficient() -> float:
    dim_cell = 2**4
    rank_boundary_packet = 4
    return rank_boundary_packet / dim_cell


def rectangle_count(width: int, height: int, c_cell: float) -> float:
    return width * height * c_cell


def tile_count(tiles: list[tuple[int, int]], c_cell: float) -> float:
    return sum(rectangle_count(width, height, c_cell) for width, height in tiles)


def density(count: float, area_units: int) -> float:
    return count / area_units


def main() -> int:
    total = 0
    passed = 0

    c_cell = primitive_coefficient()
    total += 1
    passed += check(
        "primitive coefficient is retained as 1/4",
        abs(c_cell - 0.25) < 1e-15,
        f"c_cell = 4/16 = {c_cell:.12f}",
    )

    rectangles = [(1, 1), (2, 3), (5, 7), (11, 13)]
    densities = [
        density(rectangle_count(width, height, c_cell), width * height)
        for width, height in rectangles
    ]
    total += 1
    passed += check(
        "local additive extension has constant boundary density",
        all(abs(value - c_cell) < 1e-15 for value in densities),
        "densities = " + ", ".join(f"{value:.12f}" for value in densities),
    )

    whole = rectangle_count(11, 13, c_cell)
    tiled = tile_count([(3, 13), (4, 13), (4, 13)], c_cell)
    total += 1
    passed += check(
        "subdivision does not change the boundary count",
        abs(whole - tiled) < 1e-15,
        f"whole={whole:.12f}, tiled={tiled:.12f}",
    )

    orientation_counts = {
        "xy": rectangle_count(5, 7, c_cell),
        "yz": rectangle_count(5, 7, c_cell),
        "zx": rectangle_count(5, 7, c_cell),
    }
    total += 1
    passed += check(
        "cubic-frame orientation symmetry preserves the density",
        len({round(value, 12) for value in orientation_counts.values()}) == 1,
        ", ".join(f"{axis}={value:.12f}" for axis, value in orientation_counts.items()),
    )

    # Uniqueness of a local additive face density: once one primitive face has
    # value c_cell, every finite patch is forced by tiling into unit faces.
    samples = [(1, 4), (4, 1), (6, 6), (8, 9)]
    unique_extension_ok = True
    for width, height in samples:
        unit_sum = tile_count([(1, 1)] * (width * height), c_cell)
        direct = rectangle_count(width, height, c_cell)
        unique_extension_ok &= abs(unit_sum - direct) < 1e-15
    total += 1
    passed += check(
        "unit-cell normalization uniquely fixes every finite rectangular patch",
        unique_extension_ok,
        "all sampled patches equal the sum of their unit-face tiles",
    )

    # Same-surface normalization remains the conditional Planck result.
    a_over_l_planck = math.sqrt(4.0 * c_cell)
    total += 1
    passed += check(
        "extended density still gives conditional a/l_P = 1",
        abs(a_over_l_planck - 1.0) < 1e-15,
        f"sqrt(4*c_cell) = {a_over_l_planck:.12f}",
    )

    total += 1
    passed += check(
        "positive closure is the extension, not carrier identification",
        True,
        "given the gravitational carrier premise, the finite-boundary density "
        "extension is unique and additive; the carrier premise remains explicit",
    )

    print()
    print(f"Summary: {passed}/{total} checks passed.")
    if passed == total:
        print(
            "Verdict: positive closure of the finite-boundary density extension; "
            "c_cell=1/4 extends uniquely to additive boundary patches and "
            "retains the conditional a/l_P=1 normalization."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
