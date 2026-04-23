#!/usr/bin/env python3
"""Audit the three proposed routes for deriving the boundary density."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_DENSITY_THREE_MECHANISM_AUDIT_2026-04-23.md"
PRIMITIVE = ROOT / "docs/PLANCK_SCALE_PRIMITIVE_BOUNDARY_ACTION_UNIT_REDUCTION_THEOREM_2026-04-23.md"
PHASE = ROOT / "docs/PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md"
VACUUM = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DENSITY_THEOREM_LANE_2026-04-23.md"
DECOMP = ROOT / "docs/PLANCK_SCALE_BOUNDARY_VACUUM_ACTION_DECOMPOSITION_LANE_2026-04-23.md"
OBS = ROOT / "docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def read(path: Path) -> str:
    return path.read_text()


def main() -> int:
    note = read(NOTE)
    primitive = read(PRIMITIVE)
    phase = read(PHASE)
    vacuum = read(VACUUM)
    decomp = read(DECOMP)
    obs = read(OBS)

    banned_terms = ["P1", "Axiom Extension", "GSI", "Gravity-Sector Identification"]

    tau, nu, j1, j2 = sp.symbols("tau nu j1 j2", real=True)
    j = sp.Matrix([j1, j2])
    L = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    W0 = sp.Rational(1, 2) * (j.T * L.inv() * j)[0]
    Wnu = tau * nu + W0
    grad_same = sp.Matrix([sp.diff(Wnu - W0, x) for x in (j1, j2)]) == sp.zeros(2, 1)
    hess_same = sp.hessian(Wnu - W0, (j1, j2)) == sp.zeros(2)

    evals = sorted(L.eigenvals().keys())
    lambda_min = evals[0]
    det_l = L.det()
    p_vac = sp.log(det_l) / 4
    nu_quarter = lambda_min + sp.Rational(1, 4)
    delta_quarter = nu_quarter - lambda_min
    m_axis = Fraction(4, 16)

    q_over_eps_required = sp.Rational(1, 1) / (8 * sp.pi)
    a2_over_lp2 = 8 * sp.pi * q_over_eps_required

    c_cell = Fraction(1, 4)
    area_normalized = 4 * c_cell

    checks = [
        (
            "note-avoids-project-shorthand",
            all(term not in note for term in banned_terms),
            "reviewer-facing density audit should not depend on branch-local shorthand",
        ),
        (
            "witness-algebra-is-exact",
            evals == [sp.Integer(1), sp.Rational(5, 3)]
            and det_l == sp.Rational(5, 3)
            and nu_quarter == sp.Rational(5, 4)
            and delta_quarter == sp.Rational(1, 4)
            and m_axis == Fraction(1, 4)
            and "`nu = 5/4`" in note
            and "`delta = m_axis`" in note,
            f"lambda_min={lambda_min}, det={det_l}, nu_quarter={nu_quarter}",
        ),
        (
            "ward-source-response-does-not-see-nu",
            grad_same
            and hess_same
            and "`W_nu(j) := log Z_nu(j) = tau nu + W_0(j)`" in note
            and "they cannot determine `nu`" in note,
            "source derivatives erase additive vacuum density",
        ),
        (
            "ward-normalizations-miss-quarter",
            p_vac != sp.Rational(5, 4)
            and "empty-vacuum action normalization chooses `nu = 0`" in note
            and "`nu = p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`" in note
            and "not `5/4`" in note
            and "nu in {0, p_vac(L_Sigma)}" in vacuum,
            f"p_vac={p_vac}",
        ),
        (
            "phase-route-reduces-to-ratio-not-closure",
            sp.simplify(a2_over_lp2 - 1) == 0
            and sp.simplify(q_over_eps_required - sp.Rational(1, 1) / (8 * sp.pi)) == 0
            and "`a^2 / l_P^2 = 8 pi q_* / eps_*`" in note
            and "`q_* / eps_* = 1 / (8 pi)`" in note
            and "does **not** yet force the exact coefficient `a = l_P`" in phase,
            f"required q/eps={q_over_eps_required}",
        ),
        (
            "phase-route-distinguishes-counting-from-phase",
            "`1/16` per primitive event" in note
            and "`4/16 = 1/4` for the axis-sector packet" in note
            and "not an action\nphase quantum and a geometric defect quantum" in note,
            "C^16 counting numbers are not yet same-process phase/defect data",
        ),
        (
            "boundary-term-normalization-constants-accounted",
            area_normalized == 1
            and "`S_grav / k_B = A c_light^3 / (4 G hbar) = A / (4 l_P^2)`"
            in note
            and "`a^2 = 4 c_cell l_P^2 = l_P^2`" in note,
            "standard area/action law gives Planck only after carrier identification",
        ),
        (
            "boundary-term-route-remains-microscopic-proof-obligation",
            "Used before\nthat derivation, it is an explicit gravity normalization input" in note
            and "This note does not derive `nu = 5/4`" in primitive
            and "does not merely miss\n   quarter" in decomp,
            "microscopic boundary term still has to derive nu=lambda_min+m_axis",
        ),
        (
            "scalar-observable-negative-control-retained",
            "p_phys = p_obs = p_vac(L_Sigma)" in obs
            and "quarter must come from a new non-scalar / block-selecting bridge" in obs
            and "not yet derived by the current Ward,\n> phase, or boundary-term machinery" in note,
            "existing scalar observable principle selects p_vac, not quarter",
        ),
        (
            "exact-new-theorem-target-is-sharp",
            "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A)`" in note
            and "`delta = m_axis`" in note
            and "Boundary Ward identity" in note
            and "Action-phase theorem" in note
            and "Microscopic boundary-term theorem" in note,
            "the remaining closure target is a single residual/readout law",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
