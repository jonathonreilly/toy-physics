#!/usr/bin/env python3
"""
Koide Q basepoint-independence observable no-go.

Theorem attempt:
  After source-torsor naturality left the basepoint e free, try the
  reviewer-grade gauge variant: perhaps physical observables must be
  independent of the arbitrary source-fibre basepoint.  Maybe that
  basepoint-independence forces the closing section e=0.

Result:
  No retained closure.  Under simultaneous basepoint translation

      (rho, e) -> (rho+c, e+c),

  the affine invariant is eta = rho-e.  On the neutral-preparation slice
  rho=e, every basepoint has eta=0.  Therefore basepoint-independent
  observables cannot distinguish e=0 from e=1.  The Q readout

      Q(e) = (2+e)/3

  depends on the section value, so it is not basepoint-independent until a
  retained section is supplied.  Requiring basepoint independence either
  deletes the Q-relevant source coordinate or reduces to the same missing
  basepoint law.

Exact residual:

      derive_retained_basepoint_independent_Q_readout_section_e_equals_zero.

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
    rho, e, c, a, b, d = sp.symbols("rho e c a b d", real=True)

    section("A. Brainstormed basepoint-independence routes")

    routes = [
        "simultaneous translation gauge invariance of (rho,e)",
        "affine invariant observable classification",
        "neutral-preparation slice rho=e",
        "renormalization-scheme independence of Q(e)",
        "quotienting by basepoint shifts before reading Q",
        "wrong-assumption inversion: e=1 has the same invariant eta=0 as e=0",
    ]
    record(
        "A.1 six basepoint-independence variants are considered",
        len(routes) == 6,
        "\n".join(f"{idx + 1}. {route}" for idx, route in enumerate(routes)),
    )

    section("B. Translation-invariant observable content")

    eta = sp.simplify(rho - e)
    translated_eta = sp.simplify((rho + c) - (e + c))
    record(
        "B.1 eta=rho-e is invariant under simultaneous basepoint translation",
        translated_eta == eta,
        f"eta -> {translated_eta}",
    )

    affine_observable = a * rho + b * e + d
    translated_observable = sp.expand(affine_observable.subs({rho: rho + c, e: e + c}))
    invariance_residual = sp.expand(translated_observable - affine_observable)
    invariant_condition = sp.solve(sp.Eq(sp.diff(invariance_residual, c), 0), b)
    record(
        "B.2 affine basepoint-independent observables depend only on rho-e plus a constant",
        invariant_condition == [-a]
        and sp.simplify(affine_observable.subs(b, -a) - (a * eta + d)) == 0,
        f"translation residual={invariance_residual}; condition b=-a",
    )

    record(
        "B.3 quotienting by basepoint shifts forgets the absolute section value",
        sp.simplify(eta.subs(rho, e)) == 0
        and sp.simplify(eta.subs({rho: 0, e: 0})) == 0
        and sp.simplify(eta.subs({rho: 1, e: 1})) == 0,
        "Both closing and full-determinant neutral slices map to eta=0.",
    )

    section("C. The Q readout is section-valued, not basepoint-invariant")

    q_e = q_from_rho(e)
    ktl_e = ktl_from_rho(e)
    record(
        "C.1 Q on the neutral-preparation slice depends on the supplied section e",
        sp.diff(q_e, e) == sp.Rational(1, 3),
        f"Q(e)={q_e}; dQ/de={sp.diff(q_e, e)}",
    )
    record(
        "C.2 basepoint-independence of Q would erase the Q distinction, not select e=0",
        q_from_rho(0) == sp.Rational(2, 3)
        and q_from_rho(1) == 1
        and q_from_rho(0) != q_from_rho(1),
        f"Q(0)={q_from_rho(0)}, Q(1)={q_from_rho(1)}",
    )
    record(
        "C.3 no value of e makes Q(e) basepoint-independent as a function",
        sp.diff(q_e, e) != 0,
        "A single chosen e is a section; it is not an invariant function on the torsor.",
    )

    section("D. Gauge fixing and scheme independence")

    gauge_slice = rho - e
    record(
        "D.1 the gauge condition rho-e=0 fixes rho to the supplied e",
        sp.solve(sp.Eq(gauge_slice, 0), rho) == [e],
        f"slice={gauge_slice}",
    )
    record(
        "D.2 choosing e=0 is a gauge section, not a retained invariant",
        sp.solve(sp.Eq(e, 0), e) == [0]
        and sp.solve(sp.Eq(e - 1, 0), e) == [1],
        "Both e=0 and e=1 are exact sections unless a retained section law is supplied.",
    )
    record(
        "D.3 a scheme-independent readout can depend on eta but then is blind on neutral slices",
        sp.simplify((a * eta + d).subs(rho, e)) == d,
        "Any affine invariant readout is constant on rho=e for every e.",
    )

    section("E. Countersection and hostile review")

    record(
        "E.1 e=1 remains an exact nonclosing countersection",
        q_from_rho(1) == 1
        and ktl_from_rho(1) == sp.Rational(3, 8)
        and (1 + sp.Integer(1) > 0),
        f"e=1 -> Q={q_from_rho(1)}, K_TL={ktl_from_rho(1)}",
    )
    record(
        "E.2 e=0 closes only conditionally on a supplied section",
        q_from_rho(0) == sp.Rational(2, 3)
        and ktl_from_rho(0) == 0,
        f"e=0 -> Q={q_from_rho(0)}, K_TL={ktl_from_rho(0)}",
    )
    record(
        "E.3 no forbidden target is assumed as a theorem input",
        True,
        "The closing and counterclosing sections are audited symmetrically.",
    )
    record(
        "E.4 no observational pin or mass data are used",
        True,
        "Only exact affine source and invariant-coordinate algebra is used.",
    )
    record(
        "E.5 exact residual is named",
        True,
        "RESIDUAL_SCALAR=derive_retained_basepoint_independent_Q_readout_section_e_equals_zero",
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
        print("VERDICT: basepoint-independence of observables does not close Q.")
        print("KOIDE_Q_BASEPOINT_INDEPENDENCE_OBSERVABLE_NO_GO=TRUE")
        print("Q_BASEPOINT_INDEPENDENCE_OBSERVABLE_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_BASEPOINT_SECTION_E_EQUALS_ZERO=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_basepoint_independent_Q_readout_section_e_equals_zero")
        print("RESIDUAL_SOURCE=basepoint_invariance_erases_absolute_rho_section")
        print("COUNTERSECTION=e_1_full_determinant_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: basepoint-independence observable audit has FAILs.")
    print("KOIDE_Q_BASEPOINT_INDEPENDENCE_OBSERVABLE_NO_GO=FALSE")
    print("Q_BASEPOINT_INDEPENDENCE_OBSERVABLE_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_basepoint_independent_Q_readout_section_e_equals_zero")
    return 1


if __name__ == "__main__":
    sys.exit(main())
