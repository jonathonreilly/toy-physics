#!/usr/bin/env python3
"""
Exact root-face launch theorem for the 3+1 plaquette program.

This runner isolates the exact local launch sectors on a plaquette face.

Two local face problems matter:
  1. the root face q itself, with 4 incident 3-cells
  2. a generic frontier face with one parent cell already occupied, leaving
     3 exterior incident 3-cells

In both cases, keeping the face in the boundary requires odd exterior parity.
That gives exact 1-cell and 3-cell launch sectors.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


DIMS = 4

Cell = tuple[tuple[int, int, int, int], tuple[int, int, int]]
Plaquette = tuple[tuple[int, int, int, int], tuple[int, int]]


def cell_faces(cell: Cell) -> tuple[Plaquette, ...]:
    anchor, axes = cell
    faces: list[Plaquette] = []
    for omitted_axis in axes:
        plane = tuple(a for a in axes if a != omitted_axis)
        faces.append((anchor, plane))
        shifted = list(anchor)
        shifted[omitted_axis] += 1
        faces.append((tuple(shifted), plane))
    return tuple(faces)


def boundary_faces(cells: tuple[Cell, ...]) -> frozenset[Plaquette]:
    boundary: set[Plaquette] = set()
    for cell in cells:
        for face in cell_faces(cell):
            if face in boundary:
                boundary.remove(face)
            else:
                boundary.add(face)
    return frozenset(boundary)


def root_face() -> Plaquette:
    return ((0, 0, 0, 0), (0, 1))


def incident_cells(face: Plaquette) -> tuple[Cell, ...]:
    anchor, plane = face
    orthogonal_axes = [axis for axis in range(DIMS) if axis not in plane]
    cells: list[Cell] = []
    for extra_axis in orthogonal_axes:
        axes = tuple(sorted((*plane, extra_axis)))
        cells.append((anchor, axes))
        shifted = list(anchor)
        shifted[extra_axis] -= 1
        cells.append((tuple(shifted), axes))
    return tuple(cells)


def root_incident_cells() -> tuple[Cell, ...]:
    return incident_cells(root_face())


def generic_parent_cell() -> Cell:
    return ((0, 0, 0, 0), (0, 1, 2))


def generic_exterior_cells() -> tuple[Cell, ...]:
    parent = generic_parent_cell()
    return tuple(cell for cell in root_incident_cells() if cell != parent)


def launch_sector_counts(cells: tuple[Cell, ...], tagged_face: Plaquette) -> Counter[tuple[int, int]]:
    counts: Counter[tuple[int, int]] = Counter()
    for subset_size in range(1, len(cells) + 1, 2):
        for subset in combinations(cells, subset_size):
            boundary = boundary_faces(tuple(subset))
            if tagged_face not in boundary:
                continue
            counts[(len(boundary), len(boundary) - 1)] += 1
    return counts


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    q = root_face()
    root_cells = root_incident_cells()
    exterior_cells = generic_exterior_cells()
    root_counts = launch_sector_counts(root_cells, q)
    generic_counts = launch_sector_counts(exterior_cells, q)

    print("=" * 78)
    print("EXACT ROOT-FACE LAUNCH THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print(f"Root face q                         = {q}")
    print(f"Incident 3-cells at q              = {len(root_cells)}")
    print(f"Generic exterior 3-cells per face  = {len(exterior_cells)}")
    print()
    print("Root-face odd launch sectors")
    for key, multiplicity in sorted(root_counts.items()):
        boundary_count, outgoing = key
        print(f"  |dV| = {boundary_count:2d}, outgoing frontier faces = {outgoing:2d}, multiplicity = {multiplicity}")
    print()
    print("Generic frontier-face odd launch sectors")
    for key, multiplicity in sorted(generic_counts.items()):
        boundary_count, outgoing = key
        print(f"  |dV| = {boundary_count:2d}, outgoing frontier faces = {outgoing:2d}, multiplicity = {multiplicity}")
    print()
    print("Structural local launch polynomials")
    print("  root face:    H_root(z,p) = 1 + 4 p^4 z^5 + 4 p^14 z^15")
    print("  generic face: H_gen(z,p)  = 1 + 3 p^4 z^5 + 1 p^14 z^15")
    print()

    checks = [
        check_equal("root face has 4 incident 3-cells", len(root_cells), 4),
        check_equal("generic frontier face has 3 exterior 3-cells", len(exterior_cells), 3),
        check_equal("root-face launch sectors", dict(root_counts), {(6, 5): 4, (16, 15): 4}),
        check_equal("generic-face launch sectors", dict(generic_counts), {(6, 5): 3, (16, 15): 1}),
    ]

    print("Checks")
    passed = 0
    for ok, message in checks:
        print(" ", message)
        passed += int(ok)
    failed = len(checks) - passed
    print()
    print(f"SUMMARY: exact {passed} pass / {failed} fail")
    print()

    if failed:
        return 1

    print("Conclusion: local frontier faces already have 1-cell and 3-cell launch sectors.")
    print("So a single directed-cell launch cannot by itself close the full rooted problem.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
