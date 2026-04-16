#!/usr/bin/env python3
"""
Common exact geometry for the 3+1 plaquette surface program.

This module keeps the rooted 3-chain / 4-cube combinatorics in one place so the
quotient theorem, quotient engine, and later surface-gas notes all use the same
exact cubical data.

Self-contained: standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


DIMS = 4

Cell = tuple[tuple[int, int, int, int], tuple[int, int, int]]
Plaquette = tuple[tuple[int, int, int, int], tuple[int, int]]
Hypercube = tuple[int, int, int, int]


@dataclass(frozen=True)
class BasisVector:
    pivot: Cell
    rows: frozenset[Cell]
    hypercubes: frozenset[Hypercube]


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


def boundary_faces(cells: frozenset[Cell] | tuple[Cell, ...] | set[Cell]) -> frozenset[Plaquette]:
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


def root_incident_cells() -> tuple[Cell, ...]:
    return cells_incident_to_face(root_face())


def root_incidence(cells: frozenset[Cell] | tuple[Cell, ...] | set[Cell]) -> int:
    return len(set(root_incident_cells()).intersection(cells))


def rooted_levels(max_cells: int) -> dict[int, set[frozenset[Cell]]]:
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


def omitted_axis(cell: Cell) -> int:
    axes = set(cell[1])
    for axis in range(DIMS):
        if axis not in axes:
            return axis
    raise ValueError(f"invalid 3-cell axes: {cell}")


def hypercubes_incident_to_cell(cell: Cell) -> tuple[Hypercube, ...]:
    anchor, _axes = cell
    missing = omitted_axis(cell)
    cubes: list[Hypercube] = []
    for shift in (0, -1):
        origin = list(anchor)
        origin[missing] += shift
        cubes.append(tuple(origin))
    return tuple(cubes)


def hypercube_boundary_cells(origin: Hypercube) -> frozenset[Cell]:
    boundary: set[Cell] = set()
    for omitted_axis in range(DIMS):
        axes = tuple(axis for axis in range(DIMS) if axis != omitted_axis)
        boundary.add((origin, axes))
        shifted = list(origin)
        shifted[omitted_axis] += 1
        boundary.add((tuple(shifted), axes))
    return frozenset(boundary)


def support_box(cells: frozenset[Cell] | tuple[Cell, ...] | set[Cell], pad: int = 0) -> tuple[tuple[int, int], ...]:
    anchors = [cell[0] for cell in cells]
    bounds: list[tuple[int, int]] = []
    for axis in range(DIMS):
        lo = min(anchor[axis] for anchor in anchors) - 1 - pad
        hi = max(anchor[axis] for anchor in anchors) + pad
        bounds.append((lo, hi))
    return tuple(bounds)


def hypercubes_in_box(bounds: tuple[tuple[int, int], ...]) -> tuple[Hypercube, ...]:
    ranges = [range(lo, hi + 1) for lo, hi in bounds]
    return tuple(product(*ranges))


def canonical_surface_key(cells: frozenset[Cell] | tuple[Cell, ...] | set[Cell]) -> tuple[Plaquette, ...]:
    return tuple(sorted(boundary_faces(cells)))


def reduce_rows_against_basis(
    rows: set[Cell],
    witness: set[Hypercube],
    basis: dict[Cell, BasisVector],
) -> tuple[set[Cell], set[Hypercube]]:
    while rows:
        pivot = max(rows)
        vector = basis.get(pivot)
        if vector is None:
            break
        rows.symmetric_difference_update(vector.rows)
        witness.symmetric_difference_update(vector.hypercubes)
    return rows, witness


def build_boundary_basis(hypercubes: tuple[Hypercube, ...]) -> dict[Cell, BasisVector]:
    basis: dict[Cell, BasisVector] = {}
    for cube in sorted(hypercubes):
        rows = set(hypercube_boundary_cells(cube))
        witness = {cube}
        rows, witness = reduce_rows_against_basis(rows, witness, basis)
        if not rows:
            continue
        pivot = max(rows)
        basis[pivot] = BasisVector(pivot, frozenset(rows), frozenset(witness))
    return basis


def closed_chain_fill_witness(
    cells: frozenset[Cell] | tuple[Cell, ...] | set[Cell],
    max_pad: int = 2,
) -> tuple[frozenset[Hypercube], int]:
    target = frozenset(cells)
    if not target:
        return frozenset(), 0
    if boundary_faces(target):
        raise ValueError("target 3-chain is not closed")
    for pad in range(max_pad + 1):
        basis = build_boundary_basis(hypercubes_in_box(support_box(target, pad)))
        remainder, witness = reduce_rows_against_basis(set(target), set(), basis)
        if not remainder:
            return frozenset(witness), pad
    raise RuntimeError("closed chain was not filled inside the tested support boxes")


def same_boundary_witness(
    left: frozenset[Cell] | tuple[Cell, ...] | set[Cell],
    right: frozenset[Cell] | tuple[Cell, ...] | set[Cell],
    max_pad: int = 2,
) -> tuple[frozenset[Hypercube], int]:
    if canonical_surface_key(left) != canonical_surface_key(right):
        raise ValueError("3-chains do not have the same plaquette boundary")
    return closed_chain_fill_witness(frozenset(left).symmetric_difference(right), max_pad=max_pad)


def box_cells(shape: tuple[int, int, int, int]) -> tuple[Cell, ...]:
    cubes = [tuple(index) for index in product(*(range(length) for length in shape))]
    cells: set[Cell] = set()
    for cube in cubes:
        cells.update(hypercube_boundary_cells(cube))
    return tuple(sorted(cells))
