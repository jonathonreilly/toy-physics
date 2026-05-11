#!/usr/bin/env python3
"""Bounded runner for canonical mass-coupling linearity.

The runner checks the narrow theorem in
docs/CLOSURE_C_BB_CANONICAL_MASS_COUPLING_NOTE_2026-05-10_cBB.md:

Given a canonical scalar mass term S_m = m * sum_x n_x and a supplied
Born/source density rho_grav(x) = <n_x>, the local source contribution is
rho_mass(x; m) = m * rho_grav(x).  The check is symbolic/algebraic and
does not add a new framework premise or promote the parent gravity chain.

Target: PASS=10, FAIL=0.
"""

from __future__ import annotations

import sys

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


section("Canonical mass term is affine in the scalar mass parameter")

m = sp.Symbol("m", real=True)
alpha = sp.Symbol("alpha", real=True)
n = sp.Symbol("n", real=True)
S_m = m * n

check(
    "d/dm of the canonical mass term is the density operator",
    sp.simplify(sp.diff(S_m, m) - n) == 0,
    detail=f"d(m*n)/dm={sp.diff(S_m, m)}",
)

check(
    "all higher m-derivatives vanish for the canonical mass term",
    sp.simplify(sp.diff(S_m, m, 2)) == 0,
    detail=f"d2(m*n)/dm2={sp.diff(S_m, m, 2)}",
)

rho = [sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)]
m0 = sp.Rational(5, 7)
rho_mass = [m0 * r for r in rho]

check(
    "local source equals m*rho_grav at each site",
    rho_mass == [sp.Rational(5, 14), sp.Rational(5, 21), sp.Rational(5, 42)],
    detail=f"rho_mass={rho_mass}",
)

check(
    "integrated source equals m for a normalized one-particle density",
    sp.simplify(sum(rho_mass) - m0) == 0,
    detail=f"sum={sum(rho_mass)}",
)

alpha0 = sp.Rational(11, 5)
scaled = [(alpha0 * m0) * r for r in rho]
alpha_scaled = [alpha0 * v for v in rho_mass]

check(
    "homogeneity: rho_mass(alpha*m) = alpha*rho_mass(m)",
    all(sp.simplify(a - b) == 0 for a, b in zip(scaled, alpha_scaled)),
    detail=f"alpha={alpha0}",
)

section("Independent species add linearly")

rho1 = [sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(0)]
rho2 = [sp.Rational(0), sp.Rational(1, 3), sp.Rational(2, 3)]
m1 = sp.Rational(2, 5)
m2 = sp.Rational(7, 11)
combined = [m1 * a + m2 * b for a, b in zip(rho1, rho2)]

check(
    "distinct species source is sum_i m_i*rho_i(x)",
    combined == [
        sp.Rational(1, 5),
        sp.Rational(1, 5) + sp.Rational(7, 33),
        sp.Rational(14, 33),
    ],
    detail=f"combined={combined}",
)

shared_profile = rho
shared_total = [(m1 + m2) * r for r in shared_profile]
shared_sum = [m1 * r + m2 * r for r in shared_profile]

check(
    "same-profile species reduce to M*rho with M=sum_i m_i",
    all(sp.simplify(a - b) == 0 for a, b in zip(shared_total, shared_sum)),
    detail=f"M={sp.simplify(m1 + m2)}",
)

check(
    "different profiles are not collapsed to one common density by this lemma",
    combined != [(m1 + m2) * r for r in rho],
    detail="linear superposition is the scoped statement",
)

section("Nonlinear replacements fail the canonical linear-source gate")

def nonlinear_fails_homogeneity(expr: sp.Expr) -> bool:
    lhs = expr.subs(m, alpha0 * m0)
    rhs = alpha0 * expr.subs(m, m0)
    return sp.simplify(lhs - rhs) != 0


nonlinear_forms = {
    "m^2": m**2,
    "sqrt(m)": sp.sqrt(m),
    "exp(m)": sp.exp(m),
    "1/m": 1 / m,
}

check(
    "standard nonlinear replacements fail homogeneity at the test point",
    all(nonlinear_fails_homogeneity(expr) for expr in nonlinear_forms.values()),
    detail=", ".join(nonlinear_forms),
)

q = sp.Symbol("q", real=True)
linear_family = q * m

check(
    "the homogeneous additive scalar family is q*m",
    sp.simplify(linear_family.subs(m, alpha * m) - alpha * linear_family) == 0,
    detail="q is a convention/normalization coefficient",
)

print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
sys.exit(1 if FAIL > 0 else 0)
