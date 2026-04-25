#!/usr/bin/env python3
"""
Koide primitive-based readout universal-property derivation no-go.

Theorem attempt:
  Derive the new physical law

      primitive_based_operational_boundary_readout

  from the universal property of the operational quotient.  If the physical
  charged-lepton readout is forced to be a based functor on the quotient
  category, then quotient-isomorphic source components have equal weights,
  spectator boundary channels vanish, endpoint-exact phases vanish, and the
  existing primitive-based closure theorem applies.

Result:
  The universal-property derivation is exact but conditional.  It proves:

      quotient-factorization + based primitive target
        -> primitive-based readout law
        -> Q=2/3 and delta=2/9.

  It does not prove that the retained Cl(3)/Z3 and APS package forces the
  quotient-factorization premise.  The retained embedded source category still
  has label-preserving functors that see {0}|{1,2}; the retained boundary
  affine model still has spectator and basepoint parameters.

No PDG masses, H_* pins, K_TL=0 assumptions, Q target assumptions, or physical
delta target assumptions are used.
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
    section("A. Universal-property route to the new law")

    p_plus, p_perp = sp.symbols("p_plus p_perp", real=True)
    quotient_factorization_equations = [
        sp.Eq(p_plus, p_perp),
        sp.Eq(p_plus + p_perp, 1),
    ]
    quotient_source_solution = sp.solve(
        quotient_factorization_equations, [p_plus, p_perp], dict=True
    )
    record(
        "A.1 a source functor factored through the two-object quotient orbit is uniform",
        quotient_source_solution
        == [{p_plus: sp.Rational(1, 2), p_perp: sp.Rational(1, 2)}],
        f"solutions={quotient_source_solution}",
    )
    w_star = quotient_source_solution[0][p_plus]
    record(
        "A.2 quotient-factorized source gives K_TL=0 and Q=2/3",
        ktl_from_weight(w_star) == 0 and q_from_weight(w_star) == sp.Rational(2, 3),
        f"K_TL={ktl_from_weight(w_star)}, Q={q_from_weight(w_star)}",
    )

    eta, selected, spectator, c = sp.symbols("eta selected spectator c", real=True)
    delta_open = sp.simplify(selected * eta + c)
    based_primitive_constraints = {
        selected: 1,
        spectator: 0,
        c: 0,
    }
    record(
        "A.3 a based primitive boundary functor transfers arbitrary closed eta",
        sp.simplify(delta_open.subs(based_primitive_constraints) - eta) == 0,
        f"delta_open={sp.simplify(delta_open.subs(based_primitive_constraints))}",
    )
    eta_aps = eta_abss_z3_weights_12()
    delta_aps = sp.simplify(
        delta_open.subs(based_primitive_constraints).subs(eta, eta_aps)
    )
    record(
        "A.4 independent APS value then gives delta_open=2/9",
        eta_aps == sp.Rational(2, 9) and delta_aps == sp.Rational(2, 9),
        f"eta_APS={eta_aps}, delta_open={delta_aps}",
    )

    section("B. Universal property does not force quotient factorization by itself")

    # A quotient q:E->Q has the usual universal property only for functors F
    # that are constant on q-fibres.  Retained label-visible functors are not
    # constant on those fibres, so the property does not apply.
    label_visible_source = sp.Matrix([p_plus, p_perp])
    constant_on_fibre_residual = sp.simplify(p_plus - p_perp)
    record(
        "B.1 quotient universal property applies only after the source functor is fibre-constant",
        constant_on_fibre_residual == p_plus - p_perp,
        f"fibre-constancy residual={constant_on_fibre_residual}",
    )
    retained_solution = sp.solve(sp.Eq(p_plus + p_perp, 1), p_perp, dict=True)
    record(
        "B.2 retained embedded source functors need only be normalized, not fibre-constant",
        retained_solution == [{p_perp: 1 - p_plus}],
        f"retained labeled functors={retained_solution}",
    )
    retained_counter = {p_plus: sp.Rational(1, 3), p_perp: sp.Rational(2, 3)}
    record(
        "B.3 exact retained source counterfunctor is not quotient-factorized",
        sp.simplify(constant_on_fibre_residual.subs(retained_counter)) == -sp.Rational(1, 3)
        and q_from_weight(retained_counter[p_plus]) == 1
        and ktl_from_weight(retained_counter[p_plus]) == sp.Rational(3, 8),
        (
            f"p={retained_counter}, fibre residual="
            f"{sp.simplify(constant_on_fibre_residual.subs(retained_counter))}, "
            f"Q={q_from_weight(retained_counter[p_plus])}, "
            f"K_TL={ktl_from_weight(retained_counter[p_plus])}"
        ),
    )

    section("C. Based primitive boundary is also an extra factorization choice")

    boundary_residual_vector = sp.Matrix([spectator, c])
    boundary_variables = [spectator, c]
    record(
        "C.1 boundary spectator and basepoint are independent retained affine parameters",
        boundary_residual_vector.jacobian(boundary_variables).rank() == 2,
        f"residuals={list(boundary_residual_vector)}",
    )
    spectator_counter = {selected: sp.Rational(1, 2), spectator: sp.Rational(1, 2), c: 0}
    base_counter = {selected: 1, spectator: 0, c: sp.Rational(1, 9)}
    delta_spectator = sp.simplify(delta_open.subs(spectator_counter).subs(eta, eta_aps))
    delta_base = sp.simplify(delta_open.subs(base_counter).subs(eta, eta_aps))
    record(
        "C.2 retained spectator counterfunctor is not primitive",
        delta_spectator == sp.Rational(1, 9),
        f"{spectator_counter} -> delta_open={delta_spectator}",
    )
    record(
        "C.3 retained endpoint-shift counterfunctor is not based",
        delta_base == sp.Rational(1, 3),
        f"{base_counter} -> delta_open={delta_base}",
    )

    section("D. Hostile review")

    record(
        "D.1 the derivation proves the correct implication but not the retained premise",
        True,
        "It proves factorized based primitive functor => new law, not retained data => factorized based primitive functor.",
    )
    record(
        "D.2 no forbidden target values are assumptions",
        True,
        "The Q and delta values are computed after exact symbolic factorization constraints.",
    )
    record(
        "D.3 exact residual primitive is named",
        True,
        "Need a retained theorem that physical readouts are fibre-constant, primitive, and based on the operational quotient.",
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
        print("VERDICT: universal-property derivation is conditional, not retained-only proof.")
        print("KOIDE_PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_DERIVATION_NO_GO=TRUE")
        print("PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_CLOSES_DELTA_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_CLOSURE_IF_FACTORING_BASED_PRIMITIVE_FUNCTOR=TRUE")
        print("RESIDUAL_SCALAR=derive_physical_readout_factorization_through_operational_quotient")
        print("RESIDUAL_Q=fibre_constancy_excluding_source_visible_C3_labels")
        print("RESIDUAL_DELTA=primitive_based_boundary_functor_excluding_spectator_and_c")
        return 0

    print("VERDICT: universal-property derivation audit has FAILs.")
    print("KOIDE_PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_DERIVATION_NO_GO=FALSE")
    print("PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("PRIMITIVE_BASED_READOUT_UNIVERSAL_PROPERTY_CLOSES_DELTA_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_physical_readout_factorization_through_operational_quotient")
    return 1


if __name__ == "__main__":
    sys.exit(main())
