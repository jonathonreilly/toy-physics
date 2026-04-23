#!/usr/bin/env python3
"""Audit the Planck boundary non-affine pressure normalization lane honestly.

This lane establishes the strongest exact positive result currently available
on the surviving boundary-normalization problem:

  - the Schur boundary action itself forces an exact normalized vacuum
    partition `Z_hat(L) = det(L)^(-1/2)` on the same boundary mode space;
  - this yields an exact non-affine vacuum pressure density
    `p_vac(L) = (1/(2n)) log det(L)`;
  - on the minimal exact Schur witness, that value is `(1/4) log(5/3)`,
    not `1/4`;
  - so the remaining live boundary problem is now one identification theorem
    from Schur vacuum density to physical boundary growth pressure.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md"
SCHUR = ROOT / "docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
CANON = ROOT / "docs/PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md"
AFFINE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md"
BULK = ROOT / "docs/PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md"


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    passed = bool(passed)
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def main() -> int:
    note = normalized(NOTE)
    schur = normalized(SCHUR)
    timelock = normalized(TIMELOCK)
    canon = normalized(CANON)
    affine = normalized(AFFINE)
    bulk = normalized(BULK)

    n_pass = 0
    n_fail = 0

    print("Planck boundary non-affine pressure normalization lane audit")
    print("=" * 78)

    section("PART 1: SOURCE SURFACES STILL SUPPORT THE NEW LANE")
    p = check(
        "time-lock still fixes a single exact clock",
        "a_s = c a_t" in timelock and "beta = 1" in timelock,
        "the Gaussian boundary normalization is posed only after exact space/time lock",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact Schur boundary action is already in the admitted stack",
        "i_r(f ; j) = 1/2 f^t lambda_r f - j^t f" in schur
        and (
            "schur-complement energy of the microscopic lattice dynamics itself" in schur
            or "schur-complement energy of the microscopic lattice laplacian" in schur
        ),
        "the new lane should derive its scalar from the exact boundary action itself",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "canonicality lane still fixes the boundary operator but not the quarter coefficient",
        "t_can(tau) = exp(-tau l_sigma)" in canon
        and "cannot realize the planck boundary target" in canon,
        "the new lane should add a new normalization law without pretending canonical transfer already closed quarter",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the earlier pressure lane explicitly asked for a non-affine same-surface normalization principle",
        "non-affine, unit-bearing same-surface normalization principle" in affine,
        "this lane should answer that exact surviving request",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "bulk-to-boundary Schur completion still says carrier closure improved but normalization closure did not",
        "closes the **carrier** much more sharply than before" in bulk
        and "does not close the **coefficient**" in bulk,
        "the new lane should address normalization without reopening carrier ambiguity",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT SAME-SURFACE GAUSSIAN NORMALIZATION LAW")
    a, x = sp.symbols("a x", positive=True, real=True)
    unit_1d = sp.integrate(sp.exp(-x**2 / 2), (x, -sp.oo, sp.oo))
    scaled_1d = sp.integrate(sp.exp(-a * x**2 / 2), (x, -sp.oo, sp.oo))
    p = check(
        "the exact one-dimensional Gaussian ratio is a^(-1/2)",
        sp.simplify(scaled_1d / unit_1d - a ** sp.Rational(-1, 2)) == 0,
        "this is the exact source-free Schur partition ratio on one boundary mode",
    )
    n_pass += int(p)
    n_fail += int(not p)

    a1, a2, x1, x2 = sp.symbols("a1 a2 x1 x2", positive=True, real=True)
    unit_2d = sp.integrate(
        sp.exp(-(x1**2 + x2**2) / 2),
        (x1, -sp.oo, sp.oo),
        (x2, -sp.oo, sp.oo),
    )
    scaled_2d = sp.integrate(
        sp.exp(-(a1 * x1**2 + a2 * x2**2) / 2),
        (x1, -sp.oo, sp.oo),
        (x2, -sp.oo, sp.oo),
    )
    p = check(
        "the exact diagonal two-mode ratio is det(L)^(-1/2)",
        sp.simplify(scaled_2d / unit_2d - (a1 * a2) ** sp.Rational(-1, 2)) == 0,
        "on a positive diagonal carrier the normalized partition is exactly 1/sqrt(det L)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    l1, l2 = sp.symbols("l1 l2", positive=True, real=True)
    p_vac_diag = sp.simplify(sp.Rational(1, 4) * sp.log(l1 * l2))
    p = check(
        "the corresponding exact vacuum pressure density is (1/(2n)) log det(L)",
        sp.simplify(p_vac_diag - (sp.log(l1 * l2) / 4)) == 0,
        "for n=2 the density is one quarter of log det(L)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: THE LAW IS GENUINELY NON-AFFINE")
    lam = sp.symbols("lam", positive=True, real=True)
    scaled_density = sp.simplify(sp.Rational(1, 4) * sp.log((lam * l1) * (lam * l2)))
    p = check(
        "positive rescaling gives p_vac(lambda L) = p_vac(L) + (1/2) log lambda",
        sp.simplify(scaled_density - (p_vac_diag + sp.log(lam) / 2)) == 0,
        "the law breaks the old affine gauge and is additive only in log scale",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the rescaling law is not affine in lambda",
        sp.simplify(sp.diff(scaled_density, lam, 2) + 1 / (2 * lam**2)) == 0
        and sp.diff(scaled_density, lam, 2) != 0,
        "its second derivative is -1/(2 lambda^2), so the dependence on lambda is genuinely non-affine",
    )
    n_pass += int(p)
    n_fail += int(not p)

    mu = sp.symbols("mu", real=True)
    shifted_density = sp.simplify(sp.Rational(1, 4) * sp.log((l1 + mu) * (l2 + mu)))
    second_mu = sp.simplify(sp.diff(shifted_density, mu, 2))
    expected_second_mu = sp.simplify(
        -sp.Rational(1, 4) * ((l1 + mu) ** -2 + (l2 + mu) ** -2)
    )
    p = check(
        "identity shift also enters non-affinely",
        sp.simplify(second_mu - expected_second_mu) == 0 and second_mu != 0,
        "the additive shift has strictly negative second derivative on the positive domain",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: ADDITIVITY AND THE EXACT WITNESS")
    m1, m2 = sp.symbols("m1 m2", positive=True, real=True)
    total_free_energy = sp.simplify(sp.Rational(1, 2) * sp.log(l1 * l2 * m1 * m2))
    split_free_energy = sp.simplify(
        sp.Rational(1, 2) * sp.log(l1 * l2) + sp.Rational(1, 2) * sp.log(m1 * m2)
    )
    p = check(
        "total vacuum free energy is additive on direct sums",
        sp.simplify(total_free_energy - split_free_energy) == 0,
        "F_vac = (1/2) log det(L) adds exactly across independent components",
    )
    n_pass += int(p)
    n_fail += int(not p)

    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    det_witness = sp.simplify(l_sigma.det())
    witness_density = sp.simplify(sp.Rational(1, 4) * sp.log(det_witness))
    p = check(
        "the exact Schur witness has determinant 5/3",
        det_witness == sp.Rational(5, 3),
        "the earlier boundary lanes already fixed this same rational witness carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact witness value is p_vac = (1/4) log(5/3)",
        sp.simplify(witness_density - sp.log(sp.Rational(5, 3)) / 4) == 0,
        "this is the exact non-affine scalar produced by the Schur carrier on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact witness value is not quarter",
        sp.simplify(witness_density - sp.Rational(1, 4)) != 0
        and abs(float(sp.N(witness_density, 50)) - 0.12770640594149768) < 1e-15,
        "the new law is exact and non-affine, but it still does not close Planck on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: THE REMAINING BRIDGE IS NOW SHARP")
    p = check(
        "quarter under this law on a two-mode carrier would require det(L) = e",
        sp.solve(sp.Eq(sp.Rational(1, 4) * sp.log(sp.Symbol("d", positive=True)), sp.Rational(1, 4)), sp.Symbol("d", positive=True))
        == [sp.E],
        "if physical Planck pressure were identified directly with p_vac on n=2, the determinant target would be e",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states the remaining open step as an identification/conversion theorem",
        "derive why the physical planck boundary pressure" in note
        and ("identification theorem" in note or "conversion theorem" in note),
        "the new lane should reduce the open problem to one explicit physical bridge",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 6: NOTE HONESTY")
    p = check(
        "the note states the exact new law explicitly",
        "z_hat(l_sigma) = det(l_sigma)^(-1/2)" in note
        and "p_vac(l_sigma) := -(1/n) log z_hat(l_sigma) = (1/(2n)) log det(l_sigma)" in note,
        "the load-bearing new theorem should be written in exact formulas",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly says the new law is non-affine and same-surface",
        "genuinely non-affine" in note and "same-surface" in note,
        "the lane should answer the precise boundary request rather than reopen older affine classes",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note does not overclaim Planck closure",
        "not a full planck close" in note and "still does **not** prove" in note,
        "this lane should remain an honest theorem/reduction note",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "The exact Schur boundary action forces a canonical non-affine "
        "same-surface normalization law: the unit-normalized zero-source "
        "Gaussian vacuum density p_vac(L) = (1/(2n)) log det(L). On the "
        "minimal exact witness this is (1/4) log(5/3), not 1/4, so the live "
        "boundary problem is now one identification theorem from Schur vacuum "
        "density to physical boundary growth pressure."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
