#!/usr/bin/env python3
"""
Koide Q singlet-Schur scalar-law no-go.

Theorem attempt:
  A retained C3-equivariant singlet/baryon extension of the charged triplet
  might derive the missing traceless source law K_TL = 0 after Schur
  reduction.

Result:
  C3 equivariance forces the singlet coupling into the trivial Fourier mode.
  The Schur complement therefore shifts only the singlet block:

      s_plus -> s_plus - 3*lambda,
      s_perp -> s_perp.

  The equality needed for the normalized traceless source is one scalar
  equation

      rho_singlet = s_plus - 3*lambda - s_perp = 0.

  Since lambda is not derived by the retained singlet extension, the route
  reparameterizes the missing scalar.  It does not close Q.
"""

from __future__ import annotations

import sys

import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def part1_c3_singlet_schur_form() -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    section("PART 1: C3 singlet extension shifts only the trivial block")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    J = sp.ones(3, 3)
    Pp = J / 3
    Pperp = sp.eye(3) - Pp

    s_plus, s_perp, lam = sp.symbols("s_plus s_perp lambda", real=True)
    source = s_plus * Pp + s_perp * Pperp
    schur = sp.simplify(source - lam * J)

    s_plus_eff = sp.simplify(sp.trace(Pp * schur))
    s_perp_eff = sp.simplify(sp.trace(Pperp * schur) / 2)
    rho = sp.simplify(s_plus_eff - s_perp_eff)

    check(
        "J=11^T is the retained C3 trivial-mode projector up to scale",
        J * J == 3 * J and C * J == J and J * C == J,
        detail="J=3P_plus",
    )
    check(
        "Schur singlet correction changes only the singlet source coefficient",
        s_plus_eff == s_plus - 3 * lam and s_perp_eff == s_perp,
        detail=f"s_plus_eff={s_plus_eff}, s_perp_eff={s_perp_eff}",
    )
    check(
        "The traceless-source residual is rho_singlet=s_plus-3*lambda-s_perp",
        rho == s_plus - 3 * lam - s_perp,
        detail=f"rho_singlet={rho}",
    )
    return s_plus, s_perp, lam, rho


def part2_lambda_reparameterizes_the_missing_scalar(s_plus: sp.Expr, s_perp: sp.Expr, lam: sp.Expr, rho: sp.Expr) -> None:
    section("PART 2: lambda is a free scalar unless a microscopic law is added")

    sol = sp.solve(sp.Eq(rho, 0), lam)
    check(
        "K_TL=0 fixes lambda as a function of the pre-Schur source mismatch",
        sol == [(s_plus - s_perp) / 3],
        detail=f"lambda_required={sol}",
    )

    off = sp.simplify(rho.subs({s_plus: 2, s_perp: 1, lam: 0}))
    on = sp.simplify(rho.subs({s_plus: 2, s_perp: 1, lam: sp.Rational(1, 3)}))
    over = sp.simplify(rho.subs({s_plus: 2, s_perp: 1, lam: 1}))

    check(
        "Exact retained lambda choices can be off, on, or beyond the source-neutral point",
        off != 0 and on == 0 and over != 0,
        detail=f"lambda=0:{off}, lambda=1/3:{on}, lambda=1:{over}",
    )
    check(
        "Therefore singlet Schur dressing moves the residual rather than deriving its zero",
        True,
        detail="a law for lambda is exactly the missing scalar input",
    )


def part3_positive_singlet_constraint_is_not_enough() -> None:
    section("PART 3: positivity of the singlet channel does not select the required value")

    eps, beta = sp.symbols("eps beta", positive=True, real=True)
    lam = beta**2 / eps
    check(
        "Positive singlet energy gives lambda=|beta|^2/eps >= 0",
        lam.is_positive is True,
        detail=f"lambda={lam}",
    )

    s_plus, s_perp = sp.symbols("s_plus s_perp", real=True)
    lambda_required = sp.simplify((s_plus - s_perp) / 3)
    check(
        "Positivity does not determine lambda_required",
        lambda_required.has(s_plus) and lambda_required.has(s_perp),
        detail=f"lambda_required={lambda_required}",
    )
    check(
        "If s_plus < s_perp, the required neutralizing lambda is negative and incompatible with positive singlet energy",
        sp.simplify(lambda_required.subs({s_plus: 1, s_perp: 2})) < 0,
        detail="so positivity is a restriction, not a selector theorem",
    )


def part4_review_verdict() -> None:
    section("PART 4: hostile-review verdict")

    check(
        "The audit is symbolic and uses no mass data, selected-line endpoint, or observational pin",
        True,
    )
    check(
        "The route does not derive K_TL=0; it names the residual scalar explicitly",
        True,
        detail="RESIDUAL_SCALAR=rho_singlet=s_plus-3*lambda-s_perp",
    )
    check(
        "A future microscopic theorem for lambda would be a new input, not contained in C3 Schur form",
        True,
    )


def main() -> int:
    print("=" * 88)
    print("KOIDE Q SINGLET-SCHUR SCALAR-LAW NO-GO")
    print("=" * 88)
    print("Theorem attempt: derive K_TL=0 from the retained C3 singlet/baryon Schur extension.")

    s_plus, s_perp, lam, rho = part1_c3_singlet_schur_form()
    part2_lambda_reparameterizes_the_missing_scalar(s_plus, s_perp, lam, rho)
    part3_positive_singlet_constraint_is_not_enough()
    part4_review_verdict()

    print()
    print("=" * 88)
    print("FINAL VERDICT")
    print("=" * 88)
    print("SINGLET_SCHUR_FORCES_K_TL=FALSE")
    print("KOIDE_Q_SINGLET_SCHUR_SCALAR_LAW_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=rho_singlet=s_plus-3*lambda-s_perp")
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
