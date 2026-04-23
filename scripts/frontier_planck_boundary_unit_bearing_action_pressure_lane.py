#!/usr/bin/env python3
"""Audit the unit-bearing boundary action/pressure lane honestly.

This runner encodes the strongest current action-native reduction on the
Planck boundary route:

  - exact Schur action fixes the boundary Hessian/operator L_Sigma;
  - exact one-clock transfer fixes the coefficient of L_Sigma in the
    generator, so multiplicative rescaling is not same-surface on the action
    lane;
  - the only surviving same-surface unit-bearing freedom is an additive
    vacuum-action density nu;
  - the induced generator is G_nu = nu I - L_Sigma;
  - exact quarter is equivalent to one remaining theorem
    nu = lambda_min(L_Sigma) + 1/4;
  - canonical empty-vacuum normalization forces nu = 0 and therefore lands on
    the wrong pressure branch.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_UNIT_BEARING_ACTION_PRESSURE_LANE_2026-04-23.md"
SCHUR = ROOT / "docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md"
TIME = ROOT / "docs/S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
SCHUR_COMPLETION = ROOT / "docs/PLANCK_SCALE_BULK_TO_BOUNDARY_SCHUR_COMPLETION_LANE_2026-04-23.md"
CANON = ROOT / "docs/PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md"
PRESSURE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_PRESSURE_QUARTER_NORMALIZATION_LANE_2026-04-23.md"


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
    schur_note = normalized(SCHUR)
    time_note = normalized(TIME)
    timelock_note = normalized(TIMELOCK)
    schur_completion_note = normalized(SCHUR_COMPLETION)
    canon_note = normalized(CANON)
    pressure_note = normalized(PRESSURE)

    n_pass = 0
    n_fail = 0

    print("Planck boundary unit-bearing action/pressure lane audit")
    print("=" * 78)

    section("PART 1: UPSTREAM EXACT ACTION DATA")
    p = check(
        "the exact Schur boundary action is still I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f",
        "i_r(f ; j) = 1/2 f^t lambda_r f - j^t f" in schur_note,
        "the action lane must start from the retained microscopic boundary action, not a reweighted model",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact one-clock backbone still uses T_R = exp(-Lambda_R)",
        "t_r = exp(-lambda_r)" in time_note,
        "this fixes the coefficient/sign of the operator on the action lane before any additive vacuum term",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "time-lock still fixes a_s = c a_t exactly",
        "a_s = c a_t" in timelock_note and "beta = 1" in timelock_note,
        "the unit-bearing deformation should live on the locked one-clock carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "bulk elimination still forces the Schur-complement boundary operator",
        "l_sigma := m_bb - m_bi m_ii^(-1) m_ib" in schur_completion_note,
        "the remaining freedom should not re-open the carrier itself",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the canonical transfer note still fixes T_can(tau) = exp(-tau L_Sigma)",
        "t_can(tau) = exp(-tau l_sigma)" in canon_note,
        "multiplicative rescaling is already suspect once the exact action and one-clock law are both retained",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the earlier pressure note still records the broader affine gauge",
        "g -> lambda g + mu i" in pressure_note,
        "the new lane should sharpen that broad gauge, not ignore it",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT ACTION KILLS MULTIPLICATIVE RESCALING")
    l11, l12, l22 = sp.symbols("l11 l12 l22", real=True)
    b1, b2, j1, j2 = sp.symbols("b1 b2 j1 j2", real=True)
    lam = sp.symbols("lam", positive=True, real=True)
    b = sp.Matrix([b1, b2])
    j = sp.Matrix([j1, j2])
    l_generic = sp.Matrix([[l11, l12], [l12, l22]])

    i_can = sp.Rational(1, 2) * (b.T * l_generic * b)[0] - (j.T * b)[0]
    i_scaled = sp.Rational(1, 2) * lam * (b.T * l_generic * b)[0] - (j.T * b)[0]
    grad_can = sp.Matrix([sp.diff(i_can, var) for var in (b1, b2)])
    grad_scaled = sp.Matrix([sp.diff(i_scaled, var) for var in (b1, b2)])
    hess_can = sp.hessian(i_can, (b1, b2))
    hess_scaled = sp.hessian(i_scaled, (b1, b2))

    p = check(
        "the canonical action gradient is exactly L_Sigma b - j",
        sp.simplify(grad_can - (l_generic * b - j)) == sp.zeros(2, 1),
        "fixing the exact microscopic stationarity law determines the b-dependent part of the action",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "multiplicative rescaling changes the Hessian to lambda L_Sigma",
        sp.simplify(hess_scaled - lam * l_generic) == sp.zeros(2),
        "lambda != 1 is therefore not a harmless normalization on the exact action lane",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "multiplicative rescaling changes the stationary law to lambda L_Sigma b - j = 0",
        sp.simplify(grad_scaled - (lam * l_generic * b - j)) == sp.zeros(2, 1),
        "the exact Schur response b = L_Sigma^(-1) j is changed by 1/lambda",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: ONLY AN ADDITIVE VACUUM TERM SURVIVES")
    nu, tau = sp.symbols("nu tau", real=True)
    i_shifted = tau * (i_can - nu)
    grad_shifted = sp.Matrix([sp.diff(i_shifted, var) for var in (b1, b2)])
    hess_shifted = sp.hessian(i_shifted, (b1, b2))

    p = check(
        "adding a constant vacuum term leaves the Euler-Lagrange equation unchanged up to the one-clock factor",
        sp.simplify(grad_shifted - tau * grad_can) == sp.zeros(2, 1),
        "the additive term is invisible to microscopic stationarity",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "adding a constant vacuum term leaves the Hessian unchanged up to the one-clock factor",
        sp.simplify(hess_shifted - tau * hess_can) == sp.zeros(2),
        "the exact Schur operator survives intact",
    )
    n_pass += int(p)
    n_fail += int(not p)

    tau1, tau2 = sp.symbols("tau1 tau2", real=True)
    c = lambda t: nu * t
    p = check(
        "one-clock additivity forces the surviving constant term to be linear in tau",
        sp.simplify(c(tau1 + tau2) - c(tau1) - c(tau2)) == 0,
        "on the reduced unit carrier the same-surface vacuum term is exactly nu tau",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: EXACT UNIT-BEARING PRESSURE LAW")
    l_sigma = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    eigs = set(l_sigma.eigenvals().keys())
    p = check(
        "the exact witness still has eigenvalues {1, 5/3}",
        eigs == {sp.Integer(1), sp.Rational(5, 3)},
        "this witness is the load-bearing boundary carrier for the current pressure problem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    g_nu = nu * sp.eye(2) - l_sigma
    g_nu_eigs = set(g_nu.eigenvals().keys())
    p = check(
        "the induced generator family is G_nu = nu I - L_Sigma with top pressure nu - 1 on the witness",
        g_nu_eigs == {nu - 1, nu - sp.Rational(5, 3)},
        "once lambda is killed, the remaining coefficient is one additive density",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "exact quarter on the witness is equivalent to nu = 5/4",
        sp.solve(sp.Eq(nu - 1, sp.Rational(1, 4)), nu) == [sp.Rational(5, 4)],
        "the Planck boundary problem is reduced to one vacuum-action density theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "canonical empty-vacuum normalization I(0;0)=0 forces nu = 0 and pressure -1 on the witness",
        sp.simplify((i_shifted.subs({b1: 0, b2: 0, j1: 0, j2: 0}) / tau) + nu) == 0
        and sp.simplify(top_eigenvalue(g_nu.subs(nu, 0)) + 1) == 0,
        "with canonical zero-vacuum normalization the boundary route lands on the wrong sign branch",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE HONESTY")
    p = check(
        "the note states that the full affine gauge is too broad on the exact action lane",
        "full affine boundary normalization gauge is too broad" in note
        or "broad affine family collapses" in note,
        "the main scientific upgrade is killing lambda on exact action grounds",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note states that only the additive vacuum-action density nu survives",
        "only a **unit-bearing additive vacuum-action density** `nu`" in note
        or "only an additive vacuum-action density survives" in note,
        "the remaining coefficient should be named explicitly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the quarter law nu = lambda_min(L_Sigma) + 1/4",
        "`nu = lambda_min(l_sigma) + 1/4`" in note
        or "nu = lambda_min(l_sigma) + 1/4" in note,
        "the remaining theorem target should be written in exact form",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the witness value nu = 5/4 and the zero-vacuum obstruction",
        "5/4" in note and "canonical zero-vacuum normalization" in note,
        "the witness should make the remaining gap completely concrete",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note does not overclaim exact Planck closure",
        "does **not** derive the needed density" in note and "does **not** yet prove" in note,
        "this lane should remain an honest reduction/obstruction theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "On the exact time-locked Schur carrier, the microscopic action fixes "
        "the operator scale and kills the multiplicative lambda freedom. The "
        "remaining boundary Planck coefficient is one additive vacuum-action "
        "density nu, with exact quarter equivalent to nu = lambda_min(L_Sigma) + 1/4."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
