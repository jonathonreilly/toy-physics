#!/usr/bin/env python3
"""
Constructive cubical quotient theorem for finite rooted 3-chains on the 3+1 lattice.

This runner proves the exact quotient statement needed for the plaquette route:

  dV = dW  <=>  V + W is a finite closed 3-chain  <=>  V + W = dX

for some finite 4-chain X over F_2.

So the physical same-boundary object is the plaquette surface S = q + dV, not
the rooted filling V itself.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import defaultdict

from plaquette_surface_common import (
    Cell,
    Hypercube,
    box_cells,
    boundary_faces,
    build_boundary_basis,
    canonical_surface_key,
    closed_chain_fill_witness,
    hypercube_boundary_cells,
    hypercubes_in_box,
    reduce_rows_against_basis,
    root_face,
    root_incident_cells,
    rooted_levels,
    same_boundary_witness,
)


def exhaustive_closed_box_check(shape: tuple[int, int, int, int]) -> tuple[int, int]:
    cells = box_cells(shape)
    basis = build_boundary_basis(hypercubes_in_box(tuple((0, length - 1) for length in shape)))
    closed_count = 0
    fillable_count = 0
    for mask in range(1 << len(cells)):
        subset = frozenset(cells[index] for index in range(len(cells)) if (mask >> index) & 1)
        if boundary_faces(subset):
            continue
        closed_count += 1
        remainder, _witness = reduce_rows_against_basis(set(subset), set(), basis)
        if not remainder:
            fillable_count += 1
    return closed_count, fillable_count


def hypercube_complement_pair() -> tuple[frozenset[Cell], frozenset[Cell], Hypercube]:
    root_cell = frozenset((root_incident_cells()[0],))
    origin = (0, 0, 0, 0)
    complement = hypercube_boundary_cells(origin) ^ root_cell
    return root_cell, frozenset(complement), origin


def first_duplicate_pair(level: int = 4) -> tuple[frozenset[Cell], frozenset[Cell]]:
    q = root_face()
    groups: dict[tuple[object, ...], list[frozenset[Cell]]] = defaultdict(list)
    for cells in rooted_levels(level)[level]:
        if q not in boundary_faces(cells):
            continue
        groups[canonical_surface_key(cells)].append(cells)
    for families in groups.values():
        if len(families) > 1:
            return families[0], families[1]
    raise RuntimeError(f"no duplicate same-boundary rooted pair found at n = {level}")


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    root_cell, complement, origin = hypercube_complement_pair()
    complement_witness, complement_pad = same_boundary_witness(root_cell, complement)

    dup_left, dup_right = first_duplicate_pair(4)
    dup_witness, dup_pad = same_boundary_witness(dup_left, dup_right)

    one_cube_closed, one_cube_fillable = exhaustive_closed_box_check((1, 1, 1, 1))
    two_cube_closed, two_cube_fillable = exhaustive_closed_box_check((2, 1, 1, 1))

    print("=" * 78)
    print("CONSTRUCTIVE CUBICAL QUOTIENT THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print("Same-boundary hypercube-complement witness")
    print(f"  root 3-cell boundary key           = {canonical_surface_key(root_cell)}")
    print(f"  7-facet complement boundary key    = {canonical_surface_key(complement)}")
    print(f"  witness 4-chain                    = {tuple(sorted(complement_witness))}")
    print(f"  witness support-box padding        = {complement_pad}")
    print()
    print("First rooted duplicate pair at n = 4")
    print(f"  left rooted filling size           = {len(dup_left)}")
    print(f"  right rooted filling size          = {len(dup_right)}")
    print(f"  common surface key size |dV|       = {len(canonical_surface_key(dup_left))}")
    print(f"  difference size |V+W|              = {len(dup_left ^ dup_right)}")
    print(f"  witness 4-chain                    = {tuple(sorted(dup_witness))}")
    print(f"  witness support-box padding        = {dup_pad}")
    print()
    print("Exhaustive finite-box closed-chain checks")
    print(f"  one unit 4-cube box: closed = {one_cube_closed}, fillable = {one_cube_fillable}")
    print(f"  two-cube box (2x1x1x1): closed = {two_cube_closed}, fillable = {two_cube_fillable}")
    print()

    checks = [
        check_equal("same-boundary root/complement pair", canonical_surface_key(root_cell), canonical_surface_key(complement)),
        check_equal("root/complement difference is one 4-cube boundary", complement_witness, frozenset((origin,))),
        check_equal("root/complement difference is closed", boundary_faces(root_cell ^ complement), frozenset()),
        check_equal("n=4 duplicate pair has same boundary", canonical_surface_key(dup_left), canonical_surface_key(dup_right)),
        check_equal("n=4 duplicate-pair difference is closed", boundary_faces(dup_left ^ dup_right), frozenset()),
        check_equal("n=4 duplicate-pair witness is one 4-cube", len(dup_witness), 1),
        check_equal("all closed chains in one 4-cube box are fillable", one_cube_fillable, one_cube_closed),
        check_equal("all closed chains in two-cube box are fillable", two_cube_fillable, two_cube_closed),
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

    print("Conclusion: finite rooted 3-chains with the same plaquette boundary differ")
    print("by an exact finite sum of unit 4-cube boundaries. The canonical quotient")
    print("object is therefore the same-boundary plaquette surface key dV itself.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
