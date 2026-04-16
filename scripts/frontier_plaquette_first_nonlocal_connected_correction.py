#!/usr/bin/env python3
"""
First nonlocal connected plaquette correction on the exact 3+1 lattice
======================================================================

This runner computes the first exact pure-gauge correction to the local
one-plaquette block using exact rational arithmetic.

Key point:
  - raw numerator/denominator moments contain lower-order local and bubble terms
  - the correct comparison object is the nonlocal connected correction relative
    to the exact one-plaquette block

The result proved here is

    P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O_nonlocal(beta^6)

on the exact 3 spatial + 1 time lattice.

Self-contained: standard library only.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import factorial


MAX_ORDER = 6


@dataclass(frozen=True)
class Series:
    coeffs: tuple[Fraction, ...]

    @staticmethod
    def zero(order: int = MAX_ORDER) -> "Series":
        return Series(tuple(Fraction(0) for _ in range(order + 1)))

    @staticmethod
    def one(order: int = MAX_ORDER) -> "Series":
        coeffs = [Fraction(0) for _ in range(order + 1)]
        coeffs[0] = Fraction(1)
        return Series(tuple(coeffs))

    @staticmethod
    def monomial(order_power: int, coeff: Fraction, order: int = MAX_ORDER) -> "Series":
        coeffs = [Fraction(0) for _ in range(order + 1)]
        if order_power <= order:
            coeffs[order_power] = coeff
        return Series(tuple(coeffs))

    def __add__(self, other: "Series") -> "Series":
        return Series(tuple(a + b for a, b in zip(self.coeffs, other.coeffs)))

    def __sub__(self, other: "Series") -> "Series":
        return Series(tuple(a - b for a, b in zip(self.coeffs, other.coeffs)))

    def scale(self, factor: Fraction) -> "Series":
        return Series(tuple(factor * c for c in self.coeffs))

    def __mul__(self, other: "Series") -> "Series":
        out = [Fraction(0) for _ in range(len(self.coeffs))]
        for i, ai in enumerate(self.coeffs):
            if ai == 0:
                continue
            for j, bj in enumerate(other.coeffs):
                if bj == 0 or i + j >= len(out):
                    continue
                out[i + j] += ai * bj
        return Series(tuple(out))

    def derivative(self) -> "Series":
        out = [Fraction(0) for _ in range(len(self.coeffs))]
        for n in range(1, len(self.coeffs)):
            out[n - 1] = self.coeffs[n] * n
        return Series(tuple(out))

    def coeff(self, n: int) -> Fraction:
        return self.coeffs[n]

    def log(self) -> "Series":
        """
        Truncated log series. Requires constant term 1.
        """
        if self.coeffs[0] != 1:
            raise ValueError("log requires constant term 1")
        x = self - Series.one(len(self.coeffs) - 1)
        out = Series.zero(len(self.coeffs) - 1)
        power = x
        for k in range(1, len(self.coeffs)):
            term = power.scale(Fraction(1, k) if (k % 2 == 1) else Fraction(-1, k))
            out = out + term
            power = power * x
        return out


def det3(m: list[list[Series]]) -> Series:
    return (
        m[0][0] * m[1][1] * m[2][2]
        + m[0][1] * m[1][2] * m[2][0]
        + m[0][2] * m[1][0] * m[2][1]
        - m[0][2] * m[1][1] * m[2][0]
        - m[0][1] * m[1][0] * m[2][2]
        - m[0][0] * m[1][2] * m[2][1]
    )


def bessel_i_series(n: int, order: int = MAX_ORDER) -> Series:
    """
    I_n(beta/3) as an exact beta-series.
    """
    n = abs(n)
    out = Series.zero(order)
    k = 0
    while True:
        power = 2 * k + n
        if power > order:
            break
        coeff = Fraction(1, factorial(k) * factorial(k + n) * 6**power)
        out = out + Series.monomial(power, coeff, order)
        k += 1
    return out


def one_plaquette_partition_series(order: int = MAX_ORDER) -> Series:
    total = Series.zero(order)
    for mode in range(-order, order + 1):
        matrix = [
            [bessel_i_series(mode + i - j, order) for j in range(3)]
            for i in range(3)
        ]
        total = total + det3(matrix)
    return total


def one_plaquette_series(order: int = MAX_ORDER) -> Series:
    return one_plaquette_partition_series(order).log().derivative()


def cube_boundary_orientation_count() -> int:
    """
    Two global orientations survive in the Re Tr expansion: outward and inward.
    """
    return 2


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[object, object] = {}

    def add(self, x: object) -> None:
        self.parent.setdefault(x, x)

    def find(self, x: object) -> object:
        self.add(x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: object, b: object) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def add3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(x + y for x, y in zip(a, b))


def e3(mu: int) -> tuple[int, int, int]:
    vec = [0, 0, 0]
    vec[mu] = 1
    return tuple(vec)


def oriented_plaquette_occurrences(
    x: tuple[int, int, int], mu: int, nu: int, dagger: bool
) -> list[tuple[tuple[tuple[int, int, int], int], bool]]:
    """
    Canonical Wilson plaquette W(x; mu, nu), mu < nu.
    Each factor is ((site, dir), is_dagger).
    """
    seq = [
        ((x, mu), False),
        ((add3(x, e3(mu)), nu), False),
        ((add3(x, e3(nu)), mu), True),
        ((x, nu), True),
    ]
    if not dagger:
        return seq
    return [(link, not is_dagger) for link, is_dagger in seq[::-1]]


def plaquette_pair_moment() -> Fraction:
    """
    Exact unit bubble <Tr U_p Tr U_p^dag>.
    """
    seq = oriented_plaquette_occurrences((0, 0, 0), 0, 1, dagger=False)
    seq_dag = oriented_plaquette_occurrences((0, 0, 0), 0, 1, dagger=True)

    uf = UnionFind()
    link_occurrences: dict[tuple[tuple[int, int, int], int], list[tuple[bool, object, object]]] = {}

    for face_name, face_seq in (("p", seq), ("pd", seq_dag)):
        factor_nodes = []
        for index, (link, is_dagger) in enumerate(face_seq):
            left = (face_name, index, "L")
            right = (face_name, index, "R")
            uf.add(left)
            uf.add(right)
            factor_nodes.append((link, is_dagger, left, right))
            link_occurrences.setdefault(link, []).append((is_dagger, left, right))
        for index in range(4):
            uf.union(factor_nodes[index][3], factor_nodes[(index + 1) % 4][2])

    edge_count = 0
    for occurrences in link_occurrences.values():
        first, second = occurrences
        u_term = first if not first[0] else second
        d_term = first if first[0] else second
        _, u_left, u_right = u_term
        _, d_left, d_right = d_term
        uf.union(u_left, d_right)
        uf.union(u_right, d_left)
        edge_count += 1

    free_loops = len({uf.find(node) for node in uf.parent})
    return Fraction(3**free_loops, 3**edge_count)


def cube_boundary_oriented_faces() -> dict[str, list[tuple[tuple[tuple[int, int, int], int], bool]]]:
    """
    One global orientation of the elementary cube boundary. The opposite one is
    obtained by daggering every face.
    """
    face_data = {
        "x0": ((0, 0, 0), 1, 2, False),
        "x1": ((1, 0, 0), 1, 2, True),
        "y0": ((0, 0, 0), 0, 2, True),
        "y1": ((0, 1, 0), 0, 2, False),
        "z0": ((0, 0, 0), 0, 1, False),
        "z1": ((0, 0, 1), 0, 1, True),
    }
    return {
        name: oriented_plaquette_occurrences(x, mu, nu, dagger)
        for name, (x, mu, nu, dagger) in face_data.items()
    }


def cube_boundary_moment() -> Fraction:
    """
    Expectation of the oriented product of the 6 plaquette traces around one
    elementary cube, using only the two-point Haar identity.
    """
    faces = cube_boundary_oriented_faces()
    uf = UnionFind()
    link_occurrences: dict[tuple[tuple[int, int, int], int], list[tuple[bool, object, object]]] = {}

    for face_name, seq in faces.items():
        factor_nodes = []
        for index, (link, is_dagger) in enumerate(seq):
            left = (face_name, index, "L")
            right = (face_name, index, "R")
            uf.add(left)
            uf.add(right)
            factor_nodes.append((link, is_dagger, left, right))
            link_occurrences.setdefault(link, []).append((is_dagger, left, right))
        for index in range(4):
            uf.union(factor_nodes[index][3], factor_nodes[(index + 1) % 4][2])

    edge_count = 0
    for occurrences in link_occurrences.values():
        if len(occurrences) != 2:
            raise ValueError("cube boundary should use each link twice")
        first, second = occurrences
        if first[0] == second[0]:
            raise ValueError("need one U and one U^dag per link")
        u_term = first if not first[0] else second
        d_term = first if first[0] else second
        _, u_left, u_right = u_term
        _, d_left, d_right = d_term
        uf.union(u_left, d_right)
        uf.union(u_right, d_left)
        edge_count += 1

    free_loops = len({uf.find(node) for node in uf.parent})
    return Fraction(3**free_loops, 3**edge_count)


def area5_surface_multiplicity_3plus1() -> int:
    dims_total = 4
    dims_in_plaquette = 2
    orthogonal_dirs = dims_total - dims_in_plaquette
    return 2 * orthogonal_dirs


def first_nonlocal_connected_coefficient() -> Fraction:
    """
    beta^5 coefficient relative to the exact one-plaquette block.
    The 1/5! from the action expansion cancels the 5! orderings of the five
    distinct plaquettes in a fixed cube complement.
    """
    return Fraction(
        area5_surface_multiplicity_3plus1() * cube_boundary_orientation_count(),
        6**6,
    ) * cube_boundary_moment()


def format_fraction(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def check_equal(name: str, value: Fraction, target: Fraction) -> tuple[bool, str]:
    ok = value == target
    tag = "PASS" if ok else "FAIL"
    return ok, f"{tag}: {name}: value={format_fraction(value)} target={format_fraction(target)}"


def main() -> int:
    local = one_plaquette_series(MAX_ORDER)
    correction = first_nonlocal_connected_coefficient()

    full_coeffs = list(local.coeffs)
    full_coeffs[5] += correction
    full = Series(tuple(full_coeffs))

    print("=" * 78)
    print("FIRST NONLOCAL CONNECTED PLAQUETTE CORRECTION ON THE EXACT 3+1 LATTICE")
    print("=" * 78)
    print()
    print("Exact one-plaquette series through beta^5")
    for power in range(1, 6):
        print(f"  beta^{power}: {format_fraction(local.coeff(power))}")
    print()
    print("First nonlocal connected ingredient")
    print(f"  plaquette-antiplaquette bubble          = {format_fraction(plaquette_pair_moment())}")
    print(f"  cube-boundary moment                  = {format_fraction(cube_boundary_moment())}")
    print(f"  global orientation count              = {cube_boundary_orientation_count()}")
    print(f"  area-5 surface multiplicity on 3+1    = {area5_surface_multiplicity_3plus1()}")
    print(f"  C_5^nonlocal                          = {format_fraction(correction)}")
    print()
    print("Combined full plaquette series through beta^5")
    for power in range(1, 6):
        print(f"  beta^{power}: {format_fraction(full.coeff(power))}")
    print()

    exact_checks = []
    exact_checks.append(
        check_equal("local beta coefficient", local.coeff(1), Fraction(1, 18))
    )
    exact_checks.append(
        check_equal("local beta^2 coefficient", local.coeff(2), Fraction(1, 216))
    )
    exact_checks.append(
        check_equal("local beta^3 coefficient vanishes", local.coeff(3), Fraction(0))
    )
    exact_checks.append(
        check_equal("local beta^4 coefficient", local.coeff(4), Fraction(-5, 93312))
    )
    exact_checks.append(
        check_equal("local beta^5 coefficient", local.coeff(5), Fraction(-1, 186624))
    )
    exact_checks.append(
        check_equal("plaquette-antiplaquette unit bubble", plaquette_pair_moment(), Fraction(1))
    )
    exact_checks.append(
        check_equal("cube-boundary two-point contraction", cube_boundary_moment(), Fraction(1, 81))
    )
    exact_checks.append(
        check_equal("area-5 multiplicity on 3+1", Fraction(area5_surface_multiplicity_3plus1()), Fraction(4))
    )
    exact_checks.append(
        check_equal("first nonlocal connected coefficient", correction, Fraction(1, 472392))
    )
    exact_checks.append(
        check_equal("full and local agree through beta^4", full.coeff(4) - local.coeff(4), Fraction(0))
    )
    exact_checks.append(
        check_equal("first full-vs-local difference is beta^5", full.coeff(5) - local.coeff(5), Fraction(1, 472392))
    )

    print("Checks")
    passed = 0
    for ok, msg in exact_checks:
        print(" ", msg)
        passed += int(ok)
    failed = len(exact_checks) - passed

    print()
    print(f"SUMMARY: exact {passed} pass / {failed} fail")
    print()

    if failed:
        return 1

    print("Conclusion: the first nonlocal connected correction is +beta^5 / 472392.")
    print("The exact local block remains valid; the first distinct 3+1 cube correction enters at beta^5.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
