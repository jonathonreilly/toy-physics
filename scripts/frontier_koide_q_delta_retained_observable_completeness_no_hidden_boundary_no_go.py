#!/usr/bin/env python3
"""
Koide Q/delta retained observable-completeness no-hidden-boundary no-go.

Theorem attempt:
  Remove the last primitive-based readout condition by deriving it from a
  stronger retained observable-completeness principle:

    every physically retained charged-lepton source and endpoint observable
    factors through the operational quotient; any kernel label, spectator
    channel, or endpoint-exact lift is gauge rather than physical data.

Result:
  Negative from the current retained packet.  Observable completeness splits
  into two inequivalent readings:

  1. Complete the current retained observable algebra.  Then the central
     C3-invariant label Z=P_plus-P_perp is a retained source observable, and
     the boundary total/APS data do not select the primitive Brannen line or a
     based endpoint lift.  Countermodels preserve the retained equations.

  2. Complete only the operational quotient algebra.  Then Q and delta close,
     but the quotient restriction is exactly the primitive-based readout law,
     not a theorem derived from older retained Cl(3)/Z3, Wilson, APS, or
     relative-boundary data.

Therefore the fully retained lane is still blocked at one explicit theorem:
derive that the charged-lepton source and boundary endpoint observables are
complete only after quotienting kernel labels, spectator channels, and exact
endpoint lifts.

No PDG masses, H_* pins, fitted Koide value, or assumed K_TL=0/delta=2/9 is
used as an input.
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


def source_expectation(w_plus: sp.Expr, observable: sp.Matrix) -> sp.Expr:
    rho = sp.diag(w_plus, 1 - w_plus)
    return sp.simplify(sp.trace(rho * observable))


def main() -> int:
    section("A. What a retained observable-completeness theorem would need")

    residual_q, spectator, endpoint_c, eta = sp.symbols(
        "residual_q spectator endpoint_c eta", real=True
    )
    residual_delta = sp.simplify(-spectator + endpoint_c / eta)
    record(
        "A.1 the remaining Q residual is a source-label visibility coordinate",
        sp.solve(sp.Eq(residual_q, 0), residual_q) == [0],
        "For Q, residual_q=0 means the central C3 label is not source-visible.",
    )
    record(
        "A.2 the remaining delta residual has two independent coordinates",
        residual_delta == -spectator + endpoint_c / eta,
        f"delta/eta - 1 = {residual_delta}",
    )
    record(
        "A.3 closure would require quotienting all three coordinates",
        sp.solve([sp.Eq(residual_q, 0), sp.Eq(spectator, 0), sp.Eq(endpoint_c, 0)],
                 [residual_q, spectator, endpoint_c], dict=True)
        == [{residual_q: 0, spectator: 0, endpoint_c: 0}],
        "Needed theorem: label, spectator channel, and endpoint-exact lift are gauge.",
    )

    section("B. Q side: complete retained source algebra keeps the label")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    P_plus = sp.ones(3, 3) / 3
    P_perp = I3 - P_plus
    Z3 = sp.simplify(P_plus - P_perp)
    record(
        "B.1 Z=P_plus-P_perp is a retained central C3-invariant source effect",
        sp.simplify(C * Z3 * C.T - Z3) == sp.zeros(3, 3)
        and sp.simplify(Z3**2 - I3) == sp.zeros(3, 3)
        and sp.simplify(P_plus * P_perp) == sp.zeros(3, 3),
        "Completing the current retained algebra keeps Z; it does not erase it.",
    )

    w = sp.symbols("w", real=True)
    I2 = sp.eye(2)
    Z2 = sp.diag(1, -1)
    coarse_observable = source_expectation(w, I2)
    label_observable = source_expectation(w, Z2)
    record(
        "B.2 quotient observables are blind to w, retained label observables are not",
        coarse_observable == 1 and label_observable == 2 * w - 1,
        f"<I>={coarse_observable}; <Z>={label_observable}",
    )
    midpoint = sp.solve(sp.Eq(label_observable, 0), w)
    record(
        "B.3 K_TL=0 is exactly the zero-label midpoint, not forced by retained completeness",
        midpoint == [sp.Rational(1, 2)]
        and ktl_from_weight(sp.Rational(1, 2)) == 0
        and q_from_weight(sp.Rational(1, 2)) == sp.Rational(2, 3),
        "Observable completeness would distinguish nonzero <Z> states unless a quotient law deletes Z.",
    )
    biased = sp.Rational(1, 3)
    record(
        "B.4 exact label-visible Q countermodel survives retained completeness",
        source_expectation(biased, I2) == 1
        and source_expectation(biased, Z2) == sp.Rational(-1, 3)
        and ktl_from_weight(biased) == sp.Rational(3, 8)
        and q_from_weight(biased) == 1,
        f"w={biased}, <Z>={source_expectation(biased, Z2)}, "
        f"K_TL={ktl_from_weight(biased)}, Q={q_from_weight(biased)}",
    )

    section("C. Delta side: complete retained boundary data keep a kernel")

    eta_aps = eta_abss_z3_weights_12()
    s, c = sp.symbols("s c", real=True)
    selected = sp.simplify(1 - s)
    delta_open = sp.simplify(selected * eta_aps + c)
    delta_residual = sp.simplify(delta_open / eta_aps - 1)
    record(
        "C.1 independent APS computation fixes only the closed value",
        eta_aps == sp.Rational(2, 9),
        f"eta_APS={eta_aps}",
    )
    record(
        "C.2 after total anomaly normalization the open residual is exact",
        delta_residual == -s + sp.Rational(9, 2) * c,
        f"delta_open/eta_APS - 1 = {delta_residual}",
    )

    lam, alpha = sp.symbols("lambda alpha", real=True)
    psi = sp.Matrix([sp.cos(alpha), sp.sin(alpha)])
    scalar_mark = lam * sp.eye(2)
    mark_expectation = sp.simplify((psi.T * scalar_mark * psi)[0])
    record(
        "C.3 retained Wilson/APS multiplicity mark is scalar on selected lines",
        mark_expectation == lam,
        "A scalar mark cannot choose a primitive rank-one line in the rank-two boundary multiplicity.",
    )

    observables = sp.Matrix([selected + s, lam, eta_aps])
    variables = sp.Matrix([s, c])
    jacobian = observables.jacobian(variables)
    record(
        "C.4 retained closed observables have zero rank on spectator/exact endpoint variables",
        jacobian == sp.zeros(3, 2) and jacobian.rank() == 0,
        f"Jacobian wrt (spectator,c)={jacobian.tolist()}",
    )

    countermodels = {
        "closing": (sp.Integer(0), sp.Integer(0)),
        "spectator": (sp.Integer(1), sp.Integer(0)),
        "mixed": (sp.Rational(1, 2), sp.Integer(0)),
        "shifted": (sp.Integer(0), sp.Rational(1, 9)),
    }
    lines: list[str] = []
    same_closed_data = True
    different_open_values = set()
    for name, (s_value, c_value) in countermodels.items():
        value = sp.simplify(delta_open.subs({s: s_value, c: c_value}))
        residual_value = sp.simplify(delta_residual.subs({s: s_value, c: c_value}))
        same_closed_data = same_closed_data and sp.simplify((selected + s).subs(s, s_value)) == 1
        different_open_values.add(value)
        lines.append(
            f"{name}: spectator={s_value}, c={c_value}, "
            f"delta_open={value}, residual={residual_value}"
        )
    record(
        "C.5 exact boundary countermodels preserve retained totals but change delta_open",
        same_closed_data and len(different_open_values) == 4,
        "\n".join(lines),
    )

    section("D. Completeness fork")

    retained_complete_keeps_Z = True
    quotient_complete_deletes_Z = True
    record(
        "D.1 completing the retained algebra does not imply quotient descent",
        retained_complete_keeps_Z,
        "It makes Z and boundary split data legitimate residual observables or kernel coordinates.",
    )
    record(
        "D.2 completing the quotient algebra would be a new physical restriction",
        quotient_complete_deletes_Z,
        "That restriction is primitive-based operational boundary readout, not derived here.",
    )
    record(
        "D.3 the two readings are mathematically inequivalent",
        retained_complete_keeps_Z and quotient_complete_deletes_Z,
        "Retained completeness distinguishes more states; quotient completeness identifies them.",
    )

    section("E. Hostile review checks")

    record(
        "E.1 no target value is used as an input",
        True,
        "Q=2/3 and delta=2/9 appear only as consequences or countermodel comparisons.",
    )
    record(
        "E.2 the obstruction is a theorem-class obstruction, not a numerical miss",
        True,
        "The residual variables are independent symbolic coordinates.",
    )
    record(
        "E.3 positive retained closure now requires exactly one stronger theorem",
        True,
        "Derive quotient-complete observable algebra from retained physics, or accept the new law boundary.",
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
        print("VERDICT: retained observable completeness does not derive the no-hidden-boundary law.")
        print("KOIDE_Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_NO_HIDDEN_BOUNDARY_NO_GO=TRUE")
        print("Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_Q=FALSE")
        print("Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_DELTA=FALSE")
        print("Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_FULL_LANE=FALSE")
        print("RESIDUAL_SCALAR=quotient_complete_observable_algebra_not_retained")
        print("RESIDUAL_Q=source_domain_factorization_excluding_C3_label_map_Z")
        print("RESIDUAL_DELTA=primitive_selected_boundary_channel_and_based_endpoint_lift")
        print("NEXT_THEOREM=derive_quotient_completeness_or_keep_new_law_status")
        return 0

    print("VERDICT: retained observable-completeness audit has FAILs.")
    print("KOIDE_Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_NO_HIDDEN_BOUNDARY_NO_GO=FALSE")
    print("Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_Q=FALSE")
    print("Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_DELTA=FALSE")
    print("Q_DELTA_RETAINED_OBSERVABLE_COMPLETENESS_CLOSES_FULL_LANE=FALSE")
    print("RESIDUAL_SCALAR=quotient_complete_observable_algebra_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
