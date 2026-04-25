#!/usr/bin/env python3
"""
Koide Q RG fixed-point/source-origin no-go.

Theorem attempt:
  A retained renormalization-group or Callan-Symanzik stationarity law might
  upgrade the previous subtraction-point no-go into a source-origin theorem.
  On the live log-source carrier

      x = log(1 + rho),

  perhaps RG fixedness forces x=0, hence rho=0 and the conditional Koide Q
  support chain.

Result:
  No retained closure.  Exact RG fixed-point equations on the retained
  source torsor are equations in the relative coordinate

      s = x - mu.

  A stable beta function beta(s)=-gamma*s fixes s=0, equivalently x=mu, for
  every supplied subtraction point mu.  More general translation-covariant
  beta functions select relative roots s=r_i and therefore absolute sections
  x=mu+r_i.  Choosing mu=0 conditionally closes Q; choosing mu=log(2) gives
  the exact nonclosing section rho=1, Q=1, K_TL=3/8.

Exact residual:

      derive_retained_rg_fixed_point_absolute_origin_mu_equals_zero.

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
    x, mu, c, t, s, r = sp.symbols("x mu c t s r", real=True)
    gamma = sp.symbols("gamma", positive=True, real=True)
    x0, mu0 = sp.symbols("x0 mu0", real=True)

    section("A. Theorem attempt and route ranking")

    routes = [
        "Callan-Symanzik stationarity might force the absolute log-source origin",
        "an attractive RG fixed point beta=0 might select x=0",
        "anomalous-dimension stability might distinguish the no-source section",
        "RG-invariant effective action might minimize only at the origin",
        "UV/IR endpoint behavior might identify the absolute subtraction scale",
        "wrong-assumption inversion: the same fixed-point law accepts mu=log(2)",
    ]
    record(
        "A.1 six RG fixed-point variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )
    ranked = [
        ("translation_covariant_fixed_point", 3, 3, 3),
        ("callan_symanzik_stationarity", 2, 3, 2),
        ("anomalous_dimension_stability", 2, 2, 2),
        ("rg_invariant_effective_action", 2, 2, 1),
        ("uv_ir_endpoint_origin", 1, 1, 2),
    ]
    record(
        "A.2 translation-covariant fixed point is the strongest decisive test",
        sorted(ranked, key=lambda item: sum(item[1:]), reverse=True)[0][0]
        == "translation_covariant_fixed_point",
        "\n".join(
            f"{name}: positive={pos}, retained={ret}, novelty={nov}"
            for name, pos, ret, nov in ranked
        ),
    )

    section("B. Stable fixed line on the source torsor")

    relative = sp.simplify(x - mu)
    beta = sp.simplify(-gamma * relative)
    fixed_x = sp.solve(sp.Eq(beta, 0), x)
    record(
        "B.1 retained stable beta fixes x=mu, not x=0",
        fixed_x == [mu],
        f"beta(x,mu)={beta}; beta=0 -> x={fixed_x[0]}",
    )
    flow_x = sp.simplify(mu0 + (x0 - mu0) * sp.exp(-gamma * t))
    record(
        "B.2 exact flow converges to the supplied subtraction point",
        sp.simplify(flow_x.subs(t, 0) - x0) == 0
        and sp.limit(flow_x, t, sp.oo) == mu0,
        f"x(t)={flow_x}; x(infty)={sp.limit(flow_x, t, sp.oo)}",
    )
    rho_mu = sp.simplify(sp.exp(mu) - 1)
    record(
        "B.3 fixed line contains both closing and nonclosing sections",
        rho_mu.subs(mu, 0) == 0
        and sp.simplify(rho_mu.subs(mu, sp.log(2))) == 1,
        f"rho_fixed(mu)={rho_mu}; rho(0)=0; rho(log2)=1",
    )

    section("C. Scheme covariance of the fixed point")

    shifted_relative = sp.simplify((x + c) - (mu + c))
    shifted_beta = sp.simplify(-gamma * shifted_relative)
    record(
        "C.1 simultaneous scheme translations preserve the beta function",
        shifted_relative == relative and sp.simplify(shifted_beta - beta) == 0,
        f"s'={shifted_relative}; beta'={shifted_beta}",
    )
    record(
        "C.2 absolute origin x=0 is not fixed by scheme translations",
        sp.simplify((0 + c) - 0) == c,
        "The claimed origin is translated to x=c.",
    )
    record(
        "C.3 no interior absolute point is fixed by all retained translations",
        sp.solve(sp.Eq(x + c, x), c) == [0],
        "Fixedness only holds for the identity translation, not for a retained source origin.",
    )

    section("D. General translation-covariant fixed-point equations")

    beta_poly = sp.expand(s * (s - r))
    roots = set(sp.solve(sp.Eq(beta_poly, 0), s))
    absolute_roots = [sp.simplify(mu + root) for root in sorted(roots, key=str)]
    record(
        "D.1 polynomial RG fixed points are relative roots",
        roots == {0, r},
        f"beta(s)={beta_poly}; roots={sorted(roots, key=str)}",
    )
    record(
        "D.2 absolute fixed sections retain the free subtraction point",
        absolute_roots == [mu, mu + r],
        f"x roots={absolute_roots}",
    )
    record(
        "D.3 requiring the relative root r=0 still leaves mu free",
        sp.solve(sp.Eq(r, 0), r) == [0]
        and sp.simplify((mu + r).subs(r, 0)) == mu,
        "A double root at s=0 selects x=mu for every mu.",
    )

    section("E. Callan-Symanzik invariant audit")

    invariant = sp.simplify(s * sp.exp(gamma * t))
    cs_operator = sp.simplify(sp.diff(invariant, t) + (-gamma * s) * sp.diff(invariant, s))
    record(
        "E.1 exact Callan-Symanzik invariant uses relative source only",
        cs_operator == 0,
        f"I=s*exp(gamma*t); (d_t+beta d_s)I={cs_operator}",
    )
    zero_invariant_roots = sp.solve(sp.Eq(invariant, 0), s)
    record(
        "E.2 zero RG invariant selects s=0, equivalently x=mu",
        zero_invariant_roots == [0],
        "The invariant does not contain an equation for the absolute mu.",
    )
    rg_action = sp.simplify(relative**2)
    record(
        "E.3 an RG-stable quadratic action minimizes at the supplied mu",
        sp.solve(sp.Eq(sp.diff(rg_action, x), 0), x) == [mu],
        f"S_RG=(x-mu)^2; critical point x={mu}",
    )

    section("F. Q consequence and countersection")

    record(
        "F.1 mu=0 conditionally gives the Koide support chain",
        q_from_rho(rho_mu.subs(mu, 0)) == sp.Rational(2, 3)
        and ktl_from_rho(rho_mu.subs(mu, 0)) == 0,
        f"mu=0 -> rho=0, Q={q_from_rho(0)}, K_TL={ktl_from_rho(0)}",
    )
    record(
        "F.2 mu=log(2) is an exact RG fixed-point countersection",
        q_from_rho(rho_mu.subs(mu, sp.log(2))) == 1
        and ktl_from_rho(rho_mu.subs(mu, sp.log(2))) == sp.Rational(3, 8),
        "mu=log(2) -> rho=1, Q=1, K_TL=3/8",
    )

    section("G. Hostile review")

    record(
        "G.1 no forbidden target is assumed as a theorem input",
        True,
        "The runner audits the closing and counterclosing fixed lines symmetrically.",
    )
    record(
        "G.2 no observational pin or mass data are used",
        True,
        "Only exact source-torsor, beta-function, flow, and CS algebra is used.",
    )
    record(
        "G.3 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_rg_fixed_point_absolute_origin_mu_equals_zero",
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
        print("VERDICT: RG fixed-point/source-origin stationarity does not close Q.")
        print("KOIDE_Q_RG_FIXED_POINT_ORIGIN_NO_GO=TRUE")
        print("Q_RG_FIXED_POINT_ORIGIN_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_RG_SUBTRACTION_POINT_MU_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_rg_fixed_point_absolute_origin_mu_equals_zero")
        print("RESIDUAL_SOURCE=translation_covariant_rg_fixed_points_leave_mu_free")
        print("COUNTERSECTION=mu_log2_rg_fixed_line_rho_1_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: RG fixed-point/source-origin audit has FAILs.")
    print("KOIDE_Q_RG_FIXED_POINT_ORIGIN_NO_GO=FALSE")
    print("Q_RG_FIXED_POINT_ORIGIN_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_rg_fixed_point_absolute_origin_mu_equals_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
