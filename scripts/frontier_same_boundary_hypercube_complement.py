#!/usr/bin/env python3
"""
Exact same-boundary 4-cube complement theorem on the 3+1 plaquette surface.

This runner identifies the first exact same-boundary ambiguity of the rooted
3-chain problem itself.

Fix one rooted 3-cell c.  Inside any incident unit 4-cube, the only subsets of
the 8 boundary 3-cells with the same plaquette boundary as c are:

  1. the facet c itself
  2. the 7-facet complement of c in that 4-cube boundary

The complement is connected and has the same boundary as c.  For a tagged root
face q there are 4 incident root cells and each root cell lies in exactly 2
incident 4-cubes, giving 8 minimal rooted same-boundary hidden completions.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter, deque
from itertools import combinations


DIMS = 4

Cell = tuple[tuple[int, int, int, int], tuple[int, int, int]]
Plaquette = tuple[tuple[int, int, int, int], tuple[int, int]]
Hypercube = tuple[int, int, int, int]


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


def boundary_faces(cells: tuple[Cell, ...] | frozenset[Cell]) -> frozenset[Plaquette]:
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


def hypercubes_incident_to_cell(cell: Cell) -> tuple[Hypercube, ...]:
    anchor, axes = cell
    omitted_axis = next(axis for axis in range(DIMS) if axis not in axes)
    hypercubes: list[Hypercube] = []
    for shift in (0, -1):
        origin = list(anchor)
        origin[omitted_axis] += shift
        hypercubes.append(tuple(origin))
    return tuple(hypercubes)


def hypercube_boundary_cells(origin: Hypercube) -> tuple[Cell, ...]:
    boundary: list[Cell] = []
    for omitted_axis in range(DIMS):
        axes = tuple(axis for axis in range(DIMS) if axis != omitted_axis)
        lower_anchor = origin
        upper_anchor = list(origin)
        upper_anchor[omitted_axis] += 1
        boundary.append((lower_anchor, axes))
        boundary.append((tuple(upper_anchor), axes))
    return tuple(boundary)


def connected(cells: frozenset[Cell]) -> bool:
    if not cells:
        return False
    face_sets = {cell: set(cell_faces(cell)) for cell in cells}
    start = next(iter(cells))
    seen = {start}
    frontier = deque([start])
    while frontier:
        current = frontier.popleft()
        for candidate in cells:
            if candidate in seen:
                continue
            if face_sets[current].intersection(face_sets[candidate]):
                seen.add(candidate)
                frontier.append(candidate)
    return len(seen) == len(cells)


def same_boundary_subsets(target: Cell, origin: Hypercube) -> dict[int, list[frozenset[Cell]]]:
    target_boundary = boundary_faces((target,))
    facets = hypercube_boundary_cells(origin)
    matches: dict[int, list[frozenset[Cell]]] = {}
    for subset_size in range(1, len(facets) + 1):
        families: list[frozenset[Cell]] = []
        for subset in combinations(facets, subset_size):
            subset_cells = frozenset(subset)
            if boundary_faces(subset_cells) == target_boundary:
                families.append(subset_cells)
        if families:
            matches[subset_size] = families
    return matches


def minimal_root_hidden_completions() -> list[tuple[Cell, Hypercube, frozenset[Cell]]]:
    rooted: list[tuple[Cell, Hypercube, frozenset[Cell]]] = []
    for cell in root_incident_cells():
        for origin in hypercubes_incident_to_cell(cell):
            facets = set(hypercube_boundary_cells(origin))
            if cell not in facets:
                continue
            complement = frozenset(facets - {cell})
            if root_face() not in boundary_faces(complement):
                continue
            rooted.append((cell, origin, complement))
    return rooted


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    target = ((0, 0, 0, 0), (0, 1, 2))
    target_boundary = boundary_faces((target,))
    origins = hypercubes_incident_to_cell(target)
    matches = same_boundary_subsets(target, origins[0])
    rooted_hidden = minimal_root_hidden_completions()
    rooted_size_hist = Counter(len(complement) for _, _, complement in rooted_hidden)

    print("=" * 78)
    print("EXACT SAME-BOUNDARY 4-CUBE COMPLEMENT THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print(f"root face q                              = {root_face()}")
    print(f"chosen rooted 3-cell c                   = {target}")
    print(f"incident 4-cubes to c                    = {origins}")
    print(f"boundary size of c                       = {len(target_boundary)}")
    print()
    print("Same-boundary subsets on one incident 4-cube")
    for subset_size, families in sorted(matches.items()):
        print(f"  subset size {subset_size}: multiplicity {len(families)}")
        for family in families:
            print(f"    {tuple(sorted(family))}")
    print()
    print("Minimal rooted same-boundary hidden completions at q")
    for cell, origin, complement in rooted_hidden:
        print(f"  root cell {cell}, 4-cube origin {origin}, complement size {len(complement)}")
    print()

    checks = [
        check_equal("root face has 4 incident cells", len(root_incident_cells()), 4),
        check_equal("a rooted 3-cell has 2 incident 4-cubes", len(origins), 2),
        check_equal("same-boundary subset-size classes on one 4-cube", sorted(matches), [1, 7]),
        check_equal("exact one-cell local filling multiplicity", len(matches[1]), 1),
        check_equal("exact seven-cell complement multiplicity", len(matches[7]), 1),
        check_equal("seven-cell complement is connected", connected(next(iter(matches[7]))), True),
        check_equal(
            "seven-cell complement has same boundary as c",
            boundary_faces(next(iter(matches[7]))),
            target_boundary,
        ),
        check_equal("rooted minimal hidden completion count", len(rooted_hidden), 8),
        check_equal("rooted hidden completion sizes", dict(sorted(rooted_size_hist.items())), {7: 8}),
        check_equal(
            "every rooted hidden completion keeps q on the boundary",
            all(root_face() in boundary_faces(complement) for _, _, complement in rooted_hidden),
            True,
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

    print("Conclusion: the rooted 3-chain problem already has a local same-boundary")
    print("hidden completion sector: a 3-cell can be replaced by the 7-facet complement")
    print("of any incident 4-cube boundary while preserving the plaquette boundary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
