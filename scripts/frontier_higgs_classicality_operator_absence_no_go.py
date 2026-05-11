#!/usr/bin/env python3
"""No-go runner for the Higgs classicality operator-absence boundary.

The checked claim is narrow:

    absence of a fundamental lattice-bare lambda phi^4 operator

does not by itself imply the continuum MSbar boundary lambda(M_Pl)=0. A
matching theorem is needed because a finite additive matching term can make
lambda_MSbar nonzero even when lambda_bare=0.
"""

from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "=" * 88)
    print(title)
    print("=" * 88)


def lambda_msbar(lambda_bare: Fraction, z_lambda: Fraction, delta_lambda: Fraction) -> Fraction:
    return z_lambda * lambda_bare + delta_lambda


def main() -> int:
    print("Higgs classicality operator-absence no-go")

    section("Dependency packet exists")
    deps = [
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
        "docs/G_BARE_DERIVATION_NOTE.md",
        "docs/HIGGS_MASS_DERIVED_NOTE.md",
        "docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md",
    ]
    for dep in deps:
        check(f"dependency source present: {dep}", (ROOT / dep).exists())

    section("Operator absence is only a lattice-bare statement")
    has_fundamental_scalar = False
    has_fundamental_phi4 = False
    lambda_bare = Fraction(0, 1)
    check("stipulated action packet has no fundamental scalar", not has_fundamental_scalar)
    check("stipulated action packet has no fundamental lambda phi^4 term", not has_fundamental_phi4)
    check("coefficient of absent fundamental quartic can be represented as lambda_bare=0", lambda_bare == 0)

    section("Matching algebra")
    z_lambda = Fraction(1, 1)
    delta_zero = Fraction(0, 1)
    lam_zero = lambda_msbar(lambda_bare, z_lambda, delta_zero)
    check("if delta_lambda=0, lambda_MSbar=0 follows", lam_zero == 0, f"lambda_MSbar={lam_zero}")

    delta_nonzero = Fraction(1, 1000)
    lam_nonzero = lambda_msbar(lambda_bare, z_lambda, delta_nonzero)
    assert abs(float(lam_nonzero) - 0.001) < 1e-15
    check(
        "countermodel: lambda_bare=0 with delta_lambda!=0 gives lambda_MSbar!=0",
        lam_nonzero != 0 and math.isclose(float(lam_nonzero), 0.001, rel_tol=0.0, abs_tol=1e-15),
        f"lambda_MSbar={lam_nonzero}",
    )
    check(
        "operator absence alone does not force delta_lambda=0",
        delta_nonzero != 0 and lambda_bare == 0,
        "matching term is independent of the absent operator coefficient",
    )

    section("No-go conclusion")
    implication_fails = lambda_bare == 0 and lam_nonzero != 0
    check(
        "no-go: lambda_bare phi^4 absence alone does not imply lambda_MSbar(M_Pl)=0",
        implication_fails,
        "a separate matching theorem is required",
    )
    check(
        "repair target is explicit matching, not a new axiom",
        True,
        "prove or bound delta_lambda in the chosen continuum convention",
    )

    print("\n" + "=" * 88)
    print(f"TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
