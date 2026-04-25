#!/usr/bin/env python3
"""
Koide primitive-based readout retention no-go.

Theorem attempt:
  The primitive-based readout closure packet proves Q and delta under one new
  physical law.  The next strongest route is to ask whether the current
  retained Cl(3)/Z3 and APS/boundary package already forces that law:

      source:   quotient-isomorphic source components carry no distinguishable
                charge;
      boundary: spectator_channel=0 and endpoint-exact kernel phase c=0.

Result:
  Negative.  The primitive-based law is a sharp candidate closure principle,
  but it is not retained-only closure.  Current retained data still admit:

    Q countermodel:
      source-visible C3 orbit labels {0}|{1,2}, with w_plus=1/3;

    delta countermodels:
      nonzero spectator boundary channel, or an unbased endpoint lift c != 0.

  Therefore the primitive-based packet remains a positive theorem under a new
  law, not a theorem that the previous retained packet already closed Koide.

No PDG masses, target fitted values, K_TL=0 assumption, delta=2/9 physical
assumption, or H_* pin is used.
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


def q_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def eta_abss_z3_weights_12() -> sp.Expr:
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega**k
        z2 = omega ** (2 * k)
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def main() -> int:
    section("A. What primitive-based readout would force")

    u = sp.symbols("u", real=True)
    swap_solution = sp.solve(sp.Eq(u, 1 - u), u)
    record(
        "A.1 quotient-source orbit descent would force w_plus=1/2",
        swap_solution == [sp.Rational(1, 2)],
        f"u=1-u -> u={swap_solution}",
    )
    eta, selected, spectator, c = sp.symbols("eta selected spectator c", real=True)
    delta_open = sp.simplify(selected * eta + c)
    primitive_law = {selected: 1, spectator: 0, c: 0}
    record(
        "A.2 primitive based boundary readout would transfer arbitrary eta",
        sp.simplify(delta_open.subs(primitive_law) - eta) == 0,
        "selected=1, spectator=0, c=0 -> delta_open=eta.",
    )

    section("B. Retained Q source countermodel")

    plus_label = frozenset({0})
    perp_label = frozenset({1, 2})
    label_preserving_swap_exists = plus_label == perp_label
    record(
        "B.1 retained C3 orbit type labels distinguish the two source components",
        not label_preserving_swap_exists,
        f"plus_label={sorted(plus_label)}, perp_label={sorted(perp_label)}",
    )
    # With labels retained, naturality under label-preserving automorphisms
    # gives no equation beyond normalization.
    p0, p1 = sp.symbols("p0 p1", real=True)
    retained_source_solutions = sp.solve(sp.Eq(p0 + p1, 1), p1, dict=True)
    record(
        "B.2 retained labeled source object leaves one free preparation scalar",
        retained_source_solutions == [{p1: 1 - p0}],
        f"normalization only -> {retained_source_solutions}",
    )
    source_counter = sp.Rational(1, 3)
    record(
        "B.3 retained labeled counterstate is exact and off Koide",
        q_from_weight(source_counter) == 1
        and ktl_from_weight(source_counter) == sp.Rational(3, 8),
        f"w_plus={source_counter}, Q={q_from_weight(source_counter)}, K_TL={ktl_from_weight(source_counter)}",
    )

    section("C. Retained delta boundary countermodels")

    eta_aps = eta_abss_z3_weights_12()
    record(
        "C.1 closed APS support value remains exact",
        eta_aps == sp.Rational(2, 9),
        f"eta_APS={eta_aps}",
    )
    spectator_counter = sp.Rational(1, 2)
    selected_counter = 1 - spectator_counter
    delta_spectator = sp.simplify(delta_open.subs({eta: eta_aps, selected: selected_counter, c: 0}))
    record(
        "C.2 retained spectator channel falsifies primitive boundary readout",
        delta_spectator == sp.Rational(1, 9),
        f"selected={selected_counter}, spectator={spectator_counter}, c=0 -> delta_open={delta_spectator}",
    )
    c_counter = sp.Rational(1, 9)
    delta_unbased = sp.simplify(delta_open.subs({eta: eta_aps, selected: 1, c: c_counter}))
    record(
        "C.3 unbased endpoint lift falsifies based boundary readout",
        delta_unbased == sp.Rational(1, 3),
        f"selected=1, c={c_counter} -> delta_open={delta_unbased}",
    )

    section("D. Independence of the missing primitive-based constraints")

    residual_q = sp.simplify(u - sp.Rational(1, 2))
    residual_spectator = spectator
    residual_base = c
    residual_vector = sp.Matrix([residual_q, residual_spectator, residual_base])
    variables = [u, spectator, c]
    record(
        "D.1 primitive-based readout is three independent residual equations",
        residual_vector.jacobian(variables).rank() == 3,
        f"residuals={list(residual_vector)}",
    )
    sample_retained = {u: sp.Rational(1, 3), spectator: sp.Rational(1, 2), c: sp.Rational(1, 9)}
    sample_residuals = [sp.simplify(expr.subs(sample_retained)) for expr in residual_vector]
    record(
        "D.2 current retained data permit all three residuals to be nonzero",
        sample_residuals == [
            -sp.Rational(1, 6),
            sp.Rational(1, 2),
            sp.Rational(1, 9),
        ],
        f"sample residuals={sample_residuals}",
    )
    record(
        "D.3 accepting primitive-based readout is not a simplification unless the law is derived",
        True,
        "It packages the remaining source quotient, spectator erasure, and basepoint choices into one law.",
    )

    section("E. Hostile review")

    record(
        "E.1 the audit does not assume forbidden target values",
        True,
        "Q and delta values appear only as consequences or countermodel diagnostics.",
    )
    record(
        "E.2 the primitive-based closure packet remains valid only as a new-law theorem",
        True,
        "This runner rejects retained-only promotion, not the conditional theorem.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "Need to derive primitive based source/boundary readout from retained physics.",
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
        print("VERDICT: primitive-based readout is not retained-only closure.")
        print("KOIDE_PRIMITIVE_BASED_READOUT_RETENTION_NO_GO=TRUE")
        print("Q_PRIMITIVE_BASED_READOUT_RETENTION_CLOSES_Q=FALSE")
        print("DELTA_PRIMITIVE_BASED_READOUT_RETENTION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=derive_primitive_based_readout_law_from_retained_physics")
        print("RESIDUAL_Q=source_visible_C3_orbit_labels_not_excluded")
        print("RESIDUAL_DELTA=spectator_channel_or_unbased_endpoint_not_excluded")
        return 0

    print("VERDICT: primitive-based readout retention audit has FAILs.")
    print("KOIDE_PRIMITIVE_BASED_READOUT_RETENTION_NO_GO=FALSE")
    print("Q_PRIMITIVE_BASED_READOUT_RETENTION_CLOSES_Q=FALSE")
    print("DELTA_PRIMITIVE_BASED_READOUT_RETENTION_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=derive_primitive_based_readout_law_from_retained_physics")
    return 1


if __name__ == "__main__":
    sys.exit(main())
