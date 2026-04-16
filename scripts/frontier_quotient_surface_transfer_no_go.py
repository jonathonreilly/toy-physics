#!/usr/bin/env python3
"""
Exact no-go against quotient-surface-only rooted transfer on the 3+1 plaquette surface.

After quotienting rooted fillings by exact 4-cube boundary moves, the physical
anchored object is the same-boundary surface key dV. This runner asks the next
natural question:

  does that quotient surface key determine the next rooted quotient
  continuation law?

The answer is no. At n = 4 the next quotient-surface count is still the same
for duplicate representatives, but the next boundary-size histogram already
differs. By n = 5 even the scalar next quotient-surface count differs for every
duplicate pair.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from plaquette_surface_common import (
    Cell,
    boundary_faces,
    canonical_surface_key,
    cell_faces,
    cells_incident_to_face,
    root_face,
    rooted_levels,
)


MAX_CELLS = 5


def rooted_groups(level: int) -> dict[tuple[object, ...], list[frozenset[Cell]]]:
    q = root_face()
    groups: dict[tuple[object, ...], list[frozenset[Cell]]] = defaultdict(list)
    for cells in rooted_levels(MAX_CELLS)[level]:
        if q in boundary_faces(cells):
            groups[canonical_surface_key(cells)].append(cells)
    return groups


def next_quotient_summary(cells: frozenset[Cell]) -> tuple[int, tuple[tuple[int, int], ...], tuple[tuple[object, ...], ...]]:
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
    return len(keys), tuple(sorted(histogram.items())), tuple(sorted(keys))


def first_pair_with_different_histogram(groups: dict[tuple[object, ...], list[frozenset[Cell]]]) -> tuple[frozenset[Cell], frozenset[Cell]]:
    for families in groups.values():
        if len(families) != 2:
            continue
        left, right = families
        if next_quotient_summary(left)[1] != next_quotient_summary(right)[1]:
            return left, right
    raise RuntimeError("expected a duplicate pair with different next quotient histogram")


def first_pair_with_different_count(groups: dict[tuple[object, ...], list[frozenset[Cell]]]) -> tuple[frozenset[Cell], frozenset[Cell]]:
    for families in groups.values():
        if len(families) != 2:
            continue
        left, right = families
        if next_quotient_summary(left)[0] != next_quotient_summary(right)[0]:
            return left, right
    raise RuntimeError("expected a duplicate pair with different next quotient count")


def duplicate_transfer_summary(groups: dict[tuple[object, ...], list[frozenset[Cell]]]) -> tuple[int, int, int]:
    diff_counts = 0
    diff_histograms = 0
    diff_sets = 0
    for families in groups.values():
        if len(families) != 2:
            continue
        left, right = families
        left_summary = next_quotient_summary(left)
        right_summary = next_quotient_summary(right)
        if left_summary[0] != right_summary[0]:
            diff_counts += 1
        if left_summary[1] != right_summary[1]:
            diff_histograms += 1
        if left_summary[2] != right_summary[2]:
            diff_sets += 1
    return diff_counts, diff_histograms, diff_sets


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    groups4 = rooted_groups(4)
    groups5 = rooted_groups(5)

    dup4_groups = {key: families for key, families in groups4.items() if len(families) > 1}
    dup5_groups = {key: families for key, families in groups5.items() if len(families) > 1}

    n4_diff_counts, n4_diff_histograms, n4_diff_sets = duplicate_transfer_summary(dup4_groups)
    n5_diff_counts, n5_diff_histograms, n5_diff_sets = duplicate_transfer_summary(dup5_groups)

    n4_left, n4_right = first_pair_with_different_histogram(dup4_groups)
    n5_left, n5_right = first_pair_with_different_count(dup5_groups)
    n4_left_summary = next_quotient_summary(n4_left)
    n4_right_summary = next_quotient_summary(n4_right)
    n5_left_summary = next_quotient_summary(n5_left)
    n5_right_summary = next_quotient_summary(n5_right)

    print("=" * 78)
    print("EXACT QUOTIENT-SURFACE ROOTED TRANSFER NO-GO ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print("Duplicate quotient-surface classes")
    print(f"  n = 4 duplicate classes            = {len(dup4_groups)}")
    print(f"  n = 5 duplicate classes            = {len(dup5_groups)}")
    print()
    print("Representative dependence summary")
    print(f"  n = 4: different next quotient counts     = {n4_diff_counts}")
    print(f"  n = 4: different next |dV|-histograms     = {n4_diff_histograms}")
    print(f"  n = 4: different next quotient sets       = {n4_diff_sets}")
    print(f"  n = 5: different next quotient counts     = {n5_diff_counts}")
    print(f"  n = 5: different next |dV|-histograms     = {n5_diff_histograms}")
    print(f"  n = 5: different next quotient sets       = {n5_diff_sets}")
    print()
    print("n = 4 witness: same quotient class, same scalar count, different histogram")
    print(f"  A = {tuple(sorted(n4_left))}")
    print(f"  B = {tuple(sorted(n4_right))}")
    print(f"  count(A) = {n4_left_summary[0]}, hist(A) = {dict(n4_left_summary[1])}")
    print(f"  count(B) = {n4_right_summary[0]}, hist(B) = {dict(n4_right_summary[1])}")
    print()
    print("n = 5 witness: same quotient class, different scalar count")
    print(f"  A = {tuple(sorted(n5_left))}")
    print(f"  B = {tuple(sorted(n5_right))}")
    print(f"  count(A) = {n5_left_summary[0]}, hist(A) = {dict(n5_left_summary[1])}")
    print(f"  count(B) = {n5_right_summary[0]}, hist(B) = {dict(n5_right_summary[1])}")
    print()

    checks = [
        check_equal("n=4 duplicate class count", len(dup4_groups), 80),
        check_equal("n=5 duplicate class count", len(dup5_groups), 2848),
        check_equal("n=4 scalar next quotient count is representative-independent", n4_diff_counts, 0),
        check_equal("n=4 next |dV|-histogram differs on 32 duplicate classes", n4_diff_histograms, 32),
        check_equal("n=4 next quotient set differs on every duplicate class", n4_diff_sets, 80),
        check_equal("n=5 scalar next quotient count differs on every duplicate class", n5_diff_counts, 2848),
        check_equal("n=5 next |dV|-histogram differs on every duplicate class", n5_diff_histograms, 2848),
        check_equal("n=5 next quotient set differs on every duplicate class", n5_diff_sets, 2848),
        check_equal("n=4 witness scalar count match", n4_left_summary[0], n4_right_summary[0]),
        check_equal("n=5 witness scalar counts", (n5_left_summary[0], n5_right_summary[0]), (47, 49)),
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

    print("Conclusion: the quotient surface key is the correct physical counting object,")
    print("but it is not a Markov state for rooted continuation. Any exact rooted transfer")
    print("must retain extra hidden-filling information beyond the bare quotient surface.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
