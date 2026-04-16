#!/usr/bin/env python3
"""
Exact propagated two-shell theorem for the first hidden quotient sector.

Start from the exact n = 5 hidden quotient sector proved in
frontier_hidden_shell_channel_theorem.py. Extend every representative by one
root-preserving 3-cell and group the resulting n = 6 fillings by quotient
surface key.

This tests the next honest closure question:

  does the first hidden sector stay local under one more rooted extension?

The answer is yes, but not in the naive 12-state sense. The propagated hidden
sector is still a local unit-4-cube defect, but it has grown from a one-cell
shell to a two-cell shell.

Self-contained except for the exact rooted n = 5 hidden-sector theorem.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from frontier_hidden_shell_channel_theorem import duplicate_groups
from plaquette_surface_common import (
    Cell,
    boundary_faces,
    canonical_surface_key,
    cell_faces,
    cells_incident_to_face,
    hypercubes_incident_to_cell,
    hypercube_boundary_cells,
    root_face,
)


def rooted_children(cells: frozenset[Cell]) -> tuple[frozenset[Cell], ...]:
    q = root_face()
    adjacent: set[Cell] = set()
    for occupied in cells:
        for face in cell_faces(occupied):
            for candidate in cells_incident_to_face(face):
                if candidate in cells:
                    continue
                adjacent.add(candidate)

    children: list[frozenset[Cell]] = []
    for candidate in adjacent:
        child = frozenset((*cells, candidate))
        if q in boundary_faces(child):
            children.append(child)
    return tuple(children)


def hidden_image_groups() -> dict[tuple[object, ...], set[frozenset[Cell]]]:
    groups: dict[tuple[object, ...], set[frozenset[Cell]]] = defaultdict(set)
    for left, right in duplicate_groups(5):
        for cells in (left, right):
            for child in rooted_children(cells):
                groups[canonical_surface_key(child)].add(child)
    return groups


def witness_origin_from_difference(diff: frozenset[Cell]) -> tuple[int, int, int, int] | None:
    for seed in diff:
        for origin in hypercubes_incident_to_cell(seed):
            if hypercube_boundary_cells(origin) == diff:
                return origin
    return None


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    groups = hidden_image_groups()
    multiplicity_hist = Counter(len(families) for families in groups.values())
    duplicates = [tuple(families) for families in groups.values() if len(families) == 2]

    diff_size_hist: Counter[int] = Counter()
    witness_count = 0
    shared_outside_hist: Counter[int] = Counter()
    sample_pair: tuple[frozenset[Cell], frozenset[Cell]] | None = None
    sample_origin: tuple[int, int, int, int] | None = None

    for left, right in duplicates:
        diff = frozenset(left ^ right)
        diff_size_hist[len(diff)] += 1
        origin = witness_origin_from_difference(diff)
        if origin is None:
            continue

        witness_count += 1
        witness = hypercube_boundary_cells(origin)
        outside_left = frozenset(left - witness)
        outside_right = frozenset(right - witness)
        if outside_left != outside_right:
            raise RuntimeError("propagated duplicate pair does not share the same exterior shell")
        shared_outside_hist[len(outside_left)] += 1

        if sample_pair is None:
            sample_pair = (left, right)
            sample_origin = origin

    print("=" * 78)
    print("EXACT PROPAGATED TWO-SHELL THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print("One-step image of the n = 5 hidden quotient sector")
    print(f"  quotient classes in the image        = {len(groups)}")
    print(f"  quotient multiplicity histogram      = {dict(sorted(multiplicity_hist.items()))}")
    print(f"  duplicate quotient classes           = {len(duplicates)}")
    print()
    print("Duplicate-pair geometry")
    print(f"  symmetric-difference size histogram  = {dict(sorted(diff_size_hist.items()))}")
    print(f"  classes with unit 4-cube witness     = {witness_count}")
    print(f"  shared exterior-cell histogram       = {dict(sorted(shared_outside_hist.items()))}")
    print()
    if sample_pair is not None and sample_origin is not None:
        print("Sample propagated duplicate pair")
        print(f"  witness cube origin                  = {sample_origin}")
        print(f"  left                                 = {tuple(sorted(sample_pair[0]))}")
        print(f"  right                                = {tuple(sorted(sample_pair[1]))}")
        print()

    checks = [
        check_equal("image quotient class count", len(groups), 140224),
        check_equal("image multiplicity histogram", dict(sorted(multiplicity_hist.items())), {1: 58944, 2: 81280}),
        check_equal("duplicate quotient class count", len(duplicates), 81280),
        check_equal("duplicate symmetric-difference size histogram", dict(sorted(diff_size_hist.items())), {8: 81280}),
        check_equal("every duplicate pair has a unit 4-cube witness", witness_count, 81280),
        check_equal("every duplicate pair is a two-shell defect", dict(sorted(shared_outside_hist.items())), {2: 81280}),
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

    print("Conclusion: the first propagated hidden quotient layer stays local. Every")
    print("duplicate class in the one-step image is again a single unit 4-cube defect,")
    print("but the hidden shell has grown from one shared exterior 3-cell to two.")
    print("So the 12-state one-shell alphabet is not a closed final transfer state; it")
    print("lifts to an exact two-shell sector under one more rooted extension.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
