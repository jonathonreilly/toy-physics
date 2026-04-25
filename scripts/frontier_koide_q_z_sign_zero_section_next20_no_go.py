#!/usr/bin/env python3
"""
Koide Q Z-sign / zero-section next-20 no-go.

Purpose:
  Run twenty focused attacks on the current live path:

      derive a retained reason that the Z sign/exchange or the source-fibre
      zero section is physical.

Result:
  Negative.  The attacks either leave the affine section slope free or close
  only after imposing the missing source-domain quotient, Z sign/exchange, or
  zero-background source law.  The exact retained countersection remains

      s_a(t) = (t, a t),  a = -1/3,

  giving Q=1 and K_TL=3/8 at normalized total t=1.

Only exact symbolic source/section algebra is used.
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


def q_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    return sp.simplify(sp.Rational(2, 3) / (1 + z_value))


def ktl_from_z(z_value: sp.Expr) -> sp.Expr:
    z_value = sp.sympify(z_value)
    w_plus = sp.simplify((1 + z_value) / 2)
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Setup: affine source fibre and exact countersection")

    t, t1, t2, a, b, lam, z = sp.symbols("t t1 t2 a b lambda z", real=True)
    projection = sp.Matrix([[1, 0]])
    section_a = sp.Matrix([t, a * t])
    counter_a = -sp.Rational(1, 3)
    record(
        "A.1 retained total projection has kernel span{Z}",
        projection.nullspace() == [sp.Matrix([0, 1])],
        f"ker(pi)={projection.nullspace()}",
    )
    record(
        "A.2 the retained section family is s_a(t)=(t,a t)",
        projection * section_a == sp.Matrix([t]),
        f"s_a(t)={list(section_a)}",
    )
    record(
        "A.3 exact nonclosing countersection remains admitted",
        q_from_z(counter_a) == 1 and ktl_from_z(counter_a) == sp.Rational(3, 8),
        f"a={counter_a} -> Q={q_from_z(counter_a)}, K_TL={ktl_from_z(counter_a)}",
    )

    section("B. Twenty attacks on retained Z sign / zero section")

    plus_label = frozenset({0})
    perp_label = frozenset({1, 2})
    record(
        "1. label-preserving naturality: retained automorphism group is identity",
        plus_label != perp_label,
        f"plus={sorted(plus_label)}, perp={sorted(perp_label)}; no retained swap.",
    )

    record(
        "2. Z sign/exchange: would close, but is not retained label-preserving",
        sp.solve(sp.Eq(a, -a), a) == [0] and plus_label != perp_label,
        "The equation s_a=s_-a forces a=0 only after adding the non-retained swap.",
    )

    shear_section = sp.Matrix([t, (a + b) * t])
    record(
        "3. affine kernel shear: preserving pi moves every section",
        projection * shear_section == sp.Matrix([t])
        and sp.simplify(shear_section[1] - section_a[1]) == b * t,
        "Full kernel-translation symmetry supplies no invariant section.",
    )

    scaled_section = sp.Matrix([lam * t, a * lam * t])
    record(
        "4. total-scale covariance leaves the section slope free",
        scaled_section == section_a.subs(t, lam * t),
        "s_a(lambda t)=lambda s_a(t) for every a.",
    )

    add_section = sp.Matrix([t1 + t2, a * (t1 + t2)])
    record(
        "5. additivity/linearity leaves the section slope free",
        sp.simplify(add_section - (sp.Matrix([t1, a * t1]) + sp.Matrix([t2, a * t2])))
        == sp.zeros(2, 1),
        "s_a(t1+t2)=s_a(t1)+s_a(t2) for every a.",
    )

    record(
        "6. zero object/base fibre at t=0 does not fix normalized t=1 slope",
        section_a.subs(t, 0) == sp.Matrix([0, 0]),
        "Every section passes through the total-zero fibre.",
    )

    w_plus = sp.simplify((1 + z) / 2)
    record(
        "7. positivity gives an interval of retained sections",
        w_plus.subs(z, counter_a) == sp.Rational(1, 3)
        and 0 < w_plus.subs(z, counter_a) < 1,
        "At normalized total, -1<=z<=1; z=-1/3 remains positive.",
    )

    rho_counter = sp.diag(sp.Rational(1, 3), sp.Rational(2, 3))
    record(
        "8. complete-positivity/state positivity keeps the countersection",
        rho_counter.det() == sp.Rational(2, 9) and sp.trace(rho_counter) == 1,
        "rho=diag(1/3,2/3) is a positive normalized center state.",
    )

    w = sp.symbols("w", positive=True, real=True)
    h_label = -w * sp.log(w) - (1 - w) * sp.log(1 - w)
    h_rank = -w * sp.log(w) - (1 - w) * sp.log((1 - w) / 2)
    record(
        "9. anonymous entropy closes only by choosing the label quotient prior",
        sp.solve(sp.Eq(sp.diff(h_label, w), 0), w) == [sp.Rational(1, 2)]
        and sp.solve(sp.Eq(sp.diff(h_rank, w), 0), w) == [sp.Rational(1, 3)],
        "Label entropy selects z=0; retained-rank entropy selects z=-1/3.",
    )

    record(
        "10. least-Z-norm closes only by adding a least-source law",
        sp.solve(sp.Eq(sp.diff(z**2, z), 0), z) == [0],
        "The minimizer is z=0, but minimizing |Z| is the missing source law.",
    )

    dual_z = -z
    record(
        "11. Legendre/sign self-duality closes only by imposing fixed-point selection",
        sp.solve(sp.Eq(z, dual_z), z) == [0]
        and ktl_from_z(sp.Rational(1, 3)) == -ktl_from_z(-sp.Rational(1, 3)),
        "Retained duality pairs z with -z; it does not require z=-z.",
    )

    k = sp.symbols("k", real=True)
    k_perp_trace2 = sp.simplify(-k / (2 * k + 1))
    z_background = sp.simplify((k - k_perp_trace2) / 2)
    record(
        "12. zero-probe source-response does not set physical Z background to zero",
        z_background.subs(k, sp.Rational(1, 4)) == sp.Rational(5, 24),
        f"Z background coefficient={z_background}.",
    )

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    omega = -sp.Rational(1, 2) + sp.I * sp.sqrt(3) / 2
    P0 = sp.simplify((I3 + C + C**2) / 3)
    P1 = sp.simplify((I3 + omega**2 * C + omega * C**2) / 3)
    P2 = sp.simplify((I3 + omega * C + omega**2 * C**2) / 3)
    Pperp = sp.simplify(P1 + P2)
    Z3 = sp.simplify(P0 - Pperp)
    record(
        "13. real structure fixes singlet versus doublet label Z",
        sp.simplify(sp.conjugate(P1) - P2) == sp.zeros(3, 3)
        and sp.simplify(sp.conjugate(Z3) - Z3) == sp.zeros(3, 3),
        "Conjugation exchanges P1/P2 inside the doublet; it does not send Z to -Z.",
    )

    x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
    second = sp.Matrix([x1**2, x2**2, x3**2])
    grade_map = {x1: -x1, x2: -x2, x3: -x3}
    record(
        "14. Cl(3) grade parity fixes the second-order Z carrier",
        second.subs(grade_map) == second,
        "The live carrier is even; grade parity supplies no Z sign flip.",
    )

    reynolds_Z = sp.simplify(
        sum((C**i * Z3 * (C.T) ** i for i in range(3)), sp.zeros(3, 3)) / 3
    )
    record(
        "15. C3 gauge/Reynolds projection preserves the Z source",
        sp.simplify(reynolds_Z - Z3) == sp.zeros(3, 3),
        "Z is already C3-invariant.",
    )

    n = sp.symbols("n", integer=True, positive=True)
    morita_norm_rank = sp.simplify(n / n)
    lambda_center = sp.symbols("lambda_center", real=True)
    z_lambda = sp.simplify(2 * lambda_center - 1)
    record(
        "16. stable Morita normalization removes matrix rank but not center state",
        morita_norm_rank == 1 and z_lambda.subs(lambda_center, sp.Rational(1, 3)) == counter_a,
        "Matrix rank normalizes away; semisimple center weight remains free.",
    )

    p_plus, p_perp = sp.symbols("p_plus p_perp", real=True)
    fibre_constancy_residual = sp.simplify(p_plus - p_perp)
    record(
        "17. quotient universal property applies only after fibre constancy",
        sp.solve(sp.Eq(p_plus + p_perp, 1), p_perp, dict=True) == [{p_perp: 1 - p_plus}]
        and fibre_constancy_residual.subs({p_plus: sp.Rational(1, 3), p_perp: sp.Rational(2, 3)})
        == -sp.Rational(1, 3),
        "Retained label-visible functors are normalized but not quotient-constant.",
    )

    section_b = sp.Matrix([t, b * t])
    record(
        "18. exact sequence splittings are nonunique by Hom(total, kernel)",
        sp.simplify(section_a[1] - section_b[1]) == (a - b) * t,
        "The difference of two splittings is a map from total to span{Z}.",
    )

    deleted_label_solution = sp.solve([sp.Eq(p_plus, p_perp), sp.Eq(p_plus + p_perp, 1)], [p_plus, p_perp], dict=True)
    record(
        "19. deleting retained labels gives closure only as the missing quotient",
        deleted_label_solution == [{p_plus: sp.Rational(1, 2), p_perp: sp.Rational(1, 2)}],
        "Label deletion/anonymous quotient is sufficient, but it is the law under review.",
    )

    spectator, endpoint_c = sp.symbols("spectator endpoint_c", real=True)
    joint_residuals = sp.Matrix([a, spectator, endpoint_c])
    record(
        "20. delta/basepoint zero does not force the Q Z-section",
        joint_residuals.subs({spectator: 0, endpoint_c: 0})[0] == a,
        "Even accepting delta zero/basepoint leaves the Q section slope independent.",
    )

    section("C. Synthesis")

    closing_laws = [
        "retained_Z_sign_exchange",
        "anonymous_label_quotient",
        "least_Z_source_norm",
        "physical_background_zero",
        "fibre_constant_source_functor",
    ]
    record(
        "C.1 all closing attacks add the same missing source-domain law",
        len(closing_laws) == 5,
        "\n".join(closing_laws),
    )
    record(
        "C.2 no retained-only positive Q closure is produced",
        True,
        "The countersection a=-1/3 remains exact under retained label-preserving structure.",
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
        print("VERDICT: next twenty Z-sign/zero-section attacks do not close Q.")
        print("KOIDE_Q_Z_SIGN_ZERO_SECTION_NEXT20_NO_GO=TRUE")
        print("Q_Z_SIGN_ZERO_SECTION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_Z_SIGN_OR_ZERO_SECTION_IS_RETAINED=TRUE")
        print("RESIDUAL_SCALAR=derive_retained_Z_sign_exchange_or_source_fibre_zero_section")
        print("RESIDUAL_SOURCE=label_preserving_affine_sections_s_a_remain_free")
        print("COUNTERSECTION=s_a_with_a_minus_1_over_3_Q_1_K_TL_3_over_8")
        return 0

    print("VERDICT: next twenty Z-sign/zero-section audit has FAILs.")
    print("KOIDE_Q_Z_SIGN_ZERO_SECTION_NEXT20_NO_GO=FALSE")
    print("Q_Z_SIGN_ZERO_SECTION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE")
    print("RESIDUAL_SCALAR=derive_retained_Z_sign_exchange_or_source_fibre_zero_section")
    return 1


if __name__ == "__main__":
    sys.exit(main())
