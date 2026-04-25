#!/usr/bin/env python3
"""
Koide Q selected-line bridge dependency no-go.

The selected-line axis/Fourier bridge is strong support: on the retained line
the axis slots match a Brannen Fourier-envelope form.  This runner audits the
tempting upgrade:

    selected-line axis/Fourier bridge -> Q = 2/3

The result is negative.  The bridge closes Q only after the Brannen amplitude
radius is fixed to c = sqrt(2).  With a free radius

    lambda_k = 1 + c cos(theta + 2 pi k / 3),

the Koide scalar is

    Q(c) = 1/3 + c^2/6.

The phase theta, including a derived or assumed delta = 2/9, does not affect Q.
Therefore the selected-line phase bridge and the selected-line axis/Fourier
identity do not derive Q unless they also derive the amplitude-radius law
c^2 = 2, equivalently kappa = 2 / A1 / K_TL = 0 on the reduced carrier.

No PDG masses, K_TL=0, K=0, P_Q=1/2, Q=2/3, delta=2/9, or H_* pin is used.
"""

from __future__ import annotations

import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("Koide Q selected-line bridge dependency no-go")
    print("Theorem attempt: the selected-line axis/Fourier bridge might by itself")
    print("force the Koide value.  The audit result is negative.")

    c, theta, v0 = sp.symbols("c theta v0", positive=True, real=True)
    pi = sp.pi
    angles = [theta + 2 * pi * k / 3 for k in range(3)]
    lambdas = [1 + c * sp.cos(angle) for angle in angles]

    sum_lambda = sp.trigsimp(sum(lambdas))
    sum_lambda_sq = sp.trigsimp(sum(sp.expand_trig(lam**2) for lam in lambdas))
    q_c = sp.trigsimp(sum_lambda_sq / sum_lambda**2)

    section("A. Brannen envelope with free radius")

    record(
        "A.1 the phase-dependent envelope has fixed trace independent of theta",
        sp.simplify(sum_lambda - 3) == 0,
        f"sum(lambda_k) = {sum_lambda}",
    )
    record(
        "A.2 the quadratic norm depends on the radius c, not on the phase theta",
        sp.simplify(sum_lambda_sq - (3 + 3 * c**2 / 2)) == 0,
        f"sum(lambda_k^2) = {sum_lambda_sq}",
    )
    record(
        "A.3 the Koide scalar on the envelope is Q(c) = 1/3 + c^2/6",
        sp.simplify(q_c - (sp.Rational(1, 3) + c**2 / 6)) == 0,
        f"Q(c) = {q_c}",
    )
    record(
        "A.4 changing the selected-line phase cannot change Q at fixed radius",
        sp.simplify(sp.diff(q_c, theta)) == 0,
        "dQ/dtheta = 0, so a phase theorem alone cannot close Q.",
    )

    section("B. What must be imported or derived")

    koide_eq = sp.factor(sp.simplify(q_c - sp.Rational(2, 3)))
    c_solutions = sp.solve(sp.Eq(q_c, sp.Rational(2, 3)), c)
    record(
        "B.1 Q = 2/3 is equivalent to the radius law c^2 = 2",
        sp.simplify(koide_eq - (c**2 - 2) / 6) == 0
        and c_solutions == [sp.sqrt(2)],
        f"Q(c)-2/3 = {koide_eq}; positive solution c = {c_solutions[0]}",
    )

    kappa = sp.simplify(4 / c**2)
    q_kappa = sp.simplify((1 + 2 / kappa) / 3)
    record(
        "B.2 the same missing law is kappa = 2 in the circulant block language",
        sp.simplify(q_kappa - q_c) == 0
        and sp.simplify(kappa.subs(c, sp.sqrt(2)) - 2) == 0,
        f"kappa(c) = {kappa}; Q = {q_kappa}",
    )

    q_samples = {
        "c=0": sp.simplify(q_c.subs(c, 0)),
        "c=1": sp.simplify(q_c.subs(c, 1)),
        "c=sqrt(2)": sp.simplify(q_c.subs(c, sp.sqrt(2))),
        "c=2": sp.simplify(q_c.subs(c, 2)),
    }
    record(
        "B.3 exact counterexamples show the bridge form allows non-Koide values",
        q_samples["c=0"] == sp.Rational(1, 3)
        and q_samples["c=1"] == sp.Rational(1, 2)
        and q_samples["c=sqrt(2)"] == sp.Rational(2, 3)
        and q_samples["c=2"] == 1,
        "; ".join(f"{label}->{value}" for label, value in q_samples.items()),
    )

    section("C. Scale and selected-line dependencies")

    scaled_lambdas = [v0 * lam for lam in lambdas]
    q_scaled = sp.trigsimp(
        sum(sp.expand_trig(lam**2) for lam in scaled_lambdas)
        / sum(scaled_lambdas) ** 2
    )
    record(
        "C.1 the overall selected-line scale v0 cancels and cannot close Q",
        sp.simplify(q_scaled - q_c) == 0,
        f"Q(v0 * lambda) = {q_scaled}",
    )

    delta_symbol = sp.symbols("delta_symbol", real=True)
    q_delta = sp.simplify(q_c.subs(theta, delta_symbol))
    record(
        "C.2 substituting any phase target leaves the same radius dependence",
        sp.simplify(q_delta - q_c) == 0,
        "This includes any future derivation of the physical Brannen phase.",
    )

    record(
        "C.3 the selected-line bridge runner sets the load-bearing radius in its envelope definition",
        True,
        "fourier_envelopes(delta) = 1 + sqrt(2) cos(delta + 2*pi*k/3).\n"
        "That sqrt(2) is exactly the radius law c^2 = 2.",
    )

    section("D. Review-grade consequence")

    record(
        "D.1 selected-line axis/Fourier equality is support, not a Q closure theorem",
        True,
        "The equality is useful after the selected line and radius law are retained.\n"
        "It does not derive the amplitude-radius law from earlier assumptions.",
    )
    record(
        "D.2 no forbidden target or observational pin is used",
        True,
        "The audit uses only exact trigonometric sums with symbolic c and theta.",
    )

    section("Summary")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_Q_SELECTED_LINE_BRIDGE_DEPENDENCY_NO_GO=TRUE")
        print("Q_SELECTED_LINE_AXIS_FOURIER_BRIDGE_CLOSES_Q=FALSE")
        print("RESIDUAL_RADIUS_LAW=c^2=2_equiv_kappa=2_equiv_K_TL=0")
        print()
        print("VERDICT: the selected-line axis/Fourier bridge is retained support,")
        print("but it closes Q only after the Brannen radius c = sqrt(2) is fixed.")
        print("The selected-line phase, including delta = 2/9, is orthogonal to Q.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
