#!/usr/bin/env python3
"""Audit the boundary spectral-radius quarter lane honestly.

This runner encodes a sharpened obstruction:
  - stochastic/Markov-normalized transfer carriers cannot give rho = exp(1/4);
  - parameter-free finite algebraic carriers cannot give rho = exp(1/4);
  - on scaled Gibbs/Perron families, exact quarter is a tuning equation for
    the extra normalization parameter mu;
  - the canonical unscaled Ising-type boundary family misses the target.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def perron_root(matrix: sp.Matrix) -> sp.Expr:
    vals = matrix.eigenvals()
    return max(vals, key=lambda expr: abs(complex(sp.N(expr, 50))))


def scaled_mu_star(rho_base: sp.Expr) -> sp.Expr:
    return sp.Rational(1, 4) - sp.log(rho_base)


def main() -> int:
    note = normalized(NOTE)
    target_root = sp.exp(sp.Rational(1, 4))
    target_pressure = sp.Rational(1, 4)
    n_pass = 0
    n_fail = 0

    print("Planck boundary spectral-radius quarter theorem lane audit")
    print("=" * 78)

    section("PART 1: TARGET ROOT / PRESSURE")
    p = check(
        "quarter pressure is exactly equivalent to rho = exp(1/4)",
        sp.simplify(sp.log(target_root) - target_pressure) == 0,
        "log(exp(1/4)) = 1/4 exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the target root exp(1/4) is transcendental",
        target_root.is_transcendental is True and target_root.is_algebraic is False,
        "Lindemann-Weierstrass puts the exact target outside the algebraic class",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: STOCHASTIC / MARKOV NORMALIZATION NO-GO")
    stochastic_examples = {
        "binary fair chain": sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)],
                                         [sp.Rational(1, 2), sp.Rational(1, 2)]]),
        "biased 3-state chain": sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 6)],
                                            [sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4)],
                                            [sp.Rational(1, 5), sp.Rational(1, 5), sp.Rational(3, 5)]])
    }
    stochastic_ok = True
    for name, matrix in stochastic_examples.items():
        rho = perron_root(matrix)
        stochastic_ok &= sp.simplify(rho - 1) == 0
        print(f"  sample {name:28s} rho = {sp.N(rho, 16)}")

    p = check(
        "representative stochastic carriers have spectral radius 1, not exp(1/4)",
        stochastic_ok and sp.simplify(1 - target_root) != 0,
        "a probability transfer law cannot realize the quarter-growth target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: PARAMETER-FREE ALGEBRAIC NO-GO")
    algebraic_examples = {
        "full-shift 2x2": sp.Matrix([[1, 1], [1, 1]]),
        "Fibonacci": sp.Matrix([[1, 1], [1, 0]]),
        "radical-weighted": sp.Matrix([[sp.sqrt(2), 1], [1, sp.sqrt(3)]]),
    }
    algebraic_ok = True
    for name, matrix in algebraic_examples.items():
        rho = perron_root(matrix)
        algebraic_ok &= rho.is_algebraic is True and sp.simplify(rho - target_root) != 0
        print(f"  sample {name:28s} rho = {sp.N(rho, 16)}")

    p = check(
        "representative parameter-free algebraic carriers miss exp(1/4)",
        algebraic_ok,
        "their Perron roots stay algebraic, whereas the target root is transcendental",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: SCALE-FAMILY TUNING THEOREM")
    base_examples = {
        "full shift": sp.Matrix([[1, 1], [1, 1]]),
        "Fibonacci": sp.Matrix([[1, 1], [1, 0]]),
        "rank-one projector": sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)],
                                          [sp.Rational(1, 2), sp.Rational(1, 2)]]),
    }
    tuning_ok = True
    for name, base in base_examples.items():
        rho_base = perron_root(base)
        mu_star = scaled_mu_star(rho_base)
        rho_scaled = sp.exp(mu_star) * rho_base
        tuning_ok &= sp.simplify(rho_scaled - target_root) == 0
        print(
            f"  base {name:28s} rho(B) = {sp.N(rho_base, 16)}   "
            f"mu_* = {sp.N(mu_star, 16)}"
        )

    p = check(
        "on every tested scaled family the quarter condition just fixes mu_*",
        tuning_ok,
        "rho(e^mu B) = exp(mu) rho(B), so exact quarter is a one-parameter tuning law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: CANONICAL UNSCALED ISING-TYPE FAMILY MISSES THE TARGET")
    J = sp.symbols("J", real=True)
    rho_ising = sp.exp(J) + sp.exp(-J)
    p = check(
        "the symmetric unscaled Ising family has rho(J) = 2 cosh(J)",
        sp.simplify(rho_ising - 2 * sp.cosh(J)) == 0,
        "the eigenvalues are e^J +/- e^(-J), so the Perron root is 2 cosh(J)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    sample_J = [sp.Integer(0), sp.Rational(1, 2), 1]
    sample_gap_ok = True
    for val in sample_J:
        rho_val = sp.N(rho_ising.subs(J, val), 30)
        sample_gap_ok &= float(rho_val) > float(sp.N(target_root, 30))
        mu_star = sp.N(target_pressure - sp.log(rho_ising.subs(J, val)), 30)
        print(
            f"  Ising J={float(sp.N(val, 6)):>6.3f}: rho(B(J))={float(rho_val):.12f}, "
            f"mu_*(J)={float(mu_star):.12f}"
        )

    p = check(
        "the unscaled Ising family stays strictly above the target root",
        sample_gap_ok and float(sp.N(target_root, 30)) < 2.0,
        "since 2 cosh(J) >= 2 > exp(1/4), this family cannot hit quarter without extra scaling",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: NOTE HONESTY")
    p = check(
        "the note explicitly names stochastic normalization as a dead class",
        "stochastic / markov-normalized boundary carrier" in note
        or "stochastic / markov normalization" in note,
        "the first obstruction class is stated directly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly says scaled families reduce quarter to mu tuning",
        "mu = 1/4 - log rho(b(theta))" in note
        and "tuning equation" in note,
        "the load-bearing obstruction is written as an exact formula",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly leaves only a new parameter-free normalization principle",
        "new parameter-free gravitational normalization principle" in note,
        "the surviving constructive target is spelled out",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "Exact boundary pressure 1/4 is not forced by the currently natural "
        "finite-state transfer classes. Stochastic carriers fix rho=1, "
        "parameter-free algebraic carriers miss the transcendental target, "
        "and scaled Gibbs/Perron families realize quarter only by tuning the "
        "extra normalization parameter mu."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
