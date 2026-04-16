#!/usr/bin/env python3
"""
Exact quotient-distinct same-boundary surface engine on the 3+1 plaquette surface.

This runner replaces raw rooted-filling counting by the physical quotient
object:

    S = q + dV

Two rooted fillings V and W define the same physical anchored surface exactly
when dV = dW, equivalently when V + W is a finite 4-cube boundary.

Self-contained: standard library only.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from plaquette_surface_common import (
    Cell,
    boundary_faces,
    canonical_surface_key,
    root_face,
    root_incidence,
    rooted_levels,
    same_boundary_witness,
)


MAX_CELLS = 5


def rooted_surface_groups(levels: dict[int, set[frozenset[Cell]]]) -> dict[int, dict[tuple[object, ...], list[frozenset[Cell]]]]:
    q = root_face()
    grouped: dict[int, dict[tuple[object, ...], list[frozenset[Cell]]]] = {}
    for count, families in levels.items():
        by_key: dict[tuple[object, ...], list[frozenset[Cell]]] = defaultdict(list)
        for cells in families:
            if q not in boundary_faces(cells):
                continue
            by_key[canonical_surface_key(cells)].append(cells)
        grouped[count] = by_key
    return grouped


def aggregate_surface_polynomial(groups: dict[int, dict[tuple[object, ...], list[frozenset[Cell]]]]) -> dict[int, int]:
    coeffs: Counter[int] = Counter()
    for per_level in groups.values():
        for key in per_level:
            coeffs[len(key) - 2] += 1
    return dict(sorted(coeffs.items()))


def format_polynomial(polynomial: dict[int, int]) -> str:
    return "1 + " + " + ".join(f"{coeff} p^{power}" for power, coeff in polynomial.items())


def duplicate_summary(per_level: dict[tuple[object, ...], list[frozenset[Cell]]]) -> tuple[dict[int, int], dict[int, int], dict[tuple[tuple[int, int], ...], int]]:
    multiplicity_hist: Counter[int] = Counter()
    boundary_hist: Counter[int] = Counter()
    launch_hist: Counter[tuple[tuple[int, int], ...]] = Counter()
    for key, families in per_level.items():
        if len(families) == 1:
            continue
        multiplicity_hist[len(families)] += 1
        boundary_hist[len(key)] += len(families) - 1
        launches = tuple(sorted(Counter(root_incidence(cells) for cells in families).items()))
        launch_hist[launches] += 1
    return dict(sorted(multiplicity_hist.items())), dict(sorted(boundary_hist.items())), dict(launch_hist)


def first_duplicate_pair(per_level: dict[tuple[object, ...], list[frozenset[Cell]]]) -> tuple[frozenset[Cell], frozenset[Cell]]:
    for families in per_level.values():
        if len(families) > 1:
            return families[0], families[1]
    raise RuntimeError("no duplicate pair found on this level")


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    levels = rooted_levels(MAX_CELLS)
    groups = rooted_surface_groups(levels)
    polynomial = aggregate_surface_polynomial(groups)

    print("=" * 78)
    print("EXACT QUOTIENT-DISTINCT SAME-BOUNDARY SURFACE ENGINE ON THE 3+1 LATTICE")
    print("=" * 78)
    print()

    first_overcount_level = None
    for count in range(1, MAX_CELLS + 1):
        per_level = groups[count]
        raw_count = sum(len(families) for families in per_level.values())
        unique_count = len(per_level)
        by_boundary = Counter(len(key) for key in per_level)
        multiplicity_hist, duplicate_boundary_hist, duplicate_launch_hist = duplicate_summary(per_level)
        if first_overcount_level is None and raw_count > unique_count:
            first_overcount_level = count

        print(f"n = {count}")
        print(f"  raw rooted fillings                 = {raw_count}")
        print(f"  quotient-distinct surfaces          = {unique_count}")
        print(f"  hidden fillings removed             = {raw_count - unique_count}")
        print(f"  unique by |dV|                      = {dict(sorted(by_boundary.items()))}")
        print(f"  duplicate multiplicity histogram    = {multiplicity_hist}")
        print(f"  duplicate raw-extra by |dV|         = {duplicate_boundary_hist}")
        print(f"  duplicate launch-sector histogram   = {duplicate_launch_hist}")
        print()

    dup4_left, dup4_right = first_duplicate_pair(groups[4])
    dup4_witness, dup4_pad = same_boundary_witness(dup4_left, dup4_right)
    dup5_left, dup5_right = first_duplicate_pair(groups[5])
    dup5_witness, dup5_pad = same_boundary_witness(dup5_left, dup5_right)

    print("Formal quotient count generator through n <= 5")
    print(f"  G_surface_partial(p) = {format_polynomial(polynomial)}")
    print("  This is an exact quotient-distinct surface count series, not yet a")
    print("  theorem-grade finite-beta plaquette weight law.")
    print()
    print("Sample duplicate witnesses")
    print(f"  n = 4 duplicate witness cubes       = {tuple(sorted(dup4_witness))} (pad {dup4_pad})")
    print(f"  n = 5 duplicate witness cubes       = {tuple(sorted(dup5_witness))} (pad {dup5_pad})")
    print()

    checks = [
        check_equal("area-5 rooted multiplicity survives quotient", len(groups[1]), 4),
        check_equal("n=1 raw equals quotient", sum(len(v) for v in groups[1].values()), len(groups[1])),
        check_equal("n=2 raw equals quotient", sum(len(v) for v in groups[2].values()), len(groups[2])),
        check_equal("n=3 raw equals quotient", sum(len(v) for v in groups[3].values()), len(groups[3])),
        check_equal("first raw overcount starts at n=4", first_overcount_level, 4),
        check_equal("n=4 hidden fillings removed", sum(len(v) for v in groups[4].values()) - len(groups[4]), 80),
        check_equal("n=5 hidden fillings removed", sum(len(v) for v in groups[5].values()) - len(groups[5]), 2848),
        check_equal("n=4 duplicate classes are all simple pairs", duplicate_summary(groups[4])[0], {2: 80}),
        check_equal("n=5 duplicate classes are all simple pairs", duplicate_summary(groups[5])[0], {2: 2848}),
        check_equal("n=4 duplicate classes stay in the k=1 launch sector", duplicate_summary(groups[4])[2], {((1, 2),): 80}),
        check_equal("n=5 duplicate classes stay in the k=1 launch sector", duplicate_summary(groups[5])[2], {((1, 2),): 2848}),
        check_equal("n=4 duplicate difference is one 4-cube boundary", len(dup4_witness), 1),
        check_equal("n=5 duplicate difference is one 4-cube boundary", len(dup5_witness), 1),
        check_equal("quotient count at n=4", len(groups[4]), 24920),
        check_equal("quotient count at n=5", len(groups[5]), 563796),
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

    print("Conclusion: the raw rooted engine overcounts fillings rather than physical")
    print("anchored plaquette surfaces, and the first quotient collision occurs at n = 4")
    print("as a single unit 4-cube boundary move. The canonical physical object is the")
    print("quotient-distinct same-boundary surface key.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
