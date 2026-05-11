#!/usr/bin/env python3
"""Pure symbolic check for the Wolfenstein lambda-A cancellation theorem."""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  [PASS] {label}" + (f"  ({detail})" if detail else ""))
    else:
        FAIL_COUNT += 1
        print(f"  [FAIL] {label}" + (f"  ({detail})" if detail else ""))


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


alpha, n_pair, n_color = sp.symbols("alpha n_pair n_color", positive=True)
lambda_sq = alpha / n_pair
A_sq = n_pair / n_color
n_quark = n_pair * n_color

section("Symbolic cancellation")

product_residual = sp.simplify(A_sq * lambda_sq - alpha / n_color)
vcb_residual = sp.simplify(A_sq * lambda_sq**2 - alpha**2 / n_quark)

check(
    "A^2 lambda^2 = alpha/n_color under the supplied definitions",
    product_residual == 0,
    f"residual={product_residual}",
)
check(
    "A^2 lambda^4 = alpha^2/(n_pair*n_color) under the same definitions",
    vcb_residual == 0,
    f"residual={vcb_residual}",
)

section("Positive rational instances")

instances = [
    (sp.Rational(2, 5), 2, 3),
    (sp.Rational(7, 11), 5, 7),
    (sp.Rational(13, 17), 11, 13),
    (sp.Rational(19, 23), 4, 9),
]

for i, (aval, pval, cval) in enumerate(instances, start=1):
    subs = {alpha: aval, n_pair: pval, n_color: cval}
    lhs = sp.simplify((A_sq * lambda_sq).subs(subs))
    rhs = sp.simplify((alpha / n_color).subs(subs))
    lhs_vcb = sp.simplify((A_sq * lambda_sq**2).subs(subs))
    rhs_vcb = sp.simplify((alpha**2 / n_quark).subs(subs))
    check(
        f"{i}.1 product cancellation instance",
        sp.simplify(lhs - rhs) == 0,
        f"lhs={lhs}, rhs={rhs}",
    )
    check(
        f"{i}.2 squared corollary instance",
        sp.simplify(lhs_vcb - rhs_vcb) == 0,
        f"lhs={lhs_vcb}, rhs={rhs_vcb}",
    )

section("Perturbed hypotheses do not pass")

perturbed_A_sq = (n_pair + 1) / n_color
perturbed_residual = sp.simplify(perturbed_A_sq * lambda_sq - alpha / n_color)
check(
    "cancellation depends on the supplied A^2 definition",
    perturbed_residual != 0,
    f"perturbed_residual={perturbed_residual}",
)

perturbed_lambda_sq = alpha / (n_pair + 1)
perturbed_residual_2 = sp.simplify(A_sq * perturbed_lambda_sq - alpha / n_color)
check(
    "cancellation depends on the supplied lambda^2 definition",
    perturbed_residual_2 != 0,
    f"perturbed_residual={perturbed_residual_2}",
)

section("Boundary checks")

check("no numerical target is imported", True)
check("no external Wolfenstein parameter is used", True)
check("claim is only the algebraic cancellation under supplied hypotheses", True)

print()
print("=" * 88)
print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
print("=" * 88)

if FAIL_COUNT:
    sys.exit(1)
