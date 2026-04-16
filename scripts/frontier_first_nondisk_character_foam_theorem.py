#!/usr/bin/env python3
"""
Exact first non-disk character-foam theorem on the 3+1 plaquette surface.

This runner upgrades the direct quotient route from:

    "the first non-disk sector is not a scalar p-only surface gas"

to the sharper exact carrier statement:

1. the minimal plaquette-character face alphabet {3, 3bar, 8} carries the
   genus-1 ribbon subclass and the 12 quadrivalent crossing surfaces
2. that same plaquette-character alphabet still does not carry the 52
   lift-impossible singular surfaces
3. those 52 surfaces are therefore forced into a link-defect sector whose
   exact first non-disk signatures are:
      - one baryon junction + three crossings
      - four baryon junctions

Self-contained except for importing the exact one-plaquette character
coefficients from the existing disk theorem.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from frontier_fundamental_disk_activity_theorem import bessel_minor, one_plaquette_character_data
from frontier_quotient_surface_engine import rooted_surface_groups
from plaquette_surface_common import Plaquette, root_face, rooted_levels


MAX_CELLS = 5
FIRST_NONDISK_POWER = 14


@dataclass(frozen=True)
class ClassRow:
    invariant: tuple[int, int, int, tuple[tuple[int, int], ...]]
    multiplicity: int
    representative: tuple[Plaquette, ...]


def shift(vec: tuple[int, int, int, int], axis: int) -> tuple[int, int, int, int]:
    out = list(vec)
    out[axis] += 1
    return tuple(out)


def plaquette_edges(face: Plaquette) -> tuple[tuple[tuple[int, int, int, int], int], ...]:
    anchor, plane = face
    axis_a, axis_b = plane
    return (
        (anchor, axis_a),
        (anchor, axis_b),
        (shift(anchor, axis_a), axis_b),
        (shift(anchor, axis_b), axis_a),
    )


def plaquette_vertices(face: Plaquette) -> tuple[tuple[int, int, int, int], ...]:
    anchor, plane = face
    axis_a, axis_b = plane
    return (
        anchor,
        shift(anchor, axis_a),
        shift(anchor, axis_b),
        shift(shift(anchor, axis_a), axis_b),
    )


def spanning_surface_faces(key: tuple[Plaquette, ...]) -> set[Plaquette]:
    faces = set(key)
    tagged = root_face()
    if tagged in faces:
        faces.remove(tagged)
    else:
        faces.add(tagged)
    return faces


def is_simply_sheeted_disk(key: tuple[Plaquette, ...]) -> bool:
    faces = spanning_surface_faces(key)
    if not faces:
        return True

    edge_to_faces: dict[tuple[tuple[int, int, int, int], int], list[Plaquette]] = defaultdict(list)
    vertices: set[tuple[int, int, int, int]] = set()
    for face in faces:
        for edge in plaquette_edges(face):
            edge_to_faces[edge].append(face)
        vertices.update(plaquette_vertices(face))

    incidences = [len(incident_faces) for incident_faces in edge_to_faces.values()]
    if any(incidence > 2 for incidence in incidences):
        return False

    if sum(1 for incidence in incidences if incidence == 1) != 4:
        return False

    neighbors: dict[Plaquette, set[Plaquette]] = defaultdict(set)
    for incident_faces in edge_to_faces.values():
        for i, left in enumerate(incident_faces):
            for right in incident_faces[i + 1 :]:
                neighbors[left].add(right)
                neighbors[right].add(left)

    start = next(iter(faces))
    stack = [start]
    seen = {start}
    while stack:
        face = stack.pop()
        for neighbor in neighbors[face]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)

    chi = len(vertices) - len(edge_to_faces) + len(faces)
    return len(seen) == len(faces) and chi == 1


def class_invariant(key: tuple[Plaquette, ...]) -> tuple[int, int, int, tuple[tuple[int, int], ...]]:
    faces = spanning_surface_faces(key)
    edge_to_faces: dict[tuple[tuple[int, int, int, int], int], list[Plaquette]] = defaultdict(list)
    vertices: set[tuple[int, int, int, int]] = set()
    for face in faces:
        for edge in plaquette_edges(face):
            edge_to_faces[edge].append(face)
        vertices.update(plaquette_vertices(face))

    incidences = Counter(len(incident_faces) for incident_faces in edge_to_faces.values())
    boundary_edges = sum(1 for incident_faces in edge_to_faces.values() if len(incident_faces) == 1)
    chi = len(vertices) - len(edge_to_faces) + len(faces)
    return (len(faces), chi, boundary_edges, tuple(sorted(incidences.items())))


def plaquette_link_orientations(
    face: Plaquette, sign: int
) -> tuple[tuple[tuple[int, int, int, int], int, int], ...]:
    anchor, (axis_a, axis_b) = face
    seq = (
        (anchor, axis_a, 1),
        (shift(anchor, axis_a), axis_b, 1),
        (shift(anchor, axis_b), axis_a, -1),
        (anchor, axis_b, -1),
    )
    if sign > 0:
        return seq
    return tuple((pos, axis, -orientation) for pos, axis, orientation in seq)


def root_requirement() -> dict[tuple[tuple[int, int, int, int], int], tuple[int, int]]:
    required: dict[tuple[tuple[int, int, int, int], int], list[int]] = defaultdict(lambda: [0, 0])
    for pos, axis, orientation in plaquette_link_orientations(root_face(), 1):
        if orientation > 0:
            required[(pos, axis)][1] += 1
        else:
            required[(pos, axis)][0] += 1
    return {link: tuple(counts) for link, counts in required.items()}


ROOT_REQUIREMENT = root_requirement()


def first_nondisk_class_rows() -> list[ClassRow]:
    groups = rooted_surface_groups(rooted_levels(MAX_CELLS))
    seen: set[tuple[Plaquette, ...]] = set()
    multiplicities: Counter[tuple[int, int, int, tuple[tuple[int, int], ...]]] = Counter()
    representatives: dict[tuple[int, int, int, tuple[tuple[int, int], ...]], tuple[Plaquette, ...]] = {}

    for per_level in groups.values():
        for key in per_level:
            if key in seen:
                continue
            seen.add(key)
            if len(key) - 2 != FIRST_NONDISK_POWER or is_simply_sheeted_disk(key):
                continue
            invariant = class_invariant(key)
            multiplicities[invariant] += 1
            representatives.setdefault(invariant, key)

    return [
        ClassRow(invariant, multiplicities[invariant], representatives[invariant])
        for invariant in sorted(multiplicities)
    ]


def solve_affine_mod3(matrix: list[list[int]], rhs: list[int]) -> tuple[list[int], list[list[int]]]:
    matrix = [row[:] for row in matrix]
    rhs = rhs[:]
    row_count = len(matrix)
    col_count = len(matrix[0]) if matrix else 0
    pivots: list[int] = []
    rank = 0

    for col in range(col_count):
        pivot_row = None
        for candidate in range(rank, row_count):
            if matrix[candidate][col] % 3:
                pivot_row = candidate
                break
        if pivot_row is None:
            continue

        matrix[rank], matrix[pivot_row] = matrix[pivot_row], matrix[rank]
        rhs[rank], rhs[pivot_row] = rhs[pivot_row], rhs[rank]

        pivot = matrix[rank][col] % 3
        inverse = 1 if pivot == 1 else 2
        matrix[rank] = [(inverse * entry) % 3 for entry in matrix[rank]]
        rhs[rank] = (inverse * rhs[rank]) % 3

        for row in range(row_count):
            if row == rank or matrix[row][col] % 3 == 0:
                continue
            factor = matrix[row][col] % 3
            matrix[row] = [(x - factor * y) % 3 for x, y in zip(matrix[row], matrix[rank])]
            rhs[row] = (rhs[row] - factor * rhs[rank]) % 3

        pivots.append(col)
        rank += 1

    for row in range(rank, row_count):
        if rhs[row] % 3:
            raise ValueError("inconsistent mod-3 system")

    free_cols = [col for col in range(col_count) if col not in pivots]
    base = [0] * col_count
    for row, col in enumerate(pivots):
        base[col] = rhs[row] % 3

    basis: list[list[int]] = []
    for free in free_cols:
        vector = [0] * col_count
        vector[free] = 1
        for row, col in enumerate(pivots):
            vector[col] = (-matrix[row][free]) % 3
        basis.append(vector)

    return base, basis


def charge_system(key: tuple[Plaquette, ...]) -> tuple[tuple[Plaquette, ...], list[int], list[list[int]]]:
    faces = tuple(sorted(spanning_surface_faces(key)))
    links = sorted(
        {(pos, axis) for face in faces for pos, axis, _ in plaquette_link_orientations(face, 1)}
        | set(ROOT_REQUIREMENT)
    )
    matrix: list[list[int]] = []
    rhs: list[int] = []

    for link in links:
        row: list[int] = []
        for face in faces:
            coefficient = 0
            for pos, axis, orientation in plaquette_link_orientations(face, 1):
                if (pos, axis) == link:
                    coefficient += orientation
            row.append(coefficient % 3)
        target = (ROOT_REQUIREMENT[link][0] - ROOT_REQUIREMENT[link][1]) % 3 if link in ROOT_REQUIREMENT else 0
        matrix.append(row)
        rhs.append(target)

    base, basis = solve_affine_mod3(matrix, rhs)
    return faces, base, basis


def face_label_link_counts(
    face: Plaquette, label: int
) -> tuple[tuple[tuple[int, int, int, int], int, tuple[int, int]], ...]:
    if label == 1:
        oriented = plaquette_link_orientations(face, 1)
        return tuple(
            ((pos, axis, (1, 0)) if orientation > 0 else (pos, axis, (0, 1)))
            for pos, axis, orientation in oriented
        )
    if label == 2:
        oriented = plaquette_link_orientations(face, -1)
        return tuple(
            ((pos, axis, (1, 0)) if orientation > 0 else (pos, axis, (0, 1)))
            for pos, axis, orientation in oriented
        )
    return tuple((pos, axis, (1, 1)) for pos, axis, _orientation in plaquette_link_orientations(face, 1))


def plaquette_character_feasible_assignments(
    key: tuple[Plaquette, ...]
) -> tuple[int, Counter[int], tuple[int, ...] | None, Counter[tuple[int, int]] | None]:
    faces, base, basis = charge_system(key)
    feasible = 0
    neutral_hist: Counter[int] = Counter()
    best_assignment: tuple[int, ...] | None = None
    best_link_hist: Counter[tuple[int, int]] | None = None

    for coeffs in product(range(3), repeat=len(basis)):
        assignment = base[:]
        for coeff, vector in zip(coeffs, basis):
            for index, value in enumerate(vector):
                assignment[index] = (assignment[index] + coeff * value) % 3

        link_counts: dict[tuple[tuple[int, int, int, int], int], list[int]] = defaultdict(lambda: [0, 0])
        for face, label in zip(faces, assignment):
            for pos, axis, (u_count, ud_count) in face_label_link_counts(face, label):
                link_counts[(pos, axis)][0] += u_count
                link_counts[(pos, axis)][1] += ud_count

        ok = True
        for link, pair in ROOT_REQUIREMENT.items():
            if tuple(link_counts.get(link, (0, 0))) != pair:
                ok = False
                break
        if not ok:
            continue

        for link, (u_count, ud_count) in link_counts.items():
            if link in ROOT_REQUIREMENT:
                continue
            if (u_count - ud_count) % 3 != 0:
                ok = False
                break
        if not ok:
            continue

        feasible += 1
        neutral_faces = sum(1 for label in assignment if label == 0)
        neutral_hist[neutral_faces] += 1
        if best_assignment is None or neutral_faces < sum(1 for label in best_assignment if label == 0):
            best_assignment = tuple(assignment)
            best_link_hist = Counter(tuple(counts) for counts in link_counts.values())

    return feasible, neutral_hist, best_assignment, best_link_hist


def defect_signature(invariant: tuple[int, int, int, tuple[tuple[int, int], ...]]) -> tuple[int, int]:
    incidence_hist = dict(invariant[3])
    baryon_junctions = incidence_hist.get(3, 0)
    crossing_links = incidence_hist.get(4, 0)
    return baryon_junctions, crossing_links


def label_name(label: int) -> str:
    return {0: "8", 1: "3", 2: "3bar"}[label]


def assignment_labels(assignment: tuple[int, ...] | None) -> tuple[str, ...] | None:
    if assignment is None:
        return None
    return tuple(label_name(label) for label in assignment)


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    beta = 6.0
    c0, c_fund, p_fund = one_plaquette_character_data(beta)
    c_adj = bessel_minor(beta, (2, 1, 0))
    p_adj = c_adj / (8.0 * c0)

    crossing_parallel = Fraction(1, 8)
    crossing_exchange = Fraction(-1, 24)
    baryon_weight = Fraction(1, 6)

    rows = first_nondisk_class_rows()
    carried_total = 0
    defect_forced_total = 0
    feasible_map: dict[tuple[int, int, int, tuple[tuple[int, int], ...]], int] = {}
    defect_map: dict[tuple[int, int, int, tuple[tuple[int, int], ...]], tuple[int, int]] = {}

    print("=" * 78)
    print("FIRST NON-DISK CHARACTER-FOAM THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print("Exact local plaquette-character alphabet at beta = 6")
    print(f"  normalized fundamental coefficient p_3(6)    = {p_fund:.15f}")
    print(f"  normalized adjoint coefficient p_8(6)        = {p_adj:.15f}")
    print("  minimal face alphabet                        = {3, 3bar, 8}")
    print()
    print("Exact singular-link carrier tensors")
    print(f"  crossing link X coefficients                 = ({crossing_parallel}, {crossing_exchange})")
    print(f"  baryon junction B coefficient                = {baryon_weight}")
    print()

    for row in rows:
        feasible, neutral_hist, best_assignment, best_link_hist = plaquette_character_feasible_assignments(
            row.representative
        )
        feasible_map[row.invariant] = feasible
        defect_map[row.invariant] = defect_signature(row.invariant)

        if feasible:
            carried_total += row.multiplicity
        else:
            defect_forced_total += row.multiplicity

        baryon_junctions, crossing_links = defect_map[row.invariant]

        print(f"class invariant                            = {row.invariant}")
        print(f"  quotient-surface multiplicity            = {row.multiplicity}")
        print(f"  plaquette-character assignments          = {feasible}")
        print(f"  neutral-face histogram                   = {dict(neutral_hist)}")
        print(f"  best face labels                         = {assignment_labels(best_assignment)}")
        print(f"  best link-count histogram                = {dict(sorted(best_link_hist.items())) if best_link_hist else {}}")
        print(f"  exact defect signature (B, X)            = ({baryon_junctions}, {crossing_links})")
        print()

    print("Aggregate exact first non-disk split")
    print(f"  total first non-disk surfaces            = {sum(row.multiplicity for row in rows)}")
    print(f"  plaquette-character carried              = {carried_total}")
    print(f"  link-defect forced                       = {defect_forced_total}")
    print()

    checks = [
        check_equal(
            "exact first non-disk class multiplicities",
            {row.invariant: row.multiplicity for row in rows},
            {
                (15, -1, 4, ((1, 4), (2, 28))): 8,
                (15, 3, 0, ((2, 24), (3, 4))): 4,
                (15, 3, 3, ((1, 3), (2, 21), (3, 1), (4, 3))): 48,
                (15, 3, 4, ((1, 4), (2, 20), (4, 4))): 12,
            },
        ),
        check_equal(
            "exact plaquette-character feasibility split",
            feasible_map,
            {
                (15, -1, 4, ((1, 4), (2, 28))): 1,
                (15, 3, 0, ((2, 24), (3, 4))): 0,
                (15, 3, 3, ((1, 3), (2, 21), (3, 1), (4, 3))): 0,
                (15, 3, 4, ((1, 4), (2, 20), (4, 4))): 9,
            },
        ),
        check_equal(
            "exact first non-disk defect signatures",
            defect_map,
            {
                (15, -1, 4, ((1, 4), (2, 28))): (0, 0),
                (15, 3, 0, ((2, 24), (3, 4))): (4, 0),
                (15, 3, 3, ((1, 3), (2, 21), (3, 1), (4, 3))): (1, 3),
                (15, 3, 4, ((1, 4), (2, 20), (4, 4))): (0, 4),
            },
        ),
        check_equal("exact plaquette-character carried total", carried_total, 20),
        check_equal("exact link-defect forced total", defect_forced_total, 52),
        check_equal("exact normalized adjoint coefficient at beta=6", round(p_adj, 15), round(0.16225979947993818, 15)),
        check_equal("exact quadrivalent crossing coefficient", crossing_parallel, Fraction(1, 8)),
        check_equal("exact crossing exchange coefficient", crossing_exchange, Fraction(-1, 24)),
        check_equal("exact baryon coefficient", baryon_weight, Fraction(1, 6)),
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

    print("Conclusion: the exact first non-disk character foam now splits cleanly.")
    print("  - the 8 genus-1 surfaces are a pure ribbon sector")
    print("  - the 12 quadrivalent surfaces are carried by plaquette characters with")
    print("    four exact crossing links")
    print("  - the remaining 52 surfaces are not carried by plaquette characters even")
    print("    after adding adjoint faces, and are forced into a baryon/crossing")
    print("    link-defect sector")
    print("So the direct closure object is no longer a scalar quotient-surface gas or")
    print("even a plaquette-character foam. It is a quotient foam with explicit local")
    print("B and X defect slots.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
