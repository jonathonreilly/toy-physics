#!/usr/bin/env python3
"""Runner for the 1D submultiplicativity tautological-bound note.

The runner verifies only the bounded support statement:
for A_k(x) = alpha_LM * x on R, ||A_15 ... A_0|| = alpha_LM^16.
It does not identify this scalar model with a physical blocking operator.
"""

from __future__ import annotations

import sys
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 80

ROOT = Path(__file__).resolve().parent.parent
NOTE = (
    ROOT
    / "docs"
    / "BOUGEROL_LACROIX_STAGGERED_BLOCKING_SUBMULT_TAUTOLOGICAL_BOUND_BOUNDED_THEOREM_NOTE_2026-05-10.md"
)

PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286209"
)
P_AVG = Decimal("0.5934")
ALPHA_BARE = Decimal(1) / (Decimal(4) * PI)
U0 = P_AVG ** (Decimal(1) / Decimal(4))
ALPHA_LM = ALPHA_BARE / U0
ALPHA_LM_REFERENCE = Decimal("0.09066783601728631")
STEPS = 16

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


def norm_1d(scalar: Decimal) -> Decimal:
    return abs(scalar)


def product_power(alpha: Decimal, steps: int) -> Decimal:
    value = Decimal(1)
    for _ in range(steps):
        value *= alpha
    return value


def main() -> int:
    print("=" * 76)
    print("1D SUBMULTIPLICATIVITY TAUTOLOGICAL-BOUND RUNNER")
    print("=" * 76)

    rel_err = abs(ALPHA_LM - ALPHA_LM_REFERENCE) / ALPHA_LM_REFERENCE
    check(
        "alpha_LM matches the canonical same-surface value",
        rel_err < Decimal("1e-15"),
        f"alpha_LM={ALPHA_LM:.18}",
    )

    check("alpha_LM is a contraction input", Decimal(0) < ALPHA_LM < Decimal(1))

    single_step_norms = [norm_1d(ALPHA_LM) for _ in range(STEPS)]
    check(
        "each 1D operator has norm alpha_LM",
        all(abs(n - ALPHA_LM) < Decimal("1e-70") for n in single_step_norms),
    )

    product_scalar = product_power(ALPHA_LM, STEPS)
    product_norm = norm_1d(product_scalar)
    alpha_power = ALPHA_LM ** STEPS
    check(
        "direct product norm equals alpha_LM^16",
        abs(product_norm - alpha_power) < Decimal("1e-70"),
        f"alpha_LM^16={alpha_power:.6e}",
    )

    product_of_norms = Decimal(1)
    for single_norm in single_step_norms:
        product_of_norms *= single_norm
    check(
        "submultiplicativity is saturated in the 1D scalar model",
        abs(product_norm - product_of_norms) < Decimal("1e-70"),
    )

    mu = [ALPHA_LM ** k for k in range(STEPS + 1)]
    ratios = [mu[k + 1] / mu[k] for k in range(STEPS)]
    check(
        "rung ratios are alpha_LM by construction",
        all(abs(r - ALPHA_LM) < Decimal("1e-70") for r in ratios),
    )
    check(
        "mu_16 / mu_0 equals the same product norm",
        abs((mu[STEPS] / mu[0]) - product_norm) < Decimal("1e-70"),
    )

    counter_alpha = Decimal("0.5")
    check(
        "the identity does not select alpha_LM",
        product_power(counter_alpha, STEPS) == counter_alpha ** STEPS,
        "counterexample alpha=0.5 also satisfies the identity",
    )

    counter_steps = 8
    check(
        "the identity does not select the step count 16",
        product_power(ALPHA_LM, counter_steps) == ALPHA_LM ** counter_steps,
        "N=8 also satisfies the same formula",
    )

    lambda_1 = ALPHA_LM.ln()
    check(
        "singleton-product Lyapunov exponent is log(alpha_LM)",
        abs((product_norm.ln() / Decimal(STEPS)) - lambda_1) < Decimal("1e-70"),
    )

    if NOTE.exists():
        body = NOTE.read_text()
        forbidden = [
            "closes the hierarchy formula",
            "derives alpha_LM",
            "derives the integer `16`",
        ]
        check(
            "note keeps the review boundary free of promotion language",
            all(item not in body for item in forbidden),
        )
    else:
        check("companion note exists", False, str(NOTE))

    print("=" * 76)
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    print("=" * 76)
    if FAIL == 0:
        print("VERDICT: bounded support only; no hierarchy closure")
        return 0
    print("VERDICT: runner failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
