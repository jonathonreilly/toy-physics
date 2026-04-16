#!/usr/bin/env python3
"""
Exact two-shell channel theorem for the propagated hidden quotient sector.

This runner refines the exact propagated two-shell theorem. The one-step image
of the n = 5 hidden quotient sector is known to consist exactly of duplicate
quotient classes of the form

  one unit 4-cube boundary + two shared exterior 3-cells.

The question here is whether that two-shell sector still collapses to a finite
local alphabet under unit 4-cube symmetry, and whether its representatives
carry a finite exact one-step quotient transfer law.

Self-contained except for exact prior hidden-shell / two-shell geometry.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import permutations, product

from frontier_hidden_shell_channel_theorem import (
    canonical_cell_from_vertices,
    cell_vertices,
    next_quotient_histogram,
)
from frontier_hidden_two_shell_theorem import hidden_image_groups, witness_origin_from_difference


DIMS = 4
CUBE_SYMMETRIES = tuple(
    (perm, flips)
    for perm in permutations(range(DIMS))
    for flips in product((False, True), repeat=DIMS)
)

LocalCell = tuple[tuple[int, int, int, int], tuple[int, int, int]]


def relative_cells(
    cells: frozenset[tuple[tuple[int, int, int, int], tuple[int, int, int]]],
    origin: tuple[int, int, int, int],
) -> tuple[LocalCell, ...]:
    return tuple(
        sorted(
            (
                tuple(anchor[axis] - origin[axis] for axis in range(DIMS)),
                axes,
            )
            for anchor, axes in cells
        )
    )


@lru_cache(maxsize=None)
def transform_point(
    point: tuple[int, int, int, int],
    perm: tuple[int, ...],
    flips: tuple[bool, ...],
) -> tuple[int, int, int, int]:
    image = [0, 0, 0, 0]
    for axis in range(DIMS):
        value = point[axis]
        if flips[axis]:
            value = 1 - value
        image[perm[axis]] = value
    return tuple(image)


@lru_cache(maxsize=None)
def transform_local_cell(
    cell: LocalCell,
    perm: tuple[int, ...],
    flips: tuple[bool, ...],
) -> LocalCell:
    vertices = frozenset(transform_point(vertex, perm, flips) for vertex in cell_vertices(cell))
    return canonical_cell_from_vertices(vertices)


@lru_cache(maxsize=None)
def canonical_ordered_raw(raw_cells: tuple[LocalCell, ...]) -> tuple[LocalCell, ...]:
    best: tuple[LocalCell, ...] | None = None
    for perm, flips in CUBE_SYMMETRIES:
        candidate = tuple(sorted(transform_local_cell(cell, perm, flips) for cell in raw_cells))
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise RuntimeError("failed to canonicalize ordered two-shell state")
    return best


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    image = hidden_image_groups()
    duplicates = [tuple(families) for families in image.values() if len(families) == 2]

    raw_unordered_hist: Counter[tuple[tuple[LocalCell, ...], tuple[LocalCell, ...]]] = Counter()
    raw_ordered_hist: Counter[tuple[LocalCell, ...]] = Counter()
    raw_representative: dict[tuple[LocalCell, ...], frozenset[object]] = {}

    for left, right in duplicates:
        origin = witness_origin_from_difference(frozenset(left ^ right))
        if origin is None:
            raise RuntimeError("expected every propagated duplicate pair to have a unit 4-cube witness")

        left_raw = relative_cells(left, origin)
        right_raw = relative_cells(right, origin)

        raw_unordered_hist[min((left_raw, right_raw), (right_raw, left_raw))] += 1
        raw_ordered_hist[left_raw] += 1
        raw_ordered_hist[right_raw] += 1

        raw_representative.setdefault(left_raw, left)
        raw_representative.setdefault(right_raw, right)

    ordered_orbit_hist: Counter[tuple[LocalCell, ...]] = Counter()
    ordered_representative: dict[tuple[LocalCell, ...], frozenset[object]] = {}
    raw_to_orbit: dict[tuple[LocalCell, ...], tuple[LocalCell, ...]] = {}

    for raw_state, multiplicity in raw_ordered_hist.items():
        orbit = canonical_ordered_raw(raw_state)
        raw_to_orbit[raw_state] = orbit
        ordered_orbit_hist[orbit] += multiplicity
        ordered_representative.setdefault(orbit, raw_representative[raw_state])

    unordered_orbit_hist: Counter[tuple[tuple[LocalCell, ...], tuple[LocalCell, ...]]] = Counter()
    for raw_pair, multiplicity in raw_unordered_hist.items():
        left_raw, right_raw = raw_pair
        left_orbit = raw_to_orbit[left_raw]
        right_orbit = raw_to_orbit[right_raw]
        orbit_pair = min((left_orbit, right_orbit), (right_orbit, left_orbit))
        unordered_orbit_hist[orbit_pair] += multiplicity

    ordered_histograms: dict[tuple[LocalCell, ...], tuple[tuple[int, int], ...]] = {}
    ordered_counts: dict[tuple[LocalCell, ...], int] = {}
    for orbit, representative in ordered_representative.items():
        ordered_histograms[orbit] = next_quotient_histogram(representative)
        ordered_counts[orbit] = sum(multiplicity for _boundary, multiplicity in ordered_histograms[orbit])

    unordered_channel_hist: Counter[tuple[int, int]] = Counter()
    for orbit_pair, multiplicity in unordered_orbit_hist.items():
        left_orbit, right_orbit = orbit_pair
        counts = tuple(sorted((ordered_counts[left_orbit], ordered_counts[right_orbit])))
        unordered_channel_hist[counts] += multiplicity

    print("=" * 78)
    print("EXACT TWO-SHELL CHANNEL THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print("Propagated two-shell hidden sector")
    print(f"  duplicate quotient classes           = {len(duplicates)}")
    print(f"  unique raw ordered states            = {len(raw_ordered_hist)}")
    print(f"  unique raw unordered pairs           = {len(raw_unordered_hist)}")
    print(f"  ordered local two-shell orbits       = {len(ordered_orbit_hist)}")
    print(f"  unordered two-shell pair orbits      = {len(unordered_orbit_hist)}")
    print()
    print("Ordered two-shell orbit multiplicities")
    for multiplicity, orbit_count in sorted(Counter(ordered_orbit_hist.values()).items()):
        print(f"  multiplicity {multiplicity}: orbit count {orbit_count}")
    print()
    print("Ordered two-shell sample transfer data")
    ordered_count_hist = Counter(ordered_counts.values())
    for index, (orbit, multiplicity) in enumerate(ordered_orbit_hist.most_common()[:20]):
        print(
            f"  orbit {index}: multiplicity {multiplicity}, next count {ordered_counts[orbit]}, "
            f"histogram {dict(ordered_histograms[orbit])}"
        )
    print()
    print("Ordered two-shell next-count histogram")
    for count, orbit_count in sorted(ordered_count_hist.items()):
        print(f"  next quotient count {count}: orbit count {orbit_count}")
    print()
    print("Unordered two-shell channel histogram")
    for counts, multiplicity in sorted(unordered_channel_hist.items()):
        print(f"  counts {counts}: multiplicity {multiplicity}")
    print()
    print(f"  distinct ordered transfer histograms = {len({ordered_histograms[orbit] for orbit in ordered_orbit_hist})}")
    print(f"  distinct unordered count channels    = {len(unordered_channel_hist)}")
    print()

    checks = [
        check_equal("propagated duplicate quotient class count", len(duplicates), 81280),
        check_equal("unique raw ordered two-shell states", len(raw_ordered_hist), 49840),
        check_equal("unique raw unordered two-shell pairs", len(raw_unordered_hist), 24920),
        check_equal("ordered local two-shell orbit count", len(ordered_orbit_hist), 226),
        check_equal("unordered two-shell pair orbit count", len(unordered_orbit_hist), 121),
        check_equal(
            "ordered two-shell orbit multiplicities",
            dict(sorted(Counter(ordered_orbit_hist.values()).items())),
            {
                176: 2,
                192: 6,
                272: 6,
                304: 6,
                320: 4,
                352: 19,
                368: 1,
                384: 9,
                400: 1,
                480: 6,
                544: 48,
                576: 2,
                608: 10,
                640: 7,
                672: 1,
                704: 23,
                736: 3,
                768: 6,
                960: 10,
                1088: 20,
                1280: 9,
                1408: 26,
                1536: 1,
            },
        ),
        check_equal(
            "ordered two-shell next-count orbit histogram",
            dict(sorted(ordered_count_hist.items())),
            {54: 2, 55: 1, 56: 12, 57: 8, 58: 24, 59: 39, 60: 28, 61: 42, 62: 23, 63: 23, 64: 9, 65: 12, 66: 2, 67: 1},
        ),
        check_equal(
            "ordered two-shell transfer histogram count",
            len({ordered_histograms[orbit] for orbit in ordered_orbit_hist}),
            184,
        ),
        check_equal(
            "unordered two-shell channel histogram",
            dict(sorted(unordered_channel_hist.items())),
            {
                (54, 57): 576,
                (54, 58): 960,
                (55, 55): 336,
                (56, 58): 3296,
                (56, 59): 2752,
                (56, 60): 2816,
                (57, 57): 552,
                (57, 58): 960,
                (57, 59): 480,
                (57, 61): 2240,
                (58, 58): 1280,
                (58, 59): 544,
                (58, 60): 3424,
                (58, 61): 4112,
                (58, 63): 1408,
                (58, 64): 352,
                (59, 59): 4072,
                (59, 60): 4288,
                (59, 61): 2768,
                (59, 62): 3616,
                (59, 63): 5104,
                (59, 64): 2112,
                (59, 65): 352,
                (60, 60): 1408,
                (60, 61): 5184,
                (60, 62): 2512,
                (60, 64): 384,
                (61, 61): 2640,
                (61, 62): 2720,
                (61, 63): 1328,
                (61, 64): 1632,
                (61, 65): 3552,
                (62, 62): 3808,
                (62, 63): 1632,
                (62, 64): 544,
                (63, 63): 2112,
                (63, 64): 544,
                (63, 65): 816,
                (63, 66): 1152,
                (64, 65): 608,
                (65, 67): 304,
            },
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

    print("Conclusion: the propagated two-shell hidden sector also collapses to a")
    print("finite local alphabet under unit 4-cube symmetry, but not a tiny one.")
    print("It has 226 ordered local orbits, 121 unordered pair-orbits, and 184")
    print("distinct exact one-step quotient transfer histograms.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
