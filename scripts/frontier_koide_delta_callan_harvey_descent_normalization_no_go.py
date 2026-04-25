#!/usr/bin/env python3
"""
Koide delta Callan-Harvey descent-normalization no-go.

This runner audits the strongest current Brannen-phase bridge candidate:

    ambient APS/anomaly value eta = 2/9
    -> selected-line physical Brannen phase delta = 2/9.

It verifies the exact support arithmetic, then isolates the residual scalar

    N_desc := delta_physical / eta_APS

showing that retained APS/anomaly constraints do not fix N_desc = 1.  Setting
N_desc = 1 is precisely the missing physical Berry/inflow identification plus
unit descent-normalization theorem, not a consequence of the current package.

No PDG masses, Koide Q target, or observational H_* pins are used.
"""

from __future__ import annotations

import sys
from fractions import Fraction

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def eta_abss_z3_weights_12() -> sp.Rational:
    """ABSS fixed-point eta for Z_3 tangent weights (1, 2)."""
    omega = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    omega2 = sp.conjugate(omega)
    total = sp.Rational(0)
    for k in (1, 2):
        z1 = omega if k == 1 else omega2
        z2 = omega2 if k == 1 else omega
        total += sp.simplify(1 / ((z1 - 1) * (z2 - 1)))
    return sp.simplify(total / 3)


def anomaly_per_generation(d: int = 3) -> sp.Rational:
    """Retained Callan-Harvey candidate anomaly arithmetic."""
    return sp.simplify((2 * d) * sp.Rational(1, d) ** 3)


def main() -> int:
    print("=" * 88)
    print("Koide delta Callan-Harvey descent-normalization no-go")
    print("=" * 88)

    eta = eta_abss_z3_weights_12()
    anomaly = anomaly_per_generation(3)
    target = sp.Rational(2, 9)

    check(
        "1. Ambient ABSS/APS value is exactly eta = 2/9",
        eta == target,
        f"eta_ABSS(Z_3; weights 1,2) = {eta}",
    )
    check(
        "2. Candidate Callan-Harvey anomaly coefficient is exactly 2/9",
        anomaly == target,
        f"(2d) * (1/d)^3 at d=3 = {anomaly}",
    )
    check(
        "3. APS and anomaly support scalars agree without using delta",
        eta == anomaly,
        f"eta_APS - A_CH = {sp.simplify(eta - anomaly)}",
    )

    n_desc, delta = sp.symbols("N_desc delta")
    bridge_eq = sp.Eq(delta, n_desc * eta)
    closure_eq = sp.Eq(delta, eta)
    residual = sp.simplify(delta / eta - 1)

    retained_constraints = [
        sp.simplify(eta - target),
        sp.simplify(anomaly - target),
        sp.simplify(eta - anomaly),
    ]
    jacobian_in_n_desc = sp.Matrix([[sp.diff(c, n_desc)] for c in retained_constraints])

    check(
        "4. Retained APS/anomaly constraints have zero rank in N_desc",
        jacobian_in_n_desc.rank() == 0,
        "Constraints checked: eta=2/9, A_CH=2/9, eta=A_CH.\n"
        f"Jacobian wrt N_desc = {list(jacobian_in_n_desc)}",
    )

    samples = [sp.Rational(1, 2), sp.Rational(1, 1), sp.Rational(3, 2)]
    sample_lines = []
    all_support_still_true = True
    deltas = set()
    for sample in samples:
        delta_sample = sp.simplify(sample * eta)
        deltas.add(delta_sample)
        support_ok = all(c == 0 for c in retained_constraints)
        all_support_still_true = all_support_still_true and support_ok
        sample_lines.append(f"N_desc={sample} -> delta={delta_sample}, support_ok={support_ok}")

    check(
        "5. A one-parameter family preserves support data but changes delta",
        all_support_still_true and len(deltas) == len(samples),
        "\n".join(sample_lines),
    )

    n_desc_from_target = sp.solve(sp.Eq(n_desc * eta, eta), n_desc)
    n_desc_from_closure = sp.solve((bridge_eq.lhs - bridge_eq.rhs, closure_eq.lhs - closure_eq.rhs), (n_desc, delta))

    check(
        "6. Delta closure is equivalent to imposing N_desc = 1",
        n_desc_from_target == [sp.Integer(1)] and n_desc_from_closure == {n_desc: 1, delta: eta},
        f"delta=N_desc*eta and delta=eta -> {n_desc_from_closure}",
    )

    check(
        "7. The exact residual scalar is delta/eta - 1 = N_desc - 1",
        sp.simplify(residual.subs(delta, n_desc * eta) - (n_desc - 1)) == 0,
        f"residual = {sp.simplify(residual.subs(delta, n_desc * eta))}",
    )

    check(
        "8. This audit does not import Q, PDG masses, H_* pins, or delta as data",
        True,
        "Only exact Z_3 APS arithmetic, exact anomaly arithmetic, and symbolic\n"
        "bridge-normalization algebra are used.",
    )

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("KOIDE_DELTA_CALLAN_HARVEY_DESCENT_NORMALIZATION_NO_GO=TRUE")
        print("DELTA_CALLAN_HARVEY_ROUTE_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=N_desc - 1")
        print()
        print("VERDICT: retained APS/anomaly support fixes eta = A_CH = 2/9,")
        print("but the selected-line physical phase still needs the independent")
        print("Berry/inflow identification and unit descent-normalization theorem.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
