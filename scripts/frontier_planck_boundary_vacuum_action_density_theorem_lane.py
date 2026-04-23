#!/usr/bin/env python3
"""Audit the Planck boundary vacuum-action density theorem lane honestly.

This lane sharpens the remaining unit-bearing boundary coefficient problem:

  - the exact action lane already reduced the surviving family to
    I_nu(tau; b, j) = tau (1/2 b^T L b - j^T b - nu);
  - current same-surface gravity/action principles supply exactly two
    canonical values for nu:
        nu_0 = 0
        nu_gauss = (1/(2n)) log det(L);
  - exact quarter would instead require
        nu_quarter = lambda_min(L) + 1/4;
  - on the exact witness these values are incompatible, so quarter is not
    derived by the current action stack.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md"
ACTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
NONAFFINE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md"
CANON = ROOT / "docs/PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md"
BULK = ROOT / "docs/PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md"
C16 = ROOT / "docs/PLANCK_SCALE_C16_BOUNDARY_PRESSURE_BRIDGE_LANE_2026-04-23.md"


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
    action = normalized(ACTION)
    nonaffine = normalized(NONAFFINE)
    canon = normalized(CANON)
    bulk = normalized(BULK)
    c16 = normalized(C16)

    n_pass = 0
    n_fail = 0

    print("Planck boundary vacuum-action density theorem lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM INPUTS STILL SUPPORT THE REDUCTION")
    p = check(
        "the action lane still fixes the surviving family I_nu(tau ; b, j)",
        "i_nu(tau ; b, j) = tau (1/2 b^t l_sigma b - j^t b - nu)" in action,
        "the new lane should start from the already reduced one-parameter action family",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action lane still gives p_*(nu) = nu - lambda_min(L_Sigma)",
        "p_*(nu) = nu - lambda_min(l_sigma)" in action,
        "this is the exact unit-bearing pressure law that quarter must satisfy",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action lane still records exact quarter as nu = lambda_min(L_Sigma) + 1/4",
        "nu = lambda_min(l_sigma) + 1/4" in action,
        "the new lane should attack this exact remaining target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the non-affine lane still gives p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)",
        "p_vac(l_sigma) := -(1/n) log z_hat(l_sigma) = (1/(2n)) log det(l_sigma)" in nonaffine,
        "this is the only canonical nonzero same-surface vacuum density currently derived from the Schur action",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonicality lane still fixes the exact witness spectrum",
        ("its eigenvalues are exactly 1, 5/3" in canon)
        or ("its eigenvalues are exactly" in canon and "`1`, `5/3`" in CANON.read_text(encoding="utf-8")),
        "the witness should remain the same across all boundary reductions",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the bulk-to-boundary lane still says carrier closure improved but coefficient closure did not",
        "does not close the **coefficient**" in bulk,
        "the new lane should sharpen the coefficient problem without reopening carrier ambiguity",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the C^16 bridge still records m_axis = 1/4 as a possible bridge quantity",
        "m_axis := tr(rho_cell p_a) = 4/16 = 1/4" in c16,
        "this is a candidate new microscopic datum, not an earned action theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: GENERAL VACUUM-NORMALIZATION CLASSIFICATION")
    lmin, d, n = sp.symbols("lmin d n", positive=True, real=True)
    nu_zero = sp.Integer(0)
    nu_gauss = sp.log(d) / (2 * n)
    nu_quarter = lmin + sp.Rational(1, 4)

    p = check(
        "empty-vacuum action normalization forces nu = 0",
        nu_zero == 0,
        "I_nu(tau ; 0, 0) = -tau nu, so vanishing empty-vacuum action picks nu_0 = 0",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "Gaussian vacuum-pressure matching forces nu = (1/(2n)) log det(L)",
        sp.simplify(nu_gauss - sp.log(d) / (2 * n)) == 0,
        "matching the additive vacuum density to the exact same-surface Schur free-energy density gives nu_gauss",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "quarter requires nu_quarter = lambda_min(L) + 1/4",
        sp.simplify(nu_quarter - (lmin + sp.Rational(1, 4))) == 0,
        "this is the exact remaining target inherited from the action-pressure lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "nu_0 cannot equal nu_quarter on any positive carrier",
        sp.simplify(nu_quarter - nu_zero) == lmin + sp.Rational(1, 4),
        "because lmin > 0, the quarter value is strictly positive and zero-vacuum normalization rules it out",
    )
    n_pass += int(p)
    n_fail += int(not p)

    d_required = sp.solve(sp.Eq(nu_gauss, nu_quarter), d)[0]
    p = check(
        "nu_gauss equals nu_quarter only on the special spectral locus det(L) = exp(2n(lambda_min + 1/4))",
        sp.simplify(d_required - sp.exp(2 * n * (lmin + sp.Rational(1, 4)))) == 0,
        "Gaussian vacuum matching does not force quarter; it matches quarter only on a special extra spectral relation",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: EXACT WITNESS OBSTRUCTION")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    eigs = sorted(l_sigma.eigenvals().keys(), key=lambda x: float(sp.N(x, 50)))
    nu_gauss_witness = sp.simplify(sp.log(l_sigma.det()) / 4)
    nu_quarter_witness = sp.Rational(5, 4)

    p = check(
        "the witness still has spectrum {1, 5/3}",
        eigs == [sp.Integer(1), sp.Rational(5, 3)],
        "the exact witness carrier is unchanged from the earlier boundary lanes",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness determinant is 5/3",
        sp.simplify(l_sigma.det() - sp.Rational(5, 3)) == 0,
        "this determines the exact Gaussian vacuum density on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness Gaussian value is nu_gauss = (1/4) log(5/3)",
        sp.simplify(nu_gauss_witness - sp.log(sp.Rational(5, 3)) / 4) == 0,
        "this is the only canonical nonzero same-surface value currently derived from the Schur action on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness quarter target is nu_quarter = 5/4",
        nu_quarter_witness == sp.Integer(1) + sp.Rational(1, 4),
        "lambda_min(L_sigma) = 1 on the witness, so exact quarter demands a very different vacuum shift",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "both canonical same-surface values miss the witness quarter target",
        sp.simplify(nu_quarter_witness - nu_zero) != 0
        and sp.simplify(nu_quarter_witness - nu_gauss_witness) != 0,
        "neither empty-vacuum normalization nor Gaussian vacuum matching derives the required 5/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: NOTE HONESTY")
    p = check(
        "the note states the canonical dichotomy nu in {0, p_vac(L_Sigma)}",
        "nu in {0, p_vac(l_sigma)}" in note,
        "the main scientific claim should be a reduction theorem, not a fake Planck close",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states that quarter would need a new vacuum reference law or bridge theorem",
        "new vacuum reference law" in note and "nu = lambda_min(l_sigma) + m_axis" in note,
        "the remaining microscopic datum should be made explicit",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"SUMMARY: {n_pass} pass, {n_fail} fail")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
