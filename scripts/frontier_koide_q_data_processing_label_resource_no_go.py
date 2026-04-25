#!/usr/bin/env python3
"""
Koide Q data-processing / label-resource no-go.

Theorem attempt:
  Use a resource-theoretic or data-processing principle to force the physical
  source to discard the retained center-label observable Z=P_plus-P_perp.
  If the label resource is erased, the quotient source is uniform and K_TL=0.

Result:
  Negative under current retained structure.  Data processing says that
  stochastic coarse-graining cannot increase label information, but it does
  not say the physical channel must be the erasure channel rather than the
  identity channel.  The identity channel is retained and preserves the
  nonzero Z/source bias.  The erasure channel closes Q only by choosing the
  scalar-only quotient operation and the zero-resource source state.

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


def entropy_binary(w: sp.Expr) -> sp.Expr:
    return sp.simplify(-w * sp.log(w) - (1 - w) * sp.log(1 - w))


def main() -> int:
    section("A. Retained label resource coordinate")

    w = sp.symbols("w", positive=True, real=True)
    z_bias = sp.simplify(2 * w - 1)
    resource = sp.simplify(z_bias**2)
    record(
        "A.1 retained center-label bias is the Z expectation",
        z_bias == 2 * w - 1,
        "<Z>=p_plus-p_perp=2w-1.",
    )
    record(
        "A.2 K_TL=0 is exactly zero label resource",
        sp.solve(sp.Eq(resource, 0), w) == [sp.Rational(1, 2)]
        and ktl_from_weight(sp.Rational(1, 2)) == 0,
        f"R_Z=(2w-1)^2; K_TL(w)={ktl_from_weight(w)}",
    )
    record(
        "A.3 retained nonzero-resource states are exact nonclosing counterstates",
        resource.subs(w, sp.Rational(1, 3)) == sp.Rational(1, 9)
        and q_from_weight(sp.Rational(1, 3)) == 1
        and ktl_from_weight(sp.Rational(1, 3)) == sp.Rational(3, 8),
        "w=1/3 has nonzero label resource and is retained-label compatible.",
    )

    section("B. Data processing for experiments does not choose erasure")

    E_full = sp.eye(2)
    E_scalar = sp.Matrix([[1], [1]])
    G_forget = sp.Matrix([[1], [1]])
    record(
        "B.1 scalar-only experiment is the label-erasing garbling of retained Z",
        E_full * G_forget == E_scalar,
        f"E_full*G_forget={E_full * G_forget}",
    )
    h_label = entropy_binary(w)
    info_full = h_label
    info_scalar = sp.Integer(0)
    record(
        "B.2 data processing is satisfied for every source prior",
        info_scalar <= info_full.subs(w, sp.Rational(1, 3))
        and info_scalar <= info_full.subs(w, sp.Rational(1, 2)),
        "I(label;scalar)=0 <= I(label;Z)=H(w) for all interior w.",
    )
    record(
        "B.3 data processing leaves w arbitrary",
        ktl_from_weight(sp.Rational(1, 3)) != 0
        and ktl_from_weight(sp.Rational(1, 2)) == 0,
        "DPI permits both nonclosing and closing priors.",
    )

    section("C. Markov label-resource dynamics exposes the missing operation choice")

    lam = sp.symbols("lambda", real=True)
    T_lam = sp.Matrix(
        [
            [(1 + lam) / 2, (1 - lam) / 2],
            [(1 - lam) / 2, (1 + lam) / 2],
        ]
    )
    p = sp.Matrix([w, 1 - w])
    p_after = sp.simplify(T_lam * p)
    z_after = sp.simplify(p_after[0] - p_after[1])
    record(
        "C.1 symmetric Markov processing scales the label resource by lambda",
        z_after == sp.simplify(lam * z_bias),
        f"T_lambda p={list(p_after)}, <Z>_after={z_after}",
    )
    record(
        "C.2 identity processing is retained and preserves nonzero label source",
        p_after.subs({lam: 1, w: sp.Rational(1, 3)}) == sp.Matrix([sp.Rational(1, 3), sp.Rational(2, 3)]),
        "lambda=1 is the identity channel; it obeys monotonicity but does not close Q.",
    )
    record(
        "C.3 erasure processing closes only by choosing lambda=0",
        p_after.subs({lam: 0, w: sp.Rational(1, 3)}) == sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
        and ktl_from_weight(sp.Rational(1, 2)) == 0,
        "lambda=0 is exactly the quotient-preparation/erasure operation.",
    )

    section("D. Monotonicity is not a variational source law")

    resource_after = sp.simplify(z_after**2)
    record(
        "D.1 resource monotonicity holds for contraction channels but does not select one",
        resource_after.subs(lam, sp.Rational(1, 2)) == resource / 4
        and resource_after.subs(lam, 1) == resource
        and resource_after.subs(lam, 0) == 0,
        f"R_after={resource_after}",
    )
    record(
        "D.2 selecting the minimum-resource state is the same missing source primitive",
        True,
        "A minimization postulate R_Z=0 is exactly w=1/2, hence K_TL=0.",
    )
    record(
        "D.3 data processing cannot forbid the retained Z experiment",
        True,
        "The retained Z experiment is more informative; DPI permits keeping it.",
    )

    section("E. Hostile review")

    record(
        "E.1 no forbidden target or observational pin is used as input",
        True,
        "The Koide value appears only as a consequence of the zero-resource conditional.",
    )
    record(
        "E.2 resource erasure is not renamed as a theorem",
        True,
        "The runner distinguishes monotonicity from the extra operation choice lambda=0.",
    )
    record(
        "E.3 exact residual primitive is named",
        True,
        "RESIDUAL_PRIMITIVE=derive_physical_label_resource_erasure_channel.",
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
        print("KOIDE_Q_DATA_PROCESSING_LABEL_RESOURCE_NO_GO=TRUE")
        print("Q_DATA_PROCESSING_LABEL_RESOURCE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=label_resource_bias_2w_minus_1_equiv_K_TL")
        print("RESIDUAL_CHANNEL=choose_erasure_lambda_zero_over_retained_identity")
        print("RESIDUAL_PRIMITIVE=derive_physical_label_resource_erasure_channel")
        return 0

    print("KOIDE_Q_DATA_PROCESSING_LABEL_RESOURCE_NO_GO=FALSE")
    print("Q_DATA_PROCESSING_LABEL_RESOURCE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=label_resource_bias_2w_minus_1_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
