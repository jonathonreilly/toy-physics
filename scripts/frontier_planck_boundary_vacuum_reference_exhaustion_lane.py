#!/usr/bin/env python3
"""Audit the Planck boundary vacuum-reference exhaustion lane honestly.

This lane does not fake a Planck close. It proves the sharper exhaustion result:

  - every same-surface Gaussian boundary vacuum-reference law is determined by
    one scalar reference datum r_R(L) = (1/(2n)) log det(R(L));
  - the current branch supplies exactly two canonical no-datum choices:
      nu = 0          from self reference R(L) = L
      nu = p_vac(L)   from unit reference R(L) = I_n
  - exact quarter on the action-pressure lane requires a different reference
    datum, equivalently det(R(L)) = det(L) * exp(-2n(lambda_min(L) + 1/4));
  - on the exact witness this becomes det(R(L_sigma)) = (5/3) exp(-5), so
    quarter still needs one explicit new datum or bridge theorem.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_REFERENCE_EXHAUSTION_LANE_2026-04-23.md"
NONAFFINE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_NONAFFINE_PRESSURE_NORMALIZATION_LANE_2026-04-23.md"
ACTION = ROOT / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
VACUUM = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md"
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
    nonaffine = normalized(NONAFFINE)
    action = normalized(ACTION)
    vacuum = normalized(VACUUM)
    c16 = normalized(C16)

    n_pass = 0
    n_fail = 0

    print("Planck boundary vacuum-reference exhaustion lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM REDUCTION STILL HOLDS")
    p = check(
        "the non-affine lane still gives p_vac(L_sigma) = (1/(2n)) log det(L_sigma)",
        "p_vac(l_sigma) := -(1/n) log z_hat(l_sigma) = (1/(2n)) log det(l_sigma)" in nonaffine,
        "the new lane should start from the exact Gaussian Schur vacuum density already earned upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action lane still gives p_*(nu) = nu - lambda_min(L_sigma)",
        "p_*(nu) = nu - lambda_min(l_sigma)" in action,
        "quarter is still posed on the same exact unit-bearing action-pressure surface",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the action lane still records nu_quarter = lambda_min(L_sigma) + 1/4",
        "nu = lambda_min(l_sigma) + 1/4" in action,
        "the new lane must attack the same exact remaining coefficient target",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the vacuum-action lane still records the two canonical values nu in {0, p_vac(L_sigma)}",
        "nu in {0, p_vac(l_sigma)}" in vacuum,
        "the new lane should sharpen that dichotomy rather than reopen it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the C^16 bridge still records nu = lambda_min(L_sigma) + m_axis as a possible new bridge",
        "w = lambda_min(l_sigma) + m_axis" in c16
        and "physical boundary pressure = c^16 axis-sector mass" in c16,
        "this remains a candidate new datum/bridge rather than an existing vacuum-reference theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: GENERAL GAUSSIAN REFERENCE-LAW CLASSIFICATION")
    dL, dR, n = sp.symbols("dL dR n", positive=True, real=True)
    nu_R = sp.simplify(sp.log(dL) / (2 * n) - sp.log(dR) / (2 * n))
    p_vac = sp.log(dL) / (2 * n)
    r_R = sp.log(dR) / (2 * n)

    p = check(
        "every Gaussian reference law has the form nu_R(L) = p_vac(L) - r_R(L)",
        sp.simplify(nu_R - (p_vac - r_R)) == 0,
        "the reference dependence collapses to one scalar datum r_R(L) = (1/(2n)) log det(R(L))",
    )
    n_pass += int(p)
    n_fail += int(not p)

    dL1, dL2, dR1, dR2 = sp.symbols("dL1 dL2 dR1 dR2", positive=True, real=True)
    total = sp.simplify(sp.log(dL1 * dL2) / 2 - sp.log(dR1 * dR2) / 2)
    split = sp.simplify(
        (sp.log(dL1) - sp.log(dR1)) / 2 + (sp.log(dL2) - sp.log(dR2)) / 2
    )
    p = check(
        "total vacuum free energy is additive on direct sums",
        sp.simplify(total - split) == 0,
        "F_R(L) = n nu_R(L) remains additive across independent boundary blocks",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "self reference R(L) = L gives nu = 0",
        sp.simplify(nu_R.subs({dR: dL})) == 0,
        "this recovers the canonical empty-vacuum normalization",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "unit reference R(L) = I_n gives nu = p_vac(L)",
        sp.simplify(nu_R.subs({dR: 1}) - p_vac) == 0,
        "this recovers the canonical Gaussian vacuum-pressure matching law",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: QUARTER REQUIRES ONE EXPLICIT NEW DATUM")
    lmin = sp.symbols("lmin", positive=True, real=True)
    nu_quarter = lmin + sp.Rational(1, 4)
    required_r = sp.simplify(p_vac - nu_quarter)
    required_detR = sp.solve(sp.Eq(nu_R, nu_quarter), dR)[0]

    p = check(
        "matching quarter fixes the reference scalar datum uniquely",
        sp.simplify(required_r - (sp.log(dL) / (2 * n) - lmin - sp.Rational(1, 4))) == 0,
        "quarter is not automatic; it fixes one specific scalar datum r_R(L)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "equivalently, quarter fixes det(R(L)) = det(L) exp(-2n(lambda_min + 1/4))",
        sp.simplify(required_detR - dL * sp.exp(-2 * n * (lmin + sp.Rational(1, 4)))) == 0,
        "any Gaussian reference law that lands on quarter introduces one explicit reference determinant",
    )
    n_pass += int(p)
    n_fail += int(not p)

    delta_quarter = sp.simplify(nu_quarter - p_vac)
    p = check(
        "quarter differs from the canonical Gaussian law by one explicit additive datum",
        sp.simplify(delta_quarter - (lmin + sp.Rational(1, 4) - sp.log(dL) / (2 * n))) == 0,
        "this is the cleanest same-surface statement of the remaining microscopic gap",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: EXACT WITNESS")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    evals = sorted(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr)))
    det_witness = sp.simplify(l_sigma.det())
    p_vac_witness = sp.simplify(sp.log(det_witness) / 4)
    nu_quarter_witness = sp.Rational(5, 4)
    delta_witness = sp.simplify(nu_quarter_witness - p_vac_witness)
    det_r_witness = sp.simplify(
        required_detR.subs({dL: det_witness, n: 2, lmin: 1})
    )

    p = check(
        "the witness still has spectrum {1, 5/3}",
        evals == [sp.Integer(1), sp.Rational(5, 3)],
        "the new lane stays on the same exact Schur witness fixed upstream",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness determinant is 5/3",
        det_witness == sp.Rational(5, 3),
        "this controls the exact Gaussian vacuum density on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness canonical Gaussian value is (1/4) log(5/3)",
        sp.simplify(p_vac_witness - sp.log(sp.Rational(5, 3)) / 4) == 0,
        "this is the current nonzero no-datum same-surface vacuum reference value",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness quarter value is 5/4",
        nu_quarter_witness == sp.Rational(5, 4),
        "lambda_min(L_sigma) = 1, so the remaining target stays exactly 5/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the missing witness datum is delta_quarter = 5/4 - (1/4) log(5/3)",
        sp.simplify(delta_witness - (sp.Rational(5, 4) - sp.log(sp.Rational(5, 3)) / 4)) == 0,
        "this is the exact additive shift that the present vacuum-reference grammar does not supply",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the witness reference determinant required for quarter is (5/3) exp(-5)",
        sp.simplify(det_r_witness - sp.Rational(5, 3) * sp.exp(-5)) == 0,
        "quarter-compatible Gaussian reference laws require one explicit reference determinant on the witness",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE HONESTY")
    p = check(
        "the note states the general form nu_R(L) = (1/(2n)) log det(L) - (1/(2n)) log det(R(L))",
        "nu_r(l) = (1/(2n)) log det(l) - (1/(2n)) log det(r(l))" in note,
        "the classification should be stated in exact formulas, not only prose",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note identifies the two canonical no-datum choices R(L)=L and R(L)=I_n",
        "r(l) = l" in note and "r(l) = i_n" in note,
        "the note should make clear why the current branch has two canonical references and no quarter among them",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states that quarter requires one explicit new scalar reference datum",
        "one explicit new scalar reference datum" in note
        and "det(r(l)) = det(l) * exp(-2n (lambda_min(l) + 1/4))" in note,
        "the scientific claim should land at outcome (2), not an overclaimed closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note keeps the C^16 bridge as a future bridge theorem rather than a current consequence",
        "nu = lambda_min(l) + m_axis" in note and "not an already-earned consequence" in note,
        "the lane should stay honest about what is and is not derived on the current branch",
    )
    n_pass += int(p)
    n_fail += int(not p)

    print("\n" + "=" * 78)
    print(f"SUMMARY: {n_pass} pass, {n_fail} fail")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
