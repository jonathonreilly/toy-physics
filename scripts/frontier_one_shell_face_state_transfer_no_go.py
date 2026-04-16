#!/usr/bin/env python3
"""
Exact no-go against one-shell face-state multiset transfer on the 3+1 plaquette surface.

This runner sharpens the local-closure obstruction beyond the minimal scalar
face ansatz.  It defines the exact one-shell local state of a boundary face f:

  - all occupied 3-cells incident to f
  - all occupied 3-cells incident to any plaquette face of those incident cells

reduced by the full affine stabilizer of a plaquette face.

It then enumerates every rooted connected 3-chain with |V| = 3 and q in dV,
groups them by the multiset of one-shell local boundary-face states on dV, and
shows that this exact multiset still does not determine the next exact rooted
continuation count.

So any closure mediated only by the multiset of exact one-shell face-star
states is not the full gauge-vacuum transfer.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product


DIMS = 4
MAX_CELLS = 3

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
    return cells_incident_to_face(root_face())


def rooted_levels(max_cells: int = MAX_CELLS) -> dict[int, set[frozenset[Cell]]]:
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


def next_rooted_count(cells: frozenset[Cell]) -> int:
    q = root_face()
    next_shapes: set[frozenset[Cell]] = set()
    adjacent: set[Cell] = set()
    for occupied in cells:
        for face in cell_faces(occupied):
            for candidate in cells_incident_to_face(face):
                if candidate in cells:
                    continue
                adjacent.add(candidate)
    for candidate in adjacent:
        new_cells = frozenset((*cells, candidate))
        if q in boundary_faces(new_cells):
            next_shapes.add(new_cells)
    return len(next_shapes)


@lru_cache(maxsize=None)
def cell_vertices(cell: Cell) -> frozenset[tuple[int, int, int, int]]:
    anchor, axes = cell
    vertices: set[tuple[int, int, int, int]] = set()
    for bits in product((0, 1), repeat=3):
        point = list(anchor)
        for bit, axis in zip(bits, axes):
            point[axis] += bit
        vertices.add(tuple(point))
    return frozenset(vertices)


def canonical_cell_from_vertices(vertices: frozenset[tuple[int, int, int, int]]) -> Cell:
    mins = tuple(min(vertex[axis] for vertex in vertices) for axis in range(DIMS))
    maxs = tuple(max(vertex[axis] for vertex in vertices) for axis in range(DIMS))
    axes = tuple(axis for axis in range(DIMS) if maxs[axis] - mins[axis] == 1)
    return mins, axes


@lru_cache(maxsize=None)
def face_neighborhood(face: Plaquette) -> frozenset[Cell]:
    cells: set[Cell] = set(cells_incident_to_face(face))
    frontier = list(cells)
    for cell in frontier:
        for next_face in cell_faces(cell):
            for candidate in cells_incident_to_face(next_face):
                cells.add(candidate)
    return frozenset(cells)


def face_stabilizer() -> tuple[tuple[dict[int, int], tuple[bool, bool, bool, bool]], ...]:
    group: list[tuple[dict[int, int], tuple[bool, bool, bool, bool]]] = []
    for plane_image in ((0, 1), (1, 0)):
        for orth_image in ((2, 3), (3, 2)):
            axis_image = {
                0: plane_image[0],
                1: plane_image[1],
                2: orth_image[0],
                3: orth_image[1],
            }
            for reflects in product((False, True), repeat=4):
                group.append((axis_image, reflects))
    return tuple(group)


FACE_STABILIZER = face_stabilizer()


def transform_relative_vertex(
    vertex: tuple[int, int, int, int],
    axis_image: dict[int, int],
    reflects: tuple[bool, bool, bool, bool],
) -> tuple[int, int, int, int]:
    image = [0, 0, 0, 0]
    for axis, value in enumerate(vertex):
        image[axis_image[axis]] = value
    if reflects[0]:
        image[0] = 1 - image[0]
    if reflects[1]:
        image[1] = 1 - image[1]
    if reflects[2]:
        image[2] = -image[2]
    if reflects[3]:
        image[3] = -image[3]
    return tuple(image)


def normalize_local_face_state(cells: frozenset[Cell], face: Plaquette) -> tuple[Cell, ...]:
    anchor, plane = face
    orthogonal_axes = tuple(axis for axis in range(DIMS) if axis not in plane)
    axis_renaming = {
        plane[0]: 0,
        plane[1]: 1,
        orthogonal_axes[0]: 2,
        orthogonal_axes[1]: 3,
    }

    occupied = tuple(sorted(cell for cell in cells if cell in face_neighborhood(face)))
    best: tuple[Cell, ...] | None = None

    for axis_image, reflects in FACE_STABILIZER:
        transformed_cells: list[Cell] = []
        for cell in occupied:
            transformed_vertices: set[tuple[int, int, int, int]] = set()
            for vertex in cell_vertices(cell):
                relative = tuple(vertex[axis] - anchor[axis] for axis in range(DIMS))
                renamed = [0, 0, 0, 0]
                for axis, value in enumerate(relative):
                    renamed[axis_renaming[axis]] = value
                transformed_vertices.add(
                    transform_relative_vertex(tuple(renamed), axis_image, reflects)
                )
            transformed_cells.append(canonical_cell_from_vertices(frozenset(transformed_vertices)))
        candidate = tuple(sorted(transformed_cells))
        if best is None or candidate < best:
            best = candidate

    if best is None:
        raise RuntimeError("empty local face state is impossible on a boundary face")
    return best


def boundary_state_multiset_signature(cells: frozenset[Cell]) -> tuple[tuple[tuple[Cell, ...], int], ...]:
    histogram = Counter(normalize_local_face_state(cells, face) for face in boundary_faces(cells))
    return tuple(sorted(histogram.items()))


def witness_pair(rooted_n3: list[frozenset[Cell]]) -> tuple[
    tuple[tuple[tuple[Cell, ...], int], ...],
    frozenset[Cell],
    frozenset[Cell],
    int,
    int,
]:
    buckets: defaultdict[
        tuple[tuple[tuple[Cell, ...], int], ...],
        list[tuple[int, frozenset[Cell]]],
    ] = defaultdict(list)
    for cells in rooted_n3:
        buckets[boundary_state_multiset_signature(cells)].append((next_rooted_count(cells), cells))

    for signature, items in buckets.items():
        counts = sorted({count for count, _ in items})
        if counts != [35, 37]:
            continue
        examples: dict[int, frozenset[Cell]] = {}
        for count, cells in items:
            examples.setdefault(count, cells)
        return signature, examples[35], examples[37], 35, 37

    raise RuntimeError("expected witness pair with continuation counts 35 and 37")


WITNESS_A = frozenset(
    {
        ((0, -1, 0, 0), (0, 1, 3)),
        ((0, 0, -1, 0), (0, 2, 3)),
        ((0, 0, 0, 0), (0, 1, 3)),
    }
)

WITNESS_B = frozenset(
    {
        ((0, 0, -1, 0), (0, 1, 2)),
        ((0, 0, 0, -1), (0, 1, 3)),
        ((0, 0, 0, 0), (0, 1, 2)),
    }
)


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    levels = rooted_levels(MAX_CELLS)
    rooted_n3 = rooted_shapes(levels, 3)
    signature, witness_a, witness_b, count_a, count_b = witness_pair(rooted_n3)
    witness_a_signature = boundary_state_multiset_signature(witness_a)
    witness_b_signature = boundary_state_multiset_signature(witness_b)
    witness_a_next = next_rooted_count(witness_a)
    witness_b_next = next_rooted_count(witness_b)

    print("=" * 78)
    print("EXACT ONE-SHELL FACE-STATE TRANSFER NO-GO ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print(f"face stabilizer size                  = {len(FACE_STABILIZER)}")
    print(f"exact rooted n = 3 count              = {len(rooted_n3)}")
    print(f"witness continuation counts           = {count_a}, {count_b}")
    print(f"witness boundary-face count           = {len(boundary_faces(witness_a))}")
    print(f"witness signature local-state types   = {len(signature)}")
    print()
    print("Witness A (continuation count 35)")
    print(f"  {tuple(sorted(witness_a))}")
    print("Witness B (continuation count 37)")
    print(f"  {tuple(sorted(witness_b))}")
    print()
    print("Shared exact one-shell boundary-state multiset")
    for local_state, multiplicity in signature:
        print(f"  multiplicity {multiplicity:2d}: {local_state}")
    print()

    checks = [
        check_equal("face stabilizer size", len(FACE_STABILIZER), 64),
        check_equal("exact rooted n=3 count", len(rooted_n3), 1164),
        check_equal("explicit witness A recovered", witness_a, WITNESS_A),
        check_equal("explicit witness B recovered", witness_b, WITNESS_B),
        check_equal("witness A one-shell multiset", witness_a_signature, signature),
        check_equal("witness B one-shell multiset", witness_b_signature, signature),
        check_equal("witness A continuation count", witness_a_next, 35),
        check_equal("witness B continuation count", witness_b_next, 37),
        check_equal("witness boundary-face count", len(boundary_faces(witness_a)), 16),
        check_equal("witness signature type count", len(signature), 5),
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

    print("Conclusion: the full multiset of exact one-shell boundary-face states")
    print("still does not determine the next rooted continuation count.")
    print("So any closure mediated only by one-shell local face-state multisets is not exact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
