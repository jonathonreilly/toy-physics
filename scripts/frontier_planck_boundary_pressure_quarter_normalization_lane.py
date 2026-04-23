#!/usr/bin/env python3
"""Audit the boundary pressure quarter normalization lane honestly.

This runner encodes the strongest current result on the boundary-pressure
normalization problem:

  - the time-locked collective Schur class still carries an affine
    normalization gauge G -> lambda G + mu I;
  - on the exact rational Schur witness, quarter pressure is the tuning line
    mu = lambda + 1/4;
  - standard canonical normalizations either kill the route, miss quarter,
    or realize it only as a trivial identity shift;
  - exact 3+1 democracy does not force quarter except in the scalar case.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md"
TRANSFER = ROOT / "docs/PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md"
SPECTRAL = ROOT / "docs/PLANCK_SCALE_BOUNDARY_SPECTRAL_RADIUS_QUARTER_THEOREM_LANE_2026-04-23.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"


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


def top_eigenvalue(matrix: sp.Matrix) -> sp.Expr:
    values = matrix.eigenvals()
    return max(values, key=lambda expr: float(sp.N(sp.re(expr), 50)))


def main() -> int:
    note = normalized(NOTE)
    transfer_note = normalized(TRANSFER)
    spectral_note = normalized(SPECTRAL)
    timelock_note = normalized(TIMELOCK)

    n_pass = 0
    n_fail = 0

    print("Planck boundary pressure quarter normalization lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM BOUNDARY / TIME-LOCK EVIDENCE")
    p = check(
        "time-lock still fixes a_s = c a_t exactly",
        "a_s = c a_t" in timelock_note and "beta = 1" in timelock_note,
        "the normalization problem is posed only after the exact space/time lock",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "transfer-operator note still phrases the target as sup spec(G_Sigma) = 1/4",
        "sup spec(g_sigma) = 1/4" in transfer_note,
        "the current lane should attack the additive pressure target directly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "spectral-radius note still records stochastic normalization as dead",
        "stochastic / markov" in spectral_note and "rho(t) = 1" in spectral_note,
        "the new lane inherits that negative class instead of reopening it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT WITNESS AND AFFINE GAUGE")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    expected_eigs = {sp.Integer(1), sp.Rational(5, 3)}
    p = check(
        "the exact Schur witness has eigenvalues {1, 5/3}",
        set(l_sigma.eigenvals().keys()) == expected_eigs,
        "this is the same rational collective boundary witness already on the branch",
    )
    n_pass += int(p)
    n_fail += int(not p)

    lam, mu = sp.symbols("lam mu", positive=True, real=True)
    g_affine = mu * sp.eye(2) - lam * l_sigma
    affine_eigs = set(sp.factor(ev) for ev in g_affine.eigenvals().keys())
    expected_affine = {mu - lam, mu - sp.Rational(5, 3) * lam}
    affine_ok = all(
        any(sp.simplify(found - expected) == 0 for expected in expected_affine)
        for found in affine_eigs
    ) and len(affine_eigs) == len(expected_affine)
    p = check(
        "the affine same-surface family has eigenvalues mu-lambda and mu-5 lambda/3",
        affine_ok,
        "positive rescaling plus identity shift preserves the same witness class",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "quarter pressure on the witness is exactly the tuning line mu = lambda + 1/4",
        sp.solve(sp.Eq(mu - lam, sp.Rational(1, 4)), mu) == [lam + sp.Rational(1, 4)],
        "the current boundary class leaves a one-parameter affine family of quarter points",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: STANDARD NORMALIZATIONS MISS QUARTER")
    g_trace = l_sigma / sp.trace(l_sigma)
    p = check(
        "trace-one positive normalization gives top pressure 5/8, not 1/4",
        sp.simplify(top_eigenvalue(g_trace) - sp.Rational(5, 8)) == 0,
        "G_tr = L_Sigma / Tr(L_Sigma) has eigenvalues 5/8 and 3/8",
    )
    n_pass += int(p)
    n_fail += int(not p)

    centered = l_sigma - sp.trace(l_sigma) * sp.eye(2) / 2
    centered_eigs = set(centered.eigenvals().keys())
    p = check(
        "the centered witness has eigenvalues +-1/3",
        centered_eigs == {sp.Rational(1, 3), -sp.Rational(1, 3)},
        "trace-zero centering isolates the nontrivial boundary shape but not its scale",
    )
    n_pass += int(p)
    n_fail += int(not p)

    g_op = centered / sp.Rational(1, 3)
    p = check(
        "operator-norm normalization gives top pressure 1",
        sp.simplify(top_eigenvalue(g_op) - 1) == 0,
        "||C||_op = 1/3, so dividing by it does not produce quarter",
    )
    n_pass += int(p)
    n_fail += int(not p)

    frob_sq = sp.simplify(sum(entry**2 for entry in centered))
    g_frob = centered / sp.sqrt(frob_sq)
    p = check(
        "Frobenius normalization gives top pressure 1/sqrt(2)",
        sp.simplify(top_eigenvalue(g_frob) - 1 / sp.sqrt(2)) == 0,
        "||C||_F = sqrt(2)/3, so Frobenius normalization still misses quarter",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: DEMOCRATIC 3+1 TRACE NORMALIZATION DOES NOT FORCE QUARTER")
    g_iso = sp.eye(4) / 4
    g_nontrivial = sp.diag(sp.Rational(1, 2), sp.Rational(1, 6), sp.Rational(1, 6), sp.Rational(1, 6))
    p = check(
        "trace-one democratic scalar generator realizes quarter only in the trivial identity case",
        sp.trace(g_iso) == 1
        and sp.simplify(top_eigenvalue(g_iso) - sp.Rational(1, 4)) == 0
        and sp.trace(g_nontrivial) == 1
        and sp.simplify(top_eigenvalue(g_nontrivial) - sp.Rational(1, 2)) == 0,
        (
            "on the 4-channel trace-one class, quarter is compatible with I_4/4 but a "
            "nontrivial positive generator already jumps above it"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE HONESTY")
    p = check(
        "the note states the affine normalization gauge explicitly",
        "g -> lambda g + mu i" in note and "p_* -> lambda p_* + mu" in note,
        "the core no-go is the affine normalization freedom on pressure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the exact witness tuning line mu = lambda + 1/4",
        "mu = lambda + 1/4" in note,
        "the underdetermined quarter condition should be written in explicit coordinates",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note names the failed standard normalizations and the 3+1 democracy obstruction",
        "5/8" in note
        and "1/sqrt(2)" in note
        and ("3+1 democracy" in note or "dimension counting does not rescue quarter" in note),
        "the no-go should cover both matrix-normalization and dimension-counting rescue attempts",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note does not overclaim closure",
        "does **not** prove" in note and "not yet" in note,
        "this lane should remain an obstruction note, not a fake Planck close",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The time-locked collective boundary Schur class still carries an affine "
        "pressure gauge. On the exact rational witness, quarter is a tuning line, "
        "not a theorem consequence. Standard parameter-free normalizations either "
        "miss 1/4 or realize it only as a trivial identity shift."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
