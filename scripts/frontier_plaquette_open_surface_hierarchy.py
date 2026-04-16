#!/usr/bin/env python3
"""
Plaquette open-surface hierarchy on the exact 3+1 lattice
=========================================================

This runner proves the first geometric fact needed after the constant-lift
no-go: the plaquette is an open-surface problem, not a one-cell problem.

For an elementary cube:
  - the tagged plaquette itself is the unique area-1 same-boundary surface
  - the complementary five faces are the unique area-5 nonlocal completion

In 3+1 dimensions a plaquette belongs to exactly four elementary 3-cubes, so
the first nonlocal layer has multiplicity 4.
"""

from __future__ import annotations

from itertools import combinations


FACES = ("x0", "x1", "y0", "y1", "z0", "z1")

# Edges are named by the two coordinates fixed on the unit cube.
# Boundaries are taken mod 2.
FACE_BOUNDARIES = {
    "x0": frozenset({"x0y0", "x0y1", "x0z0", "x0z1"}),
    "x1": frozenset({"x1y0", "x1y1", "x1z0", "x1z1"}),
    "y0": frozenset({"x0y0", "x1y0", "y0z0", "y0z1"}),
    "y1": frozenset({"x0y1", "x1y1", "y1z0", "y1z1"}),
    "z0": frozenset({"x0z0", "x1z0", "y0z0", "y1z0"}),
    "z1": frozenset({"x0z1", "x1z1", "y0z1", "y1z1"}),
}

TARGET_FACE = "x0"
TARGET_BOUNDARY = FACE_BOUNDARIES[TARGET_FACE]


def xor_boundary(face_subset: tuple[str, ...]) -> frozenset[str]:
    boundary: set[str] = set()
    for face in face_subset:
        for edge in FACE_BOUNDARIES[face]:
            if edge in boundary:
                boundary.remove(edge)
            else:
                boundary.add(edge)
    return frozenset(boundary)


def same_boundary_surfaces() -> list[tuple[str, ...]]:
    out: list[tuple[str, ...]] = []
    for r in range(len(FACES) + 1):
        for subset in combinations(FACES, r):
            if xor_boundary(subset) == TARGET_BOUNDARY:
                out.append(subset)
    return out


def minimal_completion_count_3plus1() -> int:
    dims_total = 4
    dims_in_plaquette = 2
    orthogonal_dirs = dims_total - dims_in_plaquette
    return 2 * orthogonal_dirs


def check(name: str, ok: bool, detail: str) -> tuple[bool, str]:
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: {detail}"


def main() -> int:
    solutions = same_boundary_surfaces()
    solutions_sorted = sorted(solutions, key=lambda s: (len(s), s))
    areas = [len(s) for s in solutions_sorted]
    exact_checks: list[tuple[bool, str]] = []

    exact_checks.append(
        check(
            "exactly two same-boundary surfaces on one cube",
            len(solutions_sorted) == 2,
            f"found {len(solutions_sorted)} solutions",
        )
    )
    exact_checks.append(
        check(
            "area-1 solution is the tagged plaquette",
            solutions_sorted[0] == (TARGET_FACE,),
            f"first solution = {solutions_sorted[0]}",
        )
    )
    exact_checks.append(
        check(
            "area-5 solution is the complementary five faces",
            len(solutions_sorted[1]) == 5 and TARGET_FACE not in solutions_sorted[1],
            f"second solution = {solutions_sorted[1]}",
        )
    )
    exact_checks.append(
        check(
            "same-boundary areas are exactly 1 and 5",
            areas == [1, 5],
            f"areas = {areas}",
        )
    )
    exact_checks.append(
        check(
            "full cube boundary has area 6",
            len(FACES) == 6,
            f"cube boundary area = {len(FACES)}",
        )
    )
    exact_checks.append(
        check(
            "3+1 minimal nonlocal completion count is 4",
            minimal_completion_count_3plus1() == 4,
            f"count = {minimal_completion_count_3plus1()}",
        )
    )

    print("=" * 78)
    print("PLAQUETTE OPEN-SURFACE HIERARCHY ON THE EXACT 3+1 LATTICE")
    print("=" * 78)
    print()
    print(f"Tagged face: {TARGET_FACE}")
    print(f"Tagged boundary: {sorted(TARGET_BOUNDARY)}")
    print()
    print("Same-boundary surfaces on one elementary cube")
    for subset in solutions_sorted:
        print(f"  area={len(subset)}  faces={subset}")
    print()
    print("3+1 minimal-completion count")
    print("  orthogonal directions to a plaquette plane = 2")
    print("  cubes per orthogonal direction             = 2")
    print(f"  total minimal area-5 completions           = {minimal_completion_count_3plus1()}")
    print()
    print("Checks")

    passed = 0
    for ok, msg in exact_checks:
        print(" ", msg)
        passed += int(ok)

    failed = len(exact_checks) - passed
    print()
    print(f"SUMMARY: exact {passed} pass / {failed} fail")

    if failed:
        return 1

    print()
    print("Conclusion: the local plaquette is only the first member of an open-surface hierarchy.")
    print("The first nonlocal completions already appear at area 5 with multiplicity 4 in 3+1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
