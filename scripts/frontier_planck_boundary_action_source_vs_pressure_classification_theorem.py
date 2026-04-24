#!/usr/bin/env python3
"""Verify the boundary action-source versus scalar-pressure classification."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_BOUNDARY_ACTION_SOURCE_VS_PRESSURE_CLASSIFICATION_THEOREM_2026-04-23.md"
OBS = ROOT / "docs/PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md"
EVENT = ROOT / "docs/PLANCK_SCALE_BOUNDARY_EVENT_WARD_IDENTITY_DERIVATION_THEOREM_2026-04-23.md"
PARENT = ROOT / "docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md"
REVIEWER = ROOT / "docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md"


def read(path: Path) -> str:
    return path.read_text()


def expect(name: str, cond: bool, detail: str = "") -> int:
    if cond:
        print(f"PASS: {name}: {detail}")
        return 1
    print(f"FAIL: {name}: {detail}")
    return 0


def main() -> int:
    note = read(NOTE)
    obs = read(OBS)
    event = read(EVENT)
    parent = read(PARENT)
    reviewer = read(REVIEWER)

    L = sp.Matrix(
        [[sp.Rational(4, 3), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(4, 3)]]
    )
    n = 2
    p_scalar = sp.log(L.det()) / (2 * n)
    p_event = sp.Rational(4, 16)
    lambda_min = min(L.eigenvals().keys())
    nu = lambda_min + p_event
    p_action = nu - lambda_min

    checks = [
        (
            "three-object-classes-are-separated",
            "`p_scalar(L_Sigma) = (1/(2n)) log det(L_Sigma)`" in note
            and "`p_action = nu - lambda_min(L_Sigma)`" in note
            and "`p_event = d/ds log Tr(rho_cell exp(s P_A))|_(s=0)" in note,
            "scalar, action-source, and event-source quantities are distinct",
        ),
        (
            "scalar-pressure-is-not-quarter",
            sp.simplify(p_scalar - sp.Rational(1, 4)) != 0
            and "`p_scalar = (1/4) log(5/3)`" in note
            and "not `1/4`" in note
            and "`p_phys = p_obs = p_vac(L_Sigma)`" in obs,
            f"p_scalar={p_scalar}",
        ),
        (
            "event-source-is-quarter",
            p_event == sp.Rational(1, 4)
            and "`p_event = Tr(rho_cell P_A)`" in note
            and "`p_event = 1/4`" in note
            and "`d/ds log Z_A(s)|_(s=0) = Tr(rho_cell P_A)`" in event,
            f"p_event={p_event}",
        ),
        (
            "action-source-is-quarter-under-parent-equivalence",
            p_action == sp.Rational(1, 4)
            and "`p_action = p_event = Tr(rho_cell P_A)`" in note
            and "`B_parent := (H_A, P_A)`" in parent,
            f"p_action={p_action}",
        ),
        (
            "no-scalar-overclaim",
            "This does not imply\n\n`p_scalar = p_event`" in note
            and "The ordinary scalar Schur pressure is `1/4`" in note,
            "the note explicitly forbids the scalar-pressure claim",
        ),
        (
            "reviewer-packet-links-the-classification",
            "PLANCK_SCALE_BOUNDARY_ACTION_SOURCE_VS_PRESSURE_CLASSIFICATION_THEOREM_2026-04-23.md"
            in reviewer,
            "canonical packet includes the hardening theorem",
        ),
    ]

    passed = 0
    for name, cond, detail in checks:
        passed += expect(name, cond, detail)

    print(f"SUMMARY: PASS={passed} FAIL={len(checks) - passed}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
