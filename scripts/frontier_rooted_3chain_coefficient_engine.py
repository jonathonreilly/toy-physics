#!/usr/bin/env python3
"""
Exact rooted 3-chain coefficient engine for the 3+1 plaquette program.

This runner pushes the pure-gauge open-surface program one exact layer beyond
the first nonlocal connected coefficient. It enumerates connected rooted
3-chains V with q in dV through five 3-cells and tabulates the exact same-
boundary counts by boundary-face number F = |dV|.

Important correction:
  connected 3-chains are not all boundary-shellable. A cell can attach across
  a plaquette face that is temporarily internal and only later returns to the
  boundary. So exact rooted enumeration must grow by any shared plaquette face,
  not only current boundary faces.

It also proves the next local-closure obstruction:

  a directed-cell closure that factorizes the 15 outward child slots of a root
  cell predicts only F = 14 at n = 3 and gives count 1320,

while the exact rooted 3-chain data on the 3+1 lattice gives

  F = 14 count 1036,
  F = 12 count 64,
  F = 16 count 64,

with an exact k = 3 root-launch sector already present at n = 3.

So the next viable closure must retain local edge-coupled child motifs on a
directed cell. Face-slot factorization is already dead at n = 3.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
DIMS = 4
MAX_CELLS = 5
LOCAL_PLAQUETTE_AT_BETA6 = 0.422531739649983


Cell = tuple[tuple[int, int, int, int], tuple[int, int, int]]
Plaquette = tuple[tuple[int, int, int, int], tuple[int, int]]


@dataclass(frozen=True)
class RootedStats:
    total_count: int
    by_boundary_faces: dict[int, int]
    by_root_incidence: dict[int, int]


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


def rooted_stats(levels: dict[int, set[frozenset[Cell]]]) -> dict[int, RootedStats]:
    q = root_face()
    incident = set(root_incident_cells())
    stats: dict[int, RootedStats] = {}
    for count, families in levels.items():
        by_faces: Counter[int] = Counter()
        by_root_incidence: Counter[int] = Counter()
        total = 0
        for cells in families:
            boundary = boundary_faces(cells)
            if q not in boundary:
                continue
            total += 1
            by_faces[len(boundary)] += 1
            by_root_incidence[len(incident.intersection(cells))] += 1
        stats[count] = RootedStats(
            total_count=total,
            by_boundary_faces=dict(sorted(by_faces.items())),
            by_root_incidence=dict(sorted(by_root_incidence.items())),
        )
    return stats


def exact_partial_dressing_polynomial(stats: dict[int, RootedStats]) -> dict[int, int]:
    """
    Return H_partial(p) = 1 + sum coeff_k p^k through MAX_CELLS,
    where P = p * H and p is the exact local one-plaquette block.
    """
    polynomial: Counter[int] = Counter()
    for rooted in stats.values():
        for boundary_count, multiplicity in rooted.by_boundary_faces.items():
            polynomial[boundary_count - 2] += multiplicity
    return dict(sorted(polynomial.items()))


def evaluate_partial_dressing(polynomial: dict[int, int], p: float) -> float:
    return 1.0 + sum(coeff * (p ** power) for power, coeff in polynomial.items())


def naive_factorized_n3_prediction() -> dict[int, int]:
    """
    Directed-cell face-factorized closure at n = 3:

    - choose 1 of the 4 root cells
    - either add 2 outward child slots on that same root cell: C(15, 2)
    - or add 1 outward child slot and then 1 outward grandchild slot: 15 * 15

    This predicts only the tree-like F = 14 sector and no F = 12 sector.
    """
    per_root = 15 * 15 + (15 * 14) // 2
    return {14: 4 * per_root, 12: 0}


def format_polynomial(polynomial: dict[int, int]) -> str:
    pieces = [f"{coeff} p^{power}" for power, coeff in polynomial.items()]
    return "1 + " + " + ".join(pieces)


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    levels = rooted_levels(MAX_CELLS)
    stats = rooted_stats(levels)
    polynomial = exact_partial_dressing_polynomial(stats)
    p_local = LOCAL_PLAQUETTE_AT_BETA6
    h_partial = evaluate_partial_dressing(polynomial, p_local)
    p_partial = p_local * h_partial

    print("=" * 78)
    print("EXACT ROOTED 3-CHAIN COEFFICIENT ENGINE ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()

    print("Exact rooted counts with q in dV")
    for count in range(1, MAX_CELLS + 1):
        rooted = stats[count]
        print(f"  n = {count}: total = {rooted.total_count}")
        print(f"    by |dV|: {rooted.by_boundary_faces}")
        print(f"    by root-incidence: {rooted.by_root_incidence}")
    print()

    print("Exact local-resummed partial dressing through n = 5")
    print(f"  H_partial(p) = {format_polynomial(polynomial)}")
    print(f"  with p = P_1plaq(6) = {p_local:.15f}")
    print(f"  H_partial(P_1plaq(6)) = {h_partial:.15f}")
    print(f"  P_partial^(n<=5)(6)   = {p_partial:.15f}")
    print()

    print("Directed-cell face-factorization no-go at n = 3")
    naive = naive_factorized_n3_prediction()
    exact_n3 = stats[3].by_boundary_faces
    print(f"  naive factorized prediction = {naive}")
    print(f"  exact rooted data          = {exact_n3}")
    print()

    checks = [
        check_equal("n=1 rooted count", stats[1].total_count, 4),
        check_equal("n=2 rooted count", stats[2].total_count, 60),
        check_equal("n=3 rooted count", stats[3].total_count, 1164),
        check_equal("n=4 rooted count", stats[4].total_count, 25000),
        check_equal("n=5 rooted count", stats[5].total_count, 566644),
        check_equal("n=3 by |dV|", stats[3].by_boundary_faces, {12: 64, 14: 1036, 16: 64}),
        check_equal("n=3 root-incidence split", stats[3].by_root_incidence, {1: 1160, 3: 4}),
        check_equal("n=4 root-incidence split", stats[4].by_root_incidence, {1: 24852, 3: 148}),
        check_equal("n=5 root-incidence split", stats[5].by_root_incidence, {1: 562352, 3: 4292}),
        check_equal("factorized closure predicts no F=12 sector at n=3", naive[12], 0),
        check_equal("exact rooted engine gives nonzero F=12 sector at n=3", exact_n3[12], 64),
        check_equal("exact rooted engine gives nonzero F=16 sector at n=3", exact_n3[16], 64),
        check_equal("factorized closure overcounts F=14 at n=3", naive[14], 1320),
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

    print("Conclusion: the corrected rooted 3-chain engine is exact through five 3-cells,")
    print("boundary-shellable growth is false, and directed-cell face-slot factorization is already false at n = 3.")
    print("The next viable closure must retain local edge-coupled child motifs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
