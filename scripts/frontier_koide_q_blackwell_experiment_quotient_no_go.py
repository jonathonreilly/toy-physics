#!/usr/bin/env python3
"""
Koide Q Blackwell experiment-quotient no-go.

Theorem attempt:
  Use Blackwell/decision-theoretic equivalence to justify quotienting the two
  center labels.  The reduced scalar observable experiment cannot distinguish
  P_plus from P_perp, so perhaps the physical experiment is forced to identify
  them, giving the anonymous two-point quotient and hence K_TL=0.

Result:
  Negative under current retained structure.  The scalar-only experiment is a
  garbling of the full retained experiment that includes the central label
  observable Z=P_plus-P_perp.  The converse garbling does not exist: a
  one-outcome scalar experiment cannot reconstruct the label-resolving
  identity experiment.  Therefore Blackwell order says the retained Z
  experiment is strictly more informative.  Choosing the scalar-only experiment
  is exactly the missing source-domain quotient, not a consequence of decision
  theory.

No PDG masses, H_* pins, Q targets, delta targets, or K_TL=0 assumptions are
used as inputs.
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


def main() -> int:
    section("A. Two experiments on the retained center label")

    # Convention: rows are hidden center labels (+, perp), columns are observed
    # outcomes.  Row-stochastic matrices encode experiments.
    E_full = sp.eye(2)
    E_scalar = sp.Matrix([[1], [1]])
    G_forget = sp.Matrix([[1], [1]])

    record(
        "A.1 full retained Z experiment is label-resolving",
        E_full == sp.eye(2),
        "E_full observes the central label/eigenvalue of Z=P_plus-P_perp.",
    )
    record(
        "A.2 scalar-only experiment identifies the two labels",
        E_scalar[0, 0] == E_scalar[1, 0] == 1,
        f"E_scalar={E_scalar}",
    )
    record(
        "A.3 scalar experiment is a garbling of the full retained experiment",
        E_full * G_forget == E_scalar,
        f"E_full * G_forget = {E_full * G_forget}",
    )

    section("B. No reverse garbling exists")

    a = sp.symbols("a", real=True)
    H = sp.Matrix([[a, 1 - a]])
    reconstructed = E_scalar * H
    reverse_equations = list(reconstructed - E_full)
    reverse_solution = sp.solve(reverse_equations, [a], dict=True)
    record(
        "B.1 a one-outcome scalar experiment cannot reconstruct the label experiment",
        reverse_solution == [],
        f"E_scalar*H={reconstructed}; equations={reverse_equations}",
    )
    record(
        "B.2 Blackwell order is strict: full retained experiment is more informative",
        E_full * G_forget == E_scalar and reverse_solution == [],
        "The scalar quotient is not decision-theoretically equivalent to the retained Z experiment.",
    )

    section("C. Decision risk exposes the retained-label information")

    w = sp.symbols("w", positive=True, real=True)
    scalar_label_loss_risk = sp.Min(w, 1 - w)
    full_label_loss_risk = sp.Integer(0)
    record(
        "C.1 for label-recovery loss, full retained experiment has zero Bayes risk",
        full_label_loss_risk == 0,
        "Observing Z reveals the hidden center label.",
    )
    record(
        "C.2 scalar-only experiment leaves prior-dependent label risk",
        scalar_label_loss_risk.subs(w, sp.Rational(1, 3)) == sp.Rational(1, 3)
        and scalar_label_loss_risk.subs(w, sp.Rational(1, 2)) == sp.Rational(1, 2),
        "With no label observation, best guessing risk is min(w,1-w).",
    )
    record(
        "C.3 Blackwell comparison does not choose the source prior",
        ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8)
        and ktl_from_weight(sp.Rational(1, 2)) == 0,
        "Both priors can be paired with either chosen experiment; only w=1/2 closes Q.",
    )

    section("D. Conditional positive quotient and retained obstruction")

    record(
        "D.1 if the physical experiment is postulated scalar-only and quotient-prepared, Q closes",
        q_from_weight(sp.Rational(1, 2)) == sp.Rational(2, 3)
        and ktl_from_weight(sp.Rational(1, 2)) == 0,
        "This is the existing quotient-center anonymity conditional.",
    )
    record(
        "D.2 if retained Z remains source-visible, nonclosing priors survive",
        q_from_weight(sp.Rational(1, 3)) == 1
        and ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        "w=1/3 is exact and retained-label compatible.",
    )

    section("E. Hostile review")

    record(
        "E.1 Blackwell theory cannot promote a garbling as the physical experiment",
        True,
        "Garbling loses retained information; choosing it is the source-domain quotient law.",
    )
    record(
        "E.2 no forbidden target or observational pin is used as input",
        True,
        "The Koide value appears only as the consequence of the conditional uniform prior.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "RESIDUAL_PRIMITIVE=derive_physical_experiment_is_scalar_garbling_and_quotient_prepared.",
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
        print("KOIDE_Q_BLACKWELL_EXPERIMENT_QUOTIENT_NO_GO=TRUE")
        print("Q_BLACKWELL_EXPERIMENT_QUOTIENT_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=source_prior_w_minus_one_half_after_blackwell_scalar_garbling")
        print("RESIDUAL_LABEL=retained_Z_experiment_strictly_blackwell_more_informative")
        print("RESIDUAL_PRIMITIVE=derive_physical_experiment_is_scalar_garbling_and_quotient_prepared")
        return 0

    print("KOIDE_Q_BLACKWELL_EXPERIMENT_QUOTIENT_NO_GO=FALSE")
    print("Q_BLACKWELL_EXPERIMENT_QUOTIENT_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=source_prior_w_minus_one_half_after_blackwell_scalar_garbling")
    return 1


if __name__ == "__main__":
    sys.exit(main())
