#!/usr/bin/env python3
"""
Exact local directed-cell boundary-cluster theorem on the 3+1 plaquette surface.

This runner isolates one directed root 3-cell with a fixed incoming plaquette
face q and enumerates every local outward child configuration exactly.

The exact local picture is:
  - 1 directed root cell
  - 5 outward root faces
  - 15 outward child cells
  - 2^15 raw local child subsets
  - 16 affine stabilizer symmetries preserving the directed root
  - 2844 exact orbit states under that stabilizer

It also isolates the first local coupling structure:
  - 15 child pairs lie on the same outward root face
  - 16 child pairs lie on distinct outward faces but still share a plaquette
  - 74 child pairs are disjoint

So even locally, the directed-cell boundary problem is not a product over
outward faces.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


DIMS = 4
CHILD_COUNT = 15

Cell = tuple[tuple[int, int, int, int], tuple[int, int, int]]
Plaquette = tuple[tuple[int, int, int, int], tuple[int, int]]
GroupElement = tuple[bool, bool, bool, bool]


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


def vertices_cell(cell: Cell) -> set[tuple[int, int, int, int]]:
    anchor, axes = cell
    vertices: set[tuple[int, int, int, int]] = set()
    for bits in product((0, 1), repeat=3):
        point = list(anchor)
        for bit, axis in zip(bits, axes):
            point[axis] += bit
        vertices.add(tuple(point))
    return vertices


def canonical_cell_from_vertices(vertices: set[tuple[int, int, int, int]]) -> Cell:
    mins = tuple(min(vertex[axis] for vertex in vertices) for axis in range(DIMS))
    maxs = tuple(max(vertex[axis] for vertex in vertices) for axis in range(DIMS))
    axes = tuple(axis for axis in range(DIMS) if maxs[axis] - mins[axis] == 1)
    return mins, axes


def vertices_face(face: Plaquette) -> set[tuple[int, int, int, int]]:
    anchor, axes = face
    vertices: set[tuple[int, int, int, int]] = set()
    for bits in product((0, 1), repeat=2):
        point = list(anchor)
        for bit, axis in zip(bits, axes):
            point[axis] += bit
        vertices.add(tuple(point))
    return vertices


def canonical_face_from_vertices(vertices: set[tuple[int, int, int, int]]) -> Plaquette:
    mins = tuple(min(vertex[axis] for vertex in vertices) for axis in range(DIMS))
    maxs = tuple(max(vertex[axis] for vertex in vertices) for axis in range(DIMS))
    axes = tuple(axis for axis in range(DIMS) if maxs[axis] - mins[axis] == 1)
    return mins, axes


def affine_transform(
    vertex: tuple[int, int, int, int],
    swap_xy: bool,
    reflect_x: bool,
    reflect_y: bool,
    reflect_t: bool,
) -> tuple[int, int, int, int]:
    point = list(vertex)
    if swap_xy:
        point[0], point[1] = point[1], point[0]
    if reflect_x:
        point[0] = 1 - point[0]
    if reflect_y:
        point[1] = 1 - point[1]
    if reflect_t:
        point[3] = -point[3]
    return tuple(point)


def transform_cell(cell: Cell, group_element: GroupElement) -> Cell:
    transformed = {affine_transform(vertex, *group_element) for vertex in vertices_cell(cell)}
    return canonical_cell_from_vertices(transformed)


def transform_face(face: Plaquette, group_element: GroupElement) -> Plaquette:
    transformed = {affine_transform(vertex, *group_element) for vertex in vertices_face(face)}
    return canonical_face_from_vertices(transformed)


def root_face() -> Plaquette:
    return ((0, 0, 0, 0), (0, 1))


def root_cell() -> Cell:
    return ((0, 0, 0, 0), (0, 1, 2))


def outgoing_root_faces() -> tuple[Plaquette, ...]:
    q = root_face()
    return tuple(face for face in cell_faces(root_cell()) if face != q)


def outgoing_child_cells() -> tuple[Cell, ...]:
    root = root_cell()
    seen: set[Cell] = set()
    children: list[Cell] = []
    for face in outgoing_root_faces():
        for child in cells_incident_to_face(face):
            if child == root or child in seen:
                continue
            seen.add(child)
            children.append(child)
    return tuple(children)


def stabilizer_permutations(children: tuple[Cell, ...]) -> tuple[tuple[int, ...], ...]:
    q = root_face()
    root = root_cell()
    child_index = {child: index for index, child in enumerate(children)}
    permutations: set[tuple[int, ...]] = set()
    for group_element in product((False, True), repeat=4):
        if transform_cell(root, group_element) != root:
            continue
        if transform_face(q, group_element) != q:
            continue
        images = [transform_cell(child, group_element) for child in children]
        if not all(image in child_index for image in images):
            continue
        permutations.add(tuple(child_index[image] for image in images))
    return tuple(sorted(permutations))


def mask_to_cells(mask: int, children: tuple[Cell, ...]) -> tuple[Cell, ...]:
    subset = [children[index] for index in range(len(children)) if mask & (1 << index)]
    return (root_cell(), *subset)


def outgoing_face_count(mask: int, children: tuple[Cell, ...]) -> int:
    return len(boundary_faces(mask_to_cells(mask, children))) - 1


def shared_face_count(mask: int, children: tuple[Cell, ...]) -> int:
    subset_cells = mask_to_cells(mask, children)
    boundary_count = len(boundary_faces(subset_cells))
    total_faces = 6 * len(subset_cells)
    return (total_faces - boundary_count) // 2


def orbit_rep(mask: int, permutations: tuple[tuple[int, ...], ...]) -> int:
    images = []
    for permutation in permutations:
        image = 0
        for source_index, target_index in enumerate(permutation):
            if mask & (1 << source_index):
                image |= 1 << target_index
        images.append(image)
    return min(images)


def child_slot_orbits(permutations: tuple[tuple[int, ...], ...]) -> list[list[int]]:
    unused = set(range(CHILD_COUNT))
    orbits: list[list[int]] = []
    while unused:
        seed = min(unused)
        orbit = sorted({permutation[seed] for permutation in permutations})
        orbits.append(orbit)
        unused -= set(orbit)
    return orbits


def pair_class_counts(children: tuple[Cell, ...]) -> tuple[int, int, int]:
    outward_faces = outgoing_root_faces()
    same_face_pairs = 0
    cross_face_coupled_pairs = 0
    disjoint_pairs = 0
    face_sets = [set(cell_faces(child)) for child in children]

    for left, right in combinations(range(len(children)), 2):
        touched_left = {index for index, face in enumerate(outward_faces) if face in face_sets[left]}
        touched_right = {index for index, face in enumerate(outward_faces) if face in face_sets[right]}
        shared_faces = face_sets[left].intersection(face_sets[right])
        if len(touched_left.union(touched_right)) == 1:
            same_face_pairs += 1
        elif shared_faces:
            cross_face_coupled_pairs += 1
        else:
            disjoint_pairs += 1

    return same_face_pairs, cross_face_coupled_pairs, disjoint_pairs


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    root = root_cell()
    q = root_face()
    outward_faces = outgoing_root_faces()
    children = outgoing_child_cells()
    permutations = stabilizer_permutations(children)
    slot_orbits = child_slot_orbits(permutations)

    raw_subset_count = 1 << len(children)
    seen_reps: set[int] = set()
    orbit_by_child_count: Counter[int] = Counter()
    orbit_by_outgoing_faces: Counter[int] = Counter()
    orbit_by_pair: Counter[tuple[int, int]] = Counter()

    for mask in range(raw_subset_count):
        rep = orbit_rep(mask, permutations)
        if rep in seen_reps:
            continue
        seen_reps.add(rep)
        child_count = rep.bit_count()
        outgoing = outgoing_face_count(rep, children)
        orbit_by_child_count[child_count] += 1
        orbit_by_outgoing_faces[outgoing] += 1
        orbit_by_pair[(child_count, outgoing)] += 1

    same_face_pairs, cross_face_coupled_pairs, disjoint_pairs = pair_class_counts(children)

    print("=" * 78)
    print("EXACT LOCAL DIRECTED-CELL BOUNDARY-CLUSTER THEOREM ON THE 3+1 LATTICE")
    print("=" * 78)
    print()
    print(f"Incoming face q              = {q}")
    print(f"Directed root cell           = {root}")
    print(f"Outward root faces           = {len(outward_faces)}")
    print(f"Outward child cells          = {len(children)}")
    print(f"Raw local child subsets      = {raw_subset_count}")
    print(f"Stabilizer size              = {len(permutations)}")
    print(f"Orbit state count            = {len(seen_reps)}")
    print()
    print("Child-slot orbit structure under the directed stabilizer")
    for orbit in slot_orbits:
        print(f"  orbit size {len(orbit)}: {orbit}")
    print()
    print("Orbit counts by child count")
    print(f"  {dict(sorted(orbit_by_child_count.items()))}")
    print()
    print("Orbit counts by outgoing frontier-face count")
    print(f"  {dict(sorted(orbit_by_outgoing_faces.items()))}")
    print()
    print("Selected exact local classes (child count, outgoing frontier faces)")
    selected = {key: value for key, value in sorted(orbit_by_pair.items()) if key[0] <= 4}
    print(f"  {selected}")
    print()
    print("Exact local pair classes among the 15 child cells")
    print(f"  same outward face                      = {same_face_pairs}")
    print(f"  distinct outward faces but edge-coupled = {cross_face_coupled_pairs}")
    print(f"  distinct outward faces and disjoint     = {disjoint_pairs}")
    print()

    checks = [
        check_equal("directed root has 5 outward faces", len(outward_faces), 5),
        check_equal("directed root has 15 outward child cells", len(children), 15),
        check_equal("raw local subset count", raw_subset_count, 32768),
        check_equal("directed-cell stabilizer size", len(permutations), 16),
        check_equal("child-slot orbit sizes", sorted(len(orbit) for orbit in slot_orbits), [1, 2, 4, 8]),
        check_equal("local orbit-state count", len(seen_reps), 2844),
        check_equal("same-face child pairs", same_face_pairs, 15),
        check_equal("cross-face but edge-coupled child pairs", cross_face_coupled_pairs, 16),
        check_equal("cross-face disjoint child pairs", disjoint_pairs, 74),
        check_equal("empty local subset leaves 5 outgoing faces", outgoing_face_count(0, children), 5),
        check_equal("empty local subset has zero shared plaquette faces", shared_face_count(0, children), 0),
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

    print("Conclusion: the directed local boundary problem is finite and exact,")
    print("but it is already locally coupled and not a product over outward faces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
