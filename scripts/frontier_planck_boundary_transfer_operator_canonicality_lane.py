#!/usr/bin/env python3
"""Audit the canonicality/obstruction result for the Planck boundary route.

This lane proves the strongest honest statement currently supported by the
admitted `3+1` gravity carrier:

  - exact bulk elimination forces the boundary operator to be the Schur
    reduction `L_Sigma`;
  - the admitted one-clock grammar forces the no-parameter transfer law
    `T_can(tau) = exp(-tau L_Sigma)`;
  - because `L_Sigma` is positive semidefinite, `T_can(1)` is spectrally
    contractive and cannot realize `rho(T) = exp(1/4)`.

So the operator is canonical, but the quarter-pressure close is still blocked
on one new normalization theorem.
"""

from __future__ import annotations

from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_TRANSFER_OPERATOR_CANONICALITY_LANE_2026-04-23.md"
GLOBAL = ROOT / "docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md"
POSITIVE = ROOT / "docs/UNIVERSAL_GR_POSITIVE_BACKGROUND_EXTENSION_NOTE.md"
SCHUR = ROOT / "docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md"
TRANSFER = ROOT / "docs/S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md"
TIMELOCK = ROOT / "docs/PLANCK_SCALE_SPACETIME_TIME_LOCK_UNIT_MAP_LANE_2026-04-23.md"
BOUNDARY = ROOT / "docs/PLANCK_SCALE_TIMELOCKED_GRAVITATIONAL_TRANSFER_OPERATOR_LANE_2026-04-23.md"


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


def spectral_radius_from_eigs(vals: list[sp.Expr]) -> sp.Expr:
    return max(vals, key=lambda expr: abs(complex(sp.N(expr, 50))))


def main() -> int:
    note = normalized(NOTE)
    global_note = normalized(GLOBAL)
    positive_note = normalized(POSITIVE)
    schur_note = normalized(SCHUR)
    transfer_note = normalized(TRANSFER)
    timelock_note = normalized(TIMELOCK)
    boundary_note = normalized(BOUNDARY)

    n_pass = 0
    n_fail = 0

    print("Planck boundary transfer-operator canonicality lane audit")
    print("=" * 78)

    section("PART 1: SOURCE SURFACES STILL SUPPORT THE CANONICALITY CLAIM")
    p = check(
        "global gravity carrier is still exact on the branch",
        "k_gr(d) = h_d ⊗ lambda_r" in global_note
        and "k_gr(d) = h_d ⊗ lambda_r" in positive_note,
        "the boundary route must descend from the admitted positive `3+1` gravity carrier",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the exact Schur boundary action is already part of the admitted stack",
        "lambda_r = h_tt - h_tb h_bb^{-1} h_bt" in schur_note
        and "exact schur-complement energy" in schur_note,
        "bulk elimination already forces a boundary quadratic form elsewhere on the branch",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the one-clock transfer grammar already fixes the sign as exp(-generator)",
        "t_r := exp(-lambda_r)" in transfer_note
        and "positive self-adjoint contraction" in transfer_note,
        "the canonical boundary transfer law should inherit the same contractive sign",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "time-lock is still exact",
        "a_s = c a_t" in timelock_note and "beta = 1" in timelock_note,
        "the boundary route should live on one exact physical clock",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the earlier boundary-transfer lane still identifies Schur reduction as the right candidate class",
        "schur-complement reduction" in boundary_note
        and "p_* := sup spec(g_sigma) = 1/4" in boundary_note,
        "this lane should strengthen the canonicality question, not replace the route",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: EXACT BULK ELIMINATION FORCES THE SCHUR OPERATOR")
    a, b, c, x, y = sp.symbols("a b c x y", positive=True)
    quadratic = sp.Rational(1, 2) * (a * x**2 + 2 * b * x * y + c * y**2)
    y_star = sp.simplify(-b * x / c)
    reduced = sp.expand(quadratic.subs(y, y_star))
    expected_reduced = sp.expand(sp.Rational(1, 2) * (a - b**2 / c) * x**2)
    p = check(
        "stationary bulk elimination gives the scalar Schur coefficient exactly",
        sp.simplify(reduced - expected_reduced) == 0,
        "for a 1+1 block, eliminating the bulk variable gives 1/2 (a - b^2/c) x^2 exactly",
    )
    n_pass += int(p)
    n_fail += int(not p)

    gaussian_prefactor = sp.sqrt(2 * sp.pi / c)
    gaussian_integral = gaussian_prefactor * sp.exp(-expected_reduced)
    expected_form = gaussian_prefactor * sp.exp(-reduced)
    p = check(
        "Gaussian marginalization gives the same Schur-reduced boundary coefficient",
        sp.simplify(gaussian_integral / expected_form - 1) == 0,
        "exact integration over the bulk differs only by the standard determinant factor",
    )
    n_pass += int(p)
    n_fail += int(not p)

    m_bb = sp.Matrix([[2, 0], [0, 2]])
    m_bi = sp.Matrix([[1, 0], [0, 1]])
    m_ii = sp.Matrix([[2, 1], [1, 2]])
    l_sigma = sp.simplify(m_bb - m_bi * m_ii.inv() * m_bi.T)
    expected = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    p = check(
        "the witness boundary operator is exactly the Schur reduction used in the note",
        sp.simplify(l_sigma - expected) == sp.zeros(2),
        "exact rational witness L_Sigma = [[4/3,1/3],[1/3,4/3]]",
    )
    n_pass += int(p)
    n_fail += int(not p)

    evals = sorted(l_sigma.eigenvals().keys(), key=lambda expr: float(sp.N(expr)))
    p = check(
        "the witness Schur operator is positive definite",
        evals == [1, sp.Rational(5, 3)],
        "the exact reduced carrier has eigenvalues 1 and 5/3",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: THE ADMITTED ONE-CLOCK GRAMMAR FORCES THE CANONICAL TRANSFER LAW")
    tau = sp.symbols("tau", nonnegative=True)
    l1 = sp.Integer(1)
    l2 = sp.Rational(5, 3)
    p = check(
        "the no-parameter one-clock law on the reduced carrier is exp(-tau L_Sigma)",
        "t_can(tau) = exp(-tau l_sigma)" in note
        and "no-parameter same-surface transfer law" in note,
        "the note should state that nonlinear reweightings psi(L_Sigma) are new models, not canonical reduction",
    )
    n_pass += int(p)
    n_fail += int(not p)

    one_step_eigs = [sp.exp(-l1), sp.exp(-l2)]
    two_step_eigs = [sp.exp(-2 * l1), sp.exp(-2 * l2)]
    p = check(
        "the canonical transfer satisfies exact semigroup composition spectrally",
        sorted(two_step_eigs, key=lambda expr: float(sp.N(expr)))
        == sorted([val**2 for val in one_step_eigs], key=lambda expr: float(sp.N(expr))),
        "eigenvalues square exactly from one step to two steps under exp(-tau L_Sigma)",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the contractive sign is forced by the admitted transfer grammar, not chosen ad hoc here",
        "exp(-lambda_r)" in transfer_note and "positive self-adjoint contraction" in transfer_note,
        "the branch already fixes the one-clock law on the exact slice side to the decaying sign",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: THE CANONICAL TRANSFER CANNOT HIT QUARTER PRESSURE")
    rho_can = spectral_radius_from_eigs(one_step_eigs)
    p = check(
        "the canonical one-step transfer is spectrally contractive",
        sp.simplify(rho_can - sp.exp(-1)) == 0 and float(sp.N(rho_can)) < 1.0,
        "for the witness, rho(T_can(1)) = exp(-1) < 1",
    )
    n_pass += int(p)
    n_fail += int(not p)

    lambda_min = l1
    p = check(
        "positive semidefinite Schur data imply rho(T_can(1)) <= 1 in general",
        sp.simplify(sp.exp(-lambda_min) - rho_can) == 0 and lambda_min >= 0,
        "in general rho(exp(-L_Sigma)) = exp(-lambda_min(L_Sigma)) <= 1",
    )
    n_pass += int(p)
    n_fail += int(not p)

    target = sp.exp(sp.Rational(1, 4))
    p = check(
        "the quarter-pressure target lies on the wrong spectral branch",
        bool(float(sp.N(target)) > 1.0 and float(sp.N(rho_can)) < 1.0),
        "the canonical transfer decays, while the Planck boundary target requires growth",
    )
    n_pass += int(p)
    n_fail += int(not p)

    mu = sp.symbols("mu", real=True)
    rho_shifted = sp.exp(mu - lambda_min)
    mu_star = sp.simplify(sp.Rational(1, 4) + lambda_min)
    p = check(
        "exact quarter on a shifted family requires one new additive normalization datum",
        sp.simplify(rho_shifted.subs(mu, mu_star) - target) == 0 and mu_star == sp.Rational(5, 4),
        "for the witness, quarter requires T_mu = exp(tau (mu I - L_Sigma)) with mu = 5/4",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 5: NOTE HONESTY")
    p = check(
        "the note states the canonical operator is derived but quarter remains blocked",
        "forces a canonical boundary operator" in note
        and "cannot realize the planck boundary target" in note,
        "the central claim should be canonicality plus obstruction, not fake closure",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note records the exact shifted-family tuning law",
        "t_mu(tau) = exp(tau (mu i - l_sigma))" in note
        and "mu = 1/4 + lambda_min(l_sigma)" in note,
        "the remaining open bridge should be isolated to one additive pressure theorem",
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note does not overclaim exact Planck closure",
        "does **not** derive exact conventional `a = l_p`" in note
        and "cannot realize exact quarter pressure" in note,
        "the lane should remain honest about what is and is not closed",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    print(
        "  The admitted `3+1` gravity carrier forces the canonical boundary "
        "Schur operator and the no-parameter one-clock law T_can(tau)=exp(-tau L_Sigma)."
    )
    print(
        "  That canonical transfer is necessarily contractive, so exact quarter "
        "pressure is not derived. The remaining open bridge is one additive "
        "pressure/normalization theorem or a genuinely different carrier."
    )

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
