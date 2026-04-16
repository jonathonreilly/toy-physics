#!/usr/bin/env python3
"""
Exact fundamental-disk activity theorem on the 3+1 plaquette surface.

This runner promotes one specific part of the current quotient-surface route
from "formal" to exact:

1. the local anchor p = P_1plaq(beta) is the exact normalized fundamental
   character coefficient of the one-plaquette Wilson weight
2. the simply-sheeted disk sector of the quotient-surface gas through n <= 5
   can be identified exactly by topology
3. the isolated fundamental-sheet weight of that disk sector is exactly p^A

This still does not close the full plaquette, because the full
character-labeled / sheet-enriched activity law for the non-disk /
higher-sheet sectors remains open.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque

import numpy as np
from scipy.special import iv

from frontier_anchored_surface_gas_route import LOCAL_PLAQUETTE_AT_BETA6
from frontier_plaquette_first_nonlocal_connected_correction import one_plaquette_series
from frontier_quotient_surface_engine import rooted_surface_groups
from plaquette_surface_common import Plaquette, root_face, rooted_levels


MAX_MODE = 80
MAX_CELLS = 5
DIMS = 4


def bessel_minor(beta: float, partition: tuple[int, int, int], max_mode: int = MAX_MODE) -> float:
    total = 0.0
    for mode in range(-max_mode, max_mode + 1):
        mat = np.array(
            [
                [iv(mode + partition[i] - i + j, beta / 3.0) for j in range(3)]
                for i in range(3)
            ],
            dtype=float,
        )
        total += float(np.linalg.det(mat))
    return total


def one_plaquette_character_data(beta: float) -> tuple[float, float, float]:
    c0 = bessel_minor(beta, (0, 0, 0))
    cf = bessel_minor(beta, (1, 0, 0))
    p = cf / (3.0 * c0)
    return c0, cf, p


def e(axis: int) -> tuple[int, int, int, int]:
    vec = [0, 0, 0, 0]
    vec[axis] = 1
    return tuple(vec)


def add(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(x + y for x, y in zip(a, b))


def plaquette_edges(face: Plaquette) -> tuple[tuple[tuple[int, int, int, int], int], ...]:
    anchor, plane = face
    axis_a, axis_b = plane
    return (
        (anchor, axis_a),
        (anchor, axis_b),
        (add(anchor, e(axis_a)), axis_b),
        (add(anchor, e(axis_b)), axis_a),
    )


def plaquette_vertices(face: Plaquette) -> tuple[tuple[int, int, int, int], ...]:
    anchor, plane = face
    axis_a, axis_b = plane
    return (
        anchor,
        add(anchor, e(axis_a)),
        add(anchor, e(axis_b)),
        add(add(anchor, e(axis_a)), e(axis_b)),
    )


def spanning_surface_faces(key: tuple[Plaquette, ...]) -> set[Plaquette]:
    faces = set(key)
    faces.symmetric_difference_update({root_face()})
    return faces


def is_simply_sheeted_disk(key: tuple[Plaquette, ...]) -> bool:
    faces = spanning_surface_faces(key)
    if not faces:
        return True

    edges: set[tuple[tuple[int, int, int, int], int]] = set()
    vertices: set[tuple[int, int, int, int]] = set()
    edge_to_faces: dict[tuple[tuple[int, int, int, int], int], list[Plaquette]] = defaultdict(list)

    for face in faces:
        for edge in plaquette_edges(face):
            edges.add(edge)
            edge_to_faces[edge].append(face)
        vertices.update(plaquette_vertices(face))

    incidences = [len(incident_faces) for incident_faces in edge_to_faces.values()]
    if any(incidence > 2 for incidence in incidences):
        return False

    boundary_edges = sum(1 for incidence in incidences if incidence == 1)
    if boundary_edges != 4:
        return False

    neighbors: dict[Plaquette, set[Plaquette]] = defaultdict(set)
    for incident_faces in edge_to_faces.values():
        for i in range(len(incident_faces)):
            for j in range(i + 1, len(incident_faces)):
                neighbors[incident_faces[i]].add(incident_faces[j])
                neighbors[incident_faces[j]].add(incident_faces[i])

    start = next(iter(faces))
    queue = deque([start])
    seen = {start}
    while queue:
        face = queue.popleft()
        for neighbor in neighbors[face]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    if len(seen) != len(faces):
        return False

    chi = len(vertices) - len(edges) + len(faces)
    return chi == 1


def unique_and_disk_sector_polynomials() -> tuple[int, int, dict[int, int], dict[int, int], dict[int, int]]:
    levels = rooted_levels(MAX_CELLS)
    groups = rooted_surface_groups(levels)
    seen: set[tuple[Plaquette, ...]] = set()
    unique_poly: Counter[int] = Counter()
    disk_poly: Counter[int] = Counter()
    duplicate_poly: Counter[int] = Counter()
    total_surfaces = 0
    disk_surfaces = 0

    for per_level in groups.values():
        for key in per_level:
            if key in seen:
                duplicate_poly[len(key) - 2] += 1
                continue
            seen.add(key)
            total_surfaces += 1
            unique_poly[len(key) - 2] += 1
            if is_simply_sheeted_disk(key):
                disk_surfaces += 1
                disk_poly[len(key) - 2] += 1

    return (
        total_surfaces,
        disk_surfaces,
        dict(sorted(unique_poly.items())),
        dict(sorted(disk_poly.items())),
        dict(sorted(duplicate_poly.items())),
    )


def evaluate_polynomial(polynomial: dict[int, int], p: float) -> float:
    return 1.0 + sum(coeff * (p**power) for power, coeff in polynomial.items())


def check_close(name: str, value: float, target: float, tol: float) -> tuple[bool, str]:
    delta = abs(value - target)
    ok = delta <= tol
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value:.15f} target={target:.15f} delta={delta:.3e} tol={tol:.1e}"


def check_equal(name: str, value: object, target: object) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={value} target={target}"


def main() -> int:
    beta = 6.0
    c0, cf, p_char = one_plaquette_character_data(beta)
    p_local = LOCAL_PLAQUETTE_AT_BETA6

    total_surfaces, disk_surfaces, unique_poly, disk_poly, duplicate_poly = unique_and_disk_sector_polynomials()
    unique_h = evaluate_polynomial(unique_poly, p_char)
    unique_p = p_char * unique_h
    disk_h = evaluate_polynomial(disk_poly, p_char)
    disk_p = p_char * disk_h

    remainder_poly = {
        power: unique_poly.get(power, 0) - disk_poly.get(power, 0)
        for power in sorted(set(unique_poly) | set(disk_poly))
        if unique_poly.get(power, 0) - disk_poly.get(power, 0)
    }

    p_series = one_plaquette_series()
    area5_leading = 4.0 * float(p_series.coeff(1) ** 5)

    print("=" * 78)
    print("EXACT FUNDAMENTAL-DISK ACTIVITY THEOREM ON THE 3+1 PLAQUETTE SURFACE")
    print("=" * 78)
    print()
    print("Exact one-plaquette character data at beta = 6")
    print(f"  trivial coefficient c_0(6)          = {c0:.15f}")
    print(f"  fundamental coefficient c_f(6)      = {cf:.15f}")
    print(f"  p_char = c_f / (3 c_0)              = {p_char:.15f}")
    print(f"  exact local plaquette P_1plaq(6)    = {p_local:.15f}")
    print()
    print("Quotient-distinct spanning-surface census through n <= 5")
    print(f"  total unique quotient surfaces       = {total_surfaces}")
    print(f"  simply-sheeted disk surfaces         = {disk_surfaces}")
    print(f"  non-disk / higher-sheet remainder    = {total_surfaces - disk_surfaces}")
    print(f"  exact unique surface polynomial      = {unique_poly}")
    print(f"  exact disk-sector polynomial         = {disk_poly}")
    print(f"  cross-level duplicate polynomial     = {duplicate_poly}")
    print(f"  first non-disk deviation polynomial  = {remainder_poly}")
    print()
    print("Exact isolated fundamental unique-surface sector at beta = 6")
    print(f"  H_fund,unique^(n<=5)(6)              = {unique_h:.15f}")
    print(f"  P_fund,unique,iso^(n<=5)(6)          = {unique_p:.15f}")
    print()
    print("Exact isolated fundamental-disk sector at beta = 6")
    print(f"  H_fund,disk^(n<=5)(6)                = {disk_h:.15f}")
    print(f"  P_fund,disk,iso^(n<=5)(6)            = {disk_p:.15f}")
    print()
    print("Area-5 consistency")
    print(f"  exact leading coeff of 4 p(beta)^5   = {area5_leading:.15f}")
    print(f"  target 1 / 472392                    = {1.0 / 472392.0:.15f}")
    print()

    checks = [
        check_close("normalized fundamental coefficient equals P_1plaq(6)", p_char, p_local, 1.0e-12),
        check_equal("total unique quotient surfaces through n<=5", total_surfaces, 589824),
        check_equal("simply-sheeted disk surfaces through n<=5", disk_surfaces, 449632),
        check_equal(
            "exact unique quotient-surface polynomial",
            unique_poly,
            {4: 4, 8: 60, 10: 80, 12: 1092, 14: 2792, 16: 24468, 18: 70180, 20: 421432, 22: 68832, 24: 884},
        ),
        check_equal(
            "exact disk-sector polynomial",
            disk_poly,
            {4: 4, 8: 60, 10: 80, 12: 1092, 14: 2720, 16: 22740, 18: 62400, 20: 360536},
        ),
        check_equal("cross-level duplicate polynomial", duplicate_poly, {10: 64, 12: 56}),
        check_equal(
            "first non-disk deviation polynomial",
            remainder_poly,
            {14: 72, 16: 1728, 18: 7780, 20: 60896, 22: 68832, 24: 884},
        ),
        check_close("exact isolated fundamental unique-surface sector value", unique_p, 0.5522173124905123, 1.0e-12),
        check_close("exact isolated fundamental-disk sector value", disk_p, 0.5496643074058972, 1.0e-12),
        check_close("4 p(beta)^5 reproduces the area-5 coefficient", area5_leading, 1.0 / 472392.0, 1.0e-15),
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

    print("Conclusion: the local anchor p is the exact normalized fundamental")
    print("character coefficient of the one-plaquette Wilson weight, and the")
    print("simply-sheeted disk sector of the quotient-surface gas is now exact")
    print("through n <= 5. What remains open is the full character-labeled /")
    print("sheet-enriched activity law for the non-disk / higher-sheet sectors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
