#!/usr/bin/env python3
"""
Exact Z_3 face-orientation lift theorem for the first non-disk quotient sector.

This runner isolates the first genuine non-disk / higher-sheet window on the
direct quotient-surface route: the p^14 correction in the exact unique
quotient-surface series through n <= 5.

For each exact p^14 non-disk surface class, it exhausts all 2^15 face-sign
assignments and asks whether the class admits a pure fundamental orientation
lift compatible with:

1. the tagged plaquette boundary
2. the exact SU(3) center-neutrality constraint on every internal link

The outcome is an exact no-go against a pure p-only fundamental-sheet activity
law on the full first non-disk sector.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product

from frontier_fundamental_disk_activity_theorem import (
    LOCAL_PLAQUETTE_AT_BETA6,
    is_simply_sheeted_disk,
    plaquette_edges,
    plaquette_vertices,
    spanning_surface_faces,
)
from frontier_quotient_surface_engine import rooted_surface_groups
from plaquette_surface_common import Plaquette, root_face, rooted_levels


MAX_CELLS = 5
FIRST_NONDISK_POWER = 14


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


def shift(vec: tuple[int, int, int, int], axis: int) -> tuple[int, int, int, int]:
    out = list(vec)
    out[axis] += 1
    return tuple(out)


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


def root_boundary_requirement() -> dict[tuple[tuple[int, int, int, int], int], tuple[int, int]]:
    required: dict[tuple[tuple[int, int, int, int], int], list[int]] = defaultdict(lambda: [0, 0])
    for pos, axis, orientation in plaquette_link_orientations(root_face(), 1):
        if orientation > 0:
            required[(pos, axis)][1] += 1
        else:
            required[(pos, axis)][0] += 1
    return {link: tuple(counts) for link, counts in required.items()}


ROOT_REQUIREMENT = root_boundary_requirement()
INTERNAL_ALLOWED_PATTERNS = {
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 0),
    (0, 3),
}


def valid_internal_pattern(counts: tuple[int, int]) -> bool:
    up_count, down_count = counts
    if (up_count - down_count) % 3 != 0:
        return False
    return counts in INTERNAL_ALLOWED_PATTERNS


def orientation_lift_data(
    key: tuple[Plaquette, ...]
) -> tuple[int, Counter[tuple[tuple[tuple[int, int], int], ...]]]:
    faces = tuple(sorted(spanning_surface_faces(key)))
    valid_lifts = 0
    lift_histograms: Counter[tuple[tuple[tuple[int, int], int], ...]] = Counter()

    for signs in product((-1, 1), repeat=len(faces)):
        link_counts: dict[tuple[tuple[int, int, int, int], int], list[int]] = defaultdict(lambda: [0, 0])
        for face, sign in zip(faces, signs):
            for pos, axis, orientation in plaquette_link_orientations(face, sign):
                if orientation > 0:
                    link_counts[(pos, axis)][0] += 1
                else:
                    link_counts[(pos, axis)][1] += 1

        ok = True
        for link, counts in link_counts.items():
            pair = tuple(counts)
            if link in ROOT_REQUIREMENT:
                if pair != ROOT_REQUIREMENT[link]:
                    ok = False
                    break
            elif not valid_internal_pattern(pair):
                ok = False
                break

        if not ok:
            continue

        for link, pair in ROOT_REQUIREMENT.items():
            if tuple(link_counts.get(link, (0, 0))) != pair:
                ok = False
                break

        if not ok:
            continue

        valid_lifts += 1
        histogram = Counter(tuple(counts) for counts in link_counts.values())
        lift_histograms[tuple(sorted(histogram.items()))] += 1

    return valid_lifts, lift_histograms


def first_nondisk_class_data() -> list[tuple[tuple[int, int, int, tuple[tuple[int, int], ...]], int, tuple[Plaquette, ...]]]:
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

    return [(invariant, multiplicities[invariant], representatives[invariant]) for invariant in sorted(multiplicities)]


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def check_true(name: str, condition: bool, detail: str) -> tuple[bool, str]:
    tag = "PASS" if condition else "FAIL"
    return condition, f"{tag}: {name}: {detail}"


def main() -> int:
    class_rows = first_nondisk_class_data()
    summary_rows: list[tuple[tuple[int, int, int, tuple[tuple[int, int], ...]], int, int, Counter[tuple[tuple[tuple[int, int], int], ...]]]] = []
    pure_fundamental_total = 0
    lift_impossible_total = 0

    print("=" * 78)
    print("FIRST NON-DISK Z_3 FACE-ORIENTATION LIFT THEOREM ON THE 3+1 LATTICE")
    print("=" * 78)
    print()
    print("Exact first genuine non-disk unique quotient sector")
    print(f"  beta = 6 local anchor p             = {LOCAL_PLAQUETTE_AT_BETA6:.15f}")
    print(f"  first genuine non-disk power        = p^{FIRST_NONDISK_POWER}")
    print()

    for invariant, multiplicity, representative in class_rows:
        valid_lifts, histogram = orientation_lift_data(representative)
        pure_fundamental_total += multiplicity if valid_lifts else 0
        lift_impossible_total += multiplicity if not valid_lifts else 0
        summary_rows.append((invariant, multiplicity, valid_lifts, histogram))

        print(f"class invariant                         = {invariant}")
        print(f"  quotient-surface multiplicity         = {multiplicity}")
        print(f"  valid pure-fundamental Z_3 lifts      = {valid_lifts}")
        print(f"  valid-link histogram families         = {dict(histogram)}")
        if invariant[1] == -1:
            genus = (1 - invariant[1]) // 2
            print(f"  manifold genus                        = {genus}")
            print(f"  exact ribbon color factor             = 3^({invariant[1]} - 1) = 1/9")
            print(f"  exact class contribution to H at p^14 = {(multiplicity / 9):.15f} p^14")
        print()

    print("Aggregate exact split of the first genuine non-disk sector")
    print(f"  total p^14 non-disk surfaces         = {sum(row[1] for row in summary_rows)}")
    print(f"  pure-fundamental-lift-admissible     = {pure_fundamental_total}")
    print(f"  lift-impossible on pure fund sheets  = {lift_impossible_total}")
    print()

    checks = [
        check_equal(
            "exact p^14 non-disk class multiplicities",
            {invariant: multiplicity for invariant, multiplicity, _ in class_rows},
            {
                (15, -1, 4, ((1, 4), (2, 28))): 8,
                (15, 3, 0, ((2, 24), (3, 4))): 4,
                (15, 3, 3, ((1, 3), (2, 21), (3, 1), (4, 3))): 48,
                (15, 3, 4, ((1, 4), (2, 20), (4, 4))): 12,
            },
        ),
        check_equal(
            "exact valid pure-fundamental lift counts by class",
            {invariant: valid_lifts for invariant, _multiplicity, valid_lifts, _histogram in summary_rows},
            {
                (15, -1, 4, ((1, 4), (2, 28))): 1,
                (15, 3, 0, ((2, 24), (3, 4))): 0,
                (15, 3, 3, ((1, 3), (2, 21), (3, 1), (4, 3))): 0,
                (15, 3, 4, ((1, 4), (2, 20), (4, 4))): 3,
            },
        ),
        check_equal("exact admissible pure-fundamental surface total", pure_fundamental_total, 20),
        check_equal("exact lift-impossible surface total", lift_impossible_total, 52),
        check_true(
            "the majority of the first non-disk sector lies outside a pure p-only sheet gas",
            lift_impossible_total > pure_fundamental_total,
            f"{lift_impossible_total} > {pure_fundamental_total}",
        ),
        check_true(
            "the genus-1 class is the unique pure ribbon-manifold class in the p^14 window",
            any(invariant[1] == -1 and valid_lifts == 1 for invariant, _multiplicity, valid_lifts, _histogram in summary_rows),
            "one genus-1 class with a single valid lift is present",
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

    print("Conclusion: the first genuine non-disk quotient sector already splits")
    print("exactly into three behaviors:")
    print("  1. pure ribbon-manifold genus-1 surfaces")
    print("  2. pure-fundamental quadrivalent crossing surfaces")
    print("  3. lift-impossible classes that require enrichment beyond a pure")
    print("     p-only fundamental-sheet quotient gas")
    print("So the direct exact closure object must be a character-labeled or")
    print("equivalently sheet-enriched quotient foam, not a scalar p-only surface gas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
