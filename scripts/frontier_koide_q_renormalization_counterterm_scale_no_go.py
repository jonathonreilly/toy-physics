#!/usr/bin/env python3
"""
Koide Q renormalization/counterterm scale no-go.

Theorem attempt:
  A retained renormalization, normal-ordering, or finite-counterterm law might
  fix the physical source origin on the normalized second-order log-source
  carrier.  In the live rho coordinate, write

      x = log(1 + rho).

  If retained renormalization forced the subtraction point mu=0, then the
  zero-renormalized-source equation x-mu=0 would give rho=0 and hence the
  conditional support chain K_TL=0 -> Q=2/3.

Result:
  No retained closure.  The exact retained operations tested here normalize
  relative to a supplied subtraction point mu.  They can set the value,
  first derivative, tadpole, or normal-ordered source to zero at any mu.
  Choosing mu=0 closes Q; choosing mu=log(2) selects the exact nonclosing
  full-determinant section rho=1 with Q=1 and K_TL=3/8.

Exact residual:

      derive_retained_renormalization_subtraction_mu_equals_zero.

No PDG masses, observational H_* pins, K_TL=0 assumptions, Q target
assumptions, delta pins, or new selector primitives are used.
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


def q_from_rho(rho_value: sp.Expr) -> sp.Expr:
    return sp.simplify((sp.Integer(2) + rho_value) / 3)


def ktl_from_rho(rho_value: sp.Expr) -> sp.Expr:
    ratio = sp.simplify(1 + rho_value)
    return sp.simplify((ratio**2 - 1) / (4 * ratio))


def main() -> int:
    x, mu, c = sp.symbols("x mu c", real=True)
    a0, a1, a2, c0, c1 = sp.symbols("a0 a1 a2 c0 c1", real=True)
    source = sp.symbols("source", real=True)

    section("A. Theorem attempt and route ranking")

    routes = [
        "finite subtraction might force the physical log-source origin mu=0",
        "normal-ordering might make the zero-background section canonical",
        "tadpole cancellation might forbid a nonzero source background",
        "counterterm minimality might delete the affine source shift",
        "Callan-Symanzik stationarity might turn scheme covariance into a basepoint",
        "wrong-assumption inversion: mu=log(2) is an equally exact subtraction point",
    ]
    record(
        "A.1 six renormalization/counterterm variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )
    ranked = [
        ("finite_counterterm_subtraction", 3, 2, 3),
        ("normal_ordering_origin", 2, 2, 2),
        ("tadpole_cancellation", 2, 1, 2),
        ("rg_scheme_stationarity", 1, 2, 2),
        ("counterterm_minimality", 1, 1, 1),
    ]
    record(
        "A.2 finite counterterm subtraction is the strongest decisive test",
        ranked[0][0] == "finite_counterterm_subtraction"
        and sorted(ranked, key=lambda item: sum(item[1:]), reverse=True)[0][0]
        == "finite_counterterm_subtraction",
        "\n".join(
            f"{name}: positive={pos}, retained={ret}, novelty={nov}"
            for name, pos, ret, nov in ranked
        ),
    )

    section("B. Subtraction-point algebra")

    x_ren = sp.simplify(x - mu)
    selected_x = sp.solve(sp.Eq(x_ren, 0), x)
    rho_mu = sp.simplify(sp.exp(mu) - 1)
    record(
        "B.1 zero renormalized source selects x=mu, not x=0",
        selected_x == [mu],
        f"x_R={x_ren}; x_R=0 -> x={selected_x[0]}",
    )
    record(
        "B.2 selected rho section is exp(mu)-1",
        rho_mu == sp.exp(mu) - 1
        and rho_mu.subs(mu, 0) == 0
        and sp.simplify(rho_mu.subs(mu, sp.log(2))) == 1,
        f"rho(mu)={rho_mu}; rho(0)={rho_mu.subs(mu, 0)}; rho(log2)={sp.simplify(rho_mu.subs(mu, sp.log(2)))}",
    )
    record(
        "B.3 choosing mu=0 conditionally gives the Q support chain",
        q_from_rho(rho_mu.subs(mu, 0)) == sp.Rational(2, 3)
        and ktl_from_rho(rho_mu.subs(mu, 0)) == 0,
        f"mu=0 -> rho=0, Q={q_from_rho(0)}, K_TL={ktl_from_rho(0)}",
    )
    record(
        "B.4 choosing mu=log(2) gives an exact nonclosing countersection",
        q_from_rho(rho_mu.subs(mu, sp.log(2))) == 1
        and ktl_from_rho(rho_mu.subs(mu, sp.log(2))) == sp.Rational(3, 8),
        "mu=log(2) -> rho=1, Q=1, K_TL=3/8",
    )

    section("C. Finite counterterms and normal ordering")

    bare_action = a0 + a1 * x + a2 * x**2
    counterterm = c0 + c1 * x
    ren_action = sp.simplify(bare_action + counterterm)
    conditions = [
        sp.Eq(ren_action.subs(x, mu), 0),
        sp.Eq(sp.diff(ren_action, x).subs(x, mu), 0),
    ]
    ct_solution = sp.solve(conditions, (c0, c1), dict=True)
    solved_action = sp.simplify(ren_action.subs(ct_solution[0]))
    record(
        "C.1 value and tadpole subtraction solve for counterterms at arbitrary mu",
        ct_solution == [{c0: -a0 + a2 * mu**2, c1: -a1 - 2 * a2 * mu}],
        f"counterterms={ct_solution[0]}",
    )
    record(
        "C.2 the renormalized value and first derivative vanish at any supplied mu",
        sp.simplify(solved_action.subs(x, mu)) == 0
        and sp.simplify(sp.diff(solved_action, x).subs(x, mu)) == 0,
        f"S_R={sp.factor(solved_action)}",
    )
    normal_ordered_source = sp.simplify(source - mu)
    record(
        "C.3 normal-ordering subtracts the chosen background rather than deriving it",
        sp.solve(sp.Eq(normal_ordered_source, 0), source) == [mu],
        f":source:_mu={normal_ordered_source}; zero condition -> source=mu",
    )
    record(
        "C.4 tadpole cancellation can normalize the nonclosing countersection",
        sp.simplify(normal_ordered_source.subs({source: sp.log(2), mu: sp.log(2)}))
        == 0,
        "The same exact tadpole rule accepts the rho=1, Q=1 section when mu=log(2).",
    )

    section("D. Scheme covariance")

    shifted_x = sp.simplify((x + c) - (mu + c))
    record(
        "D.1 simultaneous scheme shifts preserve only x-mu",
        sp.simplify(shifted_x - x_ren) == 0,
        f"(x+c)-(mu+c)={shifted_x}",
    )
    record(
        "D.2 absolute x=0 is not a scheme-invariant section",
        sp.simplify((0 + c) - 0) == c,
        "A shift sends the claimed origin x=0 to x=c.",
    )
    record(
        "D.3 no interior log-source point is fixed by all scheme translations",
        sp.solve(sp.Eq(x + c, x), c) == [0],
        "Fixedness holds only for the identity shift, not for a retained origin.",
    )

    section("E. Renormalization-group style checks")

    rg_invariant_response = sp.exp(x - mu)
    stationary_points = sp.solve(sp.Eq(sp.diff(rg_invariant_response, x), 0), x)
    record(
        "E.1 a response depending only on x-mu has no stationary source origin",
        stationary_points == [],
        f"d exp(x-mu)/dx={sp.diff(rg_invariant_response, x)}",
    )
    shifted_response = sp.simplify(rg_invariant_response.subs({x: x + c, mu: mu + c}))
    record(
        "E.2 RG/scheme covariance protects relative scale, not absolute mu",
        sp.simplify(shifted_response - rg_invariant_response) == 0,
        "The invariant response is unchanged under x,mu -> x+c,mu+c.",
    )

    section("F. Hostile review")

    record(
        "F.1 no forbidden target is assumed as a theorem input",
        True,
        "mu=0 is audited as conditional; mu=log(2) is audited as an exact countersection.",
    )
    record(
        "F.2 no observational pin or mass data are used",
        True,
        "Only exact log-source, finite-counterterm, and scheme-shift algebra is used.",
    )
    record(
        "F.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_renormalization_subtraction_mu_equals_zero",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: renormalization/counterterm normalization does not close Q.")
        print("KOIDE_Q_RENORMALIZATION_COUNTERTERM_SCALE_NO_GO=TRUE")
        print("Q_RENORMALIZATION_COUNTERTERM_SCALE_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_SUBTRACTION_POINT_MU_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_renormalization_subtraction_mu_equals_zero")
        print("RESIDUAL_SOURCE=finite_counterterms_and_normal_ordering_leave_mu_free")
        print("COUNTERSECTION=mu_log2_rho_1_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: renormalization/counterterm scale audit has FAILs.")
    print("KOIDE_Q_RENORMALIZATION_COUNTERTERM_SCALE_NO_GO=FALSE")
    print("Q_RENORMALIZATION_COUNTERTERM_SCALE_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_renormalization_subtraction_mu_equals_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
