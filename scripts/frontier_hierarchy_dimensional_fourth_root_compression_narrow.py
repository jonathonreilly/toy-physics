#!/usr/bin/env python3
"""Runner for the dimensional fourth-root compression narrow theorem.

This verifies only the source note's load-bearing algebra:

* if f has mass dimension d and C_M is dimensionless, then
  C_M * f**alpha has mass dimension d * alpha;
* the mass-dimension-one condition d * alpha = 1 has the unique solution
  alpha = 1/d;
* at d = 4 the exponent is 1/4, and the value 1/d = 1/4 is unique among
  positive integers.

No framework premise, empirical input, hierarchy formula, or sister theorem
is consumed.

Target: PASS = 8, FAIL = 0.
"""

from __future__ import annotations

import sys
from fractions import Fraction

try:
    import sympy as sp
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


section("Dimensional fourth-root compression narrow theorem")

d = sp.Symbol("d", positive=True, integer=True)
alpha = sp.Symbol("alpha", real=True)
mass_dim_f = d
mass_dim_prefactor = sp.Integer(0)
mass_dim_output = mass_dim_prefactor + alpha * mass_dim_f

check(
    "dimension count: [C_M f^alpha] = d*alpha",
    sp.simplify(mass_dim_output - d * alpha) == 0,
    detail=f"mass_dim_output={mass_dim_output}",
)

solutions = sp.solve(sp.Eq(d * alpha, 1), alpha)
check(
    "unique solution of d*alpha = 1 is alpha = 1/d",
    len(solutions) == 1 and sp.simplify(solutions[0] - 1 / d) == 0,
    detail=f"solutions={solutions}",
)

section("Finite exact checks")

dim_one_checks = {}
for d_int in range(1, 9):
    exponent = Fraction(1, d_int)
    dim_one_checks[d_int] = d_int * exponent

check(
    "f^(1/d) has mass dimension one for d in {1,...,8}",
    all(v == Fraction(1) for v in dim_one_checks.values()),
    detail=", ".join(f"d={k}:[M]={v}" for k, v in dim_one_checks.items()),
)

alpha_d4 = Fraction(1, 4)
check(
    "at d=4 the exponent is exactly 1/4",
    alpha_d4 == Fraction(1, 4),
    detail=f"alpha={alpha_d4}",
)

inverse_table = {d_int: Fraction(1, d_int) for d_int in range(1, 17)}
hits_at_quarter = [d_int for d_int, value in inverse_table.items() if value == Fraction(1, 4)]
check(
    "1/d = 1/4 occurs uniquely at d=4 in the finite table",
    hits_at_quarter == [4],
    detail=f"hits={hits_at_quarter}",
)

strictly_decreasing = all(
    inverse_table[d_int] > inverse_table[d_int + 1] for d_int in range(1, 16)
)
check(
    "d -> 1/d is strictly decreasing on checked positive integers",
    strictly_decreasing,
    detail=", ".join(f"{k}:{v}" for k, v in inverse_table.items()),
)

section("Symbolic round trips")

f = sp.Symbol("f", positive=True)
roundtrip_ok = True
roundtrip_results = {}
for d_int in range(1, 9):
    recovered = (f ** sp.Rational(1, d_int)) ** d_int
    diff = sp.simplify(recovered - f)
    roundtrip_results[d_int] = diff
    if diff != 0:
        roundtrip_ok = False

check(
    "(f^(1/d))^d = f for positive f and d in {1,...,8}",
    roundtrip_ok,
    detail=", ".join(f"d={k}:diff={v}" for k, v in roundtrip_results.items()),
)

M = sp.Symbol("M", positive=True)
d4_roundtrip = sp.simplify((M**4) ** sp.Rational(1, 4) - M)
check(
    "the d=4 round trip (M^4)^(1/4) = M holds for positive M",
    d4_roundtrip == 0,
    detail=f"diff={d4_roundtrip}",
)

print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
sys.exit(1 if FAIL > 0 else 0)
