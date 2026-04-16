#!/usr/bin/env python3
"""
Exact directed-cell boundary-state transfer obstruction on the 3+1 plaquette surface.

This runner compares two rooted 3-chain growth rules:

  1. boundary-shellable growth: add a new cell only across a current boundary face
  2. exact connected growth: add a new cell across any shared plaquette face of the
     current cluster

The exact result is that boundary-shellable transfer is not the full rooted
gauge problem. It already undercounts at n = 3.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter


DIMS = 4
MAX_CELLS = 5

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


def boundary_faces(cells: frozenset[Cell]) -> frozenset[Plaquette]:
    boundary: set[Plaquette] = set()
    for cell in cells:
        for face in cell_faces(cell):
            if face in boundary:
                boundary.remove(face)
            else:
                boundary.add(face)
    return frozenset(boundary)


def cells_incident_to_face(face: Plaquette) -> tuple[Cell, ...]:
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


def root_face() -> Plaquette:
    return ((0, 0, 0, 0), (0, 1))


def root_incident_cells() -> tuple[Cell, ...]:
    q = root_face()
    incident: list[Cell] = []
    for extra_axis in (2, 3):
        axes = tuple(sorted((0, 1, extra_axis)))
        incident.append((q[0], axes))
        shifted = list(q[0])
        shifted[extra_axis] -= 1
        incident.append((tuple(shifted), axes))
    return tuple(incident)


def boundary_shellable_levels(max_cells: int = MAX_CELLS) -> dict[int, set[frozenset[Cell]]]:
    levels: dict[int, set[frozenset[Cell]]] = {
        1: {frozenset((cell,)) for cell in root_incident_cells()}
    }
    for count in range(2, max_cells + 1):
        next_level: set[frozenset[Cell]] = set()
        for cells in levels[count - 1]:
            for face in boundary_faces(cells):
                for candidate in cells_incident_to_face(face):
                    if candidate in cells:
                        continue
                    next_level.add(frozenset((*cells, candidate)))
        levels[count] = next_level
    return levels


def exact_connected_levels(max_cells: int = MAX_CELLS) -> dict[int, set[frozenset[Cell]]]:
    levels: dict[int, set[frozenset[Cell]]] = {
        1: {frozenset((cell,)) for cell in root_incident_cells()}
    }
    for count in range(2, max_cells + 1):
        next_level: set[frozenset[Cell]] = set()
        for cells in levels[count - 1]:
            adjacent: set[Cell] = set()
            for occupied in cells:
                for face in cell_faces(occupied):
                    for candidate in cells_incident_to_face(face):
                        if candidate in cells:
                            continue
                        adjacent.add(candidate)
            for candidate in adjacent:
                next_level.add(frozenset((*cells, candidate)))
        levels[count] = next_level
    return levels


def rooted_shapes(levels: dict[int, set[frozenset[Cell]]], count: int) -> list[frozenset[Cell]]:
    q = root_face()
    return [cells for cells in levels[count] if q in boundary_faces(cells)]


def root_launch_count(cells: frozenset[Cell]) -> int:
    return len(set(root_incident_cells()).intersection(cells))


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    shellable = boundary_shellable_levels(MAX_CELLS)
    exact = exact_connected_levels(MAX_CELLS)

    print("=" * 78)
    print("EXACT DIRECTED-CELL BOUNDARY-STATE TRANSFER OBSTRUCTION ON THE 3+1 LATTICE")
    print("=" * 78)
    print()

    exact_totals: dict[int, int] = {}
    shellable_totals: dict[int, int] = {}

    for count in range(1, MAX_CELLS + 1):
        exact_rooted = rooted_shapes(exact, count)
        shellable_rooted = rooted_shapes(shellable, count)
        exact_totals[count] = len(exact_rooted)
        shellable_totals[count] = len(shellable_rooted)

        by_launch = Counter(root_launch_count(cells) for cells in exact_rooted)
        by_faces = Counter(len(boundary_faces(cells)) for cells in exact_rooted)

        print(f"n = {count}")
        print(f"  exact rooted total            = {len(exact_rooted)}")
        print(f"  boundary-shellable total      = {len(shellable_rooted)}")
        print(f"  exact minus shellable         = {len(exact_rooted) - len(shellable_rooted)}")
        print(f"  exact root-launch sectors     = {dict(sorted(by_launch.items()))}")
        print(f"  exact boundary-face counts    = {dict(sorted(by_faces.items()))}")
        print()

    checks = [
        check_equal("n=1 exact rooted count", exact_totals[1], 4),
        check_equal("n=2 exact rooted count", exact_totals[2], 60),
        check_equal("n=3 exact rooted count", exact_totals[3], 1164),
        check_equal("n=4 exact rooted count", exact_totals[4], 25000),
        check_equal("n=5 exact rooted count", exact_totals[5], 566644),
        check_equal("n=3 shellable undercount", exact_totals[3] - shellable_totals[3], 64),
        check_equal("n=4 shellable undercount", exact_totals[4] - shellable_totals[4], 2340),
        check_equal("n=5 shellable undercount", exact_totals[5] - shellable_totals[5], 71124),
        check_equal(
            "n=3 first multi-launch sector appears",
            Counter(root_launch_count(cells) for cells in rooted_shapes(exact, 3)),
            {1: 1160, 3: 4},
        ),
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

    print("Conclusion: a transfer that sees only current boundary faces is not exact.")
    print("The full rooted problem already contains internal-face-return sectors and")
    print("a k = 3 root-launch sector at n = 3.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
