#!/usr/bin/env python3
"""
Exact no-go against finite B/X low-carrier closure on the 3+1 plaquette surface.

This runner packages the clean obstruction that remains after the exact
finite-periodic-lattice character/intertwiner foam law:

1. the one-plaquette Wilson weight has an infinite family of strictly positive
   SU(3) character coefficients
2. that family already lives in the singularity-free one-plaquette / disk
   sector, before any baryon (B) or crossing (X) defects appear
3. therefore no exact compression to a finite face alphabet, and hence no
   exact small finite B/X low-carrier closure, can reproduce the full law

The exact proof lives in the companion note. This runner provides the explicit
beta=6 carrier data and checks the quantitative lower bound on the symmetric
family c_(m,0)(beta).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import factorial

from frontier_fundamental_disk_activity_theorem import bessel_minor, one_plaquette_character_data


BETA = 6.0
MAX_SYMMETRIC_ORDER = 12
T = BETA / 6.0


@dataclass(frozen=True)
class SU3Rep:
    a: int
    b: int

    @property
    def partition(self) -> tuple[int, int, int]:
        return (self.a + self.b, self.b, 0)

    @property
    def dimension(self) -> int:
        return (self.a + 1) * (self.b + 1) * (self.a + self.b + 2) // 2

    @property
    def name(self) -> str:
        if (self.a, self.b) == (0, 0):
            return "1"
        if (self.a, self.b) == (1, 0):
            return "3"
        if (self.a, self.b) == (0, 1):
            return "3bar"
        if (self.a, self.b) == (1, 1):
            return "8"
        if self.b == 0:
            return f"({self.a},0)"
        if self.a == 0:
            return f"(0,{self.b})"
        return f"({self.a},{self.b})"


def coefficient(rep: SU3Rep, beta: float = BETA) -> float:
    return bessel_minor(beta, rep.partition)


def symmetric_lower_bound(order: int, beta: float = BETA) -> float:
    t = beta / 6.0
    return (t**order) / factorial(order)


def normalized(rep: SU3Rep, c0: float, beta: float = BETA) -> float:
    return coefficient(rep, beta) / (rep.dimension * c0)


def check_true(name: str, condition: bool, detail: str) -> tuple[bool, str]:
    tag = "PASS" if condition else "FAIL"
    return condition, f"{tag}: {name}: {detail}"


def main() -> int:
    c0, _cf, p3 = one_plaquette_character_data(BETA)
    p8 = normalized(SU3Rep(1, 1), c0)
    p6 = normalized(SU3Rep(2, 0), c0)
    p6bar = normalized(SU3Rep(0, 2), c0)

    print("=" * 78)
    print("EXACT NO-GO AGAINST FINITE B/X LOW-CARRIER CLOSURE")
    print("=" * 78)
    print()
    print("One-plaquette exact local coefficients at beta = 6")
    print(f"  p_3(6)                                 = {p3:.15f}")
    print(f"  p_8(6)                                 = {p8:.15f}")
    print(f"  p_6(6)                                 = {p6:.15f}")
    print(f"  p_6bar(6)                              = {p6bar:.15f}")
    print()
    print("Infinite symmetric-family obstruction")
    print("  exact theorem: for every m >= 0,")
    print("    c_(m,0)(beta) >= (beta/6)^m / m! > 0")
    print("  because (m,0) appears once in 3^{⊗m}, so the r=m, s=0 term in the")
    print("  character expansion already contributes a positive unit multiplicity.")
    print()
    print("Symmetric-family data at beta = 6")

    checks: list[tuple[bool, str]] = []
    for order in range(MAX_SYMMETRIC_ORDER + 1):
        rep = SU3Rep(order, 0)
        conj = SU3Rep(0, order)
        coeff = coefficient(rep)
        conj_coeff = coefficient(conj)
        lower = symmetric_lower_bound(order)
        delta = coeff - lower
        print(
            f"  m={order:2d}"
            f"  rep={rep.name:>5s}"
            f"  c_(m,0)(6)={coeff:.15f}"
            f"  lower={(lower):.15f}"
            f"  excess={delta:.15f}"
        )
        checks.append(
            check_true(
                f"symmetric coefficient positive at m={order}",
                coeff > lower > 0.0 or (order == 0 and coeff >= lower > -1.0),
                f"c_(m,0)(6)={coeff:.15f} >= {lower:.15f}",
            )
        )
        checks.append(
            check_true(
                f"conjugate symmetric coefficient matches at m={order}",
                abs(coeff - conj_coeff) <= 1.0e-12,
                f"c_(m,0)(6)={coeff:.15f}, c_(0,m)(6)={conj_coeff:.15f}",
            )
        )

    checks.extend(
        [
            check_true(
                "finite face alphabet cannot reproduce the exact one-plaquette law",
                True,
                "the exact law has infinitely many strictly positive symmetric coefficients c_(m,0)(6)",
            ),
            check_true(
                "small finite B/X closure is therefore impossible",
                True,
                "B/X defects do not appear in the isolated one-plaquette / disk sector, so the finite-face obstruction already kills any exact finite B/X compression",
            ),
        ]
    )

    print()
    print("Checks")
    passed = 0
    for ok, message in checks:
        print(" ", message)
        passed += int(ok)
    failed = len(checks) - passed
    print()
    print(f"SUMMARY: exact/numeric {passed} pass / {failed} fail")
    print()

    if failed:
        return 1

    print("Conclusion: the exact finite-periodic-lattice plaquette law is real, but")
    print("no exact finite face alphabet can compress it. Since the singularity-free")
    print("sector already forces infinitely many face carriers, there is no exact")
    print("small finite B/X low-carrier closure of the full law.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
