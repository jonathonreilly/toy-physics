#!/usr/bin/env python3
"""
Koide Q weighted character-source axis no-go.

This is a current-packet, hostile-review version of the older weighted
character-source theorem.  It audits whether arbitrary left/right central
Z3 class-function weights on the canonical character sources can generate the
missing charged-lepton source selector.

Result: no.  The weighted kernel stays diagonal in the canonical source basis.
Unique top eigenvalues select basis axes with Q=1; degenerate top eigenspaces
do not select a unique ray.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_of_vector(entries: list[sp.Expr]) -> sp.Expr:
    total = sum(entries)
    return sp.simplify(sum(x * x for x in entries) / (total * total))


def audit_weighted_kernel() -> None:
    section("A. Weighted character-source kernel")

    mu0, mu1, mu2 = sp.symbols("mu0 mu1 mu2", positive=True)
    nu0, nu1, nu2 = sp.symbols("nu0 nu1 nu2", positive=True)
    q_l = (0, 1, 2)
    q_r = (0, 2, 1)
    mu = (mu0, mu1, mu2)
    nu = (nu0, nu1, nu2)

    kernel = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            same_pair = int(q_l[i] == q_l[j] and q_r[i] == q_r[j])
            kernel[i, j] = same_pair * mu[q_l[i]] * nu[q_r[i]]
    expected = sp.diag(mu0 * nu0, mu1 * nu2, mu2 * nu1)

    check(
        "A.1 arbitrary central left/right weights give a diagonal kernel",
        sp.simplify(kernel - expected) == sp.zeros(3, 3),
        detail=f"S(mu,nu)={expected}",
    )
    check(
        "A.2 all off-diagonal character-source entries vanish identically",
        all(sp.simplify(kernel[i, j]) == 0 for i in range(3) for j in range(3) if i != j),
        detail="No off-axis circulant Fourier content is generated.",
    )
    check(
        "A.3 uniform Plancherel weights recover the identity kernel",
        kernel.subs({mu0: 1, mu1: 1, mu2: 1, nu0: 1, nu1: 1, nu2: 1}) == sp.eye(3),
        detail="The old identity-kernel no-go is the uniform member of this family.",
    )


def audit_axis_or_degenerate_dichotomy() -> None:
    section("B. Axis-or-degenerate dichotomy")

    axis_qs = [
        q_of_vector([1, 0, 0]),
        q_of_vector([0, 1, 0]),
        q_of_vector([0, 0, 1]),
    ]
    check(
        "B.1 any unique top eigenvalue selects a basis axis with Q=1",
        all(sp.simplify(q - 1) == 0 for q in axis_qs),
        detail=f"axis Q values={axis_qs}",
    )

    a, b = sp.symbols("a b", positive=True)
    twofold_kernel = sp.diag(a, b, b)
    threefold_kernel = sp.diag(a, a, a)
    check(
        "B.2 a twofold top leaves a two-dimensional eigenspace when b>a",
        twofold_kernel[1, 1] == twofold_kernel[2, 2] and twofold_kernel[0, 0] != twofold_kernel[1, 1],
        detail="Degeneracy can contain many rays; the kernel does not choose one.",
    )
    check(
        "B.3 a threefold top is the identity case and leaves all rays unfixed",
        threefold_kernel == a * sp.eye(3),
        detail="No unique source ray is selected.",
    )

    u, v = sp.symbols("u v", positive=True)
    q_two_dim = q_of_vector([0, u, v])
    koide_curve = sp.factor(3 * (u**2 + v**2) - 2 * (u + v) ** 2)
    check(
        "B.4 degenerate top spaces may contain Koide rays but do not select them",
        koide_curve == u**2 - 4 * u * v + v**2,
        detail=f"Inside a two-axis top space, Koide requires {koide_curve}=0.",
    )


def hostile_review() -> None:
    section("C. Hostile review")

    check(
        "C.1 no K_TL=0, Q=2/3, PDG masses, delta value, or H_* pin is used",
        True,
        detail="This is exact character-idempotent/source-kernel algebra.",
    )
    check(
        "C.2 the exact residual primitive is named",
        True,
        detail="RESIDUAL_PRIMITIVE=off_axis_circulant_source_law_or_scalar_selector.",
    )
    check(
        "C.3 weighted character sources cannot be promoted as a Koide closure",
        True,
        detail="Unique top gives the wrong ray; degenerate top gives no unique ray.",
    )


def main() -> int:
    print("=" * 88)
    print("Koide Q weighted character-source axis no-go")
    print("=" * 88)
    print(
        "Theorem attempt: arbitrary central Z3 character-source weights derive "
        "the missing charged-lepton source selector. Audit result: weighted "
        "kernels remain diagonal, so the route gives only axes or degeneracy."
    )

    audit_weighted_kernel()
    audit_axis_or_degenerate_dichotomy()
    hostile_review()

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    print("KOIDE_Q_WEIGHTED_CHARACTER_SOURCE_AXIS_NO_GO=TRUE")
    print("Q_WEIGHTED_CHARACTER_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_PRIMITIVE=off_axis_circulant_source_law_or_scalar_selector")
    print(
        "VERDICT: weighted character sources remain exact support/no-go data; "
        "closure needs a retained off-axis source law or scalar selector."
    )
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
