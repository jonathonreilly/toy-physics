#!/usr/bin/env python3
"""
Exact hidden-shell channel theorem for the n=5 quotient duplicate sector.

This runner turns the first hidden-filling obstruction into a finite local
state alphabet. Every quotient duplicate class at rooted size n = 5 is:

  one unit 4-cube boundary + one shared exterior 3-cell

and under the full symmetry group of the unit 4-cube that local shell reduces
to a finite set of exact channels.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations, product

from plaquette_surface_common import (
    Cell,
    boundary_faces,
    canonical_surface_key,
    cell_faces,
    cells_incident_to_face,
    hypercube_boundary_cells,
    hypercubes_incident_to_cell,
    root_face,
    rooted_levels,
)


DIMS = 4
MAX_CELLS = 5


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


def next_quotient_count(cells: frozenset[Cell]) -> int:
    return sum(multiplicity for _faces, multiplicity in next_quotient_histogram(cells))


def next_quotient_histogram(cells: frozenset[Cell]) -> tuple[tuple[int, int], ...]:
    q = root_face()
    keys: set[tuple[object, ...]] = set()
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
            keys.add(canonical_surface_key(new_cells))
    histogram = Counter(len(key) for key in keys)
    return tuple(sorted(histogram.items()))


CUBE_SYMMETRIES = tuple(
    (perm, flips)
    for perm in permutations(range(DIMS))
    for flips in product((False, True), repeat=DIMS)
)


def transform_point(point: tuple[int, int, int, int], perm: tuple[int, ...], flips: tuple[bool, ...]) -> tuple[int, int, int, int]:
    image = [0, 0, 0, 0]
    for axis in range(DIMS):
        value = point[axis]
        if flips[axis]:
            value = 1 - value
        image[perm[axis]] = value
    return tuple(image)


def transform_cells_local(
    cells: frozenset[Cell] | tuple[Cell, ...],
    origin: tuple[int, int, int, int],
    perm: tuple[int, ...],
    flips: tuple[bool, ...],
) -> tuple[Cell, ...]:
    transformed: list[Cell] = []
    for cell in cells:
        vertices: set[tuple[int, int, int, int]] = set()
        for vertex in cell_vertices(cell):
            relative = tuple(vertex[axis] - origin[axis] for axis in range(DIMS))
            vertices.add(transform_point(relative, perm, flips))
        transformed.append(canonical_cell_from_vertices(frozenset(vertices)))
    return tuple(sorted(transformed))


def canonical_unordered_local_pair(
    left: frozenset[Cell],
    right: frozenset[Cell],
    origin: tuple[int, int, int, int],
) -> tuple[tuple[Cell, ...], tuple[Cell, ...]]:
    best: tuple[tuple[Cell, ...], tuple[Cell, ...]] | None = None
    for perm, flips in CUBE_SYMMETRIES:
        transformed_left = transform_cells_local(left, origin, perm, flips)
        transformed_right = transform_cells_local(right, origin, perm, flips)
        candidate = min((transformed_left, transformed_right), (transformed_right, transformed_left))
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise RuntimeError("failed to canonicalize unordered local pair")
    return best


def canonical_ordered_local_shell(
    cells: frozenset[Cell],
    origin: tuple[int, int, int, int],
) -> tuple[Cell, ...]:
    best: tuple[Cell, ...] | None = None
    for perm, flips in CUBE_SYMMETRIES:
        transformed = transform_cells_local(cells, origin, perm, flips)
        if best is None or transformed < best:
            best = transformed
    if best is None:
        raise RuntimeError("failed to canonicalize ordered local shell")
    return best


def duplicate_groups(level: int) -> list[tuple[frozenset[Cell], frozenset[Cell]]]:
    q = root_face()
    groups: dict[tuple[object, ...], list[frozenset[Cell]]] = defaultdict(list)
    for cells in rooted_levels(MAX_CELLS)[level]:
        if q in boundary_faces(cells):
            groups[canonical_surface_key(cells)].append(cells)
    return [tuple(families) for families in groups.values() if len(families) == 2]


def witness_origin_from_difference(left: frozenset[Cell], right: frozenset[Cell]) -> tuple[int, int, int, int]:
    diff = left ^ right
    seed = next(iter(diff))
    for origin in hypercubes_incident_to_cell(seed):
        if hypercube_boundary_cells(origin) == diff:
            return origin
    raise RuntimeError("expected duplicate difference to be exactly one unit 4-cube boundary")


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    duplicates = duplicate_groups(5)

    unordered_orbit_hist: Counter[tuple[tuple[Cell, ...], tuple[Cell, ...]]] = Counter()
    unordered_counts: dict[tuple[tuple[Cell, ...], tuple[Cell, ...]], tuple[int, int]] = {}

    ordered_orbit_hist: Counter[tuple[Cell, ...]] = Counter()
    ordered_counts: dict[tuple[Cell, ...], int] = {}
    ordered_histograms: dict[tuple[Cell, ...], tuple[tuple[int, int], ...]] = {}

    for left, right in duplicates:
        origin = witness_origin_from_difference(left, right)
        unordered = canonical_unordered_local_pair(left, right, origin)
        counts = tuple(sorted((next_quotient_count(left), next_quotient_count(right))))
        unordered_orbit_hist[unordered] += 1
        unordered_counts[unordered] = counts

        for cells in (left, right):
            ordered = canonical_ordered_local_shell(cells, origin)
            ordered_orbit_hist[ordered] += 1
            ordered_histograms[ordered] = next_quotient_histogram(cells)
            ordered_counts[ordered] = sum(multiplicity for _faces, multiplicity in ordered_histograms[ordered])

    unordered_channel_hist: Counter[tuple[int, int]] = Counter()
    for orbit, multiplicity in unordered_orbit_hist.items():
        unordered_channel_hist[unordered_counts[orbit]] += multiplicity

    print("=" * 78)
    print("EXACT HIDDEN-SHELL CHANNEL THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print(f"n = 5 duplicate quotient classes      = {len(duplicates)}")
    print(f"unordered local shell orbits          = {len(unordered_orbit_hist)}")
    print(f"ordered local shell orbits            = {len(ordered_orbit_hist)}")
    print()
    print("Unordered hidden-shell channel histogram")
    for counts, multiplicity in sorted(unordered_channel_hist.items()):
        print(f"  counts {counts}: multiplicity {multiplicity}")
    print()
    print("Ordered shell count histogram")
    ordered_count_hist = Counter(ordered_counts.values())
    for count, multiplicity in sorted(ordered_count_hist.items()):
        print(f"  next quotient count {count}: orbit multiplicity {multiplicity}")
    print()
    print("Ordered shell |dV| transfer histograms")
    for index, (orbit, multiplicity) in enumerate(ordered_orbit_hist.most_common()):
        print(
            f"  orbit {index}: multiplicity {multiplicity}, next count {ordered_counts[orbit]}, "
            f"histogram {dict(ordered_histograms[orbit])}"
        )
    print()
    print("Canonical unordered shell orbits")
    for index, (orbit, multiplicity) in enumerate(unordered_orbit_hist.most_common()):
        print(f"  orbit {index}: multiplicity {multiplicity}, counts {unordered_counts[orbit]}")
        print(f"    A = {orbit[0]}")
        print(f"    B = {orbit[1]}")
    print()
    print("Canonical ordered shell orbits")
    for index, (orbit, multiplicity) in enumerate(ordered_orbit_hist.most_common()):
        print(f"  orbit {index}: multiplicity {multiplicity}, next count {ordered_counts[orbit]}")
        print(f"    {orbit}")
    print()

    checks = [
        check_equal("n=5 duplicate quotient class count", len(duplicates), 2848),
        check_equal("unordered local shell orbit count", len(unordered_orbit_hist), 6),
        check_equal("ordered local shell orbit count", len(ordered_orbit_hist), 12),
        check_equal(
            "unordered hidden-shell channel histogram",
            dict(sorted(unordered_channel_hist.items())),
            {(47, 49): 512, (49, 50): 576, (49, 51): 864, (49, 52): 576, (51, 53): 320},
        ),
        check_equal(
            "ordered shell orbit multiplicities",
            dict(sorted(Counter(ordered_orbit_hist.values()).items())),
            {288: 2, 320: 2, 512: 2, 576: 6},
        ),
        check_equal(
            "ordered shell next-count orbit histogram",
            dict(sorted(ordered_count_hist.items())),
            {47: 1, 49: 5, 50: 1, 51: 3, 52: 1, 53: 1},
        ),
        check_equal(
            "ordered shell transfer histogram count",
            len({ordered_histograms[orbit] for orbit in ordered_orbit_hist}),
            12,
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

    print("Conclusion: the first hidden quotient sector does not require an amorphous")
    print("memory term. At n = 5 it reduces exactly to a finite local cube-shell")
    print("alphabet: 6 unordered channels or 12 ordered channels under unit 4-cube symmetry.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
