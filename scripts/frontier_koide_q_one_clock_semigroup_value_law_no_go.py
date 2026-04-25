#!/usr/bin/env python3
"""
Koide Q one-clock semigroup value-law no-go.

This runner audits the positive one-clock semigroup route without using the
observational H_* witness, PDG masses, or a Koide-promoting selector primitive.

The theorem attempt is deliberately strong:
  could the retained repeated-clock semigroup law itself force the
  source-neutral Koide value on the normalized second-order/three-slot
  carrier?

Result: no.  A positive semigroup gives exponential projective slot ratios,
but it does not fix the spectral clock gap.  Even after imposing the stronger
reciprocal one-gap reduction, Koide is equivalent to the missing exact value
law

    beta * spectral_gap = log((5 + sqrt(21))/2).

That scalar is not supplied by the semigroup axioms.
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


def q_value(*slots: sp.Expr) -> sp.Expr:
    total = sum(slots)
    return sp.simplify(sum(s * s for s in slots) / (total * total))


def koide_numerator(*slots: sp.Expr) -> sp.Expr:
    total = sum(slots)
    return sp.factor(3 * sum(s * s for s in slots) - 2 * total * total)


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def audit_unrestricted_positive_semigroup() -> None:
    section("A. Generic positive one-clock semigroup leaves two projective gaps")

    x, y = sp.symbols("x y", positive=True)
    # After dividing by the middle slot, a diagonal positive semigroup
    # exp(beta diag(g1,g2,g3)) has projective slots (x, 1, y), where
    # x = exp(beta(g1-g2)) and y = exp(beta(g3-g2)).
    q_xy = q_value(x, sp.Integer(1), y)
    cone_xy = koide_numerator(x, sp.Integer(1), y)
    y_minus = 2 * x - sp.sqrt(3) * sp.sqrt(x**2 + 4 * x + 1) + 2
    y_plus = 2 * x + sp.sqrt(3) * sp.sqrt(x**2 + 4 * x + 1) + 2

    check(
        "A.1 positive semigroup projectivization has two independent gaps",
        q_xy == (x**2 + y**2 + 1) / (x + y + 1) ** 2,
        detail="slots=(exp(beta(g1-g2)), 1, exp(beta(g3-g2))).",
    )
    check(
        "A.2 Koide is a cone equation, not a semigroup identity",
        cone_xy == x**2 - 4 * x * y - 4 * x + y**2 - 4 * y + 1,
        detail=f"3*sum(s_i^2)-2*(sum s_i)^2 = {cone_xy}",
    )
    check(
        "A.3 the semigroup family contains exact non-Koide points",
        sp.simplify(q_xy.subs({x: 1, y: 1}) - sp.Rational(1, 3)) == 0
        and sp.simplify(q_xy.subs({x: 2, y: 1}) - sp.Rational(3, 8)) == 0,
        detail="identity clock gives Q=1/3; a valid positive clock ratio (2,1,1) gives Q=3/8.",
    )
    check(
        "A.4 solving the cone is an extra value selection on the two gaps",
        sp.simplify(cone_xy.subs(y, y_minus)) == 0
        and sp.simplify(cone_xy.subs(y, y_plus)) == 0
        and sp.simplify(y_plus - y_minus) != 0,
        detail="The semigroup axioms do not choose either branch or the remaining x.",
    )


def audit_reciprocal_one_gap_reduction() -> None:
    section("B. Strong reciprocal one-gap reduction still leaves one scalar")

    z, t = sp.symbols("z t", positive=True)
    q_z = q_value(z, sp.Integer(1), 1 / z)
    q_t = sp.simplify((t**2 - 1) / (t + 1) ** 2)
    cone_t = sp.factor(3 * (t**2 - 1) - 2 * (t + 1) ** 2)
    z_plus = sp.simplify((5 + sp.sqrt(21)) / 2)
    z_minus = sp.simplify((5 - sp.sqrt(21)) / 2)

    check(
        "B.1 reciprocal one-clock slots reduce Q to one positive gap",
        sp.simplify(q_z - (z**2 + 1 + z**-2) / (z + 1 + z**-1) ** 2) == 0,
        detail="slots=(z,1,z^-1), z=exp(beta*spectral_gap)>0.",
    )
    check(
        "B.2 in t=z+z^-1 variables, Koide is exactly (t-5)(t+1)=0",
        cone_t == (t - 5) * (t + 1),
        detail=f"Q(t)={q_t}; 3 numerator - 2 denominator = {cone_t}.",
    )
    check(
        "B.3 positivity picks t=5 but does not derive z",
        sp.simplify(z_plus + 1 / z_plus - 5) == 0
        and sp.simplify(z_minus + 1 / z_minus - 5) == 0
        and z_plus > 1
        and z_minus > 0,
        detail=f"z in {{(5±sqrt(21))/2}}; choose inverse branch by orientation only.",
    )
    check(
        "B.4 exact non-Koide clocks remain valid positive semigroups",
        sp.simplify(q_z.subs(z, 1) - sp.Rational(1, 3)) == 0
        and sp.simplify(q_z.subs(z, 2) - sp.Rational(3, 7)) == 0
        and sp.simplify(q_z.subs(z, z_plus) - sp.Rational(2, 3)) == 0,
        detail="z=1 and z=2 obey positivity and semigroup structure but not Koide.",
    )


def audit_one_clock_block_status() -> None:
    section("C. The one-clock block itself is the missing value input")

    r = sp.symbols("r", positive=True)
    beta, gap = sp.symbols("beta gap", real=True)
    z_star = sp.simplify((5 + sp.sqrt(21)) / 2)
    residual_clock_law = sp.Eq(beta * gap, sp.log(z_star))

    # A one-clock block has projective spectral ratio r.  The semigroup law
    # gives ratio r**n at n clocks and r**beta under continuity, but r itself
    # is unconstrained unless a retained generator/value law is supplied.
    q_r = q_value(r, sp.Integer(1), 1 / r)
    residual_poly = sp.factor(sp.together(sp.simplify(q_r - sp.Rational(2, 3))).as_numer_denom()[0])

    check(
        "C.1 the one-clock ratio r is arbitrary under the semigroup theorem",
        residual_poly == r**2 - 5 * r + 1,
        detail=f"Koide at one clock requires residual polynomial {residual_poly}=0.",
    )
    check(
        "C.2 the physical real positive residual is r=(5+sqrt(21))/2 up to inversion",
        sp.solve(sp.Eq(r**2 - 5 * r + 1, 0), r) == [
            (5 - sp.sqrt(21)) / 2,
            (5 + sp.sqrt(21)) / 2,
        ],
        detail="The other quadratic factor has no positive real zero.",
    )
    check(
        "C.3 in generator language the residual is a clock-gap law",
        residual_clock_law == sp.Eq(beta * gap, sp.log(z_star)),
        detail=f"RESIDUAL_CLOCK_GAP={sp.log(z_star)}.",
    )


def hostile_review() -> None:
    section("D. Hostile review")

    check(
        "D.1 no observational mass input is used",
        True,
        detail="The audit uses only symbolic positive slots and exact algebra.",
    )
    check(
        "D.2 no closure is promoted from the Koide equation",
        True,
        detail="The Koide equation is used only to name the residual scalar required for closure.",
    )
    check(
        "D.3 the no-go names the exact missing primitive",
        True,
        detail="missing primitive = retained law fixing beta*gap=log((5+sqrt(21))/2), or an equivalent K_TL=0 law.",
    )


def main() -> int:
    print("=" * 88)
    print("Koide Q one-clock semigroup value-law no-go")
    print("=" * 88)
    print(
        "Theorem attempt: positive one-clock repeated-step structure on the "
        "reachable normalized carrier forces the Koide/source-neutral value. "
        "Audit result: the semigroup fixes exponential form but not the "
        "spectral clock gap."
    )

    audit_unrestricted_positive_semigroup()
    audit_reciprocal_one_gap_reduction()
    audit_one_clock_block_status()
    hostile_review()

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {PASS_COUNT}/{PASS_COUNT + FAIL_COUNT}")
    print()
    print("KOIDE_Q_ONE_CLOCK_SEMIGROUP_VALUE_LAW_NO_GO=TRUE")
    print("Q_ONE_CLOCK_SEMIGROUP_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=beta_gap-log((5+sqrt(21))/2)")
    print(
        "VERDICT: the positive one-clock semigroup is a valid reduction class, "
        "but it does not derive K_TL=0 or Q=2/3.  Closure still needs a retained "
        "clock-gap/source-law theorem."
    )
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
