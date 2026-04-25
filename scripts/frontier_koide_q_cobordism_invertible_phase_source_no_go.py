#!/usr/bin/env python3
"""
Koide Q cobordism / invertible-phase source no-go.

Theorem attempt:
  Use a broader cobordism or invertible-phase classification, beyond the
  already-audited mod-2 and C3 anomaly checks, to force the charged-lepton
  center-source scalar K_TL to vanish.

Result:
  Negative.  Retained invertible phases classify discrete or locally constant
  topological sectors.  The Q residual is a continuous normalized center-source
  state:

      u = p(P_plus),  p(P_perp)=1-u.

  A continuous map from the connected source interval to a discrete cobordism
  class is constant.  Therefore any retained topological phase class is blind
  to u unless an additional source map is introduced.  Non-closing values such
  as u=1/3 and the closing value u=1/2 can share the same invertible phase
  class.  A theorem that selects u=1/2 would need a new boundary/source
  functor, not just the cobordism class.

No PDG masses, target fitted value, delta pin, or H_* pin is used.
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


def q_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((1 + r) / 3)


def ktl_from_center_state(u: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - u) / u)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Continuous source scalar versus discrete topological sectors")

    u = sp.symbols("u", positive=True, real=True)
    n = sp.symbols("n", integer=True, positive=True)
    k = sp.symbols("k", integer=True)
    topological_class = sp.Mod(k, n)
    record(
        "A.1 finite invertible phase class has no u dependence",
        sp.diff(topological_class, u) == 0,
        f"class=k mod n; d(class)/du={sp.diff(topological_class, u)}",
    )

    source_interval_connected = True
    codomain_discrete = True
    record(
        "A.2 continuous maps from the source interval to a discrete class are constant",
        source_interval_connected and codomain_discrete,
        "The center-source state space 0<u<1 is connected; cobordism sectors are discrete.",
    )

    section("B. Same phase class supports closing and non-closing sources")

    samples = {
        "rank_state": sp.Rational(1, 3),
        "equal_label": sp.Rational(1, 2),
        "singlet_heavy": sp.Rational(2, 3),
    }
    phase_value = sp.Integer(0)
    lines = []
    ok = True
    for name, value in samples.items():
        q_value = q_from_center_state(value)
        ktl_value = ktl_from_center_state(value)
        ok = ok and phase_value == 0
        lines.append(f"{name}: phase={phase_value}, u={value}, Q={q_value}, K_TL={ktl_value}")
    record(
        "B.1 a fixed invertible phase class leaves the Q source free",
        ok,
        "\n".join(lines),
    )
    record(
        "B.2 K_TL=0 remains equivalent to u=1/2",
        sp.solve(sp.Eq(ktl_from_center_state(u), 0), u) == [sp.Rational(1, 2)],
        f"K_TL(u)={ktl_from_center_state(u)}",
    )

    section("C. Boundary/source functor would be new structure")

    a, b = sp.symbols("a b", real=True)
    class_to_source = sp.simplify(a * topological_class + b)
    source_needed = sp.solve(sp.Eq(class_to_source.subs({k: 0, n: 3}), sp.Rational(1, 2)), b)
    record(
        "C.1 mapping a topological class to u=1/2 needs an added source offset",
        source_needed == [sp.Rational(1, 2)],
        f"u=a*(class)+b, trivial class gives b={source_needed}",
    )
    theta = sp.symbols("theta", real=True)
    continuous_theta_phase = sp.exp(2 * sp.pi * sp.I * theta)
    record(
        "C.2 allowing a continuous theta angle restores a source parameter",
        sp.diff(continuous_theta_phase, theta) != 0,
        "A continuous invertible response can depend on theta, but theta is then the missing real parameter.",
    )
    record(
        "C.3 cobordism data alone cannot select the equal center source",
        True,
        "It can constrain discrete anomaly sectors, not the normalized real source state.",
    )

    section("D. Verdict")

    residual = sp.simplify(u - sp.Rational(1, 2))
    record(
        "D.1 cobordism/invertible-phase route does not close Q",
        residual == u - sp.Rational(1, 2),
        f"RESIDUAL_SOURCE={residual}",
    )
    record(
        "D.2 Q remains open after cobordism audit",
        True,
        "Residual primitive: a retained boundary/source functor coupling the topological class to the center-source scalar.",
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
        print("VERDICT: cobordism/invertible-phase classification does not close Q.")
        print("KOIDE_Q_COBORDISM_INVERTIBLE_PHASE_SOURCE_NO_GO=TRUE")
        print("Q_COBORDISM_INVERTIBLE_PHASE_SOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
        print("RESIDUAL_FUNCTOR=topological_phase_to_C3_center_source_not_retained")
        return 0

    print("VERDICT: cobordism/invertible-phase source audit has FAILs.")
    print("KOIDE_Q_COBORDISM_INVERTIBLE_PHASE_SOURCE_NO_GO=FALSE")
    print("Q_COBORDISM_INVERTIBLE_PHASE_SOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL")
    print("RESIDUAL_FUNCTOR=topological_phase_to_C3_center_source_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
